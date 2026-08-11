/* ############################################################################
   ###                                                                            ###
   ###   RODAR NESTE SERVIDOR:   C E N T R A L   (instancia DISMONTFLIC\MSSQLSERVERTT)  ###
   ###                                                                            ###
   ############################################################################ */

/* ============================================================================
   02 - CENTRAL  (Subscriber, assinatura PULL)
   ----------------------------------------------------------------------------
   Rodar somente DEPOIS que o snapshot inicial na substacao concluiu.
   Todas as conexoes daqui apontam para a Srv-Novo-Mundo (Central -> Substacao).
   ============================================================================ */

USE ecm_copel_novo_mundo;   -- banco de destino na central. O contexto deve ser o banco assinante.
GO

/* ----------------------------------------------------------------------------
   1. CRIAR A ASSINATURA PULL (aponta para o publisher na substacao)
   ---------------------------------------------------------------------------- */
EXEC sp_addpullsubscription
     @publisher         = N'Srv-Novo-Mundo',    -- instancia publicadora (substacao) de onde puxar.
     @publisher_db      = N'ecm_copel_novo_mundo',           -- banco publicado na substacao.
     @publication       = N'Pub_ecm_novo_mundo', -- publicacao a assinar.
     @independent_agent = N'true',               -- deve casar com a publicacao (criada com independent_agent=true).
     @subscription_type = N'pull';               -- 'pull' = o agente roda aqui na central.
GO

/* ----------------------------------------------------------------------------
   2. CRIAR O JOB DO DISTRIBUTION AGENT (roda AQUI, na central)
      E este agente que conecta na substacao, busca os comandos e aplica na central.

      >>> IMPORTANTE (validado em producao na JD Figueira, SQL 2022): <<<
      Nesta versao do SQL Server, sp_addpullsubscription_agent NAO aceita
      @publisher_security_mode, @publisher_login nem @publisher_password.
      Passar qualquer um deles da erro 8145. Use so os do distribuidor.
      A conexao do agente com o PUBLISHER e derivada da assinatura.
   ---------------------------------------------------------------------------- */
EXEC sp_addpullsubscription_agent
     @publisher                 = N'Srv-Novo-Mundo',          -- instancia publicadora (substacao).
     @publisher_db              = N'ecm_copel_novo_mundo',     -- banco publicado na substacao.
     @publication               = N'Pub_ecm_novo_mundo',       -- publicacao assinada.
     @distributor               = N'Srv-Novo-Mundo',          -- instancia distribuidora (fica na substacao).
     @job_login                 = N'DISMONTFLIC\svc_repl',     -- CONTA WINDOWS que roda o job na central. Use host\conta (o formato .\conta foi RECUSADO com erro de proxy). Deve ter login no SQL da central (ver bloco de permissao abaixo).
     @job_password              = N'Repl#Copel2026',  -- senha dessa conta Windows.
     @distributor_security_mode = 0,                           -- SQL Auth para conectar no DISTRIBUTOR.
     @distributor_login         = N'repl_user',                -- login SQL no distributor (na substacao).
     @distributor_password      = N'Repl#Copel2026',     -- senha do repl_user (definida no arquivo 01).
     @frequency_type            = 64;                          -- 64 = inicia junto com o SQL Server Agent (continuo).
GO

/* ----------------------------------------------------------------------------
   PASSO OBRIGATORIO: dar a conta do JOB acesso ao SQL DA CENTRAL
   ----------------------------------------------------------------------------
   O Distribution Agent conecta no SUBSCRIBER (a propria central) por Windows
   Authentication usando a conta @job_login. Sem login no SQL da central, o
   agente falha com "Agent message code 20084. The process could not connect to
   Subscriber" e fica em loop de retry (snapshot nunca e aplicado).
   Rode isto na CENTRAL:
   ---------------------------------------------------------------------------- */
-- USE master;
-- GO
-- CREATE LOGIN [DISMONTFLIC\svc_repl] FROM WINDOWS;
-- GO
-- USE ecm_copel_novo_mundo;
-- GO
-- CREATE USER [DISMONTFLIC\svc_repl] FOR LOGIN [DISMONTFLIC\svc_repl];
-- ALTER ROLE db_owner ADD MEMBER [DISMONTFLIC\svc_repl];
-- GO

/* ----------------------------------------------------------------------------
   NOTA SOBRE O SHARE DE SNAPSHOT (o que SQL Auth NAO resolve)
   ----------------------------------------------------------------------------
   As conexoes SQL usam repl_user (SQL Auth). Mas ler o snapshot em
   \\Srv-Novo-Mundo\repldata e uma operacao de arquivo do Windows, feita pela
   conta @job_login. Sem dominio comum entre substacao e central, escolha uma:
     A) Conta local espelhada: crie a MESMA conta Windows (mesmo nome e senha)
        na central (para rodar o job) e na substacao (com leitura no share).
        O Windows faz pass-through e o acesso ao share funciona.
     B) Entregar o snapshot por FTP em vez de UNC: configure a publicacao com os
        parametros @ftp_address/@ftp_port/@ftp_login/@ftp_password e o agente com
        @use_ftp = 1. Assim o snapshot vai por credencial, sem share Windows.
   ---------------------------------------------------------------------------- */

/* ----------------------------------------------------------------------------
   3. INICIAR A PRIMEIRA SINCRONIZACAO
      Com agente continuo (frequency_type=64) ele sobe junto com o SQL Agent.
      Para forcar agora, localize o job e inicie.
   ---------------------------------------------------------------------------- */
USE msdb;
GO
-- Lista o(s) job(s) do Distribution Agent desta assinatura
SELECT j.job_id, j.name, j.enabled
FROM   dbo.sysjobs AS j
WHERE  j.name LIKE N'%Pub_ecm_novo_mundo%';     -- filtra pelo nome da publicacao presente no nome do job.
GO

-- Iniciar manualmente (troque pelo nome retornado acima)
-- EXEC dbo.sp_start_job @job_name = N'<nome_do_job_do_distribution_agent>';
GO

/* ----------------------------------------------------------------------------
   4. CONFERIR A ASSINATURA PULL
   ---------------------------------------------------------------------------- */
USE ecm_copel_novo_mundo;
GO
EXEC sys.sp_helppullsubscription
     @publisher    = N'Srv-Novo-Mundo',         -- filtra a assinatura por publisher.
     @publisher_db = N'ecm_copel_novo_mundo',                -- filtra por banco publicado.
     @publication  = N'Pub_ecm_novo_mundo';      -- filtra pela publicacao.
GO
