"""
Vereinheitliche Funktionsklasse für das Schul-Analysis Framework.

Dies ist die zentrale, echte unified Klasse - keine Wrapper-Logik mehr!
Alle spezialisierten Klassen erben von dieser Basis-Klasse.
"""

from typing import Any, Union

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
            from .exponential import ExponentialFunktion
            from .ganzrationale import GanzrationaleFunktion
            from .lineare import LineareFunktion
            from .quadratisch import QuadratischeFunktion
            from .strukturiert import (
                KompositionFunktion,
                ProduktFunktion,
                QuotientFunktion,
                SummeFunktion,
            )
            from .trigonometrisch import TrigonometrischeFunktion

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
        self.name = None  # Standardmäßig kein Name

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

    def __call__(self, x_wert, **kwargs):
        """
        Ermöglicht f(x) Syntax für Funktionsauswertung mit optionaler Parameter-Substitution.

        Diese Methode wurde erweitert, um symbolische Ergebnisse zurückzugeben,
        wenn die Funktion noch Parameter enthält.

        Args:
            x_wert: x-Wert für die Auswertung
            **kwargs: Optionale Parameter-Substitution (z.B. a=3)

        Returns:
            Numerisches oder symbolisches Ergebnis

        Examples:
            >>> f = Funktion("a*x^2 + b*x + c")
            >>> f(4)              # 16*a + 4*b + c (symbolisch)
            >>> f(4, a=2)        # 32 + 4*b + c (teilweise substituiert)
            >>> f(4, a=2, b=3)   # 47 (vollständig substituiert)
        """
        # Kombiniere kwargs mit eventuell vorhandenen Parametern
        if kwargs:
            # Erstelle temporäre Funktion mit substituierten Parametern
            temp_funktion = self.setze_parameter(**kwargs)
            return temp_funktion.wert(x_wert)
        else:
            # Normale Auswertung ohne zusätzliche Parameter
            return self.wert(x_wert)

    def wert(self, x_wert):
        """
        Berechnet den Funktionswert an einer Stelle.

        Gibt symbolische Ergebnisse zurück, wenn die Funktion noch Parameter enthält.

        Args:
            x_wert: x-Wert für die Auswertung

        Returns:
            Numerisches oder symbolisches Ergebnis

        Examples:
            >>> f = Funktion("a*x^2 + b*x + c")
            >>> f.wert(4)         # 16*a + 4*b + c
            >>> f2 = f.setze_parameter(a=3)
            >>> f2.wert(4)        # 48 + 4*b + c
        """
        try:
            # Substituiere den x-Wert
            ergebnis = self.term_sympy.subs(self._variable_symbol, x_wert)

            # Vereinfache das Ergebnis
            ergebnis = ergebnis.simplify()

            # Prüfe, ob das Ergebnis noch Parameter enthält
            if ergebnis.free_symbols - {self._variable_symbol}:
                # Symbolisches Ergebnis zurückgeben (mit Parameter)
                return ergebnis
            else:
                # Numerisches Ergebnis zurückgeben
                return ergebnis

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

    def setze_parameter(self, **kwargs):
        """
        Setzt Parameter und gibt neue Funktion zurück.

        Diese Methode ermöglicht die intuitive Manipulation parametrisierter
        Funktionen durch Substitution von Parameterwerten.

        Args:
            **kwargs: Parameter-Wert-Paare (z.B. a=3, b=2)

        Returns:
            Funktion: Neue Funktion mit gesetzten Parametern

        Raises:
            ValueError: Wenn ungültige Parameter angegeben werden

        Examples:
            >>> f = Funktion("a*x^2 + b*x + c")
            >>> f2 = f.setze_parameter(a=3)    # 3*x^2 + b*x + c
            >>> f3 = f.setze_parameter(a=3, b=2)  # 3*x^2 + 2*x + c
            >>> result = f.setze_parameter(a=3)(4)  # 48 + 4b + c

        Didaktischer Hinweis:
            Diese Methode ist perfekt für den Unterricht geeignet, da sie eine
            intuitive Möglichkeit bietet, Parameter in Funktionen zu setzen und
            die Auswirkungen sofort zu sehen. Sie unterstützt typische
            Unterrichtsszenarien wie Parameterbestimmung aus Bedingungen.
        """
        try:
            # Prüfe, ob die angegebenen Parameter existieren
            for param_name in kwargs.keys():
                param_symbol = sp.Symbol(param_name)
                if param_symbol not in self.term_sympy.free_symbols:
                    # Pädagogische Fehlermeldung
                    verfügbare_parameter = [str(p) for p in self.parameter]
                    if verfügbare_parameter:
                        raise ValueError(
                            f"Parameter '{param_name}' kommt in der Funktion "
                            f"f(x) = {self.term()} nicht vor. "
                            f"Verfügbare Parameter: {verfügbare_parameter}"
                        )
                    else:
                        raise ValueError(
                            f"Die Funktion f(x) = {self.term()} hat keine Parameter. "
                            "Nur Funktionen mit Parametern können mit setze_parameter() manipuliert werden."
                        )

            # Führe die Substitution durch
            new_expr = self.term_sympy.subs(kwargs)

            # Erstelle neue Funktion mit dem substituierten Ausdruck
            neue_funktion = Funktion(new_expr)

            return neue_funktion

        except Exception as e:
            if isinstance(e, ValueError):
                # Pädagogische Fehlermeldungen bereits oben
                raise e
            else:
                # Technische Fehler in pädagogischer Form
                raise ValueError(
                    f"Fehler bei der Parameter-Substitution: {str(e)}. "
                    "Bitte überprüfe, ob alle Parameter korrekt angegeben wurden."
                )

    def ableitung(self, ordnung: int = 1) -> "Funktion":
        """Berechnet die Ableitung"""
        abgeleiteter_term = diff(self.term_sympy, self._variable_symbol, ordnung)

        # Erstelle neue Funktion mit Namen
        abgeleitete_funktion = Funktion(abgeleiteter_term)

        # Setze Namen für abgeleitete Funktion
        if hasattr(self, "name") and self.name:
            base_name = self.name
            if ordnung == 1:
                abgeleitete_funktion.name = f"{base_name}'"
            elif ordnung == 2:
                abgeleitete_funktion.name = f"{base_name}''"
            elif ordnung == 3:
                abgeleitete_funktion.name = f"{base_name}'''"
            else:
                abgeleitete_funktion.name = f"{base_name}^{{{ordnung}}}"
        else:
            # Standardnamen wenn kein Basisname vorhanden
            if ordnung == 1:
                abgeleitete_funktion.name = "f'"
            elif ordnung == 2:
                abgeleitete_funktion.name = "f''"
            elif ordnung == 3:
                abgeleitete_funktion.name = "f'''"
            else:
                abgeleitete_funktion.name = f"f^{{{ordnung}}}"

        return abgeleitete_funktion

    def Ableitung(self, ordnung: int = 1) -> "Funktion":
        """Berechnet die Ableitung (Alias für ableitung)"""
        return self.ableitung(ordnung)

    def integral(self, ordnung: int = 1) -> "Funktion":
        """Berechnet das Integral"""
        import sympy as sp

        integrierter_term = sp.integrate(self.term_sympy, self._variable_symbol)
        # Erstelle neue Funktion mit Namen
        integrierte_funktion = Funktion(integrierter_term)
        # Setze Namen für integrierte Funktion
        if hasattr(self, "name") and self.name:
            base_name = self.name
            if ordnung == 1:
                integrierte_funktion.name = f"∫{base_name}"
            else:
                integrierte_funktion.name = f"∫^{ordnung}{base_name}"
        else:
            # Standardnamen wenn kein Basisname vorhanden
            if ordnung == 1:
                integrierte_funktion.name = "∫f"
            else:
                integrierte_funktion.name = f"∫^{ordnung}f"
        return integrierte_funktion

    def Integral(self, ordnung: int = 1) -> "Funktion":
        """Berechnet das Integral (Alias für integral)"""
        return self.integral(ordnung)

    @property
    def nullstellen(self) -> list:
        """Berechnet die Nullstellen"""
        try:
            lösungen = solve(self.term_sympy, self._variable_symbol)
            return [lösung for lösung in lösungen if lösung.is_real]
        except Exception:
            return []

    def Nullstellen(self) -> list:
        """Berechnet die Nullstellen (Alias für nullstellen)"""
        return self.nullstellen

    @property
    def extremstellen(self) -> list[tuple[Any, str]]:
        """
        Berechnet die Extremstellen der Funktion.

        Returns:
            Liste von (x_wert, art) Tupeln, wobei art "Minimum" oder "Maximum" sein kann

        Examples:
            >>> f = Funktion("x^2 - 4x + 3")
            >>> extremstellen = f.extremstellen()  # [(2.0, "Minimum")]
        """
        try:
            # Berechne erste Ableitung
            f_strich = sp.diff(self.term_sympy, self._variable_symbol)

            # Löse f'(x) = 0
            kritische_punkte = solve(f_strich, self._variable_symbol)

            # Filtere reelle Lösungen
            reelle_punkte = [p for p in kritische_punkte if p.is_real]

            # Bestimme Art der Extremstellen durch zweite Ableitung
            f_doppelstrich = sp.diff(f_strich, self._variable_symbol)
            extremstellen = []

            for punkt in reelle_punkte:
                try:
                    # Werte zweite Ableitung an diesem Punkt aus
                    wert = f_doppelstrich.subs(self._variable_symbol, punkt)
                    if wert > 0:
                        art = "Minimum"
                    elif wert < 0:
                        art = "Maximum"
                    else:
                        art = "Sattelpunkt"

                    # Konvertiere zu numerischem Wert wenn möglich
                    if hasattr(punkt, "evalf"):
                        x_wert = punkt.evalf()
                    else:
                        x_wert = float(punkt) if hasattr(punkt, "__float__") else punkt

                    extremstellen.append((x_wert, art))
                except Exception:
                    # Bei Berechnungsfehlern überspringen wir den Punkt
                    continue

            return extremstellen

        except Exception:
            # Bei Fehlern leere Liste zurückgeben
            return []

    def Extremstellen(self) -> list[tuple[Any, str]]:
        """Berechnet die Extremstellen (Alias für extremstellen)"""
        return self.extremstellen

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

    def _repr_latex_(self):
        """
        LaTeX-Darstellung für Jupyter Notebooks und IPython.

        Returns:
            str: LaTeX-String der Funktion
        """
        return self.term_latex()

    def latex_display(self) -> str:
        """
        Gibt die Funktion als formatierten LaTeX-String zurück.

        Speziell für die Darstellung in Marimo mit mo.md() optimiert.

        Returns:
            str: LaTeX-String der Funktion

        Examples:
            >>> f = Funktion("x^2 + 2*x + 1")
            >>> f.latex_display()  # "$x^{2} + 2 x + 1$"
        """
        return f"${self.term_latex()}$"

    def __eq__(self, other):
        if not isinstance(other, Funktion):
            return False
        return self.term_sympy.equals(other.term_sympy)

    def definitionsbereich(self) -> str:
        """Gibt den Definitionsbereich der Funktion zurück."""
        return "ℝ (alle reellen Zahlen)"

    def polstellen(self) -> list:
        """Berechnet die Polstellen der Funktion."""
        # Für allgemeine Funktionen Standard-Implementierung
        return []

    @property
    def wendestellen(self) -> list[tuple[Any, str]]:
        """Berechnet die Wendestellen der Funktion."""
        try:
            # Berechne zweite Ableitung
            f_strich = sp.diff(self.term_sympy, self._variable_symbol)
            f_doppelstrich = sp.diff(f_strich, self._variable_symbol)

            # Löse f''(x) = 0
            kritische_punkte = solve(f_doppelstrich, self._variable_symbol)

            # Filtere reelle Lösungen
            reelle_punkte = [p for p in kritische_punkte if p.is_real]

            wendestellen = []
            for punkt in reelle_punkte:
                try:
                    # Konvertiere zu numerischem Wert wenn möglich
                    if hasattr(punkt, "evalf"):
                        x_wert = punkt.evalf()
                    else:
                        x_wert = float(punkt) if hasattr(punkt, "__float__") else punkt

                    wendestellen.append((x_wert, "Wendepunkt"))
                except Exception:
                    continue

            return wendestellen
        except Exception:
            return []

    def Wendestellen(self) -> list[tuple[Any, str]]:
        """Berechnet die Wendestellen (Alias für wendestellen)."""
        return self.wendestellen

    def zeige_funktion_plotly(self, x_bereich=None, **kwargs):
        """Visualisiert die Funktion mit Plotly."""
        from .visualisierung import Graph

        return Graph(self, x_bereich=x_bereich, **kwargs)

    def graph(self, x_min=None, x_max=None, y_min=None, y_max=None, **kwargs):
        """Visualisiert die Funktion mit Plotly (einheitliche Methode)."""
        from .visualisierung import Graph

        return Graph(self, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, **kwargs)

    def Graph(self, x_min=None, x_max=None, y_min=None, y_max=None, **kwargs):
        """Visualisiert die Funktion mit Plotly (einheitliche Methode)."""
        return self.graph(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, **kwargs)


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
