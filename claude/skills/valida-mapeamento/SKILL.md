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

## Quick Reference — o que checar

1. **JSON é espelho do SQL**: todo campo e todo ID do SQL devem aparecer, idênticos, no JSON (e vice-versa) — não é só "parecido", tem que bater 1:1.
2. **IDs declarados no script (ex: `DECLARE @ModuloId UNIQUEIDENTIFIER = '...'`) têm que ser idênticos ao valor correspondente no JSON.**
3. **Se a pasta já tem uma versão anterior (v1, v2, ...), os IDs têm que bater em todas as versões** — não só entre o script e o JSON da mesma versão, mas também comparando script/JSON de uma versão contra os das outras.
4. **Mnemônicos não podem se repetir dentro do mesmo arquivo** — cada mnemônico deve ser único no script/JSON. Além disso, se existe v1 e está sendo feita a v2, o mnemônico de cada UID deve permanecer o mesmo entre as versões (não pode trocar o mnemônico de um UID já existente).
5. **`hashCommitMap` do JSON tem que bater com o hash no nome do arquivo** — ex: arquivo `TreetechGit-mapa_clientes-da9dfe577f87` → `hashCommitMap: da9dfe577f87` (o hash é o trecho depois do último `-` no nome do arquivo).
6. **`identifier` (JSON) é equivalente a `E3Lib` (script) — os dois têm que estar iguais.**
7. **Todos os IDs existentes no `fl.sql` têm que constar também em `GruposPadrao.sql` e `VersaoRecurso.sql`.**
8. **Subtipo e categoria têm que ser iguais em todas as versões** — se for v1 (sem versão anterior para comparar), confirmar manualmente se subtipo e categoria estão corretos.
9. **O .csv/Excel de origem (o arquivo com o nome "limpo" no nome do arquivo) é quem origina o SQL e o JSON** — os três (csv/Excel, SQL, JSON) têm que bater entre si.
10. **Se a coluna "Gráfico Rápido" do csv/Excel estiver "Sim" na frente de um campo, o tipo desse campo tem que ser `1537`.**
11. **Se o `E3Lib` for um destes, avisar que existem especificidades para esse caso** (ainda não detalhadas): `DM1`, `SEL2414`, `TM_V2`, `DM2`, `SPS`, `TMV e SDV`, `AVR`, `TM1 e TM2`, `BM`.
12. **Arquivos `sigma-sync-import` ficam numa pasta própria chamada `SYNC`.** Independente do protocolo (MDB/DNP), o SYNC é o mesmo — só existe 1 arquivo de SYNC por versão. Esse arquivo é um JSON e segue a mesma regra de espelhamento: tem que ter as mesmas informações que o SQL.
13. Outros erros comuns: lista ainda a ser detalhada por ela (checklist manual que ela já usa hoje).

## Implementation

1. Ler o JSON de mapeamento, o script SQL e o .csv/Excel de origem indicados.
2. Cruzar campo a campo: todo campo do JSON deve ter correspondente no SQL, e todo campo relevante do SQL deve estar mapeado no JSON (JSON é espelho do SQL).
3. Extrair todo `DECLARE @XxxId ... = 'valor'` do script e conferir se o mesmo ID aparece no JSON.
4. Se existir(em) versão(ões) anterior(es) na mesma pasta (v1, v2, ...), extrair os mesmos IDs de cada versão e comparar entre todas — todos os IDs equivalentes devem ser idênticos entre versões.
5. Listar todos os mnemônicos do arquivo e verificar se algum se repete dentro do mesmo arquivo. Se existir v1, conferir também se o mnemônico de cada UID que já existia na v1 permanece o mesmo na v2.
6. Extrair o hash do final do nome do arquivo (após o último `-`) e conferir se é idêntico ao valor de `hashCommitMap` no JSON.
7. Conferir se `identifier` (JSON) é idêntico a `E3Lib` (script).
8. Extrair todos os IDs do `fl.sql` e conferir se cada um também aparece em `GruposPadrao.sql` e em `VersaoRecurso.sql`.
9. Comparar subtipo e categoria entre todas as versões existentes (v1, v2, ...) — devem ser idênticos. Se só existir v1, conferir manualmente se subtipo e categoria estão corretos (sem versão anterior para comparar).
10. Identificar o .csv/Excel de origem pelo nome "limpo" no nome do arquivo e cruzá-lo com o SQL e o JSON — os três têm que bater entre si.
11. Para cada campo com "Sim" na coluna "Gráfico Rápido" do csv/Excel, conferir se o tipo do campo correspondente no SQL/JSON é `1537`.
12. Conferir o valor de `E3Lib`/`identifier`: se for `DM1`, `SEL2414`, `TM_V2`, `DM2`, `SPS`, `TMV e SDV`, `AVR`, `TM1 e TM2` ou `BM`, avisar a Manu que esse mapeamento tem especificidades próprias (ainda não detalhadas na skill) antes de seguir a validação padrão.
13. Localizar o(s) arquivo(s) `sigma-sync-import` dentro da pasta `SYNC`; confirmar que existe apenas 1 arquivo de SYNC por versão (independente de ser MDB ou DNP) e cruzar esse JSON com o SQL, aplicando a mesma regra de espelhamento (item 1).
14. Ao final, gerar um relatório com tudo que está incorreto (ver seção "Formato do Relatório Final").

## Formato do Relatório Final

Ao terminar todas as checagens, sempre fechar com um relatório único listando tudo que foi encontrado de incorreto (não é opcional, mesmo que a divergência pareça pequena):

- Organizar por regra/categoria (ex: IDs, mnemônicos, hashCommitMap, identifier/E3Lib, fl.sql x GruposPadrao/VersaoRecurso, subtipo/categoria, csv/Excel de origem, Gráfico Rápido, SYNC).
- Para cada item incorreto: dizer o que é, onde foi encontrado (arquivo/campo) e qual o valor esperado x valor encontrado.
- Se nada foi encontrado de errado, dizer isso explicitamente (não omitir o relatório).
- Se algum caso caiu numa exceção (ver seção "Exceções") e por isso não foi reportado como erro, também pode mencionar rapidamente, para deixar claro que foi conferido.

## Common Mistakes

- ID declarado no script (`DECLARE @ModuloId ...`) diferente do valor no JSON.
- ID divergente entre versões (v1 vs v2 etc.) quando deveria ser o mesmo.
- Campo ou ID presente no SQL mas ausente (ou diferente) no JSON, quebrando o espelhamento.
- Mnemônico repetido dentro do mesmo arquivo.
- Mnemônico de um UID que já existia na v1 mudou na v2.
- `hashCommitMap` do JSON diferente do hash presente no nome do arquivo.
- `identifier` (JSON) diferente de `E3Lib` (script).
- ID presente no `fl.sql` mas faltando em `GruposPadrao.sql` e/ou `VersaoRecurso.sql`.
- Subtipo/categoria divergente entre versões, ou incorreto quando é v1.
- .csv/Excel de origem (arquivo "limpo") divergente do SQL e/ou do JSON.
- Campo com "Gráfico Rápido = Sim" no csv/Excel mas tipo diferente de `1537` no SQL/JSON.
- Arquivo `sigma-sync-import` fora da pasta `SYNC`, mais de 1 arquivo de SYNC na mesma versão, ou conteúdo do SYNC divergente do SQL.
- Demais erros comuns ainda a ser detalhados por ela.

## Exceções

- **Mapas de cliente** (Manu avisa explicitamente quando o mapeamento é de um cliente específico): pode acontecer, raramente, de v1 e v2 terem campos com o mesmo ID mas descrição personalizada para aquele cliente. Isso **não é divergência** — não reportar como erro quando for esse caso.
- **Evolução normal entre v1 → v2**: quando existe v1 e está sendo feita v2, o que precisa se manter estável é o **mnemônico de cada UID já existente** (regra fixa, ver item 4/5 do Quick Reference). Já é esperado e normal que a v2 tenha: campos novos que não existiam na v1, mudança de unidade de medida de um campo existente, ou mudança de descrição de um campo existente. Essas mudanças **não são erro** — só reportar como divergência se o mnemônico de um UID que já existia mudou.

## Pendências

- Detalhar o restante da lista de erros comuns/checklist manual (seção "Common Mistakes").
