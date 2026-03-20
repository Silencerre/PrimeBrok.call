import streamlit as st

# --- ПОВНА БАЗА ДАНИХ (ЛОГІКА ТАБЛИЦІ TOW) ---
# База основних локацій та тарифів до найближчих портів
LOCATIONS = {
    "Abilene (TX)": {"port": "TX", "price": 375},
    "Adelanto (CA)": {"port": "CA", "price": 275},
    "Albuquerque (NM)": {"port": "TX", "price": 850},
    "Alexandria (VA)": {"port": "NJ", "price": 425},
    "Atlanta (GA)": {"port": "GA", "price": 250},
    "Baltimore (MD)": {"port": "NJ", "price": 325},
    "Billings (MT)": {"port": "WA", "price": 950},
    "Boise (ID)": {"port": "WA", "price": 850},
    "Bridgeport (PA)": {"port": "NJ", "price": 225},
    "Casper (WY)": {"port": "TX", "price": 1100},
    "Charleston (SC)": {"port": "GA", "price": 350},
    "Chicago (IL)": {"port": "NJ", "price": 750},
    "Columbus (OH)": {"port": "NJ", "price": 650},
    "Dallas (TX)": {"port": "TX", "price": 325},
    "Denver (CO)": {"port": "TX", "price": 950},
    "Detroit (MI)": {"port": "NJ", "price": 700},
    "Eugene (OR)": {"port": "WA", "price": 450},
    "Houston (TX)": {"port": "TX", "price": 200},
    "Indianapolis (IN)": {"port": "NJ", "price": 750},
    "Jacksonville (FL)": {"port": "GA", "price": 375},
    "Las Vegas (NV)": {"port": "CA", "price": 450},
    "Los Angeles (CA)": {"port": "CA", "price": 200},
    "Miami (FL)": {"port": "GA", "price": 650},
    "Nashville (TN)": {"port": "GA", "price": 550},
    "New Orleans (LA)": {"port": "TX", "price": 550},
    "New York (NY)": {"port": "NJ", "price": 250},
    "Oklahoma City (OK)": {"port": "TX", "price": 450},
    "Orlando (FL)": {"port": "GA", "price": 550},
    "Philadelphia (PA)": {"port": "NJ", "price": 250},
    "Phoenix (AZ)": {"port": "CA", "price": 550},
    "Portland (OR)": {"port": "WA", "price": 350},
    "Richmond (VA)": {"port": "NJ", "price": 450},
    "Salt Lake City (UT)": {"port": "CA", "price": 850},
    "San Antonio (TX)": {"port": "TX", "price": 350},
    "San Diego (CA)": {"port": "CA", "price": 350},
    "Seattle (WA)": {"port": "WA", "price": 250},
    "St. Louis (MO)": {"port": "TX", "price": 850},
    "Washington (DC)": {"port": "NJ", "price": 400}
}

# --- ФУНКЦІЇ РОЗРАХУНКУ ---

def get_auction_fee(bid):
    # Динамічна сітка зборів (Вкладка BASE)
    if bid < 100: return 1
    if bid < 500: return 180
    if bid < 1000: return 300
    if bid < 2000: return 480
    if bid < 3000: return 580
    if bid < 4000: return 680
    if bid < 5000: return 780
    return bid * 0.15

def calc_customs(bid, engine, vol, yr):
    # Гібрид рахується як бензин (Ваша умова)
    calc_type = "Бензин" if engine == "Гібрид" else engine
    if calc_type == "Електро": return 0
    
    age = 2026 - yr
    if age <= 0: age = 1
    coeff = 50 if calc_type == "Бензин" else 75
    
    accise = (vol / 1000) * coeff * (age if age <= 15 else 15)
    duty = bid * 0.10
    vat = (bid + duty + accise) * 0.20
    return accise + duty + vat

# --- ІНТЕРФЕЙС PRIME BROK ---

st.set_page_config(page_title="PrimeBrok Calculator", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🚢 PrimeBrok Pro")
st.write("### Система точного прорахунку вартості авто")

col_main, col_res = st.columns([2, 1])

with col_main:
    c1, c2 = st.columns(2)
    with c1:
        bid = st.number_input("Ставка на аукціоні ($)", value=5000, step=100)
        engine = st.selectbox("Двигун", ["Бензин", "Дизель", "Гібрид", "Електро"])
        body = st.selectbox("Кузов", ["Седан", "SUV / Кросовер", "Пікап / Мінівен"])
    with c2:
        city = st.selectbox("Локація аукціону (City)", sorted(list(LOCATIONS.keys())))
        year = st.number_input("Рік випуску", 2010, 2026, 2020)
        volume = st.number_input("Об'єм (см³)", value=2000)

# --- ЛОГІКА ОБЧИСЛЕНЬ ---
loc_info = LOCATIONS[city]
land_price = loc_info['price']

# Доплати за тип кузова (з таблиці BASE)
if body == "SUV / Кросовер": land_price += 150
if body == "Пікап / Мінівен": land_price += 300

# Доплата за Гібрид/Електро (Ваша умова)
is_special = engine in ["Електро", "Гібрид"]
if is_special: land_price += 200

# Море (середній тариф по портах)
sea_rates = {"NJ": 1100, "GA": 1200, "TX": 1150, "CA": 1350, "WA": 1400}
sea_freight = sea_rates[loc_info['port']]

auction_fee = get_auction_fee(bid)
customs = calc_customs(bid, engine, volume, year)
swift = 166

total_cost = bid + auction_fee + land_price + sea_freight + swift + customs

# --- ВИВІД ---
with col_res:
    st.subheader("📊 Деталізація")
    st.metric("Аукціон + Swift", f"${int(bid + auction_fee + swift)}")
    st.metric("Доставка (Суша+Море)", f"${int(land_price + sea_freight)}")
    st.metric("Розмитнення", f"${int(customs)}")
    st.divider()
    st.success(f"## ВСЬОГО: ${int(total_cost)}")
    
    if is_special:
        st.caption("ℹ️ Доставка дорожча (Електро/Гібрид), мито за пільговим тарифом.")

st.info(f"📍 Найближчий порт: {loc_info['port']} | Тип розрахунку: {engine}")
