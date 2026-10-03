# Relatório Final — Template

- **Local**: na pasta de topo da estrutura aberta no VSCode (maior hierarquia disponível). Nunca dentro de subpastas como `DB/`, `client/` ou `E3/`.
- **Nome**: `Validacao-Producao-<EMPRESA>-<tipo>-<versao>.md` (ex: `Validacao-Producao-Eletronuclear-4NET-Rev-1.3.md`). Esse é o mesmo padrão que a revalidação procura — não variar.
- **Normalizar o `<EMPRESA>`**: espaços → `-`, sem acento. Nome composto vira `Global-Technology`, não `Global Technology`. Sem isso a revalidação não acha o relatório anterior.
- Caminhos em `Arquivos analisados:` são relativos a onde o relatório foi salvo.

## Regras

- **Cabeçalho obrigatório em todo relatório**: título, linha de contexto, `Arquivos analisados:`, painel de rodadas e `---`.
- **Uma seção por bloco verificado** (ver "Seções" abaixo).
- **Tudo é checklist**: `- [ ]` = problema, `- [x]` = conferido e OK. Sem parágrafo solto e sem "nenhum problema encontrado" — bloco sem problema lista cada conferência como `- [x]`.
- **Dentro de cada seção: primeiro todos os `- [ ]` (por ordem de ID), depois todos os `- [x]`.**
- **Todo item traz o caminho literal ou trecho** que identifica o problema.
- `- [ ]` diz o problema e **esperado vs encontrado**; `- [x]` diz **por que está OK**.
- Linguagem simples, frases curtas — quem lê é o usuário acompanhando a entrega.

## Seções

Nesta ordem. Seção sem nada a reportar ainda aparece, com os `- [x]` das conferências feitas.

| Seção | O que entra |
|---|---|
| **Estrutura de Pastas** | pastas obrigatórias, toleradas, fora do padrão |
| **Arquivos Obrigatórios** | `create-database-client`, `perfil-root`, pasta da Rev |
| **Módulos** | tabela GUID × fontes, versões, divergência de alias/`E3Lib` |
| **Ativos** | `001` ↔ `hierarchy_export` ↔ `_config.sql` |
| **Scripts de Engenharia** | lacunas na numeração, cruzamento com `Configuracoes*Configurador` |
| **Comunicação** | Sync ou E3. Se Sync: `001` ↔ `sync.json` e `Label` dos IEDs |

## Itens Rastreáveis

Todo problema (`- [ ]`) é um **item rastreável**.

- **ID**: `<PREFIXO>-<NN>`, com apenas dois prefixos:
  - **`PASTA`** — estrutura de pastas.
  - **`ARQ`** — arquivos: **ausentes ou com conteúdo inconsistente**. Cobre arquivo que não existe, GUID órfão, versão divergente, ativo inexistente e identificador mal formado.

  Nenhum ID é pré-atribuído a uma verificação: numerar **na ordem em que o problema é encontrado**, dentro de cada prefixo. Número **nunca é reutilizado**.

- **Status** (logo após o título):

  | Status | Checkbox | Quando |
  |---|---|---|
  | 🔴 `aberto` | `- [ ]` | Encontrado, ainda não resolvido |
  | 🟡 `parcial` | `- [ ]` | Parcialmente corrigido, falta parte |
  | ✅ `resolvido` | `- [x]` | Corrigido — sempre com a rodada (`resolvido na R2`) |
  | ⚪ `nao-corrigir` | `- [x]` | Decidido não corrigir — com justificativa |

- **Linhas do item** (nesta ordem; omitir o que não se aplica):
  - `Esperado:` / `Encontrado:` — o problema, com caminho literal ou trecho.
  - `Onde:` — o caminho literal ou trecho que a revalidação vai procurar para saber se foi corrigido.
  - `Histórico:` — uma entrada por rodada: `R1 aberto · R2 resolvido`.
  - `Obs.:` — observação do usuário. **Nunca apagar nem reescrever.**

## Notas Informativas

Algumas conferências registram uma observação sem que haja problema. Entram como `- [x]`, **nunca** como `- [ ]`:

- Alias do arquivo diferente do `E3Lib`, com o GUID fechando em todas as fontes.
- Comunicação Sync → `E3/` não aplicável.
- Ativo sem determinado módulo configurado (pode ser intencional).
- Variação de grafia no nome de pasta (`03 - JSONS` vs `03-JSON`).

Item marcado como **provisório** (contorna bug do gerador) traz a ressalva na própria linha, para quem ler depois saber que não é regra de arquitetura.

## Painel de Rodadas

Logo abaixo de `Arquivos analisados:`. Uma linha por rodada. **Data = a data de hoje, no formato AAAA-MM-DD.**

Significado das colunas, sempre referentes **àquela rodada**:

| Coluna | Significado |
|---|---|
| 🔴 Abertos | Itens que seguem `- [ ]` 🔴 ao fim da rodada |
| 🟡 Parciais | Itens `- [ ]` 🟡 ao fim da rodada |
| ✅ Resolvidos | Itens que passaram a `- [x]` **nesta** rodada |
| Novos | Itens criados **nesta** rodada |

## Esqueleto

```markdown
# Validação de Produção — <EMPRESA> (<tipo> / <versão> / <comunicação>)

<Primeira validação | Revalidação (R<n>)>.

Arquivos analisados:
- Pasta: `<caminho da pasta da empresa>`
- Tipo: 4NET | 4WEB
- Versão: 1.0 | Rev X.X
- Comunicação: Sync | E3

| Rodada | Data | 🔴 Abertos | 🟡 Parciais | ✅ Resolvidos | Novos |
|---|---|---|---|---|---|
| R1 | AAAA-MM-DD | 3 | 0 | 0 | 3 |

---

## Estrutura de Pastas

- [ ] **PASTA-01 — Pasta `client/` ausente** · 🔴 aberto
  - Esperado: `client/` · Encontrado: pasta não existe
  - Onde: raiz da pasta da empresa
  - Histórico: R1 aberto
- [x] **Pasta `DB/` presente**: `DB/` encontrada na raiz.
- [x] **Pasta `01-BACKBONE/` presente**: `DB/01-BACKBONE/` encontrada.
- [x] **Pasta `escopo/` tolerada**: área temporária, não é achado.

## Arquivos Obrigatórios

- [ ] **ARQ-01 — `*-perfil-root.sql` ausente em `01-BACKBONE/`** · 🔴 aberto
  - Esperado: arquivo terminando em `-perfil-root.sql` · Encontrado: nenhum
  - Onde: `DB/01-BACKBONE/`
  - Histórico: R1 aberto
- [x] **`create-database-client` presente**: `client/000-create-database-client.sql` encontrado.

## Módulos

- [ ] **ARQ-02 — Versão do módulo BMC divergente** · 🔴 aberto
  - Esperado: mesma versão nas 5 fontes · Encontrado: `v13` nos `.sql`, `"12.0"` no `sync.json`
  - Onde: `DB/03 - JSONS/01-BMC-sigma-sync-import.json`
  - Histórico: R1 aberto
- [x] **4 módulos, GUIDs íntegros**: BMC, MBR_V2, SDG e TM presentes nas 5 fontes.
- [x] **Alias ≠ `E3Lib` no módulo TM**: arquivo `07-TM-fl.sql`, `E3Lib = 'NTM'`.
      Conferido pelo GUID `6cb1f7a9…2427` — consistente. Atenção ao renomear arquivos.

## Ativos

- [x] **10 ativos conferidos**: mesmos GUIDs no `001` e no `hierarchy_export.json`.
- [x] **`_config.sql` sem GUID órfão**: todos os ativos citados pertencem ao conjunto.

## Scripts de Engenharia

- [ ] **ARQ-03 — Lacuna na sequência de `01-BACKBONE/`** · 🔴 aberto
  - Esperado: `001`…`055` sem falhas · Encontrado: `030` ausente
  - Onde: `DB/01-BACKBONE/`
  - Histórico: R1 aberto
- [x] **Módulos de engenharia batem**: seções `Configuracoes*Configurador` preenchidas têm
      script correspondente; as vazias não têm.

## Comunicação

- [x] **Comunicação Sync → pasta `E3/` não aplicável**: ausência esperada, não é achado.
- [x] **`001` ↔ `sync.json` fecham 1:1**: 24 blocos `ModuloAtivo` e 24 IEDs, módulo e versão
      conferidos em todos.
- [x] **`Label` dos IEDs**: todos no padrão `{Empresa} - {Instalação} - {Ativo} - {Módulo}`.
- [x] **`Identifier` dos IEDs únicos**: sem repetição. Formato não é validado.
```
