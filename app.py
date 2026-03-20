import streamlit as st

# Настройка страницы
st.set_page_config(page_title="Auto Auction Calculator", layout="centered")

st.title("🚀 Калькулятор логистики авто")
st.write("Расчет на основе логики таблицы (IAAI/Copart)")

# --- ИСХОДНЫЕ ДАННЫЕ (ЛОГИКА ТАБЛИЦЫ) ---
# Наземка (Inland)
INLAND_COSTS = {
    "Atlanta (GA)": 400,
    "New Jersey (NJ)": 250,
    "Savannah (GA)": 350
}

# Морской фрахт (Ocean) в зависимости от порта и типа топлива
OCEAN_FREIGHT = {
    "Constanta (RO)": {"GAS": 2635, "EV/HYB": 2860},
    "Odesa (UA)": {"GAS": 2100, "EV/HYB": 2350}
}

# Фиксированные сборы
SWIFT = 121
AUCTION_FEE_DEFAULT = 340 # Из твоего примера
INSURANCE = 50

# --- ИНТЕРФЕЙС ---
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        bid = st.number_input("Ставка на аукционе ($)", min_value=0, value=500, step=50)
        state = st.selectbox("Штат отправки (Origin)", list(INLAND_COSTS.keys()))
        fuel_type = st.radio("Тип топлива", ["GAS", "EV/HYB"], horizontal=True)
        
    with col2:
        port = st.selectbox("Порт назначения (Destination)", list(OCEAN_FREIGHT.keys()))
        customs = st.number_input("Таможенные платежи ($)", min_value=0, value=1720)
        other_fees = st.number_input("Прочие расходы / Склад ($)", min_value=0, value=0)

# --- РАСЧЕТ ---
# 1. Аукцион
total_auction = bid + AUCTION_FEE_DEFAULT + SWIFT

# 2. Логистика
inland_price = INLAND_COSTS[state]
ocean_price = OCEAN_FREIGHT[port][fuel_type]
total_shipping = inland_price + ocean_price + INSURANCE

# 3. ИТОГО
grand_total = total_auction + total_shipping + customs + other_fees

st.divider()

# --- ВЫВОД РЕЗУЛЬТАТОВ ---
c1, c2, c3 = st.columns(3)
c1.metric("Аукцион + Fees", f"${total_auction}")
c2.metric("Доставка и Фрахт", f"${total_shipping}")
c3.metric("Таможня", f"${customs}")

st.subheader(f"ИТОГО 'ALL IN': :green[${grand_total}]")

# Детализация для проверки
with st.expander("Посмотреть детализацию затрат"):
    st.write(f"**Аукционный сбор:** ${AUCTION_FEE_DEFAULT}")
    st.write(f"**Swift:** ${SWIFT}")
    st.write(f"**Наземка ({state}):** ${inland_price}")
    st.write(f"**Фрахт ({port} - {fuel_type}):** ${ocean_price}")
    st.write(f"**Страховка:** ${INSURANCE}")
    st.write(f"**Таможня:** ${customs}")

# Футер с расчетом долга (как в таблице)
st.info(f"К оплате (DEBT): -${grand_total}")
