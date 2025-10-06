import marimo

__generated_with = "0.16.3"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    # Test der Magic Factory Architecture
    from schul_analysis import Funktion

    # Quadratische Funktion erstellen - sollte automatisch QuadratischeFunktion zurückgeben
    f = Funktion("x^2 - 4x + 3")

    mo.md(f"""
    ### Magic Factory Test

    **Funktion**: `f(x) = {f.term()}`

    **Typ**: `{type(f).__name__}`

    **Ist quadratisch**: {f.ist_quadratisch()}

    **Ist ganzrational**: {f.ist_ganzrational()}

    **Grad**: {f.grad()}
    """)
    return (f,)


@app.cell
def _(f, mo):
    # Nullstellen berechnen
    try:
        nullstellen = f.nullstellen()
        mo.md(f"""
        ### Nullstellen

        **Nullstellen**: {nullstellen}

        **Anzahl Nullstellen**: {len(nullstellen)}
        """)
    except Exception as e:
        mo.md(f"**Fehler bei Nullstellenberechnung**: {e}")
    return


@app.cell
def _(f, mo):
    # Spezialmethoden testen (nur bei QuadratischeFunktion verfügbar)
    try:
        scheitelpunkt = f.get_scheitelpunkt()
        oeffnungsfaktor = f.get_oeffnungsfaktor()

        mo.md(f"""
        ### Spezialmethoden (nur für quadratische Funktionen)

        **Scheitelpunkt**: {scheitelpunkt}

        **Öffnungsfaktor**: {oeffnungsfaktor}
        """)
    except Exception as e:
        mo.md(f"**Fehler bei Spezialmethoden**: {e}")
    return


@app.cell
def _(mo):
    mo.md(
        """
    ## Lineare Funktion Test

    Teste mit linearer Funktion `2x + 3`
    """
    )
    return


@app.cell
def _(mo):
    from schul_analysis import Funktion

    # Lineare Funktion erstellen
    g = Funktion("2x + 3")

    mo.md(f"""
    **Lineare Funktion**: `g(x) = {g.term()}`

    **Typ**: `{type(g).__name__}`

    **Ist linear**: {g.ist_linear()}

    **Steigung**: {g.steigung if hasattr(g, "steigung") else "Nicht verfügbar"}
    """)
    return


if __name__ == "__main__":
    app.run()
