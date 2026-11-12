# Galeria comparativa R07: garra SAMI (UR30)

Gerada por `scripts/r07_galeria.py` (re-executável). Todos os valores vêm dos arquivos de resultado (fatiamento Orca, FE por voxels, impacto, vida); nada foi recalculado por solver. Os números estão em `dados_comparativos.csv` (separador `;`, UTF-8).

Cores fixas: R07 com esqueleto = azul forte; R07 sem esqueleto = azul claro; giroide uniforme 30/35/40% = cinza claro/médio/escuro; R06 = laranja; Hexa3D 30% PA6-CF = lilás; atual Tritan = contorno preto hachurado.

| Figura | O que mostra |
|---|---|
| [01_massa_garra.png](01_massa_garra.png) | Massa impressa da garra (superior + 2 inferiores) por variante, com a garra atual em Tritan Hexa3D 30% como referência e a variação percentual. |
| [02_garra_completa_payload.png](02_garra_completa_payload.png) | Massa da garra completa montada e da garra com 2 caixas, em kg e em % do payload de 30 kg do UR30. |
| [03_carga_maxima_montagem.png](03_carga_maxima_montagem.png) | Carga máxima numa asa da garra montada (kg) por variante, para PA6-CF e PAHT CF15, com referências de 24 e 30 kg. |
| [04_fs_24_30.png](04_fs_24_30.png) | Fatores de segurança da garra montada com 24 e 30 kg numa asa, em PA6-CF e PAHT CF15, com linhas em FS = 1 e FS = 2. |
| [05_massa_x_resistencia.png](05_massa_x_resistencia.png) | Gráfico de compromisso: massa impressa da garra (x) contra carga máxima numa asa em PA6-CF (y), por variante. |
| [06_rigidez_deslocamento.png](06_rigidez_deslocamento.png) | Deslocamento máximo da asa com 24 kg (mm) e rigidez da asa montada (N/mm) por variante. |
| [07_mapas_montagem_lado_a_lado.png](07_mapas_montagem_lado_a_lado.png) | Mosaico dos mapas de índice de falha da garra montada (24 kg numa asa) para R06, R07 com/sem esqueleto e giroide uniforme 30/40/35%. |
| [08_mapas_superior_lado_a_lado.png](08_mapas_superior_lado_a_lado.png) | Mosaico dos mapas de índice de falha da peça superior isolada (24 kg numa asa) para R07 com/sem esqueleto, giroide 30/40% e R06. |
| [09_impacto_curvas.png](09_impacto_curvas.png) | Histórico no tempo da tensão Z de pico e do índice de falha do giroide durante o tranco de 24 kg, por variante disponível. |
| [10_impacto_resumo.png](10_impacto_resumo.png) | Tensão Z de pico dinâmica, fator dinâmico e fator de segurança dinâmico (PA6-CF e PAHT CF15) por variante de impacto disponível. |
| [11_impacto_snapshot_pico.png](11_impacto_snapshot_pico.png) | Seção crítica da peça superior no quadro de índice de falha máximo do impacto, colorida pelo índice de falha, deslocamento ampliado 25×, mesma escala de cor. |
| [12_fadiga.png](12_fadiga.png) | Vida estimada em fadiga (horas, escala log) por variante e material, para só erros de 24 kg e para uso misto com 1% de erros. |

## Ressalvas

- FE por voxels é estimativa (lei Gibson-Ashby para o giroide, não calibrada por ensaio); tensões de pico × 2,2.
- Hexa3D 30% não tem FE próprio: no gráfico massa × resistência usa o resultado do giroide 30% uniforme.
- A garra atual em Tritan só entra nas comparações de massa (sem FE em Tritan).
- Fadiga (12) vem do modelo anterior da peça superior isolada (`r07_vida.json`), não da garra montada.

## Entradas ausentes nesta execução

- massa da garra UNI_15: fatiamento ausente/sem ok para superior e inferior esq.
- impacto ainda não disponível: IMPACTO/impacto_R06.json
- frames ainda não disponíveis: IMPACTO/frames_R06.npz
- impacto ainda não disponível: IMPACTO/impacto_F25_SEM_ISO.json
- frames ainda não disponíveis: IMPACTO/frames_F25_SEM_ISO.npz
- impacto ainda não disponível: IMPACTO/impacto_UNI_35.json
- frames ainda não disponíveis: IMPACTO/frames_UNI_35.npz
