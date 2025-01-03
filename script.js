const downloadButton = document.getElementById('download');
const status = document.getElementById('status');

downloadButton.addEventListener('click', async () => {
    const url = document.getElementById('url').value.trim();
    const format = document.getElementById('format').value;

    if (!url) {
        status.textContent = "Please enter a valid URL.";
        return;
    }

    try {
        status.textContent = "Processing...";
        const response = await fetch('http://127.0.0.1:8000/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, format }),
        });

        const data = await response.json();
        if (data.success) {
            window.location.href = `http://127.0.0.1:8000/files/${data.file_name}`;
        } else {
            status.textContent = data.detail;
        }
    } catch (error) {
        console.error(error);
        status.textContent = "An error occurred while downloading the video.";
    }
});
