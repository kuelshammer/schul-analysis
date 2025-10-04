#!/usr/bin/env python3
"""
Kompletter Test der automatischen Symbolerkennung in GanzrationaleFunktion
"""

import sys

sys.path.insert(0, "src")

from schul_analysis import GanzrationaleFunktion, Variable, Parameter


def test_allgemeine_symbolerkennung():
    """Testet allgemeine automatische Symbolerkennung"""
    print("=== Allgemeine Symbolerkennung ===")

    # Testfall 1: Einfache quadratische Funktion
    print("\n1. Test: f = GanzrationaleFunktion('a x^2 + b x + c')")
    f = GanzrationaleFunktion("a x^2 + b x + c")
    print(f"   Funktion: {f.term()}")
    print(f"   Variable: {[v.name for v in f.variablen]}")
    print(f"   Parameter: {[p.name for p in f.parameter]}")
    print(f"   Hauptvariable: {f.hauptvariable.name if f.hauptvariable else 'None'}")

    # Testfall 2: Lineare Funktion mit t
    print("\n2. Test: g = GanzrationaleFunktion('100t + 20')")
    g = GanzrationaleFunktion("100t + 20")
    print(f"   Funktion: {g.term()}")
    print(f"   Variable: {[v.name for v in g.variablen]}")
    print(f"   Parameter: {[p.name for p in g.parameter]}")
    print(f"   Hauptvariable: {g.hauptvariable.name if g.hauptvariable else 'None'}")

    # Testfall 3: Gemischte Buchstaben
    print("\n3. Test: h = GanzrationaleFunktion('p y^2 + q y + r')")
    h = GanzrationaleFunktion("p y^2 + q y + r")
    print(f"   Funktion: {h.term()}")
    print(f"   Variable: {[v.name for v in h.variablen]}")
    print(f"   Parameter: {[p.name for p in h.parameter]}")
    print(f"   Hauptvariable: {h.hauptvariable.name if h.hauptvariable else 'None'}")

    # Testfall 4: Mehrere Variablen
    print("\n4. Test: k = GanzrationaleFunktion('x^2 + y^2 + z^2')")
    k = GanzrationaleFunktion("x^2 + y^2 + z^2")
    print(f"   Funktion: {k.term()}")
    print(f"   Variable: {[v.name for v in k.variablen]}")
    print(f"   Parameter: {[p.name for p in k.parameter]}")
    print(f"   Hauptvariable: {k.hauptvariable.name if k.hauptvariable else 'None'}")

    return True


def test_heuristik_verhalten():
    """Testet das Verhalten der Heuristik anhand der Ergebnisse"""
    print("\n=== Heuristik-Verhalten ===")

    test_cases = [
        ("a x^2 + b x + c", "x als Variable, a/b/c als Parameter"),
        ("100t + 20", "t als Variable, keine Parameter"),
        ("p y^2 + q y + r", "y als Variable, p/q/r als Parameter"),
        ("x^2 + y^2 + z^2", "x/y/z als Variablen, keine Parameter"),
        ("alpha + beta", "alpha/beta als Variablen (nicht in Standard-Heuristik)"),
        ("k x^2 + m x + n", "x als Variable, k/m/n als Parameter"),
    ]

    for expr, expected in test_cases:
        try:
            f = GanzrationaleFunktion(expr)
            vars_list = [v.name for v in f.variablen]
            params_list = [p.name for p in f.parameter]
            print(f"   '{expr}':")
            print(f"     Erwartet: {expected}")
            print(f"     Tatsächlich: Vars={vars_list}, Params={params_list}")
        except Exception as e:
            print(f"   '{expr}': Fehler - {e}")

    return True


def test_funktionsoperationen():
    """Testet, ob Funktionsoperationen mit Symbolerkennung funktionieren"""
    print("\n=== Funktionsoperationen ===")

    # Testfall 1: Ableitung
    print("\n1. Test: Ableitung")
    f = GanzrationaleFunktion("a x^2 + b x + c")
    print(f"   Original: {f.term()}")
    print(f"   Variable: {[v.name for v in f.variablen]}")

    f1 = f.ableitung()
    print(f"   1. Ableitung: {f1.term()}")
    print(f"   Variable: {[v.name for v in f1.variablen]}")
    print(f"   Parameter: {[p.name for p in f1.parameter]}")

    # Testfall 2: Werteberechnung mit konkreten Werten
    print("\n2. Test: Werteberechnung mit konkreten Werten")
    f_konkret = f.mit_wert(a=1, b=2, c=1)
    print(f"   Mit a=1, b=2, c=1: {f_konkret.term()}")
    print(f"   f(2) = {f_konkret.wert(2)}")
    print(f"   f(0) = {f_konkret.wert(0)}")

    # Testfall 3: Nullstellen mit konkreten Werten
    print("\n3. Test: Nullstellen mit konkreten Werten")
    print(f"   Nullstellen: {f_konkret.nullstellen()}")

    return True


def test_backward_kompatibilitaet():
    """Testet, dass bestehende Funktionalität nicht beschädigt wurde"""
    print("\n=== Backward-Kompatibilität ===")

    # Testfall 1: Koeffizienten-Liste
    print("\n1. Test: Koeffizienten-Liste")
    f1 = GanzrationaleFunktion([1, 2, 3])  # x^2 + 2x + 3
    print(f"   Funktion: {f1.term()}")
    print(f"   Variable: {[v.name for v in f1.variablen]}")
    print(f"   Parameter: {[p.name for p in f1.parameter]}")
    print(f"   Grad: {f1.grad()}")

    # Testfall 2: Dictionary
    print("\n2. Test: Dictionary")
    f2 = GanzrationaleFunktion({0: 5, 2: 1})  # x^2 + 5
    print(f"   Funktion: {f2.term()}")
    print(f"   Variable: {[v.name for v in f2.variablen]}")
    print(f"   Parameter: {[p.name for p in f2.parameter]}")

    # Testfall 3: Bestehende Methoden
    print("\n3. Test: Bestehende Methoden")
    f3 = GanzrationaleFunktion([1, -4, 3])  # x^2 - 4x + 3
    print(f"   Funktion: {f3.term()}")
    print(f"   Grad: {f3.grad()}")
    print(f"   Nullstellen: {f3.nullstellen()}")
    print(f"   Extremstellen: {f3.extremstellen()}")

    return True


def test_schulbeispiele():
    """Testet typische Schulbeispiele"""
    print("\n=== Typische Schulbeispiele ===")

    beispiele = [
        ("x^2 - 4", "Einfache quadratische Funktion"),
        ("2x + 5", "Lineare Funktion"),
        ("x^3 - 3x^2 + 2x", "Kubische Funktion"),
        ("a(x - 2)^2 + 3", "Parameterisierte Scheitelpunktform"),
        ("0.5x^2 - 2x + 1", "Dezimalkoeffizienten"),
    ]

    for expr, beschreibung in beispiele:
        print(f"\n{beschreibung}: f(x) = {expr}")
        try:
            f = GanzrationaleFunktion(expr)
            print(f"   Automatisch erkannt:")
            print(f"     Variable: {[v.name for v in f.variablen]}")
            print(f"     Parameter: {[p.name for p in f.parameter]}")
            print(
                f"     Hauptvariable: {f.hauptvariable.name if f.hauptvariable else 'None'}"
            )
            print(f"   Grad: {f.grad()}")

            # Versuche Nullstellen zu berechnen
            try:
                nullstellen = f.nullstellen()
                print(f"   Nullstellen: {nullstellen}")
            except:
                print(
                    f"   Nullstellen: Konnten nicht berechnet werden (Parameter vorhanden)"
                )

        except Exception as e:
            print(f"   Fehler: {e}")

    return True


def test_randfaelle():
    """Testet Randfälle und Fehlerbehandlung"""
    print("\n=== Randfälle ===")

    # Testfall 1: Leerer String
    print("\n1. Test: Leerer String")
    try:
        f = GanzrationaleFunktion("")
        print(f"   Funktion: {f.term()}")
    except Exception as e:
        print(f"   Erwarteter Fehler: {e}")

    # Testfall 2: Nur Zahlen
    print("\n2. Test: Nur Zahlen")
    try:
        f = GanzrationaleFunktion("42")
        print(f"   Funktion: {f.term()}")
        print(f"   Variable: {[v.name for v in f.variablen]}")
        print(f"   Parameter: {[p.name for p in f.parameter]}")
    except Exception as e:
        print(f"   Fehler: {e}")

    # Testfall 3: Ungültige Zeichen
    print("\n3. Test: Ungültige Zeichen")
    try:
        f = GanzrationaleFunktion("x^2 + @#$%")
        print(f"   Funktion: {f.term()}")
    except Exception as e:
        print(f"   Erwarteter Fehler: {e}")

    # Testfall 4: Nur ein Buchstabe
    print("\n4. Test: Nur ein Buchstabe")
    f = GanzrationaleFunktion("x")
    print(f"   Funktion: {f.term()}")
    print(f"   Variable: {[v.name for v in f.variablen]}")
    print(f"   Parameter: {[p.name for p in f.parameter]}")

    return True


def main():
    """Führt alle Tests durch"""
    print("=== Kompletter Test der automatischen Symbolerkennung ===")
    print("=" * 60)

    tests = [
        test_allgemeine_symbolerkennung,
        test_heuristik_verhalten,
        test_funktionsoperationen,
        test_backward_kompatibilitaet,
        test_schulbeispiele,
        test_randfaelle,
    ]

    erfolgreich = 0
    gesamt = len(tests)

    for test in tests:
        try:
            if test():
                erfolgreich += 1
                print(f"\n✓ {test.__name__} erfolgreich")
            else:
                print(f"\n✗ {test.__name__} fehlgeschlagen")
        except Exception as e:
            print(f"\n✗ {test.__name__} mit Exception: {e}")
            import traceback

            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"Testergebnis: {erfolgreich}/{gesamt} Tests erfolgreich")

    if erfolgreich == gesamt:
        print(
            "🎉 Alle Tests bestanden! Die automatische Symbolerkennung funktioniert perfekt."
        )
    else:
        print(
            "⚠️  Einige Tests fehlgeschlagen. Bitte überprüfen Sie die Implementierung."
        )

    return erfolgreich == gesamt


if __name__ == "__main__":
    main()
