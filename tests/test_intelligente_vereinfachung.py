#!/usr/bin/env python3
"""Testfälle für die intelligente Vereinfachungsstrategie"""

import os
import sys

import sympy as sp

# Füge src zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from schul_analysis import Funktion


def test_polynom_mit_parametern():
    """Test: Vereinfachung von Polynomen mit Parametern"""
    print("=== Test 1: Polynome mit Parametern ===")

    # Test 1: Einfaches quadratisches Polynom
    f1 = Funktion("a*x^2 + b*x + c")
    print(f"Original: {f1.term()}")
    print(f"Parameter: {[p.name for p in f1.parameter]}")

    # Erste Ableitung
    f1_abl = f1.ableitung()
    print(f"1. Ableitung: {f1_abl.term()}")
    print("Erwartet: 2*a*x + b (nicht ausmultipliziert)")

    # Zweite Ableitung
    f1_abl2 = f1.ableitung(2)
    print(f"2. Ableitung: {f1_abl2.term()}")
    print("Erwartet: 2*a")

    print()

    # Test 2: Komplexeres Polynom
    f2 = Funktion("(a+b)^2*x^4 + (a-b)*x^2 + c")
    print(f"Original: {f2.term()}")
    f2_abl = f2.ableitung()
    print(f"1. Ableitung: {f2_abl.term()}")
    print("Erwartet: Parameter sollten nicht ausmultipliziert werden")


def test_exponential_mit_parametern():
    """Test: Vereinfachung von Exponentialfunktionen mit Parametern"""
    print("\n=== Test 2: Exponentialfunktionen mit Parametern ===")

    # Test 1: exp(x) mit polynom
    f1 = Funktion("(x^2 + 4*x - 3)*exp(-x)")
    print(f"Original: {f1.term()}")
    f1_abl = f1.ableitung()
    print(f"1. Ableitung: {f1_abl.term()}")
    print("Erwartet: exp(-x) sollte ausgeklammert bleiben")

    # Test 2: Parameter im Exponent
    f2 = Funktion("exp(a*x + b)")
    print(f"Original: {f2.term()}")
    f2_abl = f2.ableitung()
    print(f"1. Ableitung: {f2_abl.term()}")
    print("Erwartet: a*exp(a*x + b)")

    print()

    # Test 3: Gemischte Funktion
    f3 = Funktion("(a*x^2 + b)*exp(c*x)")
    print(f"Original: {f3.term()}")
    f3_abl = f3.ableitung()
    print(f"1. Ableitung: {f3_abl.term()}")
    print("Erwartet: exp(c*x) sollte ausgeklammert sein")


def test_trigonometrisch_mit_parametern():
    """Test: Vereinfachung von trigonometrischen Funktionen mit Parametern"""
    print("\n=== Test 3: Trigonometrische Funktionen mit Parametern ===")

    # Test 1: sin(x) mit Polynom
    f1 = Funktion("(x^2 + a*x + b)*sin(x)")
    print(f"Original: {f1.term()}")
    f1_abl = f1.ableitung()
    print(f"1. Ableitung: {f1_abl.term()}")
    print("Erwartet: sin(x) und cos(x) Terme sollten gruppiert sein")

    # Test 2: Parameter im Argument
    f2 = Funktion("sin(a*x + b)")
    print(f"Original: {f2.term()}")
    f2_abl = f2.ableitung()
    print(f"1. Ableitung: {f2_abl.term()}")
    print("Erwartet: a*cos(a*x + b)")


def test_rationale_funktionen_mit_parametern():
    """Test: Vereinfachung von rationalen Funktionen mit Parametern"""
    print("\n=== Test 4: Rationale Funktionen mit Parametern ===")

    # Test 1: Einfache rationale Funktion
    f1 = Funktion("(a*x + b)/(c*x + d)")
    print(f"Original: {f1.term()}")
    f1_abl = f1.ableitung()
    print(f"1. Ableitung: {f1_abl.term()}")
    print("Erwartet: Zusammengefasster Bruch")

    # Test 2: Komplexere rationale Funktion
    f2 = Funktion("(x^2 + a*x + b)/(x^2 + c*x + d)")
    print(f"Original: {f2.term()}")
    f2_abl = f2.ableitung()
    print(f"1. Ableitung: {f2_abl.term()}")


def test_performance_vergleich():
    """Test: Performance-Vergleich zwischen alter und neuer Methode"""
    print("\n=== Test 5: Performance-Vergleich ===")

    import time

    # Test mit komplexem Ausdruck
    f = Funktion("(a+b+c)^4*x^6 + (a-b)^3*x^4 + (a+c)^2*x^2 + b")

    # Alte Methode (direkte Ableitung)
    start_time = time.time()
    for _ in range(10):
        abgeleitet_alt = sp.diff(f.term_sympy, f._variable_symbol)
    alt_zeit = time.time() - start_time

    # Neue Methode
    start_time = time.time()
    for _ in range(10):
        abgeleitet_neu = f.ableitung()
    neu_zeit = time.time() - start_time

    print(f"Alte Methode: {alt_zeit:.4f}s")
    print(f"Neue Methode: {neu_zeit:.4f}s")
    print(f"Overhead: {((neu_zeit - alt_zeit) / alt_zeit * 100):.1f}%")


def test_keine_parameter_fall():
    """Test: Normale Funktionen ohne Parameter sollten sich nicht verändern"""
    print("\n=== Test 6: Funktionen ohne Parameter ===")

    # Test 1: Einfache quadratische Funktion
    f1 = Funktion("x^2 + 4*x + 3")
    print(f"Original: {f1.term()}")
    f1_abl = f1.ableitung()
    print(f"1. Ableitung: {f1_abl.term()}")
    print("Erwartet: 2*x + 4 (normale Vereinfachung)")

    # Test 2: Exponentialfunktion ohne Parameter
    f2 = Funktion("exp(x) + x^2")
    print(f"Original: {f2.term()}")
    f2_abl = f2.ableitung()
    print(f"1. Ableitung: {f2_abl.term()}")


def test_parameter_substitution():
    """Test: Parameter-Substitution sollte weiterhin funktionieren"""
    print("\n=== Test 7: Parameter-Substitution ===")

    # Funktion mit Parametern
    f = Funktion("a*x^2 + b*x + c")

    # Parameter setzen
    f_konkret = f.setze_parameter(a=2, b=3, c=1)
    print(f"Original mit Parametern: {f.term()}")
    print(f"Mit eingesetzten Parametern: {f_konkret.term()}")
    print(f"1. Ableitung: {f_konkret.ableitung().term()}")

    # Test mit Auswertung
    wert = f_konkret(2)
    print(f"f(2) = {wert}")


if __name__ == "__main__":
    print("Teste intelligente Vereinfachungsstrategie für parametrisierte Ausdrücke")
    print("=" * 70)

    try:
        test_polynom_mit_parametern()
        test_exponential_mit_parametern()
        test_trigonometrisch_mit_parametern()
        test_rationale_funktionen_mit_parametern()
        test_performance_vergleich()
        test_keine_parameter_fall()
        test_parameter_substitution()

        print("\n✅ Alle Tests abgeschlossen!")

    except Exception as e:
        print(f"\n❌ Fehler bei der Ausführung: {e}")
        import traceback

        traceback.print_exc()
