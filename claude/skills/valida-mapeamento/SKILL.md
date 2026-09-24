---
name: valida-mapeamento
description: Use when Manu pede para validar um mapeamento (task "Teste mapeamento") — conferir consistência entre um JSON de mapeamento e o script SQL correspondente.
---

# Valida Mapeamento

## Overview

Skill de apoio à task "Teste mapeamento" do trabalho da Manu. O objetivo é comparar um JSON de mapeamento, o script SQL, o JSON de SYNC e o .csv/Excel de origem, apontando divergências antes de considerar o mapeamento pronto.

## When to Use

- Manu pede para validar/conferir um mapeamento contra um script SQL.
- Ela cola ou aponta um conjunto (JSON de mapeamento + script SQL + .csv/Excel de origem) e pede revisão.

## Restrições

- **Só pode ler arquivos dentro da pasta indicada por Manu no VSCode** (a pasta do módulo aberta/apontada). Não abrir, buscar ou ler arquivos fora dessa pasta (ex: outros módulos, outras pastas do workspace) mesmo que pareçam relevantes para comparação — se faltar algum arquivo esperado dentro da pasta indicada, perguntar para Manu em vez de procurar em outro lugar.
- **Não rodar comandos git** (ex: `git log`, `git diff`, `git show`, `git blame`) para buscar contexto, histórico ou versões anteriores de arquivo. A validação usa só os arquivos presentes na pasta indicada, exatamente como estão no momento — nunca consultar o histórico do repositório.

## Antes de Começar

**A primeira coisa a fazer, antes de qualquer pergunta ou leitura de arquivo, é checar se já existe uma doc de relatório de validação (`.md`) na raiz da pasta do módulo** — é rápido (só olhar a pasta) e evita perder tempo perguntando ou lendo arquivo à toa. Se existir, é uma segunda validação: ler essa doc inteira (Manu pode ter feito alterações e observações manuais nela — comentários, explicações, itens já marcados como corrigidos) e seguir o fluxo descrito em "Segunda Validação". O cabeçalho da doc já responde versão, protocolo e se é mapa de cliente — não perguntar de novo o que já está escrito lá, só confirmar com a Manu se mudou algo.

Se não existir doc (primeira validação), perguntar para a Manu, sempre, antes de validar qualquer coisa:

1. Qual versão do módulo está sendo validada (v1, v2, etc.).
2. Se é um mapa de cliente (para aplicar a exceção de descrição personalizada por UID, ver "Exceções").
3. Qual protocolo está sendo validado, `DNP` ou `MDB` — **só se valida um protocolo por vez**, mesmo que a pasta do módulo tenha as duas subpastas.

Não presumir nenhuma dessas três coisas sozinho.

## Passo a Passo de Validação

A ordem importa: primeiro fecha a consistência interna desta versão (csv ↔ script ↔ JSON), só depois compara com versão anterior (se houver), só depois valida o SYNC, e por último o relatório.

### Bloco A — csv ↔ script ↔ JSON desta versão

1. **Ler os arquivos.** JSON de mapeamento e script SQL (`fl.sql`, `GruposPadrao.sql`, `VersaoRecurso.sql`) do protocolo escolhido, mais o .csv/Excel de origem.
2. **Espelhamento JSON ↔ SQL.** Todo campo e todo ID do SQL devem aparecer, idênticos, no JSON de mapeamento (e vice-versa) — não é só "parecido", tem que bater 1:1. Extrair todo `DECLARE @XxxId ... = 'valor'` do script (`@ModuloId`, `@CampoIdN`, `@AlarmeIdN`, etc.) e conferir se o mesmo ID aparece no JSON.
3. **Mnemônicos únicos dentro do arquivo.** Nenhum mnemônico pode se repetir dentro do mesmo arquivo. **Se encontrar duplicidade, não resolver sozinho** (ex: não inventar um sufixo tipo "2" para desempatar) — só reportar para a Manu avaliar.
4. **Descrições únicas dentro do arquivo.** Mesma regra do item 3, aplicada às descrições em vez dos mnemônicos: nenhuma repetida dentro do arquivo, e não resolver duplicidade sozinho, só reportar.
5. **E3Lib.** O valor do `E3Lib` do script tem que ser idêntico ao `E3Lib` do JSON de mapeamento.
6. **IDs no GruposPadrao/VersaoRecurso.** Todos os IDs existentes no `fl.sql` (ModuloId + CampoIds + AlarmeIds) têm que constar também em `GruposPadrao.sql` e em `VersaoRecurso.sql`.
7. **Identificar e cruzar o csv/Excel de origem.** É o arquivo que traz o hash de commit no nome ou o arquivo com o mesmo nome do csv dentro da pasta zipada — **não é o `modulo.csv` genérico, nem um arquivo com nome igual ao `E3Lib`** (ex: `BM.csv`). Esse tipo costuma ser export de tags OPC/Archestra (colunas como `ObjectType;Name;AdviseType;...AllowRead;AllowWrite`), sem UUID, sem "Mnemônico" e sem "Gráfico Rápido" — para confirmar que achou o arquivo certo, checar se ele tem colunas `UUID` e `Mnemônico`. Depois de identificado, cruzar com SQL e JSON — os três têm que bater entre si. **Atenção ao formato do UUID**: no csv costuma vir sem hífen (`1ca40722324346a1b92e56270fd35ea7`), SQL/JSON com hífen (`1ca40722-3243-46a1-b92e-56270fd35ea7`) — mesmo valor, formatação diferente; normalizar removendo hífens dos dois lados antes de comparar, senão dá falso positivo.
8. **Gráfico Rápido → tipo 1537.** Se a coluna "Gráfico Rápido" do csv/Excel estiver "Sim" na frente de um campo, o tipo desse campo no SQL/JSON tem que ser `1537`.
9. **E3Lib com especificidades conhecidas.** Se o `E3Lib` for um destes, avisar a Manu que existem especificidades para esse caso (ainda não detalhadas na skill) antes de seguir a validação padrão: `DM1`, `SEL2414`, `TM_V2`, `DM2`, `SPS`, `TMV e SDV`, `AVR`, `TM1 e TM2`, `BM`.
10. **Encoding.** Varrer descrições/textos (SQL, JSON, csv/Excel) procurando caracteres estranhos/corrompidos no meio de uma descrição, começando pelo `?` isolado, mas também qualquer outro símbolo ou sequência fora do lugar. Exemplo real já encontrado: `Concentração de H?` / `Gas sensor H?`, onde o `?` substituiu o "2" de "H2"/"H₂" — não é só acentuação perdida, também pode ser número/subscrito perdido. **Atenção ao falso positivo**: csv de origem em **Windows-1252/ISO-8859-1** é normal — ler assumindo UTF-8 faz acentos aparecerem trocados mesmo com o arquivo correto; ler respeitando a codificação real antes de julgar. Reportar qualquer ocorrência suspeita que sobrar depois disso, mesmo sem certeza absoluta.

### Bloco B — Comparação com versão anterior (só se existir v1, v2, ... na mesma pasta)

Só executar este bloco depois do Bloco A estar fechado (csv ↔ script ↔ JSON já conferidos nesta versão). Se não existir versão anterior, pular para o Bloco C e, no lugar deste bloco, confirmar manualmente se subtipo/categoria estão corretos (não há referência para comparar).

11. **IDs entre versões.** Extrair os mesmos IDs de cada versão e comparar entre todas — todos os IDs equivalentes devem ser idênticos entre versões.
12. **Mnemônico estável entre versões.** O mnemônico de cada UID já existente na versão anterior deve permanecer o mesmo na versão nova (não pode trocar). Se achar mudança, só reportar — não corrigir sozinho.
13. **Subtipo e categoria.** Têm que ser iguais em todas as versões existentes.

### Bloco C — SYNC

Validar por último, depois que script/JSON/csv (e a comparação de versão, se houve) já estiverem fechados.

14. **Localizar o SYNC e espelhar contra o SQL.** Arquivos `sigma-sync-import` ficam na pasta própria `SYNC` — confirmar que existe apenas 1 arquivo de SYNC por versão (independente do protocolo ser MDB ou DNP). Cruzar esse JSON com o SQL, aplicando a mesma regra de espelhamento do item 2.
15. **identifier.** `identifier` é um campo exclusivo do JSON de SYNC (no JSON de mapeamento o campo equivalente já se chama `E3Lib`) — o valor tem que ser idêntico ao `E3Lib` do script/JSON de mapeamento.
16. **Hash do mapa (SYNC ↔ csv/zip).** `hashCommitMap` é exclusivo do JSON de SYNC (não existe no JSON de mapeamento — não confundir os dois). **O hash NÃO está no nome do próprio arquivo SYNC** (`sigma-sync-import.json` normalmente não tem hash no nome). Ele tem que bater com o hash presente no nome do **csv/Excel de origem** e/ou do **zip** — ex: csv `Fabricante_Nome-Do-Modulo_mdb_v1_da9dfe577f87.csv` e zip `TreetechGit-mapa_clientes-da9dfe577f87.zip` → `hashCommitMap: da9dfe577f87` (trecho depois do último `_`/`-` no nome desses arquivos).
17. **Versão do mapa (SYNC ↔ JSON de mapeamento).** `resourceVersionValue` e `productVersion` do JSON de SYNC são derivados do campo `VersaoMapa` do JSON de mapeamento (ex: `"VersaoMapa": "v2-MDB"`):
    - `resourceVersionValue` é só o número da versão, formato `N.0` (`v2-MDB` → `"2.0"`).
    - `productVersion` é o mesmo número, com o protocolo trocado por `sync` (`v2-MDB` → `"v2.0-sync"`).

### Bloco D — Relatório

18. **Gerar o relatório final** (ver "Formato do Relatório Final"). Se já existia uma doc de validação anterior, atualizar essa mesma doc em vez de criar uma nova (ver "Segunda Validação").

## Segunda Validação

Quando já existe uma doc de relatório (`.md`) de uma validação anterior na pasta do módulo:

1. Ler a doc inteira antes de começar a revalidar — Manu pode ter adicionado observações, explicações ou anotações manuais nos itens (ex: por que algo não foi corrigido, contexto adicional, item marcado como já resolvido).
2. Levar essas observações em consideração durante a nova validação — não ignorar nem sobrescrever sem checar o que ela escreveu.
3. Refazer todas as checagens normalmente ("Passo a Passo de Validação").
4. Por último, **atualizar a mesma doc** (não criar um relatório novo do zero): manter os checkboxes já marcados e as observações da Manu, atualizar o status dos itens que foram corrigidos, e adicionar quaisquer novos itens incorretos encontrados nessa rodada.

## Formato do Relatório Final

Ao terminar todas as checagens, sempre fechar com um relatório único (não é opcional, mesmo que a divergência pareça pequena):

- **OBRIGATÓRIO: todo relatório abre com o cabeçalho padrão abaixo — nunca pular essa parte, mesmo em revalidação de doc existente.** Formato:
  - Título `# Validação de Mapeamento — Módulo <NOME> (<versão> / <protocolo>)` (ex: `# Validação de Mapeamento — Módulo MDJ (V2 / MDB)`).
  - Uma linha logo abaixo indicando o contexto da validação: se é a primeira validação do módulo (sem versão anterior para comparar) ou uma revalidação, e se é mapeamento de cliente específico ou não (ver "Exceções").
  - Uma lista `Arquivos analisados:` com todos os arquivos usados na validação (SQL, JSON, csv/Excel fonte, SYNC), com o caminho relativo (ex: `MDB/MDJ-fl.sql`).
  - Um separador (`---`) antes do corpo do relatório.
- **Organizar por arquivo** (ex: `fl.sql`, `GruposPadrao.sql`, `VersaoRecurso.sql`, JSON de mapeamento, JSON de SYNC, csv/Excel) — Manu depois vai comentar os problemas no Pull Request do Azure DevOps, e lá a navegação é arquivo por arquivo, não por categoria de regra.
- **O relatório inteiro é uma checklist Markdown, sem parágrafos soltos de texto explicando "nada de errado encontrado"**: cada checagem feita (de cada item do "Passo a Passo de Validação" aplicável àquele arquivo) vira uma linha de checklist, `- [x]` quando validado e OK, `- [ ]` quando é um problema/divergência. Tudo é checklist, item por item, na ordem que fizer sentido para o arquivo — não separar em "primeiro os problemas, depois um texto corrido do que foi validado".
  - `- [x] **<o que foi checado>**: <trecho/valor relevante> — <resultado, por que está OK>.`
  - `- [ ] **<o que foi checado>**: <trecho literal do arquivo, Ctrl+F> — <o problema, valor esperado x valor encontrado>.`
  - Isso vale mesmo quando está tudo OK num arquivo: listar cada checagem feita como `- [x]` em vez de um subtítulo tipo "Nenhum problema encontrado" seguido de texto corrido.
- **Para cada item (marcado ou não), incluir um trecho exato e literal do arquivo (um `Ctrl+F` funcional)** — ex: a linha inteira do `DECLARE @ModuloId ...`, o nome exato do campo/mnemônico, o trecho de JSON. Não descrever só "o campo X está errado" ou "campo X confere": copiar o texto como aparece no arquivo.
- Junto do trecho, dizer o que é o problema e qual o valor esperado x valor encontrado (itens `- [ ]`), ou por que está OK (itens `- [x]`).
- **OBRIGATÓRIO: ao citar qualquer trecho do csv/Excel de origem, montar uma tabela Markdown usando o `;` do csv como separador de coluna** (cabeçalho + linha(s) relevante(s)) — nunca colar a linha crua com `;` direto no relatório.
- **Não incluir checagem de algo estrutural/esperado que não faz parte da regra de validação daquele arquivo** — ex: não relatar "fl.json não possui `hashCommitMap`" como item `[x]`, porque esse campo já é sabidamente exclusivo do SYNC (não é uma checagem, é só um fato conhecido de estrutura). Só vira item de checklist algo que de fato foi comparado/cruzado entre arquivos.
- Se algum caso caiu numa exceção (ver "Exceções") e por isso não foi reportado como erro, pode mencionar rapidamente, para deixar claro que foi conferido.
- **O relatório tem que ser salvo como um arquivo `.md` dentro da pasta do módulo** (não é só mostrar no chat) — ele serve de guia depois para conferir se as correções apontadas foram feitas.
- **Salvar na raiz da pasta do módulo, fora das subpastas de protocolo** (ex: `MDB`, `DNP`, `SYNC`) — não dentro delas.

## Common Mistakes

- ID declarado no script (`DECLARE @ModuloId ...`) diferente do valor no JSON.
- ID divergente entre versões (v1 vs v2 etc.) quando deveria ser o mesmo.
- Campo ou ID presente no SQL mas ausente (ou diferente) no JSON, quebrando o espelhamento.
- Mnemônico repetido dentro do mesmo arquivo.
- Descrição repetida dentro do mesmo arquivo.
- Mnemônico de um UID que já existia na v1 mudou na v2.
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

## Exceções

- **Mapas de cliente** (Manu avisa explicitamente quando o mapeamento é de um cliente específico): pode acontecer, raramente, de v1 e v2 terem campos com o mesmo ID mas descrição personalizada para aquele cliente. Isso **não é divergência** — não reportar como erro quando for esse caso.
- **Csv de origem em Windows-1252/ISO-8859-1**: é normal e esperado que o csv de origem não esteja em UTF-8. Ler assumindo UTF-8 e ver acentos trocados **não é um problema de encoding real** — os bytes do arquivo estão corretos, só precisa ler com a codificação certa. Não reportar isso como erro de encoding.
- **Evolução normal entre v1 → v2**: o que precisa se manter estável é o **mnemônico de cada UID já existente** (regra fixa, ver item 12 do "Passo a Passo de Validação", Bloco B). Já é esperado e normal que a v2 tenha: campos novos que não existiam na v1, mudança de unidade de medida de um campo existente, ou mudança de descrição de um campo existente. Essas mudanças **não são erro** — só reportar como divergência se o mnemônico de um UID que já existia mudou.
- **Linhas do tipo "Comando" no csv/Excel de origem não entram nos arquivos de mapeamento.** Quando a coluna "Tratamento"/tipo do csv indica que a linha é um comando (ex: mnemônicos `cmdreset...`, tipicamente `RW`/`Holding register` sem leitura associada), é esperado e normal que esse UUID **não** apareça no `fl.sql`, `fl.json`, `GruposPadrao.sql`, `VersaoRecurso.sql` nem no SYNC — comandos não fazem parte deste mapeamento. **Não reportar a ausência desses UUIDs como erro/faltando.**
- **Trechos de debug/comando não fazem parte do script final**: é normal e esperado que o SQL não contenha comandos de debug (ex: `SELECT`, `PRINT` avulsos usados só para conferir valor durante o desenvolvimento) nem outros comandos auxiliares que não sejam parte da lógica de mapeamento. A ausência desses trechos nos arquivos **não é erro** — não reportar como divergência ou item faltante.
- **Campos de metadado do framework não têm origem no csv/Excel** — mnemônicos como `VersaoProduto`, `VersaoMapa`, `HashCommitMapa` e `DataHoraUltimaLeituraSensor` (e equivalentes) existem no `fl.sql`/`fl.json` mas são gerados/controlados pelo próprio framework, não dados do equipamento. **Não reportar a ausência deles no csv como erro/faltando.**
  - No SYNC, a maioria desses campos **tem sim equivalente** e deve ser conferida normalmente: `VersaoMapa` ↔ `resourceVersionValue`/`productVersion` e `HashCommitMapa` ↔ `hashCommitMap` (ver itens 16/17 do "Passo a Passo de Validação", Bloco C — nomes diferentes, mas é o mesmo dado). Só `DataHoraUltimaLeituraSensor` realmente **não tem** e nunca vai ter equivalente no JSON de SYNC (vem do software em tempo de execução, não é dado estático de mapeamento) — só esse pode ter a ausência no SYNC ignorada, sem virar item de checklist.

## Pendências

- Detalhar o restante da lista de erros comuns/checklist manual (seção "Common Mistakes").
