const summarizeBtn = document.getElementById('summarizeBtn')
const inputText = document.getElementById('inputText')
const output = document.getElementById('output')

summarizeBtn.addEventListener('click', async () => {
  const text = inputText.value.trim()
  if(!text){ output.textContent = 'Please paste some text first.'; return }
  output.textContent = 'Summarizing... (this may take a few seconds)'
  const minLen = parseInt(document.getElementById('minLen').value) || 30
  const maxLen = parseInt(document.getElementById('maxLen').value) || 130
  try{
    const res = await fetch('http://localhost:8000/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, min_length: minLen, max_length: maxLen })
    })
    if(!res.ok){ const err = await res.json(); output.textContent = 'Error: ' + err.detail; return }
    const data = await res.json()
    output.textContent = data.summary
  }catch(err){
    output.textContent = 'Network error — make sure backend is running at http://localhost:8000'
  }
})
