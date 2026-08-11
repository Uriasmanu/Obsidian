/* ############################################################################
   ###                                                                            ###
   ###   RODAR NESTE SERVIDOR:   C E N T R A L   (instancia DISMONTFLIC\MSSQLSERVERTT)  ###
   ###                                                                            ###
   ############################################################################ */

/* ============================================================================
   04 - CENTRAL  (Subscriber MERGE, assinatura PULL)
   BANCO 2: sigmaecm_copel_figueira -> sigmaecm  (BIDIRECIONAL)
   ----------------------------------------------------------------------------
   Rodar somente DEPOIS que o snapshot do arquivo 03 concluiu.
   Conexoes que cruzam a rede (publisher/distributor) em SQL Auth.
   O Merge Agent SEMPRE conecta no subscriber local por Windows (estrutural).
   ============================================================================ */

USE sigmaecm;   -- banco de destino na central (o que o sistema central tambem edita).
GO

/* ----------------------------------------------------------------------------
   0. PRE-REQUISITOS NA CENTRAL (AS-BUILT, descobertos na implantacao)
   ---------------------------------------------------------------------------- */

-- 0.1 Login da conta do job no SQL da central + db_owner no banco de destino.
--     Sem isso, o Merge Agent falha com erro 20084 (nao conecta no subscriber).
IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = N'DISMONTFLIC\svc_repl')
    CREATE LOGIN [DISMONTFLIC\svc_repl] FROM WINDOWS;
GO
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'DISMONTFLIC\svc_repl')
    CREATE USER [DISMONTFLIC\svc_repl] FOR LOGIN [DISMONTFLIC\svc_repl];
ALTER ROLE db_owner ADD MEMBER [DISMONTFLIC\svc_repl];
GO

-- 0.2 Database Master Key: o merge com SQL Auth criptografa os segredos de
--     replicacao usando a DMK do banco. Sem ela, aparece o warning
--     "does not contain database master key" e a conexao pode falhar.
IF NOT EXISTS (SELECT 1 FROM sys.symmetric_keys WHERE name = N'##MS_DatabaseMasterKey##')
    CREATE MASTER KEY ENCRYPTION BY PASSWORD = N'<SenhaForteDaMasterKey>';
GO

-- 0.3 Marcar a coluna Id como ROWGUIDCOL nas 7 tabelas TAMBEM na central.
--     Obrigatorio para o merge com @sync_type = 'none' (tabelas ja existem dos
--     dois lados). Na subestacao isso e feito no arquivo 03, passo 4a.
ALTER TABLE dbo.MonitoramentoRedeOnline    ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.ModuloAtivo                ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.MonitoramentoRedeHistorico ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.Usuario                    ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.AlarmeAnunciador           ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.Alarme                     ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.AlarmeAnunciadorEvento     ALTER COLUMN Id ADD ROWGUIDCOL;
GO

/* ----------------------------------------------------------------------------
   1. CRIAR A ASSINATURA MERGE PULL (com @sync_type = 'none')
      @subscriber_type = 'global' + @subscription_priority: resolucao de conflito
      por prioridade. Publisher tem prioridade 100, entao com 75 aqui a
      SUBESTACAO vence o conflito (regra: instalacao sempre vence).
      @sync_type = 'none': nao aplica snapshot, preserva o schema do EF.
   ---------------------------------------------------------------------------- */
EXEC sp_addmergepullsubscription
     @publisher            = N'Srv-Jd-Figueira',           -- publicadora (subestacao).
     @publisher_db         = N'sigmaecm_copel_figueira',   -- banco publicado na subestacao.
     @publication          = N'Pub_sigmaecm',              -- publicacao merge.
     @subscriber_type      = N'global',                    -- 'global' = assinatura de servidor com prioridade.
     @subscription_priority = 75,                          -- < 100 (publisher), entao a subestacao vence conflito.
     @sync_type            = N'none';                      -- nao aplica snapshot; tabelas ja existem dos dois lados.
GO

/* ----------------------------------------------------------------------------
   2. CRIAR O JOB DO MERGE AGENT (roda AQUI, na central)
   ---------------------------------------------------------------------------- */
EXEC sp_addmergepullsubscription_agent
     @publisher                 = N'Srv-Jd-Figueira',           -- publicadora (subestacao).
     @publisher_db              = N'sigmaecm_copel_figueira', -- banco publicado.
     @publication               = N'Pub_sigmaecm',      -- publicacao merge.
     @distributor               = N'Srv-Jd-Figueira',           -- distribuidor (local na subestacao).
     @job_login                 = N'DISMONTFLIC\svc_repl',    -- CONTA WINDOWS que roda o job na central. Use host\conta (o formato .\conta e recusado por erro de proxy). Precisa de login no SQL da central (ver bloco abaixo).
     @job_password              = N'<SenhaWindowsDaSvcRepl>',
     @publisher_security_mode   = 0,                          -- SQL Auth para conectar no PUBLISHER (o agente de MERGE aceita este parametro, diferente do transacional).
     @publisher_login           = N'repl_user',
     @publisher_password        = N'<SenhaReplUserForte>',
     @distributor_security_mode = 0,                          -- SQL Auth para conectar no DISTRIBUTOR.
     @distributor_login         = N'repl_user',
     @distributor_password      = N'<SenhaReplUserForte>',
     @frequency_type            = 64;                         -- 64 = inicia junto com o SQL Server Agent (sincronizacao continua).
GO

/* ----------------------------------------------------------------------------
   PASSO OBRIGATORIO: dar a conta do JOB acesso ao SQL DA CENTRAL
   ----------------------------------------------------------------------------
   Igual ao banco 1: o Merge Agent conecta no SUBSCRIBER (a central) por Windows
   Auth usando @job_login. Sem login no SQL da central, falha com erro 20084 e
   fica em loop de retry. Rode isto na CENTRAL (db_owner no banco de destino):
   ---------------------------------------------------------------------------- */
-- USE master;
-- GO
-- IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = N'DISMONTFLIC\svc_repl')
--     CREATE LOGIN [DISMONTFLIC\svc_repl] FROM WINDOWS;
-- GO
-- USE sigmaecm;
-- GO
-- IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'DISMONTFLIC\svc_repl')
--     CREATE USER [DISMONTFLIC\svc_repl] FOR LOGIN [DISMONTFLIC\svc_repl];
-- ALTER ROLE db_owner ADD MEMBER [DISMONTFLIC\svc_repl];
-- GO

/* ----------------------------------------------------------------------------
   NOTA SOBRE O SHARE DE SNAPSHOT (igual ao banco 1)
   A conta @job_login le \\Srv-Jd-Figueira\repldata. Sem dominio comum, use conta
   local espelhada (mesmo nome e senha nos dois servidores) ou entrega por FTP.
   ---------------------------------------------------------------------------- */

/* ----------------------------------------------------------------------------
   3. INICIAR A PRIMEIRA SINCRONIZACAO
   ---------------------------------------------------------------------------- */
USE msdb;
GO
SELECT j.job_id, j.name, j.enabled
FROM   dbo.sysjobs AS j
WHERE  j.name LIKE N'%Pub_sigmaecm%';   -- localiza o job do Merge Agent.
GO
-- EXEC dbo.sp_start_job @job_name = N'<nome_do_job_do_merge_agent>';
GO

/* ----------------------------------------------------------------------------
   4. CONFERIR A ASSINATURA MERGE
   ---------------------------------------------------------------------------- */
USE sigmaecm;
GO
EXEC sp_helpmergepullsubscription
     @publisher    = N'Srv-Jd-Figueira',
     @publisher_db = N'sigmaecm_copel_figueira',
     @publication  = N'Pub_sigmaecm';
GO
