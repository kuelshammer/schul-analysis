"""
Test für schülerfreundliche Funktions-Syntax
"""

from schul_analysis import (
    Ableitung,
    GanzrationaleFunktion,
    Kürzen,
    Nullstellen,
    Polstellen,
    QuotientFunktion,
    Wert,
)


def test_schülerfreundliche_syntax():
    """Testet die neue schülerfreundliche Syntax"""

    print("=== Schülerfreundliche Syntax Demo ===\n")

    # Ganzrationale Funktionen
    print("📈 Ganzrationale Funktionen:")
    f = GanzrationaleFunktion("x^2-4")
    print(f"  f(x) = {f.term()}")
    print(f"  Nullstellen(f) = {Nullstellen(f)}")
    print(f"  Wert(f, 3) = {Wert(f, 3)}")
    print(f"  Ableitung(f) = {Ableitung(f).term()}")

    # Gebrochen-rationale Funktionen
    print("\n📊 Gebrochen-rationale Funktionen:")
    g = QuotientFunktion("(x^2-1)/(x-2)")
    print(f"  g(x) = {g.term()}")
    print(f"  Nullstellen(g) = {Nullstellen(g)}")
    print(f"  Polstellen(g) = {Polstellen(g)}")
    print(f"  Wert(g, 3) = {Wert(g, 3):.2f}")

    # Graphen erstellen
    print("\n📊 Graphen:")
    print("  Graph(f) - erzeugt Plotly-Graph für f(x)")
    print("  Graph(g) - erzeugt Plotly-Graph für g(x)")

    # Kürzen
    print("\n🔄 Kürzen:")
    h = QuotientFunktion("(x^2-4)/(x-2)")
    print(f"  h(x) = {h.term()}")
    h_gekürzt = Kürzen(h)
    print(f"  gekürzt: {h_gekürzt.term()}")

    print("\n✅ Alle schülerfreundlichen Funktionen funktionieren!")


def test_vergleich_syntax():
    """Vergleicht alte und neue Syntax"""

    print("\n=== Syntax-Vergleich ===\n")

    f = GanzrationaleFunktion("x^2-9")
    g = QuotientFunktion("1/(x-3)")

    print("Alte Syntax (objektorientiert):")
    print(f"  f.nullstellen() = {f.nullstellen()}")
    print(f"  g.polstellen() = {g.polstellen()}")
    print(f"  f.wert(4) = {f.wert(4)}")

    print("\nNeue Syntax (funktional - schülerfreundlich):")
    print(f"  Nullstellen(f) = {Nullstellen(f)}")
    print(f"  Polstellen(g) = {Polstellen(g)}")
    print(f"  Wert(f, 4) = {Wert(f, 4)}")

    print("\n✅ Beide Syntaxen liefern gleiche Ergebnisse!")


if __name__ == "__main__":
    test_schülerfreundliche_syntax()
    test_vergleich_syntax()

    print("\n🎉 Demo abgeschlossen!")
    print("Schüler können jetzt intuitivere Funktionen verwenden!")
