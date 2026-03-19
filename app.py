import streamlit as st

# Налаштування PrimeBrok
st.set_page_config(page_title="PrimeBrok Calculator", page_icon="📈", layout="wide")

# --- ПОВНА БАЗА ЛОКАЦІЙ ---
ALL_LOCATIONS = sorted([
    "ABILENE", "ABILENE (TX)", "ACE - CARSON (CA)", "ACE - PERRIS (CA)", "ADELANTO", "ADRIAN", "AFTON", "AKRON-CANTON (OH)", 
    "ALBANY", "ALBANY (NY)", "ALBUQUERQUE", "ALBUQUERQUE (NM)", "ALEXANDRIA", "ALTOONA", "ALTOONA (PA)", "AMARILLO", 
    "AMARILLO (TX)", "ANAHEIM (CA)", "ANCHORAGE (AK)", "ANDREWS", "APPLETON (WI)", "ARLINGTON (TX)", "ASHEVILLE (NC)", 
    "ASHLAND (KY)", "ATLANTA", "ATLANTA EAST (GA)", "ATLANTA NORTH (GA)", "ATLANTA SOUTH (GA)", "ATLANTA WEST (GA)", 
    "AUSTIN (TX)", "AVENEL (NJ)", "BAKERSFIELD (CA)", "BALTIMORE", "BALTIMORE (MD)", "BATON ROUGE (LA)", "BILLINGS", 
    "BIRMINGHAM (AL)", "BOISE (ID)", "BOSTON (MA)", "BRIDGEPORT (PA)", "BROOKHAVEN (NY)", "BUFFALO (NY)", "BURLINGTON", 
    "CASPER (WY)", "CHARLESTON (SC)", "CHARLOTTE (NC)", "CHATTANOOGA (TN)", "CHICAGO NORTH", "CHICAGO SOUTH", "CHICAGO WEST", 
    "CINCINNATI (OH)", "CLEARWATER (FL)", "CLEVELAND (OH)", "COLORADO SPRINGS (CO)", "COLUMBIA", "COLUMBIA (SC)", 
    "COLUMBIA STATION", "COLUMBUS (OH)", "CONCORD (NC)", "CORPUS CHRISTI (TX)", "DALLAS (TX)", "DALLAS SOUTH", 
    "DAYTON (OH)", "DENVER (CO)", "DENVER CENTRAL", "DES MOINES (IA)", "DETROIT", "DOTHAN (AL)", "DUNDEE", "EL PASO (TX)", 
    "ELGIN (IL)", "ENGLISHTOWN (NJ)", "EUGENE (OR)", "FAYETTEVILLE (AR)", "FLINT", "FONTANA (CA)", "FORT LAUDERDALE (FL)", 
    "FORT WORTH (TX)", "FRESNO", "FRESNO (CA)", "GLASSBORO (NJ)", "GRAHAM (WA)", "GRAND RAPIDS (MI)", "GREER (SC)", 
    "HARTFORD", "HAYWARD", "HAYWARD (CA)", "HONOLULU (HI)", "HOUSTON", "HOUSTON EAST (TX)", "INDIANAPOLIS (IN)", 
    "JACKSON (MS)", "JACKSONVILLE (FL)", "KANSAS CITY (KS)", "KNOXVILLE", "LAUREL (MD)", "LAS VEGAS", "LEXINGTON", 
    "LITTLE ROCK (AR)", "LOGANVILLE (GA)", "LONG ISLAND (NY)", "LOS ANGELES", "LOS ANGELES (CA)", "LOUISVILLE (KY)", 
    "LUFKIN (TX)", "MACON (GA)", "MARTINEZ (CA)", "MCALLEN (TX)", "MEMPHIS", "MIAMI", "MIAMI CENTRAL", "MIAMI NORTH", 
    "MIAMI SOUTH", "MILWAUKEE", "MINNEAPOLIS", "MOBILE (AL)", "MONTGOMERY (AL)", "NASHVILLE (TN)", "NEW ORLEANS", 
    "NEWBURGH", "NEWBURGH (NY)", "NORTH HOLLYWOOD (CA)", "OCALA (FL)", "OKLAHOMA CITY (OK)", "ORLANDO (FL)", "ORLANDO NORTH", 
    "ORLANDO SOUTH", "PASCO (WA)", "PEKIN (IL)", "PHILADELPHIA", "PHOENIX", "PITTSBURGH", "PORTLAND", "PORT NEWARK (NJ)", 
    "PUYALLUP (WA)", "PUNTA GORDA (FL)", "RALEIGH (NC)", "RENO", "RICHMOND (VA)", "ROCHESTER (NY)", "SACRAMENTO", 
    "SALT LAKE CITY", "SAN ANTONIO", "SAN BERNARDINO (CA)", "SAN DIEGO", "SAN JOSE (CA)", "SAVANNAH", "SEATTLE", 
    "SHREVEPORT (LA)", "SOMERVILLE (NJ)", "SPOKANE", "ST. LOUIS", "SUN VALLEY (CA)", "SYRACUSE", "TALLAHASSEE (FL)", 
    "TAMPA (FL)", "TAMPA SOUTH", "TANNER (AL)", "TIFTON (GA)", "TRENTON (NJ)", "TUCSON", "TULSA", "VALLEJO", 
    "VALLEJO (CA)", "VAN NUYS (CA)", "WACO (TX)", "WALDORF (MD)", "WASHINGTON DC", "WEST PALM BEACH (FL)", "WHEELING (IL)", 
    "WICHITA", "WILMINGTON", "YORK (PA)"
])

STATES = ["---", "NJ", "GA", "TX", "CA", "WA", "FL", "IL", "NY", "PA", "MD", "SC", "NC", "OH"]

# --- ІНТЕРФЕЙС PRIME BROK ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>📈 PrimeBrok Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Професійна платформа розрахунку авто з США</p>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("📍 Локація")
    selected_loc = st.selectbox("Локація аукціону (B4)", ALL_LOCATIONS, index=0)
    selected_state = st.selectbox("Штат (C4)", STATES)
    selected_port = st.selectbox("Порт призначення (D4)", ["Constanta", "Odesa", "Klaipeda"])
    year = st.number_input("Рік по Шильдіку (C3)", min_value=1990, max_value=2026, value=2015)

with col2:
    st.subheader("📝 Деталі Лота")
    bid = st.number_input("Ставка (B5), $", min_value=0, value=2000, step=100)
    engine = st.text_input("Об'єм двигуна (D3)", "2.0")
    body = st.selectbox("Тип кузова (E4)", ["------", "SUV"])
    fuel = st.selectbox("Паливо / Завантаження (F4)", ["GAS", "Diesel", "HYB", "EV", "2", "3"])

with col3:
    st.subheader("💰 Витрати")
    auction_fee = st.number_input("Збір Аукціону (C6), $", value=630)
    swift = st.number_input("Swift (C7), $", value=166)
    insurance = st.number_input("Страхування (C13), $", value=50)
    customs = st.number_input("Митні платежі (C15), $", value=4504)
    paid = st.number_input("Скільки оплачено (F3), $", value=0)

# --- РОЗРАХУНОК ---
total_all_in = bid + auction_fee + swift + insurance + customs
debt = total_all_in - paid

st.markdown("---")
res_col1, res_col2, res_col3 = st.columns(3)

with res_col1:
    st.metric("ALL IN (З митом)", f"${total_all_in:,.0f}")
with res_col2:
    st.metric("БЕЗ МИТНИЦІ", f"${total_all_in - customs:,.0f}")
with res_col3:
    if debt > 0:
        st.error(f"DEBT (БОРГ): ${debt:,.0f}")
    else:
        st.success("ОПЛАЧЕНО ПОВНІСТЮ")
