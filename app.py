import streamlit as st

# --- ПОВНА БАЗА ЛОКАЦІЙ (TOW) ---
# Для кожного міста вказані ціни трала до ваших 5 портів
TOWING_DATA = {
    "Baltimore (MD)": {"NJ": 325, "GA": 750, "TX": 1250, "CA": 2400, "WA": 2600},
    "Richmond (VA)": {"NJ": 450, "GA": 600, "TX": 1100, "CA": 2300, "WA": 2500},
    "Atlanta (GA)": {"NJ": 850, "GA": 250, "TX": 850, "CA": 2100, "WA": 2400},
    "Chicago (IL)": {"NJ": 750, "GA": 850, "TX": 1050, "CA": 1850, "WA": 1950},
    "Houston (TX)": {"NJ": 1200, "GA": 850, "TX": 200, "CA": 1450, "WA": 1950},
    "Los Angeles (CA)": {"NJ": 2400, "GA": 2100, "TX": 1450, "CA": 200, "WA": 1100},
    "Seattle (WA)": {"NJ": 2600, "GA": 2500, "TX": 1950, "CA": 1100, "WA": 250},
}

# Вартість морю (фрахт) до Констанци за портами
SEA_RATES = {
    "NJ": 1150,
    "GA": 1250,
    "TX": 1200,
    "CA": 1400,
    "WA": 1500
}

# --- ЛОГІКА PRIME BROK ---

def get_auction_fee(bid):
    if bid < 500: return 185
    if bid < 1000: return 320
    if bid < 3000: return 550
    if bid < 5000: return 750
    return bid * 0.14

def calc_customs(bid, engine, vol, yr):
    # Гібрид = Бензин (Мито), Електро = 0
    calc_type = "Бензин" if engine == "Гібрид" else engine
    if calc_type == "Електро": return 0
    
    age = 2026 - yr
    if age <= 0: age = 1
    coeff = 50 if calc_type == "Бензин" else 75
    accise = (vol / 1000) * coeff * (age if age <= 15 else 15)
    duty = bid * 0.10
    vat = (bid + duty + accise) * 0.20
    return accise + duty + vat

# --- ІНТЕРФЕЙС ---

st.set_page_config(page_title="PrimeBrok Pro", layout="wide")
st.title("🚢 PrimeBrok: Розумна Логістика (NJ, GA, TX, CA, WA)")

with st.sidebar:
    st.header("📋 Параметри")
    bid = st.number_input("Ставка ($)", value=5000)
    engine = st.selectbox("Двигун", ["Бензин", "Дизель", "Гібрид", "Електро"])
    body = st.selectbox("Кузов", ["Седан", "SUV / Кросовер"])
    year = st.number_input("Рік", 2010, 2026, 2020)
    volume = st.number_input("Об'єм (см³)", value=2000)
    city = st.selectbox("Місто аукціону", sorted(list(TOWING_DATA.keys())))

# РОЗРАХУНОК
possible_ports = TOWING_DATA[city]
# Знаходимо найвигідніший порт для цього міста
best_port = min(possible_ports, key=lambda k: possible_ports[k] + SEA_RATES[k])
land_cost = possible_ports[best_port]

# Націнка за кузов
if body == "SUV / Кросовер": land_cost += 150

# Гібрид/Електро: Доставка дорожча (+200 за вашою логікою)
is_special = engine in ["Електро", "Гібрид"]
if is_special: land_cost += 200

sea_cost = SEA_RATES[best_port]
customs = calc_customs(bid, engine, volume, year)
total = bid + get_auction_fee(bid) + land_cost + sea_cost + 166 + customs

# ВИВІД
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Трал (Суша)", f"${int(land_cost)}")
    st.caption(f"Напрямок: {city} ➔ {best_port}")
with c2:
    st.metric("Морський фрахт", f"${int(sea_cost)}")
    st.caption(f"Порт відправки: {best_port}")
with c3:
    st.metric("Митні платежі", f"${int(customs)}")
    st.caption("По бензиновій сітці" if engine == "Гібрид" else "")

st.divider()
st.success(f"## 🔥 ПІДСУМКОВА ВАРТІСТЬ ALL IN: ${int(total)}")

if is_special:
    st.info("💡 Увага: Для Гібридів та Електрокарів логістика розрахована за спеціальним тарифом.")
