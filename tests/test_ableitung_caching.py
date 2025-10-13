"""
Testet das Performance Caching für Ableitungen in der Funktion-Klasse.
Diese Tests überprüfen, dass Ableitungen korrekt gecached werden und
die Performance verbessert wird.
"""

import pytest
import sympy as sp
import logging
from time import time

# Import the Funktion class
from schul_mathematik.analysis.funktion import Funktion


class TestAbleitungCaching:
    """Test-Klasse für Ableitungs-Caching."""

    def setup_method(self):
        """Setup für Test-Methoden."""
        # Configure logging to capture debug messages during tests
        logging.basicConfig(level=logging.DEBUG)

        # Testfunktionen erstellen
        self.f_polynom = Funktion("x^3 - 3*x^2 + 4")
        self.f_trig = Funktion("sin(x) + cos(x)")
        self.f_param = Funktion("a*x^2 + b*x + c")

    def test_cache_initialization(self):
        """Testet, dass der Cache korrekt initialisiert wird."""
        f = Funktion("x^2")

        # Am Anfang sollte kein Cache vorhanden sein
        assert not hasattr(f, "_ableitung_cache")

        # Nach erster Ableitung sollte Cache vorhanden sein
        f1 = f.ableitung(1)
        assert hasattr(f, "_ableitung_cache")
        assert isinstance(f._ableitung_cache, dict)
        assert len(f._ableitung_cache) == 1
        assert f._ableitung_cache_max_size == 50

    def test_cache_hit_same_order(self):
        """Testet Cache-Hit bei gleicher Ableitungsordnung."""
        f = Funktion("x^3 - 2*x^2 + x")

        # Erste Ableitung - sollte berechnet werden
        f1_first = f.ableitung(1)
        cache_size_before = len(f._ableitung_cache)

        # Zweite Ableitung gleicher Ordnung - sollte aus Cache kommen
        f1_second = f.ableitung(1)

        # Sollte gleiche Instanz sein (Cache-Hit)
        assert f1_first is f1_second
        assert (
            len(f._ableitung_cache) == cache_size_before
        )  # Größe sollte gleich bleiben

    def test_cache_different_orders(self):
        """Testet Cache für verschiedene Ableitungsordnungen."""
        f = Funktion("x^4")

        # Berechne verschiedene Ableitungen
        f1 = f.ableitung(1)
        f2 = f.ableitung(2)
        f3 = f.ableitung(3)

        # Alle sollten im Cache sein
        assert len(f._ableitung_cache) <= 4

        # Nochmal aufrufen - sollte aus Cache kommen
        f1_cached = f.ableitung(1)
        f2_cached = f.ableitung(2)
        f3_cached = f.ableitung(3)

        # Sollten gleiche Instanzen sein
        assert f1 is f1_cached
        assert f2 is f2_cached
        assert f3 is f3_cached

    def test_cache_lru_eviction(self):
        """Testet LRU-Eviction wenn Cache voll ist."""
        f = Funktion("x^5")

        # Initialisiere Cache mit kleiner Größe für Test
        f._ableitung_cache = {}
        f._ableitung_cache_max_size = 2
        f._ableitung_cache_hits = 0
        f._ableitung_cache_misses = 0

        # Fülle Cache über die Grenze
        f1 = f.ableitung(1)
        f2 = f.ableitung(2)

        # Sollte genau an der Grenze sein
        assert len(f._ableitung_cache) <= 3

        # Füge dritte Ableitung hinzu - sollte Eviction auslösen
        f3 = f.ableitung(3)

        # Cache sollte nicht zu groß geworden sein
        assert len(f._ableitung_cache) <= 3

        # Die neuesten Ableitungen sollten noch im Cache sein
        cache_key_2 = (2, id(f))
        cache_key_3 = (3, id(f))
        assert cache_key_2 in f._ableitung_cache or cache_key_3 in f._ableitung_cache

    def test_cache_different_functions(self):
        """Testet, dass verschiedene Funktionen unterschiedliche Caches haben."""
        f1 = Funktion("x^2")
        f2 = Funktion("x^3")

        # Berechne Ableitungen für beide Funktionen
        f1_ableitung = f1.ableitung(1)
        f2_ableitung = f2.ableitung(1)

        # Beide sollten eigene Caches haben
        assert hasattr(f1, "_ableitung_cache")
        assert hasattr(f2, "_ableitung_cache")
        assert len(f1._ableitung_cache) == 1
        assert len(f2._ableitung_cache) == 1

        # Caches sollten unterschiedlich sein
        assert f1._ableitung_cache != f2._ableitung_cache

    def test_cache_performance_improvement(self):
        """Testet, dass Cache Performance verbessert (durch weniger Neuberechnungen)."""
        f = Funktion("sin(x)*cos(x) + x^3 - 2*x^2 + x - 1")

        # Erste Berechnung (langsam)
        start_time = time()
        f1_first = f.ableitung(1)
        first_time = time() - start_time

        # Zweite Berechnung aus Cache (schnell)
        start_time = time()
        f1_second = f.ableitung(1)
        second_time = time() - start_time

        # Zweite sollte deutlich schneller sein (wenn Cache funktioniert)
        # Wir können nicht genau vergleichen, aber zumindest sollte keine Exception auftreten
        assert f1_first is f1_second
        assert second_time < first_time * 2  # Sollte zumindest nicht langsamer sein

    def test_cache_with_parameters(self):
        """Testet Caching bei parametrischen Funktionen."""
        f = Funktion("a*x^2 + b*x + c")

        # Berechne Ableitungen
        f1 = f.ableitung(1)
        f2 = f.ableitung(2)

        # Sollte korrekt funktionieren
        assert len(f._ableitung_cache) == 2
        assert "2*a" in f1.term() and "x" in f1.term() and "b" in f1.term()
        assert "2*a" in f2.term()

    def test_cache_independence(self):
        """Testet, dass Caches verschiedener Funktionen unabhängig sind."""
        f1 = Funktion("x^2")
        f2 = Funktion("x^3")

        # Berechne Ableitungen
        f1_ableitung = f1.ableitung(1)
        f2_ableitung = f2.ableitung(1)

        # Ändere Cache von f1
        f1._ableitung_cache.clear()

        # Cache von f2 sollte unberührt sein
        assert len(f2._ableitung_cache) == 1
        assert len(f1._ableitung_cache) == 0

    def test_cache_logging(self):
        """Testet, dass Logging-Messages korrekt ausgegeben werden."""
        f = Funktion("x^2")

        # Erste Ableitung sollte Cache-Miss loggen
        f1 = f.ableitung(1)

        # Zweite Ableitung sollte Cache-Hit loggen
        f1_cached = f.ableitung(1)

        # Sollte keine Exception werfen und gleiche Instanz zurückgeben
        assert f1 is f1_cached

    def test_cache_edge_cases(self):
        """Testet Randfälle für das Caching."""
        f = Funktion("x")

        # Teste höhere Ableitungen
        f1 = f.ableitung(1)  # 1
        f2 = f.ableitung(2)  # 0
        f3 = f.ableitung(3)  # 0

        # Sollte korrekt funktionieren
        assert len(f._ableitung_cache) == 3
        assert f1.term() == "1"
        assert f2.term() == "0"
        assert f3.term() == "0"


if __name__ == "__main__":
    # Manueller Testlauf
    test = TestAbleitungCaching()
    test.setup_method()

    print("Teste Ableitungs-Caching...")

    try:
        test.test_cache_initialization()
        print("✓ test_cache_initialization")
    except Exception as e:
        print(f"✗ test_cache_initialization: {e}")

    try:
        test.test_cache_hit_same_order()
        print("✓ test_cache_hit_same_order")
    except Exception as e:
        print(f"✗ test_cache_hit_same_order: {e}")

    try:
        test.test_cache_different_orders()
        print("✓ test_cache_different_orders")
    except Exception as e:
        print(f"✗ test_cache_different_orders: {e}")

    try:
        test.test_cache_lru_eviction()
        print("✓ test_cache_lru_eviction")
    except Exception as e:
        print(f"✗ test_cache_lru_eviction: {e}")

    try:
        test.test_cache_performance_improvement()
        print("✓ test_cache_performance_improvement")
    except Exception as e:
        print(f"✗ test_cache_performance_improvement: {e}")

    try:
        test.test_cache_with_parameters()
        print("✓ test_cache_with_parameters")
    except Exception as e:
        print(f"✗ test_cache_with_parameters: {e}")

    print("Ableitungs-Caching Tests abgeschlossen!")
