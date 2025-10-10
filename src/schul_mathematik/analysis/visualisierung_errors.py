"""
Erweiterte Fehlerbehandlung für Visualisierungen

Spezialisierte Fehlerklassen und Hilfsfunktionen für die Behandlung von
Visualisierungsproblemen im Schul-Analysis Framework.
"""

from typing import Any, Optional
import numpy as np
import plotly.graph_objects as go

from .errors import (
    SchulAnalysisError,
    VisualisierungsError,
    DarstellungsError,
    MathematischerDomainError,
    handle_schul_analysis_error,
)


class PlotBereichError(VisualisierungsError):
    """Fehler bei ungültigen Plot-Bereichen"""

    def __init__(
        self,
        problem: str,
        x_bereich: Optional[tuple] = None,
        y_bereich: Optional[tuple] = None,
    ):
        super().__init__("Plot-Bereich", problem)
        self.x_bereich = x_bereich
        self.y_bereich = y_bereich

        if x_bereich and x_bereich[0] >= x_bereich[1]:
            self.suggestion = "Der x-Bereich muss gültig sein (von < bis)."
        elif y_bereich and y_bereich[0] >= y_bereich[1]:
            self.suggestion = "Der y-Bereich muss gültig sein (von < bis)."
        else:
            self.suggestion = (
                "Prüfe die Bereichsangaben und wähle einen sinnvollen Wertebereich."
            )


class DatenpunktBerechnungsError(VisualisierungsError):
    """Fehler bei der Berechnung von Datenpunkten"""

    def __init__(self, funktionstyp: str, problem: str, x_wert: Optional[float] = None):
        super().__init__(f"Datenpunkt-Berechnung ({funktionstyp})", problem)
        self.funktionstyp = funktionstyp
        self.x_wert = x_wert

        if "Division durch Null" in problem:
            self.suggestion = "Die Funktion hat wahrscheinlich eine Polstelle an dieser Position. Verwende einen anderen x-Bereich."
        elif "Overflow" in problem:
            self.suggestion = "Der Funktionswert ist zu groß. Verkleinere den x-Bereich oder verwende logarithmische Darstellung."
        else:
            self.suggestion = (
                "Prüfe die Funktionseingabe und wähle einen geeigneten x-Bereich."
            )


class PlotKonfigurationError(VisualisierungsError):
    """Fehler bei der Plot-Konfiguration"""

    def __init__(self, parameter: str, wert: Any, erlaubte_werte: list):
        super().__init__(
            "Plot-Konfiguration", f"Ungültiger Parameter '{parameter}': {wert}"
        )
        self.parameter = parameter
        self.wert = wert
        self.erlaubte_werte = erlaubte_werte

        self.suggestion = (
            f"Erlaubte Werte für '{parameter}': {', '.join(map(str, erlaubte_werte))}"
        )


class MehrfachFunktionenError(VisualisierungsError):
    """Fehler bei der Darstellung mehrerer Funktionen"""

    def __init__(self, anzahl_funktionen: int, max_erlaubt: int):
        super().__init__(
            "Mehrfachfunktionen-Darstellung",
            f"Zu viele Funktionen: {anzahl_funktionen} > {max_erlaubt}",
        )
        self.anzahl_funktionen = anzahl_funktionen
        self.max_erlaubt = max_erlaubt

        self.suggestion = (
            f"Reduziere die Anzahl der Funktionen auf maximal {max_erlaubt}."
        )


class AspektVerhaeltnisError(VisualisierungsError):
    """Fehler bei der Aspect-Ratio-Konfiguration"""

    def __init__(self, problem: str, aspect_ratio: Optional[float] = None):
        super().__init__("Aspect-Ratio", problem)
        self.aspect_ratio = aspect_ratio

        if aspect_ratio and aspect_ratio <= 0:
            self.suggestion = (
                "Das Aspect-Ratio muss positiv sein (z.B. 1.0 für quadratisch)."
            )
        else:
            self.suggestion = (
                "Verwende ein gültiges Aspect-Ratio (z.B. 1.0, 1.5, 16/9)."
            )


class InteraktiveElementeError(VisualisierungsError):
    """Fehler bei interaktiven Plot-Elementen"""

    def __init__(self, elementtyp: str, problem: str):
        super().__init__(f"Interaktive Elemente ({elementtyp})", problem)
        self.elementtyp = elementtyp

        self.suggestion = "Prüfe die Konfiguration der interaktiven Elemente und deaktiviere sie bei Problemen."


class VisualisierungsPerformanceError(VisualisierungsError):
    """Fehler bei Performance-Problemen"""

    def __init__(self, operation: str, dauer: float, max_dauer: float):
        super().__init__(
            "Performance", f"{operation} zu langsam: {dauer:.2f}s > {max_dauer:.2f}s"
        )
        self.operation = operation
        self.dauer = dauer
        self.max_dauer = max_dauer

        self.suggestion = (
            "Reduziere die Anzahl der Datenpunkte oder vereinfache die Funktion."
        )


# Hilfsfunktionen für die Fehlerbehandlung


def validiere_plot_bereich(
    x_min: float,
    x_max: float,
    y_min: Optional[float] = None,
    y_max: Optional[float] = None,
) -> None:
    """
    Validiert den Plot-Bereich und wirft bei Problemen eine Ausnahme

    Args:
        x_min, x_max: x-Bereich
        y_min, y_max: y-Bereich (optional)

    Raises:
        PlotBereichError: Bei ungültigem Bereich
    """
    if x_min >= x_max:
        raise PlotBereichError(
            f"Ungültiger x-Bereich: [{x_min}, {x_max}]", x_bereich=(x_min, x_max)
        )

    if y_min is not None and y_max is not None and y_min >= y_max:
        raise PlotBereichError(
            f"Ungültiger y-Bereich: [{y_min}, {y_max}]", y_bereich=(y_min, y_max)
        )

    # Prüfe auf unvernünftig große Bereiche
    if abs(x_max - x_min) > 1e6:
        raise PlotBereichError(
            f"x-Bereich zu groß: [{x_min}, {x_max}]", x_bereich=(x_min, x_max)
        )


def validiere_anzahl_funktionen(funktionen: list, max_anzahl: int = 10) -> None:
    """
    Validiert die Anzahl der Funktionen für Mehrfachdarstellung

    Args:
        funktionen: Liste der Funktionen
        max_anzahl: Maximale erlaubte Anzahl

    Raises:
        MehrfachFunktionenError: Bei zu vielen Funktionen
    """
    if len(funktionen) > max_anzahl:
        raise MehrfachFunktionenError(len(funktionen), max_anzahl)


def validiere_aspect_ratio(aspect_ratio: float) -> None:
    """
    Validiert das Aspect-Ratio

    Args:
        aspect_ratio: Aspect-Ratio Wert

    Raises:
        AspektVerhaeltnisError: Bei ungültigem Aspect-Ratio
    """
    if aspect_ratio <= 0:
        raise AspektVerhaeltnisError(
            f"Ungültiges Aspect-Ratio: {aspect_ratio}", aspect_ratio=aspect_ratio
        )

    # Prüfe auf unvernünftig große/kleine Werte
    if aspect_ratio > 10 or aspect_ratio < 0.1:
        raise AspektVerhaeltnisError(
            f"Extremes Aspect-Ratio: {aspect_ratio}", aspect_ratio=aspect_ratio
        )


def sicher_berechne_datenpunkte(
    funktion, x_werte: np.ndarray, funktionstyp: str = "Funktion"
) -> tuple[np.ndarray, np.ndarray]:
    """
    Berechnet Datenpunkte sicher mit Fehlerbehandlung

    Args:
        funktion: Die zu berechnende Funktion
        x_werte: x-Werte als numpy-Array
        funktionstyp: Typ der Funktion für Fehlermeldungen

    Returns:
        Tuple (x_werte_gueltig, y_werte) mit gültigen Datenpunkten

    Raises:
        DatenpunktBerechnungsError: Bei Berechnungsfehlern
    """
    y_werte = []
    gueltige_x = []

    for x in x_werte:
        try:
            y = funktion(x)

            # Prüfe auf NaN oder Inf
            if np.isnan(y) or np.isinf(y):
                continue

            y_werte.append(y)
            gueltige_x.append(x)

        except (ValueError, TypeError, ZeroDivisionError, OverflowError) as e:
            # Einzelnfehler werden ignoriert, aber protokolliert
            continue
        except Exception as e:
            raise DatenpunktBerechnungsError(
                funktionstyp, f"Unerwarteter Fehler bei x={x}: {str(e)}", x_wert=x
            )

    if not gueltige_x:
        raise DatenpunktBerechnungsError(
            funktionstyp, "Keine gültigen Datenpunkte berechenbar"
        )

    return np.array(gueltige_x), np.array(y_werte)


def behandle_visualisierungs_fehler(func):
    """
    Decorator für automatische Fehlerbehandlung in Visualisierungsfunktionen

    Args:
        func: Die zu dekorierende Funktion

    Returns:
        Dekorierte Funktion mit Fehlerbehandlung
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SchulAnalysisError:
            # Unsere eigenen Fehler werden weitergereicht
            raise
        except (ValueError, TypeError, ZeroDivisionError, OverflowError) as e:
            # Bekannte mathematische Fehler
            raise DarstellungsError("Allgemeine Funktion", str(e))
        except Exception as e:
            # Unerwartete Fehler
            raise VisualisierungsError("Unbekannt", f"Unerwarteter Fehler: {str(e)}")

    return wrapper


def erstelle_fehlerhafte_visualisierung(
    fehlermeldung: str, titel: str = "Fehler"
) -> go.Figure:
    """
    Erstellt eine Fehler-Visualisierung für den Fall, dass nichts angezeigt werden kann

    Args:
        fehlermeldung: Die anzuzeigende Fehlermeldung
        titel: Titel für die Figur

    Returns:
        Plotly-Figur mit Fehlermeldung
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="text",
            text=[fehlermeldung],
            textposition="middle center",
            showlegend=False,
            marker=dict(color="red", size=20),
        )
    )

    fig.update_layout(
        title=titel,
        xaxis=dict(showgrid=False, showticklabels=False, range=[-1, 1]),
        yaxis=dict(showgrid=False, showticklabels=False, range=[-1, 1]),
        plot_bgcolor="lightyellow",
        paper_bgcolor="white",
        width=600,
        height=400,
    )

    return fig


# Export der Klassen und Funktionen
__all__ = [
    "PlotBereichError",
    "DatenpunktBerechnungsError",
    "PlotKonfigurationError",
    "MehrfachFunktionenError",
    "AspektVerhaeltnisError",
    "InteraktiveElementeError",
    "VisualisierungsPerformanceError",
    "validiere_plot_bereich",
    "validiere_anzahl_funktionen",
    "validiere_aspect_ratio",
    "sicher_berechne_datenpunkte",
    "behandle_visualisierungs_fehler",
    "erstelle_fehlerhafte_visualisierung",
]
