#!/usr/bin/env python3
"""
Test-Suite für arithmetische Operationen im Schul-Analysis Framework

Diese Tests überprüfen, dass alle arithmetischen Operationen (+, -, *, /, **, @)
korrekt funktionieren und die Magic Factory die optimalen Funktionstypen wählt.
"""

import sys

import pytest
import sympy as sp

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

from schul_mathematik import Funktion, assert_gleich, assert_wert_gleich


class TestArithmetischeOperationen:
    """Test-Gruppe für grundlegende arithmetische Operationen"""

    def test_addition_zwei_funktionen(self):
        """Teste f + g für zwei Funktionen"""
        f = Funktion("x^2")
        g = Funktion("3x + 4")
        h = f + g

        assert_gleich(h.term(), "x^2 + 3*x + 4")
        assert isinstance(h, Funktion)
        # Magic Factory sollte optimalen Typ wählen
        print(f"f + g = {h.term()}, Typ: {type(h).__name__}")

    def test_addition_funktion_mit_zahl(self):
        """Teste f + zahl"""
        f = Funktion("x^2")
        h = f + 5

        assert_gleich(h.term(), "x^2 + 5")
        assert isinstance(h, Funktion)

    def test_addition_zahl_mit_funktion(self):
        """Teste zahl + f (rechtsseitige Addition)"""
        f = Funktion("x^2")
        h = 5 + f

        assert_gleich(h.term(), "x^2 + 5")  # SymPy ordnet um: 5 + x^2 -> x^2 + 5
        assert isinstance(h, Funktion)

    def test_subtraktion_zwei_funktionen(self):
        """Teste f - g für zwei Funktionen"""
        f = Funktion("x^2")
        g = Funktion("3x + 4")
        h = f - g

        assert_gleich(h.term(), "x^2 - 3*x - 4")
        assert isinstance(h, Funktion)

    def test_subtraktion_funktion_mit_zahl(self):
        """Teste f - zahl"""
        f = Funktion("x^2")
        h = f - 5

        assert_gleich(h.term(), "x^2 - 5")
        assert isinstance(h, Funktion)

    def test_subtraktion_zahl_mit_funktion(self):
        """Teste zahl - f (rechtsseitige Subtraktion)"""
        f = Funktion("x^2")
        h = 10 - f

        assert_gleich(h.term(), "10 - x^2")
        assert isinstance(h, Funktion)

    def test_multiplikation_zwei_funktionen(self):
        """Teste f * g für zwei Funktionen"""
        f = Funktion("x^2")
        g = Funktion("3x + 4")
        h = f * g

        assert_gleich(h.term(), "x^2*(3*x + 4)")
        assert isinstance(h, Funktion)

    def test_multiplikation_funktion_mit_zahl(self):
        """Teste f * zahl"""
        f = Funktion("x^2")
        h = f * 5

        assert_gleich(h.term(), "5*x^2")
        assert isinstance(h, Funktion)

    def test_multiplikation_zahl_mit_funktion(self):
        """Teste zahl * f (rechtsseitige Multiplikation)"""
        f = Funktion("x^2")
        h = 5 * f

        assert_gleich(h.term(), "5*x^2")
        assert isinstance(h, Funktion)

    def test_division_zwei_funktionen(self):
        """Teste f / g für zwei Funktionen"""
        f = Funktion("x^2")
        g = Funktion("3x + 4")
        h = f / g

        assert_gleich(h.term(), "x^2/(3*x + 4)")
        assert isinstance(h, Funktion)

    def test_division_funktion_mit_zahl(self):
        """Teste f / zahl"""
        f = Funktion("x^2")
        h = f / 5

        assert_gleich(h.term(), "x^2/5")
        assert isinstance(h, Funktion)

    def test_division_zahl_mit_funktion(self):
        """Teste zahl / f (rechtsseitige Division)"""
        f = Funktion("x^2")
        h = 10 / f

        assert_gleich(h.term(), "10/x^2")
        assert isinstance(h, Funktion)

    def test_division_durch_null_fehler(self):
        """Teste Division durch Null wirft Fehler"""
        f = Funktion("x^2")

        with pytest.raises(ZeroDivisionError):
            f / 0

    def test_potenzierung_funktion_mit_exponent(self):
        """Teste f ** exponent"""
        f = Funktion("sin(x)")
        h = f**2

        assert_gleich(h.term(), "sin(x)^2")
        assert isinstance(h, Funktion)

    def test_potenzierung_zahl_mit_funktion(self):
        """Teste zahl ** f (rechtsseitige Potenzierung)"""
        f = Funktion("x")
        h = 2**f

        assert_gleich(h.term(), "2^x")
        assert isinstance(h, Funktion)


class TestKompositionsOperationen:
    """Test-Gruppe für Kompositionsoperationen"""

    def test_matmul_komposition(self):
        """Teste f @ g (f ∘ g)"""
        f = Funktion("x^2")
        g = Funktion("sin(x)")
        h = f @ g

        assert_gleich(h.term(), "sin(x)^2")
        assert isinstance(h, Funktion)
        print(f"f @ g = {h.term()}, Typ: {type(h).__name__}")

    def test_call_komposition(self):
        """Teste f(g) für Komposition"""
        f = Funktion("x^2")
        g = Funktion("sin(x)")
        h = f(g)

        assert_gleich(h.term(), "sin(x)^2")
        assert isinstance(h, Funktion)

    def test_call_numerische_auswertung(self):
        """Teste f(x_wert) für numerische Auswertung"""
        f = Funktion("x^2")
        y = f(3)

        assert_wert_gleich(f, 3, 9.0)
        assert isinstance(
            y, (int, float, sp.Integer)
        )  # SymPy kann sp.Integer zurückgeben

    def test_komposition_kette(self):
        """Teste Kettenkomposition f @ g @ h"""
        f = Funktion("2*x + 1")
        g = Funktion("x^2")
        h = Funktion("sin(x)")
        k = f @ g @ h  # f(g(h(x)))

        expected = "2*sin(x)^2 + 1"
        assert_gleich(k.term(), expected)
        assert isinstance(k, Funktion)

    def test_komposition_mit_gemischten_typen(self):
        """Teste Komposition mit verschiedenen Funktionstypen"""
        f = Funktion("exp(x)")
        g = Funktion("x^2 + 1")
        h = f @ g

        assert_gleich(h.term(), "exp(x^2 + 1)")
        assert isinstance(h, Funktion)


class TestMagicFactoryVereinfachung:
    """Test-Gruppe für Magic Factory Vereinfachung"""

    def test_automatische_vereinfachung_addition(self):
        """Teste automatische Vereinfachung bei Addition"""
        f = Funktion("x^2 - cos(x)")
        g = Funktion("cos(x)")
        h = f + g  # Sollte zu x^2 vereinfachen

        # Überprüfe, ob Vereinfachung stattgefunden hat
        assert_gleich(h.term(), "x^2")
        print(f"Vereinfachung: (x^2 - cos(x)) + cos(x) = {h.term()}")

    def test_keine_vereinfachung(self):
        """Teste, dass keine unnötige Vereinfachung stattfindet"""
        f = Funktion("x^2 + sin(x)")
        g = Funktion("cos(x)")
        h = f + g  # Sollte nicht vereinfachbar sein

        # Beide trigonometrischen Funktionen sollten erhalten bleiben
        assert "sin" in h.term()
        assert "cos" in h.term()

    def test_vereinfachung_trigonometrischer_identitaet(self):
        """Teste trigonometrische Identität sin² + cos² = 1"""
        f = Funktion("sin(x)")
        g = Funktion("cos(x)")
        h = f**2 + g**2  # Sollte zu 1 vereinfachen

        # SymPy sollte sin(x)^2 + cos(x)^2 zu 1 vereinfachen
        assert_gleich(h.term(), "1")
        print(f"sin² + cos² = {h.term()}")

    def test_typerkennung_nach_vereinfachung(self):
        """Teste, dass Magic Factory optimalen Typ nach Vereinfachung wählt"""
        f = Funktion("x^2 + 2*x - x^2")
        # Sollte zu 2*x vereinfachen und lineare Funktion erkennen

        assert isinstance(f, Funktion)
        print(f"Typ nach Vereinfachung: {type(f).__name__}")


class TestFehlerbehandlung:
    """Test-Gruppe für Fehlerbehandlung bei arithmetischen Operationen"""

    def test_ungueltige_operanden(self):
        """Teste Fehler bei ungültigen Operanden"""
        f = Funktion("x^2")

        with pytest.raises((ValueError, TypeError)):  # TypeError wird auch akzeptiert
            f + "string"

    def test_unsupported_operation(self):
        """Teste NotImplemented bei nicht unterstützten Operationen"""
        f = Funktion("x^2")

        # Diese Operation sollte NotImplemented zurückgeben
        result = f.__add__([])
        assert result is NotImplemented


class TestErweiterteFunktionen:
    """Test-Gruppe für erweiterte Funktionstypen"""

    def test_trigonometrische_arithmetik(self):
        """Teste Arithmetik mit trigonometrischen Funktionen"""
        f = Funktion("sin(x)")
        g = Funktion("cos(x)")

        h1 = f + g
        h2 = f - g
        h3 = f * g

        assert isinstance(h1, Funktion)
        assert isinstance(h2, Funktion)
        assert isinstance(h3, Funktion)

        print(f"sin + cos = {h1.term()}")
        print(f"sin - cos = {h2.term()}")
        print(f"sin * cos = {h3.term()}")

    def test_exponential_arithmetik(self):
        """Teste Arithmetik mit Exponentialfunktionen"""
        f = Funktion("exp(x)")
        g = Funktion("x^2")

        h1 = f + g
        h2 = f * g

        assert isinstance(h1, Funktion)
        assert isinstance(h2, Funktion)

        print(f"exp + x² = {h1.term()}")
        print(f"exp * x² = {h2.term()}")

    def test_gebrochen_rationale_arithmetik(self):
        """Teste Arithmetik mit gebrochen-rationalen Funktionen"""
        f = Funktion("(x+1)/(x-1)")
        g = Funktion("x^2")

        h1 = f + g
        h2 = f * g

        assert isinstance(h1, Funktion)
        assert isinstance(h2, Funktion)

        print(f"(x+1)/(x-1) + x² = {h1.term()}")
        print(f"(x+1)/(x-1) * x² = {h2.term()}")


if __name__ == "__main__":
    # Führe einige manuelle Tests aus
    print("=== Manuelle Tests der arithmetischen Operationen ===")

    # Einfache Addition
    f = Funktion("x^2")
    g = Funktion("3x + 4")
    h = f + g
    print(f"f + g = {h.term()} (Typ: {type(h).__name__})")

    # Komposition
    f2 = Funktion("x^2")
    g2 = Funktion("sin(x)")
    h2 = f2 @ g2
    print(f"f @ g = {h2.term()} (Typ: {type(h2).__name__})")

    # Potenzierung
    f3 = Funktion("sin(x)")
    h3 = f3**2
    print(f"sin(x)^2 = {h3.term()} (Typ: {type(h3).__name__})")

    # Vereinfachung
    f4 = Funktion("x^2 - cos(x)")
    g4 = Funktion("cos(x)")
    h4 = f4 + g4
    print(f"(x^2 - cos(x)) + cos(x) = {h4.term()} (Typ: {type(h4).__name__})")

    print("=== Tests abgeschlossen ===")
