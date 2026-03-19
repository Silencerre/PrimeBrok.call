import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# --- НАСТРОЙКИ СТОРІНКИ ---
st.set_page_config(page_title="PrimeBrok Logistics Pro", page_icon="⚓", layout="wide")

# --- ЛОГІКА СКЛАДІВ ТА ПОРТІВ (З ВАШОЇ ТАБЛИЦІ) ---
# Ключ: Порт виходу в США. Значення: Ціна евакуатора (середня по штату до цього порту)
US_EXIT_PORTS = {
    "Port of Newark (NJ)": 175,
    "Port of Savannah (GA)": 250,
    "Port of Houston (TX)": 325,
    "Port of Los Angeles (CA)": 450,
    "Port of Miami (FL)": 275,
    "Port of Chicago (IL)": 350
}

# Карта відповідності штатів до найближчих портів виходу
STATE_TO_EXIT_PORT = {
    "NJ": "Port of Newark (NJ)", "NY": "Port of Newark (NJ)", "PA": "Port of Newark (NJ)",
    "GA": "Port of Savannah (GA)", "SC": "Port of Savannah (GA)",
    "TX": "Port of Houston (TX)", "LA": "Port of Houston (TX)",
    "CA": "Port of Los Angeles (CA)", "WA": "Port of Los Angeles (CA)",
    "FL": "Port of Miami (FL)",
    "IL": "Port of Chicago (IL)", "OH": "Port of Chicago (IL)"
}

SEA_FREIGHT = {
    "Constanta (Romania)": 2850,
    "Odesa (Ukraine)": 3100,
    "Klaipeda (Lithuania)": 2950
}

def get_auction_fee(bid):
    if bid < 100: return 50
    elif bid < 1000: return 350
    elif bid < 2000: return 540
    elif bid < 5000: return 790
    return 950

# --- РОБОТ-ЛОГІСТ v5.0 ---
def fetch_full_logic(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().upper()
            
            # Пошук локації аукціона (місто, штат)
            auction_loc = "Unknown"
            state_found = "NJ"
            # Шукаємо комбінації типу "HOUSTON, TX" або "NEWARK, NJ"
            loc_match = re.search(r'([A-Z\s]+),\s([A-Z]{2})', text)
            if loc_match:
                auction_loc = f"{loc_match.group(1).strip()}, {loc_match.group(2)}"
                state_found = loc_match.group(2)

            # Визначаємо порт виходу на основі штату
            exit_port = STATE_TO_EXIT_PORT.get(state_found, "Port of Newark (NJ)")

            # Дані авто
            year_match = re.search(r'(20\d{2})', text)
            year = max(2000, min(2026, int(year_match.group(1)))) if year_match else 2018
            
            engine_match = re.search(r'(\d\.\d)L', text)
            engine = float(engine_match.group(1)) if engine_match else 2.0

            return {
                "auction_loc": auction_loc,
                "exit_port": exit_port,
                "year": year,
                "engine": engine,
                "status": "success"
            }
    except:
        pass
    return {"status": "error"}

# --- СЕСІЯ ---
if 'logistics' not in st.session_state:
    st.session_state.logistics = {
        "auction_loc": "Оберіть лот", 
        "exit_port": "Port of Newark (NJ)", 
        "year": 2018, "engine": 2.0
    }

st.title("🏯 PrimeBrok: Повний логістичний ланцюг")

url_input = st.text_input("🔗 Посилання на лот для повного прорахунку шляху")

if url_input and st.button("🚀 РОЗРАХУВАТИ ЛОГІСТИКУ"):
    with st.spinner("Прокладаю маршрут США -> Європа..."):
        res = fetch_full_logic(url_input)
        if res["status"] == "success":
            st.session_state.logistics = res
            st.success(f"✅ Маршрут знайдено: {res['auction_loc']} -> {res['exit_port']}")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🇺🇸 Логістика в США")
    # Показуємо конкретне місто аукціона
    st.warning(f"📍 Аукціон: {st.session_state.logistics['auction_loc']}")
    
    bid = st.number_input("Ставка (Bid), $", min_value=0, value=2000)
    
    # Вибір порта виходу (автоматично підтягнутий)
    exit_list = list(US_EXIT_PORTS.keys())
    exit_idx = exit_list.index(st.session_state.logistics["exit_port"])
    selected_exit = st.selectbox("ПОРТ ВИХОДУ (Склад США)", exit_list, index=exit_idx)
    
    # Порт призначення
    selected_dest = st.selectbox("ПОРТ ПРИБУТТЯ (Європа)", list(SEA_FREIGHT.keys()))

with col2:
    st.subheader("📋 Дані авто")
    year = st.number_input("Рік", 2000, 2026, value=int(st.session_state.logistics["year"]))
    engine = st.number_input("Двигун (L)", 0.1, 10.0, value=float(st.session_state.logistics["engine"]))
    fuel = st.selectbox("Паливо", ["Бензин", "Дизель", "Електро", "Гібрид"])

with col3:
    st.subheader("💰 Витрати")
    customs = st.number_input("Мито (Растаможка), $", value=3500)
    service = st.number_input("Брокер + Експедитор, $", value=800)
    paid = st.number_input("Вже сплачено, $", value=0)

# Розрахунок
auction_fee = get_auction_fee(bid)
tow_to_port = US_EXIT_PORTS[selected_exit] # Ціна евакуатора до обраного порта
sea_cost = SEA_FREIGHT[selected_dest] # Ціна моря
total = bid + auction_fee + tow_to_port + sea_cost + 166 + 50 + customs + service

st.markdown("---")
res1, res2, res3 = st.columns(3)
res1.metric("МАРШРУТ", f"{selected_exit} ➡️ {selected_dest.split(' ')[0]}")
res2.metric("ВСЬОГО (ALL IN)", f"${total:,.0f}")
res3.metric("ЕВАКУАТОР (TOW)", f"${tow_to_port}")

with st.expander("📝 Детальний маршрут для клієнта"):
    report = f"""
    📍 Локація лота: {st.session_state.logistics['auction_loc']}
    🚛 Евакуатор до порту: {selected_exit} — ${tow_to_port}
    🚢 Морський фрахт: {selected_dest} — ${sea_cost}
    -------------------------------------------
    💰 Ставка: ${bid} | Збори: ${auction_fee} | Мито: ${customs}
    🏁 ПІДСУМОК: ${total}
    """
    st.code(report)
