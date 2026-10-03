# Validação Passo a Passo — Detalhe

Detalhe completo de cada item da "Referência Rápida" do `SKILL.md`. A ordem dos blocos é definida lá.

## O Coletor Faz os Blocos 3 a 10

```bash
python scripts/coletar.py "<pasta>"        # relatório legível
python scripts/coletar.py "<pasta>" --json # mesma coisa em JSON
```

O que ele já entrega, pronto: empresa (4 fontes) · estrutura · sequências · tabela de módulos por GUID com versões · ativos · engenharia · comunicação · item provisório do SDG · lista de achados.

Os blocos abaixo descrevem **o que ele confere e por quê** — servem para interpretar a saída, decidir o que vira item e conferir à mão quando ele marcar `??` ou falhar. **Não reimplementar a extração.**

Opções: `--sync` / `--e3` forçam o modo quando a dedução automática estiver errada.

## Onde Achar Cada Coisa

Tabela de referência para **todas** as buscas desta skill. Os arquivos passam de 6000 linhas — nunca ler inteiro, sempre buscar por estes padrões.

### Módulo (GUID)

| Fonte | Padrão a buscar |
|---|---|
| `00-INITIAL-SCRIPTS/*-fl.sql` | `DECLARE @ModuloId UNIQUEIDENTIFIER = '<GUID>'` |
| `00-INITIAL-SCRIPTS/*-VersaoRecurso.sql` | `SET @RecursoId = '<GUID>'` com `@RecursoTipo = 1` |
| `02-GROUPS/*-GruposPadrao.sql` | `DECLARE @ModuloId UNIQUEIDENTIFIER = '<GUID>'` |
| `03 - JSONS/*-sigma-sync-import.json` | `modules[0].id` — **não** `fields[].moduleId`, que aparece antes no arquivo |
| `01-BACKBONE/001_*.sql` | `SET @ModuloId = N'<GUID>'` |

### Versão do módulo

| Fonte | Padrão | Notação |
|---|---|---|
| `*-VersaoRecurso.sql` | `DECLARE @TagVersaoMapa VARCHAR(50) = 'vN-MDB'` | `vN-MDB` |
| `*-GruposPadrao.sql` | `DECLARE @VersaoModulo NVARCHAR(500) = N'vN-MDB'` | `vN-MDB` |
| `001_*.sql` | `SET @VersaoModuloAtivo = N'vN-MDB'` | `vN-MDB` |
| `*-sigma-sync-import.json` | `"versions": ["N.0"]` | `N.0` |
| `*_sync.json` | `"ModuleVersion": "N.0"` | `N.0` |

### Outros

| O quê | Onde | Padrão |
|---|---|---|
| `E3Lib` do módulo | `*-fl.sql` | `E3Lib = '<ALIAS>'` |
| Ativo | `001_*.sql` | `SET @AtivoId = N'<GUID>'` |
| Ativo | `*_config.sql` | GUIDs dentro de `INSERT INTO #Ativos...(AtivoId) VALUES (...)` |
| Ativo | `hierarchy_export.json` | `Ativos[].Id` e `Ativos[].Identificador` |
| Módulo-ativo | `001_*.sql` | `SET @ModuloAtivoId = N'<GUID>'` |
| Módulo-ativo | `*_sync.json` | `"AssetModuleId": "<GUID>"` |
| Módulo-ativo | `hierarchy_export.json` | `ModulosAtivos[].Id` |
| Grupo de campos | `*-sigma-sync-import.json` | `fieldGroups[].id` — o array **do topo**, cujos itens são objetos |
| Grupo de campos | `*_sync.json` | `FieldGroupId` dentro de `Associations[]` |

## 1. Deduzir o Caminho da Pasta

**Antes de qualquer pergunta ou leitura de arquivo**, deduzir o caminho a partir da pasta aberta no VSCode. Nunca perguntar o caminho ao usuário. Usar essa pasta de topo como raiz de todas as verificações.

Se a pasta aberta contiver mais de uma pasta de empresa candidata, perguntar qual delas junto com as perguntas iniciais (bloco 2).

## 2. Deduzir e Confirmar

Deduzir primeiro, perguntar depois — e fazer tudo em uma única chamada (AskUserQuestion), já com a dedução marcada como resposta provável.

- **4NET ou 4WEB?** — não é dedutível. Pergunta de verdade.
- **Rev ou 1.0?** — existe `01-BACKBONE/Rev *` ⇒ Rev, e o número vem do nome da pasta. Não existe ⇒ 1.0.
- **Sync ou E3?** — `*_sync.json` presente e `E3/` ausente ⇒ Sync. `E3/` com `.prj` e `.dll` ⇒ E3.

**Divergência entre dedução e resposta é achado.** Se o usuário responde `Rev 1.3` e não existe pasta `Rev 1.3`, reportar como item `PASTA` — não acreditar na resposta e seguir.

## 3. Derivar o Nome da Empresa

O relatório precisa de `<EMPRESA>` no nome do arquivo. Derivar de quatro fontes e conferir que batem entre si:

1. nome da pasta aberta → ex. `ecm_global_technology_yermarus_tps`
2. `hierarchy_export.json` → `Empresas[0].Nome` e `Instalacoes[0].Nome`
3. `client/*-create-database-client.sql` → `CREATE DATABASE [<banco>]`
4. prefixo dos arquivos de `01-BACKBONE/`

Divergência entre as quatro é achado real — indica deploy apontando para banco errado. Item `ARQ`.

Normalizar para o nome do relatório: espaços → `-`, sem acento.

## 4. Conferir a Estrutura de Pastas de Topo

**4NET — obrigatórias:**
- `client/`
- `DB/` com `00-INITIAL-SCRIPTS/`, `01-BACKBONE/`, `02-GROUPS/` e `03 - JSONS/`

**Não obrigatória:** `system/` — ausência não é achado.

**Tolerada:** `escopo/` — nunca vira item, e a ausência também não é achado.

Casar nomes com tolerância de grafia (`03[ -_]*JSONS?`). Variação de grafia é nota `- [x]`, nunca `- [ ]`.

Pasta realmente fora do padrão → item `PASTA`.

> **4WEB:** estrutura ainda não definida. Se o usuário responder 4WEB, **parar e avisar** — não inferir estrutura.

## 5. Arquivos Obrigatórios

**Sempre, para 4NET:**
- `client/*-create-database-client.sql` — casar pelo sufixo, ignorando a quantidade de dígitos do prefixo. Ausente → `ARQ`.
- `DB/01-BACKBONE/*-perfil-root.sql` — ausente → `ARQ`. **Não vem do gerador**, então ausência é sempre erro de quem montou.

**Se Rev:**
- `DB/01-BACKBONE/Rev X.X/` — pasta com o número exato confirmado no bloco 2. Ausente → `PASTA`.

## 5.1 Extrair os Módulos do `001`

Localizar `01-BACKBONE/001[ _-]*.sql` (regex — o nome é `001_<empresa>.sql`, com underscore). Exigir **exatamente um** arquivo com prefixo `001`; nenhum ou mais de um → `ARQ`, e pular esta etapa.

O arquivo traz um bloco por par ativo × módulo:

```sql
--Adicionando ModuloAtivo
SET @ModuloAtivoId = N'<GUID do módulo-ativo>'
SET @ModuloId      = N'<GUID do módulo>'
...
SET @VersaoModuloAtivo = N'vN-MDB'
```

Extrair, por bloco: `ModuloAtivoId`, `ModuloId` e `VersaoModuloAtivo`. O conjunto de módulos ativos é o `distinct` dos `@ModuloId`. Linha comentada (`--`) não conta.

> **Varrer sequencialmente, acumulando por bloco.** Regex que atravessa blocos emparelha errado e produz dezenas de divergências falsas num arquivo correto.

> **Não existe seção `--MODULOS`** nesse arquivo. Se alguém procurar por ela, não vai achar.

## 5.2 Tabela de Módulos por GUID

Montar uma tabela indexada pelo **GUID**, com uma coluna por fonte:

| GUID | Alias arq. | `E3Lib` | `-fl` | `-VersaoRecurso` | `-GruposPadrao` | `-sigma-sync-import` | no `001` |

O conjunto de GUIDs precisa ser **idêntico** nas cinco fontes. GUID presente em uma e ausente em outra → item `ARQ`, nomeando módulo e fonte que falta.

### Exceção: módulo com regra de `fieldGroups`

Os módulos desta **lista fechada** (por `E3Lib`) **não têm sigma próprio**:

| `TM1` | `TM2` | `AVR` | `AVRGROUP` | `SDV` | `TMV` |
|---|---|---|---|---|---|

Neles a variante é um grupo dentro do sigma da **família**, e esse sigma carrega o `modules[].id` e o `modules[].identifier` de **um** dos membros. Então o GUID fecha em **4 fontes** (`-fl`, `-VersaoRecurso`, `-GruposPadrao`, `001`), e a ausência no sigma é nota `- [x]`, **nunca** achado. Quem confere a ligação com o sigma é o bloco 8.6, pelo `FieldGroupId`.

Exemplo real: `002 - AVRGROUP-sigma-sync-import.json` declara `"id": "78B5F19A…"` — o GUID do **AVR** — e seis `fieldGroups` `GROUP_1`…`GROUP_6`. O GUID do AVRGROUP não aparece em sigma nenhum, e está certo.

A lista vale **nos dois sentidos**: módulo fora dela que venha com `FieldGroupId` preenchido é achado (bloco 8.6). Módulo novo com grupo só passa a ser aceito depois de entrar na lista — aqui e em `COM_FIELDGROUP`, no `coletar.py`.

**O nome do arquivo não é prova.** O alias no nome pode diferir do `E3Lib` (ex.: `07-TM-fl.sql` com `E3Lib = 'NTM'`). Quando isso acontecer:

- GUID fecha em todas as fontes → nota `- [x]` registrando a divergência de alias, com o GUID como evidência.
- GUID não fecha → item `ARQ`.

## 5.3 Versão do Módulo

A mesma versão aparece em cinco lugares, em duas notações. Extrair o número de cada uma e comparar:

- de `vN-MDB` → pega o `N` (`v13-MDB` → `13`)
- de `"N.0"` → pega o `N` (`"13.0"` → `13`)

Todos iguais → `- [x]`. Divergência → item `ARQ` mostrando as duas versões lado a lado.

**Por que importa:** se o `GruposPadrao` roda com versão diferente da cadastrada, o `DELETE ... WHERE VersaoModulo = @VersaoModulo` do início do script não apaga nada e os grupos antigos ficam duplicados. Passa no deploy, aparece na tela do cliente.

**Dois formatos de `VersaoRecurso`** — o parser precisa cobrir os dois, senão reporta ausência onde não há:
- com variável: `DECLARE @TagVersaoMapa VARCHAR(50) = 'vN-MDB'`
- inline: `TagsVersaoMapa LIKE '%vN-MDB%'`

**`@TagVersaoFirmware`** (`'v13[fw1.11R1]'`): conferir só o prefixo `vN`, que tem que bater com a versão do módulo. O sufixo entre colchetes é versão de firmware, outro número, sem par em nenhuma outra fonte — ignorar.

## 5.4 Lacunas na Numeração

**Em toda pasta cujos arquivos são numerados**, a sequência vai de `001` (ou `01`) até o maior número, sem lacuna. A numeração é **ordem de execução**, não organização.

| Pasta | Sequência esperada |
|---|---|
| `DB/00-INITIAL-SCRIPTS/` | `01`…`NN` |
| `DB/01-BACKBONE/` | `001`…`NNN`, mais `999` (perfil-root, o último a executar) |
| `DB/02-GROUPS/` | `01`…`NN` |
| `DB/03 - JSONS/` | `01`…`NN` (sigma-sync-import), depois `005`/`006` (sync e hierarchy, os últimos) |
| `client/` | arquivo único |

O salto para `999` **não** é lacuna — é posição final reservada. Em `03 - JSONS/` a sequência é única e contínua, apesar do zero à esquerda variar.

Lacuna → item `ARQ`:

```
- [ ] ARQ-NN — Lacuna na sequência de 01-BACKBONE/ · 🔴 aberto
  Esperado: 001…055 sem falhas · Encontrado: 030 ausente
  Onde: DB/01-BACKBONE/
```

**Por que nenhuma outra conferência pega isso:** se o script de config de um ativo específico não foi copiado, o script "mãe" do módulo continua presente e as outras conferências passam. A lacuna é o único sinal.

**Limitação, registrar como nota:** a skill só confere até o maior número existente. Se os últimos scripts ficaram para trás, a sequência fecha sem lacuna. O bloco 7 cobre parte disso.

## 5.5 GruposPadrao

Para cada módulo com `.fl` em `00-INITIAL-SCRIPTS/`, deve existir um `*-GruposPadrao.sql` em `02-GROUPS/` com o mesmo GUID. Ausente → item `ARQ`.

Já coberto pela tabela do 5.2 — esta é a coluna `-GruposPadrao`.

## 6. Ativos

**6.1 — `001` ↔ `hierarchy_export.json`**

O conjunto de `SET @AtivoId = N'…'` do `001` deve ser igual a `Ativos[].Id` do `hierarchy_export.json`. Diferença → item `ARQ` listando os GUIDs órfãos.

**6.2 — `_config.sql` ↔ conjunto validado**

Todo `AtivoId` citado nos `*_config.sql` de `01-BACKBONE/` deve pertencer ao conjunto de 6.1. Os scripts listam os ativos assim:

```sql
INSERT INTO #AtivosParaConfigurarModulo (AtivoId)
VALUES ('<GUID>');
```

**Por que conferir:** o script não valida nada. GUID errado faz o cursor rodar sobre tabela vazia, o script termina com sucesso e **o módulo não é configurado naquele ativo** — sem erro, sem aviso. Pipeline verde, cliente sem o módulo.

GUID fora do conjunto → item `ARQ`, nomeando arquivo e GUID.

**Inverso, como nota:** ativo que não aparece em nenhum `_config.sql` de um módulo está sem aquele módulo configurado. Pode ser intencional → `- [x]` informativo, não problema.

## 7. Scripts de Engenharia

Padrões em `01-BACKBONE/`:

| Padrão | Papel |
|---|---|
| `001_<empresa>.sql` | backbone / hierarquia |
| `NNN_<empresa>_eng_<modulo>.sql` | habilita o módulo de engenharia |
| `NNN_<empresa>_<ativo>_eng_<modulo>_config.sql` | parametriza o módulo por ativo |
| `NNN_<empresa>_<ativo>_eng_chroma_fisico.sql` | chroma, direto por ativo |
| `NNN_<empresa>_temperatura_ambiente.sql` | temperatura ambiente, todos os ativos |
| `999_<empresa>_perfil-root.sql` | perfil root |

**Conferência cruzada:** as seções `Configuracoes*Configurador` **preenchidas** no `hierarchy_export.json` devem ter script de engenharia correspondente em `01-BACKBONE/`; as **vazias** não devem ter.

| Seção no `hierarchy_export.json` | Script |
|---|---|
| `ConfiguracoesEficienciaResfriamentoConfigurador` | `eng_eficiencia_do_resfriamento_cooling_efficiency` |
| `ConfiguracoesEnvelhecimentoIsolacaoConfigurador` | `eng_envelhecimento_isolacao_ageing` |
| `ConfiguracoesGradienteFinalConfigurador` | `eng_gradiente_final_do_enrolamento_forecast` |
| `ConfiguracoesSimulacaoCargaConfigurador` | `eng_simulacao_de_carga_hypothetical_present_condition` |
| `ConfiguracoesManutencaoResfriamentoConfigurador` | `eng_manutencao_do_resfriamento_fan` |
| `ConfiguracoesChromaFisicoConfigurador` | `eng_chroma_fisico` |
| `ConfiguracoesTemperaturaAmbienteConfigurador` | `temperatura_ambiente` |
| `ConfiguracoesAguaPapelConfigurador` | *(nome não conhecido — ver abaixo)* |
| `ConfiguracoesManutencaoComutadorConfigurador` | *(nome não conhecido — ver abaixo)* |
| `ConfiguracoesDiferencialTemperaturaComutadorConfigurador` | *(nome não conhecido — ver abaixo)* |

Divergência → item `ARQ`.

> **Três seções sem nome de script mapeado.** Na produção de referência, `AguaPapel`,
> `ManutencaoComutador` e `DiferencialTemperaturaComutador` estavam **vazias**, então não há
> script correspondente para saber o nome. Se alguma delas vier **preenchida** numa produção,
> conferir que existe *algum* script de engenharia novo em `01-BACKBONE/` e **perguntar ao
> usuário** qual é o nome esperado — **não adivinhar** o nome do arquivo.

> **Exceção, não cobrar:** `eng_chroma_fisico` e `temperatura_ambiente` **não têm** script "mãe" `NNN_<empresa>_eng_<modulo>.sql`, só os por ativo. É o padrão desses dois módulos.

## 8. Comunicação — `sync.json`

Só quando a comunicação é **Sync**. O `*_sync.json` é o mapa da comunicação inteira: se estiver inconsistente, o deploy sobe e nada comunica.

### 8.1 `001` ↔ `sync.json` — a conferência mais importante

Cada bloco `ModuloAtivo` do `001` corresponde a **um IED** do `sync.json`, ligados pelo **ModuloAtivoId**:

| No `001_*.sql` | No `*_sync.json` |
|---|---|
| `SET @ModuloAtivoId = N'<GUID>'` | `"AssetModuleId": "<GUID>"` |
| `SET @ModuloId = N'<GUID>'` | `"ModuleIdentifier"` = o `E3Lib` desse GUID |
| `SET @VersaoModuloAtivo = N'vN-MDB'` | `"ModuleVersion": "N.0"` |
| `SET @HasOscillography = 0` | `"HasOscillography": false` |
| `SET @SetGroup = NULL` | `"TableSufix": null` |

Três conferências:

1. Todo `ModuloAtivoId` do `001` existe como `AssetModuleId` no `sync.json`. Falta → módulo instalado no banco que **não vai comunicar**.
2. Todo `AssetModuleId` do `sync.json` existe como `ModuloAtivoId` no `001`. Falta → IED apontando para módulo-ativo que **não existe no banco**.
3. Para cada par, módulo e versão batem.

Divergência → item `ARQ`, listando os GUIDs órfãos de cada lado.

**É a conferência que garante que banco e comunicação descrevem a mesma instalação**, e é o erro mais comum: o gerador às vezes entrega menos IEDs do que o `001` tem módulos-ativo.

### 8.2 Ativos e módulos do `sync.json`

- Todo `"ModuleIdentifier"` tem módulo correspondente — **não pelo nome do arquivo**. Sem correspondente → IED apontando para módulo inexistente → `ARQ`.

  **O `ModuleIdentifier` vem do `modules[].identifier` do sigma, não do `E3Lib`.** Numa família os dois divergem de propósito: `TM1` e `TM2` são `E3Lib`, mas o sigma dos dois diz `"identifier": "TM"`, e é `TM` que aparece no `sync.json`. O mesmo com `AVRGROUP`, que vira `AVR`. Casar contra a união dos `modules[].identifier` de todos os sigmas **mais** os `E3Lib` — o `E3Lib` entra porque nem todo módulo tem sigma próprio. Cobrar só o `E3Lib` produz achado falso em toda produção com família.
- Todo `"AssetIdentifier"` existe como `Ativos[].Identificador` no `hierarchy_export.json`. Sem correspondente → `ARQ`.

### 8.3 `Identifier` — NÃO validar formato

**O `Identifier` do IED não precisa ser um GUID.** Valores como `"sdg"` ou um GUID incompleto
são aceitáveis — não são achado e **não devem ser reportados**.

Conferir apenas que são **únicos** dentro do arquivo (bloco 8.5). Formato, nunca.

### 8.4 `Label`

Reconstruir o `Label` esperado e comparar:

```
{Empresa} - {Instalação} - {Ativo} - {ModuleIdentifier}
```

Empresa e instalação vêm do `hierarchy_export.json`; o nome do ativo vem do `AssetIdentifier`. Divergência → item `ARQ`:

```
- [ ] ARQ-NN — Label do IED NN não corresponde ao módulo · 🔴 aberto
  Esperado: "<Empresa> - <Instalação> - ST#1 - NTM"
  Encontrado: "<Empresa> - <Instalação> - ST#1 - SDG"
  Onde: DB/03 - JSONS/<arquivo>_sync.json, IED NN
```

Gravidade baixa — é texto de exibição —, mas é sintoma de bloco copiado sem ajustar, e costuma vir acompanhado de problema no `Identifier`.

### 8.5 Organização interna — conferir como nota

| Nível | Regra |
|---|---|
| `Name` | nome da **instalação** do `hierarchy_export.json` |
| `DataSources` | um só, representando o gateway |
| `Ieds` | um por aparelho |
| Ordem dos `Ieds` | agrupados por ativo, em blocos contíguos |
| `Associations` | uma por `ModuloAtivo` — **várias** no mesmo IED quando o módulo tem grupo (8.6) |
| `Identifier` / `AssetModuleId` | únicos no arquivo inteiro |
| `DatabaseConnectionId` | sempre `null` — valor diferente → `ARQ` |

**Não conferir:** `SourceIdentifier` e `SerialNumber` — detalhe, fora de escopo.

**`FieldGroupId`**: conferido pelo bloco 8.6.

**Não transformar em regra** o conjunto de módulos por tipo de ativo (ex. "monitor de bucha leva BMC + SDG"). Isso é desenho de cada instalação, não padrão 4NET — quem valida o conjunto é o bloco 8.1.

### 8.6 `FieldGroupId` — grupo de campos do IED

**Um IED é o aparelho; cada associação dele é um `ModuloAtivo`.** Aparelho sem grupo vira uma associação. Aparelho **com** grupo vira **uma associação por grupo**, todas no mesmo ativo, cada uma com seu `AssetModuleId` e seu `FieldGroupId`.

```
AVR_V2 no Cemirim:  1 IED · 1 ativo · 7 associações
                    └─ 7 AssetModuleId distintos, 7 FieldGroupId distintos
```

Ou seja: **o grupo é divisão interna do aparelho**, não a variante do modelo. No TM1 de Guaraciaba há um grupo só, e aí o IED tem uma associação — é o caso degenerado, não a regra.

Quem tem grupo declara no próprio sigma, num array `fieldGroups` **no topo do arquivo**:

```json
"fieldGroups": [
  { "id": "976996db-5ea2-4917-90b1-48db1899d36c",
    "identifierSuffix": "1",
    "description": "TM1 - Monitor de Temperatura do Óleo e Enrolamentos",
    "moduleId": "dbdf1f02-de9f-4551-9233-c45b5bcb92be",
    "moduleVersion": "1.0" }
]
```

**Quem decide é uma lista fechada de módulos, por `E3Lib`:**

| `TM1` | `TM2` | `AVR` | `AVRGROUP` | `SDV` | `TMV` |
|---|---|---|---|---|---|

A mesma lista está em `COM_FIELDGROUP`, no `coletar.py` — mexeu numa, mexer na outra.

O módulo de cada associação sai do `001`: `AssetModuleId` → bloco → `@ModuloId` → `E3Lib`. **Não** usar o `ModuleIdentifier` do IED para isso: numa família ele é o mesmo para os dois módulos (`TM` cobre `TM1` e `TM2`), então não distingue a associação.

| Módulo da associação | `FieldGroupId` esperado |
|---|---|
| na lista | preenchido, e o GUID existe na **união** dos `fieldGroups[].id` de **todos** os sigmas da pasta |
| fora da lista | `null` |

Qualquer um dos dois lados fora disso → item `ARQ`, nomeando o IED e a associação.

> **Procurar o grupo na união dos sigmas, não no sigma do próprio módulo.** A variante não tem sigma próprio (5.2): o grupo do `TM2` mora no arquivo cujo `modules[].id` é o do `TM1`. Procurar só no sigma do módulo acusa "grupo inexistente" em produção correta.

Conferir junto:

- `FieldGroupId` **não se repete** dentro do mesmo IED — uma associação por grupo.
- `fieldGroups[].moduleId` e `moduleVersion` batem com o `modules[0]` do mesmo arquivo.
- Todo `fields[].fieldGroups` aponta para um `fieldGroups[].id` existente.

**Dois `fieldGroups` no mesmo arquivo, não confundir:** o do topo traz **objetos** (`[{ "id": … }]`); o de dentro de `fields[]` traz **só strings** (`["976996db…"]`). Casar pelo `{` — o padrão do bloco 8.1 serve.

**Por que importa:** o `FieldGroupId` é o que amarra cada `ModuloAtivo` ao conjunto de campos certo. Errado ou vazio num módulo que tem grupo, o registro sobe e lê os campos do grupo errado — ou nenhum.

> **Nunca abrir item por contagem de associação.** IED com várias associações é o normal em módulo da lista. O cruzamento do 8.1 percorre **associação por associação** — quem iterar por IED e descartar os de associação múltipla acusa dezenas de "módulo instalado que não vai comunicar" numa produção correta.

**Resultado nas produções de referência:**

| Produção | Módulos com `fieldGroups` | Como aparece |
|---|---|---|
| `ecm-guaraciaba-marimbondo` | TM (v1.0), 1 grupo | 7 IEDs de TM com o mesmo `FieldGroupId`; os outros 18 `null` |
| `[PROD] - CEMIRIM HOLAMBRA SYNC` | SDV (4), AVR_V2 (7), TMV (4) | 13 IEDs → 25 associações; 15 com `FieldGroupId`, todos distintos; os outros 8 módulos `null` |
| `ecm_vale_se_ponta_madeira` | AVR+AVRGROUP (7), TM1+TM2 (2) | 38 IEDs → 80 associações; 42 com `FieldGroupId`, os outros 38 `null` |

## 9. Comunicação E3

Se a comunicação for E3, conferir independentemente do tipo (4NET ou 4WEB):

- `E3/` existe na raiz da pasta da empresa → ausente, item `PASTA`.
- `E3/*.prj` — ao menos um. Ausente → item `ARQ`.
- `E3/*.dll` — ao menos um. Ausente → item `ARQ`.

Se a comunicação for **Sync**, a ausência de `E3/` é esperada — registrar como `- [x]` (`Comunicação Sync → pasta E3/ não aplicável`), não como achado. A **presença** de `.prj` / `.dll` numa produção Sync é que vira item.

## 10. Item Provisório — `Funcionalidades` do SDG

> ⚠️ **Provisório — contorna bug conhecido do gerador.** Baseado em uma única produção de referência. **Remover quando o bug for corrigido na origem.**

Em todo bloco `ModuloAtivo` do `001` cujo módulo seja o **SDG** (identificado pelo `E3Lib`, não pelo nome do arquivo), `@ModuloAtivoFuncionalidades` deve ser **`1`**.

`@ModuloAtivoFuncionalidades` é campo de bits — `Geral = 1, Parametro = 2, Grafico = 4`. O gerador emite `7` (os três) para o SDG, mas o SDG é gateway: só tem Geral.

Valor `7` no SDG → item `ARQ`, apontando que é o bug conhecido:

```
- [ ] ARQ-NN — Funcionalidades do SDG com valor do gerador · 🔴 aberto
  Esperado: @ModuloAtivoFuncionalidades = 1 (SDG é gateway, só Geral)
  Encontrado: = 7, em N blocos
  Onde: DB/01-BACKBONE/001_*.sql
```

**Limites desta regra — não ultrapassar:**
- Vale **só para o SDG** e **só para o valor `1`**.
- **Não** cobrar valores dos outros módulos. Eles variam por projeto e cobrar errado vira falso positivo em toda produção.
- Se aparecer produção legítima com SDG ≠ 1, a regra está errada e deve ser revista com o usuário.

## 11. Reportar o que Está Fora do Padrão

Qualquer pasta ou arquivo fora da estrutura esperada vira item `- [ ]` com prefixo `PASTA` ou `ARQ`. Não ignorar itens extras — podem indicar deploy incorreto ou sobra de versão anterior.

Lembrar que `ARQ` cobre **ausência e conteúdo inconsistente**: GUID órfão, versão divergente, ativo inexistente e identificador mal formado entram como `ARQ`.

## 12. Gerar o Relatório Final

Preencher o esqueleto de `report-template.md`. Nunca montar o relatório do zero. Ao final, informar ao usuário o caminho onde o relatório foi salvo e o resumo por ID.
