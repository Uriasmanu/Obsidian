---
name: valida-mapeamento
description: Use when Manu pede para validar, conferir ou revisar um mapeamento de módulo (task "Teste mapeamento"), apontando para um JSON de mapeamento, script SQL, JSON de SYNC e/ou csv/Excel de origem.
---

# Valida Mapeamento

## Overview

Skill de apoio à task "Teste mapeamento" do trabalho da Manu. O objetivo é comparar um JSON de mapeamento, o script SQL, o JSON de SYNC e o .csv/Excel de origem, apontando divergências antes de considerar o mapeamento pronto.

## When to Use

- Manu pede para validar/conferir um mapeamento contra um script SQL.
- Ela cola ou aponta um conjunto (JSON de mapeamento + script SQL + .csv/Excel de origem) e pede revisão.

## Restrições

- **A skill só valida e aponta — nunca altera nenhum arquivo do mapeamento** (csv, SQL, JSON, SYNC). Nem para "limpar" o csv, encurtar mnemônico, numerar `16_M`/`16_U` ou corrigir encoding: tudo vira item `- [ ]` no relatório para a Manu corrigir. O único arquivo que a skill cria/atualiza é o relatório `.md` da validação.
- **Só pode ler arquivos dentro da pasta indicada por Manu no VSCode** (a pasta do módulo aberta/apontada). Não abrir, buscar ou ler arquivos fora dessa pasta (ex: outros módulos, outras pastas do workspace) mesmo que pareçam relevantes para comparação — se faltar algum arquivo esperado dentro da pasta indicada, perguntar para Manu em vez de procurar em outro lugar.
- **Não rodar comandos git** (ex: `git log`, `git diff`, `git show`, `git blame`) para buscar contexto, histórico ou versões anteriores de arquivo. A validação usa só os arquivos presentes na pasta indicada, exatamente como estão no momento — nunca consultar o histórico do repositório.

## Antes de Começar

**A primeira coisa a fazer, antes de qualquer pergunta ou leitura de arquivo, é checar se já existe uma doc de relatório de validação (`.md`) na raiz da pasta do módulo** — é rápido (só olhar a pasta) e evita perder tempo perguntando ou lendo arquivo à toa. Se existir, é uma segunda validação: ler essa doc inteira (Manu pode ter feito alterações e observações manuais nela — comentários, explicações, itens já marcados como corrigidos) e seguir o fluxo descrito em "Segunda Validação". O cabeçalho da doc já responde versão, protocolo e se é mapa de cliente — não perguntar de novo o que já está escrito lá, só confirmar com a Manu se mudou algo.

Se não existir doc (primeira validação), perguntar para a Manu, sempre, antes de validar qualquer coisa:

1. Qual versão do módulo está sendo validada (v1, v2, etc.).
2. Se é um mapa de cliente (para aplicar a exceção de descrição personalizada por UID, ver "Exceções").
3. Qual protocolo está sendo validado, `DNP` ou `MDB` — **só se valida um protocolo por vez**, mesmo que a pasta do módulo tenha as duas subpastas. **Só perguntar se a pasta do módulo tiver as duas subpastas (`DNP` e `MDB`)**; se só existir uma delas, usar essa direto, sem perguntar. O outro protocolo só é lido como referência para o item 12b (mnemônico igual por UUID).

Não presumir a versão nem se é mapa de cliente sozinho — essas duas sempre pergunta.

## Quick Reference — Passo a Passo

A ordem importa: primeiro fecha a consistência interna desta versão (csv ↔ script ↔ JSON), só depois compara com versão anterior (se houver), só depois valida o SYNC, e por último o relatório. **Detalhamento completo de cada item (regras, exemplos, falsos positivos) em `checklist.md`, nesta mesma pasta da skill.**

| Bloco | # | Checagem |
|---|---|---|
| A — csv ↔ script ↔ JSON desta versão | 1 | Ler os arquivos (JSON, SQL, csv/Excel de origem) |
| | 2 | Espelhamento JSON ↔ SQL (todo ID/campo bate 1:1) |
| | 3 | Mnemônicos únicos dentro do arquivo |
| | 3b | Mnemônico com no máximo 50 caracteres |
| | 3c | Mnemônico no formato `^[a-z0-9]+$` (minúsculo, sem `_`/acento) |
| | 3d | Abreviações padrão (só sugestão) |
| | 4 | Descrições únicas dentro do arquivo |
| | 5 | `E3Lib` do script == `E3Lib` do JSON de mapeamento |
| | 5b | `Imagem` == `<E3Lib>.svg`, e idêntico entre script e JSON |
| | 6 | IDs do `fl.sql` também em `GruposPadrao.sql`/`VersaoRecurso.sql`, e formato/conteúdo de `TagsVersaoMapa`/`TagsVersaoFirmware` |
| | 7 | Identificar e cruzar o csv/Excel de origem correto |
| | 7b | Nome do csv: `<nome>_<protocolo>_v<N>_<hash12>.csv`, batendo com pasta/protocolo |
| | 7c | Csv limpo (sem UUID vazio, sem linha sem classificação, sem `Privado`) e nada disso mapeado |
| | 7d | Classificado sem Tipo/Registrador → SAM Team (`#docs-mapa`) |
| | 7e | Tratamento `16_M`/`16_U` → mnemônicos numerados |
| | 8 | "Gráfico Rápido = Sim" → tipo `1537` |
| | 9 | `E3Lib` com especificidades conhecidas → avisar |
| | 10 | Encoding (caracteres corrompidos numa descrição) |
| | 10b | Csv de origem fora de UTF-8 → ponto de atenção |
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

Quando já existe uma doc de relatório (`.md`) de uma validação anterior na pasta do módulo:

1. Ler a doc inteira antes de começar a revalidar — Manu pode ter adicionado observações, explicações ou anotações manuais nos itens (ex: por que algo não foi corrigido, contexto adicional, item marcado como já resolvido).
2. Levar essas observações em consideração durante a nova validação — não ignorar nem sobrescrever sem checar o que ela escreveu.
3. Refazer todas as checagens normalmente ("Quick Reference" / `checklist.md`).
4. Por último, **atualizar a mesma doc** (não criar um relatório novo do zero): manter os checkboxes já marcados e as observações da Manu, atualizar o status dos itens que foram corrigidos, e adicionar quaisquer novos itens incorretos encontrados nessa rodada.

## Formato do Relatório Final

Ao terminar todas as checagens, sempre fechar com um relatório único (não é opcional, mesmo que a divergência pareça pequena):

- **OBRIGATÓRIO: todo relatório abre com o cabeçalho padrão abaixo — nunca pular essa parte, mesmo em revalidação de doc existente.** Formato:
  - Título `# Validação de Mapeamento — Módulo <NOME> (<versão> / <protocolo>)` (ex: `# Validação de Mapeamento — Módulo MDJ (V2 / MDB)`).
  - Uma linha logo abaixo indicando o contexto da validação: se é a primeira validação do módulo (sem versão anterior para comparar) ou uma revalidação, e se é mapeamento de cliente específico ou não (ver "Exceções").
  - Uma lista `Arquivos analisados:` com todos os arquivos usados na validação (SQL, JSON, csv/Excel fonte, SYNC), com o caminho relativo (ex: `MDB/MDJ-fl.sql`).
  - Um separador (`---`) antes do corpo do relatório.
- **Organizar por arquivo** (ex: `fl.sql`, `GruposPadrao.sql`, `VersaoRecurso.sql`, JSON de mapeamento, JSON de SYNC, csv/Excel) — Manu depois vai comentar os problemas no Pull Request do Azure DevOps, e lá a navegação é arquivo por arquivo, não por categoria de regra.
- **O relatório inteiro é uma checklist Markdown, sem parágrafos soltos de texto explicando "nada de errado encontrado"**: cada checagem feita (de cada item do "Quick Reference"/`checklist.md` aplicável àquele arquivo) vira uma linha de checklist, `- [x]` quando validado e OK, `- [ ]` quando é um problema/divergência. Tudo é checklist, item por item — nunca um parágrafo corrido explicando o que foi validado.
- **Dentro de cada arquivo, ordem fixa: todos os `- [ ]` (problemas) primeiro, depois todos os `- [x]` (OK)** — quem for comentar no PR precisa achar os problemas de cara, sem escanear item OK no meio.
  - `- [x] **<o que foi checado>**: <trecho/valor relevante> — <resultado, por que está OK>.`
  - `- [ ] **<o que foi checado>**: <trecho literal do arquivo, Ctrl+F> — <o problema, valor esperado x valor encontrado>.`
  - Isso vale mesmo quando está tudo OK num arquivo: listar cada checagem feita como `- [x]` em vez de um subtítulo tipo "Nenhum problema encontrado" seguido de texto corrido.
- **Para cada item (marcado ou não), incluir um trecho exato e literal do arquivo (um `Ctrl+F` funcional)** — ex: a linha inteira do `DECLARE @ModuloId ...`, o nome exato do campo/mnemônico, o trecho de JSON. Não descrever só "o campo X está errado" ou "campo X confere": copiar o texto como aparece no arquivo.
- Junto do trecho, dizer o que é o problema e qual o valor esperado x valor encontrado (itens `- [ ]`), ou por que está OK (itens `- [x]`).
- **Linguagem simples e direta, fácil de entender de primeira** — frases curtas, sem palavra rebuscada/técnica desnecessária nem jargão de validação. Quem vai ler é a própria Manu comentando no PR, não precisa soar formal.
- **OBRIGATÓRIO: ao citar qualquer trecho do csv/Excel de origem, montar uma tabela Markdown usando o `;` do csv como separador de coluna** (cabeçalho + linha(s) relevante(s)) — nunca colar a linha crua com `;` direto no relatório.
- **Não incluir checagem de algo estrutural/esperado que não faz parte da regra de validação daquele arquivo** — ex: não relatar "fl.json não possui `hashCommitMap`" como item `[x]`, porque esse campo já é sabidamente exclusivo do SYNC (não é uma checagem, é só um fato conhecido de estrutura). Só vira item de checklist algo que de fato foi comparado/cruzado entre arquivos.
- **Caso enquadrado numa exceção (ver "Exceções") não vira item de checklist no relatório** — não é uma divergência, então não gera `- [x]` nem `- [ ]`, mesmo com nota de "exceção aplicada". Se for útil registrar que foi conferido, no máximo uma menção curta em texto corrido perto do item relacionado, nunca como linha de checklist própria.
- **O relatório tem que ser salvo como um arquivo `.md` dentro da pasta do módulo** (não é só mostrar no chat) — ele serve de guia depois para conferir se as correções apontadas foram feitas.
- **Salvar na raiz da pasta do módulo, fora das subpastas de protocolo** (ex: `MDB`, `DNP`, `SYNC`) — não dentro delas.

## Common Mistakes

- ID declarado no script (`DECLARE @ModuloId ...`) diferente do valor no JSON.
- ID divergente entre versões (v1 vs v2 etc.) quando deveria ser o mesmo.
- Campo ou ID presente no SQL mas ausente (ou diferente) no JSON, quebrando o espelhamento.
- Mnemônico repetido dentro do mesmo arquivo.
- Descrição repetida dentro do mesmo arquivo.
- Mnemônico de um UID que já existia na v1 mudou na v2.
- Mnemônico do mesmo UUID diferente entre MDB e DNP.
- Mnemônico novo com mais de 50 caracteres, com maiúscula, `_`, acento ou caractere especial.
- Csv de origem com linha em branco / UUID vazio, linha sem classificação ou linha `Privado` — ou alguma delas mapeada no SQL/JSON/SYNC.
- Nome do csv sem protocolo/versão/hash, ou com protocolo/versão diferente da pasta.
- Linhas com tratamento `16_M`/`16_U` com mnemônico sem numeração (ex: dois `indnumeroserie` em vez de `indnumeroserie1`/`indnumeroserie2`).
- **Corrigir o arquivo em vez de só apontar** — a skill nunca edita csv/SQL/JSON/SYNC (ver "Restrições").
- `hashCommitMap` do JSON de SYNC diferente do hash presente no nome do csv/Excel de origem ou do zip.
- `identifier` (JSON de SYNC) ou `E3Lib` (JSON de mapeamento) diferente do `E3Lib` do script.
- ID presente no `fl.sql` mas faltando em `GruposPadrao.sql` e/ou `VersaoRecurso.sql`.
- Subtipo/categoria divergente entre versões, ou incorreto quando é v1.
- .csv/Excel de origem divergente do SQL e/ou do JSON.
- Confundir o `modulo.csv` genérico ou um export tipo `<E3Lib>.csv` (ex: `BM.csv`, tags OPC/Archestra) com o csv/Excel de origem real (o de origem tem o hash de commit no nome, colunas `UUID` e `Mnemônico`).
- Reportar acento "trocado" como erro de encoding quando na verdade é só leitura em UTF-8 de um csv que está em Windows-1252/ISO-8859-1 (normal para esse tipo de export).
- Campo com "Gráfico Rápido = Sim" no csv/Excel mas tipo diferente de `1537` no SQL/JSON.
- Arquivo `sigma-sync-import` fora da pasta `SYNC`, mais de 1 arquivo de SYNC na mesma versão, ou conteúdo do SYNC divergente do SQL.
- Problema de encoding numa descrição (ex: `?` isolado ou outro caractere estranho no meio do texto).
- **Esquecer o cabeçalho do relatório** (título com módulo/versão/protocolo, linha de contexto e lista `Arquivos analisados:`) — ver "Formato do Relatório Final". Isso é obrigatório em todo relatório, não só um extra opcional.
- Demais erros comuns ainda a ser detalhados por ela.

## Fora de Escopo

Os arquivos abaixo podem aparecer na pasta do módulo, mas **não fazem parte da validação desta skill** — não precisam ser cruzados com SQL/JSON/csv:

- `slave.json` (config de simulador Modbus).
- `tbl_a_IED.csv`, `tbl_d_IED.csv`, `tbl_h_IED.csv`, `tbl_s_IED.csv`.
- `alarms_*.csv`.

Na tabela `VersaoRecurso`, os tipos de recurso `Ativo` (5), `Instalacao` (6), `Empresa` (7) e `Sistema` (8) **não são versionados** — ausência deles no `VersaoRecurso.sql` é esperada, não é erro/faltando.

## Exceções

- **Mapas de cliente** (Manu avisa explicitamente quando o mapeamento é de um cliente específico): pode acontecer, raramente, de v1 e v2 terem campos com o mesmo ID mas descrição personalizada para aquele cliente. Isso **não é divergência** — não reportar como erro quando for esse caso.
- **Csv de origem em Windows-1252/ISO-8859-1**: ler assumindo UTF-8 e ver acentos trocados **não é um problema de encoding real nos textos** — os bytes estão corretos, só precisa ler com a codificação certa. Não reportar os acentos como corrupção (item 10); a codificação do arquivo em si fora de UTF-8 é só o ponto de atenção do item 10b.
- **Mnemônico herdado acima de 50 caracteres**: se veio igual de versão/protocolo anterior (mesmo UUID), é ponto de atenção do item 3b, não erro — a regra de mnemônico estável (item 12/12b) tem prioridade.
- **Evolução normal entre v1 → v2**: o que precisa se manter estável é o **mnemônico de cada UID já existente** (regra fixa, ver item 12 do `checklist.md`, Bloco B). Já é esperado e normal que a v2 tenha: campos novos que não existiam na v1, mudança de unidade de medida de um campo existente, ou mudança de descrição de um campo existente. Essas mudanças **não são erro** — só reportar como divergência se o mnemônico de um UID que já existia mudou.
- **Linhas do tipo "Comando" no csv/Excel de origem não entram nos arquivos de mapeamento.** Quando a coluna "Tratamento"/tipo do csv indica que a linha é um comando (ex: mnemônicos `cmdreset...`, tipicamente `RW`/`Holding register` sem leitura associada), é esperado e normal que esse UUID **não** apareça no `fl.sql`, `fl.json`, `GruposPadrao.sql`, `VersaoRecurso.sql` nem no SYNC — comandos não fazem parte deste mapeamento. **Não reportar a ausência desses UUIDs como erro/faltando.**
- **Trechos de debug/comando não fazem parte do script final**: é normal e esperado que o SQL não contenha comandos de debug (ex: `SELECT`, `PRINT` avulsos usados só para conferir valor durante o desenvolvimento) nem outros comandos auxiliares que não sejam parte da lógica de mapeamento. A ausência desses trechos nos arquivos **não é erro** — não reportar como divergência ou item faltante.
- **Campos de metadado do framework não têm origem no csv/Excel** — mnemônicos como `VersaoProduto`, `VersaoMapa`, `HashCommitMapa` e `DataHoraUltimaLeituraSensor` (e equivalentes) existem no `fl.sql`/`fl.json` mas são gerados/controlados pelo próprio framework, não dados do equipamento. **Não reportar a ausência deles no csv como erro/faltando.**
  - No SYNC, a maioria desses campos **tem sim equivalente** e deve ser conferida normalmente: `VersaoMapa` ↔ `resourceVersionValue`/`productVersion` e `HashCommitMapa` ↔ `hashCommitMap` (ver itens 16/17 do `checklist.md`, Bloco C — nomes diferentes, mas é o mesmo dado). Só `DataHoraUltimaLeituraSensor` realmente **não tem** e nunca vai ter equivalente no JSON de SYNC (vem do software em tempo de execução, não é dado estático de mapeamento) — só esse pode ter a ausência no SYNC ignorada, sem virar item de checklist.
- **Equipamento que não é produto Treetech** (sem branch/versão no Bitbucket): `TagsVersaoMapa` padrão esperado é `v1-MDB` ou `v1-DNP` (conforme o protocolo), e `TagsVersaoFirmware` padrão é `v1[fw1.0]`. Não reportar como erro/faltando quando o `VersaoRecurso.sql` desse tipo de equipamento tiver só esses valores.

## Pendências

- Detalhar o restante da lista de erros comuns/checklist manual (seção "Common Mistakes").
