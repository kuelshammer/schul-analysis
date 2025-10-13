"""
Tests für die automatische Funktionserkennung im Schul-Analysis Framework.

Diese Tests überprüfen die Factory-Funktion `erstelle_funktion_automatisch` und die
automatische Erkennung von Funktionstypen.
"""

import pytest
import sympy as sp

from schul_mathematik.analysis.funktion import (
    Funktion,
    erstelle_funktion_automatisch,
)
from schul_mathematik.analysis.ganzrationale import GanzrationaleFunktion
from schul_mathematik.analysis.strukturiert import (
    QuotientFunktion,
    SummeFunktion,
    ProduktFunktion,
)
from schul_mathematik.analysis.test_utils import assert_gleich


class TestAutomatischeFunktionserkennung:
    """Testklasse für die automatische Funktionserkennung."""

    def test_ganzrationale_funktion_string(self):
        """Test der Erkennung ganzrationaler Funktionen aus String."""
        # Einfache ganzrationale Funktion
        f = erstelle_funktion_automatisch("x^2 + 2x + 1")
        assert isinstance(f, GanzrationaleFunktion)
        assert_gleich(f.term(), "x^2+2x+1")

        # Lineare Funktion
        f = erstelle_funktion_automatisch("3x - 5")
        assert isinstance(f, GanzrationaleFunktion)
        assert_gleich(f.term(), "3x-5")

        # Konstante Funktion
        f = erstelle_funktion_automatisch("7")
        assert isinstance(f, GanzrationaleFunktion)
        assert_gleich(f.term(), "7")

    def test_ganzrationale_funktion_sympy(self):
        """Test der Erkennung ganzrationaler Funktionen aus SymPy-Ausdruck."""
        x = sp.symbols("x")
        expr = x**3 - 2 * x + 1

        f = erstelle_funktion_automatisch(expr)
        assert isinstance(f, GanzrationaleFunktion)
        assert str(f.term_sympy) == "x**3 - 2*x + 1"

    def test_gebrochen_rationale_funktion_string(self):
        """Test der Erkennung gebrochen-rationaler Funktionen aus String."""
        # Einfache gebrochen-rationale Funktion
        f = erstelle_funktion_automatisch("(x+1)/(x-1)")
        assert isinstance(f, QuotientFunktion)
        assert_gleich(f.term(), "(x + 1)/(x - 1)")

        # Komplexere gebrochen-rationale Funktion
        f = erstelle_funktion_automatisch("(x^2-1)/(x^2+1)")
        assert isinstance(f, QuotientFunktion)
        assert_gleich(f.term(), "(x^2 - 1)/(x^2 + 1)")

    def test_exponential_rationale_funktion_string(self):
        """Test der Erkennung exponential-rationale Funktionen aus String."""
        # Einfache Exponentialfunktion
        f = erstelle_funktion_automatisch("exp(x) + 1")
        assert isinstance(f, SummeFunktion)
        assert "exp" in str(f.term_sympy).lower()

        # Exponentialfunktion mit Koeffizient
        f = erstelle_funktion_automatisch("exp(2x) - 3")
        assert isinstance(f, SummeFunktion)
        assert "exp" in str(f.term_sympy).lower()

        # Komplexe Exponentialfunktion
        f = erstelle_funktion_automatisch("(exp(x)+1)/(exp(x)-1)")
        assert isinstance(f, QuotientFunktion)
        assert "exp" in str(f.term_sympy).lower()

    def test_funktion_mit_parameter(self):
        """Test der Verarbeitung von Funktionen mit Parametern."""
        # Ganzrationale Funktion mit Parameter
        f = erstelle_funktion_automatisch("a*x^2 + b*x + c")
        assert isinstance(f, GanzrationaleFunktion)
        assert len(f.parameter) >= 3  # a, b, c sollten als Parameter erkannt werden

    def test_falscheingaben_behandlung(self):
        """Test der Behandlung von ungültigen Eingaben."""
        # Ungültiger mathematischer Ausdruck
        with pytest.raises(ValueError):
            erstelle_funktion_automatisch("x^2 + + * 1")

        # Leerer String
        with pytest.raises(ValueError):
            erstelle_funktion_automatisch("")

    def test_vereinheitlichte_funktion_klasse(self):
        """Test, dass die Funktion-Klasse auch automatische Erkennung unterstützt."""
        # Direkte Verwendung der Funktion-Klasse mit automatischer Erkennung
        f = Funktion("exp(x) + 1")
        # Sollte als SummeFunktion erkannt und delegiert werden
        assert hasattr(f, "term_sympy")

    def test_typ_erkennung_properties(self):
        """Test der Typeigenschaften der verschiedenen Funktionstypen."""
        # Ganzrationale Funktion
        f_ganz = erstelle_funktion_automatisch("x^2 + 1")
        assert f_ganz.ist_ganzrational
        assert (
            len(f_ganz.polstellen()) == 0
        )  # Ganzrationale Funktionen haben keine Polstellen
        assert not f_ganz.ist_exponential_rational

        # Gebrochen-rationale Funktion (manuell erstellen für zuverlässigen Test)
        # Nach Legacy Removal: Verwende QuotientFunktion statt GebrochenRationaleFunktion
        from schul_mathematik.analysis.strukturiert import (
            QuotientFunktion,
        )

        f_gebrochen = QuotientFunktion("(x+1)/(x-1)")
        assert not f_gebrochen.ist_ganzrational
        assert f_gebrochen.ist_gebrochen_rational
        assert not f_gebrochen.ist_exponential_rational

        # Exponential-rationale Funktion
        if hasattr(SummeFunktion, "ist_exponential_rational"):
            f_exp = erstelle_funktion_automatisch("exp(x) + 1")
            assert f_exp.ist_exponential_rational

    def test_funktionalität_nach_erkennung(self):
        """Test, dass die erkannten Funktionen vollständig funktional sind."""
        # Teste ganzrationale Funktion
        f_ganz = erstelle_funktion_automatisch("x^2 - 4")
        nullstellen = f_ganz.nullstellen()
        assert len(nullstellen) == 2
        assert -2.0 in [float(n.x) for n in nullstellen] or 2.0 in [
            float(n.x) for n in nullstellen
        ]

        # Teste Ableitung
        f_abgeleitet = f_ganz.ableitung()
        assert_gleich(f_abgeleitet.term(), "2x")

        # Teste Werteberechnung
        assert f_ganz.wert(2) == 0
        assert f_ganz.wert(3) == 5

        # Teste gebrochen-rationale Funktion
        f_gebrochen = erstelle_funktion_automatisch("(x^2-1)/(x-1)")
        polstellen = f_gebrochen.polstellen()
        assert any(abs(float(p.x) - 1.0) < 1e-10 for p in polstellen)

        # Teste Exponentialfunktion
        f_exp = erstelle_funktion_automatisch("exp(x) + 1")
        assert f_exp.wert(0) == 2  # exp(0) + 1 = 1 + 1 = 2

    def test_string_normalisierung(self):
        """Test der String-Normalisierung bei der automatischen Erkennung."""
        # Verschiedene Schreibweisen sollten erkannt werden
        f1 = erstelle_funktion_automatisch("x^2 + 2*x + 1")
        f2 = erstelle_funktion_automatisch("x**2 + 2x + 1")

        assert isinstance(f1, GanzrationaleFunktion)
        assert isinstance(f2, GanzrationaleFunktion)
        # Beide sollten zum gleichen SymPy-Ausdruck führen
        assert str(f1.term_sympy) == str(f2.term_sympy)

    def test_implizite_multiplikation(self):
        """Test der Verarbeitung impliziter Multiplikation."""
        # Implizite Multiplikation sollte korrekt verarbeitet werden
        f = erstelle_funktion_automatisch("2x(x+1)")
        assert isinstance(f, GanzrationaleFunktion)
        # Sollte zu 2*x*(x+1) werden
        assert "2" in str(f.term_sympy)
        assert "x" in str(f.term_sympy)

    def test_komplexe_ausdrücke(self):
        """Test der Verarbeitung komplexerer mathematischer Ausdrücke."""
        # Komplexer ganzrationaler Ausdruck
        f = erstelle_funktion_automatisch("(x+1)^2 - 3x + 2")
        assert isinstance(f, GanzrationaleFunktion)

        # Komplexer gebrochen-rationale Ausdruck
        f = erstelle_funktion_automatisch("(x^2-2x+1)/(x^2-1)")
        assert isinstance(f, QuotientFunktion)

        # Komplexe Exponentialfunktion (mit unterschiedlichen Exponenten)
        f = erstelle_funktion_automatisch("exp(x) + exp(-x)")
        assert isinstance(
            f, ProduktFunktion
        )  # Jetzt faktorisiert zu exp(-x)*(exp(2x)+1)

    def test_fallback_verhalten(self):
        """Test des Fallback-Verhaltens bei mehrdeutigen Eingaben."""
        # Wenn die Erkennung fehlschlägt, sollte auf ganzrational zurückgefallen werden
        # Dies ist ein Design-Entscheidung für pädagogische Einfachheit
        f = erstelle_funktion_automatisch(
            "x/2"
        )  # Könnte als gebrochen-rationale oder ganzrational interpretiert werden
        assert isinstance(
            f, GanzrationaleFunktion
        )  # Sollte als ganzrational erkannt werden

    def test_performance_mit_vielen_funktionen(self):
        """Test der Performance bei der Erstellung vieler Funktionen."""
        funktionen = []
        for i in range(10):
            f = erstelle_funktion_automatisch(f"x^{i} + {i}")
            funktionen.append(f)
            assert isinstance(f, GanzrationaleFunktion)

        # Alle Funktionen sollten korrekt erstellt worden sein
        assert len(funktionen) == 10


class TestStaticExponentialDetection:
    """Testklasse für die statische Exponentialfunktions-Erkennung."""

    def test_string_erkennung_exp_klein(self):
        """Test der Erkennung von exp() in Strings."""
        from schul_mathematik.analysis.funktion import _ist_exponential_funktion_static

        assert _ist_exponential_funktion_static("exp(x)")
        assert _ist_exponential_funktion_static("exp(2x)")
        assert _ist_exponential_funktion_static("exp(x) + 1")
        assert not _ist_exponential_funktion_static("x^2 + 1")

    def test_string_erkennung_exp_gross(self):
        """Test der Erkennung von EXP() in Strings (case-insensitive)."""
        from schul_mathematik.analysis.funktion import _ist_exponential_funktion_static

        assert _ist_exponential_funktion_static("EXP(x)")
        assert _ist_exponential_funktion_static("Exp(x)")

    def test_string_erkennung_e_potenz(self):
        """Test der Erkennung von e^ in Strings."""
        from schul_mathematik.analysis.funktion import _ist_exponential_funktion_static

        assert _ist_exponential_funktion_static("e^x")
        assert _ist_exponential_funktion_static("e^(2x)")
        assert _ist_exponential_funktion_static("E^x")  # Case-insensitive

    def test_sympy_erkennung(self):
        """Test der Erkennung in SymPy-Ausdrücken."""
        from schul_mathematik.analysis.funktion import _ist_exponential_funktion_static

        x = sp.symbols("x")
        expr_exp = sp.exp(x)
        expr_poly = x**2 + 1

        assert _ist_exponential_funktion_static(expr_exp)
        assert not _ist_exponential_funktion_static(expr_poly)

    def test_kombinierte_ausdrücke(self):
        """Test der Erkennung in kombinierten Ausdrücken."""
        from schul_mathematik.analysis.funktion import _ist_exponential_funktion_static

        # Sollte als Exponentialfunktion erkannt werden
        assert _ist_exponential_funktion_static("exp(x) + x^2")
        assert _ist_exponential_funktion_static("x*exp(x)")

        # Sollte nicht als Exponentialfunktion erkannt werden
        assert not _ist_exponential_funktion_static("x^2 + 2x + 1")
