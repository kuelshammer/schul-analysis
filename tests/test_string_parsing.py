#!/usr/bin/env python3
"""
Test für die neue String-basierte Definition von parametrischen Funktionen
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik import Parameter, ParametrischeFunktion, Variable, a, k, x


def test_string_parsing():
    print("=== Test: String-basierte Definition von parametrischen Funktionen ===")

    # 1. Einfache Beispiele mit vordefinierten Objekten
    print("\n1. Einfache Beispiele mit vordefinierten x und a:")

    try:
        # f(x) = a*x^2 - 1
        f1 = ParametrischeFunktion("a*x^2 - 1", x, a)
        print(f"f1(x) = {f1.term()}")

        # g(x) = 2*a*x + 3
        f2 = ParametrischeFunktion("2*a*x + 3", x, a)
        print(f"f2(x) = {f2.term()}")

        # h(x) = a*x^3 + k*x^2 + x - 5
        f3 = ParametrischeFunktion("a*x^3 + k*x^2 + x - 5", x, a, k)
        print(f"f3(x) = {f3.term()}")

    except Exception as e:
        print(f"FEHLER: {e}")
        import traceback

        traceback.print_exc()

    # 2. Teste mit konkreten Werten
    print("\n2. Teste mit konkreten Parameterwerten:")

    try:
        # f_a(x) = a*x^2 - 1
        f1 = ParametrischeFunktion("a*x^2 - 1", x, a)

        # Konkrete Funktionen
        f1_a2 = f1.mit_wert(a=2)  # f_2(x) = 2x^2 - 1
        f1_a_minus1 = f1.mit_wert(a=-1)  # f_-1(x) = -x^2 - 1

        print(f"f_a=2(x) = {f1_a2.term()}")
        print(f"f_a=-1(x) = {f1_a_minus1.term()}")
        print(f"f_2(1) = {f1_a2.wert(1)}")
        print(f"f_-1(1) = {f1_a_minus1.wert(1)}")

    except Exception as e:
        print(f"FEHLER: {e}")
        import traceback

        traceback.print_exc()

    # 3. Teste Gleichungslöser
    print("\n3. Teste Gleichungslöser mit String-basierten Funktionen:")

    try:
        # f_a(x) = a*x^2 - 1
        f1 = ParametrischeFunktion("a*x^2 - 1", x, a)

        # Löse f_2(x) = 7
        loesungen_x = f1.löse_für_x(2, 7)  # 2x^2 - 1 = 7
        print(f"f_2(x) = 7 → x = {loesungen_x}")

        # Löse f_a(1) = 0
        loesungen_a = f1.löse_für_parameter(1, 0)  # a*1^2 - 1 = 0
        print(f"f_a(1) = 0 → a = {loesungen_a}")

    except Exception as e:
        print(f"FEHLER: {e}")
        import traceback

        traceback.print_exc()

    # 4. Vergleich mit Koeffizienten-Methode
    print("\n4. Vergleich mit Koeffizienten-Methode:")

    try:
        # Gleiche Funktion auf zwei Arten definieren
        f_string = ParametrischeFunktion("a*x^2 + x", x, a)
        f_koeff = ParametrischeFunktion([0, 1, a], [x])

        print(f"String-Methode: {f_string.term()}")
        print(f"Koeffizienten-Methode: {f_koeff.term()}")

        # Teste, ob beide Methoden gleiche Ergebnisse liefern
        f_string_a3 = f_string.mit_wert(a=3)
        f_koeff_a3 = f_koeff.mit_wert(a=3)

        print(
            f"Beide Methoden f_3(2) gleich: {f_string_a3.wert(2) == f_koeff_a3.wert(2)}"
        )

    except Exception as e:
        print(f"FEHLER: {e}")
        import traceback

        traceback.print_exc()

    # 5. Komplexere Beispiele
    print("\n5. Komplexere Beispiele:")

    try:
        # Eigene Variablen/Parameter
        mein_x = Variable("x")
        mein_b = Parameter("beta")

        # f_β(x) = β*x^2 + 2*x - 1
        f4 = ParametrischeFunktion("beta*x^2 + 2*x - 1", mein_x, mein_b)
        print(f"f4(x) = {f4.term()}")

        # Test mit griechischen Buchstaben
        f4_b2 = f4.mit_wert(beta=2)
        print(f"f_β=2(x) = {f4_b2.term()}")
        print(f"f_β=2(1) = {f4_b2.wert(1)}")

    except Exception as e:
        print(f"FEHLER: {e}")
        import traceback

        traceback.print_exc()

    print("\n=== Test abgeschlossen ===")


if __name__ == "__main__":
    test_string_parsing()
