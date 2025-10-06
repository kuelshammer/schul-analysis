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

    Diese Klasse ist das Herzstück der Magic Factory Architecture. Sie kann:
    - Beliebige mathematische Ausdrücke verarbeiten
    - Alle Grundoperationen bereitstellen (Ableiten, Integrieren, etc.)
    - Automatische Typenerkennung: Funktion("x^2") gibt QuadratischeFunktion zurück!
    - Als Basis für spezialisierte pädagogische Klassen dienen

    Die Factory-Architektur kombiniert Einfachheit und Funktionalität:
    - Einfachheit: f = Funktion("x^2") - nur eine Zeile
    - Power: f.get_scheitelpunkt() - volle Funktionalität der spezialisierten Klasse
    - Pädagogisch perfekt: Schüler lernen mit einfachen Aufrufen, bekommen aber alle Spezialmethoden

    Examples:
        >>> f = Funktion("x^2 + 1")              # Gibt automatisch QuadratischeFunktion zurück!
        >>> g = Funktion("2x + 3")                # Gibt automatisch LineareFunktion zurück!
        >>> h = Funktion("(x^2 + 1)/(x - 1)")    # Gebrochen-rationale Funktion
        >>> i = Funktion("exp(x) + 1")           # Exponentiale Funktion
        >>> j = Funktion("sin(x)")                # Trigonometrische Funktion

        Automatische Funktionalität:
        >>> f = Funktion("x^2 - 4x + 3")
        >>> type(f)                              # <class 'schul_analysis.quadratisch.QuadratischeFunktion'>
        >>> f.get_scheitelpunkt()                 # (2.0, -1.0) - nur bei QuadratischeFunktion verfügbar!

        >>> g = Funktion("2x + 5")
        >>> type(g)                              # <class 'schul_analysis.lineare.LineareFunktion'>
        >>> g.steigung                           # 2 - nur bei LineareFunktion verfügbar!
    """

    def __new__(cls, *args, **kwargs):
        """
        Magic Factory - Funktion() Konstruktor gibt automatisch richtige Unterklasse zurück!

        This makes Funktion("x^2") return a QuadratischeFunktion automatically
        while keeping the simple API for users.

        Extended with automatic structure detection for products, sums, quotients, compositions.
        """
        # Wenn es bereits eine Instanz ist, gib sie zurück
        if cls is not Funktion:
            return super().__new__(cls)

        # Extrahiere eingabe und nenner aus den Argumenten
        eingabe = kwargs.get("eingabe", args[0] if args else None)
        nenner = kwargs.get("nenner", args[1] if len(args) > 1 else None)

        # Intelligente Typenerkennung und automatische Instanziierung
        try:
            # Erstelle temporäre Basis-Funktion zur Analyse
            temp_funktion = object.__new__(Funktion)
            temp_funktion._initialisiere_basiskomponenten()
            temp_funktion._verarbeite_eingabe(eingabe, nenner)
            temp_funktion._erstelle_symbole_ausdruecke()

            # Importiere spezialisierte Klassen
            from .ganzrationale import GanzrationaleFunktion
            from .lineare import LineareFunktion
            from .quadratisch import QuadratischeFunktion
            from .exponential import ExponentialFunktion
            from .trigonometrisch import TrigonometrischeFunktion
            from .strukturiert import (
                ProduktFunktion,
                SummeFunktion,
                QuotientFunktion,
                KompositionFunktion,
            )

            # Automatische Typenerkennung - Prioritätenreihenfolge:

            # 1. Spezialisierte Typen (Lineare/Quadratische haben höchste Priorität)
            if temp_funktion.ist_linear():
                # Lineare Funktion -> LineareFunktion
                return LineareFunktion(eingabe)
            elif temp_funktion.ist_quadratisch():
                # Quadratische Funktion -> QuadratischeFunktion
                return QuadratischeFunktion(eingabe)

            # 2. Strukturierte Typen (Produkte, Summen, Quotienten, Kompositionen)
            # Diese Analyse muss nach der Grundfunktions-Analyse erfolgen
            struktur_info = None
            try:
                from .struktur import analysiere_funktionsstruktur

                struktur_info = analysiere_funktionsstruktur(temp_funktion)

                # Nur für komplexe Strukturen strukturierte Klassen verwenden
                if struktur_info["struktur"] in [
                    "produkt",
                    "summe",
                    "quotient",
                    "komposition",
                ]:
                    if struktur_info["struktur"] == "produkt":
                        return ProduktFunktion(eingabe, struktur_info)
                    elif struktur_info["struktur"] == "summe":
                        return SummeFunktion(eingabe, struktur_info)
                    elif struktur_info["struktur"] == "quotient":
                        return QuotientFunktion(eingabe, struktur_info)
                    elif struktur_info["struktur"] == "komposition":
                        return KompositionFunktion(eingabe, struktur_info)
            except Exception:
                # Bei Fehlern in der Strukturanalyse: weiter mit anderer Typenerkennung
                pass

            # 3. Grundfunktionen (ganzrational, exponential, trigonometrisch)
            if temp_funktion.ist_ganzrational:
                # Andere ganzrationale Funktion -> GanzrationaleFunktion
                return GanzrationaleFunktion(eingabe)
            elif temp_funktion.ist_exponential_rational:
                # Exponentialfunktion
                return ExponentialFunktion(eingabe)
            elif temp_funktion.ist_trigonometrisch:
                # Trigonometrische Funktion
                return TrigonometrischeFunktion(eingabe)

            # 4. Basis-Funktion für alle anderen Fälle
            return super().__new__(cls)

        except Exception:
            # Bei Fehlern bei der Typenerkennung: verwende Basis-Funktion
            return super().__new__(cls)

    def __init__(
        self,
        eingabe: Union[str, sp.Basic, "Funktion", tuple[str, str], None] = None,
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
        # Echte Unified Architecture - Keine Wrapper-Delegation mehr!

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
        """Parset String-Eingabe zu SymPy-Ausdruck mit deutschen Fehlermeldungen"""
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
            # Pädagogische Fehlermeldungen
            if "SyntaxError" in str(e) or "invalid syntax" in str(e):
                raise ValueError(
                    f"Syntaxfehler in '{eingabe}'. "
                    "Bitte überprüfe deine Eingabe. Häufige Fehler:\n"
                    "- Klammern müssen paaren: (2x+3) statt (2x+3\n"
                    "- Operatoren brauchen zwei Zahlen: 2*x statt 2x\n"
                    "- Nur mathematische Zeichen verwenden"
                )
            elif "Symbol" in str(e) or "symbol" in str(e):
                # Finde ungültige Symbole
                import re

                gefunden = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", bereinigt)
                erlaubte = {"x", "a", "b", "c", "k", "m", "n", "p", "q", "t", "y", "z"}
                ungueltige = [s for s in gefunden if s not in erlaubte]
                if ungueltige:
                    raise ValueError(
                        f"Unbekannte Variable(n) '{', '.join(ungueltige)}' in '{eingabe}'. "
                        "Erlaubte Variablen sind: x, a, b, c, k, m, n, p, q, t, y, z.\n"
                        "Hast du dich vielleicht vertippt?"
                    )
                else:
                    raise ValueError(
                        f"Unbekanntes Symbol in '{eingabe}'. "
                        "Bitte überprüfe deine Eingabe auf Tippfehler."
                    )
            else:
                raise ValueError(f"Kann '{eingabe}' nicht verarbeiten: {e}")

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

    # Kernfunktionalität - Alle zentral in einer Klasse!

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
            return Ergebnis  # Behalte exakte SymPy-Werte bei
        except Exception as e:
            # Pädagogische Fehlermeldungen
            if "division by zero" in str(e).lower():
                raise ValueError(
                    f"Division durch Null bei f({x_wert}). "
                    "Die Funktion ist an dieser Stelle nicht definiert. "
                    "Überprüfe, ob der Nenner an dieser Stelle Null wird."
                )
            elif "complex" in str(e).lower() or "imaginary" in str(e).lower():
                raise ValueError(
                    f"Komplexes Ergebnis bei f({x_wert}). "
                    "Die Funktion liefert an dieser Stelle eine komplexe Zahl. "
                    "Für reelle Funktionen ist dies möglicherweise nicht definiert."
                )
            else:
                raise ValueError(f"Fehler bei Berechnung von f({x_wert}): {e}")

    def ableitung(self, ordnung: int = 1) -> "Funktion":
        """Berechnet die Ableitung"""
        abgeleiteter_term = diff(self.term_sympy, self._variable_symbol, ordnung)
        return Funktion(abgeleiteter_term)

    def nullstellen(self) -> list:
        """Berechnet die Nullstellen"""
        try:
            lösungen = solve(self.term_sympy, self._variable_symbol)
            return [lösung for lösung in lösungen if lösung.is_real]
        except Exception:
            return []

    # Typenerkennung - Alle zentral!

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

    # Introspektive Methoden für Factory-Funktion

    def ist_linear(self) -> bool:
        """Prüft, ob die Funktion linear ist (ax + b)"""
        if not self.ist_ganzrational:
            return False

        # Prüfe Grad (muss 1 sein)
        try:
            grad = self.term_sympy.as_poly(self._variable_symbol).degree()
            return grad == 1
        except Exception:
            return False

    def ist_quadratisch(self) -> bool:
        """Prüft, ob die Funktion quadratisch ist (ax² + bx + c)"""
        if not self.ist_ganzrational:
            return False

        try:
            grad = self.term_sympy.as_poly(self._variable_symbol).degree()
            return grad == 2
        except Exception:
            return False

    def ist_kubisch(self) -> bool:
        """Prüft, ob die Funktion kubisch ist (ax³ + bx² + cx + d)"""
        if not self.ist_ganzrational:
            return False

        try:
            grad = self.term_sympy.as_poly(self._variable_symbol).degree()
            return grad == 3
        except Exception:
            return False

    def grad(self) -> int:
        """Gibt den Grad des Polynoms zurück"""
        if not self.ist_ganzrational:
            return 0

        try:
            return self.term_sympy.as_poly(self._variable_symbol).degree()
        except Exception:
            return 0

    # Hilfsmethoden

    def __str__(self):
        return self.term()

    def __repr__(self):
        return f"Funktion('{self.term()}')"

    def __eq__(self, other):
        if not isinstance(other, Funktion):
            return False
        return self.term_sympy.equals(other.term_sympy)


# Factory-Funktion für Konsistenz und Abwärtskompatibilität


def erstelle_funktion_automatisch(
    eingabe: Union[str, sp.Basic, "Funktion", tuple[str, str], None],
    nenner: Union[str, sp.Basic, "Funktion", None] = None,
) -> Funktion:
    """
    Magic Factory Wrapper - Einfache Schnittstelle zur automatischen Funktionserstellung.

    Diese Funktion ist nur ein Wrapper für die Magie des Funktion() Konstruktors.
    Seit der Magic Factory Implementation kann man einfach Funktion(eingabe) verwenden!

    Args:
        eingabe: String, SymPy-Ausdruck, Funktion-Objekt oder Tuple (zaehler, nenner)
        nenner: Optionaler Nenner (wenn eingabe nur Zähler ist)

    Returns:
        Funktion: Automatisch erkannte und erstellte Funktion (spezialisierte Klasse)

    Examples:
        >>> f = erstelle_funktion_automatisch("x^2 - 4x + 3")
        >>> type(f)  # <class 'schul_analysis.quadratisch.QuadratischeFunktion'>
        >>> f.get_scheitelpunkt()  # (2.0, -1.0)

        >>> g = erstelle_funktion_automatisch("2x + 5")
        >>> type(g)  # <class 'schul_analysis.lineare.LineareFunktion'>
        >>> g.steigung  # 2

    Magic Factory Tipp:
        Seit der Magic Factory kannst du auch einfach schreiben:
        >>> f = Funktion("x^2 - 4x + 3")  # Gibt automatisch QuadratischeFunktion zurück!
    """
    # Delegiere an die Magie des Konstruktors
    return Funktion(eingabe, nenner)
