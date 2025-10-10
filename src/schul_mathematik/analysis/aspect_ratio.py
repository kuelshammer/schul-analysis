"""
Enhanced Aspect Ratio Control for Plotly Visualizations

This module provides sophisticated aspect ratio control for mathematical visualizations,
ensuring proper mathematical proportions and educational accuracy in the Schul-Analysis Framework.
"""

from typing import Any

import plotly.graph_objects as go

from .visualisierung_errors import AspektVerhaeltnisError, validiere_aspect_ratio


class AspectRatioType:
    """Enumeration für verschiedene Aspect-Ratio-Typen"""

    QUADRATISCH = "quadratisch"  # 1:1 für mathematische Genauigkeit
    GOLDENER_SCHNITT = "goldener_schnitt"  # ≈1.618 für ästhetische Proportionen
    BREITBILD = "breitbild"  # 16:9 für moderne Displays
    STANDARD = "standard"  # 4:3 klassisches Format
    KINO = "kino"  # 21:9 ultra-breit
    CUSTOM = "custom"  # Benutzerdefiniert


class AspectRatioController:
    """Kontrolliert das Aspect-Ratio für Plotly-Visualisierungen"""

    # Vordefinierte Aspect-Ratios
    PREDEFINED_RATIOS = {
        AspectRatioType.QUADRATISCH: 1.0,
        AspectRatioType.GOLDENER_SCHNITT: 1.618033988749895,
        AspectRatioType.BREITBILD: 16 / 9,
        AspectRatioType.STANDARD: 4 / 3,
        AspectRatioType.KINO: 21 / 9,
    }

    # Namen für die Anzeige
    RATIO_NAMES = {
        AspectRatioType.QUADRATISCH: "Quadratisch (1:1)",
        AspectRatioType.GOLDENER_SCHNITT: "Goldener Schnitt (≈1.618:1)",
        AspectRatioType.BREITBILD: "Breitbild (16:9)",
        AspectRatioType.STANDARD: "Standard (4:3)",
        AspectRatioType.KINO: "Kino (21:9)",
        AspectRatioType.CUSTOM: "Benutzerdefiniert",
    }

    def __init__(self):
        self.current_ratio = AspectRatioType.QUADRATISCH
        self.custom_ratio = 1.0
        self.auto_adjust = True
        self.mathematical_mode = True

    def set_aspect_ratio(
        self, ratio_type: str, custom_value: float | None = None
    ) -> None:
        """
        Setzt das Aspect-Ratio

        Args:
            ratio_type: Typ des Aspect-Ratios
            custom_value: Benutzerdefinierter Wert (nur für CUSTOM)
        """
        if (
            ratio_type not in self.PREDEFINED_RATIOS
            and ratio_type != AspectRatioType.CUSTOM
        ):
            raise AspektVerhaeltnisError(f"Unbekannter Aspect-Ratio-Typ: {ratio_type}")

        self.current_ratio = ratio_type

        if ratio_type == AspectRatioType.CUSTOM:
            if custom_value is None:
                raise AspektVerhaeltnisError(
                    "Für benutzerdefiniertes Aspect-Ratio muss ein Wert angegeben werden"
                )
            validiere_aspect_ratio(custom_value)
            self.custom_ratio = custom_value

    def get_aspect_ratio_value(self) -> float:
        """Gibt den aktuellen Aspect-Ratio-Wert zurück"""
        if self.current_ratio == AspectRatioType.CUSTOM:
            return self.custom_ratio
        return self.PREDEFINED_RATIOS[self.current_ratio]

    def get_aspect_ratio_name(self) -> str:
        """Gibt den Namen des aktuellen Aspect-Ratios zurück"""
        return self.RATIO_NAMES[self.current_ratio]

    def calculate_figure_dimensions(
        self, base_width: int = 800, min_width: int = 400, max_width: int = 1200
    ) -> tuple[int, int]:
        """
        Berechnet Figurendimensionen basierend auf Aspect-Ratio

        Args:
            base_width: Basisbreite
            min_width: Minimale Breite
            max_width: Maximale Breite

        Returns:
            Tuple (width, height)
        """
        # Begrenze die Breite auf sinnvolle Werte
        width = max(min_width, min(max_width, base_width))
        aspect_ratio = self.get_aspect_ratio_value()

        # Berechne Höhe basierend auf Aspect-Ratio
        height = int(width / aspect_ratio)

        return width, height

    def create_mathematical_aspect_config(self) -> dict[str, Any]:
        """
        Erstellt Konfiguration für mathematisches Aspect-Ratio

        Returns:
            Dictionary mit Plotly-Konfiguration
        """
        if not self.mathematical_mode:
            return {}

        aspect_ratio = self.get_aspect_ratio_value()

        return {
            "xaxis": {
                "scaleanchor": "y",
                "scaleratio": aspect_ratio,
            },
            "yaxis": {
                "scaleanchor": "x",
                "scaleratio": 1.0 / aspect_ratio,
            },
        }

    def auto_adjust_for_content(
        self,
        x_range: tuple[float, float],
        y_range: tuple[float, float],
        padding: float = 0.1,
    ) -> tuple[float, float]:
        """
        Passt das Aspect-Ratio automatisch an den Inhalt an

        Args:
            x_range: x-Bereich (min, max)
            y_range: y-Bereich (min, max)
            padding: Zusätzlicher Abstand (10%)

        Returns:
            Angepasstes Aspect-Ratio
        """
        if not self.auto_adjust:
            return self.get_aspect_ratio_value()

        x_span = abs(x_range[1] - x_range[0])
        y_span = abs(y_range[1] - y_range[0])

        if y_span == 0:
            return self.get_aspect_ratio_value()

        # Berechne natürliches Aspect-Ratio des Inhalts
        content_ratio = x_span / y_span

        # Füge Padding hinzu
        content_ratio *= 1 + padding

        # Wähle das nächstliegende vordefinierte Ratio
        best_match = self.current_ratio
        min_difference = float("inf")

        for ratio_type, ratio_value in self.PREDEFINED_RATIOS.items():
            difference = abs(ratio_value - content_ratio)
            if difference < min_difference:
                min_difference = difference
                best_match = ratio_type

        # Nur ändern, wenn der Unterschied signifikant ist (> 20%)
        if min_difference > 0.2 * content_ratio:
            self.current_ratio = best_match

        return self.get_aspect_ratio_value()

    def apply_to_figure(
        self,
        fig: go.Figure,
        x_range: tuple[float, float] | None = None,
        y_range: tuple[float, float] | None = None,
        base_width: int = 800,
    ) -> go.Figure:
        """
        Wendet das Aspect-Ratio auf eine Plotly-Figur an

        Args:
            fig: Plotly-Figur
            x_range: Optional x-Bereich für Auto-Adjust
            y_range: Optional y-Bereich für Auto-Adjust
            base_width: Basisbreite für die Figurengröße

        Returns:
            Angepasste Plotly-Figur
        """
        # Auto-Adjust, wenn Bereiche gegeben sind
        if x_range is not None and y_range is not None:
            self.auto_adjust_for_content(x_range, y_range)

        # Berechne Dimensionen
        width, height = self.calculate_figure_dimensions(base_width)

        # Erstelle Aspect-Ratio-Konfiguration
        aspect_config = self.create_mathematical_aspect_config()

        # Kombiniere mit Basis-Layout
        layout_updates = {"width": width, "height": height, **aspect_config}

        # Wende Updates an
        fig.update_layout(**layout_updates)

        return fig

    def create_ratio_selector_config(self) -> dict[str, Any]:
        """
        Erstellt Konfiguration für einen interaktiven Aspect-Ratio-Selector

        Returns:
            Dictionary für Plotly-Buttons
        """
        buttons = []

        for ratio_type in self.PREDEFINED_RATIOS.keys():
            buttons.append(
                {
                    "args": [
                        {
                            "xaxis.scaleanchor": "y",
                            "xaxis.scaleratio": self.PREDEFINED_RATIOS[ratio_type],
                            "width": 800,
                            "height": int(800 / self.PREDEFINED_RATIOS[ratio_type]),
                        }
                    ],
                    "label": self.RATIO_NAMES[ratio_type],
                    "method": "relayout",
                }
            )

        return {
            "type": "buttons",
            "direction": "down",
            "showactive": True,
            "x": 0.01,
            "xanchor": "left",
            "y": 1.02,
            "yanchor": "top",
            "buttons": buttons,
        }


# Globale Instanz
aspect_ratio_controller = AspectRatioController()


# Convenience-Funktionen für die API
def setze_aspect_ratio(ratio_type: str, custom_value: float | None = None) -> None:
    """
    Setzt das globale Aspect-Ratio

    Args:
        ratio_type: Typ des Aspect-Ratios
        custom_value: Benutzerdefinierter Wert

    Beispiele:
        >>> setze_aspect_ratio("quadratisch")
        >>> setze_aspect_ratio("goldener_schnitt")
        >>> setze_aspect_ratio("custom", custom_value=1.5)
    """
    aspect_ratio_controller.set_aspect_ratio(ratio_type, custom_value)


def get_aspect_ratio_info() -> dict[str, Any]:
    """
    Gibt Informationen über das aktuelle Aspect-Ratio zurück

    Returns:
        Dictionary mit Aspect-Ratio-Informationen
    """
    return {
        "type": aspect_ratio_controller.current_ratio,
        "name": aspect_ratio_controller.get_aspect_ratio_name(),
        "value": aspect_ratio_controller.get_aspect_ratio_value(),
        "mathematical_mode": aspect_ratio_controller.mathematical_mode,
        "auto_adjust": aspect_ratio_controller.auto_adjust,
    }


def wende_aspect_ratio_an(
    fig: go.Figure,
    x_range: tuple[float, float] | None = None,
    y_range: tuple[float, float] | None = None,
    base_width: int = 800,
) -> go.Figure:
    """
    Wendet das aktuelle Aspect-Ratio auf eine Figur an

    Args:
        fig: Plotly-Figur
        x_range: Optional x-Bereich für Auto-Adjust
        y_range: Optional y-Bereich für Auto-Adjust
        base_width: Basisbreite

    Returns:
        Angepasste Figur
    """
    return aspect_ratio_controller.apply_to_figure(fig, x_range, y_range, base_width)


def erstelle_aspect_ratio_buttons() -> dict[str, Any]:
    """
    Erstellt konfigurierte Buttons für Aspect-Ratio-Auswahl

    Returns:
        Dictionary für Plotly-Layout-Buttons
    """
    return aspect_ratio_controller.create_ratio_selector_config()


# Export der wichtigsten Funktionen und Klassen
__all__ = [
    "AspectRatioType",
    "AspectRatioController",
    "aspect_ratio_controller",
    "setze_aspect_ratio",
    "get_aspect_ratio_info",
    "wende_aspect_ratio_an",
    "erstelle_aspect_ratio_buttons",
]
