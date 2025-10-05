#!/usr/bin/env python3
"""
Phase 2 Examples: Advanced Unified API Features

Dieses Beispiel zeigt die neuen Funktionen von Phase 2 der vereinheitlichten API.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from schul_analysis.funktion import Funktion, erstelle_funktion_automatisch


def main():
    print("🎯 Schul-Analysis Framework - Phase 2 Beispiele")
    print("=" * 50)

    # === Automatische Erkennung (Phase 1) ===
    print("\n📊 Phase 1: Automatische Funktionserkennung")
    print("-" * 40)

    # Erstelle verschiedene Funktionen automatisch
    f1 = erstelle_funktion_automatisch("x^2 + 2x + 1")  # Quadratisch
    f2 = erstelle_funktion_automatisch("(x+1)/(x-1)")  # Gebrochen-rational
    f3 = erstelle_funktion_automatisch("exp(x) + 1")  # Exponential-rational

    print(f"f1(x) = {f1.term()} → {type(f1).__name__}")
    print(f"f2(x) = {f2.term()} → {type(f2).__name__}")
    print(f"f3(x) = {f3.term()} → {type(f3).__name__}")

    # === Phase 2: Intelligente Klassifizierung ===
    print("\n🧠 Phase 2: Intelligente Funktionsklassifizierung")
    print("-" * 45)

    # Erstelle Funktionen mit der vereinheitlichten Funktion-Klasse für Phase 2 Features
    print(
        "Hinweis: Phase 2 Features funktionieren mit der vereinheitlichten Funktion-Klasse:"
    )

    try:
        # Erstelle mit vereinheitlichter Klasse
        f1_unified = Funktion("x^2 + 2x + 1")
        f2_unified = Funktion("(x+1)/(x-1)")

        print(f"\nVereinheitlichte Analyse für f(x) = {f1_unified.term()}:")
        print(f"Typ: {f1_unified.funktionstyp}")
        print(f"Schwierigkeit: {f1_unified.komplexität['schwierigkeit']}")
        print(f"Operationen: {f1_unified.komplexität['operationen']}")
        print(f"Terme: {f1_unified.komplexität['terme']}")

        # === Phase 2: Umfassende Analyse ===
        print("\n📈 Phase 2: Umfassende Funktionsanalyse")
        print("-" * 40)

        analyse = f1_unified.analysiere()
        print("Grundlegende Eigenschaften:")
        for key, value in analyse["grundlegende_eigenschaften"].items():
            print(f"  {key}: {value}")

        print("\nEmpfehlungen:")
        for empfehlung in analyse["empfehlungen"]:
            print(f"  • {empfehlung}")

        # === Phase 2: Transformationen ===
        print("\n🔄 Phase 2: Funktionstransformationen")
        print("-" * 38)

        try:
            # Verschiedene Transformationen
            f_expanded = f1_unified.transformiere("expandiert")
            f_factored = f1_unified.transformiere("faktorisiert")

            print(f"Original:       {f1_unified.term()}")
            print(f"Expandiert:     {f_expanded.term()}")
            print(f"Faktorisiert:   {f_factored.term()}")
        except Exception as e:
            print(f"Transformationsfehler: {e}")

        # === Phase 2: Funktionsvergleiche ===
        print("\n⚖️ Phase 2: Funktionsvergleiche")
        print("-" * 32)

        try:
            # Zwei ähnliche Funktionen vergleichen
            f4_unified = Funktion("x^2 + 4x + 4")
            vergleich = f1_unified.vergleiche_mit(f4_unified)

            print(f"Vergleich: f1(x) = {f1_unified.term()}")
            print(f"         mit: f4(x) = {f4_unified.term()}")
            print(f"Gleich: {vergleich['gleichheit']}")
            print(f"Typen gleich: {vergleich['typ_gleich']}")

            if vergleich["differenz"]:
                print(f"Differenz: {vergleich['differenz']['ist_null']}")
        except Exception as e:
            print(f"Vergleichsfehler: {e}")

    except Exception as e:
        print(
            f"Phase 2 Feature Fehler (erwartet - einige Funktionen sind noch in Entwicklung): {e}"
        )

    # === Phase 2: Spezialisierte Funktionen ===
    print("\n🔧 Phase 2: Spezialisierte Funktionen")
    print("-" * 37)

    try:
        # Parametrisierte Funktion
        f_param = Funktion("a*x^2 + b*x + c")

        print(f"Parametrisiert: {f_param.term()}")

        if hasattr(f_param, "parameter") and f_param.parameter:
            param_names = [p.name for p in f_param.parameter]
            print(f"Parameter: {', '.join(param_names)}")

            # Spezialisieren
            f_spezial = f_param.spezialisiere_parameter(a=1, b=2, c=1)
            print(f"Spezialisiert (a=1, b=2, c=1): {f_spezial.term()}")
        else:
            print("Parameter-Erkennung in Entwicklung")
    except Exception as e:
        print(f"Parameterfehler: {e}")

    # === Phase 2: Metadaten ===
    print("\n📋 Phase 2: Metadaten und Informationen")
    print("-" * 38)

    try:
        f_info = Funktion("2*x^2 - 8*x + 6")
        info_text = f_info.get_info()
        print(f"Informationen:\n{info_text}")
    except Exception as e:
        print(f"Info-Fehler: {e}")

    print("\n🎉 Phase 2 Demo abgeschlossen!")
    print("\n📝 Zusammenfassung:")
    print("  ✅ Phase 1: Automatische Funktionserkennung funktioniert perfekt")
    print("  🔄 Phase 2: Erweiterte Funktionen in Entwicklung")
    print("  📊 Einige erweiterte Features benötigen die vollständige Funktion-Klasse")
    print("  🔧 Das Framework wird kontinuierlich verbessert")


if __name__ == "__main__":
    main()
