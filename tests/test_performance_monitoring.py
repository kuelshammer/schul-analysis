"""
Tests für das Performance Monitoring System.

Diese Tests überprüfen die umfassende Monitoring-Funktionalität mit:
- Echtzeit-Metriken für Berechnungsdauern
- Memory-Usage-Tracking
- Performance-Profiling
- Automatisierten Performance-Alerts
- Benchmarking-Funktionalität
"""

import json
import tempfile
import time
import threading
from unittest.mock import patch, MagicMock
from pathlib import Path

import pytest

from src.schul_mathematik.analysis.monitoring import (
    PerformanceMonitor,
    PerformanceMetrik,
    PerformanceAlert,
    PerformanceSnapshot,
    MetrikTyp,
    AlertLevel,
    performance_monitor,
    messe_performance,
    get_performance_bericht,
    exportiere_performance_daten,
    registriere_performance_callback,
    monitor,
)


class TestPerformanceMetrik:
    """Tests für die PerformanceMetrik Datenklasse."""

    def test_initialisierung(self):
        """Teste die Initialisierung einer PerformanceMetrik."""
        metrik = PerformanceMetrik(
            typ=MetrikTyp.BERECHNUNGSDAUER,
            name="test_berechnung",
            wert=1.5,
            einheit="s",
            tags={"test": "wert"},
        )

        assert metrik.typ == MetrikTyp.BERECHNUNGSDAUER
        assert metrik.name == "test_berechnung"
        assert metrik.wert == 1.5
        assert metrik.einheit == "s"
        assert metrik.tags == {"test": "wert"}
        assert isinstance(metrik.zeitstempel, float)

    def test_to_dict(self):
        """Teste die Konvertierung zu einem Dictionary."""
        metrik = PerformanceMetrik(
            typ=MetrikTyp.BERECHNUNGSDAUER,
            name="test_berechnung",
            wert=1.5,
            einheit="s",
        )

        dict_form = metrik.to_dict()

        assert dict_form["typ"] == "berechnungsdauer"
        assert dict_form["name"] == "test_berechnung"
        assert dict_form["wert"] == 1.5
        assert dict_form["einheit"] == "s"
        assert "zeitstempel" in dict_form


class TestPerformanceAlert:
    """Tests für die PerformanceAlert Datenklasse."""

    def test_initialisierung(self):
        """Teste die Initialisierung eines PerformanceAlert."""
        metrik = PerformanceMetrik(MetrikTyp.BERECHNUNGSDAUER, "test", 2.0, "s")

        alert = PerformanceAlert(
            level=AlertLevel.WARNING,
            nachricht="Test-Warnung",
            metrik=metrik,
            grenzwert=1.0,
            empfohlene_aktion="Überprüfen",
        )

        assert alert.level == AlertLevel.WARNING
        assert alert.nachricht == "Test-Warnung"
        assert alert.metrik == metrik
        assert alert.grenzwert == 1.0
        assert alert.empfohlene_aktion == "Überprüfen"

    def test_to_dict(self):
        """Teste die Konvertierung zu einem Dictionary."""
        metrik = PerformanceMetrik(MetrikTyp.BERECHNUNGSDAUER, "test", 2.0, "s")

        alert = PerformanceAlert(
            level=AlertLevel.WARNING,
            nachricht="Test-Warnung",
            metrik=metrik,
            grenzwert=1.0,
            empfohlene_aktion="Überprüfen",
        )

        dict_form = alert.to_dict()

        assert dict_form["level"] == "warning"
        assert dict_form["nachricht"] == "Test-Warnung"
        assert dict_form["metrik"]["name"] == "test"
        assert dict_form["grenzwert"] == 1.0


class TestPerformanceSnapshot:
    """Tests für die PerformanceSnapshot Datenklasse."""

    def test_initialisierung(self):
        """Teste die Initialisierung eines PerformanceSnapshot."""
        snapshot = PerformanceSnapshot(
            cpu_verbrauch=25.5,
            memory_verbrauch=1024 * 1024,
            cache_stats={"hits": 10, "misses": 5},
            aktive_threads=3,
        )

        assert snapshot.cpu_verbrauch == 25.5
        assert snapshot.memory_verbrauch == 1024 * 1024
        assert snapshot.cache_stats == {"hits": 10, "misses": 5}
        assert snapshot.aktive_threads == 3

    def test_to_dict(self):
        """Teste die Konvertierung zu einem Dictionary."""
        snapshot = PerformanceSnapshot(
            cpu_verbrauch=25.5,
            memory_verbrauch=1024 * 1024,
            cache_stats={"hits": 10, "misses": 5},
            aktive_threads=3,
        )

        dict_form = snapshot.to_dict()

        assert dict_form["cpu_verbrauch"] == 25.5
        assert dict_form["memory_verbrauch"] == 1024 * 1024
        assert dict_form["cache_stats"]["hits"] == 10
        assert dict_form["aktive_threads"] == 3


class TestPerformanceMonitor:
    """Tests für die Haupt-PerformanceMonitor Klasse."""

    def test_initialisierung(self):
        """Teste die Initialisierung des PerformanceMonitors."""
        mon = PerformanceMonitor()

        assert mon.config is not None
        assert len(mon._metriken) == 0
        assert len(mon._alerts) == 0
        assert len(mon._snapshots) == 0
        assert not mon._aktiv

    def test_starte_stoppe_monitoring(self):
        """Teste das Starten und Stoppen des Monitorings."""
        mon = PerformanceMonitor()

        # Standardmäßig nicht aktiv
        assert not mon._aktiv

        # Starte Monitoring
        mon.starte_monitoring()
        assert mon._aktiv

        # Stoppe Monitoring
        mon.stoppe_monitoring()
        assert not mon._aktiv

    def test_messe_berechnung_context_manager(self):
        """Teste den Context Manager für die Berechnungsmessung."""
        mon = PerformanceMonitor()

        # Teste Messung einer schnellen Operation
        with mon.messe_berechnung("test_operation", kategorie="unit_test"):
            time.sleep(0.01)  # 10ms

        # Prüfe, ob die Metrik registriert wurde
        metriken = mon.get_metriken(MetrikTyp.BERECHNUNGSDAUER)
        assert len(metriken) == 1
        assert metriken[0].name == "test_operation"
        assert metriken[0].wert > 0.005  # Sollte > 5ms sein
        assert metriken[0].tags == {"kategorie": "unit_test"}

    def test_registriere_metrik(self):
        """Teste die direkte Registrierung von Metriken."""
        mon = PerformanceMonitor()

        metrik = PerformanceMetrik(
            typ=MetrikTyp.BERECHNUNGSDAUER,
            name="manuelle_metrik",
            wert=2.5,
            einheit="s",
        )

        mon.registriere_metrik(metrik)

        metriken = mon.get_metriken(MetrikTyp.BERECHNUNGSDAUER)
        assert len(metriken) == 1
        assert metriken[0] == metrik

    def test_registriere_callback(self):
        """Teste die Registrierung von Callbacks."""
        mon = PerformanceMonitor()

        callback_called = False
        received_metrik = None

        def test_callback(metrik):
            nonlocal callback_called, received_metrik
            callback_called = True
            received_metrik = metrik

        mon.registriere_callback(MetrikTyp.BERECHNUNGSDAUER, test_callback)

        # Registriere eine Metrik, die den Callback auslösen sollte
        metrik = PerformanceMetrik(
            MetrikTyp.BERECHNUNGSDAUER, "callback_test", 1.0, "s"
        )
        mon.registriere_metrik(metrik)

        assert callback_called
        assert received_metrik == metrik

    def test_erstelle_system_snapshot(self):
        """Teste die Erstellung von System-Snapshots."""
        mon = PerformanceMonitor()

        snapshot = mon.erstelle_system_snapshot()

        assert isinstance(snapshot, PerformanceSnapshot)
        assert snapshot.cpu_verbrauch >= 0
        assert snapshot.memory_verbrauch >= 0
        assert isinstance(snapshot.cache_stats, dict)
        assert snapshot.aktive_threads >= 1

    @patch("builtins.print")
    def test_performance_alerts(self, mock_print):
        """Teste die Erstellung von Performance-Alerts."""
        mon = PerformanceMonitor()

        # Setze niedrige Grenzwerte für Tests
        mon._grenzwerte["berechnungsdauer"]["test_alert"] = {
            "warning": 0.001,
            "error": 0.002,
            "critical": 0.003,
        }

        # Teste verschiedene Alert-Level
        with mon.messe_berechnung("test_alert"):
            time.sleep(0.0005)  # Sollte WARNING auslösen

        with mon.messe_berechnung("test_alert"):
            time.sleep(0.0025)  # Sollte CRITICAL auslösen

        # Prüfe, ob Alerts erzeugt wurden
        alerts = mon.get_alerts()
        assert len(alerts) >= 1

        # Prüfe, ob etwas gedruckt wurde
        assert mock_print.called

    def test_get_metriken(self):
        """Teste das Abrufen von Metriken."""
        mon = PerformanceMonitor()

        # Registriere verschiedene Metriken
        for i in range(5):
            metrik = PerformanceMetrik(
                typ=MetrikTyp.BERECHNUNGSDAUER,
                name=f"test_{i}",
                wert=i * 0.1,
                einheit="s",
            )
            mon.registriere_metrik(metrik)

        # Teste Abruf aller Metriken
        all_metriken = mon.get_metriken()
        assert len(all_metriken) == 5

        # Teste Abruf mit Typ-Filter
        berechnungszeiten = mon.get_metriken(MetrikTyp.BERECHNUNGSDAUER)
        assert len(berechnungszeiten) == 5

        # Teste Limit
        limited = mon.get_metriken(limit=2)
        assert len(limited) == 2

    def test_get_alerts(self):
        """Teste das Abrufen von Alerts."""
        mon = PerformanceMonitor()

        # Erstelle manuell einige Alerts
        metrik = PerformanceMetrik(MetrikTyp.BERECHNUNGSDAUER, "test", 1.0, "s")

        alert1 = PerformanceAlert(AlertLevel.WARNING, "Warnung", metrik, 0.5, "Test")
        alert2 = PerformanceAlert(AlertLevel.ERROR, "Fehler", metrik, 2.0, "Test")

        mon._alerts.append(alert1)
        mon._alerts.append(alert2)

        # Teste Abruf aller Alerts
        all_alerts = mon.get_alerts()
        assert len(all_alerts) == 2

        # Teste Filter nach Level
        warning_alerts = mon.get_alerts(AlertLevel.WARNING)
        assert len(warning_alerts) == 1
        assert warning_alerts[0].level == AlertLevel.WARNING

    def test_get_performance_bericht(self):
        """Teste die Erstellung von Performance-Berichten."""
        mon = PerformanceMonitor()

        # Füge einige Testdaten hinzu
        for i in range(3):
            metrik = PerformanceMetrik(
                typ=MetrikTyp.BERECHNUNGSDAUER,
                name="test_berechnung",
                wert=0.1 * (i + 1),
                einheit="s",
            )
            mon.registriere_metrik(metrik)

        bericht = mon.get_performance_bericht()

        # Prüfe Berichtstruktur
        assert "timestamp" in bericht
        assert "berechnungs_performance" in bericht
        assert "system_status" in bericht
        assert "cache_performance" in bericht
        assert "alerts" in bericht
        assert "monitoring_status" in bericht

        # Prüfe Berechnungs-Performance
        berechnung = bericht["berechnungs_performance"]
        assert berechnung["anzahl_messungen"] == 3
        assert berechnung["durchschnittliche_dauer"] == pytest.approx(
            0.2, rel=1e-9
        )  # Floating-point tolerance
        assert berechnung["maximale_dauer"] == pytest.approx(0.3, rel=1e-9)
        assert berechnung["minimale_dauer"] == pytest.approx(0.1, rel=1e-9)

    def test_exportiere_metriken(self):
        """Teste den Export von Metriken."""
        mon = PerformanceMonitor()

        # Füge Testdaten hinzu
        metrik = PerformanceMetrik(MetrikTyp.BERECHNUNGSDAUER, "test", 1.0, "s")
        mon.registriere_metrik(metrik)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_file = f.name

        try:
            # Exportiere Metriken
            mon.exportiere_metriken(temp_file)

            # Prüfe, ob Datei erstellt wurde
            assert Path(temp_file).exists()

            # Prüfe Inhalt
            with open(temp_file, "r", encoding="utf-8") as f:
                daten = json.load(f)

            assert "metriken" in daten
            assert "alerts" in daten
            assert "snapshots" in daten
            assert "bericht" in daten
            assert len(daten["metriken"]) == 1

        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_exportiere_metriken_ungueltiges_format(self):
        """Teste den Export mit ungültigem Format."""
        mon = PerformanceMonitor()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            temp_file = f.name

        try:
            with pytest.raises(ValueError):
                mon.exportiere_metriken(temp_file, format="xml")
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_setze_grenzwert(self):
        """Teste das Setzen von benutzerdefinierten Grenzwerten."""
        mon = PerformanceMonitor()

        # Setze neuen Grenzwert
        mon.setze_grenzwert("berechnungsdauer", "custom_test", "warning", 2.0)

        # Prüfe, ob Grenzwert gesetzt wurde
        assert mon._grenzwerte["berechnungsdauer"]["custom_test"]["warning"] == 2.0

    def test_reset_metriken(self):
        """Teste das Zurücksetzen von Metriken."""
        mon = PerformanceMonitor()

        # Füge Testdaten hinzu
        metrik = PerformanceMetrik(MetrikTyp.BERECHNUNGSDAUER, "test", 1.0, "s")
        mon.registriere_metrik(metrik)

        # Prüfe, dass Daten vorhanden sind
        assert len(mon.get_metriken()) > 0

        # Reset
        mon.reset_metriken()

        # Prüfe, dass Daten gelöscht wurden
        assert len(mon.get_metriken()) == 0
        assert len(mon.get_alerts()) == 0
        assert len(mon.get_snapshots()) == 0


class TestPerformanceDecorator:
    """Tests für den Performance Decorator."""

    def test_performance_monitor_decorator(self):
        """Teste den @performance_monitor Decorator."""
        # Verwende die globale Monitor-Instanz für Decorator-Tests
        global monitor
        monitor.reset_metriken()

        @performance_monitor("decorated_function", test_type="unit")
        def test_function(x, y):
            time.sleep(0.01)
            return x + y

        # Führe die Funktion aus
        ergebnis = test_function(2, 3)
        assert ergebnis == 5

        # Prüfe, ob Metrik registriert wurde
        metriken = monitor.get_metriken(MetrikTyp.BERECHNUNGSDAUER)
        assert len(metriken) >= 1  # Kann mehr sein, da andere Tests laufen

        # Finde unsere spezifische Metrik
        unsere_metriken = [m for m in metriken if m.name == "decorated_function"]
        assert len(unsere_metriken) == 1
        assert unsere_metriken[0].tags == {"test_type": "unit"}

    def test_performance_monitor_default_name(self):
        """Teste den Decorator mit Standardnamen."""
        global monitor
        monitor.reset_metriken()

        @performance_monitor()
        def test_function():
            time.sleep(0.01)
            return "test"

        # Führe die Funktion aus
        test_function()

        # Prüfe, ob Metrik mit Funktionsnamen registriert wurde
        metriken = monitor.get_metriken(MetrikTyp.BERECHNUNGSDAUER)
        assert len(metriken) >= 1

        # Der Name sollte den Modul- und Funktionsnamen enthalten
        # Finde Metriken, die Teile des erwarteten Namens enthalten
        test_metriken = [m for m in metriken if "test_function" in m.name]
        assert len(test_metriken) >= 1


class TestBequemeFunktionen:
    """Tests für die bequemen Funktionen."""

    def test_messe_performance(self):
        """Teste die messe_performance Funktion."""
        # Verwende die globale Monitor-Instanz
        global monitor
        monitor.reset_metriken()

        with messe_performance("manuelle_messung", kategorie="test"):
            time.sleep(0.01)

        metriken = monitor.get_metriken(MetrikTyp.BERECHNUNGSDAUER)
        assert len(metriken) >= 1

        # Finde unsere spezifische Metrik
        unsere_metriken = [m for m in metriken if m.name == "manuelle_messung"]
        assert len(unsere_metriken) == 1
        assert unsere_metriken[0].tags == {"kategorie": "test"}

    def test_get_performance_bericht(self):
        """Teste die globale get_performance_bericht Funktion."""
        # Diese Funktion nutzt die globale Monitor-Instanz
        bericht = get_performance_bericht()

        assert isinstance(bericht, dict)
        assert "timestamp" in bericht
        assert "berechnungs_performance" in bericht

    def test_registriere_performance_callback(self):
        """Teste die globale registriere_performance_callback Funktion."""
        callback_called = False

        def test_callback(metrik):
            nonlocal callback_called
            callback_called = True

        registriere_performance_callback(MetrikTyp.BERECHNUNGSDAUER, test_callback)

        # Füge eine Metrik hinzu, um den Callback auszulösen
        metrik = PerformanceMetrik(
            MetrikTyp.BERECHNUNGSDAUER, "callback_test", 1.0, "s"
        )
        monitor.registriere_metrik(metrik)

        assert callback_called

    def test_exportiere_performance_daten(self):
        """Teste die globale exportiere_performance_daten Funktion."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_file = f.name

        try:
            exportiere_performance_daten(temp_file)

            # Prüfe, ob Datei erstellt wurde
            assert Path(temp_file).exists()

            # Prüfe Inhalt
            with open(temp_file, "r", encoding="utf-8") as f:
                daten = json.load(f)

            assert "metriken" in daten
            assert "export_timestamp" in daten

        finally:
            Path(temp_file).unlink(missing_ok=True)


class TestThreadSafety:
    """Tests für Thread-Sicherheit."""

    def test_concurrent_metric_registration(self):
        """Teste gleichzeitige Metrik-Registrierung."""
        mon = PerformanceMonitor()

        def worker(worker_id):
            for i in range(10):
                metrik = PerformanceMetrik(
                    typ=MetrikTyp.BERECHNUNGSDAUER,
                    name=f"worker_{worker_id}_metrik_{i}",
                    wert=0.1,
                    einheit="s",
                )
                mon.registriere_metrik(metrik)

        # Starte mehrere Threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Warte auf alle Threads
        for thread in threads:
            thread.join()

        # Prüfe, ob alle Metriken registriert wurden
        all_metriken = mon.get_metriken()
        assert len(all_metriken) == 50  # 5 Workers * 10 Metriken


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
