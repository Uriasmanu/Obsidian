---
name: valida-mapeamento
description: Use when o usuário pede para validar, conferir ou revisar um mapeamento de módulo (task "Teste mapeamento"), apontando para um JSON de mapeamento, script SQL, JSON de SYNC e/ou csv/Excel de origem.
---

# Valida Mapeamento

## Overview

Skill de apoio à task "Teste mapeamento" do trabalho do usuário. O objetivo é comparar um JSON de mapeamento, o script SQL, o JSON de SYNC e o .csv/Excel de origem, apontando divergências antes de considerar o mapeamento pronto.

## When to Use

- O usuário pede para validar/conferir um mapeamento contra um script SQL.
- Ela cola ou aponta um conjunto (JSON de mapeamento + script SQL + .csv/Excel de origem) e pede revisão.

## Restrições

- **A skill só valida e aponta — nunca altera nenhum arquivo do mapeamento** (csv, SQL, JSON, SYNC). Nem para "limpar" o csv, encurtar mnemônico, numerar `16_M`/`16_U` ou corrigir encoding: tudo vira item `- [ ]` no relatório para o usuário corrigir. O único arquivo que a skill cria/atualiza é o relatório `.md` da validação.
- **Só pode ler arquivos dentro da pasta indicada pelo usuário no VSCode** (a pasta do módulo aberta/apontada). Não abrir, buscar ou ler arquivos fora dessa pasta (ex: outros módulos, outras pastas do workspace) mesmo que pareçam relevantes para comparação — se faltar algum arquivo esperado dentro da pasta indicada, perguntar para o usuário em vez de procurar em outro lugar.
- **Não rodar comandos git** (ex: `git log`, `git diff`, `git show`, `git blame`) para buscar contexto, histórico ou versões anteriores de arquivo. A validação usa só os arquivos presentes na pasta indicada, exatamente como estão no momento — nunca consultar o histórico do repositório.

## Antes de Começar

1. **Antes de qualquer pergunta ou leitura de arquivo, olhar se já existe um relatório `Validacao-Mapeamento-*.md` na pasta indicada no VSCode (ou em subpastas dela)** — local e nome padrão em `report-template.md`. Se achar um fora do padrão, usar esse mesmo e avisar o usuário. Se existir, é uma segunda validação: ler a doc inteira e seguir "Segunda Validação". O cabeçalho da doc já responde versão, protocolo e se é mapa de cliente — não perguntar de novo, só confirmar com o usuário se mudou algo.
2. Se não existir (primeira validação), deduzir pelo caminho da pasta:
   - **Versão**: a pasta de versão no caminho (ex: `.../<MODULO>/v1/MDB` → `v1`).
   - **Protocolo**: se só existe a subpasta `MDB` ou só `DNP`, é essa. **Só se valida um protocolo por vez**; o outro protocolo só é lido como referência para o item 12b.
3. Ainda na primeira validação, fazer **todas as perguntas numa única chamada, com opções prontas** (AskUserQuestion):
   - **É mapa de cliente?** (sim / não) — sempre perguntar, nunca presumir. Mapa de cliente = equipamento que não é produto Treetech (define as exceções E1 e E8).
   - **Versão**: confirmar a deduzida (ex: `v1 (deduzida do caminho)` / outra).
   - **Protocolo** (`MDB` / `DNP`): só quando a pasta tem as duas subpastas.

## Automação — rodar primeiro

As checagens mecânicas estão em `valida.py`, nesta pasta da skill. Rodar antes de ler os arquivos grandes e usar a saída como base do relatório:

```
python valida.py <pasta_protocolo> [--anterior <pasta_protocolo_versao_anterior>] [--outro-protocolo <pasta_outro_protocolo>]
```

- Se `python` abrir a Microsoft Store, usar `%LOCALAPPDATA%\Programs\Python\Python313\python.exe`.
- Passar `--anterior`/`--outro-protocolo` só com pastas que estão dentro da pasta indicada pelo usuário (ver "Restrições").
- A saída vem agrupada por arquivo: `[ERRO]` vira `- [ ]`, `[OK]` vira `- [x]`. `[ATENCAO]`/`[SUGESTAO]` viram `- [ ]` marcados como ponto de atenção/sugestão, e `[INFO]` não vira item.
- Cada achado termina com `{chave: <item>/<tipo de arquivo>/<slug>}`. A chave não muda entre rodadas (não depende de nome de arquivo, número nem valor) — copiar para a linha `Chave:` do item rastreável no relatório.
- Na revalidação, rodar com `--completo` para listar todos os trechos sem corte (necessário para detectar correção parcial).
- O script não substitui o julgamento. Continua manual: aplicar as exceções E1–E8, confirmar subtipo/categoria na v1 (item 13), ler a doc anterior na revalidação e copiar o trecho literal (Ctrl+F) de cada item com grep direcionado. Nunca ler os `.sql`/`.json` inteiros.

## Quick Reference — Passo a Passo

A ordem importa: primeiro fecha a consistência interna desta versão (csv ↔ script ↔ JSON), só depois compara com versão anterior (se houver), só depois valida o SYNC, e por último o relatório. **Detalhamento completo de cada item (regras, exemplos, falsos positivos) em `checklist.md`, nesta mesma pasta da skill.**

| Bloco | # | Checagem |
|---|---|---|
| A — csv ↔ script ↔ JSON desta versão | 1 | Ler os arquivos (JSON, SQL, csv/Excel de origem) |
| | 2 | Espelhamento JSON ↔ SQL (todo ID/campo bate 1:1) |
| | 3 | Mnemônicos únicos dentro do arquivo |
| | 3b | Mnemônico com no máximo 50 caracteres |
| | 3c | Mnemônico `^[a-z0-9]+$` sem o prefixo do software (`get_`); PascalCase só em mapa antigo, nunca misturado |
| | 3d | Abreviações padrão (só sugestão) |
| | 4 | Descrições únicas dentro do arquivo |
| | 5 | `E3Lib` do script == `E3Lib` do JSON de mapeamento |
| | 5b | `Imagem` == `<E3Lib>.svg`, e idêntico entre script e JSON |
| | 6 | IDs do `fl.sql` também em `GruposPadrao.sql`/`VersaoRecurso.sql`, e formato/conteúdo de `TagsVersaoMapa`/`TagsVersaoFirmware` |
| | 7 | Identificar o csv/Excel de origem pelo nome e cruzar |
| | 7b | Nome do csv: `<nome>_<protocolo>_v<N>_<hash12>.csv`, batendo com pasta/protocolo |
| | 7c | Csv limpo (sem UUID vazio, sem linha sem classificação, sem `Privado`) e nada disso mapeado |
| | 7d | Classificado sem Tipo/Registrador → SAM Team (`#docs-mapa`) |
| | 7e | Tratamento `16_M`/`16_U` → mnemônicos numerados |
| | 8 | "Gráfico Rápido = Sim" → tipo `1537` |
| | 9 | `E3Lib` com especificidades conhecidas → avisar |
| | 10 | Encoding (caracteres corrompidos numa descrição) |
| B — comparação com versão anterior / outro protocolo | 11 | IDs idênticos entre versões |
| | 12 | Mnemônico estável entre versões (UID já existente) |
| | 12b | Mnemônico igual entre protocolos (MDB ↔ DNP) para o mesmo UUID |
| | 13 | Subtipo/categoria iguais entre versões |
| C — SYNC (validar por último) | 14 | Localizar SYNC e espelhar contra o SQL |
| | 15 | `identifier` (SYNC) == `E3Lib` |
| | 16 | `hashCommitMap` (SYNC) == hash do csv/zip |
| | 17 | `resourceVersionValue`/`productVersion` (SYNC) == `VersaoMapa` |
| D — Relatório | 18 | Gerar o relatório final |

## Segunda Validação

Quando já existe uma doc de relatório (`.md`) de uma validação anterior na pasta do módulo. Formato dos itens rastreáveis (ID, status, `Onde:`, `Chave:`, `Depende de:`, `Histórico:`) em `report-template.md`.

1. **Ler a doc inteira** e montar a lista de itens rastreáveis: ID, status, `Onde:`, `Chave:`, `Depende de:`, trechos encontrados e `Obs.:`. A rodada nova é `R<última + 1>` do painel.
   - Se a doc for do formato antigo (sem IDs), converter primeiro: dar ID a cada `- [ ]`, status 🔴 `aberto`, `Histórico: R1 aberto`, e montar o painel com a R1.
2. **Status de PR**: se o usuário disser na conversa quais itens comentou (ex: "comentei CSV-01 e VR-03"), mudar esses para 💬 `no-pr` e preencher `PR:` se ele passar o link. Status que ele mudou à mão na doc prevalece.
3. **Rodar `valida.py --completo`** e refazer as checagens manuais ("Quick Reference" / `checklist.md`).
4. **Reconferir cada item em aberto** (🔴, 💬, 🟡, 🔁), com a chave e com grep no `Onde:`:
   - Chave some da saída ou aparece só como `[OK]`, **e** o trecho do `Onde:` não é mais encontrado → ✅ `resolvido na R<n>`. Vira `- [x]`, com uma linha `Agora:` trazendo o trecho literal atual.
   - Chave continua, mas com menos trechos que antes → 🟡 `parcial`. Atualizar a lista só com o que falta e registrar `parcial (<faltam> de <antes>)`.
   - Chave continua com os mesmos trechos → mantém o status e registra `R<n> continua`.
   - `Chave: manual` → decidir só pelo grep do `Onde:` e pela checagem manual do item.
   - Item com `Depende de:` → reconferir mesmo que a chave pareça igual; se a causa raiz foi resolvida, o derivado costuma sumir junto.
   - Se o `Onde:` sumiu mas a chave continua (ex: o valor errado mudou para outro valor errado), **não é resolvido**: atualizar `Encontrado:` e `Onde:` e manter aberto.
5. **Itens já fechados**: ✅ cuja chave/`Onde:` voltou → 🔁 `reaberto` (volta a `- [ ]`). ⚪ `nao-corrigir` não é reaberto; se o problema sumiu, vira ✅.
6. **Achado novo** (chave que não existe na doc) → item novo com o próximo ID livre do prefixo, `Histórico: R<n> novo`.
7. **Atualizar a mesma doc** (nunca criar outra): linha de contexto `Revalidação (R<n>)`, `Arquivos analisados:` (o csv pode ter nome/hash novo — atualizar o título da seção e registrar o nome antigo no `Histórico:` do item afetado), nova linha no painel, reordenar cada seção (`- [ ]` por ID, depois `- [x]`). Nunca apagar item, `Obs.:` ou `PR:`.
8. Na resposta ao usuário, resumir a rodada: resolvidos, parciais, reabertos e novos, por ID.

## Relatório Final

Obrigatório ao fim de toda validação, mesmo que a divergência pareça pequena. **Formato, regras e esqueleto pronto em `report-template.md`, nesta mesma pasta da skill** — preencher o esqueleto, não montar o formato de cabeça.

## Common Mistakes

- **Corrigir o arquivo em vez de só apontar** — ver "Restrições".
- **Esquecer o cabeçalho do relatório** (título, linha de contexto, `Arquivos analisados:`) — obrigatório em todo relatório, inclusive revalidação.
- Confundir o `modulo.csv` genérico ou um export `<E3Lib>.csv` (tags OPC/Archestra) com o csv de origem real — ver item 7.

## Fora de Escopo

**Não abrir** os arquivos abaixo, nem para "dar uma olhada" — não fazem parte da validação:

- `slave.json` (config de simulador Modbus).
- `tbl_a_IED.csv`, `tbl_d_IED.csv`, `tbl_h_IED.csv`, `tbl_s_IED.csv`.
- `alarms_*.csv`.
- `modulo.csv` genérico e `<E3Lib>.csv` (export de tags OPC/Archestra).
- Qualquer outro csv cujo nome não segue o padrão do csv de origem (item 7).

Na tabela `VersaoRecurso`, os tipos de recurso `Ativo` (5), `Instalacao` (6), `Empresa` (7) e `Sistema` (8) **não são versionados** — ausência deles no `VersaoRecurso.sql` é esperada, não é erro/faltando.

## Exceções

Casos abaixo não são divergência. O `checklist.md` cita cada um pelo código (E1, E2...).

- **E1 — Mapas de cliente** (o usuário avisa explicitamente quando o mapeamento é de um cliente específico): pode acontecer, raramente, de v1 e v2 terem campos com o mesmo ID mas descrição personalizada para aquele cliente. Isso **não é divergência** — não reportar como erro quando for esse caso.
- **E3 — Mnemônico herdado acima de 50 caracteres**: se veio igual de versão/protocolo anterior (mesmo UUID), é ponto de atenção do item 3b, não erro — a regra de mnemônico estável (item 12/12b) tem prioridade.
- **E4 — Evolução normal entre v1 → v2**: o que precisa se manter estável é o **mnemônico de cada UID já existente** (item 12). É esperado e normal que a v2 tenha campos novos, mudança de unidade de medida ou mudança de descrição de um campo existente — **não é erro**.
- **E5 — Linhas do tipo "Comando" ou "Debug" no csv/Excel de origem não entram nos arquivos de mapeamento.** Quando a coluna "Classificação"/"Tratamento" indica comando (ex: mnemônicos `cmdreset...`, tipicamente `RW`/`Holding register` sem leitura associada) ou debug, é esperado que esse UUID **não** apareça no `fl.sql`, `fl.json`, `GruposPadrao.sql`, `VersaoRecurso.sql` nem no SYNC. **Não reportar a ausência desses UUIDs como erro/faltando.**
- **E6 — Trechos de debug/comando não fazem parte do script final**: é normal que o SQL não contenha comandos de debug (ex: `SELECT`, `PRINT` avulsos) nem outros comandos auxiliares fora da lógica de mapeamento. A ausência deles **não é erro**.
- **E7 — Campos de metadado do framework não têm origem no csv/Excel** — mnemônicos como `VersaoProduto`, `VersaoMapa`, `HashCommitMapa` e `DataHoraUltimaLeituraSensor` (e equivalentes) existem no `fl.sql`/`fl.json` mas são gerados pelo framework. **Não reportar a ausência deles no csv como erro/faltando.**
  - No SYNC, metadados e alarmes do framework (ex: `@AlarmeRedeDigitalId`) deveriam aparecer em `fields`: a ausência vira ponto de atenção (`Atenção:`) no item 14, não erro. `VersaoMapa`/`HashCommitMapa` também são conferidos nos itens 16/17.
- **E8 — Mapa de cliente (equipamento que não é produto Treetech, sem branch/versão no Bitbucket)** — vale quando a resposta a "É mapa de cliente?" foi sim: `TagsVersaoMapa` padrão esperado é `v1-MDB` ou `v1-DNP` (conforme o protocolo), e `TagsVersaoFirmware` padrão é `v1[fw1.0]`. Não reportar como erro/faltando quando o `VersaoRecurso.sql` desse tipo de equipamento tiver só esses valores.
- **E9 — Imagem em mapa de cliente** — em mapas de cliente, o campo `Imagem` não segue o padrão `<E3Lib>.svg`: é esperado que use a imagem de um módulo Treetech existente. Não reportar como erro quando o valor de `Imagem` não corresponder à `E3Lib` do equipamento (item 5b).

## Pendências

- Detalhar o restante da lista de erros comuns/checklist manual (seção "Common Mistakes").
