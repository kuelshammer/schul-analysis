"""
Performance Monitoring System für das Schul-Analysis Framework.

Dieses Modul implementiert umfassendes Performance-Monitoring mit:
- Echtzeit-Metriken für Berechnungsdauern
- Memory-Usage-Tracking
- Performance-Profiling für verschiedene Funktionstypen
- Automatisierte Performance-Alerts
- Benchmarking-Funktionalität
"""

import time
import tracemalloc
import threading
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable, Union
from enum import Enum
from collections import defaultdict, deque
import json
import psutil
import os

from .config_enhanced import SchulAnalysisConfig


class MetrikTyp(Enum):
    """Verschiedene Typen von Performance-Metriken."""

    BERECHNUNGSDAUER = "berechnungsdauer"
    MEMORY_VERBRAUCH = "memory_verbrauch"
    CACHE_HIT_RATE = "cache_hit_rate"
    FUNKTIONSAUFRUFE = "funktionsaufrufe"
    FEHLER_RATE = "fehler_rate"


class AlertLevel(Enum):
    """Schweregrade für Performance-Alerts."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class PerformanceMetrik:
    """Einzelne Performance-Metrik mit Metadaten."""

    typ: MetrikTyp
    name: str
    wert: Union[float, int]
    einheit: str
    zeitstempel: float = field(default_factory=time.time)
    tags: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert die Metrik in ein Dictionary."""
        return {
            "typ": self.typ.value,
            "name": self.name,
            "wert": self.wert,
            "einheit": self.einheit,
            "zeitstempel": self.zeitstempel,
            "tags": self.tags,
        }


@dataclass
class PerformanceAlert:
    """Performance-Alert mit Schweregrad und Details."""

    level: AlertLevel
    nachricht: str
    metrik: PerformanceMetrik
    grenzwert: float
    empfohlene_aktion: str
    zeitstempel: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert den Alert in ein Dictionary."""
        return {
            "level": self.level.value,
            "nachricht": self.nachricht,
            "metrik": self.metrik.to_dict(),
            "grenzwert": self.grenzwert,
            "empfohlene_aktion": self.empfohlene_aktion,
            "zeitstempel": self.zeitstempel,
        }


@dataclass
class PerformanceSnapshot:
    """Snapshot der aktuellen Performance-Situation."""

    cpu_verbrauch: float
    memory_verbrauch: float
    cache_stats: Dict[str, Any]
    aktive_threads: int
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert den Snapshot in ein Dictionary."""
        return {
            "cpu_verbrauch": self.cpu_verbrauch,
            "memory_verbrauch": self.memory_verbrauch,
            "cache_stats": self.cache_stats,
            "aktive_threads": self.aktive_threads,
            "timestamp": self.timestamp,
        }


class PerformanceMonitor:
    """
    Hauptklasse für das Performance-Monitoring.

    Diese Klasse bietet umfassendes Monitoring für:
    - Berechnungszeiten
    - Memory-Verbrauch
    - Cache-Performance
    - System-Ressourcen
    - Benutzerdefinierte Metriken
    """

    def __init__(self, config: Optional[SchulAnalysisConfig] = None):
        self.config = config or SchulAnalysisConfig()
        self._metriken = defaultdict(list)
        self._alerts = deque(maxlen=1000)
        self._snapshots = deque(maxlen=100)
        self._grenzwerte = self._initialisiere_grenzwerte()
        self._callbacks = defaultdict(list)
        self._lock = threading.Lock()
        self._aktiv = False

        # Starte Monitoring falls in Konfiguration aktiviert
        if self.config.debug.profilierung_aktiviert:
            self.starte_monitoring()

    def _initialisiere_grenzwerte(self) -> Dict[str, Dict[str, float]]:
        """Initialisiere Standard-Grenzwerte für Alerts."""
        return {
            "berechnungsdauer": {
                "warning": 1.0,  # 1 Sekunde
                "error": 5.0,  # 5 Sekunden
                "critical": 10.0,  # 10 Sekunden
            },
            "memory_verbrauch": {
                "warning": 100 * 1024 * 1024,  # 100 MB
                "error": 500 * 1024 * 1024,  # 500 MB
                "critical": 1024 * 1024 * 1024,  # 1 GB
            },
            "cache_hit_rate": {
                "warning": 0.5,  # 50%
                "error": 0.3,  # 30%
                "critical": 0.1,  # 10%
            },
        }

    def starte_monitoring(self):
        """Starte das Performance-Monitoring."""
        if self._aktiv:
            return

        self._aktiv = True
        tracemalloc.start()

        # Starte Snapshot-Sammlung im Hintergrund
        if self.config.debug.profilierung_aktiviert:
            self._start_snapshot_sammler()

    def stoppe_monitoring(self):
        """Stoppe das Performance-Monitoring."""
        if not self._aktiv:
            return

        self._aktiv = False
        tracemalloc.stop()

    def _start_snapshot_sammler(self):
        """Starte die Hintergrund-Sammlung von System-Snapshots."""

        def sammler():
            while self._aktiv:
                try:
                    snapshot = self.erstelle_system_snapshot()
                    with self._lock:
                        self._snapshots.append(snapshot)
                    time.sleep(5)  # Alle 5 Sekunden
                except Exception:
                    pass

        thread = threading.Thread(target=sammler, daemon=True)
        thread.start()

    @contextmanager
    def messe_berechnung(self, name: str, **tags):
        """
        Context Manager zum Messen von Berechnungsdauern.

        Args:
            name: Name der Berechnung
            **tags: Zusätzliche Tags für die Metrik
        """
        start_time = time.time()
        start_memory = (
            tracemalloc.get_traced_memory()[1] if tracemalloc.is_tracing() else 0
        )

        try:
            yield
        finally:
            end_time = time.time()
            end_memory = (
                tracemalloc.get_traced_memory()[1] if tracemalloc.is_tracing() else 0
            )

            dauer = end_time - start_time
            memory_delta = end_memory - start_memory

            # Speichere Berechnungsdauer
            self.registriere_metrik(
                PerformanceMetrik(
                    typ=MetrikTyp.BERECHNUNGSDAUER,
                    name=name,
                    wert=dauer,
                    einheit="s",
                    tags=tags,
                )
            )

            # Speichere Memory-Verbrauch falls signifikant
            if memory_delta > 1024:  # > 1 KB
                self.registriere_metrik(
                    PerformanceMetrik(
                        typ=MetrikTyp.MEMORY_VERBRAUCH,
                        name=f"{name}_memory",
                        wert=memory_delta,
                        einheit="bytes",
                        tags=tags,
                    )
                )

            # Prüfe auf Performance-Alerts
            self._pruefe_alerts(name, dauer, memory_delta)

    def registriere_metrik(self, metrik: PerformanceMetrik):
        """Registriere eine neue Performance-Metrik."""
        with self._lock:
            self._metriken[metrik.typ.value].append(metrik)

        # Benachrichtige Callbacks
        for callback in self._callbacks[metrik.typ.value]:
            try:
                callback(metrik)
            except Exception:
                pass

    def registriere_callback(
        self,
        metrik_typ: Union[MetrikTyp, str],
        callback: Callable[[PerformanceMetrik], None],
    ):
        """Registriere einen Callback für einen bestimmten Metrik-Typ."""
        if isinstance(metrik_typ, MetrikTyp):
            metrik_typ = metrik_typ.value
        self._callbacks[metrik_typ].append(callback)

    def erstelle_system_snapshot(self) -> PerformanceSnapshot:
        """Erstelle einen Snapshot der aktuellen System-Situation."""
        try:
            process = psutil.Process(os.getpid())

            return PerformanceSnapshot(
                cpu_verbrauch=process.cpu_percent(),
                memory_verbrauch=process.memory_info().rss,
                cache_stats=self.config.get_cache_stats(),
                aktive_threads=threading.active_count(),
            )
        except Exception:
            # Fallback bei Fehlern
            return PerformanceSnapshot(
                cpu_verbrauch=0.0,
                memory_verbrauch=0.0,
                cache_stats={},
                aktive_threads=0,
            )

    def _pruefe_alerts(self, name: str, dauer: float, memory_delta: float):
        """Prüfe auf Performance-Alerts basierend auf Grenzwerten."""
        # Prüfe Berechnungsdauer
        if name in self._grenzwerte["berechnungsdauer"]:
            grenzwerte = self._grenzwerte["berechnungsdauer"][name]

            if dauer > grenzwerte.get("critical", float("inf")):
                self._erstelle_alert(
                    AlertLevel.CRITICAL,
                    f"Kritische Berechnungsdauer für {name}",
                    dauer,
                    grenzwerte.get("critical", 0),
                    "Optimiere den Algorithmus oder erhöhe die Zeitgrenze",
                )
            elif dauer > grenzwerte.get("error", float("inf")):
                self._erstelle_alert(
                    AlertLevel.ERROR,
                    f"Lange Berechnungsdauer für {name}",
                    dauer,
                    grenzwerte.get("error", 0),
                    "Überprüfe die Komplexität der Berechnung",
                )
            elif dauer > grenzwerte.get("warning", float("inf")):
                self._erstelle_alert(
                    AlertLevel.WARNING,
                    f"Warnung: Berechnungsdauer für {name}",
                    dauer,
                    grenzwerte.get("warning", 0),
                    "Beobachte die Performance",
                )

        # Prüfe Memory-Verbrauch
        if memory_delta > self._grenzwerte["memory_verbrauch"]["critical"]:
            self._erstelle_alert(
                AlertLevel.CRITICAL,
                f"Kritischer Memory-Verbrauch für {name}",
                memory_delta,
                self._grenzwerte["memory_verbrauch"]["critical"],
                "Überprüfe auf Memory Leaks",
            )

    def _erstelle_alert(
        self,
        level: AlertLevel,
        nachricht: str,
        wert: float,
        grenzwert: float,
        aktion: str,
    ):
        """Erstelle einen neuen Performance-Alert."""
        metrik = PerformanceMetrik(
            typ=MetrikTyp.BERECHNUNGSDAUER, name="alert", wert=wert, einheit=""
        )

        alert = PerformanceAlert(
            level=level,
            nachricht=nachricht,
            metrik=metrik,
            grenzwert=grenzwert,
            empfohlene_aktion=aktion,
        )

        with self._lock:
            self._alerts.append(alert)

        # Logge den Alert
        if level == AlertLevel.CRITICAL:
            print(
                f"🚨 CRITICAL: {nachricht} ( Wert: {wert:.3f}, Grenzwert: {grenzwert})"
            )
        elif level == AlertLevel.ERROR:
            print(f"❌ ERROR: {nachricht} ( Wert: {wert:.3f}, Grenzwert: {grenzwert})")
        elif level == AlertLevel.WARNING:
            print(
                f"⚠️  WARNING: {nachricht} ( Wert: {wert:.3f}, Grenzwert: {grenzwert})"
            )

    def get_metriken(
        self, typ: Optional[Union[MetrikTyp, str]] = None, limit: int = 100
    ) -> List[PerformanceMetrik]:
        """Gib Metriken eines bestimmten Typs zurück."""
        if typ is None:
            # Alle Metriken
            result = []
            for metrik_liste in self._metriken.values():
                result.extend(metrik_liste[-limit:])
            return sorted(result, key=lambda x: x.zeitstempel, reverse=True)

        if isinstance(typ, MetrikTyp):
            typ = typ.value

        with self._lock:
            return self._metriken.get(typ, [])[-limit:]

    def get_alerts(
        self, level: Optional[AlertLevel] = None, limit: int = 50
    ) -> List[PerformanceAlert]:
        """Gib Alerts zurück, optional gefiltert nach Schweregrad."""
        with self._lock:
            alerts = list(self._alerts)

        if level is not None:
            alerts = [alert for alert in alerts if alert.level == level]

        return alerts[-limit:]

    def get_snapshots(self, limit: int = 20) -> List[PerformanceSnapshot]:
        """Gib System-Snapshots zurück."""
        with self._lock:
            return list(self._snapshots)[-limit:]

    def get_performance_bericht(self) -> Dict[str, Any]:
        """Erstelle einen umfassenden Performance-Bericht."""
        # Berechne durchschnittliche Berechnungsdauern
        berechnungszeiten = self.get_metriken(MetrikTyp.BERECHNUNGSDAUER)

        if berechnungszeiten:
            avg_dauer = sum(m.wert for m in berechnungszeiten) / len(berechnungszeiten)
            max_dauer = max(m.wert for m in berechnungszeiten)
            min_dauer = min(m.wert for m in berechnungszeiten)
        else:
            avg_dauer = max_dauer = min_dauer = 0

        # System-Status
        snapshots = self.get_snapshots()
        if snapshots:
            latest_snapshot = snapshots[-1]
            cpu_avg = sum(s.cpu_verbrauch for s in snapshots) / len(snapshots)
            memory_avg = sum(s.memory_verbrauch for s in snapshots) / len(snapshots)
        else:
            latest_snapshot = cpu_avg = memory_avg = None

        # Alerts
        alerts = self.get_alerts()
        alert_counts = defaultdict(int)
        for alert in alerts:
            alert_counts[alert.level.value] += 1

        # Cache-Statistiken
        cache_stats = self.config.get_cache_stats()

        return {
            "timestamp": time.time(),
            "berechnungs_performance": {
                "anzahl_messungen": len(berechnungszeiten),
                "durchschnittliche_dauer": avg_dauer,
                "maximale_dauer": max_dauer,
                "minimale_dauer": min_dauer,
                "einheit": "s",
            },
            "system_status": {
                "cpu_verbrauch": latest_snapshot.cpu_verbrauch
                if latest_snapshot
                else 0,
                "memory_verbrauch": latest_snapshot.memory_verbrauch
                if latest_snapshot
                else 0,
                "durchschnitt_cpu": cpu_avg or 0,
                "durchschnitt_memory": memory_avg or 0,
                "aktive_threads": latest_snapshot.aktive_threads
                if latest_snapshot
                else 0,
            },
            "cache_performance": cache_stats,
            "alerts": {
                "total": len(alerts),
                "critical": alert_counts.get("critical", 0),
                "error": alert_counts.get("error", 0),
                "warning": alert_counts.get("warning", 0),
                "info": alert_counts.get("info", 0),
            },
            "monitoring_status": {
                "aktiv": self._aktiv,
                "gespeicherte_metriken": sum(len(m) for m in self._metriken.values()),
                "gespeicherte_alerts": len(self._alerts),
                "gespeicherte_snapshots": len(self._snapshots),
            },
        }

    def exportiere_metriken(self, datei_pfad: str, format: str = "json"):
        """Exportiere Metriken in eine Datei."""
        metriken = []
        for metrik_liste in self._metriken.values():
            metriken.extend([m.to_dict() for m in metrik_liste])

        alerts = [alert.to_dict() for alert in self._alerts]
        snapshots = [snapshot.to_dict() for snapshot in self._snapshots]

        daten = {
            "metriken": metriken,
            "alerts": alerts,
            "snapshots": snapshots,
            "bericht": self.get_performance_bericht(),
            "export_timestamp": time.time(),
        }

        if format.lower() == "json":
            with open(datei_pfad, "w", encoding="utf-8") as f:
                json.dump(daten, f, indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"Unbekanntes Format: {format}")

    def setze_grenzwert(self, metrik_typ: str, name: str, level: str, wert: float):
        """Setze einen benutzerdefinierten Grenzwert."""
        if metrik_typ not in self._grenzwerte:
            self._grenzwerte[metrik_typ] = {}

        if name not in self._grenzwerte[metrik_typ]:
            self._grenzwerte[metrik_typ][name] = {}

        self._grenzwerte[metrik_typ][name][level] = wert

    def reset_metriken(self):
        """Lösche alle gesammelten Metriken."""
        with self._lock:
            self._metriken.clear()
            self._alerts.clear()
            self._snapshots.clear()


# Globale Monitor-Instanz
monitor = PerformanceMonitor()


# Bequeme Funktionen und Decorators
def performance_monitor(name: Optional[str] = None, **tags):
    """
    Decorator zum automatischen Monitoring von Funktionen.

    Args:
        name: Optionaler Name für die Metrik (standardmäßig Funktionsname)
        **tags: Zusätzliche Tags für die Metrik
    """

    def decorator(func):
        metrik_name = name or f"{func.__module__}.{func.__name__}"

        def wrapper(*args, **kwargs):
            with monitor.messe_berechnung(metrik_name, **tags):
                return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator


def messe_performance(name: str, **tags):
    """
    Bequeme Funktion zum manuellen Messen von Performance.

    Args:
        name: Name der Messung
        **tags: Zusätzliche Tags
    """
    return monitor.messe_berechnung(name, **tags)


def get_performance_bericht() -> Dict[str, Any]:
    """Gib einen aktuellen Performance-Bericht zurück."""
    return monitor.get_performance_bericht()


def exportiere_performance_daten(datei_pfad: str, format: str = "json"):
    """Exportiere Performance-Daten in eine Datei."""
    monitor.exportiere_metriken(datei_pfad, format)


def registriere_performance_callback(
    metrik_typ: Union[MetrikTyp, str], callback: Callable[[PerformanceMetrik], None]
):
    """Registriere einen Callback für Performance-Metriken."""
    monitor.registriere_callback(metrik_typ, callback)
