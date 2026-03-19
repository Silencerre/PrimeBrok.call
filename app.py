import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# --- НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(page_title="PrimeBrok AI Pro", page_icon="🌎", layout="wide")

# --- БАЗА ТАРИФІВ (TOW) ---
TOWING_DATA = {
    "NJ (New Jersey)": 175, "GA (Georgia)": 250, "TX (Texas)": 325,
    "CA (California)": 450, "WA (Washington)": 500, "FL (Florida)": 275,
    "IL (Illinois)": 350, "NY (New York)": 200, "MA (Massachusetts)": 210,
    "PA (Pennsylvania)": 190, "OH (Ohio)": 280, "VA (Virginia)": 230
}

STATE_LOOKUP = {
    "NJ": "NJ (New Jersey)", "GA": "GA (Georgia)", "TX": "TX (Texas)",
    "CA": "CA (California)", "WA": "WA (Washington)", "FL": "FL (Florida)",
    "IL": "IL (Illinois)", "NY": "NY (New York)"
}

SEA_FREIGHT = {
    "Constanta (Romania)": 2850, "Odesa (Ukraine)": 3100, "Klaipeda (Lithuania)": 2950
}

def get_auction_fee(bid):
    if bid < 100: return 50
    elif bid < 1000: return 350
    elif bid < 2000: return 540
    elif bid < 3000: return 680
    elif bid < 5000: return 790
    return 950

# --- РОБОТ-ЛОГІСТ v4.1 (ВИПРАВЛЕНИЙ) ---
def fetch_lot_details(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().upper()
            title = soup.title.string.upper() if soup.title else ""
            
            # Марка/Модель
            car_name = "АВТОМОБІЛЬ"
            match_car = re.findall(r'(?:20\d{2})\s+([A-Z0-9\s\-]+)\s+(?:LOT|STOCK)', title)
            if match_car: car_name = match_car[0].strip()

            # Рік (з перевіркою меж)
            year_match = re.search(r'(20\d{2})', text)
            year = int(year_match.group(1)) if year_match else 2018
            year = max(2000, min(2026, year)) # Запобіжник меж
            
            # Двигун
            engine_match = re.search(r'(\d\.\d)L', text)
            engine = float(engine_match.group(1)) if engine_match else 2.0
            
            # Геолокація
            detected_state = "NJ (New Jersey)"
            for key, full_name in STATE_LOOKUP.items():
                if f" {key} " in text or f", {key}" in text:
                    detected_state = full_name
                    break
            
            return {"year": year, "engine": engine, "brand": car_name, "state": detected_state, "status": "success"}
        return {"status": "blocked"}
    except:
        return {"status": "error"}

# --- СЕСІЯ (БЕЗ ПОМИЛОК) ---
if 'car' not in st.session_state:
    st.session_state.car = {"year": 2018, "engine": 2.0, "brand": "", "state": "NJ (New Jersey)"}

st.title("🏯 PrimeBrok AI: Smart Logistics")

url_input = st.text_input("🔗 Вставте посилання на лот")

if url_input and st.button("🚀 ЗАПУСТИТЬ АВТО-ПОДБОР"):
    with st.spinner("Считую локацію та параметри лота..."):
        res = fetch_lot_details(url_input)
        if res["status"] == "success":
            st.session_state.car = res
            st.success(f"✅ Локація: {res['state']} | Авто: {res['brand']}")
        else:
            st.error("❌ Не вдалося отримати дані. Введіть вручну.")

st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌎 Геолокація")
    bid = st.number_input("Ставка (Bid), $", min_value=0, value=2000)
    
    current_states = list(TOWING_DATA.keys())
    # Авто-вибір штату
    default_state_idx = current_states.index(st.session_state.car["state"])
    state = st.selectbox("Локація аукціона", current_states, index=default_state_idx)
    port = st.selectbox("Порт призначення", list(SEA_FREIGHT.keys()))

with col2:
    st.subheader("📋 Автомобіль")
    brand = st.text_input("Марка і Модель", value=st.session_state.car["brand"])
    # Використовуємо змінні з сесії з перевіркою
    year = st.number_input("Рік", 2000, 2026, value=int(st.session_state.car["year"]))
    engine = st.number_input("Двигун (L)", 0.1, 10.0, value=float(st.session_state.car["engine"]))

with col3:
    st.subheader("🧾 Оплати")
    customs = st.number_input("Растаможка, $", value=3500)
    broker = st.number_input("Брокер + Експедитор, $", value=800)
    paid = st.number_input("Уже оплачено, $", value=0)

# Розрахунок
fee = get_auction_fee(bid)
tow = TOWING_DATA[state]
sea = SEA_FREIGHT[port]
total = bid + fee + tow + sea + 166 + 50 + customs + broker

st.markdown("---")
res1, res2, res3 = st.columns(3)
res1.metric("АВТО", f"{brand} {year}")
res2.metric("ИТОГО ПО КЛЮЧУ", f"${total:,.0f}")
res3.metric("ЛОКАЦІЯ", state)

with st.expander("📲 Звіт для клієнта"):
    st.code(f"🚗 {brand} {year}\n📍 Аукціон: {state}\n💰 Ставка: ${bid}\n🚛 Логістика: ${tow+sea}\n🏁 TOTAL: ${total}")
