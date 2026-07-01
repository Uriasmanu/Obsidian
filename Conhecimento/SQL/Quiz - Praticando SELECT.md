# Quiz: Praticando SELECT

cenário: Biblioteca (tabela: livros)
livros: id, titulo, autor, ano_publicacao, genero, disponivel

cenário: Produtos (tabela: produtos)
produtos: id, nome, preco, categoria, estoque

cenário: Alunos (tabela: alunos)
alunos: id, nome, email, curso, data_nascimento

---

### Questão 1
Listar todos os livros da biblioteca
```sql
SELECT * FROM livros
```

---

### Questão 2
Listar apenas os títulos dos livros
```sql
SELECT * FROM livros
```
```sql
SELECT titulo FROM livros
```

---

### Questão 3
Listar alunos do curso de Engenharia
```sql
SELECT * FROM alunos where curso = 'Engenharia'
```
```sql
SELECT * FROM alunos WHERE curso = 'Engenharia'
```

---

### Questão 4
Listar produtos com preço maior que 100
```sql
SELECT * FROM produtos WHERE preco => 100
```
```sql
SELECT * FROM produtos WHERE preco >= 100
```

---

### Questão 5
Listar livros do gênero "Aventura", ordenados por ano
```sql
SELECT * FROM livros where genero = 'Aventura' ORDER BY ano
```
```sql
SELECT * FROM livros WHERE genero = 'Aventura' ORDER BY ano_publicacao
```

---

### Questão 6
Listar alunos nascidos depois de 2000
```sql
SELECT * FROM alunos WHERE data_nascimento > 2000
```
```sql
SELECT * FROM alunos WHERE data_nascimento > '2000-01-01'
```

---

### Questão 7
Buscar produtos com "celular" no nome
```sql
SELECT * FROM produtos where nome LIKE 'celular%'
```
```sql
SELECT * FROM produtos WHERE nome LIKE '%celular%'
```

---

### Questão 8
Listar o total de livros por gênero
```sql
não sabia
```
```sql
SELECT genero, COUNT(*) FROM livros GROUP BY genero (Não entendi a logica desse e vou precisar do texto por escrito)
```

---

### Questão 9
Listar o preço médio dos produtos
```sql
não sabia
```
```sql
SELECT AVG(preco) FROM produtos ( não sei o que é AVG)
```

---

### Questão 10
Listar os 5 produtos mais caros
```sql
não sabia
```
```sql
SELECT * FROM produtos ORDER BY preco DESC LIMIT 5
```

---

## Análise do Conhecimento

| Conceito | Status | O que Practice |
|---------|--------|----------------|
| SELECT * | ✅ Sabido | Consegue listar todas as colunas |
| SELECT coluna | ❌ Não sabe | Precisa especificar a coluna, não usar * |
| WHERE simples | ⚠️ Quase | Sabe usar, mas faltou maiúsculo |
| Operador >= | ❌ Errou | Usou => instead de >= |
| ORDER BY | ⚠️ Quase | Sabe usar, mas não lembra campo certo |
| Data em WHERE | ❌ Não sabe | Datas precisam de aspas |
| LIKE com % | ❌ Errou | Precisa % dos dois lados |
| GROUP BY | ❌ Não sabe | Para agregar por grupo |
| AVG() | ❌ Não sabe | Função de agregação |
| ORDER + DESC + LIMIT | ❌ Não sabe | Combinar para ordenar e limitar |

---

## Pontos Fortes
- SELECT básico
- Estrutura geral de queries

---

## Pontos a Melhorar
1. SELECT vs SELECT * (coluna específica)
2. Operadores: >= não =>
3. LIKE: '%termo%' (não 'termo%')
4. GROUP BY para contagem
5. Funções de agregação: AVG(), COUNT(), SUM()
6. ORDER BY + DESC + LIMIT
7. Datas com aspas

---

## Recomendação de Estudo
Praticar: GROUP BY, AVG/COUNT/SUM, ORDER BY DESC, LIMIT, LIKE com %