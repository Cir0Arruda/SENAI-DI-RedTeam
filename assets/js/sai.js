// Projeto SAI: gráfico de força junto com o vídeo do PAD, matriz de prioridade e Materiais. Custos e Retorno ficam em custo.js.
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
    const PICO_SEM = 450.914, PICO_COM = 168.523;   // parametros_resultados_R03.json
    if (!box || !v || !D) return;
    const host = box.querySelector('.pv-svg'), read = document.getElementById('pv-read');
    const W = 300, H = 205, L = 40, R = 22, T = 30, B = 26, tMax = 7, fMax = 500;
    const x = t => L + (t / tMax) * (W - L - R), y = f => T + (1 - f / fMax) * (H - T - B);
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, 'aria-hidden': 'true' }, host);
    const grid = el('g', { class: 'grid' }, svg), axis = el('g', { class: 'axis' }, svg);
    for (let f = 0; f <= fMax; f += 100) {
      el('line', { x1: L, x2: W - R, y1: y(f), y2: y(f) }, grid);
      el('text', { x: L - 6, y: y(f) + 4, 'text-anchor': 'end' }, axis).textContent = f;
    }
    el('text', { x: L - 6, y: T - 14, 'text-anchor': 'end' }, axis).textContent = 'N';
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
    lS.textContent = `${fmt(PICO_SEM, 1)} N`;   // pico exato do R03; a série amostrada a cada 0,05 ms dá 450,7
    const lC = el('text', { x: x(pC[0]) + 2, y: y(pC[2]) - 12, class: 'lbl cut', 'text-anchor': 'start', opacity: 0 }, svg);
    lC.textContent = `${fmt(PICO_COM, 1)} N · −${fmt((1 - PICO_COM / PICO_SEM) * 100, 0)}%`;
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

  /* ---------- Payback: simulação com controles (só material, 24 meses) ---------- */
  function payback() {
    const host = document.getElementById('chart-pb');
    if (!host) return;
    const $ = id => document.getElementById(id);
    const MESES = 24, TRITAN = 250, SAI = 495.54, PADS = 21.96, CAIXAS = 280;
    const triIn = $('pb-tri'), padIn = $('pb-pad'), seg = $('pb-sai');
    const every = (n, v) => (n ? Array.from({ length: Math.floor(MESES / n) }, (_, i) => [n * (i + 1), v]) : []);
    const acum = (ev, m) => ev.filter(e => e[0] <= m).reduce((a, e) => a + e[1], 0);
    const W = 640, H = 300, L = 62, R = 84, T = 14, B = 30;
    let yMax = 2200;
    const x = m => L + (m / MESES) * (W - L - R), y = v => T + (1 - v / yMax) * (H - T - B);
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img' }, host);
    const grid = el('g', { class: 'grid' }, svg), axis = el('g', { class: 'axis' }, svg);
    for (let m = 0; m <= MESES; m += 6) el('text', { x: x(m), y: H - 8, 'text-anchor': 'middle' }, axis).textContent = m ? `${m} meses` : 'início';
    const yAxis = el('g', {}, axis);
    const step = ev => {
      let d = `M${x(0)},${y(0)}`, v = 0;
      for (let m = 0; m <= MESES; m++) {
        const nv = acum(ev, m);
        d += ` H${x(m).toFixed(1)}`;
        if (nv !== v) { d += ` V${y(nv).toFixed(1)}`; v = nv; }
      }
      return d;
    };
    const clip = el('clipPath', { id: 'pb-clip' }, el('defs', {}, svg));
    const cr = el('rect', { x: 0, y: 0, width: W, height: H }, clip);
    const g = el('g', { 'clip-path': 'url(#pb-clip)' }, svg);
    const pT = el('path', { fill: 'none', stroke: INDIGO, 'stroke-width': 2.2, 'stroke-linejoin': 'round' }, g);
    const pS = el('path', { fill: 'none', stroke: RED, 'stroke-width': 2.2, 'stroke-linejoin': 'round' }, g);
    const endT = el('text', { x: x(MESES) + 8, class: 'lbl' }, g), endS = el('text', { x: x(MESES) + 8, class: 'lbl red' }, g);
    const dot = el('circle', { r: 5, fill: '#fff', stroke: RED, 'stroke-width': 2.5 }, g);
    const dotT = el('text', { class: 'lbl red', 'text-anchor': 'middle' }, g);
    // hover
    const cross = el('line', { y1: T, y2: H - B, stroke: 'rgba(21,21,29,.3)', 'stroke-dasharray': '3 3', opacity: 0 }, svg);
    const tip = document.createElement('div'); tip.className = 'tip'; host.appendChild(tip);
    let evT = [], evS = [];
    const hit = el('rect', { x: L, y: T, width: W - L - R, height: H - T - B, fill: 'transparent' }, svg);
    hit.addEventListener('pointermove', ev => {
      const r = svg.getBoundingClientRect(), hr = host.getBoundingClientRect();
      const m = Math.max(0, Math.min(MESES, Math.round(((ev.clientX - r.left) * (W / r.width) - L) / (W - L - R) * MESES)));
      const a = acum(evT, m), b = acum(evS, m), d = a - b;
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

    const play = () => {
      if (reduce) { cr.setAttribute('width', W); return; }
      const t0 = performance.now();
      const st = now => { const k = Math.max(0, Math.min(1, (now - t0) / 1200)); cr.setAttribute('width', L + ease(k) * (W - L)); if (k < 1) requestAnimationFrame(st); };
      cr.setAttribute('width', L); requestAnimationFrame(st);
    };
    const update = anim => {
      const nT = +triIn.value, nP = +padIn.value, nS = +seg.querySelector('button.on').dataset.n;
      $('pb-tri-o').textContent = nT === 1 ? 'mês' : `${nT} meses`;
      $('pb-pad-o').textContent = nP === 1 ? 'mês' : `${nP} meses`;
      evT = every(nT, TRITAN);
      evS = [[0, SAI], ...every(nP, PADS), ...every(nS, SAI)];
      const hoje = acum(evT, MESES), sai = acum(evS, MESES);
      // eixo y arredondado para cima em passos de R$ 500
      yMax = Math.max(1000, Math.ceil(Math.max(hoje, sai) * 1.1 / 500) * 500);
      grid.replaceChildren(); yAxis.replaceChildren();
      const stepV = yMax > 4000 ? 1000 : 500;
      for (let v = 0; v <= yMax; v += stepV) {
        el('line', { x1: L, x2: W - R, y1: y(v), y2: y(v) }, grid);
        el('text', { x: L - 8, y: y(v) + 4, 'text-anchor': 'end' }, yAxis).textContent = `R$ ${fmt(v)}`;
      }
      pT.setAttribute('d', step(evT)); pS.setAttribute('d', step(evS));
      const yT = y(hoje), yS = y(sai), sep = Math.abs(yT - yS) < 14 ? 8 : 0;
      endT.setAttribute('y', yT + 4 - (yT <= yS ? sep : -sep)); endT.textContent = `R$ ${fmt(hoje)}`;
      endS.setAttribute('y', yS + 4 + (yT <= yS ? sep : -sep)); endS.textContent = `R$ ${fmt(sai, 2)}`;
      let pb = null;
      for (let m = MESES; m >= 1 && acum(evS, m) <= acum(evT, m); m--) pb = m;
      if (pb !== null) {
        dot.setAttribute('cx', x(pb)); dot.setAttribute('cy', y(acum(evS, pb))); dot.setAttribute('opacity', 1);
        dotT.setAttribute('x', x(pb)); dotT.setAttribute('y', y(acum(evS, pb)) + 22); dotT.textContent = 'se paga aqui';
      } else { dot.setAttribute('opacity', 0); dotT.textContent = ''; }
      const qT = evT.length, qS = every(nS, 1).length, evit = Math.max(0, qT - qS);
      const mes = $('pb-mes'), cx = $('pb-cx');
      const txtMes = pb ? `${pb} ${pb === 1 ? 'mês' : 'meses'}` : 'mais de 24 meses';
      mes.textContent = txtMes; mes.dataset.final = txtMes;
      $('pb-mes-s').textContent = pb ? 'só com material' : 'só com material; as caixas garantidas ainda contam';
      const txtCx = fmt(evit * CAIXAS);
      cx.textContent = txtCx; cx.dataset.final = txtCx;
      $('pb-cx-s').textContent = `${evit} ${evit === 1 ? 'quebra evitada' : 'quebras evitadas'} × 280 caixas`;
      $('pb-sub').textContent = `Tritan R$ ${fmt(hoje)} × SAI R$ ${fmt(sai, 2)} · ${hoje >= sai ? `economia de R$ ${fmt(hoje - sai, 2)}` : `o SAI gasta R$ ${fmt(sai - hoje, 2)} a mais em material`}`;
      svg.setAttribute('aria-label', `Gasto acumulado com material em 24 meses: Tritan R$ ${fmt(hoje)}, SAI R$ ${fmt(sai, 2)}. ${pb ? `O SAI se paga no ${pb}º mês.` : 'O SAI não se paga em 24 meses só com material.'}`);
      if (anim) play();
    };
    triIn.addEventListener('input', () => update(false));
    padIn.addEventListener('input', () => update(false));
    seg.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
      seg.querySelectorAll('button').forEach(o => { o.classList.toggle('on', o === b); o.setAttribute('aria-selected', o === b); });
      update(true);
    }));
    $('pb-reset').addEventListener('click', () => {
      triIn.value = 3; padIn.value = 2;
      seg.querySelectorAll('button').forEach((o, i) => { o.classList.toggle('on', i === 0); o.setAttribute('aria-selected', i === 0); });
      update(true);
    });
    update(false);
    const slide = host.closest('.slide');
    document.addEventListener('slidechange', ev => { if (ev.detail.slide === slide) play(); });
    if (isOn(host)) play();
  }

  /* ---------- Matriz de prioridade: valor agregado × complexidade ---------- */
  function matriz() {
    const host = document.getElementById('chart-matriz');
    if (!host) return;
    const W = 560, H = 380, L = 44, R = 16, T = 14, B = 44, MAX = 10.6;
    const x = v => L + (v / MAX) * (W - L - R), y = v => T + (1 - v / MAX) * (H - T - B);
    const ideias = [
      { n: 'Ventosas', c: 3, v: 2, cor: '#9a9ae8', lx: 0, ly: -16, a: 'middle' },
      { n: 'Tratativa dos dados', c: 5, v: 2, cor: '#9a9ae8', lx: 0, ly: 26, a: 'middle' },
      { n: 'Híbrido', c: 10, v: 7, cor: INDIGO, lx: -14, ly: 5, a: 'end' },
      { n: 'Impressão de metais', c: 10, v: 8, cor: INDIGO, lx: -14, ly: 5, a: 'end' },
      { n: 'Projeto SAI', c: 6, v: 9, cor: RED, lx: 0, ly: -20, a: 'middle', win: true },
    ];
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', class: 'mx-svg',
      'aria-label': 'Matriz de prioridade: Projeto SAI valor 9 e complexidade 6 (escolhido); impressão de metais valor 8 e complexidade 10; híbrido valor 7 e complexidade 10; tratativa dos dados valor 2 e complexidade 5; ventosas valor 2 e complexidade 3.' }, host);
    // quadrantes
    const q = el('g', { class: 'mx-q' }, svg);
    el('rect', { x: x(0), y: y(MAX), width: x(MAX) - x(0), height: y(5) - y(MAX), class: 'mx-best' }, q);   // metade de cima: alto valor
    [['Ganhos rápidos', x(.25), y(MAX) + 16, 'start'], ['Estratégicos', x(MAX) - 4, y(MAX) + 16, 'end'],
     ['Pouco impacto', x(.25), y(0) - 8, 'start'], ['Evitar', x(MAX) - 4, y(0) - 8, 'end']]
      .forEach(([s, qx, qy, an]) => { el('text', { x: qx, y: qy, 'text-anchor': an, class: 'mx-qt' }, q).textContent = s; });
    const grid = el('g', { class: 'grid' }, svg);
    for (let v = 0; v <= 10; v += 2) {
      el('line', { x1: x(v), x2: x(v), y1: y(0), y2: y(MAX) }, grid);
      el('line', { x1: x(0), x2: x(MAX), y1: y(v), y2: y(v) }, grid);
    }
    el('line', { x1: x(5), x2: x(5), y1: y(0), y2: y(MAX), class: 'mx-mid' }, svg);
    el('line', { x1: x(0), x2: x(MAX), y1: y(5), y2: y(5), class: 'mx-mid' }, svg);
    const axis = el('g', { class: 'axis' }, svg);
    for (let v = 0; v <= 10; v += 2) {
      el('text', { x: x(v), y: y(0) + 16, 'text-anchor': 'middle' }, axis).textContent = v;
      el('text', { x: L - 8, y: y(v) + 4, 'text-anchor': 'end' }, axis).textContent = v;
    }
    el('text', { x: x(0), y: H - 4, class: 'mx-ax' }, axis).textContent = '← menos complexo';
    el('text', { x: x(MAX), y: H - 4, 'text-anchor': 'end', class: 'mx-ax' }, axis).textContent = 'complexidade →';
    el('text', { x: 0, y: 0, transform: `translate(12 ${y(0)}) rotate(-90)`, class: 'mx-ax' }, axis).textContent = 'valor agregado →';
    // pontos
    const tip = document.createElement('div'); tip.className = 'tip'; host.appendChild(tip);
    const pts = ideias.map((d, i) => {
      const g = el('g', { class: `mx-pt${d.win ? ' win' : ''}`, style: `--d:${d.win ? 900 : i * 140}ms`, tabindex: 0,
        'aria-label': `${d.n}: valor ${d.v}, complexidade ${d.c}` }, svg);
      if (d.win) el('circle', { cx: x(d.c), cy: y(d.v), r: 15, class: 'mx-ring', fill: 'none', stroke: RED }, g);
      el('circle', { cx: x(d.c), cy: y(d.v), r: 18, fill: 'transparent' }, g);   // área de hover maior que a marca
      el('circle', { cx: x(d.c), cy: y(d.v), r: d.win ? 10 : 7, fill: d.cor, stroke: '#fff', 'stroke-width': 2, class: 'mx-dot' }, g);
      const tx = el('text', { x: x(d.c) + d.lx, y: y(d.v) + d.ly, 'text-anchor': d.a, class: `mx-lbl${d.win ? ' win' : ''}` }, g);
      tx.textContent = d.win ? 'Projeto SAI · escolhido' : d.n;
      const show = () => {
        tip.innerHTML = `<b>${d.n}${d.win ? ' (escolhido)' : ''}</b><div>valor agregado: ${d.v}</div><div>complexidade: ${d.c}</div>`;
        tip.classList.add('on');
        const r = svg.getBoundingClientRect(), hr = host.getBoundingClientRect(), k = r.width / W;
        const px = r.left - hr.left + x(d.c) * k, py = r.top - hr.top + y(d.v) * k;
        tip.style.left = `${Math.min(Math.max(px - tip.offsetWidth / 2, 4), host.clientWidth - tip.offsetWidth - 4)}px`;
        tip.style.top = `${Math.max(py - tip.offsetHeight - 16, 4)}px`;
      };
      const hide = () => tip.classList.remove('on');
      g.addEventListener('pointerenter', show); g.addEventListener('pointerleave', hide);
      g.addEventListener('focus', show); g.addEventListener('blur', hide);
      return g;
    });
    const play = () => {
      host.classList.remove('play');
      void host.offsetWidth;
      host.classList.add('play');
    };
    const slide = host.closest('.slide');
    document.addEventListener('slidechange', ev => { if (ev.detail.slide === slide) play(); });
    if (reduce || isOn(host)) host.classList.add('play');
  }

  /* ---------- Materiais: vídeo da garra com peso → vista 3D por dentro, troca automática ---------- */
  function matPanes() {
    const seg = document.getElementById('mat-tabs');
    if (!seg) return;
    const slide = seg.closest('.slide'), v = document.getElementById('video-mat'), cut = document.getElementById('mat-cut');
    let timer = 0, raf = 0, autoCut = true;
    const clear = () => { clearTimeout(timer); cancelAnimationFrame(raf); };
    const setCut = val => { if (!cut) return; cut.value = Math.round(val); cut.dispatchEvent(new Event('input')); };
    // corte automático: desce até 40% da altura, segura e volta (para mostrar o miolo)
    const animCut = () => {
      if (!cut || reduce || !autoCut) return;
      const t0 = performance.now(), D = 11000;
      const st = now => {
        const k = Math.max(0, Math.min(1, (now - t0) / D));
        const f = k < .35 ? ease(k / .35) : k < .75 ? 1 : 1 - ease((k - .75) / .25);
        setCut(100 - 60 * f);
        if (k < 1 && autoCut) raf = requestAnimationFrame(st);
      };
      raf = requestAnimationFrame(st);
    };
    const show = (id, auto = true) => {
      clear();
      seg.querySelectorAll('button').forEach(b => {
        const on = b.dataset.pane === id;
        b.classList.toggle('on', on); b.setAttribute('aria-selected', on);
        document.getElementById(b.dataset.pane).classList.toggle('on', on);
      });
      if (id === 'mat-video') {
        setCut(100);
        v.currentTime = 0; v.play().catch(() => {});
      } else {
        v.pause();
        window.dispatchEvent(new Event('resize'));
        animCut();
        if (auto) timer = setTimeout(() => { if (isOn(seg)) show('mat-video'); }, 12000);
      }
    };
    v.addEventListener('ended', () => { timer = setTimeout(() => { if (isOn(seg)) show('mat-3d'); }, 2500); });
    seg.querySelectorAll('button').forEach(b => b.addEventListener('click', () => show(b.dataset.pane)));
    if (cut) cut.addEventListener('pointerdown', () => { autoCut = false; cancelAnimationFrame(raf); });
    document.addEventListener('slidechange', ev => {
      if (ev.detail.slide === slide) { autoCut = true; show('mat-video'); }
      else { clear(); v.pause(); }
    });
    if (isOn(seg)) show('mat-video');
  }

  padChart(); payback(); matriz(); matPanes();
})();
