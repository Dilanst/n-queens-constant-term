"""Sensitivity checks using in-memory mutations of the distributed English article."""
from pathlib import Path

from cotejo import diferencia, extraer, inventario
from exacto import exigir


def verificar(articulo):
    main = Path(articulo)
    if main.is_dir():
        main = main / "main.tex"
    reference = inventario(main)
    base = main.parent
    sections = "sections/"
    abstract = sections + "00_abstract.tex"
    intro = sections + "01_introduction.tex"
    factors = sections + "06e_normalizers.tex"

    def source(name):
        return (base / name).read_text(encoding="utf-8-sig")

    def changed(name, updated):
        return {**reference, name: [list(item) for item in extraer(updated)[0]]}

    def replace_once(name, old, new):
        text = source(name)
        exigir(old in text, f"Mutation target missing in {name}: {old}")
        return changed(name, text.replace(old, new, 1))

    mutations = [
        ("sign", intro, r"\log Q(n)-\log n!", r"\log Q(n)+\log n!"),
        ("digit", abstract, "0.9401", "0.9402"),
        ("number in words", abstract, "two laws", "three laws"),
        ("inclusion", "main.tex", r"\input{sections/01_introduction}", ""),
        ("local coefficient", factors, "-5a_2", "-6a_2"),
        ("row and column coefficient", factors, "4a_2+O(k^{-1})", "3a_2+O(k^{-1})"),
        ("Schur complement coefficient", factors, r"\log\det U=a_2+", r"\log\det U=2a_2+"),
    ]
    for name, file, old, new in mutations:
        exigir(bool(diferencia(reference, replace_once(file, old, new))), "Undetected change: " + name)
    added = changed(intro, source(intro) + "\n" + r"\[z=3\]" + "\n")
    exigir(bool(diferencia(reference, added)), "Undetected additional formula")
    omitted = {name: items for name, items in reference.items() if name != abstract}
    exigir(bool(diferencia(reference, omitted)), "Undetected missing section")
    spaced = replace_once(intro, r"\log Q(n)-\log n!", r"\log Q(n) - \log n!")
    exigir(not diferencia(reference, spaced), "Harmless spacing changed the inventory")
    merged = replace_once(intro, r"\log Q", r"\logQ")
    exigir(bool(diferencia(reference, merged)), "Different control sequences were conflated")
    return {"alteraciones_detectadas": len(mutations) + 2, "controles_positivos": 2}
