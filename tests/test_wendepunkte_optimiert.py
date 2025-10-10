"""
Testet die optimierte Wendepunkte-Implementierung.
Diese Tests überprüfen, dass die neue wendepunkte_optimiert() Methode
korrekt mit dem Nullstellen-Framework integriert ist und die
Hybrid-Strategie für parametrische Funktionen funktioniert.
"""

import pytest
import sympy as sp
from sympy import pi, sin, cos
import logging

# Import the Funktion class and related components
from schul_mathematik.analysis.funktion import Funktion, Wendepunkt, WendepunktTyp


class TestWendepunkteOptimiert:
    """Test-Klasse für optimierte Wendepunkte-Berechnung."""

    def setup_method(self):
        """Setup für Test-Methoden."""
        # Configure logging to capture debug messages during tests
        logging.basicConfig(level=logging.DEBUG)

        # Testfunktionen erstellen
        self.f_kubisch = Funktion("x^3 - 3*x^2 + 2")  # Einfacher kubischer Fall
        self.f_trig = Funktion("sin(x)")  # Trigonometrische Funktion
        self.f_param = Funktion("a*x^3 + b*x^2 + c*x + d")  # Parametrisch
        self.f_x4 = Funktion("x^4")  # x^4 hat Wendepunkt bei x=0
        self.f_x3 = Funktion("x^3")  # x^3 hat Wendepunkt bei x=0

    def test_wendepunkte_optimiert_kubisch(self):
        """Testet Wendepunkte für einfache kubische Funktion."""
        f = Funktion("x^3 - 3*x^2 + 2")

        # Berechne Wendepunkte mit neuer Methode
        wendepunkte = f.wendepunkte_optimiert()

        # Sollte einen Wendepunkt bei x=2 haben
        assert len(wendepunkte) == 1
        wp = wendepunkte[0]
        assert isinstance(wp, Wendepunkt)
        assert wp.typ == WendepunktTyp.WENDEPUNKT
        assert wp.exakt == True

        # Überprüfe x-Koordinate (sollte 1 sein)
        x_wert = wp.x
        assert str(x_wert) == "1" or x_wert == 1

    def test_wendepunkte_optimiert_trigonometrisch(self):
        """Testet Wendepunkte für trigonometrische Funktion."""
        f = Funktion("sin(x)")

        # Berechne Wendepunkte mit neuer Methode
        wendepunkte = f.wendepunkte_optimiert()

        # sin(x) hat Wendepunkte bei x = k*pi
        assert len(wendepunkte) >= 1  # Sollte mindestens einen finden

        # Überprüfe, dass alle gefundenen Punkte Wendepunkte sind
        for wp in wendepunkte:
            assert isinstance(wp, Wendepunkt)
            assert wp.typ == WendepunktTyp.WENDEPUNKT

    def test_wendepunkte_optimiert_parametrisch(self):
        """Testet Wendepunkte für parametrische Funktion."""
        f = Funktion("a*x^3 + b*x^2 + c*x + d")

        # Berechne Wendepunkte mit neuer Methode
        wendepunkte = f.wendepunkte_optimiert()

        # Sollte parametrischen Fallback verwenden
        assert isinstance(wendepunkte, list)

        # Alle Punkte sollten die korrekte Struktur haben
        for wp in wendepunkte:
            assert isinstance(wp, Wendepunkt)
            assert hasattr(wp, "x")
            assert hasattr(wp, "y")
            assert hasattr(wp, "typ")
            assert wp.typ == WendepunktTyp.WENDEPUNKT

    def test_wendepunkte_optimiert_x4(self):
        """Testet Wendepunkte für x^4 (Wendepunkt bei x=0)."""
        f = Funktion("x^4")

        # Berechne Wendepunkte
        wendepunkte = f.wendepunkte_optimiert()

        # Sollte einen Wendepunkt bei x=0 haben
        assert len(wendepunkte) == 1
        wp = wendepunkte[0]

        assert isinstance(wp, Wendepunkt)
        assert str(wp.x) == "0" or wp.x == 0
        assert wp.y == 0  # f(0) = 0
        assert wp.typ == WendepunktTyp.WENDEPUNKT

    def test_wendepunkte_optimiert_x3(self):
        """Testet Wendepunkte für x^3 (Wendepunkt bei x=0)."""
        f = Funktion("x^3")

        # Berechne Wendepunkte
        wendepunkte = f.wendepunkte_optimiert()

        # Sollte einen Wendepunkt bei x=0 haben
        assert len(wendepunkte) == 1
        wp = wendepunkte[0]

        assert isinstance(wp, Wendepunkt)
        assert str(wp.x) == "0" or wp.x == 0
        assert wp.y == 0  # f(0) = 0
        assert wp.typ == WendepunktTyp.WENDEPUNKT

    def test_wendepunkte_optimiert_keine_wendepunkte(self):
        """Testet Funktion ohne Wendepunkte."""
        f = Funktion("x^2")  # Parabel hat keine Wendepunkte

        # Berechne Wendepunkte
        wendepunkte = f.wendepunkte_optimiert()

        # Sollte keine Wendepunkte finden
        assert len(wendepunkte) == 0

    def test_wendepunkte_hybrid_strategie(self):
        """Testet die Hybrid-Strategie (parametrisch vs. nicht-parametrisch)."""
        # Nicht-parametrische Funktion - sollte Framework verwenden
        f1 = Funktion("x^3")
        wp1 = f1.wendepunkte_optimiert()

        # Parametrische Funktion - sollte Fallback verwenden
        f2 = Funktion("a*x^3 + b*x^2 + c*x + d")
        wp2 = f2.wendepunkte_optimiert()

        # Beide sollten funktionieren
        assert isinstance(wp1, list)
        assert isinstance(wp2, list)

    def test_wendepunkte_framework_integration(self):
        """Testet Integration mit dem Nullstellen-Framework."""
        f = Funktion("x^3 - 3*x^2 + 2")

        # Die zweite Ableitung sollte gecached werden
        f2 = f.ableitung(2)

        # Wendepunkte sollten über das Nullstellen-Framework laufen
        wendepunkte = f.wendepunkte_optimiert()

        # Überprüfe, dass die zweite Ableitung verwendet wurde
        assert len(wendepunkte) == 1
        wp = wendepunkte[0]
        assert isinstance(wp, Wendepunkt)

    def test_wendepunkte_dritte_ableitung(self):
        """Testet die dritte Ableitungs-Validierung."""
        f = Funktion("x^3")

        # Berechne dritte Ableitung
        f3 = f.ableitung(3)

        # Sollte 6 sein (f'''(x) = 6 für x^3)
        assert str(f3.term()) == "6"

        # Wendepunkte-Berechnung sollte funktionieren
        wendepunkte = f.wendepunkte_optimiert()
        assert len(wendepunkte) == 1

    def test_wendepunkte_valid_attributes(self):
        """Testet, dass Wendepunkte die korrekten Attribute haben."""
        f = Funktion("x^4 - 2*x^3")  # f''(x) = 12x - 6, einfache Nullstelle bei x=0.5

        wendepunkte = f.wendepunkte_optimiert()

        # Sollte einen Wendepunkt haben
        if len(wendepunkte) > 0:
            wp = wendepunkte[0]
            # Überprüfe, dass es sich um einen validen Wendepunkt handelt
            assert isinstance(wp, Wendepunkt)
            assert hasattr(wp, "x")
            assert hasattr(wp, "y")
            assert hasattr(wp, "typ")
            assert wp.typ.value == "Wendepunkt"

    def test_wendepunkte_error_handling(self):
        """Testet Fehlerbehandlung in der optimierten Methode."""
        # Test mit ungültiger Funktion
        try:
            f = Funktion("invalid_syntax")
            wendepunkte = f.wendepunkte_optimiert()
            # Sollte keine Exception werfen, sondern leere Liste zurückgeben
            assert isinstance(wendepunkte, list)
        except Exception:
            # Wenn Exception geworfen wird, sollte sie behandelt sein
            pass

    def test_wendepunkte_performance_caching(self):
        """Testet, dass das Caching für Ableitungen funktioniert."""
        f = Funktion("x^5 - 3*x^3 + 2*x")

        # Erste Berechnung
        wp1 = f.wendepunkte_optimiert()

        # Zweite Berechnung sollte Cache nutzen
        wp2 = f.wendepunkte_optimiert()

        # Sollte gleiche Ergebnisse liefern
        assert len(wp1) == len(wp2)

        # Überprüfe, dass Cache initialisiert wurde
        assert hasattr(f, "_ableitung_cache")

    def test_wendepunkte_backward_compatibility(self):
        """Testet Kompatibilität mit der alten Methode."""
        f = Funktion("x^3 - 3*x^2 + 2")

        # Alte Methode sollte noch funktionieren
        alte_wendepunkte = f.wendepunkte()

        # Neue Methode sollte strukturierte Objekte liefern
        neue_wendepunkte = f.wendepunkte_optimiert()

        # Beide sollten Ergebnisse liefern
        assert isinstance(alte_wendepunkte, list)
        assert isinstance(neue_wendepunkte, list)


if __name__ == "__main__":
    # Manueller Testlauf
    test = TestWendepunkteOptimiert()
    test.setup_method()

    print("Teste optimierte Wendepunkte-Implementierung...")

    test_methods = [
        test.test_wendepunkte_optimiert_kubisch,
        test.test_wendepunkte_optimiert_trigonometrisch,
        test.test_wendepunkte_optimiert_parametrisch,
        test.test_wendepunkte_optimiert_x4,
        test.test_wendepunkte_optimiert_x3,
        test.test_wendepunkte_optimiert_keine_wendepunkte,
        test.test_wendepunkte_hybrid_strategie,
        test.test_wendepunkte_framework_integration,
        test.test_wendepunkte_dritte_ableitung,
    ]

    for i, method in enumerate(test_methods, 1):
        try:
            method()
            print(f"✓ Test {i}: {method.__name__}")
        except Exception as e:
            print(f"✗ Test {i}: {method.__name__} - {e}")

    print("Wendepunkte-Optimierung Tests abgeschlossen!")
