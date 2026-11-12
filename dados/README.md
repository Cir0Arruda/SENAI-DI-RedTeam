# Dados da garra SAMI (UR30): simulações e fatiamentos

Esta pasta guarda os arquivos que geram os números, as imagens e o vídeo do site. Nada aqui é ensaio físico: são fatiamentos reais no OrcaSlicer e simulações numéricas, com as hipóteses descritas em cada arquivo e no [relatório](RELATORIO_R07.md).

## Variantes comparadas

| Código | O que é |
|---|---|
| R07 COM (`F25_COM`, `R07_COM`) | esqueleto interno (almas 100%) + zonas + giroide 25% (superior) / 20% (inferiores) |
| R07 SEM (`F25_SEM`, `R07_SEM`) | mesmas zonas, sem as almas |
| `UNI_30` / `UNI_35` / `UNI_40` | giroide uniforme 30/35/40%, sem esqueleto e sem zonas |
| `UNI_HONEYCOMB3D30` | 3D honeycomb (Hexa3D) 30% uniforme, padrão da garra instalada |
| `UNI_TPMSD40` | TPMS-D 40% uniforme, proposta inicial |
| R06 | versão anterior: zonas TPMS-D |

A garra instalada é de Tritan Hexa3D 30%. Sua massa é estimada como o fatiamento Hexa3D 30% × 1,18/1,10 (densidades), dando 1.577 g de peças impressas.

## Pastas

| Pasta | Conteúdo | Origem |
|---|---|---|
| `orca/` | massa por peça, filamento, tempo e avisos de cada fatiamento | OrcaSlicer CLI, Creality K1 Max, 1:1, PA6-CF 1,10 g/cm³, 5 paredes, camada 0,2 mm. Nada foi enviado à impressora. |
| `montagem/` | garra **montada** (superior + inferior): carga máxima numa asa, FS a 24/30 kg, rigidez, flecha | FE por voxels de 3 mm, giroide homogeneizado (Gibson-Ashby), pico × 2,2 (calibrado no Fusion do R06) |
| `impacto/` | tranco de 24 kg numa asa aplicado em 10 ms; séries no tempo (`hist`) | FE transiente 3D (Newmark, Rayleigh 3%) da peça superior |
| `fadiga/` | vida estimada da peça superior | curva S-N normalizada conservadora + regra de Miner |
| `decisao/` | tabela consolidada para decidir com × sem esqueleto (`DECISAO_ESQUELETO.json`, `dados_comparativos.csv`) | junta as pastas acima |
| `materiais/`, `fusion/` | cartões de material e montagem do modelo do Fusion | |
| `videos/` | números mostrados junto dos vídeos (`videos_r07.json`) | gerados por `scripts/r07_videos.py` só com campos já calculados |
| `scripts/` | scripts Python que geraram os resultados, as figuras e o vídeo | |

Cargas: massa × (g + 5 m/s²), com as duas caixas numa asa só (erro da seladora). 24 kg → 355,4 N; 30 kg → 444,2 N.
Resistência entre camadas (Z): PA6-CF 48 MPa e PAHT CF15 18,2 MPa (TDS dos fabricantes).

## Vídeos de simulação

Os vídeos do site são renderizados a partir dos campos já calculados. Nenhum vídeo cria resultado novo.

| Vídeo | O que mostra | De onde vem |
|---|---|---|
| `impacto_r07_comparativo.mp4` | corte vertical da peça superior das 4 variantes durante o tranco | `r07_impacto.py` |
| `carga_24kg_asa.mp4` | garra montada com e sem esqueleto e giroide 30% uniforme, carga de 0 a 24 kg numa asa; FS final de cada uma | `r07_montagem.py --campos` (FE estático linear: o campo escala com o peso) |
| `impacto_distribuicao.mp4` | peça superior com e sem esqueleto, índice de falha voxel a voxel durante os 80 ms do tranco | `r07_impacto.py --campos3d` |
| `absorcao_giroide.mp4` | só o giroide: quanto da própria resistência ele usa e a parcela da energia de deformação que ele guarda | `r07_impacto.py --campos3d` |

As figuras de camadas (`camadas_r07_*.jpg`) vêm dos G-codes reais do Orca. O corte do encaixe (`encaixe_r07_*.jpg`) é feito com os modificadores do Orca, então mostra geometria e não é FE.

## Limites

- Os resultados de FE são **estimativas** e não substituem ensaio de bancada.
- A resistência real entre camadas depende da impressão (secagem, temperatura, orientação).
- Hexa3D e TPMS-D não têm FE próprio: recebem a resistência do giroide de mesma densidade, porque a lei homogeneizada não distingue o tipo de célula.
- Os preços (R$/kg) e os dados de produção (45 min, 280 caixas, R$ 84.000) foram informados pela equipe.
