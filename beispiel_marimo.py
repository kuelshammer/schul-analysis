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

    from schul_mathematik.analysis.api import (
        Funktion,
        Graph,
        Taylorpolynom,
    )

    return Funktion, Graph, Taylorpolynom


@app.cell
def _(Funktion):
    f = Funktion("sin(x)")
    return (f,)


@app.cell
def _(Taylorpolynom, f):
    t = Taylorpolynom(f, 1, 3)
    return (t,)


@app.cell
def _(Graph, f, t):
    Graph(f, t)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
