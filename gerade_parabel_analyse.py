import marimo

__generated_with = "0.16.3"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    from src.schul_analysis import GanzrationaleFunktion, Nullstellen, Ableitung, Extremstellen, Extrempunkte, Graph
    return Ableitung, Extrempunkte, GanzrationaleFunktion, Nullstellen


@app.cell
def _(GanzrationaleFunktion):
    f = GanzrationaleFunktion("(x+4)(x-1)(x-4)")
    g = GanzrationaleFunktion("1-3x")
    return f, g


@app.cell
def _(f):
    f.nullstellen()
    return


@app.cell
def _(Nullstellen, g):
    Nullstellen(g)
    return


@app.cell
def _(Ableitung, f):
    f1=Ableitung(f)
    f2=Ableitung(f1)
    return f1, f2


@app.cell
def _(f, f1, f2):
    f, f1, f2
    return


@app.cell
def _(f):
    repr(f)
    return


@app.cell
def _(Extrempunkte, f):
    Extrempunkte(f)
    return


@app.cell
def _(f):
    f.graph()
    return


@app.cell
def _(Ableitung, f):
    ff = Ableitung(f)
    return (ff,)


@app.cell
def _(ff):
    ff.graph(x_min=-10,y_max=50)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
