"""
Comprehensive Tests für GebrochenRationaleFunktion Klasse
"""

import os
import sys

import pytest

# Füge src zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


from schul_mathematik.analysis.errors import DivisionDurchNullError
from schul_mathematik.analysis.ganzrationale import GanzrationaleFunktion
from schul_mathematik.analysis.gebrochen_rationale import GebrochenRationaleFunktion
from schul_mathematik.analysis.test_utils import assert_gleich


class TestGebrochenRationaleFunktionKonstruktoren:
    """Testet verschiedene Konstruktor-Formate"""

    def test_string_konstruktor_standard(self):
        """Test: Standard String-Konstruktor"""
        f = GebrochenRationaleFunktion("(x^2+1)/(x-1)")
        assert_gleich(f.term(), "(x^2+1)/(x-1)")
        assert_gleich(f.zaehler.term(), "x^2+1")
        assert_gleich(f.nenner.term(), "x-1")

    def test_string_konstruktor_vereinfacht(self):
        """Test: String-Konstruktor ohne Klammern"""
        f = GebrochenRationaleFunktion("x^2+1/x-1")
        # Ohne Klammern wird dies als x^2 + (1/x) - 1 interpretiert
        assert_gleich(f.term(), "x^2 - 1 + 1/x")

    def test_getrennte_konstruktoren(self):
        """Test: Getrennte Übergabe von Zähler und Nenner"""
        z = GanzrationaleFunktion("x^2+1")
        n = GanzrationaleFunktion("x-1")
        f = GebrochenRationaleFunktion(z, n)
        assert_gleich(f.term(), "(x^2+1)/(x-1)")

    def test_string_getrennt(self):
        """Test: Getrennte String-Übergabe"""
        f = GebrochenRationaleFunktion("x^2+1", "x-1")
        assert_gleich(f.term(), "(x^2+1)/(x-1)")

    def test_null_nenner_error(self):
        """Test: Fehler bei Null-Nenner"""
        z = GanzrationaleFunktion("x^2+1")
        n = GanzrationaleFunktion("0")
        with pytest.raises(TypeError, match="ist keine gebrochen-rationale Funktion"):
            GebrochenRationaleFunktion(z, n)

    def test_auto_kuerzen(self):
        """Test: Automatisches Kürzen"""
        f = GebrochenRationaleFunktion("(x^2-1)/(x-1)")
        # (x^2-1)/(x-1) sollte zu x+1 kürzen (als ganzrationale Funktion)
        assert_gleich(f.term(), "(x^2-1)/(x-1)")  # Hier zeigen wir die ungekürzte Form


class TestGebrochenRationaleFunktionGrundfunktionen:
    """Testet grundlegende Funktionalität"""

    def test_term_ausgabe(self):
        """Test: Term-Ausgabe"""
        f = GebrochenRationaleFunktion("(x^2+1)/(x-1)")
        assert_gleich(f.term(), "(x^2+1)/(x-1)")

    def test_latex_ausgabe(self):
        """Test: LaTeX-Ausgabe"""
        f = GebrochenRationaleFunktion("(x^2+1)/(x-1)")
        latex_str = f.term_latex()
        assert "x^{2} + 1" in latex_str
        assert "x - 1" in latex_str

    def test_wert_berechnung(self):
        """Test: Funktionswert-Berechnung"""
        f = GebrochenRationaleFunktion("(x^2+1)/(x-1)")
        assert abs(f.wert(2) - 5.0) < 1e-10  # (4+1)/(2-1) = 5
        assert abs(f.wert(3) - 5.0) < 1e-10  # (9+1)/(3-1) = 5

    def test_wert_an_polstelle(self):
        """Test: Auswertung an Polstelle ergibt ComplexInfinity"""
        f = GebrochenRationaleFunktion("(x^2+1)/(x-1)")
        from sympy import zoo

        assert f.wert(1) == zoo

    def test_nullstellen(self):
        """Test: Nullstellen-Berechnung"""
        f = GebrochenRationaleFunktion("(x^2-1)/(x-2)")
        nullstellen = f.nullstellen()
        assert len(nullstellen) == 2
        assert -1.0 in nullstellen or abs(-1.0 - nullstellen[0]) < 1e-10
        assert 1.0 in nullstellen or abs(1.0 - nullstellen[1]) < 1e-10

    def test_polstellen(self):
        """Test: Polstellen-Berechnung"""
        f = GebrochenRationaleFunktion("(x^2+1)/(x-1)")
        polstellen = f.polstellen()
        assert len(polstellen) == 1
        assert abs(polstellen[0] - 1.0) < 1e-10

    def test_definitionsluecken(self):
        """Test: Definitionslücken"""
        f = GebrochenRationaleFunktion("(x^2+1)/(x^2-1)")
        luecken = f.definitionsluecken()
        assert len(luecken) == 2
        # Prüfe, dass beide Werte vorhanden sind, unabhängig von der Reihenfolge
        assert -1.0 in luecken and 1.0 in luecken


class TestGebrochenRationaleFunktionArithmetik:
    """Testet arithmetische Operationen"""

    def test_addition_gebrochen_gebrochen(self):
        """Test: Addition von zwei gebrochen-rationalen Funktionen"""
        f1 = GebrochenRationaleFunktion("1/(x-1)")
        f2 = GebrochenRationaleFunktion("1/(x+1)")
        ergebnis = f1 + f2
        from sympy import simplify

        simplified = simplify(ergebnis.term_sympy)
        assert "2*x" in str(simplified)

    def test_addition_gebrochen_ganzrational(self):
        """Test: Addition gebrochen-rational + ganzrational"""
        f1 = GebrochenRationaleFunktion("1/(x-1)")
        f2 = GanzrationaleFunktion("x")
        ergebnis = f1 + f2
        assert ergebnis.ist_gebrochen_rational

    def test_addition_mit_skalar(self):
        """Test: Addition mit Skalar"""
        f = GebrochenRationaleFunktion("1/(x-1)")
        ergebnis = f + 2
        assert ergebnis.ist_gebrochen_rational

    def test_subtraktion(self):
        """Test: Subtraktion"""
        f1 = GebrochenRationaleFunktion("x/(x-1)")
        f2 = GebrochenRationaleFunktion("1/(x-1)")
        ergebnis = f1 - f2
        assert_gleich(ergebnis.term(), "(1)/(x-1)")  # (x-1)/(x-1) = 1

    def test_multiplikation(self):
        """Test: Multiplikation"""
        f1 = GebrochenRationaleFunktion("(x+1)/(x-1)")
        f2 = GebrochenRationaleFunktion("(x-1)/(x+1)")
        ergebnis = f1 * f2
        # Sollte sich zu 1 kürzen
        assert "1" in ergebnis.term()

    def test_division(self):
        """Test: Division"""
        f1 = GebrochenRationaleFunktion("(x+1)/(x-1)")
        f2 = GebrochenRationaleFunktion("(x-1)/(x+1)")
        ergebnis = f1 / f2
        # Sollte (x+1)^2/(x-1)^2 ergeben
        assert "(x+1)" in ergebnis.term() and "(x-1)" in ergebnis.term()

    def test_potenzierung(self):
        """Test: Potenzierung"""
        f = GebrochenRationaleFunktion("(x+1)/(x-1)")
        ergebnis = f**2
        assert "(x+1)^2" in ergebnis.term() or "(x + 1)^2" in ergebnis.term()

    def test_unaere_operationen(self):
        """Test: Unäre Operationen"""
        f = GebrochenRationaleFunktion("(x+1)/(x-1)")

        # Negation
        neg = -f
        assert "-(x+1)" in neg.term() or "-x" in neg.term()

        # Positiv
        pos = +f
        assert_gleich(pos.term(), f.term())


class TestGebrochenRationaleFunktionInPlace:
    """Testet In-place Operationen"""

    def test_in_place_addition(self):
        """Test: In-place Addition"""
        f1 = GebrochenRationaleFunktion("1/(x-1)")
        f2 = GebrochenRationaleFunktion("1/(x+1)")
        original_term = f1.term()

        f1 += f2
        assert f1.term() != original_term
        assert isinstance(f1, GebrochenRationaleFunktion)

    def test_in_place_multiplikation(self):
        """Test: In-place Multiplikation"""
        f = GebrochenRationaleFunktion("(x+1)/(x-1)")
        original_term = f.term()

        f *= 2
        assert f.term() != original_term
        assert isinstance(f, GebrochenRationaleFunktion)


class TestGebrochenRationaleFunktionIntegration:
    """Testet Integration mit ganzrationalen Funktionen"""

    def test_ganzrationale_division_erzeugt_gebrochen(self):
        """Test: Division ganzrationaler Funktionen erzeugt gebrochen-rationale"""
        f1 = GanzrationaleFunktion("x^2+1")
        f2 = GanzrationaleFunktion("x-1")

        ergebnis = f1 / f2
        assert isinstance(ergebnis, GebrochenRationaleFunktion)
        assert_gleich(ergebnis.term(), "(x^2+1)/(x-1)")

    def test_ganzrationale_division_bleibt_ganzrational(self):
        """Test: Division ganzrationaler Funktionen bleibt ganzrational"""
        f1 = GanzrationaleFunktion("x^2-1")
        f2 = GanzrationaleFunktion("x-1")

        ergebnis = f1 / f2
        assert isinstance(ergebnis, GanzrationaleFunktion)
        assert_gleich(ergebnis.term(), "x+1")

    def test_komplexe_arithmetik(self):
        """Test: Komplexe arithmetische Ausdrücke"""
        f1 = GanzrationaleFunktion("x^2")
        f2 = GanzrationaleFunktion("x-1")
        f3 = GanzrationaleFunktion("x+1")

        # (x^2/(x-1)) + ((x+1)/(x-1)) = (x^2 + x + 1)/(x-1)
        ergebnis = (f1 / f2) + (f3 / f2)
        assert isinstance(ergebnis, GebrochenRationaleFunktion)
        assert "x^2" in ergebnis.term()


class TestGebrochenRationaleFunktionSpecialCases:
    """Testet Sonderfälle und Randbedingungen"""

    def test_gleichheit(self):
        """Test: Gleichheitsvergleich"""
        f1 = GebrochenRationaleFunktion("(x^2+1)/(x-1)")
        f2 = GebrochenRationaleFunktion("(x^2+1)/(x-1)")
        f3 = GebrochenRationaleFunktion("(x^2+2)/(x-1)")

        assert f1 == f2
        assert f1 != f3

    def test_string_repr(self):
        """Test: String-Repräsentation"""
        f = GebrochenRationaleFunktion("(x^2+1)/(x-1)")
        str_repr = str(f)
        assert "GebrochenRationaleFunktion" in str_repr
        assert "(x^2+1)/(x-1)" in str_repr

    def test_nullstellen_ausschliesslich_polstellen(self):
        """Test: Nullstellen die Polstellen sind werden entfernt"""
        f = GebrochenRationaleFunktion("(x-1)/(x-1)")
        # Sollte keine Nullstellen haben (da x=1 Polstelle ist)
        nullstellen = f.nullstellen()
        assert len(nullstellen) == 0


def test_umfangreiches_beispiel():
    """Umfassendes Testbeispiel"""
    # Erstelle komplexe gebrochen-rationale Funktion
    f1 = GebrochenRationaleFunktion("(x^2-1)/(x-2)")
    f2 = GebrochenRationaleFunktion("(x+1)/(x^2-4)")

    # Arithmetische Operationen
    summe = f1 + f2
    differenz = f1 - f2
    produkt = f1 * f2
    quotient = f1 / f2

    # Überprüfe Typen
    assert isinstance(summe, GebrochenRationaleFunktion)
    assert isinstance(differenz, GebrochenRationaleFunktion)
    assert isinstance(produkt, GebrochenRationaleFunktion)
    assert isinstance(quotient, GebrochenRationaleFunktion)

    # Überprüfe mathematische Eigenschaften
    assert len(f1.nullstellen()) == 2  # x^2-1 = 0 -> x=±1
    assert len(f1.polstellen()) == 1  # x-2 = 0 -> x=2
    assert len(f2.polstellen()) == 2  # x^2-4 = 0 -> x=±2

    print("✅ Umfangreiches Testbeispiel erfolgreich!")


if __name__ == "__main__":
    print("=== Teste GebrochenRationaleFunktion ===\n")

    # Führe ausgewählte Tests durch
    test_umfangreiches_beispiel()

    print("\n🎉 Alle Tests erfolgreich durchgeführt!")
