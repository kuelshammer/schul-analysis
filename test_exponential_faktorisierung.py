#!/usr/bin/env python3
"""
Testscript für die neue Exponential-Summen Faktorisierung
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

from schul_mathematik.analysis.struktur import analysiere_funktionsstruktur
from schul_mathematik.analysis.funktion import Funktion
import sympy as sp


def test_exponential_faktorisierung():
    """Testet die neue Exponential-Faktorisierungslogik"""

    print("=== Teste Exponential-Summen Faktorisierung ===\n")

    test_cases = [
        "exp(x) + exp(2*x)",
        "exp(2*x) + exp(x)",
        "exp(3*x) + exp(5*x)",
        "2*exp(x) + 3*exp(2*x)",
        "exp(x) + exp(x)",  # Gleiche Koeffizienten - sollte nicht faktorisiert werden
        "exp(x) + x^2",  # Gemischt - sollte nicht faktorisiert werden
        "exp(2*x) + exp(-x)",
    ]

    for test_case in test_cases:
        print(f"Teste: {test_case}")
        try:
            # Strukturanalyse
            struktur = analysiere_funktionsstruktur(test_case)
            print(f"  Struktur: {struktur['struktur']}")
            print(f"  Komponenten: {[k['term'] for k in struktur['komponenten']]}")

            # Funktion erstellen
            f = Funktion(test_case)
            print(f"  Funktionstyp: {type(f).__name__}")
            print(f"  Funktionsterm: {f.term()}")

            if hasattr(f, "faktoren"):
                print(f"  Faktoren: {[str(faktor) for faktor in f.faktoren]}")

            print()

        except Exception as e:
            print(f"  FEHLER: {e}")
            print()


if __name__ == "__main__":
    test_exponential_faktorisierung()
