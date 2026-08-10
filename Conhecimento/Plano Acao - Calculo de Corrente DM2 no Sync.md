

---

### 03/08/2026 - Plano de implementação definido

**Ação:** Defini o plano de implementação baseado na análise do PR de referência e da documentação.

**Plano de Implementação:**

1. **Criar documento de regra de negócio**
   - Seguir a lógica usada para os campos `16_M` e `16_U``Sigma.Sync.Run.Worker`
   - Criar arquivo dentro de `Algorithms` e colocar a Lógica: `IF Set_AjusteFinoParaCalculoDeCorrente = 0 THEN Set_AjusteFinoParaCalculoDeCorrente = 4095` 
   - Ver uma alternativa de adicionar de forma mais pratica o calculo `(Driver.General.DM2_1.Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Original * MDB_DM2_V1_2_1.Get_ValorProporcionalCorrente) / MDB_DM2_V1_2_1.Set_AjusteFinoParaCalculoDeCorrente` que se repete para os 24 campos de corrente

2. **mapeamento do DM2**
   - DM2 passa a ter o arquivo `DM2-algorithmFieldMaps-sync-import.json` com os campos: `Get_ValorProporcionalCorrente` e `Set_AjusteFinoParaCalculoDeCorrente`

3. **Atualizar arquivo de importação principal**
   - Arquivo: `DM2-sigma-sync-import`
   - Adicionar campos: `_Filtrado` e `_Convertido`, `_Corrente`
   - **Nota:** A doc diz que esses campos são criados apenas nas tabelas `H` e `S`, mas vou adicionar no JSON principal (criará nas 4 tabelas)


### 10/08/2026 - Resultados do cálculo e análise do comportamento

**Resultado:** O cálculo não funcionou 100% como esperado. Os campos `Get_ValorProporcionalCorrente` e `Set_AjusteFinoParaCalculoDeCorrente` ficaram com valor `null` na tabela.

**Comportamento no E3 (referência):**

| Campo                                 | Valor E3    |
| ------------------------------------- | ----------- |
| `Get_ValorProporcionalCorrente`       | 24 (padrão) |
| `Set_AjusteFinoParaCalculoDeCorrente` | 4095        |

**Teste manual de alteração no SDG:**

Ao alterar `Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Original` de `0` para `100` no banco de dados, os resultados foram:

E3

| Campo                                                     | Valor             |
| --------------------------------------------------------- | ----------------- |
| `Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Original`   | 100               |
| `Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Corrente`   | 0,586080586080586 |
| `Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Convertido` | 0                 |


**Comportamento no Sync:**

| Campo                                 | Valor E3 |
| ------------------------------------- | -------- |
| `Get_ValorProporcionalCorrente`       | Null     |
| `Set_AjusteFinoParaCalculoDeCorrente` | Null     |


| Campo                                                     | Valor             |
| --------------------------------------------------------- | ----------------- |
| `Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Original`   | 100               |
| `Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Corrente`   | 0,586080586080586 |
| `Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Convertido` | 0                 |