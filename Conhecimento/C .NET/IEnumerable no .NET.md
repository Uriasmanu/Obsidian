O `IEnumerable<T>` no .NET é uma [[Interface do .NET]] usada para representar coleções de objetos que podem ser percorridas sequencialmente. Ele faz parte do namespace `System.Collections.Generic` e é fundamental para trabalhar com coleções no .NET.

## 🔹 **O que é o `IEnumerable<T>`?**

`IEnumerable<T>` define um único método, `GetEnumerator()`, que retorna um **enumerador** (`IEnumerator<T>`) para percorrer os elementos da coleção.

Ele é usado para suportar **iteração com `foreach`**, permitindo que objetos de uma coleção sejam acessados sequencialmente sem expor a implementação interna.

## 🔹 **Diferença entre `IEnumerable<T>` e `List<T>`**

|Característica|`IEnumerable<T>`|`List<T>`|
|---|---|---|
|Modificável|❌ Não|✅ Sim|
|Acesso por índice|❌ Não|✅ Sim|
|Performance|✅ Melhor para grandes coleções|❌ Pior se houver muitas modificações|

⚠️ **Se precisar de acesso por índice (`list[0]`) ou adicionar/remover itens, use `List<T>`.**  
⚠️ **Se quiser apenas iterar sem modificar, `IEnumerable<T>` é mais eficiente.**