/* ############################################################################
   ###                                                                      ###
   ###   RODAR NESTE SERVIDOR:   Srv-Novo-Mundo   (subestacao JD Figueira)  ###
   ###                                                                      ###
   ############################################################################ */

/* ============================================================================
   01 - Srv-Novo-Mundo  (Publisher + Distributor local)
   REPLICACAO TRANSACIONAL PULL DE TODAS AS TABELAS  (Srv-Novo-Mundo -> CENTRAL)
   ----------------------------------------------------------------------------
   Execute as secoes 1 a 6 em ordem.
   Conexao: somente Central -> Substacao. A substacao nunca disca na central.
   AJUSTE os valores entre <...> e os nomes de banco/publicacao/login.
   ============================================================================ */


/* ----------------------------------------------------------------------------
   0. LOGIN SQL DE REPLICACAO  (SQL AUTHENTICATION)
      Criado na Srv-Novo-Mundo. E este login que:
        - a central usa para conectar no publisher e no distributor (pull); e
        - os agentes locais (Log Reader e Snapshot) usam para conectar no publisher.
      So precisa existir na Srv-Novo-Mundo. Use a mesma senha no arquivo 02.
   ---------------------------------------------------------------------------- */
USE master;
GO
IF NOT EXISTS (SELECT 1 FROM sys.sql_logins WHERE name = N'repl_user')
    CREATE LOGIN repl_user WITH PASSWORD = N'<SenhaReplUserForte>', CHECK_POLICY = ON;
GO
-- Da acesso ao banco publicado (necessario para os agentes e para o snapshot).
USE ecm_copel_novo_mundo;
GO
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'repl_user')
    CREATE USER repl_user FOR LOGIN repl_user;
ALTER ROLE db_owner ADD MEMBER repl_user;
GO


/* ----------------------------------------------------------------------------
   1. DISTRIBUTOR LOCAL NA Srv-Novo-Mundo
   ---------------------------------------------------------------------------- */
USE master;
GO
EXEC sp_adddistributor
     @distributor = N'Srv-Novo-Mundo',          -- instancia que sera o Distributor. Deve ser igual a SELECT @@SERVERNAME da substacao.
     @password    = N'Repl#Copel2026';  -- senha da conta interna 'distributor_admin' usada na comunicacao com o distribuidor.
GO

EXEC sp_adddistributiondb
     @database      = N'distribution',           -- nome do banco de distribuicao (convencao: 'distribution'). Guarda os comandos a entregar.
     @security_mode = 0,                         -- 0 = SQL Authentication.
     @login         = N'repl_user',              -- login SQL usado nessa conexao.
     @password      = N'Repl#Copel2026';   -- senha do login SQL.
GO

-- Registra a substacao como Publisher atendido pelo distribuidor local.
EXEC sp_adddistpublisher
     @publisher         = N'Srv-Novo-Mundo',    -- instancia publicadora (a propria substacao).
     @distribution_db   = N'distribution',       -- banco de distribuicao que atende este publisher.
     @security_mode     = 0,                     -- 0 = SQL Authentication na ligacao Publisher <-> Distributor.
     @login             = N'repl_user',          -- login SQL usado nessa conexao.
     @password          = N'Repl#Copel2026',  -- senha do login SQL.
     @working_directory = N'\\Srv-Novo-Mundo\repldata';  -- PASTA DE SNAPSHOT (UNC). E daqui que a central (pull) LE o snapshot. Precisa dar leitura para a conta do agente da central.
GO


/* ----------------------------------------------------------------------------
   2. HABILITAR O BANCO DA Srv-Novo-Mundo PARA PUBLICACAO
   ---------------------------------------------------------------------------- */
USE master;
GO
EXEC sp_replicationdboption
     @dbname  = N'ecm_copel_novo_mundo',                     -- banco de origem que sera publicado.
     @optname = N'publish',                      -- opcao 'publish' liga a capacidade de publicacao transacional/snapshot neste banco.
     @value   = N'true';                         -- 'true' liga, 'false' desliga.
GO

-- Cria o Log Reader Agent JA com SQL Authentication para conectar no publisher.
-- IMPORTANTE: rode isto ANTES do sp_addpublication. Se a publicacao for criada
-- primeiro, o Log Reader e criado em Windows Auth por padrao.
USE ecm_copel_novo_mundo;
GO
EXEC sp_addlogreader_agent
     @publisher_security_mode = 0,               -- 0 = SQL Authentication para conectar no publisher (a substacao).
     @publisher_login         = N'repl_user',    -- login SQL usado pelo Log Reader no publisher.
     @publisher_password      = N'Repl#Copel2026';  -- senha do login SQL.
     -- @job_login/@job_password omitidos de proposito: o JOB roda sob a conta de
     -- servico do SQL Server Agent (Windows). Isso e estrutural, nao vira SQL Auth.
GO


/* ----------------------------------------------------------------------------
   3. CRIAR A PUBLICACAO TRANSACIONAL  (PULL habilitado, PUSH bloqueado)
   ---------------------------------------------------------------------------- */
USE ecm_copel_novo_mundo;
GO
EXEC sp_addpublication
     @publication       = N'Pub_ecm_novo_mundo', -- nome da publicacao (identificador deste conjunto de artigos).
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
     @publication             = N'Pub_ecm_novo_mundo',
     @frequency_type          = 1,               -- agenda do Snapshot Agent. 1 = sob demanda (uma vez, sem recorrencia). Ex.: 4=diario, 8=semanal.
     @publisher_security_mode = 0,               -- 0 = SQL Authentication para o Snapshot Agent conectar no publisher.
     @publisher_login         = N'repl_user',    -- login SQL usado pelo Snapshot Agent no publisher.
     @publisher_password      = N'Repl#Copel2026';  -- senha do login SQL.
     -- @job_login/@job_password omitidos: o JOB roda sob a conta de servico do SQL Agent (Windows).
GO

-- Concede acesso da publicacao ao login SQL (Publication Access List - PAL).
-- Sem isso, repl_user nao consegue conectar no publisher/distributor pela replicacao.
EXEC sp_grant_publication_access
     @publication = N'Pub_ecm_novo_mundo',
     @login       = N'repl_user';
GO


/* ----------------------------------------------------------------------------
   4. PUBLICAR TODAS AS TABELAS
   ---------------------------------------------------------------------------- */

-- 4.1 DIAGNOSTICO: tabelas SEM chave primaria (ficam de fora do transacional)
--     O transacional EXIGE PK em toda tabela publicada. Estas nao podem entrar.
SELECT s.name AS esquema, t.name AS tabela_sem_pk
FROM   sys.tables  AS t
JOIN   sys.schemas AS s ON s.schema_id = t.schema_id
WHERE  t.is_ms_shipped = 0                       -- ignora tabelas de sistema.
  AND  NOT EXISTS (SELECT 1 FROM sys.indexes i
                   WHERE i.object_id = t.object_id AND i.is_primary_key = 1)  -- sem indice de PK.
ORDER  BY s.name, t.name;
GO

-- 4.2 Adiciona como artigo cada tabela COM PK ainda nao publicada.
--     Seguro para repetir: o TRY/CATCH ignora as ja existentes e adiciona so as novas.
DECLARE @pub sysname = N'Pub_ecm_novo_mundo';
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

-- 4.3 Conferir os artigos publicados
EXEC sys.sp_helparticle @publication = N'Pub_ecm_novo_mundo';
GO


/* ----------------------------------------------------------------------------
   5. REGISTRAR A ASSINATURA PULL NO PUBLISHER
      Informa ao publisher que existe um subscriber pull (a central).
   ---------------------------------------------------------------------------- */
USE ecm_copel_novo_mundo;
GO
EXEC sp_addsubscription
     @publication       = N'Pub_ecm_novo_mundo',          -- publicacao assinada.
     @subscriber        = N'DISMONTFLIC\MSSQLSERVERTT',   -- instancia assinante (central, instancia nomeada host\instancia).
     @destination_db    = N'ecm_copel_novo_mundo',                   -- banco de destino na central que recebe os dados.
     @subscription_type = N'pull',                        -- 'pull' = o Distribution Agent roda no subscriber (central puxa).
     @sync_type         = N'automatic';                   -- 'automatic' = inicializa a assinatura automaticamente a partir do snapshot.
GO


/* ----------------------------------------------------------------------------
   6. GERAR O SNAPSHOT INICIAL
      Dispara o Snapshot Agent agora. Acompanhe ate concluir antes do arquivo 02.
   ---------------------------------------------------------------------------- */
EXEC sys.sp_startpublication_snapshot
     @publication = N'Pub_ecm_novo_mundo';   -- inicia imediatamente o Snapshot Agent desta publicacao.
GO

-- Acompanhar o snapshot (rode de novo ate ver runstatus de conclusao).
-- runstatus: 1=inicio 2=sucesso 3=em progresso 4=ocioso 5=tentando de novo 6=falha
USE distribution;
GO
SELECT TOP (10) [time], runstatus, comments
FROM   dbo.MSsnapshot_history
ORDER  BY [time] DESC;
GO
