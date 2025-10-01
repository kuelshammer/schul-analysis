"""
Schmiegkurven (Interpolationspolynome) für das Schul-Analysis Framework.

Implementiert Interpolationspolynome, die durch vorgegebene Punkte mit optionalen
Tangenten- oder Normalenbedingungen verlaufen.

Dies ist ein ergänzendes Konzept zu Taylorpolynomen:
- Taylorpolynom: Approximation einer Funktion um einen Punkt
- Schmiegkurve: Interpolation durch vorgegebene Punkte mit Bedingungen

HINWEIS: Bei Polynomen hohen Grades und vielen Punkten kann es zu starken
Oszillationen zwischen den Stützpunkten kommen (Runges Phänomen).
"""

from typing import Any

import numpy as np
import plotly.graph_objects as go
import sympy as sp
from sympy import solve, symbols

from .config import config
from .errors import (
    SchulAnalysisError,
)
from .ganzrationale import GanzrationaleFunktion


class SchmiegkurvenError(SchulAnalysisError):
    """Basisklasse für Schmiegkurven-Fehler"""

    pass


class UngueltigePunkteError(SchmiegkurvenError):
    """Fehler bei ungültigen Punktkonfigurationen"""

    pass


class KeineLoesungError(SchmiegkurvenError):
    """Fehler wenn keine Lösung für das Gleichungssystem existiert"""

    pass


class Schmiegkurve:
    """
    Repräsentiert ein Interpolationspolynom (Schmiegkurve), das durch vorgegebene
    Punkte mit optionalen Tangenten- oder Normalenbedingungen verläuft.

    Dies ist ein Interpolationspolynom, das im Gegensatz zu Taylorpolynomen
    nicht eine Funktion approximiert, sondern durch Punkte mit Bedingungen verläuft.
    """

    def __init__(
        self,
        punkte: list[tuple[float, float]],
        tangenten: list[float | None] | None = None,
        normalen: list[float | None] | None = None,
        grad: int | None = None,
    ):
        """
        Konstruktor für allgemeine Schmiegkurven.

        Args:
            punkte: Liste von (x, y) Punkten, durch die die Kurve verlaufen soll
            tangenten: Liste von Tangentensteigungen an den entsprechenden Punkten
            normalen: Liste von Normalensteigungen an den entsprechenden Punkten
            grad: Gewünschter Grad des Polynoms (wird automatisch bestimmt wenn None)
        """
        self.punkte = punkte
        self.tangenten = tangenten or []
        self.normalen = normalen or []
        self.grad = grad
        self._cache = {}

        # Validiere Eingaben
        self._validiere_eingaben()

        # Bestimme den benötigten Grad
        if self.grad is None:
            self.grad = self._berechne_benoetigten_grad()

        # Erstelle die Schmiegkurve
        self.funktion = self._erstelle_schmiegkurve()

        # Optimize for performance with lambdify
        try:
            x = symbols("x")
            self.funktion_numpy = sp.lambdify(x, self.funktion, "numpy")
        except Exception:
            self.funktion_numpy = None

    def _validiere_eingaben(self):
        """Validiert die Eingabeparameter"""
        if len(self.punkte) < 1:
            raise UngueltigePunkteError("Mindestens ein Punkt erforderlich")

        # Prüfe ob Tangenten und Normalen zur Punkteliste passen
        if self.tangenten and len(self.tangenten) != len(self.punkte):
            raise UngueltigePunkteError(
                f"Anzahl der Tangenten ({len(self.tangenten)}) muss "
                f"mit Anzahl der Punkte ({len(self.punkte)}) übereinstimmen"
            )

        if self.normalen and len(self.normalen) != len(self.punkte):
            raise UngueltigePunkteError(
                f"Anzahl der Normalen ({len(self.normalen)}) muss "
                f"mit Anzahl der Punkte ({len(self.punkte)}) übereinstimmen"
            )

        # Prüfe ob ein Punkt sowohl Tangente als auch Normale hat
        for i, (t, n) in enumerate(zip(self.tangenten, self.normalen, strict=False)):
            if t is not None and n is not None:
                # Prüfe ob Tangente und Normale senkrecht stehen
                if not np.isclose(t * n, -1, atol=1e-10):
                    raise UngueltigePunkteError(
                        f"An Punkt {i}: Tangente ({t}) und Normale ({n}) "
                        "müssen senkrecht aufeinander stehen"
                    )

    def _berechne_benoetigten_grad(self) -> int:
        """
        Berechnet den minimal benötigten Grad für die Schmiegkurve.

        Returns:
            Minimaler Grad des Polynoms
        """
        anzahl_punkte = len(self.punkte)
        anzahl_tangenten = sum(1 for t in self.tangenten if t is not None)
        anzahl_normalen = sum(1 for n in self.normalen if n is not None)

        # Jede Bedingung braucht eine Gleichung
        anzahl_gleichungen = anzahl_punkte + anzahl_tangenten + anzahl_normalen

        # Für ein Polynom vom Grad n brauchen wir n+1 Koeffizienten
        # Also: n+1 >= anzahl_gleichungen => n >= anzahl_gleichungen - 1
        min_grad = anzahl_gleichungen - 1

        return max(min_grad, 0)  # Mindestens Grad 0 (Konstante)

    def _erstelle_schmiegkurve(self) -> GanzrationaleFunktion:
        """
        Erstellt die Schmiegkurve durch Lösung des linearen Gleichungssystems.

        Returns:
            Die resultierende ganzrationale Funktion
        """
        x = symbols("x")

        # Erstelle allgemeines Polynom vom Grad self.grad
        koeffizienten = [sp.symbols(f"a_{i}") for i in range(self.grad + 1)]
        polynom = sum(a * x**i for i, a in enumerate(koeffizienten))

        # Erstelle Gleichungssystem
        gleichungen = []

        # Punktbedingungen: f(x_i) = y_i
        for x_i, y_i in self.punkte:
            gleichung = polynom.subs(x, x_i) - y_i
            gleichungen.append(gleichung)

        # Tangentenbedingungen: f'(x_i) = t_i
        if self.tangenten:
            ableitung = polynom.diff(x)
            for i, (x_i, _) in enumerate(self.punkte):
                if self.tangenten[i] is not None:
                    gleichung = ableitung.subs(x, x_i) - self.tangenten[i]
                    gleichungen.append(gleichung)

        # Normalenbedingungen: f'(x_i) = -1/n_i (da n * t = -1)
        if self.normalen:
            ableitung = polynom.diff(x)
            for i, (x_i, _) in enumerate(self.punkte):
                if self.normalen[i] is not None:
                    if self.normalen[i] == 0:
                        raise UngueltigePunkteError(
                            f"An Punkt {i}: Normale kann nicht horizontal sein"
                        )
                    tangente_aus_normale = -1 / self.normalen[i]
                    gleichung = ableitung.subs(x, x_i) - tangente_aus_normale
                    gleichungen.append(gleichung)

        # Löse das Gleichungssystem
        try:
            loesung = solve(gleichungen, koeffizienten, dict=True)

            if not loesung:
                raise KeineLoesungError(
                    "Keine Lösung für das Gleichungssystem gefunden"
                )

            # Setze die Lösung in das Polynom ein
            geloestes_polynom = polynom.subs(loesung[0])

            # Konvertiere zu ganzrationaler Funktion
            return GanzrationaleFunktion(geloestes_polynom)

        except Exception as e:
            raise KeineLoesungError(f"Fehler bei Lösung des Gleichungssystems: {e}")

    @classmethod
    def schmiegparabel(
        cls,
        punkt1: tuple[float, float],
        punkt2: tuple[float, float],
        punkt3: tuple[float, float],
        tangente1: float | None = None,
        tangente3: float | None = None,
    ) -> "Schmiegkurve":
        """
        Erzeugt eine Schmiegparabel durch 3 Punkte mit optionalen Tangenten.

        Args:
            punkt1, punkt2, punkt3: Drei Punkte durch die die Parabel verläuft
            tangente1: Optionale Tangente an punkt1
            tangente3: Optionale Tangente an punkt3

        Returns:
            Schmiegkurve mit Parabel
        """
        punkte = [punkt1, punkt2, punkt3]
        tangenten = [tangente1, None, tangente3]

        return cls(punkte, tangenten=tangenten, grad=2)

    @classmethod
    def schmieggerade(
        cls, punkt: tuple[float, float], tangente: float
    ) -> "Schmiegkurve":
        """
        Erzeugt eine Schmieggerade durch einen Punkt mit gegebener Tangente.

        Args:
            punkt: Punkt durch den die Gerade verläuft
            tangente: Steigung der Geraden

        Returns:
            Schmiegkurve mit Gerade
        """
        return cls([punkt], tangenten=[tangente], grad=1)

    @property
    def term(self) -> str:
        """Gibt den Funktionsterm als String zurück"""
        return self.funktion.term

    @property
    def term_latex(self) -> str:
        """Gibt den Funktionsterm in LaTeX-Formatierung zurück"""
        return self.funktion.term_latex

    def wert(self, x: float) -> float:
        """Berechnet den Funktionswert an der Stelle x"""
        return self.funktion.wert(x)

    def ableitung(self, ordnung: int = 1) -> GanzrationaleFunktion:
        """Berechnet die Ableitung der Schmiegkurve"""
        return self.funktion.ableitung(ordnung)

    def nullstellen(self) -> list[float]:
        """Berechnet die Nullstellen der Schmiegkurve"""
        return self.funktion.nullstellen()

    def __str__(self) -> str:
        return f"Schmiegkurve: f(x) = {self.term}"

    def __repr__(self) -> str:
        return f"Schmiegkurve(punkte={self.punkte}, grad={self.grad})"

    @classmethod
    def hermite_interpolation(
        cls,
        punkte: list[tuple[float, float]],
        werte: list[float],
        ableitungen: list[float],
    ) -> "Schmiegkurve":
        """
        Erzeugt eine Schmiegkurve mittels Hermite-Interpolation.

        Args:
            punkte: Stützstellen x_i
            werte: Funktionswerte f(x_i)
            ableitungen: Ableitungswerte f'(x_i)

        Returns:
            Hermite-Interpolationspolynom
        """
        if len(punkte) != len(werte) or len(punkte) != len(ableitungen):
            raise UngueltigePunkteError(
                "Anzahl von Punkten, Werten und Ableitungen muss übereinstimmen"
            )

        # Konvertiere zu (x, y) Punkten und Tangenten
        punkte_xy = list(zip(punkte, werte, strict=False))
        return cls(punkte_xy, tangenten=ableitungen)

    @classmethod
    def schmiegkegel(
        cls,
        punkte: list[tuple[float, float]],
        tangenten: list[float] | None = None,
        grad: int = 3,
    ) -> "Schmiegkurve":
        """
        Erzeugt einen Schmiegkegel (kubisches Polynom) durch bis zu 4 Punkte
        mit optionalen Tangentenbedingungen.

        Args:
            punkte: Liste von Punkten (maximal 4)
            tangenten: Optionale Tangentenbedingungen
            grad: Grad des Polynoms (Standard 3)

        Returns:
            Schmiegkurve mit kubischem Polynom
        """
        if len(punkte) > 4:
            raise UngueltigePunkteError("Schmiegkegel unterstützt maximal 4 Punkte")

        return cls(punkte, tangenten=tangenten, grad=grad)

    def zeige_gleichungssystem(self) -> str:
        """
        Zeigt das zur Konstruktion verwendete Gleichungssystem an.

        Returns:
            Formatierter String mit dem Gleichungssystem
        """
        if "gleichungssystem" not in self._cache:
            x = symbols("x")

            # Erstelle allgemeines Polynom
            koeffizienten = [sp.symbols(f"a_{i}") for i in range(self.grad + 1)]
            polynom = sum(a * x**i for i, a in enumerate(koeffizienten))

            # Erstelle Gleichungen für die Anzeige
            gleichungen_text = []

            # Punktbedingungen
            for i, (x_i, y_i) in enumerate(self.punkte):
                gleichungen_text.append(f"P{i + 1}: f({x_i}) = {y_i}")

            # Tangentenbedingungen
            if self.tangenten:
                for i, (x_i, _) in enumerate(self.punkte):
                    if self.tangenten[i] is not None:
                        gleichungen_text.append(
                            f"T{i + 1}: f'({x_i}) = {self.tangenten[i]}"
                        )

            # Normalenbedingungen
            if self.normalen:
                for i, (x_i, _) in enumerate(self.punkte):
                    if self.normalen[i] is not None:
                        tangente = -1 / self.normalen[i]
                        gleichungen_text.append(
                            f"N{i + 1}: f'({x_i}) = {tangente:.3f} (aus Normale)"
                        )

            # Allgemeine Form
            gleichungen_text.append(f"Polynom: {polynom}")

            self._cache["gleichungssystem"] = "\n".join(gleichungen_text)

        return self._cache["gleichungssystem"]

    def validiere_loesung(self) -> dict:
        """
        Validiert, ob die erstellte Kurve alle Bedingungen erfüllt.

        Returns:
            Dictionary mit Validierungsergebnissen
        """
        ergebnisse = {
            "punkte_erfuellt": True,
            "tangenten_erfuellt": True,
            "normalen_erfuellt": True,
            "abweichungen": [],
        }

        # Prüfe Punktbedingungen
        for i, (x_i, y_i) in enumerate(self.punkte):
            berechnet_y = self.wert(x_i)
            abweichung = abs(berechnet_y - y_i)
            if abweichung > 1e-10:
                ergebnisse["punkte_erfuellt"] = False
                ergebnisse["abweichungen"].append(
                    f"Punkt {i + 1}: Erwartet {y_i}, erhalten {berechnet_y:.6f}"
                )

        # Prüfe Tangentenbedingungen
        if self.tangenten:
            ableitung = self.ableitung()
            for i, (x_i, _) in enumerate(self.punkte):
                if self.tangenten[i] is not None:
                    berechnete_tangente = ableitung.wert(x_i)
                    abweichung = abs(berechnete_tangente - self.tangenten[i])
                    if abweichung > 1e-10:
                        ergebnisse["tangenten_erfuellt"] = False
                        ergebnisse["abweichungen"].append(
                            f"Tangente {i + 1}: Erwartet {self.tangenten[i]}, "
                            f"erhalten {berechnete_tangente:.6f}"
                        )

        # Prüfe Normalenbedingungen
        if self.normalen:
            ableitung = self.ableitung()
            for i, (x_i, _) in enumerate(self.punkte):
                if self.normalen[i] is not None:
                    berechnete_tangente = ableitung.wert(x_i)
                    erwartete_tangente = -1 / self.normalen[i]
                    abweichung = abs(berechnete_tangente - erwartete_tangente)
                    if abweichung > 1e-10:
                        ergebnisse["normalen_erfuellt"] = False
                        ergebnisse["abweichungen"].append(
                            f"Normale {i + 1}: Erwartete Tangente {erwartete_tangente:.6f}, "
                            f"erhalten {berechnete_tangente:.6f}"
                        )

        return ergebnisse

    def _berechne_tangente_ableitung(self, x: float) -> float:
        """Hilfsmethode zur Berechnung der Tangentensteigung"""
        if "ableitung" not in self._cache:
            self._cache["ableitung"] = self.ableitung()
        return self._cache["ableitung"].wert(x)

    def zeige_schmiegkurve_plotly(
        self,
        x_range: tuple[float, float] = None,
        punkte: int = 200,
        zeige_tangenten: bool = True,
        zeige_punkte: bool = True,
        **kwargs,
    ) -> Any:
        """
        Zeigt die Schmiegkurve mit Punkten und optionalen Tangenten.

        Args:
            x_range: x-Bereich für die Darstellung
            punkte: Anzahl der zu berechnenden Punkte
            zeige_tangenten: Ob Tangenten an den Stützstellen angezeigt werden sollen
            zeige_punkte: Ob die Stützpunkte markiert werden sollen

        Returns:
            Plotly Figure oder Marimo UI Element
        """
        if x_range is None:
            # Automatischen Bereich basierend auf Punkten bestimmen
            x_werte = [p[0] for p in self.punkte]
            x_min, x_max = min(x_werte), max(x_werte)
            breite = x_max - x_min
            x_range = (x_min - breite * 0.2, x_max + breite * 0.2)

        # Erstelle x-Werte für die Kurve
        x_kurve = np.linspace(x_range[0], x_range[1], punkte)
        y_kurve = [self.wert(x) for x in x_kurve]

        fig = go.Figure()

        # Hauptkurve
        fig.add_trace(
            go.Scatter(
                x=x_kurve,
                y=y_kurve,
                mode="lines",
                name=f"Schmiegkurve: {self.term}",
                line={"color": config.COLORS["primary"], "width": 3},
            )
        )

        # Punkte markieren
        if zeige_punkte:
            x_punkte = [p[0] for p in self.punkte]
            y_punkte = [p[1] for p in self.punkte]

            fig.add_trace(
                go.Scatter(
                    x=x_punkte,
                    y=y_punkte,
                    mode="markers",
                    name="Stützpunkte",
                    marker={
                        "color": config.COLORS["secondary"],
                        "size": 10,
                        "symbol": "circle",
                    },
                )
            )

        # Tangenten anzeigen
        if zeige_tangenten and (self.tangenten or self.normalen):
            for i, (x_i, y_i) in enumerate(self.punkte):
                # Bestimme Tangentensteigung
                if self.tangenten and self.tangenten[i] is not None:
                    steigung = self.tangenten[i]
                elif self.normalen and self.normalen[i] is not None:
                    steigung = -1 / self.normalen[i]
                else:
                    continue

                # Berechne Tangentenpunkte für die Darstellung
                x_tangent = np.array([x_i - 0.5, x_i + 0.5])
                y_tangent = y_i + steigung * (x_tangent - x_i)

                # Stelle sicher, dass die Tangente im sichtbaren Bereich ist
                if all(x_range[0] <= x <= x_range[1] for x in x_tangent):
                    fig.add_trace(
                        go.Scatter(
                            x=x_tangent,
                            y=y_tangent,
                            mode="lines",
                            name=f"Tangente bei P{i + 1}",
                            line={
                                "color": config.COLORS["tertiary"],
                                "width": 2,
                                "dash": "dash",
                            },
                        )
                    )

        # Layout konfigurieren
        fig.update_layout(
            **config.get_plot_config(),
            title=kwargs.get("title", f"Schmiegkurve durch {len(self.punkte)} Punkte"),
            xaxis={
                **config.get_axis_config(mathematical_mode=True),
                "range": x_range,
                "title": "x",
            },
            yaxis={
                **config.get_axis_config(mathematical_mode=False),
                "title": f"f(x) = {self.term}",
            },
        )

        # Rückgabe mit Marimo UI wenn verfügbar
        try:
            import marimo as mo

            return mo.ui.plotly(fig)
        except ImportError:
            return fig

    def zeige_konstruktion_plotly(
        self, x_range: tuple[float, float] = None, **kwargs
    ) -> Any:
        """
        Zeigt detaillierte Konstruktionsinformationen mit Gleichungssystem.

        Args:
            x_range: x-Bereich für die Darstellung

        Returns:
            Plotly Figure mit Annotations
        """
        fig = self.zeige_schmiegkurve_plotly(x_range=x_range, **kwargs)

        # Füge Annotations mit Konstruktionsdetails hinzu
        annotations = []

        for i, (x_i, y_i) in enumerate(self.punkte):
            annotation_text = f"P{i + 1}({x_i}, {y_i})"

            if self.tangenten and self.tangenten[i] is not None:
                annotation_text += f"<br>T: {self.tangenten[i]}"
            elif self.normalen and self.normalen[i] is not None:
                annotation_text += f"<br>N: {self.normalen[i]}"

            annotations.append(
                {
                    "x": x_i,
                    "y": y_i,
                    "xref": "x",
                    "yref": "y",
                    "text": annotation_text,
                    "showarrow": True,
                    "arrowhead": 2,
                    "ax": 20,
                    "ay": -30,
                    "font": {"size": 10},
                }
            )

        fig.update_layout(annotations=annotations)

        try:
            import marimo as mo

            return mo.ui.plotly(fig)
        except ImportError:
            return fig

    def zeige_loesungsweg(self) -> str:
        """
        Zeigt den kompletten Lösungsweg der Schmiegkurven-Konstruktion.

        Returns:
            Formatierter Text mit dem kompletten Lösungsweg
        """
        loesungsweg = []

        loesungsweg.append("=" * 60)
        loesungsweg.append("SCHMIEGKURVEN-KONSTRUKTION - LÖSUNGSWEG")
        loesungsweg.append("=" * 60)
        loesungsweg.append("")

        # 1. Problemstellung
        loesungsweg.append("1. Problemstellung:")
        loesungsweg.append(f"   Gesucht: Polynom vom Grad {self.grad}")
        loesungsweg.append(f"   durch {len(self.punkte)} Punkte")

        if any(t is not None for t in self.tangenten):
            anzahl_t = sum(1 for t in self.tangenten if t is not None)
            loesungsweg.append(f"   mit {anzahl_t} Tangentenbedingungen")

        if any(n is not None for n in self.normalen):
            anzahl_n = sum(1 for n in self.normalen if n is not None)
            loesungsweg.append(f"   mit {anzahl_n} Normalenbedingungen")

        loesungsweg.append("")

        # 2. Punkte und Bedingungen
        loesungsweg.append("2. Gegebene Bedingungen:")
        for i, (x, y) in enumerate(self.punkte):
            bedingungen = [f"P{i + 1}({x}, {y})"]

            if self.tangenten and self.tangenten[i] is not None:
                bedingungen.append(f'f"({x}) = {self.tangenten[i]}')

            if self.normalen and self.normalen[i] is not None:
                bedingungen.append(f"Normale: m = {self.normalen[i]}")

            separator = ", "
            loesungsweg.append(f"   {separator.join(bedingungen)}")

        loesungsweg.append("")

        # 3. Lösung und Validierung
        loesungsweg.append("3. Lösung:")
        loesungsweg.append(f"   f(x) = {self.term}")

        validierung = self.validiere_loesung()
        if validierung["abweichungen"]:
            loesungsweg.append("   ⚠️  Warnungen:")
            for abweichung in validierung["abweichungen"]:
                loesungsweg.append(f"      - {abweichung}")
        else:
            loesungsweg.append("   ✅ Alle Bedingungen erfüllt!")

        return "\n".join(loesungsweg)
