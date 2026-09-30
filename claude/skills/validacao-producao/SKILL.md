---
name: validacao-producao
description: Use when a task ou deploy está marcado como concluído mas ainda não foi verificado no ambiente de produção real — sintomas incluem "funcionou no ambiente", "testei localmente", "passou nos testes" sem confirmação em prod.
---

# Validação de Produção

## Overview

Nenhuma task está concluída até que o comportamento correto seja confirmado diretamente em produção. Ambientes de dev/homologação não equivalem a prod.

## Quando Usar

- Após qualquer deploy ou merge para produção
- Quando uma correção de bug é marcada como feita
- Antes de fechar uma task no Azure DevOps
- Quando alguém diz "funciona em homologação"

**Não usar para:** tarefas puramente internas sem impacto em produção (ex: refactor sem deploy)

## Perguntas Iniciais

Antes de qualquer validação, perguntar:

1. É **4NET** ou **4WEB**?
2. É **Rev** ou **1.0**?
3. A comunicação é **Sync** ou **E3**?
4. A pasta da empresa já existe?

---

## Estrutura de Pastas — 4NET

Quando for **4NET**, verificar se existem as seguintes pastas:

**Se for versão 1.0:**
```
client/
└── 00-create-database-client.sql
DB/
├── 00-INITIAL-SCRIPTS
├── 01-BACKBONE
│   └── *-perfil-root.sql  ← obrigatório
├── 02-GROUPS
└── 03-JSON
```

**Se for Rev (ex: Rev 1.3):**
```
client/
└── 00-create-database-client.sql
DB/
├── 00-INITIAL-SCRIPTS
├── 01-BACKBONE
│   ├── *-perfil-root.sql  ← obrigatório
│   └── Rev 1.3/
├── 02-GROUPS
└── 03-JSON
```

---

## Estrutura de Pastas — Comunicação E3

Quando a comunicação for **E3**, verificar se existe a pasta `E3` com:

```
E3/
├── *.prj
└── *.dll
```

---

## Checklist de Validação

- [ ] Acessar o endpoint/tela afetada diretamente em produção
- [ ] Executar o fluxo completo que foi alterado
- [ ] Confirmar que dados persistem corretamente (quando aplicável)
- [ ] Verificar logs de erro no ambiente de produção
- [ ] Checar se funcionalidades adjacentes não foram impactadas

## Erros Comuns

| Situação | Problema |
|----------|----------|
| "Passou nos testes" | Testes não cobrem 100% dos cenários reais |
| "Funciona em homologação" | Dados, configs e volume diferem de prod |
| "Deploy deu sucesso" | Deploy bem-sucedido ≠ funcionalidade correta |
| "Validei ontem" | Deploys subsequentes podem ter revertido |

## Red Flags — PARE e Valide

- Task fechada sem acesso ao ambiente de produção
- Validação feita apenas por outro membro sem registro
- "Já estava funcionando antes do meu deploy"
- Nenhum screenshot/log comprovando o comportamento em prod

**Toda task sem evidência de validação em prod = task não concluída.**
