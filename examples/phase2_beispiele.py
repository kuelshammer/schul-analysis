#!/usr/bin/env python3
"""
Phase 2 Examples: Advanced Unified API Features

Dieses Beispiel zeigt die neuen Funktionen von Phase 2 der vereinheitlichten API.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from schul_analysis.funktion import erstelle_funktion_automatisch


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

    # Zeige detaillierte Informationen für eine Funktion
    print(f"\nAnalyse für f(x) = {f1.term()}:")
    print(f"Typ: {f1.funktionstyp}")
    print(f"Schwierigkeit: {f1.komplexität['schwierigkeit']}")
    print(f"Operationen: {f1.komplexität['operationen']}")
    print(f"Terme: {f1.komplexität['terme']}")

    # === Phase 2: Umfassende Analyse ===
    print("\n📈 Phase 2: Umfassende Funktionsanalyse")
    print("-" * 40)

    analyse = f1.analysiere()
    print("Grundlegende Eigenschaften:")
    for key, value in analyse["grundlegende_eigenschaften"].items():
        print(f"  {key}: {value}")

    print(f"\nEmpfehlungen:")
    for empfehlung in analyse["empfehlungen"]:
        print(f"  • {empfehlung}")

    # === Phase 2: Transformationen ===
    print("\n🔄 Phase 2: Funktionstransformationen")
    print("-" * 38)

    try:
        # Verschiedene Transformationen
        f_expanded = f1.transformiere("expandiert")
        f_factored = f1.transformiere("faktorisiert")

        print(f"Original:       {f1.term()}")
        print(f"Expandiert:     {f_expanded.term()}")
        print(f"Faktorisiert:   {f_factored.term()}")
    except Exception as e:
        print(f"Transformationsfehler: {e}")

    # === Phase 2: Funktionsvergleiche ===
    print("\n⚖️ Phase 2: Funktionsvergleiche")
    print("-" * 32)

    try:
        # Zwei ähnliche Funktionen vergleichen
        f4 = erstelle_funktion_automatisch("x^2 + 4x + 4")
        vergleich = f1.vergleiche_mit(f4)

        print(f"Vergleich: f1(x) = {f1.term()}")
        print(f"         mit: f4(x) = {f4.term()}")
        print(f"Gleich: {vergleich['gleichheit']}")
        print(f"Typen gleich: {vergleich['typ_gleich']}")

        if vergleich["differenz"]:
            print(f"Differenz: {vergleich['differenz']['ist_null']}")
    except Exception as e:
        print(f"Vergleichsfehler: {e}")

    # === Phase 2: Spezialisierte Funktionen ===
    print("\n🔧 Phase 2: Spezialisierte Funktionen")
    print("-" * 37)

    # Parametrisierte Funktion
    try:
        from schul_analysis.funktion import Funktion

        f_param = Funktion("a*x^2 + b*x + c")

        print(f"Parametrisiert: {f_param.term()}")

        if f_param.parameter:
            param_names = [p.name for p in f_param.parameter]
            print(f"Parameter: {', '.join(param_names)}")

            # Spezialisieren
            f_spezial = f_param.spezialisiere_parameter(a=1, b=2, c=1)
            print(f"Spezialisiert (a=1, b=2, c=1): {f_spezial.term()}")
    except Exception as e:
        print(f"Parameterfehler: {e}")

    print("\n🎉 Phase 2 Demo abgeschlossen!")
    print(
        "\nHinweis: Einige erweiterte Funktionen benötigen zusätzliche Abhängigkeiten"
    )
    print("wie plotly für die Visualisierung oder die vollständige Funktion-Klasse.")


if __name__ == "__main__":
    main()
