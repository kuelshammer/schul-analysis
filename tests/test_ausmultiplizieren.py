"""
Tests für die Ausmultiplizieren-Funktionalität.

Diese Tests überprüfen, dass die Ausmultiplizieren-Funktion korrekt arbeitet
und verschiedene Arten von Ausdrücken korrekt expandiert.
"""

import pytest
import sympy as sp
import sys
import os

# Füge src zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from schul_analysis import Funktion, Ausmultiplizieren
from schul_analysis.test_utils import assert_gleich


class TestAusmultiplizierenGrundlagen:
    """Testet grundlegende Ausmultiplizieren-Funktionalität"""

    def test_einfache_binome(self):
        """Test: Ausmultiplizieren von einfachen Binomen"""
        # (x+1)(x-2) -> x² - x - 2
        f = Funktion("(x+1)(x-2)")
        # Term kann in anderer Reihenfolge sein, also prüfe mathematische Äquivalenz
        assert_gleich(f.term_sympy, sp.sympify("(x + 1)*(x - 2)"))

        # Wrapper-Funktion test
        f_expanded = Ausmultiplizieren(f)
        assert_gleich(f_expanded.term_sympy, sp.sympify("x**2 - x - 2"))

        # Original sollte unverändert sein
        assert_gleich(f.term_sympy, sp.sympify("(x + 1)*(x - 2)"))

    def test_method_aufruf(self):
        """Test: Direkter Methodenaufruf am Objekt"""
        # (x+1)(x-2) -> x² - x - 2
        f = Funktion("(x+1)(x-2)")
        original_term_sympy = f.term_sympy

        # In-place Änderung
        result = f.ausmultiplizieren()
        assert result is f  # Sollte self zurückgeben
        assert_gleich(f.term_sympy, sp.sympify("x**2 - x - 2"))
        # Term sollte sich strukturell geändert haben (nicht mathematisch gleich)
        assert f.term_sympy != original_term_sympy  # Strukturelle Ungleichheit
        assert str(f.term_sympy) != str(
            original_term_sympy
        )  # String-Darstellung unterschiedlich

    def test_potenzen_ausmultiplizieren(self):
        """Test: Ausmultiplizieren von Potenzen"""
        # (x+1)² -> x² + 2x + 1
        f = Funktion("(x+1)^2")
        f_expanded = Ausmultiplizieren(f)
        assert_gleich(f_expanded.term_sympy, sp.sympify("x**2 + 2*x + 1"))

        # (x+1)³ -> x³ + 3x² + 3x + 1
        g = Funktion("(x+1)^3")
        g_expanded = Ausmultiplizieren(g)
        assert_gleich(g_expanded.term_sympy, sp.sympify("x**3 + 3*x**2 + 3*x + 1"))

    def test_dreifaches_produkt(self):
        """Test: Ausmultiplizieren von drei Faktoren"""
        # (x-1)(x+2)(x-3) -> x³ - 2x² - 5x + 6
        f = Funktion("(x-1)(x+2)(x-3)")
        f_expanded = Ausmultiplizieren(f)
        assert_gleich(f_expanded.term_sympy, sp.sympify("x**3 - 2*x**2 - 5*x + 6"))

    def test_konstante_faktoren(self):
        """Test: Ausmultiplizieren mit konstanten Faktoren"""
        # 2(x+1)(x-2) -> 2x² - 2x - 4
        f = Funktion("2(x+1)(x-2)")
        f_expanded = Ausmultiplizieren(f)
        assert_gleich(f_expanded.term_sympy, sp.sympify("2*x**2 - 2*x - 4"))


class TestAusmultiplizierenKomplex:
    """Testet komplexere Ausmultiplizieren-Szenarien"""

    def test_mehrfache_variablen(self):
        """Test: Ausmultiplizieren mit mehreren Variablen"""
        # (x+y)(x-y) -> x² - y²
        f = Funktion("(x+y)(x-y)")
        f_expanded = Ausmultiplizieren(f)
        assert_gleich(f_expanded.term_sympy, sp.sympify("x**2 - y**2"))

    def test_gemischte_ausdruecke(self):
        """Test: Ausmultiplizieren von gemischten Ausdrücken"""
        # (x+1)(x² + 2x + 1) -> x³ + 3x² + 3x + 1
        f = Funktion("(x+1)(x^2 + 2x + 1)")
        f_expanded = Ausmultiplizieren(f)
        assert_gleich(f_expanded.term_sympy, sp.sympify("x**3 + 3*x**2 + 3*x + 1"))

    def test_trinomische_ausdruecke(self):
        """Test: Ausmultiplizieren von trinomischen Ausdrücken"""
        # (x+y+z)² -> x² + y² + z² + 2xy + 2xz + 2yz
        f = Funktion("(x+y+z)^2")
        f_expanded = Ausmultiplizieren(f)
        expected = sp.sympify("x**2 + y**2 + z**2 + 2*x*y + 2*x*z + 2*y*z")
        assert_gleich(f_expanded.term_sympy, expected)


class TestAusmultiplizierenSpezialfaelle:
    """Testet spezielle Fälle und Randbedingungen"""

    def test_bereits_expandierter_ausdruck(self):
        """Test: Bereits expandierter Ausdruck sollte unverändert bleiben"""
        f = Funktion("x^2 + 2x + 1")
        f_expanded = Ausmultiplizieren(f)
        assert_gleich(f_expanded.term_sympy, sp.sympify("x**2 + 2*x + 1"))

    def test_einfache_terme(self):
        """Test: Einfache Terme sollten unverändert bleiben"""
        # Linearer Term
        f = Funktion("2x + 3")
        f_expanded = Ausmultiplizieren(f)
        assert_gleich(f_expanded.term_sympy, sp.sympify("2*x + 3"))

        # Konstanter Term
        g = Funktion("5")
        g_expanded = Ausmultiplizieren(g)
        assert_gleich(g_expanded.term_sympy, sp.sympify("5"))

    def test_exponentialschreibweise(self):
        """Test: Verschiedene Schreibweisen von Exponenten"""
        # (x+1)**2 sollte funktionieren
        f = Funktion("(x+1)**2")
        f_expanded = Ausmultiplizieren(f)
        assert_gleich(f_expanded.term_sympy, sp.sympify("x**2 + 2*x + 1"))

    def test_nullfunktion(self):
        """Test: Nullfunktion"""
        f = Funktion("0")
        f_expanded = Ausmultiplizieren(f)
        assert_gleich(f_expanded.term_sympy, sp.sympify("0"))


class TestAusmultiplizierenFunktionseigenschaften:
    """Testet, dass nach dem Ausmultiplizieren die Funktionseigenschaften erhalten bleiben"""

    def test_funktionstyp_erhalten(self):
        """Test: Funktionstyp sollte erhalten bleiben"""
        f = Funktion("(x+1)(x-2)")
        original_type = type(f)

        f_expanded = Ausmultiplizieren(f)
        assert type(f_expanded) == original_type

    def test_werteberechnung_erhalten(self):
        """Test: Werteberechnung sollte nach dem Ausmultiplizieren gleich bleiben"""
        f = Funktion("(x+1)(x-2)")

        # Werte vor dem Ausmultiplizieren
        werte_original = [f.wert(x) for x in [0, 1, 2, 3]]

        # Ausmultiplizieren und Werte vergleichen
        f_expanded = Ausmultiplizieren(f)
        werte_expandiert = [f_expanded.wert(x) for x in [0, 1, 2, 3]]

        for w1, w2 in zip(werte_original, werte_expandiert):
            assert abs(float(w1) - float(w2)) < 1e-10

    def test_ableitung_erhalten(self):
        """Test: Ableitung sollte nach dem Ausmultiplizieren gleich sein"""
        f = Funktion("(x+1)(x-2)")

        # Ableitung vor dem Ausmultiplizieren
        f1 = f.ableitung()

        # Ausmultiplizieren und ableiten
        f_expanded = Ausmultiplizieren(f)
        f_expanded_1 = f_expanded.ableitung()

        # Die Ableitungen sollten äquivalent sein
        assert_gleich(f1.term_sympy.simplify(), f_expanded_1.term_sympy.simplify())

    def test_nullstellen_erhalten(self):
        """Test: Nullstellen sollten nach dem Ausmultiplizieren gleich bleiben"""
        f = Funktion("(x+1)(x-2)")

        # Nullstellen vor dem Ausmultiplizieren
        nullstellen_original = f.nullstellen

        # Ausmultiplizieren und Nullstellen vergleichen
        f_expanded = Ausmultiplizieren(f)
        nullstellen_expandiert = f_expanded.nullstellen

        # Nullstellen sollten gleich sein (eventuell in anderer Reihenfolge)
        assert set(nullstellen_original) == set(nullstellen_expandiert)


class TestAusmultiplizierenIntegration:
    """Testet Integration mit anderen Framework-Funktionen"""

    def test_ausmultiplizieren_nach_arithmetik(self):
        """Test: Ausmultiplizieren nach arithmetischen Operationen"""
        f = Funktion("x+1")
        g = Funktion("x-2")
        h = f * g  # Sollte (x+1)(x-2) ergeben

        # Jetzt ausmultiplizieren
        h_expanded = Ausmultiplizieren(h)
        assert_gleich(h_expanded.term_sympy, sp.sympify("x**2 - x - 2"))

    def test_ausmultiplizieren_vor_ableitung(self):
        """Test: Ausmultiplizieren vor der Ableitung"""
        f = Funktion("(x+1)^3")

        # Methode 1: Direkt ableiten
        f1 = f.ableitung()

        # Methode 2: Zuerst ausmultiplizieren, dann ableiten
        f_expanded = Ausmultiplizieren(f)
        f_expanded_1 = f_expanded.ableitung()

        # Beide Ableitungen sollten äquivalent sein
        assert_gleich(f1.term_sympy.simplify(), f_expanded_1.term_sympy.simplify())

    def test_latex_darstellung(self):
        """Test: LaTeX-Darstellung nach dem Ausmultiplizieren"""
        f = Funktion("(x+1)(x-2)")
        f_expanded = Ausmultiplizieren(f)

        # LaTeX sollte die expandierte Form zeigen
        latex = f_expanded.term_latex()
        assert "x^{2}" in latex  # Sollte x² enthalten
        assert "x" in latex  # Sollte x enthalten


class TestAusmultiplizierenFehlerbehandlung:
    """Testet Fehlerbehandlung bei ungültigen Eingaben"""

    def test_ungueltige_funktion(self):
        """Test: Ungültige Funktion sollte Fehler werfen"""
        # Dies sollte durch die Typenprüfung im Konstruktor abgefangen werden
        with pytest.raises((ValueError, TypeError)):
            # Ungültiger mathematischer Ausdruck
            f = Funktion("x++y")
            Ausmultiplizieren(f)

    def test_division_durch_null_erhalten(self):
        """Test: Division durch Null sollte erhalten bleiben"""
        f = Funktion("1/x")
        f_expanded = Ausmultiplizieren(f)

        # Sollte immer noch 1/x sein (nicht ausmultiplizierbar)
        assert_gleich(f_expanded.term_sympy, sp.sympify("1/x"))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
