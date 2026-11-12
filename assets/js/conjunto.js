// Peso do conjunto inteiro (garra superior + 2 inferiores + resto da montagem), todas as rodadas. Lê window.CONJUNTO.
(() => {
  const D = window.CONJUNTO;
  const host = document.getElementById('chart-conjunto');
  if (!D || !host) return;
  const NS = 'http://www.w3.org/2000/svg';
  const fmt = (n, d = 1) => n.toLocaleString('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
  const sgn = (n, d = 1) => (n > 0 ? '+' : n < 0 ? '−' : '') + fmt(Math.abs(n), d);
  const kg = g => fmt(g / 1000, 3);
  const el = (tag, attrs = {}, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  // cor = peça (identidade), igual em todas as linhas
  const PARTS = [
    { f: 'sup_g', k: 'Superior', c: '#3b3d50' },
    { f: 'inf_esq_g', k: 'Inferior esq.', c: '#5b5bd6' },
    { f: 'inf_dir_g', k: 'Inferior dir.', c: '#9a9ae8' },
    { f: 'resto_g', k: 'Ferragens, ventosas e PADs', c: '#cfd0db' },
  ];
  const rows = D.linhas;

  const lg = host.querySelector('.legend');
  if (lg) lg.innerHTML = PARTS.map(p => `<span><i style="background:${p.c}; height:10px; width:10px; border-radius:3px"></i>${p.k}</span>`).join('');

  const W = 620, rowH = 18, gap = 6, L = 214, R = 92, T = 22;
  const H = T + rows.length * (rowH + gap) + 20;
  const max = 3200, x = g => L + (g / max) * (W - L - R);
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Peso do conjunto inteiro por opção: ' + rows.map(r => `${r.rot} ${kg(r.conjunto_g)} kg`).join('; ') }, host);
  const tip = document.createElement('div'); tip.className = 'tip'; host.appendChild(tip);

  const ax = el('g', { class: 'axis' }, svg);
  for (let g = 0; g <= 3000; g += 500) {
    el('line', { x1: x(g), x2: x(g), y1: T - 6, y2: H - 16 }, ax);
    el('text', { x: x(g), y: H - 2, 'text-anchor': 'middle' }, ax).textContent = `${fmt(g / 1000, 1)} kg`;
  }
  const ref = D.conj_tritan_kg * 1000;
  el('line', { x1: x(ref), x2: x(ref), y1: T - 8, y2: H - 16, stroke: 'rgba(21,21,29,.6)', 'stroke-dasharray': '3 3' }, svg);
  el('text', { x: x(ref), y: 11, class: 'lbl', 'text-anchor': 'middle', style: 'font-size:10px' }, svg).textContent = `Tritan instalada ${kg(ref)} kg`;

  rows.forEach((r, i) => {
    const y = T + i * (rowH + gap);
    const lab = el('text', { x: 0, y: y + rowH / 2 + 4, class: 'lbl', style: r.k === 'TRITAN' ? 'font-weight:600' : '' }, svg);
    lab.textContent = r.rot;
    const g = el('g', { class: 'grow', style: 'transform-origin:left center' }, svg);
    let acc = 0;
    PARTS.forEach((p, j) => {
      const w = x(r[p.f]) - x(0);
      const last = j === PARTS.length - 1;
      // 2 px de respiro entre segmentos; ponta arredondada só no fim da barra
      el(last ? 'path' : 'rect', last
        ? { d: `M${x(0) + acc},${y} h${Math.max(w - 4, 0)} a4,4 0 0 1 4,4 v${rowH - 8} a4,4 0 0 1 -4,4 h${-Math.max(w - 4, 0)} z`, fill: p.c }
        : { x: x(0) + acc, y, width: Math.max(w - 2, 0), height: rowH, fill: p.c }, g);
      acc += w;
    });
    el('text', { x: W - R + 8, y: y + rowH / 2 + 4, class: 'lbl' }, svg).textContent =
      r.k === 'TRITAN' ? `${kg(r.conjunto_g)} kg` : `${kg(r.conjunto_g)} · ${sgn(r.pct_conjunto)}%`;
    const hit = el('rect', { x: 0, y: y - gap / 2, width: W, height: rowH + gap, fill: 'transparent' }, svg);
    hit.addEventListener('pointermove', ev => {
      const hr = host.getBoundingClientRect();
      tip.innerHTML = `<b>${r.rot}</b> · ${r.rodada}` +
        PARTS.map(p => `<div class="r"><i style="background:${p.c}"></i>${p.k}: ${fmt(r[p.f], 0)} g${p.f === 'inf_dir_g' && r.inf_dir_espelho ? ' (espelho)' : ''}</div>`).join('') +
        `Garra impressa: ${fmt(r.garra_g, 0)} g (${sgn(r.pct_garra)}%)<br><b>Conjunto: ${kg(r.conjunto_g)} kg</b> (${sgn(r.dif_conjunto_g, 0)} g)<br>Com 2 caixas: ${fmt(r.com_caixas_kg, 2)} kg · folga UR30 ${fmt(r.folga_ur30_kg, 2)} kg`;
      tip.classList.add('on');
      const tx = ev.clientX - hr.left, ty = ev.clientY - hr.top;
      tip.style.left = `${Math.min(Math.max(tx + 14, 8), host.clientWidth - tip.offsetWidth - 8)}px`;
      tip.style.top = `${Math.max(ty - tip.offsetHeight - 10, 8)}px`;
    });
    hit.addEventListener('pointerleave', () => tip.classList.remove('on'));
  });

  const tb = document.getElementById('tbl-conjunto');
  if (tb) tb.innerHTML = rows.map(r => `<tr${r.k === 'TRITAN' ? ' class="ref"' : ''}><td class="nw" title="${r.rodada}">${r.rot}</td>
    <td>${fmt(r.sup_g, 0)}</td><td>${fmt(r.inf_esq_g, 0)}</td><td>${fmt(r.inf_dir_g, 0)}${r.inf_dir_espelho ? '<sup>e</sup>' : ''}</td>
    <td>${fmt(r.garra_g, 0)}</td><td><b>${kg(r.conjunto_g)}</b></td><td>${r.k === 'TRITAN' ? '—' : sgn(r.dif_conjunto_g, 0) + ' g'}</td><td>${fmt(r.com_caixas_kg, 2)}</td></tr>`).join('');
  const so = document.getElementById('tbl-conjunto-sup');
  if (so) so.innerHTML = D.so_superior.map(s => `${s.rot.replace('R06 superior uniforme ', 'R06 uniforme ')} <b>${fmt(s.sup_g, 0)} g</b>`).join(' · ');
})();
