import streamlit as st

# Налаштування сторінки
st.set_page_config(page_title="PrimeBrok - Професійний Калькулятор", page_icon="🚗", layout="wide")

# --- СТИЛІЗАЦІЯ ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1 { color: #1E3A8A; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

# --- ЛОГІКА ТАРИФІВ (ВИЯВЛЕНО В ТАБЛИЦІ) ---
def get_auction_fee(bid):
    if bid < 500: return 250
    if bid < 1000: return 350
    if bid < 2000: return 500
    if bid < 3000: return 630
    if bid < 4000: return 750
    return 850  # Спрощена сітка з вашої таблиці

def get_towing_cost(location):
    # Логіка з вашої вкладки TOW
    costs = {
        "ALBANY": 200, "NEWARK": 150, "SAVANNAH": 250, 
        "HOUSTON": 300, "LOS ANGELES": 450, "CHICAGO": 350
    }
    return costs.get(location, 250)

# --- ІНТЕРФЕЙС ---
st.title("🏯 PrimeBrok Intelligence")
st.subheader("Повний розрахунок вартості авто з США")

# Основна форма
with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📍 ПОХОДЖЕННЯ")
        bid = st.number_input("Ставка аукціону (Bid), $", min_value=0, value=2000, step=100)
        location = st.selectbox("Локація (Площадка)", ["ALBANY", "NEWARK", "SAVANNAH", "HOUSTON", "LOS ANGELES", "CHICAGO"])
        port = st.selectbox("Порт призначення", ["Constanta", "Odesa", "Klaipeda"])
        
    with col2:
        st.info("📝 ТЕХНІЧНІ ДАНІ")
        year = st.number_input("Рік випуску", 1990, 2026, 2008)
        engine = st.number_input("Об'єм двигуна (л)", 0.1, 10.0, 2.0)
        fuel = st.selectbox("Тип палива", ["Бензин", "Дизель", "Гібрид", "Електро"])
        
    with col3:
        st.info("💰 ФІНАНСИ")
        customs = st.number_input("Митне очищення, $", value=4504)
        broker = st.number_input("Брокер + Експедитор, $", value=800)
        paid = st.number_input("Внесена оплата, $", value=0)

# --- РОЗРАХУНОК ---
fee = get_auction_fee(bid)
tow = get_towing_cost(location)
sea_freight = 2860 if port == "Constanta" else 3000 # Приклад логіки моря
swift = 166
insurance = 50

total_transport = tow + sea_freight
total_all_in = bid + fee + swift + total_transport + insurance + customs + broker
current_debt = total_all_in - paid

# --- РЕЗУЛЬТАТИ ---
st.markdown("---")
res1, res2, res3, res4 = st.columns(4)

res1.metric("ALL IN (ПОВНИЙ)", f"${total_all_in:,.0f}")
res2.metric("АУКЦІОННИЙ ЗБІР", f"${fee}")
res3.metric("ЛОГІСТИКА", f"${total_transport}")
if current_debt > 0:
    res4.error(f"БОРГ: ${current_debt:,.0f}")
else:
    res4.success("ОПЛАЧЕНО")

# Деталізація для клієнта
with st.expander("📊 Детальна специфікація витрат"):
    st.write(f"**Аукціон:** ${bid} (Ставка) + ${fee} (Збір) + ${swift} (Swift) = **${bid+fee+swift}**")
    st.write(f"**Доставка:** ${tow} (Евакуатор) + ${sea_freight} (Море) + ${insurance} (Страховка) = **${total_transport+insurance}**")
    st.write(f"**Митниця та сервіс:** ${customs} (Мито) + ${broker} (Брокер) = **${customs+broker}**")
