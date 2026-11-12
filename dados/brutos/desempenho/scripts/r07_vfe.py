"""R07 - Elementos finitos por voxels (hexaedros de 8 nós) para a garra SAMI com zonas internas.

Ferramenta de PROJETO e de varredura (muitos casos de carga, com/sem esqueleto, impacto), usada
antes e ao lado do Fusion. Não substitui o Fusion: o resultado oficial de tensão vem do Fusion;
este solver serve para localizar pontos quentes, comparar variantes e alimentar fadiga/impacto.

Modelo:
  * grade fina (FINE mm) -> classifica cada célula em CASCA (paredes + topo/base), ESQUELETO
    (almas sólidas), e zonas de preenchimento giroide com densidade phi; elemento = bloco H mm.
  * rigidez do elemento = soma das frações x rigidez de cada classe (regra de mistura de Voigt).
  * PA6-CF sólido transversalmente isotrópico (plano XY de deposição x eixo Z de camadas).
  * giroide homogeneizado: E* = E_XY * phi^2 (Gibson-Ashby, flexão dominante; conservador).
  * tensão no material de cada classe = C_classe : deformação do elemento (deformação comum).
Hipóteses explícitas no JSON de saída. Unidades: mm, N, MPa.
"""
from __future__ import annotations
import json, time
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np
import scipy.sparse as sp
import pyamg
import trimesh
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / '04_Modificadores' / 'origem'
OUT = ROOT / '06_Engenharia' / 'R07'
OUT.mkdir(parents=True, exist_ok=True)

# ---- material PA6-CF (Bambu PA6-CF V3, seco; fonte: TDS do fabricante em materiais.json) ----
MAT = dict(E_xy=4430.0, E_z=2170.0, nu_p=0.35, nu_pz=0.35, S_xy=102.0, S_z=48.0, rho=1.09e-3)  # rho g/mm³
NU_INFILL = 0.30


def C_solid(m=MAT):
    Ep, Ez, nup, nupz = m['E_xy'], m['E_z'], m['nu_p'], m['nu_pz']
    nuzp = nupz * Ez / Ep
    Gzp = Ez / (2 * (1 + nupz))  # hipótese: sem G_xz medido
    S = np.zeros((6, 6))
    S[0, 0] = S[1, 1] = 1 / Ep
    S[0, 1] = S[1, 0] = -nup / Ep
    S[0, 2] = S[2, 0] = S[1, 2] = S[2, 1] = -nuzp / Ez
    S[2, 2] = 1 / Ez
    S[3, 3] = S[4, 4] = 1 / Gzp
    S[5, 5] = 2 * (1 + nup) / Ep
    return np.linalg.inv(S)


def C_iso(E, nu):
    l = E * nu / ((1 + nu) * (1 - 2 * nu)); mu = E / (2 * (1 + nu))
    C = np.zeros((6, 6)); C[:3, :3] = l; C[np.arange(3), np.arange(3)] += 2 * mu
    C[3, 3] = C[4, 4] = C[5, 5] = mu
    return C


def C_infill(phi):
    return C_iso(MAT['E_xy'] * phi ** 2, NU_INFILL)


def infill_strength(phi):
    return 0.3 * MAT['S_xy'] * phi ** 1.5  # resistência do giroide homogeneizado (hipótese G-A)


# ---- elemento hexaédrico ----
CORN = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])


def B_at(xi, h):
    s = 2 * CORN - 1
    dN = np.zeros((3, 8))
    for a in range(8):
        sx, sy, sz = s[a]
        dN[0, a] = sx * (1 + sy * xi[1]) * (1 + sz * xi[2]) / 8
        dN[1, a] = sy * (1 + sx * xi[0]) * (1 + sz * xi[2]) / 8
        dN[2, a] = sz * (1 + sx * xi[0]) * (1 + sy * xi[1]) / 8
    dN *= 2 / h
    B = np.zeros((6, 24))
    for a in range(8):
        x, y, z = dN[:, a]
        B[0, 3 * a] = x; B[1, 3 * a + 1] = y; B[2, 3 * a + 2] = z
        B[3, 3 * a + 1] = z; B[3, 3 * a + 2] = y
        B[4, 3 * a] = z; B[4, 3 * a + 2] = x
        B[5, 3 * a] = y; B[5, 3 * a + 1] = x
    return B


def Ke(C, h):
    g = 1 / np.sqrt(3); K = np.zeros((24, 24)); detJ = (h / 2) ** 3
    for i in (-g, g):
        for j in (-g, g):
            for k in (-g, g):
                B = B_at((i, j, k), h); K += B.T @ C @ B * detJ
    return K


# ---- geometria / voxels ----
@dataclass
class Design:
    name: str
    base_phi: float = 0.20
    wall_mm: float = 2.25            # 5 voltas x 0,45 mm
    web_paths: list = field(default_factory=list)   # [[(x,y),(x,y),...], ...]
    web_t: float = 0.0               # espessura da alma sólida (mm); 0 = sem esqueleto
    zones: list = field(default_factory=list)       # [(mask_fn(X,Y,Z)->bool, phi)], prioridade = ordem
    solid_zones: list = field(default_factory=list) # [mask_fn] -> 100% sólido


def seg_dist(P, a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); d = b - a
    t = np.clip(((P - a) @ d) / (d @ d), 0, 1)
    return np.linalg.norm(P - (a + t[:, None] * d), axis=1)


def polyline_mask(X, Y, paths, half):
    P = np.c_[X.ravel(), Y.ravel()]; m = np.zeros(len(P), bool)
    for path in paths:
        for a, b in zip(path[:-1], path[1:]):
            m |= seg_dist(P, a, b) <= half
    return m.reshape(X.shape)


class Model:
    def __init__(self, stl, H=3.0, FINE=0.75):
        self.stl = stl; self.H = H; self.FINE = FINE
        mesh = trimesh.load(stl, force='mesh'); self.mesh = mesh
        n = int(round(H / FINE)); self.n = n
        lo = mesh.bounds[0] - 2 * H; hi = mesh.bounds[1] + 2 * H
        shape = np.ceil((hi - lo) / H).astype(int); self.lo = lo; self.shape = shape  # elementos
        t = time.time()
        vox = mesh.voxelized(FINE).fill()
        M = vox.matrix; o = vox.transform[:3, 3]
        fine = np.zeros(shape * n, bool)
        off = np.round((o - lo) / FINE).astype(int)
        fine[off[0]:off[0] + M.shape[0], off[1]:off[1] + M.shape[1], off[2]:off[2] + M.shape[2]] = M
        self.fine = fine
        self.dist = ndimage.distance_transform_edt(fine) * FINE  # distância à superfície (dentro)
        gx = lo[0] + (np.arange(fine.shape[0]) + 0.5) * FINE
        gy = lo[1] + (np.arange(fine.shape[1]) + 0.5) * FINE
        gz = lo[2] + (np.arange(fine.shape[2]) + 0.5) * FINE
        self.g = (gx, gy, gz)
        print(f'voxel fino {fine.shape} em {time.time() - t:.1f}s, volume {fine.sum() * FINE ** 3 / 1000:.1f} cm³ (STL {mesh.volume / 1000:.1f})')

    def classify(self, d: Design):
        """Retorna rótulo por célula fina: 0 fora, 1 sólido (casca/alma/sólido), 2.. infill por phi."""
        fine = self.fine; gx, gy, gz = self.g
        lab_phi = np.full(fine.shape, -1.0, np.float32)   # -1 fora; 1.0 sólido; phi infill
        lab_phi[fine] = d.base_phi
        X2, Y2 = np.meshgrid(gx, gy, indexing='ij')
        for fn, phi in reversed(d.zones):  # menor prioridade primeiro; última escrita vence
            m = fn(X2[..., None], Y2[..., None], gz[None, None, :]) & fine
            lab_phi[m] = phi
        for fn in d.solid_zones:
            m = fn(X2[..., None], Y2[..., None], gz[None, None, :]) & fine
            lab_phi[m] = 1.0
        if d.web_t > 0 and d.web_paths:
            m2 = polyline_mask(X2, Y2, d.web_paths, d.web_t / 2)
            lab_phi[m2[..., None] & fine] = 1.0
        lab_phi[fine & (self.dist <= d.wall_mm)] = 1.0  # casca
        return lab_phi

    def mass_g(self, lab):
        v = self.FINE ** 3
        solid = (lab >= 0.999).sum() * v
        inf = lab[(lab >= 0) & (lab < 0.999)]
        return MAT['rho'] * (solid + inf.sum() * v), solid / 1000, inf.size * v / 1000

    def elements(self, lab):
        """Frações por classe em cada elemento H. Classes: phi únicos (1.0 = sólido)."""
        n = self.n; S = self.shape
        L = lab.reshape(S[0], n, S[1], n, S[2], n)
        classes = sorted({round(float(p), 4) for p in np.unique(lab) if p >= 0})
        F = np.stack([(np.isclose(L, c, atol=1e-4)).sum(axis=(1, 3, 5)) / n ** 3 for c in classes], -1)
        occ = F.sum(-1) > 0.12   # descarta elementos quase vazios
        return classes, F, occ

    def solve(self, lab, loads, fixed_fn, tag='', tol=1e-8):
        t0 = time.time(); H = self.H; S = self.shape
        classes, F, occ = self.elements(lab)
        ei = np.argwhere(occ); ne = len(ei)
        Fe = F[occ]
        Cs = [C_solid() if c >= 0.999 else C_infill(c) for c in classes]
        Kc = np.stack([Ke(C, H).ravel() for C in Cs])            # (nc, 576)
        # numeração dos nós
        nid = -np.ones(S + 1, np.int64)
        cn = (ei[:, None, :] + CORN[None]).reshape(-1, 3)
        u = np.unique(cn, axis=0); nid[u[:, 0], u[:, 1], u[:, 2]] = np.arange(len(u))
        enodes = nid[cn[:, 0], cn[:, 1], cn[:, 2]].reshape(ne, 8)
        edofs = (3 * enodes[:, :, None] + np.arange(3)).reshape(ne, 24)
        nn = len(u); ndof = 3 * nn
        rows = np.repeat(edofs, 24, axis=1).ravel(); cols = np.tile(edofs, (1, 24)).ravel()
        data = (Fe @ Kc).ravel()
        K = sp.coo_matrix((data, (rows, cols)), shape=(ndof, ndof)).tocsr(); del data, rows, cols
        X = self.lo + u * H  # coordenadas dos nós
        fixed = fixed_fn(X)
        fdofs = (3 * np.where(fixed)[0][:, None] + np.arange(3)).ravel()
        free = np.setdiff1d(np.arange(ndof), fdofs)
        Kf = K[free][:, free].tocsr()
        Bnull = np.zeros((ndof, 6))
        Bnull[0::3, 0] = 1; Bnull[1::3, 1] = 1; Bnull[2::3, 2] = 1
        c = X - X.mean(0)
        Bnull[0::3, 3] = -c[:, 1]; Bnull[1::3, 3] = c[:, 0]
        Bnull[1::3, 4] = -c[:, 2]; Bnull[2::3, 4] = c[:, 1]
        Bnull[0::3, 5] = c[:, 2]; Bnull[2::3, 5] = -c[:, 0]
        ml = pyamg.smoothed_aggregation_solver(Kf, B=Bnull[free], max_coarse=2000)
        M = ml.aspreconditioner()
        results = {}
        for name, fn in loads.items():
            f = fn(X, nn)
            res = []
            x, info = sp.linalg.cg(Kf, f[free], rtol=tol, M=M, maxiter=3000, callback=lambda xk: res.append(1))
            U = np.zeros(ndof); U[free] = x
            # reação no engaste (checagem de equilíbrio)
            R = K @ U - f
            results[name] = dict(U=U, f=f, info=info, iters=len(res), reaction=R[fdofs].reshape(-1, 3).sum(0))
        self.last = dict(classes=classes, Fe=Fe, ei=ei, enodes=enodes, edofs=edofs, X=X, nn=nn, K=K)
        print(f'[{tag}] elementos {ne}, gdl {ndof}, livres {len(free)}, tempo {time.time() - t0:.1f}s')
        return results

    def stresses(self, U):
        """Tensão no material de cada classe a partir da deformação no centróide do elemento."""
        L = self.last; B0 = B_at((0, 0, 0), self.H)
        eps = (U[L['edofs']] @ B0.T)  # (ne,6)
        out = {}
        for k, c in enumerate(L['classes']):
            C = C_solid() if c >= 0.999 else C_infill(c)
            sig = eps @ C.T
            out[c] = (sig, L['Fe'][:, k])
        return eps, out


def vm(s):
    sx, sy, sz, tyz, txz, txy = s.T
    return np.sqrt(0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2) + 3 * (tyz ** 2 + txz ** 2 + txy ** 2))


def failure_indices(sig):
    """Sólido FFF: índice no plano XY (máx. principal 2D) e entre camadas (Z, tração + cisalhamento)."""
    sx, sy, sz, tyz, txz, txy = sig.T
    c = (sx + sy) / 2; r = np.sqrt(((sx - sy) / 2) ** 2 + txy ** 2)
    p_xy = np.maximum(np.abs(c + r), np.abs(c - r))
    fi_xy = p_xy / MAT['S_xy']
    s_int = np.sqrt(np.maximum(sz, 0) ** 2 + 3 * (tyz ** 2 + txz ** 2))
    fi_z = s_int / MAT['S_z']
    return fi_xy, fi_z
