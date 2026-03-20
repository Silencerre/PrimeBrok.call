import streamlit as st

# --- ПОЛНАЯ КОНФИГУРАЦИЯ ИЗ ТАБЛИЦЫ ---
st.set_page_config(page_title="Auto Logistics PRO", layout="wide")

# 1. Сетка сборов аукциона (IAAI/Copart)
def calculate_auction_fee(bid):
    if bid <= 499: return 250
    if bid <= 599: return 340
    if bid <= 699: return 360
    if bid <= 799: return 380
    if bid <= 899: return 400
    if bid <= 999: return 420
    return 500 + (bid * 0.03) # Динамический шаг для высоких ставок

# 2. Справочник логистики (Штат -> Тип авто)
LOGISTICS = {
    "Atlanta (GA)": {"inland": 400, "ocean_gas": 2635, "ocean_ev": 2860},
    "New Jersey (NJ)": {"inland": 250, "ocean_gas": 2100, "ocean_ev": 2350},
    "Savannah (GA)": {"inland": 350, "ocean_gas": 2600, "ocean_ev": 2850}
}

st.title("🚗 Профессиональный расчет доставки авто")
st.divider()

# --- ВВОД ДАННЫХ ОБ АВТОМОБИЛЕ ---
with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        car_name = st.text_input("Марка / Модель", placeholder="Напр: BMW X5")
        year = st.number_input("Год выпуска", min_value=1900, max_value=2026, value=2020)
    with c2:
        engine_vol = st.text_input("Объем двигателя (литры / кВт)", value="2.0")
        fuel_type = st.selectbox("Тип топлива / Привод", ["GAS", "DIESEL", "EV (Electric)", "HYBRID"])
    with c3:
        lot_id = st.text_input("ID Лота (Stock #)", value="00000000")
        location = st.selectbox("Локация (Штат покупки)", list(LOGISTICS.keys()))

st.divider()

# --- ФИНАНСОВАЯ ЧАСТЬ ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("💰 Затраты на аукционе")
    bid = st.number_input("Ставка (Bid) ($)", value=500, step=100)
    auc_fee = calculate_auction_fee(bid)
    swift = 121
    st.write(f"Сбор аукциона: **${auc_fee}**")
    st.write(f"Swift перевод: **${swift}**")

with col_right:
    st.subheader("🚢 Логистика и Таможня")
    # Логика выбора цены фрахта в зависимости от типа топлива
    is_ev = "EV" in fuel_type or "HYBRID" in fuel_type
    ocean_price = LOGISTICS[location]["ocean_ev"] if is_ev else LOGISTICS[location]["ocean_gas"]
    inland_price = LOGISTICS[location]["inland"]
    
    customs = st.number_input("Митні платежі (Customs) ($)", value=1720)
    insurance = 50
    broker_fee = 150 # Твоя комиссия

# --- РАСЧЕТ ИТОГА ---
total_auction = bid + auc_fee + swift
total_delivery = inland_price + ocean_price + insurance
grand_total = total_auction + total_delivery + customs + broker_fee

st.divider()

# --- ИТОГОВОЕ ТАБЛО ---
res1, res2, res3 = st.columns(3)
res1.metric("АУКЦИОН + СБОРЫ", f"${total_auction}")
res2.metric("ДОСТАВКА В ПОРТ", f"${total_delivery}")
res3.metric("ТАМОЖНЯ", f"${customs}")

st.error(f"## ИТОГО 'ALL IN': ${grand_total}")

# --- КНОПКА СОХРАНЕНИЯ (ИМИТАЦИЯ ТАБЛИЦЫ) ---
if st.button("Добавить в отчет"):
    st.success(f"Автомобиль {car_name} ({year}, {engine_vol}L) успешно просчитан!")
    st.table({
        "Параметр": ["Авто", "Год", "Объем", "Топливо", "Локация", "Итого к оплате"],
        "Данные": [car_name, year, engine_vol, fuel_type, location, f"${grand_total}"]
    })
