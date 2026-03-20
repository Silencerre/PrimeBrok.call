<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Логистический калькулятор США</title>
    <style>
        :root {
            --primary: #2c3e50;
            --accent: #e74c3c;
            --light: #ecf0f1;
        }
        body { font-family: 'Segoe UI', sans-serif; background: #f4f7f6; padding: 20px; }
        .calc-card {
            max-width: 500px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        h2 { text-align: center; color: var(---primary); margin-bottom: 25px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: 600; color: #555; }
        select, input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 16px;
        }
        .result-box {
            margin-top: 25px;
            padding: 20px;
            background: var(--primary);
            color: white;
            border-radius: 10px;
            text-align: center;
        }
        .total-price { font-size: 28px; font-weight: bold; color: #2ecc71; }
        .detail { font-size: 14px; color: #bdc3c7; margin-top: 10px; }
    </style>
</head>
<body>

<div class="calc-card">
    <h2>Калькулятор доставки</h2>
    
    <div class="form-group">
        <label>Пункт назначения</label>
        <select id="destination" onchange="calculate()">
            <option value="odesa">Одесса, Украина</option>
            <option value="constanta">Констанца, Румыния</option>
        </select>
    </div>

    <div class="form-group">
        <label>Штат отправки (Порт)</label>
        <select id="origin" onchange="calculate()">
            <option value="NJ">New Jersey (NJ)</option>
            <option value="GA">Georgia (GA)</option>
            <option value="TX">Texas (TX)</option>
            <option value="CA">California (CA)</option>
        </select>
    </div>

    <div class="form-group">
        <label>Тип топлива / Загрузка</label>
        <select id="type" onchange="calculate()">
            <option value="gas">Бензин / Дизель</option>
            <option value="ev">Электро / Гибрид</option>
            <option value="gas3">Контейнер на 3 авто</option>
        </select>
    </div>

    <div class="form-group">
        <label>Доставка до порта (Towing), $</label>
        <input type="number" id="towing" value="300" oninput="calculate()">
    </div>

    <div class="result-box">
        <div>Финальная стоимость доставки:</div>
        <div class="total-price" id="totalResult">$0</div>
        <div class="detail" id="breakdown">Выберите параметры</div>
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
        const total = seaFreight + towing;

        document.getElementById('totalResult').innerText = '$' + total;
        document.getElementById('breakdown').innerText = 
            `Фрахт: $${seaFreight} + Эвакуатор: $${towing}`;
    }

    // Инициализация при загрузке
    calculate();
</script>

</body>
</html>
