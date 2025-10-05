"""
Vereinheitliche Funktionsklasse für das Schul-Analysis Framework.

Dies ist die zentrale, echte unified Klasse - keine Wrapper-Logik mehr!
Alle spezialisierten Klassen erben von dieser Basis-Klasse.
"""

from typing import Union

import sympy as sp
from sympy import diff, latex, solve, symbols

# Type Hint compatibility for different Python versions
try:
    # Python 3.14+ - native union syntax available
    UNION_TYPE_AVAILABLE = True
except ImportError:
    UNION_TYPE_AVAILABLE = False

from .symbolic import _Parameter, _Variable


class Funktion:
    """
    Zentrale vereinheitlichte Funktionsklasse für das Schul-Analysis Framework.

    Diese Klasse ist das Herzstück der unified Architecture. Sie kann:
    - Beliebige mathematische Ausdrücke verarbeiten
    - Alle Grundoperationen bereitstellen (Ableiten, Integrieren, etc.)
    - Automatische Typenerkennung durchführen
    - Als Basis für spezialisierte pädagogische Klassen dienen

    Examples:
        >>> f = Funktion("x^2 + 1")              # ganzrational
        >>> g = Funktion("(x^2 + 1)/(x - 1)")    # gebrochen-rational
        >>> h = Funktion("exp(x) + 1")           # exponential
        >>> t = Funktion("sin(x)")                # trigonometrisch
    """

    def __init__(
        self,
        eingabe: Union[str, sp.Basic, "Funktion", tuple[str, str]],
        nenner: Union[str, sp.Basic, "Funktion", None] = None,
    ):
        """
        Konstruktor für die vereinheitlichte Funktionsklasse.

        Args:
            eingabe: Kann sein:
                     - String: "x^2 + 1", "(x^2 + 1)/(x - 1)", "exp(x) + 1"
                     - SymPy-Ausdruck
                     - Funktion-Objekt (für Kopien)
                     - Tuple: (zaehler_string, nenner_string)
            nenner: Optionaler Nenner (wenn eingabe nur Zähler ist)
        """
        # 🔥 ECHTE UNIFIED ARCHITECTURE - Keine Wrapper-Delegation mehr! 🔥

        # Grundlegende Initialisierung
        self._initialisiere_basiskomponenten()

        # Verarbeite die Eingabe und erstelle SymPy-Ausdruck
        self._verarbeite_eingabe(eingabe, nenner)

        # Erstelle SymPy-Ausdrücke für Berechnungen
        self._erstelle_symbole_ausdruecke()

    def _initialisiere_basiskomponenten(self):
        """Initialisiert die grundlegenden Komponenten"""
        self._variable_symbol = symbols("x")
        self.variablen: list[_Variable] = []
        self.parameter: list[_Parameter] = []
        self.hauptvariable: _Variable | None = None
        self.original_eingabe = ""
        self._cache = {}

    def _verarbeite_eingabe(
        self,
        eingabe: Union[str, sp.Basic, "Funktion", tuple[str, str]],
        nenner: Union[str, sp.Basic, "Funktion", None] = None,
    ):
        """Verarbeitet die Eingabe und erstellt Term"""
        # Speichere ursprüngliche Eingabe
        if isinstance(eingabe, tuple) and len(eingabe) == 2:
            self.original_eingabe = f"({eingabe[0]})/({eingabe[1]})"
        else:
            self.original_eingabe = str(eingabe)

        # Verarbeite verschiedene Eingabetypen
        if isinstance(eingabe, tuple) and len(eingabe) == 2:
            self._verarbeite_tuple_eingabe(eingabe)
        elif isinstance(eingabe, Funktion):
            self._verarbeite_funktions_kopie(eingabe)
        else:
            self._verarbeite_standard_eingabe(eingabe, nenner)

    def _verarbeite_tuple_eingabe(self, eingabe: tuple[str, str]):
        """Verarbeitet Tupel-Eingabe (zaehler, nenner)"""
        zaehler_str, nenner_str = eingabe
        zaehler_expr = self._parse_string_to_sympy(zaehler_str)
        nenner_expr = self._parse_string_to_sympy(nenner_str)
        self.term_sympy = zaehler_expr / nenner_expr

    def _verarbeite_funktions_kopie(self, andere_funktion: "Funktion"):
        """Verarbeitet Kopie einer anderen Funktion"""
        self.term_sympy = andere_funktion.term_sympy.copy()
        self._variable_symbol = andere_funktion._variable_symbol
        self.variablen = andere_funktion.variablen.copy()
        self.parameter = andere_funktion.parameter.copy()
        self.hauptvariable = andere_funktion.hauptvariable

    def _verarbeite_standard_eingabe(
        self,
        eingabe: str | sp.Basic,
        nenner: Union[str, sp.Basic, "Funktion", None] = None,
    ):
        """Verarbeitet Standard-Eingabe"""
        if isinstance(eingabe, str):
            self.term_sympy = self._parse_string_to_sympy(eingabe)
        else:
            self.term_sympy = eingabe

        # Wenn Nenner angegeben, kombiniere
        if nenner is not None:
            if isinstance(nenner, str):
                nenner_expr = self._parse_string_to_sympy(nenner)
            else:
                nenner_expr = nenner
            self.term_sympy = self.term_sympy / nenner_expr

    def _parse_string_to_sympy(self, eingabe: str) -> sp.Basic:
        """Parset String-Eingabe zu SymPy-Ausdruck mit allen Transformationen"""
        from sympy.parsing.sympy_parser import (
            implicit_multiplication_application,
            parse_expr,
            standard_transformations,
        )

        # Bereinige Eingabe
        bereinigt = eingabe.strip().replace("$", "").replace("^", "**")

        # Verwende alle Transformationen
        transformations = standard_transformations + (
            implicit_multiplication_application,
        )

        try:
            return parse_expr(bereinigt, transformations=transformations)
        except Exception as e:
            raise ValueError(f"Kann '{eingabe}' nicht parsen: {e}")

    def _erstelle_symbole_ausdruecke(self):
        """Erstelle SymPy-Ausdrücke und führe Initialisierung durch"""
        # Erkenne Hauptvariable automatisch
        alle_symbole = self.term_sympy.free_symbols
        if not alle_symbole:
            self.hauptvariable = _Variable("x")
            self._variable_symbol = symbols("x")
        else:
            # Heuristik zur Hauptvariablen-Erkennung
            for symbol in alle_symbole:
                symbol_name = str(symbol)
                if symbol_name == "x":
                    self.hauptvariable = _Variable(symbol_name)
                    self._variable_symbol = symbol
                    break
                elif symbol_name in ["t", "y", "z"]:
                    self.hauptvariable = _Variable(symbol_name)
                    self._variable_symbol = symbol
                    break
            else:
                # Nimm erstes Symbol
                first_symbol = list(alle_symbole)[0]
                self.hauptvariable = _Variable(str(first_symbol))
                self._variable_symbol = first_symbol

        # Klassifiziere Symbole in Variablen und Parameter
        self._klassifiziere_symbole()

    def _klassifiziere_symbole(self):
        """Klassifiziert Symbole in Variablen und Parameter"""
        for symbol in self.term_sympy.free_symbols:
            symbol_name = str(symbol)
            if symbol_name == str(self._variable_symbol):
                self.variablen.append(_Variable(symbol_name))
            elif symbol_name in ["a", "b", "c", "k", "m", "n", "p", "q"]:
                self.parameter.append(_Parameter(symbol_name))
            else:
                # Default: als Variable behandeln
                self.variablen.append(_Variable(symbol_name))

    # 🔥 KERNFUNKTIONALITÄT - Alle zentral in einer Klasse! 🔥

    def term(self) -> str:
        """Gibt den Term als String zurück"""
        return str(self.term_sympy).replace("**", "^")

    def term_latex(self) -> str:
        """Gibt den Term als LaTeX-String zurück"""
        return latex(self.term_sympy)

    def __call__(self, x_wert):
        """Ermöglicht f(x) Syntax für Funktionsauswertung"""
        return self.wert(x_wert)

    def wert(self, x_wert):
        """Berechnet den Funktionswert an einer Stelle"""
        try:
            Ergebnis = self.term_sympy.subs(self._variable_symbol, x_wert)
            return float(Ergebnis) if Ergebnis.is_real else Ergebnis
        except Exception as e:
            raise ValueError(f"Fehler bei Berechnung von f({x_wert}): {e}")

    def ableitung(self, ordnung: int = 1) -> "Funktion":
        """Berechnet die Ableitung"""
        abgeleiteter_term = diff(self.term_sympy, self._variable_symbol, ordnung)
        return Funktion(abgeleiteter_term)

    def nullstellen(self) -> list:
        """Berechnet die Nullstellen"""
        try:
            lösungen = solve(self.term_sympy, self._variable_symbol)
            return [
                float(lösung) if lösung.is_real else lösung
                for lösung in lösungen
                if lösung.is_real
            ]
        except Exception:
            return []

    # 🔥 TYPENERKENNUNG - Alle zentral! 🔥

    @property
    def ist_ganzrational(self) -> bool:
        """Prüft, ob die Funktion ganzrational ist"""
        return self.term_sympy.is_polynomial(self._variable_symbol)

    @property
    def ist_gebrochen_rational(self) -> bool:
        """Prüft, ob die Funktion gebrochen-rational ist"""
        return (
            self.term_sympy.is_rational_function(self._variable_symbol)
            and not self.ist_ganzrational
        )

    @property
    def ist_exponential_rational(self) -> bool:
        """Prüft, ob die Funktion exponential-rational ist"""
        return self.term_sympy.has(sp.exp)

    @property
    def ist_trigonometrisch(self) -> bool:
        """Prüft, ob die Funktion trigonometrisch ist"""
        return self.term_sympy.has(sp.sin, sp.cos, sp.tan, sp.cot, sp.sec, sp.csc)

    @property
    def ist_gemischt(self) -> bool:
        """Prüft, ob die Funktion gemischt ist"""
        merkmale = 0
        if self.term_sympy.is_polynomial(self._variable_symbol):
            merkmale += 1
        if self.term_sympy.is_rational_function(
            self._variable_symbol
        ) and not self.term_sympy.is_polynomial(self._variable_symbol):
            merkmale += 1
        if self.term_sympy.has(sp.sin, sp.cos, sp.tan, sp.cot, sp.sec, sp.csc):
            merkmale += 1
        if self.term_sympy.has(sp.exp):
            merkmale += 1
        if self.term_sympy.has(sp.log, sp.ln):
            merkmale += 1
        if self.term_sympy.has(sp.sqrt):
            merkmale += 1
        return merkmale > 1

    @property
    def funktionstyp(self) -> str:
        """Gibt den Funktionstyp als String zurück"""
        if self.ist_ganzrational:
            return "ganzrational"
        elif self.ist_gebrochen_rational:
            return "gebrochen-rational"
        elif self.ist_exponential_rational:
            return "exponential-rational"
        elif self.ist_trigonometrisch:
            return "trigonometrisch"
        elif self.ist_gemischt:
            return "gemischt"
        else:
            return "allgemein"

    # 🔥 HILFSMETHODEN 🔥

    def __str__(self):
        return self.term()

    def __repr__(self):
        return f"Funktion('{self.term()}')"

    def __eq__(self, other):
        if not isinstance(other, Funktion):
            return False
        return self.term_sympy.equals(other.term_sympy)


# 🔥 FACTORY-FUNKTION für automatische Erkennung 🔥


def erstelle_funktion_automatisch(
    eingabe: Union[str, sp.Basic, "Funktion", tuple[str, str]],
    nenner: Union[str, sp.Basic, "Funktion", None] = None,
) -> Funktion:
    """
    Factory-Funktion, die automatisch den richtigen Funktionstyp erkennt und erstellt.

    Args:
        eingabe: String, SymPy-Ausdruck, Funktion-Objekt oder Tuple (zaehler, nenner)
        nenner: Optionaler Nenner (wenn eingabe nur Zähler ist)

    Returns:
        Funktion: Automatisch erkannte und erstellte Funktion (spezialisierte Klasse)
    """
    # 🔥 FACTORY-LOGIK: Automatische Typenerkennung 🔥

    # Erstelle erstmal eine Basis-Funktion zur Typanalyse
    basis_funktion = Funktion(eingabe, nenner)

    # Importiere spezialisierte Klassen (zur Vermeidung von Circular Imports)
    from .ganzrationale import GanzrationaleFunktion
    from .gebrochen_rationale import (
        ExponentialRationaleFunktion,
        GebrochenRationaleFunktion,
    )
    from .trigonometrisch import TrigonometrischeFunktion

    # 🔥 AUTOMATISCHE TYPENERKENNUNG 🔥
    if basis_funktion.ist_ganzrational:
        # 🔥 FIX: GanzrationaleFunktion hat andere Signatur (kein nenner) 🔥
        if nenner is not None:
            # Wenn Nenner angegeben, kombiniere vorher
            if isinstance(eingabe, tuple) and len(eingabe) == 2:
                # Tuple-Eingabe (zaehler, nenner)
                combined_str = f"({eingabe[0]})/({eingabe[1]})"
                return GanzrationaleFunktion(combined_str)
            else:
                combined_str = f"{eingabe}/{nenner}"
                return GanzrationaleFunktion(combined_str)
        else:
            # Konvertiere zu String für ganzrationale Funktion
            if isinstance(eingabe, Funktion):
                eingabe_str = eingabe.term()
            else:
                eingabe_str = str(eingabe)
            return GanzrationaleFunktion(eingabe_str)
    elif basis_funktion.ist_gebrochen_rational:
        # Konvertiere zu passendem Format für gebrochen-rationale Funktion
        if isinstance(eingabe, Funktion):
            eingabe_str = eingabe.term()
        else:
            eingabe_str = str(eingabe)
        if isinstance(nenner, Funktion):
            nenner_str = nenner.term()
        else:
            nenner_str = str(nenner) if nenner is not None else None
        return GebrochenRationaleFunktion(eingabe_str, nenner_str)
    elif basis_funktion.ist_exponential_rational:
        # Konvertiere zu passendem Format für exponential-rationale Funktion
        if isinstance(eingabe, Funktion):
            eingabe_str = eingabe.term()
        else:
            eingabe_str = str(eingabe)
        return ExponentialRationaleFunktion(eingabe_str)
    elif basis_funktion.ist_trigonometrisch:
        # Konvertiere zu passendem Format für trigonometrische Funktion
        if isinstance(eingabe, Funktion):
            eingabe_str = eingabe.term()
        else:
            eingabe_str = str(eingabe)
        return TrigonometrischeFunktion(eingabe_str)
    else:
        # Fallback auf Basis-Klasse für gemischte oder allgemeine Funktionen
        return basis_funktion
