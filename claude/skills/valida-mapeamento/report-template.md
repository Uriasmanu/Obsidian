# Relatório Final — Template

- **Local**: na pasta mais alta que o usuário indicou no VSCode para avaliar (ex: indicou `<MODULO>/` → salvar em `<MODULO>/`; indicou `<MODULO>/v1/` → salvar em `v1/`). Nunca dentro de `MDB`/`DNP`/`SYNC`.
- **Nome**: `Validacao-Mapeamento-<MODULO>-<versao>-<PROTOCOLO>.md`, onde `<MODULO>` é o nome da pasta do módulo.
- Os caminhos em `Arquivos analisados:` são relativos a onde o relatório foi salvo.
- Em revalidação, atualizar a mesma doc (ver "Segunda Validação" no `SKILL.md`).

## Regras

- **Cabeçalho obrigatório em todo relatório, inclusive revalidação**: título, linha de contexto, `Arquivos analisados:` com caminho relativo, e `---`.
- **Uma seção por arquivo** (`fl.sql`, `GruposPadrao.sql`, `VersaoRecurso.sql`, JSON de mapeamento, csv de origem, JSON de SYNC) — o usuário comenta no PR do Azure DevOps arquivo por arquivo.
- **Tudo é checklist**: `- [ ]` = problema, `- [x]` = conferido e OK. Ponto de atenção (3b herdado, 3c camelCase, 9, 10b, 14 framework ausente no SYNC) e sugestão (3d) também são `- [ ]`, com o texto começando por `Atenção:` ou `Sugestão:`. Nada de parágrafo solto nem "Nenhum problema encontrado" — arquivo sem problema lista cada checagem feita como `- [x]`.
- **Dentro de cada seção: todos os `- [ ]` primeiro, depois todos os `- [x]`.**
- **Todo item traz um trecho literal do arquivo** (Ctrl+F funcional): a linha do `DECLARE`, o nome exato do campo, o trecho do JSON.
- `- [ ]` diz o problema e **esperado x encontrado**; `- [x]` diz **por que está OK**.
- **Trecho do csv sempre vira tabela Markdown** (colunas separadas pelo `;` do csv, cabeçalho + linha(s) relevante(s)) — nunca a linha crua com `;`.
- Linguagem simples, frases curtas, sem jargão — quem lê é o usuário comentando no PR.
- **Não vira item**: fato estrutural conhecido que não é comparação entre arquivos (ex: `fl.json` não ter `hashCommitMap`), nem caso de exceção (no máximo uma menção curta em texto perto do item relacionado). Exceção à regra: E2 e E3 continuam virando o ponto de atenção `- [ ]` dos itens 10b e 3b.

## Esqueleto

```markdown
# Validação de Mapeamento — Módulo <NOME> (<versão> / <protocolo>)

<Primeira validação do módulo, sem versão anterior para comparar | Revalidação>. <Mapeamento de cliente específico | Não é mapeamento de cliente>.

Arquivos analisados:
- `MDB/<e3lib>-fl.sql`
- `MDB/<e3lib>-GruposPadrao.sql`
- `MDB/<e3lib>-VersaoRecurso.sql`
- `MDB/<e3lib>-fl.json`
- `MDB/<nome>_mdb_v1_<hash12>.csv`
- `SYNC/<e3lib>-sigma-sync-import.json`

---

## `MDB/<e3lib>-fl.sql`

- [ ] **Imagem do módulo**: `Imagem = 'outro.svg'` — esperado `<e3lib>.svg`, encontrado `outro.svg`.
- [ ] **Encoding da descrição**: `Concentração de H?` — o `?` substituiu o "2" de H₂.
- [x] **E3Lib igual ao JSON**: `E3Lib = '<e3lib>'` — mesmo valor no `fl.json`.
- [x] **Mnemônicos únicos**: 47 campos `get_...` — nenhum repetido.

## `MDB/<e3lib>-VersaoRecurso.sql`

- [ ] **Formato de `TagsVersaoFirmware`**: `DECLARE @TagVersaoFirmware VARCHAR(50) = 'v1[fwv1[fw1.0]]';` — template aninhado duas vezes; esperado `v1[fw1.0]`.
- [x] **Formato de `TagsVersaoMapa`**: `DECLARE @TagVersaoMapa VARCHAR(50) = 'v1-MDB'` — formato `v<major>-<PROTOCOLO>` correto.

## `MDB/<nome>_mdb_v1_<hash12>.csv`

- [ ] **Codificação do arquivo**: arquivo em Windows-1252 — o processo pede UTF-8.
- [ ] **Gráfico rápido sem tipo 1537**: no SQL o campo `get_<mnemonico>` está com `TipoCampo = 1`, esperado `1537`.

  | UUID | Mnemônico | Classificação | Gráfico rápido |
  |---|---|---|---|
  | `<uuid sem hífen>` | `<mnemonico>` | Medida | Sim |

- [x] **Nome do arquivo**: `<nome>_mdb_v1_<hash12>.csv` — tem protocolo, versão e hash, e bate com a pasta `v1/MDB`.

## `SYNC/<e3lib>-sigma-sync-import.json`

- [x] **Hash do mapa**: `"hashCommitMap": "<hash12>"` — igual ao hash no nome do csv.
```
