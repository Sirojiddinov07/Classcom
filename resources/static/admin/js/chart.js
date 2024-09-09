document.addEventListener('DOMContentLoaded', function () {
    const labelsElement = document.getElementById('chart-labels');
    const userDataElement = document.getElementById('chart-user-data');
    const moderatorDataElement = document.getElementById('chart-moderator-data');
    const userLabelElement = document.getElementById('chart-user-label');
    const moderatorLabelElement = document.getElementById('chart-moderator-label');

    let labels = [];
    let userData = [];
    let moderatorData = [];
    let userLabel = 'Foydaluvchilar soni';
    let moderatorLabel = 'Moderatorlar soni';

    if (labelsElement && labelsElement.textContent) {
        try {
            labels = JSON.parse(labelsElement.textContent);
        } catch (e) {
            console.error('Error parsing labels JSON:', e);
        }
    }

    if (userDataElement && userDataElement.textContent) {
        try {
            userData = JSON.parse(userDataElement.textContent);
        } catch (e) {
            console.error('Error parsing user data JSON:', e);
        }
    }

    if (moderatorDataElement && moderatorDataElement.textContent) {
        try {
            moderatorData = JSON.parse(moderatorDataElement.textContent);
        } catch (e) {
            console.error('Error parsing moderator data JSON:', e);
        }
    }

    if (userLabelElement && userLabelElement.textContent) {
        try {
            userLabel = userLabelElement.textContent;
        } catch (e) {
            console.error('Error parsing user label:', e);
        }
    }

    if (moderatorLabelElement && moderatorLabelElement.textContent) {
        try {
            moderatorLabel = moderatorLabelElement.textContent;
        } catch (e) {
            console.error('Error parsing moderator label:', e);
        }
    }

    const ctx = document.getElementById('userCountChart').getContext('2d');

    const userCountChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: userLabel,
                    data: userData,
                    backgroundColor: 'rgb(65,144,176, 0.2)',
                    borderColor: 'rgb(65,144,176)',
                    borderWidth: 1
                },
                {
                    label: moderatorLabel,
                    data: moderatorData,
                    backgroundColor: 'rgb(255,44,44, 0.2)',
                    borderColor: 'rgb(255,44,44)',
                    borderWidth: 1
                }
            ]
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