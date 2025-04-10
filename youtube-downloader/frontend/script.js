document.getElementById('downloadForm').addEventListener('submit', function (e) {
  e.preventDefault();
  
  const url = document.getElementById('videoURL').value;
  const format = document.getElementById('format').value;

  document.getElementById('status').innerText = 'Processing...';

  fetch('http://localhost:5000/download', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url, format })
  })
  .then(res => {
    if (!res.ok) throw new Error('Failed to fetch');
    return res.blob();
  })
  .then(blob => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'video.' + (format === 'mp3' ? 'mp3' : 'mp4');
    document.body.appendChild(a);
    a.click();
    a.remove();
    document.getElementById('status').innerText = 'Download Ready!';
  })
  .catch(err => {
    console.error(err);
    document.getElementById('status').innerText = 'Failed to download.';
  });
});