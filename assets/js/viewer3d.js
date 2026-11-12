// Visualizadores 3D (three.js) das peças da garra. Cada caixa [data-viewer3d] carrega só quando o slide é aberto.
// Modos: peça sólida (STL) ou peça translúcida + zonas internas do Orca (modificadores R07) com corte por altura.
import * as THREE from 'three';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const loader = new STLLoader();
const raw = {};   // geometria crua (sem centralizar), compartilhada entre visualizadores
const loadRaw = name => (raw[name] ||= new Promise((res, rej) =>
  loader.load(`assets/models/${name}.stl`, g => res(g), undefined, rej)));

// Cores = mesmas legendas do G-code/Orca nos slides
const C = { shell: 0xe7e5ef, pad: 0xf07c24, solido: 0x1e6fb8, colar: 0x7b3fe4, rosa: 0xf03cf0, amarelo: 0xf5c400, pes: 0xff8ad8 };
const PARTS = {
  garra_superior: { shell: 'garra_superior' },
  garra_inferior: { shell: 'garra_inferior' },
  pads: { shell: 'pads', color: C.pad },
  r07_sup_com: { shell: 'garra_superior', zones: [['r07/sup_solido', C.solido], ['r07/sup_colar', C.colar], ['r07/sup_rosa', C.rosa], ['r07/sup_amarelo', C.amarelo]] },
  r07_sup_sem: { shell: 'garra_superior', zones: [['r07/sup_sem_solido', C.solido], ['r07/sup_sem_colar', C.colar], ['r07/sup_sem_rosa', C.rosa], ['r07/sup_sem_amarelo', C.amarelo]] },
  r07_inf: { shell: 'garra_inferior', zones: [['r07/inf_solido', C.solido], ['r07/inf_rosa', C.rosa], ['r07/inf_pes', C.pes], ['r07/inf_amarelo', C.amarelo]] },
  // garra superior + 8 metades de PAD na posição de montagem (animação de encaixe)
  encaixe: { shell: 'garra_superior', pads: ['A1', 'A2', 'A3', 'A4'].flatMap(a => [`pads_montados/${a}_L`, `pads_montados/${a}_R`]) }
};

function makeViewer(box) {
  const slide = box.closest('.slide');
  const tabs = document.getElementById(box.dataset.tabs);
  const info = document.getElementById(box.dataset.info);
  const cut = document.getElementById(box.dataset.cut);
  const msg = box.querySelector('.vmsg');
  let renderer, scene, camera, controls, group, started = false, running = false, token = 0;
  const plane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 1e6);

  function init() {
    started = true;
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.localClippingEnabled = true;
    box.appendChild(renderer.domElement);
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(35, 1, 1, 10000);
    scene.add(new THREE.HemisphereLight(0xffffff, 0xb9b4d8, 1.1));
    const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(1, 1.4, 1.2); scene.add(key);
    const rim = new THREE.DirectionalLight(0xffd6d6, 0.6); rim.position.set(-1.2, 0.4, -1); scene.add(rim);
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; controls.autoRotate = true; controls.autoRotateSpeed = 1.2;
    renderer.domElement.addEventListener('pointerdown', () => { controls.autoRotate = false; });
    new ResizeObserver(resize).observe(box);
    resize();
    const first = tabs && (tabs.querySelector('button.on') || tabs.querySelector('button'));
    show(first ? first.dataset.part : box.dataset.part);
  }

  function resize() {
    const w = box.clientWidth, h = box.clientHeight;
    if (!w || !h || !renderer) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
  }

  function loop() {
    if (!running) return;
    if (group && group.userData.anim) group.userData.anim(performance.now() / 1000);
    controls.update(); renderer.render(scene, camera);
    requestAnimationFrame(loop);
  }

  function setCut() {
    if (!group || !cut) return;
    const bb = group.userData.bb, f = +cut.value / 100;
    plane.constant = bb.min.y + (bb.max.y - bb.min.y) * f + 0.01;   // mostra tudo abaixo da altura escolhida
    const out = document.getElementById(cut.dataset.out);
    if (out) out.textContent = f >= 1 ? 'peça inteira' : `corte a ${Math.round((bb.max.y - bb.min.y) * f)} mm da base`;
  }

  // Cada PAD (par de metades) gira em torno do próprio ressalto e desce até encaixar; as metades se fecham.
  function addPads(g, padGeos, c) {
    const items = [];
    for (let i = 0; i < padGeos.length; i += 2) {
      const pair = padGeos.slice(i, i + 2).map(src => {
        const geo = src.clone(); geo.translate(-c.x, -c.y, -c.z); geo.rotateX(-Math.PI / 2); geo.computeVertexNormals();
        geo.computeBoundingBox(); return geo;
      });
      const bb = new THREE.Box3(); pair.forEach(geo => bb.union(geo.boundingBox));
      const ctr = bb.getCenter(new THREE.Vector3());
      const pivot = new THREE.Group(); pivot.position.copy(ctr);
      const halves = pair.map(geo => {
        geo.translate(-ctr.x, -ctr.y, -ctr.z);
        const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: C.pad, roughness: 0.5, metalness: 0.02, side: THREE.DoubleSide }));
        const hc = geo.boundingBox.clone().translate(new THREE.Vector3(-ctr.x, -ctr.y, -ctr.z)).getCenter(new THREE.Vector3());
        m.userData.dir = new THREE.Vector3(hc.x, 0, hc.z).normalize();
        pivot.add(m); return m;
      });
      g.add(pivot); items.push({ pivot, home: ctr.clone(), halves, delay: (i / 2) * 0.35 });
    }
    const ease = t => t < 0 ? 0 : t > 1 ? 1 : 1 - Math.pow(1 - t, 3);
    g.userData.anim = t => {
      const T = 7, u = t % T;
      items.forEach(it => {
        // 0–1,6 s: girando no alto · 1,6–3,4 s: desce e fecha · 3,4–6,4 s: montado · 6,4–7 s: sobe de novo
        const p = u < 6.4 ? ease((u - 1.6 - it.delay) / 1.8) : 1 - ease((u - 6.4) / 0.6);
        const lift = (1 - p) * 80, open = (1 - p) * 26;
        it.pivot.position.set(it.home.x, it.home.y + lift, it.home.z);
        it.pivot.rotation.y = (1 - p) * (t * 1.6 + it.delay * 3);
        it.halves.forEach(h => h.position.copy(h.userData.dir).multiplyScalar(open));
      });
    };
  }

  async function show(name) {
    const def = PARTS[name], my = ++token;
    msg.textContent = 'Carregando modelo…'; msg.style.display = '';
    try {
      const names = [def.shell, ...(def.zones || []).map(z => z[0]), ...(def.pads || [])];
      const geos = await Promise.all(names.map(loadRaw));
      if (my !== token) return;
      const shellGeo = geos[0];
      shellGeo.computeBoundingBox();
      const c = shellGeo.boundingBox.getCenter(new THREE.Vector3());
      const g = new THREE.Group();
      const nz = (def.zones || []).length;
      geos.forEach((src, i) => {
        if (i > nz) return;            // PADs posicionados: tratados abaixo
        const geo = src.clone();
        geo.translate(-c.x, -c.y, -c.z);
        geo.rotateX(-Math.PI / 2);     // STL em Z-up → cena Y-up
        geo.computeVertexNormals();
        const zone = i > 0, hasZones = !!def.zones;
        const mat = new THREE.MeshStandardMaterial({
          color: zone ? def.zones[i - 1][1] : (def.color || C.shell),
          roughness: zone ? 0.45 : 0.55, metalness: 0.05,
          transparent: hasZones && !zone, opacity: hasZones && !zone ? 0.18 : 1,
          depthWrite: !(hasZones && !zone), side: THREE.DoubleSide,
          clippingPlanes: hasZones ? [plane] : []
        });
        const mesh = new THREE.Mesh(geo, mat);
        if (hasZones && !zone) mesh.renderOrder = 2;
        g.add(mesh);
      });
      if (def.pads) addPads(g, geos.slice(1 + nz), c);
      if (group) { scene.remove(group); group.traverse(o => { if (o.isMesh) { o.geometry.dispose(); o.material.dispose(); } }); }
      group = g; scene.add(group);
      if (group.userData.anim) group.userData.anim(1e-3 + 5);   // mede já montado
      group.userData.bb = new THREE.Box3().setFromObject(group);
      if (def.pads) group.userData.bb.max.y += 80;                    // espaço para os PADs subirem
      if (cut) { cut.closest('.cutrow').hidden = !def.zones; setCut(); }
      const sph = group.userData.bb.getBoundingSphere(new THREE.Sphere());
      const r = sph.radius;
      camera.near = r / 100; camera.far = r * 20; camera.updateProjectionMatrix();
      const vfov = THREE.MathUtils.degToRad(camera.fov);
      const hfov = 2 * Math.atan(Math.tan(vfov / 2) * camera.aspect);
      const dist = (r * 1.08) / Math.sin(Math.min(vfov, hfov) / 2);
      camera.position.set(0.55, 0.62, 0.67).normalize().multiplyScalar(dist);
      controls.target.set(0, 0, 0); controls.update();
      msg.style.display = 'none';
    } catch (e) {
      msg.textContent = 'Não foi possível carregar o modelo 3D.';
      console.error(e);
    }
  }

  if (tabs) tabs.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
    tabs.querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b));
    if (info) info.textContent = b.dataset.info || '';
    if (started) show(b.dataset.part);
  }));
  if (cut) cut.addEventListener('input', setCut);

  const onChange = () => {
    const visible = slide.classList.contains('on');
    if (visible && !started) init();
    if (visible && !running) { running = true; loop(); }
    if (!visible) running = false;
  };
  document.addEventListener('slidechange', onChange);
  onChange();
}

document.querySelectorAll('[data-viewer3d]').forEach(makeViewer);
