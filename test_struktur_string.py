#!/usr/bin/env python3
"""
Test der Strukturanalyse mit String-Eingabe
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

from schul_mathematik.analysis.struktur import (
    analysiere_funktionsstruktur,
    _faktorisiere_exponential_summe,
)
import sympy as sp


def test_struktur_mit_string():
    """Testet die Strukturanalyse mit String-Eingabe"""

    print("=== Teste Strukturanalyse mit String-Eingabe ===\n")

    test_string = "exp(x) + exp(2*x)"
    print(f"Test-String: {test_string}")

    # Strukturanalyse
    struktur = analysiere_funktionsstruktur(test_string)
    print(f"Struktur: {struktur['struktur']}")
    print(f"Komponenten: {[k['term'] for k in struktur['komponenten']]}")

    # Teste die Faktorisierung direkt mit dem geparsten Ausdruck
    x = sp.symbols("x")
    parsed_expr = sp.exp(x) + sp.exp(2 * x)
    print(f"\nGeparster Ausdruck: {parsed_expr}")
    print(f"Typ des geparsten Ausdrucks: {type(parsed_expr)}")

    kann_faktorisiert, gemeinsamer_faktor, rest_faktor = (
        _faktorisiere_exponential_summe(parsed_expr, x)
    )
    print(f"Kann faktorisiert: {kann_faktorisiert}")
    if kann_faktorisiert:
        print(f"Gemeinsamer Faktor: {gemeinsamer_faktor}")
        print(f"Rest-Faktor: {rest_faktor}")

    # Teste, was in der Strukturanalyse passiert
    print(f"\n=== Debug in Strukturanalyse ===")
    temp_funktion = __import__(
        "schul_mathematik.analysis.funktion", fromlist=["Funktion"]
    ).Funktion(test_string)
    expr_analyse = temp_funktion.term_sympy
    print(f"expr_analyse: {expr_analyse}")
    print(f"Typ: {type(expr_analyse)}")

    variable = temp_funktion._variable_symbol
    print(f"Variable: {variable}")

    # Teste Faktorisierung mit diesem Ausdruck
    kann_faktorisiert2, gemeinsamer_faktor2, rest_faktor2 = (
        _faktorisiere_exponential_summe(expr_analyse, variable)
    )
    print(f"Kann faktorisiert (mit Struktur-Analyse-Expr): {kann_faktorisiert2}")
    if kann_faktorisiert2:
        print(f"Gemeinsamer Faktor: {gemeinsamer_faktor2}")
        print(f"Rest-Faktor: {rest_faktor2}")


if __name__ == "__main__":
    test_struktur_mit_string()
