"""R06 - Gera os projetos Orca K1 Max a partir dos 3MF que JÁ fatiam (salvos pelo usuário no Orca).

Mantém intacta a malha da peça (exterior original) e todo o perfil K1 Max; troca somente os
modificadores pelas zonas internas R06 e inclui os três (amarelo 30, azul 50, rosa 70).
Depois fatia pela CLI do Orca (mesmos argumentos que funcionaram no R04) e extrai massas.
Uso (cwd qualquer): python r06_orca_patch.py [SUPERIOR INFERIOR_ESQ INFERIOR_DIR]
"""
from __future__ import annotations
import datetime, json, re, subprocess, sys, zipfile
from pathlib import Path
import numpy as np
import trimesh

DESK = Path(__file__).resolve().parents[2]
O = DESK / 'desempenho'
sys.path.insert(0, str(DESK / 'FUSION' / 'fusion_mcp_compact'))
import r04_extract_slicer as ext  # noqa: E402

ORCA = 'C:/Program Files/OrcaSlicer/orca-slicer.exe'
SRC = O / '04_Modificadores' / 'origem'
ZON = O / '04_Modificadores' / 'R06'
OUT = O / '05_Orca' / 'R06'
OUT.mkdir(parents=True, exist_ok=True)
PARTS = {'SUPERIOR': 'SUPERIOR_BASE_20.stl', 'INFERIOR_ESQ': 'INFERIOR_ESQ_BASE_20.stl',
         'INFERIOR_DIR': 'INFERIOR_DIR_BASE_20.stl'}
ZONES = [('AMARELO', 30), ('AZUL', 50), ('ROSA', 70)]


def mesh_xml(oid: int, uuid: str, m: trimesh.Trimesh) -> str:
    v = '\n'.join(f'     <vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x, y, z in m.vertices)
    t = '\n'.join(f'     <triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in m.faces)
    return (f'  <object id="{oid}" p:UUID="{uuid}" type="model">\n   <mesh>\n    <vertices>\n{v}\n    </vertices>\n'
            f'    <triangles>\n{t}\n    </triangles>\n   </mesh>\n  </object>\n')


def patch_inline(key: str, zin: zipfile.ZipFile, main: str) -> Path:
    """Formato com malhas no próprio 3dmodel.model (objetos 1..4 + objeto-pai 5)."""
    ns = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
    part = trimesh.load(SRC / PARTS[key], force='mesh')
    obj1 = re.search(r'<object id="1".*?</object>', main, re.S).group(0)
    v1 = np.array(re.findall(r'<vertex x="([-0-9.e]+)" y="([-0-9.e]+)" z="([-0-9.e]+)"', obj1), float)
    shift = part.bounds[0] - v1.min(0)                   # mundo -> frame do 3MF (só translação)
    assert np.allclose(part.bounds[1] - shift, v1.max(0), atol=0.05), 'frame divergente'
    out = main
    for oid, (color, pct) in enumerate(ZONES, start=2):
        m = trimesh.load(ZON / f'{key}_MOD_{color}_{pct}.stl', force='mesh')
        m.apply_translation(-shift)
        v = ''.join(f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}" />' for x, y, z in m.vertices)
        t = ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}" />' for a, b, c in m.faces)
        new = f'<object id="{oid}" type="model" name="MOD_{color}_{pct}_INTERNO_R06"><mesh><vertices>{v}</vertices><triangles>{t}</triangles></mesh></object>'
        out = re.sub(rf'<object id="{oid}" .*?</object>', lambda _: new, out, count=1, flags=re.S)
    cfg = zin.read('Metadata/model_settings.config').decode('utf-8')
    cfg = cfg.replace('_NAO_IMPRIMIVEL', '_INTERNO_R06').replace('R04_ESCALA_REAL', 'R06_ZONAS_INTERNAS')
    dst = OUT / f'GARRA_{key}_R06_ZONAS_INTERNAS_K1MAX.3mf'
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            n = item.filename
            data = out if n == '3D/3dmodel.model' else cfg if n == 'Metadata/model_settings.config' else zin.read(n)
            zout.writestr(n, data)
    _ = ns
    return dst


def patch(key: str) -> Path:
    src3mf = O / '05_Orca' / f'GARRA_{key}_TPMSD_K1MAX_ESCALA_REAL.3mf'
    zin = zipfile.ZipFile(src3mf)
    main = zin.read('3D/3dmodel.model').decode('utf-8')
    found = re.search(r'p:path="(/3D/Objects/[^"]+)"', main)
    if not found:
        return patch_inline(key, zin, main)
    objpath = found.group(1)
    objxml = zin.read(objpath.lstrip('/')).decode('utf-8')
    zoff = float(re.search(r'objectid="1"[^>]*transform="1 0 0 0 1 0 0 0 1 [-0-9.e]+ [-0-9.e]+ ([-0-9.e]+)"', main).group(1))

    part = trimesh.load(SRC / PARTS[key], force='mesh')
    center = part.bounds.mean(axis=0)                      # frame local = centro do bbox da peça
    # Verificação do frame: a malha original no 3MF tem o mesmo bbox centrado
    v1 = np.array([[float(x) for x in m] for m in re.findall(
        r'<vertex x="([-0-9.e]+)" y="([-0-9.e]+)" z="([-0-9.e]+)"/>', objxml.split('<object id="2"')[0])])
    assert np.allclose(v1.min(0), part.bounds[0] - center, atol=0.05), (v1.min(0), part.bounds[0] - center)

    part_obj = re.search(r'  <object id="1".*?</object>\n', objxml, re.S).group(0)
    new_objs = [part_obj]
    for i, (color, pct) in enumerate(ZONES, start=2):
        m = trimesh.load(ZON / f'{key}_MOD_{color}_{pct}.stl', force='mesh')
        m.apply_translation(-center)
        new_objs.append(mesh_xml(i, f'0001000{i - 1}-81cb-4c03-9d28-80fed5dfa1dc', m))
    head = objxml.split('  <object id="1"')[0]
    tail = objxml[objxml.rfind('</resources>'):]
    objxml_new = head + ''.join(new_objs) + ' ' + tail

    parent = len(ZONES) + 2
    comps = '\n'.join(
        f'    <component p:path="{objpath}" objectid="{i}" p:UUID="0001000{i - 1}-b206-40ff-9872-83e8017abed1" '
        f'transform="1 0 0 0 1 0 0 0 1 0 0 {zoff}"/>' for i in range(1, parent))
    main_new = re.sub(r'<object id="\d+"(.*?)<components>.*?</components>',
                      lambda mm: f'<object id="{parent}"{mm.group(1)}<components>\n{comps}\n   </components>', main, flags=re.S)
    main_new = re.sub(r'<item objectid="\d+"', f'<item objectid="{parent}"', main_new)

    cfg = zin.read('Metadata/model_settings.config').decode('utf-8')
    part1 = re.search(r'    <part id="1".*?</part>\n', cfg, re.S).group(0)
    part1 = re.sub(r'(key="matrix" value=")[^"]+', rf'\g<1>1 0 0 0 0 1 0 0 0 0 1 {zoff} 0 0 0 1', part1)
    mods = ''.join(
        f'    <part id="{i}" subtype="modifier_part">\n'
        f'      <metadata key="name" value="MOD_{c}_{p}_INTERNO_R06"/>\n'
        f'      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 {zoff} 0 0 0 1"/>\n'
        f'      <metadata key="sparse_infill_density" value="{p}%"/>\n'
        f'      <metadata key="sparse_infill_pattern" value="tpmsd"/>\n'
        f'    </part>\n' for i, (c, p) in enumerate(ZONES, start=2))
    cfg_new = re.sub(r'    <part id="1".*</part>\n', part1 + mods, cfg, flags=re.S)
    cfg_new = re.sub(r'<object id="\d+"', f'<object id="{parent}"', cfg_new, count=1)
    cfg_new = re.sub(r'(key="object_id" value=")\d+', rf'\g<1>{parent}', cfg_new)
    cfg_new = re.sub(r'(assemble_item object_id=")\d+', rf'\g<1>{parent}', cfg_new)
    cfg_new = cfg_new.replace('R04_ESCALA_REAL"', 'R06_ZONAS_INTERNAS"')

    dst = OUT / f'GARRA_{key}_R06_ZONAS_INTERNAS_K1MAX.3mf'
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            n = item.filename
            if n == '3D/3dmodel.model':
                zout.writestr(n, main_new)
            elif n == objpath.lstrip('/'):
                zout.writestr(n, objxml_new)
            elif n == 'Metadata/model_settings.config':
                zout.writestr(n, cfg_new)
            elif n == 'Metadata/project_settings.config':
                ps = json.loads(zin.read(n))
                # O Orca renomeou o preset da impressora com sufixo do projeto; sem isso a CLI recusa
                # (erro 3001 'process not compatible with printer'). Só metadado, nenhum parâmetro muda.
                if ps['printer_settings_id'] not in ps.get('print_compatible_printers', []):
                    ps['print_compatible_printers'] = ps.get('print_compatible_printers', []) + [ps['printer_settings_id']]
                zout.writestr(n, json.dumps(ps, indent=4, ensure_ascii=False))
            elif n == 'Metadata/slice_info.config' or n.endswith('.gcode') or n.endswith('.md5'):
                continue  # resultado de fatiamento antigo não vale para o R06
            else:
                zout.writestr(item, zin.read(n))
    return dst


def slice_(key: str, inp: Path) -> dict:
    folder = OUT / f'Resultado_{key}'
    folder.mkdir(exist_ok=True)
    for old in folder.glob('*'):
        if old.is_file():
            old.unlink()
    out = folder / f'{key}_R06_FATIADO.3mf'
    state = {'case': key, 'start_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'input': str(inp), 'printer': 'Creality K1 Max 300 mm, bico 0,4 mm', 'scale': 1,
             'sent_to_printer': False}
    args = [ORCA, str(inp), '--slice', '0', '--outputdir', str(folder), '--export-3mf', out.name]  # args extras do R04 quebram a CLI
    with (folder / 'Orca_fatiamento.log').open('wb') as f:
        r = subprocess.run(args, stdout=f, stderr=subprocess.STDOUT, timeout=2400, cwd=folder)
    state.update({'returncode': r.returncode, 'ok': r.returncode == 0 and out.exists(),
                  'end_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat()})
    if state['ok']:
        data = ext.extract(folder)
        state.update({'mass_g': data['category_mass_g'], 'orca_total_g': data['Orca_summary']['total_filament_mass_g'],
                      'time_s': data['Orca_summary']['prediction_s'], 'warnings': data['Orca_summary']['warnings']})
    (folder / 'status.json').write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(state, ensure_ascii=True), flush=True)
    return state


if __name__ == '__main__':
    keys = sys.argv[1:] or list(PARTS)
    res = {}
    for k in keys:
        res[k] = slice_(k, patch(k))
    (OUT / 'r06_fatiamento_resumo.json').write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
