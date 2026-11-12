# -*- coding: utf-8 -*-
"""
Galeria comparativa R07 (garra SAMI, UR30).

Lê apenas arquivos de resultado já existentes (fatiamento Orca, FE por voxels,
impacto transiente, vida) e gera figuras PNG + INDEX.md + dados_comparativos.csv
em 06_Engenharia/R07/GALERIA/.  Não roda fatiador nem solver.

Re-executável: entradas ausentes são puladas e listadas no final.

Uso:
  "<venv>/Scripts/python.exe" scripts/r07_galeria.py
"""
import csv
import glob
import json
import os
import sys
from collections import OrderedDict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.image as mpimg  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORCA = os.path.join(R, "05_Orca")
ENG = os.path.join(R, "06_Engenharia", "R07")
MONT = os.path.join(ENG, "MONTAGEM")
IMP = os.path.join(ENG, "IMPACTO")
OUT = os.path.join(ENG, "GALERIA")
os.makedirs(OUT, exist_ok=True)

DPI = 150
INK = "#222222"
MUTED = "#555555"
GRID = "#DDDDDD"

# ---------------------------------------------------------------- constantes
# (fornecidas no pedido / no deck do cliente; rótulos das chaves dos JSON)
RHO_PA6CF = 1.10        # g/cm3, densidade usada no fatiamento Orca
RHO_TRITAN = 1.18       # g/cm3
GARRA_ATUAL_KG = 2.834  # garra completa montada (CAD, deck do cliente)
GARRA_2CX_KG = 26.834   # garra + 2 caixas (deck do cliente)
CAIXAS_KG = GARRA_2CX_KG - GARRA_ATUAL_KG
PAYLOAD_UR30 = 30.0
UTS_Z_PA6 = 48.0        # MPa (chave "..._Z48")
UTS_Z_PAHT = 18.2       # MPa (chave "..._Z18.2")

# ---------------------------------------------------------------- variantes
# cor fixa por variante em TODAS as figuras
VAR = OrderedDict([
    ("TRITAN_ATUAL", dict(rot="Atual: Tritan Hexa3D 30%", cor="#FFFFFF", borda="#000000")),
    ("HEXA3D30", dict(rot="Hexa3D 30% (PA6-CF)", cor="#9C7CC4")),
    ("R06", dict(rot="R06 (zonas internas)", cor="#E07B1F")),
    ("R07_COM", dict(rot="R07 com esqueleto", cor="#1F5BB5")),
    ("R07_SEM", dict(rot="R07 sem esqueleto", cor="#8DB4E2")),
    ("R07_SEM_ISO", dict(rot="R07 sem esqueleto, giroide + denso", cor="#3C9AA6")),
    ("UNI_15", dict(rot="Giroide 15% uniforme", cor="#CFCFCF")),
    ("UNI_30", dict(rot="Giroide 30% uniforme", cor="#A8A8A8")),
    ("UNI_35", dict(rot="Giroide 35% uniforme", cor="#767676")),
    ("UNI_40", dict(rot="Giroide 40% uniforme", cor="#3F3F3F")),
    ("TPMSD40", dict(rot="TPMS-D 40% uniforme", cor="#5E9E5E")),
])
for _k, _v in VAR.items():
    _v.setdefault("borda", _v["cor"])

FE_ORDEM = ["R06", "R07_COM", "R07_SEM", "UNI_30", "UNI_35", "UNI_40"]

# mapeamentos para os nomes dos arquivos
MAP_SUP = {"R06": "R06", "R07_COM": "F25_COM", "R07_SEM": "F25_SEM",
           "R07_SEM_ISO": "F25_SEM_ISO", "UNI_30": "UNI_30", "UNI_35": "UNI_35", "UNI_40": "UNI_40"}
MAP_INF = {"R06": "INF_R06", "R07_COM": "INF_F20_COM", "R07_SEM": "INF_F20_SEM",
           "UNI_30": "INF_UNI_30", "UNI_35": "INF_UNI_35", "UNI_40": "INF_UNI_40"}
MAP_IMP = {"R06": "R06", "R07_COM": "F25_COM", "R07_SEM": "F25_SEM", "R07_SEM_ISO": "F25_SEM_ISO",
           "UNI_30": "UNI_30", "UNI_35": "UNI_35", "UNI_40": "UNI_40"}
MAP_VIDA = {"R06 (atual)": "R06", "R07 COM esqueleto": "R07_COM",
            "R07 SEM esqueleto (mesmos %)": "R07_SEM",
            "R07 SEM esqueleto, giroide mais denso (mesma massa)": "R07_SEM_ISO"}

PULADOS = []
CRIADOS = []


def pular(msg):
    PULADOS.append(msg)
    print("  [pulado] " + msg)


def ler_json(path):
    if not os.path.isfile(path):
        pular("arquivo ausente: " + os.path.relpath(path, R))
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:  # noqa: BLE001
        pular("falha ao ler %s (%s)" % (os.path.relpath(path, R), e))
        return None


def br(v, nd=1):
    """Formata número no padrão brasileiro (1.234,5)."""
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return "n/d"
    s = "{:,.{nd}f}".format(v, nd=nd)
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def pct(v, nd=1):
    return ("+" if v > 0 else "") + br(v, nd) + "%"


def rodape(fig, txt):
    import textwrap
    larg = int(fig.get_figwidth() * 17)
    linhas_ = []
    for par in txt.split("\n"):
        linhas_.extend(textwrap.wrap(par, larg) or [""])
    fig.text(0.01, 0.008, "\n".join(linhas_), fontsize=7.5, color=MUTED, ha="left", va="bottom")


def salvar(fig, nome, desc):
    p = os.path.join(OUT, nome)
    fig.savefig(p, dpi=DPI, facecolor="white")
    plt.close(fig)
    CRIADOS.append((nome, desc))
    print("  [ok] " + nome)


def eixo_br(ax, qual="x", nd=0):
    from matplotlib.ticker import FuncFormatter
    fm = FuncFormatter(lambda x, _p: br(x, nd))
    (ax.xaxis if qual == "x" else ax.yaxis).set_major_formatter(fm)


def rot_quebra(v):
    return (VAR[v]["rot"].replace(" (", "\n(").replace(" uniforme", "\nuniforme")
            .replace(" esqueleto", "\nesqueleto").replace(", giroide", ",\ngiroide"))


def ref_dir(ax, y, txt, color=INK):
    """Rótulo de linha de referência fora do eixo, à direita (não colide com barras)."""
    import matplotlib.transforms as mtr
    tr = mtr.blended_transform_factory(ax.transAxes, ax.transData)
    ax.text(1.005, y, txt, transform=tr, ha="left", va="center", fontsize=8.5, color=color, clip_on=False)


def estilo(ax, eixo="x"):
    ax.grid(axis=eixo, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=INK, labelsize=9)


plt.rcParams.update({"font.size": 10, "text.color": INK, "axes.labelcolor": INK,
                     "axes.titlecolor": INK, "axes.edgecolor": "#888888"})

# ================================================================ 1. MASSAS
print("== Lendo fatiamentos")
comp = ler_json(os.path.join(ORCA, "R07", "COMPARATIVO", "r07_comparativo_fatiamento.json")) or {}
b25 = ler_json(os.path.join(ORCA, "R07", "r07_fatiamento_base25.json")) or {}
b20 = ler_json(os.path.join(ORCA, "R07", "r07_fatiamento_base20.json")) or {}
r06f = ler_json(os.path.join(ORCA, "R06", "r06_fatiamento_resumo.json")) or {}


def peca(src, key, nome):
    e = src.get(key)
    if not e or not e.get("ok") or "mass_g" not in e:
        return None
    return dict(fonte=nome + ":" + key, peca=float(e["mass_g"]["peca"]),
                total=float(e.get("orca_total_g") or np.nan), tempo=float(e.get("time_s") or np.nan))


def garra(var, sup, ie, idr):
    if sup is None or ie is None:
        falta = [n for n, x in (("superior", sup), ("inferior esq.", ie)) if x is None]
        pular("massa da garra %s: fatiamento ausente/sem ok para %s" % (var, " e ".join(falta)))
        return None
    espelho = idr is None
    if espelho:
        idr = dict(ie)
    return dict(sup=sup["peca"], ie=ie["peca"], idr=idr["peca"], espelho=espelho,
                garra_g=sup["peca"] + ie["peca"] + idr["peca"],
                total_orca_g=sup["total"] + ie["total"] + idr["total"],
                tempo_h=(sup["tempo"] + ie["tempo"] + idr["tempo"]) / 3600.0,
                fontes="; ".join([sup["fonte"], ie["fonte"], idr["fonte"] + (" (espelho)" if espelho else "")]))


C = "COMPARATIVO"
MASSA = OrderedDict()
cands = {
    "R06": (peca(r06f, "SUPERIOR", "R06"), peca(r06f, "INFERIOR_ESQ", "R06"), peca(r06f, "INFERIOR_DIR", "R06")),
    "R07_COM": (peca(b25, "SUPERIOR", "base25"), peca(b20, "INFERIOR_ESQ", "base20"), peca(b20, "INFERIOR_DIR", "base20")),
    "R07_SEM": (peca(comp, "R07_SEM_SUPERIOR", C), peca(b20, "INFERIOR_ESQ", "base20"), peca(b20, "INFERIOR_DIR", "base20")),
}
for var, tag in [("UNI_15", "UNI_GIROIDE15"), ("UNI_30", "UNI_GIROIDE30"), ("UNI_35", "UNI_GIROIDE35"),
                 ("UNI_40", "UNI_GIROIDE40"), ("HEXA3D30", "UNI_HONEYCOMB3D30"), ("TPMSD40", "UNI_TPMSD40")]:
    cands[var] = (peca(comp, tag + "_SUPERIOR", C), peca(comp, tag + "_INFERIOR_ESQ", C),
                  peca(comp, tag + "_INFERIOR_DIR", C))
for var in VAR:
    if var in cands:
        g = garra(var, *cands[var])
        if g:
            MASSA[var] = g

if "HEXA3D30" in MASSA:
    h = MASSA["HEXA3D30"]
    f = RHO_TRITAN / RHO_PA6CF
    MASSA["TRITAN_ATUAL"] = dict(sup=h["sup"] * f, ie=h["ie"] * f, idr=h["idr"] * f, espelho=h["espelho"],
                                 garra_g=h["garra_g"] * f, total_orca_g=np.nan, tempo_h=np.nan,
                                 fontes="Hexa3D30 x 1,18/1,10")
else:
    pular("referência Tritan Hexa3D 30%: sem fatiamento UNI_HONEYCOMB3D30")

M_TRI = MASSA.get("TRITAN_ATUAL", {}).get("garra_g")
for var, m in MASSA.items():
    m["pct_vs_tritan"] = (m["garra_g"] / M_TRI - 1) * 100 if M_TRI else np.nan
    m["garra_completa_kg"] = GARRA_ATUAL_KG + ((m["garra_g"] - M_TRI) / 1000.0 if M_TRI else np.nan)
    m["garra_2cx_kg"] = m["garra_completa_kg"] + CAIXAS_KG
    m["pct_payload"] = m["garra_2cx_kg"] / PAYLOAD_UR30 * 100

# ================================================================ 2. FE
print("== Lendo FE")
MON = OrderedDict()
for v in FE_ORDEM:
    d = ler_json(os.path.join(MONT, "montagem_%s.json" % v))
    if d:
        MON[v] = d
SUP = {}
for v, n in MAP_SUP.items():
    d = ler_json(os.path.join(ENG, n + ".json"))
    if d:
        SUP[v] = d
INF = {}
for v, n in MAP_INF.items():
    d = ler_json(os.path.join(ENG, n + ".json"))
    if d:
        INF[v] = d

PICO = None
for d in MON.values():
    if "PICO" in d:
        PICO = float(d["PICO"])
        break
VIDA = ler_json(os.path.join(ENG, "r07_vida.json"))
if PICO is None and VIDA:
    PICO = float(VIDA.get("PICO_fator_Fusion_voxel", np.nan))
if PICO is None:
    PICO = 2.2
    print("  [aviso] fator de pico não encontrado nos JSON; usando 2,2")

print("== Lendo impacto")
IMPD = OrderedDict()
FRAMES = OrderedDict()
for v, n in MAP_IMP.items():
    p = os.path.join(IMP, "impacto_%s.json" % n)
    if os.path.isfile(p):
        d = ler_json(p)
        if d:
            IMPD[v] = d
    else:
        pular("impacto ainda não disponível: IMPACTO/impacto_%s.json" % n)
    p = os.path.join(IMP, "frames_%s.npz" % n)
    if os.path.isfile(p):
        try:
            FRAMES[v] = dict(np.load(p, allow_pickle=False))
        except Exception as e:  # noqa: BLE001
            pular("frames_%s.npz ilegível (%s)" % (n, e))
    else:
        pular("frames ainda não disponíveis: IMPACTO/frames_%s.npz" % n)
conhecidos = set(MAP_IMP.values())
for p in glob.glob(os.path.join(IMP, "impacto_*.json")):
    n = os.path.basename(p)[8:-5]
    if n not in conhecidos:
        pular("impacto_%s.json existe mas não tem variante mapeada (ignorado)" % n)

VIDA_V = OrderedDict()
if VIDA:
    for k, d in VIDA.get("variantes", {}).items():
        if k in MAP_VIDA:
            VIDA_V[MAP_VIDA[k]] = d
        else:
            pular("r07_vida.json: variante '%s' sem mapeamento (ignorada)" % k)

FONTE_ORCA = "Fonte: fatiamento real OrcaSlicer, Creality K1 Max, escala 1:1, PA6-CF 1,10 g/cm³ (massa da peça, sem suportes). " \
             "Tritan = Hexa3D 30% × 1,18/1,10."
FONTE_MON = "Fonte: FE por voxels da garra montada (superior + inferior dir.), engaste nos furos da flange, carga nas 4 bases " \
            "de ventosa de uma asa. Estimativa; fator de pico %s." % br(PICO, 1)


def rot(v):
    return VAR[v]["rot"]


def cor(v):
    return VAR[v]["cor"]


def borda(v):
    return VAR[v]["borda"]


# ================================================================ FIG 01
print("== Figuras")
if MASSA:
    ordem = sorted(MASSA, key=lambda v: MASSA[v]["garra_g"])
    fig, ax = plt.subplots(figsize=(10, 0.55 * len(ordem) + 1.8))
    y = np.arange(len(ordem))
    vals = [MASSA[v]["garra_g"] for v in ordem]
    for i, v in enumerate(ordem):
        lw = 1.6 if v == "TRITAN_ATUAL" else 0.6
        ax.barh(i, MASSA[v]["garra_g"], color=cor(v), edgecolor=borda(v) if v != "TRITAN_ATUAL" else "#000000",
                lw=lw, height=0.66, hatch="//" if v == "TRITAN_ATUAL" else None)
        txt = br(MASSA[v]["garra_g"], 0) + " g"
        if M_TRI and v != "TRITAN_ATUAL":
            txt += "  (" + pct(MASSA[v]["pct_vs_tritan"]) + ")"
        elif v == "TRITAN_ATUAL":
            txt += "  (referência)"
        ax.text(MASSA[v]["garra_g"] + max(vals) * 0.01, i, txt, va="center", fontsize=9, color=INK, zorder=4,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.0, alpha=0.9))
    if M_TRI:
        ax.axvline(M_TRI, color="#000000", ls="--", lw=1.1, zorder=1)
        ax.text(M_TRI - max(vals) * 0.008, len(ordem) - 0.45, "atual (Tritan) %s g" % br(M_TRI, 0), ha="right",
                va="bottom", fontsize=8.5, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels([rot(v) for v in ordem])
    ax.set_xlim(0, max(vals) * 1.22)
    ax.set_ylim(-0.6, len(ordem) - 0.05)
    eixo_br(ax, "x")
    ax.set_xlabel("Massa impressa da garra: superior + 2 inferiores (g)")
    estilo(ax, "x")
    fig.suptitle("Massa impressa da garra por variante (vs. atual Tritan Hexa3D 30%)", fontsize=12.5, x=0.01, ha="left")
    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    esp = [rot(v) for v in ordem if MASSA[v]["espelho"] and v != "TRITAN_ATUAL"]
    nota = FONTE_ORCA
    if esp:
        nota += "\nInferior dir. = espelho do inferior esq. (mesma massa) em: " + ", ".join(esp) + "."
    rodape(fig, nota)
    salvar(fig, "01_massa_garra.png", "Massa impressa da garra (superior + 2 inferiores) por variante, com a garra atual em Tritan Hexa3D 30% como referência e a variação percentual.")
else:
    pular("01_massa_garra.png: nenhuma massa disponível")

# ================================================================ FIG 02
if MASSA and M_TRI:
    ordem = sorted(MASSA, key=lambda v: MASSA[v]["garra_g"])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 0.5 * len(ordem) + 2.2), sharey=True,
                                 gridspec_kw=dict(width_ratios=[1, 1.35]))
    y = np.arange(len(ordem))
    gk = [MASSA[v]["garra_completa_kg"] for v in ordem]
    for i, v in enumerate(ordem):
        tri = v == "TRITAN_ATUAL"
        a1.barh(i, MASSA[v]["garra_completa_kg"], color=cor(v), edgecolor="#000000" if tri else borda(v),
                lw=1.6 if tri else 0.6, hatch="//" if tri else None, height=0.66)
        a1.text(MASSA[v]["garra_completa_kg"] + 0.03, i, br(MASSA[v]["garra_completa_kg"], 3) + " kg",
                va="center", fontsize=9)
        a2.barh(i, MASSA[v]["garra_completa_kg"], color=cor(v), edgecolor="#000000" if tri else borda(v),
                lw=1.6 if tri else 0.6, hatch="//" if tri else None, height=0.66)
        a2.barh(i, CAIXAS_KG, left=MASSA[v]["garra_completa_kg"], color="#EDEDED", edgecolor="#BBBBBB",
                lw=0.6, height=0.66)
        a2.text(PAYLOAD_UR30 + 0.4, i, "%s kg  (%s%% do payload)" % (br(MASSA[v]["garra_2cx_kg"], 2),
                                                                         br(MASSA[v]["pct_payload"], 1)),
                va="center", fontsize=9)
    a1.set_xlim(0, max(gk) * 1.35)
    a1.set_yticks(y)
    a1.set_yticklabels([rot(v) for v in ordem])
    a1.set_xlabel("Garra completa montada (kg)")
    a1.set_title("Garra completa (CAD + ventosas + fixadores)", fontsize=10.5, loc="left")
    a2.axvline(PAYLOAD_UR30, color="#000000", lw=1.4)
    a2.text(PAYLOAD_UR30 + 0.4, len(ordem) - 0.45, "payload UR30 = %s kg" % br(PAYLOAD_UR30, 0), ha="left",
            va="bottom", fontsize=8.5)
    a2.set_xlim(0, PAYLOAD_UR30 * 1.6)
    eixo_br(a1, "x", 1)
    a2.set_ylim(-0.6, len(ordem) + 0.05)
    a1.set_ylim(-0.6, len(ordem) + 0.05)
    a2.set_xlabel("Garra completa + 2 caixas (kg)")
    a2.set_title("Garra + 2 caixas (%s kg) vs. payload do UR30" % br(CAIXAS_KG, 0), fontsize=10.5, loc="left")
    a2.legend(handles=[Patch(facecolor="#EDEDED", edgecolor="#BBBBBB", label="2 caixas (%s kg)" % br(CAIXAS_KG, 0))],
              loc="upper left", bbox_to_anchor=(0.0, -0.13), fontsize=8.5, frameon=False)
    estilo(a1, "x")
    estilo(a2, "x")
    fig.suptitle("Massa da garra completa e uso do payload do UR30", fontsize=12.5, x=0.01, ha="left")
    fig.tight_layout(rect=[0, 0.06, 1, 0.95])
    rodape(fig, "Garra atual = %s kg (CAD, deck do cliente; com 2 caixas = %s kg). Nova garra = %s kg + (massa impressa nova − "
                "massa impressa Tritan)/1000.\n" % (br(GARRA_ATUAL_KG, 3), br(GARRA_2CX_KG, 3), br(GARRA_ATUAL_KG, 3))
           + "Massas impressas: fatiamento OrcaSlicer K1 Max 1:1; Tritan = Hexa3D 30% × 1,18/1,10.")
    salvar(fig, "02_garra_completa_payload.png", "Massa da garra completa montada e da garra com 2 caixas, em kg e em % do payload de 30 kg do UR30.")
else:
    pular("02_garra_completa_payload.png: falta massa ou referência Tritan")

# ================================================================ FIG 03
if MON:
    vs = [v for v in FE_ORDEM if v in MON]
    fig, ax = plt.subplots(figsize=(11, 5.6))
    x = np.arange(len(vs))
    w = 0.38
    top = 0
    for i, v in enumerate(vs):
        a = MON[v]["kg_max_PA6-CF_Z48"]
        b = MON[v]["kg_max_PAHT_CF15_Z18.2"]
        top = max(top, a, b)
        ax.bar(i - w / 2, a, w, color=cor(v), edgecolor=INK, lw=0.6)
        ax.bar(i + w / 2, b, w, color="white", edgecolor=cor(v) if v != "UNI_30" else "#7A7A7A", lw=1.4, hatch="///")
        ax.text(i - w / 2, a + top * 0.012 if top else a, br(a, 1), ha="center", va="bottom", fontsize=8.5)
        ax.text(i + w / 2, b + 1, br(b, 1), ha="center", va="bottom", fontsize=8.5)
    for k, ls in ((24, "--"), (30, "--")):
        ax.axhline(k, color=INK, ls=ls, lw=1.0)
        ref_dir(ax, k, "%d kg" % k)
    ax.set_xticks(x)
    ax.set_xticklabels([rot_quebra(v) for v in vs], fontsize=9)
    ax.set_ylabel("Carga máxima numa asa (kg)")
    ax.set_xlim(-0.6, len(vs) - 0.4)
    ax.set_ylim(0, top * 1.12)
    estilo(ax, "y")
    ax.legend(handles=[Patch(facecolor="#888888", edgecolor=INK, label="PA6-CF (Z = %s MPa)" % br(UTS_Z_PA6, 0)),
                       Patch(facecolor="white", edgecolor="#555555", hatch="///",
                             label="PAHT CF15 (Z = %s MPa)" % br(UTS_Z_PAHT, 1))],
              loc="upper right", fontsize=9, frameon=False)
    fig.suptitle("Carga máxima estática numa asa: garra montada", fontsize=12.5, x=0.01, ha="left")
    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    rodape(fig, FONTE_MON + " Falha por tração entre camadas (Z).")
    salvar(fig, "03_carga_maxima_montagem.png", "Carga máxima numa asa da garra montada (kg) por variante, para PA6-CF e PAHT CF15, com referências de 24 e 30 kg.")
else:
    pular("03_carga_maxima_montagem.png: nenhum montagem_*.json")

# ================================================================ FIG 04
if MON:
    vs = [v for v in FE_ORDEM if v in MON]
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.6), sharey=True)
    w = 0.38
    top = max(max(MON[v]["FS_24kg_PA6-CF_Z48"], MON[v]["FS_24kg_PAHT_CF15_Z18.2"]) for v in vs)
    for ax, (mat, k24, k30) in zip(axs, [("PA6-CF (Z = %s MPa)" % br(UTS_Z_PA6, 0), "FS_24kg_PA6-CF_Z48", "FS_30kg_PA6-CF_Z48"),
                                         ("PAHT CF15 (Z = %s MPa)" % br(UTS_Z_PAHT, 1), "FS_24kg_PAHT_CF15_Z18.2",
                                          "FS_30kg_PAHT_CF15_Z18.2")]):
        for i, v in enumerate(vs):
            a, b = MON[v][k24], MON[v][k30]
            ax.bar(i - w / 2, a, w, color=cor(v), edgecolor=INK, lw=0.6)
            ax.bar(i + w / 2, b, w, color="white", edgecolor=cor(v) if v != "UNI_30" else "#7A7A7A", lw=1.4, hatch="///")
            ax.text(i - w / 2, a + top * 0.012, br(a, 2), ha="center", va="bottom", fontsize=8)
            ax.text(i + w / 2, b + top * 0.012, br(b, 2), ha="center", va="bottom", fontsize=8)
        ax.axhline(1, color="#B22222", lw=1.2)
        ax.axhline(2, color=INK, lw=1.0, ls="--")
        ref_dir(ax, 1, "FS = 1\n(ruptura)", "#B22222")
        ref_dir(ax, 2, "FS = 2")
        ax.set_xticks(np.arange(len(vs)))
        ax.set_xticklabels([rot_quebra(v) for v in vs], fontsize=8.5)
        ax.set_title(mat, fontsize=11, loc="left")
        ax.set_xlim(-0.6, len(vs) - 0.4)
        estilo(ax, "y")
    axs[0].set_ylim(0, top * 1.12)
    axs[0].set_ylabel("Fator de segurança (–)")
    axs[1].legend(handles=[Patch(facecolor="#888888", edgecolor=INK, label="24 kg numa asa"),
                           Patch(facecolor="white", edgecolor="#555555", hatch="///", label="30 kg numa asa")],
                  loc="upper right", fontsize=9, frameon=False)
    fig.suptitle("Fator de segurança da garra montada a 24 kg e 30 kg numa asa", fontsize=12.5, x=0.01, ha="left")
    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    rodape(fig, FONTE_MON)
    salvar(fig, "04_fs_24_30.png", "Fatores de segurança da garra montada com 24 e 30 kg numa asa, em PA6-CF e PAHT CF15, com linhas em FS = 1 e FS = 2.")

# ================================================================ FIG 05
pts = []
for v in VAR:
    if v in MASSA and v in MON:
        pts.append((v, MASSA[v]["garra_g"], MON[v]["kg_max_PA6-CF_Z48"], False))
if "HEXA3D30" in MASSA and "UNI_30" in MON:
    pts.append(("HEXA3D30", MASSA["HEXA3D30"]["garra_g"], MON["UNI_30"]["kg_max_PA6-CF_Z48"], True))
if pts:
    fig, ax = plt.subplots(figsize=(10.5, 6.4))
    for v, x_, y_, proxy in pts:
        ax.scatter(x_, y_, s=130, color="white" if proxy else cor(v), edgecolor=cor(v) if proxy else INK,
                   lw=2.0 if proxy else 0.8, zorder=3, marker="D" if proxy else "o")
    # rótulos com deslocamentos simples para evitar sobreposição
    lab = sorted(pts, key=lambda p: p[2])
    for j, (v, x_, y_, proxy) in enumerate(lab):
        t = rot(v) + "\n%s g · %s kg" % (br(x_, 0), br(y_, 1))
        if proxy:
            t = rot(v) + "\n%s g · %s kg*" % (br(x_, 0), br(y_, 1))
        off = {"R06": (12, -26), "R07_SEM": (12, -26), "UNI_30": (12, 6), "HEXA3D30": (-12, 6)}.get(v, (12, -6))
        ha = "right" if off[0] < 0 else "left"
        ax.annotate(t, (x_, y_), xytext=off, textcoords="offset points", fontsize=8.5, ha=ha, va="bottom", color=INK)
    if M_TRI:
        ax.axvline(M_TRI, color="#000000", ls="--", lw=1.1)
        ax.text(M_TRI, 4, " massa atual\n Tritan Hexa3D 30%%\n (%s g)" % br(M_TRI, 0), fontsize=8.5, ha="left",
                va="bottom")
    ax.axhline(24, color=MUTED, ls=":", lw=1)
    ax.axhline(30, color=MUTED, ls=":", lw=1)
    xs = [p[1] for p in pts] + ([M_TRI] if M_TRI else [])
    ax.set_xlim(min(xs) - 60, max(xs) + 160)
    ax.text(ax.get_xlim()[0], 24, " 24 kg", fontsize=8, va="bottom", color=MUTED)
    ax.text(ax.get_xlim()[0], 30, " 30 kg", fontsize=8, va="bottom", color=MUTED)
    eixo_br(ax, "x")
    ax.set_ylim(0, max(p[2] for p in pts) * 1.18)
    ax.set_xlabel("Massa impressa da garra (g)  ← mais leve")
    ax.set_ylabel("Carga máxima numa asa, PA6-CF (kg)  ↑ mais forte")
    estilo(ax, "both")
    fig.suptitle("Compromisso massa × resistência (garra montada, PA6-CF)", fontsize=12.5, x=0.01, ha="left")
    fig.tight_layout(rect=[0, 0.08, 1, 0.95])
    rodape(fig, "Massa: fatiamento OrcaSlicer K1 Max 1:1 (PA6-CF). Resistência: FE por voxels da garra montada (superior + "
                "inferior dir.), carga nas 4 ventosas de uma asa; estimativa, fator de pico %s." % br(PICO, 1) +
           "\n* Hexa3D 30% sem FE próprio: usa a resistência do giroide 30% uniforme (mesma lei homogeneizada Gibson-Ashby).")
    salvar(fig, "05_massa_x_resistencia.png", "Gráfico de compromisso: massa impressa da garra (x) contra carga máxima numa asa em PA6-CF (y), por variante.")
else:
    pular("05_massa_x_resistencia.png: sem pares massa/FE")

# ================================================================ FIG 06
if MON:
    vs = [v for v in FE_ORDEM if v in MON]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 0.55 * len(vs) + 2.4), sharey=True)
    y = np.arange(len(vs))
    d = [MON[v]["casos"]["ONE_24"]["desl_max_mm"] for v in vs]
    k = [MON[v]["rigidez_asa_montada_N_mm"] for v in vs]
    for i, v in enumerate(vs):
        a1.barh(i, d[i], color=cor(v), edgecolor=INK, lw=0.6, height=0.66)
        a1.text(d[i] + max(d) * 0.015, i, br(d[i], 2) + " mm", va="center", fontsize=9)
        a2.barh(i, k[i], color=cor(v), edgecolor=INK, lw=0.6, height=0.66)
        a2.text(k[i] + max(k) * 0.015, i, br(k[i], 1) + " N/mm", va="center", fontsize=9)
    a1.set_yticks(y)
    a1.set_yticklabels([rot(v) for v in vs])
    a1.set_xlim(0, max(d) * 1.25)
    a2.set_xlim(0, max(k) * 1.28)
    eixo_br(a1, "x", 1)
    a1.set_xlabel("Deslocamento máximo com 24 kg numa asa (mm)  ← menor é melhor")
    a2.set_xlabel("Rigidez da asa montada (N/mm)  → maior é melhor")
    a1.set_title("Deflexão a 24 kg", fontsize=11, loc="left")
    a2.set_title("Rigidez da asa", fontsize=11, loc="left")
    estilo(a1, "x")
    estilo(a2, "x")
    fig.suptitle("Deflexão e rigidez da asa: garra montada", fontsize=12.5, x=0.01, ha="left")
    fig.tight_layout(rect=[0, 0.05, 1, 0.94])
    rodape(fig, FONTE_MON)
    salvar(fig, "06_rigidez_deslocamento.png", "Deslocamento máximo da asa com 24 kg (mm) e rigidez da asa montada (N/mm) por variante.")


# ================================================================ FIG 07 / 08 (mosaicos)
def mosaico(itens, ncol, nome, titulo, nota, desc, fw, fh):
    ok = [(v, p) for v, p in itens if os.path.isfile(p)]
    for v, p in itens:
        if not os.path.isfile(p):
            pular("%s: imagem ausente %s" % (nome, os.path.relpath(p, R)))
    if not ok:
        pular(nome + ": nenhuma imagem")
        return
    nrow = int(np.ceil(len(ok) / ncol))
    fig, axs = plt.subplots(nrow, ncol, figsize=(fw * ncol, fh * nrow + 1.0), squeeze=False)
    for ax in axs.flat:
        ax.axis("off")
    for ax, (v, p) in zip(axs.flat, ok):
        ax.imshow(mpimg.imread(p), interpolation="lanczos")
        ax.set_title(rot(v), fontsize=13, loc="left", color=INK, pad=10)
        ax.add_patch(plt.Rectangle((0, 1.0), 1, 0.012, transform=ax.transAxes, color=cor(v), clip_on=False))
    fig.suptitle(titulo, fontsize=15, x=0.01, ha="left")
    fig.tight_layout(rect=[0, 0.03, 1, 0.965])
    rodape(fig, nota)
    salvar(fig, nome, desc)


ordem_m = ["R06", "R07_COM", "R07_SEM", "UNI_30", "UNI_40", "UNI_35"]
mosaico([(v, os.path.join(MONT, "mapa_montagem_%s.png" % v)) for v in ordem_m], 2,
        "07_mapas_montagem_lado_a_lado.png",
        "Mapas de índice de falha da garra montada, 24 kg numa asa (planta XY e vista lateral YZ)",
        "Imagens originais de 06_Engenharia/R07/MONTAGEM/mapa_montagem_<V>.png (FE por voxels, sem fator de pico). "
        "ATENÇÃO: cada mapa tem sua própria escala de cor; compare os valores da barra de cor, não só as cores.",
        "Mosaico dos mapas de índice de falha da garra montada (24 kg numa asa) para R06, R07 com/sem esqueleto e giroide uniforme 30/40/35%.",
        8.4, 3.7)
ordem_s = ["R07_COM", "R07_SEM", "UNI_30", "UNI_40", "R06"]
mosaico([(v, os.path.join(ENG, "mapa_%s_ONE_24.png" % MAP_SUP[v])) for v in ordem_s], 3,
        "08_mapas_superior_lado_a_lado.png",
        "Mapas de índice de falha da peça superior isolada, 24 kg numa asa",
        "Imagens originais de 06_Engenharia/R07/mapa_<V>_ONE_24.png (FE por voxels da peça superior, sem fator de pico). "
        "Cada mapa tem sua própria escala de cor.",
        "Mosaico dos mapas de índice de falha da peça superior isolada (24 kg numa asa) para R07 com/sem esqueleto, giroide 30/40% e R06.",
        5.2, 4.7)

# ================================================================ FIG 09
FONTE_IMP = ("Fonte: FE transiente por voxels (Newmark) da peça superior, tranco de 24 kg aplicado em %s ms numa asa, massa da "
             "carga acoplada. Estimativa; σZ = FI_z × %s MPa × fator de pico %s.")
if IMPD:
    tr = next(iter(IMPD.values())).get("TR_ms", np.nan)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 8.2), sharex=True)
    for v, d in IMPD.items():
        h = d["hist"]
        t = np.asarray(h["t_ms"], float)
        sz = np.asarray(h["FI_z"], float) * UTS_Z_PA6 * PICO
        ip = int(np.argmax(sz))
        fg = np.asarray(h["FI_giroide"], float)
        ig = int(np.argmax(fg))
        a1.plot(t, sz, color=cor(v), lw=2.0,
                label="%s: pico %s MPa em %s ms" % (rot(v), br(sz[ip], 1), br(t[ip], 1)))
        a2.plot(t, fg, color=cor(v), lw=2.0)
        a1.plot(t[ip], sz[ip], "o", color=cor(v), mec=INK, ms=6, zorder=4)
        a2.plot(t[ig], fg[ig], "o", color=cor(v), mec=INK, ms=6, zorder=4)
    a1.axhline(UTS_Z_PAHT, color="#B22222", lw=1.3, ls="--")
    a1.text(40, UTS_Z_PAHT, "PAHT CF15: resistência Z = %s MPa" % br(UTS_Z_PAHT, 1), ha="center", va="bottom",
            fontsize=8.5, color=INK)
    eixo_br(a2, "y", 2)
    for a in (a1, a2):
        if np.isfinite(tr):
            a.axvspan(0, tr, color="#F2F2F2", zorder=0)
        estilo(a, "both")
    if np.isfinite(tr):
        a1.text(tr / 2, 0.5, "subida da\ncarga", ha="center", va="bottom", fontsize=8, color=MUTED)
    a1.set_ylim(0, max(UTS_Z_PAHT * 1.25, a1.get_ylim()[1]))
    a1.set_ylabel("σZ de pico entre camadas (MPa)")
    a1.set_title("Tensão de tração entre camadas (Z) no ponto crítico", fontsize=11, loc="left")
    a2.set_ylabel("Índice de falha máximo do giroide (–)")
    a2.set_xlabel("Tempo (ms)")
    a2.set_title("Quanto o preenchimento (giroide) é solicitado", fontsize=11, loc="left")
    a2.set_ylim(bottom=0)
    fig.suptitle("Resposta ao impacto: tranco de 24 kg numa asa (peça superior)", fontsize=12.5, x=0.01, ha="left")
    nleg = len(IMPD)
    fig.tight_layout(rect=[0, 0.04, 1, 0.955 - 0.022 * int(np.ceil(nleg / 2))])
    fig.legend(*a1.get_legend_handles_labels(), loc="upper left", bbox_to_anchor=(0.06, 0.955), ncol=2,
               fontsize=9, frameon=False)
    rodape(fig, FONTE_IMP % (br(tr, 0), br(UTS_Z_PA6, 0), br(PICO, 1)))
    salvar(fig, "09_impacto_curvas.png", "Histórico no tempo da tensão Z de pico e do índice de falha do giroide durante o tranco de 24 kg, por variante disponível.")
else:
    pular("09_impacto_curvas.png: nenhum impacto_*.json")

# ================================================================ FIG 10
if IMPD:
    vs = list(IMPD)
    fig, axs = plt.subplots(1, 3, figsize=(14, 5.2), gridspec_kw=dict(width_ratios=[1, 1, 1.5]))
    x = np.arange(len(vs))
    lbl = [rot_quebra(v) for v in vs]
    sp = [IMPD[v]["sigma_Z_pico_MPa_(x PICO)"] for v in vs]
    fd = [IMPD[v]["fator_dinamico_3D"] for v in vs]
    f1 = [IMPD[v]["FS_dinamico_PA6CF_Z48"] for v in vs]
    f2 = [IMPD[v]["FS_dinamico_PAHT_Z18.2"] for v in vs]
    for i, v in enumerate(vs):
        axs[0].bar(i, sp[i], 0.6, color=cor(v), edgecolor=INK, lw=0.6)
        axs[0].text(i, sp[i] * 1.01, br(sp[i], 1), ha="center", va="bottom", fontsize=9)
        axs[1].bar(i, fd[i], 0.6, color=cor(v), edgecolor=INK, lw=0.6)
        axs[1].text(i, fd[i] * 1.01, br(fd[i], 2), ha="center", va="bottom", fontsize=9)
        axs[2].bar(i - 0.2, f1[i], 0.38, color=cor(v), edgecolor=INK, lw=0.6)
        axs[2].bar(i + 0.2, f2[i], 0.38, color="white", edgecolor=cor(v) if v != "UNI_30" else "#7A7A7A", lw=1.4,
                   hatch="///")
        axs[2].text(i - 0.2, f1[i] * 1.01, br(f1[i], 2), ha="center", va="bottom", fontsize=8.5)
        axs[2].text(i + 0.2, f2[i] * 1.01, br(f2[i], 2), ha="center", va="bottom", fontsize=8.5)
    axs[0].axhline(UTS_Z_PAHT, color="#B22222", ls="--", lw=1.2)
    ref_dir(axs[0], UTS_Z_PAHT, "Z PAHT\n%s" % br(UTS_Z_PAHT, 1), "#B22222")
    axs[0].set_ylim(0, max(max(sp), UTS_Z_PAHT) * 1.2)
    axs[0].set_ylabel("MPa")
    axs[0].set_title("σZ de pico dinâmico", fontsize=11, loc="left")
    axs[1].set_ylim(0, max(fd) * 1.25)
    axs[1].set_ylabel("pico dinâmico / estático (–)")
    axs[1].set_title("Fator dinâmico", fontsize=11, loc="left")
    axs[2].axhline(1, color="#B22222", lw=1.2)
    axs[2].axhline(2, color=INK, lw=1.0, ls="--")
    ref_dir(axs[2], 1, "FS = 1", "#B22222")
    ref_dir(axs[2], 2, "FS = 2")
    axs[2].set_ylim(0, max(max(f1), 2) * 1.2)
    axs[2].set_ylabel("Fator de segurança dinâmico (–)")
    eixo_br(axs[0], "y", 0)
    eixo_br(axs[1], "y", 2)
    eixo_br(axs[2], "y", 1)
    axs[2].set_title("FS dinâmico por material", fontsize=11, loc="left")
    axs[2].legend(handles=[Patch(facecolor="#888888", edgecolor=INK, label="PA6-CF (Z %s MPa)" % br(UTS_Z_PA6, 0)),
                           Patch(facecolor="white", edgecolor="#555555", hatch="///",
                                 label="PAHT CF15 (Z %s MPa)" % br(UTS_Z_PAHT, 1))],
                  loc="upper right", fontsize=8.5, frameon=False)
    for a in axs:
        a.set_xticks(x)
        a.set_xticklabels(lbl, fontsize=8.5)
        a.set_xlim(-0.6, len(vs) - 0.4)
        estilo(a, "y")
    fig.suptitle("Resumo do impacto (tranco de 24 kg numa asa, peça superior)", fontsize=12.5, x=0.01, ha="left")
    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    tr = IMPD[vs[0]].get("TR_ms", np.nan)
    rodape(fig, FONTE_IMP % (br(tr, 0), br(UTS_Z_PA6, 0), br(PICO, 1)))
    salvar(fig, "10_impacto_resumo.png", "Tensão Z de pico dinâmica, fator dinâmico e fator de segurança dinâmico (PA6-CF e PAHT CF15) por variante de impacto disponível.")

# ================================================================ FIG 11
if FRAMES:
    AMP = 25.0
    vs = list(FRAMES)
    vmax = max(float(np.nanmax(FRAMES[v]["fi"])) for v in vs)
    n = len(vs)
    fig, axs = plt.subplots(1, n, figsize=(6.2 * n + 0.8, 4.6), squeeze=False)
    axs = axs[0]
    sc = None
    for ax, v in zip(axs, vs):
        F = FRAMES[v]
        s, z, fi = F["s"], F["z"], F["fi"]
        kf = int(np.argmax(np.nanmax(fi, axis=1)))
        su = s + AMP * F["us"][kf]
        zu = z + AMP * F["uz"][kf]
        ax.scatter(s, z, s=6, marker="s", color="#E6E6E6", lw=0, zorder=1)
        ax.set_aspect("equal")
        pad = 8
        ax.set_xlim(min(s.min(), su.min()) - pad, max(s.max(), su.max()) + pad)
        ax.set_ylim(min(z.min(), zu.min()) - pad, max(z.max(), zu.max()) + pad)
        ax.set_title("%s\nquadro de FI máximo: t = %s ms (FI máx = %s)" % (rot(v), br(float(F["t"][kf]), 1),
                                                                          br(float(fi[kf].max()), 3)),
                     fontsize=10, loc="left")
        ax.set_xlabel("s ao longo da seção (mm)")
        ax.set_ylabel("z (mm)")
        ax.tick_params(labelsize=8.5)
        ax._snap = (su, zu, fi[kf], s, z)
    fig.tight_layout(rect=[0, 0.07, 0.93, 0.92])
    fig.canvas.draw()
    for ax in axs:
        su, zu, fv, s, z = ax._snap
        # tamanho do marcador = passo da grade em pontos (para os quadrados se tocarem)
        ds = np.median(np.diff(np.unique(np.round(s, 2))))
        dz = np.median(np.diff(np.unique(np.round(z, 2))))
        passo = max(ds, dz)
        ppmm = ax.transData.transform([(0, 0), (1, 0)])
        px = abs(ppmm[1, 0] - ppmm[0, 0]) * passo
        ms = (px * 72.0 / fig.dpi) ** 2
        ax.collections[0].set_sizes([ms])
        o = np.argsort(fv)
        sc = ax.scatter(su[o], zu[o], c=fv[o], s=ms, marker="s", cmap="inferno", vmin=0, vmax=vmax, lw=0, zorder=2)
    cax = fig.add_axes([0.945, 0.15, 0.012, 0.65])
    cb = fig.colorbar(sc, cax=cax)
    cb.set_label("Índice de falha (voxel, sem fator de pico)", fontsize=9)
    cb.ax.tick_params(labelsize=8)
    eixo_br(cb.ax, "y", 2)
    fig.suptitle("Impacto: seção crítica no instante de índice de falha máximo (deslocamento ampliado ×%s)" % br(AMP, 0),
                 fontsize=12.5, x=0.01, ha="left")
    rodape(fig, "Fonte: IMPACTO/frames_<V>.npz (FE transiente por voxels da peça superior, tranco de 24 kg numa asa). Cinza = "
                "geometria indeformada. Mesma escala de cor (0 a %s) em todos os painéis." % br(vmax, 3))
    salvar(fig, "11_impacto_snapshot_pico.png", "Seção crítica da peça superior no quadro de índice de falha máximo do impacto, colorida pelo índice de falha, deslocamento ampliado 25×, mesma escala de cor.")
else:
    pular("11_impacto_snapshot_pico.png: nenhum frames_*.npz")

# ================================================================ FIG 12
MAT_VIDA = [("PA6-CF valor usado no FE (Z=48 MPa)", "PA6-CF (Z = 48 MPa)"),
            ("PAHT CF15 (TDS, Z=18,2 MPa)", "PAHT CF15 (Z = 18,2 MPa)")]
if VIDA_V:
    vs = [v for v in VAR if v in VIDA_V]
    ok = all(m in VIDA_V[v].get("materiais", {}) and "fadiga" in VIDA_V[v]["materiais"][m] for v in vs for m, _ in MAT_VIDA)
    if not ok:
        pular("12_fadiga.png: r07_vida.json sem os campos de fadiga esperados")
    else:
        fig, axs = plt.subplots(1, 2, figsize=(13.5, 5.6), sharey=True)
        x = np.arange(len(vs))
        w = 0.38
        vals_all = []
        for ax, (chave, tit) in zip(axs, [("horas_so_24kg", "Só erros de 24 kg numa asa (480 ciclos/h)"),
                                          ("horas_mix_1pct_erro", "Uso misto: 1% dos ciclos com erro de 24 kg")]):
            for i, v in enumerate(vs):
                for j, (m, mrot) in enumerate(MAT_VIDA):
                    hv = float(VIDA_V[v]["materiais"][m]["fadiga"][chave])
                    vals_all.append(hv)
                    xx = i + (-w / 2 if j == 0 else w / 2)
                    if hv > 0:
                        if j == 0:
                            ax.bar(xx, hv, w, color=cor(v), edgecolor=INK, lw=0.6)
                        else:
                            ax.bar(xx, hv, w, color="white", edgecolor=cor(v), lw=1.4, hatch="///")
                    ax.text(xx, max(hv, 0.6) * 1.15, br(hv, 0) + " h" if hv >= 1 else "< 1 h", ha="center",
                            va="bottom", fontsize=8, rotation=0, zorder=4,
                            bbox=dict(facecolor="white", edgecolor="none", pad=0.6, alpha=0.85))
            ax.set_yscale("log")
            ax.set_title(tit, fontsize=10.5, loc="left")
            ax.set_xticks(x)
            ax.set_xticklabels([rot(v).replace(" esqueleto", "\nesqueleto").replace(", giroide", ",\ngiroide")
                                .replace(" (", "\n(") for v in vs], fontsize=8.5)
            ax.axhline(8760, color=MUTED, ls=":", lw=1)
            ref_dir(ax, 8760, "1 ano\n24/7", MUTED)
            estilo(ax, "y")
        axs[0].set_ylim(0.5, max(vals_all) * 20)
        axs[0].set_ylabel("Vida estimada até a falha por fadiga (h, escala log)")
        axs[1].legend(handles=[Patch(facecolor="#888888", edgecolor=INK, label="PA6-CF (Z = 48 MPa)"),
                               Patch(facecolor="white", edgecolor="#555555", hatch="///",
                                     label="PAHT CF15 (Z = 18,2 MPa)")],
                      loc="upper left", fontsize=8.5, frameon=False)
        fig.suptitle("Vida em fadiga estimada (peça superior)", fontsize=12.5, x=0.01, ha="left")
        fig.tight_layout(rect=[0, 0.09, 1, 0.95])
        hip = "; ".join(VIDA.get("HIPOTESES", [])[:3])
        rodape(fig, "Fonte: 06_Engenharia/R07/r07_vida.json (modelo anterior da peça superior isolada, NÃO da garra montada). "
                    "Hipóteses: " + hip + ".\nS-N normalizada conservadora; valores são ordens de grandeza, não ensaiados. "
                    "'1 ano 24/7' = 8.760 h (referência visual).")
        salvar(fig, "12_fadiga.png", "Vida estimada em fadiga (horas, escala log) por variante e material, para só erros de 24 kg e para uso misto com 1% de erros.")
else:
    pular("12_fadiga.png: r07_vida.json ausente ou sem variantes")

# ================================================================ CSV
linhas = []
for v in VAR:
    r = OrderedDict(variante=v, rotulo=rot(v), cor=cor(v))
    m = MASSA.get(v)
    if m:
        r.update(massa_sup_g=round(m["sup"], 2), massa_inf_esq_g=round(m["ie"], 2), massa_inf_dir_g=round(m["idr"], 2),
                 inf_dir_espelho=m["espelho"], massa_garra_impressa_g=round(m["garra_g"], 2),
                 filamento_orca_total_g=round(m["total_orca_g"], 2) if np.isfinite(m["total_orca_g"]) else "",
                 tempo_impressao_total_h=round(m["tempo_h"], 2) if np.isfinite(m["tempo_h"]) else "",
                 pct_vs_tritan_hexa3d30=round(m["pct_vs_tritan"], 2) if np.isfinite(m["pct_vs_tritan"]) else "",
                 garra_completa_kg=round(m["garra_completa_kg"], 4) if np.isfinite(m["garra_completa_kg"]) else "",
                 garra_mais_2caixas_kg=round(m["garra_2cx_kg"], 4) if np.isfinite(m["garra_2cx_kg"]) else "",
                 pct_payload_UR30=round(m["pct_payload"], 2) if np.isfinite(m["pct_payload"]) else "",
                 fontes_massa=m["fontes"])
    fe_src = v if v in MON else ("UNI_30" if v == "HEXA3D30" and "UNI_30" in MON else None)
    if fe_src:
        d = MON[fe_src]
        r["FE_montagem_fonte"] = "montagem_%s.json" % fe_src + (" (proxy: mesma lei homogeneizada)" if fe_src != v else "")
        r["FE_massa_sup_g"] = d["massa_FE_g"].get("superior_g")
        r["FE_massa_inf_g"] = d["massa_FE_g"].get("inferior_g")
        for cs in ("ONE_24", "ONE_30"):
            c = d["casos"].get(cs, {})
            for kk in ("desl_max_mm", "FI_z_superior", "FI_xy_superior", "FI_z_inferior", "FI_xy_inferior", "FI_giroide_max"):
                r["mont_%s_%s" % (cs, kk)] = c.get(kk, "")
        for kk in ("peca_critica", "rigidez_asa_montada_N_mm", "sigma_Z_24kg_MPa_(x PICO)", "kg_max_PA6-CF_Z48",
                   "FS_24kg_PA6-CF_Z48", "FS_30kg_PA6-CF_Z48", "kg_max_PAHT_CF15_Z18.2", "FS_24kg_PAHT_CF15_Z18.2",
                   "FS_30kg_PAHT_CF15_Z18.2", "PICO"):
            r["mont_" + kk] = d.get(kk, "")
    if v in SUP:
        d = SUP[v]
        r["sup_FE_arquivo"] = MAP_SUP[v] + ".json"
        r["sup_mass_model_g"] = d.get("mass_model_g", "")
        for cs in ("ONE_24", "ONE_30", "SYM_24"):
            c = d.get("cases", {}).get(cs)
            if c:
                r["sup_%s_disp_max_mm" % cs] = c.get("disp_max_mm", "")
                r["sup_%s_solid_FI_z_max" % cs] = c.get("solid_FI_z_max", "")
                r["sup_%s_solid_FI_xy_max" % cs] = c.get("solid_FI_xy_max", "")
                r["sup_%s_infill_FI_max" % cs] = json.dumps(c.get("infill_FI_max", {}))
    if v in INF:
        d = INF[v]
        r["inf_FE_arquivo"] = MAP_INF[v] + ".json"
        for kk in ("mass_model_g", "disp_max_mm", "FI_z", "FI_xy"):
            r["inf_" + kk] = d.get(kk, "")
    if v in IMPD:
        d = IMPD[v]
        r["imp_arquivo"] = "impacto_%s.json" % MAP_IMP[v]
        for kk in ("massa_FE_g", "f1_Hz_com_24kg", "TR_ms", "zeta", "FI_z_estatico", "FI_z_pico_dinamico", "t_pico_ms",
                   "fator_dinamico_3D", "sigma_Z_pico_MPa_(x PICO)", "FI_giroide_pico", "desl_pico_mm",
                   "FS_dinamico_PA6CF_Z48", "FS_dinamico_PAHT_Z18.2"):
            r["imp_" + kk] = d.get(kk, "")
    if v in FRAMES:
        F = FRAMES[v]
        kf = int(np.argmax(np.nanmax(F["fi"], axis=1)))
        r["frames_t_FImax_ms"] = float(F["t"][kf])
        r["frames_FImax"] = round(float(F["fi"][kf].max()), 5)
    if v in VIDA_V:
        d = VIDA_V[v]
        r["vida_rigidez_asa_N_mm"] = d.get("rigidez_asa_N_mm", "")
        r["vida_freq_natural_24kg_Hz"] = d.get("freq_natural_24kg_Hz", "")
        for m, tag in (("PA6-CF valor usado no FE (Z=48 MPa)", "PA6"), ("PAHT CF15 (TDS, Z=18,2 MPa)", "PAHT")):
            md = d.get("materiais", {}).get(m)
            if md:
                for kk in ("kg_max_estatico_g", "kg_max_com_g+5", "FS_24kg_g+5", "FS_30kg_g+5"):
                    r["vida_%s_%s" % (tag, kk)] = md.get(kk, "")
                for kk, vv in md.get("fadiga", {}).items():
                    r["vida_%s_%s" % (tag, kk)] = vv
    if len(r) > 3:
        linhas.append(r)

cols = []
for r in linhas:
    for k in r:
        if k not in cols:
            cols.append(k)
csv_p = os.path.join(OUT, "dados_comparativos.csv")
with open(csv_p, "w", newline="", encoding="utf-8-sig") as f:
    wtr = csv.DictWriter(f, fieldnames=cols, delimiter=";")
    wtr.writeheader()
    for r in linhas:
        wtr.writerow(r)
print("  [ok] dados_comparativos.csv (%d variantes, %d colunas)" % (len(linhas), len(cols)))

# ================================================================ INDEX.md
with open(os.path.join(OUT, "INDEX.md"), "w", encoding="utf-8") as f:
    f.write("# Galeria comparativa R07: garra SAMI (UR30)\n\n")
    f.write("Gerada por `scripts/r07_galeria.py` (re-executável). Todos os valores vêm dos arquivos de resultado "
            "(fatiamento Orca, FE por voxels, impacto, vida); nada foi recalculado por solver. "
            "Os números estão em `dados_comparativos.csv` (separador `;`, UTF-8).\n\n")
    f.write("Cores fixas: R07 com esqueleto = azul forte; R07 sem esqueleto = azul claro; giroide uniforme 30/35/40% = "
            "cinza claro/médio/escuro; R06 = laranja; Hexa3D 30% PA6-CF = lilás; atual Tritan = contorno preto hachurado.\n\n")
    f.write("| Figura | O que mostra |\n|---|---|\n")
    for nome, desc in CRIADOS:
        f.write("| [%s](%s) | %s |\n" % (nome, nome, desc))
    f.write("\n## Ressalvas\n\n")
    f.write("- FE por voxels é estimativa (lei Gibson-Ashby para o giroide, não calibrada por ensaio); tensões de pico × %s.\n"
            % br(PICO, 1))
    f.write("- Hexa3D 30% não tem FE próprio: no gráfico massa × resistência usa o resultado do giroide 30% uniforme.\n")
    f.write("- A garra atual em Tritan só entra nas comparações de massa (sem FE em Tritan).\n")
    f.write("- Fadiga (12) vem do modelo anterior da peça superior isolada (`r07_vida.json`), não da garra montada.\n")
    if PULADOS:
        f.write("\n## Entradas ausentes nesta execução\n\n")
        for p in PULADOS:
            f.write("- %s\n" % p)
print("  [ok] INDEX.md")

print("\n== Resumo")
print("Criados (%d): %s" % (len(CRIADOS), ", ".join(c[0] for c in CRIADOS)))
print("Pulados (%d):" % len(PULADOS))
for p in PULADOS:
    print("  - " + p)
print("\nTabela-chave:")
print("%-14s %9s %8s %8s %8s %8s %8s" % ("variante", "garra_g", "%Tritan", "kgPA6", "kgPAHT", "desl24", "FSimpPAHT"))
for v in VAR:
    m = MASSA.get(v, {})
    mo = MON.get(v, {})
    im = IMPD.get(v, {})
    print("%-14s %9s %8s %8s %8s %8s %8s" % (
        v, br(m["garra_g"], 0) if m else "-", br(m["pct_vs_tritan"], 1) if m else "-",
        mo.get("kg_max_PA6-CF_Z48", "-"), mo.get("kg_max_PAHT_CF15_Z18.2", "-"),
        mo.get("casos", {}).get("ONE_24", {}).get("desl_max_mm", "-") if mo else "-",
        im.get("FS_dinamico_PAHT_Z18.2", "-")))
sys.exit(0)
