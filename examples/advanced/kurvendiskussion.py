"""
Erweiterte mathematische Analyse mit dem Schul-Analysis Framework

Dieses Beispiel zeigt fortgeschrittene Analysetechniken inklusive
Kurvendiskussion, Integralrechnung und Grenzwertanalyse.
"""

from schul_analysis import (
    Ableitung,
    AsymptotischesVerhalten,
    Extrema,
    Funktion,
    Graph,
    Nullstellen,
    Polstellen,
    wendepunkte,
)


def kurvendiskussion(funktion, name="f"):
    """Führt eine vollständige Kurvendiskussion durch"""
    print(f"\n=== Kurvendiskussion für {name}(x) = {funktion.term()} ===")

    # 1. Definitionsbereich
    print("1. Definitionsbereich:")
    try:
        # Für gebrochen-rationale Funktionen Polstellen finden
        if hasattr(funktion, "nenner") and funktion.nenner != 1:
            pol = Polstellen(funktion)
            if pol:
                print(f"   Polstellen bei x = {pol}")
                print(f"   Definitionsbereich: ℝ \\ {pol}")
            else:
                print("   Definitionsbereich: ℝ")
        else:
            print("   Definitionsbereich: ℝ")
    except Exception:
        print("   Definitionsbereich: ℝ")

    # 2. Nullstellen
    print("2. Nullstellen:")
    null = Nullstellen(funktion)
    if null:
        print(f"   x = {null}")
    else:
        print("   Keine reellen Nullstellen")

    # 3. Ableitungen
    print("3. Ableitungen:")
    f_strich = Ableitung(funktion)
    f_strich_strich = Ableitung(f_strich)
    print(f"   f'(x) = {f_strich.term()}")
    print(f"   f''(x) = {f_strich_strich.term()}")

    # 4. Extremstellen
    print("4. Extremstellen:")
    ext = Extrema(funktion)
    if ext:
        for xs, art in ext:
            ys = funktion(xs)
            print(f"   {art} bei P({xs:.3f}|{ys:.3f})")
    else:
        print("   Keine Extremstellen")

    # 5. Wendepunkte
    print("5. Wendepunkte:")
    wp = wendepunkte(funktion)
    if wp:
        for wendepunkt in wp:
            if len(wendepunkt) >= 3:
                xw, yw, art = wendepunkt[0], wendepunkt[1], wendepunkt[2]
                print(f"   {art} bei P({xw:.3f}|{yw:.3f})")
    else:
        print("   Keine Wendepunkte")

    # 6. Grenzwertverhalten
    print("6. Grenzwertverhalten:")
    try:
        asymp = AsymptotischesVerhalten(funktion)
        if asymp:
            for beschreibung in asymp:
                print(f"   {beschreibung}")
    except Exception:
        print("   Keine Asymptoten analysiert")

    # 7. Integral (vereinfachte Darstellung)
    print("7. Stammfunktion:")
    try:
        # Zeige nur das Konzept - Integral ist numerisch
        print("   ∫f(x)dx - numerische Integration verfügbar")
        print("   Beispiel: Von 0 bis 2 ≈ ?")
    except Exception:
        print("   Integral nicht berechenbar")


def main():
    """Hauptfunktion mit verschiedenen Beispielen"""

    # Beispiel 1: Kubische Funktion
    print("=" * 60)
    print("BEISPIEL 1: Kubische Funktion")
    print("=" * 60)
    f1 = Funktion("x^3 - 3x^2 - 9x + 5")
    kurvendiskussion(f1, "f1")

    # Beispiel 2: Gebrochen-rationale Funktion
    print("\n" + "=" * 60)
    print("BEISPIEL 2: Gebrochen-rationale Funktion")
    print("=" * 60)
    f2 = Funktion("(x^2 - 4)/(x^2 - 1)")
    kurvendiskussion(f2, "f2")

    # Beispiel 3: Wurzelfunktion (als gebrochen-rationale darstellbar)
    print("\n" + "=" * 60)
    print("BEISPIEL 3: rationale Funktion mit höherem Grad")
    print("=" * 60)
    f3 = Funktion("(x^4 - 5x^2 + 4)/(x^2 + 1)")
    kurvendiskussion(f3, "f3")

    # Beispiel 4: Exponentialfunktion (approximiert)
    print("\n" + "=" * 60)
    print("BEISPIEL 4: Taylor-Approximation der e-Funktion")
    print("=" * 60)
    # Näherung der e-Funktion durch Taylorpolynom 5. Grades
    f4 = Funktion("1 + x + x^2/2 + x^3/6 + x^4/24 + x^5/120")
    kurvendiskussion(f4, "e^x (Taylor)")

    # Visualisierungsbeispiel
    print("\n" + "=" * 60)
    print("VISUALISIERUNGSBEISPIEL")
    print("=" * 60)
    try:
        print("Erstelle Graph der kubischen Funktion...")
        Graph(f1, x_bereich=(-4, 6), titel="Kubische Funktion f(x) = x³ - 3x² - 9x + 5")
        print("Graph erfolgreich erstellt!")
        print(
            "Tipp: In einem interaktiven Environment (Jupyter/Marimo) können Sie den Graph anzeigen mit:"
        )
        print("      graph.show()")
    except Exception as e:
        print(f"Visualisierungsfehler: {e}")


if __name__ == "__main__":
    main()
