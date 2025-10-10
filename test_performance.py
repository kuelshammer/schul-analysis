#!/usr/bin/env python3
"""
Performance-Vergleich: Alte vs. neue parametrische Methoden.
"""

import sys
import time

sys.path.insert(0, "src")

from schul_mathematik.analysis.funktion import Funktion


def performance_vergleich():
    """Vergleicht die Performance zwischen alten und neuen Methoden."""

    print("⚡ Performance-Vergleich: Alte vs. Neue Methoden\n")

    test_funktionen = [
        "x^2 - (a+b)*x + a*b",
        "a*x^2 + b*x + c",
        "x^3 + a*x",
        "a*x^3 + b*x^2 + c*x + d",
    ]

    for term in test_funktionen:
        print(f"📊 Funktion: {term}")

        f = Funktion(term)

        # Alte Methoden
        start_time = time.time()

        # Teste alte Methoden (wenn verfügbar)
        try:
            if hasattr(f, "_nullstellen_parametrisch_fallback"):
                _ = f._nullstellen_parametrisch_fallback()
            alte_nullstellen_zeit = time.time() - start_time
        except:
            alte_nullstellen_zeit = float("inf")

        start_time = time.time()
        try:
            if hasattr(f, "_extremstellen_parametrisch_fallback"):
                _ = f._extremstellen_parametrisch_fallback()
            alte_extremstellen_zeit = time.time() - start_time
        except:
            alte_extremstellen_zeit = float("inf")

        # Neue Methoden
        start_time = time.time()
        try:
            _ = f.nullstellen_optimiert()
            neue_nullstellen_zeit = time.time() - start_time
        except:
            neue_nullstellen_zeit = float("inf")

        start_time = time.time()
        try:
            _ = f.extremstellen_optimiert()
            neue_extremstellen_zeit = time.time() - start_time
        except:
            neue_extremstellen_zeit = float("inf")

        # Vergleiche Ergebnisse
        print(
            f"   Nullstellen - Alt: {alte_nullstellen_zeit:.4f}s, Neu: {neue_nullstellen_zeit:.4f}s"
        )
        if neue_nullstellen_zeit < alte_nullstellen_zeit:
            print(
                f"   ✅ Neue Methode {alte_nullstellen_zeit / neue_nullstellen_zeit:.1f}x schneller"
            )
        elif alte_nullstellen_zeit < neue_nullstellen_zeit:
            print(
                f"   ⚠️  Alte Methode {neue_nullstellen_zeit / alte_nullstellen_zeit:.1f}x schneller"
            )
        else:
            print(f"   ➖️  Gleiche Performance")

        print(
            f"   Extremstellen - Alt: {alte_extremstellen_zeit:.4f}s, Neu: {neue_extremstellen_zeit:.4f}s"
        )
        if neue_extremstellen_zeit < alte_extremstellen_zeit:
            print(
                f"   ✅ Neue Methode {alte_extremstellen_zeit / neue_extremstellen_zeit:.1f}x schneller"
            )
        elif alte_extremstellen_zeit < neue_extremstellen_zeit:
            print(
                f"   ⚠️  Alte Methode {neue_extremstellen_zeit / alte_extremstellen_zeit:.1f}x schneller"
            )
        else:
            print(f"   ➖️  Gleiche Performance")

        print()


if __name__ == "__main__":
    performance_vergleich()
