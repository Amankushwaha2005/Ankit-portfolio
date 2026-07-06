document.addEventListener('DOMContentLoaded', () => {
  const filters = document.querySelectorAll('.gallery-filter');
  const sections = document.querySelectorAll('.gallery-section');
  const items = document.querySelectorAll('.gallery-item');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxTitle = document.getElementById('lightboxTitle');
  const lightboxDesc = document.getElementById('lightboxDesc');
  const closeBtn = document.querySelector('.lightbox-close');
  const prevBtn = document.querySelector('.lightbox-prev');
  const nextBtn = document.querySelector('.lightbox-next');

  let visibleItems = [];
  let currentIndex = 0;

  filters.forEach(btn => {
    btn.addEventListener('click', () => {
      filters.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;

      sections.forEach(section => {
        if (filter === 'all') {
          section.style.display = 'block';
        } else {
          section.style.display = section.dataset.category === filter ? 'block' : 'none';
        }
      });
    });
  });

  function getVisibleItems() {
    const activeFilter = document.querySelector('.gallery-filter.active')?.dataset.filter || 'all';
    return Array.from(items).filter(item => {
      if (activeFilter === 'all') return true;
      return item.dataset.category === activeFilter;
    });
  }

  function openLightbox(index) {
    visibleItems = getVisibleItems();
    currentIndex = index;
    showSlide();
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function showSlide() {
    const item = visibleItems[currentIndex];
    if (!item) return;
    const img = item.querySelector('img');
    const title = item.querySelector('.gallery-overlay h3');
    const desc = item.querySelector('.gallery-overlay p');
    lightboxImg.src = img.src;
    lightboxImg.alt = img.alt;
    lightboxTitle.textContent = title?.textContent || '';
    lightboxDesc.textContent = desc?.textContent || '';
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
  }

  items.forEach((item, i) => {
    item.addEventListener('click', () => {
      visibleItems = getVisibleItems();
      currentIndex = visibleItems.indexOf(item);
      openLightbox(currentIndex);
    });
  });

  closeBtn?.addEventListener('click', closeLightbox);
  lightbox?.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });

  prevBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    visibleItems = getVisibleItems();
    currentIndex = (currentIndex - 1 + visibleItems.length) % visibleItems.length;
    showSlide();
  });

  nextBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    visibleItems = getVisibleItems();
    currentIndex = (currentIndex + 1) % visibleItems.length;
    showSlide();
  });

  document.addEventListener('keydown', (e) => {
    if (!lightbox?.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') prevBtn?.click();
    if (e.key === 'ArrowRight') nextBtn?.click();
  });
});
