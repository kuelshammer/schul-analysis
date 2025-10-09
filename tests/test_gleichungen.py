#!/usr/bin/env python3
"""
Test für die neuen Gleichungslöser-Funktionen
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik import GanzrationaleFunktion, ParametrischeFunktion, a, x


def test_gleichungsloeser():
    print("=== Test Gleichungslöser-Funktionen ===")

    # 1. Teste GanzrationaleFunktion.löse_gleichung()
    print("\n1. Teste GanzrationaleFunktion.löse_gleichung()")

    f = GanzrationaleFunktion("x^2 + 2x - 3")
    print(f"f(x) = {f.term()}")

    # Standard-Nullstellen
    nullstellen = f.löse_gleichung(0)
    print(f"f(x) = 0 → {nullstellen}")

    # Andere Zielwerte
    loesungen_5 = f.löse_gleichung(5)
    print(f"f(x) = 5 → {loesungen_5}")

    # Komplexeres Beispiel
    g = GanzrationaleFunktion("x^3 - 3x + 1")
    print(f"\ng(x) = {g.term()}")
    g_nullstellen = g.löse_gleichung(0)
    print(f"g(x) = 0 → {g_nullstellen}")

    # 2. Teste ParametrischeFunktion.löse_für_x()
    print("\n2. Teste ParametrischeFunktion.löse_für_x()")

    # Erstelle parametrische Funktion: ax^2 + x
    f_param = ParametrischeFunktion([0, 1, a], [x])
    print(f"f_param(x) = {f_param.term()}")

    # Löse für verschiedene Parameterwerte
    for a_wert in [1, 2, -1]:
        loesungen = f_param.löse_für_x(a_wert, 0)
        print(f"f_{a_wert}(x) = 0 → {loesungen}")

        # Nicht-Nullstellen-Gleichungen
        loesungen_17 = f_param.löse_für_x(a_wert, 17)
        print(f"f_{a_wert}(x) = 17 → {loesungen_17}")

    # 3. Teste ParametrischeFunktion.löse_für_parameter()
    print("\n3. Teste ParametrischeFunktion.löse_für_parameter()")

    # f_a(a/2) = 1 → a(a/2)^2 + (a/2) = 1 → a^3/4 + a/2 = 1
    loesungen_param1 = f_param.löse_für_parameter("a/2", 1)
    print(f"f_a(a/2) = 1 → a = {loesungen_param1}")

    # f_a(2) = 5 → a(2)^2 + 2 = 5 → 4a + 2 = 5
    loesungen_param2 = f_param.löse_für_parameter(2, 5)
    print(f"f_a(2) = 5 → a = {loesungen_param2}")

    # f_a(sqrt(2)) = 3 → a(sqrt(2))^2 + sqrt(2) = 3 → 2a + sqrt(2) = 3
    loesungen_param3 = f_param.löse_für_parameter("sqrt(2)", 3)
    print(f"f_a(sqrt(2)) = 3 → a = {loesungen_param3}")

    # 4. Teste Fehlerbehandlung
    print("\n4. Teste Fehlerbehandlung")

    # Funktion ohne Parameter
    f_kein_param = GanzrationaleFunktion("x^2 + 1")
    try:
        f_kein_param.löse_für_parameter(1, 0)
    except Exception as e:
        print(f"Erwarteter Fehler: {e}")

    print("\n=== Test abgeschlossen ===")


if __name__ == "__main__":
    test_gleichungsloeser()
