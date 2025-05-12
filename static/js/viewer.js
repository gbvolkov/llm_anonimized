// viewer.js

function renderViewer() {
  // Get raw content and selected format
  var raw = deanonimizedContent || '';
  var format = document.getElementById('format-select').value;

  // Convert Markdown if needed
  var html = (format === 'markdown')
    ? marked.parse(raw)
    : raw;

  // Sanitize the generated HTML
  var clean = DOMPurify.sanitize(html, {
    // Optionally customize tags/attributes:
    // ALLOWED_TAGS: ['p','a','strong','em','ul','li','img', ...],
    // ALLOWED_ATTR: ['href','src','alt', ...]
  });

  // Render into the div
  document.getElementById('viewer').innerHTML = clean;
}

// Initial render and re-render on format change
window.addEventListener('DOMContentLoaded', function() {
  var select = document.getElementById('format-select');
  select.addEventListener('change', renderViewer);
  renderViewer();
});