"""
Comprehensive Visualization Examples

Dieses Beispiel zeigt die verschiedenen Visualisierungsmöglichkeiten des Schul-Analysis Frameworks,
einschließlich intelligenter Skalierung, spezieller Punkte und Plotly-Integration.
"""

import numpy as np
from schul_analysis import (
    Funktion,
    Graph,
    Nullstellen,
    Ableitung,
    Extremstellen,
    Wendepunkte,
)


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

    try:
        # Automatische Skalierung
        graph = Graph(f)
        print("✅ Graph mit automatischer Skalierung erstellt")

        # Manueller Bereich
        graph_manual = Graph(f, x_min=-4, x_max=6, y_min=-20, y_max=15)
        print("✅ Graph mit manuellem Bereich erstellt")

        return graph, graph_manual

    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None, None


def demo_multiple_functions():
    """Visualisierung mehrerer Funktionen"""
    print("\n=== 2. Mehrere Funktionen ===")

    # Drei Funktionen zum Vergleich
    f1 = Funktion("x^2")
    f2 = Funktion("x^2 - 4")
    f3 = Funktion("x^2 + 2x + 1")

    print("Funktionen zum Vergleich:")
    print(f"f₁(x) = {f1.term()}")
    print(f"f₂(x) = {f2.term()}")
    print(f"f₃(x) = {f3.term()}")

    try:
        # Alle Funktionen in einem Graphen
        graph = Graph(f1, f2, f3, titel="Vergleich quadratischer Funktionen")
        print("✅ Vergleichsgraph erstellt")
        return graph

    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None


def demo_special_points():
    """Visualisierung mit speziellen Punkten"""
    print("\n=== 3. Spezielle Punkte hervorheben ===")

    # Funktion mit vielen interessanten Punkten
    f = Funktion("x^4 - 8x^2 + 16")

    print(f"Funktion: f(x) = {f.term()}")

    # Berechne interessante Punkte
    nullstellen = Nullstellen(f)
    extremstellen = Extremstellen(f)
    wendepunkte = Wendepunkte(f)

    print(f"Nullstellen: {nullstellen}")
    print(f"Extremstellen: {extremstellen}")
    print(f"Wendepunkte: {wendepunkte}")

    try:
        # Graph mit allen speziellen Punkten
        graph = Graph(
            f,
            x_bereich=(-3, 3),
            titel="Funktion mit speziellen Punkten",
            zeige_nullstellen=True,
            zeige_extremstellen=True,
            zeige_wendepunkte=True,
        )
        print("✅ Graph mit speziellen Punkten erstellt")
        return graph

    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None


def demo_advanced_features():
    """Erweiterte Visualisierungsfeatures"""
    print("\n=== 4. Erweiterte Features ===")

    # Komplexere Funktion
    f = Funktion("(x^2 - 4)/(x^2 - 1)")

    print(f"Funktion: f(x) = {f.term()}")
    print("Features:")
    print("- Polstellen erkennung")
    print("- Asymptoten Darstellung")
    print("- Diskontinuitäten Handling")

    try:
        # Graph mit allen Features
        graph = Graph(
            f,
            x_bereich=(-3, 3),
            titel="Gebrochen-rationale Funktion",
            zeige_polstellen=True,
            punkte=500,  # Höhere Auflösung
        )
        print("✅ Komplexer Graph erstellt")
        return graph

    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None


def demo_custom_styling():
    """Benutzerdefinierte Stile und Layouts"""
    print("\n=== 5. Benutzerdefinierte Stile ===")

    f = Funktion("sin(x)")  # Wird als Polynom angenähert

    # Annäherung der Sinusfunktion durch Taylor-Polynom
    f_sin = Funktion("x - x^3/6 + x^5/120")

    print(f"Annäherung: f(x) = {f_sin.term()}")

    try:
        # Verschiedene Stil-Optionen
        graph1 = Graph(f_sin, x_bereich=(-np.pi, np.pi), titel="Sinus-Approximation")
        graph2 = Graph(
            f_sin,
            x_bereich=(-2 * np.pi, 2 * np.pi),
            titel="Sinus-Approximation (erweiterter Bereich)",
        )

        print("✅ Verschiedene Stile erstellt")
        return graph1, graph2

    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None, None


def demo_interactive_features():
    """Interaktive Features für Exploration"""
    print("\n=== 6. Interaktive Features ===")

    f = Funktion("x^3 - 6x^2 + 11x - 6")

    print(f"Funktion: f(x) = {f.term()}")
    print("Interaktive Features:")
    print("- Zoom- und Pan-Funktionen")
    print("- Hover-Informationen")
    print("- automatische Skalierung")

    try:
        # Graph für interaktive Exploration
        graph = Graph(
            f,
            x_bereich=(0, 4),
            titel="Interaktive Exploration",
            punkte=1000,  # Hohe Auflösung für glatte Kurven
        )
        print("✅ Interaktiver Graph erstellt")

        # Plotly-spezifische Features nutzen
        if hasattr(graph, "update_layout"):
            graph.update_layout(
                hovermode="x unified", showlegend=True, width=800, height=600
            )

        return graph

    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None


def create_comparison_matrix():
    """Vergleichsmatrix verschiedener Visualisierungen"""
    print("\n=== 7. Vergleichsmatrix ===")

    # Verschiedene Funktionstypen
    funktionen = [
        ("Linear", Funktion("2x + 1")),
        ("Quadratisch", Funktion("x^2 - 4")),
        ("Kubisch", Funktion("x^3 - 3x")),
        ("Rational", Funktion("1/(x^2 + 1)")),
    ]

    graphs = []

    for name, func in funktionen:
        try:
            graph = Graph(func, titel=f"{name}: {func.term()}")
            graphs.append((name, graph))
            print(f"✅ {name}: {func.term()}")
        except Exception as e:
            print(f"❌ {name}: {e}")

    return graphs


def main():
    """Hauptfunktion - führt alle Demos aus"""

    print("🎨 Schul-Analysis Visualisierungs-Demos")
    print("=" * 50)

    # Sammle alle Graphen für die Ausgabe
    all_graphs = []

    # Demo 1: Grundlegende Visualisierung
    graph1, graph1_manual = demo_basic_visualization()
    if graph1:
        all_graphs.append(("Grundlegend", graph1))
    if graph1_manual:
        all_graphs.append(("Grundlegend (manuell)", graph1_manual))

    # Demo 2: Multiple Funktionen
    graph2 = demo_multiple_functions()
    if graph2:
        all_graphs.append(("Multiple Funktionen", graph2))

    # Demo 3: Spezielle Punkte
    graph3 = demo_special_points()
    if graph3:
        all_graphs.append(("Spezielle Punkte", graph3))

    # Demo 4: Erweiterte Features
    graph4 = demo_advanced_features()
    if graph4:
        all_graphs.append(("Erweitert", graph4))

    # Demo 5: Benutzerdefinierte Stile
    graph5_1, graph5_2 = demo_custom_styling()
    if graph5_1:
        all_graphs.append(("Sinus 1", graph5_1))
    if graph5_2:
        all_graphs.append(("Sinus 2", graph5_2))

    # Demo 6: Interaktive Features
    graph6 = demo_interactive_features()
    if graph6:
        all_graphs.append(("Interaktiv", graph6))

    # Demo 7: Vergleichsmatrix
    comparison_graphs = create_comparison_matrix()
    for name, graph in comparison_graphs:
        all_graphs.append((f"Vergleich: {name}", graph))

    print(f"\n=== Zusammenfassung ===")
    print(f"Insgesamt erstellte Graphen: {len(all_graphs)}")

    for name, graph in all_graphs:
        print(f"✅ {name}: {type(graph).__name__}")

    print("\n💡 Tipps für die Nutzung:")
    print("- In Jupyter/Marimo: graph.show() zum Anzeigen")
    print("- Als HTML exportieren: graph.write_html('datei.html')")
    print("- Als Bild exportieren: graph.write_image('datei.png')")
    print("- Interaktive Features nutzen in Plotly-kompatiblen Umgebungen")

    return all_graphs


if __name__ == "__main__":
    graphs = main()
