# Implantação e configuração de módulos de engenharia

> Documentação para execução da implantação de engenharia.

Existem duas maneiras das quais você pode configurar os Módulos de Engenharia, **pelo banco de dados, através de script**, ou pelo **Postman**.

Recomendo fortemente utilizar o método do **Banco**, ele é muito mais simples e bem mais rápido.

---
#Método via Banco de Dados
Para fazer via Banco de dados, você primeiramente irá precisar executar os [scripts auxiliares](https://dev.azure.com/treetech/SigmaFacelift/_wiki/wikis/SigmaFacelift.wiki/1604/M%C3%B3dulos-de-Engenharia) dos módulos necessários para seu projeto.

Após executado os scripts auxiliares, é só você executar os scripts de configuração, colocando os ativos do seu projeto e também alterando os módulos dos campos.

![image.png](/.attachments/image-66cd0cbc-3fee-4ca5-8f7e-f84bb105eb00.png)
![image.png](/.attachments/image-caa631b5-852b-4acc-afac-6900c47aa8fc.png)

Segue em anexo os arquivos de cada módulo:
- [eng-agua-papel-config.sql](/.attachments/eng-agua-papel-config-4f6d957a-7c6d-4d1d-8f61-34b6e000187e.sql)
- [eng-diferencial-temperatura-comutador-config.sql](/.attachments/eng-diferencial-temperatura-comutador-config-0c0057fc-807a-4f7a-ab2b-272b50362bae.sql)
- [eng-eficiencia-resfriamento-config.sql](/.attachments/eng-eficiencia-resfriamento-config-ccc2f02b-5c06-47ff-8f9c-c1d3ed056d18.sql)
- [eng-envelhecimento-isolacao-config.sql](/.attachments/eng-envelhecimento-isolacao-config-fa444680-2c3a-4385-b7a5-5ce8b061733a.sql)
- [eng-gradiente-final-config.sql](/.attachments/eng-gradiente-final-config-1d95478e-2d15-479f-b166-d3b3fc9685a7.sql)
- [eng-manutencao-comutador-config.sql](/.attachments/eng-manutencao-comutador-config-e505665f-dfd0-44e3-ae41-95c9e53ada4d.sql)
- [eng-simulacao-carga-config.sql](/.attachments/eng-simulacao-carga-config-891a569c-509f-46d8-94c7-3b2950017a2c.sql)
- [sup-temperatura-ambiente-config.sql](/.attachments/sup-temperatura-ambiente-config-6e9b65b8-799a-43a1-aa34-6ed367ed92a0.sql)
---
#Método via Postman
## Configuração via API

> Para configurar os módulos de engenharia via API, você vai precisar primeiro baixar o [Postman](https://www.postman.com/downloads/) e importar a [Collection](/.attachments/ModulosEngenharia.postman_collection-418c6467-6f24-40b9-95af-352259156626.json) e os [Environments](/.attachments/ecm-impl.postman_environment-907bd7af-1b87-4ee9-a445-cbf054da5820.json).
Após a importação, no canto superior direito, você deve colocar os Environments: ![image.png](/.attachments/image-9a0e5461-f84b-4d3d-ac9e-d1759576bdec.png)
Nos Environments, você consegue alterar a url da API, e o usuário e a senha para poder fazer o login por Bearer Token
![image.png](/.attachments/image-1a6e4821-9b51-4276-bf5d-ae72f945c02f.png)
O Token é pego de forma automática e você não precisa se preocupar com ele, para autenticar você precisa abrir o método POST ObtemTokenSuperAdmin e clicar em Send em azul, não se esqueça de estar logado na VPN.
![image.png](/.attachments/image-a0d7703a-6d3c-4898-af6c-6b55af3735fe.png)
Nós módulos, altere a Chave moduloAtivoId:
![image.png](/.attachments/image-e777d7d3-fe55-46ff-84ef-0d2c159176c6.png)
Para descobrir o módulo ativo id, basta fazer uma busca no banco, procurando pelo módulo e o ativo.
Já na parte do Body, você vai colocar os Valores para as Chaves, onde os Valores são os Campos Módulos Ativos:
![image.png](/.attachments/image-0d76578a-72ad-422f-8085-fe9ef3225193.png)
Por exemplo, se eu quiser saber qual é os Valores para as Chaves, eu utilizo os scripts disponíveis de cada módulo, substituindo a instalação e o ativo, e então eu pego os ids dos campos módulos ativos e substituo na chave correta.
Depois de ter alterado tudo, é só clicar no botão Send e verificar o resultado (O resultado esperado é 200) Caso de, por exemplo, 401, autentique novamente por que perdeu a chave de acesso.

---


##Associações de engenharia
> Os módulos de engenharia, diferentemente dos módulos de supervisão, não são elementos físicos, reais, mas sim, cálculos, onde as Propriedades são os elementos para a fórmula e os Campos dos módulos de supervisão são o que conectam valores para os elementos.


## Água no Papel
### Script para pegar os ids dos Campos Módulos Ativos: [agua-papel.sql](/.attachments/agua-papel-5fd1a044-6775-4c9e-a900-28bc7c51e741.sql)

### Fontes de comparação
| Propriedade | Campo | CampoId |
| :---------: | :---------: | :---------: | 
| temperaturaAmbienteId | GET_IndicacaoDeTemperaturaMedidaPeloRtdA | 59995DBD-19B9-4F4E-AEAA-AA6EDB36B926 |
| temperaturaOleoId | GET_IndicacaoDeTemperaturaDoOleo | F8E3FE96-5F76-4BE2-A8BF-C08352F114DA |
| umidadeRelativaOleoId | GET_IndicacaoDeSaturacaoRelativa | AAC7AA18-2B65-4109-8E7F-4373ADC93103 |
| enrolamento1.temperaturaId | GET_IndicacaoDeTemperaturaDoEnrolamento1 | CF29C51F-4EEE-4D49-85C8-58E614F2622B |
| enrolamento2.temperaturaId | GET_Tm2IndicacaoDeTemperaturaDoEnrolamento2 | EF35E552-8F84-404A-89F8-8B0174BDF283 |
| enrolamento3.temperaturaId | GET_Tm2IndicacaoDeTemperaturaDoEnrolamento3 | 62CA1F4C-B982-4F9A-8195-39FDB8EA51B4 |

## Envelhecimento Isolação

### Script para pegar os ids dos Campos Módulos Ativos: [envelhecimento-isolacao.sql](/.attachments/envelhecimento-isolacao-98c276f3-db96-4167-be4f-7b13aa6e8552.sql)

### Fontes de comparação

| Propriedade | Campo | CampoId |
| :---------: | :---------: | :---------: | 
| enrolamento1.temperaturaId | GET_IndicacaoDeTemperaturaDoEnrolamento1 | CF29C51F-4EEE-4D49-85C8-58E614F2622B |
| enrolamento2.temperaturaId | GET_Tm2IndicacaoDeTemperaturaDoEnrolamento2 | EF35E552-8F84-404A-89F8-8B0174BDF283 |
| enrolamento3.temperaturaId | GET_Tm2IndicacaoDeTemperaturaDoEnrolamento3 | 62CA1F4C-B982-4F9A-8195-39FDB8EA51B4 |

## Gradiente Final

### Script para pegar os ids dos Campos Módulos Ativos: [gradiente-final.sql](/.attachments/gradiente-final-d4cf33c0-690d-444b-8f63-8e56f9d30c0b.sql)

### Fontes de comparação

| Propriedade | Campo | CampoId |
| :---------: | :---------: | :---------: | 
| temperaturaOleoId | GET_IndicacaoDeTemperaturaDoOleo | F8E3FE96-5F76-4BE2-A8BF-C08352F114DA |
| constanteTempoOleoId | SET_ParametroDeConstanteDeTempoDaInerciaTermicaDoEnrolamento1 | A7AC7155-F81C-44FE-A166-CD5A0BCEB1D2 |
| enrolamento1.temperaturaEnrolamentoId | GET_IndicacaoDeTemperaturaDoEnrolamento1 | CF29C51F-4EEE-4D49-85C8-58E614F2622B |
| enrolamento1.gradienteFinalEnrolamentoOleoId | GET_IndicacaoDeGradienteFinalDeTemperaturaDoEnrolamento1AposEstabilizacaoTermica | A3876001-8CDD-4661-A241-EB5E66CD1924 |
| enrolamento1.temperaturaAlarmeTemperaturaEnrolamentoId | SET_ParametroDeAlarmePorTemperaturaDoEnrolamento1 | C118A2B8-45F7-4331-8976-BB6A8328993D |
| enrolamento1.temperaturaDesligamentoTemperaturaEnrolamentoId | SET_ParametroDeDesligamentoPorTemperaturaDoEnrolamento1 | 8C0A0D80-2BD4-4256-BD54-D799012B0A00 |
| enrolamento1.percentualCarregamentoId | GET_IndicacaoDePercentualDeCargaDoEnrolamento1 | 859D2A2A-B8CD-43F0-8DD2-3C73C217D80D |
| enrolamento2.temperaturaEnrolamentoId | GET_Tm2IndicacaoDeTemperaturaDoEnrolamento2 | EF35E552-8F84-404A-89F8-8B0174BDF283 |
| enrolamento2.gradienteFinalEnrolamentoOleoId | GET_Tm2IndicacaoDeGradienteFinalDeTemperaturaDoEnrolamento2AposEstabilizacaoTermica | B89F09B2-5C06-47B4-979C-4DF7991465C0 |
| enrolamento2.temperaturaAlarmeTemperaturaEnrolamentoId | SET_Tm2ParametroDeAlarmePorTemperaturaDoEnrolamento2 | B963DF40-D405-489D-B260-640138D2D1CA |
| enrolamento2.temperaturaDesligamentoTemperaturaEnrolamentoId | SET_Tm2ParametroDeDesligamentoPorTemperaturaDoEnrolamento2 | 777EA9E9-A40F-469E-92B5-5CCC3BB79CD8 |
| enrolamento2.percentualCarregamentoId | GET_Tm2IndicacaoDePercentualDeCargaDoEnrolamento2 | 2426C9D6-7B14-4171-84E0-A4EFD2240E24 |
| enrolamento3.temperaturaEnrolamentoId | GET_Tm2IndicacaoDeTemperaturaDoEnrolamento3 | 62CA1F4C-B982-4F9A-8195-39FDB8EA51B4 |
| enrolamento3.gradienteFinalEnrolamentoOleoId | GET_Tm2IndicacaoDeGradienteFinalDeTemperaturaDoEnrolamento3AposEstabilizacaoTermica | 60BD8799-4811-44A6-9513-78B285DAC42A |
| enrolamento3.temperaturaAlarmeTemperaturaEnrolamentoId | SET_Tm2ParametroDeAlarmePorTemperaturaDoEnrolamento3 | 7B8F3650-2647-423C-93ED-9613157BF8E5 |
| enrolamento3.temperaturaDesligamentoTemperaturaEnrolamentoId | SET_Tm2ParametroDeDesligamentoPorTemperaturaDoEnrolamento3 | 6F025AAE-DDF1-4873-860D-675E0B94B050 |
| enrolamento3.percentualCarregamentoId | GET_Tm2IndicacaoDePercentualDeCargaDoEnrolamento3 | 7B42A418-82E4-4618-BDB0-1AB795356678 |

## Eficiência Resfriamento

### Script para pegar os ids dos Campos Módulos Ativos: [eficiencia-resfriamento.sql](/.attachments/eficiencia-resfriamento-ac75f31d-b0c8-4d32-ac9f-2e937da178a5.sql)

### Fontes de comparação
| Propriedade | Campo | CampoId |
| :---------: | :---------: | :---------: | 
| carregamentoId | GET_IndicacaoDePercentualDeCargaDoEnrolamento1 | 859D2A2A-B8CD-43F0-8DD2-3C73C217D80D |
| estagioResfriamentoId | Get_IndicacaoDeEstagioAtualDeResfriamento | 5950E403-D791-49E4-987A-0E70D6295646 |
| temperaturaAmbienteId | GET_IndicacaoDeTemperaturaMedidaPeloRtdA | 59995DBD-19B9-4F4E-AEAA-AA6EDB36B926 |
| temperaturaOleoMedidaId | GET_IndicacaoDeTemperaturaDoOleo | F8E3FE96-5F76-4BE2-A8BF-C08352F114DA |

## Manutenção Comutador

### Script para pegar os ids dos Campos Módulos Ativos: [manutencao-comutador.sql](/.attachments/manutencao-comutador-8ef2aea2-bdfa-4c3f-b7d5-f067e56a4d46.sql)

### Fontes de comparação
| Propriedade | Campo | CampoId |
| :---------: | :---------: | :---------: | 
| comutador1.numeroTotalOperacoesId | SET_ParametroDeNumeroTotalDeOperacoesDoComutador | 649D31F9-A4F1-400F-9656-CB86C26C5147 |
| comutador1.tempoTotalServicoDesdeUltimaManutencaoId | - | - |
| comutador1.tempoRestanteParaManutencaoPorTempoServicoId | - | - |
| comutador1.numeroOperacoesDesdeUltimaManutencaoId | SET_ParametroDeNumeroDeOperacoesDoComutadorDesdeAUltimaManutencao | 5B7355B4-35C5-41ED-9C4A-68D2694A6854 |
| comutador1.mediaOperacoesDiariaId | GET_IndicacaoDeMediaDeOperacoesPorDia | DF9E962C-EDE9-4223-9699-561C8D54F6E8 |
| comutador1.tempoRestanteParaManutencaoPorI2PUId | GET_IndicacaoDeDiasDeAvisoDeManutencaoPorIpu2 | D03A5854-C927-42DD-88EB-73ABACDF0576 |
| comutador1.tempoRestanteParaManutencaoPorNumeroOperacoesId | - | - |
| comutador1.somaI2PUId | - | - |
| comutador1.somaI2PUDesdeUltimaManutencaoId | SET_ParametroDeValorDaSomatoriaDeIpu2AposAUltimaManutencao | D304142C-7132-4C21-9ADA-E61DC4B681FD |
| comutador1.mediaDiariaI2PUId | GET_IndicacaoDeMediaDeIpu2PorDia | B7B93237-BAFD-4C48-8397-E052C71D6BB4 |
| comutador1.limiteComutacaoId | - | - |
| comutador1.limiteI2PUId | SET_ParametroDeValorDaSomatoriaDeIpu2ParaAvisoDeManutencao | F59E2465-89FE-4B5C-AAD9-299848B89E2D |
| comutador2.numeroTotalOperacoesId | SET_ParametroDeNumeroTotalDeOperacoesDoComutador | 649D31F9-A4F1-400F-9656-CB86C26C5147 |
| comutador2.tempoTotalServicoDesdeUltimaManutencaoId | - | - |
| comutador2.tempoRestanteParaManutencaoPorTempoServicoId | - | - |
| comutador2.numeroOperacoesDesdeUltimaManutencaoId | SET_ParametroDeNumeroDeOperacoesDoComutadorDesdeAUltimaManutencao | 5B7355B4-35C5-41ED-9C4A-68D2694A6854 |
| comutador2.mediaOperacoesDiariaId | GET_IndicacaoDeMediaDeOperacoesPorDia | DF9E962C-EDE9-4223-9699-561C8D54F6E8 |
| comutador2.tempoRestanteParaManutencaoPorI2PUId | GET_IndicacaoDeDiasDeAvisoDeManutencaoPorIpu2 | D03A5854-C927-42DD-88EB-73ABACDF0576 |
| comutador2.tempoRestanteParaManutencaoPorNumeroOperacoesId | - | - |
| comutador2.somaI2PUId | - | - |
| comutador2.somaI2PUDesdeUltimaManutencaoId | SET_ParametroDeValorDaSomatoriaDeIpu2AposAUltimaManutencao | D304142C-7132-4C21-9ADA-E61DC4B681FD |
| comutador2.mediaDiariaI2PUId | GET_IndicacaoDeMediaDeIpu2PorDia | B7B93237-BAFD-4C48-8397-E052C71D6BB4 |
| comutador2.limiteComutacaoId | - | - |
| comutador2.limiteI2PUId | SET_ParametroDeValorDaSomatoriaDeIpu2ParaAvisoDeManutencao | F59E2465-89FE-4B5C-AAD9-299848B89E2D |
| comutador3.numeroTotalOperacoesId | SET_ParametroDeNumeroTotalDeOperacoesDoComutador | 649D31F9-A4F1-400F-9656-CB86C26C5147 |
| comutador3.tempoTotalServicoDesdeUltimaManutencaoId | - | - |
| comutador3.tempoRestanteParaManutencaoPorTempoServicoId | - | - |
| comutador3.numeroOperacoesDesdeUltimaManutencaoId | SET_ParametroDeNumeroDeOperacoesDoComutadorDesdeAUltimaManutencao | 5B7355B4-35C5-41ED-9C4A-68D2694A6854 |
| comutador3.mediaOperacoesDiariaId | GET_IndicacaoDeMediaDeOperacoesPorDia | DF9E962C-EDE9-4223-9699-561C8D54F6E8 |
| comutador3.tempoRestanteParaManutencaoPorI2PUId | GET_IndicacaoDeDiasDeAvisoDeManutencaoPorIpu2 | D03A5854-C927-42DD-88EB-73ABACDF0576 |
| comutador3.tempoRestanteParaManutencaoPorNumeroOperacoesId | - | - |
| comutador3.somaI2PUId | - | - |
| comutador3.somaI2PUDesdeUltimaManutencaoId | SET_ParametroDeValorDaSomatoriaDeIpu2AposAUltimaManutencao | D304142C-7132-4C21-9ADA-E61DC4B681FD |
| comutador3.mediaDiariaI2PUId | GET_IndicacaoDeMediaDeIpu2PorDia | B7B93237-BAFD-4C48-8397-E052C71D6BB4 |
| comutador3.limiteComutacaoId | - | - |
| comutador3.limiteI2PUId | SET_ParametroDeValorDaSomatoriaDeIpu2ParaAvisoDeManutencao | F59E2465-89FE-4B5C-AAD9-299848B89E2D |

## Diferencial Temperatura do Comutador

### Script para pegar os ids dos Campos Módulos Ativos: [diferencial-temperatura-comutador.sql](/.attachments/diferencial-temperatura-comutador-62cdc678-2143-497b-9a18-6d501f1dd2de.sql)

### Fontes de comparação
| Propriedade | Campo | CampoId |
| :---------: | :---------: | :---------: | 
| temperaturaOleoId | GET_IndicacaoDeTemperaturaDoOleo | F8E3FE96-5F76-4BE2-A8BF-C08352F114DA |
| comutador1.temperaturaComutadorId | GET_IndicacaoDeTemperaturaDoOleoDoComutador1 | 8C96C894-5C99-45B0-BB2D-1C64FF2301C7 |
| comutador1.diferencialTemperaturaInstantaneoValorId | GET_IndicacaoDeDiferencialDeTemperaturaInstantaneoComutador1 | E2D45CD4-8A85-4FD3-A00E-BF7DD5FE2BDB |
| comutador1.diferencialTemperaturaInstantaneoValorMaximoIedId | GET_IndicacaoDeMaiorValorDeDiferencialDeTemperaturaComutador1 | EF8C322C-7DDF-44B8-9FEB-839A7EA1F10C |
| comutador1.diferencialTemperaturaInstantaneoAlarmeId | SET_ParametroDeAlarmePorDiferencialDeTemperaturaInstantaneoDoComutador | D82734F8-F0A1-45E4-A750-BC9BBE68F5F1 |
| comutador1.diferencialTemperaturaInstantaneoAjusteAlarmeIedId | SET_ParametroDeAlarmePorDiferencialDeTemperaturaInstantaneoDoComutador | D82734F8-F0A1-45E4-A750-BC9BBE68F5F1 |
| comutador1.diferencialTemperaturaFiltradoValorId | GET_IndicacaoDeDiferencialDeTemperaturaFiltradoComutador1 | 18CDAB64-C077-4413-A7A8-85AF07A72F30 |
| comutador1.diferencialTemperaturaFiltradoValorMaximoIedId | GET_IndicacaoDeMaiorValorDeDiferencialDeTemperaturaFiltradoComutador1 | C3828127-6CFC-46CC-ACF2-0A2A5631FD99 |
| comutador1.diferencialTemperaturaFiltradoAlarmeId | SET_ParametroDeAlarmePorDiferencialDeTemperaturaFiltradoDoComutador | 93F7D724-2F46-4E3B-93CB-9D9C2AA00160 |
| comutador1.diferencialTemperaturaFiltradoAjusteAlarmeIedId | SET_ParametroDeAlarmePorDiferencialDeTemperaturaFiltradoDoComutador | 93F7D724-2F46-4E3B-93CB-9D9C2AA00160 |
| comutador1.percentualCarregamentoId | GET_IndicacaoDePercentualDeCargaDoEnrolamento1 | 859D2A2A-B8CD-43F0-8DD2-3C73C217D80D |
| comutador1.tapAtualId | GET_IndicacaoDePosicaoDeTapAtual | 8F204A24-5FD4-4082-B52C-1B76848F6933 |
| comutador1.constanteTempoFiltragemDiferenciaisTemperaturaIedId | SET_ParametroDeConstanteDeTempoParaFiltroDoDiferencialDeTemperaturaDoComutador | 071091A6-CA31-446E-A1D0-5EAEC0EC6168 |
| comutador2.temperaturaComutadorId | GET_IndicacaoDeTemperaturaDoOleoDoComutador2 | 77DDABBB-A50A-49C5-A88C-01F622E4273A |
| comutador2.diferencialTemperaturaInstantaneoValorId | GET_IndicacaoDeDiferencialDeTemperaturaInstantaneoComutador2 | D5A28DE6-CB27-45A3-9A56-152D0EC56FFD |
| comutador2.diferencialTemperaturaInstantaneoValorMaximoIedId | GET_IndicacaoDeMaiorValorDeDiferencialDeTemperaturaComutador2 | 9CCF1FF3-2CA4-4212-9415-4747B1CA7304 |
| comutador2.diferencialTemperaturaInstantaneoAlarmeId | SET_ParametroDeAlarmePorDiferencialDeTemperaturaInstantaneoDoComutador | D82734F8-F0A1-45E4-A750-BC9BBE68F5F1 |
| comutador2.diferencialTemperaturaInstantaneoAjusteAlarmeIedId | SET_ParametroDeAlarmePorDiferencialDeTemperaturaInstantaneoDoComutador | D82734F8-F0A1-45E4-A750-BC9BBE68F5F1 |
| comutador2.diferencialTemperaturaFiltradoValorId | GET_IndicacaoDeDiferencialDeTemperaturaFiltradoComutador2 | E2ACD54A-7062-4339-82B7-8F2BAE78F29F |
| comutador2.diferencialTemperaturaFiltradoValorMaximoIedId | GET_IndicacaoDeMaiorValorDeDiferencialDeTemperaturaFiltradoComutador2 | 12C2E55A-6D3B-438A-8614-95D0BBB4A8DC |
| comutador2.diferencialTemperaturaFiltradoAlarmeId | SET_ParametroDeAlarmePorDiferencialDeTemperaturaFiltradoDoComutador | 93F7D724-2F46-4E3B-93CB-9D9C2AA00160 |
| comutador2.diferencialTemperaturaFiltradoAjusteAlarmeIedId | SET_ParametroDeAlarmePorDiferencialDeTemperaturaFiltradoDoComutador | 93F7D724-2F46-4E3B-93CB-9D9C2AA00160 |
| comutador2.percentualCarregamentoId | GET_Tm2IndicacaoDePercentualDeCargaDoEnrolamento2 | 2426C9D6-7B14-4171-84E0-A4EFD2240E24 |
| comutador2.tapAtualId | GET_IndicacaoDePosicaoDeTapAtual | 8F204A24-5FD4-4082-B52C-1B76848F6933 |
| comutador2.constanteTempoFiltragemDiferenciaisTemperaturaIedId | SET_ParametroDeConstanteDeTempoParaFiltroDoDiferencialDeTemperaturaDoComutador | 071091A6-CA31-446E-A1D0-5EAEC0EC6168 |
| comutador3.temperaturaComutadorId | GET_IndicacaoDeTemperaturaMaximaDoComutador3 | F37D0235-F053-4069-93DE-EEAB6C8D062F |
| comutador3.diferencialTemperaturaInstantaneoValorId | GET_IndicacaoDeDiferencialDeTemperaturaInstantaneoComutador3 | A694B65D-A698-4C18-BB01-C72E333FFF32 |
| comutador3.diferencialTemperaturaInstantaneoValorMaximoIedId | GET_IndicacaoDeMaiorValorDeDiferencialDeTemperaturaComutador3 | A335F0DE-604C-4D9E-8EB7-34521F1F52B9 |
| comutador3.diferencialTemperaturaInstantaneoAlarmeId | SET_ParametroDeAlarmePorDiferencialDeTemperaturaInstantaneoDoComutador | D82734F8-F0A1-45E4-A750-BC9BBE68F5F1 |
| comutador3.diferencialTemperaturaInstantaneoAjusteAlarmeIedId | SET_ParametroDeAlarmePorDiferencialDeTemperaturaInstantaneoDoComutador | D82734F8-F0A1-45E4-A750-BC9BBE68F5F1 |
| comutador3.diferencialTemperaturaFiltradoValorId | GET_IndicacaoDeDiferencialDeTemperaturaFiltradoComutador3 | A3E706A1-F6F0-453C-A4EB-0EBFFE8C2D51 |
| comutador3.diferencialTemperaturaFiltradoValorMaximoIedId | GET_IndicacaoDeMaiorValorDeDiferencialDeTemperaturaFiltradoComutador3 | 3FE8D1E5-1972-43F4-95A7-F9C188D4B111 |
| comutador3.diferencialTemperaturaFiltradoAlarmeId | SET_ParametroDeAlarmePorDiferencialDeTemperaturaFiltradoDoComutador | 93F7D724-2F46-4E3B-93CB-9D9C2AA00160 |
| comutador3.diferencialTemperaturaFiltradoAjusteAlarmeIedId | SET_ParametroDeAlarmePorDiferencialDeTemperaturaFiltradoDoComutador | 93F7D724-2F46-4E3B-93CB-9D9C2AA00160 |
| comutador3.percentualCarregamentoId | GET_Tm2IndicacaoDePercentualDeCargaDoEnrolamento3 | 7B42A418-82E4-4618-BDB0-1AB795356678 |
| comutador3.tapAtualId | GET_IndicacaoDePosicaoDeTapAtual | 8F204A24-5FD4-4082-B52C-1B76848F6933 |
| comutador3.constanteTempoFiltragemDiferenciaisTemperaturaIedId | SET_ParametroDeConstanteDeTempoParaFiltroDoDiferencialDeTemperaturaDoComutador | 071091A6-CA31-446E-A1D0-5EAEC0EC6168 |

## Simulação de Carga

### Script para pegar os ids dos Campos Módulos Ativos: [simulacao-carga.sql](/.attachments/simulacao-carga-eb286ec1-1728-4ddc-998e-506c5b76c80e.sql)

### Fontes de comparação
| Propriedade | Campo | CampoId |
| :---------: | :---------: | :---------: | 
| temperaturaInicialOleoId | GET_IndicacaoDeTemperaturaDoOleo | F8E3FE96-5F76-4BE2-A8BF-C08352F114DA |
| temperaturaInicialEnrolamentoId | GET_IndicacaoDeTemperaturaDoEnrolamento1 | CF29C51F-4EEE-4D49-85C8-58E614F2622B |
| fatorHotspotEnrolamentoId | SET_ParametroDeFatorDeHotSpotIecHs | 3D56DA72-4D56-47B1-899C-C6C3CCE0B3FA |
| constanteTempoEnrolamentoId | SET_ParametroDeConstanteDeTempoDaInerciaTermicaDoEnrolamento1 | A7AC7155-F81C-44FE-A166-CD5A0BCEB1D2 |
| histereseDesligamentoResfriamentoId | SET_ParametroDeHistereseDoResfriamento | 477B6AC2-5EF7-4F53-9C65-78B69F3BC0F5 |
| temperaturaAlarmeOleoId | SET_ParametroDeAlarmePorTemperaturaDoOleo | 1D4A92CC-5E39-46A6-91F6-A39C56497399 |
| temperaturaDesligamentoOleoId | SET_ParametroDeDesligamentoPorTemperaturaDoOleo | 8F44A68D-7063-4721-9913-348C7A4E0FAE |
| temperaturaAlarmeEnrolamentoId | SET_ParametroDeAlarmePorTemperaturaDoEnrolamento1 | C118A2B8-45F7-4331-8976-BB6A8328993D |
| temperaturaDesligamentoEnrolamentoId | SET_ParametroDeDesligamentoPorTemperaturaDoEnrolamento1 | 8C0A0D80-2BD4-4256-BD54-D799012B0A00 |
| temperaturaOperacaoAutomaticaEstagio1Id | SET_ParametroDeTemperaturaDePartidaDoEstagioDeResfriamento1 | 515B2AAE-C1FA-4550-B6EC-4FF49A425A32 |
| temperaturaOperacaoAutomaticaEstagio2Id | SET_ParametroDeTemperaturaDePartidaDoEstagioDeResfriamento2 | A50271B4-6679-4C80-B766-E5775C3173A6 |
| temperaturaOperacaoAutomaticaEstagio3Id | SET_ParametroDeTemperaturaDePartidaDoEstagioDeResfriamento3 | 0F08F5ED-1CBD-4DDB-961A-7180EE9413B4 |
| temperaturaOperacaoAutomaticaEstagio4Id | SET_ParametroDeTemperaturaDePartidaDoEstagioDeResfriamento4 | 0186DAF7-C69B-40F9-86A6-66D0864EB4E0 |