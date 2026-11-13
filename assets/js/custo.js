// Custos e Retorno: Tritan × garra SAI (dados em custo-dados.js).
// Custos: custo direto acumulado em R$, por caixas produzidas. Retorno: caixas perdidas com a linha parada, por mês.
// Linhas, não escadas: a quebra do Tritan é aleatória (em média a cada 3 meses), então o gráfico mostra o valor esperado.
(() => {
  const C = window.CUSTO;
  if (!C) return;
  const NS = 'http://www.w3.org/2000/svg';
  const RED = '#e5232f', INDIGO = '#5b5bd6';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fmt = (n, d = 0) => n.toLocaleString('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
  const rs = v => (Math.abs(v) >= 1e6 ? `R$ ${fmt(v / 1e6, 2)} mi` : Math.abs(v) >= 1e4 ? `R$ ${fmt(v / 1e3, 0)} mil` : `R$ ${fmt(v, 0)}`);
  const cxTxt = v => (v >= 1e6 ? `${fmt(v / 1e6, 1)} mi` : v >= 1e3 ? `${fmt(v / 1e3, 0)} mil` : fmt(v));
  const ease = k => 1 - Math.pow(1 - k, 3);
  const el = (tag, attrs = {}, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  const isOn = node => !!node && node.closest('.slide')?.classList.contains('on');
  const nice = v => { const p = 10 ** Math.floor(Math.log10(v)), m = v / p; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * p; };
  const hTxt = m => (m < 60 ? `${fmt(m)} min` : m % 60 ? `${fmt(m / 60, 1)} h` : `${m / 60} h`);
  const mesTxt = m => (m === 0 ? 'início' : m === 12 ? '1 ano' : m === 24 ? '2 anos' : `${m} meses`);

  // Gráfico de linhas. eixo 'caixas': x = caixas produzidas (mês embaixo). eixo 'mes': x = meses (mais simples de ler).
  // simples: rótulos com o nome no fim das linhas, área do ganho pintada e notas curtas no próprio gráfico.
  function chart(host, { mesMax, campo, un = 'rs', eixo = 'caixas', simples = false, encLbl = 'se paga aqui', alt = 306 }) {
    const yf = un === 'rs' ? rs : v => fmt(v);
    const W = 560, H = alt, L = simples ? 56 : 70, R = simples ? 104 : 76, T = simples ? 26 : 16, B = simples ? 44 : 60;
    const CXM = C.producao.caixas_por_mes;
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img' }, host);
    const grid = el('g', { class: 'grid' }, svg), axis = el('g', { class: 'axis' }, svg), yAx = el('g', {}, axis);
    const xMax = eixo === 'mes' ? mesMax : mesMax * CXM;
    const xv = p => (eixo === 'mes' ? p.mes : p.caixas);
    const x = v => L + (v / xMax) * (W - L - R);
    let yMax = 1;
    const y = v => T + (1 - v / yMax) * (H - T - B);
    if (eixo === 'mes') {
      for (let m = 0; m <= mesMax; m += 3) {
        const big = m % 6 === 0;
        el('line', { x1: x(m), x2: x(m), y1: H - B, y2: H - B + (big ? 5 : 3), stroke: 'rgba(21,21,29,.25)' }, axis);
        if (big) el('text', { x: m ? x(m) : x(0) - 2, y: H - B + 19, 'text-anchor': m ? 'middle' : 'start' }, axis).textContent = mesTxt(m);
      }
      el('text', { x: (L + W - R) / 2, y: H - 4, class: 'ax-t', 'text-anchor': 'middle' }, axis).textContent = 'tempo com a linha rodando 24 h por dia';
    } else {
      for (let m = 0; m <= mesMax; m += 6) {
        const cx = m * CXM;
        el('line', { x1: x(cx), x2: x(cx), y1: H - B, y2: H - B + 4, stroke: 'rgba(21,21,29,.25)' }, axis);
        el('text', { x: x(cx), y: H - B + 17, 'text-anchor': 'middle' }, axis).textContent = m ? cxTxt(cx) : '0';
        el('text', { x: x(cx), y: H - B + 31, 'text-anchor': 'middle', class: 'sub-tick' }, axis).textContent = m ? `${m} meses` : 'início';
      }
      el('text', { x: (L + W - R) / 2, y: H - 4, class: 'ax-t', 'text-anchor': 'middle' }, axis).textContent = 'caixas produzidas (e o mês de referência)';
    }
    if (simples) el('text', { x: L - 8, y: T - 12, class: 'ax-t', 'text-anchor': 'start' }, axis).textContent = un === 'rs' ? 'R$ gastos' : 'caixas perdidas (soma)';
    const clip = el('clipPath', { id: `${host.id}-clip` }, el('defs', {}, svg));
    const cr = el('rect', { x: 0, y: 0, width: W, height: H }, clip);
    const g = el('g', { 'clip-path': `url(#${host.id}-clip)` }, svg);
    const area = el('path', { fill: 'rgba(229,35,47,.10)', stroke: 'none' }, g);
    const areaT = el('text', { class: 'lbl', 'text-anchor': 'middle', 'font-weight': 600 }, g);
    const pT = el('path', { fill: 'none', stroke: INDIGO, 'stroke-width': 2.4, 'stroke-linejoin': 'round' }, g);
    const pS = el('path', { fill: 'none', stroke: RED, 'stroke-width': 2.4, 'stroke-linejoin': 'round' }, g);
    const dots = el('g', {}, g);
    const notas = el('g', {}, g);
    const endT = el('text', { class: 'lbl' }, g), endS = el('text', { class: 'lbl' }, g);
    const enc = el('g', {}, g);
    const encLn = el('line', { stroke: RED, 'stroke-width': 1.2, 'stroke-dasharray': '2 3' }, enc);
    const encDot = el('circle', { r: 6, fill: '#fff', stroke: RED, 'stroke-width': 2.5 }, enc);
    const encT1 = el('text', { class: 'lbl', 'text-anchor': 'start', 'font-weight': 600 }, enc), encT2 = el('text', { class: 'lbl sm', 'text-anchor': 'start' }, enc);
    // hover: ponto de cada trimestre
    const cross = el('line', { y1: T, y2: H - B, stroke: 'rgba(21,21,29,.3)', 'stroke-dasharray': '3 3', opacity: 0 }, svg);
    const tip = document.createElement('div'); tip.className = 'tip'; host.appendChild(tip);
    const hit = el('rect', { x: L, y: T, width: W - L - R, height: H - T - B, fill: 'transparent' }, svg);
    let S = [];
    hit.addEventListener('pointermove', ev => {
      const r = svg.getBoundingClientRect(), hr = host.getBoundingClientRect();
      const fx = ((ev.clientX - r.left) * (W / r.width) - L) / (W - L - R) * xMax;
      const p = S.reduce((a, q) => (Math.abs(xv(q) - fx) < Math.abs(xv(a) - fx) ? q : a));
      const d = p.tritan - p.sai;
      cross.setAttribute('x1', x(xv(p))); cross.setAttribute('x2', x(xv(p))); cross.setAttribute('opacity', 1);
      const linha = un === 'rs'
        ? [`Tritan: R$ ${fmt(p.tritan, 0)}`, `SAI: R$ ${fmt(p.sai, 0)}`, d >= 0 ? `o SAI economiza R$ ${fmt(d, 0)}` : `o SAI ainda custa R$ ${fmt(-d, 0)} a mais`]
        : [`Tritan: ${fmt(p.tritan)} caixas perdidas`, `SAI: ${fmt(p.sai)} caixas perdidas`, d > 0 ? `o SAI salvou ${fmt(d)} caixas` : d === 0 ? 'empate' : `o SAI ainda perdeu ${fmt(-d)} caixas a mais`];
      tip.innerHTML = `<b>${p.mes ? `${mesTxt(p.mes)} · ${cxTxt(p.caixas)} caixas produzidas` : 'início'}</b>
        <div class="r"><i style="background:${INDIGO}"></i>${linha[0]}</div>
        <div class="r"><i style="background:${RED}"></i>${linha[1]}</div>
        <div>${linha[2]}</div>`;
      tip.classList.add('on');
      const hx = ev.clientX - hr.left, hy = ev.clientY - hr.top;
      tip.style.left = `${Math.min(Math.max(hx + 14, 8), host.clientWidth - tip.offsetWidth - 8)}px`;
      tip.style.top = `${Math.max(hy - tip.offsetHeight - 10, 8)}px`;
    });
    hit.addEventListener('pointerleave', () => { cross.setAttribute('opacity', 0); tip.classList.remove('on'); });

    const play = () => {
      if (reduce) { cr.setAttribute('width', W); return; }
      const t0 = performance.now();
      const st = now => { const k = Math.max(0, Math.min(1, (now - t0) / 1600)); cr.setAttribute('width', L + ease(k) * (W - L)); if (k < 1) requestAnimationFrame(st); };
      cr.setAttribute('width', L); requestAnimationFrame(st);
    };
    const nota = (px, py, txt, anchor = 'start') => { el('text', { x: px, y: py, class: 'lbl sm', 'text-anchor': anchor }, notas).textContent = txt; };
    const show = cen => {
      const c = C.cenarios[cen];
      S = c[`serie_${campo}`].filter(p => p.mes <= mesMax);
      const top = Math.max(...S.map(p => Math.max(p.tritan, p.sai)));
      const step = nice(top / 4);
      yMax = Math.ceil(top * 1.06 / step) * step;
      grid.replaceChildren(); yAx.replaceChildren(); notas.replaceChildren();
      for (let v = 0; v <= yMax + 1e-6; v += step) {
        el('line', { x1: L, x2: W - R, y1: y(v), y2: y(v) }, grid);
        el('text', { x: L - 8, y: y(v) + 4, 'text-anchor': 'end' }, yAx).textContent = yf(v);
      }
      const pt = (p, k) => `${x(xv(p)).toFixed(1)},${y(p[k]).toFixed(1)}`;
      const path = k => S.map((p, i) => `${i ? 'L' : 'M'}${pt(p, k)}`).join('');
      pT.setAttribute('d', path('tritan')); pS.setAttribute('d', path('sai'));
      dots.replaceChildren();
      S.forEach(p => {
        el('circle', { cx: x(xv(p)), cy: y(p.tritan), r: 3.6, fill: INDIGO, stroke: '#fff', 'stroke-width': 1.6 }, dots);
        el('circle', { cx: x(xv(p)), cy: y(p.sai), r: 3.6, fill: RED, stroke: '#fff', 'stroke-width': 1.6 }, dots);
      });
      const e = c[`encontro_${campo}`];
      const last = S[S.length - 1], yT = y(last.tritan), yS = y(last.sai), sep = Math.abs(yT - yS) < 30 ? 15 : 0;
      const nomeT = simples ? `Tritan: ${yf(last.tritan)}` : yf(last.tritan), nomeS = simples ? `SAI: ${yf(last.sai)}` : yf(last.sai);
      endT.setAttribute('x', x(xv(last)) + 8); endT.setAttribute('y', yT + 4 - (yT <= yS ? sep : -sep)); endT.textContent = nomeT;
      endS.setAttribute('x', x(xv(last)) + 8); endS.setAttribute('y', yS + 4 + (yT <= yS ? sep : -sep)); endS.textContent = nomeS;
      if (simples) { endT.setAttribute('font-weight', 600); endS.setAttribute('font-weight', 600); }
      // área do ganho: entre as linhas, depois do empate
      area.setAttribute('d', ''); areaT.textContent = '';
      if (simples && e) {
        const ex = e.mes, depois = S.filter(p => p.mes > ex);
        const ini = `${x(ex).toFixed(1)},${y(e.valor).toFixed(1)}`;
        area.setAttribute('d', `M${ini}${depois.map(p => `L${pt(p, 'tritan')}`).join('')}${[...depois].reverse().map(p => `L${pt(p, 'sai')}`).join('')}Z`);
        const d = last.tritan - last.sai;
        if (d > 0) {
          const ax = x(xv(last)) - (W - L - R) * 0.2, ay = (y(last.tritan) * 0.35 + y(last.sai) * 0.65);
          areaT.setAttribute('x', ax); areaT.setAttribute('y', ay); areaT.textContent = `${fmt(d)} caixas salvas`;
        }
      }
      // notas curtas no gráfico (só no simples): o que faz cada linha subir
      if (simples) {
        const m = 12, p = S.find(q => q.mes === m);
        if (p) nota(x(m) - 8, y(p.tritan) - 12, `cada quebra: +${fmt(C.troca.caixas)} caixas`, 'end');
        const p0 = S[0];
        nota(x(0) + 10, y(p0.sai) + 16, `instalação: ${fmt(p0.sai)} caixas`);
        S.filter(q => q.mes > 0 && q.mes < mesMax && q.mes % (c.vida_meses || 24) === 0).forEach(q => nota(x(q.mes), y(q.sai) + 18, 'garra nova', 'middle'));
      }
      if (e) {
        const ex = x(eixo === 'mes' ? e.mes : e.mes * CXM), ey = y(e.valor);
        encDot.setAttribute('cx', ex); encDot.setAttribute('cy', ey);
        // perto da base (retorno rápido): rótulo no alto, com linha guia; senão, abaixo e à direita do ponto
        const alto = ey > H - B - 60, ly = alto ? T + 22 : ey + 24;
        encLn.setAttribute('x1', ex); encLn.setAttribute('x2', ex); encLn.setAttribute('y1', ey - 7); encLn.setAttribute('y2', alto ? ly + 22 : ey - 7);
        encT1.setAttribute('x', ex + 8); encT1.setAttribute('y', ly); encT1.textContent = encLbl;
        encT2.setAttribute('x', ex + 8); encT2.setAttribute('y', ly + 15);
        encT2.textContent = eixo === 'mes' ? `${fmt(e.mes, e.mes % 1 ? 1 : 0)} meses (${e.dias} dias)` : `${cxTxt(e.caixas)} caixas · ${e.dias < 60 ? `${e.dias} dias` : `${fmt(e.mes, 1)} meses`}`;
        enc.setAttribute('opacity', 1);
      } else enc.setAttribute('opacity', 0);
      const oque = un === 'rs' ? 'Custo direto acumulado' : 'Caixas perdidas acumuladas';
      svg.setAttribute('aria-label', `${oque} até ${mesMax} meses (${cxTxt(last.caixas)} caixas produzidas): Tritan ${yf(last.tritan)}, garra SAI ${yf(last.sai)}.${e ? ` As linhas se cruzam em ${fmt(e.mes, 1)} meses, cerca de ${e.dias} dias.` : ''}`);
      return c;
    };
    const slide = host.closest('.slide');
    document.addEventListener('slidechange', ev => { if (ev.detail.slide === slide) play(); });
    if (isOn(host)) play();
    return { show, play };
  }

  // Slide de Custos: custo direto no período de manutenção (24 meses)
  const hC = document.getElementById('chart-custo');
  if (hC) chart(hC, { mesMax: 24, campo: 'direto', alt: 236 }).show('previsto');

  // Slide de Retorno: caixas perdidas com a linha parada, no ciclo de 2 anos, com cenário (sem converter em reais)
  const hR = document.getElementById('chart-roi2');
  if (hR) {
    const ch = chart(hR, { mesMax: C.cenarios.previsto.serie_caixas.at(-1).mes, campo: 'caixas', un: 'cx', eixo: 'mes', simples: true, encLbl: 'empata aqui' });
    const $ = id => document.getElementById(id);
    const put = cen => {
      const c = ch.show(cen), e = c.encontro_caixas;
      const cp = c.caixas_perdidas_24m, sp = c.paradas_surpresa_24m, lp = c.linha_parada_min_24m;
      const set = (id, v) => { const n = $(id); if (n) n.textContent = v; };
      set('roi2-pb', e ? `${e.dias} dias` : '—');
      set('roi2-tit', e ? `compensa a instalação em ${e.dias} dias` : 'não compensa');
      set('roi2-pb-s', e ? `cerca de ${fmt(e.mes, e.mes % 1 ? 1 : 0)} meses de linha rodando` : '');
      set('roi2-min', `${hTxt(lp.tritan)} → ${hTxt(lp.sai)}`);
      set('roi2-min-s', `Tritan ${fmt(lp.tritan)} min; SAI ${fmt(lp.sai)} min`);
      set('roi2-cx', fmt(cp.a_mais));
      set('roi2-cx-s', `Tritan perde ${fmt(cp.tritan)}; SAI ${fmt(cp.sai)}`);
      set('roi2-sp', `${sp.tritan} → ${sp.sai}`);
      set('roi2-txt', cen === 'previsto'
        ? 'Previsto: a garra SAI só para a linha na instalação. Os PADs são trocados a cada trimestre em menos de 5 min, sem contar como parada.'
        : `Conservador: a garra SAI dura só ${c.vida_meses} meses e ainda quebra ${c.quebras_sai_ano} vez por ano, com parada surpresa de ${C.troca.min} min.`);
    };
    put('previsto');
    document.querySelectorAll('#roi2-cen button').forEach(b => b.addEventListener('click', () => {
      document.querySelectorAll('#roi2-cen button').forEach(o => { o.classList.toggle('on', o === b); o.setAttribute('aria-selected', o === b); });
      put(b.dataset.c); ch.play();
    }));
  }
})();
