#!/usr/bin/env python3
"""
Test-Skript für Edge-Cases der optimierten Nullstellenberechnung.

Testet:
1. Parameter-abhängige Funktionen
2. Komplexe trigonometrische Gleichungen
3. Grenzwert-Fälle und numerische Stabilität
4. Fehlerbehandlung bei ungültigen Eingaben
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis import Funktion


def test_parameter_abhängige_funktionen():
    """Testet Nullstellenberechnung mit Parametern."""
    print("=== Test Parameter-abhängige Funktionen ===")

    test_fälle = [
        ("a*x^2 + b*x + c", "Allgemeines quadratisches Polynom"),
        ("x^2 - 2*a*x + a^2", "Perfektes Quadrat"),
        ("(x-a)*(x-b)", "Linearfaktoren"),
        ("a*sin(x) + b*cos(x)", "Trigonometrisch mit Parametern"),
    ]

    for term, beschreibung in test_fälle:
        print(f"\n{beschreibung}: {term}")
        try:
            f = Funktion(term)
            nullstellen = f.nullstellen()
            print(f"  Nullstellen: {len(nullstellen)} gefunden")
            for ns in nullstellen[:3]:  # Zeige max. 3
                print(f"    {ns}")

            # Teste Hybrid-API
            hybrid = f.nullstellen_mit_wiederholungen()
            print(f"  Hybrid: {len(hybrid)} Einträge")

        except Exception as e:
            print(f"  Fehler: {type(e).__name__}: {e}")


def test_komplexe_trigonometrische_gleichungen():
    """Testet komplexe trigonometrische Gleichungen."""
    print("\n=== Test Komplexe Trigonometrische Gleichungen ===")

    test_fälle = [
        ("sin(x) + cos(x)", "Grundform"),
        ("sin(x) + cos(x) + tan(x)", "Mit Tangens"),
        ("2*sin(x) - 3*cos(x)", "Mit Koeffizienten"),
        ("sin(x) * cos(x)", "Produkt"),
        ("sin^2(x) - cos^2(x)", "Quadratische Form"),
    ]

    for term, beschreibung in test_fälle:
        print(f"\n{beschreibung}: {term}")
        try:
            f = Funktion(term)
            nullstellen = f.nullstellen()
            print(f"  Nullstellen: {len(nullstellen)} gefunden")
            for ns in nullstellen[:2]:  # Zeige max. 2
                print(f"    {ns}")

        except Exception as e:
            print(f"  Fehler: {type(e).__name__}: {e}")


def test_grenzwert_fälle():
    """Testet Grenzwert-Fälle und numerische Stabilität."""
    print("\n=== Test Grenzwert-Fälle ===")

    test_fälle = [
        ("x^100 - 1", "Hochgradiges Polynom"),
        ("(x-1)^50", "Hohe Vielfachheit"),
        ("x^2 + 1", "Keine reellen Nullstellen"),
        ("exp(x)", "Keine Nullstellen"),
        ("1/x", "Polstelle"),
        ("sin(1/x)", "Oszillation bei x=0"),
    ]

    for term, beschreibung in test_fälle:
        print(f"\n{beschreibung}: {term}")
        try:
            f = Funktion(term)
            nullstellen = f.nullstellen()
            print(f"  Nullstellen: {len(nullstellen)} gefunden")
            for ns in nullstellen[:2]:
                print(f"    {ns}")

        except Exception as e:
            print(f"  Fehler: {type(e).__name__}: {e}")


def test_fehlerbehandlung():
    """Testet die verbesserte Fehlerbehandlung."""
    print("\n=== Test Fehlerbehandlung ===")

    test_fälle = [
        ("", "Leere Eingabe"),
        ("invalid_syntax", "Ungültige Syntax"),
        ("x + ", "Unvollständiger Ausdruck"),
        ("sqrt(-1)", "Komplexe Zahl"),
        ("log(0)", "Ungültiger Logarithmus"),
        ("1/0", "Division durch Null"),
    ]

    for term, beschreibung in test_fälle:
        print(f"\n{beschreibung}: '{term}'")
        try:
            f = Funktion(term)
            nullstellen = f.nullstellen()
            print(f"  Unerwarteter Erfolg: {nullstellen}")

        except Exception as e:
            print(f"  Erwarteter Fehler: {type(e).__name__}")
            print(f"  Nachricht: {e}")


def test_type_consistency_edge_cases():
    """Testet Type-Consistency in Edge-Fällen."""
    print("\n=== Test Type-Consistency Edge Cases ===")

    # Teste verschiedene Kombinationen
    test_fälle = [
        ("x^2 - 4", "Einfach"),
        ("(x-1)^3 * (x-2)^2", "Mehrere Vielfachheiten"),
        ("x^2 * sin(x)", "Gemischte Typen"),
        ("exp(x) - 1", "Exponentiell"),
    ]

    for term, beschreibung in test_fälle:
        print(f"\n{beschreibung}: {term}")
        try:
            f = Funktion(term)

            # Teste beide APIs
            strukturiert = f.nullstellen()
            hybrid = f.nullstellen_mit_wiederholungen()

            # Type-Checks
            all_have_x = all(hasattr(ns, "x") for ns in strukturiert)
            all_have_multiplicity = all(
                hasattr(ns, "multiplicitaet") for ns in strukturiert
            )

            # Konsistenz-Checks
            multiplicity_sum = sum(ns.multiplicitaet for ns in strukturiert)
            hybrid_length = len(hybrid)

            print(f"  Strukturiert: {len(strukturiert)} Nullstellen")
            print(f"  Hybrid: {hybrid_length} Einträge")
            print(
                f"  Type-Safety: x={all_have_x}, multiplicity={all_have_multiplicity}"
            )
            print(f"  Konsistenz: {multiplicity_sum == hybrid_length}")

        except Exception as e:
            print(f"  Fehler: {type(e).__name__}: {e}")


def test_performance_with_caching():
    """Testet Performance-Verbesserungen durch Caching."""
    print("\n=== Test Performance mit Caching ===")

    import time

    # Komplexe Funktion mit wiederholten Berechnungen
    f = Funktion("(x-1)^5 * (x-2)^3 * (x-3)^2 * sin(x)")

    print(f"Funktion: {f.term()}")
    print("Führe 5 Berechnungen durch...")

    times = []
    for i in range(5):
        start_time = time.time()
        nullstellen = f.nullstellen()
        end_time = time.time()
        times.append(end_time - start_time)
        print(f"  Durchlauf {i + 1}: {times[-1]:.4f}s, {len(nullstellen)} Nullstellen")

    avg_time = sum(times) / len(times)
    improvement = ((times[0] - times[-1]) / times[0] * 100) if times[0] > 0 else 0

    print(f"\nDurchschnitt: {avg_time:.4f}s")
    print(f"Cache-Verbesserung: {improvement:.1f}%")


if __name__ == "__main__":
    print("Teste Edge-Cases für die optimierte Nullstellenberechnung...")

    try:
        test_parameter_abhängige_funktionen()
        test_komplexe_trigonometrische_gleichungen()
        test_grenzwert_fälle()
        test_fehlerbehandlung()
        test_type_consistency_edge_cases()
        test_performance_with_caching()
        print("\n=== Alle Edge-Case-Tests abgeschlossen ===")
    except Exception as e:
        print(f"Fehler beim Testen: {e}")
        import traceback

        traceback.print_exc()
