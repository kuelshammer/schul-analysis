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

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

    from schul_analysis import Funktion, Term

    # Zwei einfache Funktionen für erste Experimente
    f = Funktion("x^2 -4x+3")
    g = Funktion("3x + 5")
    return Term, f, g


@app.cell
def _(f, g):
    h = f/g
    return (h,)


@app.cell
def _(Term, h):
    Term(h)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
