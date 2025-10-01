"""
Zentrale Konfiguration für das Schul-Analysis Framework.

Diese Klasse zentralisiert alle Konfigurationsparameter und macht
das Framework leicht konfigurierbar und wartbar.
"""

import os
from typing import Any


class SchulAnalysisConfig:
    """Zentrale Konfigurationsklasse für Schul-Analysis"""

    # 🎯 Plotting-Konfiguration
    DEFAULT_PLOT_RANGE: tuple[float, float] = (-10, 10)
    PLOTLY_THEME: str = "plotly_white"
    DEFAULT_FIGURE_SIZE: tuple[int, int] = (800, 600)

    # 🎨 Farben und Stile
    COLORS: dict[str, str] = {
        "primary": "blue",
        "secondary": "red",
        "tertiary": "green",
        "background": "white",
        "grid": "lightgray",
        "axis": "black",
    }

    # 🚀 Performance-Konfiguration
    CACHE_SIZE: int = 128
    MAX_COMPLEXITY: int = 1000
    NUMERICAL_PRECISION: float = 1e-10

    # 🔒 Sicherheitskonfiguration
    MAX_INPUT_LENGTH: int = 1000
    ALLOWED_PATTERNS: tuple[str, ...] = (
        r"^[0-9+\-*/^()x\s.]+$|^[a-zA-Z_][a-zA-Z0-9_]*\s*\(",
    )

    # 📚 Didaktische Konfiguration
    SHOW_STEPS: bool = True
    LANGUAGE: str = "de"  # de, en
    EDUCATIONAL_MODE: bool = True

    # 🔧 Debug-Konfiguration
    DEBUG: bool = os.getenv("SCHUL_ANALYSIS_DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = "INFO"

    @classmethod
    def get_plot_config(cls) -> dict[str, Any]:
        """Gibt Plotly-Konfiguration zurück"""
        return {
            "template": cls.PLOTLY_THEME,
            "width": cls.DEFAULT_FIGURE_SIZE[0],
            "height": cls.DEFAULT_FIGURE_SIZE[1],
            "plot_bgcolor": cls.COLORS["background"],
            "paper_bgcolor": cls.COLORS["background"],
        }

    @classmethod
    def get_axis_config(cls, mathematical_mode: bool = True) -> dict[str, Any]:
        """Gibt Achsenkonfiguration zurück"""
        config = {
            "showgrid": True,
            "zeroline": True,
            "showline": True,
            "gridcolor": cls.COLORS["grid"],
            "zerolinecolor": cls.COLORS["axis"],
            "linewidth": 2,
        }

        if mathematical_mode:
            config.update(
                {
                    "scaleanchor": "y",
                    "scaleratio": 1,
                }
            )

        return config

    @classmethod
    def get_line_config(
        cls, color_key: str = "primary", width: int = 3
    ) -> dict[str, Any]:
        """Gibt Linienkonfiguration zurück"""
        return {
            "color": cls.COLORS.get(color_key, "blue"),
            "width": width,
        }

    @classmethod
    def get_marker_config(
        cls, color_key: str = "secondary", size: int = 12
    ) -> dict[str, Any]:
        """Gibt Marker-Konfiguration zurück"""
        return {
            "color": cls.COLORS.get(color_key, "red"),
            "size": size,
            "symbol": "circle",
        }


# Globale Konfigurationsinstanz
config = SchulAnalysisConfig()
