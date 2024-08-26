const BASE_URL = 'http://' + window.location.hostname + ':8081';

document.getElementById('addMediaInput').addEventListener('click', function () {
    const mediaInputs = document.getElementById('mediaInputs');
    const newMediaInput = document.createElement('div');
    newMediaInput.classList.add('mediaInput');
    newMediaInput.innerHTML = `
        <label for="file_desc">Description:</label>
        <input type="text" name="file_desc" required><br><br>

        <label for="media_files">Select Media Files:</label>
        <input type="file" name="media_files" required><br><br>
    `;
    mediaInputs.appendChild(newMediaInput);
});

document.getElementById('mediaForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const topicId = document.getElementById('topic_id').value;
    const mediaInputs = document.querySelectorAll('.mediaInput');
    const formData = new FormData();

    formData.append('topic_id', topicId);
    mediaInputs.forEach(input => {
        const fileDesc = input.querySelector('input[name="file_desc"]').value;
        const mediaFile = input.querySelector('input[name="media_files"]').files[0];

        formData.append('file_desc', fileDesc);
        formData.append('media_files', mediaFile);
    });

    const queryParams = new URLSearchParams({topic_id: topicId}).toString();

    fetch(BASE_URL + `/media/?${queryParams}`, {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.detail || 'Unknown error');
                });
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('response').innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById('response').innerText = 'Error: ' + error.message;
        });
});