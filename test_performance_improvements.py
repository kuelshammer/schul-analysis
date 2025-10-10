#!/usr/bin/env python3
"""
Performance-Test für die neuen Optimierungen der Nullstellenberechnung.

Testet:
1. Caching-Effizienz bei wiederholten Berechnungen
2. Optimierung der Duplikatentfernung
3. Verbesserte Fehlerbehandlung
"""

import sys
import time
from functools import lru_cache

sys.path.insert(0, "src")

from schul_mathematik.analysis import Funktion


def test_caching_efficiency():
    """Testet die Caching-Effizienz bei wiederholten Berechnungen."""
    print("=== Test Caching-Effizienz ===")

    # Test-Funktion mit mehrfachen Nullstellen
    f = Funktion("(x-1)^3 * (x-2)^2 * (x-3)^4")

    print(f"Funktion: {f.term()}")
    print("Erste Berechnung (ohne Cache)...")
    start_time = time.time()
    nullstellen1 = f.nullstellen()
    first_time = time.time() - start_time
    print(f"Ergebnis: {nullstellen1}")
    print(f"Zeit: {first_time:.4f}s")

    print("\nZweite Berechnung (mit Cache)...")
    start_time = time.time()
    nullstellen2 = f.nullstellen()
    second_time = time.time() - start_time
    print(f"Ergebnis: {nullstellen2}")
    print(f"Zeit: {second_time:.4f}s")

    print(
        f"\nPerformance-Verbesserung: {((first_time - second_time) / first_time * 100):.1f}%"
    )
    print(f"Ergebnisse identisch: {nullstellen1 == nullstellen2}")


def test_duplicate_removal():
    """Testet die optimierte Duplikatentfernung."""
    print("\n=== Test Optimierung Duplikatentfernung ===")

    # Erstelle eine Test-Liste mit vielen Duplikaten
    test_liste = [1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5] * 100

    print(f"Testliste: {len(test_liste)} Elemente")

    # Alte Methode (O(n²))
    start_time = time.time()
    alt_ergebnis = []
    for item in test_liste:
        if item not in alt_ergebnis:
            alt_ergebnis.append(item)
    alt_zeit = time.time() - start_time

    # Neue Methode (set-basiert)
    start_time = time.time()
    neu_ergebnis = []
    gesehen = set()
    for item in test_liste:
        if item not in gesehen:
            gesehen.add(item)
            neu_ergebnis.append(item)
    neu_zeit = time.time() - start_time

    print(f"Alte Methode: {alt_zeit:.4f}s, Ergebnis: {len(alt_ergebnis)} Elemente")
    print(f"Neue Methode: {neu_zeit:.4f}s, Ergebnis: {len(neu_ergebnis)} Elemente")
    print(f"Performance-Verbesserung: {((alt_zeit - neu_zeit) / alt_zeit * 100):.1f}%")
    print(f"Ergebnisse identisch: {alt_ergebnis == neu_ergebnis}")


def test_error_handling():
    """Testet die verbesserte Fehlerbehandlung."""
    print("\n=== Test Verbesserte Fehlerbehandlung ===")

    # Test 1: Ungültige Funktion
    print("Test 1: Ungültige Funktion")
    try:
        f = Funktion("invalid_function_syntax")
        nullstellen = f.nullstellen()
        print(f"Ergebnis: {nullstellen}")
    except Exception as e:
        print(f"Fehler erkannt: {type(e).__name__}: {e}")

    # Test 2: Komplexe trigonometrische Funktion
    print("\nTest 2: Komplexe trigonometrische Funktion")
    try:
        f = Funktion("sin(x) + cos(x) + tan(x)")
        nullstellen = f.nullstellen()
        print(f"Ergebnis: {len(nullstellen)} Nullstellen gefunden")
        for ns in nullstellen[:2]:  # Zeige nur die ersten beiden
            print(f"  {ns}")
    except Exception as e:
        print(f"Fehler: {type(e).__name__}: {e}")


def test_type_consistency():
    """Testet die Type-Consistency-Verbesserungen."""
    print("\n=== Test Type-Consistency ===")

    # Test verschiedene Funktionstypen
    test_funktionen = [
        ("x^2 - 4", "Einfaches Polynom"),
        ("(x-1)^2 * (x-2)", "Polynom mit Vielfachheit"),
        ("sin(x) + cos(x)", "Trigonometrische Funktion"),
        ("x^2 * sin(x)", "Produktfunktion"),
        ("exp(x) + 1", "Exponentialfunktion"),
    ]

    for term, beschreibung in test_funktionen:
        try:
            f = Funktion(term)
            nullstellen = f.nullstellen()
            hybrid = f.nullstellen_mit_wiederholungen()

            print(f"\n{beschreibung}: {term}")
            print(f"  Strukturiert: {len(nullstellen)} Nullstellen")
            print(f"  Hybrid: {len(hybrid)} Nullstellen")

            # Prüfe Type-Consistency
            all_dataclasses = all(hasattr(ns, "x") for ns in nullstellen)
            print(f"  Alle Datenklassen: {all_dataclasses}")

            # Prüfe Vielfachheit
            multiplicity_sum = sum(ns.multiplicitaet for ns in nullstellen)
            hybrid_length = len(hybrid)
            print(f"  Vielfachheit konsistent: {multiplicity_sum == hybrid_length}")

        except Exception as e:
            print(f"  Fehler: {type(e).__name__}: {e}")


def benchmark_large_polynomials():
    """Benchmark für große Polynome."""
    print("\n=== Benchmark für große Polynome ===")

    # Erstelle ein Polynom hohen Grades
    hochgradiges_polynom = "(x-1)*(x-2)*(x-3)*(x-4)*(x-5)*(x-6)*(x-7)*(x-8)"
    f = Funktion(hochgradiges_polynom)

    print(f"Polynom: {hochgradiges_polynom}")

    # Mehrere Berechnungen für Cache-Test
    print("Führe 10 Berechnungen durch...")
    times = []
    for i in range(10):
        start_time = time.time()
        nullstellen = f.nullstellen()
        end_time = time.time()
        times.append(end_time - start_time)
        print(f"  Durchlauf {i + 1}: {times[-1]:.4f}s")

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print(f"\nDurchschnittszeit: {avg_time:.4f}s")
    print(f"Schnellste: {min_time:.4f}s")
    print(f"Langsamste: {max_time:.4f}s")
    print(f"Cache-Effekt: {((max_time - min_time) / max_time * 100):.1f}% Verbesserung")


if __name__ == "__main__":
    print("Performance-Test für die optimierte Nullstellenberechnung...")

    try:
        test_caching_efficiency()
        test_duplicate_removal()
        test_error_handling()
        test_type_consistency()
        benchmark_large_polynomials()
        print("\n=== Alle Performance-Tests abgeschlossen ===")
    except Exception as e:
        print(f"Fehler beim Testen: {e}")
        import traceback

        traceback.print_exc()
