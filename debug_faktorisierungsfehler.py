#!/usr/bin/env python3
"""
Debug des spezifischen Faktorisierungsproblems
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

import sympy as sp
from schul_mathematik.analysis.struktur import _faktorisiere_exponential_summe


def debug_faktorisierungsfehler():
    """Debuggt, warum die Faktorisierung fehlschlägt"""

    print("=== Debug Faktorisierungsfehler ===\n")

    x = sp.symbols("x")

    # Test mit dem konkreten Ausdruck aus der Strukturanalyse
    expr = sp.exp(2 * x) + sp.exp(x)
    print(f"Ausdruck: {expr}")
    print(f"Typ: {type(expr)}")
    print(f"Funktion: {expr.func}")
    print(f"Args: {expr.args}")

    # Teste Schritt für Schritt
    if not isinstance(expr, sp.Add) or len(expr.args) != 2:
        print(f"  FEHLER: Keine Summe mit 2 Termen")
        return

    term1, term2 = expr.args
    print(f"  Term1: {term1} (Typ: {type(term1)})")
    print(f"  Term2: {term2} (Typ: {type(term2)})")

    # Exponential-Term Erkennung
    def ist_exponential_term(term):
        print(f"    Prüfe Term: {term}")
        if isinstance(term, sp.Mul):
            print(f"    Ist Mul - Faktoren: {term.args}")
            for factor in term.args:
                print(f"      Faktor: {factor} (Typ: {type(factor)})")
                if isinstance(factor, sp.exp):
                    print(f"      >>> Exponential-Faktor gefunden: {factor}")
                    return factor
        elif isinstance(term, sp.exp):
            print(f"    >>> Reiner Exponential-Term")
            return term
        print(f"    >>> Kein Exponential-Term")
        return None

    exp1 = ist_exponential_term(term1)
    exp2 = ist_exponential_term(term2)

    print(f"  Exponential-Term 1: {exp1}")
    print(f"  Exponential-Term 2: {exp2}")

    if exp1 is None or exp2 is None:
        print(f"  FEHLER: Nicht beide sind Exponential-Terme")
        return

    # Teste die eigentliche Funktion
    kann_faktorisiert, gemeinsamer_faktor, rest_faktor = (
        _faktorisiere_exponential_summe(expr, x)
    )
    print(f"\nErgebnis der Funktion:")
    print(f"  Kann faktorisiert: {kann_faktorisiert}")
    if kann_faktorisiert:
        print(f"  Gemeinsamer Faktor: {gemeinsamer_faktor}")
        print(f"  Rest-Faktor: {rest_faktor}")

    # Teste mit manuell erstellter Funktion
    print(f"\n=== Manueller Test ===")
    expr_manual = sp.exp(x) + sp.exp(2 * x)
    print(f"Manueller Ausdruck: {expr_manual}")
    kann_faktorisiert_manual, gemeinsamer_faktor_manual, rest_faktor_manual = (
        _faktorisiere_exponential_summe(expr_manual, x)
    )
    print(f"Manuell - Kann faktorisiert: {kann_faktorisiert_manual}")
    if kann_faktorisiert_manual:
        print(f"Manuell - Gemeinsamer Faktor: {gemeinsamer_faktor_manual}")
        print(f"Manuell - Rest-Faktor: {rest_faktor_manual}")


if __name__ == "__main__":
    debug_faktorisierungsfehler()
