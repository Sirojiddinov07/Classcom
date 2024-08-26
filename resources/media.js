const BASE_URL = 'http://' + window.location.hostname + ':8081';

document.getElementById('addMediaInput')?.addEventListener('click', function () {
    const mediaInputs = document.getElementById('mediaInputs');
    if (mediaInputs) {
        const newMediaInput = document.createElement('div');
        newMediaInput.classList.add('mediaInput');
        newMediaInput.innerHTML = `
            <label for="desc">Description:</label>
            <input type="text" name="desc" required><br><br>

            <label for="file">Select Media Files:</label>
            <input type="file" name="file" required><br><br>
        `;
        mediaInputs.appendChild(newMediaInput);
    }
});

document.getElementById('mediaForm')?.addEventListener('submit', function (event) {
    event.preventDefault();

    const mediaInputs = document.querySelectorAll('.mediaInput');
    const mediaData = [];

    Promise.all(Array.from(mediaInputs).map((input, index) => {
        const fileDesc = input.querySelector('input[name="desc"]')?.value;
        const mediaFile = input.querySelector('input[name="file"]')?.files[0];

        if (fileDesc && mediaFile) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = function(event) {
                    mediaData.push({
                        file: event.target.result.split(',')[1], // Base64 encoded file
                        desc: fileDesc
                    });
                    resolve();
                };
                reader.onerror = reject;
                reader.readAsDataURL(mediaFile); // Reads the file as Base64
            });
        }
    })).then(() => {
        const requestData = {
            media: mediaData
        };

        return fetch(BASE_URL + `/media/?topic_id=21`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            return response.json().then(data => {
                throw new Error(data.detail || 'Unknown error');
            });
        }
    }).then(data => {
        document.getElementById('response').innerText = JSON.stringify(data, null, 2);
    }).catch(error => {
        document.getElementById('response').innerText = 'Error: ' + error.message;
    });
});
