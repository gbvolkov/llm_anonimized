function toggleResponses() {
    const llmDiv = document.getElementById('llm_response');
    const deanDiv = document.getElementById('dean_response');
    const view = document.querySelector('input[name="view"]:checked').value;
    llmDiv.hidden = (view !== 'llm');
    deanDiv.hidden = (view !== 'dean');
}

document.addEventListener('DOMContentLoaded', function() {
  // Config page navigation
  const link = document.getElementById('config-link');
  if (link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const model = document.getElementById('model').value;
      const baseUrl = link.getAttribute('data-config-url');
      window.location.href = baseUrl + '?model=' + encodeURIComponent(model);
    });
  }

  // Show spinner on form submission
  const form = document.getElementById('mainForm');
  const spinner = document.getElementById('spinner-overlay');
  if (form && spinner) {
    form.addEventListener('submit', function() {
      // Show spinner by removing visual hide
      spinner.classList.remove('visually-hidden');
    });;
  }
});
