// DOM Elements
const recordButton = document.getElementById('recordButton');
const recordingStatus = document.getElementById('recordingStatus');
const audioFile = document.getElementById('audioFile');
const results = document.getElementById('results');
const originalText = document.getElementById('originalText');
const correctedText = document.getElementById('correctedText');
const playAudio = document.getElementById('playAudio');
const loading = document.getElementById('loading');

// Audio recording variables
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// Handle audio recording
recordButton.addEventListener('click', async () => {
    if (!isRecording) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                await processAudio(audioBlob);
            };

            mediaRecorder.start();
            isRecording = true;
            recordButton.classList.add('recording');
            recordingStatus.textContent = 'Recording...';
        } catch (err) {
            console.error('Error accessing microphone:', err);
            alert('Error accessing microphone. Please ensure you have granted microphone permissions.');
        }
    } else {
        mediaRecorder.stop();
        isRecording = false;
        recordButton.classList.remove('recording');
        recordingStatus.textContent = 'Processing...';
    }
});

// Handle file upload
audioFile.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (file) {
        await processAudio(file);
    }
});

// Drag and drop functionality
const dropZone = document.querySelector('.border-2');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropZone.classList.add('drag-over');
}

function unhighlight(e) {
    dropZone.classList.remove('drag-over');
}

dropZone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const file = dt.files[0];
    if (file && file.type.startsWith('audio/')) {
        processAudio(file);
    }
}

// Process audio file
async function processAudio(audioFile) {
    try {
        showLoading();
        const formData = new FormData();
        formData.append('audio', audioFile);

        const response = await fetch('/correct/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        // Update UI with results
        originalText.textContent = data.original_text;
        correctedText.textContent = data.corrected_text;
        
        // Set up audio playback
        playAudio.onclick = () => {
            const audio = new Audio(data.audio_path);
            audio.play();
        };

        showResults();
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while processing the audio. Please try again.');
    } finally {
        hideLoading();
    }
}

// UI Helper functions
function showLoading() {
    loading.classList.remove('hidden');
    results.classList.add('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
}

function showResults() {
    results.classList.remove('hidden');
} 