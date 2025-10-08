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

    from schul_analysis import (
        Ableitung,
        Ausmultiplizieren,
        Funktion,
        Term,
        Wendepunkte,
        Graph,
    )

    # Zwei einfache Funktionen für erste Experimente
    f = Funktion("(x+1)^2")
    g = Funktion("(x-1)^2")
    return Ableitung, Ausmultiplizieren, Graph, Term, Wendepunkte, f, g


@app.cell
def _(f, g):
    h = f * g
    return (h,)


@app.cell
def _(Ausmultiplizieren, h):
    Ausmultiplizieren(h)
    return


@app.cell
def _(Term, h):
    Term(h)
    return


@app.cell
def _(Wendepunkte, h):
    Wendepunkte(h)
    return


@app.cell
def _(Ableitung, h):
    h1 = Ableitung(h)
    return (h1,)


@app.cell
def _(Term, h1):
    Term(h1)
    return


@app.cell
def _(Graph, h1):
    Graph(h1)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
