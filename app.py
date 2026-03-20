import streamlit as st

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Prime Broker Elite", layout="wide")

# --- ДАННЫЕ ЛОГИСТИКИ (СВЯЗКА ЛОКАЦИЯ -> ПОРТ) ---
# Структура: "Локация": "Ближайший Порт"
AUCTION_TO_PORT = {
    "Atlanta, GA": "GA",
    "Savannah, GA": "GA",
    "Theodore, AL": "GA",
    "Newark, NJ": "NJ",
    "Elizabeth, NJ": "NJ",
    "Philadelphia, PA": "NJ",
    "Boston, MA": "NJ",
    "Houston, TX": "TX",
    "Dallas, TX": "TX",
    "San Antonio, TX": "TX",
    "Los Angeles, CA": "CA",
    "San Diego, CA": "CA",
    "Sacramento, CA": "CA"
}

# Стоимость эвакуатора (Towing) по умолчанию для локаций
TOWING_PRICES = {
    "Atlanta, GA": 400, "Savannah, GA": 240, "Theodore, AL": 600,
    "Newark, NJ": 200, "Elizabeth, NJ": 200, "Philadelphia, PA": 300, "Boston, MA": 450,
    "Houston, TX": 250, "Dallas, TX": 450, "San Antonio, TX": 400,
    "Los Angeles, CA": 250, "San Diego, CA": 350, "Sacramento, CA": 500
}

# Тарифы морского фрахта (Sea Freight)
FREIGHT_RATES = {
    "Одесса": {
        "NJ": {"Gas": 2475, "Diesel": 2475, "EV": 2575},
        "GA": {"Gas": 2450, "Diesel": 2450, "EV": 2600},
        "TX": {"Gas": 2575, "Diesel": 2575, "EV": 2700},
        "CA": {"Gas": 3250, "Diesel": 3250, "EV": 3375}
    },
    "Констанца": {
        "NJ": {"Gas": 2665, "Diesel": 2665, "EV": 2930},
        "GA": {"Gas": 2635, "Diesel": 2635, "EV": 2860},
        "TX": {"Gas": 2755, "Diesel": 2755, "EV": 2960},
        "CA": {"Gas": 3410, "Diesel": 3410, "EV": 3560}
    },
    "Клайпеда": {
        "NJ": {"Gas": 2100, "Diesel": 2100, "EV": 2200},
        "GA": {"Gas": 2200, "Diesel": 2200, "EV": 2350},
        "TX": {"Gas": 2300, "Diesel": 2300, "EV": 2450},
        "CA": {"Gas": 2900, "Diesel": 2900, "EV": 3100}
    }
}

# --- ИНТЕРФЕЙС ---
st.title("💼 Prime Broker: Профессиональный расчет логистики")

with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1. Аукцион")
        auction_loc = st.selectbox("Локация автомобиля (Auction)", list(AUCTION_TO_PORT.keys()))
        auto_port = AUCTION_TO_PORT[auction_loc]
        st.info(f"Автоматический порт отправки: **{auto_port}**")
        
        bid_price = st.number_input("Ставка аукциона ($)", value=5000, step=500)
        auction_fee = st.number_input("Сбор аукциона ($)", value=700)

    with col2:
        st.markdown("### 2. Характеристики")
        fuel = st.selectbox("Тип двигателя", ["Gas", "Diesel", "EV"])
        engine = st.number_input("Объем (см³)", value=2000) if fuel != "EV" else 0
        year = st.number_input("Год выпуска", value=2021, min_value=2000)
        dest = st.selectbox("Порт назначения", ["Одесса", "Констанца", "Клайпеда"])

    with col3:
        st.markdown("### 3. Логистика")
        towing = st.number_input("Эвакуатор (Towing) $", value=TOWING_PRICES[auction_loc])
        shipping = FREIGHT_RATES[dest][auto_port][fuel]
        st.write(f"Фрахт (Sea Freight): **${shipping}**")
        
        extra_fees = st.number_input("Прочие (Swift, Доки) $", value=250)

# --- РАСЧЕТ ТАМОЖНИ (УКРАИНА) ---
def get_customs(bid, eng, yr, f):
    if f == "EV": return bid * 0.01 # Упрощенно для электро
    age_coeff = max(1, min(15, 2026 - yr - 1))
    base = 50 if (f == "Gas" and eng <= 3000) else 100
    if f == "Diesel": base = 75 if eng <= 3500 else 150
    excise = base * (eng / 1000) * age_coeff
    duty, vat = bid * 0.10, (bid + (bid*0.1) + excise) * 0.20
    return excise + duty + vat

customs = get_customs(bid_price, engine, year, fuel)
total_delivery = shipping + towing + extra_fees
total_all_in = bid_price + auction_fee + total_delivery + customs

# --- ИТОГОВЫЙ БЛОК ---
st.divider()
res1, res2, res3 = st.columns(3)
res1.metric("ДОСТАВКА ИТОГО", f"${total_delivery}")
res2.metric("ТАМОЖНЯ (УЗ)", f"${int(customs)}")
res3.metric("ИТОГО ПОД КЛЮЧ", f"${int(total_all_in)}")

# ДЕТАЛЬНАЯ ТАБЛИЦА
st.markdown("### Детализация расходов")
st.table({
    "Статья расходов": ["Авто", "Сбор аукциона", "Towing (Внутр.)", "Sea Freight (Море)", "Таможня", "Комиссии"],
    "Сумма ($)": [bid_price, auction_fee, towing, shipping, int(customs), extra_fees]
})
