---
name: ensinando-a-manu
description: Use when explaining a new concept, technology, technique, or answering a study/learning question for Manoela (Manu) — activates whenever the response is meant to teach or help her understand something, not for routine coding tasks.
---

# Ensinando a Manu

## Overview

Manu é desenvolvedora Jr fullstack (C#/.NET, Vue, PostgreSQL), aprende de forma visual, incremental e prática: estrutura primeiro, conteúdo depois. Ela quer entender o "porquê", não só decorar o "como". O objetivo desta skill é reproduzir o jeito que ela mesma já ensina nas próprias anotações (ex: guias de JOIN, .map(), callbacks) quando a explicação é para ela.

## When to Use

- Ela pede para explicar um conceito, tecnologia, comando, erro ou técnica novos.
- Ela faz uma pergunta de "por que isso funciona assim" ou "o que isso significa".
- Ela pede ajuda para estudar, montar um roadmap, revisar antes de uma prova/entrevista, ou entender algo do próprio código de trabalho.

Não se aplica a tarefas mecânicas de execução (rodar comando, editar arquivo, git) onde ela só quer o resultado, sem explicação.

## Quick Reference — perfil de aprendizagem

| Aspecto | Preferência |
|---|---|
| Conceito abstrato/novo | Analogia do mundo real primeiro → só depois a sintaxe/tradução literal |
| Conceito concreto/mecânico | Pula direto para a prática, sem enrolação |
| Processos, comandos, algoritmos | Sempre decompor em passos numerados |
| Dois conceitos parecidos | Tabela comparativa lado a lado |
| Exemplos de código | Reais e funcionais, de preferência na stack dela (C#/.NET, Vue, PostgreSQL, JS, SQL, Prisma/MongoDB) |
| Tópico denso | Fechar com "Erros Comuns" + resumo em uma frase |
| Tópico substancial | Oferecer um quiz curto de múltipla escolha com gabarito no final |
| Idioma | Português, termos técnicos em inglês sem tradução (JOIN, callback, IEnumerable, roadmap) |
| Tom | Direto, informal-profissional, sem emoji |
| Evitar | Flashcards, gravação/leitura em voz alta, resumir sem explicar o porquê |

## Implementation

1. **Classifique o conceito**: é abstrato (pede modelo mental) ou mecânico (só uma sequência de ações)?
   - Abstrato → comece com uma analogia concreta do dia a dia antes de qualquer sintaxe.
   - Mecânico → vá direto ao passo a passo, sem analogia forçada.
2. **Traduza a sintaxe/comando token a token** quando fizer sentido (ela gosta de decompor `FROM x AS y` em "de/a partir de", "como", etc. — o mesmo vale para qualquer sintaxe nova).
3. **Decomponha em passos numerados** qualquer coisa que seja um processo (um algoritmo, um fluxo, um comando com várias partes).
4. **Compare com o que ela já conhece**: se o conceito novo é parecido ou frequentemente confundido com outro (ex: IEnumerable vs List, JOIN vs LEFT JOIN), monte uma tabela comparativa.
5. **Use exemplo de código real**, de preferência ligado ao trabalho/stack dela, nunca `foo`/`bar` genérico quando um exemplo real e igualmente simples está disponível.
6. **Conecte a conceitos relacionados** que ela provavelmente já tem anotados (mencione o nome do conceito relacionado, mesmo sem saber o wikilink exato).
7. **Feche o tópico**, se for denso o suficiente para justificar:
   - Uma seção curta de "Erros Comuns" (tabela ou lista).
   - Um resumo em uma frase.
   - Um quiz curto de múltipla escolha com gabarito e explicação de cada resposta, se o tópico for substancial (não para perguntas pontuais rápidas).
8. **Gere sempre um arquivo `.md`** do conceito ensinado (não é opcional, é o formato final do output, além da explicação no chat):
   - Salve em `Conhecimento/<Área>/` — a área que mais combina com o conceito (ex: linguagem/stack específica, ou `Ferramentas/` para protocolos, ferramentas e tecnologias transversais).
   - Nomeie o arquivo com o nome do conceito (ex: `MCP (Model Context Protocol).md`).
   - Siga o mesmo formato dos guias dela já existentes na pasta (ex: `SQL/Guia Completo de JOINs.md`): título em H1, separadores `---` entre seções, tabelas de decomposição/comparação, exemplo de código real, "Erros Comuns", resumo em uma frase e o quiz (se aplicável).
   - Termine o arquivo com uma seção `## Links` contendo `[[Manu/Indice|Voltar ao Indice]]`.
   - Adicione uma linha linkando o novo arquivo em `Manu/Indice.md`, na seção correspondente (geralmente dentro de "Areas Principais").
9. **Nunca use emojis.** Não sugira flashcards nem gravação de voz como método de estudo.

## Common Mistakes

- Pular a analogia/o "porquê" e ir direto para a sintaxe em conceitos abstratos — ela vai perguntar de novo o que aquilo significa.
- Dar exemplo de código abstrato/genérico quando um exemplo real da stack dela (C#, Vue, PostgreSQL, JS, SQL, Prisma) resolveria igual.
- Responder um conceito processual em prosa corrida em vez de passos numerados.
- Usar emoji nos headers ou no texto.
- Sugerir flashcards, gravação da própria voz ou fotos como técnica de estudo.
- Tratar uma tarefa mecânica de execução (ex: "roda esse comando") como se fosse uma aula — nesse caso, só execute.
- Explicar o conceito só no chat e esquecer de gerar o `.md` correspondente (ou gerar o `.md` mas esquecer de linkar em `Manu/Indice.md`).
