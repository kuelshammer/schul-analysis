"""
Tests für die setze_parameter() Methode in der Funktion-Klasse.

Diese Tests überprüfen die neue intuitive API für parametrisierte Funktionen.
"""

import os
import sys

import pytest
import sympy as sp

# Füge src zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from schul_mathematik import Funktion
from schul_mathematik.analysis.test_utils import assert_gleich


class TestSetzeParameter:
    """Test-Klasse für die setze_parameter() Methode."""

    def test_einfache_parameter_substitution(self):
        """Teste einfache Parameter-Substitution."""
        f = Funktion("a*x^2 + b*x + c")

        # Einzelner Parameter - Nutze equals statt String-Vergleich
        f2 = f.setze_parameter(a=3)
        expected2 = Funktion("3*x**2 + b*x + c")
        assert f2.term_sympy.equals(expected2.term_sympy)

        # Mehrere Parameter
        f3 = f.setze_parameter(a=2, b=3)
        expected3 = Funktion("2*x**2 + 3*x + c")
        assert f3.term_sympy.equals(expected3.term_sympy)

        # Alle Parameter
        f4 = f.setze_parameter(a=1, b=2, c=3)
        expected4 = Funktion("x**2 + 2*x + 3")
        assert f4.term_sympy.equals(expected4.term_sympy)

    def test_kombinierte_nutzung(self):
        """Teste kombinierte Nutzung: setze_parameter() + Auswertung."""
        f = Funktion("a*x^2 + b*x + c")

        # Parameter setzen und auswerten - Ergebnis enthält noch Parameter b, c
        result = f.setze_parameter(a=2)(4)
        expected = 32 + 4 * sp.Symbol("b") + sp.Symbol("c")  # 2*16 + 4*b + c
        assert result.equals(expected)

        # Alle Parameter setzen und auswerten
        result2 = f.setze_parameter(a=2, b=3, c=1)(4)
        expected2 = 45  # 2*16 + 3*4 + 1 = 32 + 12 + 1 = 45
        assert result2 == expected2

    def test_symbolische_auswertung(self):
        """Teste symbolische Auswertung mit Parametern."""
        f = Funktion("a*x^2 + b*x + c")

        # Symbolische Auswertung ohne Parameter-Substitution
        result = f(4)
        # Sollte 16*a + 4*b + c ergeben
        assert result == 16 * sp.Symbol("a") + 4 * sp.Symbol("b") + sp.Symbol("c")

        # Teilweise Substitution in __call__
        result2 = f(4, a=2)
        # Sollte 32 + 4*b + c ergeben
        assert result2 == 32 + 4 * sp.Symbol("b") + sp.Symbol("c")

    def test_fehlerbehandlung_ungueltige_parameter(self):
        """Teste Fehlerbehandlung bei ungültigen Parametern."""
        f = Funktion("a*x^2 + b*x + c")

        # Ungültiger Parameter
        with pytest.raises(
            ValueError, match="Parameter 'x' kommt in der Funktion nicht vor"
        ):
            f.setze_parameter(x=5)

        with pytest.raises(
            ValueError, match="Parameter 'd' kommt in der Funktion nicht vor"
        ):
            f.setze_parameter(d=10)

    def test_fehlerbeteilung_keine_parameter(self):
        """Teste Fehlerbehandlung bei Funktionen ohne Parameter."""
        f = Funktion("x^2 + 2*x + 1")

        with pytest.raises(ValueError, match="hat keine Parameter"):
            f.setze_parameter(a=3)

    def test_quotienten_funktion(self):
        """Teste setze_parameter() mit Quotienten-Funktionen."""
        g = Funktion("(a*x + 1)/(x^2 - b)")

        # Parameter im Zähler setzen
        g2 = g.setze_parameter(a=3)
        assert_gleich(g2.term(), "(3*x + 1)/(x**2 - b)")

        # Parameter im Nenner setzen
        g3 = g.setze_parameter(b=4)
        assert_gleich(g3.term(), "(a*x + 1)/(x**2 - 4)")

        # Beide Parameter setzen
        g4 = g.setze_parameter(a=3, b=4)
        assert_gleich(g4.term(), "(3*x + 1)/(x**2 - 4)")

    def test_produkt_funktion(self):
        """Teste setze_parameter() mit Produkt-Funktionen."""
        h = Funktion("sin(a*x) * exp(b*x)")

        # Parameter in trigonometrischer Komponente
        h2 = h.setze_parameter(a=2)
        assert "sin(2*x)" in str(h2.term())

        # Parameter in exponentieller Komponente
        h3 = h.setze_parameter(b=1)
        assert "exp(x)" in str(h3.term())

        # Beide Parameter
        h4 = h.setze_parameter(a=2, b=1)
        assert "sin(2*x)" in str(h4.term()) and "exp(x)" in str(h4.term())

    def test_teilweise_substitution(self):
        """Teste teilweise Parameter-Substitution."""
        f = Funktion("a*x^2 + b*x + c")

        # Nur a setzen
        f_a = f.setze_parameter(a=3)
        assert_gleich(f_a.term(), "3*x**2 + b*x + c")
        assert f_a.parameter == [
            sp.Symbol("b"),
            sp.Symbol("c"),
        ]  # b und c bleiben Parameter

        # Nur b setzen
        f_b = f.setze_parameter(b=2)
        assert_gleich(f_b.term(), "a*x**2 + 2*x + c")
        assert f_b.parameter == [
            sp.Symbol("a"),
            sp.Symbol("c"),
        ]  # a und c bleiben Parameter

    def test_wert_methode_mit_parametern(self):
        """Teste die wert() Methode mit Parametern."""
        f = Funktion("a*x^2 + b*x + c")

        # Symbolisches Ergebnis
        result = f.wert(4)
        assert result == 16 * sp.Symbol("a") + 4 * sp.Symbol("b") + sp.Symbol("c")

        # Nach Parameter-Substitution
        f2 = f.setze_parameter(a=2)
        result2 = f2.wert(4)
        assert result2 == 32 + 4 * sp.Symbol("b") + sp.Symbol("c")

        # Vollständig substituiert
        f3 = f.setze_parameter(a=2, b=3, c=1)
        result3 = f3.wert(4)
        assert result3 == 45

    def test_parametererkennung(self):
        """Teste, ob Parameter korrekt erkannt werden."""
        f = Funktion("a*x^2 + b*x + c")

        # Prüfe, ob die richtigen Parameter erkannt wurden
        parameter_namen = [str(p) for p in f.parameter]
        assert "a" in parameter_namen
        assert "b" in parameter_namen
        assert "c" in parameter_namen
        assert "x" not in parameter_namen  # x ist Variable, nicht Parameter

    def test_komplexe_parameter_funktion(self):
        """Teste mit einer komplexeren parametrisierten Funktion."""
        k = Funktion("(a*x + b)/(c*x + d)")

        # Teilweise Substitution
        k2 = k.setze_parameter(a=2, b=3)
        assert_gleich(k2.term(), "(2*x + 3)/(c*x + d)")

        # Alle Parameter setzen
        k3 = k.setze_parameter(a=2, b=3, c=1, d=4)
        assert_gleich(k3.term(), "(2*x + 3)/(x + 4)")

        # Auswertung testen
        result = k3.setze_parameter(a=2, b=3, c=1, d=4)(2)
        expected = (2 * 2 + 3) / (2 + 4)  # 7/6
        assert result == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
