// Visualizador 3D (three.js) das peças da garra. Só carrega quando o slide é aberto.
import * as THREE from 'three';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const box = document.getElementById('viewer');
const msg = document.getElementById('viewer-msg');
const tabs = document.getElementById('viewer-parts');
const info = document.getElementById('viewer-info');
const slide = box && box.closest('.slide');

let renderer, scene, camera, controls, mesh, started = false, running = false;
const cache = {};
const loader = new STLLoader();

const MATERIALS = {
  garra_superior: { color: 0xe7e5ef, roughness: 0.55, metalness: 0.05 },
  garra_inferior: { color: 0xe7e5ef, roughness: 0.55, metalness: 0.05 },
  pads: { color: 0xf07c24, roughness: 0.7, metalness: 0.0 }   // laranja da impressão em TPU
};

function init() {
  started = true;
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  box.appendChild(renderer.domElement);

  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(35, 1, 1, 10000);
  scene.add(new THREE.HemisphereLight(0xffffff, 0xb9b4d8, 1.1));
  const key = new THREE.DirectionalLight(0xffffff, 1.6);
  key.position.set(1, 1.4, 1.2);
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xffd6d6, 0.6);
  rim.position.set(-1.2, 0.4, -1);
  scene.add(rim);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 1.2;
  renderer.domElement.addEventListener('pointerdown', () => { controls.autoRotate = false; });

  new ResizeObserver(resize).observe(box);
  resize();
  show('garra_superior');
}

function resize() {
  const w = box.clientWidth, h = box.clientHeight;
  if (!w || !h) return;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}

function loop() {
  if (!running) return;
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(loop);
}

function load(name) {
  if (!cache[name]) {
    cache[name] = new Promise((res, rej) => loader.load(`assets/models/${name}.stl`, g => {
      g.computeVertexNormals();
      g.center();
      g.rotateX(-Math.PI / 2);   // STL em Z-up → cena Y-up
      g.computeBoundingSphere();
      res(g);
    }, undefined, rej));
  }
  return cache[name];
}

async function show(name) {
  msg.textContent = 'Carregando modelo…';
  msg.style.display = '';
  try {
    const geo = await load(name);
    if (mesh) scene.remove(mesh);
    mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial(MATERIALS[name]));
    scene.add(mesh);
    const r = geo.boundingSphere.radius;
    camera.near = r / 100; camera.far = r * 20; camera.updateProjectionMatrix();
    // Distância que enquadra a esfera envolvente no menor dos dois campos de visão
    const vfov = THREE.MathUtils.degToRad(camera.fov);
    const hfov = 2 * Math.atan(Math.tan(vfov / 2) * camera.aspect);
    const dist = (r * 1.08) / Math.sin(Math.min(vfov, hfov) / 2);
    camera.position.set(0.55, 0.5, 0.67).normalize().multiplyScalar(dist);
    controls.target.set(0, 0, 0);
    controls.update();
    msg.style.display = 'none';
  } catch (e) {
    msg.textContent = 'Não foi possível carregar o modelo 3D.';
    console.error(e);
  }
}

if (box && slide) {
  tabs.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
    tabs.querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b));
    info.textContent = b.dataset.info;
    if (started) show(b.dataset.part);
  }));

  const onChange = () => {
    const visible = slide.classList.contains('on');
    if (visible && !started) init();
    if (visible && !running) { running = true; loop(); }
    if (!visible) running = false;
  };
  document.addEventListener('slidechange', onChange);
  onChange();
}
