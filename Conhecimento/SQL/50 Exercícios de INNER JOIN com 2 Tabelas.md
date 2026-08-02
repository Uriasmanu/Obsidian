# 50 Exercícios de INNER JOIN com 2 Tabelas

Cada exercício pede para escrever a query SQL. As tabelas com dados estão ao final de cada exercício.

---

## Tabelas de Referência

As mesmas tabelas são usadas em todos os exercícios:

### Tabela Cliente

| Id | Nome | Email | Cidade |
|---|---|---|---|
| 1 | João | joao@email.com | São Paulo |
| 2 | Maria | maria@email.com | Rio de Janeiro |
| 3 | Pedro | pedro@email.com | Belo Horizonte |
| 4 | Ana | ana@email.com | São Paulo |
| 5 | Lucas | lucas@email.com | Curitiba |
| 6 | Juliana | juliana@email.com | Porto Alegre |
| 7 | Rafael | rafael@email.com | Salvador |
| 8 | Fernanda | fernanda@email.com | Brasília |

### Tabela Pedido

| Id | ClienteId | Data | Valor |
|---|---|---|---|
| 101 | 1 | 2024-01-10 | 150.00 |
| 102 | 2 | 2024-01-11 | 250.00 |
| 103 | 1 | 2024-01-12 | 80.00 |
| 104 | 3 | 2024-01-13 | 320.00 |
| 105 | 5 | 2024-01-14 | 90.00 |
| 106 | 2 | 2024-01-15 | 180.00 |
| 107 | 4 | 2024-01-16 | 400.00 |
| 108 | 7 | 2024-01-17 | 210.00 |

---

## Exercícios

### Exercício 1
Liste o nome do cliente e a data de cada pedido.

**Resultado esperado:**

| Cliente | Data |
|---|---|
| João | 2024-01-10 |
| Maria | 2024-01-11 |
| João | 2024-01-12 |
| Pedro | 2024-01-13 |
| Lucas | 2024-01-14 |
| Maria | 2024-01-15 |
| Ana | 2024-01-16 |
| Rafael | 2024-01-17 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId;
```

---

### Exercício 2
Liste o nome do cliente e o valor de cada pedido.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| João | 150.00 |
| Maria | 250.00 |
| João | 80.00 |
| Pedro | 320.00 |
| Lucas | 90.00 |
| Maria | 180.00 |
| Ana | 400.00 |
| Rafael | 210.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId;
```

---

### Exercício 3
Liste o email do cliente e o id do pedido.

**Resultado esperado:**

| Email | PedidoId |
|---|---|
| joao@email.com | 101 |
| maria@email.com | 102 |
| joao@email.com | 103 |
| pedro@email.com | 104 |
| lucas@email.com | 105 |
| maria@email.com | 106 |
| ana@email.com | 107 |
| rafael@email.com | 108 |

**Resposta:**
```sql
SELECT c.Email, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId;
```

---

### Exercício 4
Liste o nome do cliente e o id do pedido, mas apenas para pedidos acima de R$ 200,00.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| Maria | 102 |
| Pedro | 104 |
| Ana | 107 |
| Rafael | 108 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Valor > 200;
```

---

### Exercício 5
Liste o nome do cliente e o valor do pedido, ordenado por valor do maior para o menor.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| Ana | 400.00 |
| Pedro | 320.00 |
| Maria | 250.00 |
| Rafael | 210.00 |
| Maria | 180.00 |
| João | 150.00 |
| Lucas | 90.00 |
| João | 80.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
ORDER BY p.Valor DESC;
```

---

### Exercício 6
Liste o nome do cliente e a data do pedido, apenas para o cliente "João".

**Resultado esperado:**

| Cliente | Data |
|---|---|
| João | 2024-01-10 |
| João | 2024-01-12 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Nome = 'João';
```

---

### Exercício 7
Liste o nome do cliente e o valor do pedido, apenas para clientes de "São Paulo".

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| João | 150.00 |
| João | 80.00 |
| Ana | 400.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Cidade = 'São Paulo';
```

---

### Exercício 8
Liste o nome do cliente e o id do pedido, ordenado por nome do cliente.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| Ana | 107 |
| João | 101 |
| João | 103 |
| Lucas | 105 |
| Maria | 102 |
| Maria | 106 |
| Pedro | 104 |
| Rafael | 108 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
ORDER BY c.Nome;
```

---

### Exercício 9
Liste o nome do cliente e a data do pedido, para pedidos feitos em janeiro de 2024.

**Resultado esperado:**

| Cliente | Data |
|---|---|
| João | 2024-01-10 |
| Maria | 2024-01-11 |
| João | 2024-01-12 |
| Pedro | 2024-01-13 |
| Lucas | 2024-01-14 |
| Maria | 2024-01-15 |
| Ana | 2024-01-16 |
| Rafael | 2024-01-17 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Data BETWEEN '2024-01-01' AND '2024-01-31';
```

---

### Exercício 10
Liste o nome do cliente e o valor do pedido, apenas para valores entre R$ 100 e R$ 300.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| João | 150.00 |
| Maria | 250.00 |
| Pedro | 320.00 |
| Maria | 180.00 |
| Rafael | 210.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Valor BETWEEN 100 AND 300;
```

---

### Exercício 11
Liste o nome do cliente e o id do pedido, onde o id do pedido é maior que 105.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| Maria | 106 |
| Ana | 107 |
| Rafael | 108 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Id > 105;
```

---

### Exercício 12
Liste o nome do cliente e a data do pedido, ordenado por data do mais antigo para o mais recente.

**Resultado esperado:**

| Cliente | Data |
|---|---|
| João | 2024-01-10 |
| Maria | 2024-01-11 |
| João | 2024-01-12 |
| Pedro | 2024-01-13 |
| Lucas | 2024-01-14 |
| Maria | 2024-01-15 |
| Ana | 2024-01-16 |
| Rafael | 2024-01-17 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
ORDER BY p.Data ASC;
```

---

### Exercício 13
Liste o nome do cliente e o valor do pedido, apenas para o cliente "Maria".

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| Maria | 250.00 |
| Maria | 180.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Nome = 'Maria';
```

---

### Exercício 14
Liste o nome do cliente e o id do pedido, onde o nome do cliente começa com "J".

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| João | 101 |
| João | 103 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Nome LIKE 'J%';
```

---

### Exercício 15
Liste o nome do cliente e a data do pedido, apenas para pedidos com valor maior que 150.

**Resultado esperado:**

| Cliente | Data |
|---|---|
| Maria | 2024-01-11 |
| Pedro | 2024-01-13 |
| Ana | 2024-01-16 |
| Rafael | 2024-01-17 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Valor > 150;
```

---

### Exercício 16
Liste o nome do cliente e o valor do pedido, ordenado por nome do cliente e depois por valor.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| Ana | 400.00 |
| João | 80.00 |
| João | 150.00 |
| Lucas | 90.00 |
| Maria | 180.00 |
| Maria | 250.00 |
| Pedro | 320.00 |
| Rafael | 210.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
ORDER BY c.Nome, p.Valor;
```

---

### Exercício 17
Liste o nome do cliente e o id do pedido, para o cliente com Id igual a 1.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| João | 101 |
| João | 103 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Id = 1;
```

---

### Exercício 18
Liste o nome do cliente e a data do pedido, onde a data é anterior a 2024-01-14.

**Resultado esperado:**

| Cliente | Data |
|---|---|
| João | 2024-01-10 |
| Maria | 2024-01-11 |
| João | 2024-01-12 |
| Pedro | 2024-01-13 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Data < '2024-01-14';
```

---

### Exercício 19
Liste o nome do cliente e o valor do pedido, apenas para valores menores que 100.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| João | 80.00 |
| Lucas | 90.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Valor < 100;
```

---

### Exercício 20
Liste o nome do cliente e o id do pedido, ordenado por id do pedido.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| João | 101 |
| Maria | 102 |
| João | 103 |
| Pedro | 104 |
| Lucas | 105 |
| Maria | 106 |
| Ana | 107 |
| Rafael | 108 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
ORDER BY p.Id;
```

---

### Exercício 21
Liste o nome do cliente e a data do pedido, para o cliente de "Rio de Janeiro".

**Resultado esperado:**

| Cliente | Data |
|---|---|
| Maria | 2024-01-11 |
| Maria | 2024-01-15 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Cidade = 'Rio de Janeiro';
```

---

### Exercício 22
Liste o nome do cliente e o valor do pedido, onde o valor é diferente de 150.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| Maria | 250.00 |
| João | 80.00 |
| Pedro | 320.00 |
| Lucas | 90.00 |
| Maria | 180.00 |
| Ana | 400.00 |
| Rafael | 210.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Valor <> 150;
```

---

### Exercício 23
Liste o nome do cliente e o id do pedido, onde o nome do cliente contém "a".

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| Maria | 102 |
| Ana | 107 |
| Rafael | 108 |
| Maria | 106 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Nome LIKE '%a%';
```

---

### Exercício 24
Liste o nome do cliente e a data do pedido, ordenado por data do mais recente para o mais antigo.

**Resultado esperado:**

| Cliente | Data |
|---|---|
| Rafael | 2024-01-17 |
| Ana | 2024-01-16 |
| Maria | 2024-01-15 |
| Lucas | 2024-01-14 |
| Pedro | 2024-01-13 |
| João | 2024-01-12 |
| Maria | 2024-01-11 |
| João | 2024-01-10 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
ORDER BY p.Data DESC;
```

---

### Exercício 25
Liste o nome do cliente e o valor do pedido, para o cliente com Id igual a 2.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| Maria | 250.00 |
| Maria | 180.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Id = 2;
```

---

### Exercício 26
Liste o nome do cliente e o id do pedido, onde o id do pedido é par.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| Maria | 102 |
| Pedro | 104 |
| Lucas | 105 |
| Maria | 106 |
| Ana | 107 |
| Rafael | 108 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Id % 2 = 0;
```

---

### Exercício 27
Liste o nome do cliente e a data do pedido, para pedidos com valor maior ou igual a 200.

**Resultado esperado:**

| Cliente | Data |
|---|---|
| Maria | 2024-01-11 |
| Pedro | 2024-01-13 |
| Ana | 2024-01-16 |
| Rafael | 2024-01-17 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Valor >= 200;
```

---

### Exercício 28
Liste o nome do cliente e o valor do pedido, onde o nome do cliente termina com "o".

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| João | 150.00 |
| João | 80.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Nome LIKE '%o';
```

---

### Exercício 29
Liste o nome do cliente e o id do pedido, ordenado por id do cliente.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| João | 101 |
| João | 103 |
| Maria | 102 |
| Maria | 106 |
| Pedro | 104 |
| Ana | 107 |
| Lucas | 105 |
| Rafael | 108 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
ORDER BY c.Id;
```

---

### Exercício 30
Liste o nome do cliente e a data do pedido, para o cliente de "Belo Horizonte".

**Resultado esperado:**

| Cliente | Data |
|---|---|
| Pedro | 2024-01-13 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Cidade = 'Belo Horizonte';
```

---

### Exercício 31
Liste o nome do cliente e o valor do pedido, onde o valor é maior que 300.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| Pedro | 320.00 |
| Ana | 400.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Valor > 300;
```

---

### Exercício 32
Liste o nome do cliente e o id do pedido, onde o nome do cliente tem 4 letras.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| Ana | 107 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE LENGTH(c.Nome) = 4;
```

---

### Exercício 33
Liste o nome do cliente e a data do pedido, para pedidos feitos entre 2024-01-12 e 2024-01-15.

**Resultado esperado:**

| Cliente | Data |
|---|---|
| João | 2024-01-12 |
| Pedro | 2024-01-13 |
| Lucas | 2024-01-14 |
| Maria | 2024-01-15 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Data BETWEEN '2024-01-12' AND '2024-01-15';
```

---

### Exercício 34
Liste o nome do cliente e o valor do pedido, ordenado por valor do menor para o maior.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| João | 80.00 |
| Lucas | 90.00 |
| João | 150.00 |
| Maria | 180.00 |
| Rafael | 210.00 |
| Maria | 250.00 |
| Pedro | 320.00 |
| Ana | 400.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
ORDER BY p.Valor ASC;
```

---

### Exercício 35
Liste o nome do cliente e o id do pedido, para o cliente com Id maior que 5.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| Rafael | 108 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Id > 5;
```

---

### Exercício 36
Liste o nome do cliente e a data do pedido, onde o nome do cliente contém "e".

**Resultado esperado:**

| Cliente | Data |
|---|---|
| Pedro | 2024-01-13 |
| Rafael | 2024-01-17 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Nome LIKE '%e%';
```

---

### Exercício 37
Liste o nome do cliente e o valor do pedido, para valores diferentes de 80, 90 e 150.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| Maria | 250.00 |
| Pedro | 320.00 |
| Maria | 180.00 |
| Ana | 400.00 |
| Rafael | 210.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Valor NOT IN (80, 90, 150);
```

---

### Exercício 38
Liste o nome do cliente e o id do pedido, onde o id do pedido é ímpar.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| João | 101 |
| João | 103 |
| Pedro | 104 |
| Ana | 107 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Id % 2 <> 0;
```

---

### Exercício 39
Liste o nome do cliente e a data do pedido, para o cliente de "Curitiba".

**Resultado esperado:**

| Cliente | Data |
|---|---|
| Lucas | 2024-01-14 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Cidade = 'Curitiba';
```

---

### Exercício 40
Liste o nome do cliente e o valor do pedido, onde o nome do cliente começa com "M".

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| Maria | 250.00 |
| Maria | 180.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Nome LIKE 'M%';
```

---

### Exercício 41
Liste o nome do cliente e o id do pedido, para pedidos com valor maior que 100 e menor que 300.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| João | 101 |
| Maria | 102 |
| Maria | 106 |
| Rafael | 108 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Valor > 100 AND p.Valor < 300;
```

---

### Exercício 42
Liste o nome do cliente e a data do pedido, ordenado por nome do cliente e depois por data.

**Resultado esperado:**

| Cliente | Data |
|---|---|
| Ana | 2024-01-16 |
| João | 2024-01-10 |
| João | 2024-01-12 |
| Lucas | 2024-01-14 |
| Maria | 2024-01-11 |
| Maria | 2024-01-15 |
| Pedro | 2024-01-13 |
| Rafael | 2024-01-17 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
ORDER BY c.Nome, p.Data;
```

---

### Exercício 43
Liste o nome do cliente e o valor do pedido, para o cliente com Id igual a 3.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| Pedro | 320.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Id = 3;
```

---

### Exercício 44
Liste o nome do cliente e o id do pedido, onde o nome do cliente tem mais de 5 letras.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| Maria | 102 |
| Maria | 106 |
| Pedro | 104 |
| Rafael | 108 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE LENGTH(c.Nome) > 5;
```

---

### Exercício 45
Liste o nome do cliente e a data do pedido, onde a data é posterior a 2024-01-14.

**Resultado esperado:**

| Cliente | Data |
|---|---|
| Maria | 2024-01-15 |
| Ana | 2024-01-16 |
| Rafael | 2024-01-17 |

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Data > '2024-01-14';
```

---

### Exercício 46
Liste o nome do cliente e o valor do pedido, para valores maiores que 150 e menores que 400.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| Maria | 250.00 |
| Pedro | 320.00 |
| Maria | 180.00 |
| Rafael | 210.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE p.Valor > 150 AND p.Valor < 400;
```

---

### Exercício 47
Liste o nome do cliente e o id do pedido, para o cliente de "Porto Alegre".

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|

*Nenhum resultado (Juliana não tem pedidos)*

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Cidade = 'Porto Alegre';
```

---

### Exercício 48
Liste o nome do cliente e a data do pedido, onde o nome do cliente começa com "F".

**Resultado esperado:**

| Cliente | Data |
|---|---|

*Nenhum resultado (Fernanda não tem pedidos)*

**Resposta:**
```sql
SELECT c.Nome, p.Data
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Nome LIKE 'F%';
```

---

### Exercício 49
Liste o nome do cliente e o valor do pedido, para o cliente com Id menor ou igual a 2.

**Resultado esperado:**

| Cliente | Valor |
|---|---|
| João | 150.00 |
| João | 80.00 |
| Maria | 250.00 |
| Maria | 180.00 |

**Resposta:**
```sql
SELECT c.Nome, p.Valor
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId
WHERE c.Id <= 2;
```

---

### Exercício 50
Liste o nome do cliente e o id do pedido, para todos os clientes que fizeram pedidos.

**Resultado esperado:**

| Cliente | PedidoId |
|---|---|
| João | 101 |
| Maria | 102 |
| João | 103 |
| Pedro | 104 |
| Lucas | 105 |
| Maria | 106 |
| Ana | 107 |
| Rafael | 108 |

**Resposta:**
```sql
SELECT c.Nome, p.Id
FROM Cliente c
INNER JOIN Pedido p ON c.Id = p.ClienteId;
```

---

## Resumo dos Conceitos Utilizados

| Conceito | Sintaxe | Exemplo |
|---|---|---|
| JOIN | `FROM A INNER JOIN B ON A.Id = B.AId` | `FROM Cliente c INNER JOIN Pedido p ON c.Id = p.ClienteId` |
| WHERE | `WHERE coluna = valor` | `WHERE c.Nome = 'João'` |
| ORDER BY | `ORDER BY coluna ASC/DESC` | `ORDER BY p.Valor DESC` |
| LIKE | `WHERE coluna LIKE 'padrão'` | `WHERE c.Nome LIKE 'J%'` |
| BETWEEN | `WHERE coluna BETWEEN a AND b` | `WHERE p.Valor BETWEEN 100 AND 300` |
| AND | `WHERE condição1 AND condição2` | `WHERE p.Valor > 100 AND p.Valor < 300` |
| OR | `WHERE condição1 OR condição2` | `WHERE c.Nome = 'João' OR c.Nome = 'Maria'` |
| NOT IN | `WHERE coluna NOT IN (valores)` | `WHERE p.Valor NOT IN (80, 90, 150)` |
| LENGTH | `LENGTH(coluna)` | `LENGTH(c.Nome) > 5` |

---

## Links

- [[SQL/Guia Completo de JOINs|Guia Completo de JOINs]]
- [[SQL/Conhecimentos em SQL|SQL]]
- [[Manu/Indice|Voltar ao Indice]]
