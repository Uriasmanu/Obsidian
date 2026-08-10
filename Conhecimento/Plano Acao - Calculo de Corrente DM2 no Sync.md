

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


# 10/08


O calculo não funcionou 100% como esperado, os campos `Get_ValorProporcionalCorrente` e `Set_AjusteFinoParaCalculoDeCorrente` ficaram com valor null na tabela

outra coisa que reparei é que ao acessar o E3 para ver como ele se comporta, vi que na parametrização do DM2 tem um campo `Get_ValorProporcionalCorrente` que ja vem por padrão como 24

Com o E3 esses dois campos `Get_ValorProporcionalCorrente` e `Set_AjusteFinoParaCalculoDeCorrente` tem o valor respectivo de 24 e 4095

quando eu altero o valor do campo Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Original no SDG de 0 para 100 no banco de dados Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Original fica igual a 1  e Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Corrente igual a 0,586080586080586 e Get_IndicacaoDeValorLidoNaEntradaAnalogicaI1_Convertido fica igual a 0
