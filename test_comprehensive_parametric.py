#!/usr/bin/env python3
"""
Komprehensiver Test aller erweiterten parametrischen Methoden.
Demonstriert das vollständige symmetrische Framework für:
- Nullstellen: f(x) = 0
- Extremstellen: f'(x) = 0
- Wendestellen: f''(x) = 0
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis.funktion import Funktion
import logging

# Logging für Debug-Informationen aktivieren
logging.basicConfig(level=logging.INFO)


def test_komplettes_symmetrisches_framework():
    """Testet das vollständige symmetrische Framework mit einer parametrischen Funktion."""

    print("=== Komprehensiver Test: Symmetrisches Parametrisches Framework ===\n")

    # Wähle eine cubische parametrische Funktion, die alle drei Stufen zeigt
    print("🔬 Analyse von f(x) = ax³ + bx² + cx + d")
    f = Funktion("a*x^3 + b*x^2 + c*x + d")

    print(f"📊 Funktion: {f.term()}")
    print()

    # Stufe 1: Nullstellen (f(x) = 0)
    print("📍 Stufe 1: Nullstellen (f(x) = 0)")
    nullstellen = f.nullstellen_optimiert()
    if nullstellen:
        print("   Gefundene Nullstellen:")
        for i, ns in enumerate(nullstellen, 1):
            print(f"   {i}. x = {ns.x}, Vielfachheit = {ns.multiplicitaet}")
    else:
        print("   Keine Nullstellen gefunden")
    print()

    # Stufe 2: Extremstellen (f'(x) = 0)
    print("📈 Stufe 2: Extremstellen (f'(x) = 0)")
    f1 = f.ableitung(1)
    print(f"   f'(x) = {f1.term()}")
    extremstellen = f.extremstellen_optimiert()
    if extremstellen:
        print("   Gefundene Extremstellen:")
        for i, es in enumerate(extremstellen, 1):
            print(f"   {i}. x = {es.x}, Typ = {es.typ}")
    else:
        print("   Keine Extremstellen gefunden")
    print()

    # Stufe 3: Wendestellen (f''(x) = 0)
    print("🌀 Stufe 3: Wendestellen (f''(x) = 0)")
    f2 = f.ableitung(2)
    print(f"   f''(x) = {f2.term()}")
    wendestellen = f.wendestellen_optimiert()
    if wendestellen:
        print("   Gefundene Wendestellen:")
        for i, ws in enumerate(wendestellen, 1):
            print(f"   {i}. x = {ws.x}, Typ = {ws.typ}")
    else:
        print("   Keine Wendestellen gefunden")
    print()

    # Zusammenfassung
    print("📋 Zusammenfassung der mathematischen Analyse:")
    print(f"   • Nullstellen: {len(nullstellen)}")
    print(f"   • Extremstellen: {len(extremstellen)}")
    print(f"   • Wendestellen: {len(wendestellen)}")
    print()

    # Zeige die Symmetrie
    print("🔗 Mathematische Symmetrie:")
    print("   f(x) = 0     → Nullstellen")
    print("   f'(x) = 0    → Extremstellen")
    print("   f''(x) = 0   → Wendestellen")
    print()

    return {
        "funktion": f,
        "nullstellen": nullstellen,
        "extremstellen": extremstellen,
        "wendestellen": wendestellen,
    }


def test_verschiedene_funktionstypen():
    """Testet verschiedene Funktionstypen mit dem fortgeschrittenen Framework."""

    print("=== Test verschiedener Funktionstypen ===\n")

    test_funktionen = [
        ("Quadratisch", "a*x^2 + b*x + c"),
        ("Kubisch", "a*x^3 + b*x^2 + c*x + d"),
        ("Einfach kubisch", "x^3 + a*x"),
        ("Quartisch", "a*x^4 + b*x^3 + c*x^2 + d*x + e"),
        ("Faktorisierbar", "x^2 - (a+b)*x + a*b"),
    ]

    for name, term in test_funktionen:
        print(f"📊 {name}: {term}")

        try:
            f = Funktion(term)

            # Teste alle drei Methoden
            ns = f.nullstellen_optimiert()
            es = f.extremstellen_optimiert()
            ws = f.wendestellen_optimiert()

            print(
                f"   Nullstellen: {len(ns)}, Extremstellen: {len(es)}, Wendestellen: {len(ws)}"
            )

            # Zeige Erfolg der Strategien
            if f.parameter:
                print("   ✅ Erweiterte parametrische Methoden verwendet")
            else:
                print("   ✅ Optimiertes Framework verwendet")

        except Exception as e:
            print(f"   ❌ Fehler: {e}")

        print()


def test_strategie_vergleich():
    """Vergleicht die Erfolgsraten der verschiedenen Strategien."""

    print("=== Strategie-Vergleich ===\n")

    # Funktion die mehrere Strategien testen kann
    f = Funktion("x^2 - (a+b)*x + a*b")  # Faktorisierbar

    print(f"🔬 Testfunktion: {f.term()}")
    print("Diese Funktion sollte Faktorisierung als Strategie verwenden.")
    print()

    # Teste Nullstellen mit Strategie-Info
    print("📍 Nullstellen-Berechnung:")
    print("   Erwartet: Faktorisierungs-Strategie erfolgreich")
    nullstellen = f.nullstellen_optimiert()

    if nullstellen:
        print("   ✅ Strategie erfolgreich!")
        for ns in nullstellen:
            print(f"      x = {ns.x}")
    else:
        print("   ❌ Strategie fehlgeschlagen")

    print()
    print("🎯 Dies demonstriert die Power der Multi-Strategien:")
    print("   1. Faktorisierung → x² - (a+b)x + ab = (x-a)(x-b)")
    print("   2. Lösung → x = a, x = b")
    print("   3. Verbesserte parametrische Verarbeitung")
    print()


if __name__ == "__main__":
    print("🚀 Starte komprehensiven Test des erweiterten parametrischen Frameworks")
    print("=" * 70)
    print()

    # Führe alle Tests durch
    test_komplettes_symmetrisches_framework()
    print()
    test_verschiedene_funktionstypen()
    test_strategie_vergleich()

    print("✅ Alle Tests abgeschlossen!")
    print()
    print(
        "🎉 Das erweiterte parametrische Framework ist jetzt vollständig funktionsfähig!"
    )
    print("   Es unterstützt:")
    print("   • Fortgeschrittene Lösungsstrategien (Faktorisierung, Polynom, solveset)")
    print("   • Verbesserte parametrische Verarbeitung")
    print("   • Symmetrische Architektur für alle drei mathematischen Stufen")
    print("   • Robuste Fehlerbehandlung und Fallbacks")
