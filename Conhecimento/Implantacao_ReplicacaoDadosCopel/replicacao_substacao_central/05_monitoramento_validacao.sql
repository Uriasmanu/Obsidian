/* ############################################################################
   ###                                                                      ###
   ###   SCRIPT MISTO:  cada secao indica RODAR EM Srv-Jd-Figueira ou CENTRAL        ###
   ###   Leia o "RODAR EM:" no inicio de cada bloco antes de executar       ###
   ###                                                                      ###
   ############################################################################ */

/* ============================================================================
   03 - MONITORAMENTO E VALIDACAO
   ----------------------------------------------------------------------------
   No modelo PULL os agentes ficam distribuidos:
       Log Reader Agent   -> Srv-Jd-Figueira  (distributor local)
       Snapshot Agent     -> Srv-Jd-Figueira  (distributor local)
       Distribution Agent -> CENTRAL (subscriber)
   ============================================================================ */


/* ----------------------------------------------------------------------------
   1. STATUS GERAL    RODAR EM: Srv-Jd-Figueira (distribution database)
   ---------------------------------------------------------------------------- */
USE distribution;
GO
EXEC sys.sp_replmonitorhelppublisher;            -- visao geral do publisher (status consolidado).
GO
EXEC sys.sp_replmonitorhelppublication
     @publisher = N'Srv-Jd-Figueira';            -- lista publicacoes e status para este publisher.
GO
EXEC sys.sp_replmonitorhelpsubscription
     @publisher        = N'Srv-Jd-Figueira',     -- publisher a consultar.
     @publisher_db     = N'ecm_copel_jdfigueira',            -- banco publicado.
     @publication      = N'Pub_ecm_jdfigueira',  -- publicacao.
     @publication_type = 0;                      -- tipo: 0 = transacional, 1 = snapshot, 2 = merge.
GO


/* ----------------------------------------------------------------------------
   2. LATENCIA FIM A FIM (TRACER TOKEN)   RODAR EM: Srv-Jd-Figueira (banco publicado)
   ---------------------------------------------------------------------------- */
USE ecm_copel_jdfigueira;
GO
-- 2.1 Posta um token; ele viaja Publisher -> Distributor -> Subscriber.
DECLARE @tokenId int;
EXEC sys.sp_posttracertoken
     @publication     = N'Pub_ecm_jdfigueira',   -- publicacao onde o token e inserido.
     @tracer_token_id = @tokenId OUTPUT;         -- retorna o id do token postado (anote).
SELECT @tokenId AS tracer_id_postado;
GO
-- 2.2 Lista tokens recentes (caso precise do id)
EXEC sys.sp_helptracertokens
     @publication = N'Pub_ecm_jdfigueira';
GO
-- 2.3 Tempo de cada salto. Troque <tracer_id> pelo id acima.
--     latency_p2d = Publisher -> Distributor | latency_d2s = Distributor -> Subscriber | overall = total
EXEC sys.sp_helptracertokenhistory
     @publication = N'Pub_ecm_jdfigueira',
     @tracer_id   = <tracer_id>;                 -- id do token retornado em 2.1/2.2.
GO


/* ----------------------------------------------------------------------------
   3. BACKLOG: COMANDOS PENDENTES   RODAR EM: Srv-Jd-Figueira (distribution database)
   ---------------------------------------------------------------------------- */
USE distribution;
GO
EXEC sys.sp_replmonitorsubscriptionpendingcmds
     @publisher         = N'Srv-Jd-Figueira',          -- publisher.
     @publisher_db      = N'ecm_copel_jdfigueira',                 -- banco publicado.
     @publication       = N'Pub_ecm_jdfigueira',       -- publicacao.
     @subscriber        = N'DISMONTFLIC\MSSQLSERVERTT',-- subscriber (central, instancia nomeada).
     @subscriber_db     = N'ecm_copel_jdfigueira',                -- banco destino na central.
     @subscription_type = 1;                           -- 0 = push, 1 = pull. Retorna pendingcmdcount e estimatedprocesstime.
GO


/* ----------------------------------------------------------------------------
   4. HISTORICO E ERROS   RODAR EM: Srv-Jd-Figueira (distribution database)
   ---------------------------------------------------------------------------- */
USE distribution;
GO
-- runstatus: 1=inicio 2=sucesso 3=em progresso 4=ocioso 5=tentando de novo 6=falha
SELECT TOP (20) [time], runstatus, delivered_transactions, delivered_commands, duration, comments
FROM   dbo.MSlogreader_history    ORDER BY [time] DESC;   -- execucoes do Log Reader (le o log da substacao).
GO
SELECT TOP (20) [time], runstatus, delivered_transactions, delivered_commands, current_delivery_rate, duration, comments
FROM   dbo.MSdistribution_history ORDER BY [time] DESC;   -- execucoes do Distribution Agent (entrega ate a central).
GO
SELECT TOP (50) [time], error_code, error_text
FROM   dbo.MSrepl_errors          ORDER BY [time] DESC;   -- erros recentes de replicacao (mensagem completa).
GO


/* ----------------------------------------------------------------------------
   5. STATUS DO AGENTE NA CENTRAL   RODAR EM: CENTRAL
   ---------------------------------------------------------------------------- */
USE msdb;
GO
-- last_run_outcome: 0=falhou 1=sucesso 3=cancelado 5=desconhecido
SELECT j.name AS job_agente, j.enabled, a.last_run_outcome, a.last_run_date, a.last_outcome_message
FROM   dbo.sysjobs AS j
JOIN   dbo.sysjobservers AS a ON a.job_id = j.job_id
WHERE  j.category_id IN (SELECT category_id FROM dbo.syscategories WHERE name LIKE N'REPL-%');  -- categorias de jobs de replicacao.
GO


/* ----------------------------------------------------------------------------
   6. VALIDACAO DE DADOS: CONTAGEM DE TODAS AS TABELAS
      Rode na Srv-Jd-Figueira (ecm_copel_jdfigueira) e na CENTRAL (ecm_copel_jdfigueira) e compare.
      Com o backlog (secao 3) zerado, as contagens devem bater.
   ---------------------------------------------------------------------------- */
-- RODAR EM: Srv-Jd-Figueira (depois troque USE para ecm_copel_jdfigueira e rode na central)
USE ecm_copel_jdfigueira;
GO
SELECT  s.name AS esquema,
        t.name AS tabela,
        SUM(p.rows) AS linhas
FROM    sys.tables AS t
JOIN    sys.schemas AS s    ON s.schema_id = t.schema_id
JOIN    sys.partitions AS p ON p.object_id = t.object_id
                           AND p.index_id IN (0,1)   -- 0 = heap, 1 = indice clustered. Pega a contagem de linhas da tabela.
WHERE   t.is_ms_shipped = 0
GROUP BY s.name, t.name
ORDER BY s.name, t.name;
GO


/* ----------------------------------------------------------------------------
   7. (OPCIONAL) VALIDACAO PROFUNDA COM tablediff (linha de comando)
      Compara linha a linha e pode gerar script de correcao. Rode da central.
        tablediff -sourceserver Srv-Jd-Figueira -sourcedatabase ecm_copel_jdfigueira -sourcetable <Tab>
                  -destinationserver DISMONTFLIC\MSSQLSERVERTT -destinationdatabase ecm_copel_jdfigueira -destinationtable <Tab>
                  -f C:\repl_check\diff_<Tab>.sql
      -sourceserver/-sourcetable = origem (substacao) | -destinationserver/-destinationtable = destino (central)
      -f = caminho do .sql de correcao gerado quando ha diferenca.
   ---------------------------------------------------------------------------- */


/* ============================================================================
   MONITORAMENTO DO BANCO 2 (MERGE)  -  Pub_sigmaecm_copel
   ============================================================================ */

/* ----------------------------------------------------------------------------
   M1. STATUS DA ASSINATURA MERGE   RODAR EM: Srv-Jd-Figueira (distribution db)
   ---------------------------------------------------------------------------- */
USE distribution;
GO
EXEC sys.sp_replmonitorhelpmergesubscription
     @publisher    = N'Srv-Jd-Figueira',
     @publisher_db = N'sigmaecm_copel_figueira',
     @publication  = N'Pub_sigmaecm_copel';
GO

/* ----------------------------------------------------------------------------
   M2. RESUMO DA PUBLICACAO MERGE   RODAR EM: Srv-Jd-Figueira (banco publicado)
   ---------------------------------------------------------------------------- */
USE sigmaecm_copel_figueira;
GO
EXEC sp_helpmergepublication @publication = N'Pub_sigmaecm_copel';
GO

/* ----------------------------------------------------------------------------
   M3. HISTORICO DO MERGE AGENT   RODAR EM: Srv-Jd-Figueira (distribution db)
   ---------------------------------------------------------------------------- */
USE distribution;
GO
SELECT TOP (20) [time], runstatus, duration, comments
FROM   dbo.MSmerge_history
ORDER  BY [time] DESC;
GO

/* ----------------------------------------------------------------------------
   M4. CONFLITOS DE MERGE   RODAR EM: Srv-Jd-Figueira (banco publicado)
        Lista conflitos por artigo. Troque <Tabela> pelo nome da tabela.
   ---------------------------------------------------------------------------- */
USE sigmaecm_copel_figueira;
GO
-- Lista as tabelas de conflito existentes
SELECT * FROM dbo.MSmerge_conflicts_info;
GO
-- Linhas em conflito de um artigo especifico (vencedor x perdedor)
-- EXEC sp_helpmergeconflictrows @publication = N'Pub_sigmaecm_copel', @source_object = N'<Tabela>';
GO

/* ----------------------------------------------------------------------------
   M5. VALIDACAO DE DADOS (tabelas especificas do merge)
        Compare contagem na subestacao e na central. Em merge a igualdade e
        eventual (apos a sincronizacao), nao instantanea.
   ---------------------------------------------------------------------------- */
-- RODAR EM: Srv-Jd-Figueira  ->  USE sigmaecm_copel_figueira;
-- RODAR EM: CENTRAL        ->  USE sigmaecm_copel;
-- SELECT COUNT(*) FROM dbo.<Tabela>;
GO
