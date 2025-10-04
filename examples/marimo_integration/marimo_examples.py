"""
Marimo Integration Examples

Dieses Beispiel zeigt die Verwendung des Schul-Analysis Frameworks in Marimo-Notebooks.
Marimo ist ein reaktives Notebook-System, das perfekt für mathematische Analysen geeignet ist.

Installation:
    pip install marimo

Starten:
    marimo edit marimo_examples.py

"""

import marimo as mo

# Initialize marimo if not already in a marimo notebook
try:
    # Try to access marimo's app context
    mo.md("# 🎓 Schul-Analysis Framework in Marimo")
    IN_MARIMO = True
except:
    IN_MARIMO = False
    print("Dieses Beispiel ist für die Verwendung in Marimo-Notebooks optimiert.")
    print("Starten Sie mit: marimo edit marimo_examples.py")


@mo.cell
def create_function_sliders():
    """Interaktive Funktionserstellung mit Sliders"""
    # Coefficients for quadratic function: ax² + bx + c
    a = mo.ui.slider(-5, 5, value=1, step=0.1, label="a (x²)")
    b = mo.ui.slider(-5, 5, value=0, step=0.1, label="b (x)")
    c = mo.ui.slider(-5, 5, value=0, step=0.1, label="c (konstant)")

    return a, b, c


@mo.cell
def create_function_from_sliders(a, b, c):
    """Erstellt Funktion aus Slider-Werten"""
    from schul_analysis import Funktion

    # Erstelle Funktion mit den Slider-Werten
    if a.value != 0:
        term = f"{a.value}x^2 + {b.value}x + {c.value}"
    elif b.value != 0:
        term = f"{b.value}x + {c.value}"
    else:
        term = f"{c.value}"

    try:
        f = Funktion(term)
        return f, term
    except:
        # Fallback: einfache quadratische Funktion
        f = Funktion("x^2")
        return f, "x^2"


@mo.cell
def analyze_function(f, term):
    """Führt mathematische Analyse durch"""
    from schul_analysis import Nullstellen, Ableitung, Extremstellen

    try:
        # Berechne Eigenschaften
        nullstellen = Nullstellen(f)
        f_strich = Ableitung(f)
        extremstellen = Extremstellen(f)

        # Erstelle Markdown mit Ergebnissen
        analysis_md = mo.md(f"""
## 📊 Analyse der Funktion f(x) = {term}

### Eigenschaften:
- **Funktionstyp**: {"Quadratisch" if "x^2" in term else "Linear" if "x" in term and "x^2" not in term else "Konstant"}
- **Term**: {f.term()}

### Nullstellen:
{f"**x = {nullstellen}**" if nullstellen else "Keine reellen Nullstellen"}

### Extremstellen:
{"".join([f"**{art}** bei x = {xs:.3f}<br>" for xs, art in extremstellen]) if extremstellen else "Keine Extremstellen"}

### Ableitung:
f'(x) = {f_strich.term()}
        """)

        return analysis_md, nullstellen, extremstellen

    except Exception as e:
        return mo.md(f"Fehler bei der Analyse: {e}"), [], []


@mo.cell
def create_interactive_plot(f, term):
    """Erstelle interaktiven Plot"""
    try:
        from schul_analysis import Graph

        # Erstelle Graph mit intelligenter Skalierung
        graph = Graph(f, titel=f"f(x) = {term}")

        # In Marimo: plotly chart anzeigen
        plotly_chart = mo.ui.plotly(graph)

        return plotly_chart

    except Exception as e:
        return mo.md(f"Fehler bei der Visualisierung: {e}")


@mo.cell
def taylor_series_demo():
    """Taylor-Reihe interaktiv demonstrieren"""
    from schul_analysis import Funktion, Taylor

    # Basisfunktion (z.B. sin(x), cos(x), e^x)
    basisfunktion = mo.ui.dropdown(
        options=["sin(x)", "cos(x)", "e^x"], value="sin(x)", label="Basisfunktion"
    )

    # Taylor-Ordnung
    ordnung = mo.ui.slider(1, 10, value=3, step=1, label="Taylor-Ordnung")

    # Entwicklungspunkt
    x0 = mo.ui.slider(-3, 3, value=0, step=0.5, label="Entwicklungspunkt x₀")

    return basisfunktion, ordnung, x0


@mo.cell
def create_taylor_approximation(basisfunktion, ordnung, x0):
    """Erstelle Taylor-Approximation"""
    try:
        from schul_analysis import Taylor

        # Erstelle Taylor-Polynom
        taylor_func = Taylor(Funktion(basisfunktion.value), ordnung.value, x0.value)

        # Zeige beide Funktionen
        original_func = Funktion(basisfunktion.value)

        return original_func, taylor_func

    except Exception as e:
        return None, mo.md(f"Fehler: {e}")


@mo.cell
def main_interface():
    """Hauptoberfläche für das Marimo-Notebook"""

    if IN_MARIMO:
        # Erstelle Tabs für verschiedene Demos
        tabs = mo.ui.tabs(
            {
                "Funktionsanalyse": [
                    mo.md("# 🎯 Interaktive Funktionsanalyse"),
                    create_function_sliders(),
                    create_function_from_sliders,
                    analyze_function,
                    create_interactive_plot,
                ],
                "Taylor-Reihen": [
                    mo.md("# 📈 Taylor-Reihen Approximation"),
                    taylor_series_demo(),
                    create_taylor_approximation,
                ],
                "Über": [
                    mo.md("""
                # 📚 Über dieses Beispiel

                Dieses Marimo-Notebook demonstriert die Integration des Schul-Analysis Frameworks.

                **Features:**
                - Interaktive Funktionsanalyse mit Sliders
                - Automatische Berechnung von Nullstellen, Extremstellen, Ableitungen
                - Echtzeit-Visualisierung mit Plotly
                - Taylor-Reihen Approximation

                **Technologie:**
                - Schul-Analysis Framework für mathematische Berechnungen
                - Marimo für reaktives Interface
                - Plotly für interaktive Graphen

                **Nutzung:**
                1. Starten Sie Marimo: `marimo edit marimo_examples.py`
                2. Wählen Sie einen Tab
                3. Passen Sie die Parameter mit den Sliders an
                4. Beobachten Sie die automatische Aktualisierung
                """)
                ],
            }
        )

        return tabs
    else:
        return mo.md("""
        # 🚫 Nicht in Marimo-Umgebung

        Dieses Beispiel ist für die Verwendung in Marimo-Notebooks optimiert.

        **Installation:**
        ```bash
        pip install marimo
        ```

        **Starten:**
        ```bash
        marimo edit marimo_examples.py
        ```
        """)


if __name__ == "__main__":
    # Starte die Hauptoberfläche
    main_interface()
