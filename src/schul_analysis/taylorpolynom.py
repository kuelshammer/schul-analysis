"""
Taylorpolynome für das Schul-Analysis Framework.

Implementiert Taylorpolynome zur Approximation von Funktionen durch Polynome
an einem Entwicklungspunkt. Enthält Fehlerabschätzung und Visualisierung.
"""

import numpy as np
import plotly.graph_objects as go
import sympy as sp
from sympy import diff, factorial, lambdify, latex, symbols

from .config import config
from .errors import (
    SchulAnalysisError,
)
from .ganzrationale import GanzrationaleFunktion
from .gebrochen_rationale import GebrochenRationaleFunktion


class TaylorpolynomError(SchulAnalysisError):
    """Basisklasse für Taylorpolynom-Fehler"""

    pass


class NichtDifferenzierbarError(TaylorpolynomError):
    """Fehler wenn Funktion nicht oft genug differenzierbar ist"""

    pass


class Taylorpolynom:
    """
    Repräsentiert ein Taylorpolynom zur Approximation einer Funktion.
    """

    def __init__(
        self,
        funktion: GanzrationaleFunktion | GebrochenRationaleFunktion | sp.Basic,
        entwicklungspunkt: float = 0,
        grad: int = 3,
    ):
        """
        Konstruktor für Taylorpolynome.

        Args:
            funktion: Zu approximierende Funktion
            entwicklungspunkt: Punkt um den entwickelt wird (Standard 0 = MacLaurin)
            grad: Grad des Taylorpolynoms
        """
        self.funktion = funktion
        self.entwicklungspunkt = entwicklungspunkt
        self.grad = grad
        self._cache = {}

        # Konvertiere zu SymPy-Ausdruck wenn nötig
        if hasattr(funktion, "term_sympy"):
            self.funktion_sympy = funktion.term_sympy
        else:
            self.funktion_sympy = funktion

        self.x = symbols("x")

        # Berechne Taylorpolynom
        self.taylor_polynom = self._berechne_taylorpolynom()

        # Optimize for performance with lambdify
        try:
            self.taylor_func_numpy = lambdify(self.x, self.taylor_polynom, "numpy")
            self.original_func_numpy = lambdify(self.x, self.funktion_sympy, "numpy")
        except Exception:
            # Fallback to slower evaluation if lambdify fails
            self.taylor_func_numpy = None
            self.original_func_numpy = None

        # Konvertiere zu ganzrationaler Funktion
        try:
            self.taylor_funktion = GanzrationaleFunktion(self.taylor_polynom)
        except Exception:
            # Fallback: Behalte als SymPy-Ausdruck
            self.taylor_funktion = self.taylor_polynom

    def _berechne_taylorpolynom(self) -> sp.Basic:
        """
        Berechnet das Taylorpolynom durch Koeffizientenberechnung.

        Returns:
            SymPy-Ausdruck des Taylorpolynoms
        """
        # Taylorformel: T_n(x) = Σ(f^(k)(a)/k! * (x-a)^k)
        taylor_summe = 0

        for k in range(self.grad + 1):
            # Berechne k-te Ableitung am Entwicklungspunkt
            try:
                k_te_ableitung = diff(self.funktion_sympy, self.x, k)
                wert_an_stelle = k_te_ableitung.subs(self.x, self.entwicklungspunkt)

                # Prüfe ob der Wert definiert ist
                if wert_an_stelle in [sp.nan, sp.oo, -sp.oo]:
                    raise NichtDifferenzierbarError(
                        f"Die {k}-te Ableitung ist an x={self.entwicklungspunkt} nicht definiert"
                    )

                # Taylor-Koeffizient
                koeffizient = wert_an_stelle / factorial(k)

                # Addiere Term zur Summe
                term = koeffizient * ((self.x - self.entwicklungspunkt) ** k)
                taylor_summe += term

            except Exception as e:
                raise NichtDifferenzierbarError(
                    f"Fehler bei Berechnung der {k}-ten Ableitung: {e}"
                )

        return sp.simplify(taylor_summe)

    @property
    def term(self) -> str:
        """Gibt den Taylorpolynom-Term als String zurück"""
        if "term" not in self._cache:
            if hasattr(self.taylor_funktion, "term"):
                self._cache["term"] = self.taylor_funktion.term
            else:
                self._cache["term"] = str(self.taylor_polynom)
        return self._cache["term"]

    @property
    def term_latex(self) -> str:
        """Gibt den Taylorpolynom-Term in LaTeX-Formatierung zurück"""
        if "term_latex" not in self._cache:
            self._cache["term_latex"] = latex(self.taylor_polynom)
        return self._cache["term_latex"]

    def wert(self, x: float) -> float:
        """Berechnet den Wert des Taylorpolynoms an der Stelle x"""
        if hasattr(self.taylor_funktion, "wert"):
            return self.taylor_funktion.wert(x)
        else:
            return float(self.taylor_polynom.subs(self.x, x))

    def ableitung(self, ordnung: int = 1) -> GanzrationaleFunktion:
        """Berechnet die Ableitung des Taylorpolynoms"""
        if hasattr(self.taylor_funktion, "ableitung"):
            return self.taylor_funktion.ableitung(ordnung)
        else:
            abgeleitet = diff(self.taylor_polynom, self.x, ordnung)
            return GanzrationaleFunktion(abgeleitet)

    def restglied_lagrange(self, x: float) -> float:
        """
        Berechnet das Lagrange-Restglied für die Fehlerabschätzung.

        Args:
            x: Stelle an der das Restglied berechnet werden soll

        Returns:
            Wert des Restglieds
        """
        # Lagrange-Restglied: R_n(x) = f^(n+1)(ξ)/(n+1)! * (x-a)^(n+1)
        # wobei ξ zwischen a und x liegt

        try:
            # (n+1)-te Ableitung
            n_plus_1_ableitung = diff(self.funktion_sympy, self.x, self.grad + 1)

            # Maximale Ableitung im Intervall [a,x] oder [x,a]
            a, x_val = self.entwicklungspunkt, x
            interval = [min(a, x_val), max(a, x_val)]

            # Suche Maximum der (n+1)-ten Ableitung im Intervall
            # Dies ist eine Vereinfachung - in der Praxis braucht man numerische Optimierung
            ableitungs_werte = []
            for test_x in np.linspace(interval[0], interval[1], 100):
                try:
                    wert = n_plus_1_ableitung.subs(self.x, test_x)
                    if wert.is_real:
                        ableitungs_werte.append(abs(float(wert)))
                except Exception:
                    continue

            if not ableitungs_werte:
                return float("nan")

            max_ableitung = max(ableitungs_werte)

            # Restglied berechnen
            restglied = (max_ableitung / factorial(self.grad + 1)) * abs(
                x - self.entwicklungspunkt
            ) ** (self.grad + 1)

            return restglied

        except Exception:
            return float("nan")

    def fehler_abschaetzung(self, x_werte: list[float]) -> list[float]:
        """
        Berechnet die Fehlerabschätzung für mehrere x-Werte.

        Args:
            x_werte: Liste von x-Werten

        Returns:
            Liste der Fehlerabschätzungen
        """
        return [self.restglied_lagrange(x) for x in x_werte]

    def konvergenzradius(self) -> float | None:
        """
        Bestimmt den Konvergenzradius der Taylorreihe (wenn möglich).

        Returns:
            Konvergenzradius oder None wenn nicht bestimmbar
        """
        # Für rationale Funktionen kann man den Konvergenzradius bestimmen
        try:
            # Für rationale Funktionen: Abstand zur nächsten Singularität
            if isinstance(self.funktion, GebrochenRationaleFunktion):
                polstellen = self.funktion.polstellen()
                if polstellen:
                    abstaende = [abs(p - self.entwicklungspunkt) for p in polstellen]
                    return min(abstaende)

            # Für exp(x), sin(x), cos(x): unendlich
            if self.funktion_sympy in [sp.exp(self.x), sp.sin(self.x), sp.cos(self.x)]:
                return float("inf")

            # Für ln(1+x): Konvergenzradius 1 um 0
            if (
                self.funktion_sympy == sp.log(1 + self.x)
                and self.entwicklungspunkt == 0
            ):
                return 1.0

            return None

        except Exception:
            return None

    def koeffizienten(self) -> list[tuple[int, float]]:
        """
        Gibt die Taylor-Koeffizienten zurück.

        Returns:
            Liste von (Grad, Koeffizient) Tupeln
        """
        koeffizienten_liste = []

        for k in range(self.grad + 1):
            try:
                k_te_ableitung = diff(self.funktion_sympy, self.x, k)
                wert_an_stelle = k_te_ableitung.subs(self.x, self.entwicklungspunkt)
                koeffizient = float(wert_an_stelle / factorial(k))
                koeffizienten_liste.append((k, koeffizient))
            except Exception:
                koeffizienten_liste.append((k, float("nan")))

        return koeffizienten_liste

    def __str__(self) -> str:
        return f"Taylorpolynom (Grad {self.grad}) um x={self.entwicklungspunkt}: T_{self.grad}(x) = {self.term}"

    def __repr__(self) -> str:
        return f"Taylorpolynom(funktion={self.funktion}, entwicklungspunkt={self.entwicklungspunkt}, grad={self.grad})"

    def zeige_taylor_approximation_plotly(
        self,
        x_range: tuple[float, float] = None,
        punkte: int = 200,
        zeige_restglied: bool = True,
        **kwargs,
    ) -> go.Figure:
        """
        Zeigt die Taylor-Approximation mit der Originalfunktion.

        Args:
            x_range: x-Bereich für die Darstellung
            punkte: Anzahl der zu berechnenden Punkte
            zeige_restglied: Ob das Restglied visualisiert werden soll

        Returns:
            Plotly Figure oder Marimo UI Element
        """
        if x_range is None:
            # Automatischen Bereich um Entwicklungspunkt wählen
            breite = 5.0
            x_range = (self.entwicklungspunkt - breite, self.entwicklungspunkt + breite)

        # Erstelle x-Werte
        x_werte = np.linspace(x_range[0], x_range[1], punkte)

        # Berechne Funktionswerte (Original)
        try:
            if hasattr(self.funktion, "wert"):
                y_original = [self.funktion.wert(x) for x in x_werte]
            else:
                y_original = [
                    float(self.funktion_sympy.subs(self.x, x)) for x in x_werte
                ]
        except Exception:
            y_original = [float("nan")] * len(x_werte)

        # Berechne Taylor-Approximation
        y_taylor = [self.wert(x) for x in x_werte]

        # Berechne Fehler/Restglied
        if zeige_restglied:
            fehler = [
                abs(y_orig - y_tay)
                for y_orig, y_tay in zip(y_original, y_taylor, strict=False)
            ]
            restglied_abschaetzung = self.fehler_abschaetzung(x_werte.tolist())

        fig = go.Figure()

        # Originalfunktion
        fig.add_trace(
            go.Scatter(
                x=x_werte,
                y=y_original,
                mode="lines",
                name="Originalfunktion",
                line={"color": config.COLORS["primary"], "width": 3},
            )
        )

        # Taylorpolynom
        fig.add_trace(
            go.Scatter(
                x=x_werte,
                y=y_taylor,
                mode="lines",
                name=f"Taylorpolynom (Grad {self.grad})",
                line={"color": config.COLORS["secondary"], "width": 3, "dash": "dash"},
            )
        )

        # Entwicklungspunkt markieren
        y_entwicklung = self.wert(self.entwicklungspunkt)
        fig.add_trace(
            go.Scatter(
                x=[self.entwicklungspunkt],
                y=[y_entwicklung],
                mode="markers",
                name=f"Entwicklungspunkt x={self.entwicklungspunkt}",
                marker={
                    "color": config.COLORS["tertiary"],
                    "size": 12,
                    "symbol": "circle",
                },
            )
        )

        # Fehlerdarstellung
        if zeige_restglied and not all(np.isnan(fehler)):
            # Zweite y-Achse für Fehler
            fig.update_layout(
                yaxis2={"title": "Fehler", "overlaying": "y", "side": "right"}
            )

            fig.add_trace(
                go.Scatter(
                    x=x_werte,
                    y=fehler,
                    mode="lines",
                    name="Tatsächlicher Fehler",
                    yaxis="y2",
                    line={"color": "red", "width": 2, "dash": "dot"},
                )
            )

            # Restglied-Abschätzung
            if not all(np.isnan(restglied_abschaetzung)):
                fig.add_trace(
                    go.Scatter(
                        x=x_werte,
                        y=restglied_abschaetzung,
                        mode="lines",
                        name="Restglied-Abschätzung",
                        yaxis="y2",
                        line={"color": "orange", "width": 2},
                    )
                )

        # Konvergenzradius einzeichnen (wenn bekannt)
        konvergenzradius = self.konvergenzradius()
        if konvergenzradius is not None and konvergenzradius != float("inf"):
            fig.add_vline(
                x=self.entwicklungspunkt + konvergenzradius,
                line_dash="dot",
                line_color="gray",
                annotation_text=f"Konvergenzradius R={konvergenzradius:.2f}",
            )

            fig.add_vline(
                x=self.entwicklungspunkt - konvergenzradius,
                line_dash="dot",
                line_color="gray",
            )

        # Layout konfigurieren
        titel = kwargs.get(
            "title",
            f"Taylor-Approximation (Grad {self.grad} um x={self.entwicklungspunkt})",
        )
        fig.update_layout(
            **config.get_plot_config(),
            title=titel,
            xaxis={
                **config.get_axis_config(mathematical_mode=True),
                "range": x_range,
                "title": "x",
            },
            yaxis={
                **config.get_axis_config(mathematical_mode=False),
                "title": "f(x)",
            },
        )

        # Rückgabe mit Marimo UI wenn verfügbar
        try:
            import marimo as mo

            return mo.ui.plotly(fig)
        except ImportError:
            return fig

    def zeige_konvergenzvergleich_plotly(
        self, max_grad: int = 6, x_range: tuple[float, float] = None, **kwargs
    ) -> go.Figure:
        """
        Zeigt mehrere Taylorpolynome unterschiedlichen Grades im Vergleich.

        Args:
            max_grad: Höchster Grad der dargestellten Polynome
            x_range: x-Bereich für die Darstellung

        Returns:
            Plotly Figure mit mehreren Taylorpolynomen
        """
        if x_range is None:
            breite = 3.0
            x_range = (self.entwicklungspunkt - breite, self.entwicklungspunkt + breite)

        # Erstelle x-Werte
        x_werte = np.linspace(x_range[0], x_range[1], 200)

        # Berechne Originalfunktion
        try:
            if hasattr(self.funktion, "wert"):
                y_original = [self.funktion.wert(x) for x in x_werte]
            else:
                y_original = [
                    float(self.funktion_sympy.subs(self.x, x)) for x in x_werte
                ]
        except Exception:
            y_original = [float("nan")] * len(x_werte)

        fig = go.Figure()

        # Originalfunktion
        fig.add_trace(
            go.Scatter(
                x=x_werte,
                y=y_original,
                mode="lines",
                name="Originalfunktion",
                line={"color": config.COLORS["primary"], "width": 4},
            )
        )

        # Taylorpolynome verschiedener Grade
        farben = ["secondary", "tertiary", "red", "green", "blue", "purple"]

        for grad in range(1, max_grad + 1):
            # Erstelle Taylorpolynom dieses Grades
            taylor_grad = Taylorpolynom(self.funktion, self.entwicklungspunkt, grad)

            y_taylor = [taylor_grad.wert(x) for x in x_werte]

            farbe = config.COLORS.get(farben[(grad - 1) % len(farben)], "gray")

            fig.add_trace(
                go.Scatter(
                    x=x_werte,
                    y=y_taylor,
                    mode="lines",
                    name=f"Grad {grad}",
                    line={"color": farbe, "width": 2, "dash": "dash"},
                )
            )

        # Entwicklungspunkt markieren
        try:
            y_entwicklung = self.wert(self.entwicklungspunkt)
            fig.add_trace(
                go.Scatter(
                    x=[self.entwicklungspunkt],
                    y=[y_entwicklung],
                    mode="markers",
                    name="Entwicklungspunkt",
                    marker={"color": "black", "size": 10, "symbol": "diamond"},
                )
            )
        except Exception:
            pass

        # Layout konfigurieren
        fig.update_layout(
            **config.get_plot_config(),
            title=f"Taylor-Polynome verschiedener Grade um x={self.entwicklungspunkt}",
            xaxis={
                **config.get_axis_config(mathematical_mode=True),
                "range": x_range,
                "title": "x",
            },
            yaxis={
                **config.get_axis_config(mathematical_mode=False),
                "title": "f(x)",
            },
        )

        try:
            import marimo as mo

            return mo.ui.plotly(fig)
        except ImportError:
            return fig

    def zeige_koeffizienten_entwicklung(self) -> str:
        """
        Zeigt die schrittweise Entwicklung der Taylor-Koeffizienten.

        Returns:
            Formatierter Text mit der Koeffizientenberechnung
        """
        entwicklung = []

        entwicklung.append("=" * 60)
        entwicklung.append("TAYLORPOLYNOM - KOEFFIZIENTENENTWICKLUNG")
        entwicklung.append("=" * 60)
        entwicklung.append("")

        entwicklung.append(f"Entwicklungspunkt: a = {self.entwicklungspunkt}")
        entwicklung.append(f"Grad: n = {self.grad}")
        entwicklung.append("")

        entwicklung.append("Taylorformel:")
        entwicklung.append("   T_n(x) = Σ[k=0 bis n] (f^(k)(a)/k!) × (x-a)^k")
        entwicklung.append("")

        entwicklung.append("Berechnung der Koeffizienten:")
        entwicklung.append("-" * 40)

        koeffizienten = self.koeffizienten()

        for k, koeffizient in koeffizienten:
            try:
                # Berechne k-te Ableitung
                k_te_ableitung = diff(self.funktion_sympy, self.x, k)
                wert_an_stelle = k_te_ableitung.subs(self.x, self.entwicklungspunkt)

                entwicklung.append(f"   k = {k}:")
                entwicklung.append(
                    f"   f^({k})({self.entwicklungspunkt}) = {wert_an_stelle}"
                )
                entwicklung.append(
                    f"   a_{k} = {wert_an_stelle} / {k}! = {koeffizient}"
                )
                entwicklung.append("")

            except Exception as e:
                entwicklung.append(f"   k = {k}: Fehler bei Berechnung - {e}")
                entwicklung.append("")

        # Zusammenfassung
        entwicklung.append("Ergebnis:")
        entwicklung.append(f"   T_{self.grad}(x) = {self.term}")
        entwicklung.append("")

        # Konvergenzradius
        konvergenzradius = self.konvergenzradius()
        if konvergenzradius is not None:
            if konvergenzradius == float("inf"):
                entwicklung.append("Konvergenzradius: R = ∞ (überall konvergent)")
            else:
                entwicklung.append(f"Konvergenzradius: R = {konvergenzradius}")
        else:
            entwicklung.append("Konvergenzradius: Nicht bestimmbar")

        entwicklung.append("")
        entwicklung.append("=" * 60)

        return "\n".join(entwicklung)

    def analysiere_approximationsgüte(
        self,
        testpunkte: list[float] = None,
        schwellen_sehr_gut: float = 0.01,
        schwellen_gut: float = 0.05,
        schwellen_akzeptabel: float = 0.1,
    ) -> dict:
        """
        Analysiert die Güte der Approximation an verschiedenen Punkten.

        Args:
            testpunkte: Liste von Testpunkten (wird automatisch generiert wenn None)

        Returns:
            Dictionary mit Analyseergebnissen
        """
        if testpunkte is None:
            # Generiere Testpunkte um Entwicklungspunkt
            abstaende = [0.1, 0.5, 1.0, 2.0]
            testpunkte = []
            for abstand in abstaende:
                testpunkte.extend(
                    [self.entwicklungspunkt - abstand, self.entwicklungspunkt + abstand]
                )
            testpunkte.sort()

        analyse = {
            "testpunkte": testpunkte,
            "fehler": [],
            "relative_fehler": [],
            "restglied_abschaetzung": [],
            "bewertung": [],
        }

        for x in testpunkte:
            try:
                # Tatsächlicher Wert
                if hasattr(self.funktion, "wert"):
                    tatsaechlich = self.funktion.wert(x)
                else:
                    tatsaechlich = float(self.funktion_sympy.subs(self.x, x))

                # Taylor-Approximation
                approx = self.wert(x)

                # Fehlerberechnung
                absoluter_fehler = abs(tatsaechlich - approx)
                relativer_fehler = (
                    absoluter_fehler / abs(tatsaechlich)
                    if tatsaechlich != 0
                    else float("inf")
                )
                restglied = self.restglied_lagrange(x)

                analyse["fehler"].append(absoluter_fehler)
                analyse["relative_fehler"].append(relativer_fehler)
                analyse["restglied_abschaetzung"].append(restglied)

                # Bewertung
                if relativer_fehler < 0.01:  # < 1%
                    bewertung = "Sehr gut"
                elif relativer_fehler < 0.1:  # < 10%
                    bewertung = "Gut"
                elif relativer_fehler < 0.5:  # < 50%
                    bewertung = "Akzeptabel"
                else:
                    bewertung = "Schlecht"

                analyse["bewertung"].append(bewertung)

            except Exception:
                analyse["fehler"].append(float("nan"))
                analyse["relative_fehler"].append(float("nan"))
                analyse["restglied_abschaetzung"].append(float("nan"))
                analyse["bewertung"].append("Nicht berechenbar")

        return analyse

    @classmethod
    def standardfunktionen(cls):
        """
        Gibt wichtige Standardfunktionen für Taylorpolynome zurück.

        Returns:
            Dictionary mit Standardfunktionen und ihren Namen
        """
        x = symbols("x")

        standardfunktionen = {
            "exp(x)": sp.exp(x),
            "sin(x)": sp.sin(x),
            "cos(x)": sp.cos(x),
            "ln(1+x)": sp.log(1 + x),
            "1/(1-x)": 1 / (1 - x),
            "sqrt(1+x)": sp.sqrt(1 + x),
            "e^x": sp.exp(x),
        }

        return standardfunktionen
