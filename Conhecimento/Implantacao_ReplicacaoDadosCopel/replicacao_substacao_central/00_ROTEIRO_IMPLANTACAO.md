# Roteiro de Implantação: Replicação Subestação para Central

Documento as-built. Descreve o procedimento que foi efetivamente executado e validado na subestação JD Figueira, incluindo os problemas encontrados e como cada um foi resolvido. Serve de referência para operar a Figueira e para plugar as próximas instalações (Novo Mundo e demais).

## 1. Visão geral

A central consolida dados de várias instalações. Cada instalação tem dois bancos, e cada um usa uma estratégia diferente de replicação. Em ambos o modelo é pull: a central puxa, e a instalação nunca abre conexão com a central.

| Banco na instalação | Banco na central | Estratégia | Sentido | Escrita na central |
|---|---|---|---|---|
| `ecm_copel_jdfigueira` (todas as tabelas) | `ecm_copel_jdfigueira` | Transacional | Só sobe | Não (só consulta) |
| `sigmaecm_copel_figueira` (7 tabelas) | `sigmaecm` | Merge, sync none | Bidirecional | Sim (sistema central opera) |

Por que estratégias diferentes: o `ecm_` na central é backup de consulta, então o transacional unidirecional serve. O `sigmaecm` na central roda o sistema Sigma que opera de verdade (reconhece alarme, tem usuários próprios, histórico de acesso), então os dois lados escrevem, e só o merge reconcilia.

## 2. Topologia e nomes reais

| Papel | Servidor | Observação |
|---|---|---|
| Publisher + Distributor | `Srv-Jd-Figueira` | SQL 2019. Nome de máquina e `@@SERVERNAME` iguais (com hifens). |
| Subscriber (pull) | `DISMONTFLIC\MSSQLSERVERTT` | SQL 2022. Instância nomeada. |

Regra de rede confirmada no ambiente: a central alcança a subestação, a subestação NÃO alcança a central. Isso é o que torna o pull obrigatório e o push proibido. Todo teste de conectividade parte da central.

Contas e credenciais (três coisas distintas, não confundir):

| Item | Tipo | Onde existe | Usado para |
|---|---|---|---|
| `repl_user` | Login SQL | Só na subestação | Conexões SQL dos agentes ao publisher e distributor |
| `svc_repl` | Conta Windows | Nos dois servidores, mesma senha (espelhada) | Rodar o job do agente na central e ler o share |
| `DISMONTFLIC\svc_repl` | Login Windows no SQL | Na central | O agente conecta no subscriber local por Windows Auth com essa conta |
| Master Key | Chave do banco `sigmaecm` | Na central | Criptografar os segredos de replicação (merge com SQL Auth) |

## 3. Fundação (a parte que mais deu trabalho)

Esta seção é a base dos dois bancos. Feita uma vez, serve para as duas replicações e é largamente reaproveitada nas próximas instalações.

### 3.1 Pré-checagem (nos dois servidores)

```sql
DECLARE @r int; EXEC @r = master.sys.sp_MS_replication_installed; SELECT @r AS replication_installed; -- 1 = ok
SELECT @@SERVERNAME AS nome_sql;
SELECT SERVERPROPERTY('ProductVersion') AS versao, SERVERPROPERTY('Edition') AS edicao;
SELECT servicename, status_desc FROM sys.dm_server_services WHERE servicename LIKE N'SQL Server Agent%'; -- Running
```

Exigências: replicação instalada (1) nos dois, Agent rodando nos dois, edição não pode ser Express, e o `@@SERVERNAME` tem que bater com o nome usado nos scripts.

### 3.2 Login SQL de replicação (na subestação)

```sql
USE master;
GO
CREATE LOGIN repl_user WITH PASSWORD = N'<SenhaReplUserForte>', CHECK_POLICY = ON;
GO
```

### 3.3 Conta Windows espelhada (nos dois servidores)

Crie a MESMA conta Windows, com a MESMA senha, na subestação e na central:

```
net user svc_repl <SenhaWindowsIgualNosDois> /add
```

### 3.4 Pasta e compartilhamento de snapshot (na subestação)

Crie `C:\repldata`, compartilhe como `repldata`, e conceda as três camadas de permissão à `svc_repl`:

```
net share repldata=C:\repldata /grant:svc_repl,READ
icacls C:\repldata /grant "svc_repl:(OI)(CI)R"
```

O caminho de rede final é `\\Srv-Jd-Figueira\repldata`.

A conta de serviço do SQL Server Agent precisa de ESCRITA nessa pasta (ela gera o snapshot):

```
icacls C:\repldata /grant "NT SERVICE\SQLSERVERAGENT:(OI)(CI)F"
```

### 3.5 Firewall

Liberar apenas Central para Subestação: porta SQL da subestação (1433 ou custom) e porta 445 (share). Nenhuma regra no sentido contrário.

### 3.6 Teste do share (gate)

Da central, este teste tem que passar antes de qualquer script de replicação:

```
net use * /delete /yes
net use \\Srv-Jd-Figueira\repldata /user:Srv-Jd-Figueira\svc_repl <SenhaWindows>
```

Deve responder "concluído com êxito". Depois `net use \\Srv-Jd-Figueira\repldata /delete` para limpar.

## 4. Fase A: Banco 1, transacional (`ecm_copel_jdfigueira`)

Arquivos `01` (subestação) e `02` (central). Todas as 60 tabelas tinham PK, então a publicação de todas foi limpa (60 artigos, 0 ignorados).

Sequência na subestação (arquivo 01): login repl_user no banco; distribuidor local (SQL Auth); habilitar publish; Log Reader Agent em SQL Auth ANTES da publicação; criar publicação (allow_push false, allow_pull true); publicar todas as tabelas; conceder acesso ao repl_user; registrar assinatura pull; gerar snapshot e aguardar runstatus 2.

Sequência na central (arquivo 02): criar o banco de destino vazio se não existir; criar assinatura pull; criar o job do Distribution Agent; validar contagem de tabelas.

Correções importantes descobertas nesta fase (já aplicadas no arquivo 02):

1. `sp_addpullsubscription_agent` (transacional) NÃO aceita `@publisher_security_mode`, `@publisher_login` nem `@publisher_password` nesta versão. Use só os do distribuidor.
2. `@job_login` precisa do formato `host\conta` (`DISMONTFLIC\svc_repl`), não `.\conta`.
3. A conta do job precisa de login no SQL da central com db_owner no banco de destino, senão o agente entra em loop com erro 20084.

Resultado: 60 tabelas sincronizadas, replicação contínua validada.

## 5. Fase B: Banco 2, merge com sync none (`sigmaecm`)

Arquivos `03` (subestação) e `04` (central). 7 tabelas: MonitoramentoRedeOnline, ModuloAtivo, MonitoramentoRedeHistorico, Usuario, AlarmeAnunciador, Alarme, AlarmeAnunciadorEvento.

Decisões que definiram o desenho:

Conflito: a instalação sempre vence. Implementado com assinatura `global` e prioridade 75 (o publisher tem prioridade 100).

Inicialização: `@sync_type = 'none'`. O banco `sigmaecm` na central é criado por EF Migrations e tem dezenas de foreign keys apontando para as 7 tabelas. O snapshot padrão (`automatic`) tentaria derrubar e recriar as tabelas e quebraria nas FKs e nas migrations do EF. O `none` não toca na estrutura, só rastreia mudanças.

ROWGUIDCOL: as tabelas já têm coluna `Id` uniqueidentifier. Marcamos ela como ROWGUIDCOL nos DOIS lados, então o merge reutiliza o `Id` e não cria a coluna `rowguid`. Os triggers de rastreamento do merge ainda são criados.

Sequência na subestação (arquivo 03): acesso do repl_user ao banco; habilitar merge publish; criar publicação merge; snapshot agent em SQL Auth; conceder acesso; marcar Id como ROWGUIDCOL (passo 4a); adicionar as 7 tabelas; registrar assinatura pull com sync none; gerar snapshot.

Sequência na central (arquivo 04): login da svc_repl no SQL + db_owner em `sigmaecm`; criar Master Key; marcar Id como ROWGUIDCOL nas 7 tabelas da central; criar assinatura merge pull com sync none; criar o job do Merge Agent.

Como sync none não desce dados antigos, a validação é por mudança: inserir ou alterar uma linha de um lado e ver aparecer no outro. Validado nos dois sentidos.

## 6. Armadilhas encontradas e soluções (troubleshooting real)

| Sintoma | Causa | Solução |
|---|---|---|
| System Error 64 no `net use` do share | Conta `svc_repl` não existia igual nos dois lados, ou senha divergente, ou cache | Recriar a conta espelhada com a mesma senha; qualificar com `host\conta`; `net use * /delete` antes |
| Erro 8145 ao criar Distribution Agent | `sp_addpullsubscription_agent` não aceita parâmetros de login do publisher nesta versão | Passar só os do distribuidor |
| Erro 20084 "could not connect to Subscriber", agente em loop, central em 0 tabelas | Conta do job sem login no SQL da central | `CREATE LOGIN [host\svc_repl] FROM WINDOWS` + db_owner no destino |
| Proxy ".\svc_repl" is not a valid Windows user | Formato `.\conta` recusado | Usar `host\conta` (`DISMONTFLIC\svc_repl`) |
| Warning "does not contain database master key" (merge) | Merge com SQL Auth precisa da DMK para criptografar segredos | `CREATE MASTER KEY` no banco de destino |
| Erro 3726 "Could not drop object 'Usuario' ... FOREIGN KEY" | sync automatic tentando derrubar tabela referenciada por FKs | Usar `@sync_type = 'none'` |
| Cannot insert explicit value for identity column | Script de INSERT de teste preenchendo coluna identity | Deixar o banco gerar o valor (foi erro só do teste; as PKs são GUID) |

## 7. Regra de ouro: EF Migrations x Merge

Depois que uma tabela entra no merge, o Entity Framework não pode mais alterar a estrutura dela livremente. Uma migration que faça `ALTER TABLE` numa das 7 tabelas replicadas (adicionar coluna, mudar tipo) precisa passar pelo mecanismo de schema change da replicação, senão quebra a replicação ou a migration.

Procedimento seguro para alterar uma tabela replicada:

1. Opção A (mudança simples de coluna): usar `sp_repladdcolumn` / `sp_repldropcolumn`, que propagam a alteração para os assinantes pela própria replicação.
2. Opção B (mudança complexa): remover o artigo do merge (`sp_dropmergearticle`), aplicar a migration do EF, readicionar o artigo e regerar o rastreamento.

As demais tabelas do `sigmaecm` (as dezenas que referenciam as 7, e todas as outras) o EF gerencia normalmente, sem restrição, porque não estão replicadas. A restrição vale só para as 7 tabelas do merge.

## 8. Roteiro para a próxima instalação (Novo Mundo e demais)

O que se REAPROVEITA (já pronto, não refazer): o distribuidor local é por instalação, mas o método é idêntico; a conta `svc_repl` espelhada e o login dela no SQL da central; a Master Key no `sigmaecm`; o padrão de nomes e scripts.

O que MUDA por instalação:

1. Nomes: servidor `SRV<NomeInstalacao>`, bancos `ecm_<local>` e `sigmaecm_<local>`, publicações `Pub_ecm_<local>` e `Pub_sigmaecm`.
2. Banco `ecm_`: cada instalação vai para um banco de mesmo nome na central (destinos separados, sem colisão).
3. Banco `sigmaecm_`: todas as instalações fazem merge para o MESMO `sigmaecm` na central. Como as PKs são GUID, Figueira e Novo Mundo coexistem sem colidir. Marcar ROWGUIDCOL nas 7 tabelas da nova instalação e usar sync none, igual à Figueira.
4. Repetir a fundação de rede/share/conta para o novo servidor (o sentido central para instalação, o share, o firewall).

Ponto de atenção para o multi-instalação: confirmar que as 7 tabelas do `sigmaecm_` da nova instalação têm PK GUID (não identity). Se alguma for identity, configurar identity range management antes de plugar, senão haverá colisão de chave na central.

## 9. Referência rápida

Nomes: subestação `Srv-Jd-Figueira`; central `DISMONTFLIC\MSSQLSERVERTT`; share `\\Srv-Jd-Figueira\repldata`.

Bancos: `ecm_copel_jdfigueira` (origem e destino, transacional); `sigmaecm_copel_figueira` (origem merge) para `sigmaecm` (destino merge).

Publicações: `Pub_ecm_jdfigueira` (transacional); `Pub_sigmaecm` (merge).

Contas: `repl_user` (SQL, só na subestação); `svc_repl` (Windows, espelhada nos dois); Master Key no `sigmaecm` da central.

Onde consultar histórico dos agentes: sempre no banco `distribution` da SUBESTAÇÃO (`MSdistribution_history`, `MSlogreader_history`, `MSmerge_history`, `MSsnapshot_history`). O banco `distribution` não existe na central.

Arquivos do pacote:

| Arquivo | Servidor | Função |
|---|---|---|
| `01_Srv-Jd-Figueira_ecm_transacional_setup.sql` | Subestação | Banco 1: setup e publicação transacional |
| `02_CENTRAL_ecm_transacional_assinatura.sql` | Central | Banco 1: assinatura pull |
| `03_Srv-Jd-Figueira_sigma_merge_setup.sql` | Subestação | Banco 2: setup e publicação merge |
| `04_CENTRAL_sigma_merge_assinatura.sql` | Central | Banco 2: Master Key, ROWGUIDCOL, assinatura merge sync none |
| `05_monitoramento_validacao.sql` | Misto | Monitoramento transacional e merge |
| `06_Srv-Jd-Figueira_health_check_alerta.sql` | Subestação | Health check e alerta por e-mail (banco 1) |
