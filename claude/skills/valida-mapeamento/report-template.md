# Relatório Final — Template

- **Local**: na pasta mais alta que o usuário indicou no VSCode para avaliar (ex: indicou `<MODULO>/` → salvar em `<MODULO>/`; indicou `<MODULO>/v1/` → salvar em `v1/`). Nunca dentro de `MDB`/`DNP`/`SYNC`.
- **Nome**: `Validacao-Mapeamento-<MODULO>-<versao>-<PROTOCOLO>.md`, onde `<MODULO>` é o nome da pasta do módulo.
- Os caminhos em `Arquivos analisados:` são relativos a onde o relatório foi salvo.
- Em revalidação, atualizar a mesma doc (ver "Segunda Validação" no `SKILL.md`).

## Regras

- **Cabeçalho obrigatório em todo relatório, inclusive revalidação**: título, linha de contexto, `Arquivos analisados:` com caminho relativo, painel de rodadas e `---`.
- **Uma seção por arquivo** (`fl.sql`, `GruposPadrao.sql`, `VersaoRecurso.sql`, JSON de mapeamento, csv de origem, JSON de SYNC) — o usuário comenta no PR do Azure DevOps arquivo por arquivo.
- **Tudo é checklist**: `- [ ]` = problema, `- [x]` = conferido e OK. Ponto de atenção (3b herdado, 3c camelCase, 9, 14 framework ausente no SYNC) e sugestão (3d) também são `- [ ]`, com o título começando por `Atenção:` ou `Sugestão:`. Nada de parágrafo solto nem "Nenhum problema encontrado" — arquivo sem problema lista cada checagem feita como `- [x]`.
- **Dentro de cada seção: todos os `- [ ]` primeiro (em ordem de ID), depois todos os `- [x]`.**
- **Todo item traz um trecho literal do arquivo** (Ctrl+F funcional): a linha do `DECLARE`, o nome exato do campo, o trecho do JSON.
- `- [ ]` diz o problema e **esperado x encontrado**; `- [x]` diz **por que está OK**.
- **Trecho do csv sempre vira tabela Markdown** (colunas separadas pelo `;` do csv, cabeçalho + linha(s) relevante(s)) — nunca a linha crua com `;`.
- Linguagem simples, frases curtas, sem jargão — quem lê é o usuário comentando no PR.
- **Não vira item**: fato estrutural conhecido que não é comparação entre arquivos (ex: `fl.json` não ter `hashCommitMap`), nem caso de exceção (no máximo uma menção curta em texto perto do item relacionado). Exceção à regra: E3 continua virando o ponto de atenção `- [ ]` do item 3b.

## Itens rastreáveis

Todo problema (`- [ ]`, inclusive atenção/sugestão) é um **item rastreável**. Checagem que já nasce OK fica numa linha simples `- [x]`, sem ID.

- **ID fixo**: `<PREFIXO>-<NN>` por arquivo — `CSV`, `SQL` (fl.sql), `GP` (GruposPadrao), `VR` (VersaoRecurso), `JSON` (fl.json), `SYNC`. Numeração sequencial dentro do prefixo, **nunca reaproveitada nem renumerada** entre rodadas. É o ID que o usuário cita no comentário do PR.
- **Status** (logo após o título):

  | Status | Checkbox | Quando |
  |---|---|---|
  | 🔴 `aberto` | `- [ ]` | Encontrado, ainda não comentado no PR |
  | 💬 `no-pr` | `- [ ]` | Usuário comentou no PR (ele muda na doc ou avisa na conversa) |
  | 🟡 `parcial` | `- [ ]` | Parte dos trechos corrigida, parte continua |
  | 🔁 `reaberto` | `- [ ]` | Estava resolvido e o problema voltou |
  | ✅ `resolvido` | `- [x]` | Corrigido — sempre com a rodada (`resolvido na R2`) |
  | ⚪ `nao-corrigir` | `- [x]` | Usuário decidiu não corrigir — com a justificativa dele |

- **Linhas do item** (nesta ordem; omitir a que não se aplica):
  - `Esperado:` / `Encontrado:` — o problema com trecho literal (ou tabela, quando são vários).
  - `Onde:` — o trecho literal que a revalidação vai procurar (Ctrl+F / grep) para saber se foi corrigido.
  - `Chave:` — a `{chave: ...}` do `valida.py` que gerou o item, ou `manual` quando veio de checagem manual.
  - `Depende de:` — ID do item causa raiz, quando este item é consequência de outro (a correção vem junto).
  - `PR:` — link ou número do comentário no PR (preenchido pelo usuário, ou pela skill quando ele informar).
  - `Histórico:` — uma entrada por rodada: `R1 aberto · R2 parcial (4 de 6) · R3 resolvido`.
  - `Obs.:` — observação do usuário. **Nunca apagar nem reescrever.**
- **Causa raiz**: quando vários itens nascem do mesmo problema, o item da causa fica em primeiro lugar na seção dele e os derivados apontam para ele com `Depende de:`. Assim basta um comentário no PR.
- **Item nunca é apagado.** Resolvido vai para o bloco `- [x]` da seção, com o ID, o status e o trecho atual que mostra a correção.

## Painel de rodadas

Fica logo abaixo de `Arquivos analisados:`. Uma linha por rodada, contando os itens rastreáveis no fim da rodada. `Novos` = itens criados naquela rodada.

## Esqueleto

```markdown
# Validação de Mapeamento — Módulo <NOME> (<versão> / <protocolo>)

<Primeira validação do módulo, sem versão anterior para comparar | Revalidação (R<n>)>. <Mapeamento de cliente específico | Não é mapeamento de cliente>.

Arquivos analisados:
- `MDB/<e3lib>-fl.sql`
- `MDB/<e3lib>-GruposPadrao.sql`
- `MDB/<e3lib>-VersaoRecurso.sql`
- `MDB/<e3lib>-fl.json`
- `MDB/<nome>_mdb_v1_<hash12>.csv`
- `SYNC/<e3lib>-sigma-sync-import.json`

| Rodada | Data | 🔴 Abertos | 💬 No PR | 🟡 Parciais | 🔁 Reabertos | ✅ Resolvidos | ⚪ Não corrigir | Novos |
|---|---|---|---|---|---|---|---|---|
| R1 | AAAA-MM-DD | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| R2 | AAAA-MM-DD | 0 | 1 | 1 | 0 | 1 | 1 | 1 |

---

## `MDB/<e3lib>-fl.sql`

- [ ] **SQL-02 — Encoding da descrição** · 🟡 parcial
  - Esperado: `Concentração de H₂` · Encontrado: `Concentração de H?` (ainda em 3 descrições)
  - Onde: `'Concentração de H?'`
  - Chave: `10/fl.sql/caractere-suspeito-na-descricao`
  - Histórico: R1 aberto · R2 parcial (3 de 8)
- [ ] **SQL-03 — Gráfico rápido sem tipo 1537** · 💬 no-pr
  - Esperado: `TipoCampo = 1537` · Encontrado: `TipoCampo = 1` no `get_<mnemonico>`

    | UUID | Mnemônico | Classificação | Gráfico rápido |
    |---|---|---|---|
    | `<uuid sem hífen>` | `<mnemonico>` | Medida | Sim |

  - Onde: `VALUES(@CampoId7, 'get_<mnemonico>'`
  - Chave: `8/fl.sql/grafico-rapido-sim-sem-tipo`
  - PR: <link do comentário>
  - Histórico: R2 novo
- [x] **SQL-01 — Imagem do módulo** · ✅ resolvido na R2
  - Agora: `Imagem = '<e3lib>.svg'`
  - Histórico: R1 aberto · R2 resolvido
- [x] **E3Lib igual ao JSON**: `E3Lib = '<e3lib>'` — mesmo valor no `fl.json`.

## `MDB/<e3lib>-VersaoRecurso.sql`

- [x] **VR-01 — Formato de `TagsVersaoFirmware`** · ⚪ nao-corrigir
  - Encontrado: `DECLARE @TagVersaoFirmware VARCHAR(50) = 'v1[fwv1[fw1.0]]';`
  - Obs.: <justificativa do usuário>
  - Histórico: R1 aberto · R2 nao-corrigir
- [x] **Formato de `TagsVersaoMapa`**: `DECLARE @TagVersaoMapa VARCHAR(50) = 'v1-MDB'` — formato `v<major>-<PROTOCOLO>` correto.

## `MDB/<nome>_mdb_v1_<hash12>.csv`

- [x] **Nome do arquivo**: `<nome>_mdb_v1_<hash12>.csv` — tem protocolo, versão e hash, e bate com a pasta `v1/MDB`.

## `SYNC/<e3lib>-sigma-sync-import.json`

- [x] **Hash do mapa**: `"hashCommitMap": "<hash12>"` — igual ao hash no nome do csv.
```
