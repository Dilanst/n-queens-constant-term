# The Constant Term of the n-Queens Problem

These exact verification programs accompany the paper by Dilan Steven Mejia.
Keep `paper/` and `verification/` as sibling folders. From `verification/`, run

```
python -B verificar.py --tiempos
```

The programs require Python 3.10 or later and use only the standard library. The run was verified
with CPython 3.13.16. The program reads `../paper/main.tex` and its included files. An explicit path
is also supported, for example `python -B verificar.py --articulo ../paper`. The `--salida` option
writes the outputs to a new folder. A discrepancy produces a nonzero exit code. The run is
deterministic and works offline.

| Check | What it verifies |
|---|---|
| Algebra | The pivot for a line containing one square, the sixteen signs of a rectangle, and the coefficients −5, +4, and +1. |
| Matrices and scaling | Determinant, cofactor, and zero-mode identities by exact elimination. Square-by-square drift and scaling in rational examples. |
| Histories | Prefix masses and the ratio of the two laws on boards of sizes 4, 5, and 6, with two weight systems and four stopping rules. |
| Geometry | Label counts for small solutions, computed directly and by distances, with a check on subsets of rows. |
| Four figures | Reads the positions from TikZ and uses integer arithmetic to check the children for the chosen row, both diagonal families, the permanent of the mask, and the witnesses. |
| Paper | Checks 38 LaTeX files, 1,940 mathematical expressions, 713 numerical tokens in the prose, 21 definitions, and 37 inclusions in order. |

Nine deliberate mutations and two positive controls are performed on English source extracts in memory.
All nine mutations must be detected. The two positive controls check that the parser accepts harmless
spacing changes and distinguishes different macros.

The tables and JSON files in `resultados/` are compared byte for byte. `METHOD.md` describes the
independent constructions and the domain of the identities. The catalog checks correspondence with
the text. The proofs in the paper address the validity of the asymptotic estimates, the external
theorem on permanents, and the limiting constant. The decimal value of the predictor comes from the
paper cited there.

## Measured timings

One CPU run using CPython 3.13.16 took 1.777 s in total. Component times in seconds: algebra 0.003, matrix 0.026, additional identities 0.107, histories 0.888, geometry 0.642, boards in the figures 0.002, article text 0.069, mutations 0.040.

The `--tiempos` option measures the timings again on the reader's machine. The difference between
the sum of the individual timings and the total includes file checks and the rest of the run.

The license is MIT. Citation metadata are in `CITATION.cff`.
