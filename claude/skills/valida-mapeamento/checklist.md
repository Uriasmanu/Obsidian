# Passo a Passo de Validação — Detalhamento

Detalhamento completo de cada item do "Quick Reference" do `SKILL.md`. A ordem importa: primeiro fecha a consistência interna desta versão (csv ↔ script ↔ JSON), só depois compara com versão anterior (se houver), só depois valida o SYNC, e por último o relatório.

## Bloco A — csv ↔ script ↔ JSON desta versão

1. **Ler os arquivos.** JSON de mapeamento e script SQL (`fl.sql`, `GruposPadrao.sql`, `VersaoRecurso.sql`) do protocolo escolhido, mais o .csv/Excel de origem.
2. **Espelhamento JSON ↔ SQL.** Todo campo e todo ID do SQL devem aparecer, idênticos, no JSON de mapeamento (e vice-versa) — não é só "parecido", tem que bater 1:1. Extrair todo `DECLARE @XxxId ... = 'valor'` do script (`@ModuloId`, `@CampoIdN`, `@AlarmeIdN`, etc.) e conferir se o mesmo ID aparece no JSON.
3. **Mnemônicos únicos dentro do arquivo.** Nenhum mnemônico pode se repetir dentro do mesmo arquivo. **Se encontrar duplicidade, não resolver sozinho** (ex: não inventar um sufixo tipo "2" para desempatar) — só reportar para a Manu avaliar.
3b. **Tamanho do mnemônico (máx. 50 caracteres).** Nenhum mnemônico vindo do csv pode passar de 50 caracteres (restrição das libs do Postgres; o limite antigo era 116). Conferir no csv, `fl.sql`, `fl.json` e SYNC. Se o mnemônico longo for **herdado** de versão/protocolo anterior (mesmo UUID, mesmo mnemônico), reportar como ponto de atenção para a Manu avaliar, não como erro — trocar quebraria a regra do item 12.
3c. **Formato do mnemônico.** Tudo minúsculo, sem `_` separando palavras, sem acento, espaço ou caractere especial — regex `^[a-z0-9]+$` (ex: `tensaoentrada`, `indtempmaxsens1`). Não se aplica aos metadados do framework (`VersaoProduto`, `VersaoMapa`, `HashCommitMapa`, `DataHoraUltimaLeituraSensor`), ver "Exceções" no `SKILL.md`.
3d. **Abreviações padrão (só aviso).** Se um mnemônico usa a palavra inteira onde existe abreviação padrão, listar como sugestão, nunca como erro: `IndicacaoDe`→`IndDe`, `ParametroDe`→`ParamDe`, `temperatura`→`temp`, `tendencia`→`tend`, `referencia`→`ref`, `alarme`→`alm`, `autodiagnostico`→`autodiag`, `corrente`→`corr`, `tensao`→`tens`, `frequencia`→`freq`, `configuracao`→`config`, `habilitacao`→`hab`, `desabilitacao`→`desab`, `limite`→`lim`, `status`→`stat`, `comunicacao`→`com`, `valor`→`val`, `maxima`→`max`, `minima`→`min`, `media`→`med`, `sensor`→`sens`, `conjunto`→`conj`, `indicacao`→`ind`, `parametro`→`param`. Mnemônico herdado de versão/protocolo anterior não entra nesse aviso.
4. **Descrições únicas dentro do arquivo.** Mesma regra do item 3, aplicada às descrições em vez dos mnemônicos: nenhuma repetida dentro do arquivo, e não resolver duplicidade sozinho, só reportar.
5. **E3Lib.** O valor do `E3Lib` do script tem que ser idêntico ao `E3Lib` do JSON de mapeamento.
5b. **Imagem do módulo.** O campo `Imagem` (`fl.sql` e `fl.json`) segue por padrão `<E3Lib>.svg` (o mesmo valor do `E3Lib` daquele módulo, com extensão `.svg`). Conferir também que o valor é idêntico entre `fl.sql` e `fl.json`. Se o nome do arquivo de imagem não bater com `<E3Lib>.svg`, reportar a divergência para a Manu avaliar (pode ser um caso válido de imagem compartilhada entre módulos, mas não presumir isso sozinho).
6. **IDs no GruposPadrao/VersaoRecurso.** Todos os IDs existentes no `fl.sql` (ModuloId + CampoIds + AlarmeIds) têm que constar também em `GruposPadrao.sql` e em `VersaoRecurso.sql`.
6b. **Conteúdo de `TagsVersaoMapa`/`TagsVersaoFirmware` no `VersaoRecurso.sql`.**
    - `TagsVersaoMapa` segue o formato `v<major>-<PROTOCOLO>` (`MDB` ou `DNP`), **sem minor** — ex: TAGs de engenharia `eng_mdb_13.0`, `eng_mdb_13.2`, `eng_mdb_13.3` viram só `v13-MDB`. Mais de uma versão fica separada por `;` (ex: `v2-MDB;v2-DNP;v17-MDB;v17-DNP`).
    - `TagsVersaoFirmware` segue o formato `v<major>[fw<descritivo>]`, **sem protocolo** e sem espaço extra entre os caracteres (ex: `v2[fw2.08R2-2.10R1]`).
    - **O script `VersaoRecurso.sql` de uma pasta de versão só pode conter tags dessa mesma versão** — ex: o script da pasta `V2` só define tags `v2-*`, o da `V17` só `v17-*`, mesmo que o recurso exista nas duas versões (a concatenação acontece ao rodar os dois scripts em sequência, não escrevendo as duas tags no mesmo script). Reportar como erro se aparecer tag de outra versão major dentro do script de uma versão.
    - Para o recurso `ModuloAtivo` (código 4): tem que haver **exatamente uma** definição de `TagsVersaoMapa` (formato `v<major>-<PROTOCOLO>`) e `TagsVersaoFirmware` **tem que estar em branco**.
7. **Identificar e cruzar o csv/Excel de origem.** É o arquivo que traz o hash de commit no nome ou o arquivo com o mesmo nome do csv dentro da pasta zipada — **não é o `modulo.csv` genérico, nem um arquivo com nome igual ao `E3Lib`** (ex: `BM.csv`). Esse tipo costuma ser export de tags OPC/Archestra (colunas como `ObjectType;Name;AdviseType;...AllowRead;AllowWrite`), sem UUID, sem "Mnemônico" e sem "Gráfico Rápido" — para confirmar que achou o arquivo certo, checar se ele tem colunas `UUID` e `Mnemônico`. Depois de identificado, cruzar com SQL e JSON — os três têm que bater entre si. **Atenção ao formato do UUID**: no csv costuma vir sem hífen (`1ca40722324346a1b92e56270fd35ea7`), SQL/JSON com hífen (`1ca40722-3243-46a1-b92e-56270fd35ea7`) — mesmo valor, formatação diferente; normalizar removendo hífens dos dois lados antes de comparar, senão dá falso positivo.
7b. **Nome do csv de origem.** Formato esperado `<nome>_<protocolo>_v<N>_<hash12>.csv` (ex: `mapa_di_v1_dnp_358997bc7207.csv`, `Eletronuclear_Sitram-Multisense-5_mdb_v1_4e73bc8cc723.csv`). Conferir que o nome tem protocolo, versão e hash de commit, que o protocolo do nome (`mdb`/`dnp`) bate com a pasta sendo validada (`MDB`/`DNP`) e que a versão do nome bate com a pasta de versão (`v1`, `v2`...).
7c. **Limpeza do csv de origem.** O csv já deveria vir limpo. Reportar se tiver:
    - linha com `UUID` vazio (inclui linha totalmente em branco, ex: `;;;;;;...`);
    - linha sem `Classificação`;
    - linha com `Nível de acesso` = `Privado`.
    Se algum UUID com acesso `Privado` ou sem classificação aparecer no `fl.sql`/`fl.json`/SYNC, é erro no mapeamento (não devia ter sido mapeado).
7d. **Classificado sem Tipo/Registrador.** Linha com `Classificação` preenchida (Alarme, Medida, etc.) mas `Tipo (Modbus)`/`Registrador (Modbus)` vazio (ou `Tipo (DNP3)`/`Índice (DNP3)` no DNP): reportar e orientar a Manu a falar com o SAM Team no canal `#docs-mapa`. Linha sem classificação e sem tipo/registrador cai só no 7c.
7e. **Registrador dividido em partes (`16_M`, `16_U` e similares).** Filtrar a coluna `Tratamento` por esses valores. Os mnemônicos dessas linhas têm que vir numerados em sequência e sem repetir o nome base (ex: `...numeroserie1` para `16_M`, `...numeroserie2` para `16_U`). Um equipamento pode ter mais de um grupo assim — conferir todos. Se estiver faltando numeração, reportar (cruza com o item 3).
8. **Gráfico Rápido → tipo 1537.** Se a coluna "Gráfico Rápido" do csv/Excel estiver "Sim" na frente de um campo, o tipo desse campo no SQL/JSON tem que ser `1537`.
9. **E3Lib com especificidades conhecidas.** Se o `E3Lib` for um destes, avisar a Manu que existem especificidades para esse caso (ainda não detalhadas na skill) antes de seguir a validação padrão: `DM1`, `SEL2414`, `TM_V2`, `DM2`, `SPS`, `TMV e SDV`, `AVR`, `TM1 e TM2`, `BM`. Indicar a página da wiki "Especificidades de IEDs" como referência.
10. **Encoding.** Varrer descrições/textos (SQL, JSON, csv/Excel) procurando caracteres estranhos/corrompidos no meio de uma descrição, começando pelo `?` isolado, mas também qualquer outro símbolo ou sequência fora do lugar. Exemplo real já encontrado: `Concentração de H?` / `Gas sensor H?`, onde o `?` substituiu o "2" de "H2"/"H₂" — não é só acentuação perdida, também pode ser número/subscrito perdido. **Atenção ao falso positivo**: csv de origem em **Windows-1252/ISO-8859-1** é normal — ler assumindo UTF-8 faz acentos aparecerem trocados mesmo com o arquivo correto; ler respeitando a codificação real antes de julgar. Reportar qualquer ocorrência suspeita que sobrar depois disso, mesmo sem certeza absoluta.
10b. **Codificação do arquivo csv.** O processo de mapeamento pede o csv em UTF-8. Se o csv de origem estiver em outra codificação (ex: Windows-1252), reportar como ponto de atenção (`- [ ]` com a codificação encontrada), não como corrupção de dados — os textos continuam sendo lidos com a codificação real para as demais checagens (item 10).

## Bloco B — Comparação com versão anterior / outro protocolo (só se existir v1, v2, ... ou outro protocolo na mesma pasta)

Só executar este bloco depois do Bloco A estar fechado (csv ↔ script ↔ JSON já conferidos nesta versão). Se não existir versão anterior, rodar só o 12b (se houver outro protocolo) e pular para o Bloco C e, no lugar deste bloco, confirmar manualmente se subtipo/categoria estão corretos (não há referência para comparar).

11. **IDs entre versões.** Extrair os mesmos IDs de cada versão e comparar entre todas — todos os IDs equivalentes devem ser idênticos entre versões.
12. **Mnemônico estável entre versões.** O mnemônico de cada UID já existente na versão anterior deve permanecer o mesmo na versão nova (não pode trocar). Se achar mudança, só reportar — não corrigir sozinho.
12b. **Mnemônico estável entre protocolos.** Se a pasta da versão tiver `MDB` e `DNP` (ou outro protocolo já mapeado), o mnemônico de cada UUID presente nos dois tem que ser igual. Esse item roda mesmo quando não existe versão anterior e mesmo validando um protocolo só: o outro protocolo é lido apenas como referência, sem validar o resto dele.
13. **Subtipo e categoria.** Têm que ser iguais em todas as versões existentes.

## Bloco C — SYNC

Validar por último, depois que script/JSON/csv (e a comparação de versão, se houve) já estiverem fechados.

14. **Localizar o SYNC e espelhar contra o SQL.** Arquivos `sigma-sync-import` ficam na pasta própria `SYNC` — confirmar que existe apenas 1 arquivo de SYNC por versão (independente do protocolo ser MDB ou DNP). Cruzar esse JSON com o SQL, aplicando a mesma regra de espelhamento do item 2.
15. **identifier.** `identifier` é um campo exclusivo do JSON de SYNC (no JSON de mapeamento o campo equivalente já se chama `E3Lib`) — o valor tem que ser idêntico ao `E3Lib` do script/JSON de mapeamento.
16. **Hash do mapa (SYNC ↔ csv/zip).** `hashCommitMap` é exclusivo do JSON de SYNC (não existe no JSON de mapeamento — não confundir os dois). **O hash NÃO está no nome do próprio arquivo SYNC** (`sigma-sync-import.json` normalmente não tem hash no nome). Ele tem que bater com o hash presente no nome do **csv/Excel de origem** e/ou do **zip** — ex: csv `Fabricante_Nome-Do-Modulo_mdb_v1_da9dfe577f87.csv` e zip `TreetechGit-mapa_clientes-da9dfe577f87.zip` → `hashCommitMap: da9dfe577f87` (trecho depois do último `_`/`-` no nome desses arquivos).
17. **Versão do mapa (SYNC ↔ JSON de mapeamento).** `resourceVersionValue` e `productVersion` do JSON de SYNC são derivados do campo `VersaoMapa` do JSON de mapeamento (ex: `"VersaoMapa": "v2-MDB"`):
    - `resourceVersionValue` é só o número da versão, formato `N.0` (`v2-MDB` → `"2.0"`).
    - `productVersion` é o mesmo número, com o protocolo trocado por `sync` (`v2-MDB` → `"v2.0-sync"`).

## Bloco D — Relatório

18. **Gerar o relatório final** (ver "Formato do Relatório Final" no `SKILL.md`). Se já existia uma doc de validação anterior, atualizar essa mesma doc em vez de criar uma nova (ver "Segunda Validação" no `SKILL.md`).
