# Passo a Passo de Validação — Detalhamento

Detalhamento completo de cada item do "Quick Reference" do `SKILL.md`. A ordem dos blocos está lá.

## 1. Perguntas iniciais

Fazer as quatro perguntas numa única chamada (AskUserQuestion) antes de qualquer verificação de arquivo:

- **É 4NET ou 4WEB?** — define a estrutura de pastas esperada.
- **É Rev ou 1.0?** — define se haverá pasta de revisão dentro de `01-BACKBONE/`.
- **A comunicação é Sync ou E3?** — define se a pasta `E3/` com `.prj` e `.dll` é obrigatória.
- **A pasta da empresa já existe?** — se não existir, reportar como `- [ ]` imediatamente antes de continuar.

## 2. Confirmar existência da pasta da empresa

Se a pasta da empresa **não existir**: reportar como `PASTA-01` e encerrar — não há o que verificar dentro dela.

Se existir: seguir para os próximos itens.

## 3. Verificar estrutura de pastas de nível superior

Conferir se as pastas obrigatórias de nível superior existem e estão com os nomes corretos.

**4NET:**
- `client/` — obrigatória
- `DB/` — obrigatória
  - `00-INITIAL-SCRIPTS/` — obrigatória
  - `01-BACKBONE/` — obrigatória
  - `02-GROUPS/` — obrigatória
  - `03-JSON/` — obrigatória

Qualquer pasta fora deste padrão (nome diferente, pasta extra inesperada) → reportar como `- [ ]`.

> **4WEB:** _a detalhar._

## 4. Percorrer subpastas e verificar arquivos obrigatórios

Independente da estrutura estar correta ou não, percorrer todas as subpastas e verificar:

**Sempre obrigatório em 4NET:**

- `client/00-create-database-client.sql` — se ausente, reportar como `ARQ-01`.
- `DB/01-BACKBONE/*-perfil-root.sql` — pelo menos um arquivo com esse sufixo. Se ausente, reportar como `ARQ-02`.

**Se for Rev:**

- `DB/01-BACKBONE/Rev X.X/` — pasta com o nome exato da revisão informada. Se ausente, reportar como `PASTA-02`.

**Conteúdo das demais subpastas:**

> `00-INITIAL-SCRIPTS/`, `02-GROUPS/`, `03-JSON/` — _conteúdo obrigatório a detalhar._

## 5. Comunicação E3

Se a comunicação for E3, verificar independente do tipo (4NET ou 4WEB):

- `E3/` existe na raiz da pasta da empresa → se ausente, reportar como `PASTA-03`.
- `E3/*.prj` — pelo menos um arquivo `.prj`. Se ausente, reportar como `ARQ-03`.
- `E3/*.dll` — pelo menos um arquivo `.dll`. Se ausente, reportar como `ARQ-04`.

## 6. Reportar o que está fora do padrão

Qualquer pasta ou arquivo encontrado que não está previsto na estrutura padrão deve ser reportado como `- [ ]` com prefixo `PASTA` ou `ARQ`, conforme o caso. Não ignorar itens extras — podem indicar deploy incorreto ou sobra de versão anterior.

## 7. Gerar relatório final

Ao final, preencher o esqueleto de `report-template.md`. Não criar o relatório de cabeça — usar sempre o template.
