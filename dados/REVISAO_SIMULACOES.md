# Revisão das simulações e dos dados do Projeto SAI

Data: 12/11/2026. Revisei os relatórios do Fusion, os projetos do Orca (configuração de impressão de cada peça), os resultados do FE próprio, o modelo do PAD, os números de todos os slides e os arquivos 3D publicados na Release.

Nada foi recalculado no Fusion nem enviado à impressora. Refiz as contas a partir dos arquivos e conferi se cada número do slide sai da fonte certa.

Foram **duas varreduras completas**. A segunda (seção 7) refez tudo depois das correções: 63 números conferidos por script, 0 com problema.

---

## 1. Resposta curta

1. **As contas batem.** Cada número de resistência, peso, PAD e custo sai da fonte declarada, com a aritmética certa.
2. **O Fusion não simulou a peça impressa.** Os dois estudos resolvidos (PA6-CF e Tritan) usam:
   - a garra superior **maciça (100%)**;
   - material **igual em todas as direções** (sem camadas);
   - os 24 kg **divididos nas 4 interfaces**, ou seja, nas duas asas.

   Preenchimento, paredes e camadas **não entram no Fusion**. O estudo do Fusion com o preenchimento do SAI (R07) **não rodou**: falhou na malha.
3. **O preenchimento e as camadas entram só no FE próprio (Python, voxels de 3 mm).** Ali estão:
   - as 5 paredes;
   - o giroide 25%/20% e as zonas;
   - a resistência entre camadas (Z 48 MPa);
   - 24 kg numa asa só.

   É dele que saem os 93 kg e o FS 3,9. Ele usa um **fator de pico de 2,2**. Antes dizia "calibrado no Fusion do R06", sem arquivo. **Refiz a calibração** (seção 4, item 1): a mesma peça maciça do [F1] no FE por voxels dá 3,23 ÷ 1,46 = **2,2** pela tensão de von Mises. O número está certo, mas pela 1ª tensão principal seria 2,7.
4. **Os erros encontrados foram corrigidos** (seção 3): 6 na primeira varredura e 12 na segunda, quase todos de texto. Nenhum muda a conclusão.
5. **Os arquivos 3D existem e são públicos**, mas estão espalhados em 3 zips, que somam 1,4 GB, com nomes confusos. Falta um pacote final do SAI pronto para a Ajinomoto: seção 6.

---

## 2. O que está certo (conferido)

| Item | Conferência |
|---|---|
| Carga de projeto | 24 kg × (9,81 + 5 m/s²) = 355,4 N ✓ |
| Fusion, montagem do estudo | fixação nos 6 furos da flange; carga −Z de 4 × 88,84 N; malha de 3 mm parabólica, 498.261 nós ✓ |
| Fusion, resultados | von Mises 3,23 MPa; 1ª principal 5,16 MPa ✓ |
| Fusion, FS e deslocamento | FS 19,8 = 102 ÷ 5,16 ✓; Tritan FS 11,5 = 58 ÷ 5,03 ✓; o PA6-CF deforma 65% menos (0,08 contra 0,23 mm) ✓ |
| "Quase 3 vezes mais firme" | E 4.430 ÷ 1.548 = 2,9 ✓ (no plano XY; entre camadas o PA6-CF é 1,4× o Tritan) |
| Preenchimento no FE próprio | giroide 25%: E 277 MPa e resistência 3,82 MPa (Gibson-Ashby) ✓ |
| Impressão da garra SAI (Orca) | K1 Max, bico 0,4, camada 0,2 mm, **5 paredes**, 6 camadas de topo e de fundo, PA6-CF a 275 °C ✓ |
| Preenchimento da garra superior | giroide 25%, com modificadores internos 100% (tubos dos furos), 55% (colar), 35% (ressaltos) e 20% (assento) ✓ |
| Preenchimento das inferiores | giroide 20% ✓ |
| Exterior | idêntico ao original: mesma malha, conferida por hash nos projetos com e sem esqueleto ✓ |
| "Sem esqueleto" | o modificador sólido do SAI só tem os tubos dos furos, menor que o da versão com almas ✓ |
| Orientação de impressão | Z do CAD = Z da impressora = Z do cálculo; a resistência entre camadas está aplicada na direção certa ✓ |
| Massa da garra | 666,4 + 383,2 + 383,2 = 1.432,8 g; filamento 1.744,5 g; 75,2 h ✓ |
| PADs | geometria R02, 8 meias-peças, TPU, giroide 40%, 3 paredes; 93,1 g de peça + 45,9 g de suporte = 139 g ✓ |
| PADs, montagem | malhas fechadas e sem interferência com a garra (checagem estática) ✓ |
| Garra montada (FE próprio) | 12,34 MPa a 24 kg → FS 48 ÷ 12,34 = 3,89 → 93,3 kg numa asa ✓; pior colagem 35,4 kg ✓ |
| PAD (modelo de molas) | ≈ 240 N; 17% da ruptura; 1.382 N; 2,2× mais energia; 27 cm contra 12 cm ✓ |
| Custos | R$ 450,08 = 1.744,5 g × R$ 258/kg ✓; R$ 21,96 = 139 g × R$ 158/kg ✓ |

---

## 3. Erros que precisam ser corrigidos

**Primeira varredura, corrigidos em 12/11/2026:** itens 1, 2, 3, 4 e 6 no site e no `REFERENCIAS.md`. O item 5 ganhou uma nota no [F2], mas ainda precisa ser conferido no Fusion.

O item 4 foi conferido no inventário da montagem original: ela tem só a garra superior e os dois suportes de ventosa, sem PADs. Por isso os 8 PADs entram no peso do SAI: 2,690 + 0,093 = 2,783 kg.

| # | Onde | Problema | Correção |
|---|---|---|---|
| 1 | Slide PAD (8) | O rodapé diz "Fonte: Autodesk Fusion … simulação". Os números do PAD (−63%, 451/169 N, 240 N, 1.380 N) **não vêm do Fusion**: são do modelo de molas 1D, em Python. O próprio registro do Fusion diz "Impacto sem/com PAD: não resolvido". | "Modelo 3D no Autodesk Fusion · forças por modelo de molas (estimativa)" |
| 2 | Encerramento, [F1] | "24 kg numa asa". No Fusion a carga foi **dividida nas 4 interfaces** (as duas asas) e a peça era **maciça**. | "peça maciça, 24 kg divididos nas 4 interfaces" |
| 3 | `REFERENCIAS.md`, [F1] | "malha adaptativa (10% refinado)". O relatório mostra **0 etapas de refinamento**; os 10% são só um campo de configuração. Também não houve estudo de convergência. | "malha de 3 mm, sem refinamento adaptativo e sem estudo de convergência" |
| 4 | Custos, Sustentabilidade, Conclusão | "2,690 kg, −144 g (−5,1%)" **não soma os 8 PADs novos** (93 g de TPU). A conta supõe que eles já existem na garra atual. | Se a garra atual não tem PADs: **2,783 kg, −51 g (−1,8%)**. A equipe precisa confirmar. |
| 5 | Relatório Fusion do Tritan | O cabeçalho mostra o critério "resistência a escoamento", mas o FS 11,5 corresponde ao de ruptura (58 ÷ 5,03). Com escoamento seria 13,3. | Confirmar no Fusion qual critério foi usado. Muda pouco: o Tritan fica entre 11,5 e 13,3. |
| 6 | Processo (4) | "Garra com caixas: 26 kg", mas a conta ao lado dá 26,8 kg. | "26,8 kg" |

**Segunda varredura, corrigidos em 12/11/2026:**

| # | Onde | Problema | Correção |
|---|---|---|---|
| 7 | Custos (10) | "R$ 627,33" no gasto do ano. A conta é 495,54 + 6 × 21,96 = **627,30**. | "R$ 627,30" (3 lugares) |
| 8 | Custos (10) | "6 PADs a cada 2 meses": são 6 trocas no ano, cada uma de **8 PADs**. | "6 jogos de 8 PADs" |
| 9 | Custos (10) | Filamento "1.745 g" com custo R$ 450,08, que é 1.744,5 g × R$ 258/kg (1.745 g daria 450,21). | "1.744,5 g" |
| 10 | Processo (4) | "7–8 paletes, ≈ 280 caixas". 280 ÷ 40 = **7 paletes** exatas. | "7 paletes, 280 caixas" |
| 11 | Intro (3) e Processo (4) | "6 caixas/min" × 45 min = 270, não 280. O ritmo é aproximado. | "cerca de 6 caixas por minuto" |
| 12 | PAD (8) | "onde a trinca começava" (nos ressaltos). O FE e a capa dizem que a garra rompe na **raiz da flange**. | "onde ela recebe as batidas" |
| 13 | Giroide (9) | "sem plano fraco": a peça impressa tem plano fraco entre camadas (48 contra 102 MPa). | Frase removida |
| 14 | ROI (11) e Conclusão (13) | "Fadiga acima de 100 anos" sem a condição. Na pior colagem cai para 2,4 a 2,6 anos. | "com a colagem entre camadas da ficha, a fadiga passa de 100 anos" |
| 15 | Gráfico do PAD (8) | O rótulo mostrava 450,7 N (amostra da série a cada 0,05 ms); o pico do R03 é 450,9 N. | O rótulo lê o pico exato: 450,9 → 168,5 N, −63% |
| 16 | Encerramento [F4], `REFERENCIAS.md`, `RELATORIO_R07.md`, `README.md` | "Fator 2,2 calibrado no R06", sem arquivo. | "calibrado contra o [F1] na mesma peça maciça" + `fusion/calibracao_pico.json` |
| 17 | Giroide (9), layout | A tabela "Onde ele está no SAI" não quebrava linha e escondia o texto atrás de uma rolagem lateral. | A tabela quebra linha |
| 18 | Conclusão (13), layout | A nota de rodapé ficava cortada (20 px) em 1536 × 730: o ajuste de zoom acertava no limite e depois não cabia. | O ajuste confere o resultado e reduz até caber |

---

## 4. Pontos fracos (não são erros de conta, mas precisam ser ditos)

1. **Fator de pico 2,2: agora calibrado e registrado.** O FE por voxels suaviza os picos de tensão, então o script multiplica o pico por 2,2. Não havia arquivo da calibração. Refiz: o FE por voxels resolveu **a mesma peça do [F1]** (superior maciça, PA6-CF isotrópico, 355,36 N nas 4 interfaces, engaste nos 6 furos). Resultado em `fusion/calibracao_pico.json`:

   | | Fusion [F1] | FE por voxels (3 mm) | Fator |
   |---|---|---|---|
   | von Mises máxima | 3,232 MPa | 1,459 MPa | **2,22** |
   | 1ª principal máxima | 5,163 MPa | 1,915 MPa | 2,70 |
   | Deslocamento máximo | 0,080 mm | 0,078 mm | 1,03 |
   | Reação vertical | 355,36 N | 355,36 N | 1,00 |

   O deslocamento bate (3% de diferença), então os dois modelos são a mesma peça com a mesma carga. O 2,2 publicado é o fator de von Mises. **Sensibilidade:** se o critério certo for a 1ª principal (fator 2,7), todos os FS caem cerca de 19%:
   - garra montada, 24 kg numa asa: FS 3,89 → **3,17**; 93 kg → **76 kg**;
   - pior colagem (PAHT): 35,4 kg → 28,8 kg; FS 1,47 → 1,20;
   - tranco de 10 ms: FS 2,65 → 2,16; na pior colagem 1,01 → **0,82** (abaixo de 1);
   - ruptura no modelo do PAD: 1.382 N → 1.126 N; o PAD esmagado passa de 17% para 21% da ruptura.

   A conclusão do PA6-CF com a colagem da ficha não muda (FS acima de 3). O caso que fica no limite é a pior colagem num tranco: mais um motivo para o ensaio de bancada. Limite da calibração: os picos do Fusion ficam perto dos furos e do engaste, sem estudo de convergência.
2. **"Resistência entre camadas 48 MPa"** é de corpo de prova seco, 100% preenchido e **recozido a 80 °C por 12 h** (ficha Bambu). A peça impressa sem recozimento e com umidade fica abaixo disso. O caso PAHT CF15 (18,2 MPa) cobre esse risco: a garra ainda aguenta 35 kg numa asa, FS 1,47.
3. **"Fadiga acima de 100 anos"** (ROI e Conclusão) só vale com a colagem da ficha. Na pior colagem a vida cai para **cerca de 2,4 a 2,6 anos** em 24/7. *Corrigido: os slides agora dizem "com a colagem entre camadas da ficha".*
4. **"1.380 N quebra a garra"** é a carga de **uma asa inteira** que rompe a raiz da flange. Foi usada como limite de um golpe local no ressalto. É uma aproximação, não um cálculo do golpe no ressalto. Golpes laterais não foram simulados.
5. **Gráfico do PAD:** 450,9 → 168,5 N vem do estudo R03, feito com núcleo Hexa3D 15% na garra. Refeito para o SAI (giroide 25%) dá 456 → 169 N. A redução de 63% é a mesma; os valores mudam 1%.
6. **Onde a garra quebra:**
   - a capa diz "rompe na raiz, onde se prende ao robô", e o FE concorda: o ponto crítico é a raiz da flange;
   - o slide do PAD e o de Materiais dizem que a trinca começa nos ressaltos e furos dos parafusos.

   Vale alinhar com a foto da peça quebrada. *Corrigido no slide do PAD: o ressalto é "onde ela recebe as batidas".*
7. **Giroide "sem plano fraco":** o preenchimento não tem, mas a peça impressa tem: entre camadas a resistência é menos da metade (48 contra 102 MPa). Melhor dizer "espalha a carga em todas as direções". *Corrigido.*
8. **Junta parafusada tratada como colada** no FE da garra montada. Isso deixa a garra um pouco mais rígida do que a real.
9. **Materiais dos perfis:**
   - a garra foi fatiada com o perfil "Bambu PA6-CF @BBL X1C" numa K1 Max, e o Orca avisa que precisa de bico endurecido;
   - os PADs foram fatiados com "Generic TPU";
   - a ficha citada é a Bambu TPU 95A HF;
   - o modelo do PAD usa a PolyFlex TPU95.

   Definir qual TPU será comprado.
10. **Densidade do filamento:** a superior foi fatiada com 1,10 g/cm³ e as inferiores com 1,09. São cerca de 6 g a mais na superior. Irrelevante, mas inconsistente.
11. **Peso da garra atual é estimado, não pesado:** fatiamento Hexa3D 30% × 1,18/1,10 = 1.577 g. Pesar as três peças de Tritan fecha a conta do peso.
12. **Nenhum número é ensaio.** O teste de bancada (carga de prova de 24 kg numa asa, ruptura, 10⁵ ciclos) é o que valida tudo.

---

## 5. O que o Fusion simulou e o que não simulou

| Pergunta | Resposta |
|---|---|
| O Fusion considerou o preenchimento? | **Não.** Peça maciça. O modelo com casca + núcleo (R07) falhou na malha. |
| Considerou as 5 paredes? | **Não.** |
| Considerou as camadas (direção Z mais fraca)? | **Não.** Material isotrópico com valores do plano XY (102 MPa). |
| Considerou o material certo? | **Sim:** PA6-CF da ficha Bambu (E 4.430 MPa) e Tritan TX1001 da ficha Eastman. O Poisson é aproximado (0,39 e 0,38). |
| A carga é a do erro da seladora (24 kg numa asa)? | **Não.** São 24 kg divididos nas duas asas. O caso de uma asa só foi feito no FE próprio. |
| Considerou a garra inferior, os parafusos e os PADs? | **Não.** Só a peça superior. |
| Simulou o impacto com e sem PAD? | **Não.** O PAD foi calculado com o modelo de molas. |

Leitura: os estudos do Fusion servem para **comparar os dois materiais na mesma geometria** (o PA6-CF deforma 65% menos). **Não servem para dizer quanto a garra impressa aguenta.** Esse número vem do FE próprio, que precisa do fator 2,2 confirmado.

---

## 6. Arquivos 3D para a Ajinomoto

Release pública `dados-2026-11-12`: <https://github.com/Cir0Arruda/SENAI-DI-RedTeam/releases/tag/dados-2026-11-12>

**O que a Ajinomoto precisa para imprimir o SAI, e onde está hoje:**

| Peça | Arquivo | Pacote |
|---|---|---|
| Garra superior, projeto Orca com modificadores | `desempenho/05_Orca/R07/COMPARATIVO/GARRA_SUPERIOR_R07_SEM_ESQUELETO_GIROIDE25_K1MAX.3mf` | `orca_projetos_3mf.zip` (84 MB) |
| Garra inferior esquerda | `desempenho/05_Orca/R07/GARRA_INFERIOR_ESQ_R07_ESQUELETO_GIROIDE20_K1MAX.3mf` (o nome diz "esqueleto", mas a peça não tem) | `orca_projetos_3mf.zip` |
| Garra inferior direita | `desempenho/05_Orca/R07/GARRA_INFERIOR_DIR_R07_ESQUELETO_GIROIDE20_K1MAX.3mf` | `orca_projetos_3mf.zip` |
| 8 PADs | `desempenho/05_Orca/CONFIRMADO_R05/PADs_TPU95A40_K1MAX_ESCALA_REAL.3mf` | `orca_projetos_3mf.zip` |
| Fatiados com G-code (só K1 Max) | `R07_SEM_SUPERIOR_R06_FATIADO.3mf` (o nome diz "R06", mas é R07), `INFERIOR_ESQ_B20_R06_FATIADO.3mf`, `INFERIOR_DIR_B20_R06_FATIADO.3mf` | `orca_fatiados_R07.zip` (1,04 GB) |
| CAD do exterior (STEP e F3D) | `desempenho/01_Fusion/GARRA_R04_EXTERIOR_ORIGINAL_PREPARACAO.step` | `modelos_3d.zip` (300 MB) |
| CAD dos PADs | `fusion/preparacao_garra/SAMI_PAD95_MONTAGEM_R02.step`, `SAMI_PAD95_CONFORMAL_R02.f3d`, STLs em `desempenho/02_STL_PAD/` | `modelos_3d.zip` |

**Conclusão:** a Ajinomoto **consegue** obter os arquivos, mas hoje precisaria:
- baixar 1,4 GB;
- achar 7 arquivos entre cerca de 300;
- adivinhar quais são os finais, com nomes que dizem "R06" e "ESQUELETO" sem ser.

Também não existe um **STEP do SAI com as zonas internas**. As zonas só existem como modificadores dentro do projeto do Orca. Quem não usa Orca ou Bambu Studio recebe só o exterior.

**Proposta:** um pacote `SAI_final.zip` (cerca de 90 MB) numa nova Release, com:
1. os 4 projetos `.3mf` acima, renomeados (`SAI_superior.3mf`, `SAI_inferior_esq.3mf`, `SAI_inferior_dir.3mf`, `SAI_PADs.3mf`);
2. o STEP do exterior e o STEP dos PADs;
3. os STLs dos modificadores das zonas, para quem usa outro fatiador;
4. um `LEIA-ME`:
   - material: PA6-CF seco antes de imprimir, TPU 95A;
   - bico endurecido;
   - 5 paredes, camada 0,2 mm;
   - giroide 25%/20%, PADs com 40% e 3 paredes;
   - orientação: a mesma do arquivo;
   - massas e tempos;
   - aviso: estimativa, sem ensaio.

---

## 7. Segunda varredura (depois das correções)

| Conferência | Como | Resultado |
|---|---|---|
| Números dos slides | `scripts/verifica_numeros.py`: 63 números, cada um refeito a partir do JSON de origem, com o arredondamento do slide e conferindo se o texto está mesmo no slide | **63 de 63 batem** (`verificacao_numeros.json`) |
| Texto mostrado no navegador | texto renderizado dos 14 slides visíveis, procurando os valores antigos (627,33; 7–8; 1.745 g; 2,690; 144 g mais leve; R06; 450,7; NaN; undefined) | nenhum aparece |
| Valores preenchidos por script | `data-r07` na página: R$ 450,08; 1.744,5 g; 139 g | batem com o Orca |
| Gráfico do PAD | rótulos lidos na página | 450,9 N → 168,5 N · −63%, iguais ao R03 |
| Scripts que geram os dados do site | rodei de novo `r07_site_dados.py`, `conjunto_dados.py`, `estudo_custos.py` e `pad_limites.py` e comparei com os arquivos publicados | saída idêntica; só o `r07-dados.js` perde o bloco `videos`, que outro script acrescenta (valores conferidos: 93,3 kg; FS 3,89; 35,4 kg) |
| Modelos 3D do site | os 20 STL que o site mostra contra as malhas de origem (exterior `*_BASE_20`, zonas `SEM_ALMAS_SUPERIOR` e `INFERIOR_ESQ_MOD_*`, PADs `PAD95_R02_*`) | volume, caixa e faces idênticos; todas fechadas, menos a meia-peça A1_L do site (2 faces a mais, só visual: o volume é o mesmo) |
| Layout em 1536 × 730 | rolagem e texto fora do slide, nos 14 slides | nada cortado depois das correções 17 e 18 |

**Custos:** os slides usam só o material (garra R$ 450,08 + PADs R$ 21,96 + bico R$ 23,50 = R$ 495,54). O `estudo_custos.json` traz também um cenário completo, com energia e 10% de refugo: R$ 566,02 na compra e R$ 865,22 em 24 meses. Mesmo assim o SAI fica abaixo dos R$ 2.000 do Tritan.

**Ainda em aberto (precisam da equipe, não de conta):**
1. "Parada para manuseio a cada 45 min de operação" (Processo): cerca de 6 caixas/min × 45 min dá 270, não 280. Confirmar se os 45 min são a parada ou o intervalo entre paradas.
2. Critério do FS no relatório do Tritan (item 5): ruptura (11,5) ou escoamento (13,3).
3. Critério do fator de pico (von Mises 2,2 ou 1ª principal 2,7): só o ensaio de bancada decide.
4. Pacote `SAI_final.zip` para a Ajinomoto (seção 6): proposto, ainda não montado.
5. Os slides arquivados (escondidos) mantêm valores antigos; não aparecem na apresentação.
