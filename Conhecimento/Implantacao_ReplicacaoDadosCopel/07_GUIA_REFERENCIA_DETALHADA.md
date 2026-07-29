# Guia passo a passo: Replicação Substação para Central (transacional + merge)

Dois bancos da subestação Srv-Jd-Figueira são replicados para a central DISMONTFLIC\MSSQLSERVERTT, cada um com a estratégia certa. Em ambos o modelo é pull: a central puxa, e a subestação nunca abre conexão com a central.

## Os dois bancos

| Banco na subestação | Banco na central | Estratégia | Sentido | Escrita na central |
|---|---|---|---|---|
| `ecm_copel_jdfigueira` (todas as tabelas) | `ecm_copel_jdfigueira` | Transacional | Só sobe | Não (só consulta) |
| `sigmaecm_copel_figueira` (tabelas específicas) | `sigmaecm_copel` | Merge | Bidirecional | Sim (editado por pessoas) |

Por que estratégias diferentes: o `ecm_copel_jdfigueira` na central é só backup de consulta, então o transacional unidirecional serve. Já o `sigmaecm_copel` é editado pelas pessoas nas mesmas tabelas que vêm replicadas, e só o merge reconcilia as duas pontas sem perder dados.

## Topologia

| Papel | Servidor | Versão |
|---|---|---|
| Publisher + Distributor | Srv-Jd-Figueira | SQL Server 2019 |
| Subscriber (pull) | DISMONTFLIC\MSSQLSERVERTT | SQL Server 2022 |

Os dois bancos compartilham o mesmo distribuidor local na Srv-Jd-Figueira e a central puxa os dois. Para outras subestações no futuro, cada uma é um Publisher independente com seu próprio par de bancos.

### Observação importante sobre os nomes

1. Os nomes usados nos scripts precisam bater com o que cada instância retorna em `SELECT @@SERVERNAME`. Confirme antes de rodar: na substação deve retornar `Srv-Jd-Figueira` e na central `DISMONTFLIC\MSSQLSERVERTT`. Se algum não bater, ajuste o nome registrado (`sp_dropserver` / `sp_addserver ... 'local'`) ou troque o valor nos scripts.
2. A central é uma instância nomeada. Use sempre o formato `host\instancia` (DISMONTFLIC\MSSQLSERVERTT) ao conectar nela e nos parâmetros onde ela aparece (`@subscriber`, `@distributor` em comentários, tablediff).
3. No fluxo pull, quem disca é a central. Portanto o que precisa estar liberado é a porta SQL da Srv-Jd-Figueira e o share, no sentido central para substação. A porta da instância nomeada da central só importa para você conectar nela pelo SSMS, não para o fluxo de replicação.

## Arquivos do pacote (ordem de execução)

Cada SQL traz no topo um banner indicando o servidor onde deve rodar.

| Ordem | Arquivo | Rodar no servidor | Banco / estratégia |
|---|---|---|---|
| 1 | `01_Srv-Jd-Figueira_ecm_transacional_setup.sql` | Srv-Jd-Figueira | ecm (transacional) |
| 2 | `02_CENTRAL_ecm_transacional_assinatura.sql` | CENTRAL | ecm (transacional) |
| 3 | `03_Srv-Jd-Figueira_sigma_merge_setup.sql` | Srv-Jd-Figueira | sigma (merge) |
| 4 | `04_CENTRAL_sigma_merge_assinatura.sql` | CENTRAL | sigma (merge) |
| 5 | `05_monitoramento_validacao.sql` | MISTO | os dois |
| 6 | `06_Srv-Jd-Figueira_health_check_alerta.sql` | Srv-Jd-Figueira | ecm (transacional) |

Ordem geral: faça o banco 1 inteiro primeiro (arquivos 01 e 02, aguardando o snapshot), depois o banco 2 (arquivos 03 e 04). Os dois usam o distribuidor e o login `repl_user` criados no arquivo 01, então o 01 é sempre o primeiro a rodar.

## Antes de começar (pré-requisitos)

1. **Componente de replicação instalado** nas duas instâncias (recurso "SQL Server Replication" do setup). Sem ele as procedures de replicação não existem.
2. **SQL Server Agent ligado** e em inicialização automática nas duas instâncias. Os agentes de replicação são jobs do Agent.
3. **Autenticação (modelo SQL Authentication)**. A replicação tem duas camadas de autenticação, e só a primeira vira SQL auth:
   - Camada 1 (conexões SQL dos agentes ao publisher/distributor/subscriber): usa um login SQL. Crie na Srv-Jd-Figueira o login `repl_user` (o arquivo 01, seção 0, já faz isso). É ele que a central usa para alcançar a substação e que os agentes locais usam no publisher. Use a mesma senha nos arquivos 01 e 02.
   - Camada 2 (conta de sistema que roda o job do agente e acessa o share): é sempre Windows. O job do Distribution Agent na central roda sob uma conta Windows (`@job_login`), que precisa ler o share de snapshot da substação. Isso não vira login SQL.
4. **Share de snapshot na Substação**: crie a pasta (ex.: `D:\repldata`) e compartilhe como `\\Srv-Jd-Figueira\repldata`. Como substação e central não compartilham domínio, a conta Windows do job da central precisa conseguir ler esse share. Escolha uma opção:
   - Conta local espelhada: a mesma conta Windows (mesmo nome e senha) criada na central (roda o job) e na substação (com leitura no share). O Windows faz pass-through.
   - Ou entrega do snapshot por FTP (`@use_ftp = 1` no agente e parâmetros FTP na publicação), evitando o share Windows.
5. **Firewall (ponto central da arquitetura)**: libere apenas Central para Substação.
   - Porta da instância SQL da Substação (1433 ou a porta customizada).
   - Acesso ao share de snapshot (porta 445/UNC), ou FTP se preferir transferir o snapshot por FTP.
   - Nenhuma regra no sentido Substação para Central.
6. **Criptografia do canal WAN**: TLS nas conexões SQL ou VPN. Se usar VPN, configure o firewall para permitir apenas sessões iniciadas pela Central.
7. **Database Mail na Substação** (apenas se for usar o alerta do arquivo 06): habilite o recurso e crie um profile SMTP.
8. **Chaves primárias e rowguid**: o banco 1 (transacional) só publica tabelas com PK; o arquivo 01 lista as sem PK no início, decida antes (criar PK ou deixar de fora). O banco 2 (merge) não exige PK, mas cria a coluna rowguid e triggers em cada tabela publicada (mudança de schema).

## Etapa 1: Preparar nomes e valores

Abra os seis arquivos e troque os valores entre `<...>` e os nomes de exemplo pelos reais. Servidores: `Srv-Jd-Figueira`, `DISMONTFLIC\MSSQLSERVERTT`. Bancos: `ecm_copel_jdfigueira` (banco 1), `sigmaecm_copel_figueira` e `sigmaecm_copel` (banco 2). Mais: `repl_user` e sua senha, a conta Windows do Agent da Central, o share `\\Srv-Jd-Figueira\repldata`, o profile de e-mail e o banco administrativo `<DBA>`. No arquivo 03, troque `<Tabela1>`, `<Tabela2>` pelos nomes reais das tabelas específicas do merge.

## BANCO 1 (transacional, só leitura na central)

### Etapa 2: Substação (arquivo 01)

Conecte na **Substação** e execute `01_Srv-Jd-Figueira_ecm_transacional_setup.sql` em ordem. Ele cria o login `repl_user`, o Distributor local (tudo SQL Auth), o Log Reader Agent, a publicação transacional, publica todas as tabelas com PK, registra a assinatura pull e dispara o snapshot. Aguarde o snapshot concluir (a consulta no fim da seção 6 mostra o andamento) antes de seguir.

Atenção: o distribuidor e o `repl_user` criados aqui também atendem o banco 2. Por isso este arquivo é sempre o primeiro a rodar.

### Etapa 3: Central (arquivo 02)

Só depois do snapshot pronto, conecte na **Central** e execute `02_CENTRAL_ecm_transacional_assinatura.sql`. Ele cria a assinatura pull, o job do Distribution Agent e inicia a primeira sincronização. Lembre: `ecm_copel_jdfigueira` na central é só consulta, ninguém pode gravar nessas tabelas.

## BANCO 2 (merge, bidirecional)

### Etapa 4: Substação (arquivo 03)

Conecte na **Substação** e execute `03_Srv-Jd-Figueira_sigma_merge_setup.sql`. Ele habilita merge publish, cria a publicação merge, adiciona as tabelas específicas (preencha a lista), registra a assinatura pull e dispara o snapshot. Leia os 3 avisos no fim do arquivo antes de produção: mudança de schema (rowguid mais triggers), dados que já existem na central e quem vence o conflito.

### Etapa 5: Central (arquivo 04)

Depois do snapshot do merge, conecte na **Central** e execute `04_CENTRAL_sigma_merge_assinatura.sql`. Ele cria a assinatura merge pull (com prioridade) e o job do Merge Agent. Aqui as duas pontas passam a poder editar as mesmas tabelas, e o merge reconcilia.

## Etapa 6: Validar (arquivo 05)

Execute `05_monitoramento_validacao.sql` nos servidores indicados em cada bloco. A primeira parte valida o banco 1 (tracer token, backlog, contagem de todas as tabelas). A parte final (seção MERGE) valida o banco 2 (status da assinatura merge, histórico do Merge Agent e conflitos).

## Etapa 7: Monitoramento contínuo do banco 1 (arquivo 06)

Conecte na **Substação** e execute `06_Srv-Jd-Figueira_health_check_alerta.sql`. Cria a tabela de histórico, a procedure de coleta, o job a cada 5 minutos e o alerta por e-mail quando latência ou backlog passam do limite. Esse health check é do banco 1 (transacional); o merge é acompanhado pelas consultas da seção MERGE do arquivo 05. Deixe coletando alguns dias e ajuste os limites ao volume real.

## Etapa 8: Outras substações

Para cada substação nova, duplique os arquivos trocando o nome do servidor (SRV<NomeSubestacao>), dos bancos e das publicações. Cada substação é um Publisher independente, e na central cada uma tem seu par de bancos de destino.

## Checklist final

1. Componente de replicação instalado nas duas instâncias.
2. SQL Server Agent ligado nas duas.
3. Login `repl_user` criado na Substação e conta Windows do agente definida na Central.
4. Share de snapshot criado na Substação com leitura para a Central.
5. Firewall liberado apenas Central para Substação.
6. Canal WAN criptografado.
7. Banco 1: tabelas sem PK tratadas.
8. Banco 2: tabelas específicas listadas no arquivo 03 e o vencedor do conflito decidido.
9. Banco 2: avaliado o impacto do rowguid/triggers e dos dados que já existem em `sigmaecm_copel`.
10. Snapshot inicial concluído antes de criar cada assinatura na Central.
11. Banco 1 validado (backlog perto de zero, contagens batendo) e health check ativo.

## Problemas comuns

1. **A Central não lê o snapshot**: quase sempre é permissão no share ou firewall na porta 445. Teste abrindo `\\Srv-Jd-Figueira\repldata` a partir da Central com a conta do agente.
2. **Agente falha ao conectar na Substação**: verifique o login `repl_user`, a porta SQL liberada e, se usar instância nomeada, o SQL Browser ou a porta fixa.
3. **Tabela não replicou no banco 1**: confira se ela tem PK. Sem PK, não entra no transacional (use a lista do arquivo 01, seção 4.1).
4. **Tabela nova no banco 1 não aparece**: tabelas novas não entram sozinhas. Rode de novo a seção 4 do arquivo 01 e gere o snapshot.
5. **Latência alta só no trecho Distributor para Subscriber**: o gargalo é a rede ou o agente na Central, não a leitura do log na Substação.
6. **Conflitos no banco 2 (merge)**: consulte a seção MERGE do arquivo 05 (`MSmerge_conflicts_info` e `sp_helpmergeconflictrows`). Quem vence segue a prioridade da assinatura; por padrão, a subestação.
7. **Erro 8145 ao criar o Distribution Agent** ("@publisher_security_mode is not a parameter"): nesta versão do SQL, `sp_addpullsubscription_agent` (transacional) não aceita os parâmetros de login do publisher. Passe só os do distribuidor (`@distributor_security_mode/@distributor_login/@distributor_password`). O agente de merge aceita, o transacional não.
8. **Erro 20084 "could not connect to Subscriber" com o agente em loop de retry, central fica em 0 tabelas**: a conta Windows do job (`@job_login`) não tem login no SQL da central. O agente conecta no subscriber local por Windows Auth com essa conta. Crie o login dela na central e dê db_owner no banco de destino (bloco comentado nos arquivos 02 e 04). Também: use o formato `host\conta` no `@job_login`, não `.\conta`.
