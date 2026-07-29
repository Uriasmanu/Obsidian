[[COPEL]]

Configurar usuário e senha

_DOIS SERVERS_
***Prompt de Comando CMD***

``net user svc_repl Repl#Copel2026``
- Define a senha do usuário existente

_FIQUEIRA_
``net share
- exibe as pastas compartilhada

``net share repldata2 /delete 
- Remove o compartilhamento de rede (feito para as pastas _repldata_ e _repldata2_)

``net share repldata=C:\repldata /grant:svc_repl,READ 
- cria um novo compartilhamento, apontando para pasta local

``icacls C:\repldata /grant "svc_repl:(OI)(CI)R" 
- Cria permissão de NTFS de leitura

``net use * /delete /yes
- Força a desconexão dos usuários as pastas compartilhada

``net use \\SRV-JD-FIGUEIRA\repldata /user:SRV-JD-FIGUEIRA\svc_repl Repl#Copel2026
- Cria um compartilhamento da pasta e autenticando com o usuário _svc_repl

``\\SRV-JD-FIGUEIRA\repldata
 - Valida configuração de rede
  
  ``SELECT name FROM sys.sql_logins WHERE name = N'repl_user';`` 
 -  Consulta se existe o usuário cadastrado. 

  `` icacls C:\repldata /grant "NT SERVICE\SQLSERVERAGENT:(OI)(CI)F"
 - Concede permissão ao Agente SQL 
 
  ![[Pasted image 20260728110019.png|444]]

- Cria usuário e configura permissão
```USE master;
GO
IF NOT EXISTS (SELECT 1 FROM sys.sql_logins WHERE name = N'repl_user')
    CREATE LOGIN repl_user WITH PASSWORD = N'tr3t3Ch2!PW', CHECK_POLICY = ON;
GO
-- Da acesso ao banco publicado (necessario para os agentes e para o snapshot).
USE ecm_copel_jdfigueira;
GO
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'repl_user')
    CREATE USER repl_user FOR LOGIN repl_user;
ALTER ROLE db_owner ADD MEMBER repl_user;
GO
```

- Cria o Distribuidor
```
USE master;
GO
EXEC sp_adddistributor
     @distributor = N'Srv-Jd-Figueira',          -- instancia que sera o Distributor. Deve ser igual a SELECT @@SERVERNAME da substacao.
     @password    = N'8wW%9Ls!a3ls';  -- senha da conta interna 'distributor_admin' usada na comunicacao com o distribuidor.
GO

EXEC sp_adddistributiondb
     @database      = N'distribution',           -- nome do banco de distribuicao (convencao: 'distribution'). Guarda os comandos a entregar.
     @security_mode = 0,                         -- 0 = SQL Authentication.
     @login         = N'repl_user',              -- login SQL usado nessa conexao.
     @password      = N'tr3t3Ch2!PW';   -- senha do login SQL.
GO

-- Registra a substacao como Publisher atendido pelo distribuidor local.
EXEC sp_adddistpublisher
     @publisher         = N'Srv-Jd-Figueira',    -- instancia publicadora (a propria substacao).
     @distribution_db   = N'distribution',       -- banco de distribuicao que atende este publisher.
     @security_mode     = 0,                     -- 0 = SQL Authentication na ligacao Publisher <-> Distributor.
     @login             = N'repl_user',          -- login SQL usado nessa conexao.
     @password          = N'tr3t3Ch2!PW',  -- senha do login SQL.
     @working_directory = N'\\Srv-Jd-Figueira\repldata';  -- PASTA DE SNAPSHOT (UNC). E daqui que a central (pull) LE o snapshot. Precisa dar leitura para a conta do agente da central.
GO
```

- Resultado 
```Configuration option 'allow updates' changed from 0 to 1. Run the RECONFIGURE statement to install.
 
Creating distribution tables
 
Creating table MSreplservers
Creating view MSsysservers_replservers
Creating table MSredirected_publishers
Creating table MSrepl_version
Creating table MSpublisher_databases
Creating clustered index ucMSpublisher_databases
Creating table MSpublications
Creating clustered index ucMSpublications
Creating table MSarticles
Creating clustered index ucMSarticles
Creating table MSsubscriptions
Creating clustered index ucMSsubscirptions
Creating index iMSsubscriptions
Creating index iMSsubscriptions2
Creating table MSmerge_subscriptions
Creating clustered index ucMSmerge_subscriptions
Creating table MSrepl_transactions
Creating clustered index usMSrepl_transactions
Creating table MSrepl_commands
Creating clusterd index ucMSrepl_commands
Creating table MSrepl_orginators
Creating clustered index usMSrepl_originators
Creating table MSsubscriber_info
Creating clustered index ucMSsubscriber_info
Creating table MSsubscriber_schedule
Creating table MSsnapshot_history
Creating clustered index ucMSsnapshot_history
Creating table MSlogreader_history
Creating clustered index ucMSlogreader_history
Creating table MSdistribution_history
Creating clustered index ucMSdistribution_history
Creating table MSsnapshot_agents
Creating clustered index ucMSsnapshot_agents
Creatingindex iMSsnapshot_agents
Creating table MSlogreader_agents
Creating clustered index ucMSlogreader_agents
Creatingindex iMSlogreader_agents
Creating table MSdistribution_agents
Creating clustered index ucMSdistribution_agents
Creatingindex iMSdistribution_agents
Creating table MSmerge_agents
Creating clustered index ucMSmerge_agents
Creating table MSrepl_identity_range
Creating table MSpublication_access
Creating clustered index ucMSpublication_access
Creating table MSqreader_agents
Creating unique index ucMSqreader_agents
Creating table MSqreader_history
Creating clustered index ucMSqreader_history
Creating table MSrepl_backup_lsns
Creating clustered index ucMSrepl_backup_lsns
Creating table MSpublicationthresholds
Creating clustered index ucmspublicationthresholds
Creating table IHpublishers
Creating table IHpublishertables
Creating table IHarticles
Creating table IHpublishercolumns
Creating table IHcolumns
Creating table IHindextypes
Creating table IHpublisherindexes
Creating table IHpublishercolumnindexes
Creating table IHpublications
Creating table IHextendedArticleView
Creating table IHconstrainttypes
Creating table IHpublisherconstraints
Creating table IHpublishercolumnconstraints
Creating table IHsubscriptions
Creating table sysschemaarticles
Creating table MScached_peer_lsns
Creating view IHextendedSubscriptionView
Creating view syssubscriptions
Creating view syspublications
Creating view sysarticles
Creating view sysarticlecolumns
Creating view IHsyscolumns
Creating table MSrepl_agent_jobs
Creating table MSnosyncsubsetup
 
Dropping all distribution stored procedures and functions that are now in resource or are obsolete
 
 
Dropping all distribution stored procedures and functions that are created locally
 
Creating 'fn_MSmask_agent_type'.
Creating 'sp_MSset_syncstate'.
Creating 'sp_MSadd_repl_commands27'.
Creating 'sp_MSadd_replcmds'.
Creating 'sp_MSremove_published_jobs'.
Creating 'sp_MSsubscription_cleanup'.
Creating 'sp_MSdelete_dodelete'.
Creating 'sp_MSdelete_publisherdb_trans'.
Creating 'sp_MSmaximum_cleanup_seqno'.
Creating 'sp_MSdistribution_delete'.
Creating 'sp_MSdistribution_cleanup'.
Creating 'sp_MShistory_cleanup'.
Creating 'sp_MSget_repl_version'.
Creating view MSdistribution_status
Creating 'sp_MSlog_agent_cancel'.
 
Adding user 'guest'.
 
 
Adding role 'replmonitor'.
 
Configuration option 'allow updates' changed from 1 to 0. Run the RECONFIGURE statement to install.

Horário de conclusão: 2026-07-28T11:08:17.2513953-03:00
```

- Cria Agent```
```
USE master;
GO
EXEC sp_replicationdboption
     @dbname  = N'ecm_copel_jdfigueira',                     -- banco de origem que sera publicado.
     @optname = N'publish',                      -- opcao 'publish' liga a capacidade de publicacao transacional/snapshot neste banco.
     @value   = N'true';                         -- 'true' liga, 'false' desliga.
GO

-- Cria o Log Reader Agent JA com SQL Authentication para conectar no publisher.
-- IMPORTANTE: rode isto ANTES do sp_addpublication. Se a publicacao for criada
-- primeiro, o Log Reader e criado em Windows Auth por padrao.
USE ecm_copel_jdfigueira;
GO
EXEC sp_addlogreader_agent
     @publisher_security_mode = 0,               -- 0 = SQL Authentication para conectar no publisher (a substacao).
     @publisher_login         = N'repl_user',    -- login SQL usado pelo Log Reader no publisher.
     @publisher_password      = N'tr3t3Ch2!PW';  -- senha do login SQL.
     -- @job_login/@job_password omitidos de proposito: o JOB roda sob a conta de
     -- servico do SQL Server Agent (Windows). Isso e estrutural, nao vira SQL Auth.
GO
```

- Resultado
```
Job 'SRV-JD-FIGUEIRA-ecm_copel_jdfigueira-1' started successfully.

Horário de conclusão: 2026-07-28T11:13:39.5333880-03:00

```

- Cria Publicador
```
USE ecm_copel_jdfigueira;
GO
EXEC sp_addpublication
     @publication       = N'Pub_ecm_jdfigueira', -- nome da publicacao (identificador deste conjunto de artigos).
     @description       = N'Replicacao transacional de todas as tabelas: Substacao -> Central',  -- texto livre.
     @status            = N'active',             -- 'active' = publicacao pronta para uso; 'inactive' = criada mas parada.
     @repl_freq         = N'continuous',         -- 'continuous' = transacional (Log Reader entrega mudancas continuamente); 'snapshot' = so snapshot periodico.
     @sync_method       = N'concurrent',         -- 'concurrent' = gera o snapshot sem travar as tabelas (menos bloqueio); 'native' travaria durante o snapshot.
     @independent_agent = N'true',               -- 'true' = um Distribution Agent dedicado por assinatura (recomendado); 'false' = agente compartilhado.
     @allow_push        = N'false',              -- 'false' = NAO permite assinatura push (a substacao nunca empurra para a central). Reforca a politica de seguranca.
     @allow_pull        = N'true',               -- 'true' = permite assinatura pull (a central puxa). E o modo que respeita o firewall.
     @allow_anonymous   = N'false',              -- 'false' = exige assinaturas registradas/nomeadas (mais controle e rastreio).
     @immediate_sync    = N'false';              -- 'false' = arquivos de sincronizacao gerados sob demanda para novas assinaturas (par com allow_anonymous=false).
GO

-- Cria o Snapshot Agent da publicacao (gera o snapshot inicial das tabelas).
EXEC sp_addpublication_snapshot
     @publication             = N'Pub_ecm_jdfigueira',
     @frequency_type          = 1,               -- agenda do Snapshot Agent. 1 = sob demanda (uma vez, sem recorrencia). Ex.: 4=diario, 8=semanal.
     @publisher_security_mode = 0,               -- 0 = SQL Authentication para o Snapshot Agent conectar no publisher.
     @publisher_login         = N'repl_user',    -- login SQL usado pelo Snapshot Agent no publisher.
     @publisher_password      = N'tr3t3Ch2!PW';  -- senha do login SQL.
     -- @job_login/@job_password omitidos: o JOB roda sob a conta de servico do SQL Agent (Windows).
GO

-- Concede acesso da publicacao ao login SQL (Publication Access List - PAL).
-- Sem isso, repl_user nao consegue conectar no publisher/distributor pela replicacao.
EXEC sp_grant_publication_access
     @publication = N'Pub_ecm_jdfigueira',
     @login       = N'repl_user';
GO
```


- Conferido se existem tabelas sem chave primária. 
```USE ecm_copel_jdfigueira;
GO
SELECT s.name AS esquema, t.name AS tabela_sem_pk
FROM   sys.tables  AS t
JOIN   sys.schemas AS s ON s.schema_id = t.schema_id
WHERE  t.is_ms_shipped = 0
  AND  NOT EXISTS (SELECT 1 FROM sys.indexes i
                   WHERE i.object_id = t.object_id AND i.is_primary_key = 1)
ORDER  BY s.name, t.name;
```

Todas tem. 


- Seleciona as tabelas para publicação
```
DECLARE @pub sysname = N'Pub_ecm_jdfigueira';
DECLARE @esquema sysname, @tabela sysname, @add int = 0, @skip int = 0;

DECLARE c CURSOR LOCAL FAST_FORWARD FOR
    SELECT s.name, t.name
    FROM   sys.tables  AS t
    JOIN   sys.schemas AS s ON s.schema_id = t.schema_id
    WHERE  t.is_ms_shipped = 0
      AND  EXISTS (SELECT 1 FROM sys.indexes i
                   WHERE i.object_id = t.object_id AND i.is_primary_key = 1)  -- somente tabelas com PK.
    ORDER  BY s.name, t.name;

OPEN c;
FETCH NEXT FROM c INTO @esquema, @tabela;
WHILE @@FETCH_STATUS = 0
BEGIN
    BEGIN TRY
        EXEC sys.sp_addarticle
             @publication               = @pub,        -- publicacao onde o artigo entra.
             @article                   = @tabela,     -- nome logico do artigo (usamos o proprio nome da tabela).
             @source_owner              = @esquema,    -- schema de origem na substacao.
             @source_object             = @tabela,     -- tabela de origem.
             @type                      = N'logbased', -- 'logbased' = artigo baseado no log de transacoes (padrao transacional).
             @destination_owner         = @esquema,    -- schema de destino na central (mesmo schema). Mude para isolar por substacao.
             @destination_table         = @tabela,     -- tabela de destino na central.
             @force_invalidate_snapshot = 1;           -- 1 = permite adicionar artigo invalidando o snapshot atual (necessario ao incluir tabelas apos criar a publicacao).
        SET @add += 1;
        PRINT N'Adicionado: ' + @esquema + N'.' + @tabela;
    END TRY
    BEGIN CATCH
        SET @skip += 1;
        PRINT N'Ignorado: ' + @esquema + N'.' + @tabela + N' -> ' + ERROR_MESSAGE();
    END CATCH
    FETCH NEXT FROM c INTO @esquema, @tabela;
END
CLOSE c; DEALLOCATE c;
PRINT N'Artigos adicionados: ' + CAST(@add AS varchar(10)) + N' | Ignorados: ' + CAST(@skip AS varchar(10));
GO
```

- Conferir tabelas publicadas
```USE ecm_copel_jdfigueira;
GO
EXEC sys.sp_helparticle @publication = N'Pub_ecm_jdfigueira';
GO
```

- Confirmar o Assinador
```
USE ecm_copel_jdfigueira;
GO
EXEC sp_addsubscription
     @publication       = N'Pub_ecm_jdfigueira',
     @subscriber        = N'DISMONTFLIC\MSSQLSERVERTT',
     @destination_db    = N'ecm_copel_jdfigueira',
     @subscription_type = N'pull',
     @sync_type         = N'automatic';
GO
```


_DISMONTFLIC_

- Confere se existe a base
```
SELECT name FROM sys.databases WHERE name = N'ecm_copel_jdfigueira';
```

_FIGUEIRA_

- Startar o Snapshot para salvar o log na pasta.
```
USE ecm_copel_jdfigueira;
GO
EXEC sys.sp_startpublication_snapshot @publication = N'Pub_ecm_jdfigueira';
GO
```

- Status do Snapshot
```
USE distribution;
GO
SELECT TOP (10) [time], runstatus, comments
FROM   dbo.MSsnapshot_history
ORDER  BY [time] DESC;
GO
```

- Resultado
```
time	runstatus	comments
2026-07-28 11:30:45.390	2	[100%] A snapshot of 60 article(s) was generated.
2026-07-28 11:30:32.433	3	[99%] Locking published tables while generating the snapshot
2026-07-28 11:30:32.380	3	[99%] Inserted stored proc to disable constraint/triggers article 's_ATWQ629384_SEL2414_COPEL' during concurrent snapshot into the distribution database.
2026-07-28 11:30:32.377	3	[99%] Inserted stored proc to disable constraint/triggers article 's_ATWQ629384_QUALITROLSTB000_1' during concurrent snapshot into the distribution database.
2026-07-28 11:30:32.377	3	[99%] Inserted stored proc to disable constraint/triggers article 's_ATWQ629384_QUALITROLSTB000_2' during concurrent snapshot into the distribution database.
2026-07-28 11:30:32.377	3	[99%] Inserted stored proc to disable constraint/triggers article 's_ATWQ629384_SDG' during concurrent snapshot into the distribution database.
2026-07-28 11:30:32.373	3	[99%] Inserted stored proc to disable constraint/triggers article 's_ATWQ629384_DM1' during concurrent snapshot into the distribution database.
2026-07-28 11:30:32.373	3	[99%] Inserted stored proc to disable constraint/triggers article 's_ATWQ629384_IDM' during concurrent snapshot into the distribution database.
2026-07-28 11:30:32.373	3	[99%] Inserted stored proc to disable constraint/triggers article 's_ATWQ629384_Qualitrol_TM1' during concurrent snapshot into the distribution database.
2026-07-28 11:30:32.370	3	[99%] Inserted stored proc to disable constraint/triggers article 's_ATQM499686_QUALITROLSTB000_2' during concurrent snapshot into the distribution database.
```


_DISMONTFLIC_

- Adiciona uma assinatura Pull
```USE ecm_copel_jdfigueira;
GO
EXEC sp_addpullsubscription
     @publisher         = N'Srv-Jd-Figueira',
     @publisher_db      = N'ecm_copel_jdfigueira',
     @publication       = N'Pub_ecm_jdfigueira',
     @independent_agent = N'true',
     @subscription_type = N'pull';
GO
```


```
USE ecm_copel_jdfigueira;
GO
EXEC sp_addpullsubscription_agent
     @publisher                 = N'Srv-Jd-Figueira',
     @publisher_db              = N'ecm_copel_jdfigueira',
     @publication               = N'Pub_ecm_jdfigueira',
     @distributor               = N'Srv-Jd-Figueira',
     @job_login                 = N'.\svc_repl',
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
Msg 8145, Level 16, State 1, Procedure sp_addpullsubscription_agent, Line 0 [Batch Start Line 2]
@publisher_security_mode is not a parameter for procedure sp_addpullsubscription_agent.

Completion time: 2026-07-28T11:45:29.2330533-03:00
```

- Novo Script (removendo campo, incluindo DISMONTFLIC)
```
USE ecm_copel_jdfigueira;
GO
EXEC sp_addpullsubscription_agent
     @publisher                 = N'Srv-Jd-Figueira',
     @publisher_db              = N'ecm_copel_jdfigueira',
     @publication               = N'Pub_ecm_jdfigueira',
     @distributor               = N'Srv-Jd-Figueira',
     @job_login                 = N'DISMONTFLIC\svc_repl',
     @job_password              = N'Repl#Copel2026',
     @distributor_security_mode = 0,
     @distributor_login         = N'repl_user',
     @distributor_password      = N'tr3t3Ch2!PW',
     @frequency_type            = 64;
GO
```

- Resultado
```
Job 'Srv-Jd-Figueira-ecm_copel_jdfiguei-Pub_ecm_jdfigueira-DISMONTFLIC\MSSQLS-ecm_copel_jdfiguei-18A00271-D16A-425A-804C-F0A0B79CA0A9' started successfully.

Completion time: 2026-07-28T11:52:22.9082006-03:00

```

Erro de usuário sa
![[Pasted image 20260728115600.png|577]]

Erro no Agente
![[Pasted image 20260728120255.png|585]]
Indicação que já existe um job rodando, não sendo possível iniciar o novo. 

Analisado que o usuário tava sem acesso ao BD

```
USE master;
GO
CREATE LOGIN [DISMONTFLIC\svc_repl] FROM WINDOWS;
GO
USE ecm_copel_jdfigueira;
GO
CREATE USER [DISMONTFLIC\svc_repl] FOR LOGIN [DISMONTFLIC\svc_repl];
ALTER ROLE db_owner ADD MEMBER [DISMONTFLIC\svc_repl];
GO
```


> [!NOTE]  Resultado OK
> 
> Tabelas  Populadas. 

![[Pasted image 20260728122912.png]]

