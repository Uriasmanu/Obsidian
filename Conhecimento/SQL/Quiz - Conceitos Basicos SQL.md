# Quiz: Conceitos Básicos SQL (SELECT, FROM, WHERE)

## Instruções
- Responda cada pergunta
- Compar com o gabarito no final
- Revise as que errou

---

## Pergunta 1: SELECT

Qual afirmação sobre SELECT é correta?

A) SELECT é usado para especificar qual tabela acessar

~~B) SELECT determina quais colunas serão retornadas~~

C) SELECT deve sempre ser usado com WHERE

D) SELECT não pode ser usado com funções de agregação

---

## Pergunta 2: SELECT Múltiplas Colunas

Como selecionar múltiplas colunas?

A) SELECT nome; email; telefone

~~B) SELECT nome, email, telefone~~

C) SELECT [nome, email, telefone]

D) SELECT nome + email + telefone

---

## Pergunta 3: SELECT com Alias

Para renomear uma coluna no resultado, usa-se:

~~A) SELECT nome AS "Nome do Cliente"~~

B) SELECT nome = "Nome do Cliente"

C) SELECT nome "Nome do Cliente"

D) A ou C estão corretas

---

## Pergunta 4: FROM

Qual a função do FROM?

A) Filtrar resultados

~~B) Especificar a tabela source~~

C) Ordenar resultados

D) Limitar quantidade de linhas

---

## Pergunta 5: WHERE - Comparação

Qual operador significa "diferente"?

A) =!

B) <>

~~C) !=~~

D) B ou C

---

## Pergunta 6: WHERE - AND/OR

Dados usuários com cidade = "São Paulo" e idade > 18

```
WHERE cidade = 'São Paulo' AND idade > 18
```

Quem aparecerá no resultado?

A) Qualquer pessoa de São Paulo

B) Qualquer pessoa maior de 18

~~C) Pessoas de São Paulo E maiores de 18~~

D) Pessoas de São Paulo OU maiores de 18

---

## Pergunta 7: WHERE - OR

```
WHERE cidade = 'São Paulo' OR cidade = 'Rio de Janeiro'
```

Quem aparecerá?

A) Apenas quem mora em SP

B) Apenas quem mora no Rio

~~C) Quem mora em SP ou no Rio~~

D) Quem não mora em SP nem no Rio

---

## Pergunta 8: WHERE - LIKE

Para encontrar nomes que começam com "Maria":

A) WHERE nome LIKE 'Maria%'

~~B) WHERE nome LIKE '%Maria'~~

C) WHERE nome LIKE '*Maria'

D) WHERE nome LIKE 'Maria'

---

## Pergunta 9: LIKE - Qualquer Posição

Para encontrar nomes que contêm "silva" em qualquer posição:

~~A) WHERE nome LIKE '%silva%'~~

B) WHERE nome LIKE 'silva%'

C) WHERE nome LIKE '%silva'

D) WHERE nome = '%silva%'

---

## Pergunta 10: WHERE com Números

Para buscar produtos com preço menor que 100:

~~A) WHERE preco < 100~~

B) WHERE preco < '100'

C) WHERE preco LIKE < 100

D) WHERE preco EQUAL 100

---

## Pergunta 11: ORDER BY

Para ordenar resultados por nome crescente:

A) ORDER nome ASC

B) ORDER BY nome

~~C) ORDER BY nome ASC~~

D) SORT nome

---

## Pergunta 12: LIMIT

Para mostrar apenas os 10 primeiros resultados:

~~A) TOP 10~~

B) LIMIT 10

C) TAKE 10

D) B ou A (depende do banco)

---

## Gabarito

| #   | Resposta |     |
| --- | -------- | --- |
| 1   | B        | ok  |
| 2   | B        | ok  |
| 3   | D        | x   |
| 4   | B        | ok  |
| 5   | D        | x   |
| 6   | C        | ok  |
| 7   | C        | ok  |
| 8   | A        | x   |
| 9   | A        | ok  |
| 10  | A        | ok  |
| 11  | C        | ok  |
| 12  | D        | x   |

## Score

- 12: Perfeito!
- 10-11: Excelente
- 8-9: Bom, revise as que errou
- < 8: Revise SELECT, WHERE e operadores