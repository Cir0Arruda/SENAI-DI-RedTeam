// Animações dos slides: contadores, parada da linha, montagem do palete, giroide, custo interativo, QR e o pandinha da capa.
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fmt = (n, d = 0) => n.toLocaleString('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
  const ease = t => 1 - Math.pow(1 - t, 3);
  const isOn = el => !!el && el.closest('.slide')?.classList.contains('on');

  /* Laço único: cada animação registra um passo que só roda com o slide visível */
  const steps = new Set();
  let last = performance.now();
  function frame(now) {
    const dt = Math.min(0.1, (now - last) / 1000); last = now;
    if (!document.hidden) steps.forEach(s => { if (s.active()) s.tick(dt, now); });
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  const onSlide = (el, fn) => document.addEventListener('slidechange', e => { if (e.detail.slide.contains(el)) fn(); });

  /* ---------- Contadores (data-count) ---------- */
  document.querySelectorAll('[data-count]').forEach(el => {
    const to = +el.dataset.count, d = +(el.dataset.d || 0);
    let t0 = null;
    const st = { active: () => t0 !== null, tick: (dt, now) => {
      const p = Math.min(1, (now - t0) / 1400);
      el.textContent = fmt(to * ease(p), d);
      if (p >= 1) t0 = null;
    } };
    steps.add(st);
    const start = () => { if (reduce) { el.textContent = fmt(to, d); return; } t0 = performance.now(); el.textContent = fmt(0, d); };
    onSlide(el, start); if (isOn(el)) start();
  });

  /* ---------- Parada da linha: relógio de 45 min, R$ 84.000 ---------- */
  const tk = document.getElementById('anim-parada');
  if (tk) {
    const clock = tk.querySelector('.t-clock'), rs = tk.querySelector('.t-rs'), bar = tk.querySelector('.t-bar i');
    let t = 0, run = false;
    const draw = p => {
      const min = 45 * p, mm = Math.floor(min), ss = Math.floor((min - mm) * 60);
      clock.textContent = `${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}`;
      rs.textContent = `R$ ${fmt(84000 * p)}`;
      bar.style.width = `${p * 100}%`;
    };
    steps.add({ active: () => run && isOn(tk), tick: dt => { t = Math.min(9, t + dt); draw(t / 9); if (t >= 9) run = false; } });
    const start = () => { t = 0; run = !reduce; draw(reduce ? 1 : 0); };
    onSlide(tk, start); if (isOn(tk)) start();
  }

  /* ---------- Linha: o robô monta paletes de 40 caixas ---------- */
  const svg = document.getElementById('anim-linha');
  if (svg) {
    const NS = 'http://www.w3.org/2000/svg';
    const mk = (tag, a, p) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); p.appendChild(e); return e; };
    // esteira: caixas que andam sem parar (recortadas na esteira)
    const belt = document.getElementById('belt-boxes');
    const clip = mk('clipPath', { id: 'clip-belt' }, svg); mk('rect', { x: 12, y: 150, width: 200, height: 80 }, clip);
    belt.setAttribute('clip-path', 'url(#clip-belt)');
    const bg = mk('g', { class: 'belt-move' }, belt);
    for (let i = -1; i < 8; i++) mk('rect', { x: 12 + i * 30, y: 212, width: 20, height: 14, rx: 2, class: 'bx' }, bg);
    // caixas carregadas pela garra (2 por vez)
    const claw = document.getElementById('robot-claw');
    const carry = mk('g', { class: 'carry' }, claw);
    mk('rect', { x: 424, y: 150, width: 18, height: 14, rx: 2, class: 'bx' }, carry);
    mk('rect', { x: 444, y: 150, width: 18, height: 14, rx: 2, class: 'bx' }, carry);
    const fore = document.getElementById('robot-fore');
    const pal = document.getElementById('pallet-boxes');
    const H = { cx: document.getElementById('hud-caixas'), pl: document.getElementById('hud-palete'), it: document.getElementById('hud-itens'), kg: document.getElementById('hud-kg') };
    const slots = [];
    for (let r = 0; r < 4; r++) for (let c = 0; c < 10; c++) slots.push({ x: 446 + c * 18, y: 234 - r * 15 });
    let total = 0, onPal = 0, palN = 1, phase = 0, hold = 0;
    const hud = () => { H.cx.textContent = fmt(total); H.pl.textContent = palN; H.it.textContent = fmt(total * 12); H.kg.textContent = fmt(total * 12); };
    const setSwing = s => fore.setAttribute('transform', `translate(322 0) scale(${s.toFixed(3)} 1) translate(-322 0)`);
    const reset = () => { total = 0; onPal = 0; palN = 1; phase = 0; hold = 0; pal.replaceChildren(); hud(); setSwing(1); carry.style.opacity = 0; };
    reset();
    steps.add({ active: () => isOn(svg) && !reduce, tick: dt => {
      if (hold > 0) { hold -= dt; if (hold <= 0 && total >= 280) reset(); return; }
      const dur = palN === 1 ? 0.45 : 0.22;              // primeiro palete devagar, depois acelera
      phase += dt / dur;
      // 0–0.5: vai até a esteira (s 1 → −1) e pega; 0.5–1: volta ao palete carregando
      const s = phase < 0.5 ? Math.cos(Math.PI * phase * 2) : -Math.cos(Math.PI * (phase - 0.5) * 2);
      setSwing(s);
      carry.style.opacity = phase >= 0.5 ? 1 : 0;
      if (phase >= 1) {
        phase = 0; carry.style.opacity = 0;
        for (let k = 0; k < 2; k++) { const p = slots[onPal++]; mk('rect', { x: p.x, y: p.y, width: 17, height: 14, rx: 2, class: 'bx drop' }, pal); }
        total += 2; hud();
        if (onPal >= 40) {
          if (total >= 280) { hold = 3.5; return; }
          hold = 0.7; onPal = 0; palN++;
          setTimeout(() => { pal.replaceChildren(); hud(); }, 650);
        }
      }
    } });
    onSlide(svg, reset);
    if (reduce) { slots.forEach(p => mk('rect', { x: p.x, y: p.y, width: 17, height: 14, rx: 2, class: 'bx' }, pal)); total = 280; palN = 7; hud(); }
  }

  /* ---------- Giroide: corte que sobe camada a camada ---------- */
  const cv = document.getElementById('anim-giroide');
  if (cv) {
    const ctx = cv.getContext('2d');
    const N = 240, img = ctx.createImageData(N, N), off = document.createElement('canvas');
    off.width = off.height = N;
    const octx = off.getContext('2d');
    const zEl = document.getElementById('giroide-z');
    let z = 0.9, thr = 0.39;                                   // |f| < 0,39 ≈ 25% do volume; 0,62 ≈ 40%
    const CELL_MM = 10, PERIODS = 2;
    const sx = new Float32Array(N), cx = new Float32Array(N);
    for (let i = 0; i < N; i++) { const a = (i / N) * PERIODS * 2 * Math.PI; sx[i] = Math.sin(a); cx[i] = Math.cos(a); }
    const draw = () => {
      const sz = Math.sin(z), cz = Math.cos(z), d = img.data;
      for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
        const f = sx[i] * cx[j] + sx[j] * cz + sz * cx[i];
        const k = (j * N + i) * 4, a = Math.abs(f);
        if (a < thr) { const e = 1 - a / thr; d[k] = 229 - 40 * e; d[k + 1] = 35 + 10 * (1 - e); d[k + 2] = 47; d[k + 3] = 255; }
        else { d[k] = 247; d[k + 1] = 245; d[k + 2] = 252; d[k + 3] = 255; }
      }
      octx.putImageData(img, 0, 0);
      ctx.imageSmoothingEnabled = true;
      ctx.drawImage(off, 0, 0, cv.width, cv.height);
      if (zEl) zEl.textContent = fmt(((z / (2 * Math.PI)) * CELL_MM) % (CELL_MM * 10), 1);
    };
    draw();
    steps.add({ active: () => isOn(cv) && !reduce, tick: dt => { z += dt * 0.9; draw(); } });
    document.querySelectorAll('#giroide-dens button').forEach(b => b.addEventListener('click', () => {
      document.querySelectorAll('#giroide-dens button').forEach(o => o.classList.toggle('on', o === b));
      thr = +b.dataset.t > 0.3 ? 0.62 : 0.39; draw();
    }));
  }

  /* ---------- Custo: começa na opção escolhida (sem esqueleto); tocar outra linha mostra a conta dela ---------- */
  const D = window.R07;
  const rows = [...document.querySelectorAll('tr.pick')];
  if (rows.length && D) {
    const V = Object.fromEntries(D.variantes.map(v => [v.k, v]));
    const padRs = D.pads.total_g / 1000 * D.precos.tpu_kg, bico = 23.5;
    const val = document.getElementById('custo-val'), rot = document.getElementById('custo-rot'),
          conta = document.getElementById('custo-conta'), par = document.getElementById('custo-paradas'),
          bar = document.getElementById('custo-bar');
    const tot = k => V[k].custo_rs + padRs + bico;
    const MAX = Math.max(...rows.map(r => tot(r.dataset.k)));
    const setBar = (g, p, b, max) => {
      const [ig, ip, ib] = bar.children;
      ig.style.width = `${g / max * 100}%`; ip.style.width = `${p / max * 100}%`; ib.style.width = `${b / max * 100}%`;
    };
    const neutral = () => {
      const a = tot('R07_SEM'), b = tot('R07_COM');
      val.textContent = `R$ ${fmt(a)} a ${fmt(b)}`;
      rot.textContent = 'garra R07 (sem ou com esqueleto) + 8 PADs + bico';
      conta.textContent = 'toque numa opção da tabela para ver a conta';
      par.textContent = `paga ${fmt(84000 / b)} a ${fmt(84000 / a)} garras completas`;
      bar.classList.add('range'); setBar((V.R07_SEM.custo_rs + V.R07_COM.custo_rs) / 2, padRs, bico, MAX);
    };
    const pick = k => {
      const v = V[k], t = tot(k);
      val.textContent = `R$ ${fmt(t, 2)}`;
      rot.textContent = `garra ${v.rot} + 8 PADs + bico`;
      conta.textContent = `${fmt(v.custo_rs, 2)} + ${fmt(padRs, 2)} + ${fmt(bico, 2)} · PADs com suportes (Orca)`;
      par.textContent = `paga ${fmt(84000 / t)} garras completas`;
      bar.classList.remove('range'); setBar(v.custo_rs, padRs, bico, MAX);
      val.classList.remove('pop'); void val.offsetWidth; val.classList.add('pop');
    };
    let cur = null;
    const choose = r => {
      cur = cur === r ? null : r;
      rows.forEach(o => { o.classList.toggle('sel', o === cur); o.setAttribute('aria-pressed', o === cur); });
      cur ? pick(cur.dataset.k) : neutral();
    };
    rows.forEach(r => {
      r.addEventListener('click', () => choose(r));
      r.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.stopPropagation(); choose(r); } });
    });
    // opção escolhida pela equipe: R07 sem esqueleto
    const sem = rows.find(r => r.dataset.k === 'R07_SEM');
    sem ? choose(sem) : neutral();
  }

  /* ---------- QR ampliado ---------- */
  const qrBtn = document.getElementById('qr-btn'), qrDlg = document.getElementById('qr-dialog');
  if (qrBtn && qrDlg) {
    qrBtn.addEventListener('click', () => qrDlg.showModal());
    document.getElementById('qr-close').addEventListener('click', () => qrDlg.close());
    qrDlg.addEventListener('click', e => { if (e.target === qrDlg) qrDlg.close(); });
  }

  /* ---------- Pandinha RedLab na capa ---------- */
  const stage = document.querySelector('.stage'), panda = document.getElementById('panda');
  if (stage && panda) {
    const walk = panda.parentElement, bubble = document.getElementById('panda-bubble');
    const legA = panda.querySelector('.p-leg-a'), legB = panda.querySelector('.p-leg-b'), armB = panda.querySelector('.p-arm-b'), svgP = panda.querySelector('.panda-svg');
    const W = () => walk.clientWidth, PW = () => panda.offsetWidth;
    // roteiro: entra pela esquerda, para perto do QR mostrando o balão, volta olhando o celular, sai e recomeça
    let x = -140, dir = 1, mode = 'walk', wait = 0, t = 0, target = 0;
    const targetRight = () => W() - PW() - (innerWidth > 640 ? 180 : 24);
    const pose = (swing) => {
      legA.setAttribute('transform', `rotate(${swing * 22} 69 120)`);
      legB.setAttribute('transform', `rotate(${-swing * 22} 51 120)`);
      armB.setAttribute('transform', `rotate(${-swing * 26} 28 82)`);
      svgP.style.transform = `translateY(${-Math.abs(swing) * 3}px)`;
    };
    const place = () => { panda.style.transform = `translateX(${x}px) scaleX(${dir})`; bubble.style.transform = `scaleX(${dir})`; };
    const restart = () => { x = -140; dir = 1; mode = 'walk'; target = targetRight(); bubble.classList.remove('on'); place(); };
    restart();
    if (reduce) { x = Math.max(16, targetRight()); place(); bubble.classList.add('on'); pose(0); }
    steps.add({ active: () => stage.classList.contains('is-cover') && !reduce, tick: dt => {
      t += dt;
      if (mode === 'wait') {
        pose(0); wait -= dt;
        if (wait <= 0) { bubble.classList.remove('on'); mode = 'walk'; dir = -dir; target = dir > 0 ? targetRight() : -160; }
        place(); return;
      }
      const speed = W() < 640 ? 46 : 78;
      x += dir * speed * dt;
      pose(Math.sin(t * 9));
      if ((dir > 0 && x >= target) || (dir < 0 && x <= target)) {
        x = target;
        if (dir > 0) { mode = 'wait'; wait = 5; bubble.classList.add('on'); }
        else { restart(); }
      }
      place();
    } });
    addEventListener('resize', () => { if (dir > 0) target = targetRight(); });
    document.addEventListener('slidechange', e => { if (e.detail.index === 0 && !reduce) restart(); });
  }
})();
