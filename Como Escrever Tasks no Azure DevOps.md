# Como Escrever Tasks no Azure DevOps

Guia de boas práticas para escrever tasks, issues, user stories e bugs no Azure DevOps.

---

## 1. Elementos Básicos (Para qualquer tipo de item)

- **Título Claro e Descritivo:** Deve resumir o problema ou a entrega de forma objetiva.
    
    - _Exemplo ruim:_ "Erro no sistema" ou "Atualizar Azure".
        
    - _Exemplo bom:_ "Corrigir erro de build do Yarn no pipeline de produção do Azure DevOps" ou "Documentar processo de deploy da plataforma 4WEB".
        
- **Descrição / Contexto:** Um breve resumo explicando a origem da demanda, o contexto técnico ou o valor que ela entrega.
    
- **Prioridade e Severidade:** Define a urgência para o negócio (Prioridade) e o impacto técnico (Severidade, muito usado para bugs).
    
- **Responsável e Estimativa:** Quem vai fazer e quanto tempo (ou pontos) isso deve custar.
    

## 2. O que uma _Task_ (Tarefa técnica) precisa ter

As tasks geralmente representam um passo técnico a ser executado para atingir um objetivo maior.

- **Escopo Definido:** O limite exato do que será feito (o que está dentro e o que está fora da tarefa).
    
- **Instruções Técnicas ou Links Úteis:** Caminhos de arquivos, documentações de referência, ferramentas envolvidas ou comandos necessários.
    

## 3. O que uma _Issue_ ou _User Story_ precisa ter

Quando o item representa uma funcionalidade ou uma demanda maior, ele costuma seguir o formato ágil:

- **Critérios de Aceitação (_Acceptance Criteria_):** Regras de negócio ou condições objetivas que precisam ser atendidas para que o item seja considerado pronto. Geralmente escritas em formato de cenários (_Dado que..., Quando..., Então..._).
    
- **Definição de Pronto (_Definition of Done_ - DoD):** Critérios que se aplicam a todas as entregas da equipe (ex: código revisado por outro dev, testes executados, documentação atualizada).
    

## 4. O que um _Bug_ precisa ter (O mais crítico)

Para que um desenvolvedor consiga corrigir um erro rapidamente, o bug precisa eliminar o famoso "na minha máquina funciona":

- **Passos para Reproduzir (_Steps to Reproduce_):** O passo a passo exato do que o usuário fez antes de o erro acontecer.
    
- **Comportamento Atual:** O que de fato aconteceu (qual foi o erro ou tela travada).
    
- **Comportamento Esperado:** O que deveria ter acontecido segundo a regra do sistema.
    
- **Evidências:** Capturas de tela (_prints_), vídeos curtos, logs de erro, códigos de erro ou o rastreamento da pilha (_stack trace_).
    
- **Ambiente:** Onde o erro ocorreu (Produção, Homologação, navegador específico, sistema operacional, etc.).

---

## Links

- [[Trabalho/Trabalho Conhecimento e atividades do dia a dia|Atividades do Trabalho]]
- [[Trabalho/Abertura de Bugs|Abertura de Bugs]]
- [[Trabalho/Solução Tecnica|Soluções Técnicas]]
- [[Manu/Indice|Voltar ao Indice]]
