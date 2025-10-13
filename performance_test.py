#!/usr/bin/env python3
"""
Performance-Test für das Schul-Analysis Framework

Dieses Skript testet die Performance-Verbesserungen durch Caching
und vergleicht die Ausführungszeiten vor und nach der Optimierung.
"""

import time
import statistics
from typing import List, Tuple
from src.schul_mathematik.analysis.funktion import Funktion


def zeit_messen(funktion, *args, **kwargs):
    """Misst die Ausführungszeit einer Funktion."""
    start = time.perf_counter()
    ergebnis = funktion(*args, **kwargs)
    ende = time.perf_counter()
    return ergebnis, ende - start


def performance_test_funktionen_erstellung() -> List[Tuple[str, float]]:
    """Testet die Performance bei der Erstellung verschiedener Funktionstypen."""
    print("=== Test: Funktionserstellung ===")

    test_funktionen = [
        "x^2 - 4x + 3",
        "x^3 - 3x^2 + 2x - 1",
        "sin(x) + cos(x)",
        "exp(x) + x^2",
        "(x^2 + 1)/(x - 1)",
        "a*x^2 + b*x + c",
        "2*x^3 - 5*x^2 + 3*x - 1",
        "log(x) + sqrt(x)",
    ]

    zeiten = []
    for term in test_funktionen:
        _, zeit = zeit_messen(Funktion, term)
        zeiten.append(zeit)
        print(f"Funktion('{term}'):\t{zeit:.4f}s")

    durchschnitt = statistics.mean(zeiten)
    print(f"Durchschnittszeit Funktionserstellung: {durchschnitt:.4f}s")
    print()

    return [("Funktionserstellung", durchschnitt)]


def performance_test_ableitungen() -> List[Tuple[str, float]]:
    """Testet die Performance bei Ableitungsberechnungen."""
    print("=== Test: Ableitungen ===")

    # Erstelle Testfunktionen
    f1 = Funktion("x^4 - 3*x^3 + 2*x^2 - x + 1")
    f2 = Funktion("sin(x) * exp(x)")
    f3 = Funktion("(x^2 + 1)/(x - 2)")
    f4 = Funktion("a*x^3 + b*x^2 + c*x + d")

    tests = [
        (f1.ableitung, 1, "f1.ableitung(1)"),
        (f1.ableitung, 2, "f1.ableitung(2)"),
        (f1.ableitung, 3, "f1.ableitung(3)"),
        (f2.ableitung, 1, "f2.ableitung(1)"),
        (f2.ableitung, 2, "f2.ableitung(2)"),
        (f3.ableitung, 1, "f3.ableitung(1)"),
        (f4.ableitung, 1, "f4.ableitung(1)"),
        (f4.ableitung, 2, "f4.ableitung(2)"),
    ]

    zeiten = []
    for ableitung_func, ordnung, beschreibung in tests:
        _, zeit = zeit_messen(ableitung_func, ordnung)
        zeiten.append(zeit)
        print(f"{beschreibung}:\t{zeit:.4f}s")

    durchschnitt = statistics.mean(zeiten)
    print(f"Durchschnittszeit Ableitungen: {durchschnitt:.4f}s")
    print()

    return [("Ableitungen", durchschnitt)]


def performance_test_nullstellen() -> List[Tuple[str, float]]:
    """Testet die Performance bei Nullstellenberechnungen."""
    print("=== Test: Nullstellen ===")

    test_funktionen = [
        ("x^2 - 4", "Einfach quadratisch"),
        ("x^3 - 6*x^2 + 11*x - 6", "Kubisch"),
        ("x^4 - 10*x^3 + 35*x^2 - 50*x + 24", "Quartisch"),
        ("(x^2 - 4)*(x^2 - 9)", "Produkt"),
        ("x^2 + 1", "Komplex"),
        ("a*x^2 + b*x + c", "Parametrisiert"),
    ]

    zeiten = []
    for term, beschreibung in test_funktionen:
        f = Funktion(term)
        _, zeit = zeit_messen(lambda: f.nullstellen)
        zeiten.append(zeit)
        print(f"{beschreibung}:\t{zeit:.4f}s")

    durchschnitt = statistics.mean(zeiten)
    print(f"Durchschnittszeit Nullstellen: {durchschnitt:.4f}s")
    print()

    return [("Nullstellen", durchschnitt)]


def performance_test_extrema() -> List[Tuple[str, float]]:
    """Testet die Performance bei Extremstellenberechnungen."""
    print("=== Test: Extrema ===")

    test_funktionen = [
        ("x^3 - 3*x^2 + 2", "Kubisch"),
        ("x^4 - 8*x^3 + 18*x^2 - 8", "Quartisch"),
        ("sin(x) + 0.5*x", "Trigonometrisch"),
        ("exp(-x^2)", "Exponentiell"),
        ("a*x^3 + b*x^2 + c*x + d", "Parametrisiert"),
    ]

    zeiten = []
    for term, beschreibung in test_funktionen:
        f = Funktion(term)
        _, zeit = zeit_messen(lambda: f.extrema())
        zeiten.append(zeit)
        print(f"{beschreibung}:\t{zeit:.4f}s")

    durchschnitt = statistics.mean(zeiten)
    print(f"Durchschnittszeit Extrema: {durchschnitt:.4f}s")
    print()

    return [("Extrema", durchschnitt)]


def performance_test_wendepunkte() -> List[Tuple[str, float]]:
    """Testet die Performance bei Wendepunktberechnungen."""
    print("=== Test: Wendepunkte ===")

    test_funktionen = [
        ("x^3 - 3*x^2 + 2", "Kubisch"),
        ("x^4 - 8*x^3 + 18*x^2 - 8", "Quartisch"),
        ("x^5 - 5*x^4 + 10*x^3 - 10*x^2 + 5*x - 1", "Quintisch"),
        ("sin(x)", "Trigonometrisch"),
        ("a*x^4 + b*x^3 + c*x^2 + d*x + e", "Parametrisiert"),
    ]

    zeiten = []
    for term, beschreibung in test_funktionen:
        f = Funktion(term)
        _, zeit = zeit_messen(lambda: f.wendepunkte())
        zeiten.append(zeit)
        print(f"{beschreibung}:\t{zeit:.4f}s")

    durchschnitt = statistics.mean(zeiten)
    print(f"Durchschnittszeit Wendepunkte: {durchschnitt:.4f}s")
    print()

    return [("Wendepunkte", durchschnitt)]


def performance_test_caching_effekt() -> List[Tuple[str, float]]:
    """Testet den Caching-Effekt bei wiederholten Berechnungen."""
    print("=== Test: Caching-Effekt ===")

    f = Funktion("x^5 - 3*x^4 + 2*x^3 - 5*x^2 + x - 1")

    # Erste Berechnung (Cache kalt)
    start = time.perf_counter()
    ableitung1 = f.ableitung(1)
    zeit1 = time.perf_counter() - start

    # Zweite Berechnung (sollte aus Cache kommen)
    start = time.perf_counter()
    ableitung2 = f.ableitung(1)
    zeit2 = time.perf_counter() - start

    # Dritte Berechnung (sollte aus Cache kommen)
    start = time.perf_counter()
    ableitung3 = f.ableitung(1)
    zeit3 = time.perf_counter() - start

    print(f"Erste Ableitung (kalt):\t{zeit1:.4f}s")
    print(f"Zweite Ableitung (warm):\t{zeit2:.4f}s")
    print(f"Dritte Ableitung (warm):\t{zeit3:.4f}s")

    if zeit1 > 0:
        beschleunigung = (zeit1 - zeit2) / zeit1 * 100
        print(f"Beschleunigung durch Cache: {beschleunigung:.1f}%")

    # Teste verschiedene Ableitungsordnungen
    start = time.perf_counter()
    for i in range(1, 6):
        f.ableitung(i)
    zeit_alle = time.perf_counter() - start

    print(f"Alle Ableitungen (1-5): {zeit_alle:.4f}s")
    print()

    return [("Caching-Effekt", zeit2)]


def test_cache_groesse():
    """Testet die Cache-Größe und Hit-Rate."""
    print("=== Test: Cache-Statistiken ===")

    # Erstelle viele verschiedene Funktionen
    funktionen = []
    for i in range(10):
        f = Funktion(f"x^{i + 2} - {i + 1}*x^{i + 1} + {i}*x")
        funktionen.append(f)

    # Berechne Ableitungen für alle Funktionen
    start = time.perf_counter()
    for f in funktionen:
        for ordnung in range(1, 4):
            f.ableitung(ordnung)
    zeit_erste_runde = time.perf_counter() - start

    # Wiederhole die Berechnungen (sollte aus Cache kommen)
    start = time.perf_counter()
    for f in funktionen:
        for ordnung in range(1, 4):
            f.ableitung(ordnung)
    zeit_zweite_runde = time.perf_counter() - start

    print(f"Erste Runde (Cache kalt): {zeit_erste_runde:.4f}s")
    print(f"Zweite Runde (Cache warm): {zeit_zweite_runde:.4f}s")

    if zeit_erste_runde > 0:
        beschleunigung = (zeit_erste_runde - zeit_zweite_runde) / zeit_erste_runde * 100
        print(f"Cache-Beschleunigung: {beschleunigung:.1f}%")

    print()


def main():
    """Führt alle Performance-Tests durch."""
    print("Schul-Analysis Framework - Performance-Test")
    print("=" * 50)
    print()

    # Führe alle Tests durch
    alle_ergebnisse = []

    alle_ergebnisse.extend(performance_test_funktionen_erstellung())
    alle_ergebnisse.extend(performance_test_ableitungen())
    alle_ergebnisse.extend(performance_test_nullstellen())
    alle_ergebnisse.extend(performance_test_extrema())
    alle_ergebnisse.extend(performance_test_wendepunkte())
    alle_ergebnisse.extend(performance_test_caching_effekt())

    # Cache-Statistiken
    test_cache_groesse()

    # Zusammenfassung
    print("=== Zusammenfassung ===")
    for name, zeit in alle_ergebnisse:
        print(f"{name}: {zeit:.4f}s")

    print()
    print("Performance-Test abgeschlossen!")


if __name__ == "__main__":
    main()
