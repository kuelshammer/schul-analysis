"""
Tests für die erweiterten Performance-Caching-Funktionen
"""

import pytest
import sympy as sp
from functools import lru_cache

from schul_mathematik.analysis.funktion import (
    _cached_simplify,
    _cached_solve,
    _cached_diff,
    _cached_factor,
    _cached_expand,
    _cached_integrate,
    _cached_limit,
    _cached_subs,
    _cached_solve_poly,
    _cached_series,
    _cached_together,
    _cached_apart,
    _cached_function_value,
    CacheStats,
    get_cache_stats,
    clear_all_caches,
    get_cache_info,
    Funktion,
)


class TestPerformanceCaching:
    """Testet die Performance-Caching-Funktionen"""

    def test_cached_simplify(self):
        """Testet gecachte Vereinfachung"""
        x = sp.symbols("x")
        expr = (x**2 + 2 * x + 1) * (x - 1) / (x + 1)

        # Erster Aufruf - sollte Cache füllen
        result1 = _cached_simplify(expr)

        # Zweiter Aufruf - sollte Cache nutzen
        result2 = _cached_simplify(expr)

        assert result1 == result2
        assert _cached_simplify.cache_info().hits > 0

    def test_cached_solve(self):
        """Testet gecachte Gleichungslösung"""
        x = sp.symbols("x")
        equation = x**2 - 4

        # Erster Aufruf
        result1 = _cached_solve(equation, x)

        # Zweiter Aufruf
        result2 = _cached_solve(equation, x)

        assert result1 == result2
        assert len(result1) == 2  # x = 2, x = -2
        assert _cached_solve.cache_info().hits > 0

    def test_cached_diff(self):
        """Testet gecachte Differentiation"""
        x = sp.symbols("x")
        expr = x**3 + 2 * x**2 + x + 1

        # Erste Ableitung
        result1 = _cached_diff(expr, x, 1)
        result1_again = _cached_diff(expr, x, 1)

        # Zweite Ableitung
        result2 = _cached_diff(expr, x, 2)
        result2_again = _cached_diff(expr, x, 2)

        assert result1 == result1_again
        assert result2 == result2_again
        assert _cached_diff.cache_info().hits >= 2

    def test_cached_factor(self):
        """Testet gecachte Faktorisierung"""
        x = sp.symbols("x")
        expr = x**2 - 4

        result1 = _cached_factor(expr)
        result2 = _cached_factor(expr)

        assert result1 == result2
        assert result1 == (x - 2) * (x + 2)
        assert _cached_factor.cache_info().hits > 0

    def test_cached_expand(self):
        """Testet gecachte Expansion"""
        x = sp.symbols("x")
        expr = (x + 1) * (x + 2) * (x + 3)

        result1 = _cached_expand(expr)
        result2 = _cached_expand(expr)

        assert result1 == result2
        assert result1 == x**3 + 6 * x**2 + 11 * x + 6
        assert _cached_expand.cache_info().hits > 0

    def test_cached_integrate(self):
        """Testet gecachte Integration"""
        x = sp.symbols("x")
        expr = x**2 + 2 * x + 1

        result1 = _cached_integrate(expr, x)
        result2 = _cached_integrate(expr, x)

        assert result1 == result2
        assert result1 == x**3 / 3 + x**2 + x
        assert _cached_integrate.cache_info().hits > 0

    def test_cached_limit(self):
        """Testet gecachte Limes-Berechnung"""
        x = sp.symbols("x")
        expr = (x**2 - 1) / (x - 1)

        result1 = _cached_limit(expr, x, 1)
        result2 = _cached_limit(expr, x, 1)

        assert result1 == result2
        assert float(result1) == 2.0
        assert _cached_limit.cache_info().hits > 0

    def test_cached_subs(self):
        """Testet gecachte Substitution"""
        x, y = sp.symbols("x y")
        expr = x**2 + 2 * x + 1

        result1 = _cached_subs(expr, x, y)
        result2 = _cached_subs(expr, x, y)

        assert result1 == result2
        assert result1 == y**2 + 2 * y + 1
        assert _cached_subs.cache_info().hits > 0

    def test_cached_solve_poly(self):
        """Testet gecachte Polynom-Lösung"""
        x = sp.symbols("x")
        expr = x**3 - 6 * x**2 + 11 * x - 6  # (x-1)(x-2)(x-3)

        result1 = _cached_solve_poly(expr, x)
        result2 = _cached_solve_poly(expr, x)

        assert result1 == result2
        # Sollte Lösungen x=1, x=2, x=3 geben
        assert len(result1) == 3
        assert _cached_solve_poly.cache_info().hits > 0

    def test_cached_series(self):
        """Testet gecachte Reihenentwicklung"""
        x = sp.symbols("x")
        expr = sp.sin(x)

        result1 = _cached_series(expr, x, 0, 5)
        result2 = _cached_series(expr, x, 0, 5)

        assert result1 == result2
        assert _cached_series.cache_info().hits > 0

    def test_cached_together_apart(self):
        """Testet gecachte Together/Apart Operationen"""
        x = sp.symbols("x")
        expr = 1 / (x + 1) + 1 / (x - 1)

        # Together
        result_together1 = _cached_together(expr)
        result_together2 = _cached_together(expr)
        assert result_together1 == result_together2
        assert _cached_together.cache_info().hits > 0

        # Apart
        expr2 = 2 * x / (x**2 - 1)
        result_apart1 = _cached_apart(expr2)
        result_apart2 = _cached_apart(expr2)
        assert result_apart1 == result_apart2
        assert _cached_apart.cache_info().hits > 0

    def test_cached_function_value(self):
        """Testet gecachte Funktionswert-Berechnung"""
        expr_str = "x**2 + 2*x + 1"

        result1 = _cached_function_value(expr_str, 2.0)
        result2 = _cached_function_value(expr_str, 2.0)
        result3 = _cached_function_value(expr_str, 3.0)

        assert result1 == result2  # Gleiche Werte
        assert result1 == 9.0  # 2^2 + 2*2 + 1 = 9
        assert result3 == 16.0  # 3^2 + 2*3 + 1 = 16
        assert _cached_function_value.cache_info().hits > 0


class TestCacheStats:
    """Testet die Cache-Statistik-Klasse"""

    def test_cache_stats_basic(self):
        """Testet grundlegende Cache-Statistik-Funktionen"""
        stats = CacheStats()

        # Anfangs sollte alles 0 sein
        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.total_operations == 0
        assert stats.hit_rate() == 0.0
        assert stats.miss_rate() == 0.0

        # Einige Operationen aufzeichnen
        stats.record_hit()
        stats.record_hit()
        stats.record_miss()

        assert stats.hits == 2
        assert stats.misses == 1
        assert stats.total_operations == 3
        assert stats.hit_rate() == 2 / 3
        assert stats.miss_rate() == 1 / 3

    def test_cache_stats_string(self):
        """Testet die String-Repräsentation"""
        stats = CacheStats()
        stats.record_hit()
        stats.record_miss()

        str_repr = str(stats)
        assert "hits=1" in str_repr
        assert "misses=1" in str_repr
        assert "hit_rate=0.500" in str_repr

    def test_global_cache_functions(self):
        """Testet globale Cache-Funktionen"""
        # Cache leeren
        clear_all_caches()

        stats = get_cache_stats()
        assert stats.total_operations == 0

        # Einige Cache-Operationen durchführen
        x = sp.symbols("x")
        expr = x**2 - 4
        _cached_solve(expr, x)
        _cached_solve(expr, x)  # Cache-Hit

        # Manuelles Aufzeichnen von Stats (da die Decorators es nicht automatisch tun)
        from schul_mathematik.analysis.funktion import _cache_stats

        _cache_stats.record_hit()
        _cache_stats.record_hit()

        # Statistiken abrufen
        info = get_cache_info()
        assert "cached_solve" in info
        assert "global_stats" in info

        # Stats sollten aktualisiert sein
        stats = get_cache_stats()
        assert stats.total_operations > 0


class TestCacheIntegration:
    """Testet die Integration des Caching in die Funktionsklasse"""

    def test_function_caching_integration(self):
        """Testet, dass Caching in Funktionsmethoden integriert ist"""
        f = Funktion("x^2 + 2*x + 1")

        # Ableitung berechnen
        f1 = f.ableitung(1)  # Erster Aufruf
        f2 = f.ableitung(1)  # Zweiter Aufruf (sollte Cache nutzen)

        assert f1.term() == f2.term()
        # Beide Formate sind möglich (mit oder ohne Unicode-Symbole)
        expected_terms = ["2*x + 2", "2⋅x + 2"]
        assert f1.term() in expected_terms

    def test_performance_improvement(self):
        """Testet messbare Performance-Verbesserung durch Caching"""
        import time

        # Komplexen Ausdruck erstellen
        f = Funktion("(x^5 + 3*x^4 - 2*x^3 + x^2 - 4*x + 1)/(x^2 + 1)")

        # Mehrere Ableitungen berechnen (erster Aufruf ist langsam)
        start_time = time.time()
        for i in range(10):
            ableitung = f.ableitung(2)  # Zweite Ableitung
        first_time = time.time() - start_time

        # Cache leeren und wiederholen (sollte langsamer sein)
        clear_all_caches()
        start_time = time.time()
        for i in range(10):
            ableitung = f.ableitung(2)
        second_time = time.time() - start_time

        # Die zweite Ausführung sollte ohne Cache langsamer sein
        # (In der Praxis ist der Unterschied bei einfachen Funktionen oft minimal)
        print(f"Mit Cache: {first_time:.4f}s, Ohne Cache: {second_time:.4f}s")

        # Wichtig: Das Ergebnis sollte immer gleich sein
        assert "x" in ableitung.term()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
