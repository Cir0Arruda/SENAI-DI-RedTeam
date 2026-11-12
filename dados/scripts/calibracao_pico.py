"""Calibração do fator de pico: FE por voxels (peça superior maciça, isotrópica) x Fusion [F1].
Fusion [F1]: von Mises 3,232 MPa; 1ª principal 5,163 MPa; deslocamento 0,080 mm (355,36 N nas 4 interfaces).
Só lê arquivos; não grava nada na pasta de trabalho."""
import sys, json
import numpy as np
sys.path.insert(0, sys.argv[1])
import r07_vfe as v
import r07_validar as val

H = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
m = v.Model(v.SRC / 'SUPERIOR_BASE_20.stl', H=H, FINE=H / 4)
zmin = m.mesh.bounds[0, 2]
v.C_solid = lambda mat=v.MAT: v.C_iso(4430.0, 0.39)
lab = m.classify(v.Design('MACICO', base_phi=1.0))
print('massa maciça (g)', round(m.mass_g(lab)[0], 1), '| volume STL cm3', round(m.mesh.volume / 1000, 1))
res = m.solve(lab, {'SYM': val.load_fn(list(val.BOSSES), 355.3596, H, zmin)}, val.fixed_fn_factory(m, H), tag='calib')
r = res['SYM']; U = r['U']
eps, st = m.stresses(U)
sig, frac = st[1.0]
has = frac > 0.05
VM = v.vm(sig[has])
P1 = np.array([np.linalg.eigvalsh(np.array([[s[0], s[5], s[4]], [s[5], s[1], s[3]], [s[4], s[3], s[2]]])).max() for s in sig[has]])
disp = np.linalg.norm(U.reshape(-1, 3), axis=1)
F = dict(vm=3.232, p1=5.163, d=0.080)
out = dict(H=H, reacao_N=r['reaction'].round(2).tolist(), desl_max_mm=round(float(disp.max()), 4),
           vm_max=round(float(VM.max()), 3), p1_max=round(float(P1.max()), 3),
           vm_p999=round(float(np.percentile(VM, 99.9)), 3), p1_p999=round(float(np.percentile(P1, 99.9)), 3))
out['fator_vm'] = round(F['vm'] / out['vm_max'], 2)
out['fator_p1'] = round(F['p1'] / out['p1_max'], 2)
out['razao_desl_fusion_voxel'] = round(F['d'] / out['desl_max_mm'], 2)
print(json.dumps(out, ensure_ascii=False))
