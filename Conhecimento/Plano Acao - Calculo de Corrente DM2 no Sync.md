# Plano de Ação - Implementação do Algoritmo de Cálculo de Corrente do DM2 no Sync

**Status:** Em Planejamento  
**Responsável:** Manoela Urias  
**Data de Criação:** 03/08/2026  
**Prioridade:** Alta  
**Módulo:** DM2 / Sync  
**PR de Referência:** `DM2-sync-import`  
**PR de Implementação (referência):** Pull Request 19057: [#61711]: Regra - Campos 16M e 16U

---

## 1. Compreensão da Especificação do Algoritmo DM2

### 1.1. Estudar a documentação oficial do algoritmo
- [ ] Obter documentação técnica do DM2 (versão, referências, fórmulas matemáticas)
- [ ] Identificar a versão atual do algoritmo utilizada no E3
- [ ] Mapear todas as fórmulas de cálculo de corrente envolvidas

### 1.2. Identificar variáveis de entrada
- [ ] Tensão (valor lido na entrada analógica)
- [ ] Resistência do transformador
- [ ] Temperatura ambiente
- [ ] Fator de correção
- [ ] Parâmetros de configuração do DM2 (ajuste fino, limites)
- [ ] Demais variáveis identificadas na documentação

### 1.3. Mapear saídas esperadas
- [ ] Corrente calculada (resultado final)
- [ ] Margens de erro aceitáveis
- [ ] Limites operacionais (mínimo/máximo)
- [ ] Valores proporcionais de corrente

### 1.4. Levantar premissas e restrições
- [ ] Faixa de operação válida do algoritmo
- [ ] Linearidade dos cálculos
- [ ] Frequência de atualização dos dados
- [ ] Condições de contorno (overflow, underflow, divisão por zero)

### 1.5. Comparar com versões anteriores
- [ ] Analisar diferenças entre E3 e Sync
- [ ] Identificar melhorias implementadas na versão atual
- [ ] Documentar pontos de atenção para migração

---

## 2. Análise da Estrutura Atual do Sistema Sync

### 2.1. Mapear arquitetura do Sync
- [ ] Identificar módulos e camadas do sistema
- [ ] Mapear fluxo de dados de entrada e saída
- [ ] Documentar dependências entre módulos

### 2.2. Identificar ponto de inserção do cálculo
- [ ] Avaliar se será novo serviço ou integração com módulo existente
- [ ] Definir se será processamento em tempo real ou batch
- [ ] Identificar API ou endpoint de exposição

### 2.3. Levantar dependências técnicas
- [ ] Linguagem de programação utilizada no Sync
- [ ] Frameworks e bibliotecas disponíveis
- [ ] Banco de dados e modelo de dados
- [ ] Sistema de filas/mensageria (se aplicável)

### 2.4. Verificar disponibilidade dos dados de entrada
- [ ] Confirmar quais dados já estão disponíveis no Sync
- [ ] Identificar dados que precisam ser obtidos de outras fontes
- [ ] Validar qualidade e consistência dos dados

### 2.5. Identificar integrações com outros sistemas
- [ ] SCADA (fonte de dados de campo)
- [ ] IoT / sensores
- [ ] Banco de dados históricos
- [ ] APIs externas

---

## 3. Projeto da Solução

### 3.1. Definir abordagem de implementação
- [ ] Avaliar: função pura vs microserviço vs script agendado vs pipeline
- [ ] Documentar justificativa da escolha
- [ ] Alinhar com time de arquitetura

### 3.2. Desenhar fluxo de processamento
```
Entrada → Validação → Cálculo → Saída → Logs
```
- [ ] Detalhar cada etapa do fluxo
- [ ] Definir regras de validação de entrada
- [ ] Especificar estrutura de dados de saída
- [ ] Planejar logging estruturado

### 3.3. Especificar tratamento de erros
- [ ] Dados inconsistentes ou fora de faixa
- [ ] Timeout de comunicação
- [ ] Falhas de integração com sistemas externos
- [ ] Exceções matemáticas (divisão por zero, overflow)

### 3.4. Definir critérios de desempenho
- [ ] Tempo de resposta máximo aceitável
- [ ] Uso máximo de CPU/memória
- [ ] Requisitos de escalabilidade
- [ ] Throughput mínimo esperado

### 3.5. Planejar versionamento e rollout
- [ ] Estratégia de feature flag
- [ ] Deploy gradual (canary, blue-green)
- [ ] Plano de rollback
- [ ] Comunicação com stakeholders

---

## 4. Desenvolvimento e Codificação

### 4.1. Configurar ambiente de desenvolvimento
- [ ] Setup local com dados simulados
- [ ] Ferramentas de debug e profiling
- [ ] Ambiente de homologação acessível

### 4.2. Implementar o algoritmo
- [ ] Seguir boas práticas (Clean Code, SOLID)
- [ ] Implementar funções puras para cálculo
- [ ] Criar interfaces/tipos para entrada e saída
- [ ] Implementar validação de dados

### 4.3. Criar wrappers de integração
- [ ] Conector com banco de dados
- [ ] Consumo de APIs internas
- [ ] Handler de mensagens (se aplicável)

### 4.4. Adicionar logging e métricas
- [ ] Logging estruturado (JSON)
- [ ] Métricas de performance (latência, throughput)
- [ ] Contadores de erro
- [ ] Traces para monitoramento

### 4.5. Code Review
- [ ] Revisão de lógica de negócio
- [ ] Revisão de performance
- [ ] Revisão de segurança
- [ ] Revisão de legibilidade e manutenibilidade

---

## 5. Testes e Validação

### 5.1. Testes Unitários
- [ ] Cenários nominais (casos de uso principais)
- [ ] Cenários de borda (limites máximos/mínimos)
- [ ] Cenários de erro (dados inválidos, nulos, ausentes)
- [ ] Cobertura mínima de 80%

### 5.2. Testes de Integração
- [ ] Comunicação com banco de dados
- [ ] Consumo de APIs
- [ ] Fluxo completo de dados

### 5.3. Testes de Regressão
- [ ] Verificar funcionalidades existentes do Sync
- [ ] Garantir não regressão em módulos dependentes

### 5.4. Testes de Performance
- [ ] Simulação de carga alta
- [ ] Medição de tempo de resposta
- [ ] Monitoramento de uso de recursos
- [ ] Teste de estresse

### 5.5. Testes de Aceitação (UAT)
- [ ] Execução com dados reais ou anonimizados
- [ ] Comparação com resultados de referência (E3)
- [ ] Validação com stakeholders
- [ ] Aprovação do time de produto

### 5.6. Testes de Falha
- [ ] Indisponibilidade de serviços dependentes
- [ ] Dados corrompidos ou incompletos
- [ ] Timeout de comunicação
- [ ] Recovery automático

---

## 6. Documentação e Treinamento

### 6.1. Documentação técnica
- [ ] Atualizar documentação de arquitetura
- [ ] Documentar fluxo de processamento
- [ ] Listar variáveis e fórmulas utilizadas
- [ ] Criar diagramas (fluxo, sequência, componentes)

### 6.2. Guia de operação
- [ ] Como monitorar o cálculo
- [ ] Como identificar falhas
- [ ] Procedimentos de emergência
- [ ] Troubleshooting comum

### 6.3. Compartilhamento com equipes
- [ ] Apresentação para time de engenharia
- [ ] Wiki ou Notion com documentação
- [ ] Sessão de dúvidas

### 6.4. Treinamento
- [ ] Treinamento rápido com time de QA
- [ ] Treinamento com time de DevOps
- [ ] Material de referência para novos membros

---

## 7. Homologação e Deploy

### 7.1. Ambiente de homologação
- [ ] Subir funcionalidade em homologação
- [ ] Executar bateria completa de testes
- [ ] Validar cenários reais

### 7.2. Validação com stakeholders
- [ ] Apresentar resultados para produto
- [ ] Validar com time de engenharia
- [ ] Aprovação de operações

### 7.3. Planejar deploy em produção
- [ ] Definir janela de deploy
- [ ] Planejar rollback
- [ ] Comunicar impactos aos times
- [ ] Preparar check-list de deploy

### 7.4. Executar deploy
- [ ] Deploy com monitoramento ativo
- [ ] Acompanhar logs em tempo real
- [ ] Verificar dashboards de métricas
- [ ] Confirmar funcionamento

### 7.5. Pós-deploy
- [ ] Monitorar por 24-48 horas
- [ ] Verificar anomalias
- [ ] Coletar feedback inicial
- [ ] Documentar lições aprendidas

---

## 8. Monitoramento e Melhoria Contínua

### 8.1. Dashboards
- [ ] Precisão do cálculo (comparação com referência)
- [ ] Latência de processamento
- [ ] Volume de processamento
- [ ] Taxa de erros

### 8.2. Alertas
- [ ] Desvio de precisão acima do tolerado
- [ ] Latência acima do limite
- [ ] Falhas de processamento
- [ ] Dados indisponíveis

### 8.3. Feedback
- [ ] Coletar feedback de usuários
- [ ] Coletar feedback de operações
- [ ] Registrar melhorias sugeridas

### 8.4. Otimização
- [ ] Ajustar parâmetros baseado em dados reais
- [ ] Refatorar código identificado como gargalo
- [ ] Implementar melhorias sugeridas
- [ ] Planejar próximos ciclos de melhoria

---

## 9. Checklist Final de Conclusão

- [ ] Especificação compreendida e validada com PO/arquiteto
- [ ] Código desenvolvido e revisado
- [ ] Todos os testes executados com sucesso (unitários, integração, performance, UAT)
- [ ] Documentação atualizada e aprovada
- [ ] Deploy em produção realizado e estável
- [ ] Monitoramento ativo e alertas configurados
- [ ] Feedback inicial coletado e registrado
- [ ] ADRs (Architecture Decision Records) documentadas

---

## Referências Técnicas

- `Driver.General.DM2_1.Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Original`
- `MDB_DM2_V1_2_1.Get_ValorProporcionalCorrente`
- `MDB_DM2_V1_2_1.Set_AjusteFinoParaCalculoDeCorrente`
- **PR de referência para implementação:** Pull Request 19057: [#61711]: Regra - Campos 16M e 16U

---

## Observações Importantes

1. **Envolver o time de arquitetura desde o início** para alinhar expectativas e decisões técnicas.
2. **Manter comunicação constante com stakeholders** sobre prazos, riscos e progresso.
3. **Registrar todas as decisões técnicas em ADRs** para rastreabilidade.
4. **Priorizar testes com dados reais** para validar precisão do cálculo.
5. **Garantir rollback planejado** antes de qualquer deploy em produção.

---

## Diário de Bordo

### 03/08/2026 - Início do projeto

**Ação:** Li a documentação DM2 - Especificações.

**Decisão:** Implementar as regras de cálculo de corrente por partes, em vez de tentar implementar tudo de uma vez.

**Justificativa:** A documentação é extensa e não foi possível compreender 100% de uma só vez. Implementar incrementalmente permite:
- Entender cada regra individualmente antes de passar para a próxima
- Reduzir risco de erros
- Facilitar testes e validação de cada parte
- Possibilitar revisão parcial com o time

**Próximo passo:** Identificar quais regras são independentes e podem ser implementadas primeiro (aquelas com menor dependência de outras).

---

### 03/08/2026 - Análise do PR de referência

**Ação:** Analisei o Pull Request de referência ([#61710]: Regras - Campos específicos) e reli a documentação DM2.

**Conclusão:** Precisarei utilizar o arquivo `AlgorithmFieldMap.json` para importar os campos necessários para o funcionamento do DM2.

**Campos identificados:**
- `_Convertido` - valor convertido da entrada analógica
- `_Filtrado` - valor filtrado para cálculo

**Observação:** Esses campos são essenciais para que o algoritmo de cálculo de corrente funcione corretamente. Sem eles, a API rejeita a estrutura.

**Próximo passo:** Analisar a estrutura do `AlgorithmFieldMap.json` no PR de referência para entender como esses campos são mapeados e importados.

---

### 03/08/2026 - Plano de implementação definido

**Ação:** Defini o plano de implementação baseado na análise do PR de referência e da documentação.

**Plano de Implementação:**

1. **Criar documento de regra de negócio**
   - Seguir a lógica usada para os campos `16_M` e `16_U``Sigma.Sync.Run.Worker`
   - Criar arquivo dentro de `Algorithms` e colocar a Lógica: `IF Set_AjusteFinoParaCalculoDeCorrente = 0 THEN Set_AjusteFinoParaCalculoDeCorrente = 4095` 
   - Ver uma alternativa de adicionar de forma mais pratica o calculo `(Driver.General.DM2_1.Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Original * MDB_DM2_V1_2_1.Get_ValorProporcionalCorrente) / MDB_DM2_V1_2_1.Set_AjusteFinoParaCalculoDeCorrente` que se repete para os 24 campos de corrente

2. **mapeamento do DM2**
   - DM2 passa a ter o arquivo `DM2-algorithmFieldMaps-sync-import.json` com os campos: `Get_ValorProporcionalCorrente` e `Set_AjusteFinoParaCalculoDeCorrente`

3. **Atualizar arquivo de importação principal**
   - Arquivo: `DM2-sigma-sync-import`
   - Adicionar campos: `_Filtrado` e `_Convertido`, `_Corrente`
   - **Nota:** A doc diz que esses campos são criados apenas nas tabelas `H` e `S`, mas vou adicionar no JSON principal (criará nas 4 tabelas)

**Observação:** Essa abordagem segue o padrão já estabelecido no PR de referência para campos 16M e 16U.
