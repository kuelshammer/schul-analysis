import marimo

__generated_with = "0.16.3"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    from src.schul_analysis import GanzrationaleFunktion, Nullstellen, Ableitung, Extremstellen, Extrempunkte, Graph, Wendepunkte, a, x, ParametrischeFunktion
    return GanzrationaleFunktion, Graph, Wendepunkte


@app.cell
def _(GanzrationaleFunktion):
    f = GanzrationaleFunktion("(x+2)^3-4")
    return (f,)


@app.cell
def _(Wendepunkte, f):
    Wendepunkte(f)
    return


@app.cell
def _(Graph, f):
    Graph(f)
    return


@app.cell
def _(GanzrationaleFunktion):
    g = GanzrationaleFunktion("a * x^2 + 1")
    return (g,)


@app.cell
def _(g):
    g.nullstellen()
    return


@app.cell
def _(g):
    g(2)
    return


@app.cell
def _():
    #
    return


if __name__ == "__main__":
    app.run()
