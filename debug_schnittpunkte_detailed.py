#!/usr/bin/env python3
"""
Detailliertes Debugging der Schnittpunkt-Erstellung und Validierung
"""

import sys

sys.path.insert(0, "src")

import sympy as sp
from schul_analysis import Funktion
from schul_analysis.sympy_types import (
    Schnittpunkt,
    is_exact_schnittpunkt,
    is_exact_sympy_expr,
)


def debug_detailed():
    print("=== Detailliertes Debugging ===")

    # Test: Einfache Funktionen
    f = Funktion("x^2")
    g = Funktion("2*x")

    # Manuelle Berechnung
    gleichung = sp.Eq(f.term_sympy, g.term_sympy)
    x_loesungen = sp.solve(gleichung, f._variable_symbol)

    print(f"Lösungen: {x_loesungen}")

    # Manuelles Erstellen von Schnittpunkten
    for x_loesung in x_loesungen:
        print(f"\nVerarbeite x = {x_loesung} (Typ: {type(x_loesung)})")

        y_wert = f.wert(x_loesung)
        print(f"y = {y_wert} (Typ: {type(y_wert)})")

        # Erstelle Schnittpunkt
        sp_obj = Schnittpunkt(x=x_loesung, y=y_wert, exakt=True)
        print(f"Schnittpunkt: {sp_obj}")

        # Teste Type Guards
        print(f"is_exact_sympy_expr(x): {is_exact_sympy_expr(x_loesung)}")
        print(f"is_exact_sympy_expr(y): {is_exact_sympy_expr(y_wert)}")
        print(f"is_exact_schnittpunkt(sp): {is_exact_schnittpunkt(sp_obj)}")

        # Debugge die Validierung
        print(f"sp.x.is_Float: {hasattr(sp_obj.x, 'is_Float') and sp_obj.x.is_Float}")
        print(f"sp.y.is_Float: {hasattr(sp_obj.y, 'is_Float') and sp_obj.y.is_Float}")
        print(f"sp.x atoms: {list(sp_obj.x.atoms(sp.Number))}")
        print(f"sp.y atoms: {list(sp_obj.y.atoms(sp.Number))}")

        # Prüfe auf Float in Atomen
        x_atoms = list(sp_obj.x.atoms(sp.Number))
        y_atoms = list(sp_obj.y.atoms(sp.Number))
        x_has_float = any(isinstance(atom, sp.Float) for atom in x_atoms)
        y_has_float = any(isinstance(atom, sp.Float) for atom in y_atoms)
        print(f"x_has_float: {x_has_float}, y_has_float: {y_has_float}")


if __name__ == "__main__":
    debug_detailed()
