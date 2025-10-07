"""
Comprehensive Visualization Examples

Dieses Beispiel zeigt die fortgeschrittenen Visualisierungsmöglichkeiten des Schul-Analysis Frameworks
mit Plotly für mathematisch korrekte Darstellungen.
"""

from schul_analysis import (
    Ableitung,
    Extremstellen,
    Funktion,
    Graph,
    Nullstellen,
    Wendepunkte,
)


def example_perfect_parabola():
    """Beispiel: Perfekte Parabel-Darstellung"""
    print("=== Beispiel 1: Perfekte Parabel-Darstellung ===")

    # Verschiedene Parabeln
    parabeln = [
        ("x^2", "Standardparabel"),
        ("(x-2)^2 + 1", "verschobene Parabel"),
        ("-x^2 + 4x - 3", "nach unten geöffnete Parabel"),
        ("2x^2 - 8x + 6", "gestreckte Parabel"),
    ]

    for term, beschreibung in parabeln:
        print(f"\n{beschreibung}: f(x) = {term}")
        f = Funktion(term)

        # Berechne Eigenschaften
        nullstellen = Nullstellen(f)
        extremstellen = Extremstellen(f)

        print(f"Nullstellen: {nullstellen}")
        print(f"Scheitelpunkt: {extremstellen}")

        # Erstelle Graph
        try:
            Graph(f, titel=f"{beschreibung}: f(x) = {term}")
            print("✓ Graph erstellt")
        except Exception as e:
            print(f"✗ Fehler: {e}")


def example_multiple_functions():
    """Beispiel: Mehrere Funktionen in einem Graphen"""
    print("\n=== Beispiel 2: Vergleich von Funktionen ===")

    # Erstelle mehrere Funktionen zum Vergleich
    f1 = Funktion("x^2")  # Parabel
    f2 = Funktion("x^3")  # Kubische Funktion
    f3 = Funktion("sin(x)")  # Sinus (als Taylor-Approximation)

    # Annäherung von sin(x) durch Taylor-Polynom
    f3 = Funktion("x - x^3/6 + x^5/120")

    print("Funktionen zum Vergleich:")
    print(f"f₁(x) = {f1.term()}")
    print(f"f₂(x) = {f2.term()}")
    print(f"f₃(x) = {f3.term()} (sin(x) Taylor)")

    try:
        # Erstelle Graph mit allen Funktionen
        Graph(
            f1,
            f2,
            f3,
            x_bereich=(-3, 3),
            titel="Vergleich: Parabel, Kubisch, Sinus-Approximation",
        )
        print("✓ Vergleichsgraph erstellt")
    except Exception as e:
        print(f"✗ Fehler: {e}")


def example_rational_functions():
    """Beispiel: Gebrochen-rationale Funktionen mit Polstellen"""
    print("\n=== Beispiel 3: Gebrochen-rationale Funktionen ===")

    rationale_funktionen = [
        ("(x^2 - 4)/(x - 2)", "mit hebbarem Pol"),
        ("1/(x^2 + 1)", "keine reellen Pole"),
        ("x/(x^2 - 1)", "mit zwei Polstellen"),
        ("(x^2 - 1)/(x^2 + 1)", "rationale Funktion ohne reelle Pole"),
    ]

    for term, beschreibung in rationale_funktionen:
        print(f"\n{beschreibung}: f(x) = {term}")
        f = Funktion(term)

        try:
            # TODO: Polstellen ist noch nicht implementiert
            # from schul_analysis import Polstellen
            # polstellen = Polstellen(f)
            # print(f"Polstellen: {polstellen}")
            pass

            # Erstelle Graph mit angepasstem Bereich
            if "1/(x^2 + 1)" in term:
                bereich = (-3, 3)
            elif "x/(x^2 - 1)" in term:
                bereich = (-2, 2)
            else:
                bereich = (-5, 5)

            Graph(f, x_bereich=bereich, titel=f"{beschreibung}")
            print("✓ Graph erstellt")
        except Exception as e:
            print(f"✗ Fehler: {e}")


def example_derivatives_analysis():
    """Beispiel: Ableitungsanalyse mit Mehrfachdarstellung"""
    print("\n=== Beispiel 4: Ableitungsanalyse ===")

    # Komplexere Funktion
    f = Funktion("x^4 - 4x^3 + 2x^2 + 4x - 3")
    print(f"Funktion: f(x) = {f.term()}")

    # Berechne Ableitungen
    f_strich = Ableitung(f)
    f_strich_strich = Ableitung(f_strich)
    f_strich_strich_strich = Ableitung(f_strich_strich)

    print(f"f'(x) = {f_strich.term()}")
    print(f"f''(x) = {f_strich_strich.term()}")
    print(f"f'''(x) = {f_strich_strich_strich.term()}")

    # Analyse
    nullstellen = Nullstellen(f)
    extremstellen = Extremstellen(f)
    wendepunkte = Wendepunkte(f)

    print(f"\nNullstellen: {nullstellen}")
    print(f"Extremstellen: {extremstellen}")
    print(f"Wendepunkte: {wendepunkte}")

    # Erstelle Graphen
    try:
        # Originalfunktion
        Graph(f, x_bereich=(-2, 4), titel="Funktion f(x)")
        print("✓ Graph von f(x) erstellt")

        # Erste Ableitung
        Graph(f_strich, x_bereich=(-2, 4), titel="Erste Ableitung f'(x)")
        print("✓ Graph von f'(x) erstellt")

        # Zweite Ableitung
        Graph(f_strich_strich, x_bereich=(-2, 4), titel="Zweite Ableitung f''(x)")
        print("✓ Graph von f''(x) erstellt")

    except Exception as e:
        print(f"✗ Fehler: {e}")


def example_asymptotic_behavior():
    """Beispiel: Asymptotisches Verhalten"""
    print("\n=== Beispiel 5: Asymptotisches Verhalten ===")

    # Funktionen mit unterschiedlichem asymptotischem Verhalten
    asymptotisch = [
        ("(2x + 1)/(x - 3)", "Hyperbel"),
        ("(x^2 + 1)/x", "Schiefe Asymptote"),
        ("x^2/(x^2 + 1)", "Horizontale Asymptote"),
        ("1/x^2", "Vertikale Asymptote"),
    ]

    for term, beschreibung in asymptotisch:
        print(f"\n{beschreibung}: f(x) = {term}")
        f = Funktion(term)

        try:
            # TODO: AsymptotischesVerhalten ist noch nicht implementiert
            # from schul_analysis import AsymptotischesVerhalten
            # asymptoten = AsymptotischesVerhalten(f)
            #
            # if asymptoten:
            #     print("Asymptoten:")
            #     for asymp in asymptoten:
            #         print(f"  - {asymp}")
            pass

            # Erstelle Graph
            if "Hyperbel" in beschreibung:
                bereich = (-5, 8)  # Stelle Pol bei x=3 dar
            elif "Schiefe" in beschreibung:
                bereich = (-5, 5)
            elif "x^2" in term:
                bereich = (-3, 3)
            else:
                bereich = (-4, 4)

            Graph(f, x_bereich=bereich, titel=f"{beschreibung}: f(x) = {term}")
            print("✓ Graph erstellt")
        except Exception as e:
            print(f"✗ Fehler: {e}")


def main():
    """Hauptfunktion - führt alle Beispiele aus"""

    print("🎓 Schul-Analysis Framework - Visualisierungsbeispiele")
    print("=" * 60)
    print("Dieses Beispiel zeigt die fortgeschrittenen Visualisierungsmöglichkeiten")
    print("mit Plotly für mathematisch korrekte Darstellungen.")
    print("=" * 60)

    # Führe alle Beispiele aus
    example_perfect_parabola()
    example_multiple_functions()
    example_rational_functions()
    example_derivatives_analysis()
    example_asymptotic_behavior()

    print("\n" + "=" * 60)
    print("✅ Alle Visualisierungsbeispiele abgeschlossen")
    print("\n💡 Tipps:")
    print("   - In interaktiven Umgebungen (Jupyter/Marimo) können Sie")
    print("     die Graphen mit graph.show() anzeigen")
    print("   - Passen Sie die x_bereich-Parameter an Ihre Bedürfnisse an")
    print("   - Nutzen Sie die intelligenten Skalierungsfunktionen für")
    print("     optimale Darstellungen")
    print("=" * 60)


if __name__ == "__main__":
    main()
