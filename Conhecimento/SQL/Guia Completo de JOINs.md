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
