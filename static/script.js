const API_BASE = '/api';
let trendChart = null;
let selectedConsumer = 1;
let consumerHistory = {};
let startTime = null;
let lastProduced = 0;
let lastConsumed = 0;
let noChangeCount = 0;
let updateIntervals = null;

async function parseLogsForHistory() {
    try {
        const response = await fetch(`${API_BASE}/logs`);
        const data = await response.json();

        if (!startTime && data.logs.length > 0) {
            const timeMatch = data.logs[0].match(/\d{2}:\d{2}:\d{2}/);
            if (timeMatch) {
                startTime = new Date();
                startTime.setHours(parseInt(timeMatch[0].split(':')[0]));
                startTime.setMinutes(parseInt(timeMatch[0].split(':')[1]));
                startTime.setSeconds(parseInt(timeMatch[0].split(':')[2]));
            }
        }
        if (!startTime) startTime = new Date();

        const newConsumerHistory = {};

        data.logs.forEach((log) => {
            const consumerMatch = log.match(/KONSUMENT (\d+)/);
            const countMatch = log.match(/przetworzonych:\s*(\d+)/);
            const timeMatch = log.match(/(\d{2}):(\d{2}):(\d{2})/);

            if (consumerMatch && countMatch && timeMatch) {
                const consumerId = parseInt(consumerMatch[1]);
                const count = parseInt(countMatch[1]);

                const logTime = new Date();
                logTime.setHours(parseInt(timeMatch[1]));
                logTime.setMinutes(parseInt(timeMatch[2]));
                logTime.setSeconds(parseInt(timeMatch[3]));

                const elapsedSeconds = Math.round((logTime - startTime) / 1000);

                if (!newConsumerHistory[consumerId]) {
                    newConsumerHistory[consumerId] = [];
                }

                const lastPoint = newConsumerHistory[consumerId].slice(-1)[0];
                if (!lastPoint || lastPoint.count !== count) {
                    newConsumerHistory[consumerId].push({
                        time: Math.max(0, elapsedSeconds),
                        count: count,
                    });
                }
            }
        });

        consumerHistory = newConsumerHistory;
        updateTrendChart();
    } catch (error) {}
}

async function updateDashboard() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();

        const currentProduced = data.statistics.total_produced;
        const currentConsumed = data.statistics.total_consumed;

        if (
            currentProduced === lastProduced &&
            currentConsumed === lastConsumed
        ) {
            noChangeCount++;
            if (noChangeCount >= 5) {
                clearInterval(updateIntervals.dashboard);
                clearInterval(updateIntervals.logs);
                return;
            }
        } else {
            noChangeCount = 0;
            lastProduced = currentProduced;
            lastConsumed = currentConsumed;
        }

        document.getElementById('produced').textContent = currentProduced;
        document.getElementById('consumed').textContent = currentConsumed;
        document.getElementById('efficiency').textContent =
            data.statistics.efficiency_percent.toFixed(1) + '%';
        document.getElementById('defective').textContent =
            currentProduced - currentConsumed;
        document.getElementById('update-time').textContent =
            new Date().toLocaleTimeString('pl-PL');

        const producersList = document.getElementById('producers-list');
        producersList.innerHTML = '';
        data.producers.forEach((producer) => {
            const div = document.createElement('div');
            div.className = 'producer-item';
            div.innerHTML = `
                <div class="producer-label">Producent ${producer.id} - ${
                producer.count
            } elementów</div>
                <div class="items-list">${producer.items.join(', ')}</div>
            `;
            producersList.appendChild(div);
        });

        const consumersList = document.getElementById('consumers-list');
        consumersList.innerHTML = '';
        data.consumers.forEach((consumer) => {
            const div = document.createElement('div');
            div.className = 'consumer-item';
            div.innerHTML = `
                <div class="consumer-label">Konsument ${consumer.id} - ${
                consumer.count
            } elementów</div>
                <div class="items-list">${consumer.items.join(', ')}</div>
            `;
            consumersList.appendChild(div);
        });

        await parseLogsForHistory();
        updateConsumerButtons(data);
    } catch (error) {}
}

async function updateLogs() {
    try {
        const response = await fetch(`${API_BASE}/logs`);
        const data = await response.json();

        const logsContent = document.getElementById('logs-content');
        logsContent.innerHTML = data.logs
            .map((log) => `<div class="log-line">${escapeHtml(log)}</div>`)
            .join('');

        logsContent.scrollTop = logsContent.scrollHeight;
    } catch (error) {}
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
    };
    return text.replace(/[&<>"']/g, (m) => map[m]);
}

function initTrendChart() {
    const ctx = document.getElementById('trendChart');
    if (!ctx) return;

    trendChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: `Konsument ${selectedConsumer}`,
                    data: [],
                    borderColor: '#667eea',
                    backgroundColor: '#667eea20',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            animation: false,
            scales: {
                x: {
                    title: { display: true, text: 'Czas (sekundy)' },
                },
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Skonsumowane elementy' },
                },
            },
            plugins: {
                legend: { position: 'bottom' },
            },
        },
    });
}

function updateConsumerButtons(data) {
    const container = document.getElementById('consumer-buttons');
    if (!container || container.children.length > 0) return;

    data.consumers.forEach((consumer) => {
        const btn = document.createElement('button');
        btn.className = `consumer-btn ${
            consumer.id === selectedConsumer ? 'active' : ''
        }`;
        btn.textContent = `Konsument ${consumer.id}`;
        btn.onclick = () => selectConsumer(consumer.id);
        container.appendChild(btn);
    });
}

function selectConsumer(consumerId) {
    selectedConsumer = consumerId;

    document.querySelectorAll('.consumer-btn').forEach((btn, idx) => {
        if (idx + 1 === consumerId) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    updateTrendChart();
}

function updateTrendChart() {
    if (!trendChart || !consumerHistory[selectedConsumer]) return;

    const history = consumerHistory[selectedConsumer];

    trendChart.data.labels = history.map((point) => point.time + 's');
    trendChart.data.datasets[0].data = history.map((point) => point.count);
    trendChart.data.datasets[0].label = `Konsument ${selectedConsumer}`;

    trendChart.update('none');
}

function updateConsumptionChart(data) {
    if (!trendChart) return;

    const labels = data.consumers.map((c) => `Konsument ${c.id}`);
    const counts = data.consumers.map((c) => c.count);

    consumptionChart.data.labels = labels;
    consumptionChart.data.datasets[0].data = counts;
    consumptionChart.update('none');
}

initTrendChart();
updateDashboard();
updateLogs();
updateIntervals = {
    dashboard: setInterval(updateDashboard, 1000),
    logs: setInterval(updateLogs, 2000),
};
