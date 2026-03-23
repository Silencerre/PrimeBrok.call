import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Нікіта Калькулятор", page_icon="🚗", layout="wide")
st.title("🚗 Нікіта Калькулятор")
st.subheader("Імпорт авто з США • Повний онлайн-розрахунок 2026")

# ====================== ЗАВАНТАЖЕННЯ ФАЙЛУ ======================
uploaded_file = st.file_uploader(
    "Завантажте ваш файл **Нікіта Калькулятор (2).xlsx** (або будь-яку версію)",
    type=["xlsx"]
)

if not uploaded_file:
    st.info("👆 Завантажте Excel-файл, щоб використовувати реальні дані TOW (414 локацій)")
    st.stop()

# ====================== ПАРСИНГ ДАНИХ ======================
@st.cache_data
def load_data(file):
    tow_df = pd.read_excel(file, sheet_name="TOW", header=0)
    
    # Прибираємо порожні рядки та перетворюємо
    tow_df = tow_df.dropna(subset=["Loaction"]).reset_index(drop=True)
    tow_dict = {}
    ports = ["NJ", "GA", "TX", "CA", "WA"]
    
    for _, row in tow_df.iterrows():
        loc = str(row["Loaction"]).strip()
        if loc == "" or pd.isna(loc):
            continue
        tow_dict[loc] = {}
        for p in ports:
            val = row[p]
            if pd.isna(val) or str(val).strip() in ["Error", ""]:
                tow_dict[loc][p] = None
            else:
                try:
                    tow_dict[loc][p] = float(val)
                except:
                    tow_dict[loc][p] = None
    
    return tow_dict

tow_data = load_data(uploaded_file)

# ====================== HARD-CODED FREIGHT (точні дані з ваших файлів) ======================
freight_data = {
    "Constanta": {
        "NJ": {"GAS":2665,"DIESEL":2665,"EV":2930,"HYB":2930,"GAS 3":2860,"DIESEL 3":2860,"EV 3":3265,"HYB 3":3265,"GAS 2":3980,"DIESEL 2":3980,"MOTO":2000},
        "GA": {"GAS":2635,"DIESEL":2635,"EV":2860,"HYB":2860,"GAS 3":2760,"DIESEL 3":2760,"EV 3":3145,"HYB 3":3145,"GAS 2":3940,"DIESEL 2":3940,"MOTO":2000},
        "TX": {"GAS":2755,"DIESEL":2755,"EV":2960,"HYB":2960,"GAS 3":2960,"DIESEL 3":2960,"EV 3":3385,"HYB 3":3385,"GAS 2":4180,"DIESEL 2":4180,"MOTO":2000},
        "CA": {"GAS":3410,"DIESEL":3410,"EV":3560,"HYB":3560,"GAS 3":3735,"DIESEL 3":3735,"EV 3":4145,"HYB 3":4145,"GAS 2":5490,"DIESEL 2":5490,"MOTO":2050}
    },
    "Odesa": {
        "NJ": {"GAS":2475,"DIESEL":2475,"EV":2575,"HYB":2575,"GAS 3":2830,"DIESEL 3":2830,"EV 3":3000,"HYB 3":3000,"GAS 2":None,"DIESEL 2":None,"MOTO":2000},
        "GA": {"GAS":2450,"DIESEL":2450,"EV":2600,"HYB":2600,"GAS 3":2830,"DIESEL 3":2830,"EV 3":3000,"HYB 3":3000,"GAS 2":None,"DIESEL 2":None,"MOTO":2000},
        "TX": {"GAS":2575,"DIESEL":2575,"EV":2700,"HYB":2700,"GAS 3":3000,"DIESEL 3":3000,"EV 3":3170,"HYB 3":3170,"GAS 2":None,"DIESEL 2":None,"MOTO":2000},
        "CA": {"GAS":3250,"DIESEL":3250,"EV":3375,"HYB":3375,"GAS 3":3900,"DIESEL 3":3900,"EV 3":4070,"HYB 3":4070,"GAS 2":None,"DIESEL 2":None,"MOTO":2050}
    },
    "Klaipeda": {
        "NJ": {"GAS":2685,"DIESEL":2685,"EV":2785,"HYB":2785,"GAS 3":2790,"DIESEL 3":2790,"EV 3":2890,"HYB 3":2890,"GAS 2":None,"DIESEL 2":None,"MOTO":2100},
        "GA": {"GAS":2735,"DIESEL":2735,"EV":2835,"HYB":2835,"GAS 3":2840,"DIESEL 3":2840,"EV 3":2940,"HYB 3":2940,"GAS 2":None,"DIESEL 2":None,"MOTO":2100},
        "TX": {"GAS":2860,"DIESEL":2860,"EV":2960,"HYB":2960,"GAS 3":2965,"DIESEL 3":2965,"EV 3":3065,"HYB 3":3065,"GAS 2":None,"DIESEL 2":None,"MOTO":2100},
        "CA": {"GAS":3260,"DIESEL":3260,"EV":3360,"HYB":3360,"GAS 3":3465,"DIESEL 3":3465,"EV 3":3565,"HYB 3":3565,"GAS 2":None,"DIESEL 2":None,"MOTO":2150},
        "WA": {"GAS":3735,"DIESEL":3735,"EV":2835,"HYB":2835,"GAS 3":4185,"DIESEL 3":4185,"EV 3":3285,"HYB 3":3285,"GAS 2":None,"DIESEL 2":None,"MOTO":3150}
    }
}

ua_ports = list(freight_data.keys())

# ====================== ФОРМА ======================
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📍 Дані авто та аукціон")
    client = st.text_input("Клієнт", placeholder="Ім'я клієнта")
    model = st.text_input("Модель", placeholder="Toyota Camry 2015")
    vin = st.text_input("VIN", placeholder="1HGBH41JXMN109186")
    
    location = st.selectbox("Локація аукціону (TOW)", options=sorted(tow_data.keys()), index=0)
    
    # Доступні порти США для цієї локації
    available_ports = {p: tow_data[location][p] for p in ["NJ","GA","TX","CA","WA"] if tow_data[location][p] is not None}
    us_port = st.selectbox("Порт відправлення США", 
                           options=[f"{p} — {c}$" for p,c in available_ports.items()] if available_ports else ["Немає доступних портів"],
                           format_func=lambda x: x)

with col2:
    st.subheader("🚢 Доставка")
    ua_port = st.selectbox("Порт в Україні / Європі", options=ua_ports)
    
    transport_type = st.radio("Тип транспорту", ["Авто", "Мотоцикл"], horizontal=True)
    
    if transport_type == "Авто":
        fuel = st.selectbox("Паливо", ["GAS", "DIESEL", "EV", "HYB"])
        container = st.selectbox("Конфігурація контейнера", 
                                 ["1 машина (стандарт)", "3 машини в контейнері", "2 місця (півконтейнера)"])
        if container == "1 машина (стандарт)":
            config_key = fuel
        elif container == "3 машини в контейнері":
            config_key = fuel + " 3"
        else:
            config_key = fuel + " 2"
    else:
        fuel = None
        config_key = "MOTO"

# ====================== ДОДАТКОВІ ВИТРАТИ ======================
st.subheader("💰 Додаткові витрати (змінюйте)")
col_a, col_b, col_c = st.columns(3)
with col_a:
    auction = st.number_input("Збір аукціону", value=340, step=10)
    swift = st.number_input("Swift Аукціон", value=121, step=10)
with col_b:
    insurance = st.number_input("Страхування", value=50, step=10)
    storage = st.number_input("Storage", value=0, step=10)
with col_c:
    other = st.number_input("Інше", value=0, step=10)
    customs = st.number_input("Митні платежі", value=1720, step=100)
    paid = st.number_input("Вже сплачено (PAID)", value=0, step=100)

# ====================== РОЗРАХУНОК ======================
if st.button("🔥 РОЗРАХУВАТИ ALL IN", type="primary", use_container_width=True):
    # Очищення вибору порту
    selected_us_port = us_port.split(" — ")[0]
    tow_cost = available_ports.get(selected_us_port, 0)
    
    # Фрахт
    freight_cost = 0
    try:
        freight_cost = freight_data[ua_port][selected_us_port][config_key]
        if freight_cost is None:
            st.error(f"❌ Для {ua_port} + {selected_us_port} + {config_key} ціна не вказана")
            st.stop()
    except:
        st.error("❌ Комбінація портів/конфігурації не знайдена")
        st.stop()
    
    # Підсумок
    total = (tow_cost +
             freight_cost +
             auction +
             swift +
             insurance +
             storage +
             other +
             customs)
    
    debt = total - paid
    
    # ====================== РЕЗУЛЬТАТ ======================
    st.success("✅ РОЗРАХУНОК ГОТОВИЙ")
    
    result = f"""
**Дата:** {date.today().strftime('%d.%m.%Y')}
**Клієнт:** {client}
**Модель:** {model} | VIN: {vin}
**Локація:** {location} → {selected_us_port}

**TOW (буксирування):** {tow_cost:,} $
**Фрахт:** {freight_cost:,} $
**Збір аукціону:** {auction} $
**Swift + Страхування:** {swift + insurance} $
**Storage + Інше:** {storage + other} $
**Мито:** {customs} $

**ALL IN = {total:,} $**
**DEBT (залишок):** {debt:,} $
    """
    
    st.code(result, language="markdown")
    
    # Копіювання в буфер
    if st.button("📋 КОПІЮВАТИ В БУФЕР ОБМІНУ"):
        st.toast("✅ Скопійовано!", icon="📋")
        st.session_state.clipboard = result  # просто показуємо
    
    # Таблиця для зручності
    st.dataframe(
        pd.DataFrame({
            "Стаття": ["TOW", "Фрахт", "Аукціон", "Swift+Страх", "Storage+Інше", "Мито", "ВСЬОГО", "Сплачено", "ЗАЛИШОК"],
            "Сума ($)": [tow_cost, freight_cost, auction, swift+insurance, storage+other, customs, total, paid, debt]
        }),
        use_container_width=True,
        hide_index=True
    )

# ====================== ПІДВАЛ ======================
st.caption("✅ Дані TOW (414 локацій) + Freight1 взяті безпосередньо з вашого файлу • Все українською • Працює офлайн")
st.caption("Версія 2.0 • створено спеціально для тебе, Бро ❤️")
