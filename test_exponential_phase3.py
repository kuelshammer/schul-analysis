#!/usr/bin/env python3
"""
Test script for Phase 3: Exponential-rationale Funktionen
"""

from schul_analysis import (
    ExponentialRationaleFunktion,
    GebrochenRationaleFunktion,
)


def test_exponential_rationale_funktion():
    """Testet die ExponentialRationaleFunktion Klasse"""
    print("=== Test ExponentialRationaleFunktion ===\n")

    # Test 1: Einfache Funktion f(x) = (e^x + 1)/(e^x - 1)
    print("Test 1: f(x) = (e^x + 1)/(e^x - 1)")
    f1 = ExponentialRationaleFunktion("(exp(x)+1)/(exp(x)-1)", exponent_param=1.0)

    print(f"  Term: {f1.term()}")
    print(f"  LaTeX: {f1.term_latex()}")

    # Teste mit x=1 (keine Polstelle)
    try:
        print(f"  Wert bei x=1: {f1(1)}")
    except ValueError as e:
        print(f"  Wert bei x=1: Fehler: {e}")

    # Teste mit x=0 (erwartete Polstelle)
    try:
        print(f"  Wert bei x=0: {f1(0)}")
    except ValueError as e:
        print(f"  Wert bei x=0: Fehler (erwartet): {e}")

    # Test 2: Zerlegung
    print("\nTest 2: Zerlegung")
    s1 = f1.schmiegkurve()
    r1 = f1.stoerfunktion()

    print(f"  Schmiegkurve: {s1.term()}")
    print(f"  Störfunktion: {r1.term()}")
    print(f"  Validierung: {'✅' if f1.validiere_zerlegung() else '❌'}")

    # Test 3: Erklärung der Transformation
    print("\nTest 3: Transformationserklärung")
    erklaerung = f1.erkläre_transformation()
    print(f"  Substitution: {erklaerung['substitution']}")
    print(f"  Transformierte Funktion: {erklaerung['transformierte_funktion']}")

    for schritt in erklaerung["schritte"]:
        print(f"  - {schritt['titel']}")

    # Test 4: Asymptotisches Verhalten
    print("\nTest 4: Asymptotisches Verhalten")
    verhalten = f1.analysiere_asymptotisches_verhalten()
    print(f"  Parameter: {verhalten['parameter']}")

    for key, val in verhalten["verhalten"].items():
        print(f"  {key}: {val['beschreibung']}")

    # Test 5: Komplexere Funktion f(x) = (e^{2x} + x*e^x + 1)/(e^{2x} - 1)
    print("\nTest 5: Komplexere Funktion f(x) = (e^{2x} + x*e^x + 1)/(e^{2x} - 1)")
    f2 = ExponentialRationaleFunktion(
        "(exp(2*x)+x*exp(x)+1)/(exp(2*x)-1)", exponent_param=2.0
    )

    print(f"  Term: {f2.term()}")

    # Teste mit x=1 (keine Polstelle)
    try:
        print(f"  Wert bei x=1: {f2(1)}")
    except ValueError as e:
        print(f"  Wert bei x=1: Fehler: {e}")

    # Teste mit x=0 (mögliche Polstelle)
    try:
        print(f"  Wert bei x=0: {f2(0)}")
    except ValueError as e:
        print(f"  Wert bei x=0: Fehler: {e}")

    s2 = f2.schmiegkurve()
    r2 = f2.stoerfunktion()
    print(f"  Schmiegkurve: {s2.term()}")
    print(f"  Störfunktion: {r2.term()}")
    print(f"  Validierung: {'✅' if f2.validiere_zerlegung() else '❌'}")

    print("\n=== Test abgeschlossen ===")


def test_vergleich_mit_rational():
    """Vergleicht exponential-rationale mit rationalen Funktionen"""
    print("\n=== Vergleich mit rationalen Funktionen ===\n")

    # Rationale Funktion: g(u) = (u^2 + 1)/(u - 1)
    g_rational = GebrochenRationaleFunktion("x^2+1", "x-1")

    # Exponential-rationale Funktion: f(x) = (e^{2x} + 1)/(e^x - 1)
    f_exp = ExponentialRationaleFunktion("(exp(2*x)+1)/(exp(x)-1)", exponent_param=1.0)

    print(f"Rationale Funktion: g(x) = {g_rational.term()}")
    print(f"Exponential-rationale: f(x) = {f_exp.term()}")

    # Bei x=0: u = e^0 = 1
    print("\nBei x=0 (u=e^0=1):")
    try:
        print(f"  g(1) = {g_rational(1)}")
    except Exception as e:
        print(f"  g(1) = Fehler (erwartet): {e}")

    try:
        print(f"  f(0) = {f_exp(0)}")
    except ValueError as e:
        print(f"  f(0) = Fehler (erwartet): {e}")

    # Bei x=1: u = e^1 ≈ 2.718
    u_val = 2.71828
    print(f"\nBei x=1 (u≈{u_val}):")
    print(f"  g({u_val}) ≈ {g_rational(u_val)}")
    print(f"  f(1) ≈ {f_exp(1)}")

    print("\n=== Vergleich abgeschlossen ===")


if __name__ == "__main__":
    try:
        test_exponential_rationale_funktion()
        test_vergleich_mit_rational()
        print("\n🎉 Alle Tests erfolgreich durchgeführt!")
    except Exception as e:
        print(f"\n❌ Fehler bei der Ausführung: {e}")
        import traceback

        traceback.print_exc()
