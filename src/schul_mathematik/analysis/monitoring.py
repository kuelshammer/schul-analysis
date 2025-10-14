"""
Performance Monitoring System für das Schul-Analysis Framework.

Dieses Modul bietet umfassende Performance-Überwachung für:
- Caching-Effizienz
- Berechnungszeiten
- Speicherverbrauch
- Bottleneck-Erkennung

⚠️ **WICHTIG:** Das Monitoring ist standardmäßig DEAKTIVIERT, um unnötigen Overhead
bei schulischen Berechnungen zu vermeiden. Für Performance-Analyse kann es bei Bedarf
aktiviert werden.

Aktivierungsmöglichkeiten:
- Environment Variable: `SCHUL_ANALYSIS_MONITORING=true`
- Konfiguration: `SchulAnalysisConfig.MONITORING = True`
"""

import logging
import os
import time
from collections import defaultdict, deque
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

import psutil

from .config import SchulAnalysisConfig


@dataclass
class PerformanceMetrics:
    """Strukturierte Performance-Metriken für eine Operation."""

    operation: str
    duration: float
    memory_before: float
    memory_after: float
    memory_delta: float
    cache_hits: int = 0
    cache_misses: int = 0
    cache_hit_rate: float = 0.0
    success: bool = True
    error_message: Optional[str] = None

    @property
    def memory_usage_mb(self) -> float:
        """Speicherverbrauch in MB."""
        return self.memory_delta / 1024 / 1024

    @property
    def efficiency_score(self) -> float:
        """Effizienz-Score (0-100) basierend auf Zeit und Speicher."""
        time_score = max(0, 100 - (self.duration * 10))  # 0.1s = 99 Punkte
        memory_score = max(0, 100 - (self.memory_usage_mb * 10))  # 10MB = 0 Punkte
        return (time_score + memory_score) / 2


class PerformanceMonitor:
    """
    Zentraler Performance-Monitor für das Schul-Analysis Framework.

    Features:
    - Automatische Performance-Messung
    - Caching-Statistiken
    - Speicherüberwachung
    - Bottleneck-Erkennung
    - Historische Datenanalyse
    """

    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics_history: deque = deque(maxlen=max_history)
        self.operation_stats: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "count": 0,
                "total_time": 0.0,
                "total_memory": 0.0,
                "min_time": float("inf"),
                "max_time": 0.0,
                "errors": 0,
                "cache_hits": 0,
                "cache_misses": 0,
            }
        )
        self.active_operations: Dict[str, PerformanceMetrics] = {}

        # Monitoring ist standardmäßig deaktiviert für schulischen Gebrauch
        self.enabled = SchulAnalysisConfig.MONITORING

        # Logger für Performance-Warnungen
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def monitor_operation(self, operation: str, **kwargs):
        """
        Context Manager für Performance-Monitoring einer Operation.

        Args:
            operation: Name der Operation
            **kwargs: Zusätzliche Metadaten

        Yields:
            PerformanceMetrics: Aktive Metriken für die Operation
        """
        if not self.enabled:
            yield None
            return

        # Start-Messung
        start_time = time.time()
        memory_before = psutil.Process().memory_info().rss

        # Erstelle Metriken-Objekt
        metrics = PerformanceMetrics(
            operation=operation,
            duration=0.0,
            memory_before=memory_before,
            memory_after=memory_before,
            memory_delta=0.0,
            **kwargs,
        )

        self.active_operations[operation] = metrics

        try:
            yield metrics

            # Erfolgsvolle Messung
            metrics.success = True

        except Exception as e:
            # Fehler bei der Operation
            metrics.success = False
            metrics.error_message = str(e)
            self.operation_stats[operation]["errors"] += 1
            raise

        finally:
            # Ende-Messung
            end_time = time.time()
            memory_after = psutil.Process().memory_info().rss

            metrics.duration = end_time - start_time
            metrics.memory_after = memory_after
            metrics.memory_delta = memory_after - memory_before

            # Statistiken aktualisieren
            stats = self.operation_stats[operation]
            stats["count"] += 1
            stats["total_time"] += metrics.duration
            stats["total_memory"] += metrics.memory_delta
            stats["min_time"] = min(stats["min_time"], metrics.duration)
            stats["max_time"] = max(stats["max_time"], metrics.duration)

            # Caching-Statistiken
            if hasattr(metrics, "cache_hits"):
                stats["cache_hits"] += metrics.cache_hits
            if hasattr(metrics, "cache_misses"):
                stats["cache_misses"] += metrics.cache_misses

            # Zur Historie hinzufügen
            self.metrics_history.append(metrics)

            # Aus aktiven Operationen entfernen
            if operation in self.active_operations:
                del self.active_operations[operation]

            # Performance-Warnung bei langsamen Operationen
            if metrics.duration > 1.0:  # Mehr als 1 Sekunde
                self.logger.warning(
                    f"Langsame Operation erkannt: {operation} "
                    f"dauerte {metrics.duration:.3f}s"
                )

            # Speicher-Warnung bei hohem Verbrauch
            if metrics.memory_usage_mb > 50:  # Mehr als 50MB
                self.logger.warning(
                    f"Hoher Speicherverbrauch bei {operation}: "
                    f"{metrics.memory_usage_mb:.2f}MB"
                )

    def update_cache_stats(self, operation: str, hits: int, misses: int):
        """
        Aktualisiert Caching-Statistiken für eine Operation.

        Args:
            operation: Name der Operation
            hits: Anzahl Cache-Hits
            misses: Anzahl Cache-Misses
        """
        if operation in self.active_operations:
            metrics = self.active_operations[operation]
            metrics.cache_hits = hits
            metrics.cache_misses = misses
            metrics.cache_hit_rate = (
                hits / (hits + misses) if (hits + misses) > 0 else 0.0
            )

    def get_operation_stats(self, operation: str) -> Dict[str, Any]:
        """
        Gibt detaillierte Statistiken für eine Operation zurück.

        Args:
            operation: Name der Operation

        Returns:
            Dictionary mit Statistiken
        """
        stats = self.operation_stats.get(operation, {})

        if stats.get("count", 0) > 0:
            stats.update(
                {
                    "avg_time": stats["total_time"] / stats["count"],
                    "avg_memory": stats["total_memory"] / stats["count"],
                    "cache_hit_rate": stats["cache_hits"]
                    / (stats["cache_hits"] + stats["cache_misses"])
                    if (stats["cache_hits"] + stats["cache_misses"]) > 0
                    else 0.0,
                    "error_rate": stats["errors"] / stats["count"],
                }
            )

        return stats

    def get_bottlenecks(self, min_duration: float = 0.1) -> List[Dict[str, Any]]:
        """
        Identifiziert Performance-Bottlenecks.

        Args:
            min_duration: Minimale Dauer für Bottleneck-Erkennung

        Returns:
            Liste der Bottlenecks sortiert nach Dauer
        """
        bottlenecks = []

        for operation, stats in self.operation_stats.items():
            if stats.get("count", 0) > 0:
                avg_time = stats["total_time"] / stats["count"]
                if avg_time >= min_duration:
                    bottlenecks.append(
                        {
                            "operation": operation,
                            "avg_duration": avg_time,
                            "count": stats["count"],
                            "total_time": stats["total_time"],
                            "error_rate": stats["errors"] / stats["count"],
                            "efficiency_score": max(0, 100 - (avg_time * 10)),
                        }
                    )

        return sorted(bottlenecks, key=lambda x: x["avg_duration"], reverse=True)

    def get_memory_usage(self) -> Dict[str, float]:
        """
        Gibt aktuellen Speicherverbrauch zurück.

        Returns:
            Dictionary mit Speicher-Informationen
        """
        process = psutil.Process()
        memory_info = process.memory_info()

        return {
            "rss_mb": memory_info.rss / 1024 / 1024,
            "vms_mb": memory_info.vms / 1024 / 1024,
            "percent": process.memory_percent(),
        }

    def get_cache_efficiency(self) -> Dict[str, float]:
        """
        Berechnet globale Caching-Effizienz.

        Returns:
            Dictionary mit Caching-Statistiken
        """
        total_hits = sum(stats["cache_hits"] for stats in self.operation_stats.values())
        total_misses = sum(
            stats["cache_misses"] for stats in self.operation_stats.values()
        )
        total_requests = total_hits + total_misses

        return {
            "global_hit_rate": total_hits / total_requests
            if total_requests > 0
            else 0.0,
            "total_hits": total_hits,
            "total_misses": total_misses,
            "total_requests": total_requests,
        }

    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Gibt eine Zusammenfassung der Performance-Statistiken zurück.

        Returns:
            Umfassende Performance-Zusammenfassung
        """
        total_operations = sum(
            stats["count"] for stats in self.operation_stats.values()
        )
        total_time = sum(stats["total_time"] for stats in self.operation_stats.values())

        return {
            "total_operations": total_operations,
            "total_time": total_time,
            "avg_operation_time": total_time / total_operations
            if total_operations > 0
            else 0,
            "memory_usage": self.get_memory_usage(),
            "cache_efficiency": self.get_cache_efficiency(),
            "bottlenecks": self.get_bottlenecks(),
            "top_operations": dict(
                sorted(
                    self.operation_stats.items(),
                    key=lambda x: x[1]["total_time"],
                    reverse=True,
                )[:5]
            ),
        }

    def reset_stats(self):
        """Setzt alle Statistiken zurück."""
        self.operation_stats.clear()
        self.metrics_history.clear()
        self.active_operations.clear()

        # Garbage Collection anstoßen
        gc.collect()

    def enable(self):
        """Aktiviert das Performance-Monitoring."""
        self.enabled = True

    def disable(self):
        """Deaktiviert das Performance-Monitoring."""
        self.enabled = False


# Globaler Performance-Monitor Instanz
_performance_monitor = PerformanceMonitor()


def get_performance_monitor() -> PerformanceMonitor:
    """Gibt den globalen Performance-Monitor zurück."""
    return _performance_monitor


def monitor_performance(operation: str = None):
    """
    Decorator für automatisches Performance-Monitoring von Funktionen.

    Args:
        operation: Name der Operation (wenn None, wird Funktionsname verwendet)
    """

    def decorator(func: Callable) -> Callable:
        op_name = operation or f"{func.__module__}.{func.__name__}"

        @wraps(func)
        def wrapper(*args, **kwargs):
            with get_performance_monitor().monitor_operation(op_name) as metrics:
                result = func(*args, **kwargs)

                # Wenn das Ergebnis Caching-Informationen hat
                if hasattr(result, "_cache_stats"):
                    cache_stats = result._cache_stats
                    get_performance_monitor().update_cache_stats(
                        op_name,
                        cache_stats.get("hits", 0),
                        cache_stats.get("misses", 0),
                    )

                return result

        return wrapper

    return decorator


# Convenience-Funktionen für häufige Operationen
def monitor_function_operation(func_name: str = None):
    """Decorator für Funktions-Operationen."""
    return monitor_performance(func_name or "function_operation")


def monitor_symbolic_operation(func_name: str = None):
    """Decorator für symbolische Operationen."""
    return monitor_performance(func_name or "symbolic_operation")


def monitor_visualization_operation(func_name: str = None):
    """Decorator für Visualisierungs-Operationen."""
    return monitor_performance(func_name or "visualization_operation")
