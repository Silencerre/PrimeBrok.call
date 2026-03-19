import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="PrimeBrok: Ultimate Logistics AI", page_icon="🚢", layout="wide")

# --- БАЗА ДАННЫХ ЛОГИСТИКИ (МАРШРУТЫ США) ---
# Цена эвакуатора внутри США до ближайшего экспортного узла
US_LOGISTICS = {
    "NJ": {"port": "Port of Newark (East)", "cost": 175},
    "GA": {"port": "Port of Savannah (South)", "cost": 250},
    "TX": {"port": "Port of Houston (Central)", "cost": 325},
    "CA": {"port": "Port of Los Angeles (West)", "cost": 450},
    "WA": {"port": "Port of Seattle (North-West)", "cost": 500},
    "IL": {"port": "Port of Chicago (Midwest)", "cost": 350}
}

# Карта привязки штатов аукциона к портам погрузки
STATE_TO_HUB = {
    "NY": "NJ", "PA": "NJ", "CT": "NJ", "MA": "NJ", "NJ": "NJ",
    "SC": "GA", "NC": "GA", "AL": "GA", "GA": "GA",
    "LA": "TX", "OK": "TX", "AR": "TX", "TX": "TX",
    "AZ": "CA", "NV": "CA", "UT": "CA", "CA": "CA",
    "OR": "WA", "ID": "WA", "MT": "WA", "WA": "WA",
    "WI": "IL", "MI": "IL", "IN": "IL", "OH": "IL", "IL": "IL"
}

SEA_FREIGHT = {
    "Constanta (Romania)": 2850,
    "Odesa (Ukraine)": 3100,
    "Klaipeda (Lithuania)": 2950
}

# --- ЛОГИКА СБОРОВ И НАЛОГОВ ---
def get_customs_logic(engine_type, engine_vol, year, bid):
    # Логика из таблицы: Электрокары почти без пошлин, ДВС — по объему
    if engine_type == "Электро":
        return 150 + (bid * 0.05) # Пример: минимальный сбор
    else:
        base = 1500 if year > 2015 else 2500
        vol_tax = engine_vol * 800 # Коэффициент объема
        return base + vol_tax + (bid * 0.1)

# --- РОБОТ-ПАРСЕР v7.0 (DEEP SCAN) ---
def deep_scan_lot(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            text = soup.get_text(separator=' ').upper()
            title = soup.title.string.upper() if soup.title else ""

            # Ищем год (строго 4 цифры до 2025)
            year_match = re.search(r'\b(200\d|201\d|202[0-5])\b', title)
            year = int(year_match.group(1)) if year_match else 2017

            # Ищем Штат (Location)
            detected_state = "NJ"
            loc_match = re.search(r',\s([A-Z]{2})\b', text) # Ищем формат ", TX"
            if loc_match: detected_state = loc_match.group(1)

            # Ищем объем двигателя
            eng_match = re.search(r'(\d\.\d)L', text)
            engine = float(eng_match.group(1)) if eng_match else 2.0

            # Тип топлива
            fuel = "Бензин"
            if "ELECTRIC" in text or "EV" in text: fuel = "Электро"
            elif "HYBRID" in text: fuel = "Гибрид"

            return {
                "year": year, "engine": engine, "fuel": fuel,
                "state": detected_state, "status": "success"
            }
    except: pass
    return {"status": "error"}

# --- СЕССИЯ ---
if 'master' not in st.session_state:
    st.session_state.master = {"year": 2017, "engine": 2.0, "fuel": "Бензин", "state": "NJ"}

st.title("🏯 PrimeBrok: Система Тотального Просчета")

url = st.text_input("🔗 Вставьте ссылку на лот (Copart / IAAI / Impact)")

if url and st.button("📊 ПРОСЧИТАТЬ ДО КАПЕЛЬКИ"):
    with st.spinner("Робот анализирует логистику и налоги..."):
        res = deep_scan_lot(url)
        if res["status"] == "success":
            st.session_state.master = res
            st.success(f"✅ Данные получены: Авто из {res['state']}, Двигатель {res['engine']}L ({res['fuel']})")

st.markdown("---")

# --- ИНТЕРФЕЙС ---
col1, col2, col3 = st.columns(3)

with col1:
    st.header("📍 Локация Аукциона")
    auction_state = st.session_state.master["state"]
    st.metric("Штат аукциона", auction_state)
    
    # Определяем хаб (Порт США)
    hub_code = STATE_TO_HUB.get(auction_state, "NJ")
    hub_info = US_LOGISTICS[hub_code]
    
    st.write(f"🚚 Ближайший склад: **{hub_info['port']}**")
    tow_cost = hub_info['cost']
    st.write(f"💰 Цена эвакуатора до склада: **${tow_cost}**")
    
    bid = st.number_input("Ставка (Bid), $", min_value=0, value=2000)

with col2:
    st.header("⚙️ Характеристики")
    fuel_type = st.selectbox("Тип двигателя", ["Бензин", "Дизель", "Электро", "Гибрид"], 
                             index=["Бензин", "Дизель", "Электро", "Гибрид"].index(st.session_state.master["fuel"]))
    
    year = st.number_input("Год выпуска", 2000, 2026, value=int(st.session_state.master["year"]))
    vol = st.number_input("Объем двигателя (L)", 0.0, 10.0, value=float(st.session_state.master["engine"]))
    dest_port = st.selectbox("Плывем в порт:", list(SEA_FREIGHT.keys()))

with col3:
    st.header("💰 Налоги и Итого")
    # Динамический расчет таможни
    customs_calc = get_customs_logic(fuel_type, vol, year, bid)
    customs = st.number_input("Растаможка (авто-расчет), $", value=int(customs_calc))
    
    broker = st.number_input("Брокер + Экспедитор, $", value=800)
    paid = st.number_input("Уже оплачено, $", value=0)

# ФИНАЛЬНЫЙ РАСЧЕТ
sea_cost = SEA_FREIGHT[dest_port]
auction_fee = 650 if bid > 2000 else 450 # Упрощенная сетка
total = bid + auction_fee + tow_cost + sea_cost + 166 + 50 + customs + broker

st.markdown("---")
res1, res2, res3 = st.columns(3)
res1.metric("ИТОГО ПОД КЛЮЧ", f"${total:,.0f}")
res2.metric("ДОСТАВКА (TOW + SEA)", f"${tow_cost + sea_cost}")
res3.metric("К ОПЛАТЕ", f"${total - paid:,.0f}")

with st.expander("📝 Детальный инвойс"):
    invoice = f"""
🚢 МАРШРУТ: {auction_state} -> {hub_info['port']} -> {dest_port}
-------------------------------------------
🚗 Авто: {year}г., {vol}L {fuel_type}
💰 Ставка: ${bid}
🏗️ Сборы аукциона + Swift: ${auction_fee + 166}
🚛 Эвакуатор по США: ${tow_cost}
🚢 Контейнер (Море): ${sea_cost}
🏛️ Растаможка: ${customs}
-------------------------------------------
🏁 ВСЕГО: ${total:,.0f}
    """
    st.code(invoice)
