const API_BASE = '/api';

async function updateDashboard() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        
        // Update statystyki
        document.getElementById('produced').textContent = data.statistics.total_produced;
        document.getElementById('consumed').textContent = data.statistics.total_consumed;
        document.getElementById('efficiency').textContent = data.statistics.efficiency_percent.toFixed(1) + '%';
        document.getElementById('throughput').textContent = data.statistics.average_throughput_per_sec.toFixed(2) + ' elem/s';
        document.getElementById('update-time').textContent = new Date().toLocaleTimeString('pl-PL');
        
        // Update producenci
        const producersList = document.getElementById('producers-list');
        producersList.innerHTML = '';
        data.producers.forEach(producer => {
            const div = document.createElement('div');
            div.className = 'producer-item';
            div.innerHTML = `
                <div class="producer-label">Producent ${producer.id} - ${producer.count} elementów</div>
                <div class="items-list">${producer.items.join(', ')}</div>
            `;
            producersList.appendChild(div);
        });
        
        // Update konsumenci
        const consumersList = document.getElementById('consumers-list');
        consumersList.innerHTML = '';
        data.consumers.forEach(consumer => {
            const div = document.createElement('div');
            div.className = 'consumer-item';
            div.innerHTML = `
                <div class="consumer-label">Konsument ${consumer.id} - ${consumer.count} elementów</div>
                <div class="items-list">${consumer.items.join(', ')}</div>
            `;
            consumersList.appendChild(div);
        });
        
    } catch (error) {
        console.error('Błąd aktualizacji statystyk:', error);
    }
}

async function updateLogs() {
    try {
        const response = await fetch(`${API_BASE}/logs`);
        const data = await response.json();
        
        const logsContent = document.getElementById('logs-content');
        logsContent.innerHTML = data.logs
            .map(log => `<div class="log-line">${escapeHtml(log)}</div>`)
            .join('');
        
        // Przewiń na dół
        logsContent.scrollTop = logsContent.scrollHeight;
    } catch (error) {
        console.error('Błąd aktualizacji logów:', error);
    }
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Update co 1 sekundę
updateDashboard();
updateLogs();
setInterval(updateDashboard, 1000);
setInterval(updateLogs, 2000);
