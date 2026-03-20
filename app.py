import streamlit as st
import pandas as pd

# Налаштування інтерфейсу
st.set_page_config(page_title="PrimeBrok", layout="centered")

# Назва сайту
st.title("🚢 PrimeBrok")
st.subheader("Система розрахунку логістики")

# --- БАЗА ДАНИХ ЛОКАЦІЙ (Витяг з ваших таблиць) ---
# Формат: "Локація": [NJ, GA, TX, CA, WA]
locations = {
    "Atlanta (GA)": [None, 400, None, None, None],
    "Abilene (TX)": [None, None, 460, None, None],
    "Baltimore (MD)": [400, None, None, None, None],
    "Los Angeles (CA)": [None, None, 1150, 250, None],
    "Chicago-North (IL)": [725, None, None, None, None],
    "Miami-North (FL)": [None, 450, None, None, None],
    "Savannah (GA)": [None, 240, None, None, None],
    "Seattle (WA)": [None, None, None, 875, 275],
    "Houston (TX)": [None, None, 250, None, None],
    "Newburgh (NY)": [300, None, None, None, None],
    "Philadelphia (PA)": [325, None, None, None, None],
}

# --- БАЗА ДАНИХ ФРАХТУ (Порти та типи палива) ---
# Ціни для портів залежно від штабу виходу (NJ, GA, TX, CA, WA)
shipping = {
    "Constanta": {
        "GAS/Diesel": [2665, 2635, 2755, 3410, 3000],
        "EV/HYB": [2930, 2860, 2960, 3560, 3200],
        "GAS 3": [2860, 2760, 2960, 3735, 3300],
        "GAS 2": [3980, 3940, 4180, 5490, 4500],
        "MOTO": [2000, 2000, 2000, 2050, 2100]
    },
    "Odesa": {
        "GAS/Diesel": [2475, 2450, 2575, 3250, 2900],
        "EV/HYB": [2575, 2600, 2700, 3375, 3000],
        "GAS 3": [2830, 2830, 3000, 3900, 3500],
        "MOTO": [2000, 2000, 2000, 2050, 2100]
    },
    "Klaipeda": {
        "GAS/Diesel": [2685, 2735, 2860, 3260, 3735],
        "EV/HYB": [2785, 2835, 2960, 3360, 2835],
        "GAS 3": [2790, 2840, 2965, 3465, 4185],
        "MOTO": [2100, 2100, 2100, 2150, 3150]
    }
}

# --- ВВІД ДАНИХ ---
with st.container():
    st.write("### Введіть параметри авто")
    
    col1, col2 = st.columns(2)
    
    with col1:
        loc_name = st.selectbox("Локація аукціону (Location)", list(locations.keys()))
        port = st.selectbox("Порт призначення", ["Constanta", "Odesa", "Klaipeda"])
        fuel = st.selectbox("Тип палива / Завантаження", ["GAS/Diesel", "EV/HYB", "GAS 3", "GAS 2", "MOTO"])
        
    with col2:
        bid = st.number_input("Ставка аукціону ($)", value=0)
        auction_fee = st.number_input("Збір аукціону ($)", value=340)
        customs = st.number_input("Митні платежі ($)", value=1720)

    insurance = st.number_input("Страхування ($)", value=50)
    other = st.number_input("Інші витрати (Swift тощо) ($)", value=121)

# --- ЛОГІКА РОЗРАХУНКУ ---
# 1. Знаходимо штат (індекс 0-4 для NJ, GA, TX, CA, WA)
state_index = -1
land_cost = 0

for i, cost in enumerate(locations[loc_name]):
    if cost is not None:
        state_index = i
        land_cost = cost
        break

# 2. Отримуємо морський фрахт
sea_cost = 0
if fuel in shipping[port]:
    sea_cost = shipping[port][fuel][state_index]
else:
    sea_cost = 0
    st.warning("Цей тип палива недоступний для обраного порту.")

# 3. Підрахунок сум
total_logistics = land_cost + sea_cost
total_all_in = bid + auction_fee + total_logistics + insurance + other + customs
without_customs = total_all_in - customs

# --- РЕЗУЛЬТАТИ ---
st.divider()
st.header("📊 Результати розрахунку")

res_col1, res_col2 = st.columns(2)

with res_col1:
    st.write(f"**Транспорт (Суша):** {land_cost} $")
    st.write(f"**Фрахт (Море):** {sea_cost} $")
    st.write(f"**Загальна логістика:** {total_logistics} $")

with res_col2:
    st.success(f"### ALL IN: {total_all_in} $")
    st.info(f"**Без митниці:** {without_customs} $")

st.markdown("---")
st.caption("PrimeBrok Logic Engine v1.0 | Все на українській мові за наказом повелителя.")
