# Tasks - Sigmafacelift

## Task 1: Atualizar Wiki com Scripts e Roteiro de Replicação
**Descrição:** Atualizar a wiki do repositório Sigmafacelift com os scripts oficiais de replicação de dados da Copel e o passo a passo detalhado.

**Critérios de Aceite:**
- Scripts extraídos do arquivo `Implantacao_ReplicacaoDadosCopel.zip`
- Scripts documentados na wiki
- Passo a passo de implantação adicionado à wiki
- Estrutura de pastas explicada na documentação

---

## Task 2: Adicionar Scripts PostgreSQL Oficiais
**Descrição:** Adicionar os scripts oficiais do PostgreSQL na pasta `docs` do repositório Sigmafacelift.

**Critérios de Aceite:**
- Scripts extraídos do arquivo `postgres_scripts_oficiais.zip`
- Scripts adicionados na pasta `docs` do repositório
- Scripts da pasta `system` identificados e organizados

---

## Task 3: Atualizar Roteiro de Implantação
**Descrição:** Atualizar o roteiro de implantação existente e adicionar seção específica para quando o provider for PostgreSQL.

**Critérios de Aceite:**
- Seção específica para PostgreSQL adicionada ao roteiro
- Instrução para execução dos scripts da pasta `system` quando provider for PostgreSQL
- Documentação clara e objetiva

---

## Task 4: Bug - Worker de Manutenção do Resfriamento Parou de Funcionar
**Descrição:** Após executar scripts de configuração, o worker de manutenção do resfriamento parou de funcionar. A configuração de grupos começou a aparecer (antes estava ausente), mas o frontend não atualiza as alterações.

**Tipo:** Bug  
**Prioridade:** Alta  
**Severidade:** 1 - Crítica  
**Módulo:** Resfriamento / Worker de Manutenção  

### Comportamento Atual
1. Worker de manutenção do resfriamento parou de executar
2. Configuração de grupos de resfriamento começou a aparecer (estava ausente)
3. Frontend exibe mensagem de aviso mas nunca atualiza:
   > "Atenção! Recentemente houveram alterações nos parâmetros deste módulo e/ou no ativo, porém, as mesmas ainda não foram consideradas pelo algoritmo. Aguarde até a próxima execução do algoritmo para que estas alterações sejam consideradas."
4. Erro no log:
   ```
   [14:12:17 ERR] (<s:Treetech.Sigma.Worker.Servico.Servicos.ResultadoConsultaServico.>) Não existem grupos de resfriamento ativos
   ```

### Comportamento Esperado
1. Worker de manutenção deve executar normalmente
2. Grupos de resfriamento devem ser identificados e processados
3. Frontend deve atualizar após execução do algoritmo
4. Sem erros no log sobre grupos inativos

### Passos para Reproduzir
1. Executar scripts de configuração de resfriamento
2. Verificar se grupos de resfriamento aparecem na configuração
3. Aguardar execução do worker de manutenção
4. Verificar log para erro "Não existem grupos de resfriamento ativos"
5. Verificar frontend - mensagem de aviso persiste sem atualização

### Análise Técnica
**Causa Provável:**
- Worker de manutenção não está conseguindo identificar grupos de resfriamento ativos
- Pode haver problema na query de consulta ou no status dos grupos (flag ativo = false)
- Worker pode estar parando antes de processar os grupos

**Arquivos para Investigar:**
- `Treetech.Sigma.Worker.Servico.Servicos.ResultadoConsultaServico` (onde ocorre o erro)
- Configuração de grupos de resfriamento no banco de dados
- Worker de manutenção do resfriamento (agendamento e execução)
- Frontend: lógica de atualização após alterações nos parâmetros

### Diagnóstico Adicional Necessário
- [ ] Verificar se grupos de resfriamento estão com status "ativo" no banco
- [ ] Conferir agendamento do worker de manutenção
- [ ] Analisar logs anteriores para identificar quando parou de funcionar
- [ ] Verificar se scripts alteraram alguma configuração crítica

### Notas
- Bug reportado em: 29/07/2026
- Ambiente: Produção/Homologação (verificar)
- Usuário reportou: Manoela Urias

---

