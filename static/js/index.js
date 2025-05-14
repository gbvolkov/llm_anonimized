function toggleResponses() {
    const llmDiv = document.getElementById('llm_response');
    const deanDiv = document.getElementById('dean_response');
    const view = document.querySelector('input[name="view"]:checked').value;
    llmDiv.hidden = (view !== 'llm');
    deanDiv.hidden = (view !== 'dean');
}

document.addEventListener('DOMContentLoaded', function() {
  const link = document.getElementById('config-link');
  if (!link) return;

  link.addEventListener('click', function(e) {
    e.preventDefault();
    const model = document.getElementById('model').value;
    const baseUrl = link.getAttribute('data-config-url');
    window.location.href = baseUrl + '?model=' + encodeURIComponent(model);
  });
});
