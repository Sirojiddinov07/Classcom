// resources/static/admin/js/chart.js
document.addEventListener('DOMContentLoaded', function () {
    // Retrieve and parse JSON data from hidden script elements
    const labelsElement = document.getElementById('chart-labels');
    const dataElement = document.getElementById('chart-data');
    const labelElement = document.getElementById('chart-label');

    let labels = [];
    let data = [];
    let label = 'User Count'; // Default label

    if (labelsElement && labelsElement.textContent) {
        try {
            labels = JSON.parse(labelsElement.textContent);
        } catch (e) {
            console.error('Error parsing labels JSON:', e);
        }
    }

    if (dataElement && dataElement.textContent) {
        try {
            data = JSON.parse(dataElement.textContent);
        } catch (e) {
            console.error('Error parsing data JSON:', e);
        }
    }

    if (labelElement && labelElement.textContent) {
        label = labelElement.textContent;
    }

    console.log(labels);
    console.log(data);

    // Create the chart
    const ctx = document.getElementById('userCountChart').getContext('2d');
    const userCountChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(65,144,176)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});