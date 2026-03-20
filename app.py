import streamlit as st
import pandas as pd

# Налаштування сторінки
st.set_page_config(page_title="PrimeBrok - Калькулятор авто зі США", layout="centered")

def main():
    st.title("🚢 PrimeBrok")
    st.subheader("Професійний калькулятор вартості авто зі США")

    # --- БОКОВА ПАНЕЛЬ (Введення даних) ---
    st.sidebar.header("📋 Параметри авто")
    
    auction = st.sidebar.selectbox("Оберіть аукціон", ["IAAI", "Copart"])
    lot_price = st.sidebar.number_input("Ціна лота на аукціоні ($)", min_value=0, value=2000, step=100)
    
    engine_type = st.sidebar.selectbox("Тип двигуна", ["Бензин", "Дизель", "Гібрид", "Електро"])
    engine_volume = st.sidebar.number_input("Об'єм двигуна (л)", min_value=0.0, value=2.0, step=0.1)
    year = st.sidebar.number_input("Рік випуску", min_value=1990, max_value=2026, value=2020)
    
    body_type = st.sidebar.selectbox("Тип кузова", ["Седан", "SUV/Кросовер"])
    
    # --- ЛОГІКА РОЗРАХУНКУ (Приклад на основі вашої таблиці) ---
    
    # 1. Аукціонний збір (спрощена модель для прикладу, можна замінити на повну сітку)
    auction_fee = 630 if lot_price <= 2000 else 850 
    swift_fee = 166
    
    # 2. Логістика (базується на вашій вкладці TOW)
    # Тут ми можемо додати пошук по місту, як у вашій таблиці
    transport_cost = 2685 # Значення за замовчуванням з вашого прикладу
    insurance = 50
    
    # 3. Митні платежі (приклад розрахунку)
    customs_fee = 850 # Значення з вашої таблиці
    
    # --- ВИВІД РЕЗУЛЬТАТІВ ---
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 💰 Витрати в США")
        st.write(f"**Ставка:** ${lot_price}")
        st.write(f"**Збір аукціону:** ${auction_fee}")
        st.write(f"**Swift-платіж:** ${swift_fee}")
        st.write(f"**Транспортування:** ${transport_cost}")
        st.write(f"**Страхування:** ${insurance}")

    with col2:
        st.write("### 🇪🇺 Витрати в Україні")
        st.write(f"**Митні платежі:** ${customs_fee}")
        st.write(f"**Інше:** $0")
        
    total_cost = lot_price + auction_fee + swift_fee + transport_cost + insurance + customs_fee
    
    st.success(f"## Загальна вартість (ALL IN): ${total_cost}")
    
    st.info("Розрахунок є попереднім. Для точного прорахунку зверніться до менеджера PrimeBrok.")

if __name__ == "__main__":
    main()
