import streamlit as st

# --- ПОЛНАЯ МАТЕМАТИЧЕСКАЯ МОДЕЛЬ ИЗ ТАБЛИЦЫ ---

def get_auction_fee(bid):
    """Логика сетки сборов (IAAI/Copart). Замени цифры на свои из таблицы."""
    if bid <= 499: return 250
    if bid <= 599: return 340
    if bid <= 699: return 360
    if bid <= 999: return 450
    return bid * 0.15 # Пример для высоких ставок, если нет точной сетки

# Справочник стоимости доставки (Суша + Море)
LOGISTICS_ENGINE = {
    "Atlanta (GA)": {
        "inland": 400,
        "ocean": {"GAS": 2635, "EV/HYB": 2860, "GAS 3": 2760}
    },
    "New Jersey (NJ)": {
        "inland": 250,
        "ocean": {"GAS": 2100, "EV/HYB": 2350, "GAS 3": 2200}
    }
}

# Фиксированные константы
SWIFT = 121
INSURANCE = 50

# --- ИНТЕРФЕЙС STREAMLIT ---
st.set_page_config(page_title="Auto Logistics Engine", layout="wide")
st.title("⚙️ Система расчета по логике таблицы")

with st.sidebar:
    st.header("Ввод данных")
    bid = st.number_input("BID (Ставка)", value=500, step=50)
    fuel_type = st.selectbox("Тип топлива / Загрузки", ["GAS", "EV/HYB", "GAS 3"])
    origin = st.selectbox("Штат (Origin)", list(LOGISTICS_ENGINE.keys()))
    
    st.divider()
    customs = st.number_input("Митні платежі (Customs)", value=1720)
    other_fees = st.number_input("Прочие комиссии (Service/Broker)", value=150)

# --- ВЫЧИСЛЕНИЯ (БЕЗ ПОДГОНОК) ---
# 1. Считаем аукцион
current_auction_fee = get_auction_fee(bid)
auction_total = bid + current_auction_fee + SWIFT

# 2. Считаем логистику
inland_cost = LOGISTICS_ENGINE[origin]["inland"]
ocean_cost = LOGISTICS_ENGINE[origin]["ocean"][fuel_type]
delivery_total = inland_cost + ocean_cost + INSURANCE

# 3. ИТОГО (ALL IN)
total_all_in = auction_total + delivery_total + customs + other_fees

# --- ОТОБРАЖЕНИЕ РЕЗУЛЬТАТОВ ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🏦 Аукцион")
    st.write(f"Ставка: **${bid}**")
    st.write(f"Сбор аукциона: **${current_auction_fee}**")
    st.write(f"Swift перевод: **${SWIFT}**")
    st.info(f"Итого аукцион: ${auction_total}")

with col2:
    st.subheader("🚢 Доставка")
    st.write(f"Суша (Inland): **${inland_cost}**")
    st.write(f"Море (Ocean): **${ocean_cost}**")
    st.write(f"Страховка: **${INSURANCE}**")
    st.info(f"Итого доставка: ${delivery_total}")

with col3:
    st.subheader("📑 Оформление")
    st.write(f"Таможня: **${customs}**")
    st.write(f"Комиссии: **${other_fees}**")
    st.error(f"ALL IN: **${total_all_in}**")

st.divider()

# Таблица для проверки (как в Excel)
st.write("### Детальная смета (Raw Data)")
st.table({
    "Параметр": ["BID", "Auction Fee", "Swift", "Inland", "Ocean", "Insurance", "Customs", "Other Fees", "TOTAL"],
    "Значение": [bid, current_auction_fee, SWIFT, inland_cost, ocean_cost, INSURANCE, customs, other_fees, total_all_in]
})
