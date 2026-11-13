// Visualizador de referências (slide final). Lê window.REFS, gerado de dados/REFERENCIAS.md.
(() => {
  const R = window.REFS, dlg = document.getElementById('refs-dialog');
  if (!R || !dlg) return;
  const nav = dlg.querySelector('.rv-nav'), main = dlg.querySelector('.rv-main');
  const busca = dlg.querySelector('.rv-busca input'), conta = dlg.querySelector('.rv-conta');
  const norm = s => s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
  const total = R.secoes.reduce((n, s) => n + s.itens.filter(i => i.cod).length, 0);

  // monta as seções uma vez
  const navBtns = [];
  R.secoes.forEach((s, k) => {
    const sec = document.createElement('section');
    sec.className = 'rv-sec'; sec.id = `rv-sec-${k}`;
    sec.innerHTML = `<h3>${s.titulo}</h3>${s.intro ? `<div class="rv-intro">${s.intro}</div>` : ''}`;
    s.itens.forEach(it => {
      const art = document.createElement('article');
      art.className = 'rv-item' + (it.cod ? '' : ' rv-nota');
      if (it.cod) art.id = `ref-${it.cod}`;
      art.dataset.busca = it.busca;
      art.innerHTML = (it.cod ? `<header><span class="rv-cod">${it.cod === 'Equipe' ? 'Equipe' : `[${it.cod}]`}</span>${it.titulo && it.cod !== 'Equipe' ? `<h4>${it.titulo}</h4>` : ''}</header>` : '') +
        `<div class="rv-txt">${it.html}</div>`;
      sec.appendChild(art);
    });
    main.appendChild(sec);
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'rv-chip';
    b.innerHTML = `<span>${s.titulo.replace(/\s*\(.*\)$/, '')}</span><small>${s.itens.filter(i => i.cod).length}</small>`;
    b.addEventListener('click', () => { limpa(); sec.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
    nav.appendChild(b); navBtns.push([b, sec]);
  });

  function filtra() {
    const q = norm(busca.value).split(/\s+/).filter(Boolean);
    let n = 0;
    main.querySelectorAll('.rv-sec').forEach(sec => {
      let vis = 0;
      sec.querySelectorAll('.rv-item').forEach(a => {
        const ok = !q.length || q.every(w => a.dataset.busca.includes(w));
        a.hidden = !ok; if (ok) { vis++; if (!a.classList.contains('rv-nota')) n++; }
      });
      sec.hidden = !vis;
    });
    navBtns.forEach(([b, s]) => { b.disabled = s.hidden; });
    conta.textContent = q.length ? `${n} de ${total} referências` : `${total} referências`;
    dlg.querySelector('.rv-vazio').hidden = n > 0 || !q.length;
  }
  function limpa() { if (busca.value) { busca.value = ''; filtra(); } }
  busca.addEventListener('input', filtra);

  function vai(cod) {
    const el = document.getElementById(`ref-${cod}`) || document.getElementById(`ref-${cod.split(/[–-]/)[0]}`);
    if (!el) return;
    limpa();
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    el.classList.remove('rv-flash'); void el.offsetWidth; el.classList.add('rv-flash');
  }

  // destaca a seção visível no menu
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) navBtns.forEach(([b, s]) => b.classList.toggle('on', s === e.target));
  }), { root: main, rootMargin: '0px 0px -70% 0px' });
  navBtns.forEach(([, s]) => io.observe(s));

  function abre(cod) {
    if (!dlg.open) dlg.showModal();
    filtra();
    if (cod) requestAnimationFrame(() => vai(cod)); else main.scrollTop = 0;
  }
  // botões que abrem o visualizador e códigos [F1] do slide
  document.querySelectorAll('[data-refs-open]').forEach(b => b.addEventListener('click', () => abre(b.dataset.ref)));
  document.querySelectorAll('.refs-grid li > b').forEach(b => {
    const m = b.textContent.match(/^\[([A-Z]\d*(?:[–-][A-Z]?\d+)?)\]$/);
    if (!m) return;
    b.classList.add('rv-abre'); b.tabIndex = 0; b.setAttribute('role', 'button');
    b.title = 'Abrir esta referência';
    b.addEventListener('click', () => abre(m[1]));
    b.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.stopPropagation(); abre(m[1]); } });
  });

  // dentro do visualizador: [E1] pula para a referência (sem mexer no #hash dos slides)
  main.addEventListener('click', e => {
    const a = e.target.closest('a.rv-x');
    if (a) { e.preventDefault(); vai(a.dataset.ref); }
  });
  dlg.querySelector('.rv-close').addEventListener('click', () => dlg.close());
  dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
  dlg.addEventListener('keydown', e => {
    e.stopPropagation();   // setas e espaço não trocam de slide
    if (e.key === '/' && document.activeElement !== busca) { e.preventDefault(); busca.focus(); }
  });
  filtra();
})();
