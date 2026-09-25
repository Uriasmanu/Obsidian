"""Checagens mecânicas da skill valida-mapeamento (só lê, nunca altera arquivos).

Uso: python valida.py <pasta_protocolo> [--anterior <pasta_protocolo>] [--outro-protocolo <pasta_protocolo>]
"""
import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

GUID = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
METADADOS = {"versaoproduto", "versaomapa", "hashcommitmapa", "datahoraultimaleiturasensor"}
E3LIB_ESPECIFICAS = {"DM1", "SEL2414", "TM_V2", "DM2", "SPS", "TMV", "SDV", "AVR", "TM1", "TM2", "BM"}
ABREVIACOES = {
    "indicacaode": "indde", "parametrode": "paramde", "temperatura": "temp", "tendencia": "tend",
    "referencia": "ref", "alarme": "alm", "autodiagnostico": "autodiag", "corrente": "corr",
    "tensao": "tens", "frequencia": "freq", "configuracao": "config", "habilitacao": "hab",
    "desabilitacao": "desab", "limite": "lim", "status": "stat", "comunicacao": "com", "valor": "val",
    "maxima": "max", "minima": "min", "media": "med", "sensor": "sens", "conjunto": "conj",
    "indicacao": "ind", "parametro": "param",
}
TIPO_RECURSO = {"Modulo": 1, "Campo": 2, "Alarme": 3}
GUID_ZERO = "00000000-0000-0000-0000-000000000000"
LIMITE_LISTA = 15
ORDEM_STATUS = ["ERRO", "ATENCAO", "SUGESTAO", "INFO", "OK"]


def norm_uuid(u):
    return re.sub(r"[^0-9a-f]", "", (u or "").lower())


def norm_col(nome):
    sem_acento = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", sem_acento.strip().lower())


def ler_texto(caminho):
    bruto = caminho.read_bytes()
    try:
        return bruto.decode("utf-8-sig"), "UTF-8"
    except UnicodeDecodeError:
        return bruto.decode("cp1252", errors="replace"), "Windows-1252"


def mesmo_valor(a, b):
    a, b = str(a).strip(), str(b).strip()
    if re.fullmatch(GUID, a) and re.fullmatch(GUID, b):
        return a.lower() == b.lower()
    return a == b


class Relatorio:
    def __init__(self):
        self.itens = defaultdict(list)

    def add(self, status, item, arquivo, msg, trechos=()):
        self.itens[arquivo].append((status, item, msg, list(trechos)))

    def imprimir(self):
        saida = io.StringIO()
        for arquivo, itens in self.itens.items():
            saida.write(f"\n## {arquivo}\n")
            for status, item, msg, trechos in sorted(itens, key=lambda i: ORDEM_STATUS.index(i[0])):
                saida.write(f"[{status}] {item} — {msg}\n")
                for t in trechos[:LIMITE_LISTA]:
                    saida.write(f"    > {t}\n")
                if len(trechos) > LIMITE_LISTA:
                    saida.write(f"    > ... +{len(trechos) - LIMITE_LISTA}\n")
        resumo = Counter(s for itens in self.itens.values() for s, *_ in itens)
        saida.write("\nResumo: " + ", ".join(f"{s}={resumo[s]}" for s in ORDEM_STATUS if resumo[s]) + "\n")
        sys.stdout.buffer.write(saida.getvalue().encode("utf-8"))


def split_valores_sql(s):
    valores, atual, i, em_aspas = [], "", 0, False
    while i < len(s):
        c = s[i]
        if em_aspas:
            if c == "'" and s[i + 1:i + 2] == "'":
                atual += "'"
                i += 1
            elif c == "'":
                em_aspas = False
            else:
                atual += c
        elif c == "'":
            em_aspas = True
        elif c == ",":
            valores.append(atual.strip())
            atual = ""
        else:
            atual += c
        i += 1
    valores.append(atual.strip())
    return valores


def linha_de(texto, pos):
    ini = texto.rfind("\n", 0, pos) + 1
    fim = texto.find("\n", pos)
    return texto[ini:fim if fim != -1 else None].strip()


def parse_fl_sql(texto):
    declaracoes = list(re.finditer(rf"DECLARE @(\w+) UNIQUEIDENTIFIER = '({GUID})'", texto))
    variaveis = {m.group(1): m.group(2).lower() for m in declaracoes}
    registros = []
    for i, m in enumerate(declaracoes):
        fim = declaracoes[i + 1].start() if i + 1 < len(declaracoes) else len(texto)
        bloco = texto[m.start():fim]
        ins = re.search(r"INSERT INTO (\w+) \(([^)]*)\)\s*VALUES\s*\((.*)\)[ \t]*\r?\n", bloco)
        if not ins:
            continue
        colunas = [c.strip() for c in ins.group(2).split(",")]
        valores = [variaveis.get(v[1:], v) if v.startswith("@") else v for v in split_valores_sql(ins.group(3))]
        inicio_anterior = declaracoes[i - 1].start() if i else 0
        cabecalhos = re.findall(r"--// \*+ (?:CAMPO|ALARME): (\S+) \*+ //", texto[inicio_anterior:m.start()])
        descricoes = {}
        dic = re.search(r"INSERT INTO dicionario\.\w+ \(Chave, Idioma, Valor\)\s*VALUES (.*)", bloco)
        if dic:
            for idioma, valor in re.findall(r"\(@\w+,\s*(\d+),\s*'((?:[^']|'')*)'\)", dic.group(1)):
                descricoes[int(idioma)] = valor.replace("''", "'")
        campos = dict(zip(colunas, valores))
        registros.append({
            "var": m.group(1), "id": m.group(2).lower(), "tabela": ins.group(1), "campos": campos,
            "nome": campos.get("Nome") if ins.group(1) != "Alarme" else (cabecalhos[-1] if cabecalhos else ""),
            "descricoes": descricoes, "linha": linha_de(texto, m.start()),
        })
    return registros


def parse_versao_recurso(texto):
    blocos = [(m.start(), m.group(1).lower(), int(m.group(2))) for m in re.finditer(
        rf"SET @RecursoId = '({GUID})';\s*SET @RecursoTipo = (\d+);", texto)]
    tags = []
    for m in re.finditer(r"(?:DECLARE|SET) @TagVersao(Mapa|Firmware)(?: VARCHAR\(\d+\))? = '([^']*)'", texto):
        dono = next((b for b in reversed(blocos) if b[0] < m.start()), None)
        tags.append({"tipo": m.group(1), "valor": m.group(2), "linha": linha_de(texto, m.start()),
                     "recurso_tipo": dono[2] if dono else None})
    return blocos, tags


def achar(pasta, padrao):
    return sorted(p for p in pasta.glob(padrao) if p.is_file())


def numero_versao(pasta_protocolo):
    m = re.fullmatch(r"[vV](\d+)", pasta_protocolo.parent.name)
    return int(m.group(1)) if m else None


class Mapa:
    """Arquivos de um protocolo de uma versão (ex: v1/MDB) já lidos e parseados."""

    def __init__(self, pasta):
        self.pasta = pasta
        self.protocolo = pasta.name.upper()
        self.versao = numero_versao(pasta)
        self.sql_path = next(iter(achar(pasta, "*-fl.sql")), None)
        self.json_path = next(iter(achar(pasta, "*-fl.json")), None)
        self.gp_path = next(iter(achar(pasta, "*-GruposPadrao.sql")), None)
        self.vr_path = next(iter(achar(pasta, "*-VersaoRecurso.sql")), None)
        self.csvs_hash = [p for p in achar(pasta, "*.csv") if re.search(r"_[0-9a-fA-F]{12}\.csv$", p.name)]
        self.registros = parse_fl_sql(ler_texto(self.sql_path)[0]) if self.sql_path else []
        self.json = json.loads(ler_texto(self.json_path)[0]) if self.json_path else None
        self.csv_path = self.csvs_hash[0] if len(self.csvs_hash) == 1 else None
        self.csv_linhas, self.csv_cols, self.csv_encoding = self._ler_csv()

    def _ler_csv(self):
        if not self.csv_path:
            return [], {}, None
        texto, encoding = ler_texto(self.csv_path)
        leitor = csv.reader(io.StringIO(texto), delimiter=";")
        cabecalho = next(leitor, [])
        cols = {norm_col(c): i for i, c in enumerate(cabecalho)}
        linhas = []
        for n, valores in enumerate(leitor, start=2):
            linha = {norm_col(c): (valores[i].strip() if i < len(valores) else "") for c, i in cols.items()}
            linha["_n"], linha["_raw"], linha["_cabecalho"] = n, valores, cabecalho
            linhas.append(linha)
        return linhas, cols, encoding

    def por_tabela(self, tabela):
        return [r for r in self.registros if r["tabela"] == tabela]

    def modulo(self):
        return next(iter(self.por_tabela("Modulo")), None)

    def mapeados(self):
        return [r for r in self.registros if r["tabela"] in ("Campo", "Alarme")]

    def com_origem_no_csv(self):
        """Campos/alarmes vindos do csv: exclui metadados (E7) e alarmes do framework (ex: @AlarmeRedeDigitalId)."""
        return [r for r in self.mapeados() if re.fullmatch(r"(Campo|Alarme)Id\d+", r["var"])
                and r["nome"].lower().split("_")[-1] not in METADADOS]

    def mnemonicos_por_uuid(self):
        return {norm_uuid(r["id"]): r["nome"] for r in self.mapeados()}


def tabela_csv(linha, colunas):
    cab = linha["_cabecalho"]
    idx = [i for i, c in enumerate(cab) if norm_col(c) in colunas]
    return " | ".join(f"{cab[i]}={linha['_raw'][i] if i < len(linha['_raw']) else ''}" for i in idx) + f" (linha {linha['_n']})"


def sem_prefixo(nome, mnemonico_csv=None):
    if mnemonico_csv and nome.endswith(mnemonico_csv):
        return mnemonico_csv
    return re.sub(r"^[a-z]+_", "", nome)


def estilo(mnemonico):
    if re.fullmatch(r"[a-z0-9]+", mnemonico):
        return "minusculo"
    if re.fullmatch(r"[a-z][a-zA-Z0-9]*", mnemonico):
        return "camelCase"
    return "invalido"


def classificar_csv(linha):
    if not linha.get("uuid"):
        return "sem_uuid"
    if not linha.get("classificacao"):
        return "sem_classificacao"
    if linha.get("nivel de acesso", "").lower() == "privado":
        return "privado"
    texto = " ".join([linha.get("classificacao", ""), linha.get("tratamento", "")]).lower()
    if "comando" in texto or linha.get("mnemonico", "").lower().startswith("cmd"):
        return "comando"
    return "mapeavel"


def suspeitas_encoding(texto):
    return bool(re.search(r"(?<=\w)\?|\?(?=\w)|\?$|�|[ÃÂ][\u0080-¿]", texto))


def checar_bloco_a(m, rel, anterior, outro):
    sql, js = m.sql_path.name if m.sql_path else "fl.sql", m.json_path.name if m.json_path else "fl.json"
    if not m.sql_path or not m.json_path:
        rel.add("ERRO", "1", str(m.pasta), "fl.sql ou fl.json não encontrado na pasta")
        return
    mod, jmod = m.modulo(), m.json

    diffs = []
    if mod:
        if not mesmo_valor(mod["id"], jmod.get("Id")):
            diffs.append(f"ModuloId: SQL `{mod['id']}` x JSON `{jmod.get('Id')}`")
        for col, val in mod["campos"].items():
            if col != "Id" and col in jmod and not mesmo_valor(val, jmod[col]):
                diffs.append(f"Modulo.{col}: SQL `{val}` x JSON `{jmod[col]}`")
    for tabela, chave in (("Campo", "Campos"), ("Alarme", "Alarmes")):
        sql_ids = {r["id"]: r for r in m.por_tabela(tabela)}
        json_ids = {str(c["Id"]).lower(): c for c in jmod.get(chave, [])}
        for i in sorted(set(sql_ids) - set(json_ids)):
            diffs.append(f"{tabela} `{i}` ({sql_ids[i]['nome']}) está no SQL e falta no JSON")
        for i in sorted(set(json_ids) - set(sql_ids)):
            diffs.append(f"{tabela} `{i}` ({json_ids[i].get('Nome')}) está no JSON e falta no SQL")
        for i in sorted(set(sql_ids) & set(json_ids)):
            r, c = sql_ids[i], json_ids[i]
            for col, val in r["campos"].items():
                if col not in ("Id",) and col in c and not mesmo_valor(val, c[col]):
                    diffs.append(f"{tabela} `{r['nome']}` {col}: SQL `{val}` x JSON `{c[col]}`")
            jdesc = {d["Idioma"]: d["Valor"] for d in c.get("Dicionario", [])}
            for idioma, valor in r["descricoes"].items():
                if jdesc.get(idioma) != valor:
                    diffs.append(f"{tabela} `{r['nome']}` descrição idioma {idioma}: SQL `{valor}` x JSON `{jdesc.get(idioma)}`")
    zerados = [f"{r['tabela']} `{r['nome'] or r['var']}`: {r['linha']}" for r in m.registros if r["id"] == GUID_ZERO]
    if zerados:
        rel.add("ERRO", "2", sql, "ID zerado (GUID 0000...) no fl.sql", zerados)
    total = len(m.mapeados()) + 1
    if diffs:
        rel.add("ERRO", "2", js, f"espelhamento SQL x JSON com {len(diffs)} divergência(s)", diffs)
    else:
        rel.add("OK", "2", js, f"espelhamento SQL x JSON: {total} IDs (módulo + campos + alarmes) e seus campos batem 1:1")

    csv_mnem = {norm_uuid(l["uuid"]): l.get("mnemonico", "") for l in m.csv_linhas if l.get("uuid")}
    fontes = {
        sql: [sem_prefixo(r["nome"], csv_mnem.get(norm_uuid(r["id"]))) for r in m.mapeados()],
        js: [sem_prefixo(c.get("Nome", "")) for c in jmod.get("Campos", [])],
    }
    if m.csv_path:
        fontes[m.csv_path.name] = [l["mnemonico"] for l in m.csv_linhas if l.get("mnemonico")]
    for arquivo, nomes in fontes.items():
        nomes = [n for n in nomes if n.lower() not in METADADOS]
        dup = [f"`{n}` aparece {q}x" for n, q in Counter(nomes).items() if q > 1]
        if dup:
            rel.add("ERRO", "3", arquivo, "mnemônico repetido", dup)
        else:
            rel.add("OK", "3", arquivo, f"{len(nomes)} mnemônicos, nenhum repetido")

    herdados = {}
    for ref in (anterior, outro):
        if ref:
            herdados.update(ref.mnemonicos_por_uuid())
    if m.csv_path:
        mapeaveis = [l for l in m.csv_linhas if l.get("mnemonico")]
        longos_erro, longos_atencao = [], []
        for l in mapeaveis:
            if len(l["mnemonico"]) > 50:
                herdado = herdados.get(norm_uuid(l["uuid"]), "").endswith(l["mnemonico"])
                (longos_atencao if herdado else longos_erro).append(f"`{l['mnemonico']}` ({len(l['mnemonico'])} caracteres)")
        if longos_erro:
            rel.add("ERRO", "3b", m.csv_path.name, "mnemônico com mais de 50 caracteres", longos_erro)
        if longos_atencao:
            rel.add("ATENCAO", "3b", m.csv_path.name, "mnemônico herdado com mais de 50 caracteres (E3)", longos_atencao)
        if not longos_erro and not longos_atencao:
            rel.add("OK", "3b", m.csv_path.name, "todos os mnemônicos com até 50 caracteres")

        estilos = defaultdict(list)
        for l in mapeaveis:
            estilos[estilo(l["mnemonico"])].append(l["mnemonico"])
        if estilos["invalido"]:
            rel.add("ERRO", "3c", m.csv_path.name, "mnemônico com caractere fora de [a-zA-Z0-9] (acento, `_`, espaço...)",
                    [f"`{n}`" for n in estilos["invalido"]])
        if estilos["minusculo"] and estilos["camelCase"]:
            minoria = min(("minusculo", "camelCase"), key=lambda e: len(estilos[e]))
            rel.add("ERRO", "3c", m.csv_path.name, f"arquivo mistura minúsculo e camelCase; os em {minoria}:",
                    [f"`{n}`" for n in estilos[minoria]])
        elif estilos["camelCase"]:
            rel.add("ATENCAO", "3c", m.csv_path.name, "arquivo todo em camelCase: só é aceito em mapa antigo (padrão atual é tudo minúsculo)")
        elif not estilos["invalido"]:
            rel.add("OK", "3c", m.csv_path.name, "todos os mnemônicos no padrão atual (tudo minúsculo, ^[a-z0-9]+$)")

        sugestoes = []
        for l in mapeaveis:
            if norm_uuid(l["uuid"]) in herdados:
                continue
            for palavra, abrev in ABREVIACOES.items():
                if palavra in l["mnemonico"].lower():
                    sugestoes.append(f"`{l['mnemonico']}`: `{palavra}` → `{abrev}`")
        if sugestoes:
            rel.add("SUGESTAO", "3d", m.csv_path.name, "palavra inteira onde existe abreviação padrão", sugestoes)

    for arquivo, grupos in (
        (sql, {t: [(r["descricoes"], r["nome"]) for r in m.por_tabela(t)] for t in ("Campo", "Alarme")}),
        (js, {k: [({d["Idioma"]: d["Valor"] for d in c.get("Dicionario", [])}, c.get("Nome")) for c in jmod.get(k, [])]
              for k in ("Campos", "Alarmes")}),
    ):
        dup = []
        for grupo, itens in grupos.items():
            for idioma in (1, 2, 3):
                contagem = Counter(d.get(idioma) for d, _ in itens if d.get(idioma))
                dup += [f"{grupo} idioma {idioma}: `{v}` aparece {q}x" for v, q in contagem.items() if q > 1]
        rel.add("ERRO" if dup else "OK", "4", arquivo, "descrição repetida" if dup else "nenhuma descrição repetida (por idioma)", dup)
    if m.csv_path:
        dup = []
        for col in ("descricao pt", "descricao en", "descricao es"):
            contagem = Counter(l[col] for l in m.csv_linhas if l.get(col) and classificar_csv(l) == "mapeavel")
            dup += [f"{col}: `{v}` aparece {q}x" for v, q in contagem.items() if q > 1]
        rel.add("ERRO" if dup else "OK", "4", m.csv_path.name, "descrição repetida" if dup else "nenhuma descrição repetida", dup)

    e3_sql = mod["campos"].get("E3Lib") if mod else None
    e3_json = jmod.get("E3Lib")
    if e3_sql == e3_json:
        rel.add("OK", "5", sql, f"E3Lib = '{e3_sql}' igual no fl.json", [mod["linha"]] if mod else [])
    else:
        rel.add("ERRO", "5", sql, f"E3Lib diferente: SQL `{e3_sql}` x JSON `{e3_json}`")
    img_sql, img_json = (mod["campos"].get("Imagem") if mod else None), jmod.get("Imagem")
    if img_sql != img_json:
        rel.add("ERRO", "5b", sql, f"Imagem diferente: SQL `{img_sql}` x JSON `{img_json}`")
    elif img_sql != f"{e3_sql}.svg":
        rel.add("ERRO", "5b", sql, f"Imagem `{img_sql}` não segue `<E3Lib>.svg` (esperado `{e3_sql}.svg`) — confirmar com o usuário se é imagem compartilhada")
    else:
        rel.add("OK", "5b", sql, f"Imagem = '{img_sql}' = <E3Lib>.svg, igual no JSON")
    if e3_sql and e3_sql.upper() in E3LIB_ESPECIFICAS:
        rel.add("ATENCAO", "9", sql, f"E3Lib `{e3_sql}` tem especificidades conhecidas (TM1 e TM2 andam juntos) — ver wiki 'Especificidades de IEDs'")

    checar_grupos_versao(m, rel)
    checar_csv(m, rel)


def checar_grupos_versao(m, rel):
    ids_fl = {r["id"]: r for r in m.registros if r["tabela"] in TIPO_RECURSO}
    if m.gp_path:
        texto_gp = ler_texto(m.gp_path)[0]
        ids_gp = {g.lower() for g in re.findall(GUID, texto_gp)}
        ids_campos = {i: r for i, r in ids_fl.items() if r["tabela"] != "Alarme"}
        falta = [f"{r['tabela']} `{i}` ({r['nome'] or r['var']})" for i, r in ids_campos.items() if i not in ids_gp]
        rel.add("ERRO" if falta else "OK", "6", m.gp_path.name,
                "ID do fl.sql faltando no GruposPadrao" if falta else
                f"módulo + {len(ids_campos) - 1} campos do fl.sql presentes (alarmes não entram no GruposPadrao)", falta)
        versao_modulo = re.search(r"DECLARE @VersaoModulo NVARCHAR\(\d+\) = N?'([^']*)'", texto_gp)
        if versao_modulo and m.json and versao_modulo.group(1) != m.json.get("VersaoMapa"):
            rel.add("ERRO", "6b", m.gp_path.name, f"@VersaoModulo `{versao_modulo.group(1)}` diferente de VersaoMapa `{m.json.get('VersaoMapa')}` do fl.json",
                    [linha_de(texto_gp, versao_modulo.start())])
    if not m.vr_path:
        return
    blocos, tags = parse_versao_recurso(ler_texto(m.vr_path)[0])
    ids_vr = {b[1]: b[2] for b in blocos}
    problemas = [f"{r['tabela']} `{i}` ({r['nome'] or r['var']}) faltando" for i, r in ids_fl.items() if i not in ids_vr]
    problemas += [f"{r['tabela']} `{i}` com @RecursoTipo = {ids_vr[i]}, esperado {TIPO_RECURSO[r['tabela']]}"
                  for i, r in ids_fl.items() if i in ids_vr and ids_vr[i] != TIPO_RECURSO[r["tabela"]]]
    problemas += [f"@RecursoId `{i}` (tipo {t}) não existe no fl.sql" for i, t in ids_vr.items() if i not in ids_fl and t in (1, 2, 3)]
    rel.add("ERRO" if problemas else "OK", "6", m.vr_path.name,
            "divergência de IDs com o fl.sql" if problemas else f"todos os {len(ids_fl)} IDs do fl.sql presentes com o RecursoTipo certo", problemas)

    for t in tags:
        if t["recurso_tipo"] == 4:
            continue
        valor, versao = t["valor"], m.versao
        if t["tipo"] == "Mapa":
            partes = valor.split(";")
            ruins = [p for p in partes if not re.fullmatch(r"v\d+-(MDB|DNP)", p)]
            outras = [p for p in partes if re.fullmatch(r"v\d+-(MDB|DNP)", p) and versao and int(p[1:p.index("-")]) != versao]
            if ruins:
                rel.add("ERRO", "6b", m.vr_path.name, f"TagsVersaoMapa fora do formato v<major>-<PROTOCOLO>: {ruins}", [t["linha"]])
            elif outras:
                rel.add("ERRO", "6b", m.vr_path.name, f"TagsVersaoMapa com tag de outra versão ({outras}) no script da v{versao}", [t["linha"]])
            else:
                rel.add("OK", "6b", m.vr_path.name, f"TagsVersaoMapa `{valor}` no formato certo", [t["linha"]])
            if m.json and valor != m.json.get("VersaoMapa"):
                rel.add("ERRO", "6b", m.vr_path.name, f"TagsVersaoMapa `{valor}` diferente de VersaoMapa `{m.json.get('VersaoMapa')}` do fl.json", [t["linha"]])
        else:
            partes = valor.split(";")
            ruins = [p for p in partes if not re.fullmatch(r"v\d+\[fw[^\[\]\s]+\]", p)]
            outras = [p for p in partes if p not in ruins and versao and int(re.match(r"v(\d+)", p).group(1)) != versao]
            if ruins:
                aninhado = any(p.count("[") > 1 for p in ruins)
                rel.add("ERRO", "6b", m.vr_path.name, f"TagsVersaoFirmware fora do formato v<major>[fw<descritivo>]: {ruins}"
                        + (" — template aninhado" if aninhado else ""), [t["linha"]])
            elif outras:
                rel.add("ERRO", "6b", m.vr_path.name, f"TagsVersaoFirmware com tag de outra versão ({outras})", [t["linha"]])
            else:
                rel.add("OK", "6b", m.vr_path.name, f"TagsVersaoFirmware `{valor}` no formato certo", [t["linha"]])
            if m.json and valor != m.json.get("VersaoFirmware"):
                rel.add("ERRO", "6b", m.vr_path.name, f"TagsVersaoFirmware `{valor}` diferente de VersaoFirmware `{m.json.get('VersaoFirmware')}` do fl.json", [t["linha"]])

    ativo = [t for t in tags if t["recurso_tipo"] == 4]
    if any(b[2] == 4 for b in blocos):
        mapa = [t for t in ativo if t["tipo"] == "Mapa"]
        fw = [t for t in ativo if t["tipo"] == "Firmware" and t["valor"]]
        ok = len(mapa) == 1 and re.fullmatch(r"v\d+-(MDB|DNP)", mapa[0]["valor"]) and not fw
        rel.add("OK" if ok else "ERRO", "6b", m.vr_path.name,
                "ModuloAtivo com uma TagsVersaoMapa e TagsVersaoFirmware em branco" if ok else
                "ModuloAtivo (4) precisa de exatamente uma TagsVersaoMapa v<major>-<PROTOCOLO> e TagsVersaoFirmware em branco",
                [t["linha"] for t in ativo])


def checar_csv(m, rel):
    if len(m.csvs_hash) != 1:
        rel.add("ERRO", "7", str(m.pasta), f"{len(m.csvs_hash)} csv com hash de 12 caracteres no nome — perguntar ao usuário qual é o de origem",
                [p.name for p in m.csvs_hash])
        return
    nome = m.csv_path.name
    if "uuid" not in m.csv_cols or "mnemonico" not in m.csv_cols:
        rel.add("ERRO", "7", nome, "csv sem colunas UUID e Mnemônico — não parece o csv de origem")
        return

    formato = re.fullmatch(r"(.+)_(mdb|dnp)_v(\d+)_([0-9a-f]{12})\.csv", nome, re.I)
    invertido = re.fullmatch(r"(.+)_v(\d+)_(mdb|dnp)_([0-9a-f]{12})\.csv", nome, re.I)
    if invertido:
        rel.add("ERRO", "7b", nome, "nome com versão antes do protocolo; esperado `<nome>_<protocolo>_v<N>_<hash12>.csv`")
    elif not formato:
        rel.add("ERRO", "7b", nome, "nome fora do formato `<nome>_<protocolo>_v<N>_<hash12>.csv`")
    else:
        problemas = []
        if formato.group(2).upper() != m.protocolo:
            problemas.append(f"protocolo do nome `{formato.group(2)}` x pasta `{m.protocolo}`")
        if m.versao and int(formato.group(3)) != m.versao:
            problemas.append(f"versão do nome `v{formato.group(3)}` x pasta `v{m.versao}`")
        rel.add("ERRO" if problemas else "OK", "7b", nome,
                "nome não bate com a pasta" if problemas else "nome com protocolo, versão e hash, batendo com a pasta", problemas)

    classes = defaultdict(list)
    for l in m.csv_linhas:
        classes[classificar_csv(l)].append(l)
    ids_sql = {norm_uuid(r["id"]): r for r in m.mapeados()}
    cols_tabela = {"uuid", "tratamento", "nivel de acesso", "mnemonico", "classificacao"}
    for classe, msg in (("sem_uuid", "linha sem UUID (inclui linha em branco)"),
                        ("sem_classificacao", "linha sem Classificação"), ("privado", "linha com Nível de acesso = Privado")):
        if classes[classe]:
            rel.add("ERRO", "7c", nome, msg, [tabela_csv(l, cols_tabela) for l in classes[classe]])
        mapeadas = [l for l in classes[classe] if l.get("uuid") and norm_uuid(l["uuid"]) in ids_sql]
        if mapeadas:
            rel.add("ERRO", "7c", nome, f"{msg} e mesmo assim mapeada no fl.sql", [tabela_csv(l, cols_tabela) for l in mapeadas])
    uuid_ruim = [tabela_csv(l, cols_tabela) for l in m.csv_linhas
                 if l.get("uuid") and not re.fullmatch(r"[0-9a-f]{32}|" + GUID, l["uuid"], re.I)]
    if uuid_ruim:
        rel.add("ERRO", "7c", nome, "UUID mal formado (não tem 32 caracteres hexadecimais)", uuid_ruim)
    if not any(classes[c] for c in ("sem_uuid", "sem_classificacao", "privado")):
        rel.add("OK", "7c", nome, "csv limpo: nenhuma linha sem UUID, sem classificação ou Privado")
    if classes["comando"]:
        rel.add("INFO", "7", nome, f"{len(classes['comando'])} linha(s) de comando fora do mapeamento (E5)",
                [f"`{l['mnemonico']}`" for l in classes["comando"]])

    if m.protocolo == "DNP":
        tipo_col, reg_col = "tipo (dnp3)", "indice (dnp3)"
    else:
        tipo_col, reg_col = "tipo (modbus)", "registrador (modbus)"
    sem_registro = [l for l in m.csv_linhas if l.get("classificacao") and l.get("uuid") and (not l.get(tipo_col) or not l.get(reg_col))]
    rel.add("ERRO" if sem_registro else "OK", "7d", nome,
            f"classificado sem {tipo_col}/{reg_col} — falar com o SAM Team no #docs-mapa" if sem_registro else
            f"toda linha classificada tem {tipo_col} e {reg_col}", [tabela_csv(l, cols_tabela | {tipo_col, reg_col}) for l in sem_registro])

    divididos = [l for l in m.csv_linhas if re.fullmatch(r"\d+_[A-Z]", l.get("tratamento", ""))]
    if divididos:
        ruins = [l for l in divididos if not re.search(r"\d$", l["mnemonico"])]
        rel.add("ERRO" if ruins else "OK", "7e", nome,
                "registrador dividido (16_M/16_U...) com mnemônico sem numeração" if ruins else
                f"{len(divididos)} linha(s) de registrador dividido com mnemônico numerado",
                [tabela_csv(l, cols_tabela) for l in (ruins or divididos)])

    mapeaveis = {norm_uuid(l["uuid"]): l for l in classes["mapeavel"]}
    faltando_sql = [tabela_csv(l, cols_tabela) for u, l in mapeaveis.items() if u not in ids_sql]
    uuids_csv = {norm_uuid(l.get("uuid")) for l in m.csv_linhas}
    sem_origem = [f"{r['tabela']} `{r['nome']}` `{r['id']}`" for r in m.com_origem_no_csv() if norm_uuid(r["id"]) not in uuids_csv]
    rel.add("ERRO" if faltando_sql else "OK", "7", nome, "linha do csv que devia estar mapeada e falta no fl.sql" if faltando_sql
            else f"as {len(mapeaveis)} linhas mapeáveis do csv estão no fl.sql", faltando_sql)
    if sem_origem:
        rel.add("ERRO", "7", m.sql_path.name, "campo/alarme do fl.sql sem UUID correspondente no csv", sem_origem)
    nome_errado = [f"UUID `{r['id']}`: SQL `{r['nome']}` x csv `{mapeaveis[u]['mnemonico']}`" for u, r in ids_sql.items()
                   if u in mapeaveis and not r["nome"].endswith(mapeaveis[u]["mnemonico"])]
    rel.add("ERRO" if nome_errado else "OK", "7", m.sql_path.name,
            "mnemônico do SQL diferente do csv (ignorando o prefixo do software, ex: get_)" if nome_errado else
            "mnemônicos do SQL batem com o csv (ignorando o prefixo do software)", nome_errado)

    rapidos = [l for l in classes["mapeavel"] if l.get("grafico rapido", "").lower() == "sim"]
    ruins = [f"`{ids_sql[norm_uuid(l['uuid'])]['nome']}` TipoCampo = {ids_sql[norm_uuid(l['uuid'])]['campos'].get('TipoCampo')}"
             for l in rapidos if norm_uuid(l["uuid"]) in ids_sql and ids_sql[norm_uuid(l["uuid"])]["campos"].get("TipoCampo") != "1537"]
    if rapidos:
        rel.add("ERRO" if ruins else "OK", "8", m.sql_path.name,
                "Gráfico rápido = Sim sem tipo 1537" if ruins else f"os {len(rapidos)} campos com Gráfico rápido = Sim têm tipo 1537", ruins)

    for arquivo, textos in (
        (m.sql_path.name, [d for r in m.registros for d in r["descricoes"].values()]),
        (m.json_path.name, [d["Valor"] for k in ("Campos", "Alarmes") for c in m.json.get(k, []) for d in c.get("Dicionario", [])]),
        (nome, [l[c] for l in m.csv_linhas for c in ("descricao pt", "descricao en", "descricao es") if l.get(c)]),
    ):
        suspeitos = sorted({t for t in textos if suspeitas_encoding(t)})
        rel.add("ERRO" if suspeitos else "OK", "10", arquivo,
                "caractere suspeito na descrição (? no lugar de letra/número, � ou acento corrompido)" if suspeitos else
                "nenhum caractere suspeito nas descrições", [f"`{s}`" for s in suspeitos])
    if m.csv_encoding != "UTF-8":
        rel.add("ATENCAO", "10b", nome, f"csv em {m.csv_encoding} (o processo pede UTF-8) — lido na codificação real (E2)")
    else:
        rel.add("OK", "10b", nome, "csv em UTF-8")


def checar_bloco_b(m, rel, anterior, outro):
    arquivo = m.sql_path.name
    if anterior:
        mod_a, mod = anterior.modulo(), m.modulo()
        if mod_a and mod:
            rel.add("OK" if mod_a["id"] == mod["id"] else "ERRO", "11", arquivo,
                    f"ModuloId `{mod['id']}` x anterior `{mod_a['id']}`", [mod["linha"]])
            for col in ("Subtipo", "Categoria"):
                a, b = mod_a["campos"].get(col), mod["campos"].get(col)
                rel.add("OK" if a == b else "ERRO", "13", arquivo, f"{col}: atual `{b}` x anterior `{a}`")
        nomes_ant = {r["nome"]: r["id"] for r in anterior.mapeados()}
        ids_trocados = [f"`{r['nome']}`: atual `{r['id']}` x anterior `{nomes_ant[r['nome']]}`"
                        for r in m.mapeados() if r["nome"] in nomes_ant and nomes_ant[r["nome"]] != r["id"]]
        rel.add("ERRO" if ids_trocados else "OK", "11", arquivo,
                "mesmo mnemônico com ID diferente da versão anterior" if ids_trocados else "IDs iguais aos da versão anterior", ids_trocados)
        status, msg, lista = comparar_mnemonicos(m, anterior, "versão anterior")
        rel.add(status, "12", arquivo, msg, lista)
    if outro:
        status, msg, lista = comparar_mnemonicos(m, outro, f"protocolo {outro.protocolo}")
        rel.add(status, "12b", arquivo, msg, lista)


def comparar_mnemonicos(m, ref, rotulo):
    atuais, antigos = m.mnemonicos_por_uuid(), ref.mnemonicos_por_uuid()
    comuns = set(atuais) & set(antigos)
    trocados = [f"UUID `{u}`: atual `{atuais[u]}` x {rotulo} `{antigos[u]}`" for u in sorted(comuns) if atuais[u] != antigos[u]]
    if trocados:
        return "ERRO", f"mnemônico diferente para o mesmo UUID ({rotulo})", trocados
    return "OK", f"{len(comuns)} UUIDs em comum ({rotulo}), todos com o mesmo mnemônico", []


def checar_bloco_c(m, rel):
    pasta_versao = m.pasta.parent
    syncs = sorted(pasta_versao.rglob("*sigma-sync-import*.json"))
    if len(syncs) != 1:
        rel.add("ERRO", "14", str(pasta_versao), f"{len(syncs)} arquivo(s) sigma-sync-import na versão (esperado 1)", [str(s) for s in syncs])
        if not syncs:
            return
    sync_path = syncs[0]
    nome = sync_path.name
    if sync_path.parent.name.upper() != "SYNC":
        rel.add("ERRO", "14", nome, f"SYNC fora da pasta SYNC: `{sync_path.parent.name}`")
    sync = json.loads(ler_texto(sync_path)[0])
    modulos = sync.get("modules", [])
    mod, jmod = m.modulo(), m.json or {}
    smod = modulos[0] if modulos else {}

    ids_sql = {r["id"]: r for r in m.com_origem_no_csv()}
    ids_framework = {r["id"]: r for r in m.mapeados() if r["id"] not in ids_sql}
    campos_sync = {str(f.get("id")).lower(): f for f in sync.get("fields", [])}
    ausentes = [f"{r['tabela']} `{r['nome'] or r['var']}` `{i}`" for i, r in ids_framework.items() if i not in campos_sync]
    if ausentes:
        rel.add("ATENCAO", "14", nome, "metadado/alarme do framework ausente em fields do SYNC (deveria estar — E7)", ausentes)
    diffs = [f"`{i}` ({f.get('name')}) está no SYNC e falta no fl.sql" for i, f in campos_sync.items()
             if i not in ids_sql and i not in ids_framework]
    diffs += [f"{r['tabela']} `{r['nome']}` `{i}` está no fl.sql e falta no SYNC" for i, r in ids_sql.items() if i not in campos_sync]
    for i in set(ids_sql) & set(campos_sync):
        r, f = ids_sql[i], campos_sync[i]
        if f.get("name") != r["nome"]:
            diffs.append(f"`{i}` name: SYNC `{f.get('name')}` x SQL `{r['nome']}`")
        if r["tabela"] == "Campo" and str(f.get("typeField")) != r["campos"].get("TipoCampo"):
            diffs.append(f"`{r['nome']}` typeField: SYNC `{f.get('typeField')}` x SQL TipoCampo `{r['campos'].get('TipoCampo')}`")
        if mod and str(f.get("moduleId")).lower() != mod["id"]:
            diffs.append(f"`{r['nome']}` moduleId `{f.get('moduleId')}` diferente do ModuloId")
    if mod and str(smod.get("id")).lower() != mod["id"]:
        diffs.append(f"modules.id `{smod.get('id')}` x ModuloId `{mod['id']}`")
    rel.add("ERRO" if diffs else "OK", "14", nome,
            f"espelhamento SYNC x fl.sql com {len(diffs)} divergência(s)" if diffs else f"{len(campos_sync)} fields batem com o fl.sql", diffs)

    e3 = mod["campos"].get("E3Lib") if mod else jmod.get("E3Lib")
    rel.add("OK" if smod.get("identifier") == e3 else "ERRO", "15", nome, f"`\"identifier\": \"{smod.get('identifier')}\"` x E3Lib `{e3}`")

    versoes = smod.get("versions", [{}])
    hash_csv = re.search(r"_([0-9a-fA-F]{12})\.csv$", m.csv_path.name).group(1) if m.csv_path else None
    for v in versoes:
        h = v.get("hashCommitMap")
        rel.add("OK" if h and h == hash_csv else "ERRO", "16", nome, f"`\"hashCommitMap\": \"{h}\"` x hash do csv `{hash_csv}`")
        vm = re.fullmatch(r"v(\d+)-(MDB|DNP)", jmod.get("VersaoMapa", "") or "")
        if vm:
            esperado_rv, esperado_pv = f"{vm.group(1)}.0", f"v{vm.group(1)}.0-sync"
            for campo, esperado in (("resourceVersionValue", esperado_rv), ("productVersion", esperado_pv)):
                rel.add("OK" if v.get(campo) == esperado else "ERRO", "17", nome,
                        f"`\"{campo}\": \"{v.get(campo)}\"` x esperado `{esperado}` (VersaoMapa `{jmod.get('VersaoMapa')}`)")
            sem_versao = [f"`{f.get('name')}` versions {f.get('versions')}" for f in campos_sync.values() if esperado_rv not in (f.get("versions") or [])]
            if sem_versao:
                rel.add("ERRO", "17", nome, f"field sem a versão `{esperado_rv}` em versions", sem_versao)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta", type=Path, help="pasta do protocolo validado (ex: .../v2/MDB)")
    ap.add_argument("--anterior", type=Path, help="pasta do mesmo protocolo na versão anterior (Bloco B)")
    ap.add_argument("--outro-protocolo", type=Path, help="pasta do outro protocolo da mesma versão (item 12b)")
    args = ap.parse_args()
    m = Mapa(args.pasta.resolve())
    anterior = Mapa(args.anterior.resolve()) if args.anterior else None
    outro = Mapa(args.outro_protocolo.resolve()) if args.outro_protocolo else None
    rel = Relatorio()
    print_cab = f"# valida.py — {m.pasta} (v{m.versao} / {m.protocolo})"
    sys.stdout.buffer.write((print_cab + "\n").encode("utf-8"))
    checar_bloco_a(m, rel, anterior, outro)
    checar_bloco_b(m, rel, anterior, outro)
    checar_bloco_c(m, rel)
    rel.imprimir()


if __name__ == "__main__":
    main()
