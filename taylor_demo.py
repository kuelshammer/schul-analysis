#!/usr/bin/env python3
"""
Educational demo for Taylor polynomials
Shows how to use Taylor polynomials for function approximation
"""

import numpy as np
import math
from src.schul_analysis import *


def demo_taylor_exponential():
    """Demo: Taylor polynomials for e^x approximation"""
    print("=== Demo: Taylorpolynome für e^x ===\n")

    # Erstelle eine Funktion, die e^x approximiert
    # Um x=0: e^x ≈ 1 + x + x²/2! + x³/3! + ...

    print("Taylorpolynome für e^x um x=0:")
    print("e^x ≈ 1 + x + x²/2 + x³/6 + x⁴/24 + ...\n")

    # Verschiedene Grade
    for grad in [1, 2, 3, 4]:
        # Erstelle das Taylorpolynom manuell
        koeffizienten = []
        for k in range(grad + 1):
            koeffizienten.append(1 / math.factorial(k))

        taylor_func = GanzrationaleFunktion(koeffizienten)
        taylor = Taylorpolynom(taylor_func, entwicklungspunkt=0, grad=grad)

        print(f"{grad}. Taylorpolynom: {taylor.term()}")

        # Werte an verschiedenen Stellen vergleichen
        print("  Vergleiche mit e^x:")
        for x in [0, 0.5, 1, 1.5]:
            taylor_wert = taylor.wert(x)
            exakt = math.exp(x)
            fehler = abs(taylor_wert - exakt)
            print(
                f"    x={x}: Taylor={taylor_wert:.4f}, e^x={exakt:.4f}, Fehler={fehler:.4f}"
            )
        print()


def demo_taylor_sin():
    """Demo: Taylor polynomials for sin(x) approximation"""
    print("=== Demo: Taylorpolynome für sin(x) ===\n")

    print("Taylorpolynome für sin(x) um x=0:")
    print("sin(x) ≈ x - x³/3! + x⁵/5! - x⁷/7! + ...\n")

    # Verschiedene Grade
    for grad in [3, 5, 7]:
        # Erstelle das Taylorpolynom manuell für sin(x)
        if grad == 3:
            koeff = [0, 1, 0, -1 / 6]  # x - x³/6
        elif grad == 5:
            koeff = [0, 1, 0, -1 / 6, 0, 1 / 120]  # x - x³/6 + x⁵/120
        else:  # grad == 7
            koeff = [
                0,
                1,
                0,
                -1 / 6,
                0,
                1 / 120,
                0,
                -1 / 5040,
            ]  # x - x³/6 + x⁵/120 - x⁷/5040

        taylor_func = GanzrationaleFunktion(koeff)
        taylor = Taylorpolynom(taylor_func, entwicklungspunkt=0, grad=grad)

        print(f"{grad}. Taylorpolynom: {taylor.term()}")

        # Werte an verschiedenen Stellen vergleichen
        print("  Vergleiche mit sin(x):")
        for x in [0, np.pi / 6, np.pi / 4, np.pi / 3]:
            taylor_wert = taylor.wert(x)
            exakt = math.sin(x)
            fehler = abs(taylor_wert - exakt)
            print(
                f"    x={x:.3f}: Taylor={taylor_wert:.4f}, sin(x)={exakt:.4f}, Fehler={fehler:.4f}"
            )
        print()


def demo_funktions_operatoren():
    """Demo: Using functional operators for Taylor polynomials"""
    print("=== Demo: Funktionale Operatoren ===\n")

    # Polynomfunktion erstellen
    f = GanzrationaleFunktion([1, 2, 1])  # x² + 2x + 1

    print(f"Funktion: f(x) = {f.term()}")

    # Taylorpolynom um x=1
    taylor = Taylor(f, entwicklungspunkt=1, grad=2)
    print(f"Taylorpolynom um x=1: {taylor.term()}")

    # Koeffizienten anzeigen
    koeff = TaylorKoeffizienten(f, entwicklungspunkt=1, grad=2)
    print(f"Taylor-Koeffizienten: {koeff}")

    # MacLaurin-Polynom (um x=0)
    maclaurin = MacLaurin(f, grad=2)
    print(f"MacLaurin-Polynom: {maclaurin.term()}")

    # Restglied berechnen
    for x in [0.5, 1, 1.5]:
        taylor_obj = Taylorpolynom(f, entwicklungspunkt=0, grad=2)
        restglied = taylor_obj.restglied_lagrange(x)
        taylor_wert = maclaurin.wert(x)
        exakt = f.wert(x)
        print(
            f"  Bei x={x}: Taylor={taylor_wert:.3f}, Restglied={restglied:.3f}, Summe={taylor_wert + restglied:.3f} ≈ {exakt:.3f}"
        )


def demo_approximationsqualitaet():
    """Demo: Approximation quality analysis"""
    print("\n=== Demo: Approximationsgüte ===\n")

    # Quadratische Funktion
    f = GanzrationaleFunktion([1, -2, 1])  # x² - 2x + 1

    print(f"Funktion: f(x) = {f.term()}")
    print("Entwicklung um x=1\n")

    # Verschiedene Grade
    for grad in [0, 1, 2]:
        taylor = Taylorpolynom(f, entwicklungspunkt=1, grad=grad)

        print(f"{grad}. Ordnung: {taylor.term()}")

        # Fehler an verschiedenen Stellen
        print("  Approximationsfehler:")
        for x in [0, 0.5, 1, 1.5, 2]:
            exakt = f.wert(x)
            taylor_wert = taylor.wert(x)
            fehler = abs(exakt - taylor_wert)
            print(f"    x={x}: |{exakt:.3f} - {taylor_wert:.3f}| = {fehler:.6f}")
        print()


def run_demo():
    """Run all Taylor polynomial demos"""
    print("Taylorpolynom-Demonstration")
    print("=" * 50)

    demo_taylor_exponential()
    demo_taylor_sin()
    demo_funktions_operatoren()
    demo_approximationsqualitaet()

    print("=" * 50)
    print("Demo abgeschlossen!")
    print("\nTipps für die Nutzung:")
    print("1. Taylor(f, x0, n) - Taylorpolynom n-ter Ordnung um x0")
    print("2. MacLaurin(f, n) - Taylorpolynom um x=0")
    print("3. TaylorKoeffizienten(f, x0, n) - Koeffizienten anzeigen")
    print("4. Restglied(f, x, x0, n) - Fehler abschätzen")


if __name__ == "__main__":
    run_demo()
