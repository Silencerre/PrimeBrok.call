import streamlit as st

# --- ПОВНА РОЗУМНА БАЗА ЛОКАЦІЙ (TOW + PORTS) ---
# Для кожного міста вказано порти, куди найвигідніше везти
LOCATIONS = {
    "Baltimore (MD)": {"port": "Baltimore", "land_price": 150},
    "Richmond (VA)": {"port": "Baltimore", "land_price": 350},
    "Alexandria (VA)": {"port": "Baltimore", "land_price": 250},
    "New York (NY)": {"port": "NJ", "land_price": 200},
    "Bridgeport (PA)": {"port": "NJ", "land_price": 250},
    "Atlanta (GA)": {"port": "Savannah", "land_price": 250},
    "Savannah (GA)": {"port": "Savannah", "land_price": 150},
    "Houston (TX)": {"port": "Houston", "land_price": 200},
    "Dallas (TX)": {"port": "Houston", "land_price": 350},
    "Los Angeles (CA)": {"port": "Long Beach", "land_price": 200},
    "Chicago (IL)": {"port": "NJ", "land_price": 750},
}

# Вартість мови (фрахт) до Констанци/Одеси залежно від порту США
SEA_FREIGHT = {
    "Baltimore": 1250,
    "NJ": 1200,
    "Savannah": 1300,
    "Houston": 1350,
    "Long Beach": 1650
}

# --- ЛОГІЧНІ ФУНКЦІЇ ---

def get_auction_fee(bid):
    if bid < 500: return 185
    if bid < 1000: return 320
    if bid < 3000: return 550
    if bid < 5000: return 750
    return bid * 0.14

def calc_customs(bid, engine, vol, yr):
    # Гібрид = Бензинове мито (Ваша умова)
    calc_type = "Бензин" if engine == "Гібрид" else engine
    if calc_type == "Електро": return 0 # Пільга
    
    age = 2026 - yr
    if age <= 0: age = 1
    coeff = 50 if calc_type == "Бензин" else 75
    accise = (vol / 1000) * coeff * (age if age <= 15 else 15)
    duty = bid * 0.10
    vat = (bid + duty + accise) * 0.20
    return accise + duty + vat

# --- ІНТЕРФЕЙС ---

st.set_page_config(page_title="PrimeBrok Pro", layout="wide")

st.title("🚢 PrimeBrok: Розумний Калькулятор")
st.markdown("---")

col_in, col_out = st.columns([2, 1])

with col_in:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🏎 Авто")
        bid = st.number_input("Ставка ($)", value=6000)
        engine = st.selectbox("Двигун", ["Бензин", "Дизель", "Гібрид", "Електро"])
        year = st.number_input("Рік", 2010, 2026, 2021)
        volume = st.number_input("Об'єм (см³)", value=2000)
    with c2:
        st.subheader("📍 Локація")
        city = st.selectbox("Місто аукціону", list(LOCATIONS.keys()))
        body = st.selectbox("Тип кузова", ["Седан", "SUV / Кросовер"])

# --- РОЗРАХУНОК ---
loc = LOCATIONS[city]
port_name = loc['port']
land_cost = loc['land_price']

# Корекція на SUV
if body == "SUV / Кросовер": land_cost += 150

# Корекція на Гібрид/Електро (Дорожча доставка)
is_special = engine in ["Електро", "Гібрид"]
if is_special: land_cost += 200 

ocean_cost = SEA_FREIGHT[port_name]
a_fee = get_auction_fee(bid)
customs = calc_customs(bid, engine, volume, year)
total = bid + a_fee + land_cost + ocean_cost + 166 + customs

with col_out:
    st.subheader("💰 Розрахунок")
    st.metric("Витрати США", f"${int(bid + a_fee + 166)}")
    st.metric(f"Трал до порту {port_name}", f"${int(land_cost)}")
    st.metric("Фрахт (Море)", f"${int(ocean_cost)}")
    st.metric("Мито (Україна)", f"${int(customs)}")
    st.divider()
    st.success(f"### РАЗОМ: ${int(total)}")
    
    if engine == "Гібрид":
        st.info("💡 Гібрид: Доставка за тарифом Електро, мито як за Бензин.")

st.caption(f"Логіка: Авто з {city} відправляється через порт {port_name}, що є оптимальним за ціною.")
