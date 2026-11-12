// R07 · comparação com × sem esqueleto e preenchimento uniforme. Tudo lido de window.R07 (gerado de dados/*.json).
(() => {
  const D = window.R07;
  if (!D) return;
  const NS = 'http://www.w3.org/2000/svg';
  const RED = '#e5232f', INDIGO = '#5b5bd6', GRAY = '#a9aabb', DARK = '#3b3d50';
  const fmt = (n, d = 1) => n.toLocaleString('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
  const sgn = (n, d = 1) => (n > 0 ? '+' : n < 0 ? '−' : '') + fmt(Math.abs(n), d);
  const V = Object.fromEntries(D.variantes.map(v => [v.k, v]));
  const COLOR = { R07_COM: RED, R07_SEM: INDIGO, UNI_40: DARK };
  const col = k => COLOR[k] || GRAY;

  const el = (tag, attrs = {}, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  function makeTip(host) {
    const tip = document.createElement('div'); tip.className = 'tip'; host.appendChild(tip);
    return {
      show(html, x, y) {
        tip.innerHTML = html; tip.classList.add('on');
        const hw = host.clientWidth, tw = tip.offsetWidth;
        tip.style.left = `${Math.min(Math.max(x + 14, 8), hw - tw - 8)}px`;
        tip.style.top = `${Math.max(y - tip.offsetHeight - 10, 8)}px`;
      },
      hide() { tip.classList.remove('on'); }
    };
  }
  const pointer = (svg, host, ev, W) => {
    const r = svg.getBoundingClientRect(), hr = host.getBoundingClientRect();
    return { vx: (ev.clientX - r.left) * (W / r.width), hx: ev.clientX - hr.left, hy: ev.clientY - hr.top };
  };
  const hbar = (x0, y, w, h) => w >= 0
    ? `M${x0},${y} h${Math.max(w - 4, 0)} a4,4 0 0 1 4,4 v${h - 8} a4,4 0 0 1 -4,4 h${-Math.max(w - 4, 0)} z`
    : `M${x0},${y} h${Math.min(w + 4, 0)} a4,4 0 0 0 -4,4 v${h - 8} a4,4 0 0 0 4,4 h${-Math.min(w + 4, 0)} z`;

  /* ---------- Δ massa vs garra instalada (Tritan Hexa3D 30%) ---------- */
  function chartMassa() {
    const host = document.getElementById('chart-r07-massa');
    if (!host) return;
    const order = ['R07_SEM', 'HEXA30', 'UNI_30', 'R07_COM', 'UNI_35', 'R06', 'UNI_40', 'TPMSD40'];
    const data = order.map(k => V[k]);
    const W = 600, rowH = 26, gap = 8, L = 168, R = 118, T = 22;
    const H = T + data.length * (rowH + gap) + 6;
    const lo = -12, hi = 16, x = p => L + ((p - lo) / (hi - lo)) * (W - L - R);
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Variação de massa da garra impressa em relação à garra Tritan instalada: ' + data.map(d => `${d.rot} ${sgn(d.pct_tritan)}%`).join('; ') }, host);
    const tip = makeTip(host);
    // faixa da meta 5–10% mais leve
    el('rect', { x: x(-10), y: T - 6, width: x(-5) - x(-10), height: H - T, fill: 'rgba(31,157,107,.10)' }, svg);
    el('text', { x: (x(-10) + x(-5)) / 2, y: 12, class: 'lbl', 'text-anchor': 'middle', style: 'font-size:10px; fill:#1f7d58' }, svg).textContent = 'meta −5 a −10%';
    el('line', { x1: x(0), x2: x(0), y1: T - 6, y2: H, stroke: 'rgba(21,21,29,.55)' }, svg);
    el('text', { x: x(0) + 4, y: 12, class: 'lbl', style: 'font-size:10px' }, svg).textContent = `Tritan atual ${fmt(D.tritan_g, 0)} g`;
    data.forEach((d, i) => {
      const y = T + i * (rowH + gap);
      el('text', { x: 0, y: y + rowH / 2 + 4, class: 'lbl' }, svg).textContent = d.rot;
      el('path', { d: hbar(x(0), y, x(d.pct_tritan) - x(0), rowH), fill: col(d.k), class: 'grow', style: `transform-origin:${d.pct_tritan < 0 ? 'right' : 'left'} center` }, svg);
      el('text', { x: W - R + 8, y: y + rowH / 2 + 4, class: 'lbl' }, svg).textContent = `${fmt(d.garra_g, 0)} g · ${sgn(d.pct_tritan)}%`;
      const hit = el('rect', { x: 0, y: y - gap / 2, width: W, height: rowH + gap, fill: 'transparent' }, svg);
      hit.addEventListener('pointermove', ev => {
        const p = pointer(svg, host, ev, W);
        tip.show(`<b>${d.rot}</b><br>Garra impressa: ${fmt(d.garra_g, 1)} g (${sgn(d.garra_g - D.tritan_g, 0)} g)<br>Superior ${fmt(d.sup_g, 0)} g · inferior ${fmt(d.inf_g, 0)} g (×2)<br>Filamento c/ suportes: ${fmt(d.fil_g, 0)} g · ${fmt(d.tempo_h, 1)} h`, p.hx, p.hy);
      });
      hit.addEventListener('pointerleave', () => tip.hide());
    });
  }

  /* ---------- Carga máxima numa asa, garra MONTADA ---------- */
  function chartCarga() {
    const host = document.getElementById('chart-r07-carga');
    if (!host) return;
    const S = [{ k: 'PA6-CF (Z 48 MPa)', c: RED, f: 'kg_pa6' }, { k: 'PAHT CF15 (Z 18,2 MPa)', c: INDIGO, f: 'kg_paht' }];
    const data = ['R06', 'R07_COM', 'R07_SEM', 'UNI_30', 'UNI_35', 'UNI_40'].map(k => V[k]);
    const W = 560, bh = 13, inner = 3, gap = 12, L = 150, R = 52, T = 26;
    const rowH = 2 * bh + inner, H = T + data.length * (rowH + gap) + 14;
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Carga máxima numa asa, garra montada: ' + data.map(d => `${d.rot} ${fmt(d.kg_pa6)} kg (PA6-CF), ${fmt(d.kg_paht)} kg (PAHT CF15)`).join('; ') }, host);
    const max = 110, x = v => L + (v / max) * (W - L - R);
    const tip = makeTip(host);
    S.forEach((s, j) => {
      const lx = L + j * 170;
      el('rect', { x: lx, y: 2, width: 10, height: 10, rx: 3, fill: s.c }, svg);
      el('text', { x: lx + 16, y: 11, class: 'lbl' }, svg).textContent = s.k;
    });
    [[24, '24', 'end', -3], [30, '30 kg', 'start', 3]].forEach(([v, t, a, dx]) => {
      el('line', { x1: x(v), x2: x(v), y1: T - 4, y2: H - 10, stroke: 'rgba(21,21,29,.45)', 'stroke-dasharray': '3 3' }, svg);
      el('text', { x: x(v) + dx, y: H, class: 'lbl', 'text-anchor': a, style: 'font-size:10px' }, svg).textContent = t;
    });
    data.forEach((d, i) => {
      const y0 = T + i * (rowH + gap);
      el('text', { x: 0, y: y0 + rowH / 2 + 4, class: 'lbl' }, svg).textContent = d.rot;
      S.forEach((s, j) => {
        const y = y0 + j * (bh + inner), v = d[s.f];
        el('path', { d: hbar(L, y, x(v) - L, bh), fill: s.c, class: 'grow' }, svg);
        el('text', { x: x(v) + 6, y: y + bh - 2, class: 'lbl', style: 'font-size:11px' }, svg).textContent = `${fmt(v, 0)} kg`;
      });
      const hit = el('rect', { x: 0, y: y0 - gap / 2, width: W, height: rowH + gap, fill: 'transparent' }, svg);
      hit.addEventListener('pointermove', ev => {
        const p = pointer(svg, host, ev, W);
        tip.show(`<b>${d.rot}</b> · ${fmt(d.garra_g, 0)} g` + S.map(s => `<div class="r"><i style="background:${s.c}"></i>${s.k}: ${fmt(d[s.f])} kg</div>`).join('') +
          `FS 24/30 kg PAHT: ${fmt(d.fs24_paht, 2)} / ${fmt(d.fs30_paht, 2)}<br>Rigidez da asa: ${fmt(d.k_asa)} N/mm`, p.hx, p.hy);
      });
      hit.addEventListener('pointerleave', () => tip.hide());
    });
    el('line', { x1: L, x2: L, y1: T - 4, y2: H - 10, stroke: 'rgba(21,21,29,.25)' }, svg);
  }

  /* ---------- Massa × carga máxima numa asa (garra montada); faixa PAHT → PA6-CF ---------- */
  function chartPesoCarga() {
    const host = document.getElementById('chart-r07-pesocarga');
    if (!host) return;
    const keys = ['R07_COM', 'R07_SEM', 'UNI_30', 'UNI_35', 'UNI_40', 'R06'];
    const W = 560, H = 300, L = 44, R = 18, T = 14, B = 34, x0 = 1350, x1 = 1800, yMax = 110;
    const x = g => L + ((g - x0) / (x1 - x0)) * (W - L - R), y = kg => T + (1 - kg / yMax) * (H - T - B);
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Massa da garra versus carga máxima numa asa: ' + keys.map(k => `${V[k].rot} ${fmt(V[k].garra_g, 0)} g, ${fmt(V[k].kg_pa6, 0)} kg PA6-CF, ${fmt(V[k].kg_paht, 0)} kg PAHT`).join('; ') }, host);
    const grid = el('g', { class: 'grid' }, svg), axis = el('g', { class: 'axis' }, svg);
    for (let k = 0; k <= 100; k += 20) {
      el('line', { x1: L, x2: W - R, y1: y(k), y2: y(k) }, grid);
      el('text', { x: L - 8, y: y(k) + 4, 'text-anchor': 'end' }, axis).textContent = k;
    }
    for (let g = 1400; g <= x1; g += 100) el('text', { x: x(g), y: H - 14, 'text-anchor': 'middle' }, axis).textContent = fmt(g, 0);
    el('text', { x: (L + W - R) / 2, y: H - 1, 'text-anchor': 'middle' }, axis).textContent = 'massa da garra impressa (g)';
    el('text', { x: 4, y: T - 2 }, axis).textContent = 'kg';
    // meta de massa (−5 a −10% da Tritan) e linha da Tritan
    el('rect', { x: x(D.tritan_g * 0.90), y: T, width: x(D.tritan_g * 0.95) - x(D.tritan_g * 0.90), height: H - T - B, fill: 'rgba(31,157,107,.10)' }, svg);
    el('line', { x1: x(D.tritan_g), x2: x(D.tritan_g), y1: T, y2: H - B, stroke: 'rgba(21,21,29,.45)', 'stroke-dasharray': '3 3' }, svg);
    el('text', { x: x(D.tritan_g) + 4, y: T + 10, class: 'lbl', style: 'font-size:10px' }, svg).textContent = `Tritan ${fmt(D.tritan_g, 0)} g`;
    el('text', { x: x(D.tritan_g * 0.925), y: T + 10, class: 'lbl', 'text-anchor': 'middle', style: 'font-size:10px; fill:#1f7d58' }, svg).textContent = 'meta';
    // erro de processo: 24 kg numa asa
    el('line', { x1: L, x2: W - R, y1: y(24), y2: y(24), stroke: '#c2410c', 'stroke-width': 1.5, 'stroke-dasharray': '5 4' }, svg);
    el('text', { x: L + 6, y: y(24) + 15, class: 'lbl', style: 'font-size:11px; fill:#9a3412' }, svg).textContent = '24 kg · 2 caixas numa asa';
    const off = { R07_COM: [9, 4, 'start'], R07_SEM: [-9, 4, 'end'], UNI_30: [9, 4, 'start'], UNI_35: [9, 4, 'start'], UNI_40: [9, 4, 'start'], R06: [9, 4, 'start'] };
    const SH = { R07_COM: 'R07 com', R07_SEM: 'R07 sem', UNI_30: 'Giroide 30%', UNI_35: 'Giroide 35%', UNI_40: 'Giroide 40%', R06: 'R06' };
    const tip = makeTip(host);
    keys.forEach(k => {
      const v = V[k], cx = x(v.garra_g), c = col(k), [dx, dy, a] = off[k];
      el('line', { x1: cx, x2: cx, y1: y(v.kg_paht), y2: y(v.kg_pa6), stroke: c, 'stroke-width': 2, opacity: .45 }, svg);
      el('circle', { cx, cy: y(v.kg_paht), r: 5, fill: '#fff', stroke: c, 'stroke-width': 2 }, svg);
      el('circle', { cx, cy: y(v.kg_pa6), r: 6, fill: c, stroke: '#fff', 'stroke-width': 2 }, svg);
      el('text', { x: cx + dx, y: y(v.kg_pa6) + dy, class: 'lbl', 'text-anchor': a, style: 'font-size:11px' }, svg).textContent = `${SH[k]} · ${fmt(v.kg_pa6, 0)} kg`;
      const hit = el('rect', { x: cx - 14, y: y(v.kg_pa6) - 14, width: 28, height: y(v.kg_paht) - y(v.kg_pa6) + 28, fill: 'transparent' }, svg);
      hit.addEventListener('pointermove', ev => {
        const p = pointer(svg, host, ev, W);
        tip.show(`<b>${v.rot}</b> · ${fmt(v.garra_g, 0)} g (${sgn(v.pct_tritan)}% vs Tritan)<div class="r"><i style="background:${c}"></i>PA6-CF: ${fmt(v.kg_pa6)} kg · FS 24 kg ${fmt(v.fs24_pa6, 2)}</div><div class="r"><i style="background:#fff; box-shadow:inset 0 0 0 2px ${c}"></i>PAHT CF15: ${fmt(v.kg_paht)} kg · FS 24 kg ${fmt(v.fs24_paht, 2)}${v.fs24_paht < 1 ? ' ⚠' : ''}</div>Flecha a 24 kg: ${fmt(v.desl24, 2)} mm`, p.hx, p.hy);
      });
      hit.addEventListener('pointerleave', () => tip.hide());
    });
  }

  /* ---------- Impacto: σZ no ponto crítico ao longo do tempo ---------- */
  function chartImpacto() {
    const host = document.getElementById('chart-r07-impacto');
    if (!host) return;
    const keys = ['R07_COM', 'R07_SEM', 'UNI_30', 'UNI_40'].filter(k => V[k] && V[k].impacto);
    const W = 640, H = 260, L = 40, R = 16, T = 10, B = 28, tMax = 80, sMax = 30;
    const x = t => L + (t / tMax) * (W - L - R), y = s => T + (1 - s / sMax) * (H - T - B);
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Tensão entre camadas no ponto crítico durante o tranco: ' + keys.map(k => `${V[k].rot} pico ${fmt(V[k].impacto.sz)} MPa`).join('; ') }, host);
    const grid = el('g', { class: 'grid' }, svg), axis = el('g', { class: 'axis' }, svg);
    for (let s = 0; s <= sMax; s += 10) {
      el('line', { x1: L, x2: W - R, y1: y(s), y2: y(s) }, grid);
      el('text', { x: L - 8, y: y(s) + 4, 'text-anchor': 'end' }, axis).textContent = s;
    }
    for (let t = 0; t <= tMax; t += 10) el('text', { x: x(t), y: H - 8, 'text-anchor': 'middle' }, axis).textContent = `${t} ms`;
    el('line', { x1: L, x2: W - R, y1: y(18.2), y2: y(18.2), stroke: 'rgba(21,21,29,.55)', 'stroke-dasharray': '4 4' }, svg);
    el('text', { x: W - R, y: y(18.2) - 5, class: 'lbl', 'text-anchor': 'end', style: 'font-size:10px' }, svg).textContent = 'limite Z PAHT CF15 · 18,2 MPa';
    const dash = { UNI_30: '6 4' };
    keys.forEach(k => {
      const s = V[k].impacto.serie;
      el('path', { d: s.map((p, i) => `${i ? 'L' : 'M'}${x(p[0]).toFixed(1)},${y(p[1]).toFixed(1)}`).join(''), fill: 'none', stroke: col(k), 'stroke-width': 2, 'stroke-dasharray': dash[k] || '', class: 'draw' }, svg);
    });
    const cross = el('line', { y1: T, y2: H - B, stroke: 'rgba(21,21,29,.3)', 'stroke-dasharray': '3 3', opacity: 0 }, svg);
    const dots = keys.map(k => el('circle', { r: 4, fill: col(k), stroke: '#fff', 'stroke-width': 2, opacity: 0 }, svg));
    const tip = makeTip(host);
    const hit = el('rect', { x: L, y: T, width: W - L - R, height: H - T - B, fill: 'transparent' }, svg);
    hit.addEventListener('pointermove', ev => {
      const p = pointer(svg, host, ev, W);
      const t = Math.max(0, Math.min(tMax, ((p.vx - L) / (W - L - R)) * tMax));
      const s0 = V[keys[0]].impacto.serie, i = s0.reduce((a, q, j) => (Math.abs(q[0] - t) < Math.abs(s0[a][0] - t) ? j : a), 0);
      const cx = x(s0[i][0]);
      cross.setAttribute('x1', cx); cross.setAttribute('x2', cx); cross.setAttribute('opacity', 1);
      keys.forEach((k, j) => { const q = V[k].impacto.serie[i]; dots[j].setAttribute('cx', cx); dots[j].setAttribute('cy', y(q[1])); dots[j].setAttribute('opacity', 1); });
      tip.show(`<b>${fmt(s0[i][0], 0)} ms</b>` + keys.map(k => { const q = V[k].impacto.serie[i]; return `<div class="r"><i style="background:${col(k)}"></i>${V[k].rot}: ${fmt(q[1])} MPa · giroide ${fmt(q[2] * 100, 0)}%</div>`; }).join(''), p.hx, p.hy);
    });
    hit.addEventListener('pointerleave', () => { cross.setAttribute('opacity', 0); dots.forEach(d => d.setAttribute('opacity', 0)); tip.hide(); });
    const lg = host.querySelector('.legend');
    if (lg) lg.innerHTML = keys.map(k => `<span><i style="background:${col(k)}"></i>${V[k].rot}</span>`).join('');
  }

  /* ---------- Tabelas preenchidas a partir dos dados ---------- */
  function tables() {
    const dec = document.getElementById('tbl-decisao');
    if (dec) dec.innerHTML = ['R07_COM', 'R07_SEM', 'UNI_30', 'UNI_35', 'UNI_40', 'R06'].map(k => {
      const v = V[k], im = v.impacto;
      return `<tr><td><span class="sw" style="background:${col(k)}"></span>${v.rot}</td><td>${fmt(v.garra_g, 0)} g</td><td>${sgn(v.pct_tritan)}%</td>
        <td>${fmt(v.kg_pa6)} / ${fmt(v.kg_paht)}</td><td>${fmt(v.fs30_paht, 2)}</td><td>${fmt(v.desl24, 2)} mm</td>
        <td>${im ? `${fmt(im.sz)} MPa · ${fmt(im.fs_paht, 2)}` : '<span class="na">não rodado</span>'}</td></tr>`;
    }).join('');
    const orca = document.getElementById('tbl-orca');
    if (orca) orca.innerHTML = ['R07_COM', 'R07_SEM', 'HEXA30', 'UNI_30', 'UNI_35', 'UNI_40', 'TPMSD40', 'R06'].map(k => {
      const v = V[k];
      return `<tr><td><span class="sw" style="background:${col(k)}"></span>${v.rot}</td><td>${fmt(v.sup_g, 0)}</td><td>${fmt(v.inf_g, 0)} ×2</td><td><b>${fmt(v.garra_g, 0)}</b></td>
        <td>${sgn(v.pct_tritan)}%</td><td>${v.proprio_fe ? '' : '≈ '}${fmt(v.kg_pa6, 0)} kg <small class="muted">FS ${fmt(v.fs24_pa6, 1)}</small></td><td>${fmt(v.tempo_h, 1)} h</td><td>R$ ${fmt(v.custo_rs, 2)}</td></tr>`;
    }).join('');
    const SHORT = { R07_COM: 'R07 com', R07_SEM: 'R07 sem', UNI_30: 'Giroide 30%', UNI_35: 'Giroide 35%', UNI_40: 'Giroide 40%', R06: 'R06 zonal' };
    const fsCell = f => f < 1 ? `<td class="fs-bad" title="FS < 1: rompe antes dos 24 kg">⚠ ${fmt(f, 2)}</td>` : `<td>${fmt(f, 2)}</td>`;
    const pc = document.getElementById('tbl-pesocarga');
    if (pc) pc.innerHTML = ['R07_COM', 'R07_SEM', 'UNI_30', 'UNI_35', 'UNI_40', 'R06'].map(k => {
      const v = V[k], im = v.impacto;
      return `<tr><td class="nw"><span class="sw" style="background:${col(k)}"></span>${SHORT[k]}</td><td>${fmt(v.garra_g, 0)} g</td>
        <td><b>${fmt(v.kg_pa6, 1)} kg</b></td>${fsCell(v.fs24_pa6)}<td>${fmt(v.kg_paht, 1)} kg</td>${fsCell(v.fs24_paht)}
        ${im ? `<td${im.fs_paht < 1 ? ' class="fs-bad"' : ''}>${fmt(im.fs_pa6, 2)} / ${im.fs_paht < 1 ? '⚠ ' : ''}${fmt(im.fs_paht, 2)}</td>` : '<td><span class="na">não rodado</span></td>'}</tr>`;
    }).join('');
    const vida = document.getElementById('tbl-vida');
    if (vida) vida.innerHTML = ['R06', 'R07_COM', 'R07_SEM', 'UNI_30', 'UNI_40'].map(k => {
      const v = V[k], h = n => n >= 1e5 ? '> 100.000 h' : `${fmt(n, 0)} h`;
      return `<tr><td>${v.rot}</td><td>${h(v.vida_paht.so_12kg_h)}</td><td>${h(v.vida_paht.mix_1pct_24kg_h)}</td><td>${h(v.vida_pa6.mix_1pct_24kg_h)}</td></tr>`;
    }).join('');
    // textos com valores (data-r07="VARIANTE.campo[.sub]" + data-d casas decimais)
    document.querySelectorAll('[data-r07]').forEach(e => {
      const [k, ...path] = e.dataset.r07.split('.');
      let v = path.reduce((o, p) => (o == null ? o : o[p]), k === 'pads' ? D.pads : k === 'tritan_g' ? D.tritan_g : V[k]);
      if (typeof v === 'number' && e.dataset.pct) { e.textContent = fmt(v * 100, 0); return; }
      if (typeof v === 'number') e.textContent = (e.dataset.sign ? sgn(v, +(e.dataset.d || 0)) : fmt(v, +(e.dataset.d || 0)));
    });
    // números dos vídeos (data-vid="video.variante.campo"), de dados/videos/videos_r07.json
    document.querySelectorAll('[data-vid]').forEach(e => {
      const v = e.dataset.vid.split('.').reduce((o, p) => (o == null ? o : o[p]), D.videos);
      if (typeof v === 'number') e.textContent = fmt(v, +(e.dataset.d || 0));
    });
  }

  /* ---------- Mapas da garra montada ---------- */
  function mapas() {
    const seg = document.getElementById('mapa-montagem'), img = document.getElementById('mapa-montagem-img'), cap = document.getElementById('mapa-montagem-cap');
    if (!seg) return;
    const render = k => {
      const v = V[k];
      img.src = `assets/img/r07/montagem_${k}.jpg`;
      img.alt = `Mapa de índice de falha da garra montada, ${v.rot}, 24 kg numa asa: planta e vista lateral`;
      cap.textContent = `${v.rot} · 24 kg numa asa · σZ de pico ${fmt(v.sz24, 1)} MPa · flecha ${fmt(v.desl24, 2)} mm · máx. ${fmt(v.kg_pa6, 1)} kg (PA6-CF) / ${fmt(v.kg_paht, 1)} kg (PAHT)`;
    };
    seg.querySelectorAll('button').forEach(b => {
      new Image().src = `assets/img/r07/montagem_${b.dataset.v}.jpg`;
      b.addEventListener('click', () => { seg.querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b)); render(b.dataset.v); });
    });
    render(seg.querySelector('.on').dataset.v);
  }

  /* ---------- Galeria com ampliação ---------- */
  function galeria() {
    const dlg = document.getElementById('lightbox');
    if (!dlg) return;
    const img = dlg.querySelector('img'), cap = dlg.querySelector('figcaption');
    document.querySelectorAll('[data-zoom]').forEach(a => a.addEventListener('click', ev => {
      ev.preventDefault();
      img.src = a.getAttribute('href'); img.alt = a.querySelector('img')?.alt || '';
      cap.textContent = a.dataset.zoom;
      dlg.showModal();
    }));
    dlg.addEventListener('click', () => dlg.close());
    dlg.addEventListener('keydown', ev => ev.stopPropagation());
  }

  /* ---------- Vídeo do impacto R07: toca só com o slide aberto ---------- */
  // vídeos que tocam do início quando o slide abre (#video-r07 e todo <video data-autoplay>)
  function video() {
    const vids = [document.getElementById('video-r07'), ...document.querySelectorAll('video[data-autoplay]')].filter(Boolean);
    vids.forEach(v => { v.muted = true; });
    document.addEventListener('slidechange', () => vids.forEach(v => {
      const on = v.closest('.slide').classList.contains('on') && !v.closest('[hidden]');
      if (on) { v.currentTime = 0; v.play().catch(() => {}); } else v.pause();
    }));
  }

  // seletores de vídeo: botões com data-src trocam o <video> alvo (data-target) e a legenda
  function videoTabs() {
    document.querySelectorAll('.seg[data-video]').forEach(seg => {
      const v = document.getElementById(seg.dataset.video), cap = document.getElementById(seg.dataset.cap);
      seg.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
        seg.querySelectorAll('button').forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-selected', x === b); });
        v.poster = b.dataset.poster; v.src = b.dataset.src; v.load(); v.play().catch(() => {});
        if (cap) cap.textContent = b.dataset.cap;
      }));
    });
  }

  // slide da solução: alterna entre o vídeo da carga e a vista 3D por dentro (sem esqueleto)
  function solucao() {
    const seg = document.getElementById('sol-tabs');
    if (!seg) return;
    const v = document.getElementById('video-sol');
    seg.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
      seg.querySelectorAll('button').forEach(x => {
        const on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-selected', on);
        document.getElementById(x.dataset.pane).hidden = !on;
      });
      if (v) { if (b.dataset.pane === 'sol-video') { v.currentTime = 0; v.play().catch(() => {}); } else v.pause(); }
      window.dispatchEvent(new Event('resize'));
    }));
  }

  // slide do esqueleto: COM / SEM / inferior / encaixe
  function esqueleto() {
    const seg = document.getElementById('esq-tabs');
    if (!seg) return;
    const img = document.getElementById('esq-img'), img2 = document.getElementById('esq-img2'), cap = document.getElementById('esq-cap');
    seg.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
      seg.querySelectorAll('button').forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-selected', x === b); });
      img.src = b.dataset.img; img.alt = b.dataset.alt; cap.textContent = b.dataset.cap;
      img2.hidden = !b.dataset.img2;
      if (b.dataset.img2) { img2.src = b.dataset.img2; img2.alt = b.dataset.alt + ' (sem esqueleto)'; }
      img.closest('.esq-imgs').classList.toggle('two', !!b.dataset.img2);
    }));
  }

  chartMassa(); chartPesoCarga(); chartCarga(); chartImpacto(); tables(); mapas(); galeria(); video(); videoTabs(); esqueleto(); solucao();
})();

// Animações: números contam até o valor e barras/linhas entram quando o slide abre.
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const parse = s => {
    const m = s.match(/^([^\d−-]*)([−-]?[\d.]+(?:,\d+)?)(.*)$/s);
    if (!m) return null;
    const num = parseFloat(m[2].replace('−', '-').replace(/\./g, '').replace(',', '.'));
    const dec = (m[2].split(',')[1] || '').length;
    return { pre: m[1], num, dec, suf: m[3], neg: m[2].startsWith('−') };
  };
  const fmt = (n, d) => n.toLocaleString('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
  function count(e) {
    if (!e.dataset.final) e.dataset.final = e.textContent;
    const p = parse(e.dataset.final);
    if (!p || reduce) return;
    const t0 = performance.now(), dur = 900;
    const step = now => {
      const k = Math.min(1, (now - t0) / dur), ease = 1 - Math.pow(1 - k, 3);
      const v = p.num * ease;
      e.textContent = k < 1 ? `${p.pre}${p.neg ? '−' : ''}${fmt(Math.abs(v), p.dec)}${p.suf}` : e.dataset.final;
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }
  document.addEventListener('slidechange', ev => {
    const s = ev.detail.slide;
    s.querySelectorAll('.stat b, .cnt').forEach(count);
    s.querySelectorAll('.chart').forEach(c => { c.classList.remove('play'); void c.offsetWidth; c.classList.add('play'); });
  });
})();
