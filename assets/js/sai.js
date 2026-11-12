// Projeto SAI: gráfico de força junto com o vídeo do PAD, barras de custo e gráfico de retorno (ROI).
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const RED = '#e5232f', INDIGO = '#5b5bd6';          // mesma paleta validada dos outros gráficos
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fmt = (n, d = 0) => n.toLocaleString('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
  const el = (tag, attrs = {}, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  const isOn = node => !!node && node.closest('.slide')?.classList.contains('on');
  const ease = k => 1 - Math.pow(1 - k, 3);

  /* ---------- PAD: força × tempo desenhada junto com o vídeo ---------- */
  // O vídeo (10 s) mostra 7 ms físicos: começa em 0,53 s e anda 0,933 ms por segundo (medido nos quadros do vídeo).
  function padChart() {
    const box = document.getElementById('pv-chart'), v = document.getElementById('video-impacto');
    const D = window.IMPACTO_1D;
    if (!box || !v || !D) return;
    const host = box.querySelector('.pv-svg'), read = document.getElementById('pv-read');
    const W = 340, H = 230, L = 34, R = 10, T = 20, B = 24, tMax = 7, fMax = 500;
    const x = t => L + (t / tMax) * (W - L - R), y = f => T + (1 - f / fMax) * (H - T - B);
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, 'aria-hidden': 'true' }, host);
    const grid = el('g', { class: 'grid' }, svg), axis = el('g', { class: 'axis' }, svg);
    for (let f = 0; f <= fMax; f += 100) {
      el('line', { x1: L, x2: W - R, y1: y(f), y2: y(f) }, grid);
      el('text', { x: L - 6, y: y(f) + 4, 'text-anchor': 'end' }, axis).textContent = f;
    }
    el('text', { x: L - 6, y: T - 10, 'text-anchor': 'end' }, axis).textContent = 'N';
    for (let t = 0; t <= tMax; t++) el('text', { x: x(t), y: H - 8, 'text-anchor': 'middle' }, axis).textContent = t === tMax ? `${t} ms` : t;
    const clip = el('clipPath', { id: 'pv-clip' }, el('defs', {}, svg));
    const cr = el('rect', { x: 0, y: 0, width: L, height: H }, clip);
    const path = idx => D.map((p, i) => `${i ? 'L' : 'M'}${x(p[0]).toFixed(1)},${y(p[idx]).toFixed(1)}`).join('');
    const g = el('g', { 'clip-path': 'url(#pv-clip)' }, svg);
    el('path', { d: path(1), fill: 'none', stroke: INDIGO, 'stroke-width': 2.2, 'stroke-linejoin': 'round' }, g);
    el('path', { d: path(2), fill: 'none', stroke: RED, 'stroke-width': 2.2, 'stroke-linejoin': 'round' }, g);
    const peak = idx => D.reduce((a, p) => (p[idx] > a[idx] ? p : a));
    const pS = peak(1), pC = peak(2);
    const lS = el('text', { x: x(pS[0]) + 8, y: y(pS[1]) + 4, class: 'lbl', opacity: 0 }, svg);
    lS.textContent = `${fmt(pS[1], 1)} N`;
    const lC = el('text', { x: x(pC[0]), y: y(pC[2]) - 10, class: 'lbl cut', 'text-anchor': 'middle', opacity: 0 }, svg);
    lC.textContent = `${fmt(pC[2], 1)} N · −${fmt((1 - pC[2] / pS[1]) * 100, 0)}%`;
    const head = el('line', { y1: T, y2: H - B, stroke: 'rgba(21,21,29,.35)', 'stroke-dasharray': '3 3' }, svg);
    const dS = el('circle', { r: 4, fill: INDIGO, stroke: '#fff', 'stroke-width': 2 }, svg);
    const dC = el('circle', { r: 4, fill: RED, stroke: '#fff', 'stroke-width': 2 }, svg);
    const at = t => D[Math.max(0, Math.min(D.length - 1, Math.round(t / 0.05)))];
    const phys = s => Math.max(0, Math.min(tMax, 0.9333 * (s - 0.528)));
    const draw = t => {
      const q = at(t), hx = x(t);
      cr.setAttribute('width', hx);
      head.setAttribute('x1', hx); head.setAttribute('x2', hx);
      dS.setAttribute('cx', hx); dS.setAttribute('cy', y(q[1]));
      dC.setAttribute('cx', hx); dC.setAttribute('cy', y(q[2]));
      lS.setAttribute('opacity', t >= pS[0] ? 1 : 0);
      lC.setAttribute('opacity', t >= pC[0] ? 1 : 0);
      read.innerHTML = `${fmt(t, 2)} ms · sem PAD <b>${fmt(q[1])} N</b> · com PAD <b>${fmt(q[2])} N</b>`;
    };
    draw(reduce ? tMax : 0);
    if (reduce) return;
    const loop = () => {
      if (isOn(box)) draw(phys(v.currentTime || 0));
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  /* ---------- Custos: barras crescem quando o slide abre ---------- */
  function costBars() {
    const s = document.getElementById('s-custo');
    if (!s) return;
    const bars = [...s.querySelectorAll('.sai-bar i, .cmp-bars i')];
    const grow = () => {
      bars.forEach(b => { b.style.transition = 'none'; b.style.width = '0'; });
      void s.offsetWidth;
      bars.forEach((b, i) => { b.style.transition = `width .9s cubic-bezier(.2,.7,.2,1) ${reduce ? 0 : i * 0.08}s`; b.style.width = 'var(--w)'; });
    };
    document.addEventListener('slidechange', ev => { if (ev.detail.slide === s) grow(); });
    if (isOn(s)) grow(); else bars.forEach(b => { b.style.width = 'var(--w)'; });
  }

  /* ---------- ROI: gasto acumulado com material em 24 meses, Tritan × SAI (valores de exemplo) ---------- */
  function roi() {
    const host = document.getElementById('chart-roi');
    if (!host) return;
    const MESES = 24, TRITAN = 250, SAI = 495.54, PADS = 21.96, HORAS = 730 * MESES;
    const trocasPad = Array.from({ length: MESES / 2 }, (_, i) => [2 * (i + 1), PADS]);
    // eventos [mês, valor em R$ de material]
    const tritan = Array.from({ length: MESES / 3 }, (_, i) => [3 * (i + 1), TRITAN]);
    const cen = {
      sim:  { sai: [[0, SAI], ...trocasPad], quebras: 0,
              txt: 'Pelas simulações a garra SAI não quebra; só os PADs são trocados a cada 2 meses.' },
      cons: { sai: [[0, SAI], ...trocasPad, [6, SAI], [18, SAI]], quebras: 2,
              txt: 'Conservador: a garra SAI quebra 1 vez por ano e é trocada inteira.' }
    };
    const acum = (ev, m) => ev.filter(e => e[0] <= m).reduce((a, e) => a + e[1], 0);
    const W = 640, H = 300, L = 62, R = 84, T = 14, B = 30, yMax = 2200;
    const x = m => L + (m / MESES) * (W - L - R), y = v => T + (1 - v / yMax) * (H - T - B);
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img' }, host);
    const grid = el('g', { class: 'grid' }, svg), axis = el('g', { class: 'axis' }, svg);
    for (let v = 0; v <= 2000; v += 500) {
      el('line', { x1: L, x2: W - R, y1: y(v), y2: y(v) }, grid);
      el('text', { x: L - 8, y: y(v) + 4, 'text-anchor': 'end' }, axis).textContent = `R$ ${fmt(v)}`;
    }
    for (let m = 0; m <= MESES; m += 6) el('text', { x: x(m), y: H - 8, 'text-anchor': 'middle' }, axis).textContent = m ? `${m} meses` : 'início';
    const step = ev => {
      let d = `M${x(0)},${y(0)}`, v = 0;
      for (let m = 0; m <= MESES; m++) {
        const nv = acum(ev, m);
        d += ` H${x(m).toFixed(1)}`;
        if (nv !== v) { d += ` V${y(nv).toFixed(1)}`; v = nv; }
      }
      return d;
    };
    const clip = el('clipPath', { id: 'roi-clip' }, el('defs', {}, svg));
    const cr = el('rect', { x: 0, y: 0, width: W, height: H }, clip);
    const g = el('g', { 'clip-path': 'url(#roi-clip)' }, svg);
    el('path', { d: step(tritan), fill: 'none', stroke: INDIGO, 'stroke-width': 2.2, 'stroke-linejoin': 'round' }, g);
    const pSai = el('path', { fill: 'none', stroke: RED, 'stroke-width': 2.2, 'stroke-linejoin': 'round' }, g);
    // marcadores das quebras da garra de Tritan
    tritan.forEach(([m]) => el('circle', { cx: x(m), cy: y(acum(tritan, m)), r: 3.5, fill: INDIGO, stroke: '#fff', 'stroke-width': 2 }, g));
    el('text', { x: x(3) + 6, y: y(acum(tritan, 3)) - 8, class: 'lbl' }, g).textContent = '1 quebra';
    el('text', { x: x(MESES) + 8, y: y(acum(tritan, MESES)) + 4, class: 'lbl' }, g).textContent = `R$ ${fmt(acum(tritan, MESES))}`;
    const endS = el('text', { x: x(MESES) + 8, class: 'lbl red' }, g);
    const pbDot = el('circle', { r: 5, fill: '#fff', stroke: RED, 'stroke-width': 2.5 }, g);
    const pbTxt = el('text', { class: 'lbl red', 'text-anchor': 'middle' }, g);
    // hover
    const cross = el('line', { y1: T, y2: H - B, stroke: 'rgba(21,21,29,.3)', 'stroke-dasharray': '3 3', opacity: 0 }, svg);
    const tip = document.createElement('div'); tip.className = 'tip'; host.appendChild(tip);
    let cur = 'sim';
    const hit = el('rect', { x: L, y: T, width: W - L - R, height: H - T - B, fill: 'transparent' }, svg);
    hit.addEventListener('pointermove', ev => {
      const r = svg.getBoundingClientRect(), hr = host.getBoundingClientRect();
      const m = Math.max(0, Math.min(MESES, Math.round(((ev.clientX - r.left) * (W / r.width) - L) / (W - L - R) * MESES)));
      const a = acum(tritan, m), b = acum(cen[cur].sai, m), d = a - b;
      cross.setAttribute('x1', x(m)); cross.setAttribute('x2', x(m)); cross.setAttribute('opacity', 1);
      tip.innerHTML = `<b>${m ? `${m}º mês` : 'início'}</b>
        <div class="r"><i style="background:${INDIGO}"></i>Tritan: R$ ${fmt(a, 2)}</div>
        <div class="r"><i style="background:${RED}"></i>SAI: R$ ${fmt(b, 2)}</div>
        <div>${d >= 0 ? `economia: R$ ${fmt(d, 2)}` : `ainda falta: R$ ${fmt(-d, 2)}`}</div>`;
      tip.classList.add('on');
      const hx = ev.clientX - hr.left, hy = ev.clientY - hr.top;
      tip.style.left = `${Math.min(Math.max(hx + 14, 8), host.clientWidth - tip.offsetWidth - 8)}px`;
      tip.style.top = `${Math.max(hy - tip.offsetHeight - 10, 8)}px`;
    });
    hit.addEventListener('pointerleave', () => { cross.setAttribute('opacity', 0); tip.classList.remove('on'); });

    const $ = id => document.getElementById(id);
    const setNum = (e, txt) => { e.textContent = txt; e.dataset.final = txt; };
    const count = (e, to, f) => {
      e.dataset.final = f(to);
      if (reduce) { e.textContent = f(to); return; }
      const t0 = performance.now();
      const st = now => { const k = Math.min(1, (now - t0) / 900); e.textContent = f(to * ease(k)); if (k < 1) requestAnimationFrame(st); };
      requestAnimationFrame(st);
    };
    const play = () => {
      if (reduce) { cr.setAttribute('width', W); return; }
      const t0 = performance.now();
      const st = now => { const k = Math.min(1, (now - t0) / 1600); cr.setAttribute('width', L + ease(k) * (W - L)); if (k < 1) requestAnimationFrame(st); };
      cr.setAttribute('width', L); requestAnimationFrame(st);
    };
    const show = (c, anim) => {
      cur = c;
      const C = cen[c], hoje = acum(tritan, MESES), sai = acum(C.sai, MESES);
      const eco = hoje - sai, pct = eco / sai * 100;
      let pb = null;
      // primeiro mês a partir do qual o SAI fica sempre abaixo da Tritan
      for (let m = MESES; m >= 1 && acum(C.sai, m) <= acum(tritan, m); m--) pb = m;
      pSai.setAttribute('d', step(C.sai));
      endS.setAttribute('y', y(sai) + 4);
      endS.textContent = `R$ ${fmt(sai)}`;
      if (pb !== null) {
        const py = y(acum(C.sai, pb));
        pbDot.setAttribute('cx', x(pb)); pbDot.setAttribute('cy', py); pbDot.setAttribute('opacity', 1);
        pbTxt.setAttribute('x', x(pb)); pbTxt.setAttribute('y', py + 22); pbTxt.textContent = 'se paga aqui';
      } else { pbDot.setAttribute('opacity', 0); pbTxt.textContent = ''; }
      $('roi-cen-txt').textContent = C.txt;
      $('roi-eco-s').textContent = `Tritan R$ ${fmt(hoje)} × SAI R$ ${fmt(sai, 2)}`;
      $('roi-x-s').textContent = `R$ ${fmt(eco, 2)} ÷ R$ ${fmt(sai, 2)} gastos com o SAI`;
      $('roi-h-s').textContent = `Tritan: R$ ${fmt(hoje / HORAS, 2)} por hora`;
      const fE = v => `R$ ${fmt(v, 2)}`, fX = v => `${fmt(v)}%`, fH = v => `R$ ${fmt(v, 2)}`, fP = v => `${fmt(v)} meses`;
      const els = [[$('roi-eco'), eco, fE], [$('roi-x'), pct, fX], [$('roi-h'), sai / HORAS, fH], [$('roi-pb'), pb || MESES, fP]];
      els.forEach(([e, v, f]) => (anim ? count(e, v, f) : setNum(e, f(v))));
      svg.setAttribute('aria-label', `Gasto acumulado com material em ${MESES} meses: garra de Tritan R$ ${fmt(hoje)}; garra SAI R$ ${fmt(sai, 2)}${pb ? `; o SAI se paga no ${pb}º mês` : ''}.`);
    };
    show('sim', false);
    document.querySelectorAll('#roi-cen button').forEach(b => b.addEventListener('click', () => {
      document.querySelectorAll('#roi-cen button').forEach(o => { o.classList.toggle('on', o === b); o.setAttribute('aria-selected', o === b); });
      show(b.dataset.c, true); play();
    }));
    const slide = host.closest('.slide');
    document.addEventListener('slidechange', ev => { if (ev.detail.slide === slide) play(); });
    if (isOn(host)) play();
  }

  padChart(); costBars(); roi();
})();
