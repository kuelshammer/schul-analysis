#!/usr/bin/env python3
"""
Gezielter Test für die verbesserte trigonometrische Nullstellenberechnung.
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis import Funktion
import sympy as sp


def test_trigonometrische_summen():
    """Testet verschiedene trigonometrische Summenfunktionen."""
    print("=== Test trigonometrischer Summenfunktionen ===\n")

    # Test 1: sin(x) + cos(x) - explizit als Summe
    print("1. sin(x) + cos(x)")
    f1 = Funktion("sin(x) + cos(x)")
    print(f"Funktionstyp: {f1.funktionstyp}")
    print(f"Term: {f1.term()}")

    # Prüfe ob es eine SummenFunktion ist
    if hasattr(f1, "summanden"):
        print(f"Summanden: {[str(s) for s in f1.summanden]}")

    nullstellen = f1.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    # Test 2: 2*sin(x) + 3*cos(x)
    print("\n2. 2*sin(x) + 3*cos(x)")
    f2 = Funktion("2*sin(x) + 3*cos(x)")
    print(f"Funktionstyp: {f2.funktionstyp}")
    nullstellen2 = f2.nullstellen()
    print(f"Nullstellen: {nullstellen2}")

    # Test 3: sin(x) + tan(x)
    print("\n3. sin(x) + tan(x)")
    f3 = Funktion("sin(x) + tan(x)")
    print(f"Funktionstyp: {f3.funktionstyp}")
    nullstellen3 = f3.nullstellen()
    print(f"Nullstellen: {nullstellen3}")

    # Test 4: Direkter Vergleich mit Sympy solveset
    print("\n4. Direkter Sympy-Vergleich:")
    x = sp.symbols("x")

    for i, (name, gleichung) in enumerate(
        [
            ("sin(x) + cos(x)", sp.sin(x) + sp.cos(x)),
            ("2*sin(x) + 3*cos(x)", 2 * sp.sin(x) + 3 * sp.cos(x)),
            ("sin(x) + tan(x)", sp.sin(x) + sp.tan(x)),
        ],
        1,
    ):
        print(f"\n4.{i} {name} = 0")

        # Mit solve
        solve_lösungen = sp.solve(gleichung, x)
        print(f"   solve(): {solve_lösungen}")

        # Mit solveset
        from sympy import solveset, S

        solveset_lösungen = solveset(gleichung, x, domain=S.Reals)
        print(f"   solveset(): {solveset_lösungen}")

        # Konkrete Lösungen extrahieren
        if hasattr(solveset_lösungen, "args"):
            konkrete = []
            for arg in solveset_lösungen.args:
                if hasattr(arg, "lamda"):
                    n = sp.Symbol("n", integer=True)
                    for n_val in [-1, 0, 1]:
                        try:
                            lösung = arg.lamda.expr.subs(n, n_val)
                            konkrete.append(lösung)
                        except:
                            continue
            print(f"   Konkrete Lösungen: {konkrete}")


if __name__ == "__main__":
    test_trigonometrische_summen()
