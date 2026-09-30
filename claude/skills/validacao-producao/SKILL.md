---
name: validacao-producao
description: Use when o usuário está iniciando ou concluindo uma implantação em produção, ou quando uma task de deploy está prestes a ser fechada no Azure DevOps sem evidência confirmada de que as pastas e arquivos obrigatórios foram verificados no ambiente de produção.
---

# Validação de Produção

## Overview

Uma task de deploy não está concluída até que a estrutura de pastas e arquivos obrigatórios seja confirmada diretamente em produção. Testes passando ou pipeline verde não substituem essa verificação.

## When to Use

- Ao iniciar uma implantação em produção (4NET ou 4WEB)
- Antes de fechar uma task de deploy no Azure DevOps
- Quando alguém diz "está em produção" sem mostrar a estrutura de pastas

**Não usar para:** tarefas internas sem deploy em produção (ex: refactor sem implantação)

## Restrições

- **Só valida e aponta — nunca altera arquivos.** Qualquer problema encontrado vira item `- [ ]` no relatório para o usuário corrigir.
- **Só verifica a pasta indicada pelo usuário.** Não buscar fora dela — se faltar algo esperado, perguntar ao usuário em vez de procurar em outro lugar.
- **PROIBIDO rodar qualquer comando git** (`git log`, `git diff`, `git show`, `git status` ou qualquer outro). Usar só o que está na pasta indicada no momento.
- **PROIBIDO salvar ou persistir dados dos arquivos avaliados** (scripts, configs, binários ou qualquer outro arquivo da pasta). O único arquivo que a skill cria ou atualiza é o relatório `.md` da validação.

## Antes de Começar

Fazer **todas as perguntas numa única chamada** (AskUserQuestion):

1. **É 4NET ou 4WEB?**
2. **É Rev ou 1.0?**
3. **A comunicação é Sync ou E3?**
4. **A pasta da empresa já existe?**

## Estrutura de Pastas

> **Padrão esperado**: as estruturas abaixo são os padrões obrigatórios. Qualquer pasta ou arquivo encontrado **fora deste padrão** deve ser reportado como item `- [ ]`. Independente disso, a skill **percorre todas as subpastas** para verificar se os arquivos obrigatórios estão presentes em algum lugar dentro delas — a ausência de um arquivo obrigatório é sempre reportada, mesmo que a estrutura de pastas pareça correta.

### 4NET — Versão 1.0

```
client/
└── 00-create-database-client.sql
DB/
├── 00-INITIAL-SCRIPTS/
├── 01-BACKBONE/
│   └── *-perfil-root.sql  ← obrigatório
├── 02-GROUPS/
└── 03-JSON/
```

### 4NET — Rev (ex: Rev 1.3)

```
client/
└── 00-create-database-client.sql
DB/
├── 00-INITIAL-SCRIPTS/
├── 01-BACKBONE/
│   ├── *-perfil-root.sql  ← obrigatório
│   └── Rev 1.3/           ← pasta com o nome da rev
├── 02-GROUPS/
└── 03-JSON/
```

### Comunicação E3

Independente de 4NET ou 4WEB, quando a comunicação for E3:

```
E3/
├── *.prj
└── *.dll
```

## Quick Reference — Passo a Passo

A ordem importa. **Detalhamento completo de cada item em `checklist.md`, nesta mesma pasta da skill.**

| # | Verificação |
|---|---|
| 1 | Fazer as 4 perguntas iniciais em uma única chamada |
| 2 | Confirmar que a pasta da empresa existe |
| 3 | Verificar se a estrutura de pastas de nível superior bate com o padrão do tipo |
| 4 | Percorrer todas as subpastas e confirmar que os arquivos obrigatórios estão presentes |
| 5 | Se E3: verificar pasta `E3/` com `.prj` e `.dll` |
| 6 | Reportar qualquer coisa fora do padrão como `- [ ]` |
| 7 | Gerar relatório final usando `report-template.md` |

## Relatório Final

Obrigatório ao fim de toda validação. **Formato e esqueleto em `report-template.md`, nesta mesma pasta da skill** — preencher o esqueleto, não montar de cabeça.

## Common Mistakes

| Desculpa | Realidade |
|----------|-----------|
| "O pipeline ficou verde" | Deploy bem-sucedido ≠ estrutura de pastas/arquivos correta |
| "Funcionou em homologação" | Homologação e produção são ambientes diferentes |
| "Validei ontem" | Deploys posteriores podem ter alterado a estrutura |
| "Outro membro do time validou" | Sem registro = não foi validado |

## Red Flags — PARE e Valide

- Task sendo fechada sem ninguém ter aberto a pasta de produção
- "A estrutura provavelmente é igual à última vez"
- Validação feita verbalmente sem relatório gerado
- Pular as perguntas iniciais porque "o tipo é óbvio"

**Task sem relatório de validação = task não concluída.**

## Pendências

- Detalhar estrutura 4WEB
- Detalhar conteúdo obrigatório de `00-INITIAL-SCRIPTS`, `02-GROUPS`, `03-JSON`
- Detalhar checklist de validação pós-deploy
