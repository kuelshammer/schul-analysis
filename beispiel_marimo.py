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

    import schul_analysis as a

    # Zwei einfache Funktionen für erste Experimente
    f = a.Funktion("(x+a)^2")
    g = a.Funktion("(x-b)^2")
    return a, f, g


@app.cell
def _(f, g):
    h = f * g
    return (h,)


@app.cell
def _(a, h):
    a.Ausmultiplizieren(h)
    return


@app.cell
def _(a, h):
    a.Term(h)
    return


@app.cell
def _(a, h):
    a.Extrempunkte(h)
    return


@app.cell
def _(a, h):
    h1 = a.Ableitung(h)
    return (h1,)


@app.cell
def _(a, h1):
    a.Term(h1)
    return


@app.cell
def _(a):
    q = a.Funktion("(x-10)^2")
    return (q,)


@app.cell
def _(a):
    p = a.Funktion("9")
    return (p,)


@app.cell
def _(a, q):
    a.Ausmultiplizieren(q)
    a.Term(q)

    return


@app.cell
def _(a, q):
    a.Integral(q, 2, 6)
    return


@app.cell
def _(a, p, q):
    a.FlaecheZweiFunktionen(p, q, 1, 3)
    return


@app.cell
def _(a, q):
    a.tangente(q, 3)
    return


@app.cell
def _(a, q):
    a.Achsensymmetrie(q)
    return


@app.cell
def _(a):
    a.Achsensymmetrie(a.Funktion("x^2"))
    return


@app.cell
def _(a, q):
    a.Flaeche(q, 1, 2)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
