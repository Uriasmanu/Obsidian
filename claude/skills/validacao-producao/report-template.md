# Relatório Final — Template

- **Local**: na pasta da empresa indicada pelo usuário no VSCode.
- **Nome**: `Validacao-Producao-<EMPRESA>-<tipo>-<versao>.md`
- Os caminhos em `Arquivos analisados:` são relativos a onde o relatório foi salvo.

## Regras

- **Cabeçalho obrigatório em todo relatório**: título, linha de contexto, `Arquivos analisados:`, painel de rodadas e `---`.
- **Uma seção por bloco verificado** (estrutura de pastas, arquivos obrigatórios, etc.).
- **Tudo é checklist**: `- [ ]` = problema, `- [x]` = conferido e OK. Nada de parágrafo solto nem "Nenhum problema encontrado" — bloco sem problema lista cada checagem feita como `- [x]`.
- **Dentro de cada seção: todos os `- [ ]` primeiro (em ordem de ID), depois todos os `- [x]`.**
- **Todo item traz o caminho ou trecho literal** que identifica o problema.
- `- [ ]` diz o problema e **esperado x encontrado**; `- [x]` diz **por que está OK**.
- Linguagem simples, frases curtas — quem lê é o usuário acompanhando a entrega.

## Itens rastreáveis

Todo problema (`- [ ]`) é um **item rastreável**.

- **ID fixo**: `<PREFIXO>-<NN>` por bloco — `PASTA` (estrutura de pastas), `ARQ` (arquivos obrigatórios). Numeração sequencial, **nunca reaproveitada**.
- **Status** (logo após o título):

  | Status | Checkbox | Quando |
  |---|---|---|
  | 🔴 `aberto` | `- [ ]` | Encontrado, ainda não resolvido |
  | 💬 `no-pr` | `- [ ]` | Usuário foi avisado, aguardando correção |
  | 🟡 `parcial` | `- [ ]` | Parte corrigida, parte continua |
  | 🔁 `reaberto` | `- [ ]` | Estava resolvido e o problema voltou |
  | ✅ `resolvido` | `- [x]` | Corrigido — sempre com a rodada (`resolvido na R2`) |
  | ⚪ `nao-corrigir` | `- [x]` | Decidido não corrigir — com justificativa |

- **Linhas do item** (nesta ordem; omitir a que não se aplica):
  - `Esperado:` / `Encontrado:` — o problema com caminho ou trecho literal.
  - `Onde:` — o caminho ou trecho que a revalidação vai procurar para saber se foi corrigido.
  - `Histórico:` — uma entrada por rodada: `R1 aberto · R2 resolvido`.
  - `Obs.:` — observação do usuário. **Nunca apagar nem reescrever.**

## Painel de rodadas

Fica logo abaixo de `Arquivos analisados:`. Uma linha por rodada.

## Esqueleto

```markdown
# Validação de Produção — <EMPRESA> (<tipo> / <versão> / <comunicação>)

<Primeira validação | Revalidação (R<n>)>.

Arquivos analisados:
- Pasta: `<caminho da pasta da empresa>`
- Tipo: 4NET | 4WEB
- Versão: 1.0 | Rev X.X
- Comunicação: Sync | E3

| Rodada | Data | 🔴 Abertos | 💬 Aguardando | 🟡 Parciais | ✅ Resolvidos | Novos |
|---|---|---|---|---|---|---|
| R1 | AAAA-MM-DD | 2 | 0 | 0 | 0 | 2 |

---

## Estrutura de Pastas

- [ ] **PASTA-01 — Pasta `client/` ausente** · 🔴 aberto
  - Esperado: `client/` · Encontrado: pasta não existe
  - Onde: raiz da pasta da empresa
  - Histórico: R1 aberto
- [x] **Pasta `DB/` presente**: `DB/` encontrada na raiz.
- [x] **Pasta `01-BACKBONE/` presente**: `DB/01-BACKBONE/` encontrada.

## Arquivos Obrigatórios

- [ ] **ARQ-01 — `*-perfil-root.sql` ausente em `01-BACKBONE/`** · 🔴 aberto
  - Esperado: arquivo terminando em `-perfil-root.sql` · Encontrado: nenhum
  - Onde: `DB/01-BACKBONE/`
  - Histórico: R1 aberto
- [x] **`00-create-database-client.sql` presente**: `client/00-create-database-client.sql` encontrado.

## Comunicação E3

- [x] **Pasta `E3/` presente**: encontrada na raiz.
- [x] **Arquivo `.prj` presente**: `E3/<nome>.prj` encontrado.
- [x] **Arquivo `.dll` presente**: `E3/<nome>.dll` encontrado.
```
