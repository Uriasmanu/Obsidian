# Guia Completo de JOINs em SQL

Tudo que você precisa saber sobre relacionamentos entre tabelas, de forma didática e com exemplos práticos.

---

## O que é um JOIN?

JOIN é um comando SQL que **combina dados de duas ou mais tabelas** *com base em uma coluna em comum* (geralmente uma chave estrangeira).

**Analogia:** Imagine duas planilhas no Excel — uma com vendas e outra com clientes. Você quer juntar as duas usando o "Código do Cliente" que existe nas duas. Isso é um JOIN.

---

## Por que precisamos de JOINs?

Em bancos de dados relacionais, os dados ficam **separados em tabelas distintas** por questões de organização (normalização).

**Exemplo:**
- Tabela `Empresa` tem dados da empresa
- Tabela `Instalacao` tem dados da instalação
- Tabela `Ativo` tem dados do ativo

Se você quer ver o **nome do ativo + nome da empresa**, precisa juntar as três tabelas. Sem JOIN, você teria que fazer SELECTs separados e juntar manualmente — algo ineficiente.

---

## O que é `FROM Instalacao i`?

`FROM Instalacao i` significa: **selecionar dados da tabela `Instalacao` e dar a ela o alias (apelido) `i`**

### Decomposição

| Parte | Significado |
|---|---|
| `FROM` | "de" ou "a partir de" — indica de qual tabela virão os dados |
| `Instalacao` | Nome da tabela no banco de dados |
| `i` | Alias (apelido) que você escolhe para referenciar essa tabela |

**Traduzindo:** `FROM Instalacao i` = "pegue os dados da tabela **Instalacao** e chame-a de **i**"

### Por que usar alias?

1. **Encurtar o código** — em vez de escrever `Instalacao` toda vez, você escreve `i`
2. **Evitar ambiguidade** — quando duas tabelas têm colunas com o mesmo nome, o alias identifica de qual tabela vem cada coluna

### Exemplo

```sql
-- SEM alias (funciona, mas é mais longo)
SELECT Instalacao.Nome FROM Instalacao;

-- COM alias (mais curto e prático)
SELECT i.Nome FROM Instalacao i;
```

Ambas fazem a mesma coisa. O alias é só uma abreviação.

### Como escolher o alias

Não existe regra fixa. Use o que for mais legível:

| Tabela | Alias comum | Outros exemplos |
|---|---|---|
| `Instalacao` | `i` | `inst`, `insta` |
| `Empresa` | `e` | `emp`, `empresa` |
| `Ativo` | `a` | `at` |
| `ModuloAtivo` | `ma` | `mod` |
| `CampoModuloAtivo` | `cma` | `campo` |

**Dica:** Use a primeira letra do nome da tabela. Para tabelas longas, use as iniciais (ex: `ModuloAtivo` → `ma`).

### Exemplo completo

```sql
SELECT 
    i.Nome AS Instalacao,   -- i é o alias de Instalacao
    e.Nome AS Empresa        -- e é o alias de Empresa
FROM Instalacao i            -- Instalacao com alias i
INNER JOIN Empresa e ON i.EmpresaId = e.Id;  -- Empresa com alias e
```

**Sem os alias, ficaria assim:**

```sql
SELECT 
    Instalacao.Nome AS Instalacao,
    Empresa.Nome AS Empresa
FROM Instalacao
INNER JOIN Empresa ON Instalacao.EmpresaId = Empresa.Id;
```

Funciona igual, mas é mais longo.

### Regra importante

Uma vez que você define o alias no `FROM`, **deve usá-lo em todo o resto da query**:

```sql
-- CORRETO
SELECT i.Nome FROM Instalacao i INNER JOIN Empresa e ON i.EmpresaId = e.Id;

-- ERRADO: "Instalacao.Nome" não existe mais, agora é "i.Nome"
SELECT Instalacao.Nome FROM Instalacao i INNER JOIN Empresa e ON i.EmpresaId = e.Id;
```

---

## Por que o mesmo apelido para tabela e coluna?

Às vezes parece que estamos usando o mesmo apelido para tabela e coluna, mas **são coisas diferentes**:

### Alias da tabela vs Alias da coluna

| Tipo | Sintaxe | Para que serve |
|---|---|---|
| Alias da tabela | `FROM Instalacao i` | Abreviar o nome da tabela na query |
| Alias da coluna | `i.Nome AS Instalacao` | Renomear o que aparece no resultado |

### Exemplo

```sql
SELECT 
    i.Nome AS Instalacao,   -- alias da COLUNA (o que aparece no resultado)
    e.Nome AS Empresa        -- alias da COLUNA (o que aparece no resultado)
FROM Instalacao i            -- alias da TABELA (abreviação na query)
INNER JOIN Empresa e ON i.EmpresaId = e.Id;  -- alias da TABELA
```

### O que acontece sem o alias da coluna?

```sql
-- SEM alias da coluna
SELECT i.Nome FROM Instalacao i;

-- Resultado:
-- | Nome  |
-- |-------|
-- | Papel |
-- | Sider |

-- COM alias da coluna
SELECT i.Nome AS Instalacao FROM Instalacao i;

-- Resultado:
-- | Instalacao |
-- |------------|
-- | Papel      |
-- | Sider      |
```

**Sem `AS`**, a coluna aparece com o nome original (`Nome`).
**Com `AS`**, a coluna aparece com o nome que você escolheu (`Instalacao`).

### Por que isso é útil?

Quando duas tabelas têm colunas com o mesmo nome (ex: `Nome`), o alias da coluna ajuda a **distinguir** no resultado:

```sql
SELECT 
    i.Nome AS Instalacao,   -- coluna "Nome" da tabela Instalacao → exibe como "Instalacao"
    e.Nome AS Empresa        -- coluna "Nome" da tabela Empresa → exibe como "Empresa"
FROM Instalacao i
INNER JOIN Empresa e ON i.EmpresaId = e.Id;
```

**Resultado:**

| Instalacao | Empresa |
|---|---|
| Papel | Treetech |

Sem os alias das colunas, ambas se chamariam "Nome" no resultado, o que seria confuso.

### Resumo

```
FROM Instalacao i          →  alias da TABELA (i)
SELECT i.Nome AS Instalacao  →  alias da COLUNA (Instalacao)
```

São duas coisas completamente diferentes que usam a palavra "alias" mas com propósitos distintos.

---

## O que é o `ON`?

`ON` é a cláusula que define **qual coluna de uma tabela se conecta com qual coluna da outra tabela**. É a "ponte" que liga as duas tabelas.

### Analogia

Imagine duas planilhas:
- Planilha 1: `Cliente` com coluna `Id`
- Planilha 2: `Pedido` com coluna `ClienteId`

O `ON` é como se você dissesse: *"Junte as planilhas onde o Id do Cliente é igual ao ClienteId do Pedido"*.

### Sintaxe

```sql
SELECT colunas
FROM TabelaA a
INNER JOIN TabelaB b ON a.ColunaComum = b.ColunaComum;
--                                         ↑
--                                     cláusula ON
```

### Decomposição

```sql
INNER JOIN Empresa e ON i.EmpresaId = e.Id
--          ↑              ↑           ↑
--      Tabela        Coluna da    Coluna da
--     de destino     TabelaA      TabelaB
```

| Parte | Significado |
|---|---|
| `INNER JOIN Empresa e` | "Junte com a tabela Empresa (alias e)" |
| `ON` | "onde" |
| `i.EmpresaId` | "a coluna EmpresaId da tabela Instalacao (alias i)" |
| `=` | "é igual a" |
| `e.Id` | "a coluna Id da tabela Empresa (alias e)" |

**Traduzindo a query inteira:**

```sql
FROM Instalacao i
INNER JOIN Empresa e ON i.EmpresaId = e.Id
```

*"Pegue a tabela Instalacao e junte com a tabela Empresa, ligando onde o EmpresaId da Instalacao é igual ao Id da Empresa"*

### Exemplo visual

**Tabela Instalacao:**

| Id | Nome | EmpresaId |
|---|---|---|
| 1 | Papel | 10 |
| 2 | Sider | 10 |
| 3 | Petrobras | 20 |

**Tabela Empresa:**

| Id | Nome |
|---|---|
| 10 | Treetech |
| 20 | Petrobras |

**O que o ON faz:**

```
Instalacao.EmpresaId    Empresa.Id
        ↓                   ↓
       10      ════════     10    ← Treetech (corresponde!)
       10      ════════     10    ← Treetech (corresponde!)
       20      ════════     20    ← Petrobras (corresponde!)
```

**Resultado do JOIN:**

| Instalacao | Empresa |
|---|---|
| Papel | Treetech |
| Sider | Treetech |
| Petrobras | Petrobras |

### Regra de ouro

O `ON` sempre compara **duas colunas** (uma de cada tabela) usando operadores de comparação:

| Operador | Significado | Exemplo |
|---|---|---|
| `=` | Igual a | `ON a.Id = b.Id` |
| `<>` ou `!=` | Diferente de | `ON a.Status <> b.Status` |
| `>` | Maior que | `ON a.Data > b.Data` |
| `<` | Menor que | `ON a.Valor < b.Limite` |
| `>=` | Maior ou igual | `ON a.Nivel >= b.Minimo` |
| `<=` | Menor ou igual | `ON a.Preco <= b.Maximo` |

**Na prática, 99% das vezes você usa `=`** (igualdade entre chave primária e chave estrangeira).

### Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `ON i.EmpresaId = e.Id` (certo) | Coluna correta | - |
| `ON i.Nome = e.Nome` (errado) | Comparar colunas de texto pode dar resultados inesperados | Use sempre chaves (Id) |
| Esquecer o `ON` | Query não sabe como ligar as tabelas | Sempre adicione a cláusula ON |

---

## Como o JOIN funciona por dentro

### O que o banco faz quando você escreve um JOIN?

Muita gente pensa que o banco "pega um valor e vai procurando". Mas não é assim. O banco compara **valores** e traz **colunas**.

### Regra fundamental

| O que compara | O que traz |
|---|---|
| **Valores** das colunas que estão no `ON` | **Todas as colunas** das duas tabelas |

### Passo a passo do que acontece

**Exemplo:** `FROM Cliente c INNER JOIN Pedido p ON c.Id = p.ClienteId`

**Passo 1:** O banco pega **toda** a tabela Cliente

| Id | Nome |
|---|---|
| 1 | João |
| 2 | Maria |
| 3 | Pedro |

**Passo 2:** O banco pega **toda** a tabela Pedido

| Id | ClienteId | Data |
|---|---|---|
| 101 | 1 | 2024-01-15 |
| 102 | 2 | 2024-01-16 |
| 103 | 1 | 2024-01-17 |

**Passo 3:** O banco compara **cada linha** de uma com **cada linha** da outra

```
Cliente 1 (João)  ×  Pedido 101 (ClienteId=1)  →  1 = 1?  SIM!  →  Junta!
Cliente 1 (João)  ×  Pedido 102 (ClienteId=2)  →  1 = 2?  NÃO  →  Descarta
Cliente 1 (João)  ×  Pedido 103 (ClienteId=1)  →  1 = 1?  SIM!  →  Junta!
Cliente 2 (Maria) ×  Pedido 101 (ClienteId=1)  →  2 = 1?  NÃO  →  Descarta
Cliente 2 (Maria) ×  Pedido 102 (ClienteId=2)  →  2 = 2?  SIM!  →  Junta!
Cliente 2 (Maria) ×  Pedido 103 (ClienteId=1)  →  2 = 1?  NÃO  →  Descarta
Cliente 3 (Pedro) ×  Pedido 101 (ClienteId=1)  →  3 = 1?  NÃO  →  Descarta
Cliente 3 (Pedro) ×  Pedido 102 (ClienteId=2)  →  3 = 2?  NÃO  →  Descarta
Cliente 3 (Pedro) ×  Pedido 103 (ClienteId=1)  →  3 = 1?  NÃO  →  Descarta
```

**Resultado do JOIN:**

| c.Nome | p.Id | p.ClienteId | p.Data |
|---|---|---|---|
| João | 101 | 1 | 2024-01-15 |
| João | 103 | 1 | 2024-01-17 |
| Maria | 102 | 2 | 2024-01-16 |

### Depois, o banco repete com a próxima tabela

**Próximo JOIN:** `INNER JOIN ItemPedido ip ON p.Id = ip.PedidoId`

O banco pega o **resultado anterior** e compara com `ItemPedido`:

```
Resultado anterior (João + Pedido 101)
                  ×
ItemPedido (PedidoId = 101)
                  ↓
            101 = 101?  SIM!  →  Junta!
```

### Resumo do fluxo

```
1. Pega TODA a tabela Cliente
2. Pega TODA a tabela Pedido
3. Compara TODAS as linhas (Cliente.Id = Pedido.ClienteId)
4. Onde for igual, junta as linhas
5. Pega o resultado e repete com ItemPedido
6. Pega o resultado e repete com Produto
7. Pega o resultado e repete com Categoria
8. No final, aplica o WHERE (filtra só o Pedido 101)
```

### O que NÃO acontece

| Pensamento errado | Na verdade |
|---|---|
| "Pega o valor e vai procurando" | Compara **tudo com tudo** de uma vez |
| "Armazena o resultado e faz outro select" | Faz **tudo em uma única operação** |
| "Compara colunas" | Compara **valores** das colunas |

### O que acontece

| Realidade |
|---|
| O banco compara **valores** das colunas que estão no `ON` |
| Se os valores são **iguais**, junta as duas linhas |
| Junta **todas as colunas** das duas tabelas |
| Repete isso para cada JOIN da query |

### Exemplo com 5 tabelas

```sql
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
INNER JOIN ItemPedido ip ON p.Id = ip.PedidoId
INNER JOIN Produto pr ON ip.ProdutoId = pr.Id
INNER JOIN Categoria cat ON pr.CategoriaId = cat.Id
```

**Fluxo:**

```
Cliente × Pedido → resultado1
resultado1 × ItemPedido → resultado2
resultado2 × Produto → resultado3
resultado3 × Categoria → resultado final
```

**Cada ON responde uma pergunta:** "Isso pertence a quem?"

- `c.Id = p.ClienteId` → "O Pedido pertence a qual Cliente?"
- `p.Id = ip.PedidoId` → "O ItemPedido pertence a qual Pedido?"
- `ip.ProdutoId = pr.Id` → "O ItemPedido é de qual Produto?"
- `pr.CategoriaId = cat.Id` → "O Produto é de qual Categoria?"

---

## Tipos de JOINs

Existem 4 tipos principais de JOIN:

| Tipo | O que faz |
|---|---|
| `INNER JOIN` | Retorna apenas as linhas que têm correspondência em **ambas** as tabelas |
| `LEFT JOIN` | Retorna **todas** as linhas da tabela da esquerda + correspondências da direita |
| `RIGHT JOIN` | Retorna **todas** as linhas da tabela da direita + correspondências da esquerda |
| `FULL JOIN` | Retorna **todas** as linhas de ambas as tabelas |

---

## INNER JOIN

### Conceito
Retorna apenas os registros que têm correspondência em **ambas** as tabelas. Se um registro de uma tabela não tem par na outra, ele **não aparece**.

### Anália Visual

```
Tabela A          Tabela B
┌─────┐           ┌─────┐
│  A  │           │  A  │
│  B  │           │  A  │
│  C  │           │  C  │
│  D  │           │  E  │
└─────┘           └─────┘

Resultado INNER JOIN:
┌─────┐
│  A  │  ← existe em ambas
│  C  │  ← existe em ambas
└─────┘
```

### Sintaxe

```sql
SELECT colunas
FROM TabelaA a
INNER JOIN TabelaB b ON a.ColunaComum = b.ColunaComum;
```

### Exemplo Prático

**Tabela Instalacao:**

| Id | Nome | EmpresaId |
|---|---|---|
| 1 | Papel | 10 |
| 2 | Sider | 10 |
| 3 | Petrobras | 20 |
| 4 | Vazia | NULL |

**Tabela Empresa:**

| Id | Nome |
|---|---|
| 10 | Treetech |
| 20 | Petrobras |
| 30 | Copel |

**Query:**

```sql
SELECT 
    i.Nome AS Instalacao,
    e.Nome AS Empresa
FROM Instalacao i
INNER JOIN Empresa e ON i.EmpresaId = e.Id;
```

**Resultado:**

| Instalacao | Empresa |
|---|---|
| Papel | Treetech |
| Sider | Treetech |
| Petrobras | Petrobras |

**Observação:** A instalação "Vazia" (EmpresaId = NULL) e a empresa "Copel" (sem instalação) **não apareceram**, pois não têm correspondência.

---

## LEFT JOIN

### Conceito
Retorna **todas** as linhas da tabela da esquerda (primeira tabela) e as correspondências da tabela da direita. Se não houver correspondência, os valores da direita aparecem como `NULL`.

### Analogia Visual

```
Tabela A (esquerda)     Tabela B (direita)
┌─────┐                 ┌─────┐
│  A  │                 │  A  │
│  B  │                 │  A  │
│  C  │                 │  C  │
│  D  │                 │  E  │
└─────┘                 └─────┘

Resultado LEFT JOIN:
┌─────┬─────┐
│  A  │  A  │
│  B  │NULL │  ← B não tem par na direita
│  C  │  C  │
│  D  │NULL │  ← D não tem par na direita
└─────┴─────┘
```

### Sintaxe

```sql
SELECT colunas
FROM TabelaA a
LEFT JOIN TabelaB b ON a.ColunaComum = b.ColunaComum;
```

### Exemplo Prático

**Query:**

```sql
SELECT 
    i.Nome AS Instalacao,
    e.Nome AS Empresa
FROM Instalacao i
LEFT JOIN Empresa e ON i.EmpresaId = e.Id;
```

**Resultado:**

| Instalacao | Empresa |
|---|---|
| Papel | Treetech |
| Sider | Treetech |
| Petrobras | Petrobras |
| Vazia | NULL |

**Observação:** A instalação "Vazia" aparece mesmo sem ter empresa correspondente. Isso é útil quando você quer **listar tudo de uma tabela** e só complementar dados da outra.

---

## RIGHT JOIN

### Conceito
Retorna **todas** as linhas da tabela da direita (segunda tabela) e as correspondências da tabela da esquerda. É o oposto do LEFT JOIN.

### Analogia Visual

```
Tabela A (esquerda)     Tabela B (direita)
┌─────┐                 ┌─────┐
│  A  │                 │  A  │
│  B  │                 │  A  │
│  C  │                 │  C  │
│  D  │                 │  E  │
└─────┘                 └─────┘

Resultado RIGHT JOIN:
┌─────┬─────┐
│  A  │  A  │
│  A  │  A  │
│  C  │  C  │
│NULL │  E  │  ← E não tem par na esquerda
└─────┴─────┘
```

### Sintaxe

```sql
SELECT colunas
FROM TabelaA a
RIGHT JOIN TabelaB b ON a.ColunaComum = b.ColunaComum;
```

### Exemplo Prático

**Query:**

```sql
SELECT 
    i.Nome AS Instalacao,
    e.Nome AS Empresa
FROM Instalacao i
RIGHT JOIN Empresa e ON i.EmpresaId = e.Id;
```

**Resultado:**

| Instalacao | Empresa |
|---|---|
| Papel | Treetech |
| Sider | Treetech |
| Petrobras | Petrobras |
| NULL | Copel |

**Observação:** A empresa "Copel" aparece mesmo sem nenhuma instalação associada.

---

## FULL JOIN

### Conceito
Retorna **todas** as linhas de ambas as tabelas. Se não houver correspondência, preenche com `NULL`.

### Analogia Visual

```
Tabela A (esquerda)     Tabela B (direita)
┌─────┐                 ┌─────┐
│  A  │                 │  A  │
│  B  │                 │  A  │
│  C  │                 │  C  │
│  D  │                 │  E  │
└─────┘                 └─────┘

Resultado FULL JOIN:
┌─────┬─────┐
│  A  │  A  │
│  B  │NULL │  ← B não tem par na direita
│  C  │  C  │
│  D  │NULL │  ← D não tem par na direita
│NULL │  E  │  ← E não tem par na esquerda
└─────┴─────┘
```

### Sintaxe

```sql
SELECT colunas
FROM TabelaA a
FULL JOIN TabelaB b ON a.ColunaComum = b.ColunaComum;
```

### Exemplo Prático

**Query:**

```sql
SELECT 
    i.Nome AS Instalacao,
    e.Nome AS Empresa
FROM Instalacao i
FULL JOIN Empresa e ON i.EmpresaId = e.Id;
```

**Resultado:**

| Instalacao | Empresa |
|---|---|
| Papel | Treetech |
| Sider | Treetech |
| Petrobras | Petrobras |
| Vazia | NULL |
| NULL | Copel |

**Observação:** Todas as instalações e todas as empresas aparecem, mesmo sem correspondência.

---

## Comparação entre os JOINs

| Tipo | Tabela Esquerda | Tabela Direita |
|---|---|---|
| `INNER JOIN` | Só linhas com correspondência | Só linhas com correspondência |
| `LEFT JOIN` | Todas as linhas | Só linhas com correspondência (ou NULL) |
| `RIGHT JOIN` | Só linhas com correspondência (ou NULL) | Todas as linhas |
| `FULL JOIN` | Todas as linhas | Todas as linhas |

---

## Múltiplos JOINs (mais de 2 tabelas)

Você pode encadear vários JOINs para navegar por várias tabelas.

### Exemplo: 3 tabelas

```sql
SELECT 
    a.Nome AS Ativo,
    i.Nome AS Instalacao,
    e.Nome AS Empresa
FROM Ativo a
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
INNER JOIN Empresa e ON i.EmpresaId = e.Id;
```

### Exemplo: 5 tabelas

```sql
SELECT 
    e.Nome AS Empresa,
    i.Nome AS Instalacao,
    a.Nome AS Ativo,
    ma.Codigo AS Modulo,
    cma.NomePersonalizadoCampo AS Campo
FROM CampoModuloAtivo cma
INNER JOIN ModuloAtivo ma ON cma.ModuloAtivoId = ma.Id
INNER JOIN Ativo a ON ma.AtivoId = a.Id
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
INNER JOIN Empresa e ON i.EmpresaId = e.Id;
```

**Dica:** Comece pela tabela filha e vá adicionando as tabelas pai na ordem do relacionamento.

---

## JOIN com WHERE (filtrando resultados)

Você pode combinar JOIN com WHERE para filtrar o resultado final.

### Exemplo:

```sql
SELECT 
    a.Nome AS Ativo,
    i.Nome AS Instalacao,
    e.Nome AS Empresa
FROM Ativo a
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
INNER JOIN Empresa e ON i.EmpresaId = e.Id
WHERE e.Nome = 'Treetech'
  AND i.Nome = 'Papel';
```

Isso retorna apenas os ativos da empresa "Treetech" na instalação "Papel".

---

## JOIN com alias (apelidos)

Use alias para encurtar o código e tornar a query mais legível.

### Exemplo:

```sql
SELECT 
    a.Nome AS Ativo,
    i.Nome AS Instalacao,
    e.Nome AS Empresa
FROM Ativo a
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
INNER JOIN Empresa e ON i.EmpresaId = e.Id;
```

Aqui `a`, `i` e `e` são alias para `Ativo`, `Instalacao` e `Empresa`.

---

## O que significa `i.Nome`?

A sintaxe `i.Nome` é uma forma de **referenciar uma coluna específica de uma tabela específica**.

### Decomposição

| Parte | Significado |
|---|---|
| `i` | Alias (apelido) da tabela `Instalacao` |
| `.` | Separador (ponto) |
| `Nome` | Nome da coluna que você quer acessar |

**Traduzindo:** `i.Nome` = "eu quero a coluna **Nome** da tabela **Instalacao**"

### Exemplo visual

```sql
SELECT 
    i.Nome AS Instalacao,   -- coluna Nome da tabela Instalacao (alias i)
    e.Nome AS Empresa        -- coluna Nome da tabela Empresa (alias e)
FROM Instalacao i
INNER JOIN Empresa e ON i.EmpresaId = e.Id;
```

**Resultado:**

| Instalacao | Empresa |
|---|---|
| Papel | Treetech |
| Sider | Treetech |

Cada coluna no resultado veio de uma tabela diferente, identificada pelo alias.

### Por que é necessário?

Se ambas as tabelas têm uma coluna com o mesmo nome (ex: `Nome`), o SQL não sabe qual usar:

```sql
-- ERRO: qual Nome? Ambas tabelas têm coluna "Nome"
SELECT Nome 
FROM Instalacao i 
INNER JOIN Empresa e ON i.EmpresaId = e.Id;

-- CORRETO: especifique qual Nome usando o alias
SELECT i.Nome, e.Nome 
FROM Instalacao i 
INNER JOIN Empresa e ON i.EmpresaId = e.Id;
```

### Regra geral

Sempre que você faz JOIN entre tabelas que têm colunas com o mesmo nome, use o alias para **especificar de qual tabela vem cada coluna**.

### Sintaxe completa

```sql
-- Format: alias.NomeDaColuna
i.Nome          -- Nome da tabela Instalacao
e.Nome          -- Nome da tabela Empresa
a.Codigo        -- Codigo da tabela Ativo
cma.NomePersonalizadoCampo  -- NomePersonalizadoCampo da tabela CampoModuloAtivo
```

---

## Quatro tabelas de mesmo pai

Às vezes, várias tabelas se conectam a uma mesma tabela pai. Nesse caso, você faz JOINs separados para cada uma.

### Exemplo:

```sql
SELECT 
    p.Nome AS Produto,
    pf.Nome AS Fornecedor,
    pc.Nome AS Categoria,
    pm.Nome AS Marca
FROM Produto p
INNER JOIN Fornecedor pf ON p.FornecedorId = pf.Id
INNER JOIN Categoria pc ON p.CategoriaId = pc.Id
INNER JOIN Marca pm ON p.MarcaId = pm.Id;
```

Cada tabela (`Fornecedor`, `Categoria`, `Marca`) é pai de `Produto`, mas não se conectam entre si.

---

## Resumo dos Conceitos

| Conceito | Descrição |
|---|---|
| **JOIN** | Combina linhas de duas tabelas com base em uma coluna em comum |
| **INNER JOIN** | Retorna só registros com correspondência em ambas tabelas |
| **LEFT JOIN** | Retorna todos da esquerda + correspondências da direita |
| **RIGHT JOIN** | Retorna todos da direita + correspondências da esquerda |
| **FULL JOIN** | Retorna todos de ambas as tabelas |
| **ON** | Define a coluna de ligação entre as tabelas |
| **Alias** | Apelido para encurtar o nome da tabela |
| **Foreign Key** | Coluna que aponta para a chave primária de outra tabela |

---

## Erros Comuns

| Erro | Causa | Solução |
|---|---|---|
| `column reference is ambiguous` | Coluna com mesmo nome em duas tabelas | Use o alias: `a.Nome` em vez de `Nome` |
| `invalid reference to FROM-clause` | Tabela ou alias não existe | Verifique se a tabela foi adicionada no FROM ou JOIN |
| Resultado vazio | JOIN não encontrou correspondência | Verifique se as foreign keys estão corretas |
| Resultado duplicado | Tabela filha tem múltiplas correspondências | Use `DISTINCT` ou ajuste o JOIN |

---

## Perguntas de Múltipla Escolha

### Pergunta 1
Qual tipo de JOIN retorna **apenas** os registros que têm correspondência em **ambas** as tabelas?

- a) LEFT JOIN
- b) RIGHT JOIN
- c) INNER JOIN
- d) FULL JOIN

---

### Pergunta 2
Você tem duas tabelas: `Cliente` (10 registros) e `Pedido` (15 registros). Dos 10 clientes, apenas 7 fizeram pedidos. Qual será o número de linhas retornadas por um `INNER JOIN` entre elas?

- a) 10
- b) 15
- c) 7
- d) 25

---

### Pergunta 3
Qual tipo de JOIN retorna **todas** as linhas da tabela da esquerda, mesmo que não haja correspondência na tabela da direita?

- a) INNER JOIN
- b) RIGHT JOIN
- c) LEFT JOIN
- d) FULL JOIN

---

### Pergunta 4
Em um `LEFT JOIN`, quando não há correspondência na tabela da direita, o que aparece nos campos da direita?

- a) Uma mensagem de erro
- b) O valor 0
- c) NULL
- d) Uma string vazia

---

### Pergunta 5
Qual é a função da cláusula `ON` em um JOIN?

- a) Filtrar linhas do resultado final
- b) Definir a coluna de ligação entre as tabelas
- c) Renomear colunas no resultado
- d) Ordenar o resultado

---

### Pergunta 6
Você quer listar **todas** as empresas e **apenas** as instalações que existem. Qual JOIN usar?

- a) INNER JOIN
- b) LEFT JOIN (Empresa LEFT JOIN Instalacao)
- c) RIGHT JOIN
- d) FULL JOIN

---

### Pergunta 7
Em uma query com múltiplos JOINs, qual a ordem correta?

- a) Da tabela pai para a tabela filha
- b) Da tabela filha para a tabela pai
- c) Em qualquer ordem
- d) Sempre pela tabela com mais registros

---

### Pergunta 8
O que acontece em um `FULL JOIN` quando uma tabela tem registros sem correspondência na outra?

- a) Os registros sem correspondência são ignorados
- b) Os registros sem correspondência aparecem com NULL na coluna da outra tabela
- c) Otimiza um erro
- d) A query não executa

---

### Pergunta 9
Qual é o alias correto para a tabela `Ativo`?

- a) `FROM Ativo AS a`
- b) `FROM Ativo a`
- c) Ambos estão corretos
- d) Nenhum está correto

---

### Pergunta 10
Você tem a query:

```sql
SELECT a.Nome, i.Nome
FROM Ativo a
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
```

O que acontece se um ativo tiver `InstalacaoId = NULL`?

- a) O ativo aparece no resultado com instalação NULL
- b) O ativo não aparece no resultado
- c) Otimiza um erro
- d) A query não executa

---

## Gabarito

| Pergunta | Resposta |
|---|---|
| 1 | c) INNER JOIN |
| 2 | c) 7 |
| 3 | c) LEFT JOIN |
| 4 | c) NULL |
| 5 | b) Definir a coluna de ligação entre as tabelas |
| 6 | b) LEFT JOIN (Empresa LEFT JOIN Instalacao) |
| 7 | b) Da tabela filha para a tabela pai |
| 8 | b) Os registros sem correspondência aparecem com NULL na coluna da outra tabela |
| 9 | c) Ambos estão corretos |
| 10 | b) O ativo não aparece no resultado |

---

## Explicações do Gabarito

**1.** INNER JOIN retorna apenas registros com correspondência em ambas tabelas.

**2.** Se apenas 7 clientes fizeram pedidos, o INNER JOIN retorna apenas esses 7 registros (as linhas que têm par em ambas tabelas).

**3.** LEFT JOIN retorna todas as linhas da tabela da esquerda (primeira tabela listada).

**4.** Em JOINs, quando não há correspondência, o valor padrão é NULL.

**5.** A cláusula ON define qual coluna de uma tabela se conecta com qual coluna da outra tabela.

**6.** LEFT JOIN com Empresa na esquerda retorna todas as empresas, mesmo que não tenham instalação.

**7.** Comece pela tabela filha (que tem os dados que você quer) e vá até a tabela pai.

**8.** Em FULL JOIN, registros sem correspondência em qualquer tabela aparecem com NULL na coluna da tabela que não tem par.

**9.** Ambas sintaxes são válidas no SQL: `FROM Tabela alias` e `FROM Tabela AS alias`.

**10.** INNER JOIN descarta registros sem correspondência. Se o ativo não tem InstalacaoId (NULL), ele não aparece no resultado.

---

## Links

- [[SQL/Praticando JOINs - Consultas com Múltiplas Tabelas|Praticando JOINs]]
- [[SQL/Conhecimentos em SQL|SQL]]
- [[SQL/Quiz - Praticando SELECT|Quiz SELECT]]
- [[Manu/Indice|Voltar ao Indice]]
