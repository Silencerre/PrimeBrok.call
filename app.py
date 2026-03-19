import streamlit as st

# Налаштування сторінки
st.set_page_config(page_title="PrimeBrok Calculator", page_icon="📈", layout="wide")

# --- ЛОГІКА ТАБЛИЦІ (Константи з вашого файлу) ---
# Ви можете змінювати ці цифри прямо тут, якщо тарифи зміняться
SWIFT_FEE = 166
INSURANCE = 50
STORAGE_DEFAULT = 0

# --- ІНТЕРФЕЙС ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>📈 PrimeBrok Calculator</h1>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("📍 Локація та Авто")
    year = st.number_input("Рік авто", min_value=1990, max_value=2026, value=2008)
    selected_loc = st.selectbox("Звідки (Аукціон)", ["ALBANY", "NEWARK", "SAVANNAH", "HOUSTON", "LOS ANGELES"])
    selected_port = st.selectbox("Куди (Порт)", ["Constanta", "Odesa", "Klaipeda"])
    fuel = st.selectbox("Тип палива", ["GAS", "Diesel", "HYB", "EV"])

with col2:
    st.subheader("📝 Вартість")
    bid = st.number_input("Ставка на аукціоні, $", min_value=0, value=2000, step=100)
    # Автоматичний збір (можна ускладнити за вашою сіткою пізніше)
    auction_fee = st.number_input("Збір Аукціону, $", value=630)
    # Транспорт (евакуатор + доставка)
    transport = st.number_input("Транспорт (TOW + Sea), $", value=3060)

with col3:
    st.subheader("💰 Митниця та Оплата")
    customs = st.number_input("Митні платежі, $", value=4504)
    other_fees = st.number_input("Інші витрати (Брокер тощо), $", value=0)
    paid_amount = st.number_input("Вже оплачено клієнтом, $", value=0)

# --- РОЗРАХУНОК ЗА ВАШОЮ ФОРМУЛОЮ ---
# ALL IN = Ставка + Збір + Swift + Транспорт + Страховка + Митниця + Інше
total_all_in = bid + auction_fee + SWIFT_FEE + transport + INSURANCE + customs + other_fees
debt = total_all_in - paid_amount

st.markdown("---")
res_col1, res_col2, res_col3 = st.columns(3)

with res_col1:
    st.metric("ЗАГАЛЬНИЙ ALL IN", f"${total_all_in:,.0f}")
with res_col2:
    st.metric("БЕЗ МИТНИЦІ", f"${total_all_in - customs:,.0f}")
with res_col3:
    if debt > 0:
        st.error(f"ЗАЛИШОК ДО ОПЛАТИ: ${debt:,.0f}")
    else:
        st.success("ПОВНІСТЮ ОПЛАЧЕНО")

st.info(f"В розрахунок включено: Swift (${SWIFT_FEE}) та Страхування (${INSURANCE})")
