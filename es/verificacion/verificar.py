"""Ejecución reproducible, con CSV/JSON y código de salida no nulo ante discrepancias."""
import argparse
import csv
import io
import json
import sys
from pathlib import Path
from time import perf_counter
import algebra
import cotejo
import ensayos
import geometria
import historias
import matriz
import ampliacion
import figuras

BASE=Path(__file__).resolve().parent

def como_csv(rows):
    s=io.StringIO(newline="")
    writer=csv.DictWriter(s,fieldnames=list(rows[0]),lineterminator="\n")
    writer.writeheader();writer.writerows(rows)
    return s.getvalue().encode("utf-8")

def como_json(obj):
    return (json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+"\n").encode("utf-8")

def calcular(articulo):
    ti={};datos={}
    def correr(key,fn):
        t=perf_counter();v=fn();ti[key]=perf_counter()-t;return v
    datos["identidades.json"]=como_json({"algebra":correr("álgebra",algebra.verificar),
                                        "matriz":correr("matriz",matriz.verificar)})
    datos["ampliacion.json"]=como_json(correr("identidades adicionales",ampliacion.verificar))
    datos["historias.csv"]=como_csv(correr("historias",historias.verificar))
    datos["geometria.csv"]=como_csv(correr("geometría",geometria.verificar))
    datos["figuras.json"]=como_json(correr("tableros de las figuras",lambda:figuras.verificar(articulo)))
    datos["texto.json"]=como_json({"cotejo":correr("texto",lambda:cotejo.verificar(articulo)),
                                   "ensayos":correr("alteraciones",ensayos.verificar)})
    return datos,ti

def principal():
    if not __debug__:
        raise RuntimeError("Ejecute Python sin la opción -O para comprobar las aserciones.")
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--articulo",type=Path,default=BASE.parent/"articulo"/"main.tex")
    ap.add_argument("--salida",type=Path,help="escribir una copia en un directorio nuevo")
    ap.add_argument("--tiempos",action="store_true",help="medir segundos de esta ejecución")
    args=ap.parse_args();t=perf_counter()
    datos,ti=calcular(args.articulo)
    for f,bb in datos.items():
        base=(BASE/"resultados"/f).read_bytes()
        if bb!=base:raise ValueError("Diferencia con los resultados distribuidos: "+f)
    if args.salida is not None:
        args.salida.mkdir(exist_ok=False)
        for f,bb in datos.items():
            with (args.salida/f).open("xb") as out:out.write(bb)
    print("Correcto: álgebra, matriz, historias, geometría, figuras, texto y controles negativos.")
    if args.tiempos:
        print(json.dumps({"segundos":ti,"total":perf_counter()-t,
                          "python":sys.version.split()[0]},ensure_ascii=True,indent=2))
    return 0

if __name__=="__main__":
    try:sys.exit(principal())
    except (OSError, ValueError, RuntimeError) as e:
        print("ERROR:",e,file=sys.stderr);sys.exit(1)
