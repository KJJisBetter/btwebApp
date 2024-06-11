document.addEventListener('DOMContentLoaded', function() {
    // Fetch transactions data from the APi
    fetch('/api/daily_spending')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('dailySpendingChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Daily Spending',
                        data: data.data,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                        hoverBackgroundColor: 'rgba(255, 99, 132, 0.4)',
                        hoverBorderColor: 'rgba(255, 99, 132, 1)'
                    }]
                },
                options: {
                    plugins: {
                        title: {
                            display: true,
                            text: 'Daily Spending',
                            font: {
                                size: 24
                            },
                            color: '#333'
                        },
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                font: {
                                    size: 14
                                },
                                color: '#333'
                            }
                        },
                        tooltip: {
                            enabled: true,
                            backgroundColor: 'rgba(0,0,0,0.7)',
                            titleFont: {
                                size: 16
                            },
                            bodyFont: {
                                size: 14
                            },
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    label += '$' + context.parsed.y.toFixed(2);
                                    return label;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return '$' + value;
                                },
                                font: {
                                    size: 14
                                },
                                color: '#333'
                            },
                            title: {
                                display: true,
                                text: 'Amount ($)',
                                font: {
                                    size: 16
                                },
                                color: '#333'
                            },
                            grid: {
                                color: 'rgba(0,0,0,0.1)'
                            }
                        },
                        x: {
                            ticks: {
                                font: {
                                    size: 14
                                },
                                color: '#333'
                            },
                            title: {
                                display: true,
                                text: 'Date',
                                font: {
                                    size: 16
                                },
                                color: '#333'
                            },
                            grid: {
                                color: 'rgba(0,0,0,0.1)'
                            }
                        }
                    },
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        })
        .catch(error => {
            console.error('Error', error);
        });
});

    //continue here
