document.addEventListener('DOMContentLoaded', function() {
  const select = document.getElementById('model_select');
  if (!select) return;

  select.addEventListener('change', function() {
    const baseUrl = select.dataset.configUrl;
    const model = this.value;
    window.location.href = baseUrl + '?model=' + encodeURIComponent(model);
  });
});
