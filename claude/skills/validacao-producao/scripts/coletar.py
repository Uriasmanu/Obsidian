"""Coletor de evidencias para a skill validacao-producao.

Le a pasta de producao uma unica vez e imprime um relatorio compacto com tudo
que precisa ser conferido.

======================================================================
SOMENTE LEITURA. Este programa NUNCA escreve, cria, apaga ou renomeia.
Toda a E/S passa por Coletor.ler(), que abre em modo 'r'. Se voce for
editar este arquivo: nao introduza escrita de nenhum tipo. A saida vai
para stdout -- quem quiser guardar, redireciona.
======================================================================

Uso:
    python coletar.py <pasta-da-producao> [--json]

Marcadores na saida:
    OK   conferido, sem problema
    !!   divergencia -- vira item no relatorio
    ??   indefinido -- a skill precisa perguntar ao usuario
    --   informativo, nao e achado
"""
import collections
import glob
import io
import json
import os
import re
import sys

# A versao do modulo aparece como vN-MDB nos .sql e como "N.0" nos .json.
VERSAO_SQL = re.compile(r"v(\d+)-MDB")
VERSAO_JSON = re.compile(r"^(\d+)\.0$")

# Secoes de engenharia do hierarchy_export e o trecho que identifica o script.
ENG = {
    "EficienciaResfriamento": "eng_eficiencia_do_resfriamento",
    "EnvelhecimentoIsolacao": "eng_envelhecimento_isolacao",
    "GradienteFinal": "eng_gradiente_final",
    "SimulacaoCarga": "eng_simulacao_de_carga",
    "ManutencaoResfriamento": "eng_manutencao_do_resfriamento",
    "ChromaFisico": "eng_chroma_fisico",
    "TemperaturaAmbiente": "temperatura_ambiente",
    # Sem exemplo de producao com estas preenchidas -- nome do script desconhecido.
    "AguaPapel": None,
    "ManutencaoComutador": None,
    "DiferencialTemperaturaComutador": None,
}

# Modulos sem script "mae": so existem os por ativo.
SEM_SCRIPT_MAE = {"ChromaFisico", "TemperaturaAmbiente"}

# Lista fechada (por E3Lib) dos modulos com regra de fieldGroups. A variante nao tem
# sigma proprio: ela e um grupo dentro do sigma da familia, que carrega o moduleId e o
# identifier de um dos membros. Modulo fora da lista tem FieldGroupId null.
COM_FIELDGROUP = {"TM1", "TM2", "AVR", "AVRGROUP", "SDV", "TMV"}


class Coletor:
    def __init__(self, raiz):
        self.raiz = os.path.abspath(raiz)
        self.r = {"raiz": self.raiz, "achados": [], "notas": [], "perguntar": []}

    # ---------- utilitarios ----------

    def ler(self, caminho):
        """Unico ponto de E/S do programa. Abre sempre em 'r' -- nunca escreve.

        Nunca propaga erro: um arquivo ilegivel vira achado, nao derruba a validacao.
        No Windows, caminho acima de 260 caracteres falha aqui -- o prefixo \\\\?\\ contorna.
        """
        for tentativa in (caminho, "\\\\?\\" + os.path.abspath(caminho)):
            try:
                with io.open(tentativa, mode="r", encoding="utf-8-sig", errors="replace") as f:
                    return f.read().replace("\r\n", "\n")
            except (OSError, ValueError):
                continue
        self.achado("ARQ", f"arquivo nao pode ser lido: {os.path.basename(caminho)}", caminho)
        self.r.setdefault("ilegiveis", []).append(caminho)
        return ""

    def achar(self, padrao):
        return sorted(glob.glob(os.path.join(self.raiz, padrao)))

    def pasta_json(self):
        """03 - JSONS, 03-JSON, 03_JSONS... grafia varia entre producoes."""
        for d in self.achar("DB/*"):
            if os.path.isdir(d) and re.match(r"^03[ \-_]*JSONS?$", os.path.basename(d), re.I):
                return d
        return None

    def achado(self, cat, msg, onde=""):
        self.r["achados"].append({"cat": cat, "msg": msg, "onde": onde})

    # ---------- blocos ----------

    def estrutura(self):
        out = {}
        for nome, caminho in [("client", "client"), ("DB", "DB"),
                              ("00-INITIAL-SCRIPTS", "DB/00-INITIAL-SCRIPTS"),
                              ("01-BACKBONE", "DB/01-BACKBONE"),
                              ("02-GROUPS", "DB/02-GROUPS")]:
            existe = os.path.isdir(os.path.join(self.raiz, caminho))
            out[nome] = existe
            if not existe:
                self.achado("PASTA", f"pasta obrigatoria ausente: {caminho}", caminho)

        pj = self.pasta_json()
        out["pasta_json"] = os.path.basename(pj) if pj else None
        if not pj:
            self.achado("PASTA", "pasta de JSONs ausente (03-JSON / 03 - JSONS)", "DB/")
        elif os.path.basename(pj) != "03 - JSONS":
            self.r["notas"].append(f"pasta de JSONs grafada '{os.path.basename(pj)}' -- variacao aceita")

        # Toleradas e nao obrigatorias nao geram achado em nenhuma hipotese.
        out["escopo"] = os.path.isdir(os.path.join(self.raiz, "escopo"))
        out["system"] = os.path.isdir(os.path.join(self.raiz, "system"))
        out["E3"] = os.path.isdir(os.path.join(self.raiz, "E3"))

        esperadas = {"DB", "client", "escopo", "system", "E3"}
        out["extras"] = [d for d in os.listdir(self.raiz)
                         if os.path.isdir(os.path.join(self.raiz, d)) and d not in esperadas]
        for d in out["extras"]:
            self.achado("PASTA", f"pasta fora do padrao: {d}/", d)

        for rotulo, padrao in [("create-database-client", "client/*create-database-client.sql"),
                               ("perfil-root", "DB/01-BACKBONE/*perfil-root.sql")]:
            achados = self.achar(padrao)
            out[rotulo] = os.path.basename(achados[0]) if achados else None
            if not achados:
                self.achado("ARQ", f"arquivo obrigatorio ausente: {padrao}", padrao)

        out["rev"] = [os.path.basename(d) for d in self.achar("DB/01-BACKBONE/Rev*")]
        self.r["estrutura"] = out

    def empresa(self):
        out = {"pasta": os.path.basename(self.raiz)}
        c = self.achar("client/*create-database-client.sql")
        if c:
            m = re.search(r"CREATE DATABASE \[([^\]]+)\]", self.ler(c[0]))
            out["banco"] = m.group(1) if m else None
        bk = self.achar("DB/01-BACKBONE/001*.sql")
        if bk:
            m = re.match(r"^\d+_(.+)\.sql$", os.path.basename(bk[0]))
            out["prefixo_backbone"] = m.group(1) if m else None
        h = self.hierarchy
        if h:
            out["empresa"] = h["Empresas"][0]["Nome"] if h.get("Empresas") else None
            out["instalacao"] = h["Instalacoes"][0]["Nome"] if h.get("Instalacoes") else None
        self.r["empresa"] = out

    def sequencias(self):
        """Numero = ordem de execucao. Lacuna = script que nao foi copiado."""
        out = {}
        alvos = ["client", "DB/00-INITIAL-SCRIPTS", "DB/01-BACKBONE", "DB/02-GROUPS"]
        pj = self.pasta_json()
        if pj:
            alvos.append(os.path.relpath(pj, self.raiz).replace("\\", "/"))
        for rel in alvos:
            d = os.path.join(self.raiz, rel)
            if not os.path.isdir(d):
                continue
            nums = sorted({int(m.group(1)) for f in os.listdir(d)
                           if (m := re.match(r"^(\d+)", f))})
            corpo = [n for n in nums if n != 999]
            if not corpo:
                continue
            lac = [n for n in range(min(corpo), max(corpo) + 1) if n not in corpo]
            out[rel] = {"de": min(corpo), "ate": max(corpo),
                        "tem_999": 999 in nums, "lacunas": lac}
            if lac:
                self.achado("ARQ", f"lacuna na sequencia de {rel}: faltam {lac}", rel)
        self.r["sequencias"] = out

    def modulos(self):
        """GUID e a chave primaria. Nome de arquivo e so pista."""
        mod = collections.defaultdict(dict)

        for f in self.achar("DB/00-INITIAL-SCRIPTS/*-fl.sql"):
            t = self.ler(f)
            g = re.search(r"@ModuloId\s+UNIQUEIDENTIFIER\s*=\s*'([0-9a-fA-F-]+)'", t)
            e = re.search(r"E3Lib\s*=\s*'([^']*)'", t)
            if g:
                k = g.group(1).lower()
                mod[k]["fl"] = os.path.basename(f)
                mod[k]["E3Lib"] = e.group(1) if e else None

        for f in self.achar("DB/00-INITIAL-SCRIPTS/*-VersaoRecurso.sql"):
            t = self.ler(f)
            g = re.search(r"SET @RecursoId\s*=\s*'([0-9a-fA-F-]+)'", t)
            # Dois formatos: variavel declarada ou versao inline no LIKE.
            v = (re.search(r"@TagVersaoMapa\s+VARCHAR\(\d+\)\s*=\s*'v(\d+)-MDB'", t)
                 or re.search(r"TagsVersaoMapa\s+LIKE\s*'%v(\d+)-MDB%'", t))
            fw = (re.search(r"@TagVersaoFirmware\s+VARCHAR\(\d+\)\s*=\s*'v(\d+)\[", t)
                  or re.search(r"TagsVersaoFirmware\s+LIKE\s*'%v(\d+)\[", t))
            if g:
                k = g.group(1).lower()
                mod[k]["VersaoRecurso"] = os.path.basename(f)
                mod[k]["v_VersaoRecurso"] = v.group(1) if v else None
                mod[k]["firmware"] = fw.group(1) if fw else None

        for f in self.achar("DB/02-GROUPS/*.sql"):
            t = self.ler(f)
            g = re.search(r"@ModuloId\s+UNIQUEIDENTIFIER\s*=\s*'([0-9a-fA-F-]+)'", t)
            v = re.search(r"@VersaoModulo\s+NVARCHAR\(\d+\)\s*=\s*N'v(\d+)-MDB'", t)
            if g:
                k = g.group(1).lower()
                mod[k]["GruposPadrao"] = os.path.basename(f)
                mod[k]["v_GruposPadrao"] = v.group(1) if v else None

        pj = self.pasta_json()
        self.fieldgroups, self.sigma_idents = {}, set()
        if pj:
            for f in sorted(glob.glob(os.path.join(pj, "*sigma-sync-import.json"))):
                nome = os.path.basename(f)
                try:
                    d = json.loads(self.ler(f))
                except json.JSONDecodeError as e:
                    self.achado("ARQ", f"sigma invalido: {e}", nome)
                    continue
                m0 = (d.get("modules") or [{}])[0]
                # O modules[].id e a fonte: fields[].moduleId tambem existe e confunde.
                k = str(m0.get("id") or "").lower()
                # versions ora e ["1.0"], ora [{"resourceVersionValue": "1.0", ...}].
                v = (m0.get("versions") or [None])[0]
                v = v.get("resourceVersionValue") if isinstance(v, dict) else v
                mv = re.match(r"^(\d+)\.0$", str(v or ""))
                # O fieldGroups do topo traz objetos; o de fields[] traz so strings.
                grupos = [str(x.get("id", "")).lower() for x in (d.get("fieldGroups") or [])]
                for x in grupos:
                    self.fieldgroups[x] = nome
                # E o modules[].identifier que o sync usa em ModuleIdentifier -- nao o E3Lib.
                if m0.get("identifier"):
                    self.sigma_idents.add(m0["identifier"])
                if k:
                    # Familia (TM1/TM2, AVR/AVRGROUP) divide um moduleId: acumular, nao sobrescrever.
                    mod[k].setdefault("sigma", []).append(nome)
                    mod[k]["v_sigma"] = mv.group(1) if mv else None
                    mod[k]["sigma_identifier"] = m0.get("identifier")
                    mod[k].setdefault("fieldGroups", []).extend(grupos)

        for b in self.blocos:
            k = b["ModuloId"].lower()
            mod[k]["no_001"] = True
            m = VERSAO_SQL.search(b.get("VersaoModuloAtivo", "") or "")
            mod[k]["v_001"] = m.group(1) if m else None

        fontes = ("fl", "VersaoRecurso", "GruposPadrao", "sigma", "no_001")
        for g, m in mod.items():
            com_fg = m.get("E3Lib") in COM_FIELDGROUP
            faltam = [f for f in fontes
                      if not m.get(f) and not (f == "sigma" and com_fg)]
            if faltam:
                self.achado("ARQ", f"modulo {m.get('E3Lib') or g[:8]} ({g}) ausente em: "
                                   f"{', '.join(faltam)}", "DB/")
            if com_fg and not m.get("sigma"):
                self.r["notas"].append(
                    f"modulo {m.get('E3Lib')}: sem sigma proprio -- tem regra de fieldGroups, "
                    f"a variante vive no sigma da familia. Conferido pelo FieldGroupId no sync.")
            vs = {m.get(f"v_{x}") for x in ("001", "VersaoRecurso", "GruposPadrao", "sigma")}
            vs.discard(None)
            if len(vs) > 1:
                self.achado("ARQ", f"versao divergente no modulo {m.get('E3Lib') or g[:8]}: "
                                   f"{sorted(vs)}", "DB/")
            if m.get("firmware") and m.get("v_VersaoRecurso") and m["firmware"] != m["v_VersaoRecurso"]:
                self.achado("ARQ", f"prefixo do firmware (v{m['firmware']}) difere da versao do "
                                   f"modulo (v{m['v_VersaoRecurso']}) em {m.get('E3Lib')}", "DB/")
            # Alias do arquivo != E3Lib e nota, nao achado: o GUID e que manda.
            if m.get("fl") and m.get("E3Lib"):
                alias = re.sub(r"^\d+\s*[-_]\s*|-fl\.sql$", "", m["fl"])
                if alias != m["E3Lib"]:
                    self.r["notas"].append(
                        f"modulo {alias}: alias do arquivo difere do E3Lib ({m['E3Lib']}); "
                        f"conferido pelo GUID {g[:8]}... -- consistente")
        self.r["modulos"] = dict(sorted(mod.items()))

    def backbone(self):
        """Varredura sequencial do 001 -- regex que atravessa blocos emparelha errado."""
        self.blocos, self.ativos_001 = [], set()
        bk = self.achar("DB/01-BACKBONE/001*.sql")
        if len(bk) != 1:
            self.achado("ARQ", f"esperado exatamente 1 arquivo 001*, encontrados {len(bk)}",
                        "DB/01-BACKBONE/")
            return
        t = self.ler(bk[0])
        campos = ("ModuloAtivoId|ModuloId|VersaoModuloAtivo|AtivoId|"
                  "ModuloAtivoFuncionalidades|HasOscillography|SetGroup")
        cur, ativo = None, None
        for k, v in re.findall(rf"SET @({campos})\s*=\s*N?'?([^'\s;]+)'?", t):
            if k == "AtivoId":
                ativo = v.lower()
                self.ativos_001.add(ativo)
            elif k == "ModuloAtivoId":
                if cur:
                    self.blocos.append(cur)
                cur = {"ma": v.lower(), "ativo": ativo}
            elif cur is not None:
                cur[k] = v
        if cur:
            self.blocos.append(cur)
        self.blocos = [b for b in self.blocos if "ModuloId" in b]
        self.r["backbone"] = {"blocos_moduloativo": len(self.blocos),
                              "ativos_distintos": len(self.ativos_001)}

    def ativos(self):
        h = self.hierarchy
        if not h:
            return
        hier = {a["Id"].lower() for a in h.get("Ativos", [])}
        out = {"no_001": len(self.ativos_001), "no_hierarchy": len(hier)}
        so1, so2 = sorted(self.ativos_001 - hier), sorted(hier - self.ativos_001)
        if so1:
            self.achado("ARQ", f"ativos no 001 e ausentes no hierarchy_export: {so1}", "DB/")
        if so2:
            self.achado("ARQ", f"ativos no hierarchy_export e ausentes no 001: {so2}", "DB/")
        out["identicos"] = not so1 and not so2

        orfaos = []
        for f in self.achar("DB/01-BACKBONE/*.sql"):
            if re.match(r"^001_|^999_", os.path.basename(f)):
                continue
            m = re.search(r"INSERT INTO #Ativos\w*\s*\(AtivoId\)\s*VALUES(.*?);",
                          self.ler(f), re.S)
            if not m:
                continue
            for g in re.findall(r"'([0-9a-fA-F-]{36})'", m.group(1)):
                if g.lower() not in hier:
                    orfaos.append((os.path.basename(f), g))
        for arq, g in orfaos:
            self.achado("ARQ", f"AtivoId inexistente na hierarquia: {g}", f"DB/01-BACKBONE/{arq}")
        out["orfaos_em_config"] = len(orfaos)
        self.r["ativos"] = out

    def engenharia(self):
        h = self.hierarchy
        if not h:
            return
        scripts = [os.path.basename(f) for f in self.achar("DB/01-BACKBONE/*.sql")]
        out = {}
        for chave, valor in h.items():
            if not (chave.startswith("Configuracoes") and chave.endswith("Configurador")):
                continue
            nome = chave[len("Configuracoes"):-len("Configurador")]
            preenchida = bool(valor)
            trecho = ENG.get(nome, "?")
            if trecho is None:
                out[nome] = {"preenchida": preenchida, "script": "desconhecido"}
                if preenchida:
                    self.r["perguntar"].append(
                        f"secao {chave} esta preenchida ({len(valor)} registros) mas o nome do "
                        f"script correspondente nao e conhecido -- perguntar ao usuario")
                continue
            tem = any(trecho in s for s in scripts)
            out[nome] = {"preenchida": preenchida, "script": tem}
            if preenchida and not tem:
                self.achado("ARQ", f"secao {chave} preenchida mas sem script de engenharia "
                                   f"(*{trecho}*)", "DB/01-BACKBONE/")
            if not preenchida and tem:
                self.achado("ARQ", f"script *{trecho}* presente mas a secao {chave} esta vazia",
                            "DB/01-BACKBONE/")
            if preenchida and nome not in SEM_SCRIPT_MAE:
                mae = [s for s in scripts if trecho in s and "_config" not in s]
                if not mae:
                    self.achado("ARQ", f"modulo de engenharia {nome} sem script mae "
                                       f"(so os _config por ativo)", "DB/01-BACKBONE/")
        self.r["engenharia"] = out

    def comunicacao(self, tipo_sync):
        pj = self.pasta_json()
        if not pj:
            return
        s_files = sorted(glob.glob(os.path.join(pj, "*_sync.json")))
        h_files = sorted(glob.glob(os.path.join(pj, "*hierarchy_export.json")))
        if not h_files:
            self.achado("ARQ", "*_hierarchy_export.json ausente", os.path.basename(pj))

        if not tipo_sync:
            e3 = os.path.join(self.raiz, "E3")
            out = {"modo": "E3", "pasta_E3": os.path.isdir(e3)}
            if not out["pasta_E3"]:
                self.achado("PASTA", "comunicacao E3 mas pasta E3/ ausente", "E3/")
            else:
                for ext in ("prj", "dll"):
                    achou = glob.glob(os.path.join(e3, f"*.{ext}"))
                    out[ext] = len(achou)
                    if not achou:
                        self.achado("ARQ", f"nenhum arquivo .{ext} em E3/", "E3/")
            self.r["comunicacao"] = out
            return

        if not s_files:
            self.achado("ARQ", "comunicacao Sync mas *_sync.json ausente", os.path.basename(pj))
            return
        prj = glob.glob(os.path.join(self.raiz, "E3", "*.prj"))
        dll = glob.glob(os.path.join(self.raiz, "E3", "*.dll"))
        if prj or dll:
            self.achado("PASTA", "comunicacao Sync mas ha .prj/.dll em E3/", "E3/")

        s = json.loads(self.ler(s_files[0]))
        h = self.hierarchy or {}
        emp = h["Empresas"][0]["Nome"] if h.get("Empresas") else ""
        inst = h["Instalacoes"][0]["Nome"] if h.get("Instalacoes") else ""
        nome_ativo = {a["Identificador"]: a["Nome"] for a in h.get("Ativos", [])}
        e3lib = {g: m.get("E3Lib") for g, m in self.r["modulos"].items()}

        ieds = s["DataSources"][0]["Ieds"] if s.get("DataSources") else []
        arq = os.path.basename(s_files[0])
        out = {"arquivo": arq, "modo": "Sync", "n_ieds": len(ieds),
               "n_datasources": len(s.get("DataSources", []))}

        # 8.1 -- a conferencia mais importante: 001 <-> sync, 1:1 por ModuloAtivoId.
        # O par e (IED, associacao), nao o IED: modulo com fieldGroups tem varias
        # associacoes no mesmo IED, e cada uma e um ModuloAtivo.
        porma = {}
        for i, d in enumerate(ieds):
            for a in d.get("Associations", []):
                porma[a["AssetModuleId"].lower()] = (i, d, a)
        b = {x["ma"]: x for x in self.blocos}
        so001, sosync = sorted(set(b) - set(porma)), sorted(set(porma) - set(b))
        out["so_no_001"], out["so_no_sync"] = so001, sosync
        for g in so001:
            self.achado("ARQ", f"ModuloAtivoId {g} esta no 001 mas nao tem IED no sync "
                               f"-- modulo instalado que nao vai comunicar", arq)
        for g in sosync:
            self.achado("ARQ", f"AssetModuleId {g} esta no sync mas nao tem bloco no 001 "
                               f"-- IED apontando para modulo inexistente", arq)

        for g in set(b) & set(porma):
            i, d, assoc = porma[g]
            bl = b[g]
            # O ModuleIdentifier vem do modules[].identifier do sigma, nao do E3Lib: a
            # familia inteira usa um so (TM1 e TM2 viram 'TM', AVRGROUP vira 'AVR').
            esperado = e3lib.get(bl["ModuloId"].lower())
            if (esperado and esperado != d["ModuleIdentifier"]
                    and esperado not in COM_FIELDGROUP):
                self.achado("ARQ", f"IED {i:02d}: modulo {d['ModuleIdentifier']} no sync, "
                                   f"{esperado} no 001", arq)
            m = VERSAO_SQL.search(bl.get("VersaoModuloAtivo", "") or "")
            mv = VERSAO_JSON.match(str(d.get("ModuleVersion", "")))
            if m and mv and m.group(1) != mv.group(1):
                self.achado("ARQ", f"IED {i:02d}: versao {d['ModuleVersion']} no sync, "
                                   f"v{m.group(1)}-MDB no 001", arq)
            if bl.get("HasOscillography") == "0" and d.get("HasOscillography") is not False:
                self.achado("ARQ", f"IED {i:02d}: HasOscillography diverge do 001", arq)
            if (bl.get("SetGroup", "NULL").upper() == "NULL"
                    and assoc.get("TableSufix") is not None):
                self.achado("ARQ", f"IED {i:02d}: TableSufix diverge do @SetGroup do 001", arq)
        # 8.6 -- FieldGroupId. Quem manda e a lista COM_FIELDGROUP, pelo modulo do 001.
        # O grupo e procurado na uniao dos sigmas, nao no sigma do proprio modulo: a
        # variante (TM2, AVRGROUP) nao tem sigma proprio.
        for i, d in enumerate(ieds):
            vistos = set()
            for a in d.get("Associations", []):
                bl = b.get(a.get("AssetModuleId", "").lower())
                if not bl:
                    continue
                lib = e3lib.get(bl["ModuloId"].lower())
                fgid = a.get("FieldGroupId")
                k = (fgid or "").lower()
                if lib in COM_FIELDGROUP:
                    if not fgid:
                        self.achado("ARQ", f"IED {i:02d}: {lib} tem regra de fieldGroups mas a "
                                           f"associacao {a['AssetModuleId']} veio sem "
                                           f"FieldGroupId", arq)
                    elif k not in self.fieldgroups:
                        self.achado("ARQ", f"IED {i:02d}: FieldGroupId {fgid} ({lib}) nao existe "
                                           f"em nenhum sigma da pasta", arq)
                    elif k in vistos:
                        self.achado("ARQ", f"IED {i:02d}: FieldGroupId {fgid} repetido em mais "
                                           f"de uma associacao", arq)
                elif fgid is not None:
                    self.achado("ARQ", f"IED {i:02d}: {lib} nao tem regra de fieldGroups mas a "
                                       f"associacao veio com FieldGroupId {fgid}", arq)
                if k:
                    vistos.add(k)

        # 8.2 -- modulos e ativos do sync existem do outro lado.
        # O sync nomeia o modulo pelo modules[].identifier do sigma; o E3Lib entra como
        # alternativa porque nem todo modulo tem sigma proprio.
        libs = {v for v in e3lib.values() if v} | self.sigma_idents
        for mi in sorted({d["ModuleIdentifier"] for d in ieds}):
            if libs and mi not in libs:
                self.achado("ARQ", f"ModuleIdentifier '{mi}' nao corresponde a nenhum "
                                   f"modules[].identifier de sigma nem a nenhum E3Lib", arq)
        for aid in sorted({a["AssetIdentifier"] for d in ieds
                           for a in d.get("Associations", []) if a.get("AssetIdentifier")}):
            if nome_ativo and aid not in nome_ativo:
                self.achado("ARQ", f"AssetIdentifier '{aid}' nao existe no hierarchy_export", arq)

        # 8.4 -- Label reconstruido. (Formato do Identifier NAO e validado.)
        labels = []
        for i, d in enumerate(ieds):
            if not d.get("Associations"):
                continue
            aid = d["Associations"][0]["AssetIdentifier"]
            esp = f"{emp} - {inst} - {nome_ativo.get(aid, '?')} - {d['ModuleIdentifier']}"
            if esp != d.get("Label"):
                labels.append({"ied": i, "esperado": esp, "achado": d.get("Label")})
                self.achado("ARQ", f"IED {i:02d}: Label '{d.get('Label')}' "
                                   f"(esperado '{esp}')", arq)
        out["labels_divergentes"] = labels

        # 8.5 -- organizacao interna.
        if out["n_datasources"] != 1:
            self.achado("ARQ", f"{out['n_datasources']} DataSources (esperado 1)", arq)
        if inst and s.get("Name") != inst:
            self.achado("ARQ", f"Name '{s.get('Name')}' difere da instalacao '{inst}'", arq)
        ids = [d.get("Identifier") for d in ieds]
        if len(set(ids)) != len(ids):
            dup = [x for x, n in collections.Counter(ids).items() if n > 1]
            self.achado("ARQ", f"Identifier repetido entre IEDs: {dup}", arq)
        for i, d in enumerate(ieds):
            for a in d.get("Associations", []):
                if a.get("DatabaseConnectionId") is not None:
                    self.achado("ARQ", f"IED {i:02d}: DatabaseConnectionId nao e null", arq)

        ma = self.r["ativos"].get("no_hierarchy") if self.r.get("ativos") else None
        out["modulos_ativos_hierarchy"] = len(h.get("ModulosAtivos", []))
        self.r["notas"].append("formato do Identifier dos IEDs nao e validado -- fora de escopo")
        self.r["comunicacao"] = out

    def sdg_provisorio(self):
        """Provisorio: contorna bug do gerador. Remover quando corrigido na origem."""
        sdg = {g for g, m in self.r.get("modulos", {}).items() if m.get("E3Lib") == "SDG"}
        if not sdg:
            return
        vals = sorted({b.get("ModuloAtivoFuncionalidades")
                       for b in self.blocos if b["ModuloId"].lower() in sdg} - {None})
        self.r["sdg_funcionalidades"] = vals
        if vals and vals != ["1"]:
            self.achado("ARQ", f"[PROVISORIO] @ModuloAtivoFuncionalidades do SDG = {vals}, "
                               f"esperado 1 (gateway tem so Geral)", "DB/01-BACKBONE/001*.sql")

    # ---------- orquestracao ----------

    def rodar(self, tipo_sync=None):
        pj = self.pasta_json()
        self.hierarchy = None
        if pj:
            hf = sorted(glob.glob(os.path.join(pj, "*hierarchy_export.json")))
            if hf:
                try:
                    self.hierarchy = json.loads(self.ler(hf[0]))
                except json.JSONDecodeError as e:
                    self.achado("ARQ", f"hierarchy_export.json invalido: {e}", os.path.basename(pj))
        if tipo_sync is None:
            tipo_sync = bool(pj and glob.glob(os.path.join(pj, "*_sync.json")))
        self.estrutura()
        self.backbone()
        self.empresa()
        self.sequencias()
        self.modulos()
        self.ativos()
        self.engenharia()
        self.comunicacao(tipo_sync)
        self.sdg_provisorio()
        return self.r


def imprimir(r):
    def sec(t):
        print(f"\n{'=' * 4} {t} {'=' * (60 - len(t))}")

    e = r.get("estrutura", {})
    sec("ESTRUTURA")
    for k in ("client", "DB", "00-INITIAL-SCRIPTS", "01-BACKBONE", "02-GROUPS"):
        print(f"  {'OK' if e.get(k) else '!!'}  {k}")
    print(f"  {'OK' if e.get('pasta_json') else '!!'}  {e.get('pasta_json') or 'pasta de JSONs'}")
    print(f"  --  system/ {'presente' if e.get('system') else 'ausente'} (nao obrigatoria)")
    print(f"  --  escopo/ {'presente' if e.get('escopo') else 'ausente'} (tolerada)")
    if e.get("extras"):
        print(f"  !!  pastas fora do padrao: {e['extras']}")
    print(f"  {'OK' if e.get('create-database-client') else '!!'}  {e.get('create-database-client')}")
    print(f"  {'OK' if e.get('perfil-root') else '!!'}  {e.get('perfil-root')}")
    if e.get("rev"):
        print(f"  --  pastas Rev: {e['rev']}")

    c = r.get("empresa", {})
    sec("EMPRESA (4 fontes)")
    for k in ("pasta", "empresa", "instalacao", "banco", "prefixo_backbone"):
        print(f"  {k:18} {c.get(k)}")

    sec("SEQUENCIAS (numero = ordem de execucao)")
    for d, v in r.get("sequencias", {}).items():
        marca = "OK" if not v["lacunas"] else "!!"
        print(f"  {marca}  {d:24} {v['de']:>3}..{v['ate']:<3}"
              f"{' +999' if v['tem_999'] else '     '}  lacunas: {v['lacunas'] or 'nenhuma'}")

    sec("MODULOS (GUID = chave primaria)")
    print(f"  {'GUID':11} {'E3Lib':8} {'fontes':7} {'001/VR/GP/sigma':18} fw")
    for g, m in r.get("modulos", {}).items():
        n = sum(1 for f in ("fl", "VersaoRecurso", "GruposPadrao", "sigma", "no_001") if m.get(f))
        # Modulo com regra de fieldGroups nao precisa de sigma proprio: o alvo cai para 4.
        alvo = 4 if m.get("E3Lib") in COM_FIELDGROUP and not m.get("sigma") else 5
        vs = "/".join(str(m.get(f"v_{x}")) for x in ("001", "VersaoRecurso", "GruposPadrao", "sigma"))
        fgm = " fg" if m.get("E3Lib") in COM_FIELDGROUP else "   "
        print(f"  {g[:8] + '..':11} {str(m.get('E3Lib')):8} {n}/{alvo}{fgm}  {vs:18} {m.get('firmware')}")
    if r.get("sdg_funcionalidades") is not None:
        print(f"  [provisorio] Funcionalidades do SDG: {r['sdg_funcionalidades']} (esperado ['1'])")

    a = r.get("ativos", {})
    sec("ATIVOS")
    print(f"  001: {a.get('no_001')} | hierarchy: {a.get('no_hierarchy')} | "
          f"identicos: {'OK' if a.get('identicos') else '!!'}")
    print(f"  GUIDs orfaos em scripts por ativo: {a.get('orfaos_em_config')}")

    sec("ENGENHARIA")
    for n, v in sorted(r.get("engenharia", {}).items()):
        if v["script"] == "desconhecido":
            marca = "??" if v["preenchida"] else "--"
        else:
            marca = "OK" if v["preenchida"] == v["script"] else "!!"
        print(f"  {marca}  {n:32} preenchida={str(v['preenchida']):5} script={v['script']}")

    k = r.get("comunicacao", {})
    sec(f"COMUNICACAO ({k.get('modo', '?')})")
    if k.get("modo") == "Sync":
        print(f"  arquivo: {k.get('arquivo')}")
        print(f"  IEDs: {k.get('n_ieds')} | ModulosAtivos no hierarchy: "
              f"{k.get('modulos_ativos_hierarchy')}")
        print(f"  so no 001: {k.get('so_no_001') or 'nenhum'}")
        print(f"  so no sync: {k.get('so_no_sync') or 'nenhum'}")
        print(f"  Labels divergentes: {len(k.get('labels_divergentes', []))}")
        for l in k.get("labels_divergentes", []):
            print(f"     !! IED {l['ied']:02d}\n        esperado: {l['esperado']}"
                  f"\n        achado:   {l['achado']}")
    else:
        print(f"  pasta E3/: {k.get('pasta_E3')} | .prj: {k.get('prj')} | .dll: {k.get('dll')}")

    sec(f"ACHADOS ({len(r['achados'])})")
    if not r["achados"]:
        print("  nenhum")
    for i, x in enumerate(r["achados"], 1):
        print(f"  {i:02d}. [{x['cat']}] {x['msg']}")
        if x["onde"]:
            print(f"      onde: {x['onde']}")

    if r["notas"]:
        sec("NOTAS (nao sao achados)")
        for n in r["notas"]:
            print(f"  -- {n}")
    if r["perguntar"]:
        sec("PERGUNTAR AO USUARIO")
        for p in r["perguntar"]:
            print(f"  ?? {p}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    raiz = args[0]
    if not os.path.isdir(raiz):
        print(f"pasta nao encontrada: {raiz}")
        return 2
    forcar = None
    if "--e3" in sys.argv:
        forcar = False
    if "--sync" in sys.argv:
        forcar = True
    r = Coletor(raiz).rodar(forcar)
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=1, default=str))
    else:
        imprimir(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
