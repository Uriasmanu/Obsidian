[[COPEL]]


 - Cria o usuário repl_user com permissão Owner para criar a publicação Merge
```
USE sigmaecm_copel_figueira;
GO
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'repl_user')
    CREATE USER repl_user FOR LOGIN repl_user;
ALTER ROLE db_owner ADD MEMBER repl_user;
GO 

USE master;
GO
EXEC sp_replicationdboption
    @dbname  = N'sigmaecm_copel_figueira',
     @optname = N'merge publish',
     @value   = N'true';
GO
```

- Cria publicação tipo Merge
```
USE sigmaecm_copel_figueira;
GO
EXEC sp_addmergepublication
     @publication           = N'Pub_sigmaecm',
     @description           = N'Merge bidirecional de tabelas especificas: Figueira <-> Central',
     @sync_mode             = N'native',
     @retention             = 14,
     @allow_push            = N'false',
     @allow_pull            = N'true',
     @allow_anonymous       = N'false',
     @centralized_conflicts = N'true',
     @conflict_logging      = N'both',
     @dynamic_filters       = N'false';
GO

EXEC sp_addpublication_snapshot
     @publication             = N'Pub_sigmaecm',
     @frequency_type          = 1,
     @publisher_security_mode = 0,
     @publisher_login         = N'repl_user',
     @publisher_password      = N'tr3t3Ch2!PW';
GO

EXEC sp_grant_publication_access
     @publication = N'Pub_sigmaecm',
     @login       = N'repl_user';
GO
```

- Verifica quais tabelas têm coluna `uniqueidentifier` (necessário para replicação merge, que exige um GUID identificador de linha).
```
USE sigmaecm_copel_figueira;
GO
SELECT t.name AS tabela,
       c.name AS coluna,
       ty.name AS tipo,
       c.is_rowguidcol
FROM   sys.tables t
JOIN   sys.columns c   ON c.object_id = t.object_id
JOIN   sys.types ty    ON ty.user_type_id = c.user_type_id
WHERE  t.name IN (N'MonitoramentoRedeOnline', N'ModuloAtivo', N'MonitoramentoRedeHistorico',
                  N'Usuario', N'AlarmeAnunciador', N'Alarme', N'AlarmeAnunciadorEvento')
  AND  ty.name = 'uniqueidentifier'
ORDER  BY t.name, c.name;
```

Caso a coluna `is_rowguidcol`  = 0 

- Script selecionando as colunas para serem consideradas no Merge, alterando o valor do campo para 1
```
USE sigmaecm_copel_figueira;
GO
SELECT t.name AS tabela,
       c.name AS coluna,
       ty.name AS tipo,
       c.is_rowguidcol
FROM   sys.tables t
JOIN   sys.columns c   ON c.object_id = t.object_id
JOIN   sys.types ty    ON ty.user_type_id = c.user_type_id
WHERE  t.name IN (N'MonitoramentoRedeOnline', N'ModuloAtivo', N'MonitoramentoRedeHistorico',
                  N'Usuario', N'AlarmeAnunciador', N'Alarme', N'AlarmeAnunciadorEvento')
  AND  ty.name = 'uniqueidentifier'
ORDER  BY t.name, c.name;
```


_DISMONTFLIC_

 - Criando a Assinatura do Merge
```
USE sigmaecm_copel_figueira;
GO
EXEC sp_addmergesubscription
     @publication       = N'Pub_sigmaecm',
     @subscriber        = N'DISMONTFLIC\MSSQLSERVERTT',
     @subscriber_db     = N'sigmaecm',
     @subscription_type = N'pull',
     @sync_type         = N'automatic';
GO
```

```
USE sigmaecm_copel_figueira;
GO
EXEC sys.sp_startpublication_snapshot @publication = N'Pub_sigmaecm';
GO
```

```
USE distribution;
GO
SELECT TOP (10) [time], comments
FROM   dbo.MSsnapshot_history
ORDER  BY [time] DESC;
GO
```

- Resultado OK
``2026-07-28 16:03:24.603	2	[100%] A snapshot of 7 article(s) was generated.

- Cria Login (se não existir), e cadastra o usuário com permissão Owner no banco. 
```
 USE master;
GO
IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = N'DISMONTFLIC\svc_repl')
    CREATE LOGIN [DISMONTFLIC\svc_repl] FROM WINDOWS;
GO
USE sigmaecm;
GO
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'DISMONTFLIC\svc_repl')
    CREATE USER [DISMONTFLIC\svc_repl] FOR LOGIN [DISMONTFLIC\svc_repl];
ALTER ROLE db_owner ADD MEMBER [DISMONTFLIC\svc_repl];
GO
```

- Criando e configurando assinatura *Pull*
```
USE sigmaecm;
GO
EXEC sp_addmergepullsubscription
     @publisher            = N'Srv-Jd-Figueira',
     @publisher_db         = N'sigmaecm_copel_figueira',
     @publication          = N'Pub_sigmaecm',
     @subscriber_type      = N'global',
     @subscription_priority = 75;
GO
```

```
USE sigmaecm;
GO
EXEC sp_addmergepullsubscription_agent
     @publisher                 = N'Srv-Jd-Figueira',
     @publisher_db              = N'sigmaecm_copel_figueira',
     @publication               = N'Pub_sigmaecm',
     @distributor               = N'Srv-Jd-Figueira',
     @job_login                 = N'DISMONTFLIC\svc_repl',
     @job_password              = N'Repl#Copel2026',
     @publisher_security_mode   = 0,
     @publisher_login           = N'repl_user',
     @publisher_password        = N'tr3t3Ch2!PW',
     @distributor_security_mode = 0,
     @distributor_login         = N'repl_user',
     @distributor_password      = N'tr3t3Ch2!PW',
     @frequency_type            = 64;
GO
```

- Erro 
```
DBCC execution completed. If DBCC printed error messages, contact your system administrator.
DBCC execution completed. If DBCC printed error messages, contact your system administrator.
WARNING: The database 'sigmaecm' does not contain database master key. Create a database master key and then update all replication secrets in this database. For more information, see [https://aka.ms/sql-tr-dmk-warning-troubleshooting](https://aka.ms/sql-tr-dmk-warning-troubleshooting).
DBCC execution completed. If DBCC printed error messages, contact your system administrator.
DBCC execution completed. If DBCC printed error messages, contact your system administrator.
WARNING: The database 'sigmaecm' does not contain database master key. Create a database master key and then update all replication secrets in this database. For more information, see [https://aka.ms/sql-tr-dmk-warning-troubleshooting](https://aka.ms/sql-tr-dmk-warning-troubleshooting).
DBCC execution completed. If DBCC printed error messages, contact your system administrator.
DBCC execution completed. If DBCC printed error messages, contact your system administrator.
WARNING: The database 'sigmaecm' does not contain database master key. Create a database master key and then update all replication secrets in this database. For more information, see [https://aka.ms/sql-tr-dmk-warning-troubleshooting](https://aka.ms/sql-tr-dmk-warning-troubleshooting).
Job 'Srv-Jd-Figueira-sigmaecm_copel_figueira-Pub_sigmaecm-DISMONTFLIC\MSSQLSERVER-sigmaecm- 0' started successfully.
DBCC execution completed. If DBCC printed error messages, contact your system administrator.
DBCC execution completed. If DBCC printed error messages, contact your system administrator.
WARNING: The database 'sigmaecm' does not contain database master key. Create a database master key and then update all replication secrets in this database. For more information, see [https://aka.ms/sql-tr-dmk-warning-troubleshooting](https://aka.ms/sql-tr-dmk-warning-troubleshooting).

Completion time: 2026-07-28T16:12:29.1005615-03:00
```


- Configurado a Senha [[Masterkey]] no DISMONTFLIC
```
USE sigmaecm;
GO
CREATE MASTER KEY ENCRYPTION BY PASSWORD = N'h$t$Dm*8m&Ue';
GO
```

- Atualizar senha do Distribuidor
```
USE sigmaecm;
GO
EXEC sp_change_subscription_properties
     @publisher          = N'Srv-Jd-Figueira',
     @publisher_db       = N'sigmaecm_copel_figueira',
     @publication        = N'Pub_sigmaecm',
     @property           = N'distributor_password',
     @value              = N'tr3t3Ch2!PW';
GO
```

- _Altertable_ para add [[ROWGUIDCOL]]
```
USE sigmaecm;
GO
ALTER TABLE dbo.MonitoramentoRedeOnline    ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.ModuloAtivo                ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.MonitoramentoRedeHistorico ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.Usuario                    ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.AlarmeAnunciador           ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.Alarme                     ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.AlarmeAnunciadorEvento     ALTER COLUMN Id ADD ROWGUIDCOL;
GO
```

>   Excluído FK 
> ALTER TABLE Alarme DROP CONSTRAINT FK_ModuloDm2Configuracao_Alarme_AlarmeId
> 
> SELECT name
> FROM sys.key_constraints
> WHERE type = 'PK'
> AND OBJECT_NAME(parent_object_id) = 'Alarme';
>  
> ALTER TABLE Alarme DROP CONSTRAINT PK_Alarme;
> 

VISTO QUE NÃO ACONTECE A SINCRONIZAÇÃO 
 - Analisado e concluido que a configuração da assinatura foi errada e precisará ser refeita. 

- Reset da assinatura - _DISMONTFLIC_
```
USE sigmaecm;
GO
EXEC sp_dropmergepullsubscription
     @publisher    = N'Srv-Jd-Figueira',
     @publisher_db = N'sigmaecm_copel_figueira',
     @publication  = N'Pub_sigmaecm';
GO
```

- Remove assinatura Pull - _FIGUEIRA_
  ```
USE sigmaecm;
GO
EXEC sp_dropmergepullsubscription
     @publisher    = N'Srv-Jd-Figueira',
     @publisher_db = N'sigmaecm_copel_figueira',
     @publication  = N'Pub_sigmaecm';
GO
  ```

- Recria assinatura - _FIQUEIRA_
```
USE sigmaecm_copel_figueira;
GO
EXEC sp_addmergesubscription
     @publication       = N'Pub_sigmaecm',
     @subscriber        = N'DISMONTFLIC\MSSQLSERVERTT',
     @subscriber_db     = N'sigmaecm',
     @subscription_type = N'pull',
     @sync_type         = N'none';
GO
```

- Recria assinante - _DISMONTFLIC_
```
USE sigmaecm;
GO
EXEC sp_addmergepullsubscription
     @publisher            = N'Srv-Jd-Figueira',
     @publisher_db         = N'sigmaecm_copel_figueira',
     @publication          = N'Pub_sigmaecm',
     @subscriber_type      = N'global',
     @subscription_priority = 75,
     @sync_type            = N'none';
GO

EXEC sp_addmergepullsubscription_agent
     @publisher                 = N'Srv-Jd-Figueira',
     @publisher_db              = N'sigmaecm_copel_figueira',
     @publication               = N'Pub_sigmaecm',
     @distributor               = N'Srv-Jd-Figueira',
     @job_login                 = N'DISMONTFLIC\svc_repl',
     @job_password              = N'Repl#Copel2026',
     @publisher_security_mode   = 0,
     @publisher_login           = N'repl_user',
     @publisher_password        = N'tr3t3Ch2!PW',
     @distributor_security_mode = 0,
     @distributor_login         = N'repl_user',
     @distributor_password      = N'tr3t3Ch2!PW',
     @frequency_type            = 64;
GO
```


- Consulta para verificar sincronização
```
USE distribution;
GO
SELECT TOP (10) [time], runstatus, comments
FROM   dbo.MSmerge_history
ORDER  BY [time] DESC;
GO
```


> [!NOTE] Resultado OK
>Feito a inserção de um alarme via Script, para validação e ocorreu a sincronização esperada. 

