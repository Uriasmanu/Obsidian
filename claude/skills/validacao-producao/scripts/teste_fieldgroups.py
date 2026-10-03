"""Fixture sintetica para testar a regra COM_FIELDGROUP do coletor.

Nenhum dado de producao: GUIDs e nomes sao inventados. Monta uma producao minima
com TM1/TM2 (familia com fieldGroups, um sigma so) e BM (sem fieldGroups), depois
injeta um defeito por vez e confere que o coletor acha o que deve achar.
"""
import json
import os
import shutil
import subprocess
import sys

TM1 = "11111111-1111-1111-1111-111111111111"
TM2 = "22222222-2222-2222-2222-222222222222"
BM = "33333333-3333-3333-3333-333333333333"
FG1 = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
FG2 = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
ATIVO = "44444444-4444-4444-4444-444444444444"
MA_TM1 = "55555555-5555-5555-5555-555555555555"
MA_TM2 = "66666666-6666-6666-6666-666666666666"
MA_BM = "77777777-7777-7777-7777-777777777777"

COLETOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coletar.py")


def escrever(raiz, rel, texto):
    destino = os.path.join(raiz, rel)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(texto)


def fl(alias, guid):
    return (f"DECLARE @ModuloId UNIQUEIDENTIFIER = '{guid}'\n"
            f"UPDATE Modulo SET E3Lib = '{alias}' WHERE Id = @ModuloId\n")


def versao_recurso(guid):
    return (f"SET @RecursoId = '{guid}'\n"
            f"DECLARE @TagVersaoMapa VARCHAR(50) = 'v1-MDB'\n")


def grupos(guid):
    return (f"DECLARE @ModuloId UNIQUEIDENTIFIER = '{guid}'\n"
            f"DECLARE @VersaoModulo NVARCHAR(500) = N'v1-MDB'\n")


def sigma(module_id, identifier, field_groups):
    d = {
        # fields[] vem antes e tambem tem moduleId -- e a armadilha que o coletor
        # precisa evitar ao identificar o modulo do sigma.
        "fields": [{"id": "ffffffff-0000-0000-0000-000000000001", "name": "campo",
                    "moduleId": module_id, "versions": ["1.0"]}],
        "modules": [{"id": module_id, "name": f"{identifier} - modulo de teste",
                     "identifier": identifier,
                     "versions": [{"resourceVersionValue": "1.0",
                                   "productVersion": "v1.0-sync"}]}],
    }
    if field_groups:
        d["fieldGroups"] = [{"id": g, "identifierSuffix": s, "moduleId": module_id,
                             "moduleVersion": "1.0"} for g, s in field_groups]
    return d


def bloco(ma, modulo):
    return (f"\t-- ------------------ Criando: AT001 x modulo ------------------\n"
            f"\t--Adicionando ModuloAtivo\n"
            f"\tSET @ModuloAtivoId = N'{ma}'\n"
            f"\tSET @ModuloId = N'{modulo}'\n"
            f"\tSET @ModuloAtivoFuncionalidades = 7\n"
            f"\tSET @SetGroup = NULL\n"
            f"\tSET @VersaoModuloAtivo = N'v1-MDB'\n\n")


def montar(raiz, defeito=None):
    if os.path.isdir(raiz):
        shutil.rmtree(raiz)

    escrever(raiz, "client/00-create-database-client.sql", "CREATE DATABASE [acme]\n")

    for n, (alias, guid) in enumerate([("TM1", TM1), ("TM2", TM2), ("BM", BM)]):
        escrever(raiz, f"DB/00-INITIAL-SCRIPTS/{2*n+1:03d} - {alias}-fl.sql", fl(alias, guid))
        escrever(raiz, f"DB/00-INITIAL-SCRIPTS/{2*n+2:03d} - {alias}-VersaoRecurso.sql",
                 versao_recurso(guid))
        escrever(raiz, f"DB/02-GROUPS/{n+1:03d} - {alias}-GruposPadrao.sql", grupos(guid))

    corpo = ("DECLARE @ModuloAtivoId UNIQUEIDENTIFIER = NULL\n"
             f"\tSET @AtivoId = N'{ATIVO}'\n\n"
             + bloco(MA_TM1, TM1) + bloco(MA_TM2, TM2) + bloco(MA_BM, BM))
    escrever(raiz, "DB/01-BACKBONE/001_acme.sql", corpo)
    escrever(raiz, "DB/01-BACKBONE/999_acme-perfil-root.sql", "SET @idPerfilRoot = NULL\n")

    # A familia TM: os dois sigmas carregam o moduleId do TM1 e o identifier 'TM'.
    sigmas = [("001 - TM1-sigma-sync-import.json", sigma(TM1, "TM", [(FG1, "1")])),
              ("002 - TM2-sigma-sync-import.json", sigma(TM1, "TM", [(FG2, "2")])),
              ("003 - BM-sigma-sync-import.json", sigma(BM, "BM", []))]
    if defeito == "fg_orfao_no_sigma":
        sigmas[1] = ("002 - TM2-sigma-sync-import.json", sigma(TM1, "TM", []))
    for nome, dados in sigmas:
        escrever(raiz, f"DB/03 - JSON/{nome}", json.dumps(dados, indent=1))

    fg_tm1, fg_tm2, fg_bm = FG1, FG2, None
    if defeito == "fg_faltando":
        fg_tm2 = None
    if defeito == "fg_em_modulo_sem_regra":
        fg_bm = FG1
    if defeito == "fg_repetido":
        fg_tm2 = FG1

    assoc_tm = [{"AssetModuleId": MA_TM1, "AssetIdentifier": "AT001",
                 "TableSufix": None, "FieldGroupId": fg_tm1},
                {"AssetModuleId": MA_TM2, "AssetIdentifier": "AT001",
                 "TableSufix": None, "FieldGroupId": fg_tm2}]
    if defeito == "ma_sumiu_do_sync":
        assoc_tm = assoc_tm[:1]

    sync = {"Name": "Planta 1", "DataSources": [{"SourceIdentifier": "gw", "Name": "gw",
            "SerialNumber": "1", "Ieds": [
                {"ModuleIdentifier": "TM", "ModuleVersion": "1.0",
                 "Label": "Acme - Planta 1 - TR-01 - TM", "Identifier": "ied-tm",
                 "HasOscillography": False, "Associations": assoc_tm},
                {"ModuleIdentifier": "BM", "ModuleVersion": "1.0",
                 "Label": "Acme - Planta 1 - TR-01 - BM", "Identifier": "ied-bm",
                 "HasOscillography": False, "Associations": [
                     {"AssetModuleId": MA_BM, "AssetIdentifier": "AT001",
                      "TableSufix": None, "FieldGroupId": fg_bm}]}]}]}
    escrever(raiz, "DB/03 - JSON/004_acme_sync.json", json.dumps(sync, indent=1))

    hier = {"Empresas": [{"Nome": "Acme"}], "Instalacoes": [{"Nome": "Planta 1"}],
            "Ativos": [{"Id": ATIVO, "Identificador": "AT001", "Nome": "TR-01"}],
            "ModulosAtivos": [{"Id": MA_TM1}, {"Id": MA_TM2}, {"Id": MA_BM}]}
    escrever(raiz, "DB/03 - JSON/acme_hierarchy_export.json", json.dumps(hier, indent=1))


def achados(raiz):
    saida = subprocess.run([sys.executable, COLETOR, raiz, "--json"],
                           capture_output=True, text=True).stdout
    return [a["msg"] for a in json.loads(saida)["achados"]]


CASOS = [
    (None, None),
    ("fg_faltando", "sem FieldGroupId"),
    ("fg_em_modulo_sem_regra", "nao tem regra de fieldGroups"),
    ("fg_orfao_no_sigma", "nao existe em nenhum sigma"),
    ("fg_repetido", "repetido em mais"),
    ("ma_sumiu_do_sync", "nao tem IED no sync"),
]

if __name__ == "__main__":
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixture-acme")
    falhou = False
    for defeito, esperado in CASOS:
        montar(base, defeito)
        achou = achados(base)
        if esperado is None:
            ok = not achou
            print(f"{'OK  ' if ok else 'FALHA'} baseline limpo -> {achou or 'nenhum achado'}")
        else:
            ok = any(esperado in m for m in achou)
            print(f"{'OK  ' if ok else 'FALHA'} {defeito}: esperava '{esperado}' -> {achou}")
        falhou = falhou or not ok
    shutil.rmtree(base, ignore_errors=True)
    sys.exit(1 if falhou else 0)
