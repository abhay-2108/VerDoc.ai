// Basic Markdown to HTML formatter
function formatMarkdown(text) {
  if (!text) return '';

  return text
    .replace(/^### (.*$)/gim, '<h3>$1</h3>') // Headers
    .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')   // Bold
    .replace(/-(.*?$)/gim, '<li>$1</li>')     // Bullet points
    .replace(/\n\n/g, '<br><br>')              // Paragraphs
    .replace(/\n/g, '<br>');                   // Single newlines
}

document.getElementById('dropZone').addEventListener('click', () => {
  document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    document.querySelector('.upload-area p').textContent = e.target.files[0].name;
  }
});

document.getElementById('analyzeBtn').addEventListener('click', async () => {
  const fileInput = document.getElementById('fileInput');
  const status = document.getElementById('status');
  const resultsDiv = document.getElementById('results');
  const adviceDiv = document.getElementById('advice');

  if (fileInput.files.length === 0) {
    alert('Please select a file first.');
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  status.textContent = '🔄 Analyzing with CrewAI...';
  resultsDiv.style.display = 'none';

  try {
    const response = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error('API Error');

    const result = await response.json();

    status.textContent = '✅ Analysis Complete';
    resultsDiv.style.display = 'block';
    document.getElementById('docType').textContent = `Document Type: ${result.doc_type}`;

    // Format the final advice with markdown
    adviceDiv.innerHTML = formatMarkdown(result.final_advice);

  } catch (error) {
    status.textContent = '❌ Connection Error';
    console.error(error);
  }
});
