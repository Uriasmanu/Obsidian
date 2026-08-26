# Adicionar nova tabela ao Merge Replication

## Objetivo
Adicionar a tabela `ConfiguracaoAlarme` ao processo de Merge Replication no SQL Server, garantindo que as configurações estejam iguais entre os bancos da Figueira e da Central.

---

## Scripts

### 1. Verificar colunas da tabela
```sql
USE sigmaecm_copel_figueira;
GO
SELECT c.name AS coluna, ty.name AS tipo, c.is_identity, c.is_rowguidcol
FROM   sys.columns c
JOIN   sys.types ty ON ty.user_type_id = c.user_type_id
WHERE  c.object_id = OBJECT_ID(N'dbo.ConfiguracaoAlarme')
  AND  (c.is_identity = 1 OR ty.name = 'uniqueidentifier')
ORDER  BY c.column_id;
GO
```
**O que faz:** Lista as colunas da tabela `ConfiguracaoAlarme` filtrando por colunas de identidade (`is_identity = 1`) ou do tipo `uniqueidentifier`. É necessário verificar se a coluna `Id` já está configurada como `ROWGUIDCOL` antes de prosseguir com a alteração.

---

### 2. Alterar coluna Id para ROWGUIDCOL (Figueira)
```sql
USE sigmaecm_copel_figueira;
GO
ALTER TABLE dbo.ConfiguracaoAlarme ALTER COLUMN Id ADD ROWGUIDCOL;
GO
```
**O que faz:** Adiciona a propriedade `ROWGUIDCOL` à coluna `Id` da tabela no banco da Figueira. Essa propriedade é obrigatória para tabelas participantes de Merge Replication, pois permite o rastreamento único das linhas entre os bancos de dados.

---

### 3. Alterar coluna Id para ROWGUIDCOL (Central)
```sql
USE sigmaecm;
GO
ALTER TABLE dbo.ConfiguracaoAlarme ALTER COLUMN Id ADD ROWGUIDCOL;
GO
```
**O que faz:** Realiza a mesma alteração no banco da Central (`sigmaecm`). Ambos os bancos devem ter a configuração idêntica para que a replicação funcione corretamente.

---

### 4. Adicionar tabela à publicação Merge
```sql
USE sigmaecm_copel_figueira;
GO
EXEC sp_addmergearticle
     @publication               = N'Pub_sigmaecm',
     @article                   = N'ConfiguracaoAlarme',
     @source_owner              = N'dbo',
     @source_object             = N'ConfiguracaoAlarme',
     @type                      = N'table',
     @column_tracking           = N'true',
     @force_invalidate_snapshot = 1,
     @force_reinit_subscription = 1;
GO
```
**O que faz:** Adiciona a tabela `ConfiguracaoAlarme` como artigo à publicação Merge `Pub_sigmaecm`. Parâmetros importantes:
- `@column_tracking = 'true'`: Habilita rastreamento a nível de coluna (mais eficiente que rastreamento a nível de linha)
- `@force_invalidate_snapshot = 1`: Invalida o snapshot atual (necessário para incluir novo artigo)
- `@force_reinit_subscription = 1`: Força reinicialização das assinaturas existentes

---

### 5. Verificar assinaturas Merge
```sql
USE sigmaecm_copel_figueira;
GO
EXEC sp_helpmergesubscription @publication = N'Pub_sigmaecm';
GO
```
**O que faz:** Lista todas as assinaturas vinculadas à publicação `Pub_sigmaecm`. Permite verificar o status das assinaturas e confirmar se a reinicialização foi aplicada corretamente após a adição do novo artigo.

---

### 6. Verificar artigos da publicação
```sql
USE sigmaecm_copel_figueira;
GO
EXEC sp_helpmergearticle @publication = N'Pub_sigmaecm';
GO
```
**O que faz:** Lista todos os artigos (tabelas) vinculados à publicação Merge. É útil para confirmar que a tabela `ConfiguracaoAlarme` foi adicionada com sucesso e está configurada corretamente.

---

### 7. Verificar dependências de chaves estrangeiras
```sql
USE sigmaecm;
GO
SELECT OBJECT_NAME(fk.parent_object_id) AS tabela_que_referencia
FROM   sys.foreign_keys fk
WHERE  OBJECT_NAME(fk.referenced_object_id) = N'ConfiguracaoAlarme';
GO
```
**O que faz:** Lista todas as tabelas que possuem chaves estrangeiras referenciando `ConfiguracaoAlarme`. Essa verificação é importante para garantir que não haverá problemas de integridade referencial durante a replicação, pois tabelas dependentes também podem precisar ser incluídas no processo.

---

## Resumo dos comandos

| # | Script | Banco | Descrição | Parâmetros Importantes |
|---|--------|-------|-----------|------------------------|
| 1 | SELECT columns | Figueira | Verificar colunas da tabela | Filtra por `is_identity` e `uniqueidentifier` |
| 2 | ALTER COLUMN | Figueira | Adicionar ROWGUIDCOL à coluna Id | Obrigatório para Merge Replication |
| 3 | ALTER COLUMN | Central | Adicionar ROWGUIDCOL à coluna Id | Deve ser idêntico ao banco da Figueira |
| 4 | sp_addmergearticle | Figueira | Adicionar tabela à publicação Merge | `column_tracking`, `force_invalidate_snapshot`, `force_reinit_subscription` |
| 5 | sp_helpmergesubscription | Figueira | Verificar status das assinaturas | Publicação: `Pub_sigmaecm` |
| 6 | sp_helpmergearticle | Figueira | Verificar artigos da publicação | Publicação: `Pub_sigmaecm` |
| 7 | SELECT FK | Central | Verificar dependências de chaves estrangeiras | Tabelas que referenciam `ConfiguracaoAlarme` |

---

## Notas Importantes
- **ROWGUIDCOL** é obrigatório para Merge Replication pois identifica unicamente cada linha entre múltiplos bancos de dados
- Ambos os bancos (Figueira e Central) devem ter a mesma configuração de colunas
- Após adicionar o artigo, o snapshot deve ser gerado novamente e as assinaturas reinicializadas
- Verificar dependências de chaves estrangeiras antes de prosseguir
