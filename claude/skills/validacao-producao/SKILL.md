---
name: validacao-producao
description: Use when the user is starting or completing a production deployment, when a deploy task is about to be closed in Azure DevOps without confirmed evidence that required folders and files were verified in production, or when the user asks to validar, revalidar or conferir a estrutura de producao (4NET / 4WEB).
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

## Escopo

A skill roda em cima da **pasta aberta no VSCode**. **PROIBIDO pedir o caminho da pasta ao usuário** — deduzir automaticamente da pasta aberta antes de fazer qualquer outra pergunta. O relatório de validação é salvo na **pasta de maior hierarquia** dessa estrutura (o nível mais alto disponível na pasta aberta).

## Antes de Começar

1. **Antes de qualquer pergunta ou leitura de arquivo, verificar se já existe um relatório `Validacao-Producao-*.md`** na pasta de maior hierarquia aberta no VSCode. Se existir, é uma revalidação — ler o relatório inteiro e seguir "Segunda Validação". O cabeçalho do relatório já responde tipo, versão e comunicação — não perguntar de novo, só confirmar com o usuário se mudou algo.
2. Se não existir (primeira validação), fazer **todas as perguntas numa única chamada** (AskUserQuestion):

1. **É 4NET ou 4WEB?**
2. **É Rev ou 1.0?**
3. **A comunicação é Sync ou E3?**
4. **Se Rev: a Rev troca a comunicação?** (ex: 1.0 era E3 e a Rev vira Sync) — só perguntar se for Rev.

## Estrutura de Pastas

> **Padrão esperado**: as estruturas abaixo são os padrões obrigatórios. Qualquer pasta ou arquivo encontrado **fora deste padrão** deve ser reportado como item `- [ ]`. Independente disso, a skill **percorre todas as subpastas** para verificar se os arquivos obrigatórios estão presentes em algum lugar dentro delas — a ausência de um arquivo obrigatório é sempre reportada, mesmo que a estrutura de pastas pareça correta.

A pasta-raiz do projeto segue o padrão `ecm-[CLIENTE]-[INSTALACAO]/` e fica dentro de `net/[CLIENTE]/` (4NET) ou `web/[CLIENTE]/` (4WEB).

### 4NET — Versão 1.0

```
ecm-[CLIENTE]-[INSTALACAO]/
├── client/
│   └── DB/
│       └── 00-create-database-client.sql
├── DB/
│   ├── 00-INITIAL-SCRIPTS/
│   │   ├── 000-ecm-clean-data.sql
│   │   └── 001-ecm-add-[MODULO]-fl.sql
│   ├── 01 - BACKBONE/
│   │   └── *-perfil-root.sql  ← obrigatório
│   ├── 02 - GROUPS/
│   │   └── 001-[MODULO]-GruposPadrao.sql
│   └── 03-JSONs/
│       ├── [MODULO]-sigma-sync-import
│       ├── [MODULO]-sigma-sync-algorithmFieldMaps-import
│       └── ecm_[CLIENTE]_[INSTALACAO]_sync
└── E3/  ← só se comunicação E3; ausente quando Sync
    ├── ecm-[CLIENTE]-[INSTALACAO].prj
    └── [PROTOCOLO].dll
```

### 4NET — Rev (ex: Rev 1.3)

```
ecm-[CLIENTE]-[INSTALACAO]/
├── client/
│   └── DB/
│       └── 00-create-database-client.sql
├── DB/
│   ├── 00-INITIAL-SCRIPTS/
│   ├── 01 - BACKBONE/
│   │   ├── *-perfil-root.sql  ← obrigatório
│   │   └── Rev 1.3/           ← pasta com o nome da rev
│   ├── 02 - GROUPS/
│   └── 03-JSONs/
└── E3/  ← só se comunicação E3; ausente quando Sync
    ├── ecm-[CLIENTE]-[INSTALACAO].prj
    └── [PROTOCOLO].dll
```

### 4NET — Rev com troca de comunicação (ex: 1.0 era E3, Rev vira Sync)

A pasta da Rev leva o sufixo ` - sync` no nome e tem **estrutura DB própria** dentro dela — não é só uma subpasta vazia. A pasta `E3/` não existe nesse caso.

```
ecm-[CLIENTE]-[INSTALACAO]/
├── client/
│   └── DB/
│       └── 00-create-database-client.sql
├── DB/
│   ├── 00-INITIAL-SCRIPTS/
│   ├── 01 - BACKBONE/
│   │   ├── *-perfil-root.sql  ← obrigatório
│   │   └── Rev 1.2 - sync/    ← nome com sufixo " - sync"
│   │       ├── 00-INITIAL-SCRIPTS/
│   │       ├── 01-BACKBONE/
│   │       ├── 02-GROUPS/
│   │       └── 03-JSONs/ ou 03 - JSONs/
│   ├── 02 - GROUPS/
│   └── 03-JSONs/
└── (sem E3/ — comunicação já é Sync)
```

### 4WEB

Não tem pasta `client/` nem `00-INITIAL-SCRIPTS/`. Scripts ficam diretamente na `DB/`, sem subpastas. Banco de dados é criado manualmente — ausência de `client/` não é erro.

```
ecm-[CLIENTE]-[INSTALACAO]/
├── DB/
│   ├── 001_ecm_[CLIENTE]_[INSTALACAO].sql
│   ├── 002_ecm_[CLIENTE]_[INSTALACAO]_[MODULO-ENGENHARIA].sql
│   ├── 002_ecm_[CLIENTE]_[INSTALACAO]_[ATIVO]_[MODULO-ENGENHARIA]_config.sql
│   └── 003_ecm_[CLIENTE]_[INSTALACAO]_temperatura_ambiente.sql
└── E3/  ← só se comunicação E3; ausente quando Sync
    ├── ecm-[CLIENTE]-[INSTALACAO].prj
    └── [PROTOCOLO].dll
```

### Comunicação E3 vs Sync

Quando a comunicação for **E3**, a pasta `E3/` com `.prj` e `.dll` é obrigatória. Quando for **Sync** (SigmaSync), a pasta `E3/` **não existe** — ausência não é erro.

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

## Segunda Validação

Quando já existe um relatório `Validacao-Producao-*.md` na pasta de maior hierarquia. Formato dos itens rastreáveis (`Onde:`, `Histórico:`) em `report-template.md`.

1. **Ler o relatório inteiro** e listar todos os itens em aberto (`- [ ]`): ID, status, `Onde:`, `Obs.:`. A rodada nova é `R<última + 1>` do painel.
2. **Reconferir cada item em aberto** (🔴, 🟡, 🔁) verificando se a pasta ou arquivo agora existe no caminho indicado em `Onde:`:
   - Pasta/arquivo existe agora → ✅ `resolvido na R<n>`. Vira `- [x]` com linha `Agora:` confirmando.
   - Ainda ausente → manter status, adicionar `R<n> continua` no `Histórico:`.
   - Corrigido parcialmente (ex: pasta existe mas arquivo obrigatório ainda falta) → 🟡 `parcial`.
3. **Achado novo** (não está no relatório) → item novo com o próximo ID livre do prefixo, `Histórico: R<n> novo`.
4. **Atualizar o mesmo relatório** (nunca criar outro): adicionar linha de contexto `Revalidação (R<n>)`, nova linha no painel, reordenar cada seção (`- [ ]` por ID, depois `- [x]`). Nunca apagar item ou `Obs.:`.
5. Resumir a rodada para o usuário: resolvidos, parciais, reabertos e novos, por ID.

## Relatório Final

Obrigatório ao fim de toda validação. **O relatório deve sempre ser escrito em português**, independente do idioma usado na conversa. **Formato e esqueleto em `report-template.md`, nesta mesma pasta da skill** — preencher o esqueleto, não montar de cabeça.

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
