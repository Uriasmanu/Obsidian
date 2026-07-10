
> Este documento é um material de estudo contínuo. Não precisa ser lido de uma vez só: use-o como referência, volte a ele semanalmente e marque seu progresso nos checklists.

---

## Sumário

1. [Por que comunicação importa tanto quanto código](https://claude.ai/chat/d76e5807-21cc-432c-8d13-b2feea7fa817#1-por-que-comunica%C3%A7%C3%A3o-importa-tanto-quanto-c%C3%B3digo)
2. [Explicando conceitos técnicos para públicos diferentes](https://claude.ai/chat/d76e5807-21cc-432c-8d13-b2feea7fa817#2-explicando-conceitos-t%C3%A9cnicos-para-p%C3%BAblicos-diferentes)
3. [Apresentando projetos com clareza](https://claude.ai/chat/d76e5807-21cc-432c-8d13-b2feea7fa817#3-apresentando-projetos-com-clareza)
4. [Conduzindo reuniões técnicas](https://claude.ai/chat/d76e5807-21cc-432c-8d13-b2feea7fa817#4-conduzindo-reuni%C3%B5es-t%C3%A9cnicas)
5. [Perguntas inteligentes e discussões técnicas](https://claude.ai/chat/d76e5807-21cc-432c-8d13-b2feea7fa817#5-perguntas-inteligentes-e-discuss%C3%B5es-t%C3%A9cnicas)
6. [Comunicação escrita: docs, PRs, commits e issues](https://claude.ai/chat/d76e5807-21cc-432c-8d13-b2feea7fa817#6-comunica%C3%A7%C3%A3o-escrita-docs-prs-commits-e-issues)
7. [Técnicas de oratória: voz, corpo e nervosismo](https://claude.ai/chat/d76e5807-21cc-432c-8d13-b2feea7fa817#7-t%C3%A9cnicas-de-orat%C3%B3ria-voz-corpo-e-nervosismo)
8. [Estruturando apresentações e demos técnicas](https://claude.ai/chat/d76e5807-21cc-432c-8d13-b2feea7fa817#8-estruturando-apresenta%C3%A7%C3%B5es-e-demos-t%C3%A9cnicas)
9. [Exercícios práticos diários e semanais](https://claude.ai/chat/d76e5807-21cc-432c-8d13-b2feea7fa817#9-exerc%C3%ADcios-pr%C3%A1ticos-di%C3%A1rios-e-semanais)
10. [Simulações de situações reais](https://claude.ai/chat/d76e5807-21cc-432c-8d13-b2feea7fa817#10-simula%C3%A7%C3%B5es-de-situa%C3%A7%C3%B5es-reais)
11. [Livros, cursos e materiais recomendados](https://claude.ai/chat/d76e5807-21cc-432c-8d13-b2feea7fa817#11-livros-cursos-e-materiais-recomendados)
12. [Plano de evolução de 90 dias](https://claude.ai/chat/d76e5807-21cc-432c-8d13-b2feea7fa817#12-plano-de-evolu%C3%A7%C3%A3o-de-90-dias)

---

## 1. Por que comunicação importa tanto quanto código

Código bom que ninguém entende, ninguém aprova e ninguém mantém tem valor limitado. Na prática do dia a dia de um desenvolvedor, comunicação é o que transforma trabalho técnico em impacto reconhecido.

### O que a comunicação afeta diretamente

|Área|Impacto de boa comunicação|Impacto de má comunicação|
|---|---|---|
|Code review|Feedback claro, aprendizado mútuo|Atrito, retrabalho, ressentimento|
|Estimativas|Expectativas alinhadas com stakeholders|Promessas quebradas, desconfiança|
|Arquitetura|Decisões documentadas e defensáveis|Decisões questionadas sem contexto|
|Carreira|Visibilidade, promoções, liderança técnica|Trabalho invisível, teto de carreira|
|Times remotos|Assíncrono eficiente, menos reuniões|Mal-entendidos, retrabalho constante|

> **Ideia central:** Comunicação não é "soft skill" no sentido de opcional. É uma competência técnica, assim como saber escrever um algoritmo eficiente. Um dev sênior se diferencia de um pleno mais pela capacidade de alinhar, explicar e influenciar do que pela sintaxe que domina.

### Os três eixos de comunicação de um desenvolvedor

1. **Comunicação técnica com pares** — code review, pair programming, discussões de arquitetura.
2. **Comunicação vertical** — com gestores, product owners, liderança.
3. **Comunicação externa** — com clientes, usuários finais, outras áreas do negócio.

Este guia trabalha os três eixos.

---

## 2. Explicando conceitos técnicos para públicos diferentes

O erro mais comum é usar o mesmo nível de detalhe técnico para qualquer audiência. A habilidade central aqui é **calibrar a profundidade** conforme quem ouve.

### Modelo de três camadas

Para qualquer conceito técnico, prepare três versões:

|Camada|Público|Foco|Duração|
|---|---|---|---|
|Camada 1 — Resultado|Cliente, diretoria|O que muda para o negócio/usuário|30 segundos|
|Camada 2 — Solução|Gestor, PO|Como resolve o problema, trade-offs, riscos|2 a 5 minutos|
|Camada 3 — Implementação|Devs, arquitetos|Detalhes técnicos, decisões de design|10+ minutos|

**Exemplo prático — explicando um sistema de cache:**

- **Para o cliente:** "Isso vai fazer o sistema responder mais rápido para o usuário final, especialmente em horários de pico."
- **Para o gestor:** "Vamos adicionar uma camada de cache Redis. Isso reduz carga no banco de dados e o tempo de resposta médio deve cair de 800ms para 150ms. O custo é uma complexidade extra na invalidação de dados, que vamos mitigar com TTL configurável."
- **Para outro dev:** "Implementei um cache distribuído com Redis, usando cache-aside pattern. As chaves seguem o padrão `entidade:id:versao` e o TTL é de 10 minutos, exceto para dados de configuração que invalidamos manualmente via pub/sub quando há alteração."

### Técnica da analogia

Analogias reduzem a carga cognitiva de quem não é técnico. Algumas prontas para reutilizar:

- **API:** "é como um cardápio de restaurante — você escolhe o prato pelo nome, sem precisar saber como a cozinha prepara."
- **Banco de dados vs cache:** "o banco é o arquivo morto completo; o cache é o post-it na sua mesa com a informação que você usa toda hora."
- **Fila de mensagens:** "é como uma fila de banco — os pedidos chegam e são processados na ordem, sem sobrecarregar o atendente."
- **Migração de sistema legado:** "é como reformar uma casa habitada — não dá para derrubar tudo de uma vez, tem que fazer cômodo por cômodo enquanto a família continua morando ali."

> **Exercício:** para os próximos 5 conceitos técnicos que você explicar, crie a analogia antes de explicar o conceito técnico em si. Anote as que funcionaram melhor.

### Erros comuns a evitar

- Usar jargão sem definir ("vamos fazer um refactor no service layer usando dependency injection") para quem não é dev.
- Assumir que "simplificar" significa "mentir" — simplificar é remover detalhe irrelevante para a decisão que a pessoa precisa tomar, não distorcer a realidade.
- Falar por 10 minutos sem checar se a pessoa está entendendo. Pare a cada 2-3 minutos e pergunte: "Isso faz sentido até aqui?"

---

## 3. Apresentando projetos com clareza

### A estrutura SCQA (Situação, Complicação, Questão, Ação)

Uma estrutura clássica de consultoria, muito eficaz para apresentar projetos:

1. **Situação:** contexto atual, o que existe hoje.
2. **Complicação:** o problema, o que está quebrado ou faltando.
3. **Questão:** a pergunta implícita que isso gera ("como resolvemos isso?").
4. **Ação:** a solução proposta e os próximos passos.

**Exemplo:**

> "Hoje o cadastro de clientes leva em média 40 segundos para carregar (Situação). Isso está gerando reclamações e abandono de cadastro, principalmente no mobile (Complicação). Precisamos entender se o gargalo é de banco, rede ou frontend, e resolver antes do lançamento da campanha do mês que vem (Questão). Propomos investigar com profiling nesta semana e implementar paginação + cache como primeira ação, com entrega prevista para sexta (Ação)."

### Checklist para apresentar um projeto

- [ ] Comecei pelo "porquê" antes do "como"?
- [ ] Defini o público e ajustei o nível técnico?
- [ ] Tenho um resumo de uma frase que resume o projeto inteiro?
- [ ] Mostrei o estado atual vs. estado proposto (antes/depois)?
- [ ] Apontei riscos e trade-offs, não só benefícios?
- [ ] Tenho próximos passos claros com responsáveis e prazos?
- [ ] Preparei resposta para a pergunta "quanto tempo vai levar?"
- [ ] Preparei resposta para a pergunta "quanto vai custar / quais os riscos?"

### Regra do "Elevator Pitch" técnico

Treine resumir qualquer projeto seu em 3 frases:

1. Qual problema resolve.
2. Como resolve (em alto nível).
3. Qual o impacto esperado.

> **Dica:** grave um áudio de 30 segundos explicando seu projeto atual como se fosse para alguém no elevador. Ouça de volta. Corte qualquer parte que não seja essencial.

---

## 4. Conduzindo reuniões técnicas

### Daily (Standup)

**Objetivo:** sincronizar o time, não reportar para o gestor.

Estrutura recomendada por pessoa (60-90 segundos):

- O que fiz ontem (foco em entrega, não em atividade).
- O que farei hoje.
- Impedimentos (se houver).

> **Evite:** narrar linha por linha o que foi feito. Prefira "Terminei a integração com o gateway de pagamento, hoje começo os testes de carga" a "Ontem fiz um monte de coisa, mexi em vários arquivos, tentei resolver um bug...".

### Planning

- Leve o contexto do problema, não só a lista de tarefas.
- Use perguntas abertas para o time discutir riscos: "O que pode dar errado aqui?", "Já vimos algo parecido antes?"
- Feche com critérios de aceite claros por item.

### Refinamento (Refinement / Backlog Grooming)

Checklist de perguntas para conduzir um refinamento:

- [ ] O problema está claro para todos, não só a solução?
- [ ] Existem dependências externas (outras equipes, APIs de terceiros)?
- [ ] Os critérios de aceite estão escritos, não só verbais?
- [ ] Alguém já perguntou "e se..." para casos de borda?
- [ ] O time tem uma estimativa (ainda que grosseira) antes de sair da sala?

### Retrospectiva

Modelo simples e eficaz: **Continuar / Parar / Começar**.

|Continuar|Parar|Começar|
|---|---|---|
|O que está funcionando bem e deve seguir|O que está atrapalhando e deve ser descontinuado|O que ainda não fazemos e deveríamos experimentar|

**Regras de ouro para quem conduz:**

- Não personalize problemas ("o commit do João quebrou tudo"). Foque no processo ("nosso pipeline de CI não pegou esse erro antes do merge").
- Toda ação levantada precisa ter um dono e um prazo, senão vira lista de desejos.
- Termine com no máximo 2-3 ações concretas, não 15.

### Reunião técnica de arquitetura / design review

- Envie o contexto **antes** da reunião (documento, diagrama, RFC). Reunião não é para ler, é para discutir.
- Estruture como: contexto → alternativas consideradas → trade-offs → proposta → perguntas abertas.
- Sempre apresente **pelo menos duas alternativas**, mesmo que uma seja claramente melhor — isso mostra que você considerou opções e facilita a defesa da escolha.

---

## 5. Perguntas inteligentes e discussões técnicas

### Como fazer perguntas que geram valor

Uma pergunta inteligente geralmente:

- Demonstra que você já tentou entender antes de perguntar.
- É específica, não genérica.
- Abre espaço para discussão, não fecha em "sim/não" quando o objetivo é explorar.

|Pergunta fraca|Pergunta forte|
|---|---|
|"Isso funciona?"|"Testamos esse fluxo com 10x o volume normal de requisições? Qual o comportamento esperado sob carga?"|
|"Por que fizeram assim?" (tom de crítica)|"Qual foi o principal fator que levou a essa decisão de arquitetura? Tinha alguma restrição que eu não conheço?"|
|"Não entendi nada"|"Entendi a parte do fluxo de autenticação, mas fiquei em dúvida em como o token é renovado. Pode detalhar essa parte?"|

### Framework para participar de discussões técnicas

1. **Ouça a posição completa antes de discordar.** Resuma o que entendeu antes de contra-argumentar: "Se entendi bem, sua proposta é X porque Y. Correto?"
2. **Separe fato de opinião.** "Os dados mostram que a latência dobrou" (fato) é diferente de "acho que isso vai ficar lento" (opinião/hipótese).
3. **Traga dados sempre que possível.** Benchmarks, métricas, casos reais pesam mais que preferência pessoal.
4. **Ofereça alternativas, não só críticas.** "Isso pode ter um problema de N+1 query" é menos útil do que "Isso pode ter um problema de N+1 query, uma alternativa seria usar eager loading aqui."
5. **Saiba ceder.** Nem toda discussão precisa ser vencida. Pergunte-se: "essa diferença realmente importa para o resultado final?"

> **Caixa de destaque — Desacordo saudável:** discordar de uma solução não é discordar da pessoa. Frases como "eu vejo de um jeito diferente, deixa eu explicar por quê" mantêm a discussão no nível técnico.

---

## 6. Comunicação escrita: docs, PRs, commits e issues

### Mensagens de commit

Estrutura recomendada (padrão Conventional Commits):

```
tipo(escopo): resumo curto no imperativo

Corpo explicando o quê e por quê (não o como — isso o diff já mostra).

Refs: TASK-123
```

Exemplo:

```
fix(sync): evita gravação de NULL quando IED envia mensagem incompleta

Adiciona validação de payload antes de persistir no histórico.
Mensagens incompletas agora são descartadas e logadas para análise.

Refs: SIGMA-482
```

**Checklist de commit:**

- [ ] O resumo cabe em uma linha e está no imperativo ("adiciona", não "adicionado" ou "adicionando")?
- [ ] O corpo explica o motivo da mudança, não apenas o que mudou?
- [ ] Referenciei a tarefa/issue relacionada?

### Pull Requests

Uma boa descrição de PR responde a três perguntas:

1. **O que mudou?**
2. **Por quê?**
3. **Como testar / o que revisar com atenção?**

**Template sugerido:**

```markdown
## O que muda
Breve resumo da mudança.

## Por quê
Contexto do problema ou da necessidade.

## Como testar
Passos para validar localmente.

## Pontos de atenção
Áreas do código que merecem revisão mais cuidadosa.

## Screenshots / evidências (se aplicável)
```

> **Dica:** PRs pequenos e focados recebem revisão mais rápida e de melhor qualidade que PRs grandes e genéricos. Se o PR mexe em mais de 400-500 linhas, considere dividir.

### Comentários de code review

|Em vez de|Prefira|
|---|---|
|"Isso está errado."|"Acho que isso pode gerar um problema quando X. O que acha de fazer Y?"|
|"Por que você fez assim?"|"Curioso sobre o motivo dessa abordagem — teve algum motivo específico?"|
|"Ruim."|"Essa parte ficou difícil de acompanhar. Que tal extrair em uma função com nome mais descritivo?"|

### Documentação técnica e issues

- Escreva o "porquê" antes do "como". Documentação sem contexto envelhece mal.
- Use exemplos reais de uso, não só descrição abstrata.
- Ao abrir uma issue de bug, inclua: comportamento esperado, comportamento observado, passos para reproduzir, ambiente.

---

## 7. Técnicas de oratória: voz, corpo e nervosismo

### Reduzindo o nervosismo

- **Respiração diafragmática:** inspire em 4 tempos, segure por 4, expire em 6. Faça isso 3-5 vezes antes de falar. Reduz a resposta fisiológica de ansiedade.
- **Preparação, não decoreba:** decorar palavra por palavra aumenta o pânico caso você esqueça algo. Prepare tópicos-chave e permita-se falar com suas próprias palavras.
- **Chegue cedo / teste o ambiente:** se for apresentação presencial ou por vídeo, testar o setup antes reduz uma fonte comum de ansiedade.
- **Reframe fisiológico:** a ativação do corpo antes de falar em público (coração acelerado, mãos suando) é quase idêntica à de entusiasmo. Dizer para si mesmo "estou animado" em vez de "estou nervoso" ajuda o cérebro a reinterpretar o sinal.

### Dicção e clareza

- Grave-se falando por 1 minuto sobre um tema técnico e ouça de volta. Identifique vícios de linguagem ("né", "tipo", "então assim").
- Pratique articulação com exercícios de trava-língua leves antes de apresentações importantes.
- Fale um pouco mais devagar do que parece natural — sob nervosismo, tendemos a acelerar sem perceber.

### Tom de voz e ritmo

|Elemento|Como ajustar|
|---|---|
|Volume|Projete a voz, especialmente em salas grandes ou calls com múltiplas pessoas|
|Pausas|Use pausas de 1-2 segundos após pontos importantes — dá tempo para a informação ser processada|
|Ênfase|Varie o tom para destacar palavras-chave; tom monótono é o principal motivo de perda de atenção|
|Ritmo|Alterne entre trechos mais rápidos (contexto já conhecido) e mais lentos (pontos críticos)|

### Postura e linguagem corporal (presencial ou câmera ligada)

- Mantenha os ombros relaxados, evite cruzar os braços.
- Use as mãos para reforçar pontos, mas evite gestos repetitivos e nervosos.
- Olhe para a câmera (não para sua própria imagem) em reuniões remotas — simula contato visual.
- Em apresentações presenciais, distribua o olhar entre diferentes pessoas da plateia, não fixe em uma só.

> **Exercício semanal:** grave-se explicando algo técnico por 2 minutos, sem cortes. Assista de volta prestando atenção em: ritmo, vícios de linguagem, postura, tom. Repita a mesma explicação melhorando um ponto por vez.

---

## 8. Estruturando apresentações e demos técnicas

### Estrutura geral de uma apresentação técnica

1. **Abertura (10%):** contexto e objetivo da apresentação. O que a audiência vai saber/decidir ao final.
2. **Desenvolvimento (70%):** conteúdo principal, organizado do mais geral para o mais específico.
3. **Fechamento (20%):** resumo, próximos passos, espaço para perguntas.

### Estrutura específica para demos de produto/funcionalidade

1. Mostre o **problema real** que a funcionalidade resolve (idealmente com um cenário concreto).
2. Demonstre o fluxo **do ponto de vista do usuário**, não da implementação.
3. Só entre em detalhes técnicos se o público pedir ou se for uma demo para outros devs.
4. Termine com o que vem a seguir (limitações conhecidas, próximos passos).

**Checklist pré-demo:**

- [ ] Testei o fluxo completo antes de apresentar (evite bugs ao vivo)?
- [ ] Tenho um plano B se algo falhar (print, vídeo gravado, ambiente alternativo)?
- [ ] Sei responder "e se o usuário fizer X diferente do esperado?"
- [ ] Removi dados sensíveis/reais da tela?

### Apresentando decisões de arquitetura

Estrutura recomendada (similar a um ADR — Architecture Decision Record):

```markdown
## Contexto
Qual problema estamos resolvendo e por quê agora.

## Alternativas consideradas
- Opção A: prós e contras
- Opção B: prós e contras
- Opção C: prós e contras

## Decisão
Qual foi escolhida e por quê.

## Consequências
O que isso implica no curto e no longo prazo (positivo e negativo).
```

### Slides: princípios básicos

- Um slide, uma ideia principal.
- Prefira diagramas a parágrafos longos.
- Números e métricas em destaque visual (tamanho, cor).
- Evite ler o slide — o slide é apoio visual, não o roteiro da fala.

---

## 9. Exercícios práticos diários e semanais

### Rotina diária (5-15 minutos)

|Dia|Exercício|
|---|---|
|Segunda|Explique em voz alta, em 1 minuto, o que você vai fazer na semana — como se fosse para o gestor|
|Terça|Escreva a descrição de um PR seguindo o template da seção 6|
|Quarta|Grave um áudio de 30s explicando um conceito técnico para um público não técnico|
|Quinta|Faça pelo menos 1 pergunta "forte" (seção 5) em uma discussão real do dia|
|Sexta|Releia um comentário de code review que você escreveu e reescreva de forma mais construtiva|
|Sábado/Domingo|Leitura ou vídeo de um material da seção 11 (30 min)|

### Rotina semanal

- [ ] Participei ativamente de pelo menos uma reunião (não só ouvindo)?
- [ ] Escrevi ao menos uma documentação ou comentário de PR aplicando as técnicas deste guia?
- [ ] Pratiquei uma apresentação (real ou simulada) em voz alta?
- [ ] Pedi feedback sobre minha comunicação para ao menos uma pessoa (par, gestor, cliente)?
- [ ] Revisei uma gravação minha (áudio ou vídeo) e identifiquei um ponto de melhoria?

> **Dica:** mantenha um "diário de comunicação" simples — um bloco de notas onde você anota, uma vez por dia, uma situação em que se comunicou bem e uma em que poderia ter sido melhor. Revisar isso semanalmente acelera muito o progresso.

---

## 10. Simulações de situações reais

Use estas simulações sozinho (gravando-se) ou com um colega/mentor.

### Simulação 1: Entrevista técnica

**Cenário:** o entrevistador pede para você explicar um projeto do seu portfólio.

- Pratique a resposta usando a estrutura: contexto → seu papel → desafio técnico → solução → resultado.
- Treine explicar uma decisão técnica que você tomou e teria feito diferente hoje — isso demonstra maturidade.
- Simule uma pergunta de sistema ("como você projetaria X?") pensando em voz alta, mostrando o raciocínio, não só a resposta final.

### Simulação 2: Code review difícil

**Cenário:** você precisa apontar um problema sério em um PR de um colega mais experiente.

- Pratique abrir com uma pergunta, não uma afirmação: "Vi que essa parte usa consulta direta ao banco em loop — teve algum motivo específico para não usar batch aqui?"
- Prepare-se para o caso de ele discordar: tenha dados ou exemplos prontos (benchmark, caso de produção anterior).

### Simulação 3: Apresentação de arquitetura para o time

**Cenário:** você propõe migrar um serviço para uma nova abordagem (ex: de monolito para módulo separado).

- Estruture com a seção 8 (Contexto → Alternativas → Decisão → Consequências).
- Simule pelo menos duas objeções ("isso não vai atrasar a entrega?", "por que não continuar como está?") e prepare respostas.

### Simulação 4: Defesa de decisão técnica sob questionamento

**Cenário:** um stakeholder questiona por que algo "tão simples" está demorando tanto.

- Pratique traduzir complexidade técnica em termos de risco de negócio: "Podemos entregar mais rápido, mas isso aumenta o risco de bugs em produção durante o pico de vendas. Prefere essa opção ou o prazo um pouco maior com mais segurança?"
- Evite tom defensivo. Foque em apresentar trade-offs, não em "se justificar".

### Simulação 5: Comunicação direta com cliente

**Cenário:** o cliente relata um "bug" que na verdade é uma limitação conhecida do sistema.

- Pratique validar a frustração do cliente antes de explicar: "Entendo que isso atrapalha seu fluxo. Deixa eu explicar o que está acontecendo e as opções que temos."
- Evite jargão técnico. Foque no impacto e nas opções concretas de solução.

### Simulação 6: Trabalho em equipe sob pressão de prazo

**Cenário:** o time percebe, faltando dois dias para a entrega, que uma funcionalidade não vai ficar pronta.

- Pratique comunicar o problema cedo, com transparência, propondo alternativas (reduzir escopo, negociar prazo, priorizar o essencial), em vez de esconder o atraso até o último momento.

---

## 11. Livros, cursos e materiais recomendados

### Livros sobre comunicação e oratória

- **"Como Fazer Amigos e Influenciar Pessoas"** — Dale Carnegie. Clássico atemporal sobre relacionamento interpessoal.
- **"Falar em Público sem Medo"** — abordagens práticas de controle de ansiedade e estrutura de discurso (procure edições atualizadas com técnicas de storytelling).
- **"Made to Stick"** — Chip Heath e Dan Heath. Sobre como tornar ideias memoráveis, muito aplicável a explicações técnicas.
- **"The Pyramid Principle"** — Barbara Minto. A base do raciocínio estruturado (e do modelo SCQA usado na seção 3).
- **"Crucial Conversations"** — Kerry Patterson et al. Excelente para conversas difíceis (feedback, desacordos técnicos).

### Livros sobre comunicação técnica especificamente

- **"The Pragmatic Programmer"** — capítulos sobre comunicação e documentação.
- **"Soft Skills: The Software Developer's Life Manual"** — John Sonmez.
- **"Docs for Developers"** — Jared Bhatti et al. Focado em documentação técnica de qualidade.

### Cursos e canais

- Cursos de oratória e apresentação em plataformas como Coursera, Udemy e Alura (busque por "comunicação assertiva", "public speaking", "storytelling para negócios").
- Canais no YouTube sobre arquitetura de software costumam ser ótimas referências de **como explicar** conceitos complexos de forma acessível — preste atenção não só no conteúdo, mas em como o apresentador estrutura a explicação.
- TED Talks sobre tecnologia: analise a estrutura da fala (abertura, história, dados, fechamento), não só o conteúdo.

### Comunidades e prática

- Participe de meetups técnicos e se candidate a apresentar um tema pequeno — é o ambiente de prática mais próximo do real.
- Toastmasters (clubes de oratória) é uma opção estruturada com feedback constante, presente em várias cidades e também online.

---

## 12. Plano de evolução de 90 dias

### Visão geral

|Fase|Semanas|Foco principal|
|---|---|---|
|Fase 1 — Fundação|1 a 4|Autoconsciência, comunicação escrita, base de oratória|
|Fase 2 — Aplicação|5 a 8|Reuniões, apresentações, discussões técnicas|
|Fase 3 — Consolidação|9 a 12|Simulações completas, feedback externo, refinamento|

### Fase 1 (Semanas 1-4) — Fundação

**Metas semanais:**

- **Semana 1:** Gravar-se falando 3 vezes (2 min cada), identificar 3 vícios de linguagem recorrentes.
- **Semana 2:** Reescrever 5 mensagens de commit e 2 descrições de PR usando os templates da seção 6.
- **Semana 3:** Aplicar a estrutura de 3 camadas (seção 2) em pelo menos 3 explicações reais no trabalho.
- **Semana 4:** Praticar respiração e postura antes de 2 reuniões reais; anotar diferença percebida.

**Métrica de progresso:** número de vícios de linguagem por minuto de fala (meta: reduzir em 50% até o fim da fase).

### Fase 2 (Semanas 5-8) — Aplicação

- **Semana 5:** Conduzir ativamente uma daily ou planning usando as estruturas da seção 4.
- **Semana 6:** Fazer pelo menos 3 perguntas "fortes" documentadas em reuniões reais (seção 5).
- **Semana 7:** Apresentar um tema técnico curto (10-15 min) para o time ou em um meetup.
- **Semana 8:** Conduzir uma retrospectiva usando o modelo Continuar/Parar/Começar.

**Métrica de progresso:** feedback qualitativo de pelo menos 2 colegas sobre clareza nas reuniões.

### Fase 3 (Semanas 9-12) — Consolidação

- **Semana 9:** Realizar a Simulação 3 (apresentação de arquitetura) com um colega, gravando e revisando.
- **Semana 10:** Realizar a Simulação 5 (comunicação com cliente) em uma situação real ou simulada.
- **Semana 11:** Escrever um documento técnico completo (ADR ou RFC) aplicando a seção 6 e 8.
- **Semana 12:** Apresentação final — tema técnico de sua escolha, 15-20 minutos, para audiência mista (dev + não dev), com sessão de perguntas.

**Métrica de progresso:** comparar a gravação da semana 12 com a da semana 1 — avaliar ritmo, clareza, vícios de linguagem e estrutura.

### Checklist final de acompanhamento (revisar a cada 2 semanas)

- [ ] Reduzi vícios de linguagem perceptíveis nas gravações?
- [ ] Recebo menos perguntas de esclarecimento após minhas explicações?
- [ ] Sinto menos ansiedade física antes de falar em reuniões?
- [ ] Consigo adaptar o nível técnico da explicação conforme a audiência sem esforço consciente?
- [ ] Meus PRs e commits são aprovados com menos rodadas de dúvida?
- [ ] Já conduzi pelo menos uma reunião (planning, retro ou daily) do início ao fim?
- [ ] Já apresentei algo tecnicamente para uma audiência não puramente técnica?
- [ ] Tenho um "diário de comunicação" atualizado com observações semanais?

> ⚠️ **Atenção:** este plano é um guia, não uma camisa de força. Se uma semana não seguir o cronograma exato, o importante é retomar a prática na semana seguinte — consistência ao longo dos 90 dias importa mais do que cumprir a risca cada etapa.

---

## Referência rápida (resumo de uma página)

- **Antes de explicar algo técnico:** identifique a audiência e escolha a camada certa (seção 2).
- **Antes de uma reunião:** saiba o objetivo dela e a estrutura esperada (seção 4).
- **Antes de discordar:** resuma o que entendeu, depois contra-argumente com dados (seção 5).
- **Antes de escrever um PR ou commit:** responda o quê, por quê e como testar (seção 6).
- **Antes de apresentar:** respire, estruture em SCQA, teste o ambiente (seções 3, 7 e 8).
- **Toda semana:** grave-se, revise, ajuste um ponto de cada vez (seção 9).