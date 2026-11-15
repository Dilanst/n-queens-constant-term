from itertools import permutations, product
import json


def _disponible(casilla, fijas):
    fila, columna = casilla
    return all(
        fila != i and columna != j and abs(fila - i) != abs(columna - j)
        for i, j in fijas
    )


def _solucion(perm):
    n = len(perm)
    return (
        set(perm) == set(range(1, n + 1))
        and len({i - j for i, j in enumerate(perm, 1)}) == n
        and len({i + j for i, j in enumerate(perm, 1)}) == n
    )


def _n7():
    fijas = [(1, 1)]
    indices = range(1, 8)
    columnas = [j for j in indices if _disponible((2, j), fijas)]
    soluciones = [
        perm for perm in permutations(indices)
        if perm[0] == 1 and _solucion(perm)
    ]
    por_hijo = [sum(perm[1] == j for perm in soluciones) for j in columnas]
    assert columnas == [3, 4, 5, 6, 7]
    assert por_hijo == [1, 1, 1, 1, 0]
    assert sum(por_hijo) == len(soluciones) == 4
    return {"columnas": columnas, "por_hijo": por_hijo, "total": len(soluciones)}


def _n8():
    i, ip = 2, 5
    j, jp = 2, 6
    casillas = [(i, j), (ip, j), (ip, jp), (i, jp)]
    posiciones = (1, 3)
    diagonales = [fila - col for fila, col in casillas]
    antidiagonales = [fila + col - 1 for fila, col in casillas]
    elegidas = [casillas[t - 1] for t in posiciones]
    signo = (-1) ** (len(casillas) - len(posiciones))
    assert casillas == [(2, 2), (5, 2), (5, 6), (2, 6)]
    assert elegidas == [(2, 2), (5, 6)]
    assert len(set(diagonales)) == len(set(antidiagonales)) == 4
    assert signo == 1
    return {
        "casillas": casillas, "T": posiciones, "diagonales": diagonales,
        "antidiagonales": antidiagonales, "signo": signo,
    }


def _n11():
    perm = (1, 3, 5, 7, 9, 11, 2, 4, 6, 8, 10)
    assert _solucion(perm)
    filas = (1, 3, 9, 11)
    fijas = [(i, j) for i, j in enumerate(perm, 1) if i not in filas]
    ocupadas = {j for _, j in fijas}
    columnas = [j for j in range(1, 12) if j not in ocupadas]
    mascara = [
        [int(_disponible((i, j), fijas)) for j in columnas] for i in filas
    ]
    asignaciones = permutations(range(len(columnas)))
    permanente = sum(
        all(mascara[t][j] for t, j in enumerate(sigma))
        for sigma in asignaciones
    )
    assert columnas == [1, 5, 6, 10]
    assert mascara == [[1, 0, 0, 0], [0, 1, 0, 1],
                       [1, 0, 1, 0], [0, 1, 0, 1]]
    assert not ({abs(i-j) for i,j in permutations(filas,2)} &
                {abs(i-j) for i,j in permutations(columnas,2)})
    assert permanente == 2
    return {
        "filas": filas, "columnas": columnas,
        "mascara": mascara, "permanente": permanente,
    }


def _n6():
    perm = (2, 4, 6, 1, 3, 5)
    assert _solucion(perm)
    n = len(perm)
    pares = list(permutations(range(1, n + 1), 2))

    def distancias(i, ip, j, jp):
        return abs(i - ip), abs(perm[j - 1] - perm[jp - 1])

    por_m = {2: 0, 3: 0, 4: 0}
    for (i, ip), (j, jp) in product(pares, repeat=2):
        distancia_filas, distancia_columnas = distancias(i, ip, j, jp)
        if distancia_filas == distancia_columnas:
            m = len({i, ip, j, jp})
            por_m[m] += 1

    testigos = [(1, 2, 1, 4), (1, 2, 3, 6)]
    for testigo, m in zip(testigos, (3, 4)):
        assert distancias(*testigo) == (1, 1)
        assert len(set(testigo)) == m
    assert por_m == {2: 0, 3: 136, 4: 84}
    total = sum(por_m.values())
    assert total == 4 * sum((n - d) ** 2 for d in range(1, n)) == 220
    return {"testigos": testigos, "por_m": por_m, "total": total}


def comprobar():
    return {"n7": _n7(), "n8": _n8(), "n11": _n11(), "n6": _n6()}




def verificar(articulo):
    """Comprueba las coordenadas impresas y las listas que alimentan los dibujos."""
    from pathlib import Path
    import re

    base = Path(articulo).resolve()
    base = base if base.is_dir() else base.parent
    textos = {
        nombre: re.sub(r"\s+", "", (base / "figuras" / (nombre + ".tex")).read_text(encoding="utf-8"))
        for nombre in ("historia", "rectangulo", "terminal", "testigos")
    }
    resultados = comprobar()

    def confirmar(nombre, fragmentos):
        for fragmento in fragmentos:
            if fragmento not in textos[nombre]:
                raise ValueError(f"Las coordenadas o la leyenda de {nombre} no concuerdan: {fragmento}")

    def pares_tikz(pares):
        return ",".join(f"{i}/{j}" for i, j in pares)

    h = resultados["n7"]
    confirmar("historia", (r"\bcuadricula{7}", r"\breina{7}{1}{1}", r"\breina{7}{2}{3}",
                            ",".join(map(str, h["por_hijo"])), "Q(B)=4",
                            r"(abs(\rr-1)!=abs(\cc-1))", r"(abs(\rr-2)!=abs(\cc-3))"))
    n8 = resultados["n8"]
    confirmar("rectangulo", (pares_tikz(n8["casillas"]), r"T=\{1,3\}", "(-1)^{4-2}=+1"))
    n11 = resultados["n11"]
    plantadas = (1, 3, 5, 7, 9, 11, 2, 4, 6, 8, 10)
    filas, columnas, mascara = n11["filas"], n11["columnas"], n11["mascara"]
    reinas = [(i, j) for i, j in enumerate(plantadas, 1) if i not in filas]
    libres = [(i, j) for r, i in enumerate(filas) for c, j in enumerate(columnas) if mascara[r][c]]
    matriz = ",".join(f"{r}/" + "{" + ",".join(map(str, fila)) + "}" for r, fila in enumerate(mascara, 1))
    confirmar("terminal", (pares_tikz(reinas), pares_tikz(libres), matriz, r"\operatorname{per}=2"))
    n6 = resultados["n6"]
    perm = (2, 4, 6, 1, 3, 5)
    trazos = []
    for i, ip, j, jp in n6["testigos"]:
        m = len({i, ip, j, jp})
        trazos.append((m, perm[j-1], perm[jp-1]))
    confirmar("testigos", (pares_tikz(enumerate(perm, 1)), r"\bmarca{6}{1}{\uno}", r"\bmarca{6}{2}{\dos}",
                           f"{trazos[0][0]}/0/{trazos[0][1]}/{trazos[0][2]}",
                           f"{trazos[1][0]}/8.3/{trazos[1][1]}/{trazos[1][2]}"))
    return resultados
