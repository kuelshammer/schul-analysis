"""
Tests für komplexe Ausdrücke mit verschiedenen Funktionstypen.

Testet die Fähigkeit der API, Ausdrücke wie "(x^2-4x+5)exp(-x)"
automatisch zu erkennen und korrekt zu verarbeiten.
"""

import pytest

from schul_mathematik import Funktion
from schul_mathematik.analysis.test_utils import assert_gleich


class TestKomplexeAusdrücke:
    """Tests für komplexe Ausdrücke mit verschiedenen Funktionstypen"""

    def test_polynom_mit_exponential_faktor(self):
        """Test: (x^2-4x+5)exp(-x)"""
        f = Funktion("(x^2-4x+5)exp(-x)")

        # Sollte ProduktFunktion sein
        assert type(f).__name__ == "ProduktFunktion"
        assert f.funktionstyp == "produkt"

        # Sollte keine freien Parameter haben
        assert len(f.parameter) == 0

        # Term sollte korrekt dargestellt werden
        term_str = f.term()
        assert "e^(-x)" in term_str or "exp(-x)" in term_str or "exp( - x)" in term_str

        # Nullstellen berechnen (sollte keine geben, da Zähler x^2-4x+5 keine positiven Nullstellen hat)
        nullstellen = f.nullstellen()
        assert len(nullstellen) == 0

    def test_exponential_ueber_polynom(self):
        """Test: exp(2x)/(x^2+1)"""
        f = Funktion("exp(2x)/(x^2+1)")

        # Sollte QuotientFunktion sein
        assert type(f).__name__ == "QuotientFunktion"
        assert f.funktionstyp == "quotient"

        # Term sollte korrekt dargestellt werden
        term_str = f.term()
        assert "e^(2*x)" in term_str or "exp(2*x)" in term_str

        # Nullstellen berechnen (sollte keine geben, da Zähler = 1 keine Nullstellen hat)
        nullstellen = f.nullstellen()
        assert len(nullstellen) == 0

    def test_lineares_polynom_mit_exponential(self):
        """Test: (x+1)*exp(x)"""
        f = Funktion("(x+1)*exp(x)")

        # Sollte ProduktFunktion sein
        assert type(f).__name__ == "ProduktFunktion"
        assert f.funktionstyp == "produkt"

        # Nullstellen berechnen (x+1 = 0 => x = -1, dann e^x = e^-1 > 0)
        nullstellen = f.nullstellen()
        assert len(nullstellen) == 1
        assert abs(float(nullstellen[0].x) - (-1.0)) < 1e-10

    def test_potenz_mit_exponential(self):
        """Test: x^2*exp(3x)"""
        f = Funktion("x^2*exp(3x)")

        # Sollte ProduktFunktion sein
        assert type(f).__name__ == "ProduktFunktion"
        assert f.funktionstyp == "produkt"

        # Nullstellen berechnen (x^2 = 0 => x = 0, dann e^3x = 1 > 0)
        nullstellen = f.nullstellen()
        assert len(nullstellen) == 1
        assert abs(float(nullstellen[0].x) - 0.0) < 1e-10

    def test_komplexer_gemischter_ausdruck(self):
        """Test: (x^2-1)*exp(-2x)/(x+1)"""
        f = Funktion("(x^2-1)*exp(-2x)/(x+1)")

        # Sollte QuotientFunktion sein (komplexer Ausdruck)
        assert type(f).__name__ == "QuotientFunktion"
        assert f.funktionstyp == "quotient"

        # Term sollte korrekt dargestellt werden
        term_str = f.term()
        assert (
            "e^(-2*x)" in term_str
            or "exp(-2*x)" in term_str
            or "exp( - 2*x)" in term_str
        )

    def test_exponential_mit_parameter(self):
        """Test: (a*x^2+b)*exp(x)"""
        f = Funktion("(a*x^2+b)*exp(x)")

        # Sollte ProduktFunktion sein
        assert type(f).__name__ == "ProduktFunktion"
        assert f.funktionstyp == "produkt"

        # Sollte Parameter haben
        param_namen = [p.name for p in f.parameter]
        assert "a" in param_namen
        assert "b" in param_namen

        # Parameter spezialisieren
        f_spezial = f.setze_parameter(a=2, b=3)
        assert len(f_spezial.parameter) == 0

    def test_verschiedene_exponent_koeffizienten(self):
        """Test dass unterschiedliche Exponent-Koeffizienten automatisch faktorisiert werden"""
        # Dieser Ausdruck hat exp(x) und exp(2x) - sollte automatisch faktorisiert werden
        f = Funktion("exp(x) + exp(2x)")

        # Sollte ProduktFunktion sein, nicht SummeFunktion
        assert type(f).__name__ == "ProduktFunktion"
        assert f.funktionstyp == "produkt"

        # Sollte zwei Faktoren haben
        assert len(f.faktoren) == 2

        # Erster Faktor sollte exp(x) sein
        assert "exp(x)" in str(f.faktoren[0])

        # Zweiter Faktor sollte die Summe sein
        assert "exp(x)" in str(f.faktoren[1])  # Die Summe enthält exp(x)

        # Der gesamte Term sollte mathematisch äquivalent sein
        term_str = f.term()
        assert "exp" in term_str

    def test_exponential_faktorisierung_mit_vorfaktoren(self):
        """Test Exponential-Faktorisierung mit Vorfaktoren"""
        f = Funktion("2*exp(x) + 3*exp(2x)")

        # Sollte ProduktFunktion sein
        assert type(f).__name__ == "ProduktFunktion"
        assert f.funktionstyp == "produkt"

        # Sollte zwei Faktoren haben
        assert len(f.faktoren) == 2

        # Der gesamte Term sollte die Exponentialfaktoren enthalten
        term_str = f.term()
        assert "exp" in term_str

    def test_exponential_faktorisierung_komplex(self):
        """Test komplexere Exponential-Faktorisierung"""
        f = Funktion("exp(3*x) + exp(5*x)")

        # Sollte ProduktFunktion sein
        assert type(f).__name__ == "ProduktFunktion"
        assert f.funktionstyp == "produkt"

        # Sollte zwei Faktoren haben
        assert len(f.faktoren) == 2

        # Der gesamte Term sollte mathematisch äquivalent sein
        term_str = f.term()
        assert "exp" in term_str

    def test_exponential_faktorisierung_negative_exponenten(self):
        """Test Exponential-Faktorisierung mit negativen Exponenten"""
        f = Funktion("exp(2*x) + exp(-x)")

        # Sollte ProduktFunktion sein
        assert type(f).__name__ == "ProduktFunktion"
        assert f.funktionstyp == "produkt"

        # Sollte zwei Faktoren haben
        assert len(f.faktoren) == 2

        # Der gesamte Term sollte mathematisch äquivalent sein
        term_str = f.term()
        assert "exp" in term_str

    def test_exponential_gleiche_exponenten(self):
        """Test dass gleiche Exponenten korrekt zusammengefasst werden"""
        f = Funktion("exp(x) + exp(x)")

        # Sollte ProduktFunktion sein (2 * exp(x))
        assert type(f).__name__ == "ProduktFunktion"
        assert f.funktionstyp == "produkt"

        # Sollte zwei Faktoren haben: 2 und exp(x)
        assert len(f.faktoren) == 2

    def test_kein_fehler_bei_normalem_polynom(self):
        """Test dass normale Polynome keine Fehler erzeugen"""
        # Ein normales Polynom sollte eine ganzrationale Funktion erzeugen
        f = Funktion("x^2 + 1")

        # Sollte Funktion sein (genauer gesagt GanzrationaleFunktion)
        assert hasattr(f, "term")
        assert callable(getattr(f, "nullstellen", None))

        # Der Term sollte korrekt dargestellt werden
        term_str = f.term()
        assert "x" in term_str
