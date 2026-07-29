# Documentação Unificada — Replicação de Banco de dados: Subestação para Central (COPEL)

Documento as-built. Descreve o procedimento efetivamente executado e validado na subestação JD Figueira, incluindo os problemas encontrados e como cada um foi resolvido. Serve de referência para operar a Figueira e para plugar as próximas instalações (Novo Mundo e demais).

---

## 1. Visão geral

A central consolida dados de várias instalações. Cada instalação tem dois bancos, e cada um usa uma estratégia diferente de replicação. Em ambos o modelo é **pull**: a central puxa, e a instalação (subestação) nunca abre conexão com a central.

### 1.1 Os dois bancos

| Banco na instalação | Banco na central | Estratégia | Sentido | Escrita na central |
|---|---|---|---|---|
| `ecm_copel_jdfigueira` (todas as tabelas) | `ecm_copel_jdfigueira` | Transacional | Só sobe | Não (só consulta) |
| `sigmaecm_copel_figueira` (7 tabelas específicas) | `sigmaecm` | Merge, sync none | Bidirecional | Sim (sistema central opera) |

**Por que estratégias diferentes:** o `ecm_copel_jdfigueira` na central é backup de consulta, então o transacional unidirecional serve. Já o `sigmaecm` na central roda o sistema Sigma que opera de verdade (reconhece alarme, tem usuários próprios, histórico de acesso), e só o merge reconcilia as duas pontas sem perder dados. As pessoas editam as mesmas tabelas que vêm replicadas, e só o merge reconcilia sem perda.

### 1.2 Topologia

| Papel | Servidor | Versão / Observação |
|---|---|---|
| Publisher + Distributor | `Srv-Jd-Figueira` | SQL Server 2019. Nome de máquina e `@@SERVERNAME` iguais (com hifens). |
| Subscriber (pull) | `DISMONTFLIC\MSSQLSERVERTT` | SQL Server 2022. Instância nomeada. |

Os dois bancos compartilham o mesmo distribuidor local na Srv-Jd-Figueira e a central puxa os dois. Para outras subestações no futuro, cada uma é um Publisher independente com seu próprio par de bancos.

Regra de rede confirmada no ambiente: **a central alcança a subestação, a subestação NÃO alcança a central**. Isso é o que torna o pull obrigatório e o push proibido. Todo teste de conectividade parte da central.

### 1.3 Observação importante sobre os nomes

1. Os nomes usados nos scripts precisam bater com o que cada instância retorna em `SELECT @@SERVERNAME`. Confirme antes de rodar: na subestação deve retornar `Srv-Jd-Figueira` e na central `DISMONTFLIC\MSSQLSERVERTT`. Se algum não bater, ajuste o nome registrado (`sp_dropserver` / `sp_addserver ... 'local'`) ou troque o valor nos scripts.
2. A central é uma instância nomeada. Use sempre o formato `host\instancia` (`DISMONTFLIC\MSSQLSERVERTT`) ao conectar nela e nos parâmetros onde ela aparece (`@subscriber`, `@distributor` em comentários, tablediff).
3. No fluxo pull, quem disca é a central. Portanto o que precisa estar liberado é a porta SQL da Srv-Jd-Figueira e o share, no sentido central para subestação. A porta da instância nomeada da central só importa para você conectar nela pelo SSMS, não para o fluxo de replicação.

### 1.4 Contas e credenciais

Três coisas distintas, não confundir:

| Item | Tipo | Onde existe | Usado para |
|---|---|---|---|
| `repl_user` | Login SQL | Só na subestação | Conexões SQL dos agentes ao publisher e distributor |
| `svc_repl` | Conta Windows | Nos dois servidores, mesma senha (espelhada) | Rodar o job do agente na central e ler o share |
| `DISMONTFLIC\svc_repl` | Login Windows no SQL | Na central | O agente conecta no subscriber local por Windows Auth com essa conta |
| Master Key | Chave do banco `sigmaecm` | Na central | Criptografar os segredos de replicação (merge com SQL Auth) |

---

## 2. Pré-requisitos

1. **Componente de replicação instalado** nas duas instâncias (recurso "SQL Server Replication" do setup). Sem ele as procedures de replicação não existem.
2. **SQL Server Agent ligado** e em inicialização automática nas duas instâncias. Os agentes de replicação são jobs do Agent.
3. **Autenticação (modelo SQL Authentication)**. A replicação tem duas camadas de autenticação, e só a primeira vira SQL auth:
   - **Camada 1** (conexões SQL dos agentes ao publisher/distributor/subscriber): usa um login SQL. Crie na Srv-Jd-Figueira o login `repl_user` (o passo 3.2 já faz isso). É ele que a central usa para alcançar a subestação e que os agentes locais usam no publisher. Use a mesma senha em todos os scripts.
   - **Camada 2** (conta de sistema que roda o job do agente e acessa o share): é sempre Windows. O job do Distribution Agent na central roda sob uma conta Windows (`@job_login`), que precisa ler o share de snapshot da subestação. Isso não vira login SQL.
4. **Share de snapshot na subestação**: crie a pasta (ex.: `C:\repldata`) e compartilhe como `\\Srv-Jd-Figueira\repldata`. Como subestação e central não compartilham domínio, a conta Windows do job da central precisa conseguir ler esse share. Escolha uma opção:
   - Conta local espelhada: a mesma conta Windows (mesmo nome e senha) criada na central (roda o job) e na subestação (com leitura no share). O Windows faz pass-through.
   - Ou entrega do snapshot por FTP (`@use_ftp = 1` no agente e parâmetros FTP na publicação), evitando o share Windows.
5. **Firewall (ponto central da arquitetura)**: libere apenas Central para Subestação:
   - Porta da instância SQL da Subestação (1433 ou a porta customizada).
   - Acesso ao share de snapshot (porta 445/UNC), ou FTP se preferir transferir o snapshot por FTP.
   - Nenhuma regra no sentido Subestação para Central.
6. **Criptografia do canal WAN**: TLS nas conexões SQL ou VPN. Se usar VPN, configure o firewall para permitir apenas sessões iniciadas pela Central.
7. **Database Mail na Subestação** (apenas se for usar o alerta do health check): habilite o recurso e crie um profile SMTP.
8. **Chaves primárias e rowguid**: o banco 1 (transacional) só publica tabelas com PK; a seção 4.1 lista as sem PK no início, decida antes (criar PK ou deixar de fora). O banco 2 (merge) não exige PK, mas cria a coluna rowguid e triggers em cada tabela publicada (mudança de schema).

### 2.1 Pré-checagem (nos dois servidores)

```sql
DECLARE @r int; EXEC @r = master.sys.sp_MS_replication_installed; SELECT @r AS replication_installed; -- 1 = ok
SELECT @@SERVERNAME AS nome_sql;
SELECT SERVERPROPERTY('ProductVersion') AS versao, SERVERPROPERTY('Edition') AS edicao;
SELECT servicename, status_desc FROM sys.dm_server_services WHERE servicename LIKE N'SQL Server Agent%'; -- Running
```

Exigências: replicação instalada (1) nos dois, Agent rodando nos dois, edição não pode ser Express, e o `@@SERVERNAME` tem que bater com o nome usado nos scripts.

---

## 3. Fundação (preparação dos servidores)

Esta seção é a base dos dois bancos. Feita uma vez, serve para as duas replicações e é largamente reaproveitada nas próximas instalações.

### 3.1 Login SQL de replicação (na subestação)

Crie o usuário `repl_user` com permissão `db_owner`:

```sql
USE master;
GO
CREATE LOGIN repl_user WITH PASSWORD = N'<SenhaReplUserForte>', CHECK_POLICY = ON;
GO
```

Caso o login já exista, use:

```sql
USE master;
GO
IF NOT EXISTS (SELECT 1 FROM sys.sql_logins WHERE name = N'repl_user')
    CREATE LOGIN repl_user WITH PASSWORD = N'tr3t3Ch2!PW', CHECK_POLICY = ON;
GO
```

No banco publicado (necessário para os agentes e para o snapshot):

```sql
USE ecm_copel_jdfigueira;
GO
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'repl_user')
    CREATE USER repl_user FOR LOGIN repl_user;
ALTER ROLE db_owner ADD MEMBER repl_user;
GO
```

### 3.2 Conta Windows espelhada (nos dois servidores)

Crie a MESMA conta Windows, com a MESMA senha, na subestação e na central. Execute no **Prompt de Comando CMD** nos dois servidores:

```cmd
net user svc_repl <SenhaWindowsIgualNosDois> /add
```

Para definir a senha de um usuário existente:

```cmd
net user svc_repl Repl#Copel2026
```

### 3.3 Pasta e compartilhamento de snapshot (na subestação)

Crie `C:\repldata`, compartilhe como `repldata`, e conceda as permissões necessárias:

```cmd
net share repldata=C:\repldata /grant:svc_repl,READ
icacls C:\repldata /grant "svc_repl:(OI)(CI)R"
```

O caminho de réseau final é `\\Srv-Jd-Figueira\repldata`.

A conta de serviço do SQL Server Agent precisa de **ESCRITA** nessa pasta (ela gera o snapshot):

```cmd
igacls C:\repldata /grant "NT SERVICE\SQLSERVERAGENT:(OI)(CI)F"
```

Comandos úteis para gerenciamento do compartilhamento:

```cmd
net share
```
- Exibe as pastas compartilhadas.

```cmd
net share repldata2 /delete
```
- Remove um compartilhamento de rede (feito para as pastas `repldata` e `repldata2`).

```cmd
net use * /delete /yes
```
- Força a desconexão dos usuários das pastas compartilhadas.

### 3.4 Firewall

Liberar **apenas** Central para Subestação: porta SQL da subestação (1433 ou customizada) e porta 445 (share). **Nenhuma regra no sentido contrário.**

### 3.5 Teste do share (gate)

Da central, este teste tem que passar antes de qualquer script de replicação:

```cmd
net use * /delete /yes
net use \\Srv-Jd-Figueira\repldata /user:Srv-Jd-Figueira\svc_repl <SenhaWindows>
```

Deve responder "concluído com êxito". Valide a configuração de rede:

```cmd
\\SRV-JD-FIGUEIRA\repldata
```

Depois limpe:

```cmd
net use \\SRV-JD-FIGUEIRA\repldata /delete
```

### 3.6 Criação do Distribuidor (na subestação)

O distribuidor e o `repl_user` criados aqui também atendem o banco 2. Por isso este passo é sempre o primeiro a rodar.

```sql
USE master;
GO
EXEC sp_adddistributor
     @distributor = N'Srv-Jd-Figueira',          -- instância que será o Distributor. Deve ser igual a SELECT @@SERVERNAME da subestação.
     @password    = N'8wW%9Ls!a3ls';             -- senha da conta interna 'distributor_admin' usada na comunicação com o distribuidor.
GO

EXEC sp_adddistributiondb
     @database      = N'distribution',           -- nome do banco de distribuição (convenção: 'distribution'). Guarda os comandos a entregar.
     @security_mode = 0,                         -- 0 = SQL Authentication.
     @login         = N'repl_user',              -- login SQL usado nessa conexão.
     @password      = N'tr3t3Ch2!PW';            -- senha do login SQL.
GO

-- Registra a subestação como Publisher atendido pelo distribuidor local.
EXEC sp_adddistpublisher
     @publisher         = N'Srv-Jd-Figueira',    -- instância publicadora (a própria subestação).
     @distribution_db   = N'distribution',       -- banco de distribuição que atende este publisher.
     @security_mode     = 0,                     -- 0 = SQL Authentication na ligação Publisher <-> Distributor.
     @login             = N'repl_user',          -- login SQL usado nessa conexão.
     @password          = N'tr3t3Ch2!PW',        -- senha do login SQL.
     @working_directory = N'\\Srv-Jd-Figueira\repldata';  -- PASTA DE SNAPSHOT (UNC). É daqui que a central (pull) LÊ o snapshot.
GO
```

**Resultado esperado:** criação das tabelas de distribuição (`MSreplservers`, `MSpublications`, `MSarticles`, `MSsubscriptions`, `MSmerge_subscriptions`, etc.) e das stored procedures de distribuição.

---

## 4. Fase A — Banco 1: Replicação Transacional (`ecm_copel_jdfigueira`)

Arquivos `01_Srv-Jd-Figueira_ecm_transacional_setup.sql` (subestação) e `02_CENTRAL_ecm_transacional_assinatura.sql` (central). Todas as 60 tabelas tinham PK, então a publicação de todas foi limpa (60 artigos, 0 ignorados).

### 4.1 Subestação — Setup e publicação (arquivo 01)

#### 4.1.1 Habilitar publicação e criar o Log Reader Agent

**IMPORTANTE:** rode isto ANTES do `sp_addpublication`. Se a publicação for criada primeiro, o Log Reader é criado em Windows Auth por padrão.

```sql
USE master;
GO
EXEC sp_replicationdboption
     @dbname  = N'ecm_copel_jdfigueira',          -- banco de origem que será publicado.
     @optname = N'publish',                        -- opção 'publish' liga a capacidade de publicação transacional/snapshot neste banco.
     @value   = N'true';                           -- 'true' liga, 'false' desliga.
GO

USE ecm_copel_jdfigueira;
GO
EXEC sp_addlogreader_agent
     @publisher_security_mode = 0,               -- 0 = SQL Authentication para conectar no publisher (a subestação).
     @publisher_login         = N'repl_user',    -- login SQL usado pelo Log Reader no publisher.
     @publisher_password      = N'tr3t3Ch2!PW';  -- senha do login SQL.
     -- @job_login/@job_password omitidos de propósito: o JOB roda sob a conta de
     -- serviço do SQL Server Agent (Windows). Isso é estrutural, não vira SQL Auth.
GO
```

**Resultado esperado:** `Job 'SRV-JD-FIGUEIRA-ecm_copel_jdfigueira-1' started successfully.`

#### 4.1.2 Criar a publicação transacional

```sql
USE ecm_copel_jdfigueira;
GO
EXEC sp_addpublication
     @publication       = N'Pub_ecm_jdfigueira',  -- nome da publicação (identificador deste conjunto de artigos).
     @description       = N'Replicação transacional de todas as tabelas: Subestação -> Central',
     @status            = N'active',              -- 'active' = publicação pronta para uso; 'inactive' = criada mas parada.
     @repl_freq         = N'continuous',          -- 'continuous' = transacional (Log Reader entrega mudanças continuamente); 'snapshot' = só snapshot periódico.
     @sync_method       = N'concurrent',          -- 'concurrent' = gera o snapshot sem travar as tabelas (menos bloqueio); 'native' travaria durante o snapshot.
     @independent_agent = N'true',                -- 'true' = um Distribution Agent dedicado por assinatura (recomendado); 'false' = agente compartilhado.
     @allow_push        = N'false',               -- 'false' = NÃO permite assinatura push (a subestação nunca empurra para a central). Reforça a política de segurança.
     @allow_pull        = N'true',                -- 'true' = permite assinatura pull (a central puxa). É o modo que respeita o firewall.
     @allow_anonymous   = N'false',               -- 'false' = exige assinaturas registradas/nomeadas (mais controle e rastreio).
     @immediate_sync    = N'false';               -- 'false' = arquivos de sincronização gerados sob demanda para novas assinaturas (par com allow_anonymous=false).
GO

-- Cria o Snapshot Agent da publicação (gera o snapshot inicial das tabelas).
EXEC sp_addpublication_snapshot
     @publication             = N'Pub_ecm_jdfigueira',
     @frequency_type          = 1,               -- agenda do Snapshot Agent. 1 = sob demanda (uma vez, sem recorrência). Ex.: 4=diario, 8=semanal.
     @publisher_security_mode = 0,               -- 0 = SQL Authentication para o Snapshot Agent conectar no publisher.
     @publisher_login         = N'repl_user',    -- login SQL usado pelo Snapshot Agent no publisher.
     @publisher_password      = N'tr3t3Ch2!PW';  -- senha do login SQL.
     -- @job_login/@job_password omitidos: o JOB roda sob a conta de serviço do SQL Agent (Windows).
GO

-- Concede acesso da publicação ao login SQL (Publication Access List - PAL).
-- Sem isso, repl_user não consegue conectar no publisher/distributor pela replicação.
EXEC sp_grant_publication_access
     @publication = N'Pub_ecm_jdfigueira',
     @login       = N'repl_user';
GO
```

#### 4.1.3 Verificar tabelas sem chave primária

Antes de publicar, confirme se existem tabelas sem PK. O transacional exige PK para cada artigo.

```sql
USE ecm_copel_jdfigueira;
GO
SELECT s.name AS esquema, t.name AS tabela_sem_pk
FROM   sys.tables  AS t
JOIN   sys.schemas AS s ON s.schema_id = t.schema_id
WHERE  t.is_ms_shipped = 0
  AND  NOT EXISTS (SELECT 1 FROM sys.indexes i
                   WHERE i.object_id = t.object_id AND i.is_primary_key = 1)
ORDER  BY s.name, t.name;
```

Decidir antes: criar PK ou deixar a tabela de fora da publicação.

#### 4.1.4 Selecionar as tabelas para publicação

```sql
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
             @publication               = @pub,        -- publicação onde o artigo entra.
             @article                   = @tabela,     -- nome lógico do artigo (usamos o próprio nome da tabela).
             @source_owner              = @esquema,    -- schema de origem na subestação.
             @source_object             = @tabela,     -- tabela de origem.
             @type                      = N'logbased', -- 'logbased' = artigo baseado no log de transações (padrão transacional).
             @destination_owner         = @esquema,    -- schema de destino na central (mesmo schema).
             @destination_table         = @tabela,     -- tabela de destino na central.
             @force_invalidate_snapshot = 1;           -- 1 = permite adicionar artigo invalidando o snapshot atual (necessário ao incluir tabelas após criar a publicação).
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

#### 4.1.5 Conferir tabelas publicadas

```sql
USE ecm_copel_jdfigueira;
GO
EXEC sys.sp_helparticle @publication = N'Pub_ecm_jdfigueira';
GO
```

#### 4.1.6 Registrar a assinatura pull e gerar o snapshot

```sql
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

Dispare o snapshot e aguarde concluir:

```sql
USE ecm_copel_jdfigueira;
GO
EXEC sys.sp_startpublication_snapshot @publication = N'Pub_ecm_jdfigueira';
GO
```

**Verificação do status do Snapshot:**

```sql
USE distribution;
GO
SELECT TOP (10) [time], runstatus, comments
FROM   dbo.MSsnapshot_history
ORDER  BY [time] DESC;
GO
```

**Resultado esperado:** `runstatus = 2` com mensagem `[100%] A snapshot of 60 article(s) was generated.`

Aguarde o snapshot concluir antes de seguir para a central.

### 4.2 Central — Assinatura pull (arquivo 02)

Só depois do snapshot pronto, conecte na **Central** e execute o script de assinatura.

#### 4.2.1 Login da conta do agente na central

A conta Windows do job (`svc_repl`) precisa de login no SQL da central com `db_owner` no banco de destino:

```sql
USE master;
GO
IF NOT EXISTS (SELECT 1 FROM sys.server_principals WHERE name = N'DISMONTFLIC\svc_repl')
    CREATE LOGIN [DISMONTFLIC\svc_repl] FROM WINDOWS;
GO
USE ecm_copel_jdfigueira;
GO
IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N'DISMONTFLIC\svc_repl')
    CREATE USER [DISMONTFLIC\svc_repl] FOR LOGIN [DISMONTFLIC\svc_repl];
ALTER ROLE db_owner ADD MEMBER [DISMONTFLIC\svc_repl];
GO
```

> **Nota:** sem este login, o agente entra em loop com erro 20084 "could not connect to Subscriber" e a central fica com 0 tabelas.

#### 4.2.2 Criar a assinatura pull e o Distribution Agent

```sql
USE ecm_copel_jdfigueira;
GO
EXEC sp_addpullsubscription
     @publisher         = N'Srv-Jd-Figueira',
     @publisher_db      = N'ecm_copel_jdfigueira',
     @publication       = N'Pub_ecm_jdfigueira',
     @independent_agent = N'true',
     @subscription_type = N'pull';
GO

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

> **Erro conhecido (Msg 8145):** o `sp_addpullsubscription_agent` (transacional) **NÃO** aceita os parâmetros `@publisher_security_mode`, `@publisher_login` nem `@publisher_password` nesta versão do SQL Server. Passe **somente** os do distribuidor (`@distributor_security_mode`, `@distributor_login`, `@distributor_password`). O agente de merge aceita esses parâmetros, o transacional não.

**Resultado esperado:** `Job 'Srv-Jd-Figueira-ecm_copel_jdfiguei-Pub_ecm_jdfigueira-DISMONTFLIC\MSSQLS-...' started successfully.`

Lembre: `ecm_copel_jdfigueira` na central é só consulta, ninguém pode gravar nessas tabelas.

---

## 5. Fase B — Banco 2: Replicação Merge (`sigmaecm`)

Arquivos `03_Srv-Jd-Figueira_sigma_merge_setup.sql` (subestação) e `04_CENTRAL_sigma_merge_assinatura.sql` (central). 7 tabelas: MonitoramentoRedeOnline, ModuloAtivo, MonitoramentoRedeHistorico, Usuario, AlarmeAnunciador, Alarme, AlarmeAnunciadorEvento.

### 5.1 Decisões de design

- **Conflito:** a instalação sempre vence. Implementado com assinatura `global` e prioridade 75 (o publisher tem prioridade 100).
- **Inicialização:** `@sync_type = 'none'`. O banco `sigmaecm` na central é criado por EF Migrations e tem dezenas de foreign keys apontando para as 7 tabelas. O snapshot padrão (`automatic`) tentaria derrubar e recriar as tabelas e quebraria nas FKs e nas migrations do EF. O `none` não toca na estrutura, só rastreia mudanças.
- **ROWGUIDCOL:** as tabelas já têm coluna `Id` uniqueidentifier. Marcamos ela como ROWGUIDCOL nos DOIS lados, então o merge reutiliza o `Id` e não cria a coluna `rowguid`. Os triggers de rastreamento do merge ainda são criados.

### 5.2 Subestação — Setup e publicação merge (arquivo 03)

#### 5.2.1 Habilitar merge publish e criar o usuário

```sql
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

#### 5.2.2 Criar a publicação merge

```sql
USE sigmaecm_copel_figueira;
GO
EXEC sp_addmergepublication
     @publication           = N'Pub_sigmaecm',
     @description           = N'Merge bidirecional de tabelas específicas: Figueira <-> Central',
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

#### 5.2.3 Verificar colunas uniqueidentifier (GUID)

A replicação merge exige um GUID identificador de linha. Verifique quais tabelas têm coluna `uniqueidentifier`:

```sql
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

Se `is_rowguidcol = 0` para alguma tabela, marque como ROWGUIDCOL:

```sql
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

#### 5.2.4 Registrar assinatura pull merge e gerar snapshot

```sql
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

Dispare o snapshot:

```sql
USE sigmaecm_copel_figueira;
GO
EXEC sys.sp_startpublication_snapshot @publication = N'Pub_sigmaecm';
GO
```

**Verificação do status do Snapshot:**

```sql
USE distribution;
GO
SELECT TOP (10) [time], comments
FROM   dbo.MSsnapshot_history
ORDER  BY [time] DESC;
GO
```

**Resultado esperado:** `[100%] A snapshot of 7 article(s) was generated.`

### 5.3 Central — Assinatura merge pull (arquivo 04)

Depois do snapshot do merge, conecte na **Central**.

#### 5.3.1 Login da conta do agente + Master Key

```sql
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

> **Aviso importante:** o merge com SQL Auth precisa da Database Master Key (DMK) para criptografar os segredos de replicação. Se não criar, o agente emite o warning: *"The database 'sigmaecm' does not contain database master key"*.

```sql
USE sigmaecm;
GO
CREATE MASTER KEY ENCRYPTION BY PASSWORD = N'h$t$Dm*8m&Ue';
GO
```

#### 5.3.2 Marcar ROWGUIDCOL nas tabelas da central

```sql
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

#### 5.3.3 Criar a assinatura merge pull

```sql
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

#### 5.3.4 Atualizar senha do distribuidor (se necessário)

```sql
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

#### 5.3.5 Reset da assinatura merge (caso precise refazer)

Se a assinatura foi configurada incorretamente, siga o procedimento de reset:

**Passo 1 — Remover assinatura na central:**

```sql
USE sigmaecm;
GO
EXEC sp_dropmergepullsubscription
     @publisher    = N'Srv-Jd-Figueira',
     @publisher_db = N'sigmaecm_copel_figueira',
     @publication  = N'Pub_sigmaecm';
GO
```

**Passo 2 — Remover assinatura pull na subestação:**

```sql
USE sigmaecm_copel_figueira;
GO
EXEC sp_dropmergepullsubscription
     @publisher    = N'Srv-Jd-Figueira',
     @publisher_db = N'sigmaecm_copel_figueira',
     @publication  = N'Pub_sigmaecm';
GO
```

**Passo 3 — Recriar assinatura na subestação (sync none):**

```sql
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

**Passo 4 — Recriar assinatura pull na central (sync none):**

```sql
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

### 5.4 Validação do merge

Como sync none não desce dados antigos, a validação é por mudança: inserir ou alterar uma linha de um lado e ver aparecer no outro. Validado nos dois sentidos.

**Consulta para verificar sincronização:**

```sql
USE distribution;
GO
SELECT TOP (10) [time], runstatus, comments
FROM   dbo.MSmerge_history
ORDER  BY [time] DESC;
GO
```

> **Nota:** a inserção de um alarme via script foi utilizada para validação e ocorreu a sincronização esperada.

---

## 6. Monitoramento e validação

### 6.1 Validação do banco 1 (transacional)

Execute o script `05_monitoramento_validacao.sql` nos servidores indicados em cada bloco. A primeira parte valida o banco 1 com:
- Tracer token
- Backlog
- Contagem de todas as tabelas

### 6.2 Validação do banco 2 (merge)

A parte final (seção MERGE) do script de monitoramento valida o banco 2:
- Status da assinatura merge
- Histórico do Merge Agent
- Conflitos

### 6.3 Monitoramento contínuo do banco 1 (health check)

O script `06_Srv-Jd-Figueira_health_check_alerta.sql` cria:
- Tabela de histórico
- Procedure de coleta
- Job executado a cada 5 minutos
- Alerta por e-mail quando latência ou backlog passam do limite

Deixe coletando alguns dias e ajuste os limites ao volume real.

### 6.4 Onde consultar histórico dos agentes

Sempre no banco `distribution` da **SUBESTAÇÃO** (o banco `distribution` não existe na central):

```sql
USE distribution;
GO
SELECT TOP (10) [time], runstatus, comments
FROM   dbo.MSsnapshot_history     -- Snapshots
ORDER  BY [time] DESC;
GO

SELECT TOP (10) [time], runstatus, comments
FROM   dbo.MSlogreader_history    -- Log Reader
ORDER  BY [time] DESC;
GO

SELECT TOP (10) [time], runstatus, comments
FROM   dbo.MSdistribution_history -- Distribution Agent
ORDER  BY [time] DESC;
GO

SELECT TOP (10) [time], runstatus, comments
FROM   dbo.MSmerge_history        -- Merge Agent
ORDER  BY [time] DESC;
GO
```

---

## 7. Solução de problemas comuns (Troubleshooting)

| Sintoma | Causa | Solução |
|---|---|---|
| **System Error 64 no `net use` do share** | Conta `svc_repl` não existia igual nos dois lados, ou senha divergente, ou cache | Recriar a conta espelhada com a mesma senha; qualificar com `host\conta`; `net use * /delete` antes |
| **A Central não lê o snapshot** | Quase sempre permissão no share ou firewall na porta 445 | Teste abrindo `\\Srv-Jd-Figueira\repldata` a partir da Central com a conta do agente |
| **Agente falha ao conectar na Subestação** | Login `repl_user` inexistente ou porta bloqueada | Verifique o login `repl_user`, a porta SQL liberada e, se usar instância nomeada, o SQL Browser ou a porta fixa |
| **Tabela não replicou no banco 1** | Tabela sem PK | Confira se ela tem PK. Sem PK, não entra no transacional |
| **Tabela nova no banco 1 não aparece** | Tabelas novas não entram sozinhas | Rode de novo a seção 4.1.4 e gere o snapshot |
| **Latência alta só no trecho Distributor para Subscriber** | Gargalo na rede ou no agente da Central | Verifique a rede e o agente na Central |
| **Erro 8145 ao criar Distribution Agent** | `sp_addpullsubscription_agent` (transacional) não aceita parâmetros de login do publisher | Passar só os do distribuidor (`@distributor_security_mode`, `@distributor_login`, `@distributor_password`) |
| **Erro 20084 "could not connect to Subscriber"** | Conta do job sem login no SQL da central; o agente entra em loop com 0 tabelas | `CREATE LOGIN [host\svc_repl] FROM WINDOWS` + `db_owner` no banco de destino. Use formato `host\conta`, não `.\conta` |
| **Proxy ".\svc_repl" is not a valid Windows user** | Formato `.\conta` recusado pelo SQL | Usar `host\conta` (`DISMONTFLIC\svc_repl`) |
| **Warning "does not contain database master key"** | Merge com SQL Auth precisa da DMK para criptografar segredos | `CREATE MASTER KEY` no banco de destino |
| **Erro 3726 "Could not drop object ... FOREIGN KEY"** | `sync automatic` tentando derrubar tabela referenciada por FKs | Usar `@sync_type = 'none'` |
| **Cannot insert explicit value for identity column** | Script de INSERT de teste preenchendo coluna identity | Deixar o banco gerar o valor (as PKs são GUID) |
| **Conflitos no banco 2 (merge)** | Dois lados editam a mesma linha | Consulte `MSmerge_conflicts_info` e `sp_helpmergeconflictrows`. Quem vence segue a prioridade da assinatura; por padrão, a subestação |
| **Erro de usuário 'sa'** | Usuário sem acesso ao banco de dados | Criar login e conceder `db_owner` no banco de destino |

---

## 8. Regra de ouro: EF Migrations × Merge

Depois que uma tabela entra no merge, o Entity Framework não pode mais alterar a estrutura dela livremente. Uma migration que faça `ALTER TABLE` numa das 7 tabelas replicadas (adicionar coluna, mudar tipo) precisa passar pelo mecanismo de schema change da replicação, senão quebra a replicação ou a migration.

### Procedimento seguro para alterar uma tabela replicada

**Opção A (mudança simples de coluna):**
Usar `sp_repladdcolumn` / `sp_repldropcolumn`, que propagam a alteração para os assinantes pela própria replicação.

**Opção B (mudança complexa):**
1. Remover o artigo do merge (`sp_dropmergearticle`)
2. Aplicar a migration do EF
3. Readicionar o artigo e regerar o rastreamento

As demais tabelas do `sigmaecm` (as dezenas que referenciam as 7, e todas as outras) o EF gerencia normalmente, sem restrição, porque não estão replicadas. A restrição vale **só para as 7 tabelas do merge**.

---

## 9. Roteiro para as próximas instalações

### O que se reaproveita (já pronto, não refazer)

- O distribuidor local é por instalação, mas o método é idêntico
- A conta `svc_repl` espelhada e o login dela no SQL da central
- A Master Key no `sigmaecm`
- O padrão de nomes e scripts

### O que muda por instalação

1. **Nomes:** servidor `SRV<NomeInstalacao>`, bancos `ecm_<local>` e `sigmaecm_<local>`, publicações `Pub_ecm_<local>` e `Pub_sigmaecm`.
2. **Banco `ecm_`:** cada instalação vai para um banco de mesmo nome na central (destinos separados, sem colisão).
3. **Banco `sigmaecm_`:** todas as instalações fazem merge para o MESMO `sigmaecm` na central. Como as PKs são GUID, Figueira e Novo Mundo coexistem sem colidir. Marcar ROWGUIDCOL nas 7 tabelas da nova instalação e usar sync none, igual à Figueira.
4. **Repetir a fundação** de rede/share/conta para o novo servidor (o sentido central para instalação, o share, o firewall).

### Ponto de atenção para o multi-instalação

Confirmar que as 7 tabelas do `sigmaecm_` da nova instalação têm PK GUID (não identity). Se alguma for identity, configurar identity range management antes de plugar, senão haverá colisão de chave na central.

---

## 10. Referência rápida

| Item | Valor |
|---|---|
| **Subestação** | `Srv-Jd-Figueira` |
| **Central** | `DISMONTFLIC\MSSQLSERVERTT` |
| **Share de snapshot** | `\\Srv-Jd-Figueira\repldata` |
| **Banco 1 (origem/destino)** | `ecm_copel_jdfigueira` (transacional) |
| **Banco 2 (origem)** | `sigmaecm_copel_figueira` (merge) |
| **Banco 2 (destino)** | `sigmaecm` (merge) |
| **Publicação 1** | `Pub_ecm_jdfigueira` (transacional) |
| **Publicação 2** | `Pub_sigmaecm` (merge) |
| **Login SQL** | `repl_user` (só na subestação) |
| **Conta Windows** | `svc_repl` (espelhada nos dois) |
| **Master Key** | No `sigmaecm` da central |
| **Banco de distribuição** | `distribution` (só na subestação) |

### Arquivos do pacote

| Ordem | Arquivo | Rodar no servidor | Banco / estratégia |
|---|---|---|---|
| 1 | `01_Srv-Jd-Figueira_ecm_transacional_setup.sql` | Subestação | ecm (transacional) |
| 2 | `02_CENTRAL_ecm_transacional_assinatura.sql` | Central | ecm (transacional) |
| 3 | `03_Srv-Jd-Figueira_sigma_merge_setup.sql` | Subestação | sigma (merge) |
| 4 | `04_CENTRAL_sigma_merge_assinatura.sql` | Central | sigma (merge) |
| 5 | `05_monitoramento_validacao.sql` | Misto | os dois |
| 6 | `06_Srv-Jd-Figueira_health_check_alerta.sql` | Subestação | ecm (transacional) |

**Ordem geral:** faça o banco 1 inteiro primeiro (arquivos 01 e 02, aguardando o snapshot), depois o banco 2 (arquivos 03 e 04). Os dois usam o distribuidor e o login `repl_user` criados no arquivo 01, então o 01 é sempre o primeiro a rodar.

---

## 11. Checklist final

1. Componente de replicação instalado nas duas instâncias.
2. SQL Server Agent ligado nas duas.
3. Login `repl_user` criado na Subestação e conta Windows do agente definida na Central.
4. Share de snapshot criado na Subestação com leitura para a Central.
5. Firewall liberado apenas Central para Subestação.
6. Canal WAN criptografado.
7. Banco 1: tabelas sem PK tratadas.
8. Banco 2: tabelas específicas listadas no arquivo 03 e o vencedor do conflito decidido.
9. Banco 2: avaliado o impacto do rowguid/triggers e dos dados que já existem em `sigmaecm`.
10. Snapshot inicial concluído antes de criar cada assinatura na Central.
11. Banco 1 validado (backlog perto de zero, contagens batendo) e health check ativo.
