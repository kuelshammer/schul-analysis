#!/usr/bin/env python3
"""
Detailliertes Debug-Skript für die Exponential-Faktorisierung
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

import sympy as sp


def test_ist_exponential_term():
    """Testet die Erkennung von Exponential-Termen"""

    print("=== Teste Exponential-Term-Erkennung ===\n")

    x = sp.symbols("x")

    def ist_exponential_term(term):
        print(f"  Analysiere Term: {term}")
        print(f"    Typ: {type(term)}")
        print(f"    Funktion: {term.func}")
        print(f"    Args: {term.args}")

        if isinstance(term, sp.Mul):
            print(f"    Ist Mul - prüfe Faktoren:")
            for i, factor in enumerate(term.args):
                print(f"      Faktor {i}: {factor} (Typ: {type(factor)})")
                if isinstance(factor, sp.exp):
                    print(f"      >>> Exponential-Faktor gefunden: {factor}")
                    return factor
        elif isinstance(term, sp.exp):
            print(f"    >>> Reiner Exponential-Term")
            return term
        print(f"    >>> Kein Exponential-Term")
        return None

    test_terms = [
        sp.exp(x),
        sp.exp(2 * x),
        2 * sp.exp(x),
        3 * sp.exp(2 * x),
        x**2,
        sp.sin(x),
    ]

    for term in test_terms:
        result = ist_exponential_term(term)
        print(f"  Ergebnis: {result}\n")


if __name__ == "__main__":
    test_ist_exponential_term()
