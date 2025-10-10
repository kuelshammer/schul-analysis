#!/usr/bin/env python3
"""
Korrigierte Implementierung für solveset mit periodischen Lösungen.
"""

import sympy as sp
from sympy import solveset, S, Symbol, pi, ImageSet, Union, Interval
from typing import List


def extrahiere_periodische_lösungen(
    image_set, x_bereich=(-2 * pi, 2 * pi)
) -> List[sp.Expr]:
    """Extrahiert konkrete Lösungen aus einem ImageSet für einen gegebenen Bereich."""
    if not hasattr(image_set, "lamda"):
        return []

    # Extrahiere Lambda-Ausdruck und Variable
    lambda_expr = image_set.lamda
    n_symbol = lambda_expr.variables[0]  # Normalerweise _n

    lösungen = []

    # Probiere verschiedene n-Werte im Bereich [-3, 3] für Schulmathematik
    for n_val in range(-3, 4):
        try:
            lösung = lambda_expr.expr.subs(n_symbol, n_val)

            # Prüfe, ob die Lösung im gewünschten Bereich liegt
            if hasattr(lösung, "evalf"):
                lösung_num = float(lösung.evalf())
                if x_bereich[0] <= lösung_num <= x_bereich[1]:
                    lösungen.append(lösung)
            else:
                # Symbolische Lösungen immer hinzufügen
                lösungen.append(lösung)
        except Exception as e:
            print(f"Fehler bei n={n_val}: {e}")

    return lösungen


def behandle_solveset_ergebnis(
    solveset_ergebnis, x_bereich=(-2 * pi, 2 * pi)
) -> List[sp.Expr]:
    """Verarbeitet verschiedene solveset-Ergebnistypen."""
    lösungen = []

    if isinstance(solveset_ergebnis, Union):
        # Behandle Union von mehreren ImageSets
        for arg in solveset_ergebnis.args:
            if isinstance(arg, ImageSet):
                lösungen.extend(extrahiere_periodische_lösungen(arg, x_bereich))
    elif isinstance(solveset_ergebnis, ImageSet):
        # Einzelnes ImageSet
        lösungen.extend(extrahiere_periodische_lösungen(solveset_ergebnis, x_bereich))
    else:
        # Fallback auf solve für einfache Fälle
        try:
            x = Symbol("x")
            einfache_lösungen = sp.solve(solveset_ergebnis, x)
            lösungen.extend(einfache_lösungen)
        except:
            pass

    return lösungen


def test_sin_cos_gleichung():
    """Testet die korrigierte Implementierung mit sin(x) + cos(x) = 0."""
    print("=== Test: sin(x) + cos(x) = 0 ===\n")

    x = Symbol("x")
    gleichung = sp.sin(x) + sp.cos(x)

    # Verwende solveset
    allgemeine_lösungen = solveset(gleichung, x, domain=S.Reals)
    print(f"solveset Ergebnis: {allgemeine_lösungen}")

    # Extrahiere konkrete Lösungen
    konkrete_lösungen = behandle_solveset_ergebnis(allgemeine_lösungen)

    print(f"\nGefundene Lösungen im Bereich [-2π, 2π]:")
    for i, lösung in enumerate(
        sorted(konkrete_lösungen, key=lambda x: float(x.evalf()))
    ):
        lösung_num = float(lösung.evalf())
        print(f"  {i + 1}. {lösung} ≈ {lösung_num:.3f}")

    # Vergleiche mit solve
    solve_lösungen = sp.solve(gleichung, x)
    print(f"\nsolve Ergebnis (zum Vergleich): {solve_lösungen}")

    return konkrete_lösungen


def test_andere_trigonometrische_gleichungen():
    """Testet andere trigonometrische Gleichungen."""
    print("\n" + "=" * 50)
    print("=== Weitere trigonometrische Gleichungen ===\n")

    x = Symbol("x")

    test_gleichungen = [
        (sp.sin(x), "sin(x) = 0"),
        (sp.cos(x), "cos(x) = 0"),
        (sp.tan(x), "tan(x) = 0"),
        (sp.sin(x) - 1, "sin(x) = 1"),
    ]

    for gleichung, beschreibung in test_gleichungen:
        print(f"--- {beschreibung} ---")
        allgemeine_lösungen = solveset(gleichung, x, domain=S.Reals)
        konkrete_lösungen = behandle_solveset_ergebnis(allgemeine_lösungen)

        print(f"Allgemein: {allgemeine_lösungen}")
        print(f"Konkrete Lösungen: {len(konkrete_lösungen)} gefunden")
        for lösung in sorted(konkrete_lösungen, key=lambda x: float(x.evalf()))[
            :5
        ]:  # Nur erste 5
            print(f"  {lösung} ≈ {float(lösung.evalf()):.3f}")
        print()


if __name__ == "__main__":
    test_sin_cos_gleichung()
    test_andere_trigonometrische_gleichungen()
