"""Limites do PAD de sacrifício e da garra R07 SEM esqueleto num golpe direto (modelo 1D em série, estimativa).

Cadeia: impactor -> PAD (TPU 95A, 40%) -> garra (seção local do encaixe, R07 sem esqueleto).
Entradas (todas de arquivos já publicados):
  - PAD: lei do modelo R03 (rigidez 125,5 N/mm, núcleo 3,9 mm + 2 peles de 1,2 mm, área 100 mm², TPU E 33,6 MPa)
  - Garra local: viga substituta do R03 (30 x 30 x 10 mm, 5 paredes) com o núcleo trocado de Hexa3D 15% para
    giroide 25% (superior do R07 sem esqueleto), lei de potência n = 2 como no R03
  - Carga de ruptura da garra: FE da garra montada R07 SEM, 93,3 kg numa asa com (g + 5 m/s²) = 1.382 N.
    É o ponto crítico (raiz da flange) com o pico x 2,2 calibrado; usado aqui como limite conservador.
Hipóteses do PAD:
  - "PAD no limite" = núcleo giroide 40% esmagado até a densificação: deformação 1 - 1,4 x 0,40 = 44% do núcleo
    (Gibson-Ashby); as peles acompanham na mesma proporção do R03 (5,0% / 31,3%).
  - Depois disso o PAD vira uma camada maciça de TPU (E 33,6 MPa) com a espessura que sobrou.
Nada aqui é ensaio. Servem para comparar ordens de grandeza.
Uso: python pad_limites.py <pasta do site>
"""
import json, sys
from pathlib import Path

SITE = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
G = 9.81

# PAD (R03)
k_pad = 125.49019607843141           # N/mm
core, skin2, area, E_tpu = 3.9, 2.4, 100.0, 33.6
eps_core_dens = 1 - 1.4 * 0.40      # 0,44
skin_ratio = 5.015567187945128 / 31.34729492465704
x_lim = eps_core_dens * core + eps_core_dens * skin_ratio * skin2   # compressão no limite (mm)
F_pad = k_pad * x_lim                                               # N
E_pad = 0.5 * k_pad * x_lim ** 2                                    # N·mm
k_solid = E_tpu * area / (core + skin2 - x_lim)                     # N/mm, TPU maciço que sobrou

# Garra local R07 SEM (viga substituta R03, núcleo giroide 25%)
E_s, I_skin, I_core, L = 4430.0, 1548.8853333333336, 951.1146666666665, 30.0
E_core = E_s * 0.25 ** 2
k_garra = 3 * (E_s * I_skin + E_core * I_core) / L ** 3            # N/mm
F_rup = 93.3 * (G + 5.0)                                            # N

# Golpe de referência do R03 (esfera de 263 g a 1 m/s)
m, v = 0.26305602486058527, 1.0
E0 = 0.5 * m * v ** 2 * 1000                                        # N·mm
k_serie = k_pad * k_garra / (k_pad + k_garra)
F_sem = (2 * E0 * k_garra) ** 0.5
F_com = (2 * E0 * k_serie) ** 0.5

# Cenário 1: PAD chega ao limite; garra inteira
E1 = E_pad + F_pad ** 2 / (2 * k_garra)
# Cenário 2: garra rompe (PAD já esmagado)
E2_com = E_pad + (F_rup ** 2 - F_pad ** 2) / (2 * k_solid) + F_rup ** 2 / (2 * k_garra)
E2_sem = F_rup ** 2 / (2 * k_garra)

r = dict(
    modelo='1D em série, estimativa (não é FEA nem ensaio)',
    garra='R07 sem esqueleto, seção local do encaixe; ruptura do FE da garra montada',
    k_pad_N_mm=round(k_pad, 1), k_garra_local_N_mm=round(k_garra, 1), k_tpu_macico_N_mm=round(k_solid, 1),
    golpe_referencia=dict(massa_kg=round(m, 3), v_m_s=v, energia_J=round(E0 / 1000, 3),
                          pico_sem_PAD_N=round(F_sem, 1), pico_com_PAD_N=round(F_com, 1),
                          reducao_pct=round((1 - F_com / F_sem) * 100, 1)),
    pad_no_limite=dict(compressao_mm=round(x_lim, 2), forca_N=round(F_pad, 0), forca_kgf=round(F_pad / G, 1),
                       energia_J=round(E1 / 1000, 3), garra_pct_da_ruptura=round(F_pad / F_rup * 100, 0),
                       garra_fs=round(F_rup / F_pad, 1)),
    garra_rompe=dict(forca_N=round(F_rup, 0), forca_kgf=round(F_rup / G, 1),
                     energia_com_PAD_J=round(E2_com / 1000, 2), energia_sem_PAD_J=round(E2_sem / 1000, 2),
                     vezes_mais_energia_com_PAD=round(E2_com / E2_sem, 1)),
    analogias=dict(
        pad_queda_celular_200g_cm=round(E1 / 1000 / (0.2 * G) * 100, 0),
        garra_queda_1kg_com_PAD_cm=round(E2_com / 1000 / (1.0 * G) * 100, 0),
        garra_queda_1kg_sem_PAD_cm=round(E2_sem / 1000 / (1.0 * G) * 100, 0)),
    hipoteses=['área de contato 100 mm² e lei do PAD do modelo R03',
               'núcleo giroide 40% esmagado a 44% de deformação (Gibson-Ashby)',
               'garra local = viga substituta do R03 com giroide 25%',
               'ruptura = carga máxima do FE da garra montada R07 SEM (PA6-CF, Z 48 MPa), limite conservador',
               'sem amortecimento, sem efeito de taxa, sem rasgo do TPU'],
)
out = SITE / 'dados' / 'impacto' / 'pad_limites.json'
out.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(r, ensure_ascii=False, indent=1))
