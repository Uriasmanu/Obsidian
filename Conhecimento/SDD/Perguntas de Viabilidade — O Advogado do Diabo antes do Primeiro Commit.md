
## 1. Introdução

A maioria dos projetos de software não morre por falta de código. Morre por falta de perguntas feitas cedo o suficiente. Times técnicos são treinados para resolver problemas, não para questionar se o problema vale a pena ser resolvido — e é exatamente nessa lacuna que orçamentos inteiros desaparecem, prazos duplicam e produtos são lançados para audiências que nunca existiram.

Este documento existe para forçar um desconforto necessário. Antes de qualquer linha de código, protótipo ou reunião de kickoff, o projeto precisa sobreviver a um interrogatório honesto. Não se trata de pessimismo gratuito — trata-se de transferir o custo da dúvida para o momento mais barato possível: antes de construir, não depois.

Uma boa análise crítica não busca confirmar o que os patrocinadores do projeto já acreditam. Busca o contrário: encontrar o motivo pelo qual o projeto poderia falhar, e verificar se esse motivo já foi neutralizado com evidências reais — não com otimismo, não com "vai dar certo porque a gente é bom", e não com benchmarks de mercado genéricos que não dizem nada sobre o caso específico.

Se o projeto sobreviver a este documento, ele estará mais forte. Se não sobreviver, é melhor descobrir isso agora.

**Aviso:** ⚠️ este processo deve ser desconfortável. Se todas as respostas vierem fáceis e verdes, é provável que as perguntas não estejam sendo levadas a sério.

---

## 2. Estrutura de Perguntas por Categoria

### 2.1 Negócio e Modelo de Receita

**Pergunta 1: Qual problema real este projeto resolve, e para quem, especificamente?**

- O que está sendo testado: se existe um problema validado ou apenas uma solução em busca de problema.
- 🟢 Verde: "Entrevistamos 40 clientes em segmentos distintos e 78% relataram perder mais de 5h/semana com este processo manual, com dados de suporte comprovando o volume de reclamações."
- 🔴 Vermelho: "Achamos que seria legal ter isso" ou "um concorrente lançou algo parecido".

**Pergunta 2: Como exatamente este projeto gera receita, e em quanto tempo o breakeven é esperado?**

- O que está sendo testado: se existe um modelo de monetização concreto, não apenas uma métrica de vaidade (usuários, downloads).
- 🟢 Verde: Modelo de receita definido (assinatura, transação, licença) com precificação testada em piloto pago.
- 🔴 Vermelho: "Vamos monetizar depois que tivermos escala" sem hipótese testável de como.

**Pergunta 3: Quem paga por isso, e essa pessoa tem orçamento e autoridade para pagar?**

- O que está sendo testado: confusão comum entre "usuário" e "comprador" em produtos B2B.
- 🟢 Verde: Comprador identificado com budget line já existente para esse tipo de solução.
- 🔴 Vermelho: "O usuário final vai adorar" sem identificar quem assina o cheque.

**Pergunta 4: O que acontece com o negócio se este projeto simplesmente não existisse?**

- O que está sendo testado: se o projeto é essencial ou apenas desejável.
- 🟢 Verde: Consequência concreta e mensurável (perda de contrato, multa regulatória, churn comprovado).
- 🔴 Vermelho: "Ficaríamos atrás da concorrência" sem quantificação.

---

### 2.2 Mercado e Concorrência

**Pergunta 5: Quem já resolveu esse problema, e por que os clientes ainda não usam essa solução?**

- O que está sendo testado: ingenuidade sobre concorrência direta e indireta (incluindo planilhas e processos manuais).
- 🟢 Verde: Mapeamento de 3+ concorrentes diretos com análise de gaps reais que eles não cobrem.
- 🔴 Vermelho: "Não tem concorrente" — quase sempre um sinal de mercado inexistente ou pesquisa rasa.

**Pergunta 6: Qual é o tamanho real do mercado endereçável, com fonte verificável?**

- O que está sendo testado: se o TAM/SAM/SOM é estimado com metodologia ou "chutado de cima para baixo".
- 🟢 Verde: Estimativa bottom-up baseada em número real de clientes potenciais identificáveis.
- 🔴 Vermelho: "O mercado de tecnologia é de trilhões" aplicado sem recorte.

**Pergunta 7: O que impede um concorrente com mais recursos de copiar isso em 3 meses?**

- O que está sendo testado: existência de vantagem competitiva defensável (dados proprietários, rede, custo de troca).
- 🟢 Verde: Barreira identificada e defensável (integração profunda, dados históricos, contrato de exclusividade).
- 🔴 Vermelho: "Seríamos os primeiros" como única vantagem.

---

### 2.3 Usuários e Experiência (UX/UI)

**Pergunta 8: Algum usuário real, fora da empresa, já usou um prototótipo e completou a tarefa principal sem ajuda?**

- O que está sendo testado: validação real vs. suposição interna sobre usabilidade.
- 🟢 Verde: Testes de usabilidade com 5+ usuários reais, taxa de conclusão de tarefa documentada.
- 🔴 Vermelho: "O time achou intuitivo" como única validação.

**Pergunta 9: Qual é a jornada do usuário quando algo dá errado (erro, timeout, dado ausente)?**

- O que está sendo testado: se o design cobre apenas o "caminho feliz".
- 🟢 Verde: Fluxos de erro mapeados com mensagens e recuperação definidas.
- 🔴 Vermelho: Nenhuma tela de erro no protótipo.

**Pergunta 10: Este produto foi pensado para acessibilidade e para dispositivos/conexões reais do público-alvo?**

- O que está sendo testado: suposição de que todo usuário tem hardware/internet ideal.
- 🟢 Verde: Testado em conexões lentas, dispositivos de entrada e com critérios básicos de acessibilidade (WCAG).
- 🔴 Vermelho: Testado apenas em notebook de desenvolvedor com internet de fibra.

---

### 2.4 Tecnologia e Arquitetura

**Pergunta 11: Por que esta stack específica, e quais alternativas foram descartadas e por quê?**

- O que está sendo testado: decisão técnica deliberada vs. escolha por familiaridade da equipe.
- 🟢 Verde: Comparativo documentado de 2-3 opções com critérios objetivos (custo, curva de aprendizado, ecossistema).
- 🔴 Vermelho: "É o que a gente já sabe usar" sem avaliar adequação ao problema.

**Pergunta 12: O que acontece com o sistema sob 10x o volume esperado de uso?**

- O que está sendo testado: planejamento de escalabilidade real, não teórica.
- 🟢 Verde: Teste de carga executado com métricas de degradação documentadas.
- 🔴 Vermelho: "A gente escala quando precisar" sem arquitetura preparada para isso.

**Pergunta 13: Existe dependência crítica de um único fornecedor, biblioteca ou pessoa (bus factor)?**

- O que está sendo testado: risco de ponto único de falha técnico ou humano.
- 🟢 Verde: Dependências críticas mapeadas com plano de mitigação ou substituição.
- 🔴 Vermelho: Sistema inteiro depende do conhecimento de uma única pessoa não documentado.

---

### 2.5 Dados e Privacidade (LGPD/GDPR)

**Pergunta 14: Que dados pessoais serão coletados, e existe base legal específica para cada finalidade?**

- O que está sendo testado: conformidade real com LGPD/GDPR, não apenas um banner de cookies.
- 🟢 Verde: Mapeamento de dados (data mapping) com base legal (consentimento, execução de contrato, legítimo interesse) documentada por finalidade.
- 🔴 Vermelho: "Vamos coletar tudo que for útil, depois filtramos".

**Pergunta 15: Como o usuário exerce direito de acesso, correção e exclusão dos seus dados, na prática?**

- O que está sendo testado: se os direitos do titular são um processo real ou uma cláusula de política de privacidade sem implementação.
- 🟢 Verde: Fluxo técnico e operacional definido, com prazo de resposta e responsável designado.
- 🔴 Vermelho: "Isso a gente resolve manualmente se alguém pedir".

**Pergunta 16: Em caso de vazamento de dados, qual é o plano de resposta e quem é notificado em quanto tempo?**

- O que está sendo testado: preparação para incidentes, exigida legalmente.
- 🟢 Verde: Plano de resposta a incidentes documentado, com DPO ou responsável designado.
- 🔴 Vermelho: Nenhum plano existe; "isso nunca vai acontecer com a gente".

---

### 2.6 Equipe e Capacidade Técnica

**Pergunta 17: A equipe atual já entregou algo de complexidade comparável antes?**

- O que está sendo testado: excesso de confiança em capacidade não comprovada.
- 🟢 Verde: Histórico de entregas similares documentado, com lições aprendidas aplicadas.
- 🔴 Vermelho: "É a primeira vez, mas o time é bom" sem plano de mitigação de risco.

**Pergunta 18: O que acontece com o projeto se a pessoa-chave sair amanhã?**

- O que está sendo testado: dependência crítica de indivíduos e qualidade da documentação.
- 🟢 Verde: Conhecimento distribuído, documentação atualizada, pair programming ou revisão cruzada praticados.
- 🔴 Vermelho: Um único desenvolvedor detém todo o conhecimento crítico sem registro escrito.

**Pergunta 19: A capacidade real da equipe (horas disponíveis, não headcount nominal) foi confrontada com o escopo estimado?**

- O que está sendo testado: superestimação de disponibilidade real considerando outros projetos, férias e manutenção.
- 🟢 Verde: Capacidade calculada com base em velocidade histórica real da equipe (velocity, throughput).
- 🔴 Vermelho: Estimativa baseada em "8 horas úteis por dia por pessoa" sem descontar reuniões, suporte e imprevistos.

---

### 2.7 Cronograma, Custos e ROI

**Pergunta 20: Esta estimativa de prazo foi baseada em dados históricos ou em otimismo?**

- O que está sendo testado: viés de otimismo em estimativas — o erro mais comum e mais caro em projetos de software.
- 🟢 Verde: Estimativa com margem de contingência baseada em projetos anteriores comparáveis.
- 🔴 Vermelho: Prazo definido de cima para baixo por pressão comercial, sem lastro técnico.

**Pergunta 21: Qual é o custo total (desenvolvimento + infraestrutura + manutenção + suporte) nos primeiros 24 meses, não apenas o custo de construção?**

- O que está sendo testado: subestimação do custo de manutenção pós-lançamento, frequentemente maior que o custo inicial.
- 🟢 Verde: TCO (Total Cost of Ownership) projetado incluindo operação contínua.
- 🔴 Vermelho: Orçamento cobre apenas até o "go-live".

**Pergunta 22: Qual é o ROI esperado, com premissas explícitas e testáveis?**

- O que está sendo testado: se o retorno é uma projeção fundamentada ou uma esperança disfarçada de número.
- 🟢 Verde: Modelo financeiro com premissas declaradas e sensibilidade a cenários pessimistas.
- 🔴 Vermelho: "Vai se pagar sozinho" sem projeção numérica.

---

### 2.8 Riscos Legais, Regulatórios e de Segurança

**Pergunta 23: Existe alguma regulamentação setorial específica (financeira, saúde, educação, etc.) que este projeto precisa cumprir?**

- O que está sendo testado: cegueira regulatória setorial além da LGPD genérica.
- 🟢 Verde: Requisitos regulatórios mapeados com validação jurídica específica do setor.
- 🔴 Vermelho: Nenhuma consulta jurídica foi feita antes do início do desenvolvimento.

**Pergunta 24: Foi feita alguma avaliação de segurança (pentest, análise de vulnerabilidades) antes do lançamento?**

- O que está sendo testado: segurança tratada como requisito, não como reação pós-incidente.
- 🟢 Verde: Pentest ou análise de vulnerabilidades planejada antes do go-live, com orçamento reservado.
- 🔴 Vermelho: "Vamos ver isso depois que estiver no ar".

**Pergunta 25: Quem é o responsável legal em caso de falha do sistema causar dano a terceiros?**

- O que está sendo testado: clareza contratual sobre responsabilidade civil.
- 🟢 Verde: Termos de uso e contratos revisados juridicamente, com cláusulas de responsabilidade claras.
- 🔴 Vermelho: Nenhum documento jurídico revisado antes do lançamento.

---

### 2.9 Manutenção, Escalabilidade e Evolução Futura

**Pergunta 26: Quem mantém este sistema daqui a 2 anos, quando o entusiasmo inicial já tiver passado?**

- O que está sendo testado: sustentabilidade de longo prazo além do momento de lançamento.
- 🟢 Verde: Responsável de manutenção definido com orçamento recorrente aprovado.
- 🔴 Vermelho: Nenhum plano além do lançamento; "a gente resolve isso depois".

**Pergunta 27: Existe um processo definido para atualização de dependências e correção de vulnerabilidades conhecidas?**

- O que está sendo testado: dívida técnica planejada vs. acumulada silenciosamente.
- 🟢 Verde: Processo de atualização periódica documentado e automatizado (ex: dependabot, revisões trimestrais).
- 🔴 Vermelho: Dependências nunca são atualizadas após o lançamento.

**Pergunta 28: A arquitetura permite adicionar a próxima funcionalidade óbvia sem reescrever o núcleo do sistema?**

- O que está sendo testado: rigidez arquitetural que trava evolução futura.
- 🟢 Verde: Arquitetura modular validada com um exercício de "e se precisássemos adicionar X".
- 🔴 Vermelho: Qualquer mudança pequena exige reescrita significativa.

---

### 2.10 Critérios de Sucesso e Métricas (OKRs/KPIs)

**Pergunta 29: Qual métrica específica, com número e prazo, define que este projeto foi um sucesso?**

- O que está sendo testado: ausência de critério objetivo de sucesso, que impede decisões futuras de continuar ou descontinuar.
- 🟢 Verde: KPI definido com baseline, meta e prazo (ex: "reduzir tempo de atendimento em 30% em 6 meses").
- 🔴 Vermelho: "Vamos saber que deu certo quando virmos" — sem métrica.

**Pergunta 30: Qual métrica, se piorar, dispara automaticamente uma revisão ou cancelamento do projeto?**

- O que está sendo testado: existência de critério de saída (kill switch), não apenas de entrada.
- 🟢 Verde: Threshold de risco definido antecipadamente (ex: "se CAC > LTV após 6 meses, revisar o modelo").
- 🔴 Vermelho: Nenhum critério de descontinuação existe — o projeto continua por inércia.

---

## 3. Comportamento Esperado da Empresa Durante a Análise

Ao conduzir esta análise, a empresa deve adotar as seguintes posturas:

- **Escuta ativa, mas cética**: ouvir completamente a justificativa antes de julgar, mas nunca aceitar uma resposta apenas porque foi dita com confiança.
- **Evidência acima de opinião**: toda resposta "verde" deve vir acompanhada de dado, teste, documento ou registro verificável — não de convicção pessoal.
- **Multidisciplinaridade obrigatória**: nenhuma decisão de aprovação deve ser tomada apenas pela área técnica ou apenas pelo negócio. Jurídico, financeiro, TI e negócio devem assinar formalmente.
- **Disposição real para matar o projeto**: se os sinais forem majoritariamente vermelhos, a decisão correta é interromper, redesenhar ou adiar — não seguir em frente "porque já foi investido tempo nisso" (falácia do custo afundado).
- **Decisão estruturada, não por sentimento**: aprovação ou reprovação deve seguir um scorecard ou matriz de risco formal, documentado e revisitável — não uma reunião informal de "vamos seguir em frente".

---

## 4. Checklist Final Antes da Aprovação

Nenhum projeto deve avançar para desenvolvimento completo sem que os itens abaixo estejam marcados:

- [ ] Problema validado com pesquisa qualitativa e quantitativa junto a usuários reais
- [ ] Prova de Conceito (POC) técnica executada para os riscos de maior incerteza
- [ ] Protótipo navegável testado com usuários reais fora da empresa
- [ ] Análise de concorrentes diretos e indiretos documentada
- [ ] Modelo de receita e projeção de ROI com premissas explícitas
- [ ] Mapeamento de dados pessoais e base legal (LGPD/GDPR) definidos
- [ ] Avaliação jurídica de riscos regulatórios do setor concluída
- [ ] Plano de segurança (pentest ou análise de vulnerabilidades) agendado
- [ ] TCO calculado para 24 meses, incluindo manutenção e suporte
- [ ] Capacidade real da equipe confrontada com escopo e prazo
- [ ] KPIs de sucesso e critérios de descontinuação definidos e aprovados
- [ ] Plano de resposta a incidentes de dados documentado
- [ ] Aprovação formal de negócio, TI, jurídico e financeiro registrada

**Aviso:** ⚠️ qualquer item não marcado representa um risco assumido conscientemente — deve ser registrado como tal, não ignorado silenciosamente.

---

## 5. Modelo de Matriz de Decisão

Cada pergunta das 10 categorias deve ser pontuada de 1 a 5, conforme a escala abaixo:

|Pontuação|Significado|
|---|---|
|1|Resposta ausente ou puramente especulativa|
|2|Resposta baseada em suposição, sem evidência|
|3|Resposta parcialmente validada, com lacunas relevantes|
|4|Resposta bem fundamentada, com evidência sólida|
|5|Resposta totalmente validada, com dados e testes reais|

### Estrutura de pontuação por categoria

|Categoria|Nº de perguntas|Pontuação máxima|Pontuação obtida|
|---|---|---|---|
|Negócio e Modelo de Receita|4|20||
|Mercado e Concorrência|3|15||
|Usuários e UX/UI|3|15||
|Tecnologia e Arquitetura|3|15||
|Dados e Privacidade (LGPD/GDPR)|3|15||
|Equipe e Capacidade Técnica|3|15||
|Cronograma, Custos e ROI|3|15||
|Riscos Legais e Segurança|3|15||
|Manutenção e Escalabilidade|3|15||
|Critérios de Sucesso (OKRs/KPIs)|2|10||
|**Total**|**30**|**150**||

### Critério de aprovação

|Faixa de pontuação (de 150)|Decisão|
|---|---|
|Abaixo de 75 (< 50%)|**Reprovado.** Projeto não deve avançar. Riscos estruturais não endereçados.|
|75 a 104 (50%–69%)|**Reprovado com ressalvas.** Necessário revisar e reapresentar após mitigação dos pontos vermelhos críticos.|
|105 a 129 (70%–86%)|**Aprovado condicionalmente.** Pode avançar para POC/protótipo, com plano de ação para pontos amarelos.|
|130 a 150 (87%–100%)|**Aprovado.** Projeto validado o suficiente para seguir para desenvolvimento completo.|

**Regra de veto:** independentemente da pontuação total, qualquer pergunta das categorias "Dados e Privacidade" ou "Riscos Legais, Regulatórios e de Segurança" pontuada como 1 ou 2 bloqueia a aprovação automaticamente até ser corrigida — não pode ser compensada por pontuação alta em outras áreas.

**Aviso:** ⚠️ esta matriz não substitui julgamento humano — ela existe para impedir que julgamento humano seja substituído por entusiasmo.