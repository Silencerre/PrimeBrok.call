import streamlit as st

st.set_page_config(page_title="PrimeBrok Logistics", layout="wide")

# --- ПОВНА БАЗА ДАНИХ (ВСІ ЛОКАЦІЇ ТА ШТАТИ) ---
LAND_DATA = {
    "Abilene (TX)": 460, "Amarillo (TX)": 675, "Atlanta (GA)": 400, "Avenel (NJ)": 200,
    "Baltimore (MD)": 400, "Billings (MT)": 1350, "Boise (ID)": 750, "Boston (MA)": 500,
    "Casper (WY)": 1150, "Charleston (SC)": 350, "Chicago (IL)": 725, "Columbus (OH)": 650,
    "Dallas (TX)": 300, "Denver (CO)": 950, "Detroit (MI)": 700, "Eugene (OR)": 550,
    "Houston (TX)": 250, "Indianapolis (IN)": 675, "Jacksonville (FL)": 325, "Las Vegas (NV)": 475,
    "Los Angeles (CA)": 250, "McAllen (TX)": 550, "Memphis (TN)": 650, "Miami (FL)": 450,
    "Nashville (TN)": 550, "New York (NY)": 300, "Oklahoma City (OK)": 550, "Philadelphia (PA)": 325,
    "Phoenix (AZ)": 450, "Portland (OR)": 300, "Sacramento (CA)": 325, "Salt Lake City (UT)": 850,
    "San Antonio (TX)": 325, "San Diego (CA)": 350, "Savannah (GA)": 240, "Seattle (WA)": 275,
    "St. Louis (MO)": 750, "Tacoma (WA)": 250, "Tampa (FL)": 450, "Washington (DC)": 425
}

# --- МОРСЬКИЙ ФРАХТ (МАТРИЦЯ ПОРТ-ШТАТ-ПАЛИВО) ---
SEA_RATES = {
    "Constanta": {
        "GAS": {"NJ": 2665, "GA": 2635, "TX": 2755, "CA": 3410, "WA": 3000},
        "EV": {"NJ": 2930, "GA": 2860, "TX": 2960, "CA": 3560, "WA": 3200},
        "MOTO": {"NJ": 2000, "GA": 2000, "TX": 2000, "CA": 2050, "WA": 2100}
    },
    "Odesa": {
        "GAS": {"NJ": 2475, "GA": 2450, "TX": 2575, "CA": 3250, "WA": 2900},
        "EV": {"NJ": 2575, "GA": 2600, "TX": 2700, "CA": 3375, "WA": 3000},
        "MOTO": {"NJ": 2000, "GA": 2000, "TX": 2000, "CA": 2050, "WA": 2100}
    },
    "Klaipeda": {
        "GAS": {"NJ": 2685, "GA": 2735, "TX": 2860, "CA": 3260, "WA": 3735},
        "EV": {"NJ": 2785, "GA": 2835, "TX": 2960, "CA": 3360, "WA": 2835},
        "MOTO": {"NJ": 2100, "GA": 2100, "TX": 2100, "CA": 2150, "WA": 3150}
    }
}

# --- ФІКСОВАНІ ЦІНИ (НЕ ЗМІНЮЮТЬСЯ) ---
FIXED_FEE = 795
FIXED_SWIFT = 209
FIXED_CUSTOMS = 1720
FIXED_INSURANCE = 65

st.markdown("""
    <style>
    .stSelectbox [data-baseweb="select"], .stNumberInput input { border: 2px solid #00D1FF !important; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚢 PrimeBrok — Система розрахунку")

# --- БЛАКИТНІ ПОЛЯ (КЕРУВАННЯ) ---
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        auction = st.selectbox("Аукціон", ["IAAI", "COPART"])
        fuel = st.selectbox("Тип палива", ["GAS", "EV", "MOTO"])
    with col2:
        loc = st.selectbox("Локація аукціону", list(LAND_DATA.keys()))
        # Визначаємо код штату автоматично
        state = "NJ" if "(NJ)" in loc or "(NY)" in loc or "(MD)" in loc or "(PA)" in loc or "(MA)" in loc else \
                "GA" if "(GA)" in loc or "(FL)" in loc or "(SC)" in loc or "(TN)" in loc else \
                "TX" if "(TX)" in loc or "(OK)" in loc or "(MO)" in loc or "(CO)" in loc else \
                "CA" if "(CA)" in loc or "(NV)" in loc or "(AZ)" in loc else "WA"
    with col3:
        dest_port = st.selectbox("Порт призначення", list(SEA_RATES.keys()))
        paid = st.number_input("PAID (Оплачено) $", value=0)
    with col4:
        bid = st.number_input("Ставка $", value=0)
        storage = st.number_input("Storage (Парковка) $", value=0)

# --- АВТОМАТИЧНА ЛОГІКА ---
val_land = LAND_DATA[loc]
val_sea = SEA_RATES[dest_port][fuel].get(state, 3000)
total_trans = val_land + val_sea

all_in = bid + FIXED_FEE + FIXED_SWIFT + total_trans + FIXED_INSURANCE + FIXED_CUSTOMS + storage
debt = all_in - paid

# --- ВІЗУАЛІЗАЦІЯ (ЯК У ТАБЛИЦІ) ---
st.markdown("---")
res_col1, res_col2, res_col3 = st.columns(3)

with res_col1:
    st.markdown(f'<div style="background:#d32f2f;padding:20px;border-radius:10px;text-align:center;color:white;"><h3>ALL IN</h3><h2>${all_in:,.0f}</h2></div>', unsafe_allow_html=True)
with res_col2:
    st.markdown(f'<div style="background:#388e3c;padding:20px;border-radius:10px;text-align:center;color:white;"><h3>PAID</h3><h2>${paid:,.0f}</h2></div>', unsafe_allow_html=True)
with res_col3:
    st.markdown(f'<div style="background:#1976d2;padding:20px;border-radius:10px;text-align:center;color:white;"><h3>DEBT</h3><h2>${debt:,.0f}</h2></div>', unsafe_allow_html=True)

# ФІКСОВАНІ ПОКАЗНИКИ
st.subheader("📌 Фіксовані дані (згідно з таблицею)")
f_col1, f_col2, f_col3, f_col4 = st.columns(4)
f_col1.metric("Збір Аукціону", f"${FIXED_FEE}")
f_col2.metric("Swift", f"${FIXED_SWIFT}")
f_col3.metric("Транспорт (Разом)", f"${total_trans}")
f_col4.metric("Митниця", f"${FIXED_CUSTOMS}")

st.caption(f"Логістика: Суша {val_land}$ + Море {val_sea}$ (через штат {state})")
