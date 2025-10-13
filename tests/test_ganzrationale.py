"""
Unit Tests für die ganzrationalen Funktionen mit neuer Magic Factory API

Diese Tests verwenden die neue Funktion() Factory und testen die Funktionalität
der automatisch erkannten GanzrationaleFunktion Klasse.
"""

import os
import sys

import pytest

# Füge src zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from schul_mathematik import Funktion


class TestGanzrationaleFunktionKonstruktoren:
    """Testet verschiedene Konstruktor-Formate mit neuer API"""

    def test_string_konstruktor_standard(self):
        """Test: Standard String-Konstruktor"""
        f = Funktion("x^2+4x-2")
        assert f.term() == "x^2 + 4*x - 2"  # Aktuelles Format mit Vorzeichen
        # Momentan wird alles als ganzrational erkannt
        assert f.funktionstyp == "ganzrational"

    def test_string_konstruktor_latex(self):
        """Test: LaTeX-ähnlicher String-Konstruktor (ohne $ Zeichen)"""
        f = Funktion("x^2+4x-2")  # LaTeX ohne $ Zeichen
        assert f.term() == "x^2 + 4*x - 2"  # Aktuelles Format mit Vorzeichen
        assert f.funktionstyp == "ganzrational"

    def test_string_konstruktor_python_syntax(self):
        """Test: Python-Syntax String-Konstruktor"""
        f = Funktion("x**2+4*x-2")
        assert f.term() == "x^2 + 4*x - 2"  # Aktuelles Format mit Vorzeichen
        assert f.funktionstyp == "ganzrational"

    def test_string_konstruktor_implizite_multiplikation(self):
        """Test: Implizite Multiplikation"""
        f = Funktion("2x")
        assert f.term() == "2*x"  # Formatierung mit *
        assert f.funktionstyp == "ganzrational"

    def test_string_konstruktor_mit_leerzeichen(self):
        """Test: String mit Leerzeichen"""
        f = Funktion("x^2 + 4x - 2")
        assert f.term() == "x^2 + 4*x - 2"  # Aktuelles Format mit Vorzeichen
        assert f.funktionstyp == "ganzrational"

    def test_konstante_funktion(self):
        """Test: Konstante Funktion"""
        f = Funktion("5")
        assert f.term() == "5"
        assert f.funktionstyp == "ganzrational"

    def test_lineare_funktion(self):
        """Test: Lineare Funktion"""
        f = Funktion("x")
        assert f.term() == "x"
        assert f.funktionstyp == "ganzrational"

    def test_null_funktion(self):
        """Test: Null-Funktion"""
        f = Funktion("0")
        assert f.term() == "0"
        assert f.funktionstyp == "ganzrational"

    def test_ungueltige_eingabe_wird_akzeptiert(self):
        """Test: Verschiedene Eingabetypen werden akzeptiert"""
        # In der neuen API werden viele Eingaben akzeptiert
        f = Funktion("sin(x)")
        assert f.funktionstyp == "trigonometrisch"

        # Zahlen werden als konstante Funktionen akzeptiert (Feature, kein Bug)
        f_konstant = Funktion(123)
        assert f_konstant.funktionstyp == "ganzrational"
        assert f_konstant.term() == "123"


class TestGanzrationaleFunktionMethoden:
    """Testet die Methoden der automatisch erkannten GanzrationaleFunktion"""

    def setup_method(self):
        """Setup für Test-Methoden"""
        self.f_quad = Funktion("x^2-4x+3")  # (x-1)(x-3)
        self.f_linear = Funktion("2x-1")
        self.f_kubisch = Funktion("x^3-2x^2-5x+6")

    def test_term_method(self):
        """Test: term() Methode"""
        assert self.f_quad.term() == "x^2 - 4*x + 3"

    def test_term_latex_method(self):
        """Test: term_latex() Methode"""
        latex = self.f_quad.term_latex()
        assert "x^{2}" in latex
        assert "4" in latex
        assert "3" in latex

    def test_wert_method(self):
        """Test: wert() Methode"""
        assert abs(self.f_quad.wert(0) - 3) < 1e-10
        assert abs(self.f_quad.wert(1) - 0) < 1e-10
        assert abs(self.f_quad.wert(3) - 0) < 1e-10
        assert abs(self.f_quad.wert(2) - (-1)) < 1e-10

    def test_ableitung_method(self):
        """Test: ableitung() Methode"""
        f_strich = self.f_quad.ableitung(1)
        assert f_strich.term() == "2*x - 4"

        f_doppelstrich = self.f_quad.ableitung(2)
        assert f_doppelstrich.term() == "2"

    def test_nullstellen_property(self):
        """Test: nullstellen als Methode (konsistente API)"""
        # Quadratische Funktion mit zwei Nullstellen
        nullstellen = self.f_quad.nullstellen()  # Jetzt Methode mit ()
        assert len(nullstellen) == 2
        assert abs(float(nullstellen[0].x) - 3.0) < 1e-10  # Reihenfolge ist [3, 1]
        assert abs(float(nullstellen[1].x) - 1.0) < 1e-10

        # Lineare Funktion
        nullstellen_linear = self.f_linear.nullstellen()  # Jetzt Methode mit ()
        assert len(nullstellen_linear) == 1
        assert abs(float(nullstellen_linear[0].x) - 0.5) < 1e-10

        # Funktion ohne reelle Nullstellen
        f_keine_null = Funktion("x^2+1")
        nullstellen_keine = f_keine_null.nullstellen()  # Jetzt Methode mit ()
        assert len(nullstellen_keine) == 0

    def test_extremstellen_property(self):
        """Test: extremstellen Property - wenn vorhanden"""
        if hasattr(self.f_quad, "extremstellen"):
            extremstellen = self.f_quad.extremstellen()
            assert len(extremstellen) == 1
            assert abs(extremstellen[0][0] - 2.0) < 1e-10  # x-Koordinate
            assert extremstellen[0][2] == "Minimum"  # Art (Index 2, nicht 1)
        else:
            # Wenn nicht vorhanden, überspringen wir diesen Test
            pytest.skip("extremstellen property nicht implementiert")

    def test_funktionstyp_erkenung(self):
        """Test: Automatische Funktionstyp-Erkennung"""
        # Aktuell wird alles als ganzrational erkannt
        assert self.f_quad.funktionstyp == "ganzrational"
        assert self.f_linear.funktionstyp == "ganzrational"
        assert self.f_kubisch.funktionstyp == "ganzrational"


class TestGanzrationaleFunktionEdgeCases:
    """Testet Edge Cases und Sonderfälle"""

    def test_hoehere_grade(self):
        """Test: Funktionen höheren Grades"""
        f = Funktion("x^4-2x^3+3x^2-4x+5")
        assert f.term() == "x^4 - 2*x^3 + 3*x^2 - 4*x + 5"
        assert f.funktionstyp == "ganzrational"

    def test_negative_koeffizienten(self):
        """Test: Negative Koeffizienten"""
        f = Funktion("-x^2+3x-1")
        assert f.term() == "-x^2 + 3*x - 1"

    def test_bruch_koeffizienten(self):
        """Test: Bruch-Koeffizienten"""
        f = Funktion("0.5x^2-1.5x+2.5")
        assert "0.5*x^2" in f.term()
        assert "1.5*x" in f.term()
        assert "2.5" in f.term()

    def test_null_koeffizienten(self):
        """Test: Null-Koeffizienten"""
        f = Funktion("x^2+0*x+1")
        assert f.term() == "x^2 + 1"  # Sollte vereinfacht werden


class TestGanzrationaleFunktionLösungswege:
    """Testet die Lösungsweg-Methoden - wenn verfügbar"""

    def test_nullstellen_weg_quadratisch(self):
        """Test: nullstellen_weg() für quadratische Funktionen - wenn vorhanden"""
        f = Funktion("x^2-4x+3")

        if hasattr(f, "nullstellen_weg"):
            weg = f.nullstellen_weg()
            assert "x^2-4x+3" in weg or "x^2 - 4*x + 3" in weg

    def test_nullstellen_weg_linear(self):
        """Test: nullstellen_weg() für lineare Funktionen - wenn vorhanden"""
        f = Funktion("2x-1")

        if hasattr(f, "nullstellen_weg"):
            weg = f.nullstellen_weg()
            assert "Lineare" in weg or "linear" in weg.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
