#!/usr/bin/env python3
"""
Integrationstests für kritische Workflows im Schul-Analysis Framework

Diese Tests prüfen End-to-End Szenarien, die reale Anwendungsfälle abdecken.
Basierend auf den Empfehlungen der Gemini Code Review.
"""

import pytest
from src.schul_mathematik.analysis.funktion import Funktion
from src.schul_mathematik.analysis.api import (
    Nullstellen,
    Ableitung,
    Extrema,
    Wendepunkte,
    Zeichne,
    FlaecheZweiFunktionen,
    Integral,
)


class TestKurvendiskussionWorkflow:
    """Testet den vollständigen Workflow einer Kurvendiskussion."""

    def test_vollstaendige_kurvendiskussion_polynom(self):
        """Testet komplette Kurvendiskussion für ein Polynom."""
        # GIVEN: Eine Funktion
        f = Funktion("x^3 - 3x^2 + 2")

        # WHEN: Komplette Analyse wird durchgeführt
        nullstellen = f.nullstellen
        ableitungen = [f.ableitung(i) for i in range(1, 4)]
        extrema = f.extrema()
        wendepunkte = f.wendepunkte()

        # THEN: Alle Ergebnisse sollten konsistent sein
        assert len(nullstellen) == 3  # Drei reelle Nullstellen

        # Extrema sollten mit Ableitungs-Nullstellen übereinstimmen
        extrema_x_werte = [ext[0] for ext in extrema]
        assert len(extrema_x_werte) == 2  # Zwei Extrema

        # Wendepunkte sollten mit zweiten Ableitungs-Nullstellen übereinstimmen
        wendepunkte_x_werte = [wp[0] for wp in wendepunkte if wp[2] == "Wendepunkt"]
        assert len(wendepunkte_x_werte) == 1  # Ein Wendepunkt

        print("✅ Vollständige Kurvendiskussion erfolgreich")

    def test_wrapper_api_workflow(self):
        """Testet den Workflow mit Wrapper-Funktionen."""
        # GIVEN: Eine Funktion
        f = Funktion("x^2 - 4x + 3")

        # WHEN: Wrapper-Funktionen werden verwendet
        xs = Nullstellen(f)
        f1 = Ableitung(f, 1)
        ext = Extrema(f)
        wp = Wendepunkte(f)

        # THEN: Ergebnisse sollten mit direkten Methoden übereinstimmen
        assert [float(n.x) for n in xs] == [float(n.x) for n in f.nullstellen]
        assert f1.term() == f.ableitung(1).term()
        assert ext == f.extrema()
        assert wp == f.wendepunkte()

        print("✅ Wrapper-API Workflow erfolgreich")

    def test_parametrisierte_funktion_workflow(self):
        """Testet Workflow mit parametrisierten Funktionen."""
        # GIVEN: Eine parametrisierte Funktion
        f = Funktion("a*x^2 + b*x + c")

        # WHEN: Symbolische Berechnungen werden durchgeführt
        ableitung = f.ableitung(1)
        nullstellen = f.nullstellen  # Sollte symbolische Lösungen liefern

        # THEN: Ergebnisse sollten symbolisch bleiben
        assert "a" in ableitung.term()
        assert len(nullstellen) > 0  # Sollte symbolische Lösungen haben

        print("✅ Parametrisierte Funktion Workflow erfolgreich")


class TestFunktionserstellungWorkflow:
    """Testet verschiedene Wege der Funktionserstellung."""

    def test_magic_factory_pattern(self):
        """Testet das Magic Factory Pattern für automatische Typenerkennung."""
        # GIVEN: Verschiedene Funktions-Typen
        f_lineare = Funktion("2x + 3")
        f_quadratisch = Funktion("x^2 - 4x + 3")
        f_exponential = Funktion("exp(x) + 1")
        f_trigonometrisch = Funktion("sin(x)")
        f_gebrochen = Funktion("(x^2 + 1)/(x - 1)")

        # WHEN: Typen werden überprüft
        # THEN: Richtige spezialisierte Klassen sollten zurückgegeben werden
        assert "LineareFunktion" in str(type(f_lineare))
        assert "QuadratischeFunktion" in str(type(f_quadratisch))
        assert "ExponentialFunktion" in str(type(f_exponential))
        assert "TrigonometrischeFunktion" in str(type(f_trigonometrisch))
        assert "GanzrationaleFunktion" in str(type(f_gebrochen))

        print("✅ Magic Factory Pattern erfolgreich")

    def test_funktion_aus_string_erstellung(self):
        """Testet verschiedene String-Eingabeformate."""
        # GIVEN: Verschiedene String-Formate
        test_cases = [
            "x^2 - 4",
            "x**2 - 4",  # Python-Syntax
            "2*x + 3",  # Explizite Multiplikation
            "x^3 - 3x^2 + 2x - 1",
            "sin(x) + cos(x)",
            "exp(-x^2)",
        ]

        # WHEN: Funktionen werden erstellt
        # THEN: Alle sollten ohne Fehler erstellt werden
        for term in test_cases:
            f = Funktion(term)
            assert f.term() is not None
            assert len(f.term()) > 0

        print("✅ Verschiedene String-Formate erfolgreich")

    def test_funktion_aus_koeffizienten(self):
        """Testet Funktionserstellung aus Koeffizienten."""
        # GIVEN: Koeffizienten-Liste
        koeffizienten = [1, -4, 3]  # x^2 - 4x + 3

        # WHEN: Funktion wird erstellt
        f = Funktion(koeffizienten)

        # THEN: Sollte korrekten Term haben
        assert "x^2" in f.term()
        assert "-4*x" in f.term()

        print("✅ Funktion aus Koeffizienten erfolgreich")


class TestVisualisierungsWorkflow:
    """Testet Visualisierungs-Workflows."""

    def test_zeichne_funktion_workflow(self):
        """Testet das Zeichnen von Funktionen."""
        # GIVEN: Eine Funktion
        f = Funktion("x^2 - 4")

        # WHEN: Funktion wird gezeichnet
        fig = Zeichne(f, x_bereich=(-5, 5))

        # THEN: Sollte eine gültige Figure zurückgeben
        assert fig is not None

        print("✅ Zeichne-Funktion Workflow erfolgreich")

    def test_flaeche_zwei_funktionen_workflow(self):
        """Testet die Berechnung der Fläche zwischen zwei Funktionen."""
        # GIVEN: Zwei Funktionen
        f1 = Funktion("x^2")
        f2 = Funktion("x")

        # WHEN: Fläche wird berechnet
        fig = FlaecheZweiFunktionen(f1, f2, 0, 1)

        # THEN: Sollte eine gültige Figure zurückgeben
        assert fig is not None

        print("✅ Fläche-zwei-Funktionen Workflow erfolgreich")


class TestArithmetischeOperationenWorkflow:
    """Testet arithmetische Operationen zwischen Funktionen."""

    def test_funktionen_addition_subtraktion(self):
        """Testet Addition und Subtraktion von Funktionen."""
        # GIVEN: Zwei Funktionen
        f1 = Funktion("x^2")
        f2 = Funktion("2*x + 1")

        # WHEN: Operationen werden durchgeführt
        summe = f1 + f2
        differenz = f1 - f2

        # THEN: Ergebnisse sollten korrekt sein
        assert summe.term() == "x^2 + 2*x + 1"
        assert differenz.term() == "x^2 - 2*x - 1"

        print("✅ Funktionen Addition/Subtraktion erfolgreich")

    def test_funktionen_multiplikation_division(self):
        """Testet Multiplikation und Division von Funktionen."""
        # GIVEN: Zwei Funktionen
        f1 = Funktion("x + 1")
        f2 = Funktion("x - 1")

        # WHEN: Operationen werden durchgeführt
        produkt = f1 * f2
        quotient = f1 / f2

        # THEN: Ergebnisse sollten korrekt sein
        assert produkt.term() == "x^2 - 1"
        assert "x + 1" in quotient.term() and "x - 1" in quotient.term()

        print("✅ Funktionen Multiplikation/Division erfolgreich")

    def test_funktionen_komposition(self):
        """Testet die Komposition von Funktionen."""
        # GIVEN: Zwei Funktionen
        f = Funktion("x^2")
        g = Funktion("x + 1")

        # WHEN: Komposition wird durchgeführt
        # f(g(x)) = (x+1)^2
        komposition = f(g.term())
        expected = Funktion("(x + 1)^2")

        # THEN: Ergebnis sollte korrekt sein
        assert komposition.term() == expected.term()

        print("✅ Funktionen Komposition erfolgreich")


class TestErrorHandlingWorkflow:
    """Testet Fehlerbehandlungs-Workflows."""

    def test_division_durch_null_workflow(self):
        """Testet die Behandlung von Division durch Null."""
        # GIVEN: Eine Funktion mit Polstelle
        f = Funktion("1/(x - 1)")

        # WHEN: Polstellen werden gesucht
        polstellen = f.polstellen

        # THEN: Sollte Polstelle bei x=1 erkennen
        assert 1.0 in polstellen or 1 in polstellen

        print("✅ Division-durch-Null-Handling erfolgreich")

    def test_sicherheitsvalidierung_workflow(self):
        """Testet die Sicherheitsvalidierung bei der Eingabe."""
        # GIVEN: Gefährliche Eingabe
        gefaehrliche_eingaben = [
            "import os",
            "eval('dangerous')",
            "__import__('sys')",
            "open('/etc/passwd')",
        ]

        # WHEN: Eingaben werden versucht
        # THEN: Sollte Sicherheitsfehler werfen
        for eingabe in gefaehrliche_eingaben:
            try:
                f = Funktion(eingabe)
                assert False, f"Sicherheitslücke: {eingabe}"
            except (ValueError, SyntaxError, AttributeError):
                pass  # Erwarteter Fehler

        print("✅ Sicherheitsvalidierung erfolgreich")


class TestPerformanceWorkflow:
    """Testet Performance-relevante Workflows."""

    def test_caching_effekt_workflow(self):
        """Testet den Caching-Effekt bei wiederholten Berechnungen."""
        # GIVEN: Eine komplexe Funktion
        f = Funktion("x^5 - 3x^4 + 2x^3 - 5x^2 + x - 1")

        # WHEN: Berechnungen werden wiederholt
        import time

        # Erste Berechnung
        start = time.perf_counter()
        ableitung1 = f.ableitung(1)
        zeit1 = time.perf_counter() - start

        # Zweite Berechnung (sollte aus Cache kommen)
        start = time.perf_counter()
        ableitung2 = f.ableitung(1)
        zeit2 = time.perf_counter() - start

        # THEN: Zweite Berechnung sollte schneller sein
        assert zeit2 < zeit1  # Sollte schneller sein

        print(f"✅ Caching-Effekt: {zeit1:.4f}s → {zeit2:.4f}s")

    def test_legacy_adapter_performance(self):
        """Testet die Performance des Legacy-Adapters."""
        # GIVEN: Eine Funktion
        f = Funktion("x^3 - 3x^2 + 2")

        # WHEN: Legacy-Adapter wird verwendet
        import time

        start = time.perf_counter()
        for _ in range(50):
            _ = f.legacy.nullstellen
            _ = f.legacy.get_extremstellen()
        legacy_zeit = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(50):
            _ = f.nullstellen
            _ = f.extrema()
        modern_zeit = time.perf_counter() - start

        # THEN: Legacy-Overhead sollte akzeptabel sein
        overhead_faktor = legacy_zeit / modern_zeit if modern_zeit > 0 else 1
        assert overhead_faktor < 5  # Sollte weniger als 5x langsamer sein

        print(f"✅ Legacy-Overhead: {overhead_faktor:.1f}x")


def run_integration_tests():
    """Führt alle Integrationstests durch."""
    print("Schul-Analysis Framework - Integrationstests")
    print("=" * 50)
    print()

    # Führe Tests durch
    test_suites = [
        TestKurvendiskussionWorkflow(),
        TestFunktionserstellungWorkflow(),
        TestVisualisierungsWorkflow(),
        TestArithmetischeOperationenWorkflow(),
        TestErrorHandlingWorkflow(),
        TestPerformanceWorkflow(),
    ]

    for suite in test_suites:
        suite_name = suite.__class__.__name__
        print(f"=== {suite_name} ===")

        # Finde alle Test-Methoden
        test_methods = [method for method in dir(suite) if method.startswith("test_")]

        for method_name in test_methods:
            try:
                method = getattr(suite, method_name)
                method()
                print(f"✅ {method_name}")
            except Exception as e:
                print(f"❌ {method_name}: {e}")

        print()

    print("Integrationstests abgeschlossen!")


if __name__ == "__main__":
    run_integration_tests()
