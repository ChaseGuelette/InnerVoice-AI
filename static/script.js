function submitForm() {
    const inputText = document.getElementById('inputText').value;
    const inputEmotions = document.getElementById('inputEmotions').value;

    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `inputText=${encodeURIComponent(inputText)}&inputEmotions=${encodeURIComponent(inputEmotions)}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('responseText').innerText = data.responseText;
        const audioElement = document.getElementById('audio');
        const audioSource = document.getElementById('audioSource');
        audioSource.src = 'static/output.mp3' + '?' + new Date().getTime(); // Force reload the audio by adding a timestamp
        audioElement.hidden = false;
        audioElement.load();  // Reload the audio element to play the new audio file
    })
    .catch(error => {
        console.error('Error:', error);
    });
}