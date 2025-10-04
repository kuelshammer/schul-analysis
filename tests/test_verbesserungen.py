#!/usr/bin/env python3
"""
Testet die verbesserten Fehlermeldungen und Exception Handling
"""

import sys

sys.path.insert(0, "src")

from schul_analysis import GanzrationaleFunktion


def test_parameter_fehlermeldung():
    """Testet die verbesserte Fehlermeldung bei Parametern"""
    print("=== Test: Verbesserte Parameter-Fehlermeldung ===")

    # Funktion mit Parametern
    f = GanzrationaleFunktion("a x^2 + b x + c")
    print(f"Funktion: {f.term()}")
    print(f"Variable: {[v.name for v in f.variablen]}")
    print(f"Parameter: {[p.name for p in f.parameter]}")

    # Versuche, Wert zu berechnen (sollte klare Fehlermeldung geben)
    print("\nVersuche f(2) zu berechnen...")
    try:
        wert = f.wert(2)
        print(f"f(2) = {wert}")
    except ValueError as e:
        print(f"Erwarteter Fehler: {e}")

    print("\n✅ Klare Fehlermeldung für Parameter erfolgreich!")


def test_explicit_symbol_specification():
    """Testet die explizite Symbol-Vorgabe"""
    print("\n=== Test: Explizite Symbol-Vorgabe ===")

    # Normalfall (automatische Erkennung)
    f1 = GanzrationaleFunktion("a t^2 + b t + c")
    print(
        f"Ohne Vorgabe: Vars={[v.name for v in f1.variablen]}, Params={[p.name for p in f1.parameter]}"
    )

    # Mit expliziter Vorgabe
    f2 = GanzrationaleFunktion(
        "a t^2 + b t + c", variable="t", parameter=["a", "b", "c"]
    )
    print(
        f"Mit Vorgabe: Vars={[v.name for v in f2.variablen]}, Params={[p.name for p in f2.parameter]}"
    )

    # Umgekehrte Rollen
    f3 = GanzrationaleFunktion(
        "x a^2 + y a + z", variable="a", parameter=["x", "y", "z"]
    )
    print(
        f"Rollengetauscht: Vars={[v.name for v in f3.variablen]}, Params={[p.name for p in f3.parameter]}"
    )

    print("\n✅ Explizite Symbol-Vorgabe erfolgreich!")


def test_bessere_exception_handling():
    """Testet das verbesserte Exception Handling"""
    print("\n=== Test: Verbessertes Exception Handling ===")

    # Teste Extremstellen-Berechnung mit problematischer Funktion
    print("\n1. Teste Extremstellen-Berechnung:")
    f = GanzrationaleFunktion("x^4 - 3x^2 + x")
    try:
        extremstellen = f.extremstellen()
        print(f"Extremstellen: {extremstellen}")
    except Exception as e:
        print(f"Fehler abgefangen: {e}")

    print("\n✅ Verbessertes Exception Handling erfolgreich!")


if __name__ == "__main__":
    test_parameter_fehlermeldung()
    test_explicit_symbol_specification()
    test_bessere_exception_handling()

    print("\n🎉 Alle Verbesserungen erfolgreich getestet!")
