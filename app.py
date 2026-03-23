import streamlit as st

st.set_page_config(page_title="Нікіта Калькулятор", layout="wide", page_icon="🇺🇦")

st.title("Нікіта Калькулятор")
st.markdown("**Імпорт авто з США** — Констанца / Одеса / Клайпеда")

# ────────────────────────────────────────────────
# Дані TOW — тільки ті локації, де є хоча б один нормальний порт (без Error)
# (скорочено для прикладу — додай свої 300+ локацій сюди за тим самим шаблоном)
tow = {
    "Atlanta (GA)":          {"GA": 400},
    "Atlanta East (GA)":     {"GA": 400},
    "Atlanta North (GA)":    {"GA": 400},
    "Atlanta South (GA)":    {"GA": 400},
    "Atlanta West (GA)":     {"GA": 400},
    "Savannah":              {"GA": 240},
    "Dallas (TX)":           {"TX": 350},
    "Dallas/Ft Worth (TX)":  {"TX": 350},
    "Los Angeles (CA)":      {"CA": 1150},
    "San Diego (CA)":        {"CA": 1150},
    "Seattle (WA)":          {"CA": 875, "WA": 275},
    "Avenel New Jersey (NJ)": {"NJ": 250},
    "Carteret":              {"NJ": 300},
    "Trenton":               {"NJ": 285},
    # ... сюди встав всі інші локації, де є число замість "Error"
}

# ────────────────────────────────────────────────
# Фрахт — точно з твого файлу (Constanta, Odesa, Klaipeda)
freight = {
    "Constanta": {
        "NJ": {"GAS":2665, "DIESEL":2665, "EV":2930, "HYB":2930, "GAS 3":2860, "DIESEL 3":2860, "EV 3":3265, "HYB 3":3265, "GAS 2":3980, "DIESEL 2":3980, "MOTO":2000},
        "GA": {"GAS":2635, "DIESEL":2635, "EV":2860, "HYB":2860, "GAS 3":2760, "DIESEL 3":2760, "EV 3":3145, "HYB 3":3145, "GAS 2":3940, "DIESEL 2":3940, "MOTO":2000},
        "TX": {"GAS":2755, "DIESEL":2755, "EV":2960, "HYB":2960, "GAS 3":2960, "DIESEL 3":2960, "EV 3":3385, "HYB 3":3385, "GAS 2":4180, "DIESEL 2":4180, "MOTO":2000},
        "CA": {"GAS":3410, "DIESEL":3410, "EV":3560, "HYB":3560, "GAS 3":3735, "DIESEL 3":3735, "EV 3":4145, "HYB 3":4145, "GAS 2":5490, "DIESEL 2":5490, "MOTO":2050},
    },
    "Odesa": {
        "NJ": {"GAS":2475, "DIESEL":2475, "EV":2575, "HYB":2575, "GAS 3":2830, "DIESEL 3":2830, "EV 3":3000, "HYB 3":3000, "MOTO":2000},
        "GA": {"GAS":2450, "DIESEL":2450, "EV":2600, "HYB":2600, "GAS 3":2830, "DIESEL 3":2830, "EV 3":3000, "HYB 3":3000, "MOTO":2000},
        "TX": {"GAS":2575, "DIESEL":2575, "EV":2700, "HYB":2700, "GAS 3":3000, "DIESEL 3":3000, "EV 3":3170, "HYB 3":3170, "MOTO":2000},
        "CA": {"GAS":3250, "DIESEL":3250, "EV":3375, "HYB":3375, "GAS 3":3900, "DIESEL 3":3900, "EV 3":4070, "HYB 3":4070, "MOTO":2050},
    },
    "Klaipeda": {
        "NJ": {"GAS":2685, "DIESEL":2685, "EV":2785, "HYB":2785, "GAS 3":2790, "DIESEL 3":2790, "EV 3":2890, "HYB 3":2890, "MOTO":2100},
        "GA": {"GAS":2735, "DIESEL":2735, "EV":2835, "HYB":2835, "GAS 3":2840, "DIESEL 3":2840, "EV 3":2940, "HYB 3":2940, "MOTO":2100},
        "TX": {"GAS":2860, "DIESEL":2860, "EV":2960, "HYB":2960, "GAS 3":2965, "DIESEL 3":2965, "EV 3":3065, "HYB 3":3065, "MOTO":2100},
        "CA": {"GAS":3260, "DIESEL":3260, "EV":3360, "HYB":3360, "GAS 3":3465, "DIESEL 3":3465, "EV 3":3565, "HYB 3":3565, "MOTO":2150},
        "WA": {"GAS":3735, "DIESEL":3735, "EV":2835, "HYB":2835, "GAS 3":4185, "DIESEL 3":4185, "EV 3":3285, "HYB 3":3285, "MOTO":3150},
    }
}

# ────────────────────────────────────────────────
col1, col2 = st.columns([5, 4])

with col1:
    st.subheader("Дані авто")

    client   = st.text_input("Клієнт / Замовлення №")
    model    = st.text_input("Модель + рік")
    vin      = st.text_input("VIN")

    location = st.selectbox("Локація аукціону", sorted(tow.keys()))

    # Показуємо тільки ті порти, де є ціна
    if location in tow:
        ports = [p for p, price in tow[location].items() if price is not None]
        if ports:
            us_port_label = st.selectbox("Порт відправлення США", [f"{p} — {tow[location][p]}$" for p in ports])
            us_port = us_port_label.split(" — ")[0]
            tow_cost = tow[location][us_port]
        else:
            st.warning("Для цієї локації немає доступних портів")
            us_port = None
            tow_cost = 0
    else:
        us_port = None
        tow_cost = 0

    ua_port = st.selectbox("Порт призначення", ["Constanta", "Odesa", "Klaipeda"])

    st.subheader("Тип та контейнер")

    col_type, col_fuel = st.columns(2)
    with col_type:
        is_moto = st.radio("Тип", ["Авто", "Мотоцикл"], horizontal=True) == "Мотоцикл"

    with col_fuel:
        if not is_moto:
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
            fuel = "—"
            container = "—"

with col2:
    st.subheader("Витрати")

    auction   = st.number_input("Збір аукціону", value=340, step=10)
    swift     = st.number_input("Swift аукціон", value=121, step=5)
    insurance = st.number_input("Страхування", value=50, step=10)
    storage   = st.number_input("Storage", value=0, step=50)
    other     = st.number_input("Інше", value=0, step=100)
    customs   = st.number_input("Митні платежі", value=1720, step=100)
    paid      = st.number_input("Вже сплачено", value=0, step=500)

# ────────────────────────────────────────────────
if st.button("Порахувати", type="primary", use_container_width=True):

    if not us_port:
        st.error("Обери локацію та порт США")
    else:
        try:
            freight_cost = freight[ua_port][us_port][f_key]
        except KeyError:
            freight_cost = None

        if freight_cost is None:
            st.error(f"Комбінація {ua_port} + {us_port} + {f_key} не знайдена")
        else:
            subtotal = tow_cost + freight_cost + auction + swift + insurance + storage + other
            total    = subtotal + customs
            debt     = total - paid

            st.success("Готово")

            st.markdown(f"""
            **TOW** ................ {tow_cost:>6,} $
            **Фрахт** ............. {freight_cost:>6,} $
            **Аукціон + Swift + Страх** .. {auction + swift + insurance:>6,} $
            **Storage + Інше** .... {storage + other:>6,} $
            ───────────────────────────────
            **Без мита** .......... {subtotal:>6,} $
            **Мито** .............. {customs:>6,} $
            **ВСЬОГО (ALL IN)** ... **{total:>6,} $**

            **Сплачено** .......... {paid:>6,} $
            **До оплати** ......... **{debt:>6,} $**
            """, unsafe_allow_html=True)

            st.code(f"""Нікіта Калькулятор | {st.session_state.get('today', '2025')}
Клієнт: {client}
Модель: {model}
VIN: {vin}
Локація: {location} → {us_port}
Порт UA: {ua_port}
Тип: { "Мото" if is_moto else f"{fuel} / {container}" }

TOW: {tow_cost}$
Фрахт: {freight_cost}$
Мито: {customs}$
ALL IN: {total}$
До оплати: {debt}$
""")
