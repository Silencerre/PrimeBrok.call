import streamlit as st

# --- ПОВНА БАЗА ЛОКАЦІЙ (TOW) ---
# Ваші 5 портів: NJ, GA, TX, CA, WA
TOWING_DATA = {
    "Baltimore (MD)": {"NJ": 325, "GA": 750, "TX": 1250, "CA": 2400, "WA": 2600},
    "Richmond (VA)": {"NJ": 450, "GA": 600, "TX": 1100, "CA": 2300, "WA": 2500},
    "Atlanta (GA)": {"NJ": 850, "GA": 250, "TX": 850, "CA": 2100, "WA": 2400},
    "Chicago (IL)": {"NJ": 750, "GA": 850, "TX": 1050, "CA": 1850, "WA": 1950},
    "Houston (TX)": {"NJ": 1200, "GA": 850, "TX": 200, "CA": 1450, "WA": 1950},
    "Los Angeles (CA)": {"NJ": 2400, "GA": 2100, "TX": 1450, "CA": 200, "WA": 1100},
    "Seattle (WA)": {"NJ": 2600, "GA": 2500, "TX": 1950, "CA": 1100, "WA": 250},
    "Miami (FL)": {"NJ": 950, "GA": 450, "TX": 1100, "CA": 2600, "WA": 2800},
}

# Вартість моря (фрахт) до порту призначення (напр. Констанца)
SEA_RATES = {
    "NJ": 1150,
    "GA": 1250,
    "TX": 1200,
    "CA": 1400,
    "WA": 1500
}

# --- ЛОГІКА РОЗРАХУНКІВ PRIME BROK ---

def get_auction_fee(bid):
    # Динамічна сітка (приклад з вашої таблиці BASE)
    if bid < 500: return 185
    if bid < 1000: return 320
    if bid < 2000: return 485
    if bid < 3000: return 550
    if bid < 5000: return 750
    return bid * 0.14

def calc_customs(bid, engine, vol, yr):
    # Гібрид рахується як бензин по миту (Ваша умова)
    calc_type = "Бензин" if engine == "Гібрид" else engine
    if calc_type == "Електро": return 0 # Пільга
    
    age = 2026 - yr
    if age <= 0: age = 1
    coeff = 50 if calc_type == "Бензин" else 75
    
    accise = (vol / 1000) * coeff * (age if age <= 15 else 15)
    duty = bid * 0.10
    vat = (bid + duty + accise) * 0.20
    return accise + duty + vat

# --- ІНТЕРФЕЙС САЙТУ ---

st.set_page_config(page_title="PrimeBrok - Калькулятор авто", layout="wide", page_icon="🚢")

# Стилізація
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #ffffff; text-align: center; font-family: 'Arial'; }
    .stMetric { border: 1px solid #30363d; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚢 PrimeBrok")
st.write("<p style='text-align: center;'>Професійний розрахунок вартості авто зі США під ключ</p>", unsafe_allow_html=True)

# Введення даних
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📋 Параметри лота")
    c1, c2 = st.columns(2)
    with c1:
        bid = st.number_input("Ставка на аукціоні ($)", value=5000, step=100)
        engine = st.selectbox("Тип двигуна", ["Бензин", "Дизель", "Гібрид", "Електро"])
        year = st.number_input("Рік випуску", 2010, 2026, 2020)
    with c2:
        city = st.selectbox("Місто аукціону (Location)", sorted(list(TOWING_DATA.keys())))
        body = st.selectbox("Тип кузова", ["Седан", "SUV / Кросовер"])
        volume = st.number_input("Об'єм двигуна (см³)", value=2000)

# --- РОЗРАХУНОК ЛОГІКИ ---
possible_ports = TOWING_DATA[city]
# Шукаємо найвигідніший порт для цього міста (Суша + Море)
best_port = min(possible_ports, key=lambda k: possible_ports[k] + SEA_RATES[k])
land_cost = possible_ports[best_port]

# Націнка за SUV
if body == "SUV / Кросовер": land_cost += 150

# Гібрид / Електро: Дорожча доставка (+200$), але мито за специфікою
is_special = engine in ["Електро", "Гібрид"]
if is_special: land_cost += 200

sea_cost = SEA_RATES[best_port]
auction_fee = get_auction_fee(bid)
customs = calc_customs(bid, engine, volume, year)
swift = 166

total_cost = bid + auction_fee + land_cost + sea_cost + swift + customs

# --- ВИВІД РЕЗУЛЬТАТІВ ---
with col_right:
    st.subheader("💰 Розрахунок")
    st.metric("Аукціон + Swift", f"${int(bid + auction_fee + swift)}")
    st.metric("Логістика (Суша+Море)", f"${int(land_cost + sea_cost)}")
    st.metric("Розмитнення", f"${int(customs)}")
    st.divider()
    st.success(f"### ВСЬОГО (ALL IN): ${int(total_cost)}")
    
    if is_special:
        st.info("💡 **Гібрид/Електро**: Доставка дорожча, мито розраховано за пільговими правилами.")

st.caption(f"Автоматичний вибір оптимального порту: **{best_port}**. Розрахунок PrimeBrok не включає брокерські послуги.")
