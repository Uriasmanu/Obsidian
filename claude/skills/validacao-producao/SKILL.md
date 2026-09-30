---
name: validacao-producao
description: Use when iniciando uma implantação em produção — verificar tipo (4NET/4WEB), versão (Rev/1.0), comunicação (Sync/E3) e estrutura de pastas e arquivos obrigatórios antes de considerar a entrega pronta.
---

# Validação de Produção

## Overview

Skill de apoio à implantação em produção. O objetivo é verificar se a estrutura de pastas e arquivos obrigatórios está correta antes de considerar a entrega concluída.

## When to Use

- Ao iniciar uma implantação em produção
- Antes de fechar uma task de deploy no Azure DevOps
- Quando alguém diz "já está em produção" sem evidência de validação

## Restrições

- **A skill só valida e aponta — nunca altera arquivos.** Qualquer problema encontrado vira item `- [ ]` no relatório para o usuário corrigir.
- **Só pode verificar a pasta indicada pelo usuário.** Não buscar arquivos fora dela — se faltar algo esperado, perguntar ao usuário.

## Antes de Começar

Fazer **todas as perguntas numa única chamada** (AskUserQuestion):

1. **É 4NET ou 4WEB?**
2. **É Rev ou 1.0?**
3. **A comunicação é Sync ou E3?**
4. **A pasta da empresa já existe?**

## Estrutura de Pastas

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

| # | Verificação |
|---|---|
| 1 | Perguntas iniciais respondidas (4NET/4WEB, Rev/1.0, Sync/E3, pasta existe) |
| 2 | Estrutura de pastas obrigatória presente conforme o tipo |
| 3 | Arquivos obrigatórios presentes em cada pasta |

## Relatório Final

Obrigatório ao fim de toda validação. **Formato e esqueleto em `report-template.md`, nesta mesma pasta da skill** — preencher o esqueleto, não montar de cabeça.

## Common Mistakes

- Fechar task sem verificar estrutura de pastas
- Confundir Rev com 1.0 (estrutura de `01-BACKBONE` muda)
- Esquecer de verificar pasta `E3` quando a comunicação for E3

## Pendências

- Detalhar estrutura 4WEB
- Detalhar conteúdo obrigatório de `00-INITIAL-SCRIPTS`, `02-GROUPS`, `03-JSON`
- Detalhar checklist de validação pós-deploy
