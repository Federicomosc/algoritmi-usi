(function () {
  var sidebar = document.getElementById('sidebar');
  var overlay = document.getElementById('sidebarOverlay');
  var btn = document.getElementById('menuBtn');
  var titleEl = document.getElementById('mobileTitle');

  if (!sidebar || !btn) return;

  if (titleEl) {
    var headerTitle = sidebar.querySelector('.sidebar-header .title');
    titleEl.textContent = headerTitle
      ? headerTitle.textContent.trim()
      : document.title.split('—')[0].trim();
  }

  function closeMenu() {
    sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
    document.body.classList.remove('menu-open');
    btn.setAttribute('aria-expanded', 'false');
    btn.textContent = '☰';
  }

  function openMenu() {
    sidebar.classList.add('open');
    if (overlay) overlay.classList.add('open');
    document.body.classList.add('menu-open');
    btn.setAttribute('aria-expanded', 'true');
    btn.textContent = '✕';
  }

  btn.addEventListener('click', function () {
    if (sidebar.classList.contains('open')) closeMenu();
    else openMenu();
  });

  if (overlay) overlay.addEventListener('click', closeMenu);

  sidebar.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', closeMenu);
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth > 768) closeMenu();
  });
})();
