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
    if (e.target.closest && e.target.closest('input, select, textarea')) return;   // setas movem o controle, não o slide
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

// Ajuste à tela: no computador, se o conteúdo de um slide não cabe na altura, reduz proporcionalmente (zoom) até caber.
// No celular (≤ 900 px de largura) mantém a rolagem normal.
(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const MIN = 0.6;
  function fit(s) {
    const kids = [...s.children];
    const set = z => kids.forEach(k => { k.style.zoom = z === 1 ? '' : z.toFixed(3); });
    const fits = () => s.scrollHeight - s.clientHeight <= 1;
    set(1);
    if (innerWidth <= 900 || fits()) return;
    // busca binária do maior zoom que cabe (o texto reflui ao reduzir, então a proporção simples encolhe demais)
    let lo = MIN, hi = 1;
    for (let n = 0; n < 8; n++) {
      const mid = (lo + hi) / 2;
      set(mid);
      if (fits()) lo = mid; else hi = mid;
    }
    set(lo);
  }
  // Escala de leitura: no computador, todo texto dos slides abaixo de 16 px cresce (+20% até 13 px, +15% até 16 px).
  // Lê os tamanhos originais uma vez e grava em px, então não acumula; no celular volta ao tamanho do CSS.
  const txt = slides.flatMap(s => [...s.querySelectorAll('*')]).filter(e => !e.closest('svg'));
  let escala = null;
  function legivel() {
    const on = innerWidth > 900;
    if (on === escala) return;
    escala = on;
    if (!on) { txt.forEach(e => { if (e.dataset.fs0) e.style.fontSize = ''; }); return; }
    const novo = txt.map(e => {
      const f = parseFloat(getComputedStyle(e).fontSize);
      return f < 13 ? f * 1.2 : f < 16 ? f * 1.15 : 0;
    });
    txt.forEach((e, i) => { if (novo[i]) { e.dataset.fs0 = 1; e.style.fontSize = `${novo[i].toFixed(1)}px`; } });
  }
  const fitAll = () => { legivel(); slides.forEach(fit); };
  let t = null;
  const later = () => { clearTimeout(t); t = setTimeout(fitAll, 120); };
  fitAll();
  addEventListener('load', fitAll);
  addEventListener('resize', later);
  document.fonts?.ready.then(fitAll);
  // imagens que carregam depois e abas que trocam o conteúdo
  document.addEventListener('load', e => { if (e.target.tagName === 'IMG' || e.target.tagName === 'VIDEO') later(); }, true);
  document.addEventListener('loadedmetadata', later, true);
  document.addEventListener('click', e => { const s = e.target.closest('.slide'); if (s && e.target.closest('button')) setTimeout(() => fit(s), 80); });
  // o slide ativo entra com animação (translateY), que infla a medida: mede de novo depois que ela termina
  document.addEventListener('slidechange', e => setTimeout(() => fit(e.detail.slide), 950));
  setTimeout(fitAll, 1000);
})();
