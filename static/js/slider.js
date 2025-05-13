document.addEventListener('DOMContentLoaded', () => {
  const slider    = document.getElementById('detail-slider');
  const toggleBtn = document.getElementById('toggle-slider');
  const closeBtn  = document.getElementById('close-slider');
  const tabBtns   = slider.querySelectorAll('.tab-btn');
  const panes     = slider.querySelectorAll('.pane');

  // open/close panel
  toggleBtn.addEventListener('click', () => {
    const isOpen = slider.classList.toggle('open');
    if (isOpen) {
      // default to first tab
      tabBtns.forEach((t,i) => {
        t.classList.toggle('active', i===0);
        panes[i].classList.toggle('active', i===0);
      });
    }
  });

  // close via “×”
  closeBtn.addEventListener('click', () => {
    slider.classList.remove('open');
  });

  // tab switching
  tabBtns.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;
      tabBtns.forEach(t => t.classList.toggle('active', t===tab));
      panes.forEach(p => p.classList.toggle('active', p.id === 'pane-' + target));
    });
  });
});
