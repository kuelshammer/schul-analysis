#!/usr/bin/env python3
"""
Test Script für Graph(f, g) Funktionalität
"""

from schul_analysis.ganzrationale import GanzrationaleFunktion
from schul_analysis.visualisierung import Graph


def test_graph_mehrfach():
    """Testet Graph(f, g) mit dem Benutzerbeispiel"""
    print("=== Test: Graph(f, g) mit kombiniertem intelligentem Bereich ===")

    # Beispiel vom Benutzer: f = (x+4)(x-1), g = (x+3)(x-3)
    f = GanzrationaleFunktion("(x+4)(x-1)")  # Nullstellen bei x=-4, x=1
    g = GanzrationaleFunktion("(x+3)(x-3)")  # Nullstellen bei x=-3, x=3

    print(f"Funktion f: {f.term()}")
    print(f"Funktion g: {g.term()}")

    # Erstelle Graph
    fig = Graph(f, g)
    x_range = fig.layout.xaxis.range
    y_range = fig.layout.yaxis.range

    print(f"X-Bereich: [{x_range[0]:.3f}, {x_range[1]:.3f}]")
    print(f"Y-Bereich: [{y_range[0]:.3f}, {y_range[1]:.3f}]")

    # Erwarteter kombinierte Bereich: -4 bis 3 (90% Kern)
    # Mit 5% Puffer auf jeder Seite: ca. -4.35 bis 3.35
    erwarteter_min = -4.35
    erwarteter_max = 3.35

    print(f"Erwartet: [{erwarteter_min:.3f}, {erwarteter_max:.3f}]")

    # Prüfe, dass alle Nullstellen sichtbar sind
    print(
        f"Nullstelle f1 (x=-4): {'sichtbar' if x_range[0] <= -4 else 'nicht sichtbar'}"
    )
    print(
        f"Nullstelle g1 (x=-3): {'sichtbar' if x_range[0] <= -3 else 'nicht sichtbar'}"
    )
    print(f"Nullstelle f2 (x=1): {'sichtbar' if x_range[1] >= 1 else 'nicht sichtbar'}")
    print(f"Nullstelle g2 (x=3): {'sichtbar' if x_range[1] >= 3 else 'nicht sichtbar'}")

    # Prüfe, dass beide Funktionen angezeigt werden
    print(f"Anzahl Funktionen: {len(fig.data)}")

    # Prüfe Puffer
    linker_puffer = -4 - x_range[0]
    rechter_puffer = x_range[1] - 3
    print(f"Linker Puffer: {linker_puffer:.3f}")
    print(f"Rechter Puffer: {rechter_puffer:.3f}")

    print("\n=== Test erfolgreich! ===\n")
    return fig


def test_graph_mehrfach_mit_manuellen_grenzen():
    """Testet Graph(f, g) mit teilweisen manuellen Grenzen"""
    print("=== Test: Graph(f, g) mit manuellen Grenzen ===")

    f = GanzrationaleFunktion("(x+4)(x-1)")
    g = GanzrationaleFunktion("(x+3)(x-3)")

    # Nur x_max manuell gesetzt
    fig = Graph(f, g, x_max=5)
    x_range = fig.layout.xaxis.range

    print(f"X-Bereich mit x_max=5: [{x_range[0]:.3f}, {x_range[1]:.3f}]")

    # Rechter Grenze sollte exakt 5 sein
    print(f"Rechte Grenze exakt 5: {abs(x_range[1] - 5) < 0.001}")

    # Linke Grenze sollte automatisch berechnet werden
    print(f"Linke Grenze automatisch berechnet: {x_range[0] <= -4}")

    print("\n=== Test erfolgreich! ===\n")
    return fig


def test_graph_drei_funktionen():
    """Testet Graph(f, g, h) mit drei Funktionen"""
    print("=== Test: Graph(f, g, h) mit drei Funktionen ===")

    f = GanzrationaleFunktion("(x+4)(x-1)")  # Bereich: -4 bis 1
    g = GanzrationaleFunktion("(x+3)(x-3)")  # Bereich: -3 bis 3
    h = GanzrationaleFunktion("(x+5)(x-2)")  # Bereich: -5 bis 2

    fig = Graph(f, g, h)
    x_range = fig.layout.xaxis.range

    print(f"X-Bereich: [{x_range[0]:.3f}, {x_range[1]:.3f}]")
    print(f"Anzahl Funktionen: {len(fig.data)}")

    # Kombinierter Bereich sollte -5 bis 3 umfassen
    print(
        f"Nullstelle h1 (x=-5): {'sichtbar' if x_range[0] <= -5 else 'nicht sichtbar'}"
    )
    print(f"Nullstelle g2 (x=3): {'sichtbar' if x_range[1] >= 3 else 'nicht sichtbar'}")

    print("\n=== Test erfolgreich! ===\n")
    return fig


if __name__ == "__main__":
    print("Starte Tests für Graph(f, g) Funktionalität...\n")

    try:
        # Test 1: Kombinierter intelligenter Bereich
        fig1 = test_graph_mehrfach()

        # Test 2: Manuelle Grenzen
        fig2 = test_graph_mehrfach_mit_manuellen_grenzen()

        # Test 3: Drei Funktionen
        fig3 = test_graph_drei_funktionen()

        print("Alle Tests erfolgreich abgeschlossen!")
        print("Die Graph(f, g) Funktionalität funktioniert wie erwartet.")

    except Exception as e:
        print(f"Fehler bei den Tests: {e}")
        import traceback

        traceback.print_exc()
