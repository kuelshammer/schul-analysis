"""
Schul-Analysis Framework - Einfaches Marimo Beispiel

Ein minimaler Einstieg in das Schul-Analysis Framework mit Marimo.
"""

import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell
def _():
    import os
    import sys

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    from schul_analysis import Funktion

    # Zwei einfache Funktionen für erste Experimente
    f = Funktion("x^2")
    g = Funktion("3x + 5")
    print(f"Funktion f: {f.term()}")
    print(f"Funktion g: {g.term()}")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
