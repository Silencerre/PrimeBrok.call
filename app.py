import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="PrimeBrok Logistics AI", page_icon="🚛", layout="wide")

# --- ЛОГИКА ТАРИФОВ И ПОРТОВ ---
# Порты вылета в США и стоимость эвакуатора до них (базовая)
US_EXIT_PORTS = {
    "NJ - Port of Newark": 175,
    "GA - Port of Savannah": 250,
    "TX - Port of Houston": 325,
    "CA - Port of Los Angeles": 450,
    "FL - Port of Miami": 275,
    "IL - Port of Chicago": 350
}

# Привязка штатов к ближайшим портам
STATE_TO_PORT_MAP = {
    "NJ": "NJ - Port of Newark", "NY": "NJ - Port of Newark", "PA": "NJ - Port of Newark", "CT": "NJ - Port of Newark",
    "GA": "GA - Port of Savannah", "SC": "GA - Port of Savannah", "NC": "GA - Port of Savannah",
    "TX": "TX - Port of Houston", "LA": "TX - Port of Houston", "OK": "TX - Port of Houston",
    "CA": "CA - Port of Los Angeles", "WA": "CA - Port of Los Angeles", "OR": "CA - Port of Los Angeles", "AZ": "CA - Port of Los Angeles",
    "FL": "FL - Port of Miami",
    "IL": "IL - Port of Chicago", "WI": "IL - Port of Chicago", "MI": "IL - Port of Chicago", "IN": "IL - Port of Chicago"
}

EUROPE_PORTS = {
    "Constanta (Romania)": 2850,
    "Odesa (Ukraine)": 3100,
    "Klaipeda (Lithuania)": 2950
}

def get_auction_fee(bid):
    if bid < 500: return 200
    if bid < 1000: return 350
    if bid < 2000: return 550
    if bid < 4000: return 750
    return 900

# --- УЛУЧШЕННЫЙ РОБОТ-ПАРСЕР v6.0 ---
def scrape_auction_lot(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Берем текст только из основной части, чтобы не цеплять даты из футера
            main_content = soup.find('body').get_text(separator=' ').upper()
            title = soup.title.string.upper() if soup.title else ""

            # Ищем ГОД (строго перед названием или в заголовке, исключая 2024-2026)
            years = re.findall(r'\b(200\d|201\d|202[0-4])\b', title + " " + main_content[:1000])
            year = int(years[0]) if years else 2015

            # Ищем МАРКУ/МОДЕЛЬ
            brand = "АВТОМОБИЛЬ"
            car_match = re.search(rf'{year}\s+([A-Z0-9\s\-]{{3,25}})\s+', title)
            if car_match: brand = car_match.group(1).strip()

            # Ищем ДВИГАТЕЛЬ (X.X L)
            eng_match = re.search(r'(\d\.\d)L', main_content)
            engine = float(eng_match.group(1)) if eng_match else 2.0

            # Ищем ЛОКАЦИЮ (City, ST)
            state = "NJ"
            city_state = "UNKNOWN, NJ"
            loc_match = re.search(r'([A-Z\s]{2,15}),\s([A-Z]{2})', main_content)
            if loc_match:
                city_state = f"{loc_match.group(1).strip()}, {loc_match.group(2)}"
                state = loc_match.group(2)

            return {
                "year": year, "brand": brand, "engine": engine,
                "auction_city": city_state,
                "exit_port": STATE_TO_PORT_MAP.get(state, "NJ - Port of Newark"),
                "status": "success"
            }
    except Exception as e:
        print(f"Scraping error: {e}")
    return {"status": "error"}

# --- ИНТЕРФЕЙС ---
if 'lot' not in st.session_state:
    st.session_state.lot = {"year": 2015, "brand": "", "engine": 2.0, "auction_city": "Вставьте ссылку", "exit_port": "NJ - Port of Newark"}

st.title("🏯 PrimeBrok: Полная Логистическая Цепочка")

url = st.text_input("🔗 Ссылка на лот (Copart/IAAI)")

if url and st.button("🚀 ПОЛУЧИТЬ ДАННЫЕ И ПРОЛОЖИТЬ ПУТЬ"):
    with st.spinner("Робот сканирует аукцион..."):
        data = scrape_auction_lot(url)
        if data["status"] == "success":
            st.session_state.lot = data
            st.success("✅ Данные лота и маршрут обновлены!")

st.markdown("---")

# --- ВИЗУАЛИЗАЦИЯ ПУТИ ---
st.subheader("🗺️ Маршрут следования")
c1, c2, c3 = st.columns([1, 0.2, 1])
c1.info(f"📍 **АУКЦИОН:** {st.session_state.lot['auction_city']}")
c2.write("➡️")
c3.success(f"⚓ **ПОРТ США:** {st.session_state.lot['exit_port']}")

st.markdown("---")

# --- ДЕТАЛЬНЫЙ РАСЧЕТ ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🇺🇸 Эвакуатор и Аукцион")
    bid = st.number_input("Ставка (Bid), $", min_value=0, value=2000)
    # Авто-выбор порта на основе локации лота
    port_list = list(US_EXIT_PORTS.keys())
    port_idx = port_list.index(st.session_state.lot["exit_port"])
    selected_us_port = st.selectbox("Склад/Порт в США (TOW TO)", port_list, index=port_idx)
    tow_price = US_EXIT_PORTS[selected_us_port]

with col2:
    st.subheader("🚢 Море и Тех.данные")
    dest_port = st.selectbox("Порт назначения (EUROPE)", list(EUROPE_PORTS.keys()))
    car_name = st.text_input("Марка/Модель", value=st.session_state.lot["brand"])
    year = st.number_input("Год", 2000, 2026, value=int(st.session_state.lot["year"]))
    engine = st.number_input("Объем (L)", 0.1, 10.0, value=float(st.session_state.lot["engine"]))

with col3:
    st.subheader("🏛️ Налоги и Финал")
    customs = st.number_input("Растаможка, $", value=3500)
    fees = st.number_input("Брокер + Экспедитор, $", value=800)
    paid = st.number_input("Уже оплачено клиентом, $", value=0)

# Математика
auction_fee = get_auction_fee(bid)
sea_price = EUROPE_PORTS[dest_port]
total = bid + auction_fee + tow_price + sea_price + 166 + 50 + customs + fees

st.markdown("---")
res1, res2, res3 = st.columns(3)
res1.metric("ИТОГО ПО КЛЮЧУ", f"${total:,.0f}")
res2.metric("СТОИМОСТЬ TOW", f"${tow_price}")
res3.metric("ОСТАТОК К ОПЛАТЕ", f"${total - paid:,.0f}")

with st.expander("📝 Готовый текст для клиента (Copy/Paste)"):
    client_text = f"""
🚗 **{car_name} {year} ({engine}L)**
📍 **Локация:** {st.session_state.lot['auction_city']}
-------------------------------------------
💰 **Аукцион:** ${bid} (ставка) + ${auction_fee} (сбор) + $166 (swift)
🚛 **Транзит США:** ${tow_price} (в {selected_us_port})
🚢 **Море:** ${sea_price} (в {dest_port})
🏛️ **Растаможка + Сервис:** ${customs + fees}
-------------------------------------------
🏁 **ИТОГО ПОД КЛЮЧ: ${total:,.0f}**
    """
    st.code(client_text)
