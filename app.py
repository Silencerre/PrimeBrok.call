import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Calculator", layout="centered")

# Ваш калькулятор внутри Streamlit
calc_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        :root { --primary: #2c3e50; --accent: #e74c3c; }
        body { font-family: sans-serif; background: #f4f7f6; padding: 10px; margin: 0; }
        .calc-card {
            max-width: 500px; margin: 0 auto; background: white;
            padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        select, input {
            width: 100%; padding: 10px; margin: 8px 0;
            border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box;
        }
        .result-box {
            margin-top: 20px; padding: 15px; background: #2c3e50;
            color: white; border-radius: 8px; text-align: center;
        }
        .total-price { font-size: 24px; font-weight: bold; color: #2ecc71; }
    </style>
</head>
<body>
<div class="calc-card">
    <label>Назначение</label>
    <select id="destination" onchange="calculate()">
        <option value="odesa">Одесса, Украина</option>
        <option value="constanta">Констанца, Румыния</option>
    </select>

    <label>Штат (Порт)</label>
    <select id="origin" onchange="calculate()">
        <option value="NJ">New Jersey (NJ)</option>
        <option value="GA">Georgia (GA)</option>
        <option value="TX">Texas (TX)</option>
        <option value="CA">California (CA)</option>
    </select>

    <label>Тип топлива</label>
    <select id="type" onchange="calculate()">
        <option value="gas">Бензин / Дизель</option>
        <option value="ev">Электро / Гибрид</option>
        <option value="gas3">Контейнер на 3 авто</option>
    </select>

    <label>Доставка до порта (Towing), $</label>
    <input type="number" id="towing" value="300" oninput="calculate()">

    <div class="result-box">
        <div>Итого доставка:</div>
        <div class="total-price" id="totalResult">$0</div>
    </div>
</div>

<script>
    const rates = {
        odesa: {
            NJ: { gas: 2475, ev: 2575, gas3: 2830 },
            GA: { gas: 2450, ev: 2600, gas3: 2830 },
            TX: { gas: 2575, ev: 2700, gas3: 3000 },
            CA: { gas: 3250, ev: 3375, gas3: 3900 }
        },
        constanta: {
            NJ: { gas: 2665, ev: 2930, gas3: 2860 },
            GA: { gas: 2635, ev: 2860, gas3: 2760 },
            TX: { gas: 2755, ev: 2960, gas3: 2960 },
            CA: { gas: 3410, ev: 3560, gas3: 3735 }
        }
    };

    function calculate() {
        const dest = document.getElementById('destination').value;
        const origin = document.getElementById('origin').value;
        const type = document.getElementById('type').value;
        const towing = parseFloat(document.getElementById('towing').value) || 0;
        const seaFreight = rates[dest][origin][type];
        document.getElementById('totalResult').innerText = '$' + (seaFreight + towing);
    }
    calculate();
</script>
</body>
</html>
"""

# Отрисовка компонента в Streamlit
components.html(calc_html, height=600)
