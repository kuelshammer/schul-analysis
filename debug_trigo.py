#!/usr/bin/env python3
"""
Debug-Skript zur Untersuchung von Sympy's Verhalten bei trigonometrischen Gleichungen.
"""

import sympy as sp


def test_trigonometrische_gleichungen():
    """Testet verschiedene Formen der trigonometrischen Gleichung."""
    print("=== Debug trigonometrische Gleichungen ===\n")

    x = sp.symbols("x")

    # Test 1: Originalform aus unserem Test
    print("1. Originalform: sin(x) + cos(x) = 0")
    gleichung1 = sp.sin(x) + sp.cos(x)
    print(f"Gleichung: {gleichung1}")

    lösungen1 = sp.solve(gleichung1, x)
    print(f"Lösungen: {lösungen1}")

    # Test 2: Äquivalente Form sin(x) = -cos(x)
    print("\n2. Äquivalente Form: sin(x) = -cos(x)")
    gleichung2 = sp.sin(x) + sp.cos(x)  # == 0 implizit
    print(f"Gleichung: sin(x) + cos(x) = 0")

    lösungen2 = sp.solve(gleichung2, x)
    print(f"Lösungen: {lösungen2}")

    # Test 3: tan(x) = -1 Form
    print("\n3. Tangens-Form: tan(x) = -1")
    gleichung3 = sp.tan(x) + 1
    print(f"Gleichung: {gleichung3}")

    lösungen3 = sp.solve(gleichung3, x)
    print(f"Lösungen: {lösungen3}")

    # Test 4: Vereinfachte Form
    print("\n4. Vereinfachte Form: √2 * sin(x + π/4) = 0")
    # sin(x) + cos(x) = √2 * sin(x + π/4)
    vereinfacht = sp.sqrt(2) * sp.sin(x + sp.pi / 4)
    print(f"Vereinfachte Form: {vereinfacht}")

    lösungen4 = sp.solve(vereinfacht, x)
    print(f"Lösungen: {lösungen4}")

    # Test 5: Überprüfen der Lösung
    print("\n5. Überprüfung der Lösung x = -π/4")
    test_wert = -sp.pi / 4
    ergebnis = gleichung1.subs(x, test_wert)
    print(f"sin(-π/4) + cos(-π/4) = {ergebnis}")
    print(f"Vereinfacht: {sp.simplify(ergebnis)}")

    # Test 6: Allgemeine Lösung
    print("\n6. Allgemeine Lösung mit solveset")
    from sympy import solveset, S

    allgemeine_lösungen = solveset(gleichung1, x, domain=S.Reals)
    print(f"Allgemeine Lösungen: {allgemeine_lösungen}")

    # Test 7: Periodische Lösungen
    print("\n7. Periodische Lösungen")
    if hasattr(allgemeine_lösungen, "as_relational"):
        print(f"Als Relation: {allgemeine_lösungen.as_relational(x)}")


if __name__ == "__main__":
    test_trigonometrische_gleichungen()
