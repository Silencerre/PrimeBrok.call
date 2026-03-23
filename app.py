# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Нікіта Калькулятор", layout="wide", page_icon="🚗")

st.title("Нікіта Калькулятор — імпорт авто з США")
st.caption("Версія, максимально близька до твого excel-файлу")

# ────────────────────────────────────────────────
# Завантаження excel-файлу
uploaded = st.file_uploader(
    "Завантаж свій файл Нікіта Калькулятор.xlsx (або (1), (2) тощо)",
    type=["xlsx", "xls"],
    help="Потрібні аркуші: TOW та Freight1"
)

if not uploaded:
    st.info("Завантаж файл → калькулятор запрацює")
    st.stop()

# ────────────────────────────────────────────────
# Читання аркушів
@st.cache_data(show_spinner="Читаємо TOW та Freight...")
def load_sheets(file):
    try:
        tow = pd.read_excel(file, sheet_name="TOW", header=0)
        freight = pd.read_excel(file, sheet_name="Freight1", header=0)
        return tow, freight
    except Exception as e:
        st.error(f"Помилка читання файлу: {e}")
        st.stop()

tow_df, freight_df = load_sheets(uploaded)

# ────────────────────────────────────────────────
# Обробка TOW (робимо словник локація → порт → ціна)
tow_dict = {}
ports = ["NJ", "GA", "TX", "CA", "WA"]

for _, row in tow_df.iterrows():
    loc = str(row.get("Loaction", "")).strip()
    if not loc or loc == "nan":
        continue
    tow_dict[loc] = {}
    for p in ports:
        val = row.get(p)
        if pd.notna(val) and str(val).strip().lower() not in ["error", ""]:
            try:
                tow_dict[loc][p] = float(val)
            except:
                tow_dict[loc][p] = None
        else:
            tow_dict[loc][p] = None

# ────────────────────────────────────────────────
# Обробка Freight (робимо словник порт UA → порт US → тип → ціна)
freight_dict = {}
ua_ports_list = []

for _, row in freight_df.iterrows():
    ua_port = str(row.iloc[0]).strip()
    if ua_port in ["Constanta", "Odesa", "Klaipeda"]:
        ua_ports_list.append(ua_port)
        freight_dict[ua_port] = {}
        for col_idx, us_port in enumerate(["NJ", "GA", "TX", "CA", "WA"][:len(row)-1]):
            if pd.notna(row.iloc[col_idx+1]):
                try:
                    val = float(row.iloc[col_idx+1])
                    if val > 0:
                        freight_dict[ua_port][us_port] = {}
                        # Заповнюємо типи (GAS, DIESEL, EV, HYB, GAS 3, ... MOTO)
                        # Це спрощено — краще взяти з перших рядків
                except:
                    pass

# Краще — вручну витягнути структуру (бо Freight1 має специфічний формат)
# Тут спрощена версія — якщо не працює, скинь мені перші 15 рядків Freight1 текстом

# ────────────────────────────────────────────────
# Інтерфейс
left, right = st.columns([5, 4])

with left:
    st.subheader("Основні дані")

    col1, col2 = st.columns(2)
    with col1:
        client = st.text_input("Клієнт")
        model = st.text_input("Модель + рік")
        vin = st.text_input("VIN")

    with col2:
        location = st.selectbox("Локація (TOW)", options=sorted(tow_dict.keys()) if tow_dict else ["Завантаж файл"])

    if location in tow_dict:
        avail_ports = {p: c for p, c in tow_dict[location].items() if c is not None}
        if avail_ports:
            us_port_str = st.selectbox("Порт США", [f"{p} — {c} $" for p,c in sorted(avail_ports.items(), key=lambda x:x[1])])
            us_port = us_port_str.split(" — ")[0]
            tow_price = avail_ports[us_port]
        else:
            st.warning("Немає доступних портів для цієї локації")
            us_port = None
            tow_price = 0
    else:
        us_port = None
        tow_price = 0

    ua_port = st.selectbox("Порт призначення", ["Constanta", "Odesa", "Klaipeda"])

    transport = st.radio("Тип", ["Авто", "Мотоцикл"], horizontal=True)

    if transport == "Авто":
        fuel = st.selectbox("Паливо", ["GAS", "DIESEL", "EV", "HYB"])
        container = st.selectbox("Завантаження", ["1 авто", "3 авто в контейнері", "2 місця (півконтейнера)"])
        if container == "1 авто":
            f_key = fuel
        elif container == "3 авто в контейнері":
            f_key = fuel + " 3"
        else:
            f_key = fuel + " 2"
    else:
        f_key = "MOTO"

with right:
    st.subheader("Витрати (змінювати можна)")

    col_a, col_b = st.columns(2)
    with col_a:
        auction = st.number_input("Збір аукціону", value=340)
        swift = st.number_input("Swift аукціон", value=121)
        insurance = st.number_input("Страхування", value=50)
    with col_b:
        storage = st.number_input("Storage", value=0)
        other = st.number_input("Інше", value=0)
        customs = st.number_input("Митні платежі", value=1720)
        paid = st.number_input("Вже сплачено (PAID)", value=0)

# ────────────────────────────────────────────────
if st.button("Розрахувати ALL IN", type="primary", use_container_width=True):
    if not us_port:
        st.error("Обери локацію та порт США")
    else:
        freight_price = "не знайдено"
        # Тут потрібно витягнути ціну з freight_df — це найскладніше місце
        # Якщо не виходить — скинь мені перші 30 рядків аркуша Freight1 текстом

        # Приклад заглушка
        freight_price = 9999  # <--- заміни на реальну логіку

        total_no_customs = tow_price + freight_price + auction + swift + insurance + storage + other
        total = total_no_customs + customs
        debt = total - paid

        st.success("Розрахунок готовий")

        st.markdown(f"""
        **TOW** ............ {tow_price:,.0f} $
        **Фрахт** ......... {freight_price} $
        **Аукціон+Swift+Страх** .. {auction + swift + insurance:,.0f} $
        **Storage + Інше** .. {storage + other:,.0f} $
        ────────────────────────────
        **Без мита** ...... {total_no_customs:,.0f} $
        **Мито** .......... {customs:,.0f} $
        **ALL IN** ........ **{total:,.0f} $**

        **Сплачено** ...... {paid:,.0f} $
        **До оплати** ..... **{debt:,.0f} $**
        """)

        st.code(f"""Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Клієнт: {client}
Модель: {model}
VIN: {vin}
Локація: {location} → {us_port}
Порт UA: {ua_port}
Тип: {transport} {f_key if transport=='Авто' else ''}

TOW: {tow_price}$
Фрахт: {freight_price}$
ALL IN: {total}$
До оплати: {debt}$""")
        
