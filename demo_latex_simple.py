#!/usr/bin/env python3
"""
Demonstration der LaTeX-Darstellung in Marimo

Dieses Beispiel zeigt die neue latex_display() Methode und Term() Wrapper-Funktion.
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

from schul_analysis import Funktion, Term


def demo_latex_display():
    """Demonstriert die latex_display() Methode"""
    print("=== latex_display() Methode ===")

    # Teste verschiedene Funktionstypen
    test_funktionen = [
        ("Quadratische Funktion", "x^2 - 4x + 3"),
        ("Lineare Funktion", "2*x + 5"),
        ("Exponentialfunktion", "exp(x) + 1"),
        ("Trigonometrische Funktion", "sin(x) + cos(x)"),
        ("Gebrochen-rationale Funktion", "(x^2 - 1)/(x - 1)"),
        ("Kubische Funktion", "x^3 - 3*x^2 + 2*x"),
    ]

    for beschreibung, term in test_funktionen:
        try:
            f = Funktion(term)
            latex_str = f.latex_display()
            print(f"{beschreibung}:")
            print(f"  f(x) = {term}")
            print(f"  LaTeX: {latex_str}")
            print()
        except Exception as e:
            print(f"Fehler bei {beschreibung}: {e}")
            print()


def demo_term_wrapper():
    """Demonstriert die Term() Wrapper-Funktion"""
    print("=== Term() Wrapper-Funktion ===")

    f = Funktion("x^2 - 4x + 3")

    try:
        # Term() gibt ein Marimo-Markdown-Objekt zurück
        result = Term(f)
        print(f"Term(f) Typ: {type(result)}")
        print(f"Term(f) Inhalt: {result}")
        print()

        # Teste mit anderer Funktion
        g = Funktion("sin(x) + cos(x)")
        result2 = Term(g)
        print(f"Term(g) Typ: {type(result2)}")
        print(f"Term(g) Inhalt: {result2}")

    except Exception as e:
        print(f"Fehler bei Term(): {e}")


def demo_marimo_usage():
    """Zeigt, wie man die Funktionen in Marimo verwenden würde"""
    print("=== Verwendung in Marimo ===")
    print("""
In einem Marimo-Notebook könntest du schreiben:

```python
import marimo as mo
from schul_analysis import Funktion, Term

# Erstelle Funktionen
f = Funktion("x^2 - 4x + 3")
g = Funktion("2*x + 1")

# Zeige schöne LaTeX-Darstellung
Term(f)
Term(g)

# Arithmetische Operationen funktionieren weiterhin
h = f + g  # Gibt SymPy-Ausdruck zurück
Term(h)    # Zeigt Ergebnis in LaTeX
```

Vorteile dieser Lösung:
✅ Term(f) zeigt schöne LaTeX-Darstellung in Marimo
✅ Funktionen geben SymPy-Ausdrücke für Arithmetik zurück
✅ Keine Konflikte mit bestehendem Code
✅ Funktioniert auch ohne Marimo (Fallback zu String)
""")


if __name__ == "__main__":
    print("=== LaTeX-Darstellung für Marimo Demo ===\n")

    demo_latex_display()
    print()
    demo_term_wrapper()
    print()
    demo_marimo_usage()

    print("=== Demo abgeschlossen ===")
