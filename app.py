import streamlit as st

# Настройка страницы
st.set_page_config(page_title="Car Delivery Calculator", layout="centered")

st.title("🚗 Калькулятор доставки авто из США")

# --- ДАННЫЕ (ТАРИФЫ) ---
rates = {
    "Одесса, Украина": {
        "NJ": {"Бензин/Дизель": 2475, "Электро/Гибрид": 2575, "Контейнер (3 авто)": 2830},
        "GA": {"Бензин/Дизель": 2450, "Электро/Гибрид": 2600, "Контейнер (3 авто)": 2830},
        "TX": {"Бензин/Дизель": 2575, "Электро/Гибрид": 2700, "Контейнер (3 авто)": 3000},
        "CA": {"Бензин/Дизель": 3250, "Электро/Гибрид": 3375, "Контейнер (3 авто)": 3900},
    },
    "Констанца, Румыния": {
        "NJ": {"Бензин/Дизель": 2665, "Электро/Гибрид": 2930, "Контейнер (3 авто)": 2860},
        "GA": {"Бензин/Дизель": 2635, "Электро/Гибрид": 2860, "Контейнер (3 авто)": 2760},
        "TX": {"Бензин/Дизель": 2755, "Электро/Гибрид": 2960, "Контейнер (3 авто)": 2960},
        "CA": {"Бензин/Дизель": 3410, "Электро/Гибрид": 3560, "Контейнер (3 авто)": 3735},
    }
}

# --- ИНТЕРФЕЙС ---
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        destination = st.selectbox("Пункт назначения", list(rates.keys()))
        origin = st.selectbox("Штат (Порт отправки)", ["NJ", "GA", "TX", "CA"])
    
    with col2:
        car_type = st.selectbox("Тип топлива / Загрузка", ["Бензин/Дизель", "Электро/Гибрид", "Контейнер (3 авто)"])
        towing_cost = st.number_input("Эвакуатор до порта (Towing), $", min_value=0, value=300, step=50)

    st.divider()

    # Поля для расчета аукциона (опционально)
    bid_price = st.number_input("Ставка на аукционе (Bid), $", min_value=0, value=0, step=100)
    auction_fee = st.number_input("Сбор аукциона (Auction Fee), $", min_value=0, value=0, step=50)

    # --- ЛОГИКА РАСЧЕТА ---
    sea_freight = rates[destination][origin][car_type]
    
    # Доп. расходы (Swift, страховка и т.д.)
    other_fees = 150 # Пример фиксированных комиссий
    
    total_delivery = sea_freight + towing_cost
    total_all_in = total_delivery + bid_price + auction_fee + other_fees

    # --- ВЫВОД РЕЗУЛЬТАТОВ ---
    st.subheader("Результаты расчета:")
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric("Только доставка", f"${total_delivery}")
        st.caption(f"Фрахт: ${sea_freight} + Доставка до порта: ${towing_cost}")
        
    with res_col2:
        st.metric("ИТОГО (авто + логистика)", f"${total_all_in}")
        st.caption("Включая ставку, сборы и мелкие расходы")

st.info("Данные по фрахту актуальны на 2026 год.")
