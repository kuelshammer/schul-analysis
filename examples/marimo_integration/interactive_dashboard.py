"""
Marimo Integration Examples

Dieses Beispiel zeigt, wie man das Schul-Analysis Framework in Marimo-Notebooks
integriert für interaktive mathematische Analysen.
"""

import marimo as mo
from schul_analysis import Funktion, Nullstellen, Ableitung, Extremstellen, Graph


# Beispiel 1: Interaktive Funktionsanalyse
def interaktive_funktionsanalyse():
    """Erstellt ein interaktives Dashboard zur Funktionsanalyse"""

    # Funktionseingabe
    funktion_input = mo.ui.text(
        value="x^2 - 4x + 3",
        label="Funktion f(x) = ",
        placeholder="Gib eine Funktion ein, z.B. x^2 - 4x + 3",
    )

    # Bereichsauswahl
    x_min_slider = mo.ui.slider(-10, 0, value=-5, step=0.5, label="x_min")
    x_max_slider = mo.ui.slider(0, 10, value=5, step=0.5, label="x_max")

    @mo.cell
    def analyse_funktion():
        try:
            # Funktion erstellen
            f = Funktion(funktion_input.value)

            # Mathematische Analyse
            nullstellen = Nullstellen(f)
            f_strich = Ableitung(f)
            extremstellen = Extremstellen(f)

            # Ergebnisse formatieren
            ergebnisse = [
                f"**Funktion:** f(x) = {f.term()}",
                f"**Ableitung:** f'(x) = {f_strich.term()}",
                f"**Nullstellen:** x = {nullstellen}"
                if nullstellen
                else "**Nullstellen:** Keine reellen Nullstellen",
            ]

            if extremstellen:
                for xs, art in extremstellen:
                    ys = f.wert(xs)
                    ergebnisse.append(f"**{art}:** P({xs:.3f}|{ys:.3f})")
            else:
                ergebnisse.append("**Extremstellen:** Keine Extremstellen")

            return mo.vstack(
                [
                    mo.md("\n".join(ergebnisse)),
                    # Graph erstellen
                    mo.md("**Graph:**"),
                    Graph(f, x_bereich=(x_min_slider.value, x_max_slider.value)),
                ]
            )

        except Exception as e:
            return mo.error(f"Fehler bei der Analyse: {e}")

    return mo.vstack(
        [
            mo.md("# Interaktive Funktionsanalyse"),
            funktion_input,
            mo.hstack([x_min_slider, x_max_slider]),
            analyse_funktion,
        ]
    )


# Beispiel 2: Parameter-Experimente
def parameter_experimente():
    """Interaktives Experiment mit Funktionsparametern"""

    # Parameter-Slider
    a_slider = mo.ui.slider(-5, 5, value=1, step=0.1, label="a")
    b_slider = mo.ui.slider(-5, 5, value=-2, step=0.1, label="b")
    c_slider = mo.ui.slider(-5, 5, value=0, step=0.1, label="c")

    @mo.cell
    def zeige_parameter_effekt():
        # Funktion mit aktuellen Parametern erstellen
        if c_slider.value != 0:
            f_str = f"{a_slider.value}*x^2 + {b_slider.value}*x + {c_slider.value}"
        elif b_slider.value != 0:
            f_str = f"{a_slider.value}*x^2 + {b_slider.value}*x"
        else:
            f_str = f"{a_slider.value}*x^2"

        try:
            f = Funktion(f_str)

            # Analyse durchführen
            nullstellen = Nullstellen(f)
            extremstellen = Extremstellen(f)

            # Scheitelpunkt berechnen (für Parabeln)
            if a_slider.value != 0:
                s_x = -b_slider.value / (2 * a_slider.value)
                s_y = f.wert(s_x)
                scheitelpunkt = f"S({s_x:.2f}|{s_y:.2f})"
            else:
                scheitelpunkt = "Kein Scheitelpunkt (keine Parabel)"

            return mo.vstack(
                [
                    mo.md(f"**Funktion:** f(x) = {f.term()}"),
                    mo.md(f"**Scheitelpunkt:** {scheitelpunkt}"),
                    mo.md(f"**Nullstellen:** {nullstellen}"),
                    mo.md(f"**Extremstellen:** {extremstellen}"),
                    mo.md("**Graph:**"),
                    Graph(f, x_bereich=(-10, 10)),
                ]
            )

        except Exception as e:
            return mo.error(f"Fehler: {e}")

    return mo.vstack(
        [
            mo.md("# Parameter-Experimente"),
            mo.md(
                "Experimentiere mit den Parametern der quadratischen Funktion f(x) = ax² + bx + c"
            ),
            mo.hstack([a_slider, b_slider, c_slider]),
            zeige_parameter_effekt,
        ]
    )


# Beispiel 3: Funktionenvergleich
def funktionen_vergleich():
    """Vergleicht mehrere Funktionen nebeneinander"""

    # Funktionseingaben
    f1_input = mo.ui.text(value="x^2", label="f(x) =")
    f2_input = mo.ui.text(value="x^3", label="g(x) =")
    f3_input = mo.ui.text(value="sin(x)", label="h(x) =")

    # Bereichsauswahl
    bereich_slider = mo.ui.slider(1, 20, value=10, step=1, label="Bereich ±")

    @mo.cell
    def vergleiche_funktionen():
        try:
            # Funktionen erstellen
            f1 = Funktion(f1_input.value)
            f2 = Funktion(f2_input.value)
            f3 = Funktion(f3_input.value)

            # Gemeinsamen Graphen erstellen
            x_min = -bereich_slider.value
            x_max = bereich_slider.value

            graph = Graph(
                f1, f2, f3, x_bereich=(x_min, x_max), titel="Funktionsvergleich"
            )

            return mo.vstack(
                [
                    mo.md("## Vergleich der Funktionen"),
                    graph,
                    mo.md(f"**f(x) = {f1.term()}**"),
                    mo.md(f"**g(x) = {f2.term()}**"),
                    mo.md(f"**h(x) = {f3.term()}**"),
                ]
            )

        except Exception as e:
            return mo.error(f"Fehler: {e}")

    return mo.vstack(
        [
            mo.md("# Funktionenvergleich"),
            mo.hstack([f1_input, f2_input, f3_input]),
            bereich_slider,
            vergleiche_funktionen,
        ]
    )


# Haupt-Dashboard
def main():
    """Erstellt das Haupt-Dashboard"""

    # Tabs für verschiedene Beispiele
    tabs = mo.ui.tabs(
        {
            "Funktionsanalyse": interaktive_funktionsanalyse(),
            "Parameter-Experimente": parameter_experimente(),
            "Funktionenvergleich": funktionen_vergleich(),
        }
    )

    return mo.vstack(
        [
            mo.md("# Schul-Analysis Framework + Marimo"),
            mo.md("""
        Dieses interaktive Dashboard zeigt die Integration des Schul-Analysis Frameworks
        mit Marimo für dynamische mathematische Analysen.

        **Features:**
        - 🔍 **Interaktive Funktionsanalyse**: Geben Sie beliebige Funktionen ein
        - ⚙️ **Parameter-Experimente**: Verändern Sie Parameter und sehen Sie die Effekte
        - 📊 **Funktionenvergleich**: Vergleichen Sie mehrere Funktionen nebeneinander
        - 🎯 **Automatische Berechnungen**: Nullstellen, Extremstellen, Ableitungen
        - 📈 **Dynamische Visualisierung**: Plotly-Graphen mit intelligentem Zoom
        """),
            tabs,
        ]
    )


if __name__ == "__main__":
    # In einem echten Marimo-Notebook würde man einfach:
    # main()
    pass
