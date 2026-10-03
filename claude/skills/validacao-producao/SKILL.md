---
name: validacao-producao
description: Use when the user is starting or completing a production deployment, when a deploy task is about to be closed in Azure DevOps without confirmed evidence that required folders and files were verified in production, or when the user asks to validar, revalidar or conferir a estrutura de producao (4NET / 4WEB).
---

# Validação de Produção

## Visão Geral

Uma task de deploy não está pronta enquanto a estrutura de pastas e arquivos obrigatórios não for confirmada direto em produção. Teste passando ou pipeline verde não substituem essa conferência.

O que o gerador produz costuma estar certo. **O erro entra no que é editado à mão depois** — por isso as conferências que mais pagam são as que cruzam fontes (o `001` contra o `sync.json`) e as que validam formato (GUID). Priorizar essas.

## Quando Usar

- Iniciando um deploy em produção (4NET ou 4WEB)
- Antes de fechar uma task de deploy no Azure DevOps
- Quando alguém diz "já está em produção" sem mostrar a estrutura de pastas

**Não usar para:** tasks internas sem deploy em produção (ex: refatoração pura sem entrega).

## Restrições

- **Apenas validar e reportar — NUNCA modificar nada.** Todo problema encontrado vira um item `- [ ]` no relatório, para o usuário corrigir. A skill **não conserta**, mesmo quando a correção é óbvia e mesmo se o usuário parecer querer isso no meio da validação — se ele pedir correção, terminar a validação primeiro e perguntar depois, fora dela.

  **Sem exceção:** não editar script, não renomear arquivo, não criar pasta que falta, não reordenar numeração, não acertar JSON, não converter encoding ou fim de linha, não apagar arquivo extra. Nem como "pequeno ajuste", nem "já que estou aqui", nem porque o usuário vai ter que fazer de qualquer jeito.

  **O único arquivo que a skill cria ou atualiza é o relatório `Validacao-Producao-*.md`.** Mais nada, em lugar nenhum.
- **Verificar somente a pasta aberta no VSCode.** Não procurar fora dela — se um arquivo esperado não estiver lá, ele é um achado, não um motivo para procurar em outro lugar.
- **PROIBIDO: qualquer comando git** (`git log`, `git diff`, `git show`, `git status` ou outro). Usar apenas o que está na pasta aberta agora.
- **PROIBIDO: salvar ou persistir conteúdo dos arquivos avaliados** (scripts, configs, binários). Caminho literal e trecho curto de identificação (ex: a linha `DECLARE`) são permitidos no relatório. O único arquivo que a skill cria ou atualiza é o relatório `.md`.
- **NUNCA ler arquivo inteiro.** Os arquivos passam de 6000 linhas e 300 KB — ler tudo estoura o contexto e a validação para no meio. Usar busca dirigida pelos padrões da tabela "Onde Achar Cada Coisa" do `checklist.md`.
- **Sempre citar caminho entre aspas.** Há pastas com espaço (`DB/03 - JSONS/`) e arquivos com `#` no nome (`003_..._gt#2-_y_phase_...sql`) — sem aspas o caminho quebra ou é truncado.
- **Normalizar CRLF antes de comparar conteúdo.** Fim de linha diferente faz arquivos idênticos parecerem distintos.

## Escopo

A skill roda sobre a **pasta aberta no VSCode**. **NUNCA perguntar o caminho ao usuário** — deduzir da pasta aberta antes de qualquer outra pergunta. Se a pasta aberta contiver mais de uma pasta de empresa candidata, perguntar qual delas na mesma chamada das perguntas iniciais. O relatório é salvo na **pasta de topo dessa estrutura** (maior hierarquia disponível na pasta aberta).

## Antes de Começar

1. **Antes de qualquer pergunta ou leitura de arquivo, verificar se já existe `Validacao-Producao-*.md`** na pasta de topo aberta no VSCode. Se existir, é revalidação — ler o relatório inteiro e seguir "Revalidação". O cabeçalho já responde tipo, versão e comunicação; só confirmar com o usuário se algo mudou.
2. Se não existir relatório (primeira validação), **deduzir primeiro, perguntar depois**. Duas das três respostas estão na própria pasta:

   | Pergunta | Como deduzir |
   |---|---|
   | **4NET ou 4WEB?** | Não é dedutível — perguntar de verdade |
   | **Rev ou 1.0?** | Existe `01-BACKBONE/Rev *` ⇒ Rev (número vem do nome da pasta); não existe ⇒ 1.0 |
   | **Sync ou E3?** | `*_sync.json` presente e `E3/` ausente ⇒ Sync; `E3/` com `.prj` e `.dll` ⇒ E3 |

   Fazer **todas as perguntas em uma única chamada** (AskUserQuestion), já com a dedução marcada como resposta provável. **Divergência entre dedução e resposta é achado** — se o usuário responde `Rev 1.3` e não existe pasta `Rev 1.3`, isso é o problema que a skill deveria pegar, não um motivo para acreditar na resposta.

## Estrutura de Pastas

> **Padrão esperado**: as estruturas abaixo são obrigatórias. Qualquer pasta ou arquivo **fora desse padrão** vira item `- [ ]`. Independentemente disso, a skill **percorre todas as subpastas** para conferir se os arquivos obrigatórios estão presentes — arquivo obrigatório ausente é sempre reportado, mesmo que a estrutura pareça correta.

### 4NET — Versão 1.0

```
client/
└── NNN-create-database-client.sql      ← 2 ou 3 dígitos
DB/
├── 00-INITIAL-SCRIPTS/
│   ├── NN-<ALIAS>-fl.sql
│   └── NN-<ALIAS>-VersaoRecurso.sql
├── 01-BACKBONE/
│   ├── 001_<empresa>.sql               ← backbone / hierarquia
│   ├── NNN_<empresa>_eng_<modulo>.sql
│   ├── NNN_<empresa>_<ativo>_eng_<modulo>_config.sql
│   └── 999_<empresa>_perfil-root.sql   ← sempre 999, último a executar
├── 02-GROUPS/
│   └── NN-<ALIAS>-GruposPadrao.sql
└── 03 - JSONS/
    ├── NN-<ALIAS>-sigma-sync-import.json  ← um por módulo
    ├── NNN_<empresa>_sync.json            ← se Sync
    └── NNN_<empresa>_hierarchy_export.json
```

### 4NET — Rev (ex: Rev 1.3)

Igual ao 1.0, mais a pasta da revisão:

```
DB/01-BACKBONE/
└── Rev 1.3/   ← pasta com o número da rev informado
```

### Comunicação E3

Seja 4NET ou 4WEB, quando a comunicação é E3:

```
E3/
├── *.prj
└── *.dll
```

Quando a comunicação é **Sync**, a ausência de `E3/` é **esperada** — não é achado. O achado seria a **presença** de `.prj` / `.dll` numa produção Sync.

### Nomes de Pasta — Casar com Tolerância

Grafia de nome de pasta varia entre produções. Casar por padrão, nunca por string literal:

| Pasta | Padrão aceito |
|---|---|
| `03 - JSONS/` | `03[ -_]*JSONS?` — cobre `03-JSON`, `03 - JSONS`, `03_JSONS` |
| demais numeradas | mesmo tratamento: dígitos + separador flexível + nome |

Variação de grafia é ruído, **não** achado. No máximo uma nota `- [x]`, nunca `- [ ]`.

### Pastas Toleradas

- **`escopo/`** — área temporária com a planilha de referência do configurador (ex.: `TemplatePlanilhaEntradaConfigurador_*.xlsx`). **Nunca** vira item `PASTA`, e a ausência também não é achado.

### Não É Obrigatória

- **`system/`** — não faz parte do padrão. Ausência não é achado.

## Coletor — Rodar Primeiro

**Antes de conferir qualquer coisa à mão, rodar o coletor:**

```bash
python scripts/coletar.py "<pasta-da-produção>"
```

Ele lê a pasta inteira uma vez (~100 ms) e imprime um relatório compacto com estrutura, módulos por GUID, versões, sequências, ativos, engenharia e comunicação — já marcando `OK`, `!!` (achado), `??` (perguntar) e `--` (informativo).

**O coletor é somente leitura**: um único `open()` em modo `'r'`, nenhuma escrita. A saída vai para stdout — **não redirecionar para arquivo dentro da pasta de produção.**

**A divisão de trabalho:** o coletor extrai e compara; **a skill julga e escreve o relatório** — decide o que vira `- [ ]` e o que vira nota, conversa com o usuário e mantém o histórico da revalidação.

Não refazer à mão o que o coletor já fez. Reimplementar a extração a cada execução é lento e já produziu divergência falsa por emparelhar blocos errado. Conferir à mão só o que o coletor marcar `??`, ou se ele falhar.

## Referência Rápida — Passo a Passo

A ordem importa. O coletor cobre os passos 3 a 10. **Detalhe completo de cada item em `checklist.md`, nesta mesma pasta.**

| # | Verificação |
|---|---|
| 1 | Deduzir a pasta de topo a partir da pasta aberta no VSCode |
| 2 | Deduzir tipo/versão/comunicação e confirmar em uma única chamada |
| 3 | Derivar o nome da empresa e conferir que as 4 fontes batem |
| 4 | Conferir se a estrutura de pastas de topo bate com o padrão do tipo |
| 5 | Percorrer todas as subpastas e conferir os arquivos obrigatórios |
| 5.1 | Abrir `01-BACKBONE/001[ _-]*.sql` e extrair os módulos (`SET @ModuloId`) e as versões (`SET @VersaoModuloAtivo`) |
| 5.2 | Montar a tabela de módulos por **GUID** e conferir que o conjunto é idêntico nas 5 fontes — **4** nos módulos com regra de `fieldGroups`, que não têm sigma próprio |
| 5.3 | Conferir que a versão de cada módulo bate nas 5 fontes (`vN-MDB` ⇄ `N.0`) |
| 5.4 | Conferir que não há lacuna na numeração de **toda** pasta numerada |
| 6 | Ativos: `001` ↔ `hierarchy_export.json` ↔ `_config.sql` |
| 7 | Engenharia: seções `Configuracoes*Configurador` ↔ scripts em `01-BACKBONE/` |
| 8 | Comunicação: `001` ↔ `sync.json` (1:1 por `ModuloAtivoId`, **associação a associação**) e `Label` dos IEDs |
| 8.6 | `FieldGroupId` das associações ↔ lista fechada de módulos com regra de `fieldGroups` |
| 9 | Se E3: conferir pasta `E3/` com `.prj` e `.dll` |
| 10 | ⚠️ Provisório: conferir `@ModuloAtivoFuncionalidades = 1` nos blocos do **SDG** |
| 11 | Reportar como `- [ ]` tudo que estiver fora do padrão |
| 12 | Gerar o relatório final usando `report-template.md` e informar ao usuário |

> **Sobre o passo 10:** é contorno de um bug conhecido do gerador, não regra de arquitetura.
> Vale **só para o SDG** e **só para o valor `1`** — não cobrar valores dos outros módulos.
> **Remover da skill quando o bug for corrigido na origem.** Detalhe no `checklist.md`.

## Princípios de Conferência

Quatro regras que valem para a validação inteira:

1. **O GUID é a chave primária.** O nome do arquivo é só uma pista. O alias no nome pode diferir do `E3Lib` do módulo (ex.: `07-TM-fl.sql` com `E3Lib = 'NTM'`) — casar por nome produziria achado falso. Quando houver essa divergência, registrar como nota `- [x]`, não como problema; vira `- [ ]` só se o GUID não fechar.
2. **O número é ordem de execução.** Em toda pasta numerada, a sequência vai de `001` (ou `01`) até o maior número sem lacuna. O `999` do `perfil-root` é a posição final, não um buraco.
3. **O que o gerador não entrega é sempre achado real.** `999_*_perfil-root.sql`, `client/`, `00-INITIAL-SCRIPTS/`, `02-GROUPS/` e os `*-sigma-sync-import.json` não vêm do gerador — se faltam, alguém esqueceu de colocar.
4. **Família de módulo divide um sigma.** `TM1`/`TM2` e `AVR`/`AVRGROUP` têm `E3Lib` e GUID próprios no banco, mas um sigma só para a família — e a variante é um `fieldGroup` lá dentro. Por isso a variante **não** tem sigma próprio, e o `ModuleIdentifier` do `sync.json` é o mesmo para os dois (`TM`, `AVR`). Lista fechada em `COM_FIELDGROUP` (`coletar.py`) e no bloco 5.2 do `checklist.md`. Cobrar sigma próprio ou casar `ModuleIdentifier` com `E3Lib` produz achado falso.

## IDs dos Itens

Dois prefixos, e apenas dois:

- **`PASTA`** — estrutura de pastas.
- **`ARQ`** — arquivos: **ausentes ou com conteúdo inconsistente**. Cobre tanto arquivo que não existe quanto GUID órfão, versão divergente, ativo inexistente e identificador mal formado.

Nenhum ID é pré-atribuído a uma verificação específica — numerar **na ordem em que o problema é encontrado**, dentro de cada prefixo (`PASTA-01`, `PASTA-02`, `ARQ-01`, `ARQ-02`...). Número **nunca é reutilizado**, mesmo que o item seja resolvido.

## Revalidação

Quando já existe `Validacao-Producao-*.md` na pasta de topo. Formato do item (`Onde:`, `Histórico:`) em `report-template.md`.

1. **Ler o relatório inteiro** e listar todos os itens abertos (`- [ ]`): ID, status, `Onde:`, `Obs.:`. A nova rodada é `R<última + 1>` no painel.
2. **Reconferir cada item aberto** (🔴, 🟡) verificando se a pasta ou arquivo agora existe no caminho de `Onde:`:
   - Existe agora → ✅ `resolvido na R<n>`. Vira `- [x]` com uma linha `Agora:` confirmando.
   - Continua ausente → manter o status e acrescentar `R<n> continua` em `Histórico:`.
   - Parcialmente corrigido (ex: pasta existe mas o arquivo obrigatório ainda falta) → 🟡 `parcial`.
3. **Problema novo** (não está no relatório) → item novo com o próximo ID livre daquele prefixo, `Histórico: R<n> novo`.
4. **Atualizar o mesmo relatório** (nunca criar outro): acrescentar a linha de contexto `Revalidação (R<n>)`, nova linha no painel, reordenar cada seção (`- [ ]` por ID, depois `- [x]`). Nunca apagar item nem `Obs.:`.
5. Resumir a rodada ao usuário: resolvidos, parciais e novos, por ID.

## Relatório Final

Obrigatório ao fim de toda validação, inclusive a primeira. **O relatório é sempre escrito em português**, independentemente do idioma da conversa. **Formato e esqueleto em `report-template.md`, nesta mesma pasta** — preencher o esqueleto, não inventar o formato.

Ao terminar, **informar ao usuário**: o caminho onde o relatório foi salvo e um resumo por ID (abertos, parciais, resolvidos, novos).

## Fora de Escopo

Não validar, e não reportar como achado:

- **Encoding / mojibake** (`PadrÃ£o`, `M�dulo`). Existe em produções reais e não é problema de deploy. A skill não reporta e não corrige.
- **Caracteres especiais em nome de arquivo** (`#`). Não está definido se é proibido na 4NET — tratar só como armadilha técnica (aspas no caminho).
- **Fim de linha** (CRLF / LF). Irrelevante. Só normalizar antes de comparar.
- **Formato do `Identifier` dos IEDs** no `sync.json`. Não precisa ser GUID — `"sdg"` e GUID incompleto são aceitáveis. Conferir só a unicidade.
- **Conteúdo do `@idPerfilRoot`** no `perfil-root`.
- **Ordem par/ímpar** em `00-INITIAL-SCRIPTS/`. Organização, não problema — a ausência já é pega pela conferência de GUID e pela de lacuna.
- **`SourceIdentifier` e `SerialNumber`** do `sync.json`. São detalhe.

## Erros Comuns

| Desculpa | Realidade |
|--------|---------|
| "O pipeline estava verde" | Deploy com sucesso ≠ estrutura de pastas e arquivos correta |
| "Funcionou em homologação" | Homologação e produção são ambientes diferentes |
| "Eu conferi ontem" | Deploys posteriores podem ter mudado a estrutura |
| "Outra pessoa do time validou" | Sem registro = não validado |
| "O gerador produziu, então está certo" | Os defeitos reais aparecem no que foi editado à mão depois |

## Red Flags — PARE e Valide

- Task sendo fechada sem ninguém abrir a pasta de produção
- "A estrutura deve estar igual à da última vez"
- Validação feita de boca, sem relatório gerado
- Pular as perguntas iniciais porque "o tipo é óbvio"
- IED acrescentado à mão no `sync.json` sem conferir o `Label` e a correspondência com o `001`
- **Pensar "esse eu já arrumo aqui"** — não arruma. Vira item no relatório.

**Task sem relatório de validação = task não feita.**
