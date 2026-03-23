import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Нікіта Калькулятор", layout="wide", page_icon="🇺🇦🚗")

st.title("Нікіта Калькулятор")
st.caption("Імпорт авто з США • Констанца / Одеса / Клайпеда • Повна логіка митних платежів")

# Поточний рік (замість ГОД(СЕГОДНЯ()))
current_year = datetime.now().year

# ────────────────────────────────────────────────
# TOW (тільки локації з цінами)
tow = {
    "Atlanta (GA)": {"GA": 400},
    "Dallas (TX)": {"TX": 350},
    "Los Angeles (CA)": {"CA": 1150},
    "Seattle (WA)": {"CA": 875, "WA": 275},
    # Додай інші локації з твого повного списку за тим самим шаблоном
}

# Freight (з твого останнього CSV)
freight = {
    "Constanta": {
        "NJ": {"GAS": 2665, "DIESEL": 2665, "EV": 2930, "HYB": 2930, "GAS 3": 2860, "DIESEL 3": 2860, "EV 3": 3265, "HYB 3": 3265, "GAS 2": 3980, "DIESEL 2": 3980, "MOTO": 2000},
        "GA": {"GAS": 2635, "DIESEL": 2635, "EV": 2860, "HYB": 2860, "GAS 3": 2760, "DIESEL 3": 2760, "EV 3": 3145, "HYB 3": 3145, "GAS 2": 3940, "DIESEL 2": 3940, "MOTO": 2000},
        "TX": {"GAS": 2755, "DIESEL": 2755, "EV": 2960, "HYB": 2960, "GAS 3": 2960, "DIESEL 3": 2960, "EV 3": 3385, "HYB 3": 3385, "GAS 2": 4180, "DIESEL 2": 4180, "MOTO": 2000},
        "CA": {"GAS": 3410, "DIESEL": 3410, "EV": 3560, "HYB": 3560, "GAS 3": 3735, "DIESEL 3": 3735, "EV 3": 4145, "HYB 3": 4145, "GAS 2": 5490, "DIESEL 2": 5490, "MOTO": 2050},
    },
    "Odesa": {
        "NJ": {"GAS": 2475, "DIESEL": 2475, "EV": 2575, "HYB": 2575, "GAS 3": 2830, "DIESEL 3": 2830, "EV 3": 3000, "HYB 3": 3000, "MOTO": 2000},
        "GA": {"GAS": 2450, "DIESEL": 2450, "EV": 2600, "HYB": 2600, "GAS 3": 2830, "DIESEL 3": 2830, "EV 3": 3000, "HYB 3": 3000, "MOTO": 2000},
        "TX": {"GAS": 2575, "DIESEL": 2575, "EV": 2700, "HYB": 2700, "GAS 3": 3000, "DIESEL 3": 3000, "EV 3": 3170, "HYB 3": 3170, "MOTO": 2000},
        "CA": {"GAS": 3250, "DIESEL": 3250, "EV": 3375, "HYB": 3375, "GAS 3": 3900, "DIESEL 3": 3900, "EV 3": 4070, "HYB 3": 4070, "MOTO": 2050},
    },
    "Klaipeda": {
        "NJ": {"GAS": 2685, "DIESEL": 2685, "EV": 2785, "HYB": 2785, "GAS 3": 2790, "DIESEL 3": 2790, "EV 3": 2890, "HYB 3": 2890, "MOTO": 2100},
        "GA": {"GAS": 2735, "DIESEL": 2735, "EV": 2835, "HYB": 2835, "GAS 3": 2840, "DIESEL 3": 2840, "EV 3": 2940, "HYB 3": 2940, "MOTO": 2100},
        "TX": {"GAS": 2860, "DIESEL": 2860, "EV": 2960, "HYB": 2960, "GAS 3": 2965, "DIESEL 3": 2965, "EV 3": 3065, "HYB 3": 3065, "MOTO": 2100},
        "CA": {"GAS": 3260, "DIESEL": 3260, "EV": 3360, "HYB": 3360, "GAS 3": 3465, "DIESEL 3": 3465, "EV 3": 3565, "HYB 3": 3565, "MOTO": 2150},
        "WA": {"GAS": 3735, "DIESEL": 3735, "EV": 2835, "HYB": 2835, "GAS 3": 4185, "DIESEL 3": 4185, "EV 3": 3285, "HYB 3": 3285, "MOTO": 3150},
    }
}

# ────────────────────────────────────────────────
col1, col2 = st.columns([6, 5])

with col1:
    st.subheader("Дані авто")

    client = st.text_input("Клієнт")
    model = st.text_input("Модель")
    vin = st.text_input("VIN")
    year = st.number_input("Рік по шильдику", min_value=1980, max_value=2030, value=2015, step=1)
    engine_volume = st.number_input("Об'єм двигуна (л)", min_value=0.0, max_value=10.0, value=2.0, step=0.1, format="%.1f")

    location = st.selectbox("Локація аукціону", sorted(tow.keys()))

    avail = tow.get(location, {})
    if avail:
        port_label = st.selectbox("Порт США", [f"{p} — {v} $" for p, v in avail.items()])
        us_port = port_label.split(" — ")[0]
        tow_cost = avail[us_port]
    else:
        us_port = None
        tow_cost = 0

    ua_port = st.selectbox("Порт призначення", ["Constanta", "Odesa", "Klaipeda"])

    fuel_type = st.selectbox("Тип палива / завантаження", ["GAS", "DIESEL", "EV", "HYB", "GAS 3", "GAS 2", "MOTO"])

with col2:
    st.subheader("Витрати")

    auction = st.number_input("Збір аукціону", value=340)
    swift = st.number_input("Swift Аукціон", value=121)
    insurance = st.number_input("Страхування", value=50)
    storage = st.number_input("Storage", value=0)
    other = st.number_input("Інше", value=0)
    paid = st.number_input("Вже сплачено", value=0)

    customs_cost = st.number_input("Вартість авто для митниці (B3)", value=1000)

# ────────────────────────────────────────────────
if st.button("Розрахувати", type="primary"):
    if not us_port:
        st.error("Обери локацію та порт")
    else:
        try:
            freight_cost = freight[ua_port][us_port][fuel_type]
        except KeyError:
            freight_cost = None

        if freight_cost is None:
            st.error("Немає тарифу фрахту для цієї комбінації")
        else:
            # Логіка митних платежів з твоєї формули
            age = max(1, min(15, current_year - year - 1))

            if "GAS" in fuel_type or "HYB" in fuel_type:
                excise_rate = 50 if engine_volume <= 3 else 100
            elif "DIESEL" in fuel_type:
                excise_rate = 75 if engine_volume <= 3.5 else 150
            elif "EV" in fuel_type:
                excise_rate = 0  # EV має спрощену формулу
            else:
                excise_rate = 0

            excise = excise_rate * engine_volume * age * 1.2
            duty = customs_cost * 0.10
            vat_base = customs_cost + duty + excise
            vat = vat_base * 0.20

            customs = duty + excise + vat

            # Підсумок
            subtotal = tow_cost + freight_cost + auction + swift + insurance + storage + other
            total = subtotal + customs
            debt = total - paid

            st.success("Готово!")

            st.markdown(f"""
            **TOW:** {tow_cost:,} $
            **Фрахт:** {freight_cost:,} $
            **Аукціон + Swift + Страх:** {auction + swift + insurance:,} $
            **Storage + Інше:** {storage + other:,} $

            **Митні платежі:**
            - Мито 10%: {duty:,.0f} $
            - Акциз: {excise:,.0f} $
            - ПДВ 20%: {vat:,.0f} $
            **РАЗОМ мито:** {customs:,.0f} $

            **ALL IN:** **{total:,.0f} $**
            **До оплати:** **{debt:,.0f} $**
            """)

            st.code(f"""Нікіта Калькулятор
{client} | {model} | {vin} | {year} рік | {engine_volume} л | {fuel_type}
TOW: {tow_cost}$
Фрахт: {freight_cost}$
Мито: {customs:,.0f}$
ВСЬОГО: {total:,.0f}$
До оплати: {debt:,.0f}$""")
