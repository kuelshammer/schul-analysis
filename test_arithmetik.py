#!/usr/bin/env python3
"""
Umfassende Tests für die arithmetischen Operationen der GanzrationaleFunktion Klasse
"""

import sys

sys.path.insert(0, "src")

from schul_analysis.ganzrationale import GanzrationaleFunktion
import sympy as sp


def test_arithmetische_operationen():
    """Testet alle arithmetischen Operationen"""

    print("=== Test der arithmetischen Operationen ===\n")

    # Testfunktionen erstellen
    f = GanzrationaleFunktion("x^2+2x+1")  # (x+1)²
    g = GanzrationaleFunktion("x+1")  # x+1
    h = GanzrationaleFunktion("x^2 - 1")  # (x-1)(x+1)

    print("Testfunktionen:")
    print(f"f(x) = {f.term()}")
    print(f"g(x) = {g.term()}")
    print(f"h(x) = {h.term()}")
    print()

    # === Additionstests ===
    print("=== ADDITION ===")

    # Funktion+Funktion
    ergebnis = f + g
    print(f"f+g = {ergebnis.term()}")
    assert ergebnis.term() == "x^2+3x+2", (
        f"Erwartet: x^2+3x+2, erhalten: {ergebnis.term()}"
    )

    # Funktion+Zahl
    ergebnis = f + 5
    print(f"f+5 = {ergebnis.term()}")
    assert ergebnis.term() == "x^2+2x+6", (
        f"Erwartet: x^2+2x+6, erhalten: {ergebnis.term()}"
    )

    # Zahl+Funktion (rechts)
    ergebnis = 3 + g
    print(f"3+g = {ergebnis.term()}")
    assert ergebnis.term() == "x+4", f"Erwartet: x+4, erhalten: {ergebnis.term()}"

    print("✅ Additionstests erfolgreich\n")

    # === Subtraktionstests ===
    print("=== SUBTRAKTION ===")

    # Funktion - Funktion
    ergebnis = f - g
    print(f"f - g = {ergebnis.term()}")
    assert ergebnis.term() == "x^2+x", f"Erwartet: x^2+x, erhalten: {ergebnis.term()}"

    # Funktion - Zahl
    ergebnis = f - 1
    print(f"f - 1 = {ergebnis.term()}")
    assert ergebnis.term() == "x^2+2x", f"Erwartet: x^2+2x, erhalten: {ergebnis.term()}"

    # Zahl - Funktion (rechts)
    ergebnis = 5 - g
    print(f"5 - g = {ergebnis.term()}")
    assert ergebnis.term() == "4-x", f"Erwartet: 4-x, erhalten: {ergebnis.term()}"

    print("✅ Subtraktionstests erfolgreich\n")

    # === Multiplikationstests ===
    print("=== MULTIPLIKATION ===")

    # Funktion * Funktion
    ergebnis = f * g
    print(f"f * g = {ergebnis.term()}")
    assert ergebnis.term() == "x^3+3x^2+3x+1", (
        f"Erwartet: (x+1)³, erhalten: {ergebnis.term()}"
    )

    # Funktion * Zahl
    ergebnis = g * 3
    print(f"g * 3 = {ergebnis.term()}")
    assert ergebnis.term() == "3x+3", f"Erwartet: 3x+3, erhalten: {ergebnis.term()}"

    # Zahl * Funktion (rechts)
    ergebnis = 2 * f
    print(f"2 * f = {ergebnis.term()}")
    assert ergebnis.term() == "2x^2+4x+2", (
        f"Erwartet: 2x²+4x+2, erhalten: {ergebnis.term()}"
    )

    print("✅ Multiplikationstests erfolgreich\n")

    # === Divisionstests ===
    print("=== DIVISION ===")

    # Funktion / Funktion (exakt teilbar)
    ergebnis = f / g
    print(f"f / g = {ergebnis.term()}")
    assert ergebnis.term() == "x+1", f"Erwartet: x+1, erhalten: {ergebnis.term()}"

    # Funktion / Funktion (nicht exakt teilbar - sollte Fehler werfen)
    try:
        ergebnis = g / h
        print("FEHLER: g / h sollte TypeError werfen!")
        assert False, "g / h sollte TypeError werfen"
    except TypeError as e:
        print(f"g / h = TypeError: {e} (erwartet)")

    # Funktion / Zahl
    ergebnis = f / 2
    print(f"f / 2 = {ergebnis.term()}")
    assert ergebnis.term().replace(" ", "") == "x^2/2+x+1/2", (
        f"Erwartet: x^2/2+x+1/2, erhalten: {ergebnis.term()}"
    )

    # Zahl / Funktion (rechts) - sollte TypeError werfen, da kein Polynom
    try:
        ergebnis = 6 / g
        print(f"6 / g = {ergebnis.term()}")
        assert False, "6 / g sollte TypeError werfen (kein Polynom)"
    except TypeError as e:
        print(f"6 / g = TypeError: {e} (erwartet)")

    print("✅ Divisionstests erfolgreich\n")

    # === Potenzierungstests ===
    print("=== POTENZIERUNG ===")

    # Funktion ** Ganzzahl
    ergebnis = g**3
    print(f"g ** 3 = {ergebnis.term()}")
    assert ergebnis.term() == "x^3+3x^2+3x+1", (
        f"Erwartet: (x+1)³, erhalten: {ergebnis.term()}"
    )

    # Funktion ** 0
    ergebnis = g**0
    print(f"g ** 0 = {ergebnis.term()}")
    assert ergebnis.term() == "1", f"Erwartet: 1, erhalten: {ergebnis.term()}"

    # Funktion ** 1
    ergebnis = g**1
    print(f"g ** 1 = {ergebnis.term()}")
    assert ergebnis.term() == "x+1", f"Erwartet: x+1, erhalten: {ergebnis.term()}"

    # Ungültiger Exponent (sollte TypeError werfen, da NotImplemented zurückgegeben wird)
    try:
        ergebnis = g ** (-1)
        print(f"g ** (-1) = {ergebnis} (sollte TypeError sein)")
        assert False, "g ** (-1) sollte TypeError werfen"
    except TypeError as e:
        print(
            f"g ** (-1) = TypeError: {e} (erwartet, da NotImplemented zurückgegeben wird)"
        )

    print("✅ Potenzierungstests erfolgreich\n")

    # === In-Place Operationen ===
    print("=== IN-PLACE OPERATIONEN ===")

    # Test von +=
    f_copy = GanzrationaleFunktion("x^2+2x+1")
    f_copy += g
    print(f"f_copy += g = {f_copy.term()}")
    assert f_copy.term() == "x^2+3x+2", f"Erwartet: x^2+3x+2, erhalten: {f_copy.term()}"

    # Test von *=
    g_copy = GanzrationaleFunktion("x+1")
    g_copy *= 2
    print(f"g_copy *= 2 = {g_copy.term()}")
    assert g_copy.term() == "2x+2", f"Erwartet: 2x+2, erhalten: {g_copy.term()}"

    print("✅ In-Place Operationen erfolgreich\n")

    # === Unäre Operationen ===
    print("=== UNÄRE OPERATIONEN ===")

    # Negation
    ergebnis = -f
    print(f"-f = {ergebnis.term()}")
    assert ergebnis.term() == "-x^2-2x-1", (
        f"Erwartet: -x^2-2x-1, erhalten: {ergebnis.term()}"
    )

    # Positiv
    ergebnis = +f
    print(f"+f = {ergebnis.term()}")
    assert ergebnis.term() == "x^2+2x+1", (
        f"Erwartet: x²+2x+1, erhalten: {ergebnis.term()}"
    )

    print("✅ Unäre Operationen erfolgreich\n")

    # === Fehlerbehandlung ===
    print("=== FEHLERBEHANDLUNG ===")

    # Division durch Null
    try:
        ergebnis = g / 0
        print("FEHLER: Division durch Null sollte ZeroDivisionError werfen!")
        assert False
    except ZeroDivisionError:
        print("g / 0 = ZeroDivisionError (erwartet)")

    # Division durch Null-Funktion
    null_func = GanzrationaleFunktion("0")
    try:
        ergebnis = f / null_func
        print("FEHLER: Division durch Null-Funktion sollte ZeroDivisionError werfen!")
        assert False
    except ZeroDivisionError:
        print("f / null_func = ZeroDivisionError (erwartet)")

    # Ungültige Operation (String+Funktion)
    try:
        ergebnis = "test" + g
        print("FEHLER: String+Funktion sollte NotImplemented geben!")
        assert False
    except TypeError:
        print("'test'+g = TypeError (erwartet bei unpassender Typkombination)")

    print("✅ Fehlerbehandlung erfolgreich\n")

    # === Mathematische Identitäten ===
    print("=== MATHEMATISCHE IDENTITÄTEN ===")

    # Binomische Formeln
    a = GanzrationaleFunktion("x")
    b = GanzrationaleFunktion("1")

    # (a+b)² = a²+2ab+b²
    links = (a + b) ** 2
    rechts = a**2 + 2 * a * b + b**2
    print(f"(a+b)² = {links.term()}")
    print(f"a²+2ab+b² = {rechts.term()}")
    assert links == rechts, (
        f"Binomische Formel (a+b)² nicht erfüllt: {links} != {rechts}"
    )

    # (a-b)² = a² - 2ab+b²
    links = (a - b) ** 2
    rechts = a**2 - 2 * a * b + b**2
    print(f"(a-b)² = {links.term()}")
    print(f"a² - 2ab+b² = {rechts.term()}")
    assert links == rechts, (
        f"Binomische Formel (a-b)² nicht erfüllt: {links} != {rechts}"
    )

    # (a-b)(a+b) = a² - b²
    links = (a - b) * (a + b)
    rechts = a**2 - b**2
    print(f"(a-b)(a+b) = {links.term()}")
    print(f"a² - b² = {rechts.term()}")
    assert links == rechts, (
        f"Differenz von Quadraten nicht erfüllt: {links} != {rechts}"
    )

    print("✅ Mathematische Identitäten erfolgreich\n")

    print("🎉 ALLE TESTS ERFOLGREICH!")


if __name__ == "__main__":
    test_arithmetische_operationen()
