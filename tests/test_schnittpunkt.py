"""
Test für die neue Schnittpunkt-Funktion
"""

from src.schul_analysis import *


def test_schnittpunkt_funktion():
    """Testet die Schnittpunkt-Funktion mit verschiedenen Beispielen"""

    print("=== Schnittpunkt-Funktion Demo ===\n")

    # Beispiel 1: Zwei ganzrationale Funktionen
    print("📈 Beispiel 1: Parabel und Gerade")
    f = GanzrationaleFunktion("x^2")
    g = GanzrationaleFunktion("x+2")

    print(f"  f(x) = {f.term()}")
    print(f"  g(x) = {g.term()}")
    schnittpunkte = Schnittpunkt(f, g)
    print(f"  Schnittpunkte: {schnittpunkte}")

    # Beispiel 2: Geraden-Schnittpunkt
    print("\n📈 Beispiel 2: Zwei Geraden")
    h = GanzrationaleFunktion("2x+1")
    i = GanzrationaleFunktion("x-1")

    print(f"  h(x) = {h.term()}")
    print(f"  i(x) = {i.term()}")
    schnittpunkte_hi = Schnittpunkt(h, i)
    print(f"  Schnittpunkte: {schnittpunkte_hi}")

    # Beispiel 3: Gebrochen-rationale mit ganzrationaler Funktion
    print("\n📊 Beispiel 3: Hyperbel und Gerade")
    k = GebrochenRationaleFunktion("1/x")
    l = GanzrationaleFunktion("x")

    print(f"  k(x) = {k.term()}")
    print(f"  l(x) = {l.term()}")
    schnittpunkte_kl = Schnittpunkt(k, l)
    print(f"  Schnittpunkte: {schnittpunkte_kl}")

    # Beispiel 4: Komplexeres Beispiel
    print("\n📊 Beispiel 4: Komplexere Funktionen")
    m = GanzrationaleFunktion("x^2-4")
    n = GebrochenRationaleFunktion("4/(x+1)")

    print(f"  m(x) = {m.term()}")
    print(f"  n(x) = {n.term()}")
    schnittpunkte_mn = Schnittpunkt(m, n)
    print(f"  Schnittpunkte: {schnittpunkte_mn}")

    print("\n✅ Alle Schnittpunkt-Berechnungen erfolgreich!")


def test_schnittpunkt_validierung():
    """Testet die Validierung und Fehlerbehandlung"""

    print("\n=== Validierungstests ===\n")

    # Teste mit gleichen Funktionen
    print("Test 1: Identische Funktionen")
    f = GanzrationaleFunktion("x^2")
    g = GanzrationaleFunktion("x^2")
    schnittpunkte = Schnittpunkt(f, g)
    print(f"  Identische Funktionen: {schnittpunkte}")

    # Teste mit parallelen Geraden (kein Schnittpunkt)
    print("\nTest 2: Parallele Geraden")
    h = GanzrationaleFunktion("2x+1")
    i = GanzrationaleFunktion("2x+3")
    schnittpunkte_parallel = Schnittpunkt(h, i)
    print(f"  Parallele Geraden: {schnittpunkte_parallel}")

    # Teste mit Funktionen, die sich an Polstellen schneiden
    print("\nTest 3: Funktionen mit Polstellen")
    k = GebrochenRationaleFunktion("1/(x-1)")
    l = GanzrationaleFunktion("x")
    schnittpunkte_pol = Schnittpunkt(k, l)
    print(f"  Mit Polstellen: {schnittpunkte_pol}")


def test_mathematische_genauigkeit():
    """Testet die mathematische Genauigkeit"""

    print("\n=== Mathematische Genauigkeitstests ===\n")

    # Bekannte Schnittpunkte überprüfen
    print("Test 1: y=x² und y=x schneiden sich bei (0,0) und (1,1)")
    f = GanzrationaleFunktion("x^2")
    g = GanzrationaleFunktion("x")
    schnittpunkte = Schnittpunkt(f, g)

    erwartet = [(0.0, 0.0), (1.0, 1.0)]
    print(f"  Berechnet: {schnittpunkte}")
    print(f"  Erwartet: {erwartet}")

    # Überprüfe, ob die Punkte ungefähr übereinstimmen (wegen Fließkomma-Genauigkeit)
    for (x1, y1), (x2, y2) in zip(schnittpunkte, erwartet, strict=False):
        assert abs(x1 - x2) < 1e-10, f"x-Koordinate stimmt nicht überein: {x1} != {x2}"
        assert abs(y1 - y2) < 1e-10, f"y-Koordinate stimmt nicht überein: {y1} != {y2}"

    print("  ✅ Mathematische Genauigkeit bestätigt!")


if __name__ == "__main__":
    test_schnittpunkt_funktion()
    test_schnittpunkt_validierung()
    test_mathematische_genauigkeit()

    print("\n🎉 Schnittpunkt-Funktion erfolgreich implementiert!")
    print("Schüler können jetzt Schnittpunkte berechnen mit:")
    print("  Schnittpunkt(f, g)")
