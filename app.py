import streamlit as st

# --- МІЗКИ ТАБЛИЦІ (ПОВНА ЛОГІКА) ---

def get_auction_fee(bid):
    if bid <= 500: return 340
    if bid <= 1000: return 450
    if bid <= 2000: return 630
    if bid <= 5000: return 850
    return bid * 0.15

def get_logistics(location, engine, body):
    # База з вашої таблиці TOW
    base_rates = {
        "Atlanta (GA)": 3055,
        "Baltimore (MD)": 3150,
        "New Jersey (NJ)": 3000,
        "Houston (TX)": 3200,
        "Los Angeles (CA)": 3400,
        "Seattle (WA)": 3500
    }
    price = base_rates.get(location, 3055)
    
    # Націнка за кузов (SUV)
    if body == "SUV / Кросовер":
        price += 150
        
    # Гібрид/Електро дорожче (Ваше замовлення)
    if engine in ["Electric", "Hybrid"]:
        price += 200
    return price

def calculate_customs(bid, engine, volume, year):
    """ПОВНИЙ РОЗРАХУНОК МИТНИЦІ (Україна)"""
    if engine == "Electric":
        return 0 # Пільга (тільки акциз ~1 євро за кВт)
    
    # Розрахунок акцизу: Об'єм * Коефіцієнт двигуна * Вік
    age = 2026 - year
    if age <= 0: age = 1
    if age > 15: age = 15
    
    coeff = 50 if engine == "GAS" or engine == "Hybrid" else 75
    accise = (volume / 1000) * coeff * age
    
    # Мито (10% від ставки) + ПДВ (20% від всього)
    duty = bid * 0.10
    vat = (bid + duty + accise) * 0.20
    
    # Плюс ваш фікс "Customs Cost" з таблиці
    customs_cost = 1000 
    
    return accise + duty + vat + customs_cost

# --- ІНТЕРФЕЙС PRIME BROK ---

st.set_page_config(page_title="PrimeBrok Pro", layout="wide")
st.title("🚢 PrimeBrok")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Технічні дані")
    c1, c2 = st.columns(2)
    with c1:
        bid = st.number_input("Ставка ($)", value=2000)
        engine = st.selectbox("Двигун", ["GAS", "Diesel", "Hybrid", "Electric"])
        volume = st.number_input("Об'єм двигуна (см³)", value=2000, step=100)
    with c2:
        year = st.number_input("Рік випуску", 2010, 2026, 2020)
        location = st.selectbox("Локація", ["Atlanta (GA)", "Baltimore (MD)", "New Jersey (NJ)", "Houston (TX)", "Los Angeles (CA)", "Seattle (WA)"])
        body = st.selectbox("Кузов", ["Седан", "SUV / Кросовер"])

# --- ОБЧИСЛЕННЯ ---
a_fee = get_auction_fee(bid)
swift = 121
logistics = get_logistics(location, engine, body)
insurance = 50
customs_all = calculate_customs(bid, engine, volume, year)

total = bid + a_fee + swift + logistics + insurance + customs_all

with col2:
    st.subheader("💰 Розрахунок")
    st.write(f"💵 Аукціон + Swift: `${int(a_fee + swift)}`")
    st.write(f"🚚 Логістика: `${int(logistics)}`")
    st.write(f"📑 Розмитнення: `${int(customs_all)}`")
    st.divider()
    st.success(f"### РАЗОМ (ALL IN): ${int(total)}")
    
    if engine == "Hybrid":
        st.info("💡 Гібрид: розмитнення як бензин, логістика як електро.")

st.caption("PrimeBrok: Розраховано на базі повної математичної моделі вашої таблиці.")
