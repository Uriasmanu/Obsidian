---
name: valida-mapeamento
description: Use when Manu pede para validar um mapeamento (task "Teste mapeamento") — conferir consistência entre um JSON de mapeamento e o script SQL correspondente.
---

# Valida Mapeamento

## Overview

Skill de apoio à task "Teste mapeamento" do trabalho da Manu. O objetivo é comparar um JSON de mapeamento, o script SQL e o .csv/Excel de origem, apontando divergências antes de considerar o mapeamento pronto.

## When to Use

- Manu pede para validar/conferir um mapeamento contra um script SQL.
- Ela cola ou aponta um conjunto (JSON de mapeamento + script SQL + .csv/Excel de origem) e pede revisão.

## Escopo de Leitura

**A skill só pode ler arquivos dentro da pasta indicada por Manu no VSCode** (a pasta do módulo aberta/apontada). Não abrir, buscar ou ler arquivos fora dessa pasta (ex: outros módulos, outras pastas do workspace) mesmo que pareçam relevantes para comparação — se faltar algum arquivo esperado dentro da pasta indicada, perguntar para Manu em vez de procurar em outro lugar.

**Não rodar comandos git** (ex: `git log`, `git diff`, `git show`, `git blame`) para buscar contexto, histórico ou versões anteriores de arquivo. A validação usa só os arquivos presentes na pasta indicada, exatamente como estão no momento — nunca consultar o histórico do repositório.

## Quick Reference — o que checar

1. **JSON é espelho do SQL**: todo campo e todo ID do SQL devem aparecer, idênticos, no JSON (e vice-versa) — não é só "parecido", tem que bater 1:1.
2. **IDs declarados no script (ex: `DECLARE @ModuloId UNIQUEIDENTIFIER = '...'`) têm que ser idênticos ao valor correspondente no JSON.**
3. **Se a pasta já tem uma versão anterior (v1, v2, ...), os IDs têm que bater em todas as versões** — não só entre o script e o JSON da mesma versão, mas também comparando script/JSON de uma versão contra os das outras.
4. **Mnemônicos não podem se repetir dentro do mesmo arquivo** — cada mnemônico deve ser único no script/JSON. Além disso, se existe v1 e está sendo feita a v2, o mnemônico de cada UID deve permanecer o mesmo entre as versões (não pode trocar o mnemônico de um UID já existente). **Se encontrar mnemônicos duplicados, não resolver sozinho** (ex: não inventar um sufixo tipo acrescentar "2" no final para desempatar) — só reportar a duplicidade para a Manu avaliar como corrigir.
4.1. **Descrições também não podem se repetir dentro do mesmo arquivo** — cada descrição deve ser única no script/JSON, mesma lógica do item 4. Se encontrar descrições duplicadas, também não resolver sozinho — só reportar para a Manu avaliar.
4.2. **`resourceVersionValue` e `productVersion` (JSON de SYNC) são derivados do campo `VersaoMapa` do JSON de mapeamento** (ex: `"VersaoMapa": "v2-MDB"`):
   - `resourceVersionValue` é só o número da versão, no formato `N.0` (ex: `VersaoMapa: "v2-MDB"` → `resourceVersionValue: "2.0"`).
   - `productVersion` é o mesmo número de versão, mas com o protocolo trocado por `sync` (ex: `VersaoMapa: "v2-MDB"` → `productVersion: "v2.0-sync"`).
   - Conferir se esses dois valores no SYNC batem com o `VersaoMapa` do JSON de mapeamento antes de reportar divergência de versão.
5. **`hashCommitMap` é exclusivo do arquivo JSON de SYNC** (`sigma-sync-import`, dentro da pasta `SYNC` — ver item 12) — não existe no JSON de mapeamento. **Atenção: o hash NÃO está no nome do próprio arquivo SYNC** (o arquivo `sigma-sync-import.json` normalmente não tem hash no nome, ex: `nome-do-modulo-sigma-sync-import.json`). O `hashCommitMap` do SYNC tem que bater com o hash que aparece no nome do **csv/Excel de origem** e/ou do **zip** — ex: csv `Fabricante_Nome-Do-Modulo_mdb_v1_da9dfe577f87.csv` e zip `TreetechGit-mapa_clientes-da9dfe577f87.zip` → `hashCommitMap: da9dfe577f87` (o hash é o trecho depois do último `_`/`-` no nome desses arquivos).
6. **`identifier` é um campo exclusivo do JSON de SYNC** (não existe no JSON de mapeamento, ex: `fl.json` — lá o campo já se chama `E3Lib`, igual ao script). Em ambos os casos a checagem é a mesma: o valor tem que ser idêntico ao `E3Lib` do script SQL.
7. **Todos os IDs existentes no `fl.sql` têm que constar também em `GruposPadrao.sql` e `VersaoRecurso.sql`.**
8. **Subtipo e categoria têm que ser iguais em todas as versões** — se for v1 (sem versão anterior para comparar), confirmar manualmente se subtipo e categoria estão corretos.
9. **O .csv/Excel de origem é quem origina o SQL e o JSON** — os três (csv/Excel, SQL, JSON) têm que bater entre si. **Atenção na hora de identificar qual é o arquivo de origem**: é o arquivo que traz o hash de commit no nome (o mesmo hash do `hashCommitMap`, ver item 5), ou o arquivo com o mesmo nome do csv dentro da pasta zipada — **não é o `modulo.csv` genérico, nem um arquivo com o nome igual ao `E3Lib`** (ex: `BM.csv`, dentro de `MDB`/`DNP`). Esse tipo de arquivo costuma ser um export de tags OPC/Archestra (colunas como `ObjectType;Name;AdviseType;...AllowRead;AllowWrite`), sem UUID, sem coluna "Mnemônico" e sem coluna "Gráfico Rápido" — não é o csv fonte, mesmo tendo nome parecido com o módulo. Para confirmar que achou o arquivo certo, checar se ele tem colunas `UUID` e `Mnemônico`. **Atenção ao formato do UUID**: no csv de origem os UUIDs costumam vir sem hífen (ex: `1ca40722324346a1b92e56270fd35ea7`), enquanto SQL e JSON usam o formato com hífen (ex: `1ca40722-3243-46a1-b92e-56270fd35ea7`) — são o mesmo valor, só formatado diferente. Ao comparar, normalizar removendo hífens dos dois lados antes de concluir que os IDs divergem, senão dá falso positivo de erro.
10. **Se a coluna "Gráfico Rápido" do csv/Excel estiver "Sim" na frente de um campo, o tipo desse campo tem que ser `1537`.**
11. **Se o `E3Lib` for um destes, avisar que existem especificidades para esse caso** (ainda não detalhadas): `DM1`, `SEL2414`, `TM_V2`, `DM2`, `SPS`, `TMV e SDV`, `AVR`, `TM1 e TM2`, `BM`.
12. **Arquivos `sigma-sync-import` ficam numa pasta própria chamada `SYNC`.** Independente do protocolo (MDB/DNP), o SYNC é o mesmo — só existe 1 arquivo de SYNC por versão. Esse arquivo é um JSON e segue a mesma regra de espelhamento: tem que ter as mesmas informações que o SQL.
13. **Arquivos não podem ter problemas de encoding** — nenhum caractere estranho/corrompido no meio de uma descrição (ex: um `?` sozinho no meio da frase, onde deveria ter um acento ou caractere especial). Exemplo real já encontrado: descrição `Concentração de H?` / `Gas sensor H?`, onde o `?` substituiu o "2" de "H2"/"H₂" — ou seja, não é só acentuação perdida, também pode ser número/subscrito perdido. **Atenção para não confundir com falso positivo**: é normal e esperado que os csv de origem (ex: exports OPC/Archestra) venham em **Windows-1252/ISO-8859-1**, não em UTF-8 — se a skill ler o arquivo assumindo UTF-8, os acentos vão aparecer trocados/estranhos mesmo estando o arquivo correto. Isso **não é erro de encoding**; ler o arquivo respeitando a codificação real dele antes de julgar. O problema real de encoding é quando o próprio dado está corrompido/perdido (como o `?` no lugar de "2"), não quando a ferramenta de leitura assumiu a codificação errada. A lista de padrões problemáticos ainda está sendo levantada pela Manu; se a skill encontrar qualquer coisa que pareça suspeita nesse sentido (símbolo fora de lugar, sequência estranha de caracteres, etc.), mesmo que não esteja nessa lista, tem que avisar.
14. Outros erros comuns: lista ainda a ser detalhada por ela (checklist manual que ela já usa hoje).

## Implementation

0. **Antes de começar, perguntar para a Manu:** (a) qual versão do módulo está sendo validada (v1, v2, etc.), (b) se é um mapa de cliente (para aplicar a exceção de descrição personalizada por UID, ver seção "Exceções") e (c) qual protocolo está sendo validado, `DNP` ou `MDB` — **só se valida um protocolo por vez**, mesmo que a pasta do módulo tenha as duas subpastas. Não presumir nenhuma das três coisas sozinho.
0.5. **Verificar se já existe uma doc de relatório de validação (`.md`) na pasta do módulo** (ver "Formato do Relatório Final"). Se existir — é uma segunda validação —, ler essa doc inteira antes de validar de novo: Manu pode ter feito alterações e observações manuais nela (comentários, explicações, itens já marcados como corrigidos). Levar essas observações em consideração ao revalidar (ver "Segunda Validação").
1. Ler o JSON de mapeamento, o script SQL e o .csv/Excel de origem indicados.
2. Cruzar campo a campo: todo campo do JSON deve ter correspondente no SQL, e todo campo relevante do SQL deve estar mapeado no JSON (JSON é espelho do SQL).
3. Extrair todo `DECLARE @XxxId ... = 'valor'` do script e conferir se o mesmo ID aparece no JSON.
4. Se existir(em) versão(ões) anterior(es) na mesma pasta (v1, v2, ...), extrair os mesmos IDs de cada versão e comparar entre todas — todos os IDs equivalentes devem ser idênticos entre versões.
5. Listar todos os mnemônicos do arquivo e verificar se algum se repete dentro do mesmo arquivo. Se existir v1, conferir também se o mnemônico de cada UID que já existia na v1 permanece o mesmo na v2. Se achar duplicidade, apenas reportar — nunca sugerir/aplicar uma correção automática tipo acrescentar um número no final do mnemônico.
5.1. Listar todas as descrições do arquivo e verificar se alguma se repete dentro do mesmo arquivo. Se achar duplicidade, apenas reportar, mesma regra do item 5 (não resolver sozinho).
5.2. Conferir se `resourceVersionValue` e `productVersion` do JSON de SYNC batem com o `VersaoMapa` do JSON de mapeamento: `resourceVersionValue` deve ser o número da versão no formato `N.0`, e `productVersion` o mesmo número com o protocolo trocado por `sync` (ex: `VersaoMapa: "v2-MDB"` → `resourceVersionValue: "2.0"` e `productVersion: "v2.0-sync"`).
6. Extrair o `hashCommitMap` do arquivo JSON de SYNC (`sigma-sync-import`, dentro de `SYNC`) e comparar com o hash presente no nome do csv/Excel de origem e/ou do zip (não com o nome do próprio arquivo SYNC, que geralmente não tem hash). O JSON de mapeamento não tem esse campo — não confundir os dois.
7. Conferir se o `E3Lib` do script bate com o campo equivalente no JSON: `identifier` no JSON de SYNC, e `E3Lib` no JSON de mapeamento (`fl.json`) — nos dois casos, os valores têm que ser idênticos.
8. Extrair todos os IDs do `fl.sql` e conferir se cada um também aparece em `GruposPadrao.sql` e em `VersaoRecurso.sql`.
9. Comparar subtipo e categoria entre todas as versões existentes (v1, v2, ...) — devem ser idênticos. Se só existir v1, conferir manualmente se subtipo e categoria estão corretos (sem versão anterior para comparar).
10. Identificar o .csv/Excel de origem: é o arquivo com o hash de commit no nome (ver item 6) ou com o mesmo nome do csv dentro da pasta zipada — não confundir com um `modulo.csv` genérico nem com um arquivo de nome igual ao `E3Lib` (ex: `BM.csv`, export de tags OPC/Archestra sem UUID/Mnemônico/Gráfico Rápido). Confirmar que o arquivo escolhido tem colunas `UUID` e `Mnemônico` antes de usá-lo como fonte. Cruzá-lo com o SQL e o JSON — os três têm que bater entre si. Ao comparar UUIDs, normalizar removendo hífens antes (o csv costuma vir sem hífen, SQL/JSON com hífen).
11. Para cada campo com "Sim" na coluna "Gráfico Rápido" do csv/Excel, conferir se o tipo do campo correspondente no SQL/JSON é `1537`.
12. Conferir o valor de `E3Lib`/`identifier`: se for `DM1`, `SEL2414`, `TM_V2`, `DM2`, `SPS`, `TMV e SDV`, `AVR`, `TM1 e TM2` ou `BM`, avisar a Manu que esse mapeamento tem especificidades próprias (ainda não detalhadas na skill) antes de seguir a validação padrão.
13. Localizar o(s) arquivo(s) `sigma-sync-import` dentro da pasta `SYNC`; confirmar que existe apenas 1 arquivo de SYNC por versão (independente de ser MDB ou DNP) e cruzar esse JSON com o SQL, aplicando a mesma regra de espelhamento (item 1).
14. Varrer as descrições/textos dos arquivos (SQL, JSON, csv/Excel) procurando problemas de encoding: caracteres estranhos/corrompidos no meio de uma descrição, começando pelo `?` isolado, mas também qualquer outro símbolo ou sequência de caracteres que pareça fora do lugar. Antes de reportar, ler o csv de origem com a codificação correta (Windows-1252/ISO-8859-1 é comum e normal nesses exports) — acento "estranho" só por causa de leitura em UTF-8 não é erro real. Reportar qualquer ocorrência suspeita que sobrar depois disso, mesmo sem ter certeza absoluta.
15. Ao final, gerar um relatório com tudo que está incorreto (ver seção "Formato do Relatório Final"). Se já existia uma doc de validação anterior (ver item 0.5), atualizar essa mesma doc em vez de criar uma nova.

## Segunda Validação

Quando já existe uma doc de relatório (`.md`) de uma validação anterior na pasta do módulo:

1. Ler a doc inteira antes de começar a revalidar — Manu pode ter adicionado observações, explicações ou anotações manuais nos itens (ex: por que algo não foi corrigido, contexto adicional, item marcado como já resolvido).
2. Levar essas observações em consideração durante a nova validação — não ignorar nem sobrescrever sem checar o que ela escreveu.
3. Refazer todas as checagens normalmente (Quick Reference / Implementation).
4. Por último, **atualizar a mesma doc** (não criar um relatório novo do zero): manter os checkboxes já marcados e as observações da Manu, atualizar o status dos itens que foram corrigidos, e adicionar quaisquer novos itens incorretos encontrados nessa rodada.

## Formato do Relatório Final

Ao terminar todas as checagens, sempre fechar com um relatório único listando tudo que foi encontrado de incorreto (não é opcional, mesmo que a divergência pareça pequena):

- **OBRIGATÓRIO: todo relatório abre com o cabeçalho padrão abaixo — nunca pular essa parte, mesmo em revalidação de doc existente.** Formato:
  - Título `# Validação de Mapeamento — Módulo <NOME> (<versão> / <protocolo>)` (ex: `# Validação de Mapeamento — Módulo MDJ (V2 / MDB)`).
  - Uma linha logo abaixo indicando o contexto da validação: se é a primeira validação do módulo (sem versão anterior para comparar) ou uma revalidação, e se é mapeamento de cliente específico ou não (ver seção "Exceções").
  - Uma lista `Arquivos analisados:` com todos os arquivos usados na validação (SQL, JSON, csv/Excel fonte, SYNC), com o caminho relativo (ex: `MDB/MDJ-fl.sql`).
  - Um separador (`---`) antes do corpo do relatório.
- **Organizar por arquivo** (ex: `fl.sql`, `GruposPadrao.sql`, `VersaoRecurso.sql`, JSON de mapeamento, JSON de SYNC, csv/Excel) — Manu depois vai comentar os problemas no Pull Request do Azure DevOps, e lá a navegação é arquivo por arquivo, não por categoria de regra.
- **DENTRO de cada arquivo, os problemas vêm primeiro, sempre** — não importa a ordem em que foram encontrados durante a checagem, na hora de escrever o relatório os itens incorretos (checkbox `- [ ]`) aparecem antes de qualquer texto descritivo sobre o que foi validado sem problema naquele arquivo.
- **Se um arquivo não teve nenhum problema encontrado, usar um subtítulo explícito tipo "Nenhum problema encontrado"** logo abaixo do título da seção do arquivo, e só depois vem a descrição do que foi validado (como já é feito hoje) — não deixar a ausência de erro implícita só pelo tom do texto.
- **Para cada item incorreto, incluir um trecho exato e literal do arquivo (um `Ctrl+F` funcional)** — ex: a linha inteira do `DECLARE @ModuloId ...`, o nome exato do campo/mnemônico, o trecho de JSON — para ela localizar rapidamente o ponto certo no Azure DevOps na hora de comentar. Não descrever só "o campo X está errado": copiar o texto como aparece no arquivo.
- Junto do trecho, dizer o que é o problema e qual o valor esperado x valor encontrado.
- **OBRIGATÓRIO: ao citar qualquer trecho do csv/Excel de origem, montar uma tabela Markdown usando o `;` do csv como separador de coluna** (cabeçalho + linha(s) relevante(s)) — nunca colar a linha crua com `;` direto no relatório. Isso vale tanto para itens incorretos quanto para qualquer outra citação do csv no relatório.
- **Cada item incorreto vira um checkbox Markdown (`- [ ] `)** — Manu marca conforme vai comentando no Pull Request do Azure DevOps, então o relatório funciona como checklist vivo pra conferir depois se todas as correções foram feitas.
- Se nada foi encontrado de errado, dizer isso explicitamente (não omitir o relatório).
- Se algum caso caiu numa exceção (ver seção "Exceções") e por isso não foi reportado como erro, também pode mencionar rapidamente, para deixar claro que foi conferido.
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
- **Evolução normal entre v1 → v2**: quando existe v1 e está sendo feita v2, o que precisa se manter estável é o **mnemônico de cada UID já existente** (regra fixa, ver item 4/5 do Quick Reference). Já é esperado e normal que a v2 tenha: campos novos que não existiam na v1, mudança de unidade de medida de um campo existente, ou mudança de descrição de um campo existente. Essas mudanças **não são erro** — só reportar como divergência se o mnemônico de um UID que já existia mudou.
- **Linhas do tipo "Comando" no csv/Excel de origem não entram nos arquivos de mapeamento.** Quando a coluna "Tratamento"/tipo do csv indica que a linha é um comando (ex: mnemônicos `cmdreset...`, tipicamente `RW`/`Holding register` sem leitura associada), é esperado e normal que esse UUID **não** apareça no `fl.sql`, `fl.json`, `GruposPadrao.sql`, `VersaoRecurso.sql` nem no SYNC — comandos não fazem parte deste mapeamento. **Não reportar a ausência desses UUIDs como erro/faltando.**

- **Trechos de debug/comando não fazem parte do script final**: é normal e esperado que o SQL não contenha comandos de debug (ex: `SELECT`, `PRINT` avulsos usados só para conferir valor durante o desenvolvimento) nem outros comandos auxiliares que não sejam parte da lógica de mapeamento. A ausência desses trechos nos arquivos **não é erro** — não reportar como divergência ou item faltante.

## Pendências

- Detalhar o restante da lista de erros comuns/checklist manual (seção "Common Mistakes").
