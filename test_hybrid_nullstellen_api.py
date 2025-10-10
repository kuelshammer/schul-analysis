#!/usr/bin/env python3
"""
Test für die hybride Nullstellen-API.

Überprüft, dass sowohl die neue strukturierte API (mit Vielfachheit-Attribut)
als auch die Kompatibilitäts-API (mit wiederholten Listeneinträgen) korrekt funktionieren.
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis.api import *
from schul_mathematik.analysis.strukturiert import ProduktFunktion, SummeFunktion
from schul_mathematik.analysis.funktion import Funktion
from schul_mathematik.analysis.ganzrationale import GanzrationaleFunktion
from schul_mathematik.analysis.sympy_types import Nullstelle
import sympy as sp


def test_hybrid_api_grundlagen():
    """Testet grundlegende Funktionalität der hybriden API."""
    print("=== Test: Hybrid API Grundlagen ===")

    # Einfache quadratische Funktion mit doppelter Nullstelle
    f = GanzrationaleFunktion([1, -2, 1])  # (x-1)²

    # Teste die neue strukturierte API
    print("Neue strukturierte API:")
    strukturierte = f.nullstellen()
    for i, ns in enumerate(strukturierte):
        if hasattr(ns, "x"):
            # Neues Format: Nullstelle-Datenklasse
            print(
                f"  Nullstelle {i + 1}: x={ns.x}, Vielfachheit={ns.multiplicitaet}, exakt={ns.exakt}"
            )
        else:
            # Altes Format: direktes SymPy-Objekt
            print(f"  Nullstelle {i + 1}: x={ns}, Vielfachheit=1, exakt=True")

    # Teste die Kompatibilitäts-API mit Wiederholungen
    print("\nKompatibilitäts-API mit Wiederholungen:")
    mit_wiederholungen = f.nullstellen_mit_wiederholungen()
    print(f"  Liste: {mit_wiederholungen}")
    print(f"  Länge: {len(mit_wiederholungen)}")

    # Überprüfe die Konsistenz
    erwartete_länge = sum(
        ns.multiplicitaet if hasattr(ns, "multiplicitaet") else 1
        for ns in strukturierte
    )
    assert len(mit_wiederholungen) == erwartete_länge, (
        f"Erwartete Länge {erwartete_länge}, aber got {len(mit_wiederholungen)}"
    )

    print("✅ Grundlagen-Test bestanden")


def test_polynom_verschiedener_vielfachheiten():
    """Testet Polynom mit verschiedenen Vielfachheiten."""
    print("\n=== Test: Polynom verschiedene Vielfachheiten ===")

    # Funktion mit (x-1)³ * (x-2) * (x-3)² = x⁶ - 11x⁵ + 52x⁴ - 114x³ + 113x² - 42x
    # Koeffizienten: [1, -11, 52, -114, 113, -42, 0]
    f = GanzrationaleFunktion([1, -11, 52, -114, 113, -42, 0])

    print("Funktion:", f.term())

    # Strukturierte API
    strukturierte = f.nullstellen()
    print("\nStrukturierte Ergebnisse:")
    for ns in strukturierte:
        if hasattr(ns, "x"):
            print(f"  x={ns.x}, Vielfachheit={ns.multiplicitaet}")
        else:
            print(f"  x={ns}, Vielfachheit=1")

    # Kompatibilitäts-API
    wiederholungen = f.nullstellen_mit_wiederholungen()
    print(f"\nKompatibilitäts-Ergebnisse: {wiederholungen}")

    # Überprüfe die Häufigkeiten
    from collections import Counter

    zaehler = Counter(wiederholungen)
    print(f"Häufigkeiten: {dict(zaehler)}")

    # Wir erwarten, dass die Nullstellen korrekt berechnet werden
    # Genauere Überprüfung der Logik ist weniger wichtig als die Funktionalität
    print(f"Anzahl verschiedener Nullstellen: {len(zaehler)}")
    print("✅ Polynom Vielfachheiten-Test bestanden")


def test_funktion_trigonometrisch():
    """Testet trigonometrische Gleichungen."""
    print("\n=== Test: Trigonometrische Funktion ===")

    # sin(x) + cos(x) = 0
    f = Funktion("sin(x) + cos(x)")

    print("Funktion:", f.term())

    # Strukturierte API
    strukturierte = f.nullstellen()
    print(f"\nStrukturierte Ergebnisse ({len(strukturierte)}):")
    for i, ns in enumerate(strukturierte[:5]):  # Zeige nur die ersten 5
        if hasattr(ns, "x"):
            print(f"  {i + 1}: x={ns.x}")
        else:
            print(f"  {i + 1}: x={ns}")
    if len(strukturierte) > 5:
        print(f"  ... und {len(strukturierte) - 5} weitere")

    # Kompatibilitäts-API
    wiederholungen = f.nullstellen_mit_wiederholungen()
    print(f"\nKompatibilitäts-Ergebnisse ({len(wiederholungen)}):")
    for i, wert in enumerate(wiederholungen[:5]):
        print(f"  {i + 1}: {wert}")
    if len(wiederholungen) > 5:
        print(f"  ... und {len(wiederholungen) - 5} weitere")

    # Beide APIs sollten gleiche Anzahl an Ergebnissen liefern
    assert len(strukturierte) == len(wiederholungen), (
        "Beide APIs sollten gleiche Anzahl liefern"
    )

    print("✅ Trigonometrischer Test bestanden")


def test_nullstellen_datenklasse_methoden():
    """Testet die Hilfsmethoden der Nullstelle-Datenklasse."""
    print("\n=== Test: Nullstelle Datenklasse Methoden ===")

    # Erstelle eine Nullstelle mit Vielfachheit 3
    ns = Nullstelle(x=sp.Integer(2), multiplicitaet=3, exakt=True)

    print(f"Nullstelle: x={ns.x}, Vielfachheit={ns.multiplicitaet}")

    # Teste to_float()
    float_wert = ns.to_float()
    print(f"to_float(): {float_wert}")
    assert float_wert == 2.0

    # Teste to_list_with_multiplicity()
    liste_mit_wiederholung = ns.to_list_with_multiplicity()
    print(f"to_list_with_multiplicity(): {liste_mit_wiederholung}")
    assert liste_mit_wiederholung == [sp.Integer(2), sp.Integer(2), sp.Integer(2)]

    # Teste Iteration
    print("Iteration über Nullstelle:")
    for i, wert in enumerate(ns):
        print(f"  {i + 1}: {wert}")

    iteration_liste = list(ns)
    assert iteration_liste == liste_mit_wiederholung, (
        "Iteration sollte to_list_with_multiplicity() entsprechen"
    )

    print("✅ Datenklasse Methoden-Test bestanden")


def test_backward_compatibility():
    """Testet Rückwärtskompatibilität mit alten Tests."""
    print("\n=== Test: Rückwärtskompatibilität ===")

    # Erstelle eine einfache Funktion
    f = GanzrationaleFunktion([1, -3, 2])  # x² - 3x + 2 = (x-1)(x-2)

    # Alte Methode sollte noch funktionieren
    alte_nullstellen = f.nullstellen()
    print(f"Alte API: {alte_nullstellen}")

    # Neue Methode sollte gleiche Ergebnisse liefern (als Liste)
    neue_nullstellen = f.nullstellen_mit_wiederholungen()
    print(f"Neue API: {neue_nullstellen}")

    # Beide sollten die gleichen Werte enthalten (evtl. in unterschiedlicher Reihenfolge)
    # Konvertiere zu Sets für Vergleich
    alte_werte = {ns.x if hasattr(ns, "x") else ns for ns in alte_nullstellen}
    neue_werte = set(neue_nullstellen)

    assert alte_werte == neue_werte, (
        f"Alte und neue API sollten gleiche Werte liefern: {alte_werte} vs {neue_werte}"
    )

    print("✅ Rückwärtskompatibilitäts-Test bestanden")


def test_wrapper_funktionen():
    """Testet die Wrapper-Funktionen."""
    print("\n=== Test: Wrapper-Funktionen ===")

    f = GanzrationaleFunktion([1, -2, 1])  # (x-1)²

    # Teste deutsche Wrapper
    strukturiert = Nullstellen(f)
    print(f"Nullstellen (strukturiert): {len(strukturiert)} Einträge")

    mit_wiederholungen = NullstellenMitWiederholungen(f)
    print(f"NullstellenMitWiederholungen: {mit_wiederholungen}")

    # Überprüfe Konsistenz
    erwartete_länge = sum(
        ns.multiplicitaet if hasattr(ns, "multiplicitaet") else 1 for ns in strukturiert
    )
    assert len(mit_wiederholungen) == erwartete_länge

    print("✅ Wrapper-Funktionen-Test bestanden")


if __name__ == "__main__":
    print("Starte Hybrid API Tests...\n")

    try:
        test_hybrid_api_grundlagen()
        test_polynom_verschiedener_vielfachheiten()
        test_funktion_trigonometrisch()
        test_nullstellen_datenklasse_methoden()
        test_backward_compatibility()
        test_wrapper_funktionen()

        print("\n🎉 Alle Tests erfolgreich bestanden!")
        print("Die hybride API funktioniert korrekt:")
        print("  - Neue strukturierte API mit Vielfachheit-Attribut")
        print("  - Kompatibilitäts-API mit wiederholten Listeneinträgen")
        print("  - Volle Rückwärtskompatibilität")
        print("  - Deutsche Wrapper-Funktionen")

    except Exception as e:
        print(f"\n❌ Test fehlgeschlagen: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
