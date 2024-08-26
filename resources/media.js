const BASE_URL = 'http://' + window.location.hostname + ':8081';

document.getElementById('mediaForm')?.addEventListener('submit', function (event) {
    event.preventDefault();

    const mediaInputs = document.querySelectorAll('.mediaInput');
    const mediaData = [];

    mediaInputs.forEach(input => {
        const fileDesc = input.querySelector('input[name="desc"]')?.value;
        const mediaFile = input.querySelector('input[name="file"]')?.files[0];

        if (fileDesc) {
            mediaData.push({
                file: mediaFile ? mediaFile.name : "",  // Use file name or empty string
                desc: fileDesc
            });
        }
    });

    const requestData = {
        media: mediaData
    };

    fetch(BASE_URL + `/media/?topic_id=21`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)  // Send requestData as JSON
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then(data => {
                    throw new Error(data.detail || 'Unknown error');
                });
            }
        })
        .then(data => {
            document.getElementById('response').innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            if (error.name === 'TypeError') {
                document.getElementById('response').innerText = 'Network error: ' + error.message;
            } else {
                document.getElementById('response').innerText = 'Error: ' + error.message;
            }
        });
});