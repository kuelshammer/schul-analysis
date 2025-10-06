import marimo

__generated_with = "0.8.20"
app = marimo.App()


@app.cell
def __():
    import sys

    import marimo as mo

    sys.path.insert(0, "src")
    from schul_analysis import Funktion

    # Erstelle eine quadratische Funktion
    f = Funktion("x^2 - 4x + 3")

    mo.md(f"""
    # Magic Factory Architecture Test

    ## Quadratische Funktion
    **Funktion**: f(x) = {f.term()}

    **Automatisch erkannter Typ**: {type(f).__name__}

    **Grad**: {f.grad()}

    **Ist quadratisch**: {f.ist_quadratisch()}

    ## Nullstellen
    **Nullstellen**: {f.nullstellen}

    **Anzahl der Nullstellen**: {len(f.nullstellen)}

    ## Spezialmethoden (nur für quadratische Funktionen)
    **Scheitelpunkt**: {f.get_scheitelpunkt()}

    **Öffnungsfaktor**: {f.get_oeffnungsfaktor()}
    """)

    return f, mo, sys


if __name__ == "__main__":
    app.run()
