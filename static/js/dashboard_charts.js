// ===========================
// GRÁFICOS DO DASHBOARD
// ===========================

document.addEventListener('DOMContentLoaded', function () {
    // Gráfico de Barras (Ocorrências por Mês)
    const ctxMes = document.getElementById('graficoMes');
    if (ctxMes && chartData.labelsMeses && chartData.valoresMeses) {
        new Chart(ctxMes, {
            type: 'bar',
            data: {
                labels: chartData.labelsMeses,
                datasets: [{
                    label: 'Ocorrências',
                    data: chartData.valoresMeses,
                    backgroundColor: '#7b3ff2',
                    borderRadius: 6,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    tooltip: { backgroundColor: '#7b3ff2', titleColor: '#fff' },
                },
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1 } }
                }
            }
        });
    }

    // Gráfico de Pizza (Ocorrências por Cidade)
    const ctxCidade = document.getElementById('graficoCidades');
    if (ctxCidade && chartData.labelsCidades && chartData.valoresCidades) {
        new Chart(ctxCidade, {
            type: 'pie',
            data: {
                labels: chartData.labelsCidades,
                datasets: [{
                    data: chartData.valoresCidades,
                    backgroundColor: ['#7b3ff2', '#ff00a8', '#00a65a', '#f39c12', '#ff0000'],
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: { backgroundColor: '#7b3ff2', titleColor: '#fff' },
                }
            }
        });
    }
});
