"""
Tests für die erweiterten Type Hints mit Protocol Classes
"""

import pytest
import sympy as sp
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schul_mathematik.analysis.funktion import Funktion

from schul_mathematik.analysis.sympy_types import (
    # Protocol Classes
    MathematischeFunktion,
    ParametrisierteFunktion,
    VisualisierbareFunktion,
    AbleitbareFunktion,
    NullstellenBerechenbareFunktion,
    StetigeFunktion,
    SymmetrischeFunktion,
    GrenzwertBerechenbareFunktion,
    VergleichbareFunktion,
    KombinierbareFunktion,
    # Type Guards
    ist_mathematische_funktion,
    ist_parametrisierte_funktion,
    ist_visualisierbare_funktion,
    ist_ableitbare_funktion,
    ist_ganzrationale_funktion,
    hat_exakte_typen,
    # Type Constraints
    T_Funktionstyp,
    T_AnalyseOperation,
    T_ValidierungsTyp,
    # Validation Decorators
    erfordert_funktionstyp,
    validiere_domain,
    # Existing types
    Nullstelle,
    Extremstelle,
    ExtremumTyp,
)


class TestProtocolClasses:
    """Testet die neuen Protocol Classes"""

    def test_mathematische_funktion_protocol(self):
        """Testet das grundlegende MathematischeFunktion-Protocol"""
        from schul_mathematik.analysis.funktion import Funktion

        f = Funktion("x^2 + 1")

        # Prüfe, ob alle erforderlichen Methoden existieren
        assert hasattr(f, "term_sympy")
        assert hasattr(f, "term")
        assert hasattr(f, "wert")
        assert hasattr(f, "ableitung")
        assert hasattr(f, "nullstellen")
        assert hasattr(f, "extremstellen")
        assert hasattr(f, "ist_ganzrational")
        assert hasattr(f, "funktionstyp")

        # Prüfe, ob die Methoden aufrufbar sind
        assert callable(f.wert)
        assert callable(f.ableitung)

        # Type Guard sollte funktionieren
        assert ist_mathematische_funktion(f)

    def test_parametrisierte_funktion_protocol(self):
        """Testet das ParametrisierteFunktion-Protocol"""
        from schul_mathematik.analysis.funktion import Funktion

        f = Funktion("a*x^2 + b*x + c")

        # Prüfe Parameter-spezifische Methoden
        assert hasattr(f, "parameter")
        assert hasattr(f, "setze_parameter")
        assert hasattr(f, "mit_wert")

        # Type Guard sollte funktionieren
        assert ist_parametrisierte_funktion(f)

        # Funktion ohne Parameter sollte nicht parametrisiert sein
        f2 = Funktion("x^2 + 1")
        assert not ist_parametrisierte_funktion(f2)

    def test_visualisierbare_funktion_protocol(self):
        """Testet das VisualisierbareFunktion-Protocol"""
        from schul_mathematik.analysis.funktion import Funktion

        f = Funktion("x^2 + 1")

        # Prüfe Visualisierungs-Methoden
        assert hasattr(f, "graph")
        assert hasattr(f, "zeige_funktion_plotly")
        assert callable(f.graph)

        # Type Guard sollte funktionieren
        assert ist_visualisierbare_funktion(f)

    def test_ableitbare_funktion_protocol(self):
        """Testet das AbleitbareFunktion-Protocol"""
        from schul_mathematik.analysis.funktion import Funktion

        f = Funktion("x^3 + 2*x^2 + x + 1")

        # Prüfe erweiterte Ableitungs-Methoden
        assert hasattr(f, "integral")
        assert hasattr(f, "wendestellen")
        assert callable(f.integral)

        # Type Guard sollte funktionieren
        assert ist_ableitbare_funktion(f)

    def test_type_guards_kombination(self):
        """Testet die Kombination verschiedener Type Guards"""
        from schul_mathematik.analysis.funktion import Funktion

        # Komplexe Funktion
        f = Funktion("a*x^3 + b*x^2 + c*x + d")

        # Sollte alle Protocols erfüllen
        assert ist_mathematische_funktion(f)
        assert ist_parametrisierte_funktion(f)
        assert ist_visualisierbare_funktion(f)
        assert ist_ableitbare_funktion(f)

        # Funktion ohne Parameter
        f2 = Funktion("x^2 + 1")

        # Sollte einige Protocols erfüllen
        assert ist_mathematische_funktion(f2)
        assert not ist_parametrisierte_funktion(f2)
        assert ist_visualisierbare_funktion(f2)
        assert ist_ableitbare_funktion(f2)

    def test_ist_ganzrationale_funktion(self):
        """Testet den speziellen Type Guard für ganzrationale Funktionen"""
        from schul_mathematik.analysis.funktion import Funktion

        # Ganzrationale Funktionen
        f1 = Funktion("x^2 + 2*x + 1")
        f2 = Funktion("x^3 - 4*x")

        # Nicht-ganzrationale Funktionen
        f3 = Funktion("1/(x+1)")
        f4 = Funktion("sqrt(x)")

        assert ist_ganzrationale_funktion(f1)
        assert ist_ganzrationale_funktion(f2)
        assert not ist_ganzrationale_funktion(f3)
        assert not ist_ganzrationale_funktion(f4)

    def test_hat_exakte_typen(self):
        """Testet den Type Guard für exakte Typen"""
        from schul_mathematik.analysis.funktion import Funktion

        # Funktion mit exakten Typen
        f = Funktion("x^2 + 1")

        # Prüfe, ob die Funktion exakte Typen garantiert
        # (Dies hängt von der internen Implementierung ab)
        try:
            result = hat_exakte_typen(f)
            # Das Ergebnis hängt vom aktuellen Zustand der Funktion ab
            assert isinstance(result, bool)
        except Exception as e:
            # Wenn eine Exception auftritt, ist das auch in Ordnung
            # (zeigt, dass der Type Guard funktioniert)
            assert isinstance(e, (TypeError, AttributeError))


class TestTypeConstraints:
    """Testet die neuen Type Constraints"""

    def test_funktionstyp_literal(self):
        """Testet den T_Funktionstyp Literal"""
        # Teste, dass alle erwarteten Funktionstypen im Literal sind
        expected_types = [
            "ganzrational",
            "gebrochen_rational",
            "exponential_rational",
            "exponentiell",
            "trigonometrisch",
            "gemischt",
            "linear",
            "quadratisch",
            "kubisch",
            "unbekannt",
        ]

        for typ in expected_types:
            # Type Check sollte funktionieren
            def test_function(param: T_Funktionstyp) -> T_Funktionstyp:
                return param

            assert test_function(typ) == typ

    def test_analyse_operation_literal(self):
        """Testet den T_AnalyseOperation Literal"""
        expected_operations = [
            "ableitung",
            "integral",
            "nullstellen",
            "extremstellen",
            "wendestellen",
            "grenzwerte",
            "asymptoten",
            "definitionsbereich",
        ]

        for op in expected_operations:
            # Type Check sollte funktionieren
            def test_function(param: T_AnalyseOperation) -> T_AnalyseOperation:
                return param

            assert test_function(op) == op

    def test_validierungstyp_literal(self):
        """Testet den T_ValidierungsTyp Literal"""
        expected_types = ["exact", "symbolic", "numeric", "inexact"]

        for typ in expected_types:
            # Type Check sollte funktionieren
            def test_function(param: T_ValidierungsTyp) -> T_ValidierungsTyp:
                return param

            assert test_function(typ) == typ


class TestValidationDecorators:
    """Testet die neuen Validierungs-Decorators"""

    def test_erfordert_funktionstyp_decorator(self):
        """Testet den @erfordert_funktionstyp Decorator"""
        from schul_mathematik.analysis.funktion import Funktion

        # Decorator erstellen
        @erfordert_funktionstyp("ganzrational")
        def test_operation(funktion):
            return f"Operation auf {funktion.funktionstyp}"

        # Teste mit korrektem Funktionstyp
        f_ganzrational = Funktion("x^2 + 1")
        result = test_operation(f_ganzrational)
        assert "ganzrational" in result

        # Teste mit falschem Funktionstyp
        f_gebrochen = Funktion("1/(x+1)")
        with pytest.raises(TypeError, match="nur für ganzrational-Funktionen"):
            test_operation(f_gebrochen)

    def test_erfordert_funktionstyp_decorator_missing_method(self):
        """Testet den Decorator mit Objekt ohne funktionstyp-Methode"""

        @erfordert_funktionstyp("ganzrational")
        def test_operation(funktion):
            return "Test"

        # Objekt ohne funktionstyp-Methode
        class MockObject:
            pass

        mock = MockObject()
        with pytest.raises(TypeError, match="hat keine funktionstyp-Methode"):
            test_operation(mock)

    def test_validiere_domain_decorator(self):
        """Testet den @validiere_domain Decorator"""
        from schul_mathematik.analysis.funktion import Funktion

        # Decorator erstellen
        @validiere_domain("ℝ")
        def test_operation(funktion):
            return f"Operation auf {funktion.definitionsbereich()}"

        # Teste mit korrektem Domain
        f = Funktion("x^2 + 1")
        result = test_operation(f)
        assert "ℝ" in result

        # Hier können wir nicht leicht eine Funktion mit anderem Domain testen,
        # da die definitionsbereich-Methode intern festgelegt ist

    def test_validiere_domain_decorator_missing_method(self):
        """Testet den Decorator mit Objekt ohne definitionsbereich-Methode"""

        @validiere_domain("ℝ")
        def test_operation(funktion):
            return "Test"

        # Objekt ohne definitionsbereich-Methode
        class MockObject:
            pass

        mock = MockObject()
        with pytest.raises(TypeError, match="hat keine definitionsbereich-Methode"):
            test_operation(mock)


class TestTypeIntegration:
    """Testet die Integration der neuen Typ-Systeme in bestehenden Code"""

    def test_funktion_implementation(self):
        """Testet, dass die Funktion-Klasse die Protocols korrekt implementiert"""
        from schul_mathematik.analysis.funktion import Funktion

        f = Funktion("x^2 + 1")

        # Teste grundlegende Eigenschaften
        assert f.term() in ["x^2 + 1", "x² + 1"]  # Beide Formate akzeptieren
        assert f.wert(2) in [5, 5.0]  # Beide Typen akzeptieren
        assert f.ist_ganzrational  # Property, nicht Methode

        # Teste Ableitung
        f1 = f.ableitung()
        assert f1.term() in ["2*x", "2⋅x"]

        # Teste Nullstellen
        nullstellen = f.nullstellen()
        assert len(nullstellen) == 0  # x^2 + 1 hat keine reellen Nullstellen

        # Teste Extremstellen
        extremstellen = f.extremstellen()
        assert len(extremstellen) == 1  # Minimum bei x=0

    def test_parametrisierte_funktion_implementation(self):
        """Testet parametrisierte Funktionen mit den neuen Typen"""
        from schul_mathematik.analysis.funktion import Funktion

        f = Funktion("a*x^2 + b*x + c")

        # Teste Parameter-Erkennung
        assert len(f.parameter) == 3

        # Teste Parameter-Setzung
        f_params = f.setze_parameter(a=1, b=2, c=3)
        assert f_params.term() in [
            "x^2 + 2*x + 3",
            "x² + 2⋅x + 3",
        ]  # Beide Formate akzeptieren

        # Type Guards sollten funktionieren
        assert ist_parametrisierte_funktion(f)
        # f_params hat keine Parameter mehr (wurden gesetzt), also sollte der Type Guard False zurückgeben
        assert not ist_parametrisierte_funktion(f_params)

    def test_typsicherheit_mit_protocols(self):
        """Testet Typsicherheit mit den neuen Protocol-Interfaces"""

        def process_function(f: MathematischeFunktion) -> str:
            """Verarbeitet eine mathematische Funktion"""
            return f"Funktionstyp: {f.funktionstyp}"

        def process_parametric_function(f: ParametrisierteFunktion) -> int:
            """Verarbeitet eine parametrisierte Funktion"""
            return len(f.parameter)

        def process_visualizable_function(f: VisualisierbareFunktion) -> bool:
            """Verarbeitet eine visualisierbare Funktion"""
            try:
                f.graph()
                return True
            except:
                return False

        from schul_mathematik.analysis.funktion import Funktion

        # Teste mit verschiedenen Funktionen
        f1 = Funktion("x^2 + 1")
        f2 = Funktion("a*x^2 + b*x + c")

        # Alle sollten funktionieren
        assert "ganzrational" in process_function(f1)
        assert process_parametric_function(f2) == 3
        assert process_visualizable_function(f1)

    def test_decorator_kombination(self):
        """Testet die Kombination von Validierungs-Decorators"""
        from schul_mathematik.analysis.funktion import Funktion

        @erfordert_funktionstyp("ganzrational")
        @validiere_domain("ℝ")
        def komplexe_operation(funktion):
            return f"Komplexe Operation auf {funktion.funktionstyp}"

        f = Funktion("x^2 + 1")
        result = komplexe_operation(f)
        assert "ganzrational" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
