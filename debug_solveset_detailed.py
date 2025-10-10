#!/usr/bin/env python3
"""
Debug der solveset-Implementierung für trigonometrische Gleichungen.
"""

import sympy as sp
from sympy import solveset, S, Symbol, pi


def debug_solveset():
    """Debuggt die solveset-Funktionalität für sin(x) + cos(x) = 0."""
    print("=== Debug solveset für sin(x) + cos(x) = 0 ===\n")

    x = Symbol("x")
    gleichung = sp.sin(x) + sp.cos(x)

    print(f"Gleichung: {gleichung}")

    # solveset Ergebnis
    allgemeine_lösungen = solveset(gleichung, x, domain=S.Reals)
    print(f"solveset Ergebnis: {allgemeine_lösungen}")
    print(f"Typ: {type(allgemeine_lösungen)}")

    # Prüfe die Struktur
    if hasattr(allgemeine_lösungen, "is_Union"):
        print("Ist eine Union")
        print(f"Anzahl args: {len(allgemeine_lösungen.args)}")
        for i, arg in enumerate(allgemeine_lösungen.args):
            print(f"  Arg {i}: {arg} (Typ: {type(arg)})")

            if hasattr(arg, "lamda"):
                print(f"    Lambda: {arg.lamda}")
                print(f"    Lambda Expr: {arg.lamda.expr}")
                print(f"    Base Set: {arg.base_set}")

                # Teste Substitution
                n = Symbol("n", integer=True)
                print("    Test-Substitutionen:")
                for n_val in [-1, 0, 1, 2]:
                    try:
                        lösung = arg.lamda.expr.subs(n, n_val)
                        print(
                            f"      n={n_val}: {lösung} ≈ {float(lösung.evalf()):.3f}"
                        )
                    except Exception as e:
                        print(f"      n={n_val}: Fehler - {e}")

    elif hasattr(allgemeine_lösungen, "lamda"):
        print("Ist ein einzelnes ImageSet")
        print(f"Lambda: {allgemeine_lösungen.lamda}")
        print(f"Lambda Expr: {allgemeine_lösungen.lamda.expr}")

        # Teste Substitution
        n = Symbol("n", integer=True)
        print("Test-Substitutionen:")
        for n_val in [-1, 0, 1, 2]:
            try:
                lösung = allgemeine_lösungen.lamda.expr.subs(n, n_val)
                print(f"  n={n_val}: {lösung} ≈ {float(lösung.evalf()):.3f}")
            except Exception as e:
                print(f"  n={n_val}: Fehler - {e}")

    # Berechne erwartete Lösungen manuell
    print("\nErwartete Lösungen für sin(x) + cos(x) = 0:")
    print("x = nπ - π/4 für alle ganzen Zahlen n")

    for n_val in [-2, -1, 0, 1, 2]:
        manuelle_lösung = n_val * pi - pi / 4
        print(
            f"  n={n_val}: x = {manuelle_lösung} ≈ {float(manuelle_lösung.evalf()):.3f}"
        )

    # Überprüfe mit solve
    solve_lösungen = sp.solve(gleichung, x)
    print(f"\nsolve Ergebnis: {solve_lösungen}")


if __name__ == "__main__":
    debug_solveset()
