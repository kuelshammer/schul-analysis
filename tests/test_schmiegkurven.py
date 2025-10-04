"""
Test und Beispiele für Schmiegkurven im Schul-Analysis Framework.

Dieses Skript demonstriert die verschiedenen Möglichkeiten der Schmiegkurven-Erstellung
und zeigt pädagogische Anwendungen.
"""

from src.schul_analysis import (
    HermiteInterpolation,
    Schmieggerade,
    Schmiegkegel,
    SchmiegkurveAllgemein,
    Schmiegparabel,
)


def test_schmiegparabel_drei_punkte():
    """Test: Schmiegparabel durch drei Punkte"""
    print("=== Test 1: Schmiegparabel durch drei Punkte ===")

    # Drei Punkte auf der Parabel y = x²
    p1, p2, p3 = (0, 0), (1, 1), (2, 4)

    parabel = Schmiegparabel(p1, p2, p3)
    print(f"Erzeugte Parabel: f(x) = {parabel.term}")
    print("Erwartet: x²")

    # Validierung
    validierung = parabel.validiere_loesung()
    print(f"Validierung: {validierung}")

    # Prüfe Punkte
    for i, (x, y) in enumerate([p1, p2, p3]):
        berechnet = parabel.wert(x)
        print(f"P{i + 1}({x}, {y}): Berechnet = {berechnet:.6f}, Erwartet = {y}")

    print()


def test_schmiegparabel_mit_tangente():
    """Test: Schmiegparabel mit Tangentenbedingungen"""
    print("=== Test 2: Schmiegparabel mit Tangentenbedingung ===")

    # Parabel durch (0,0) mit horizontaler Tangente und (2,0)
    #     parabel = Schmiegparabel((0, 0), (1, -1), (2, 0), tangente1=0)
    #     print(f"Erzeugte Parabel: f(x) = {parabel.term}")
    #     print(f"Erwartet: x² - 2x")
    #
    #     # Prüfe Tangente bei x=0
    #     ableitung = parabel.ableitung()
    #     tangente_0 = ableitung.wert(0)
    #     print(f"Tangente bei x=0: {tangente_0:.6f} (erwartet: 0)")

    print()


def test_schmieggerade():
    """Test: Schmieggerade"""
    print("=== Test 3: Schmieggerade ===")

    # Gerade durch (1, 1) mit Steigung 2
    gerade = Schmieggerade((1, 1), 2)
    print(f"Erzeugte Gerade: f(x) = {gerade.term}")
    print("Erwartet: 2x - 1")

    # Prüfe Punkt und Steigung
    print(f"f(1) = {gerade.wert(1):.6f} (erwartet: 1)")

    ableitung = gerade.ableitung()
    print(f"f'(x) = {ableitung.term} (erwartet: 2)")

    print()


def test_hermite_interpolation():
    """Test: Hermite-Interpolation"""
    print("=== Test 4: Hermite-Interpolation ===")

    # Interpoliere mit Funktionswerten und Ableitungen
    x_werte = [0, 1]
    y_werte = [0, 1]
    y_ableitungen = [0, 0]  # Horizontale Tangenten

    hermite = HermiteInterpolation(x_werte, y_werte, y_ableitungen)
    print(f"Hermite-Polynom: f(x) = {hermite.term}")

    # Validierung
    validierung = hermite.validiere_loesung()
    print(f"Validierung: {validierung}")

    print()


def test_schmiegkegel_vier_punkte():
    """Test: Schmiegkegel durch vier Punkte"""
    print("=== Test 5: Schmiegkegel durch vier Punkte ===")

    # Vier Punkte auf y = x³
    punkte = [(0, 0), (1, 1), (2, 8), (3, 27)]

    kegel = Schmiegkegel(punkte)
    print(f"Erzeugter Kegel: f(x) = {kegel.term}")
    print("Erwartet: x³")

    # Prüfe alle Punkte
    for i, (x, y) in enumerate(punkte):
        berechnet = kegel.wert(x)
        print(f"P{i + 1}({x}, {y}): Berechnet = {berechnet:.6f}, Erwartet = {y}")

    print()


def test_schmiegkurve_mit_normalen():
    """Test: Schmiegkurve mit Normalenbedingungen"""
    print("=== Test 6: Schmiegkurve mit Normalen ===")

    # Zwei Punkte mit Normalenbedingungen
    # Normale -1 bedeutet Tangente 1 (y = x)
    # Normale -0.5 bedeutet Tangente 2 (y = 2x)
    punkte = [(0, 0), (1, 1)]
    normalen = [-1, -0.5]

    kurve = SchmiegkurveAllgemein(punkte, normalen=normalen)
    print(f"Erzeugte Kurve: f(x) = {kurve.term}")

    # Prüfe Normalen (Tangenten sollten senkrecht sein)
    ableitung = kurve.ableitung()
    for i, (x, y) in enumerate(punkte):
        tangente = ableitung.wert(x)
        normale = normalen[i]
        produkt = tangente * normale
        print(
            f"P{i + 1}: Tangente = {tangente:.6f}, Normale = {normale}, Produkt = {produkt:.6f} (erwartet: -1)"
        )

    print()


def test_paedagogisches_beispiel():
    """Pädagogisches Beispiel: Schmiegparabel für die Klasse"""
    print("=== Pädagogisches Beispiel: Schmiegparabel im Unterricht ===")

    # Aufgabe: Finde eine Parabel durch A(0,1), B(1,2), C(2,5)
    A, B, C = (0, 1), (1, 2), (2, 5)

    print("Gegeben: Punkte A(0,1), B(1,2), C(2,5)")
    print("Gesucht: Parabel f(x) = ax² + bx + c durch diese Punkte")

    parabel = Schmiegparabel(A, B, C)
    print(f"\nLösung: f(x) = {parabel.term}")

    # Zeige das Gleichungssystem
    print("\nGleichungssystem:")
    print(80 * "-")
    print(parabel.zeige_gleichungssystem())
    print(80 * "-")

    # Validiere die Lösung
    validierung = parabel.validiere_loesung()
    print(f"\nValidierung: {validierung}")

    # Zeige wichtige Eigenschaften
    print("\nEigenschaften der Parabel:")
    print(f"- Scheitelpunktform: {parabel.term}")
    print(f"- Nullstellen: {parabel.nullstellen()}")
    print(f"- y-Achsenabschnitt: {parabel.wert(0)}")

    ableitung = parabel.ableitung()
    print(f"- Ableitung: f'(x) = {ableitung.term}")

    print()


def test_fehlerbehandlung():
    """Test der Fehlerbehandlung"""
    print("=== Test 7: Fehlerbehandlung ===")

    try:
        # Zu viele Punkte für Schmiegkegel
        Schmiegkegel([(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)])
    except Exception as e:
        print(f"Erwarteter Fehler: {e}")

    try:
        # Widersprüchliche Tangente und Normale
        SchmiegkurveAllgemein(
            [(0, 0)],
            tangenten=[1],
            normalen=[1],  # Nicht senkrecht zu Tangente
        )
    except Exception as e:
        print(f"Erwarteter Fehler: {e}")

    print()


def main():
    """Führt alle Tests durch"""
    print("Schul-Analysis Framework: Schmiegkurven Tests")
    print("=" * 60)

    test_schmiegparabel_drei_punkte()
    test_schmiegparabel_mit_tangente()
    test_schmieggerade()
    test_hermite_interpolation()
    test_schmiegkegel_vier_punkte()
    test_schmiegkurve_mit_normalen()
    test_paedagogisches_beispiel()
    test_fehlerbehandlung()

    print("=" * 60)
    print("Alle Tests abgeschlossen!")


if __name__ == "__main__":
    main()
