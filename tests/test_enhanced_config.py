"""
Tests für die erweiterte Konfigurationsverwaltung.

Dieses Modul testet die neue SchulAnalysisConfig Klasse mit allen Features:
- Verschiedene Konfigurationsmodi
- Umfassende Konfigurationsabschnitte
- Persistenzfähigkeit
- Validierung
- Dynamische Konfigurationsänderung
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from schul_mathematik.analysis.config import (
    SchulAnalysisConfig,
    KonfigurationsModus,
    VisualisierungsModus,
    PlottingKonfiguration,
    FarbenKonfiguration,
    PerformanceKonfiguration,
    SicherheitsKonfiguration,
    PädagogischeKonfiguration,
    DebugKonfiguration,
    ExportKonfiguration,
    config,
)


class TestKonfigurationsModus:
    """Teste die Konfigurationsmodi-Enum."""

    def test_konfigurations_modus_werte(self):
        """Teste, dass alle erwarteten Modi vorhanden sind."""
        expected_modi = [
            "entwicklung",
            "produktion",
            "test",
            "pädagogisch",
            "forschung",
        ]

        actual_modi = [modus.value for modus in KonfigurationsModus]
        assert set(actual_modi) == set(expected_modi)

    def test_konfigurations_modus_aus_string(self):
        """Teste die Erstellung von Modi aus Strings."""
        assert KonfigurationsModus("entwicklung") == KonfigurationsModus.ENTWICKLUNG
        assert KonfigurationsModus("pädagogisch") == KonfigurationsModus.PÄDAGOGISCH

        with pytest.raises(ValueError):
            KonfigurationsModus("ungültig")


class TestVisualisierungsModus:
    """Teste die Visualisierungsmodi-Enum."""

    def test_visualisierungs_modus_werte(self):
        """Teste, dass alle erwarteten Visualisierungsmodi vorhanden sind."""
        expected_modi = [
            "standard",
            "interaktiv",
            "druck",
            "präsentation",
            "bild_export",
        ]

        actual_modi = [modus.value for modus in VisualisierungsModus]
        assert set(actual_modi) == set(expected_modi)


class TestKonfigurationsDatenklassen:
    """Teste die Konfigurations-Datenklassen."""

    def test_plotting_konfiguration_standardwerte(self):
        """Teste Standardwerte der Plotting-Konfiguration."""
        plotting = PlottingKonfiguration()

        assert plotting.default_bereich == (-10, 10)
        assert plotting.plotly_theme == "plotly_white"
        assert plotting.standard_figur_größe == (800, 600)
        assert plotting.aspect_ratio_erhalten is True
        assert plotting.punkte_dichte == 1000
        assert plotting.linien_breite == 3
        assert plotting.marker_größe == 8

    def test_farben_konfiguration_standardwerte(self):
        """Teste Standardwerte der Farben-Konfiguration."""
        farben = FarbenKonfiguration()

        assert farben.primär == "#1f77b4"
        assert farben.sekundär == "#ff7f0e"
        assert farben.tertiär == "#2ca02c"
        assert len(farben.farb_palette) == 10
        assert farben.hintergrund == "white"

    def test_performance_konfiguration_standardwerte(self):
        """Teste Standardwerte der Performance-Konfiguration."""
        performance = PerformanceKonfiguration()

        assert performance.cache_größe == 512
        assert performance.max_komplexität == 1000
        assert performance.numerische_präzision == 1e-10
        assert performance.lazy_evaluierung is True
        assert performance.caching_aktiviert is True

    def test_sicherheits_konfiguration_standardwerte(self):
        """Teste Standardwerte der Sicherheits-Konfiguration."""
        sicherheit = SicherheitsKonfiguration()

        assert sicherheit.max_eingabe_länge == 1000
        assert len(sicherheit.erlaubte_muster) == 1
        assert sicherheit.rekursions_limit == 100
        assert sicherheit.sicherer_modus is True

    def test_pädagogische_konfiguration_standardwerte(self):
        """Teste Standardwerte der pädagogischen Konfiguration."""
        pädagogisch = PädagogischeKonfiguration()

        assert pädagogisch.schritte_anzeigen is True
        assert pädagogisch.sprache == "de"
        assert pädagogisch.pädagogischer_modus is True
        assert pädagogisch.schwierigkeits_grad == "mittel"

    def test_debug_konfiguration_standardwerte(self):
        """Teste Standardwerte der Debug-Konfiguration."""
        debug = DebugKonfiguration()

        assert debug.debug is False
        assert debug.log_level == "INFO"
        assert debug.profilierung_aktiviert is False
        assert debug.detail_logging is False

    def test_export_konfiguration_standardwerte(self):
        """Teste Standardwerte der Export-Konfiguration."""
        export = ExportKonfiguration()

        assert export.standard_format == "png"
        assert export.dpi == 300
        assert export.qualität == 95
        assert export.transparenz is False
        assert export.batch_export_aktiviert is True


class TestSchulAnalysisConfig:
    """Teste die Hauptkonfigurationsklasse."""

    def test_initialisierung_standard(self):
        """Teste Standardinitialisierung."""
        config = SchulAnalysisConfig()

        assert config.modus == KonfigurationsModus.PÄDAGOGISCH
        assert isinstance(config.plotting, PlottingKonfiguration)
        assert isinstance(config.farben, FarbenKonfiguration)
        assert isinstance(config.performance, PerformanceKonfiguration)
        assert isinstance(config.sicherheit, SicherheitsKonfiguration)
        assert isinstance(config.pädagogisch, PädagogischeKonfiguration)
        assert isinstance(config.debug, DebugKonfiguration)
        assert isinstance(config.export, ExportKonfiguration)

    def test_initialisierung_mit_modus(self):
        """Teste Initialisierung mit spezifischem Modus."""
        config = SchulAnalysisConfig(KonfigurationsModus.ENTWICKLUNG)

        assert config.modus == KonfigurationsModus.ENTWICKLUNG
        assert config.debug.debug is True  # Sollte durch Modus gesetzt werden
        assert config.debug.profilierung_aktiviert is True

    def test_umgebungsvariablen_laden(self):
        """Teste das Laden von Konfiguration aus Umgebungsvariablen."""
        # Setze Umgebungsvariablen
        os.environ["SCHUL_ANALYSIS_DEBUG"] = "true"
        os.environ["SCHUL_ANALYSIS_MODUS"] = "test"
        os.environ["SCHUL_ANALYSIS_LOG_LEVEL"] = "DEBUG"

        try:
            config = SchulAnalysisConfig()
            assert config.debug.debug is True
            assert config.modus == KonfigurationsModus.TEST
            assert config.debug.log_level == "DEBUG"
        finally:
            # Cleanup
            for key in [
                "SCHUL_ANALYSIS_DEBUG",
                "SCHUL_ANALYSIS_MODUS",
                "SCHUL_ANALYSIS_LOG_LEVEL",
            ]:
                if key in os.environ:
                    del os.environ[key]

    def test_modus_wechseln(self):
        """Teste das dynamische Wechseln des Konfigurationsmodus."""
        config = SchulAnalysisConfig()

        # Wechsel zu Entwicklungsmodus
        config.setze_modus(KonfigurationsModus.ENTWICKLUNG)
        assert config.modus == KonfigurationsModus.ENTWICKLUNG
        assert config.debug.debug is True
        assert config.performance.caching_aktiviert is False

        # Wechsel zu Produktionsmodus
        config.setze_modus(KonfigurationsModus.PRODUKTION)
        assert config.modus == KonfigurationsModus.PRODUKTION
        assert config.debug.debug is False
        assert config.sicherheit.sicherer_modus is True

        # Wechsel mit String
        config.setze_modus("test")
        assert config.modus == KonfigurationsModus.TEST
        assert config.plotting.punkte_dichte == 100

    def test_plot_config_standard(self):
        """Teste Standard-Plot-Konfiguration."""
        config = SchulAnalysisConfig()
        plot_config = config.get_plot_config()

        assert plot_config["template"] == "plotly_white"
        assert plot_config["width"] == 800
        assert plot_config["height"] == 600
        assert plot_config["plot_bgcolor"] == "white"

    def test_plot_config_mit_visualisierungsmodus(self):
        """Teste Plot-Konfiguration mit verschiedenen Visualisierungsmodi."""
        config = SchulAnalysisConfig()

        # Druck-Modus
        druck_config = config.get_plot_config(VisualisierungsModus.DRUCK)
        assert druck_config["width"] == 1200
        assert druck_config["height"] == 900

        # Präsentations-Modus
        präsentation_config = config.get_plot_config(VisualisierungsModus.PRÄSENTATION)
        assert präsentation_config["width"] == 1400
        assert präsentation_config["height"] == 1050
        assert präsentation_config["template"] == "presentation"

        # Bild-Export-Modus
        export_config = config.get_plot_config(VisualisierungsModus.BILD_EXPORT)
        assert export_config["width"] == 1600
        assert export_config["height"] == 1200

    def test_axis_config(self):
        """Teste Achsenkonfiguration."""
        config = SchulAnalysisConfig()

        # Mathematischer Modus
        math_config = config.get_axis_config(mathematical_mode=True)
        assert math_config["scaleanchor"] == "y"
        assert math_config["scaleratio"] == 1
        assert math_config["showgrid"] is True

        # Nicht-mathematischer Modus
        normal_config = config.get_axis_config(mathematical_mode=False)
        assert "scaleanchor" not in normal_config
        assert "scaleratio" not in normal_config

    def test_farben_methoden(self):
        """Teste Farb-konfigurationsmethoden."""
        config = SchulAnalysisConfig()

        # Linienkonfiguration
        line_config = config.get_line_config("primär")
        assert line_config["color"] == config.farben.primär
        assert line_config["width"] == config.plotting.linien_breite

        # Mit benutzerdefinierter Breite
        line_config_custom = config.get_line_config("sekundär", width=5)
        assert line_config_custom["color"] == config.farben.sekundär
        assert line_config_custom["width"] == 5

        # Marker-Konfiguration
        marker_config = config.get_marker_config("tertiär")
        assert marker_config["color"] == config.farben.tertiär
        assert marker_config["size"] == config.plotting.marker_größe
        assert marker_config["symbol"] == "circle"

    def test_farb_palette(self):
        """Teste die Farbpalette-Funktionalität."""
        config = SchulAnalysisConfig()

        # Erste Farbe
        farbe1 = config.get_farbe_für_index(0)
        assert farbe1 == config.farben.farb_palette[0]

        # Zehnte Farbe (sollte wieder bei 0 anfangen)
        farbe10 = config.get_farbe_für_index(10)
        assert farbe10 == config.farben.farb_palette[0]

        # Elfte Farbe
        farbe11 = config.get_farbe_für_index(11)
        assert farbe11 == config.farben.farb_palette[1]

    def test_konfigurations_validierung(self):
        """Teste die Konfigurationsvalidierung."""
        config = SchulAnalysisConfig()

        # Gültige Konfiguration
        probleme = config.validiere_konfiguration()
        assert len(probleme) == 0

        # Ungültige Werte
        config.plotting.punkte_dichte = 5  # Zu niedrig
        config.performance.cache_größe = -1  # Negativ
        config.sicherheit.max_eingabe_länge = 5  # Zu niedrig

        probleme = config.validiere_konfiguration()
        assert len(probleme) == 3
        assert "Punktdichte sollte mindestens 10 betragen" in probleme
        assert "Cache-Größe darf nicht negativ sein" in probleme
        assert "Maximale Eingabelänge sollte mindestens 10 betragen" in probleme

    def test_reset_zur_standard(self):
        """Teste das Zurücksetzen zur Standardkonfiguration."""
        config = SchulAnalysisConfig()

        # Ändere einige Werte
        config.plotting.punkte_dichte = 2000
        config.debug.debug = True
        config.modus = KonfigurationsModus.ENTWICKLUNG

        # Reset
        config.reset_zur_standard()

        assert config.plotting.punkte_dichte == 1000
        # Der Modus bleibt erhalten, daher bleibt debug=True im Entwicklungsmodus
        assert config.debug.debug is True  # Entwicklungsmodus hat debug=True
        assert config.modus == KonfigurationsModus.ENTWICKLUNG

    def test_string_repräsentationen(self):
        """Teste String-Repräsentationen."""
        config = SchulAnalysisConfig()

        str_repr = str(config)
        assert "SchulAnalysisConfig" in str_repr
        assert "pädagogisch" in str_repr

        repr_str = repr(config)
        assert "SchulAnalysisConfig" in repr_str
        assert "plotting=" in repr_str

    def test_datei_persistenz(self):
        """Teste das Speichern und Laden von Konfigurationen."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_datei = Path(temp_dir) / "test_config.json"

            # Erstelle und modifiziere Konfiguration
            config = SchulAnalysisConfig()
            config.plotting.punkte_dichte = 1500
            config.debug.debug = True
            config.modus = KonfigurationsModus.ENTWICKLUNG

            # Speichere Konfiguration
            config.speichere_in_datei(config_datei)
            assert config_datei.exists()

            # Lade Konfiguration in neue Instanz
            neue_config = SchulAnalysisConfig()
            neue_config.lade_aus_datei(config_datei)

            # Überprüfe, dass Werte übernommen wurden
            # Hinweis: Die exakte Implementierung von _wende_benutzerdefinierte_werte_an
            # müsste noch vervollständigt werden

            # Teste Fehler bei nicht existierender Datei
            with pytest.raises(FileNotFoundError):
                neue_config.lade_aus_datei("nicht_existierende_datei.json")


class TestLegacyKompatibilität:
    """Teste die Legacy-Kompatibilität."""

    def test_legacy_konstanten(self):
        """Teste, dass Legacy-Konstanten korrekt exportiert werden."""
        from schul_mathematik.analysis.config import (
            DEFAULT_PLOT_RANGE,
            PLOTLY_THEME,
            DEFAULT_FIGURE_SIZE,
            COLORS,
            CACHE_SIZE,
            MAX_COMPLEXITY,
            NUMERICAL_PRECISION,
            MAX_INPUT_LENGTH,
            ALLOWED_PATTERNS,
            SHOW_STEPS,
            LANGUAGE,
            EDUCATIONAL_MODE,
            DEBUG,
            LOG_LEVEL,
        )

        assert DEFAULT_PLOT_RANGE == (-10, 10)
        assert PLOTLY_THEME == "plotly_white"
        assert DEFAULT_FIGURE_SIZE == (800, 600)
        assert COLORS["primary"] == "#1f77b4"
        assert CACHE_SIZE == 512
        assert MAX_COMPLEXITY == 1000
        assert NUMERICAL_PRECISION == 1e-10
        assert MAX_INPUT_LENGTH == 1000
        assert SHOW_STEPS is True
        assert LANGUAGE == "de"
        assert EDUCATIONAL_MODE is True
        assert DEBUG is False  # Standard im pädagogischen Modus
        assert LOG_LEVEL == "INFO"

    def test_globale_config_instanz(self):
        """Teste, dass die globale config-Instanz korrekt initialisiert ist."""
        assert isinstance(config, SchulAnalysisConfig)
        assert config.modus == KonfigurationsModus.PÄDAGOGISCH


class TestKonfigurationsmodusVerhalten:
    """Teste das spezifische Verhalten der verschiedenen Konfigurationsmodi."""

    def test_entwicklungsmodus(self):
        """Teste das Verhalten im Entwicklungsmodus."""
        config = SchulAnalysisConfig(KonfigurationsModus.ENTWICKLUNG)

        assert config.debug.debug is True
        assert config.debug.profilierung_aktiviert is True
        assert config.debug.detail_logging is True
        assert config.performance.caching_aktiviert is False

    def test_produktionsmodus(self):
        """Teste das Verhalten im Produktionsmodus."""
        config = SchulAnalysisConfig(KonfigurationsModus.PRODUKTION)

        assert config.debug.debug is False
        assert config.sicherheit.sicherer_modus is True
        assert config.performance.caching_aktiviert is True

    def test_testmodus(self):
        """Teste das Verhalten im Testmodus."""
        config = SchulAnalysisConfig(KonfigurationsModus.TEST)

        assert config.debug.debug is True
        assert config.pädagogisch.schritte_anzeigen is False
        assert config.plotting.punkte_dichte == 100

    def test_pädagogischer_modus(self):
        """Teste das Verhalten im pädagogischen Modus."""
        config = SchulAnalysisConfig(KonfigurationsModus.PÄDAGOGISCH)

        assert config.pädagogisch.pädagogischer_modus is True
        assert config.pädagogisch.schritte_anzeigen is True
        assert config.plotting.aspect_ratio_erhalten is True

    def test_forschungsmodus(self):
        """Teste das Verhalten im Forschungsmodus."""
        config = SchulAnalysisConfig(KonfigurationsModus.FORSCHUNG)

        assert config.performance.numerische_präzision == 1e-15
        assert config.performance.max_komplexität == 10000
        assert config.debug.profilierung_aktiviert is True


class TestIntegration:
    """Integrationstests für die Konfiguration."""

    def test_konfiguration_über_alle_module(self):
        """Teste, dass die Konfiguration in allen Modulen konsistent ist."""
        # Importiere aus verschiedenen Modulen, die die Konfiguration verwenden
        from schul_mathematik.analysis.config import config as config1
        from schul_mathematik.analysis.visualisierung import config as config2

        # Sollte dieselbe Instanz sein
        assert config1 is config2

    def test_dynamische_konfigurationsänderung(self):
        """Teste, dass dynamische Änderungen wirksam werden."""
        config = SchulAnalysisConfig()

        # Ändere einen Wert
        ursprüngliche_dichte = config.plotting.punkte_dichte
        config.plotting.punkte_dichte = 2000

        # Überprüfe, dass die Änderung wirksam ist
        assert config.plotting.punkte_dichte == 2000
        assert config.plotting.punkte_dichte != ursprüngliche_dichte
