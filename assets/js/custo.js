// Custos e Retorno: Tritan × garra SAI por caixas produzidas (dados em custo-dados.js).
// Custos: custo direto acumulado em R$. Retorno: caixas que deixam de sair, sem converter em reais.
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

  const hTxt = m => (m % 60 ? `${fmt(m / 60, 1)} h` : `${m / 60} h`);

  // Gráfico de linhas: x = caixas produzidas (com o mês embaixo), y = R$ ou caixas acumuladas
  function chart(host, { mesMax, campo, marca24, un = 'rs', encLbl = 'se paga aqui' }) {
    const yf = un === 'rs' ? rs : v => fmt(v);
    const W = 560, H = 306, L = 70, R = 76, T = 16, B = 60;
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img' }, host);
    const grid = el('g', { class: 'grid' }, svg), axis = el('g', { class: 'axis' }, svg), yAx = el('g', {}, axis);
    const cxMax = mesMax * C.producao.caixas_por_mes;
    const x = cx => L + (cx / cxMax) * (W - L - R);
    let yMax = 1, y = v => T + (1 - v / yMax) * (H - T - B);
    for (let m = 0; m <= mesMax; m += 6) {
      const cx = m * C.producao.caixas_por_mes;
      el('line', { x1: x(cx), x2: x(cx), y1: H - B, y2: H - B + 4, stroke: 'rgba(21,21,29,.25)' }, axis);
      el('text', { x: x(cx), y: H - B + 17, 'text-anchor': 'middle' }, axis).textContent = m ? cxTxt(cx) : '0';
      el('text', { x: x(cx), y: H - B + 31, 'text-anchor': 'middle', class: 'sub-tick' }, axis).textContent = m ? `${m} meses` : 'início';
    }
    el('text', { x: (L + W - R) / 2, y: H - 4, class: 'ax-t', 'text-anchor': 'middle' }, axis).textContent = 'caixas produzidas (e o mês de referência)';
    const clip = el('clipPath', { id: `${host.id}-clip` }, el('defs', {}, svg));
    const cr = el('rect', { x: 0, y: 0, width: W, height: H }, clip);
    const g = el('g', { 'clip-path': `url(#${host.id}-clip)` }, svg);
    const pT = el('path', { fill: 'none', stroke: INDIGO, 'stroke-width': 2.4, 'stroke-linejoin': 'round' }, g);
    const pS = el('path', { fill: 'none', stroke: RED, 'stroke-width': 2.4, 'stroke-linejoin': 'round' }, g);
    const dots = el('g', {}, g);
    const endT = el('text', { class: 'lbl' }, g), endS = el('text', { class: 'lbl red' }, g);
    const prev = el('g', {}, g);
    const enc = el('g', {}, g);
    const encLn = el('line', { stroke: RED, 'stroke-width': 1.2, 'stroke-dasharray': '2 3' }, enc);
    const encDot = el('circle', { r: 6, fill: '#fff', stroke: RED, 'stroke-width': 2.5 }, enc);
    const encT1 = el('text', { class: 'lbl red', 'text-anchor': 'start' }, enc), encT2 = el('text', { class: 'lbl sm', 'text-anchor': 'start' }, enc);
    // hover: ponto de cada trimestre
    const cross = el('line', { y1: T, y2: H - B, stroke: 'rgba(21,21,29,.3)', 'stroke-dasharray': '3 3', opacity: 0 }, svg);
    const tip = document.createElement('div'); tip.className = 'tip'; host.appendChild(tip);
    const hit = el('rect', { x: L, y: T, width: W - L - R, height: H - T - B, fill: 'transparent' }, svg);
    let S = [];
    hit.addEventListener('pointermove', ev => {
      const r = svg.getBoundingClientRect(), hr = host.getBoundingClientRect();
      const fx = ((ev.clientX - r.left) * (W / r.width) - L) / (W - L - R) * cxMax;
      const p = S.reduce((a, q) => (Math.abs(q.caixas - fx) < Math.abs(a.caixas - fx) ? q : a));
      const d = p.tritan - p.sai;
      cross.setAttribute('x1', x(p.caixas)); cross.setAttribute('x2', x(p.caixas)); cross.setAttribute('opacity', 1);
      const linha = un === 'rs'
        ? [`Tritan: R$ ${fmt(p.tritan, 0)}`, `SAI: R$ ${fmt(p.sai, 0)}`, d >= 0 ? `o SAI economiza R$ ${fmt(d, 0)}` : `o SAI ainda custa R$ ${fmt(-d, 0)} a mais`]
        : [`Tritan: ${fmt(p.tritan)} caixas perdidas`, `SAI: ${fmt(p.sai)} caixas perdidas`, d >= 0 ? `o SAI salvou ${fmt(d)} caixas` : `o SAI ainda perdeu ${fmt(-d)} caixas a mais`];
      tip.innerHTML = `<b>${p.mes ? `${p.mes} meses · ${cxTxt(p.caixas)} caixas` : 'início'}</b>
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
    const show = cen => {
      const c = C.cenarios[cen];
      S = c[`serie_${campo}`].filter(p => p.mes <= mesMax);
      const top = Math.max(...S.map(p => Math.max(p.tritan, p.sai)));
      const step = nice(top / 4);
      yMax = Math.ceil(top * 1.06 / step) * step;
      grid.replaceChildren(); yAx.replaceChildren();
      for (let v = 0; v <= yMax + 1e-6; v += step) {
        el('line', { x1: L, x2: W - R, y1: y(v), y2: y(v) }, grid);
        el('text', { x: L - 8, y: y(v) + 4, 'text-anchor': 'end' }, yAx).textContent = yf(v);
      }
      const path = k => S.map((p, i) => `${i ? 'L' : 'M'}${x(p.caixas).toFixed(1)},${y(p[k]).toFixed(1)}`).join('');
      pT.setAttribute('d', path('tritan')); pS.setAttribute('d', path('sai'));
      dots.replaceChildren();
      S.forEach(p => {
        el('circle', { cx: x(p.caixas), cy: y(p.tritan), r: 3.6, fill: INDIGO, stroke: '#fff', 'stroke-width': 1.6 }, dots);
        el('circle', { cx: x(p.caixas), cy: y(p.sai), r: 3.6, fill: RED, stroke: '#fff', 'stroke-width': 1.6 }, dots);
      });
      const last = S[S.length - 1], yT = y(last.tritan), yS = y(last.sai), sep = Math.abs(yT - yS) < 16 ? 9 : 0;
      endT.setAttribute('x', x(last.caixas) + 8); endT.setAttribute('y', yT + 4 - (yT <= yS ? sep : -sep)); endT.textContent = yf(last.tritan);
      endS.setAttribute('x', x(last.caixas) + 8); endS.setAttribute('y', yS + 4 + (yT <= yS ? sep : -sep)); endS.textContent = yf(last.sai);
      prev.replaceChildren();
      if (marca24) S.filter(q => q.mes > 0 && q.mes % (c.vida_meses || 24) === 0).forEach(p => {
        el('text', { x: x(p.caixas), y: y(p.sai) + 20, class: 'lbl sm', 'text-anchor': 'middle' }, prev).textContent = 'garra nova';
      });
      const e = c[`encontro_${campo}`];
      if (e) {
        const ex = x(e.mes * C.producao.caixas_por_mes), ey = y(e.valor);
        encDot.setAttribute('cx', ex); encDot.setAttribute('cy', ey);
        // perto da base (retorno rápido): rótulo no alto, com linha guia; senão, abaixo e à direita do ponto
        const alto = ey > H - B - 60, ly = alto ? T + 22 : ey + 24;
        encLn.setAttribute('x1', ex); encLn.setAttribute('x2', ex); encLn.setAttribute('y1', ey - 7); encLn.setAttribute('y2', alto ? ly + 22 : ey - 7);
        encT1.setAttribute('x', ex + 8); encT1.setAttribute('y', ly); encT1.textContent = encLbl;
        encT2.setAttribute('x', ex + 8); encT2.setAttribute('y', ly + 15);
        encT2.textContent = `${cxTxt(e.caixas)} caixas · ${e.dias < 60 ? `${e.dias} dias` : `${fmt(e.mes, 1)} meses`}`;
        enc.setAttribute('opacity', 1);
      } else enc.setAttribute('opacity', 0);
      const oque = un === 'rs' ? 'Custo direto acumulado' : 'Caixas perdidas acumuladas';
      svg.setAttribute('aria-label', `${oque} até ${mesMax} meses (${cxTxt(last.caixas)} caixas produzidas): Tritan ${yf(last.tritan)}, garra SAI ${yf(last.sai)}.${e ? ` As linhas se cruzam com ${cxTxt(e.caixas)} caixas, cerca de ${e.dias} dias.` : ''}`);
      return c;
    };
    const slide = host.closest('.slide');
    document.addEventListener('slidechange', ev => { if (ev.detail.slide === slide) play(); });
    if (isOn(host)) play();
    return { show, play };
  }

  // Slide de Custos: custo direto no período de manutenção (24 meses)
  const hC = document.getElementById('chart-custo');
  if (hC) chart(hC, { mesMax: 24, campo: 'direto', marca24: false }).show('previsto');

  // Slide de Retorno: caixas que deixam de sair, até 30 meses, com cenário (sem converter em reais)
  const hR = document.getElementById('chart-roi2');
  if (hR) {
    const ch = chart(hR, { mesMax: C.cenarios.previsto.serie_caixas.at(-1).mes, campo: 'caixas', marca24: true, un: 'cx', encLbl: 'compensa aqui' });
    const $ = id => document.getElementById(id);
    const put = cen => {
      const c = ch.show(cen), e = c.encontro_caixas;
      const cp = c.caixas_perdidas_24m, sp = c.paradas_surpresa_24m, lp = c.linha_parada_min_24m;
      const set = (id, v) => { const n = $(id); if (n) n.textContent = v; };
      set('roi2-pb', e ? `${e.dias} dias` : '—');
      set('roi2-tit', e ? `compensa a instalação em ${e.dias} dias` : 'não compensa');
      set('roi2-pb-s', e ? `cerca de ${cxTxt(e.caixas)} caixas produzidas` : '');
      set('roi2-min', `${hTxt(lp.tritan)} → ${hTxt(lp.sai)}`);
      set('roi2-min-s', `Tritan ${fmt(lp.tritan)} min; SAI ${fmt(lp.sai)} min`);
      set('roi2-cx', fmt(cp.a_mais));
      set('roi2-cx-s', `Tritan perde ${fmt(cp.tritan)}; SAI ${fmt(cp.sai)}`);
      set('roi2-sp', `${sp.tritan} → ${sp.sai}`);
      set('roi2-txt', cen === 'previsto'
        ? 'Previsto: a garra SAI é trocada a cada 2 anos e os PADs a cada trimestre, sempre com data marcada.'
        : `Conservador: a garra SAI dura só ${c.vida_meses} meses e ainda quebra ${c.quebras_sai_ano} vez por ano, com parada surpresa de 45 min.`);
    };
    put('previsto');
    document.querySelectorAll('#roi2-cen button').forEach(b => b.addEventListener('click', () => {
      document.querySelectorAll('#roi2-cen button').forEach(o => { o.classList.toggle('on', o === b); o.setAttribute('aria-selected', o === b); });
      put(b.dataset.c); ch.play();
    }));
  }
})();
