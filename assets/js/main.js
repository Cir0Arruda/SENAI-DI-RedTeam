// Navegação dos slides: setas/espaço/PageUp/PageDown, Home/End, swipe, botões e #hash.
(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const counter = document.getElementById('counter');
  const bar = document.getElementById('bar');
  const prev = document.getElementById('prev');
  const next = document.getElementById('next');
  const railBtns = [...document.querySelectorAll('.rail-btn[data-go]')];
  const pad = n => String(n).padStart(2, '0');
  let cur = 0;

  function go(i) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    slides[cur].classList.remove('on');
    cur = i;
    slides[cur].classList.add('on');
    counter.textContent = `${pad(cur + 1)} / ${pad(slides.length)}`;
    bar.style.width = `${((cur + 1) / slides.length) * 100}%`;
    prev.disabled = cur === 0;
    next.disabled = cur === slides.length - 1;
    // Destaca a seção ativa na barra lateral (a última cujo índice é <= atual)
    let active = null;
    railBtns.forEach(b => { if (+b.dataset.go <= cur) active = b; });
    railBtns.forEach(b => b.classList.toggle('on', b === active));
    const sec = document.getElementById('sec-title');
    if (sec) sec.textContent = `· ${slides[cur].dataset.title || 'SENAI'}`;
    history.replaceState(null, '', `#${cur + 1}`);
    document.dispatchEvent(new CustomEvent('slidechange', { detail: { index: cur, slide: slides[cur] } }));
  }

  prev.addEventListener('click', () => go(cur - 1));
  next.addEventListener('click', () => go(cur + 1));
  railBtns.forEach(b => b.addEventListener('click', () => go(+b.dataset.go)));

  document.addEventListener('keydown', e => {
    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); go(cur + 1); }
    else if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); go(cur - 1); }
    else if (e.key === 'Home') go(0);
    else if (e.key === 'End') go(slides.length - 1);
  });

  let x0 = null;
  document.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) go(cur + (dx < 0 ? 1 : -1));
    x0 = null;
  });

  const fromHash = () => {
    const n = parseInt(location.hash.slice(1), 10);
    return Number.isFinite(n) ? n - 1 : 0;
  };
  window.addEventListener('hashchange', () => { if (fromHash() !== cur) go(fromHash()); });
  go(fromHash());
})();

// Vídeo do impacto: toca só com o slide visível, volta ao início ao entrar.
(() => {
  const v = document.getElementById('video-impacto');
  if (!v) return;
  const host = v.closest('.slide');
  document.addEventListener('slidechange', e => {
    if (e.detail.slide === host) { v.currentTime = 0; v.play().catch(() => {}); }
    else v.pause();
  });
  if (host.classList.contains('on')) v.play().catch(() => {});
})();
