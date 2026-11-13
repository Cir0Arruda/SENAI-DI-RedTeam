# Garra SAI: arquivos finais para imprimir

Estes são os arquivos 3D da garra SAI que entraram nos cálculos do projeto. A versão é a **R07 sem almas**: o exterior é igual ao da garra original e só muda o miolo da peça.

**Nada aqui foi impresso nem testado em bancada.** Os números de resistência são estimativas por simulação. O teste de bancada é o próximo passo.

## Por onde começar

Abra os 4 projetos no **OrcaSlicer** (2.x) ou no **Bambu Studio**. Eles já trazem a impressora, o material, as paredes, o preenchimento e as zonas internas. Basta fatiar.

| Arquivo | Peça | Material | Preenchimento | Paredes | Peso da peça | Tempo (K1 Max) |
|---|---|---|---|---|---|---|
| `SAI_superior_PA6-CF_giroide25.3mf` | peça de cima (vai no robô) | PA6-CF | giroide 25% + 4 zonas | 5 | 666,4 g | 34,2 h |
| `SAI_inferior_esq_PA6-CF_giroide20.3mf` | asa esquerda | PA6-CF | giroide 20% + 3 zonas | 5 | 383,2 g | 20,5 h |
| `SAI_inferior_dir_PA6-CF_giroide20.3mf` | asa direita | PA6-CF | giroide 20% + 3 zonas | 5 | 383,2 g | 20,5 h |
| `SAI_PADs_TPU95A_giroide40.3mf` | 8 PADs (meias-peças) | TPU 95A | giroide 40% | 3 | 93,1 g | 11,0 h |
| **Total** | | | | | **1.525,9 g** | **86,2 h** |

Os pesos e tempos são a estimativa do OrcaSlicer numa Creality K1 Max, sem contar suporte. Em todas as peças: bico 0,4 mm, camada 0,2 mm, 6 camadas de topo e 6 de fundo.

## As zonas internas

Dentro da peça, cada zona tem um preenchimento diferente. No fatiador, isso aparece como **modificador**: uma forma invisível que muda o preenchimento só ali dentro. Os modificadores não são impressos como peça separada, e o exterior não muda.

| Peça | Zona | Preenchimento | Para quê |
|---|---|---|---|
| Superior | tubos dos furos | 100% | os parafusos apertam em material maciço |
| Superior | colar da flange do robô | 55% | a raiz, onde a garra é mais exigida |
| Superior | ressaltos parafusados | 35% | onde a garra recebe as batidas |
| Superior | assento em volta dos ressaltos | 20% | transição para o resto da peça |
| Inferiores | tubos dos furos | 100% | parafusos |
| Inferiores | ressaltos e pés das ventosas | 35% | apoio das ventosas e da junta |
| Inferiores | assento | 20% | transição |

## Outras pastas

- `stl/pecas/`: as peças em STL, para quem usa outro fatiador: as 3 da garra e os 8 PADs.
- `stl/zonas/`: as zonas internas em STL. Elas usam as mesmas coordenadas dos STL de `stl/pecas/`: cada zona já está no lugar certo dentro da sua peça. Em outro fatiador, importe a peça e as zonas dela juntas, como um objeto só, sem centralizar nem mover nenhuma. Depois marque cada zona como **modificador** e dê o preenchimento do nome do arquivo. Só o STL da peça, sem as zonas, sai com o preenchimento padrão do fatiador, diferente do que foi calculado.
- `cad/SAI_garra_montada_3pecas_8PADs.step`: CAD da garra montada (3 peças e 8 PADs, 11 corpos), exportado do Autodesk Fusion. Serve para encaixe e desenho. As zonas internas não estão no STEP: elas só existem no fatiador.
- `cad/SAI_PADs_8_pecas.step`: os 8 PADs separados.
- `manifesto.json`: o que foi conferido em cada arquivo, com o SHA-256 de cada um.

## Antes de imprimir

1. **Bico de aço endurecido.** A fibra de carbono gasta o bico de latão. O Orca avisa isso ao fatiar.
2. **Secar o PA6-CF** antes de imprimir (ele puxa umidade do ar) e guardar seco.
3. **Mesma posição do arquivo.** As camadas ficam na direção usada nos cálculos. Girar a peça muda a resistência.
4. **Não mexer no exterior.** Ele é igual ao da garra original e encaixa no robô e nas ventosas.
5. O perfil do filamento é o "Bambu PA6-CF". Se usar outra marca, ajuste a temperatura pela ficha do fabricante.

## De onde vêm os números

- **Conferência deste pacote:** `dados/scripts/sai_pacote_final.py`. O script copia os arquivos, confere material, paredes, preenchimento e cada zona contra o STL de origem, confere que cada zona em STL fica no mesmo lugar da peça que no projeto, e que todas as malhas estão fechadas. Para conferir de novo: `python dados/scripts/sai_pacote_final.py --conferir`.
- **Resistência da garra montada:** o FE próprio do projeto (Python, voxels de 3 mm) usou esta mesma versão (`R07_SEM`): as mesmas zonas, giroide 25% e 20%, 5 paredes e a resistência entre camadas. Resultado: 24 kg numa asa dão FS 3,89, e a garra aguentaria cerca de 93 kg numa asa (`dados/montagem/montagem_R07_SEM.json`).
- **Autodesk Fusion:** comparou o PA6-CF e o Tritan na peça superior maciça. Não considerou o preenchimento (`dados/REVISAO_SIMULACOES.md`, seção 5).
- **PAD:** as forças vêm de um modelo de molas (estimativa), não do Fusion.
- **Fatiados com G-code** (só para a K1 Max): Release `dados-2026-11-12`, arquivo `orca_fatiados_R07.zip` (`R07_SEM_SUPERIOR_R06_FATIADO.3mf`, `INFERIOR_ESQ_B20_R06_FATIADO.3mf` e `INFERIOR_DIR_B20_R06_FATIADO.3mf`). O "R06" no nome é do script de fatiamento: a geometria é a R07. Os PADs fatiados estão em `orca_fatiados_R04.zip` (`PAD_K1MAX_FATIADO_REFERENCIA.3mf`, giroide 40%, 3 paredes, 11,0 h).
