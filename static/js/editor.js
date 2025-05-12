// editor.js
// Renders deanonimizedContent (HTML or Markdown) into #viewer safely

function renderViewer() {
  // Raw content from server or LLM
  var raw = window.deanonimizedContent || '';
  // Current format selection
  var fmt = document.getElementById('format-select').value;

  // Convert Markdown to HTML if needed
  var html = fmt === 'markdown'
    ? marked.parse(raw)
    : raw;

  // Sanitize the HTML
  var clean = DOMPurify.sanitize(html, {
    // Optionally restrict tags/attributes:
    // ALLOWED_TAGS: ['p','a','ul','li','strong','em','img'],
    // ALLOWED_ATTR: ['href','src','alt']
  });

  // Inject into viewer
  document.getElementById('viewer').innerHTML = clean;
}

// Initialize on page load and re-render on format change
window.addEventListener('DOMContentLoaded', function() {
  var sel = document.getElementById('format-select');
  sel.addEventListener('change', renderViewer);
  renderViewer();
});