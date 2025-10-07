"""
Marimo Integration Examples

Dieses Beispiel zeigt die Verwendung des modernen Schul-Analysis Frameworks in Marimo-Notebooks.
Marimo ist ein reaktives Notebook-System, das perfekt für mathematische Analysen geeignet ist.

Installation:
    pip install marimo

Starten:
    marimo edit marimo_examples.py
"""

import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell
def _():
    """Setup und Importe"""
    from schul_analysis import Funktion, ableitung, extrema, nullstellen

    return Funktion, nullstellen, ableitung, extrema


@app.cell
def _(mo):
    """Titel und Einführung"""
    mo.md("""
    # 🎓 Schul-Analysis Framework in Marimo

    Dieses Beispiel zeigt die moderne Magic Factory API in interaktiven Marimo-Notebooks.

    ## Features:
    - ✅ Automatische Funktionserkennung
    - ✅ LaTeX-Darstellung
    - ✅ Interaktive Analyse
    - ✅ Plotly-Visualisierung
    """)
    return


@app.cell
def _(mo):
    """Interaktive Funktionserstellung"""
    # Coefficients for quadratic function: ax² + bx + c
    a_slider = mo.ui.slider(-5, 5, value=1, step=0.1, label="a (x²)")
    b_slider = mo.ui.slider(-5, 5, value=0, step=0.1, label="b (x)")
    c_slider = mo.ui.slider(-5, 5, value=0, step=0.1, label="c (konstant)")

    mo.md("### 📐 Parameter für quadratische Funktion:")
    return a_slider, b_slider, c_slider


@app.cell
def _(a_slider, b_slider, c_slider, Funktion):
    """Funktion aus Slider-Werten erstellen"""
    # Erstelle Funktion mit den Slider-Werten
    if a_slider.value != 0:
        term = f"{a_slider.value}x^2 + {b_slider.value}x + {c_slider.value}"
    elif b_slider.value != 0:
        term = f"{b_slider.value}x + {c_slider.value}"
    else:
        term = f"{c_slider.value}"

    f = Funktion(term)

    return f, term


@app.cell
def _(f, mo):
    """LaTeX-Darstellung der Funktion"""
    mo.md(f"### 📝 Funktion: {f._repr_latex_()}")
    return


@app.cell
def _(f, mo, nullstellen, extrema):
    """Automatische Analyse"""
    mo.md("### 🔍 Automatische Analyse:")

    analyse_resultate = [
        f"**Funktionstyp:** {f.funktionstyp}",
        f"**Nullstellen:** {nullstellen(f)}",
        f"**Extrema:** {extrema(f)}",
    ]

    for resultat in analyse_resultate:
        mo.md(f"- {resultat}")

    return (analyse_resultate,)


@app.cell
def _(f, ableitung, mo):
    """Ableitungen mit automatischer Namensgebung"""
    mo.md("### 📈 Ableitungen:")

    f1 = ableitung(f)  # f'
    f2 = ableitung(f1)  # f''

    mo.md(f"- **f'(x) = {f1.term()}** (Name: {f1.name})")
    mo.md(f"- **f''(x) = {f2.term()}** (Name: {f2.name})")

    return f1, f2


@app.cell
def _(f, mo):
    """Wertetabelle interaktiv"""
    mo.md("### 📊 Wertetabelle:")

    x_werte = [-3, -2, -1, 0, 1, 2, 3]
    tabelle_daten = []

    for x in x_werte:
        y = f(x)
        tabelle_daten.append(f"| x = {x:2.0f} | y = {y:6.2f} |")

    mo.md("| x | y |")
    mo.md("|---|---|")
    for zeile in tabelle_daten:
        mo.md(zeile)

    return tabelle_daten, x_werte


@app.cell
def _(f, mo):
    """Visualisierung (falls Plotly installiert)"""
    mo.md("### 📊 Visualisierung:")

    try:
        graph = f.zeige_funktion_plotly(x_bereich=(-5, 5))
        mo.ui.plotly(graph)
    except ImportError:
        mo.md("⚠️ **Plotly nicht installiert**")
        mo.md("Installieren Sie mit:")
        mo.md("```bash")
        mo.md("uv sync --group viz-math")
        mo.md("```")
    except Exception as e:
        mo.md(f"⚠️ **Fehler**: {e}")

    return (graph,)


@app.cell
def _(mo):
    """Interaktive Taylor-Demonstration"""
    mo.md("### 🔄 Taylor-Reihe Demo")

    # Taylor-Ordnung
    ordnung_slider = mo.ui.slider(1, 5, value=3, step=1, label="Taylor-Ordnung")

    return (ordnung_slider,)


@app.cell
def _(ordnung_slider, mo):
    """Taylor-Approximation erstellen"""
    from schul_analysis import Funktion

    # Approximiere sin(x) mit Taylor-Reihe
    x0 = 0  # Entwicklungspunkt

    if ordnung_slider.value == 1:
        taylor_term = "x"
    elif ordnung_slider.value == 2:
        taylor_term = "x - x^3/6"
    elif ordnung_slider.value == 3:
        taylor_term = "x - x^3/6 + x^5/120"
    elif ordnung_slider.value == 4:
        taylor_term = "x - x^3/6 + x^5/120 - x^7/5040"
    else:
        taylor_term = "x - x^3/6 + x^5/120 - x^7/5040 + x^9/362880"

    taylor_func = Funktion(taylor_term)
    original_func = Funktion("sin(x)")

    mo.md(f"**{ordnung_slider.value}. Taylor-Polynom für sin(x) um x=0:**")
    mo.md(f"T(x) = {taylor_term}")

    return original_func, taylor_func, taylor_term, x0


@app.cell
def _(original_func, taylor_func, mo):
    """Vergleich der Funktionen"""
    mo.md("### 📈 Vergleich Original vs. Approximation:")

    # Vergleich an einigen Punkten
    test_punkte = [-1, -0.5, 0, 0.5, 1]

    vergleich = []
    for x in test_punkte:
        orig_val = original_func(x)
        taylor_val = taylor_func(x)
        fehler = abs(orig_val - taylor_val)
        vergleich.append(
            f"| x = {x:4.1f} | sin(x) = {orig_val:6.3f} | T(x) = {taylor_val:6.3f} | Fehler = {fehler:6.3f} |"
        )

    mo.md("| x | sin(x) | T(x) | Fehler |")
    mo.md("|---|---|---|---|")
    for zeile in vergleich:
        mo.md(zeile)

    return test_punkte, vergleich


@app.cell
def _(mo):
    """Zusammenfassung"""
    mo.md("""
    ## 🎯 Zusammenfassung

    Dieses Beispiel zeigt die Stärken der modernen Schul-Analysis API:

    - **🎯 Magic Factory**: `Funktion("term")` - einfache Erstellung
    - **📝 LaTeX-Darstellung**: Automatische Anzeige von f(x) = term
    - **🏷️ Intelligente Namen**: Ableitungen bekommen automatisch Namen (f', f'')
    - **🔍 Deutsche API**: `nullstellen()`, `ableitung()`, `extrema()`
    - **📊 Interaktiv**: Perfekt für Marimo-Notebooks
    - **🎓 Pädagogisch**: Optimiert für den Mathematikunterricht

    ## 💡 Tipps für den Unterricht:

    1. **Interaktive Parameter**: Schüler können Parameter live verändern
    2. **Automatische Analyse**: Keine manuellen Berechnungen nötig
    3. **Visuelles Feedback**: Direkte Darstellung von Änderungen
    4. **Taylor-Reihen**: Verständliche Approximationen
    """)
    return


if __name__ == "__main__":
    app.run()
