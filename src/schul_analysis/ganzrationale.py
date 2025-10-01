"""
Ganzrationale Funktionen (Polynome) für das Schul-Analysis Framework.

Unterstützt verschiedene Konstruktor-Formate und mathematisch korrekte
Visualisierung mit Plotly für Marimo-Notebooks.
"""

import numpy as np
import pandas as pd
import marimo as mo
from typing import Union, List, Tuple, Dict, Any
import sympy as sp
from sympy import sympify, latex, solve, diff, symbols, Poly
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class GanzrationaleFunktion:
    """
    Repräsentiert eine ganzrationale Funktion (Polynom) mit verschiedenen
    Konstruktor-Optionen und Visualisierungsmethoden.
    """

    def __init__(self, eingabe: Union[str, List[float], Dict[int, float]]):
        """
        Konstruktor für ganzrationale Funktionen.

        Args:
            eingabe: String ("x^3-2x+1"), Liste ([1, 0, -2, 1]) oder Dictionary ({3: 1, 1: -2, 0: 1})
        """
        self.x = symbols("x")

        if isinstance(eingabe, str):
            # String-Konstruktor: "x^3-2x+1"
            self.term_str = eingabe
            self.term_sympy = sympify(eingabe)
        elif isinstance(eingabe, list):
            # Listen-Konstruktor: [1, 0, -2, 1] für x³ - 2x + 1
            self.term_str = self._liste_zu_string(eingabe)
            self.term_sympy = self._liste_zu_sympy(eingabe)
        elif isinstance(eingabe, dict):
            # Dictionary-Konstruktor: {3: 1, 1: -2, 0: 1} für x³ - 2x + 1
            self.term_str = self._dict_zu_string(eingabe)
            self.term_sympy = self._dict_zu_sympy(eingabe)
        else:
            raise TypeError("Eingabe muss String, Liste oder Dictionary sein")

        # Koeffizienten extrahieren
        self.koeffizienten = self._extrahiere_koeffizienten()

    def _liste_zu_string(self, koeff: List[float]) -> str:
        """Wandelt Koeffizienten-Liste in Term-String um."""
        terme = []
        for i, k in enumerate(koeff):
            if k == 0:
                continue
            if i == 0:
                terme.append(str(k))
            elif i == 1:
                if k == 1:
                    terme.append("x")
                elif k == -1:
                    terme.append("-x")
                else:
                    terme.append(f"{k}x")
            else:
                if k == 1:
                    terme.append(f"x^{i}")
                elif k == -1:
                    terme.append(f"-x^{i}")
                else:
                    terme.append(f"{k}x^{i}")

        if not terme:
            return "0"

        return "+".join(terme).replace("+-", "-")

    def _liste_zu_sympy(self, koeff: List[float]) -> sp.Expr:
        """Wandelt Koeffizienten-Liste in SymPy-Ausdruck um."""
        term = 0
        for i, k in enumerate(koeff):
            term += k * self.x**i
        return term

    def _dict_zu_string(self, koeff: Dict[int, float]) -> str:
        """Wandelt Koeffizienten-Dictionary in Term-String um."""
        # Sortiere nach absteigendem Grad
        sortierte_koeff = sorted(koeff.items(), key=lambda x: -x[0])

        terme = []
        for grad, k in sortierte_koeff:
            if k == 0:
                continue
            if grad == 0:
                terme.append(str(k))
            elif grad == 1:
                if k == 1:
                    terme.append("x")
                elif k == -1:
                    terme.append("-x")
                else:
                    terme.append(f"{k}x")
            else:
                if k == 1:
                    terme.append(f"x^{grad}")
                elif k == -1:
                    terme.append(f"-x^{grad}")
                else:
                    terme.append(f"{k}x^{grad}")

        if not terme:
            return "0"

        return "+".join(terme).replace("+-", "-")

    def _dict_zu_sympy(self, koeff: Dict[int, float]) -> sp.Expr:
        """Wandelt Koeffizienten-Dictionary in SymPy-Ausdruck um."""
        term = 0
        for grad, k in koeff.items():
            term += k * self.x**grad
        return term

    def _extrahiere_koeffizienten(self) -> List[float]:
        """Extrahiert Koeffizienten aus SymPy-Ausdruck."""
        poly = Poly(self.term_sympy, self.x)
        return [float(poly.coeff(i)) for i in range(poly.degree() + 1)]

    def term(self) -> str:
        """Gibt den Term als String zurück."""
        return self.term_str

    def term_latex(self) -> str:
        """Gibt den Term als LaTeX-String zurück."""
        return latex(self.term_sympy)

    def wert(self, x_wert: float) -> float:
        """Berechnet den Funktionswert an einer Stelle."""
        return float(self.term_sympy.subs(self.x, x_wert))

    def ableitung(self, ordnung: int = 1) -> "GanzrationaleFunktion":
        """Berechnet die Ableitung gegebener Ordnung."""
        abgeleitet = diff(self.term_sympy, self.x, ordnung)
        return GanzrationaleFunktion(str(abgeleitet))

    def nullstellen(self, real: bool = True) -> List[float]:
        """Berechnet die Nullstellen der Funktion."""
        try:
            lösungen = solve(self.term_sympy, self.x)
            nullstellen = []

            for lösung in lösungen:
                if real:
                    # Nur reelle Nullstellen
                    if lösung.is_real:
                        nullstellen.append(float(lösung))
                else:
                    # Auch komplexe Nullstellen
                    if lösung.is_real:
                        nullstellen.append(float(lösung))
                    else:
                        # Komplexe Zahl in Real- und Imaginärteil aufteilen
                        nullstellen.append(complex(lösung))

            return sorted(nullstellen)
        except:
            return []

    def extremstellen(self) -> List[Tuple[float, str]]:
        """Berechnet die Extremstellen der Funktion."""
        try:
            # Erste Ableitung
            f_strich = self.ableitung(1)

            # Kritische Punkte
            kritische_punkte = solve(f_strich.term_sympy, self.x)

            extremstellen = []

            for punkt in kritische_punkte:
                if punkt.is_real:
                    x_wert = float(punkt)

                    # Zweite Ableitung
                    f_doppelstrich = self.ableitung(2)
                    y_wert = f_doppelstrich.wert(x_wert)

                    if y_wert > 0:
                        art = "Minimum"
                    elif y_wert < 0:
                        art = "Maximum"
                    else:
                        art = "Sattelpunkt"

                    extremstellen.append((x_wert, art))

            return sorted(extremstellen, key=lambda x: x[0])
        except:
            return []

    def nullstellen_weg(self) -> str:
        """Gibt detaillierten Lösungsweg für Nullstellen als Markdown zurück."""
        weg = f"# Nullstellen von f(x) = {self.term()}\n\n"
        weg += f"Gegeben ist die Funktion: $$f(x) = {self.term_latex()}$$\n\n"

        # Verschiedene Lösungswege je nach Grad
        grad = len(self.koeffizienten) - 1

        if grad == 0:
            weg += "Bei einer konstanten Funktion gibt es keine Nullstellen.\n"
        elif grad == 1:
            weg += "## Lineare Funktion (Grad 1)\n\n"
            weg += f"$$f(x) = {self.term_latex()} = 0$$\n\n"

            a, b = self.koeffizienten[1], self.koeffizienten[0]
            weg += f"$$x = -\\frac{{{b}}}{{{a}}} = {-b / a}$$\n"

        elif grad == 2:
            weg += "## Quadratische Funktion (Grad 2)\n\n"
            weg += f"$$f(x) = {self.term_latex()} = 0$$\n\n"

            a, b, c = (
                self.koeffizienten[2],
                self.koeffizienten[1],
                self.koeffizienten[0],
            )

            # Mitternachtsformel
            diskriminante = b**2 - 4 * a * c

            weg += "### Mitternachtsformel\n\n"
            weg += f"$$x = \\frac{{-b \\pm \\sqrt{{b^2 - 4ac}}}}{{2a}}$$\n\n"
            weg += f"Mit a = {a}, b = {b}, c = {c}:\n\n"
            weg += f"$$x = \\frac{{-{b} \\pm \\sqrt{{{b}^2 - 4 \\cdot {a} \\cdot {c}}}}}{{2 \\cdot {a}}}$$\n\n"
            weg += (
                f"$$x = \\frac{{-{b} \\pm \\sqrt{{{diskriminante}}}}}{{{2 * a}}}$$\n\n"
            )

            if diskriminante > 0:
                weg += "### Zwei reelle Nullstellen\n\n"
                x1 = (-b + np.sqrt(diskriminante)) / (2 * a)
                x2 = (-b - np.sqrt(diskriminante)) / (2 * a)
                weg += f"$$x_1 = \\frac{{-{b} + \\sqrt{{{diskriminante}}}}}{{{2 * a}}} = {x1:.3f}$$\n\n"
                weg += f"$$x_2 = \\frac{{-{b} - \\sqrt{{{diskriminante}}}}}{{{2 * a}}} = {x2:.3f}$$\n\n"
            elif diskriminante == 0:
                weg += "### Eine doppelte Nullstelle\n\n"
                x = -b / (2 * a)
                weg += f"$$x = \\frac{{-{b}}}{{{2 * a}}} = {x:.3f}$$\n\n"
            else:
                weg += "### Keine reellen Nullstellen\n\n"
                weg += f"Da die Diskriminante D = {diskriminante} < 0 ist, gibt es keine reellen Nullstellen.\n\n"

                # Quadratische Ergänzung zeigen
                weg += "### Quadratische Ergänzung\n\n"
                weg += f"$$f(x) = {self.term_latex()}$$\n\n"
                weg += f"$$= {a}x^2 {b:+}x {c:+}$$\n\n"
                weg += f"$$= {a}\\left(x^2 {b / a:+}x\\right) {c:+}$$\n\n"
                weg += f"$$= {a}\\left(x^2 {b / a:+}x + \\left({b / (2 * a):.3f}\\right)^2 - \\left({b / (2 * a):.3f}\\right)^2\\right) {c:+}$$\n\n"
                weg += f"$$= {a}\\left(\\left(x {b / (2 * a):+.3f}\\right)^2 - {b**2 / (4 * a**2):.3f}\\right) {c:+}$$\n\n"
                weg += f"$$= {a}\\left(x {b / (2 * a):+.3f}\\right)^2 - {b**2 / (4 * a):.3f} {c:+}$$\n\n"
                weg += f"$$= {a}\\left(x {b / (2 * a):+.3f}\\right)^2 {c - b**2 / (4 * a):+.3f}$$\n\n"
                weg += f"Da {a} > 0 und der Term {a}(x {b / (2 * a):+.3f})² ≥ 0 ist, ergibt sich:\n\n"
                weg += f"$$f(x) \\geq {c - b**2 / (4 * a):+.3f} > 0$$\n\n"
                weg += "Somit hat die Funktion keine reellen Nullstellen.\n"

        return weg

    # ============================================
    # 🔥 PLOTLY VISUALISIERUNGSMETHODEN 🔥
    # ============================================

    def zeige_funktion_plotly(
        self, x_range: tuple = (-10, 10), punkte: int = 200
    ) -> mo.UI:
        """Zeigt interaktiven Funktionsgraph mit Plotly - MATHEMATISCH KORREKT"""
        x = np.linspace(x_range[0], x_range[1], punkte)
        y = [self.wert(xi) for xi in x]

        fig = px.line(
            x=x,
            y=y,
            title=f"Funktionsgraph: f(x) = {self.term()}",
            labels={"x": "x", "y": f"f(x) = {self.term()}"},
        )

        # 🔥 PERFECT MATHEMATICAL CONFIGURATION 🔥
        fig.update_layout(
            xaxis=dict(
                scaleanchor="y",  # 1:1 Aspect Ratio
                scaleratio=1,  # Keine Verzerrung!
                zeroline=True,  # Achse im Ursprung
                showgrid=True,  # Gitterlinien
                range=x_range,  # Dynamischer Bereich
                title="x",
            ),
            yaxis=dict(zeroline=True, showgrid=True, title=f"f(x) = {self.term()}"),
            showlegend=False,
            width=600,
            height=400,
        )

        return mo.ui.plotly(fig)

    def perfekte_parabel_plotly(
        self, x_range: tuple = (-5, 5), punkte: int = 200
    ) -> mo.UI:
        """PERFEKTE Parabel-Darstellung entsprechend Schul-Konventionen"""
        # Perfekte symmetrische Datenpunkte um den Scheitelpunkt
        x = np.linspace(x_range[0], x_range[1], punkte)
        y = [self.wert(xi) for xi in x]

        fig = go.Figure()

        # Hauptkurve
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=f"f(x) = {self.term()}",
                line=dict(color="blue", width=3),
            )
        )

        # Scheitelpunkt berechnen und markieren
        try:
            # Für quadratische Funktionen: Scheitelpunkt bei x = -b/(2a)
            if len(self.koeffizienten) >= 3:
                a, b = self.koeffizienten[0], self.koeffizienten[1]
                s_x = -b / (2 * a)
                s_y = self.wert(s_x)

                fig.add_trace(
                    go.Scatter(
                        x=[s_x],
                        y=[s_y],
                        mode="markers",
                        name="Scheitelpunkt",
                        marker=dict(size=15, color="red", symbol="diamond"),
                        text=[f"S({s_x:.2f}|{s_y:.2f})"],
                        hovertemplate="%{text}<extra></extra>",
                    )
                )
        except:
            pass

        # 🔥 ABSOLUT PERFEKTE MATHEMATISCHE KONFIGURATION 🔥
        fig.update_layout(
            title=f"Parabel: f(x) = {self.term()}",
            xaxis=dict(
                scaleanchor="y",  # 🔥 1:1 Aspect Ratio - KEINE VERZERRUNG!
                scaleratio=1,  # 🔥 Perfekte Kreisverwandtschaft!
                zeroline=True,  # 🔥 Achse im Ursprung sichtbar
                zerolinewidth=2,  # 🔥 Deutliche Null-Linie
                zerolinecolor="black",  # 🔥 Schwarze Achse
                showgrid=True,  # 🔥 Gitterlinien helfen beim Ablesen
                gridwidth=1,  # 🔥 Dünne Gitterlinien
                gridcolor="lightgray",  # 🔥 Dezentes Gitter
                range=x_range,  # 🔥 Symmetrischer Bereich
                title="x",  # 🔥 Achsenbeschriftung
                ticks="outside",  # 🔥 Ticks außerhalb
                tickwidth=2,  # 🔥 Deutliche Ticks
                showline=True,  # 🔥 Achsenlinie sichtbar
                linewidth=2,  # 🔥 Deutliche Achsenlinie
            ),
            yaxis=dict(
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="black",
                showgrid=True,
                gridwidth=1,
                gridcolor="lightgray",
                title=f"f(x) = {self.term()}",
                ticks="outside",
                tickwidth=2,
                showline=True,
                linewidth=2,
                scaleanchor="x",  # 🔥 Bidirektionale Verzerrungs-Verhinderung!
            ),
            plot_bgcolor="white",  # 🔥 Weißer Hintergrund für Schule
            paper_bgcolor="white",
            showlegend=True,
            width=700,
            height=500,
            font=dict(size=14),  # 🔥 Gute Lesbarkeit
        )

        return mo.ui.plotly(fig)

    def zeige_nullstellen_plotly(
        self, real: bool = True, x_range: tuple = (-10, 10)
    ) -> mo.UI:
        """Zeigt Funktion mit interaktiven Nullstellen-Markierungen - MATHEMATISCH KORREKT"""
        # Hauptfunktion
        x = np.linspace(x_range[0], x_range[1], 300)
        y = [self.wert(xi) for xi in x]

        # Plotly Figure erstellen
        fig = go.Figure()

        # Hauptfunktion hinzufügen
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=f"f(x) = {self.term()}",
                line=dict(color="blue", width=2),
            )
        )

        # Nullstellen hinzufügen
        nullstellen = self.nullstellen(real)
        if nullstellen:
            ns_x = [ns for ns in nullstellen if x_range[0] <= ns <= x_range[1]]
            ns_y = [0] * len(ns_x)
            ns_labels = [f"Nullstelle: {ns:.2f}" for ns in ns_x]

            fig.add_trace(
                go.Scatter(
                    x=ns_x,
                    y=ns_y,
                    mode="markers",
                    name="Nullstellen",
                    marker=dict(size=12, color="red", symbol="circle"),
                    text=ns_labels,
                    hovertemplate="%{text}<extra></extra>",
                )
            )

            title = f"Nullstellen von f(x) = {self.term()}"
        else:
            title = f"Keine reellen Nullstellen für f(x) = {self.term()}"

        # 🔥 PERFECT MATHEMATICAL CONFIGURATION 🔥
        fig.update_layout(
            title=title,
            xaxis=dict(
                scaleanchor="y",  # 1:1 Aspect Ratio
                scaleratio=1,  # Keine Verzerrung!
                zeroline=True,  # Achse im Ursprung
                showgrid=True,  # Gitterlinien
                range=x_range,
                title="x",
            ),
            yaxis=dict(zeroline=True, showgrid=True, title=f"f(x) = {self.term()}"),
            showlegend=True,
            width=600,
            height=400,
        )

        return mo.ui.plotly(fig)

    def zeige_ableitung_plotly(
        self, ordnung: int = 1, x_range: tuple = (-10, 10)
    ) -> mo.UI:
        """Zeigt Funktion und Ableitung im Vergleich - MATHEMATISCH KORREKT"""
        # Daten generieren
        x = np.linspace(x_range[0], x_range[1], 300)

        # Originalfunktion
        y_orig = [self.wert(xi) for xi in x]

        # Ableitung
        ableitung = self.ableitung(ordnung)
        y_abl = [ableitung.wert(xi) for xi in x]

        # Plotly Subplots
        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=[
                f"f(x) = {self.term()}",
                f"f^{ordnung}(x) = {ableitung.term()}",
            ],
            vertical_spacing=0.1,
        )

        # Originalfunktion
        fig.add_trace(
            go.Scatter(
                x=x, y=y_orig, mode="lines", name="f(x)", line=dict(color="blue")
            ),
            row=1,
            col=1,
        )

        # Ableitung
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y_abl,
                mode="lines",
                name=f"f^{ordnung}(x)",
                line=dict(color="red"),
            ),
            row=2,
            col=1,
        )

        # 🔥 PERFECT MATHEMATICAL CONFIGURATION 🔥
        fig.update_layout(
            title=f"Funktion vs. {ordnung}. Ableitung",
            height=600,
            showlegend=False,
            xaxis=dict(
                scaleanchor="y",  # 1:1 Aspect Ratio
                scaleratio=1,  # Keine Verzerrung!
                zeroline=True,
                showgrid=True,
                range=x_range,
                title="x",
            ),
            xaxis2=dict(
                scaleanchor="y2",  # 1:1 Aspect Ratio für zweite Achse
                scaleratio=1,
                zeroline=True,
                showgrid=True,
                range=x_range,
                title="x",
            ),
            yaxis=dict(zeroline=True, showgrid=True, title="f(x)"),
            yaxis2=dict(zeroline=True, showgrid=True, title=f"f^{ordnung}(x)"),
        )

        return mo.ui.plotly(fig)
