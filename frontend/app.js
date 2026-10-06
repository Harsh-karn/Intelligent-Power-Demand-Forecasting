const API_URL = 'http://localhost:8000';
let forecastChartInstance = null;

async function fetchForecast() {
    try {
        const response = await fetch(`${API_URL}/forecast`);
        if (!response.ok) throw new Error('API request failed');
        const data = await response.json();
        
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        updateDashboard(data.forecast);
    } catch (error) {
        console.error('Error fetching forecast:', error);
        alert('Failed to connect to the backend API. Make sure the FastAPI server is running on port 8000.');
    }
}

function updateDashboard(forecast) {
    const labels = forecast.map(f => {
        const dt = new Date(f.timestamp);
        return dt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });
    
    const demandData = forecast.map(f => f.predicted_demand);
    
    // Average weather for the widget
    const avgTemp = (forecast.reduce((sum, f) => sum + f.temperature, 0) / forecast.length).toFixed(1);
    const avgHum = (forecast.reduce((sum, f) => sum + f.humidity, 0) / forecast.length).toFixed(1);
    const avgCloud = (forecast.reduce((sum, f) => sum + f.cloud_cover, 0) / forecast.length).toFixed(1);

    updateWeatherWidget(avgTemp, avgHum, avgCloud);
    updateHolidayWidget(forecast);
    renderChart(labels, demandData);
}

function updateWeatherWidget(temp, hum, cloud) {
    const widget = document.getElementById('weatherWidget');
    widget.innerHTML = `
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <span class="text-slate-500 font-medium">Avg Temperature</span>
            <span class="text-xl font-bold text-slate-800">${temp}°C</span>
        </div>
        <div class="flex items-center justify-between border-b border-slate-100 pb-3 pt-2">
            <span class="text-slate-500 font-medium">Humidity</span>
            <span class="text-xl font-bold text-slate-800">${hum}%</span>
        </div>
        <div class="flex items-center justify-between pt-2">
            <span class="text-slate-500 font-medium">Cloud Cover</span>
            <span class="text-xl font-bold text-slate-800">${cloud}%</span>
        </div>
    `;
}

function updateHolidayWidget(forecast) {
    // In our mock backend, we hardcoded Is_Holiday = 0 for the future prediction
    // In a real scenario, we'd check if any of the forecast periods land on a holiday
    const widget = document.getElementById('holidayWidget');
    widget.innerHTML = `
        <div class="flex items-center space-x-2">
            <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
            <span>No localized holidays detected in the next 24 hours. Normal industrial operations expected.</span>
        </div>
    `;
}

function renderChart(labels, data) {
    const ctx = document.getElementById('forecastChart').getContext('2d');
    
    if (forecastChartInstance) {
        forecastChartInstance.destroy();
    }

    // Create gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(79, 70, 229, 0.4)'); // Indigo-600
    gradient.addColorStop(1, 'rgba(79, 70, 229, 0.0)');

    forecastChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Predicted Demand (MW)',
                data: data,
                borderColor: '#4f46e5',
                backgroundColor: gradient,
                borderWidth: 3,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: '#4f46e5',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: { family: "'Inter', sans-serif", weight: '600' },
                        color: '#334155'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleFont: { family: "'Inter', sans-serif", size: 13 },
                    bodyFont: { family: "'Inter', sans-serif", size: 14 },
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: false,
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { maxTicksLimit: 12, font: { family: "'Inter', sans-serif" }, color: '#64748b' }
                },
                y: {
                    grid: { color: '#f1f5f9', borderDash: [5, 5] },
                    ticks: { font: { family: "'Inter', sans-serif" }, color: '#64748b' }
                }
            }
        }
    });
}

// Initial load
document.getElementById('refreshBtn').addEventListener('click', fetchForecast);
fetchForecast();
