# El término constante del problema de las n reinas

Programas de verificación exacta que acompañan el artículo de Dilan Steven Mejia. Conserve `articulo/` y `verificacion/` como carpetas hermanas. Desde `verificacion/`, ejecute:

```
python -B verificar.py --tiempos
```

Se necesita Python 3.10 o posterior con la biblioteca estándar. La ejecución se comprobó con CPython 3.13.16. El programa lee `../articulo/main.tex` y sus inclusiones. También se admite, por ejemplo, `python -B verificar.py --articulo ../articulo`. La opción `--salida` escribe las salidas en una carpeta nueva. Una discrepancia produce un código de salida distinto de cero. La ejecución es determinista y funciona sin conexión.

| Control | Qué comprueba |
|---|---|
| Álgebra | Pivote de una línea con una casilla, dieciséis signos de un rectángulo y coeficientes −5, +4 y +1. |
| Matrices y escalado | Identidades de determinante, cofactor y modo cero mediante eliminación exacta. Deriva por casilla y escalado en ejemplos racionales. |
| Historias | Masas de los prefijos y razón de las dos leyes sobre tableros 4, 5 y 6, con dos sistemas de pesos y cuatro reglas de parada. |
| Geometría | Conteo de etiquetas en soluciones pequeñas; recuento directo y por distancias, con comprobación de los subconjuntos de filas. |
| Cuatro figuras | Lee las posiciones del TikZ y comprueba con enteros los hijos de la fila, las dos familias de diagonales, el permanente de la máscara y los testigos. |
| Artículo | Comprueba 46 archivos LaTeX, 2 253 expresiones matemáticas, los números reconocidos por el analizador, las definiciones y el orden de las inclusiones. Nueve alteraciones deliberadas deben detectarse. Dos controles positivos admiten el espaciado inocuo y distinguen macros distintas. |

Las tablas y archivos JSON de `resultados/` se comparan byte por byte. `METODO.md` describe las construcciones independientes y el dominio de las identidades. El catálogo comprueba la correspondencia con el texto. La validez de las estimaciones asintóticas, del teorema externo de permanentes y de la constante límite se estudia en las demostraciones del artículo. El valor decimal del predictor procede del artículo citado allí.

## Tiempos medidos

Una ejecución en CPU con Python 3.13.16 tardó 1,799 s. Historias, 0,993 s; geometría, 0,599 s; identidades adicionales, 0,109 s; lectura y cotejo del LaTeX, 0,068 s; matrices, 0,025 s; álgebra, 0,003 s; los cuatro tableros de las figuras, 0,002 s. La salida de `--tiempos` vuelve a medir los tiempos en la máquina del lector. La diferencia hasta el total incluye las comprobaciones de archivos y el resto de la ejecución.

La licencia es MIT. Los datos de citación se encuentran en `CITATION.cff`.
