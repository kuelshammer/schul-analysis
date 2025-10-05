import marimo

__generated_with = "0.8.20"
app = marimo.App()


@app.cell
def __():
    import marimo as mo

    return (mo,)


@app.cell
def __(mo):
    # Importieren der Funktion-Klasse
    import sys

    sys.path.insert(0, "src")
    from schul_analysis import Funktion

    # Quadratische Funktion erstellen
    f = Funktion("x^2 - 4x + 3")

    mo.md(f"""
    # Magic Factory Test

    **Funktion**: f(x) = {f.term()}

    **Typ**: {type(f).__name__}

    **Grad**: {f.grad()}

    **Ist quadratisch**: {f.ist_quadratisch()}
    """)
    return Funktion, f, sys


@app.cell
def __(f, mo):
    # Nullstellen berechnen
    nullstellen = f.nullstellen

    mo.md(f"""
    # Nullstellen

    **Nullstellen**: {nullstellen}

    **Anzahl**: {len(nullstellen)}
    """)
    return (nullstellen,)


@app.cell
def __(f, mo):
    # Spezialmethoden testen
    try:
        scheitelpunkt = f.get_scheitelpunkt()
        oeffnungsfaktor = f.get_oeffnungsfaktor()

        mo.md(f"""
        # Spezialmethoden

        **Scheitelpunkt**: {scheitelpunkt}

        **Öffnungsfaktor**: {oeffnungsfaktor}
        """)
    except Exception as e:
        mo.md(f"Fehler: {e}")
    return oeffnungsfaktor, scheitelpunkt


@app.cell
def __(mo):
    mo.md("""
    # Lineare Funktion Test

    Test mit linearer Funktion: g(x) = 2x + 3
    """)
    return


@app.cell
def __(mo):
    from schul_analysis import Funktion as FunktionImport

    # Lineare Funktion erstellen
    g = FunktionImport("2x + 3")

    mo.md(f"""
    **Lineare Funktion**: g(x) = {g.term()}

    **Typ**: {type(g).__name__}

    **Ist linear**: {g.ist_linear()}

    **Steigung**: {g.steigung}
    """)
    return FunktionImport, g


if __name__ == "__main__":
    app.run()
