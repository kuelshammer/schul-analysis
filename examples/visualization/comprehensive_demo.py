"""
Comprehensive Visualization Examples

Dieses Beispiel zeigt die verschiedenen Visualisierungsmöglichkeiten des modernen Schul-Analysis Frameworks,
einschließlich intelligenter Skalierung, spezieller Punkte und Plotly-Integration.
"""

from schul_analysis import Extrema, Funktion, Nullstellen, wendepunkte


def demo_basic_visualization():
    """Grundlegende Visualisierung mit automatischer Skalierung"""
    print("=== 1. Grundlegende Visualisierung ===")

    # Funktion mit verschiedenen interessanten Punkten
    f = Funktion("x^3 - 3x^2 - 9x + 5")

    print(f"Funktion: f(x) = {f.term()}")
    print("Intelligente Skalierung erkennt automatisch:")
    print("- Nullstellen")
    print("- Extremstellen")
    print("- Wendepunkte")

    # Mathematische Analyse
    print("\nMathematische Analyse:")
    print(f"Nullstellen: {Nullstellen(f)}")

    ext = Extrema(f)
    if ext:
        print("Extremstellen:")
        for x_ext, art in ext:
            y_ext = f(x_ext)
            print(f"  {art} bei ({x_ext:.2f}, {y_ext:.2f})")

    wp = wendepunkte(f)
    if wp:
        print("Wendepunkte:")
        for wendepunkt in wp:
            if len(wendepunkt) >= 2:
                xw, yw = wendepunkt[0], wendepunkt[1]
                print(f"  bei ({xw:.2f}, {yw:.2f})")

    # Visualisierung (wenn Plotly installiert)
    print("\nVisualisierung:")
    try:
        graph = f.zeige_funktion_plotly(x_bereich=(-4, 6))
        print("✓ Graph mit intelligenter Skalierung erstellt")
        print("  - Automatische Erkennung wichtiger Punkte")
        print("  - Mathematisch korrekte Proportionen")
        print("  - Optimale Achsenskalierung")
        return graph
    except ImportError:
        print("⚠️ Plotly nicht installiert")
        print("  Installieren mit: uv sync --group viz-math")
    except Exception as e:
        print(f"✗ Fehler bei der Visualisierung: {e}")

    return None


def demo_quadratic_functions():
    """Verschiedene quadratische Funktionen visualisieren"""
    print("\n=== 2. Quadratische Funktionen ===")

    # Verschiedene Parabeln
    parabeln = [
        ("Parabel aufwärts", "x^2 - 4x + 3"),
        ("Parabel abwärts", "-x^2 + 2x + 3"),
        ("Verschobene Parabel", "2x^2 - 8x + 6"),
        ("Breite Parabel", "0.5x^2 + x - 3"),
    ]

    for name, term in parabeln:
        print(f"\n{name}: {term}")
        f = Funktion(term)

        # Analyse
        null = Nullstellen(f)
        ext = Extrema(f)

        print(f"  Nullstellen: {null}")
        if ext:
            x_ext, art = ext[0]
            y_ext = f(x_ext)
            print(f"  Scheitelpunkt: ({x_ext:.2f}, {y_ext:.2f}) - {art}")

        # Visualisierung
        try:
            f.zeige_funktion_plotly(x_bereich=(-5, 5))
            print("  ✓ Graph erstellt")
        except Exception as e:
            print(f"  ✗ Visualisierung fehlgeschlagen: {e}")


def demo_comparison():
    """Funktionsvergleich mit mehreren Graphen"""
    print("\n=== 3. Funktionsvergleich ===")

    # Vergleich einer Funktion mit ihren Ableitungen
    print("Funktion und ihre Ableitungen:")

    f = Funktion("x^3 - 3x^2 - 4x + 2")
    f1 = f.Ableitung(1)  # f'
    f2 = f.Ableitung(2)  # f''

    print(f"Original:   f(x)  = {f.term()}")
    print(f"1. Ableitung: f'(x) = {f1.term()}")
    print(f"2. Ableitung: f''(x) = {f2.term()}")

    # Einzelne Graphen
    for _, (func, name) in enumerate(
        [(f, "Original"), (f1, "1. Ableitung"), (f2, "2. Ableitung")], 1
    ):
        try:
            func.zeige_funktion_plotly(x_bereich=(-3, 4))
            print(f"✓ {name} Graph erstellt")
        except Exception as e:
            print(f"✗ {name} Visualisierung fehlgeschlagen: {e}")


def demo_special_points():
    """Visualisierung mit hervorgehobenen speziellen Punkten"""
    print("\n=== 4. Spezielle Punkte hervorheben ===")

    # Funktion mit vielen interessanten Punkten
    f = Funktion("x^4 - 6x^3 + 8x^2 + 1")

    print(f"Funktion: f(x) = {f.term()}")

    # Finde alle speziellen Punkte
    null = Nullstellen(f)
    ext = Extrema(f)
    wp = wendepunkte(f)

    print(f"Nullstellen: {null}")
    print(f"Extremstellen: {ext}")
    print(f"Wendepunkte: {wp}")

    # Erstelle Graph mit allen Punkten
    try:
        graph = f.zeige_funktion_plotly(x_bereich=(-2, 5))
        print("✓ Graph mit allen speziellen Punkten erstellt")
        print("  - Nullstellen sind markiert")
        print("  - Extremstellen sind hervorgehoben")
        print("  - Wendepunkte sind sichtbar")
        return graph
    except Exception as e:
        print(f"✗ Visualisierung fehlgeschlagen: {e}")
        return None


def main():
    """Hauptfunktion mit allen Demos"""
    print("🎨 Comprehensive Visualization Examples")
    print("=" * 50)

    # Demo 1: Grundlegende Visualisierung
    graph1 = demo_basic_visualization()

    # Demo 2: Quadratische Funktionen
    demo_quadratic_functions()

    # Demo 3: Funktionsvergleich
    demo_comparison()

    # Demo 4: Spezielle Punkte
    graph4 = demo_special_points()

    print("\n" + "=" * 50)
    print("🎯 Zusammenfassung der Visualisierungs-Features:")
    print("✅ Magic Factory API für einfache Funktionserstellung")
    print("✅ Automatische mathematische Analyse")
    print("✅ Intelligente Skalierung und Proportionen")
    print("✅ Hervorhebung wichtiger Punkte")
    print("✅ Plotly-Integration für interaktive Graphen")
    print("✅ Perfekt für den Matheunterricht")

    print("\n💡 Tipp: In Jupyter/Marimo Notebooks können die Graphen interaktiv sein!")

    return graph1, graph4


if __name__ == "__main__":
    main()
