import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# --- НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(page_title="PrimeBrok AI Scanner", page_icon="🤖", layout="wide")

# --- БАЗА ДАНИХ (ЛОГІКА ТАБЛИЦІ) ---
TOWING_DATA = {
    "NJ (New Jersey)": 175, "GA (Georgia)": 250, "TX (Texas)": 325,
    "CA (California)": 450, "WA (Washington)": 500, "FL (Florida)": 275,
    "IL (Illinois)": 350, "NY (New York)": 200
}

SEA_FREIGHT = {
    "Constanta (Romania)": 2850, "Odesa (Ukraine)": 3100, "Klaipeda (Lithuania)": 2950
}

def get_auction_fee(bid):
    if bid < 100: return 50
    elif bid < 1000: return 350
    elif bid < 2000: return 500
    elif bid < 4000: return 750
    return 900

# --- РОБОТ-ЗЧИТУВАЧ (PARSER) ---
def fetch_lot_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text()
            
            # Пошук року (4 цифри поспіль)
            year_match = re.search(r'(20\d{2})', page_text)
            year = int(year_match.group(1)) if year_match else 2018
            
            # Пошук об'єму двигуна (напр. 2.0L або 2.5)
            engine_match = re.search(r'(\d\.\d)L?', page_text)
            engine = float(engine_match.group(1)) if engine_match else 2.0
            
            return {"year": year, "engine": engine, "status": "success"}
        else:
            return {"status": "blocked"}
    except:
        return {"status": "error"}

# --- ІНТЕРФЕЙС ---
st.title("🏯 PrimeBrok AI Intelligence")

# Поле для посилання
url_input = st.text_input("🔗 Вставте посилання на лот (Copart/IAAI)", placeholder="https://www.copart.com/lot/...")

# Кнопка запуску робота
scanned_year = 2018
scanned_engine = 2.0

if url_input:
    if st.button("🤖 Зчитати дані лота"):
        with st.spinner("Робот заходить на аукціон..."):
            result = fetch_lot_data(url_input)
            if result["status"] == "success":
                scanned_year = result["year"]
                scanned_engine = result["engine"]
                st.success(f"Дані отримано! Рік: {scanned_year}, Двигун: {scanned_engine}")
            else:
                st.warning("Аукціон заблокував запит. Введіть дані вручну, але посилання збережено.")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📍 Логістика")
    bid = st.number_input("Ставка (Bid), $", min_value=0, value=2000)
    state = st.selectbox("Штат (TOW)", list(TOWING_DATA.keys()))
    port = st.selectbox("Порт (Sea)", list(SEA_FREIGHT.keys()))

with col2:
    st.subheader("⚙️ Авто")
    year = st.number_input("Рік випуску", 2000, 2026, value=scanned_year)
    engine = st.number_input("Двигун (л)", 0.1, 10.0, value=scanned_engine)
    fuel = st.selectbox("Паливо", ["Бензин", "Дизель", "Гібрид", "Електро"])

with col3:
    st.subheader("💰 Оформлення")
    customs = st.number_input("Митниця, $", value=3500)
    broker = st.number_input("Сервіс, $", value=800)
    paid = st.number_input("Сплачено, $", value=0)

# Розрахунок
fee = get_auction_fee(bid)
total = bid + fee + TOWING_DATA[state] + SEA_FREIGHT[port] + 166 + 50 + customs + broker

st.markdown("---")
res1, res2 = st.columns(2)
res1.metric("ALL IN TOTAL", f"${total:,.0f}")
res2.metric("БОРГ", f"${total - paid:,.0f}")

with st.expander("📝 Звіт для клієнта"):
    st.code(f"Лот: {url_input}\nРік: {year}\nДвигун: {engine}\nСума під ключ: ${total}")
