import streamlit as st

# --- НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(page_title="PrimeBrok Intelligence", page_icon="🏎️", layout="wide")

# --- ЛОГІКА ТАРИФІВ (З ВАШОЇ ТАБЛИЦІ) ---

# Ціни на евакуатор (TOW) за штатами
TOWING_DATA = {
    "NJ (New Jersey)": 175,
    "GA (Georgia)": 250,
    "TX (Texas)": 325,
    "CA (California)": 450,
    "WA (Washington)": 500,
    "FL (Florida)": 275,
    "IL (Illinois)": 350,
    "NY (New York)": 200,
    "MD (Maryland)": 225
}

# Морський фрахт (Sea Freight)
SEA_FREIGHT = {
    "Constanta (Romania)": 2850,
    "Odesa (Ukraine)": 3100,
    "Klaipeda (Lithuania)": 2950,
    "Gdynia (Poland)": 3000
}

# Розрахунок збору аукціону за вашою сіткою (Fees)
def get_auction_fee(bid):
    if bid < 100: return 50
    elif bid < 500: return 200
    elif bid < 1000: return 350
    elif bid < 2000: return 500
    elif bid < 3000: return 650
    elif bid < 4000: return 750
    elif bid < 5000: return 800
    else: return 950 # Приблизний максимум для високих ставок

# --- СТИЛІЗАЦІЯ ІНТЕРФЕЙСУ ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stNumberInput, .stSelectbox, .stTextInput { border-radius: 8px !important; }
    .css-1kyxreq { justify-content: center; }
    .result-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- ШАПКА САЙТУ ---
st.title("🏯 PrimeBrok Global Logistics")
st.markdown("#### Професійний розрахунок лотів Copart та IAAI")

# --- ВВІД ДАНИХ ---
lot_url = st.text_input("🔗 Посилання на лот (Copart/IAAI/Impact)", placeholder="Вставте посилання тут...")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📍 Локація та Лот")
    bid = st.number_input("Ставка аукціону (Bid), $", min_value=0, value=2000, step=100)
    state = st.selectbox("Штат відправки (TOW)", list(TOWING_DATA.keys()))
    port = st.selectbox("Порт призначення (Sea)", list(SEA_FREIGHT.keys()))

with col2:
    st.info("⚙️ Параметри авто")
    year = st.number_input("Рік випуску", 2000, 2026, 2018)
    engine = st.number_input("Об'єм двигуна", 0.1, 10.0, 2.0)
    fuel = st.selectbox("Тип палива", ["Бензин", "Дизель", "Гібрид", "Електро"])

with col3:
    st.info("💰 Фінанси та Митниця")
    customs = st.number_input("Митні платежі, $", value=3500)
    broker_fees = st.number_input("Брокер + Експедитор, $", value=800)
    already_paid = st.number_input("Вже сплачено клієнтом, $", value=0)

# --- РОЗРАХУНКОВА ЧАСТИНА ---
auction_fee = get_auction_fee(bid)
tow_cost = TOWING_DATA[state]
sea_cost = SEA_FREIGHT[port]
swift = 166
insurance = 50

# Загальна сума
total_all_in = bid + auction_fee + tow_cost + sea_cost + swift + insurance + customs + broker_fees
remaining_debt = total_all_in - already_paid

# --- ВИВІД РЕЗУЛЬТАТІВ ---
st.markdown("---")
st.subheader("📊 Підсумок розрахунку")

res_col1, res_col2, res_col3, res_col4 = st.columns(4)

with res_col1:
    st.metric("TOTAL ALL IN", f"${total_all_in:,.0f}")
with res_col2:
    st.metric("ДОСТАВКА РАЗОМ", f"${tow_cost + sea_cost:,.0f}")
with res_col3:
    st.metric("ЗБІР АУКЦІОНУ", f"${auction_fee}")
with res_col4:
    if remaining_debt > 0:
        st.error(f"ЗАЛИШОК: ${remaining_debt:,.0f}")
    else:
        st.success("ОПЛАЧЕНО")

# ДЕТАЛІЗАЦІЯ
with st.expander("📝 Повна деталізація (можна копіювати клієнту)"):
    summary_text = f"""
    🚗 **Розрахунок лоту:** {lot_url if lot_url else 'Без посилання'}
    ---------------------------------
    🔹 **Аукціон:** ${bid} (ставка) + ${auction_fee} (збір) + ${swift} (SWIFT) = **${bid+auction_fee+swift}**
    🔹 **Логістика:** ${tow_cost} (TOW) + ${sea_cost} (Sea) + ${insurance} (Ins) = **${tow_cost+sea_cost+insurance}**
    🔹 **Оформлення:** ${customs} (Мито) + ${broker_fees} (Сервіс) = **${customs+broker_fees}**
    ---------------------------------
    🏁 **РАЗОМ ПО КЛЮЧУ: ${total_all_in:,.0f}**
    """
    st.code(summary_text, language="markdown")

st.markdown("---")
st.caption("PrimeBrok Call System v2.0 | Дані базуються на вашій Google Таблиці")
