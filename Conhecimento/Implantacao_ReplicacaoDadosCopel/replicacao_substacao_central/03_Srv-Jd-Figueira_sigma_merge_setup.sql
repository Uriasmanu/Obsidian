/* ############################################################################
   ###                                                                      ###
   ###   RODAR NESTE SERVIDOR:   Srv-Jd-Figueira   (subestacao JD Figueira)   ###
   ###                                                                      ###
   ############################################################################ */

/* ============================================================================
   03 - Srv-Jd-Figueira  (Publisher MERGE)
   BANCO 2: sigmaecm_copel_figueira -> sigmaecm  (BIDIRECIONAL)
   ----------------------------------------------------------------------------
   Merge replication: os dois lados (subestacao e central) editam as MESMAS
   tabelas, e o merge reconcilia. So tabelas ESPECIFICAS sao publicadas.

   DEPENDE DO ARQUIVO 01: o distribuidor local e o login SQL repl_user ja
   devem existir (foram criados la). Este arquivo NAO refaz o distribuidor.

   Conexao: somente Central -> Srv-Jd-Figueira (mesma regra de firewall do banco 1).

   >>> LEIA OS 3 AVISOS NO FINAL DO ARQUIVO ANTES DE EXECUTAR EM PRODUCAO. <<<
   ============================================================================ */


/* ----------------------------------------------------------------------------
   1. ACESSO DO LOGIN SQL AO BANCO DE ORIGEM
   ---------------------------------------------------------------------------- */
USE sigmaecm_copel_figueira;
GO
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'repl_user')
    CREATE USER repl_user FOR LOGIN repl_user;
ALTER ROLE db_owner ADD MEMBER repl_user;
GO


/* ----------------------------------------------------------------------------
   2. HABILITAR O BANCO PARA PUBLICACAO MERGE
   ---------------------------------------------------------------------------- */
USE master;
GO
EXEC sp_replicationdboption
     @dbname  = N'sigmaecm_copel_figueira',      -- banco de origem na subestacao.
     @optname = N'merge publish',                -- 'merge publish' habilita replicacao por mesclagem (diferente de 'publish' do transacional).
     @value   = N'true';
GO


/* ----------------------------------------------------------------------------
   3. CRIAR A PUBLICACAO MERGE
   ---------------------------------------------------------------------------- */
USE sigmaecm_copel_figueira;
GO
EXEC sp_addmergepublication
     @publication           = N'Pub_sigmaecm',  -- nome da publicacao merge.
     @description           = N'Merge bidirecional de tabelas especificas: Srv-Jd-Figueira <-> Central',
     @sync_mode             = N'native',         -- 'native' = BCP nativo no snapshot (mais rapido). 'character' para destinos heterogeneos.
     @retention             = 14,                -- dias que os metadados de mudanca/conflito sao mantidos. Subscriber que ficar offline mais que isso precisa reinicializar.
     @allow_push            = N'false',          -- 'false' = sem assinatura push (a subestacao nunca empurra para a central).
     @allow_pull            = N'true',           -- 'true' = permite pull (a central puxa). Respeita o firewall.
     @allow_anonymous       = N'false',          -- 'false' = assinaturas nomeadas (necessario para prioridade de conflito).
     @centralized_conflicts = N'true',           -- 'true' = conflitos registrados de forma centralizada (no publisher), facil de auditar.
     @conflict_logging      = N'both',           -- registra a versao vencedora e a perdedora do conflito.
     @dynamic_filters       = N'false';          -- sem filtro dinamico por assinante (todas as assinaturas recebem o mesmo conjunto).
GO

-- Snapshot Agent da publicacao merge (mesma proc do transacional), em SQL Auth.
EXEC sp_addpublication_snapshot
     @publication             = N'Pub_sigmaecm',
     @frequency_type          = 1,               -- 1 = sob demanda.
     @publisher_security_mode = 0,               -- 0 = SQL Authentication para o Snapshot Agent conectar no publisher.
     @publisher_login         = N'repl_user',
     @publisher_password      = N'<SenhaReplUserForte>';
GO

-- Concede acesso da publicacao ao login SQL (PAL).
EXEC sp_grant_publication_access
     @publication = N'Pub_sigmaecm',
     @login       = N'repl_user';
GO


/* ----------------------------------------------------------------------------
   4a. USAR A COLUNA Id EXISTENTE COMO ROWGUIDCOL (evita a coluna rowguid nova)
       As tabelas ja tem uma coluna Id do tipo uniqueidentifier. Marcando-a como
       ROWGUIDCOL, o merge REUTILIZA o Id e NAO cria a coluna rowguid.
       E so um atributo de metadados: nao altera dados nem recria a tabela.
       (Os triggers de rastreamento do merge continuam sendo criados; so a
        coluna extra e evitada.)
       Se em alguma tabela a coluna GUID nao se chamar 'Id', ajuste o nome.
   ---------------------------------------------------------------------------- */
USE sigmaecm_copel_figueira;
GO
ALTER TABLE dbo.MonitoramentoRedeOnline    ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.ModuloAtivo                ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.MonitoramentoRedeHistorico ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.Usuario                    ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.AlarmeAnunciador           ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.Alarme                     ALTER COLUMN Id ADD ROWGUIDCOL;
ALTER TABLE dbo.AlarmeAnunciadorEvento     ALTER COLUMN Id ADD ROWGUIDCOL;
GO

/* ----------------------------------------------------------------------------
   4b. ADICIONAR AS TABELAS ESPECIFICAS
      Lista inicial (7 tabelas). Podem ser adicionadas outras depois, repetindo
      o sp_addmergearticle e regerando o snapshot.
      @column_tracking = 'true' detecta conflito por coluna: se a subestacao
      altera a coluna A e a central a coluna B na mesma linha, NAO ha conflito.
      Como o Id ja e ROWGUIDCOL (passo 4a), o merge reutiliza o Id.
   ---------------------------------------------------------------------------- */
DECLARE @tabelas TABLE (nome sysname);
INSERT INTO @tabelas (nome) VALUES
    (N'MonitoramentoRedeOnline'),
    (N'ModuloAtivo'),
    (N'MonitoramentoRedeHistorico'),
    (N'Usuario'),
    (N'AlarmeAnunciador'),
    (N'Alarme'),
    (N'AlarmeAnunciadorEvento');

DECLARE @t sysname, @add int = 0, @skip int = 0;
DECLARE cur CURSOR LOCAL FAST_FORWARD FOR SELECT nome FROM @tabelas;
OPEN cur;
FETCH NEXT FROM cur INTO @t;
WHILE @@FETCH_STATUS = 0
BEGIN
    BEGIN TRY
        EXEC sp_addmergearticle
             @publication     = N'Pub_sigmaecm',
             @article         = @t,
             @source_owner    = N'dbo',
             @source_object   = @t,
             @type            = N'table',
             @column_tracking = N'true';
        SET @add += 1;  PRINT N'Adicionado: dbo.' + @t;
    END TRY
    BEGIN CATCH
        SET @skip += 1; PRINT N'Ignorado: dbo.' + @t + N' -> ' + ERROR_MESSAGE();
    END CATCH
    FETCH NEXT FROM cur INTO @t;
END
CLOSE cur; DEALLOCATE cur;
PRINT N'Artigos merge adicionados: ' + CAST(@add AS varchar(10)) + N' | Ignorados: ' + CAST(@skip AS varchar(10));
GO

-- Conferir os artigos adicionados (deve listar as 7 tabelas)
EXEC sp_helpmergearticle @publication = N'Pub_sigmaecm';
GO


/* ----------------------------------------------------------------------------
   5. REGISTRAR A ASSINATURA PULL (no publisher)
   ---------------------------------------------------------------------------- */
EXEC sp_addmergesubscription
     @publication       = N'Pub_sigmaecm',
     @subscriber        = N'DISMONTFLIC\MSSQLSERVERTT',  -- instancia da central (nomeada).
     @subscriber_db     = N'sigmaecm',             -- banco de destino na central.
     @subscription_type = N'pull',                       -- 'pull' = o Merge Agent roda na central.
     @sync_type         = N'none';                       -- 'none' = NAO aplica snapshot (nao derruba/recria tabelas). Preserva o schema do EF na central. Ver AVISO 2.
GO


/* ----------------------------------------------------------------------------
   6. GERAR O SNAPSHOT INICIAL
   ---------------------------------------------------------------------------- */
EXEC sys.sp_startpublication_snapshot @publication = N'Pub_sigmaecm';
GO
-- Acompanhar (rode de novo ate concluir)
USE distribution;
GO
SELECT TOP (10) [time], runstatus, comments FROM dbo.MSsnapshot_history ORDER BY [time] DESC;
GO


/* ============================================================================
   AVISOS IMPORTANTES (LER ANTES DE PRODUCAO)
   ----------------------------------------------------------------------------
   AVISO 1 - MUDANCA DE SCHEMA:
     O merge exige uma coluna uniqueidentifier ROWGUIDCOL. Como as tabelas ja
     tem a coluna Id (uniqueidentifier), o passo 4a a marca como ROWGUIDCOL e o
     merge REUTILIZA o Id, sem criar coluna rowguid nova. Os triggers de
     rastreamento do merge ainda sao criados (inerentes ao merge) e tem algum
     custo em escrita. Teste o impacto antes.

   AVISO 2 - SCHEMA CONTROLADO POR EF MIGRATIONS (decisao AS-BUILT):
     O banco sigmaecm na central tem as tabelas criadas por EF Migrations, com
     muitas foreign keys (dezenas de tabelas referenciam ModuloAtivo e Usuario).
     Por isso usamos @sync_type = 'none': o merge NAO derruba nem recria tabelas,
     apenas passa a rastrear mudancas. Pre-requisitos do 'none':
       - As 7 tabelas existem nos DOIS lados com schema identico (garantido pelo EF).
       - A coluna Id marcada como ROWGUIDCOL nos DOIS lados (passo 4a aqui na
         subestacao; na central o mesmo ALTER e feito no arquivo 04).
       - Dados antigos NAO descem sozinhos; so o que mudar apos ativar a assinatura.
         Para forcar carga de dados existentes, faca UPDATE tabela SET col=col.

   AVISO 3 - QUEM VENCE O CONFLITO:
     A assinatura e 'global' com prioridade (definida no arquivo 04). O Publisher
     (Srv-Jd-Figueira) tem prioridade implicita 100, entao por padrao a SUBESTACAO
     vence o conflito. Se a regra do negocio for que a CENTRAL vença, use um
     resolver por artigo no sp_addmergearticle (parametro @article_resolver).
     Liste os resolvers disponiveis com: EXEC sp_enumcustomresolvers;
   ============================================================================ */
