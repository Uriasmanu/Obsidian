# SDD (Specification Driven Development)

SDD e uma abordagem de desenvolvimento onde a especificacao (documentacao de requisitos) guia todo o processo de construcao de software. Em vez de comecar codando, voce primeiro define O QUE o sistema deve fazer, depois COMO fara.

---

## Por que usar SDD?

- **Comunicacao clara**: Todos entendem o que precisa ser construido
- **Reducao de retrabalho**: Menos mudancas durante o desenvolvimento
- **Documentacao**: Historico dasdecisoes e razoes
- **Testabilidade**: Requisitos claros = testes claros
- **Onboarding**: Novos membros entendem rapido o projeto

---

## Tópicos de Revisao

### 1. Fundamentos de Requisitos

#### O que e um requisito?
Uma condicao ou capacidade que o sistema deve satisfazer.

#### Tipos de Requisitos

| Tipo | Descricao | Exemplo |
|------|-----------|---------|
| **Funcional** | O que o sistema faz | "O sistema deve permitir login com email" |
| **Nao Funcional** | Como o sistema executa | "O sistema deve responder em menos de 2s" |
| **De Domínio** | Regras de negocio | "Desconto so aplica para pedidos acima de R$100" |
| **De Interface** | Como o usuario interage | "Botao verde para confirmacao" |

#### Niveis de Requisitos

1. **Nivel de Negocio**: Necessidades do usuario final
2. **Nivel de Usuario**: Tarefas que o usuario realiza
3. **Nivel de Produto**: Especificacoes tecnicas do sistema

---

### 2. Técnicas de Levantamento de Requisitos

#### Metodos de Coleta

- **Entrevistas**: Conversas diretas com stakeholders
- **Questionarios**: Pesquisa ampla com usuarios
- **Observacao**: Ver como usuarios trabalham
- **Workshops**: Sessoes colaborativas
- **Analise de Documentos**: Estudar processos existentes
- **Prototipacao**: Criar modelos visuais

#### Personas
Representacao ficticia do usuario alvo.

```
Nome: Maria, 35 anos
Profissao: Professora
Dor: Perda de tempo marcando aulas
Objetivo: Agendar tudo pelo celular em 2 cliques
```

#### Historias de Usuario
Formato: "Como [persona], eu quero [acao] para [beneficio]"

```
Como professor de jiu-jitsu,
eu quero marcar presenca dos alunos pelo celular,
para não perder tempo com papelada.
```

#### Critérios INVEST (bom requisito)

- **I**ndependent (independente)
- **N**egotiable (negociavel)
- **V**aluable (valioso)
- **E**stimable (estimavel)
- **S**mall (pequeno)
- **T**estable (testavel)

---

### 3. Estrutura de Documentos de Requisito

#### User Story vs Caso de Uso

**User Story**: Resumo rapido, focado no valor
**Caso de Uso**: Detalhado, com fluxo completo

#### Template de Caso de Uso

```
1. Nome: [Nome descritivo]

2. Ator: [Quem executa]

3. Pre-condicoes: [O que precisa estar pronto]

4. Fluxo Principal:
   a. [Passo 1]
   b. [Passo 2]

5. Fluxo Alternativo:
   a. [O que fazer se algo der errado]

6. Pos-condicoes: [O que acontece depois]

7. Regras de Negocio: [Restricoes aplicaveis]
```

---

### 4. Escrita de Requisitos

#### Regras de Boa Escrita

1. **Use linguagem simples** - Evite termos tecnicos desnecessarios
2. **Seja Specifico** - "O sistema deve..." em vez de "O sistema deveria..."
3. **Uma frase = uma ideia** - Nao misture varios conceitos
4. **Evite negativos duplos** - "O sistema nao deve rejeitar usuarios validos"
5. **Use verbos activos** - "O usuario deve inserir", nao "A insercao deve ser feita"

#### Erros Comuns

- Requisitos vagos: "O sistema deve ser rapido"
- Requisitos incompletos: Falta de cenario alternativo
- Requisitos contraditorios: "Deve aceitar letras E numeros"
- Requisitos impossiveis: "Deve funcionar offline E sincronizar em tempo real"

---

### 5. Levantamento de Requisitos para Software

#### Perguntas Essenciais

**Sobre o usuario:**
- Quem vai usar?
- Com que frequencia?
- Quais problemas actuales?

**Sobre o sistema:**
- Quais funcoes sao obrigatorias?
- Quais sao opcionais?
- Quais integracoes necessarias?

**Sobre qualidade:**
- Qual performance minima?
- Quais seguranca necessaria?
- Quais plataformas suportar?

---

### 6. Priorização de Requisitos

#### Metodo MoSCoW

- **M**ust have (obrigatorio) - Sem isso nao entrega
- **S**hould have (importante) - Enhance a experiencia
- **C**ould have (desejavel) - Se tempo permitir
- **W**on't have (nao agora) - Para versao futura

#### Metodo Kano

- **Basicos**: Esperados,的不满 se faltarem
- **Performance**: Mais e melhor
- **Excitantes**: Surpreendem e encantam

---

### 7. Documentação Técnica

#### Estrutura de Especificação Técnica

```
## 1. Visao Geral
   - Problema que resolve
   - Escopo do projeto

## 2. Requisitos Funcionais
   - [lista de RFs]

## 3. Requisitos Nao Funcionais
   - Performance
   - Seguranca
   - Escalabilidade

## 4. Regras de Negocio
   - [lista de regras]

## 5. Interfaces
   - APIs
   - Telas principais

## 6. Fluxos
   - Fluxo principal
   - Fluxos alternativos

## 7. Modelagem
   - Diagramas (se necessario)

## 8. Glossario
   - Termos tecnicos
```

---

### 8. Validação e Verificação

#### Review de Requisitos

- **Revisao formal**: Equipe completa revisando
- **Prototipacao**: Mostrar para usuario
- **Testes**: Validar que requisitos sao testaveis

#### Checklist de Revisao

- [ ] Cada requisito tem um ID unico?
- [ ] Esta claro quem e o ator?
- [ ] Os criterios de aceite estao definidos?
- [ ] Nao ha ambiguidade?
- [ ] Esta alinhado com o objetivo do projeto?
- [ ] E testavel?

---

## 4 Pilares do SDD (Alex Rezvov, 2026)

1. **Traceability** - Codigo e testes devem ser rastreaveis aos requisitos. Use anotacoes, commit messages estruturados, e referencias claras.

2. **DRY (Don't Repeat Yourself)** - Cada fato descrito uma vez. Valores de configuracao, definicoes de tipo, constantes, contratos de API: cada um tem fonte unica.

3. **Deterministic Enforcement** - Validacao automatizada. Se uma maquina pode verificar, uma maquina deve verificar. Linting, testes, validacao de schema, CI checks.

4. **Parsimony** - Codigo, documentacao e prompts sao concisos. Nenhum comentario redundante. Cada linha merece sua existencia.

---

## Niveis de Rigor SDD

| Nivel | Descricao | Quando Usar |
|-------|-----------|-------------|
| **spec-first** | Especificacao escrita primeiro para gerar codigo inicial. Depois abandanda. | Projetos simples, features pequenas |
| **spec-anchored** | Especificacao mantida junto ao codigo. Fonte de verdade para intent e contratos. | Sistemas em producao (sweet spot) |
| **spec-as-source** | Apenas especificacao editada por humanos. Codigo 100% gerado. | Altamente arriscado - requer ferramentas maduras |

**Regra de Ouro:** Use o minimo nivel de rigor que remove ambiguidade. spec-first para assistentes IA; spec-anchored para sistemas de longa duracao; spec-as-source apenas com ferramentas confiaveis.

---

## GitHub Spec Kit (Comandos)

Ferramentas que automatizam o fluxo especificar -> planejar -> taskar:

| Comando | Descricao |
|--------|-----------|
| `/specify` | Define "o que" e "por que" do projeto. Gera PRD. Exclui decisoes tecnicas. |
| `/plan` | Define "como" - frameworks, bibliotecas, infraestrutura. Gera plano + metadata. |
| `/task` | Quebra em tarefas implementaveis. Cada task linkada a requisitos especificos. |

### constitution.md
Documento que estabelece principios nao negociaveis do projeto. Ex: padroes de teste, convencoes de stack, requirements de seguranca.

---

## SDD com Agentes IA

**Fluxo de 4 fases:**
1. Requisitos -> Especificacao detalhada
2. Design -> Estrategia de implementacao
3. Tasks -> Tarefas discretas
4. Implementacao -> Codigo com contexto completo

**Vantagem medida:**
- 55% mais rapido completion vs ad-hoc prompting
- 60-80% menos regressoes geradas por IA
- 40% menos mid-sprint pivots

**Problemas comuns a evitar:**
- Over-specification - especificacoes detalhadas demais que viram pesadelo de manutencao
- Spec drift - especificacao diverge do codigo sem validacao
- Spec review como gargalo - forcar spec em tudo (bureaucracia desnecessaria)
- Granularidade - features muito pequenas nao precisam do fluxo completo

---

## Boas Praticas SDD

### Prática 1: Escrever Histórias de Usuario
Pegue tarefas do dia a dia e escreva como historias de usuario.

```
Exercicio: Sistema de controle de presenca
- Escreva 5 historias de usuario
- Identifique: ator, acao, beneficio
```

### Prática 2: Transformar Requiremento em Teste
Para cada requisito, pense: "Como eu testaria isso?"

```
Requisito: "O sistema deve bloquear login apos 3 tentativas falhas"
Teste: Tentativas de login 1, 2, 3, 4 -> verificar bloqueio
```

### Prática 3: Criar Casos de Uso
Pegue uma funcao simples e detalhe o caso de uso completo.

```
Exercicio: Fazer check-in na academia
- Fluxo principal
- Fluxo alternativo (nao tem credito, problema de sistema)
- Pos-condicoes
```

### Prática 4: Revisar Requisitos de Outros
Busque requisitos mal escritos e melhore.

| Original | Melhorado |
|----------|------------|
| "Sistema rapido" | "Tempo de resposta < 2 segundos" |
| "Interface boa" | "Botoes com minimo 44x44px para touch" |

### Prática 5: Priorizar com MoSCoW
Dada uma lista de requisitos, categorize cada um.

---

## Estudos Recomendados

### Livros
- "Writing Effective Use Cases" - Alistair Cockburn
- "Software Requirements" - Karl Wiegers
- "User Stories Applied" - Mike Cohn

### Conceitos Relacionados
- **BDD (Behavior Driven Development)**: Especificar comportamento
- **DDD (Domain Driven Design)**: Design orientado ao dominio
- **Agile/Scrum**: Onde SDD se encaixa em metodologias ageis
- **UML**: Notacao para diagramas de requisitos

### Links para Aprender
- IREB (International Requirements Engineering Board)
- BABOK (Business Analysis Body of Knowledge)

---

## Como Aplicar no Trabalho

1. **Antes de codar**: Escreva o requisito primeiro
2. **Pergunte sempre**: "O que o sistema deve fazer?"
3. **Documente**: Mantenha registro das decisoes
4. **Valide**: Mostre para o usuario/stakeholder
5. **Revise**: Periodicamente atualize os requisitos

---

## Ferramentas Úteis

- **Notion**: Documentacao de requisitos
- **Jira/Trello**: Gerenciamento de historias
- **Figma**: Prototipacao
- **Draw.io**: Diagramas de fluxo

---

## Pendente de Preenchimento

- [ ] Exemplos reais de requisitos escritos por mim
- [ ] Casos de uso detalhados do app de academia
- [ ] Regras de negocio do app de academia