"""
Zentrale Konfiguration für das Schul-Analysis Framework.

Diese Klasse zentralisiert alle Konfigurationsparameter und macht
das Framework leicht konfigurierbar und wartbar.
Enhanced Version mit umfassender Konfigurationsverwaltung.
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum


class KonfigurationsModus(Enum):
    """Verschiedene Konfigurationsmodi für unterschiedliche Anwendungsfälle."""

    ENTWICKLUNG = "entwicklung"
    PRODUKTION = "produktion"
    TEST = "test"
    PÄDAGOGISCH = "pädagogisch"
    FORSCHUNG = "forschung"


class VisualisierungsModus(Enum):
    """Visualisierungsmodi für unterschiedliche Darstellungsarten."""

    STANDARD = "standard"
    INTERAKTIV = "interaktiv"
    DRUCK = "druck"
    PRÄSENTATION = "präsentation"
    BILD_EXPORT = "bild_export"


@dataclass
class PlottingKonfiguration:
    """Zentrale Plotting-Konfiguration mit allen Parametern."""

    default_bereich: Tuple[float, float] = (-10, 10)
    plotly_theme: str = "plotly_white"
    standard_figur_größe: Tuple[int, int] = (800, 600)
    aspect_ratio_erhalten: bool = True
    punkte_dichte: int = 1000
    linien_breite: int = 3
    marker_größe: int = 8
    schrift_größe: int = 12
    achsen_ticks: int = 10


@dataclass
class FarbenKonfiguration:
    """Umfassende Farbkonfiguration für verschiedene Elemente."""

    primär: str = "#1f77b4"  # Blau
    sekundär: str = "#ff7f0e"  # Orange
    tertiär: str = "#2ca02c"  # Grün
    hintergrund: str = "white"
    gitter: str = "#e0e0e0"
    achsen: str = "black"
    text: str = "black"
    nulllinie: str = "#666666"
    spezielle_punkte: str = "#d62728"  # Rot

    # Farbpalette für mehrere Funktionen
    farb_palette: List[str] = field(
        default_factory=lambda: [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
        ]
    )


@dataclass
class PerformanceKonfiguration:
    """Performance-Optimierungskonfiguration."""

    cache_größe: int = 512
    max_komplexität: int = 1000
    numerische_präzision: float = 1e-10
    lazy_evaluierung: bool = True
    parallel_verarbeitung: bool = True
    max_parallel_threads: int = 4
    caching_aktiviert: bool = True
    speicher_optimierung: bool = True


@dataclass
class SicherheitsKonfiguration:
    """Sicherheits- und Validierungskonfiguration."""

    max_eingabe_länge: int = 1000
    erlaubte_muster: List[str] = field(
        default_factory=lambda: [
            r"^[0-9+\-*/^()x\s.]+$|^[a-zA-Z_][a-zA-Z0-9_]*\s*\(",
        ]
    )
    rekursions_limit: int = 100
    ausführungs_zeit_limit: float = 30.0
    validierung_strenge: bool = True
    sicherer_modus: bool = True


@dataclass
class PädagogischeKonfiguration:
    """Konfiguration für pädagogische Features."""

    schritte_anzeigen: bool = True
    sprache: str = "de"  # de, en
    pädagogischer_modus: bool = True
    erklärungen_anzeigen: bool = True
    schritt_für_schritt: bool = True
    lernpfad_aktiv: bool = False
    schwierigkeits_grad: str = "mittel"  # leicht, mittel, schwer
    fehler_als_lernchance: bool = True


@dataclass
class DebugKonfiguration:
    """Debugging und Logging Konfiguration."""

    debug: bool = False
    log_level: str = "INFO"
    profilierung_aktiviert: bool = False
    cache_statistiken: bool = False
    detail_logging: bool = False
    datei_logging: bool = False
    log_datei_pfad: Optional[str] = None


@dataclass
class ExportKonfiguration:
    """Konfiguration für Export-Funktionen."""

    standard_format: str = "png"  # png, svg, pdf, html
    dpi: int = 300
    qualität: int = 95
    transparenz: bool = False
    include_quellcode: bool = False
    batch_export_aktiviert: bool = True


class SchulAnalysisConfig:
    """
    Zentrale, erweiterte Konfigurationsklasse für Schul-Analysis.

    Diese Klasse bietet eine umfassende Konfigurationsverwaltung mit:
    - Verschiedenen Konfigurationsmodi
    - Umfassenden Konfigurationsabschnitten
    - Persistenzfähigkeit
    - Validierung
    - Dynamischer Konfigurationsänderung
    """

    def __init__(self, modus: KonfigurationsModus = KonfigurationsModus.PÄDAGOGISCH):
        self.modus = modus
        self._config_datei = None
        self._benutzerdefinierte_werte = {}

        # Initialisiere alle Konfigurationsabschnitte
        self.plotting = PlottingKonfiguration()
        self.farben = FarbenKonfiguration()
        self.performance = PerformanceKonfiguration()
        self.sicherheit = SicherheitsKonfiguration()
        self.pädagogisch = PädagogischeKonfiguration()
        self.debug = DebugKonfiguration()
        self.export = ExportKonfiguration()

        # Lade Konfiguration aus Umgebungsvariablen und passe Modus an
        self._lade_umgebungsvariablen()
        self._passe_modus_an()  # Wichtig: Modus-Anpassung nach Initialisierung

    def _lade_umgebungsvariablen(self):
        """Lade Konfiguration aus Umgebungsvariablen."""
        env_debug = os.getenv("SCHUL_ANALYSIS_DEBUG", "false").lower()
        self.debug.debug = env_debug == "true"

        env_modus = os.getenv("SCHUL_ANALYSIS_MODUS")
        if env_modus:
            try:
                self.modus = KonfigurationsModus(env_modus)
                self._passe_modus_an()
            except ValueError:
                pass

        env_log_level = os.getenv("SCHUL_ANALYSIS_LOG_LEVEL")
        if env_log_level:
            self.debug.log_level = env_log_level

    def _passe_modus_an(self):
        """Passe die Konfiguration an den gewählten Modus an."""
        if self.modus == KonfigurationsModus.ENTWICKLUNG:
            self.debug.debug = True
            self.debug.profilierung_aktiviert = True
            self.debug.detail_logging = True
            self.performance.caching_aktiviert = False

        elif self.modus == KonfigurationsModus.PRODUKTION:
            self.debug.debug = False
            self.sicherheit.sicherer_modus = True
            self.performance.caching_aktiviert = True

        elif self.modus == KonfigurationsModus.TEST:
            self.debug.debug = True
            self.pädagogisch.schritte_anzeigen = False
            self.plotting.punkte_dichte = 100  # Reduziert für schnellere Tests

        elif self.modus == KonfigurationsModus.PÄDAGOGISCH:
            self.pädagogisch.pädagogischer_modus = True
            self.pädagogisch.schritte_anzeigen = True
            self.plotting.aspect_ratio_erhalten = True

        elif self.modus == KonfigurationsModus.FORSCHUNG:
            self.performance.numerische_präzision = 1e-15
            self.performance.max_komplexität = 10000
            self.debug.profilierung_aktiviert = True

    def setze_modus(self, modus: Union[KonfigurationsModus, str]):
        """Ändere den Konfigurationsmodus."""
        if isinstance(modus, str):
            modus = KonfigurationsModus(modus)
        self.modus = modus
        self._passe_modus_an()

    def lade_aus_datei(self, datei_pfad: Union[str, Path]):
        """Lade Konfiguration aus einer JSON-Datei."""
        datei_pfad = Path(datei_pfad)
        if not datei_pfad.exists():
            raise FileNotFoundError(f"Konfigurationsdatei nicht gefunden: {datei_pfad}")

        with open(datei_pfad, "r", encoding="utf-8") as f:
            daten = json.load(f)

        self._config_datei = datei_pfad
        self._benutzerdefinierte_werte = daten
        self._wende_benutzerdefinierte_werte_an()

    def speichere_in_datei(self, datei_pfad: Optional[Union[str, Path]] = None):
        """Speichere aktuelle Konfiguration in einer JSON-Datei."""
        if datei_pfad is None:
            datei_pfad = self._config_datei or "schul_analysis_config.json"

        datei_pfad = Path(datei_pfad)

        konfig_dict = {
            "modus": self.modus.value,
            "benutzerdefinierte_werte": self._benutzerdefinierte_werte,
            "plotting": asdict(self.plotting),
            "farben": asdict(self.farben),
            "performance": asdict(self.performance),
            "sicherheit": asdict(self.sicherheit),
            "pädagogisch": asdict(self.pädagogisch),
            "debug": asdict(self.debug),
            "export": asdict(self.export),
        }

        with open(datei_pfad, "w", encoding="utf-8") as f:
            json.dump(konfig_dict, f, indent=2, ensure_ascii=False)

    def _wende_benutzerdefinierte_werte_an(self):
        """Wende benutzerdefinierte Werte auf die Konfiguration an."""
        # Implementierung zum Anwenden benutzerdefinierter Werte
        # Dies würde rekursiv durch alle Konfigurationsdatenklassen gehen

    def get_plot_config(
        self, visualisierungs_modus: Optional[VisualisierungsModus] = None
    ) -> Dict[str, Any]:
        """Gibt Plotly-Konfiguration zurück mit optionalen Modus-Anpassungen."""
        if visualisierungs_modus == VisualisierungsModus.DRUCK:
            figur_größe = (1200, 900)
            theme = "plotly_white"
        elif visualisierungs_modus == VisualisierungsModus.PRÄSENTATION:
            figur_größe = (1400, 1050)
            theme = "presentation"
        elif visualisierungs_modus == VisualisierungsModus.BILD_EXPORT:
            figur_größe = (1600, 1200)
            theme = "plotly_white"
        else:
            figur_größe = self.plotting.standard_figur_größe
            theme = self.plotting.plotly_theme

        return {
            "template": theme,
            "width": figur_größe[0],
            "height": figur_größe[1],
            "plot_bgcolor": self.farben.hintergrund,
            "paper_bgcolor": self.farben.hintergrund,
        }

    def get_axis_config(self, mathematical_mode: bool = True) -> Dict[str, Any]:
        """Gibt Achsenkonfiguration zurück."""
        config = {
            "showgrid": True,
            "zeroline": True,
            "showline": True,
            "gridcolor": self.farben.gitter,
            "zerolinecolor": self.farben.nulllinie,
            "linewidth": 2,
            "ticks": "inside",
            "tickcolor": self.farben.achsen,
            "ticklen": 5,
        }

        if mathematical_mode and self.plotting.aspect_ratio_erhalten:
            config.update(
                {
                    "scaleanchor": "y",
                    "scaleratio": 1,
                }
            )

        return config

    def get_line_config(
        self, color_key: str = "primär", width: Optional[int] = None
    ) -> Dict[str, Any]:
        """Gibt Linienkonfiguration zurück."""
        farbe = getattr(self.farben, color_key, self.farben.primär)
        return {
            "color": farbe,
            "width": width or self.plotting.linien_breite,
        }

    def get_marker_config(
        self, color_key: str = "sekundär", size: Optional[int] = None
    ) -> Dict[str, Any]:
        """Gibt Marker-Konfiguration zurück."""
        farbe = getattr(self.farben, color_key, self.farben.sekundär)
        return {
            "color": farbe,
            "size": size or self.plotting.marker_größe,
            "symbol": "circle",
            "line": {
                "color": self.farben.achsen,
                "width": 1,
            },
        }

    def get_farbe_für_index(self, index: int) -> str:
        """Gibt eine Farbe aus der Palette basierend auf dem Index zurück."""
        return self.farben.farb_palette[index % len(self.farben.farb_palette)]

    def validiere_konfiguration(self) -> List[str]:
        """Validiert die aktuelle Konfiguration und gibt eine Liste von Problemen zurück."""
        probleme = []

        if self.plotting.punkte_dichte < 10:
            probleme.append("Punktdichte sollte mindestens 10 betragen")

        if self.plotting.punkte_dichte > 10000:
            probleme.append("Punktdichte sollte 10000 nicht überschreiten")

        if self.performance.cache_größe < 0:
            probleme.append("Cache-Größe darf nicht negativ sein")

        if self.sicherheit.max_eingabe_länge < 10:
            probleme.append("Maximale Eingabelänge sollte mindestens 10 betragen")

        return probleme

    def reset_zur_standard(self):
        """Setzt alle Konfigurationen auf Standardwerte zurück."""
        original_modus = self.modus
        self.__init__(original_modus)
        self._benutzerdefinierte_werte = {}

    def __str__(self) -> str:
        """String-Repräsentation der Konfiguration."""
        return (
            f"SchulAnalysisConfig(modus={self.modus.value}, debug={self.debug.debug})"
        )

    def __repr__(self) -> str:
        """Ausführliche Repräsentation der Konfiguration."""
        return (
            f"SchulAnalysisConfig(modus={self.modus.value}, "
            f"plotting={self.plotting}, "
            f"debug={self.debug})"
        )


# Globale Konfigurationsinstanz
config = SchulAnalysisConfig()


# Legacy-Kompatibilität
DEFAULT_PLOT_RANGE = config.plotting.default_bereich
PLOTLY_THEME = config.plotting.plotly_theme
DEFAULT_FIGURE_SIZE = config.plotting.standard_figur_größe
COLORS = {
    "primary": config.farben.primär,
    "secondary": config.farben.sekundär,
    "tertiary": config.farben.tertiär,
    "background": config.farben.hintergrund,
    "grid": config.farben.gitter,
    "axis": config.farben.achsen,
}
CACHE_SIZE = config.performance.cache_größe
MAX_COMPLEXITY = config.performance.max_komplexität
NUMERICAL_PRECISION = config.performance.numerische_präzision
MAX_INPUT_LENGTH = config.sicherheit.max_eingabe_länge
ALLOWED_PATTERNS = tuple(config.sicherheit.erlaubte_muster)
SHOW_STEPS = config.pädagogisch.schritte_anzeigen
LANGUAGE = config.pädagogisch.sprache
EDUCATIONAL_MODE = config.pädagogisch.pädagogischer_modus
DEBUG = config.debug.debug
LOG_LEVEL = config.debug.log_level
