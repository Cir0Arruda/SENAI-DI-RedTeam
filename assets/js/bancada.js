// Testes de Bancada: gráficos SVG com tooltip e troca de mapas do Fusion.
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const RED = '#e5232f', INDIGO = '#5b5bd6';   // paleta validada (dataviz validator: PASS)
  const fmt = (n, d = 1) => n.toLocaleString('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });

  const el = (tag, attrs = {}, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };

  function makeTip(host) {
    const tip = document.createElement('div');
    tip.className = 'tip';
    host.appendChild(tip);
    return {
      show(html, x, y) {
        tip.innerHTML = html;
        tip.classList.add('on');
        const hw = host.clientWidth, tw = tip.offsetWidth;
        tip.style.left = `${Math.min(Math.max(x + 14, 8), hw - tw - 8)}px`;
        tip.style.top = `${Math.max(y - tip.offsetHeight - 10, 8)}px`;
      },
      hide() { tip.classList.remove('on'); }
    };
  }

  // Posição do ponteiro em coordenadas do viewBox e do host
  function pointer(svg, host, ev, W) {
    const r = svg.getBoundingClientRect(), hr = host.getBoundingClientRect();
    return { vx: (ev.clientX - r.left) * (W / r.width), hx: ev.clientX - hr.left, hy: ev.clientY - hr.top };
  }

  /* ---------- Barras horizontais: deslocamento máximo ---------- */
  function barsDesl() {
    const host = document.getElementById('chart-desl');
    if (!host) return;
    const data = [
      { k: 'PA6-CF', v: 0.08, c: RED },
      { k: 'Tritan', v: 0.23, c: INDIGO }
    ];
    const W = 520, rowH = 34, gap = 14, L = 64, R = 56, H = data.length * (rowH + gap);
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Deslocamento máximo: PA6-CF 0,08 mm; Tritan 0,23 mm' }, host);
    const max = 0.25, x = v => L + (v / max) * (W - L - R);
    const tip = makeTip(host);
    data.forEach((d, i) => {
      const y = i * (rowH + gap);
      el('text', { x: 0, y: y + rowH / 2 + 4, class: 'lbl' }, svg).textContent = d.k;
      const w = x(d.v) - L;
      // barra com ponta arredondada (4px) e base reta na linha de base
      el('path', { d: `M${L},${y} h${w - 4} a4,4 0 0 1 4,4 v${rowH - 8} a4,4 0 0 1 -4,4 h${-(w - 4)} z`, fill: d.c }, svg);
      el('text', { x: x(d.v) + 8, y: y + rowH / 2 + 4, class: 'lbl' }, svg).textContent = `${fmt(d.v, 2)} mm`;
      const hit = el('rect', { x: 0, y: y - gap / 2, width: W, height: rowH + gap, fill: 'transparent' }, svg);
      hit.addEventListener('pointermove', ev => {
        const p = pointer(svg, host, ev, W);
        tip.show(`<div class="r"><i style="background:${d.c}"></i><b>${d.k}</b></div>Deslocamento máx.: ${fmt(d.v, 2)} mm`, p.hx, p.hy);
      });
      hit.addEventListener('pointerleave', () => tip.hide());
    });
    el('line', { x1: L, x2: L, y1: -4, y2: H - gap + 4, stroke: 'rgba(21,21,29,.25)' }, svg);
  }

  /* ---------- Linhas: força × tempo (impacto 1D) ---------- */
  function lineImpacto() {
    const host = document.getElementById('chart-impacto');
    const D = window.IMPACTO_1D;
    if (!host || !D) return;
    const W = 640, H = 300, L = 44, R = 16, T = 10, B = 30;
    const tMax = 6, fMax = 500;
    const x = t => L + (t / tMax) * (W - L - R);
    const y = f => T + (1 - f / fMax) * (H - T - B);
    const pts = D.filter(p => p[0] <= tMax);
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Força de contato: pico de 450,9 N sem PAD em 0,92 ms; 168,5 N com PAD em 2,45 ms' }, host);

    const grid = el('g', { class: 'grid' }, svg), axis = el('g', { class: 'axis' }, svg);
    for (let f = 0; f <= fMax; f += 100) {
      el('line', { x1: L, x2: W - R, y1: y(f), y2: y(f) }, grid);
      el('text', { x: L - 8, y: y(f) + 4, 'text-anchor': 'end' }, axis).textContent = f;
    }
    for (let t = 0; t <= tMax; t += 1) {
      el('text', { x: x(t), y: H - 10, 'text-anchor': 'middle' }, axis).textContent = `${t} ms`;
    }
    el('text', { x: L - 8, y: T - 2 + 0, 'text-anchor': 'end' }, axis);

    const path = idx => pts.map((p, i) => `${i ? 'L' : 'M'}${x(p[0]).toFixed(1)},${y(p[idx]).toFixed(1)}`).join('');
    el('path', { d: path(1), fill: 'none', stroke: INDIGO, 'stroke-width': 2, 'stroke-linejoin': 'round' }, svg);
    el('path', { d: path(2), fill: 'none', stroke: RED, 'stroke-width': 2, 'stroke-linejoin': 'round' }, svg);

    // Rótulos diretos nos picos
    const peak = idx => pts.reduce((a, p) => (p[idx] > a[idx] ? p : a));
    const pS = peak(1), pC = peak(2);
    el('text', { x: x(pS[0]) + 10, y: y(pS[1]) + 4, class: 'lbl' }, svg).textContent = `${fmt(450.9)} N`;
    el('text', { x: x(pC[0]), y: y(pC[2]) - 10, class: 'lbl', 'text-anchor': 'middle' }, svg).textContent = `${fmt(168.5)} N`;

    // Crosshair + tooltip
    const cross = el('line', { y1: T, y2: H - B, stroke: 'rgba(21,21,29,.3)', 'stroke-dasharray': '3 3', opacity: 0 }, svg);
    const dS = el('circle', { r: 4, fill: INDIGO, stroke: '#fff', 'stroke-width': 2, opacity: 0 }, svg);
    const dC = el('circle', { r: 4, fill: RED, stroke: '#fff', 'stroke-width': 2, opacity: 0 }, svg);
    const tip = makeTip(host);
    const hit = el('rect', { x: L, y: T, width: W - L - R, height: H - T - B, fill: 'transparent' }, svg);
    hit.addEventListener('pointermove', ev => {
      const p = pointer(svg, host, ev, W);
      const t = Math.max(0, Math.min(tMax, ((p.vx - L) / (W - L - R)) * tMax));
      const q = pts.reduce((a, b) => (Math.abs(b[0] - t) < Math.abs(a[0] - t) ? b : a));
      const cx = x(q[0]);
      cross.setAttribute('x1', cx); cross.setAttribute('x2', cx); cross.setAttribute('opacity', 1);
      dS.setAttribute('cx', cx); dS.setAttribute('cy', y(q[1])); dS.setAttribute('opacity', 1);
      dC.setAttribute('cx', cx); dC.setAttribute('cy', y(q[2])); dC.setAttribute('opacity', 1);
      tip.show(`<b>${fmt(q[0], 2)} ms</b>
        <div class="r"><i style="background:${INDIGO}"></i>Sem PAD: ${fmt(q[1])} N</div>
        <div class="r"><i style="background:${RED}"></i>Com PAD: ${fmt(q[2])} N</div>`, p.hx, p.hy);
    });
    hit.addEventListener('pointerleave', () => {
      [cross, dS, dC].forEach(e => e.setAttribute('opacity', 0));
      tip.hide();
    });
  }

  /* ---------- Colunas: redução por área de contato ---------- */
  function barsArea() {
    const host = document.getElementById('chart-area');
    if (!host) return;
    const data = [
      { a: 25, red: 80.3, f: 89.1, c: 2.84 },
      { a: 50, red: 72.6, f: 123.6, c: 1.97 },
      { a: 100, red: 62.6, f: 168.5, c: 1.34, base: true },
      { a: 200, red: 50.5, f: 223.2, c: 0.89 },
      { a: 400, red: 37.3, f: 282.9, c: 0.56 }
    ];
    const W = 560, H = 300, L = 40, R = 10, T = 22, B = 34;
    const y = v => T + (1 - v / 100) * (H - T - B);
    const slot = (W - L - R) / data.length, bw = Math.min(56, slot - 18);
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Redução do pico: 25 mm² 80%, 50 mm² 73%, 100 mm² 63%, 200 mm² 50%, 400 mm² 37%' }, host);
    const grid = el('g', { class: 'grid' }, svg), axis = el('g', { class: 'axis' }, svg);
    for (let v = 0; v <= 100; v += 25) {
      el('line', { x1: L, x2: W - R, y1: y(v), y2: y(v) }, grid);
      el('text', { x: L - 8, y: y(v) + 4, 'text-anchor': 'end' }, axis).textContent = `${v}%`;
    }
    const tip = makeTip(host);
    data.forEach((d, i) => {
      const cx = L + slot * i + slot / 2, x0 = cx - bw / 2, top = y(d.red), base = y(0), h = base - top;
      el('path', {
        d: `M${x0},${base} v${-(h - 4)} a4,4 0 0 1 4,-4 h${bw - 8} a4,4 0 0 1 4,4 v${h - 4} z`,
        fill: RED, opacity: d.base ? 1 : 0.55
      }, svg);
      el('text', { x: cx, y: top - 7, class: 'lbl', 'text-anchor': 'middle' }, svg).textContent = `${fmt(d.red, 0)}%`;
      el('text', { x: cx, y: H - 12, 'text-anchor': 'middle' }, axis).textContent = `${d.a} mm²`;
      const hit = el('rect', { x: cx - slot / 2, y: T, width: slot, height: H - T - B, fill: 'transparent' }, svg);
      hit.addEventListener('pointermove', ev => {
        const p = pointer(svg, host, ev, W);
        tip.show(`<b>${d.a} mm²${d.base ? ' · caso base' : ''}</b><br>Redução: ${fmt(d.red)}%<br>Pico com PAD: ${fmt(d.f)} N<br>Compressão: ${fmt(d.c, 2)} mm`, p.hx, p.hy);
      });
      hit.addEventListener('pointerleave', () => tip.hide());
    });
  }

  /* ---------- Mapas de resultado do Fusion ---------- */
  function maps() {
    const img = document.getElementById('map-img'), cap = document.getElementById('map-cap');
    const mat = document.getElementById('map-mat'), res = document.getElementById('map-res');
    if (!img) return;
    const NAME = { pa6cf: 'PA6-CF', tritan: 'Tritan' };
    const INFO = {
      pa6cf: {
        desl: 'deslocamento total: máx. 0,08 mm nas abas externas, onde a carga é aplicada',
        p1: '1ª tensão principal (tração): máx. 5,16 MPa no anel do flange',
        p3: '3ª tensão principal (compressão): mín. −4,61 MPa',
        sf: 'fator de segurança acima de 8 em toda a peça',
        vm: null
      },
      tritan: {
        desl: 'deslocamento total: máx. 0,23 mm nas abas externas, onde a carga é aplicada',
        vm: 'tensão de Von Mises: máx. 3,22 MPa no anel do flange',
        p1: '1ª tensão principal (tração): máx. 5,03 MPa no anel do flange',
        p3: '3ª tensão principal (compressão): mín. −4,49 MPa',
        sf: 'fator de segurança acima de 8 em toda a peça'
      }
    };
    let m = 'pa6cf', r = 'desl';
    const render = () => {
      let rr = r;
      // O relatório do PA6-CF não exportou o mapa de Von Mises
      if (!INFO[m][rr]) rr = 'p1';
      img.src = `assets/img/bancada/${m}_${rr}.png`;
      img.alt = `Mapa do Fusion, ${NAME[m]}: ${INFO[m][rr]}`;
      cap.textContent = `${NAME[m]} · ${INFO[m][rr]}` + (rr !== r ? ' · Von Mises não foi exportado no relatório do PA6-CF' : '');
      res.querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.v === rr));
    };
    const bind = (group, set) => group.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
      group.querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b));
      set(b.dataset.v); render();
    }));
    bind(mat, v => { m = v; });
    bind(res, v => { r = v; });
    // pré-carrega
    Object.keys(INFO).forEach(mm => Object.keys(INFO[mm]).forEach(rr => { if (INFO[mm][rr]) new Image().src = `assets/img/bancada/${mm}_${rr}.png`; }));
  }

  /* ---------- R07: carga máxima numa asa (barras agrupadas, linhas de 24 e 30 kg) ---------- */
  function barsCarga() {
    const host = document.getElementById('chart-r07-carga');
    if (!host) return;
    const S = [{ k: 'PA6-CF (Z 48 MPa)', c: RED }, { k: 'PAHT CF15 (Z 18,2 MPa)', c: INDIGO }];
    const data = [
      { k: 'R06', v: [70.7, 26.8] },
      { k: 'R07 com', v: [115.6, 43.8] },
      { k: 'R07 sem', v: [108.8, 41.2] },
      { k: 'Sem, denso', v: [110.9, 42.0] }
    ];
    const W = 560, bh = 15, inner = 3, gap = 16, L = 84, R = 52, T = 26;
    const rowH = 2 * bh + inner, H = T + data.length * (rowH + gap) + 14;
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Carga máxima numa asa: ' + data.map(d => `${d.k} ${fmt(d.v[0])} kg (PA6-CF), ${fmt(d.v[1])} kg (PAHT CF15)`).join('; ') }, host);
    const max = 130, x = v => L + (v / max) * (W - L - R);
    const tip = makeTip(host);
    // legenda
    S.forEach((s, j) => {
      const lx = L + j * 190;
      el('rect', { x: lx, y: 2, width: 10, height: 10, rx: 3, fill: s.c }, svg);
      el('text', { x: lx + 16, y: 11, class: 'lbl' }, svg).textContent = s.k;
    });
    // referências 24 / 30 kg
    [[24, '24', 'end', -3], [30, '30 kg', 'start', 3]].forEach(([v, t, a, dx]) => {
      el('line', { x1: x(v), x2: x(v), y1: T - 4, y2: H - 10, stroke: 'rgba(21,21,29,.45)', 'stroke-dasharray': '3 3' }, svg);
      el('text', { x: x(v) + dx, y: H, class: 'lbl', 'text-anchor': a, style: 'font-size:10px' }, svg).textContent = t;
    });
    data.forEach((d, i) => {
      const y0 = T + i * (rowH + gap);
      el('text', { x: 0, y: y0 + rowH / 2 + 4, class: 'lbl' }, svg).textContent = d.k;
      d.v.forEach((v, j) => {
        const y = y0 + j * (bh + inner), w = x(v) - L;
        el('path', { d: `M${L},${y} h${w - 4} a4,4 0 0 1 4,4 v${bh - 8} a4,4 0 0 1 -4,4 h${-(w - 4)} z`, fill: S[j].c }, svg);
        el('text', { x: x(v) + 6, y: y + bh - 3, class: 'lbl', style: 'font-size:11px' }, svg).textContent = `${fmt(v, 0)} kg`;
      });
      const hit = el('rect', { x: 0, y: y0 - gap / 2, width: W, height: rowH + gap, fill: 'transparent' }, svg);
      hit.addEventListener('pointermove', ev => {
        const p = pointer(svg, host, ev, W);
        tip.show(`<b>${d.k}</b>` + S.map((s, j) => `<div class="r"><i style="background:${s.c}"></i>${s.k}: ${fmt(d.v[j])} kg · FS 24 kg ${fmt(d.v[j] / 24, 2)}</div>`).join(''), p.hx, p.hy);
      });
      hit.addEventListener('pointerleave', () => tip.hide());
    });
    el('line', { x1: L, x2: L, y1: T - 4, y2: H - 10, stroke: 'rgba(21,21,29,.25)' }, svg);
  }

  barsDesl();
  // barsCarga(): substituído por r07.js (dados da garra montada)
  lineImpacto();
  barsArea();
  maps();
})();
