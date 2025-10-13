"""
Tests für das erweiterte Konfigurationssystem.

Diese Tests überprüfen die umfassende Konfigurationsverwaltung mit:
- Verschiedenen Konfigurationsmodi
- Umfassenden Konfigurationsabschnitten
- Persistenzfähigkeit
- Validierung
- Dynamischer Konfigurationsänderung
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from src.schul_mathematik.analysis.config_enhanced import (
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
)


class TestSchulAnalysisConfig:
    """Tests für die Hauptkonfigurationsklasse."""

    def test_initialisierung_standard(self):
        """Teste die Standardinitialisierung."""
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
        """Teste die Initialisierung mit verschiedenen Modi."""
        config_entwicklung = SchulAnalysisConfig(KonfigurationsModus.ENTWICKLUNG)
        assert config_entwicklung.modus == KonfigurationsModus.ENTWICKLUNG
        assert config_entwicklung.debug.debug is True
        assert config_entwicklung.debug.profilierung_aktiviert is True

        config_produktion = SchulAnalysisConfig(KonfigurationsModus.PRODUKTION)
        assert config_produktion.modus == KonfigurationsModus.PRODUKTION
        assert config_produktion.debug.debug is False
        assert config_produktion.sicherheit.sicherer_modus is True

        config_test = SchulAnalysisConfig(KonfigurationsModus.TEST)
        assert config_test.modus == KonfigurationsModus.TEST
        assert config_test.debug.debug is True
        assert config_test.pädagogisch.schritte_anzeigen is False
        assert config_test.plotting.punkte_dichte == 100

    def test_modus_wechsel(self):
        """Teste das dynamische Wechseln des Konfigurationsmodus."""
        config = SchulAnalysisConfig()

        # Wechsel zu Entwicklungsmodus
        config.setze_modus(KonfigurationsModus.ENTWICKLUNG)
        assert config.modus == KonfigurationsModus.ENTWICKLUNG
        assert config.debug.debug is True

        # Wechsel zu Produktionsmodus
        config.setze_modus(KonfigurationsModus.PRODUKTION)
        assert config.modus == KonfigurationsModus.PRODUKTION
        assert config.debug.debug is False

    def test_modus_wechsel_mit_string(self):
        """Teste das Wechseln des Modus mit String-Übergabe."""
        config = SchulAnalysisConfig()

        config.setze_modus("entwicklung")
        assert config.modus == KonfigurationsModus.ENTWICKLUNG

        config.setze_modus("produktion")
        assert config.modus == KonfigurationsModus.PRODUKTION

    def test_umgebungsvariablen_debug(self):
        """Teste das Laden von Debug-Umgebungsvariablen."""
        with patch.dict(os.environ, {"SCHUL_ANALYSIS_DEBUG": "true"}):
            config = SchulAnalysisConfig()
            assert config.debug.debug is True

        with patch.dict(os.environ, {"SCHUL_ANALYSIS_DEBUG": "false"}):
            config = SchulAnalysisConfig()
            assert config.debug.debug is False

    def test_umgebungsvariablen_modus(self):
        """Teste das Laden von Modus-Umgebungsvariablen."""
        with patch.dict(os.environ, {"SCHUL_ANALYSIS_MODUS": "entwicklung"}):
            config = SchulAnalysisConfig()
            assert config.modus == KonfigurationsModus.ENTWICKLUNG

        with patch.dict(os.environ, {"SCHUL_ANALYSIS_MODUS": "produktion"}):
            config = SchulAnalysisConfig()
            assert config.modus == KonfigurationsModus.PRODUKTION

    def test_umgebungsvariablen_log_level(self):
        """Teste das Laden von Log-Level-Umgebungsvariablen."""
        with patch.dict(os.environ, {"SCHUL_ANALYSIS_LOG_LEVEL": "DEBUG"}):
            config = SchulAnalysisConfig()
            assert config.debug.log_level == "DEBUG"

    def test_umgebungsvariablen_performance(self):
        """Teste das Laden von Performance-Umgebungsvariablen."""
        with patch.dict(os.environ, {"SCHUL_ANALYSIS_CACHE_SIZE": "256"}):
            config = SchulAnalysisConfig()
            assert config.performance.cache_größe == 256

        with patch.dict(os.environ, {"SCHUL_ANALYSIS_MAX_COMPLEXITY": "2000"}):
            config = SchulAnalysisConfig()
            assert config.performance.max_komplexität == 2000

    def test_plot_konfiguration(self):
        """Teste die Plot-Konfigurationsmethoden."""
        config = SchulAnalysisConfig()

        # Standard Plot-Konfiguration
        plot_config = config.get_plot_config()
        assert plot_config["template"] == config.plotting.plotly_theme
        assert plot_config["width"] == config.plotting.standard_figur_größe[0]
        assert plot_config["height"] == config.plotting.standard_figur_größe[1]

        # Plot-Konfiguration mit verschiedenen Modi
        druck_config = config.get_plot_config(VisualisierungsModus.DRUCK)
        assert druck_config["width"] == 1200
        assert druck_config["height"] == 900

        präsentation_config = config.get_plot_config(VisualisierungsModus.PRÄSENTATION)
        assert präsentation_config["width"] == 1400
        assert präsentation_config["height"] == 1050

        export_config = config.get_plot_config(VisualisierungsModus.BILD_EXPORT)
        assert export_config["width"] == 1600
        assert export_config["height"] == 1200

    def test_achsen_konfiguration(self):
        """Teste die Achsen-Konfigurationsmethoden."""
        config = SchulAnalysisConfig()

        # Mathematischer Modus
        math_config = config.get_axis_config(mathematical_mode=True)
        assert math_config["scaleanchor"] == "y"
        assert math_config["scaleratio"] == 1

        # Normaler Modus
        normal_config = config.get_axis_config(mathematical_mode=False)
        assert "scaleanchor" not in normal_config
        assert "scaleratio" not in normal_config

    def test_linien_konfiguration(self):
        """Teste die Linien-Konfigurationsmethoden."""
        config = SchulAnalysisConfig()

        # Standard Linien-Konfiguration
        line_config = config.get_line_config()
        assert line_config["color"] == config.farben.primär
        assert line_config["width"] == config.plotting.linien_breite

        # Benutzerdefinierte Linien-Konfiguration
        custom_config = config.get_line_config(color_key="sekundär", width=5)
        assert custom_config["color"] == config.farben.sekundär
        assert custom_config["width"] == 5

    def test_marker_konfiguration(self):
        """Teste die Marker-Konfigurationsmethoden."""
        config = SchulAnalysisConfig()

        # Standard Marker-Konfiguration
        marker_config = config.get_marker_config()
        assert marker_config["color"] == config.farben.sekundär
        assert marker_config["size"] == config.plotting.marker_größe
        assert marker_config["symbol"] == "circle"

        # Benutzerdefinierte Marker-Konfiguration
        custom_config = config.get_marker_config(color_key="primär", size=10)
        assert custom_config["color"] == config.farben.primär
        assert custom_config["size"] == 10

    def test_farbpalette(self):
        """Teste die Farbpalette-Funktionalität."""
        config = SchulAnalysisConfig()

        # Erste Farbe
        farbe1 = config.get_farbe_für_index(0)
        assert farbe1 == config.farben.farb_palette[0]

        # Farbe innerhalb des Bereichs
        farbe2 = config.get_farbe_für_index(5)
        assert farbe2 == config.farben.farb_palette[5]

        # Farbe außerhalb des Bereichs (sollte wrappen)
        farbe3 = config.get_farbe_für_index(15)
        assert (
            farbe3 == config.farben.farb_palette[15 % len(config.farben.farb_palette)]
        )

    def test_validierung(self):
        """Teste die Konfigurationsvalidierung."""
        config = SchulAnalysisConfig()

        # Gültige Konfiguration
        probleme = config.validiere_konfiguration()
        assert len(probleme) == 0

        # Ungültige Punktdichte
        config.plotting.punkte_dichte = 5
        probleme = config.validiere_konfiguration()
        assert "Punktdichte sollte mindestens 10 betragen" in probleme

        config.plotting.punkte_dichte = 15000
        probleme = config.validiere_konfiguration()
        assert "Punktdichte sollte 10000 nicht überschreiten" in probleme

        # Negative Cache-Größe
        config.performance.cache_größe = -1
        probleme = config.validiere_konfiguration()
        assert "Cache-Größe darf nicht negativ sein" in probleme

        # Zu kurze Eingabelänge
        config.sicherheit.max_eingabe_länge = 5
        probleme = config.validiere_konfiguration()
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

        # Überprüfe, ob die Werte zurückgesetzt wurden
        assert config.plotting.punkte_dichte == 1000  # Standardwert
        # Debug sollte True sein im ENTWICKLUNG Modus
        assert config.debug.debug == True  # ENTWICKLUNG Modus hat debug=True
        assert (
            config.modus == KonfigurationsModus.ENTWICKLUNG
        )  # Modus sollte erhalten bleiben

    def test_cache_statistiken(self):
        """Teste die Cache-Statistik-Funktionalität."""
        config = SchulAnalysisConfig()

        # Aktiviere Cache-Statistiken
        config.debug.cache_statistiken = True

        # Initiale Statistiken
        stats = config.get_cache_stats()
        assert stats["hits"] == 0
        assert stats["misses"] == 0
        assert stats["total"] == 0
        assert stats["hit_rate"] == 0

        # Registriere einige Hits und Misses
        config.cache_hit()
        config.cache_hit()
        config.cache_miss()
        config.cache_hit()

        stats = config.get_cache_stats()
        assert stats["hits"] == 3
        assert stats["misses"] == 1
        assert stats["total"] == 4
        assert stats["hit_rate"] == 0.75

        # Reset Statistiken
        config.reset_cache_stats()
        stats = config.get_cache_stats()
        assert stats["hits"] == 0
        assert stats["misses"] == 0
        assert stats["total"] == 0

    def test_string_repräsentation(self):
        """Teste die String-Repräsentation."""
        config = SchulAnalysisConfig()

        str_repr = str(config)
        assert "SchulAnalysisConfig" in str_repr
        assert "modus=pädagogisch" in str_repr
        assert "debug=False" in str_repr

        repr_str = repr(config)
        assert "SchulAnalysisConfig" in repr_str
        assert "modus=pädagogisch" in repr_str


class TestKonfigurationsPersistenz:
    """Tests für die Konfigurationspersistenz."""

    def test_speichern_und_laden(self):
        """Teste das Speichern und Laden von Konfigurationen."""
        config = SchulAnalysisConfig()

        # Ändere einige Werte
        config.plotting.punkte_dichte = 2000
        config.farben.primär = "#ff0000"
        config.performance.cache_größe = 256

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_file = f.name

        try:
            # Speichere Konfiguration
            config.speichere_in_datei(temp_file)

            # Erstelle neue Konfiguration und lade
            config2 = SchulAnalysisConfig()
            config2.lade_aus_datei(temp_file)

            # Überprüfe, ob die Werte geladen wurden
            assert config2.plotting.punkte_dichte == 2000
            assert config2.farben.primär == "#ff0000"
            assert config2.performance.cache_größe == 256

        finally:
            # Aufräumen
            Path(temp_file).unlink(missing_ok=True)

    def test_laden_mit_benutzerdefinierten_werten(self):
        """Teste das Laden mit benutzerdefinierten Werten."""
        config_daten = {
            "plotting": {"punkte_dichte": 1500, "linien_breite": 5},
            "farben": {"primär": "#00ff00", "sekundär": "#0000ff"},
            "performance": {"cache_größe": 512, "max_komplexität": 2000},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_daten, f, indent=2)
            temp_file = f.name

        try:
            config = SchulAnalysisConfig()
            config.lade_aus_datei(temp_file)

            # Überprüfe, ob die benutzerdefinierten Werte geladen wurden
            assert config.plotting.punkte_dichte == 1500
            assert config.plotting.linien_breite == 5
            assert config.farben.primär == "#00ff00"
            assert config.farben.sekundär == "#0000ff"
            assert config.performance.cache_größe == 512
            assert config.performance.max_komplexität == 2000

        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_laden_von_nichtexistierender_datei(self):
        """Teste das Laden von nicht existierenden Dateien."""
        config = SchulAnalysisConfig()

        with pytest.raises(FileNotFoundError):
            config.lade_aus_datei("/nicht/existierende/datei.json")

    def test_speichern_ohne_dateiname(self):
        """Teste das Speichern ohne Dateinamen."""
        config = SchulAnalysisConfig()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Wechsel in temporäres Verzeichnis
            original_cwd = os.getcwd()
            os.chdir(temp_dir)

            try:
                # Speichere ohne Dateinamen
                config.speichere_in_datei()

                # Überprüfe, ob die Standarddatei erstellt wurde
                assert Path("schul_analysis_config.json").exists()

            finally:
                os.chdir(original_cwd)


class TestLegacyKompatibilität:
    """Tests für die Legacy-Kompatibilität."""

    def test_legacy_konstanten(self):
        """Teste die Legacy-Konstanten."""
        # Importiere die Legacy-Konstanten
        from src.schul_mathematik.analysis.config_enhanced import (
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

        config = SchulAnalysisConfig()

        # Überprüfe, ob die Legacy-Konstanten korrekt sind
        assert DEFAULT_PLOT_RANGE == config.plotting.default_bereich
        assert PLOTLY_THEME == config.plotting.plotly_theme
        assert DEFAULT_FIGURE_SIZE == config.plotting.standard_figur_größe
        assert COLORS["primary"] == config.farben.primär
        assert COLORS["secondary"] == config.farben.sekundär
        assert COLORS["background"] == config.farben.hintergrund
        assert CACHE_SIZE == config.performance.cache_größe
        assert MAX_COMPLEXITY == config.performance.max_komplexität
        assert NUMERICAL_PRECISION == config.performance.numerische_präzision
        assert MAX_INPUT_LENGTH == config.sicherheit.max_eingabe_länge
        assert ALLOWED_PATTERNS == tuple(config.sicherheit.erlaubte_muster)
        assert SHOW_STEPS == config.pädagogisch.schritte_anzeigen
        assert LANGUAGE == config.pädagogisch.sprache
        assert EDUCATIONAL_MODE == config.pädagogisch.pädagogischer_modus
        assert DEBUG == config.debug.debug
        assert LOG_LEVEL == config.debug.log_level


class TestKonfigurationsdatenklassen:
    """Tests für die einzelnen Konfigurationsdatenklassen."""

    def test_plotting_konfiguration(self):
        """Teste die PlottingKonfiguration."""
        plotting = PlottingKonfiguration()

        assert plotting.default_bereich == (-10, 10)
        assert plotting.plotly_theme == "plotly_white"
        assert plotting.standard_figur_größe == (800, 600)
        assert plotting.aspect_ratio_erhalten is True
        assert plotting.punkte_dichte == 1000

    def test_farben_konfiguration(self):
        """Teste die FarbenKonfiguration."""
        farben = FarbenKonfiguration()

        assert farben.primär == "#1f77b4"
        assert farben.sekundär == "#ff7f0e"
        assert farben.hintergrund == "white"
        assert len(farben.farb_palette) == 10

    def test_performance_konfiguration(self):
        """Teste die PerformanceKonfiguration."""
        performance = PerformanceKonfiguration()

        assert performance.cache_größe == 512
        assert performance.max_komplexität == 1000
        assert performance.numerische_präzision == 1e-10
        assert performance.lazy_evaluierung is True
        assert performance.parallel_verarbeitung is True

    def test_sicherheits_konfiguration(self):
        """Teste die SicherheitsKonfiguration."""
        sicherheit = SicherheitsKonfiguration()

        assert sicherheit.max_eingabe_länge == 1000
        assert len(sicherheit.erlaubte_muster) > 0
        assert sicherheit.rekursions_limit == 100
        assert sicherheit.validierung_strenge is True

    def test_pädagogische_konfiguration(self):
        """Teste die PädagogischeKonfiguration."""
        pädagogisch = PädagogischeKonfiguration()

        assert pädagogisch.schritte_anzeigen is True
        assert pädagogisch.sprache == "de"
        assert pädagogisch.pädagogischer_modus is True
        assert pädagogisch.schwierigkeits_grad == "mittel"

    def test_debug_konfiguration(self):
        """Teste die DebugKonfiguration."""
        debug = DebugKonfiguration()

        assert debug.debug is False
        assert debug.log_level == "INFO"
        assert debug.profilierung_aktiviert is False
        assert debug.detail_logging is False

    def test_export_konfiguration(self):
        """Teste die ExportKonfiguration."""
        export = ExportKonfiguration()

        assert export.standard_format == "png"
        assert export.dpi == 300
        assert export.qualität == 95
        assert export.transparenz is False
        assert export.batch_export_aktiviert is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
