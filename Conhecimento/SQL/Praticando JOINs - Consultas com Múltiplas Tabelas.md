# Praticando JOINs: Consultas com Múltiplas Tabelas

Como descobrir o **empresa** e a **instalação** de um `CampoModuloAtivo` sem ir tabela por tabela.

---

## Como Descobrir o Relacionamento (quando não conhece as tabelas)

Antes de escrever qualquer JOIN, você precisa **descobrir como as tabelas se conectam**. Siga esta ordem:

### Passo 1: Listar todas as tabelas do banco

```sql
-- PostgreSQL
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- SQL Server
SELECT name 
FROM sys.tables 
ORDER BY name;
```

Isso mostra todas as tabelas disponíveis. Anote as nomes das tabelas que você precisa usar.

---

### Passo 2: Descobrir as colunas de cada tabela

```sql
-- PostgreSQL
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'NomeDaTabela'
ORDER BY ordinal_position;

-- SQL Server
SELECT 
    c.name AS column_name,
    t.name AS data_type,
    c.is_nullable
FROM sys.columns c
JOIN sys.types t ON c.user_type_id = t.user_type_id
WHERE c.object_id = OBJECT_ID('NomeDaTabela')
ORDER BY c.column_id;
```

**O que procurar:** Colunas que terminam com `Id` (ex: `InstalacaoId`, `EmpresaId`). Essas são as **chaves estrangeiras** que ligam uma tabela a outra.

---

### Passo 3: Identificar as Foreign Keys (chaves estrangeiras)

```sql
-- PostgreSQL
SELECT
    tc.constraint_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_name = 'NomeDaTabela';

-- SQL Server
SELECT
    fk.name AS constraint_name,
    cp.name AS column_name,
    OBJECT_NAME(fk.referenced_object_id) AS foreign_table_name,
    cr.name AS foreign_column_name
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc 
    ON fk.object_id = fkc.constraint_object_id
JOIN sys.columns cp 
    ON fkc.parent_object_id = cp.object_id 
    AND fkc.parent_column_id = cp.column_id
JOIN sys.columns cr 
    ON fkc.referenced_object_id = cr.object_id 
    AND fkc.referenced_column_id = cr.column_id
WHERE fk.parent_object_id = OBJECT_ID('NomeDaTabela');
```

**Isso mostra exatamente:** Qual coluna de `TabelaA` aponta para qual coluna de `TabelaB`.

---

### Passo 4: Montar o mapa de relacionamentos

Com as informações dos passos anteriores, monte uma lista assim:

| Tabela Filha | Coluna de Ligação | Tabela Pai |
|---|---|---|
| `Instalacao` | `EmpresaId` | `Empresa` |
| `Ativo` | `InstalacaoId` | `Instalacao` |
| `ModuloAtivo` | `AtivoId` | `Ativo` |
| `CampoModuloAtivo` | `ModuloAtivoId` | `ModuloAtivo` |

**Regra:** A tabela filha (que tem a coluna `Id` da outra tabela) vem do **lado N** do relacionamento. A tabela pai (que é referenciada) vem do **lado 1**.

---

### Passo 5: Visualizar como uma cadeia

```
Empresa (1) ──── (N) Instalacao
                        │
                        │ InstalacaoId
                        ▼
                     Ativo (1) ──── (N) ModuloAtivo
                                          │
                                          │ ModuloAtivoId
                                          ▼
                                   CampoModuloAtivo
```

**Dica:** Se você quer descobrir dados de `CampoModuloAtivo`, comece por ele e vá **subindo** a cadeia até chegar à tabela que tem as informações que precisa.

---

## Resumo Rápido: O que olhar primeiro

| Situação | O que fazer |
|---|---|
| Não sei quais tabelas existem | Liste as tabelas (`information_schema.tables`) |
| Não sei quais colunas uma tabela tem | Liste as colunas (`information_schema.columns`) |
| Não sei como as tabelas se conectam | Liste as foreign keys (`information_schema.table_constraints`) |
| Já sei as tabelas, mas não oJOIN | Procure colunas com `Id` no nome → essas são as ligações |

---

## O Problema

Para descobrir a empresa e instalação de um CampoModuloAtivo, você precisa navegar por 5 tabelas:

```
CampoModuloAtivo → ModuloAtivo → Ativo → Instalacao → Empresa
```

Fazer select por select é lento. A solução é usar **JOINs**.

---

## Mapa de Relacionamentos

```
Empresa (1) ──── (N) Instalacao
                        │
                        │ InstalacaoId
                        ▼
                     Ativo (1) ──── (N) ModuloAtivo
                                          │
                                          │ ModuloAtivoId
                                          ▼
                                   CampoModuloAtivo
```

| Tabela Filha | Coluna de Ligação | Tabela Pai |
|---|---|---|
| `Instalacao` | `EmpresaId` | `Empresa` |
| `Ativo` | `InstalacaoId` | `Instalacao` |
| `ModuloAtivo` | `AtivoId` | `Ativo` |
| `CampoModuloAtivo` | `ModuloAtivoId` | `ModuloAtivo` |

---

## Solução Completa (5 tabelas)

```sql
SELECT 
    e.Nome AS Empresa,
    i.Nome AS Instalacao,
    i.Codigo AS CodigoInstalacao,
    a.Nome AS Ativo,
    a.Codigo AS CodigoAtivo,
    ma.NomePersonalizadoModulo AS Modulo,
    cma.NomePersonalizadoCampo AS Campo
FROM CampoModuloAtivo cmae as 
INNER JOIN ModuloAtivo ma ON cma.ModuloAtivoId = ma.Id
INNER JOIN Ativo a ON ma.AtivoId = a.Id
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
INNER JOIN Empresa e ON i.EmpresaId = e.Id
WHERE cma.Id = 'B7A74886-8648-4326-A070-AD16F90F27A3'
```

---

## Como Montar um JOIN (Passo a Passo Prático)

Suponha que você quer: **"Listar os campos de módulo ativo com o nome da empresa"**

1. **Identifique as tabelas necessárias:** `CampoModuloAtivo`, `ModuloAtivo`, `Ativo`, `Instalacao`, `Empresa`

2. **Comece pela tabela filha (que tem os dados que você quer):**
   ```sql
   FROM CampoModuloAtivo cma
   ```

3. **Adicione o primeiro JOIN (a tabela pai mais próxima):**
   ```sql
   INNER JOIN ModuloAtivo ma ON cma.ModuloAtivoId = ma.Id
   ```

4. **Continue adicionando JOINs até chegar à tabela desejada:**
   ```sql
   INNER JOIN Ativo a ON ma.AtivoId = a.Id
   INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
   INNER JOIN Empresa e ON i.EmpresaId = e.Id
   ```

5. **Monte o SELECT com as colunas que precisa:**
   ```sql
   SELECT 
       cma.NomePersonalizadoCampo AS Campo,
       e.Nome AS Empresa
   FROM CampoModuloAtivo cma
   INNER JOIN ModuloAtivo ma ON cma.ModuloAtivoId = ma.Id
   INNER JOIN Ativo a ON ma.AtivoId = a.Id
   INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
   INNER JOIN Empresa e ON i.EmpresaId = e.Id
   ```

---

## Exercícios Práticos

### Nível 1 — 2 tabelas

**Exercício 1:**
 Liste o nome de todos os ativos e o nome da instalação onde estão localizados.

```sql
SELECT 
    a.Nome AS Ativo,
    i.Nome AS Instalacao
FROM Ativo a
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
```

**Exercício 2:**
 Liste o nome de todas as instalações e o nome da empresa que pertencem.

```sql
SELECT 
    i.Nome AS Instalacao,
    e.Nome AS Empresa
FROM Instalacao i
INNER JOIN Empresa e ON i.EmpresaId = e.Id
```

**Exercício 3:**
 Liste os módulos ativos e o nome do ativo ao qual pertencem.

```sql
SELECT 
    ma.Codigo AS Modulo,
    a.Nome AS Ativo
FROM ModuloAtivo ma
INNER JOIN Ativo a ON ma.AtivoId = a.Id
```

**Exercício 4:**
 Liste os campos do módulo ativo com o código do campo e o nome do campo.

```sql
SELECT 
    cma.Codigo AS CodigoCampoModulo,
    cma.NomePersonalizadoCampo AS CampoModulo,
    c.Codigo AS CodigoCampo,
    c.Nome AS NomeCampo
FROM CampoModuloAtivo cma
INNER JOIN Campo c ON cma.CampoId = c.Id
```

---

### Nível 2 — 3 tabelas

**Exercício 5:**
 Liste os campos de módulo ativo com o nome do módulo e o nome do ativo.

```sql
SELECT 
    cma.NomePersonalizadoCampo AS Campo,
    ma.NomePersonalizadoModulo AS Modulo,
    a.Nome AS Ativo
FROM CampoModuloAtivo cma
INNER JOIN ModuloAtivo ma ON cma.ModuloAtivoId = ma.Id
INNER JOIN Ativo a ON ma.AtivoId = a.Id
```

**Exercício 6:**
 Liste todos os ativos com sua instalação e empresa.

```sql
SELECT 
    a.Nome AS Ativo,
    i.Nome AS Instalacao,
    e.Nome AS Empresa
FROM Ativo a
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
INNER JOIN Empresa e ON i.EmpresaId = e.Id
```

**Exercício 7:**
 Liste os módulos ativos com o ativo e a instalação.

```sql
SELECT 
    ma.Codigo AS Modulo,
    a.Nome AS Ativo,
    i.Nome AS Instalacao
FROM ModuloAtivo ma
INNER JOIN Ativo a ON ma.AtivoId = a.Id
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
```

---

### Nível 3 — 4 tabelas

**Exercício 8:**
 Liste os campos de módulo ativo com módulo, ativo e instalação.

```sql
SELECT 
    cma.NomePersonalizadoCampo AS Campo,
    ma.NomePersonalizadoModulo AS Modulo,
    a.Nome AS Ativo,
    i.Nome AS Instalacao
FROM CampoModuloAtivo cma
INNER JOIN ModuloAtivo ma ON cma.ModuloAtivoId = ma.Id
INNER JOIN Ativo a ON ma.AtivoId = a.Id
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
```

**Exercício 9:**
 Liste os campos de módulo ativo com módulo, ativo e empresa.

```sql
SELECT 
    cma.NomePersonalizadoCampo AS Campo,
    ma.NomePersonalizadoModulo AS Modulo,
    a.Nome AS Ativo,
    e.Nome AS Empresa
FROM CampoModuloAtivo cma
INNER JOIN ModuloAtivo ma ON cma.ModuloAtivoId = ma.Id
INNER JOIN Ativo a ON ma.AtivoId = a.Id
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
INNER JOIN Empresa e ON i.EmpresaId = e.Id
```

---

### Nível 4 — 5 tabelas

**Exercício 10:**
 Liste os campos de módulo ativo com módulo, ativo, instalação e empresa.

```sql
SELECT 
    cma.NomePersonalizadoCampo AS Campo,
    ma.NomePersonalizadoModulo AS Modulo,
    a.Nome AS Ativo,
    i.Nome AS Instalacao,
    e.Nome AS Empresa
FROM CampoModuloAtivo cma
INNER JOIN ModuloAtivo ma ON cma.ModuloAtivoId = ma.Id
INNER JOIN Ativo a ON ma.AtivoId = a.Id
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
INNER JOIN Empresa e ON i.EmpresaId = e.Id
```

**Exercício 11 (desafio):**
 Liste todos os campos de módulo ativo da empresa "Treetech" que estão na instalação "Papel".

```sql
SELECT 
    cma.NomePersonalizadoCampo AS Campo,
    ma.NomePersonalizadoModulo AS Modulo,
    a.Nome AS Ativo,
    i.Nome AS Instalacao,
    e.Nome AS Empresa
FROM CampoModuloAtivo cma
INNER JOIN ModuloAtivo ma ON cma.ModuloAtivoId = ma.Id
INNER JOIN Ativo a ON ma.AtivoId = a.Id
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
INNER JOIN Empresa e ON i.EmpresaId = e.Id
WHERE e.Nome = 'Treetech' 
  AND i.Nome = 'Papel'
```

---

## Dicas

| Dica | Exemplo |
|---|---|
| Use **alias** (apelidos) para encurtar | `FROM Ativo a` em vez de `FROM Ativo` |
| Comece pela tabela filha e vá para a pai | `FROM CampoModuloAtivo cma INNER JOIN ModuloAtivo ma ON ...` |
| Use **AS** para renomear colunas no resultado | `e.Nome AS Empresa` |
| INNER JOIN retorna só registros com correspondência | Se quiser todos, use LEFT JOIN |
| Se não souber o nome da coluna, olhe as colunas da tabela | `information_schema.columns` |

---

## Erros Comuns

| Erro | Causa | Solução |
|---|---|---|
| `column reference is ambiguous` | Coluna com mesmo nome em duas tabelas | Use o alias: `a.Nome` em vez de `Nome` |
| `invalid reference to FROM-clause` | Tabela ou alias não existe | Verifique se a tabela foi adicionada no FROM ou JOIN |
| `missing FROM-clause` | Esqueceu de adicionar uma tabela no FROM | Adicione a tabela que está faltando |
| Resultado vazio | JOIN não encontrou correspondência | Verifique se as foreign keys estão corretas |

---

## View para Consultas Frequentes

```sql
CREATE VIEW vw_CampoModuloAtivo_Completo AS
SELECT 
    e.Nome AS Empresa,
    i.Nome AS Instalacao,
    i.Codigo AS CodigoInstalacao,
    a.Nome AS Ativo,
    a.Codigo AS CodigoAtivo,
    ma.Codigo AS CodigoModulo,
    ma.NomePersonalizadoModulo AS Modulo,
    cma.Codigo AS CodigoCampo,
    cma.NomePersonalizadoCampo AS Campo,
    cma.Id AS CampoModuloAtivoId
FROM CampoModuloAtivo cma
INNER JOIN ModuloAtivo ma ON cma.ModuloAtivoId = ma.Id
INNER JOIN Ativo a ON ma.AtivoId = a.Id
INNER JOIN Instalacao i ON a.InstalacaoId = i.Id
INNER JOIN Empresa e ON i.EmpresaId = e.Id
```

Depois basta consultar:

```sql
SELECT * FROM vw_CampoModuloAtivo_Completo 
WHERE CampoModuloAtivoId = 'B7A74886-8648-4326-A070-AD16F90F27A3'
```

---

## Links

- [[SQL/Conhecimentos em SQL|SQL]]
- [[SQL/Quiz - Praticando SELECT|Quiz SELECT]]
- [[Trabalho/Trabalho Conhecimento e atividades do dia a dia|Atividades do Trabalho]]
- [[Manu/Indice|Voltar ao Indice]]
