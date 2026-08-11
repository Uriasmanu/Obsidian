/* ############################################################################
   ###                                                                      ###
   ###   RODAR NESTE SERVIDOR:   Srv-Jd-Figueira   (subestacao JD Figueira)  ###
   ###                                                                      ###
   ############################################################################ */

/* ============================================================================
   04 - HEALTH CHECK + ALERTA POR E-MAIL
   ----------------------------------------------------------------------------
   Roda na substacao (onde ficam o distribution database e o historico dos agentes).
   Entrega: tabela de historico + procedure (latencia e backlog) + job agendado
            + alerta por e-mail (Database Mail) ao passar do limite.
   Pre-requisito do alerta: Database Mail configurado na substacao com um profile.
   ============================================================================ */

USE <DBA>;   -- banco administrativo na substacao (crie um se nao tiver: CREATE DATABASE DBA;).
GO

/* 1. Tabela de historico ---------------------------------------------------- */
IF OBJECT_ID(N'dbo.repl_healthcheck_log', N'U') IS NULL
CREATE TABLE dbo.repl_healthcheck_log
(
    id              bigint IDENTITY(1,1) PRIMARY KEY,
    coleta_utc      datetime2(0)  NOT NULL,   -- momento da coleta (UTC).
    publication     sysname       NOT NULL,
    subscriber      sysname       NOT NULL,
    pending_cmds    int           NULL,       -- comandos ainda nao entregues a central (backlog).
    eta_seg         int           NULL,       -- estimativa em segundos para esvaziar a fila.
    latency_ms      int           NULL,       -- latencia de entrega recente em milissegundos.
    acima_do_limite bit           NOT NULL,   -- 1 se estourou backlog ou latencia.
    alertado        bit           NOT NULL DEFAULT 0  -- 1 se ja enviou e-mail para esta coleta.
);
GO

/* 2. Procedure de coleta + alerta ------------------------------------------- */
CREATE OR ALTER PROCEDURE dbo.usp_repl_healthcheck
    @publisher      sysname = N'Srv-Jd-Figueira',           -- publisher (substacao).
    @publisher_db   sysname = N'ecm_copel_jdfigueira',                  -- banco publicado.
    @publication    sysname = N'Pub_ecm_jdfigueira',        -- publicacao monitorada.
    @subscriber     sysname = N'DISMONTFLIC\MSSQLSERVERTT', -- subscriber (central, instancia nomeada).
    @subscriber_db  sysname = N'ecm_copel_jdfigueira',                 -- banco destino na central.
    @lat_limite_ms  int     = 60000,    -- limite de latencia em ms para disparar alerta (60s).
    @backlog_limite int     = 10000,    -- limite de comandos pendentes para disparar alerta.
    @enviar_email   bit     = 1,        -- 1 = envia e-mail ao estourar; 0 = so grava no historico.
    @mail_profile   sysname = N'<ProfileDatabaseMail>',     -- profile do Database Mail (precisa existir na substacao).
    @mail_to        nvarchar(400) = N'<dba@empresa.com.br>' -- destinatario(s) do alerta.
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @pending int, @eta int, @latency_ms int, @acima bit;

    -- BACKLOG: captura comandos pendentes (mesma proc da secao 3 do arquivo 03).
    DECLARE @bk TABLE (pendingcmdcount int, estimatedprocesstime int);
    INSERT INTO @bk
    EXEC distribution.sys.sp_replmonitorsubscriptionpendingcmds
         @publisher = @publisher, @publisher_db = @publisher_db,
         @publication = @publication, @subscriber = @subscriber,
         @subscriber_db = @subscriber_db,
         @subscription_type = 1;          -- 1 = pull.
    SELECT @pending = pendingcmdcount, @eta = estimatedprocesstime FROM @bk;

    -- LATENCIA: ultima latencia de entrega registrada pelo Distribution Agent.
    SELECT TOP (1) @latency_ms = h.current_delivery_latency   -- latencia em ms da entrega mais recente.
    FROM   distribution.dbo.MSdistribution_history AS h
    JOIN   distribution.dbo.MSdistribution_agents  AS a ON a.id = h.agent_id
    WHERE  a.publication = @publication
    ORDER  BY h.[time] DESC;

    -- Marca se passou de qualquer um dos limites.
    SET @acima = CASE WHEN ISNULL(@pending,0) > @backlog_limite
                       OR ISNULL(@latency_ms,0) > @lat_limite_ms THEN 1 ELSE 0 END;

    INSERT INTO dbo.repl_healthcheck_log
        (coleta_utc, publication, subscriber, pending_cmds, eta_seg, latency_ms, acima_do_limite)
    VALUES (SYSUTCDATETIME(), @publication, @subscriber, @pending, @eta, @latency_ms, @acima);
    DECLARE @id bigint = SCOPE_IDENTITY();

    -- Alerta por e-mail somente quando estourou o limite.
    IF @acima = 1 AND @enviar_email = 1
    BEGIN
        DECLARE @assunto nvarchar(200) = N'[REPLICACAO] Alerta: ' + @publication + N' -> ' + @subscriber;
        DECLARE @corpo nvarchar(max) =
            N'Health check acima do limite.' + CHAR(13)+CHAR(10) +
            N'Pendentes: ' + ISNULL(CAST(@pending AS nvarchar(20)),N'?') +
            N' (limite ' + CAST(@backlog_limite AS nvarchar(20)) + N')' + CHAR(13)+CHAR(10) +
            N'Latencia: ' + ISNULL(CAST(@latency_ms AS nvarchar(20)),N'?') +
            N' ms (limite ' + CAST(@lat_limite_ms AS nvarchar(20)) + N' ms)' + CHAR(13)+CHAR(10) +
            N'ETA fila: ' + ISNULL(CAST(@eta AS nvarchar(20)),N'?') + N' s';
        EXEC msdb.dbo.sp_send_dbmail
             @profile_name = @mail_profile,   -- profile de envio do Database Mail.
             @recipients   = @mail_to,        -- destinatarios separados por ponto e virgula.
             @subject      = @assunto,
             @body         = @corpo;
        UPDATE dbo.repl_healthcheck_log SET alertado = 1 WHERE id = @id;
    END

    -- Devolve a leitura atual (util para teste manual).
    SELECT pending_cmds = @pending, eta_seg = @eta, latency_ms = @latency_ms, acima_do_limite = @acima;
END
GO

-- Teste manual sem enviar e-mail:
-- EXEC dbo.usp_repl_healthcheck @enviar_email = 0;


/* 3. Job agendado (a cada 5 min) -------------------------------------------- */
USE msdb;
GO
DECLARE @jobName sysname = N'Repl_HealthCheck_Substacao_Central';
IF EXISTS (SELECT 1 FROM msdb.dbo.sysjobs WHERE name = @jobName)
    EXEC msdb.dbo.sp_delete_job @job_name = @jobName;    -- remove versao anterior do job, se houver.

EXEC msdb.dbo.sp_add_job
     @job_name    = @jobName,
     @description = N'Coleta latencia/backlog da replicacao e alerta por e-mail',
     @enabled     = 1;                       -- 1 = job habilitado.

EXEC msdb.dbo.sp_add_jobstep
     @job_name      = @jobName,
     @step_name     = N'Health check',
     @subsystem     = N'TSQL',               -- passo do tipo Transact-SQL.
     @database_name = N'<DBA>',              -- banco onde a procedure existe.
     @command       = N'EXEC dbo.usp_repl_healthcheck;',
     @retry_attempts= 1,                     -- tenta 1 vez de novo em caso de falha.
     @retry_interval= 1;                     -- intervalo de retentativa em minutos.

EXEC msdb.dbo.sp_add_schedule
     @schedule_name        = N'Repl_HealthCheck_5min',
     @freq_type            = 4,    -- 4 = diario.
     @freq_interval        = 1,    -- a cada 1 dia.
     @freq_subday_type     = 4,    -- 4 = subdivisao em minutos (1=uma vez, 8=horas).
     @freq_subday_interval = 5,    -- a cada 5 minutos.
     @active_start_time    = 0;    -- hora de inicio no formato HHMMSS (0 = 00:00:00).

EXEC msdb.dbo.sp_attach_schedule @job_name = @jobName, @schedule_name = N'Repl_HealthCheck_5min';
EXEC msdb.dbo.sp_add_jobserver   @job_name = @jobName, @server_name = N'(LOCAL)';  -- registra o job no Agent local.
GO

/* 4. Acompanhamento --------------------------------------------------------- */
USE <DBA>;
GO
SELECT TOP (50) * FROM dbo.repl_healthcheck_log ORDER BY coleta_utc DESC;
GO
