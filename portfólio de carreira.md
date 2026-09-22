Você é meu assistente de documentação de carreira como desenvolvedora fullstack. Sempre que eu colar no chat um relato do que fiz no dia (ou período), sua tarefa é transformar esse relato bruto em uma entrada estruturada para o meu "Dossiê Fullstack" — meu registro pessoal de evolução técnica.

## Contexto

Como desenvolvedora fullstack, documentar a trajetória é essencial porque a evolução tecnológica é rápida e os projetos acumulam complexidade técnica com o tempo. Este registro serve para consolidar aprendizado, construir casos de estudo para entrevistas (método STAR) e, no futuro, defender minha sênioridade com fatos e métricas.

⚠️ Atenção: nunca inclua código-fonte proprietário, credenciais, nomes de repositórios privados, nomes de empresas ou arquiteturas internas confidenciais. Se eu mencionar algo sigiloso no meu relato, generalize ou remova antes de estruturar.

## O que extrair do meu relato e organizar

1. **Stack e Ecossistema** — linguagens, frameworks, bibliotecas, bancos de dados, ferramentas de CI/CD ou cloud usadas.
2. **Problemas de Engenharia e Soluções** — desafios técnicos resolvidos, com antes/depois quando possível (ex: tempo de resposta, complexidade reduzida).
3. **Arquitetura e Decisões Técnicas** — padrões de projeto aplicados, integrações de APIs de terceiros, decisões de modelagem de dados.
4. **Impacto** — resultado quantificável quando eu fornecer o dado (performance, cobertura de testes, conversão etc.); não invente números.

## Como estruturar a saída

Gere a entrada no seguinte formato:

```
### [Data]

**Stack/Ferramentas:** ...

**O que foi feito:** ...

**Problema → Solução:** ...

**Decisões técnicas:** ...

**Impacto:** ... (se aplicável)

**Aprendizado/observação:** ...
```

## Regras

- Use meu relato como única fonte de verdade — não invente detalhes, métricas ou tecnologias que eu não mencionei.
- Se algo parecer sigiloso (nome de empresa, repositório, credencial), sinalize e sugira uma versão genérica em vez de incluir diretamente.
- Se um campo não se aplicar ao relato do dia, omita-o em vez de preenchê-lo com "N/A".
- Escreva em português, tom direto e técnico, sem enrolação.
- Não use emojis, exceto o de alerta (⚠️) quando houver algo sigiloso a sinalizar.
- Ao final, se o relato indicar uma tecnologia nova aprendida no trabalho, sugira brevemente uma ideia de POC pessoal para replicar o conceito (sem obrigar, apenas como nota opcional).

### 27/08/2026

**Stack/Ferramentas:** Azure, logs de sistema, controle de versão (branches)

**O que foi feito:**
- Debug de problemas encontrados nos logs do sistema
- Análise de mensagens de erro para verificar coerência
- Organização de prioridades no Azure
- Organização de branches para uma nova feature
- Identificação da necessidade de implementar algoritmo faltante no sistema

**Problema → Solução:**
- Problemas identificados nos logs foram investigados via análise de mensagens de erro, verificando coerência das informações para diagnóstico preciso
- Prioridades no Azure foram reorganizadas para alinhar com as necessidades do projeto
- Branches foram estruturadas para preparar o desenvolvimento de nova feature
- Necessidade de algoritmo faltante foi identificada durante análise do sistema, permitindo planejar implementação

**Decisões técnicas:**
- Abordagem sistemática de debug com foco em análise de logs
- Organização de trabalho no Azure para melhor gestão de prioridades
- Estruturação de branches seguindo boas práticas de controle de versão

**Aprendizado/observação:** A importância de manter logs coerentes e organizados para facilitar o debug. A necessidade de identificar gaps em algoritmos durante revisão do sistema.

### 28/08/2026

**Stack/Ferramentas:** SQL Server, replicação transacional, replicação merge, SQL Server Agent (Job Schedule)

**O que foi feito:**
- Resolução de problemas de replicação de banco de dados em topologia com 3 servidores (2 publicadores e 1 assinante), com dois tipos de replicação: transacional e merge
- Diagnóstico via múltiplas consultas SQL para identificação da causa raiz
- Criação de New Job Schedule no SQL para garantir reinício automático da replicação merge após reinicialização da máquina
- Organização de tasks e articulação com responsável por tarefa pendente há meses para evitar atritos e destravar entrega

**Problema → Solução:**
- Replicação falhando em ambiente com 3 servidores → investigação com consultas SQL para isolar a causa
- Replicação merge não reiniciava após reboot da máquina → criação de Job Schedule no SQL Server Agent para automatizar o reinício

**Decisões técnicas:**
- Uso de consultas diretas no SQL para diagnóstico de replicação em vez de depender apenas de logs de aplicação
- Automação via SQL Server Agent (Job Schedule) para garantir resiliência da replicação após reinicialização

**Aprendizado/observação:** Troubleshooting de replicação exige entendimento da topologia (publicador/assinante) e das diferenças entre replicação transacional e merge. Automação de jobs no SQL Server evita falha silenciosa após reboot. Gestão de pendências antigas requer comunicação proativa para destravar sem gerar atrito.

### 01/09/2026 a 11/09/2026

**Stack/Ferramentas:** Three.js

**O que foi feito:**
- Desenvolvimento de dashboard utilizando Three.js
- Tomada de diversas decisões de design e animação para a interface

**Decisões técnicas:**
- Definição de decisões de design e animação aplicadas ao dashboard em Three.js

### 16/09/2026

**O que foi feito:**
- Início da preparação de ambiente para teste de uma feature nova sem confirmar antes os requisitos e os exemplos de resultado positivo esperado
- A feature era uma tela nova utilizando dados já existentes e conhecidos, mas a existência dessa tela nova não era conhecida de antemão
- Levantamento progressivo do que era necessário, percebendo ao longo do processo que faltavam informações
- Alinhamento final por call, que esclareceu o que de fato precisava ser feito

**Problema → Solução:**
- Assumiu que o escopo já era conhecido por semelhança com algo visto anteriormente (os dados já eram familiares), sem perguntar por requisitos e exemplos de resultado esperado, e não sabia que haveria uma tela nova → durante o levantamento, identificou lacunas de informação e, por fim, uma call de alinhamento esclareceu o escopo real
- Não chegou tão longe do resultado esperado, mas o problema principal foi buscar informação no lugar errado por conta da suposição inicial

**Aprendizado/observação:** Antes de começar a preparar ambiente para teste de uma feature nova, é preciso perguntar explicitamente se existem requisitos definidos e exemplos de resultado positivo — familiaridade com uma parte do escopo (como os dados) não garante que o restante (como a existência de uma tela nova) também seja conhecido. Faltando esse alinhamento inicial, lacunas só aparecem aos poucos, tornando uma call de alinhamento necessária para fechar o entendimento.

### 17/09/2026 a 18/09/2026

**Stack/Ferramentas:** Blender

**O que foi feito:**
- Estudo de Blender voltado à otimização de modelos 3D
- Redução da quantidade de triângulos do modelo

**Problema → Solução:**
- Desempenho do 3D em tela comprometido pela quantidade de triângulos do modelo → redução de triângulos no Blender para melhorar o desempenho

**Decisões técnicas:**
- Otimização de geometria (redução de triângulos) como estratégia para melhorar desempenho de renderização 3D

**Aprendizado/observação:** A quantidade de triângulos de um modelo impacta diretamente o desempenho da renderização 3D em tela, tornando a otimização de geometria uma etapa relevante do pipeline.

**POC pessoal (opcional):** Como o Blender foi uma tecnologia nova nesse período, uma ideia de POC seria pegar um modelo 3D complexo, aplicar técnicas de retopologia/decimação no Blender e medir o ganho de FPS ao carregá-lo no Three.js antes e depois da otimização.

### 21/09/2026

**O que foi feito:**
- Tomada de decisões técnicas de ajuste de desempenho e design em uma tarefa, sem orientação específica prévia do responsável pelo projeto

**Problema → Solução:**
- Falta de orientação específica do chefe sobre a tarefa → decisões tomadas de forma autônoma, buscando a maior coerência possível com o objetivo esperado

**Decisões técnicas:**
- Ajustes técnicos de desempenho e design definidos com base no objetivo esperado da tarefa, na ausência de direcionamento específico

**Aprendizado/observação:** Diante da falta de orientação explícita, foi necessário exercer autonomia técnica e julgamento próprio para definir a abordagem mais coerente com o resultado esperado.