"""
Interactive Function Explorer für das Schul-Analysis Framework.

Dieses Modul bietet eine interaktive Oberfläche zur Erforschung mathematischer
Funktionen mit real-time Visualisierung, Parameter-Manipulation und
didaktischen Erklärungen für den Unterricht.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import sympy as sp
from sympy import latex, symbols

from .funktion import Funktion
from .sympy_types import ExtremumTyp, WendepunktTyp
from .visualisierung import Graph

# Importiere Plotly für interaktive Visualisierung
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logging.warning("Plotly nicht verfügbar - interaktive Features deaktiviert")


class InteraktiverFunktionExplorer:
    """
    Interaktiver Explorer für mathematische Funktionen mit didaktischen Features.

    Diese Klasse ermöglicht Lehrern und Schülern, Funktionen interaktiv zu
    erforschen mit:
    - Real-time Parameter-Manipulation
    - Visualisierung von Ableitungen
    - Analyse von Extremstellen und Wendepunkten
    - Didaktische Erklärungen und Hinweise
    """

    def __init__(
        self,
        basis_funktion: Union[str, Funktion],
        parameter: Optional[Dict[str, float]] = None,
    ):
        """
        Initialisiert den interaktiven Explorer.

        Args:
            basis_funktion: Grundfunktion als String oder Funktion-Objekt
            parameter: Standardparameter-Werte (z.B. {'a': 2, 'b': -3})
        """
        if isinstance(basis_funktion, str):
            self.basis_funktion = Funktion(basis_funktion)
        else:
            self.basis_funktion = basis_funktion

        self.parameter = parameter or {}
        self.aktuelle_funktion = (
            self.basis_funktion.setze_parameter(**self.parameter)
            if self.parameter
            else self.basis_funktion
        )

        # Explorer-Zustand
        self.zeige_ableitungen = [True, False, False]  # f, f', f''
        self.zeige_punkte = {
            "nullstellen": True,
            "extremstellen": True,
            "wendepunkte": True,
            "definitionsluecken": True,
        }
        self.x_bereich = (-10, 10)
        self.analyse_ergebnisse = {}

        # Logging für Debugging
        self.logger = logging.getLogger(__name__)

    def setze_parameter(self, **kwargs) -> "InteraktiverFunktionExplorer":
        """
        Aktualisiert Parameter und gibt neuen Explorer zurück.

        Args:
            **kwargs: Neue Parameter-Werte

        Returns:
            Neuer Explorer mit aktualisierten Parametern
        """
        neue_parameter = {**self.parameter, **kwargs}
        return InteraktiverFunktionExplorer(self.basis_funktion, neue_parameter)

    def analysiere_funktion(self) -> Dict[str, Any]:
        """
        Führt vollständige Funktionsanalyse durch.

        Returns:
            Dictionary mit Analyseergebnissen
        """
        if not self.analyse_ergebnisse:
            self.analyse_ergebnisse = {
                "nullstellen": self._berechne_nullstellen(),
                "extremstellen": self._berechne_extremstellen(),
                "wendepunkte": self._berechne_wendepunkte(),
                "definitionsluecken": self._berechne_definitionsluecken(),
                "ableitungen": self._berechne_ableitungen(),
                "asymptoten": self._berechne_asymptoten(),
            }

        return self.analyse_ergebnisse

    def erstelle_interaktives_diagramm(self) -> Optional[go.Figure]:
        """
        Erstellt ein interaktives Plotly-Diagramm mit allen Features.

        Returns:
            Plotly-Figur oder None wenn Plotly nicht verfügbar
        """
        if not PLOTLY_AVAILABLE:
            self.logger.warning(
                "Plotly nicht verfügbar - kann kein interaktives Diagramm erstellen"
            )
            return None

        # Analyse durchführen
        analyse = self.analysiere_funktion()

        # Erstelle Subplots für Hauptfunktion und Ableitungen
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Funktion f(x)",
                "Erste Ableitung f'(x)",
                "Zweite Ableitung f''(x)",
                "Zusammenfassung",
            ),
            specs=[
                [{"secondary_y": False}, {"secondary_y": False}],
                [{"secondary_y": False}, {"type": "table"}],
            ],
        )

        # X-Werte für Plots
        x_vals = [
            x / 10
            for x in range(int(self.x_bereich[0] * 10), int(self.x_bereich[1] * 10) + 1)
        ]

        # Hauptfunktion plotten
        if self.zeige_ableitungen[0]:
            y_vals = [self.aktuelle_funktion.wert(x) for x in x_vals]
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    name=f"f(x) = {self.aktuelle_funktion.term()}",
                    line=dict(color="blue", width=2),
                ),
                row=1,
                col=1,
            )

        # Erste Ableitung
        if self.zeige_ableitungen[1]:
            f1 = self.aktuelle_funktion.ableitung(1)
            y1_vals = [f1.wert(x) for x in x_vals]
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=y1_vals,
                    name=f"f'(x) = {f1.term()}",
                    line=dict(color="red", width=2),
                ),
                row=1,
                col=2,
            )

        # Zweite Ableitung
        if self.zeige_ableitungen[2]:
            f2 = self.aktuelle_funktion.ableitung(2)
            y2_vals = [f2.wert(x) for x in x_vals]
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=y2_vals,
                    name=f"f''(x) = {f2.term()}",
                    line=dict(color="green", width=2),
                ),
                row=2,
                col=1,
            )

        # Spezielle Punkte hinzufügen
        self._fuege_punkte_hinzu(fig, analyse)

        # Layout optimieren
        fig.update_layout(
            title_text=f"Interaktiver Function Explorer: {self.aktuelle_funktion.term()}",
            title_x=0.5,
            height=800,
            showlegend=True,
            hovermode="x unified",
        )

        # Zusammenfassungstabelle erstellen
        self._erstelle_zusammenfassung_tabelle(fig, analyse)

        return fig

    def erstelle_parameter_slider(self) -> Optional[Dict[str, Any]]:
        """
        Erstellt Konfiguration für Parameter-Slider.

        Returns:
            Dictionary mit Slider-Konfiguration oder None
        """
        if not self.basis_funktion.parameter:
            return None

        sliders = []
        for param in self.basis_funktion.parameter:
            param_name = str(param)
            current_value = self.parameter.get(param_name, 1.0)

            sliders.append(
                {
                    "type": "buttons",
                    "buttons": [
                        {
                            "args": [{"y": [current_value - 1]}],
                            "label": f"{param_name} - 1",
                            "method": "relayout",
                        },
                        {
                            "args": [{"y": [current_value + 1]}],
                            "label": f"{param_name} + 1",
                            "method": "relayout",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 87},
                    "showactive": False,
                    "x": 0.1,
                    "xanchor": "left",
                    "y": 1.02,
                    "yanchor": "top",
                }
            )

        return {"sliders": sliders}

    def _berechne_nullstellen(self) -> List[Dict[str, Any]]:
        """Berechnet Nullstellen mit didaktischen Informationen."""
        try:
            nullstellen = self.aktuelle_funktion.nullstellen
            return [
                {
                    "x": float(ns) if hasattr(ns, "__float__") else ns,
                    "typ": "Nullstelle",
                    "beschreibung": f"Die Funktion schneidet die x-Achse bei x = {ns}",
                }
                for ns in nullstellen
            ]
        except Exception as e:
            self.logger.warning(f"Fehler bei Nullstellenberechnung: {e}")
            return []

    def _berechne_extremstellen(self) -> List[Dict[str, Any]]:
        """Berechnet Extremstellen mit didaktischen Informationen."""
        try:
            extremstellen = self.aktuelle_funktion.extremstellen(real=True)
            ergebnisse = []

            for x_wert, y_wert, art in extremstellen:
                typ = (
                    ExtremumTyp.MINIMUM
                    if "Minimum" in str(art)
                    else ExtremumTyp.MAXIMUM
                )
                ergebnisse.append(
                    {
                        "x": float(x_wert) if hasattr(x_wert, "__float__") else x_wert,
                        "y": float(y_wert) if hasattr(y_wert, "__float__") else y_wert,
                        "typ": "Extremstelle",
                        "art": typ.value,
                        "beschreibung": f"{typ.value} bei ({x_wert:.2f}|{y_wert:.2f})",
                    }
                )

            return ergebnisse
        except Exception as e:
            self.logger.warning(f"Fehler bei Extremstellenberechnung: {e}")
            return []

    def _berechne_wendepunkte(self) -> List[Dict[str, Any]]:
        """Berechnet Wendepunkte mit didaktischen Informationen."""
        try:
            # Versuche verschiedene Methoden für Wendepunkte
            try:
                wendepunkte = self.aktuelle_funktion.wendepunkte()
            except AttributeError:
                wendepunkte = []

            ergebnisse = []
            for wp in wendepunkte:
                if hasattr(wp, "x") and hasattr(wp, "typ"):
                    ergebnisse.append(
                        {
                            "x": float(wp.x) if hasattr(wp.x, "__float__") else wp.x,
                            "typ": "Wendepunkt",
                            "art": wp.typ.value
                            if hasattr(wp.typ, "value")
                            else str(wp.typ),
                            "beschreibung": f"Wendepunkt bei x = {wp.x}",
                        }
                    )

            return ergebnisse
        except Exception as e:
            self.logger.warning(f"Fehler bei Wendepunktberechnung: {e}")
            return []

    def _berechne_definitionsluecken(self) -> List[Dict[str, Any]]:
        """Berechnet Definitionslücken."""
        try:
            if hasattr(self.aktuelle_funktion, "polstellen"):
                polstellen = self.aktuelle_funktion.polstellen()
                return [
                    {
                        "x": float(ps) if hasattr(ps, "__float__") else ps,
                        "typ": "Definitionslücke",
                        "beschreibung": f"Polstelle bei x = {ps}",
                    }
                    for ps in polstellen
                ]
            return []
        except Exception as e:
            self.logger.warning(f"Fehler bei Definitionslückenberechnung: {e}")
            return []

    def _berechne_ableitungen(self) -> Dict[str, str]:
        """Berechnet Ableitungen als LaTeX-Ausdrücke."""
        ableitungen = {}

        try:
            f1 = self.aktuelle_funktion.ableitung(1)
            ableitungen["erste"] = latex(f1.term_sympy)

            f2 = self.aktuelle_funktion.ableitung(2)
            ableitungen["zweite"] = latex(f2.term_sympy)

        except Exception as e:
            self.logger.warning(f"Fehler bei Ableitungsberechnung: {e}")

        return ableitungen

    def _berechne_asymptoten(self) -> Dict[str, Any]:
        """Berechnet Asymptoten."""
        # Vereinfachte Asymptotenberechnung
        return {"vertikal": [], "horizontal": [], "schräg": []}

    def _fuege_punkte_hinzu(self, fig: go.Figure, analyse: Dict[str, Any]) -> None:
        """Fügt spezielle Punkte zum Diagramm hinzu."""

        # Nullstellen
        if self.zeige_punkte["nullstellen"]:
            for ns in analyse["nullstellen"]:
                if isinstance(ns["x"], (int, float)):
                    fig.add_trace(
                        go.Scatter(
                            x=[ns["x"]],
                            y=[0],
                            mode="markers",
                            marker=dict(color="blue", size=10, symbol="circle"),
                            name=ns["typ"],
                            hovertext=ns["beschreibung"],
                        ),
                        row=1,
                        col=1,
                    )

        # Extremstellen
        if self.zeige_punkte["extremstellen"]:
            for es in analyse["extremstellen"]:
                if isinstance(es["x"], (int, float)) and isinstance(
                    es["y"], (int, float)
                ):
                    farbe = "red" if "Maximum" in es["art"] else "darkred"
                    fig.add_trace(
                        go.Scatter(
                            x=[es["x"]],
                            y=[es["y"]],
                            mode="markers",
                            marker=dict(color=farbe, size=12, symbol="diamond"),
                            name=f"{es['art']}",
                            hovertext=es["beschreibung"],
                        ),
                        row=1,
                        col=1,
                    )

    def _erstelle_zusammenfassung_tabelle(
        self, fig: go.Figure, analyse: Dict[str, Any]
    ) -> None:
        """Erstellt eine Zusammenfassungstabelle."""

        # Tabellendaten vorbereiten
        table_data = []

        # Nullstellen
        for ns in analyse["nullstellen"]:
            table_data.append(["Nullstelle", f"x = {ns['x']}", ""])

        # Extremstellen
        for es in analyse["extremstellen"]:
            table_data.append(["Extremstelle", f"x = {es['x']}", es["art"]])

        # Wendepunkte
        for wp in analyse["wendepunkte"]:
            table_data.append(["Wendepunkt", f"x = {wp['x']}", wp.get("art", "")])

        if table_data:
            fig.add_trace(
                go.Table(
                    header=dict(
                        values=["Typ", "x-Wert", "Eigenschaft"], fill_color="lightblue"
                    ),
                    cells=dict(
                        values=list(zip(*table_data)) if table_data else [[], [], []],
                        fill_color="white",
                    ),
                    name="Analyse-Zusammenfassung",
                ),
                row=2,
                col=2,
            )

    def exportiere_analyse(self, format: str = "dict") -> Union[Dict[str, Any], str]:
        """
        Exportiert die Analyse in verschiedenen Formaten.

        Args:
            format: 'dict', 'json', 'latex', 'markdown'

        Returns:
            Exportierte Analyse
        """
        analyse = self.analysiere_funktion()

        if format == "dict":
            return analyse
        elif format == "json":
            import json

            return json.dumps(analyse, indent=2, default=str)
        elif format == "latex":
            return self._exportiere_latex(analyse)
        elif format == "markdown":
            return self._exportiere_markdown(analyse)
        else:
            raise ValueError(f"Unbekanntes Format: {format}")

    def _exportiere_latex(self, analyse: Dict[str, Any]) -> str:
        """Exportiert Analyse als LaTeX-Dokument."""
        latex_content = [
            r"\documentclass{article}",
            r"\usepackage[ngerman]{babel}",
            r"\usepackage{amsmath}",
            r"\usepackage{amssymb}",
            r"\begin{document}",
            r"\title{Funktionsanalyse}",
            r"\maketitle",
            f"\section*{Funktion: $f(x) = {latex(self.aktuelle_funktion.term_sympy)}$}",
            "",
        ]

        # Nullstellen
        if analyse["nullstellen"]:
            latex_content.append(r"\subsection*{Nullstellen}")
            for ns in analyse["nullstellen"]:
                latex_content.append(f"\\item $x = {ns['x']}$")
            latex_content.append("")

        return "\n".join(latex_content) + r"\end{document}"

    def _exportiere_markdown(self, analyse: Dict[str, Any]) -> str:
        """Exportiert Analyse als Markdown-Dokument."""
        md_content = [
            f"# Funktionsanalyse: {self.aktuelle_funktion.term()}",
            "",
            "## Funktion",
            f"$$f(x) = {latex(self.aktuelle_funktion.term_sympy)}$$",
            "",
        ]

        # Parameter
        if self.parameter:
            md_content.append("## Parameter")
            for param, wert in self.parameter.items():
                md_content.append(f"- {param} = {wert}")
            md_content.append("")

        # Nullstellen
        if analyse["nullstellen"]:
            md_content.append("## Nullstellen")
            for ns in analyse["nullstellen"]:
                md_content.append(f"- $x = {ns['x']}$")
            md_content.append("")

        return "\n".join(md_content)


# Convenience Funktionen für schnellen Zugriff
def ErstelleInteraktivenExplorer(
    funktion: Union[str, Funktion], **parameter
) -> InteraktiverFunktionExplorer:
    """
    Erstellt einen interaktiven Funktionsexplorer.

    Args:
        funktion: Funktion als String oder Funktion-Objekt
        **parameter: Parameter-Werte

    Returns:
        InteraktiverFunktionExplorer Instanz

    Examples:
        >>> explorer = ErstelleInteraktivenExplorer("a*x^2 + b*x + c", a=1, b=-4, c=3)
        >>> fig = explorer.erstelle_interaktives_diagramm()
        >>> analyse = explorer.exportiere_analyse('markdown')
    """
    return InteraktiverFunktionExplorer(funktion, parameter)


def ZeigeInteraktiveAnalyse(
    funktion: Union[str, Funktion], **parameter
) -> Optional[go.Figure]:
    """
    Schnelle Funktion zur Erstellung einer interaktiven Analyse.

    Args:
        funktion: Zu analysierende Funktion
        **parameter: Parameter-Werte

    Returns:
        Plotly-Figur oder None
    """
    explorer = ErstelleInteraktivenExplorer(funktion, **parameter)
    return explorer.erstelle_interaktives_diagramm()
