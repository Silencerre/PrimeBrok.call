import streamlit as st

# Настройка страницы
st.set_page_config(page_title="Auto USA Calculator", page_icon="🚗", layout="wide")

# --- ДАННЫЕ ИЗ ВАШЕЙ ТАБЛИЦЫ ---
TOW_PRICES = {
    "ABILENE": 375, "ALBANY": 250, "ALBUQUERQUE": 425, "ALTOONA": 325,
    "ASHEVILLE": 350, "ATLANTA": 175, "BALTIMORE": 175, "BILLINGS": 1050
}

FREIGHT_PRICES = {
    "Odesa (UA)": 1450, "Klaipeda (LT)": 1250, "Constanta (RO)": 1350
}

# Функция расчета аукционного сбора (пример на основе стандартных сеток)
def get_auction_fee(bid):
    if bid < 500: return 200
    elif bid < 1000: return 350
    elif bid < 2000: return 450
    elif bid < 5000: return 650
    else: return bid * 0.15

# --- ИНТЕРФЕЙС ---
st.title("🧮 Автономный калькулятор доставки авто из США")
st.write("Мой повелитель, введите параметры лота для мгновенного расчета.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Параметры лота")
    bid = st.number_input("Ставка на аукционе ($)", min_value=0, value=5000, step=100)
    location = st.selectbox("Локация аукциона (TOW)", list(TOW_PRICES.keys()))
    destination = st.selectbox("Порт назначения", list(FREIGHT_PRICES.keys()))
    engine_vol = st.number_input("Объем двигателя (см³)", value=2000)
    fuel_type = st.radio("Тип двигателя", ["Бензин", "Дизель", "Электро"])

with col2:
    st.subheader("📊 Расчет стоимости")
    
    # Логика вычислений
    fee = get_auction_fee(bid)
    tow = TOW_PRICES[location]
    freight = FREIGHT_PRICES[destination]
    customs = (bid * 0.1) + (engine_vol * 0.05) # Пример упрощенной формулы таможни
    
    total_logistics = tow + freight + 150 # 150 - оформление документов
    total_cost = bid + fee + total_logistics + customs

    # Вывод результатов в карточках
    st.metric(label="ИТОГО (ALL IN)", value=f"${total_cost:,.0f}")
    
    with st.expander("Посмотреть детализацию"):
        st.write(f"🏷️ Сбор аукциона: ${fee}")
        st.write(f"🚚 Эвакуатор ({location}): ${tow}")
        st.write(f"🚢 Фрахт ({destination}): ${freight}")
        st.write(f"⚖️ Таможенные платежи (прим.): ${customs:,.0f}")

st.info("Приложение работает полностью автономно и не требует подключения к Google Sheets.")