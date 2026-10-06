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
        <div class="flex items-center justify-between pb-3 text-ink/80">
            <span class="text-sm">Temperature</span>
            <span>${temp}°C</span>
        </div>
        <div class="flex items-center justify-between pb-3 pt-2 text-ink/80">
            <span class="text-sm">Humidity</span>
            <span>${hum}%</span>
        </div>
        <div class="flex items-center justify-between pt-2 text-ink/80">
            <span class="text-sm">Cloud Cover</span>
            <span>${cloud}%</span>
        </div>
    `;
}

function updateHolidayWidget(forecast) {
    const hasHoliday = forecast.some(f => f.is_holiday === 1);
    const widget = document.getElementById('holidayWidget');
    
    if (hasHoliday) {
        widget.innerHTML = `
            <div class="flex items-start gap-2">
                <span class="text-rust text-lg leading-none">!</span>
                <span class="font-mono text-[11px] uppercase tracking-wider text-ink/80">
                    Warning: Local holiday detected in the forecast period. Model has adjusted expectations.
                </span>
            </div>
        `;
    } else {
        widget.innerHTML = `
            <div class="flex items-start gap-2">
                <span class="text-rust text-lg leading-none">↓</span>
                <span class="font-mono text-[11px] uppercase tracking-wider text-ink/80">
                    No localized holidays detected in the next 24 hours. Normal industrial operations expected.
                </span>
            </div>
        `;
    }
}

function renderChart(labels, data) {
    const ctx = document.getElementById('forecastChart').getContext('2d');
    
    if (forecastChartInstance) {
        forecastChartInstance.destroy();
    }

    // Create subtle gradient (rust)
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(217, 119, 87, 0.15)'); // Rust #d97757
    gradient.addColorStop(1, 'rgba(217, 119, 87, 0.0)');

    forecastChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'DEMAND (MW)',
                data: data,
                borderColor: '#111110', // Ink black
                backgroundColor: gradient,
                borderWidth: 2,
                pointBackgroundColor: '#d97757', // Rust dot
                pointBorderColor: '#111110',
                pointBorderWidth: 1.5,
                pointRadius: 2,
                pointHoverRadius: 5,
                fill: true,
                tension: 0.1 // More jagged, analytical feel
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: { family: "'Space Mono', monospace", size: 10, weight: 'bold' },
                        color: '#111110'
                    }
                },
                tooltip: {
                    backgroundColor: '#111110',
                    titleFont: { family: "'Space Mono', monospace", size: 11 },
                    bodyFont: { family: "'Space Mono', monospace", size: 12 },
                    padding: 10,
                    cornerRadius: 0,
                    displayColors: false,
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { 
                        maxTicksLimit: 12, 
                        font: { family: "'Space Mono', monospace", size: 10 }, 
                        color: '#111110' 
                    }
                },
                y: {
                    grid: { color: 'rgba(17, 17, 16, 0.1)', borderDash: [2, 4] },
                    ticks: { 
                        font: { family: "'Space Mono', monospace", size: 10 }, 
                        color: '#111110' 
                    }
                }
            }
        }
    });
}

// Initial load
document.getElementById('refreshBtn').addEventListener('click', fetchForecast);
fetchForecast();
