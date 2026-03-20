import streamlit as st

# Налаштування сторінки
st.set_page_config(page_title="PrimeBrok Logistics", layout="wide")

# Стилізація для "дорогого" вигляду
st.markdown("""
    <style>
    .stNumberInput input { font-size: 1.2rem !important; font-weight: bold; }
    .result-box { padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 10px; color: white; }
    .all-in { background-color: #d32f2f; }
    .paid { background-color: #388e3c; }
    .debt { background-color: #1976d2; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚢 PrimeBrok — Система логістики")
st.markdown("---")

# ОСНОВНА СІТКА (ЯК У ВАШІЙ ТАБЛИЦІ)
col_left, col_mid, col_right = st.columns([1, 1, 1])

with col_left:
    st.subheader("📋 Дані аукціону")
    auction = st.selectbox("Тип аукціону", ["IAAI", "COPART", "Other"])
    location = st.text_input("Локація (наприклад, Atlanta GA)")
    bid = st.number_input("Ставка ($)", min_value=0.0, step=50.0, value=0.0)
    auction_fee = st.number_input("Збір Аукціону ($)", min_value=0.0, value=0.0)
    swift_fee = st.number_input("Swift Аукціон ($)", min_value=0.0, value=0.0)

with col_mid:
    st.subheader("🚢 Логістика")
    destination = st.selectbox("Порт призначення", ["Constanta", "Odesa", "Klaipeda", "Poti"])
    fuel_type = st.selectbox("Тип палива / Завантаження", ["GAS", "EV", "Diesel", "Hybrid", "Moto", "GAS 3", "GAS 2"])
    
    st.write("**Транспортні витрати**")
    land_cost = st.number_input("Суша ($)", min_value=0.0, value=0.0)
    sea_cost = st.number_input("Море ($)", min_value=0.0, value=0.0)
    
    storage = st.number_input("Storage (Парковка) ($)", min_value=0.0, value=0.0)

with col_right:
    st.subheader("📂 Додатково")
    insurance = st.number_input("Страхування ($)", min_value=0.0, value=0.0)
    customs = st.number_input("Митні Платежі ($)", min_value=0.0, value=0.0)
    other = st.number_input("Інше ($)", min_value=0.0, value=0.0)
    
    st.markdown("---")
    paid_amount = st.number_input("ВЖЕ ОПЛАЧЕНО (PAID) ($)", min_value=0.0, value=0.0)

# --- ЛОГІКА РОЗРАХУНКУ (ВСЕ ЯК У ТАБЛИЦІ) ---
total_transport = land_cost + sea_cost
# ALL IN = Сума всіх витрат
all_in = bid + auction_fee + swift_fee + total_transport + insurance + storage + customs + other
# DEBT = Залишок до сплати
debt = all_in - paid_amount

# --- ВІЗУАЛЬНИЙ ПІДСУМОК ---
st.markdown("---")
res_col1, res_col2, res_col3 = st.columns(3)

with res_col1:
    st.markdown(f'<div class="result-box all-in"><h3>ALL IN</h3><h2>${all_in:,.2f}</h2></div>', unsafe_allow_html=True)

with res_col2:
    st.markdown(f'<div class="result-box paid"><h3>PAID</h3><h2>${paid_amount:,.2f}</h2></div>', unsafe_allow_html=True)

with res_col3:
    st.markdown(f'<div class="result-box debt"><h3>DEBT</h3><h2>${debt:,.2f}</h2></div>', unsafe_allow_html=True)

# Деталізація для перевірки
with st.expander("Розгорнути деталізацію витрат"):
    st.write(f"**Вартість авто на аукціоні:** ${bid + auction_fee + swift_fee}")
    st.write(f"**Загальна логістика:** ${total_transport}")
    st.write(f"**Митниця та інше:** ${customs + insurance + other + storage}")

st.caption("PrimeBrok | Весь функціонал таблиці перенесено.")
