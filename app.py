import streamlit as st

st.set_page_config(page_title="Нікіта Калькулятор", layout="wide", page_icon="🚗")

st.title("Нікіта Калькулятор")
st.markdown("Розрахунок імпорту авто з США • Констанца / Одеса / Клайпеда • 2025–2026")

# ────────────────────────────────────────────────
# TOW дані (оброблені: тільки локації з хоча б однією ціною, Error → None)
tow = {
    "ABILENE": {"TX": 460},
    "Abilene (TX)": {"TX": 460},
    "ACE - Carson (CA)": {"TX": 1150, "CA": 275},
    "ACE - Perris (CA)": {"TX": 1200, "CA": 300},
    "ADELANTO": {"CA": 350},
    "Akron-Canton (OH)": {"NJ": 575},
    "ALBANY": {"NJ": 375},
    "Albany (NY)": {"NJ": 375},
    "ALBUQUERQUE": {"TX": 675},
    "Albuquerque (NM)": {"TX": 675},
    "ALTOONA": {"NJ": 500},
    "Altoona (PA)": {"NJ": 500},
    "AMARILLO": {"TX": 525},
    "Amarillo (TX)": {"TX": 525},
    "Anaheim (CA)": {"TX": 1150, "CA": 250},
    "ANDREWS": {"TX": 525},
    "ANTELOPE": {"TX": 1275},
    "APPLETON": {"NJ": 825},
    "Appleton (WI)": {"NJ": 825},
    "Asheville (NC)": {"GA": 450},
    "Ashland": {"NJ": 775, "GA": 600},
    "Atlanta (GA)": {"GA": 400},
    "ATLANTA EAST": {"GA": 400},
    "Atlanta East (GA)": {"GA": 400},
    "ATLANTA NORTH": {"GA": 425},
    "Atlanta North (GA)": {"GA": 400},
    "ATLANTA SOUTH": {"GA": 450},
    "Atlanta South (GA)": {"GA": 400},
    "ATLANTA WEST": {"GA": 400},
    "AUGUSTA": {"GA": 350},
    "AUSTIN": {"TX": 350},
    "Austin (TX)": {"TX": 350},
    "Avenel New Jersey (NJ)": {"NJ": 250},
    "BAKERSFIELD": {"CA": 525},
    "BALTIMORE": {"NJ": 400},
    "Baltimore (MD)": {"NJ": 400},
    "BALTIMORE EAST": {"NJ": 400},
    "BATON ROUGE": {"TX": 450},
    "Baton Rouge (LA)": {"TX": 450},
    "BILLINGS": {"WA": 800},
    "Billings (MT)": {"WA": 800},
    "BIRMINGHAM": {"GA": 500},
    "Birmingham (AL)": {"GA": 475},
    "BOISE": {"CA": 850},
    "Boise (ID)": {"CA": 850},
    "Boston - Shirley (MA)": {"NJ": 450},
    "Bowling Green (KY)": {"NJ": 700, "GA": 700},
    "Bridgeport (PA)": {"NJ": 325},
    "Buckhannon (WV)": {"NJ": 600},
    "BUFFALO": {"NJ": 550},
    "Buffalo (NY)": {"NJ": 550},
    "Burlington (VT)": {"NJ": 550},
    "CANDIA": {"NJ": 475},
    "CARTERET": {"NJ": 300},
    "CARTERSVILLE": {"GA": 425},
    "CASPER": {"CA": 1050},
    "Casper (WY)": {"CA": 1050},
    "Central New Jersey (NJ)": {"NJ": 285},
    "CHAMBERSBURG": {"NJ": 400},
    "CHARLESTON": {"NJ": 600},
    "Charleston (SC)": {"GA": 275},
    "Charlotte (NC)": {"GA": 400},
    "Chatham": {"NJ": 460},
    "Chattanooga (TN)": {"GA": 500},
    "CHICAGO NORTH": {"NJ": 650},
    "CHICAGO SOUTH": {"NJ": 675},
    "Chicago-North (IL)": {"NJ": 725},
    "Chicago-South (IL)": {"NJ": 700},
    "Chicago-West (IL)": {"NJ": 650},
    "CHINA GROVE": {"GA": 400},
    "CICERO": {"NJ": 700},
    "Cincinnati (OH)": {"NJ": 575},
    "Cleveland (OH)": {"NJ": 550},
    "CLEVELAND EAST": {"NJ": 550},
    "CLEWISTON": {"GA": 525},
    "COLORADO SPRINGS": {"TX": 700},
    "Columbia": {"GA": 300},
    "COLUMBIA": {"NJ": 700, "GA": 300},
    "COLUMBIA STATION": {"NJ": 550},
    "COLUMBUS": {"NJ": 575, "NJ": 550},
    "Columbus (OH)": {"NJ": 575},
    "CONCORD": {"GA": 400},
    "Concord (NC)": {"GA": 400},
    "COPART JOBSTOWN SUBLOT": {"NJ": 375},
    "copart SUBLOT": {"NJ": 350},
    "Corpus Christi (TX)": {"TX": 350},
    "CRASHEDTOYS DALLAS": {"TX": 350},
    "CRASHEDTOYS MINNEAPOLIS": {"NJ": 800},
    "CROWLEY": {"TX": 375},
    "Culpeper (VA)": {"NJ": 400},
    "Dallas": {"TX": 350},
    "DALLAS": {"TX": 350},
    "Dallas (TX)": {"TX": 350},
    "DALLAS SOUTH": {"TX": 350},
    "Dallas/Ft Worth (TX)": {"TX": 350},
    "DAVENPORT": {"NJ": 750},
    "Davenport (IA)": {"NJ": 750},
    "DAYTON": {"NJ": 550},
    "Dayton (OH)": {"NJ": 550},
    "DEFUNIAK SPRINGS": {"GA": 450},
    "Denver": {"TX": 700},
    "DENVER": {"TX": 700},
    "DENVER CENTRAL": {"TX": 700},
    "Denver East (CO)": {"TX": 700},
    "DENVER SOUTH": {"TX": 700},
    "DES MOINES": {"NJ": 750},
    "Des Moines (IA)": {"NJ": 750},
    "DETROIT": {"NJ": 650},
    "DETROIT": {"NJ": 650},
    "Detroit (MI)": {"NJ": 700},
    "DOSWELL": {"NJ": 430},
    "DOTHAN": {"GA": 450},
    "Dothan (AL)": {"GA": 450},
    "Dundalk (MD)": {"NJ": 400},
    "DYER": {"NJ": 700},
    "Earlington": {"NJ": 725},
    "East Bay (CA)": {"TX": 1275, "CA": 525},
    "EAST GRANBY": {"NJ": 375},
    "EL PASO": {"TX": 560},
    "El Paso (TX)": {"TX": 575},
    "Elkton": {"NJ": 400},
    "Englishtown": {"NJ": 285},
    "Erie (PA)": {"NJ": 600},
    "EUGENE": {"CA": 825, "WA": 450},
    "Eugene (OR)": {"CA": 800, "WA": 450},
    "EXETER": {"NJ": 400},
    "Fargo (ND)": {"NJ": 1225},
    "FARIBAULT": {"NJ": 825},
    "Fayetteville": {"TX": 525},
    "Fayetteville (AR)": {"TX": 525},
    "FLINT": {"NJ": 735},
    "Flint (MI)": {"NJ": 735},
    "Fontana (CA)": {"TX": 1150, "CA": 300},
    "Fort Myers offsite": {"GA": 450},
    "Fort Pierce (FL)": {"GA": 425},
    "FORT WAYNE": {"NJ": 675},
    "Fort Worth North (TX)": {"TX": 375},
    "FREDERICKSBURG": {"NJ": 425},
    "FREETOWN": {"NJ": 450},
    "Fremont (CA)": {"TX": 1275, "CA": 475},
    "FRESNO": {"TX": 1275, "CA": 400},
    "Fresno (CA)": {"TX": 1275, "CA": 425},
    "FT. PIERCE": {"GA": 500},
    "FT. WORTH": {"TX": 350},
    "Gastonia": {"GA": 425},
    "GLASSBORO EAST": {"NJ": 285},
    "GLASSBORO WEST": {"NJ": 285},
    "GRAHAM": {"CA": 875, "WA": 275},
    "Grand Rapids (MI)": {"NJ": 750},
    "Granite City": {"NJ": 725},
    "Greensboro (NC)": {"GA": 425},
    "Greenville (SC)": {"GA": 350},
    "Grenada (MS)": {"GA": 550},
    "Gulf Coast (MS)": {"GA": 525},
    "HAMMOND": {"NJ": 700},
    "HAMPTON": {"NJ": 450},
    "HARRISBURG": {"NJ": 400},
    "HARTFORD": {"NJ": 350},
    "Hollywood (CA)": {"TX": 1150, "CA": 275},
    "NORTH SEATTLE": {"CA": 875, "WA": 300},
    "Northern Virginia (VA)": {"NJ": 400},
    "OCALA": {"GA": 425},
    "OGDEN": {"TX": 1125, "CA": 525},
    "OKLAHOMA CITY": {"TX": 525},
    "Oklahoma City (OK)": {"TX": 525},
    "Omaha": {"NJ": 850, "TX": 775},
    "Omaha (NE)": {"NJ": 850, "TX": 775},
    "Orlando (FL)": {"GA": 400},
    "ORLANDO NORTH": {"GA": 425},
    "ORLANDO SOUTH": {"GA": 400},
    "Orlando-North (FL)": {"GA": 425},
    "Paducah (KY)": {"NJ": 700},
    "PASCO": {"WA": 450},
    "Pensacola (FL)": {"GA": 450},
    "PEORIA": {"NJ": 675},
    "Permian Basin (TX)": {"TX": 460},
    "PHILADELPHIA": {"NJ": 325},
    "PHILADELPHIA": {"NJ": 325},
    "Philadelphia (PA)": {"NJ": 325},
    "PHILADELPHIA EAST": {"NJ": 325},
    "PHOENIX": {"TX": 775, "CA": 425},
    "Phoenix (AZ)": {"TX": 775, "CA": 425},
    "Pittsburgh (PA)": {"NJ": 500},
    "PITTSBURGH NORTH": {"NJ": 500},
    "PITTSBURGH SOUTH": {"NJ": 525},
    "PITTSBURGH WEST": {"NJ": 525},
    "Pittsburgh-North (PA)": {"NJ": 500},
    "Port Murray": {"NJ": 325},
    "Portage (WI)": {"NJ": 750},
    "Portland - Gorham (ME)": {"NJ": 550},
    "Portland (OR)": {"CA": 850, "WA": 350},
    "PORTLAND NORTH": {"CA": 875, "WA": 350},
    "PORTLAND SOUTH": {"CA": 875, "WA": 350},
    "Providence": {"NJ": 400},
    "Pulaski (VA)": {"NJ": 500},
    "PUNTA GORDA": {"GA": 450},
    "PUNTA GORDA SOUTH": {"GA": 450},
    "RALEIGH": {"GA": 400},
    "Raleigh (NC)": {"GA": 400},
    "RANCHO CUCAMONGA": {"TX": 1150, "CA": 275},
    "REDDING": {"CA": 600},
    "RENO": {"CA": 600},
    "RICHMOND": {"NJ": 440},
    "Richmond (VA)": {"NJ": 390},
    "RICHMOND EAST": {"NJ": 475},
    "Roanoke (VA)": {"NJ": 550},
    "Rochester (NY)": {"NJ": 525},
    "SACRAMENTO": {"TX": 1275, "CA": 525},
    "Sacramento (CA)": {"TX": 1175, "CA": 475},
    "SALT LAKE CITY": {"TX": 1175, "CA": 575},
    "Salt Lake City (UT)": {"TX": 1125, "CA": 525},
    "SALT LAKE CITY NORTH": {"TX": 1175, "CA": 575},
    "SAN ANTONIO": {"TX": 350},
    "San Antonio-South (TX)": {"TX": 350},
    "SAN BERNARDINO": {"TX": 1150, "CA": 275},
    "SAN DIEGO": {"TX": 1150, "CA": 325},
    "San Diego (CA)": {"TX": 1150, "CA": 325},
    "SAN JOSE": {"CA": 525},
    "SAVANNAH": {"GA": 240},
    "Sayreville (NJ)": {"NJ": 275},
    "SCRANTON": {"NJ": 375},
    "Scranton (PA)": {"NJ": 375},
    "SEAFORD": {"NJ": 400},
    "Seattle (WA)": {"CA": 875, "WA": 275},
    "Shady Spring (WV)": {"NJ": 600},
    "SHREVEPORT": {"TX": 400},
    "Shreveport (LA)": {"TX": 400},
    "Sioux Falls": {"NJ": 1075},
    "Sioux Falls (SD)": {"NJ": 1075},
    "SO SACRAMENTO": {"TX": 1275, "CA": 525},
    "SOMERVILLE": {"NJ": 285},
    "South Bend (IN)": {"NJ": 675},
    "SOUTH BOSTON": {"NJ": 450},
    "SOUTHERN ILLINOIS": {"NJ": 700},
    "Southern New Jersey (NJ)": {"NJ": 315},
    "SPARTANBURG": {"GA": 375},
    "SPOKANE": {"WA": 450},
    "Spokane (WA)": {"WA": 450},
    "SPRINGFIELD": {"NJ": 700},
    "SPRINGFIELD": {"NJ": 775},
    "Springfield (MO)": {"NJ": 675},
    "ST. CLOUD": {"NJ": 825},
    "ST. LOUIS": {"NJ": 650},
    "St. Louis (IL)": {"NJ": 675},
    "MORGANVILLE (SOMERVILLE)": {"NJ": 300},
    "FRUITLAND (SEAFORD)": {"NJ": 450},
    "Birmingham": {"GA": 550},
    "THEODORE": {"GA": 600},
    "HUDSON": {"NJ": 450},
    "White Marsh": {"NJ": 450},
    "CONWAY": {"TX": 525},
    "Lancaster": {"CA": 325},
    "SAN JOSE": {"CA": 525},
    "SANTA PAULA": {"TX": 1150, "CA": 310},
    "SAN DIEGO": {"TX": 1150, "CA": 350},
    "PERRIS": {"TX": 1200, "CA": 325},
    "OKEECHOBEE": {"GA": 500},
    "THONOTOSASSA": {"GA": 425},
    "DOVER": {"GA": 500},
    "Hartford City": {"NJ": 900},
    "GREENVILLE": {"NJ": 675},
    "SCARBOROUGH": {"NJ": 550},
    "GRAY": {"NJ": 600},
    "FRIDLEY": {"NJ": 800},
    "NEWBURGH": {"NJ": 350},
    "FLOWER MOUND": {"TX": 350},
    "FAIR HAVEN": {"NJ": 575},
    "ORLEANS": {"NJ": 560},
    "MILWAUKEE": {"NJ": 710},
    "DETROIT": {"NJ": 750},
    "MEDFORD": {"NJ": 350},
    "CALVERTON": {"NJ": 400},
    "Oklahoma City": {"TX": 550},
    "CHICAGO SOUTH": {"NJ": 750},
    "Suffolk (VA)": {"NJ": 475},
    "SUN VALLEY": {"TX": 1150, "CA": 275},
    "SYRACUSE": {"NJ": 450},
    "Syracuse (NY)": {"NJ": 425},
    "TALLAHASSEE": {"GA": 450},
    "Tampa": {"GA": 425},
    "Tampa (FL)": {"GA": 425},
    "Tampa North (FL)": {"GA": 425},
    "TAMPA SOUTH": {"GA": 425},
    "TANNER": {"GA": 475},
    "Taunton (MA)": {"NJ": 450},
    "Templeton (MA)": {"NJ": 450},
    "Tidewater (VA)": {"NJ": 450},
    "TIFTON": {"GA": 375},
    "TRENTON": {"NJ": 285},
    "TUCSON": {"TX": 1025, "CA": 475},
    "Tucson (AZ)": {"TX": 1025, "CA": 425},
    "TULSA": {"TX": 575},
    "Tulsa (OK)": {"TX": 550},
    "VALLEJO": {"TX": 1275, "CA": 500},
    "VAN NUYS": {"TX": 1150, "CA": 275},
    "VERMILION": {"NJ": 550},
    "WACO": {"TX": 350},
    "WALTON": {"NJ": 650, "GA": 650},
    "WASHINGTON DC": {"NJ": 400},
    "Wayland": {"NJ": 850},
    "WEST PALM BEACH": {"GA": 475},
    "WEST PALM BEACH": {"GA": 450},
    "WEST WARREN": {"NJ": 450},
    "Western Colorado (CO)": {"TX": 1150},
    "WHEELING": {"NJ": 650},
    "WICHITA": {"NJ": 750, "TX": 700},
    "Wichita (KS)": {"NJ": 750, "TX": 675},
    "Wilmington (NC)": {"GA": 450},
    "Windham": {"NJ": 550},
    "YORK HAVEN": {"NJ": 425},
    "York Springs (PA)": {"NJ": 400},
    "MULBERRY": {"GA": 500},
    "WHITE PLAINS": {"NJ": 450},
    "Shepherdsville": {"NJ": 775, "GA": 650},
    "ROSEVILLE": {"NJ": 800},
    "RICE": {"NJ": 775},
    "PORTLAND": {"NJ": 750},
    "PEMBROKE PINES": {"GA": 475},
    "PARAMOUNT": {"CA": 265},
    "Donna": {"TX": 375},
}

# ────────────────────────────────────────────────
# Freight дані з твоєї таблиці (повні)
freight = {
    "Constanta": {
        "NJ": {"GAS": 2665, "DIESEL": 2665, "EV": 2930, "HYB": 2930, "GAS 3": 2860, "DIESEL 3": 2860, "EV 3": 3265, "HYB 3": 3265, "GAS 2": 3980, "DIESEL 2": 3980, "MOTO": 2000},
        "GA": {"GAS": 2635, "DIESEL": 2635, "EV": 2860, "HYB": 2860, "GAS 3": 2760, "DIESEL 3": 2760, "EV 3": 3145, "HYB 3": 3145, "GAS 2": 3940, "DIESEL 2": 3940, "MOTO": 2000},
        "TX": {"GAS": 2755, "DIESEL": 2755, "EV": 2960, "HYB": 2960, "GAS 3": 2960, "DIESEL 3": 2960, "EV 3": 3385, "HYB 3": 3385, "GAS 2": 4180, "DIESEL 2": 4180, "MOTO": 2000},
        "CA": {"GAS": 3410, "DIESEL": 3410, "EV": 3560, "HYB": 3560, "GAS 3": 3735, "DIESEL 3": 3735, "EV 3": 4145, "HYB 3": 4145, "GAS 2": 5490, "DIESEL 2": 5490, "MOTO": 2050},
    },
    "Odesa": {
        "NJ": {"GAS": 2475, "DIESEL": 2475, "EV": 2575, "HYB": 2575, "GAS 3": 2830, "DIESEL 3": 2830, "EV 3": 3000, "HYB 3": 3000, "MOTO": 2000},
        "GA": {"GAS": 2450, "DIESEL": 2450, "EV": 2600, "HYB": 2600, "GAS 3": 2830, "DIESEL 3": 2830, "EV 3": 3000, "HYB 3": 3000, "MOTO": 2000},
        "TX": {"GAS": 2575, "DIESEL": 2575, "EV": 2700, "HYB": 2700, "GAS 3": 3000, "DIESEL 3": 3000, "EV 3": 3170, "HYB 3": 3170, "MOTO": 2000},
        "CA": {"GAS": 3250, "DIESEL": 3250, "EV": 3375, "HYB": 3375, "GAS 3": 3900, "DIESEL 3": 3900, "EV 3": 4070, "HYB 3": 4070, "MOTO": 2050},
    },
    "Klaipeda": {
        "NJ": {"GAS": 2685, "DIESEL": 2685, "EV": 2785, "HYB": 2785, "GAS 3": 2790, "DIESEL 3": 2790, "EV 3": 2890, "HYB 3": 2890, "MOTO": 2100},
        "GA": {"GAS": 2735, "DIESEL": 2735, "EV": 2835, "HYB": 2835, "GAS 3": 2840, "DIESEL 3": 2840, "EV 3": 2940, "HYB 3": 2940, "MOTO": 2100},
        "TX": {"GAS": 2860, "DIESEL": 2860, "EV": 2960, "HYB": 2960, "GAS 3": 2965, "DIESEL 3": 2965, "EV 3": 3065, "HYB 3": 3065, "MOTO": 2100},
        "CA": {"GAS": 3260, "DIESEL": 3260, "EV": 3360, "HYB": 3360, "GAS 3": 3465, "DIESEL 3": 3465, "EV 3": 3565, "HYB 3": 3565, "MOTO": 2150},
        "WA": {"GAS": 3735, "DIESEL": 3735, "EV": 2835, "HYB": 2835, "GAS 3": 4185, "DIESEL 3": 4185, "EV 3": 3285, "HYB 3": 3285, "MOTO": 3150},
    }
}

# ────────────────────────────────────────────────
col1, col2 = st.columns([6, 5])

with col1:
    st.subheader("Основні дані")

    client = st.text_input("Клієнт")
    model = st.text_input("Модель авто")
    vin = st.text_input("VIN")

    location = st.selectbox("Локація аукціону", options=sorted(tow.keys()))

    # Доступні порти для вибраної локації
    if location in tow:
        avail = {p: v for p, v in tow[location].items() if v is not None}
        if avail:
            port_label = st.selectbox("Порт США", [f"{p} — {v} $" for p, v in sorted(avail.items(), key=lambda x: x[1])])
            us_port = port_label.split(" — ")[0]
            tow_cost = avail[us_port]
        else:
            st.warning("Немає доступних портів")
            us_port = None
            tow_cost = 0
    else:
        us_port = None
        tow_cost = 0

    ua_port = st.selectbox("Порт в Україні/Європі", ["Constanta", "Odesa", "Klaipeda"])

    st.subheader("Тип авто та завантаження")

    transport_type = st.radio("Тип", ["Авто", "Мотоцикл"], horizontal=True)

    if transport_type == "Авто":
        fuel = st.selectbox("Паливо", ["GAS", "DIESEL", "EV", "HYB"])
        container = st.selectbox("Контейнер", ["1 авто (стандарт)", "3 машини", "2 місця (півконтейнера)"])
        if container == "1 авто (стандарт)":
            f_key = fuel
        elif container == "3 машини":
            f_key = fuel + " 3"
        else:
            f_key = fuel + " 2"
    else:
        f_key = "MOTO"
        fuel = None
        container = None

with col2:
    st.subheader("Додаткові витрати")

    auction = st.number_input("Збір аукціону", value=340)
    swift = st.number_input("Swift аукціон", value=121)
    insurance = st.number_input("Страхування", value=50)
    storage = st.number_input("Storage", value=0)
    other = st.number_input("Інше", value=0)
    customs = st.number_input("Митні платежі", value=1720)
    paid = st.number_input("Вже сплачено", value=0)

# ────────────────────────────────────────────────
if st.button("Розрахувати", type="primary", use_container_width=True):
    if not us_port:
        st.error("Оберіть локацію та порт США")
    else:
        try:
            freight_cost = freight[ua_port][us_port][f_key]
        except (KeyError, TypeError):
            freight_cost = None

        if freight_cost is None:
            st.error(f"Немає тарифу для {ua_port} + {us_port} + {f_key}")
        else:
            subtotal = tow_cost + freight_cost + auction + swift + insurance + storage + other
            total = subtotal + customs
            debt = total - paid

            st.success("Розрахунок готовий!")

            st.markdown(f"""
            **TOW (буксирування):** {tow_cost:,} $
            **Фрахт:** {freight_cost:,} $
            **Аукціон + Swift + Страхування:** {auction + swift + insurance:,} $
            **Storage + Інше:** {storage + other:,} $
            ───────────────────────────────
            **Сума без мита:** {subtotal:,} $
            **Митні платежі:** {customs:,} $
            **ALL IN:** **{total:,} $**

            **Сплачено:** {paid:,} $
            **До оплати (DEBT):** **{debt:,} $**
            """)

            copy_text = f"""Нікіта Калькулятор
Дата: сьогодні
Клієнт: {client}
Модель: {model}
VIN: {vin}
Локація: {location} → {us_port}
Порт UA: {ua_port}
Тип: {transport_type} {f_key if transport_type == 'Авто' else 'MOTO'}

TOW: {tow_cost}$
Фрахт: {freight_cost}$
Мито: {customs}$
ВСЬОГО: {total}$
До оплати: {debt}$"""

            st.code(copy_text, language="text")

            if st.button("Копіювати в буфер обміну"):
                st.session_state['clipboard'] = copy_text
                st.toast("Скопійовано!", icon="📋")
