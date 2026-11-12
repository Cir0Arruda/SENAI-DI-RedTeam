// Navegação dos slides: setas/espaço/PageUp/PageDown, Home/End, swipe, botões e #hash.
(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const counter = document.getElementById('counter');
  const bar = document.getElementById('bar');
  const prev = document.getElementById('prev');
  const next = document.getElementById('next');
  const railBtns = [...document.querySelectorAll('.rail-btn[data-go]')];
  // data-go aceita índice ou #id do slide (assim a ordem dos slides pode mudar sem quebrar a barra)
  const idx = g => g.startsWith('#') ? slides.findIndex(s => s.id === g.slice(1)) : +g;
  railBtns.forEach(b => { b.dataset.idx = idx(b.dataset.go); });
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
    railBtns.forEach(b => { if (+b.dataset.idx <= cur) active = b; });
    railBtns.forEach(b => b.classList.toggle('on', b === active));
    const sec = document.getElementById('sec-title');
    if (sec) sec.textContent = `· ${slides[cur].dataset.title || 'SENAI'}`;
    document.querySelector('.stage')?.classList.toggle('is-cover', cur === 0);
    history.replaceState(null, '', `#${cur + 1}`);
    document.dispatchEvent(new CustomEvent('slidechange', { detail: { index: cur, slide: slides[cur] } }));
  }

  prev.addEventListener('click', () => go(cur - 1));
  next.addEventListener('click', () => go(cur + 1));
  railBtns.forEach(b => b.addEventListener('click', () => go(+b.dataset.idx)));

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

// Vídeo do impacto: reprodução automática em loop contínuo (mudo, exigência dos navegadores para autoplay).
(() => {
  const v = document.getElementById('video-impacto');
  if (!v) return;
  v.muted = true; v.defaultMuted = true; v.loop = true;
  const play = () => { if (v.paused) v.play().catch(() => {}); };
  play();
  v.addEventListener('canplay', play);
  v.addEventListener('pause', () => setTimeout(play, 200));
  document.addEventListener('slidechange', play);
  document.addEventListener('visibilitychange', play);
  ['pointerdown', 'keydown'].forEach(ev => document.addEventListener(ev, play, { once: true }));
})();
