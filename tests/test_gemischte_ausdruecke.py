"""
Tests für gemischte Polynom-Exponential-Ausdrücke.

Testet die neue Fähigkeit der API, Ausdrücke wie "(x^2-4x+5)exp(-x)"
automatisch zu erkennen und korrekt zu verarbeiten.
"""

import pytest

from schul_analysis import Funktion


class TestGemischteAusdrücke:
    """Tests für gemischte Polynom-Exponential-Ausdrücke"""

    def test_polynom_mit_exponential_faktor(self):
        """Test: (x^2-4x+5)exp(-x)"""
        f = Funktion("(x^2-4x+5)exp(-x)")

        # Sollte ExponentialRationaleFunktion sein
        assert type(f).__name__ == "ExponentialRationaleFunktion"
        assert f.funktionstyp == "exponential-rational"

        # Sollte korrekte Parameter haben
        assert f.a == -1.0

        # Sollte keine freien Parameter haben
        assert len(f.parameter) == 0

        # Term sollte korrekt dargestellt werden
        assert "e^(-x)" in f.term() or "exp(-x)" in f.term()

        # Nullstellen berechnen (sollte keine geben, da Zähler x^2-4x+5 keine positiven Nullstellen hat)
        nullstellen = f.nullstellen()
        assert len(nullstellen) == 0

    def test_exponential_ueber_polynom(self):
        """Test: exp(2x)/(x^2+1)"""
        f = Funktion("exp(2x)/(x^2+1)")

        # Sollte ExponentialRationaleFunktion sein
        assert type(f).__name__ == "ExponentialRationaleFunktion"
        assert f.funktionstyp == "exponential-rational"

        # Sollte korrekte Parameter haben
        assert f.a == 2.0

        # Term sollte korrekt dargestellt werden
        assert "e^(2*x)" in f.term() or "exp(2*x)" in f.term()

        # Nullstellen berechnen (sollte keine geben, da Zähler = 1 keine Nullstellen hat)
        nullstellen = f.nullstellen()
        assert len(nullstellen) == 0

    def test_lineares_polynom_mit_exponential(self):
        """Test: (x+1)*exp(x)"""
        f = Funktion("(x+1)*exp(x)")

        # Sollte ExponentialRationaleFunktion sein
        assert type(f).__name__ == "ExponentialRationaleFunktion"
        assert f.funktionstyp == "exponential-rational"

        # Sollte korrekte Parameter haben
        assert f.a == 1.0

        # Nullstellen berechnen (x+1 = 0 => x = -1, dann e^x = e^-1 > 0)
        nullstellen = f.nullstellen()
        assert len(nullstellen) == 1
        assert abs(nullstellen[0] - (-1.0)) < 1e-10

    def test_potenz_mit_exponential(self):
        """Test: x^2*exp(3x)"""
        f = Funktion("x^2*exp(3x)")

        # Sollte ExponentialRationaleFunktion sein
        assert type(f).__name__ == "ExponentialRationaleFunktion"
        assert f.funktionstyp == "exponential-rational"

        # Sollte korrekte Parameter haben
        assert f.a == 3.0

        # Nullstellen berechnen (x^2 = 0 => x = 0, dann e^3x = 1 > 0)
        nullstellen = f.nullstellen()
        assert len(nullstellen) == 1
        assert abs(nullstellen[0] - 0.0) < 1e-10

    def test_komplexer_gemischter_ausdruck(self):
        """Test: (x^2-1)*exp(-2x)/(x+1)"""
        f = Funktion("(x^2-1)*exp(-2x)/(x+1)")

        # Sollte ExponentialRationaleFunktion sein
        assert type(f).__name__ == "ExponentialRationaleFunktion"
        assert f.funktionstyp == "exponential-rational"

        # Sollte korrekte Parameter haben
        assert f.a == -2.0

        # Term sollte korrekt dargestellt werden
        term_str = f.term()
        assert "e^(-2*x)" in term_str or "exp(-2*x)" in term_str

    def test_exponential_mit_parameter(self):
        """Test: (a*x^2+b)*exp(x)"""
        f = Funktion("(a*x^2+b)*exp(x)")

        # Sollte ExponentialRationaleFunktion sein
        assert type(f).__name__ == "ExponentialRationaleFunktion"
        assert f.funktionstyp == "exponential-rational"

        # Sollte Parameter haben
        param_namen = [p.name for p in f.parameter]
        assert "a" in param_namen
        assert "b" in param_namen

        # Parameter spezialisieren
        f_spezial = f.spezialisiere_parameter(a=2, b=3)
        assert len(f_spezial.parameter) == 0

    def test_verschiedene_exponent_koeffizienten(self):
        """Test dass unterschiedliche Exponent-Koeffizienten Fehler erzeugen"""
        # Dieser Ausdruck hat exp(x) und exp(2x) - sollte fehlschlagen
        with pytest.raises(ValueError, match="Unterschiedliche Exponent-Koeffizienten"):
            f = Funktion("exp(x) + exp(2x)")

    def test_fehler_ohne_exponential(self):
        """Test dass Ausdrücke ohne exp() Fehler erzeugen"""
        with pytest.raises(ValueError, match="Keine exp\\(\\) Funktion"):
            f = Funktion("x^2+1")
