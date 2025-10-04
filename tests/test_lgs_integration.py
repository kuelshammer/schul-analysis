#!/usr/bin/env python3
"""
Test für die automatische Symbolerkennung in GanzrationaleFunktion und LGS-Integration
"""

import sys

sys.path.insert(0, "src")

from schul_analysis import GanzrationaleFunktion, LGS


def test_lgs_integration():
    """Test der Integration zwischen GanzrationaleFunktion und LGS"""
    print("=== Test LGS Integration ===")

    # Test: Funktion mit Parametern und LGS kombinieren
    print("\n1. Test: f = GanzrationaleFunktion('a x^2 + b x + c')")
    try:
        f = GanzrationaleFunktion("a x^2 + b x + c")
        print(f"   Term: {f.term()}")
        print(f"   Hauptvariable: {f.hauptvariable}")
        print(f"   Parameter: {[str(p) for p in f.parameter]}")
        print(f"   Variablen: {[str(v) for v in f.variablen]}")

        # Erstelle Bedingungen für LGS
        if f.parameter and f.hauptvariable:
            print(f"   Mögliche LGS-Bedingungen:")
            print(f"   - f(0) = {f.wert(0)} (Parameter vorhanden)")
            print(f"   - f(1) = {f.wert(1)} (Parameter vorhanden)")
            print(f"   - f(2) = {f.wert(2)} (Parameter vorhanden)")

    except Exception as e:
        print(f"   Fehler: {e}")

    # Test: Einfache lineare Funktion mit Parameter
    print("\n2. Test: g = GanzrationaleFunktion('a t + b')")
    try:
        g = GanzrationaleFunktion("a t + b")
        print(f"   Term: {g.term()}")
        print(f"   Hauptvariable: {g.hauptvariable}")
        print(f"   Parameter: {[str(p) for p in g.parameter]}")
        print(f"   Variablen: {[str(v) for v in g.variablen]}")

    except Exception as e:
        print(f"   Fehler: {e}")

    # Test: Versuche LGS mit erkannten Parametern
    print("\n3. Test: LGS mit automatisch erkannten Parametern")
    try:
        # Hier müsste später die Integration mit ParametrischeFunktion entstehen
        print(
            "   Hinweis: Volle LGS-Integration benötigt noch ParametrischeFunktion-Anbindung"
        )
        print(
            "   Grund: GanzrationaleFunktion verwendet interne _Variable/_Parameter Klassen"
        )
        print(
            "   Lösung: Konvertierung zu echten ParametrischeFunktionen oder Erweiterung von LGS"
        )

    except Exception as e:
        print(f"   Fehler: {e}")


if __name__ == "__main__":
    test_lgs_integration()
    print("\n=== Test abgeschlossen ===")
