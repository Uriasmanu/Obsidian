# Passo a Passo de Validação — Detalhamento

Detalhamento completo de cada item do "Quick Reference" do `SKILL.md`. A ordem importa: primeiro fecha a consistência interna desta versão (csv ↔ script ↔ JSON), só depois compara com versão anterior (se houver), só depois valida o SYNC, e por último o relatório.

## Bloco A — csv ↔ script ↔ JSON desta versão

1. **Ler os arquivos.** JSON de mapeamento e script SQL (`fl.sql`, `GruposPadrao.sql`, `VersaoRecurso.sql`) do protocolo escolhido, mais o .csv/Excel de origem.
2. **Espelhamento JSON ↔ SQL.** Todo campo e todo ID do SQL devem aparecer, idênticos, no JSON de mapeamento (e vice-versa) — não é só "parecido", tem que bater 1:1. Extrair todo `DECLARE @XxxId ... = 'valor'` do script (`@ModuloId`, `@CampoIdN`, `@AlarmeIdN`, etc.) e conferir se o mesmo ID aparece no JSON.
3. **Mnemônicos únicos dentro do arquivo.** Nenhum mnemônico pode se repetir dentro do mesmo arquivo. **Se encontrar duplicidade, não resolver sozinho** (ex: não inventar um sufixo tipo "2" para desempatar) — só reportar para a Manu avaliar.
4. **Descrições únicas dentro do arquivo.** Mesma regra do item 3, aplicada às descrições em vez dos mnemônicos: nenhuma repetida dentro do arquivo, e não resolver duplicidade sozinho, só reportar.
5. **E3Lib.** O valor do `E3Lib` do script tem que ser idêntico ao `E3Lib` do JSON de mapeamento.
6. **IDs no GruposPadrao/VersaoRecurso.** Todos os IDs existentes no `fl.sql` (ModuloId + CampoIds + AlarmeIds) têm que constar também em `GruposPadrao.sql` e em `VersaoRecurso.sql`.
6b. **Conteúdo de `TagsVersaoMapa`/`TagsVersaoFirmware` no `VersaoRecurso.sql`.**
    - `TagsVersaoMapa` segue o formato `v<major>-<PROTOCOLO>` (`MDB` ou `DNP`), **sem minor** — ex: TAGs de engenharia `eng_mdb_13.0`, `eng_mdb_13.2`, `eng_mdb_13.3` viram só `v13-MDB`. Mais de uma versão fica separada por `;` (ex: `v2-MDB;v2-DNP;v17-MDB;v17-DNP`).
    - `TagsVersaoFirmware` segue o formato `v<major>[fw<descritivo>]`, **sem protocolo** e sem espaço extra entre os caracteres (ex: `v2[fw2.08R2-2.10R1]`).
    - **O script `VersaoRecurso.sql` de uma pasta de versão só pode conter tags dessa mesma versão** — ex: o script da pasta `V2` só define tags `v2-*`, o da `V17` só `v17-*`, mesmo que o recurso exista nas duas versões (a concatenação acontece ao rodar os dois scripts em sequência, não escrevendo as duas tags no mesmo script). Reportar como erro se aparecer tag de outra versão major dentro do script de uma versão.
    - Para o recurso `ModuloAtivo` (código 4): tem que haver **exatamente uma** definição de `TagsVersaoMapa` (formato `v<major>-<PROTOCOLO>`) e `TagsVersaoFirmware` **tem que estar em branco**.
7. **Identificar e cruzar o csv/Excel de origem.** É o arquivo que traz o hash de commit no nome ou o arquivo com o mesmo nome do csv dentro da pasta zipada — **não é o `modulo.csv` genérico, nem um arquivo com nome igual ao `E3Lib`** (ex: `BM.csv`). Esse tipo costuma ser export de tags OPC/Archestra (colunas como `ObjectType;Name;AdviseType;...AllowRead;AllowWrite`), sem UUID, sem "Mnemônico" e sem "Gráfico Rápido" — para confirmar que achou o arquivo certo, checar se ele tem colunas `UUID` e `Mnemônico`. Depois de identificado, cruzar com SQL e JSON — os três têm que bater entre si. **Atenção ao formato do UUID**: no csv costuma vir sem hífen (`1ca40722324346a1b92e56270fd35ea7`), SQL/JSON com hífen (`1ca40722-3243-46a1-b92e-56270fd35ea7`) — mesmo valor, formatação diferente; normalizar removendo hífens dos dois lados antes de comparar, senão dá falso positivo.
8. **Gráfico Rápido → tipo 1537.** Se a coluna "Gráfico Rápido" do csv/Excel estiver "Sim" na frente de um campo, o tipo desse campo no SQL/JSON tem que ser `1537`.
9. **E3Lib com especificidades conhecidas.** Se o `E3Lib` for um destes, avisar a Manu que existem especificidades para esse caso (ainda não detalhadas na skill) antes de seguir a validação padrão: `DM1`, `SEL2414`, `TM_V2`, `DM2`, `SPS`, `TMV e SDV`, `AVR`, `TM1 e TM2`, `BM`.
10. **Encoding.** Varrer descrições/textos (SQL, JSON, csv/Excel) procurando caracteres estranhos/corrompidos no meio de uma descrição, começando pelo `?` isolado, mas também qualquer outro símbolo ou sequência fora do lugar. Exemplo real já encontrado: `Concentração de H?` / `Gas sensor H?`, onde o `?` substituiu o "2" de "H2"/"H₂" — não é só acentuação perdida, também pode ser número/subscrito perdido. **Atenção ao falso positivo**: csv de origem em **Windows-1252/ISO-8859-1** é normal — ler assumindo UTF-8 faz acentos aparecerem trocados mesmo com o arquivo correto; ler respeitando a codificação real antes de julgar. Reportar qualquer ocorrência suspeita que sobrar depois disso, mesmo sem certeza absoluta.

## Bloco B — Comparação com versão anterior (só se existir v1, v2, ... na mesma pasta)

Só executar este bloco depois do Bloco A estar fechado (csv ↔ script ↔ JSON já conferidos nesta versão). Se não existir versão anterior, pular para o Bloco C e, no lugar deste bloco, confirmar manualmente se subtipo/categoria estão corretos (não há referência para comparar).

11. **IDs entre versões.** Extrair os mesmos IDs de cada versão e comparar entre todas — todos os IDs equivalentes devem ser idênticos entre versões.
12. **Mnemônico estável entre versões.** O mnemônico de cada UID já existente na versão anterior deve permanecer o mesmo na versão nova (não pode trocar). Se achar mudança, só reportar — não corrigir sozinho.
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
