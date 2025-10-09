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
           Nullstellen, Flaeche, Zeichne,
           Ableitung, Integral, Extrema, Wendepunkte,
           Schnittpunkte, Funktion, Tangente, Taylorpolynom
       )
    return Funktion, Taylorpolynom


@app.cell
def _(Funktion):
    f = Funktion("sin(x)")
    return (f,)


@app.cell
def _(Taylorpolynom, f):
    Taylorpolynom(f, 1, 3)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
