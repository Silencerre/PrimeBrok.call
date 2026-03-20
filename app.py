import streamlit as st

# --- ЛОГІКА РОЗРАХУНКІВ (БЕЗ КОМІСІЇ) ---

def get_auction_fee(bid):
    # Стандартна сітка зборів Copart/IAAI (можна підправити під ваші точні цифри)
    if bid <= 500: return 175
    elif bid <= 1000: return 250
    elif bid <= 1500: return 365
    elif bid <= 2000: return 450
    elif bid <= 4000: return 600
    elif bid <= 5000: return 700
    else: return bid * 0.12 # Приблизно 12% для високих ставок

def calculate_ua_tax(bid, engine_type, volume, year):
    # Базове розмитнення Україна
    age_coeff = 2026 - year
    if age_coeff <= 0: age_coeff = 1
    if age_coeff > 15: age_coeff = 15
    
    if engine_type == "Електро":
        return 0 # Пільга на електрокари (тільки акциз 1 євро за кВт, що майже 0)
    
    base_tax = 50 if engine_type == "Бензин" else 75
    accise = (volume / 1000) * base_tax * age_coeff
    duty = bid * 0.10
    vat = (bid + duty + accise) * 0.20
    return accise + duty + vat

# --- ВІЗУАЛЬНА ЧАСТИНА (STREAMLIT) ---

st.set_page_config(page_title="PrimeBrok Calc", page_icon="🚢")

# Стиль заголовка
st.markdown("<h1 style='text-align: center; color: #1E1E1E;'>🚢 PrimeBrok</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Калькулятор собівартості авто зі США (без прихованих комісій)</p>", unsafe_allow_html=True)

# Розподіл на колонки для вводу
col1, col2 = st.columns(2)

with col1:
    st.subheader("💵 Аукціон")
    bid = st.number_input("Ставка на аукціоні ($)", min_value=100, value=5000, step=100)
    engine = st.selectbox("Двигун", ["Бензин", "Дизель", "Електро", "Гібрид"])
    year = st.number_input("Рік випуску", min_value=2000, max_value=2026, value=2019)
    volume = st.number_input("Об'єм (см³)", value=2000, step=100)

with col2:
    st.subheader("🚚 Логістика")
    port = st.selectbox("Порт відправки (США)", ["New Jersey", "Savannah", "Houston", "Los Angeles"])
    # Приблизна логістика (суша + море) з вашої таблиці TOW
    towing_map = {"New Jersey": 1450, "Savannah": 1550, "Houston": 1350, "Los Angeles": 1750}
    delivery_total = towing_map[port]
    
    st.subheader("🛡 Додатково")
    insurance = st.checkbox("Страхування (1.5%)", value=True)
    ins_val = bid * 0.015 if insurance else 0
    swift = 166 # Фіксований Swift за вашою таблицею

# --- МАКИМАЛЬНО ТОЧНИЙ ПІДСУМОК ---

a_fee = get_auction_fee(bid)
customs = calculate_ua_tax(bid, engine, volume, year)
total_usa = bid + a_fee + delivery_total + ins_val + swift
grand_total = total_usa + customs

st.divider()

# Вивід результатів
res1, res2, res3 = st.columns(3)
res1.metric("Витрати США", f"${int(total_usa)}")
res2.metric("Розмитнення", f"${int(customs)}")
res3.metric("Разом (ALL IN)", f"${int(grand_total)}")

st.warning("⚠️ **Увага:** У цей розрахунок НЕ включено комісію PrimeBrok та витрати на сертифікацію/облік.")

# Кнопка для зв'язку (опціонально)
if st.button("Отримати консультацію менеджера"):
    st.balloons()
    st.write("Надішліть цей розрахунок нашому менеджеру в Telegram!")
