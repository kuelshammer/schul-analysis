"""
Unit Tests für die GanzrationaleFunktion Klasse
"""

import pytest
import sys
import os

# Füge src zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from schul_analysis.ganzrationale import GanzrationaleFunktion


class TestGanzrationaleFunktionKonstruktoren:
    """Testet verschiedene Konstruktor-Formate"""

    def test_string_konstruktor_standard(self):
        """Test: Standard String-Konstruktor"""
        f = GanzrationaleFunktion("x^2+4x-2")
        assert f.term() == "x**2+4*x**1-2*x**0"
        assert f.koeffizienten == [-2.0, 4.0, 1.0]

    def test_string_konstruktor_latex(self):
        """Test: LaTeX-Format String-Konstruktor"""
        f = GanzrationaleFunktion("$x^2+4x-2$")
        assert f.term() == "x**2+4*x**1-2*x**0"
        assert f.koeffizienten == [-2.0, 4.0, 1.0]

    def test_string_konstruktor_python_syntax(self):
        """Test: Python-Syntax String-Konstruktor"""
        f = GanzrationaleFunktion("x**2+4*x-2")
        assert f.term() == "x**2+4*x**1-2*x**0"
        assert f.koeffizienten == [-2.0, 4.0, 1.0]

    def test_string_konstruktor_implizite_multiplikation(self):
        """Test: Implizite Multiplikation"""
        f = GanzrationaleFunktion("2x")
        assert f.term() == "2*x**1"
        assert f.koeffizienten == [0.0, 2.0]

    def test_string_konstruktor_mit_leerzeichen(self):
        """Test: String mit Leerzeichen"""
        f = GanzrationaleFunktion("x^2 + 4x - 2")
        assert f.term() == "x**2+4*x**1-2*x**0"
        assert f.koeffizienten == [-2.0, 4.0, 1.0]

    def test_liste_konstruktor(self):
        """Test: Listen-Konstruktor"""
        f = GanzrationaleFunktion([1, -4, 3])  # 1 - 4x + 3x²
        assert f.koeffizienten == [1.0, -4.0, 3.0]
        assert len(f.koeffizienten) == 3

    def test_dict_konstruktor(self):
        """Test: Dictionary-Konstruktor"""
        f = GanzrationaleFunktion({2: 1, 1: -4, 0: 3})  # x² - 4x + 3
        assert f.koeffizienten == [3.0, -4.0, 1.0]
        assert len(f.koeffizienten) == 3

    def test_dict_konstruktor_mit_luecken(self):
        """Test: Dictionary-Konstruktor mit Lücken"""
        f = GanzrationaleFunktion({3: 2, 1: -3, 0: 1})  # 2x³ - 3x + 1
        assert f.koeffizienten == [1.0, -3.0, 0.0, 2.0]
        assert len(f.koeffizienten) == 4

    def test_konstante_funktion(self):
        """Test: Konstante Funktion"""
        f = GanzrationaleFunktion("5")
        assert f.koeffizienten == [5.0]
        assert f.term() == "5*x**0"

    def test_lineare_funktion(self):
        """Test: Lineare Funktion"""
        f = GanzrationaleFunktion("x")
        assert f.koeffizienten == [0.0, 1.0]
        assert f.term() == "x**1"

    def test_null_funktion(self):
        """Test: Null-Funktion"""
        f = GanzrationaleFunktion("0")
        assert f.koeffizienten == [0.0]
        assert f.term() == "0*x**0"

    def test_ungueltige_eingabe(self):
        """Test: Ungültige Eingabe"""
        with pytest.raises(ValueError):
            GanzrationaleFunktion("ungültig")

        with pytest.raises(TypeError):
            GanzrationaleFunktion(123)  # Falscher Typ


class TestGanzrationaleFunktionMethoden:
    """Testet die Methoden der GanzrationaleFunktion"""

    def setup_method(self):
        """Setup für Test-Methoden"""
        self.f_quad = GanzrationaleFunktion("x^2-4x+3")  # (x-1)(x-3)
        self.f_linear = GanzrationaleFunktion("2x-1")
        self.f_kubisch = GanzrationaleFunktion("x^3-2x^2-5x+6")

    def test_term_method(self):
        """Test: term() Methode"""
        assert self.f_quad.term() == "x**2-4*x**1+3*x**0"

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
        assert isinstance(f_strich, GanzrationaleFunktion)
        assert f_strich.koeffizienten == [0.0, -4.0, 2.0]  # -4 + 2x

        f_doppelstrich = self.f_quad.ableitung(2)
        assert isinstance(f_doppelstrich, GanzrationaleFunktion)
        assert f_doppelstrich.koeffizienten == [0.0, 0.0, 2.0]  # 2

    def test_nullstellen_method(self):
        """Test: nullstellen() Methode"""
        # Quadratische Funktion mit zwei Nullstellen
        nullstellen = self.f_quad.nullstellen()
        assert len(nullstellen) == 2
        assert abs(nullstellen[0] - 1.0) < 1e-10
        assert abs(nullstellen[1] - 3.0) < 1e-10

        # Lineare Funktion
        nullstellen_linear = self.f_linear.nullstellen()
        assert len(nullstellen_linear) == 1
        assert abs(nullstellen_linear[0] - 0.5) < 1e-10

        # Funktion ohne reelle Nullstellen
        f_keine_null = GanzrationaleFunktion("x^2+1")
        nullstellen_keine = f_keine_null.nullstellen()
        assert len(nullstellen_keine) == 0

    def test_extremstellen_method(self):
        """Test: extremstellen() Methode"""
        extremstellen = self.f_quad.extremstellen()
        assert len(extremstellen) == 1
        assert abs(extremstellen[0][0] - 2.0) < 1e-10  # x-Koordinate
        assert extremstellen[0][1] == "Minimum"  # Art

        # Kubische Funktion
        extremstellen_kubisch = self.f_kubisch.extremstellen()
        assert len(extremstellen_kubisch) == 2  # Max und Min


class TestGanzrationaleFunktionEdgeCases:
    """Testet Edge Cases und Sonderfälle"""

    def test_hoehere_grade(self):
        """Test: Funktionen höheren Grades"""
        f = GanzrationaleFunktion("x^4-2x^3+3x^2-4x+5")
        assert len(f.koeffizienten) == 5
        assert f.koeffizienten[4] == 1.0  # x^4 Koeffizient

    def test_negative_koeffizienten(self):
        """Test: Negative Koeffizienten"""
        f = GanzrationaleFunktion("-x^2+3x-1")
        assert f.koeffizienten == [-1.0, 3.0, -1.0]

    def test_bruch_koeffizienten(self):
        """Test: Bruch-Koeffizienten"""
        f = GanzrationaleFunktion("0.5x^2-1.5x+2.5")
        assert abs(f.koeffizienten[0] - 2.5) < 1e-10
        assert abs(f.koeffizienten[1] - (-1.5)) < 1e-10
        assert abs(f.koeffizienten[2] - 0.5) < 1e-10

    def test_null_koeffizienten(self):
        """Test: Null-Koeffizienten"""
        f = GanzrationaleFunktion("x^2+0*x+1")
        assert f.koeffizienten == [1.0, 0.0, 1.0]


class TestGanzrationaleFunktionLösungswege:
    """Testet die Lösungsweg-Methoden"""

    def test_nullstellen_weg_quadratisch(self):
        """Test: nullstellen_weg() für quadratische Funktionen"""
        f = GanzrationaleFunktion("x^2-4x+3")
        weg = f.nullstellen_weg()

        assert "x^2-4x+3" in weg
        assert "Mitternachtsformel" in weg
        assert "x_1" in weg or "x_2" in weg

        # Test ohne reelle Nullstellen
        f_keine = GanzrationaleFunktion("x^2+2x+3")
        weg_keine = f_keine.nullstellen_weg()
        assert "keine reellen Nullstellen" in weg_keine.lower()

    def test_nullstellen_weg_linear(self):
        """Test: nullstellen_weg() für lineare Funktionen"""
        f = GanzrationaleFunktion("2x-1")
        weg = f.nullstellen_weg()

        assert "Lineare Funktion" in weg
        assert "x = 0.5" in weg


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
