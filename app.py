import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="PrimeBrok AI Pro", page_icon="🌎", layout="wide")

# --- ПОЛНАЯ БАЗА ТАРИФОВ (ИЗ ВАШИХ ВКЛАДОК TOW) ---
TOWING_DATA = {
    "NJ (New Jersey)": 175, "GA (Georgia)": 250, "TX (Texas)": 325,
    "CA (California)": 450, "WA (Washington)": 500, "FL (Florida)": 275,
    "IL (Illinois)": 350, "NY (New York)": 200, "MA (Massachusetts)": 210,
    "PA (Pennsylvania)": 190, "OH (Ohio)": 280, "VA (Virginia)": 230,
    "SC (South Carolina)": 240, "AL (Alabama)": 260
}

# Карта для авто-подбора штата из текста аукциона
STATE_LOOKUP = {
    "NJ": "NJ (New Jersey)", "NEW JERSEY": "NJ (New Jersey)",
    "GA": "GA (Georgia)", "GEORGIA": "GA (Georgia)",
    "TX": "TX (Texas)", "TEXAS": "TX (Texas)",
    "CA": "CA (California)", "CALIFORNIA": "CA (California)",
    "WA": "WA (Washington)", "WASHINGTON": "WA (Washington)",
    "FL": "FL (Florida)", "FLORIDA": "FL (Florida)",
    "IL": "IL (Illinois)", "ILLINOIS": "IL (Illinois)",
    "NY": "NY (New York)", "NEW YORK": "NY (New York)"
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

# --- РОБОТ-ЛОГИСТ v4.0 ---
def fetch_lot_details(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().upper() # Переводим в верхний регистр для поиска
            
            # 1. Поиск Марки/Модели
            title = soup.title.string.upper() if soup.title else ""
            car_name = "НЕИЗВЕСТНОЕ АВТО"
            match_car = re.findall(r'(?:20\d{2})\s+([A-Z0-0\s\-]+)\s+(?:LOT|STOCK)', title)
            if match_car: car_name = match_car[0].strip()

            # 2. Поиск Года
            year_match = re.search(r'(20\d{2})', text)
            year = int(year_match.group(1)) if year_match else 2018
            
            # 3. Поиск Двигателя
            engine_match = re.search(r'(\d\.\d)L', text)
            engine = float(engine_match.group(1)) if engine_match else 2.0
            
            # 4. АВТО-ОПРЕДЕЛЕНИЕ ЛОКАЦИИ (Геолокация аукциона)
            detected_state = "NJ (New Jersey)" # По умолчанию
            for key, full_name in STATE_LOOKUP.items():
                if f" {key} " in text or f", {key}" in text:
                    detected_state = full_name
                    break
            
            return {"year": year, "engine": engine, "brand": car_name, "state": detected_state, "status": "success"}
        return {"status": "blocked"}
    except:
        return {"status": "error"}

# --- ИНТЕРФЕЙС ---
st.title("🏯 PrimeBrok AI: Smart Logistics")

url_input = st.text_input("🔗 Вставьте ссылку на Copart/IAAI для авто-расчета", key="main_url")

# Сессия для хранения данных
if 'data' not in st.session_state:
    st.session_state.data = {"year": 2018, "engine": 2.0, "brand": "", "state": "NJ (New Jersey)"}

if url_input:
    if st.button("🚀 ЗАПУСТИТЬ АВТО-ПОДБОР"):
        with st.spinner("Считываю локацию и параметры лота..."):
            res = fetch_lot_details(url_input)
            if res["status"] == "success":
                st.session_state.data = res
                st.success(f"✅ Локация определена: {res['state']}. Данные подтянуты!")
            else:
                st.error("❌ Не удалось считать данные. Выберите штат вручную.")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌎 Геолокация и Логистика")
    bid = st.number_input("Ставка (Bid), $", min_value=0, value=2000)
    
    # Авто-выбор штата из сессии
    current_state_list = list(TOWING_DATA.keys())
    state_index = current_state_list.index(st.session_state.data["state"])
    
    state = st.selectbox("Локация аукциона (TOW FROM)", current_state_list, index=state_index)
    port = st.selectbox("Порт прибытия (SEA TO)", list(SEA_FREIGHT.keys()))

with col2:
    st.subheader("📋 Автомобиль")
    car_name = st.text_input("Марка и Модель", value=st.session_state.data["brand"])
    year = st.number_input("Год", 2000, 2026, value=st.session_state.data["data"]["year"] if "data" in st.session_state.data else st.session_state.data["year"])
    engine = st.number_input("Двигатель (L)", 0.1, 10.0, value=st.session_state.data["engine"])

with col3:
    st.subheader("🧾 Сборы и Налоги")
    customs = st.number_input("Растаможка, $", value=4000)
    broker = st.number_input("Брокер + Экспедитор, $", value=800)
    paid = st.number_input("Уже оплачено, $", value=0)

# Математика
fee = get_auction_fee(bid)
tow = TOWING_DATA[state]
sea = SEA_FREIGHT[port]
total = bid + fee + tow + sea + 166 + 50 + customs + broker

st.markdown("---")
res1, res2, res3 = st.columns(3)
res1.metric("АВТОМОБИЛЬ", f"{car_name} {year}")
res2.metric("ИТОГО (ALL IN)", f"${total:,.0f}")
res3.metric("ЛОКАЦИЯ ОТПРАВКИ", state)

# Блок для отправки клиенту
with st.expander("📲 Сформировать отчет для клиента"):
    report = f"🚗 {car_name} {year}\n📍 Аукцион: {state}\n💰 Ставка: ${bid}\n🚛 Доставка до порта + Море: ${tow+sea}\n🏛️ Растаможка: ${customs}\n🏁 ИТОГО ПОД КЛЮЧ: ${total}"
    st.code(report)
