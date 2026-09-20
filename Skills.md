# Skills em Agentes de IA

## O que é uma "Skill"?

Uma **skill** (habilidade) é um pacote de instruções, conhecimento e/ou ferramentas que ensina um agente de IA a executar bem uma tarefa específica — sem precisar retreinar o modelo.

Pense num agente de IA (como o Claude, GPTs, etc.) como uma pessoa muito inteligente e versátil, mas que **não conhece os processos específicos da sua empresa ou do seu fluxo de trabalho**. Uma skill é como um **manual de procedimento** que você entrega a essa pessoa: "quando a situação for X, siga estes passos, use este checklist, e preste atenção nestes detalhes".

> **Analogia:** o modelo de IA é o cérebro (raciocínio geral). As skills são os "cursos de especialização" que você anexa a esse cérebro sob demanda — só são "lidos" quando a tarefa pede.

---

## Por que skills existem?

Modelos de linguagem já sabem "de tudo um pouco", mas isso traz problemas:

1. **Falta de contexto específico** — o modelo não sabe como *o seu* time faz code review, revisão de PR ou versionamento.
2. **Inconsistência** — sem instruções fixas, o agente pode resolver a mesma tarefa de formas diferentes a cada vez.
3. **Contexto limitado** — não dá para colocar tudo (todo processo, toda convenção) na conversa o tempo todo; isso gastaria espaço e atenção do modelo.

As skills resolvem isso: ficam **guardadas fora da conversa principal** e são **carregadas só quando relevantes**, mantendo o agente enxuto e focado.

---

## Como uma skill funciona na prática

Uma skill normalmente é um arquivo (ex: `SKILL.md`) com duas partes:

### 1. Metadados (o "gatilho")
Um cabeçalho curto que diz **quando** usar a skill — geralmente `name` e `description`. O agente lê essa descrição *antes* de decidir carregar o conteúdo completo, meio que "escaneando o índice de um livro" para saber se aquele capítulo é útil agora.

```markdown
---
name: revisao-de-codigo
description: Use ao revisar um Pull Request ou diff antes de aprovar mudanças no código.
---
```

### 2. Instruções (o "corpo")
O conteúdo detalhado: passo a passo, checklists, exemplos, regras, ou até scripts/ferramentas anexas que o agente pode executar.

```markdown
## Checklist de revisão
1. O código resolve o problema descrito?
2. Existem testes cobrindo o caso principal e casos de borda?
3. Há duplicação de lógica que poderia ser reaproveitada?
...
```

### O ciclo de uso

```
Usuário faz um pedido
        │
        ▼
Agente varre as descrições de skills disponíveis
        │
        ▼
"Essa skill se aplica aqui?" → SIM
        │
        ▼
Agente carrega o conteúdo completo da skill
        │
        ▼
Segue as instruções como um checklist/roteiro
```

---

## Skills vs. outros conceitos parecidos

| Conceito | O que é | Analogia |
|---|---|---|
| **Skill** | Instruções/procedimentos empacotados, carregados sob demanda | Manual de procedimento / curso |
| **Tool (ferramenta)** | Uma função concreta que o agente pode *executar* (ler arquivo, rodar comando, chamar API) | As mãos do agente |
| **MCP (Model Context Protocol)** | Um protocolo que conecta o agente a sistemas externos (bancos de dados, apps, serviços) | O "cabo USB" que liga o agente a outro sistema |
| **Plugin/Extensão** | Pacote maior que pode agrupar várias skills, tools e configurações | Uma "caixa de ferramentas" completa |
| **Prompt/System prompt** | Instruções sempre presentes na conversa, desde o início | Ordem permanente, nunca "descarregada" |

Uma skill frequentemente **usa tools** para realizar o que descreve (ex: uma skill de "revisão de código" pode instruir o agente a usar a ferramenta de leitura de arquivos e a de busca).

---

## Tipos comuns de skills

- **Skills de processo** — definem *como abordar* um tipo de problema antes de agir (ex: brainstorming antes de implementar, debugging sistemático antes de propor uma correção).
- **Skills de execução/domínio** — ensinam a produzir um artefato específico (ex: gerar um `.pptx`, um PDF, um gráfico de dados, um documento Word).
- **Skills de fluxo de trabalho** — orquestram múltiplos passos ou até múltiplos agentes (ex: rodar um workflow, agendar tarefas recorrentes).
- **Skills de conhecimento/referência** — trazem documentação especializada sobre uma API, biblioteca ou sistema externo, para o agente não "chutar" com base em memória desatualizada.

---

## Por que isso importa (benefícios)

- **Consistência** — a mesma tarefa é feita do mesmo jeito toda vez.
- **Escalabilidade de contexto** — o agente pode ter acesso a *centenas* de procedimentos sem que todos ocupem espaço na conversa o tempo todo.
- **Especialização sem retreinamento** — não é preciso treinar um novo modelo para ensinar um novo processo; basta escrever/editar um arquivo de texto.
- **Reutilização e compartilhamento** — skills podem ser versionadas, revisadas e compartilhadas entre equipes, como qualquer outro artefato de código.
- **Composição** — skills podem chamar outras skills ou se combinar (ex: uma skill de "processo" decide usar uma skill de "execução" depois).

---

## Exemplo real (self-referencial)

O próprio agente que escreveu este documento (Claude Code) funciona assim: antes de responder, ele varre uma lista de skills disponíveis (cada uma com um `name` e uma `description` curta) e decide se alguma se aplica ao pedido do usuário. Exemplos de skills desse ambiente:

- `code-review` → ativa quando é pedido para revisar um diff ou PR.
- `pdf` → ativa quando a tarefa envolve criar/editar um arquivo PDF.
- `systematic-debugging` → ativa antes de propor correções para um bug.

Isso ilustra bem o padrão: **descrição curta como gatilho → conteúdo detalhado carregado só quando necessário → agente segue o roteiro**.

---

## Resumo em uma frase

> Uma skill é um "manual de instruções" reutilizável e sob demanda que ensina um agente de IA a lidar bem com um tipo específico de tarefa, sem exigir retreinamento do modelo.

---

## Como criar suas próprias skills (Claude Code)

### Onde armazenar

| Escopo                                    | Caminho                                                         | Quando usar                                                                                               |
| ----------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Pessoal** (todos os projetos)           | `~/.claude/skills/<nome-da-skill>/SKILL.md`                     | Técnicas e processos que você usa em qualquer repositório (ex: seu jeito de debugar, de escrever commits) |
| **Do projeto** (compartilhada com o time) | `.claude/skills/<nome-da-skill>/SKILL.md` dentro do repositório | Convenções específicas *daquele* projeto (ex: como rodar os testes, padrão de PR do time)                 |
| **Plugin/Marketplace**                    | Dentro de um plugin instalado (ex: `superpowers`)               | Coleções de skills reutilizáveis entre pessoas/times, distribuídas e versionadas como um pacote           |

> No Windows, o caminho pessoal fica em `C:\Users\<seu-usuário>\.claude\skills\`.

### Estrutura de pastas

Cada skill é uma **pasta própria**, com namespace plano (todas no mesmo nível, sem aninhar categorias):

```
skills/
  minha-skill/
    SKILL.md              # obrigatório — o conteúdo principal
    referencia.md          # opcional — só se precisar de doc pesada (100+ linhas)
    script.py               # opcional — só se for uma ferramenta reutilizável
```

Regra prática: mantenha tudo **dentro do `SKILL.md`** a menos que seja referência muito grande (ex: doc de API) ou um script executável — nesse caso, separe em arquivo próprio e referencie a partir do `SKILL.md`.

### Anatomia do `SKILL.md`

```markdown
---
name: nome-da-skill
description: Use when [situação/gatilho específico que ativa a skill]
---

# Nome da Skill

## Overview
O que é isso e o princípio central, em 1-2 frases.

## When to Use
Lista de sintomas/situações concretas que indicam que essa skill se aplica.
(E, se relevante, quando NÃO usar.)

## Quick Reference
Tabela ou bullets com os pontos principais, fáceis de escanear.

## Implementation
O passo a passo, exemplos de código, checklist — o "como fazer".

## Common Mistakes
Erros comuns e como evitá-los.
```

### Regras importantes sobre o `description`

Esse é o campo que o agente lê **antes** de decidir carregar a skill inteira — é o "gatilho". Por isso:

- ✅ Comece com **"Use when..."** e descreva a **situação/sintoma**, não o processo.
- ❌ Não resuma o passo a passo da skill na descrição — isso faz o agente seguir só a descrição e pular o conteúdo detalhado.
- ✅ Escreva em terceira pessoa (ela é injetada no prompt do sistema).
- ✅ Use palavras-chave que apareceriam numa busca real (nomes de erro, sintomas, ferramentas).

```yaml
# ❌ Ruim — resume o processo, o agente pode parar de ler aqui
description: Revisão de código entre tarefas — primeiro checa specs, depois qualidade

# ✅ Bom — só a condição de gatilho
description: Use when executing implementation plans with independent tasks
```

### Exemplo mínimo de skill própria

```markdown
---
name: revisao-de-pr-time-x
description: Use when abrindo ou revisando um Pull Request neste repositório, antes de aprovar
---

# Revisão de PR — Time X

## Overview
Checklist padrão do time antes de aprovar qualquer PR.

## Quick Reference
1. Testes cobrem o caso principal e ao menos 1 caso de borda?
2. Nome de variáveis em português, funções em inglês (padrão do time)
3. Nenhum `console.log` esquecido
4. Descrição do PR explica o "porquê", não só o "o quê"

## Common Mistakes
- Aprovar sem rodar os testes localmente
- Esquecer de checar se o CHANGELOG foi atualizado
```

Salve isso em `.claude/skills/revisao-de-pr-time-x/SKILL.md` (projeto) ou `~/.claude/skills/revisao-de-pr-time-x/SKILL.md` (pessoal), e o agente passa a considerá-la automaticamente sempre que a tarefa combinar com a descrição.

### Boas práticas ao escrever

- **Seja específico no gatilho, genérico no conteúdo** — a descrição mira uma situação exata; o corpo pode ensinar o princípio geral.
- **Nomes com hífen, em formato verbo-ação** quando fizer sentido (ex: `revisando-prs` em vez de `revisao-de-pr`) — fica mais fácil de buscar.
- **Uma skill = um problema.** Se você está documentando dois processos não relacionados, crie duas skills.
- **Teste antes de confiar nela** — peça para o próprio agente resolver uma tarefa real usando a skill e veja se ele segue certinho; ajuste o texto onde ele "escorregar".
- **Não crie skill para algo que só aconteceu uma vez** — se não é um padrão que vai se repetir, não vale o esforço; melhor deixar como instrução pontual na conversa.
