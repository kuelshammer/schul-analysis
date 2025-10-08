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
from .sympy_types import (
    VALIDATION_EXACT,
    ExactNullstellenListe,
    ExtremumTyp,
    Sattelpunkt,
    SattelpunkteListe,
    StationaereStelle,
    StationaereStellenListe,
    preserve_exact_types,
    validate_exact_results,
    validate_function_result,
)


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

    @preserve_exact_types
    def ableitung(self, ordnung: int = 1) -> "Funktion":
        """
        Berechnet die Ableitung mit exakten SymPy-Ergebnissen.

        Args:
            ordnung: Ordnung der Ableitung

        Returns:
            Neue Funktion mit der abgeleiteten Funktion als exakter SymPy-Ausdruck
        """
        abgeleiteter_term = diff(self.term_sympy, self._variable_symbol, ordnung)

        # Validiere das Ergebnis
        validate_function_result(abgeleiteter_term, VALIDATION_EXACT)

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
        """
        Berechnet die Ableitung mit exakten SymPy-Ergebnissen (Alias für ableitung).

        Args:
            ordnung: Ordnung der Ableitung

        Returns:
            Neue Funktion mit der abgeleiteten Funktion als exakter SymPy-Ausdruck
        """
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
    @preserve_exact_types
    def nullstellen(self) -> ExactNullstellenListe:
        """
        Berechnet die Nullstellen mit exakten SymPy-Ergebnissen.

        Returns:
            Liste der exakten Nullstellen als SymPy-Ausdrücke
        """
        try:
            lösungen = solve(self.term_sympy, self._variable_symbol)
            # Filtere reelle Lösungen
            ergebnisse = [lösung for lösung in lösungen if lösung.is_real]

            # Validiere die Ergebnisse
            validate_exact_results(ergebnisse, "Nullstellen")

            return ergebnisse
        except Exception as e:
            raise ValueError(
                f"Fehler bei der Nullstellenberechnung: {str(e)}\n"
                "Tipp: Die Funktion kann möglicherweise nicht symbolisch gelöst werden."
            ) from e

    def Nullstellen(self) -> ExactNullstellenListe:
        """
        Berechnet die Nullstellen mit exakten SymPy-Ergebnissen (Alias für nullstellen).

        Returns:
            Liste der exakten Nullstellen als SymPy-Ausdrücke
        """
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
            reelle_punkte = []
            for p in kritische_punkte:
                # Für pädagogische Zwecke: Wir gehen davon aus, dass Parameter reell sind
                if p.is_real is not False:  # Akzeptiere None (unbekannt) und True
                    # Wenn der Punkt Symbole enthält, gehe davon aus, dass sie reell sind
                    if p.free_symbols:
                        # Erstelle reelle Symbole für die Parameter
                        reelle_punkte.append(p)
                    elif p.is_real:
                        reelle_punkte.append(p)

            # Bestimme Art der Extremstellen durch zweite Ableitung
            f_doppelstrich = sp.diff(f_strich, self._variable_symbol)
            extremstellen = []

            for punkt in reelle_punkte:
                try:
                    # Werte zweite Ableitung an diesem Punkt aus
                    wert = f_doppelstrich.subs(self._variable_symbol, punkt)

                    # Bestimme die Art der Extremstelle
                    if wert.is_number:
                        # Numerischer Wert - direkter Vergleich möglich
                        if wert > 0:
                            art = "Minimum"
                        elif wert < 0:
                            art = "Maximum"
                        else:
                            art = "Sattelpunkt"
                    else:
                        # Symbolischer Wert - versuche zu vereinfachen oder Annahmen zu treffen
                        try:
                            # Versuche den Ausdruck zu vereinfachen
                            wert_simplified = sp.simplify(wert)

                            # Für pädagogische Zwecke: gehe davon aus, dass Parameter > 0
                            # Dies ist eine Annahme, die für Schulzwecke sinnvoll ist
                            if wert_simplified.is_positive:
                                art = "Minimum"
                            elif wert_simplified.is_negative:
                                art = "Maximum"
                            else:
                                # Wenn keine klare Aussage möglich ist, nutze die allgemeine Form
                                # Für quadratische Funktionen: a > 0 -> Minimum, a < 0 -> Maximum
                                art = "Minimum/Maximum (abhängig von Parameter)"
                        except Exception:
                            # Bei komplexen symbolischen Ausdrücken
                            art = "Extremum (Art hängt von Parametern ab)"

                    # Behalte exakte symbolische Ergebnisse bei
                    # Konvertiere nur zu Float, wenn es sich um eine reine Zahl handelt
                    # und keine Parameter oder komplexen Ausdrücke enthält
                    # BEWAREARE: Behalte Brüche und exakte Darstellungen bei!
                    if punkt.is_number and not punkt.free_symbols:
                        # Prüfe, ob es sich um einen "schönen" exakten Wert handelt
                        if isinstance(punkt, (sp.Rational, sp.Integer)) or (
                            hasattr(punkt, "q") and hasattr(punkt, "p")  # Bruch-Form
                        ):
                            # Behalte exakte Form bei (Bruch, Integer)
                            x_wert = punkt
                        else:
                            # Konvertiere zu Float (für Dezimalzahlen)
                            x_wert = float(punkt)
                    else:
                        # Behalte symbolischen Ausdruck bei (enthält Parameter oder ist komplex)
                        x_wert = punkt

                    extremstellen.append((x_wert, art))
                except Exception:
                    # Bei Berechnungsfehlern überspringen wir den Punkt
                    # Debug-Info für Entwicklung
                    # print(f"Fehler bei Punkt {punkt}: {e}")
                    continue

            return extremstellen

        except Exception:
            # Bei Fehlern leere Liste zurückgeben
            return []

    def Extremstellen(self) -> list[tuple[Any, str]]:
        """Berechnet die Extremstellen (Alias für extremstellen)"""
        return self.extremstellen

    @property
    def wendepunkte(self) -> list[tuple[Any, Any, str]]:
        """
        Berechnet die Wendepunkte der Funktion.

        Returns:
            Liste von (x_wert, y_wert, art) Tupeln, wobei art "Wendepunkt" ist

        Examples:
            >>> f = Funktion("x^3 - 3x^2 + 2")
            >>> wendepunkte = f.wendepunkte  # [(1.0, 0.0, "Wendepunkt")]
        """
        try:
            # Berechne zweite Ableitung
            f2 = self.ableitung(2)

            # Löse f''(x) = 0 - verwende solve statt nullstellen für parametrisierte Funktionen
            import sympy as sp

            kritische_punkte = sp.solve(f2.term_sympy, self._variable_symbol)

            # Bestimme Wendepunkte durch dritte Ableitung
            f3 = self.ableitung(3)
            wendepunkte = []

            for punkt in kritische_punkte:
                try:
                    # Werte dritte Ableitung an diesem Punkt aus
                    # Wenn f'''(x) ≠ 0, dann ist es ein Wendepunkt
                    wert_f3 = f3.wert(punkt)

                    # Prüfe, ob dritte Ableitung ungleich null ist
                    ist_wendepunkt = False

                    if wert_f3.is_number:
                        # Numerischer Wert - direkter Vergleich möglich
                        if wert_f3 != 0:
                            ist_wendepunkt = True
                    else:
                        # Symbolischer Wert - versuche zu vereinfachen
                        try:
                            wert_f3_simplified = sp.simplify(wert_f3)
                            # Für pädagogische Zwecke: gehe davon aus, dass Parameter ≠ 0
                            # Dies ist eine Annahme, die für Schulzwecke sinnvoll ist
                            if not wert_f3_simplified.equals(0):
                                ist_wendepunkt = True
                        except Exception:
                            # Bei komplexen symbolischen Ausdrücken
                            # gehe davon aus, dass es ein Wendepunkt ist
                            # (für pädagogische Zwecke)
                            ist_wendepunkt = True

                    if ist_wendepunkt:
                        # Berechne y-Wert
                        y_wert = self.wert(punkt)

                        # Behalte exakte symbolische Ergebnisse bei
                        # Konvertiere nur zu Float, wenn es sich um eine reine Zahl handelt
                        if punkt.is_number and not punkt.free_symbols:
                            # Prüfe, ob es sich um einen "schönen" exakten Wert handelt
                            if isinstance(punkt, (sp.Rational, sp.Integer)) or (
                                hasattr(punkt, "q")
                                and hasattr(punkt, "p")  # Bruch-Form
                            ):
                                # Behalte exakte Form bei (Bruch, Integer)
                                x_wert = punkt
                            else:
                                # Konvertiere zu Float (für Dezimalzahlen)
                                x_wert = float(punkt)
                        else:
                            # Behalte symbolischen Ausdruck bei (enthält Parameter oder ist komplex)
                            x_wert = punkt

                        wendepunkte.append((x_wert, y_wert, "Wendepunkt"))
                except Exception:
                    # Bei Berechnungsfehlern überspringen wir den Punkt
                    continue

            return sorted(
                wendepunkte, key=lambda p: p[0] if isinstance(p[0], (int, float)) else 0
            )

        except Exception:
            # Bei Fehlern leere Liste zurückgeben
            return []

    def Wendepunkte(self) -> list[tuple[Any, Any, str]]:
        """Berechnet die Wendepunkte (Alias für wendepunkte)"""
        return self.wendepunkte

    @property
    @preserve_exact_types
    def stationaere_stellen(self) -> StationaereStellenListe:
        """
        Berechnet die stationären Stellen der Funktion mit exakten DataClasses.

        Stationäre Stellen sind alle Punkte, an denen die erste Ableitung null ist (f'(x) = 0).
        Dies entspricht den kritischen Punkten, die bereits in extremstellen berechnet werden.

        Returns:
            StationaereStellenListe mit strukturierten StationaereStelle-Objekten

        Examples:
            >>> f = Funktion("x^2")
            >>> stationaere_stellen = f.stationaere_stellen  # [StationaereStelle(x=0, typ=ExtremumTyp.MINIMUM)]
            >>> f = Funktion("x^3")
            >>> stationaere_stellen = f.stationaere_stellen  # [StationaereStelle(x=0, typ=ExtremumTyp.SATTELPUNKT)]
        """
        # Konvertiere extremstellen-Tupel zu StationaereStelle-Objekten
        stationaere_stellen_liste = []

        for x_wert, art in self.extremstellen:
            # Konvertiere String zu ExtremumTyp Enum
            if art == "Minimum":
                extremum_typ = ExtremumTyp.MINIMUM
            elif art == "Maximum":
                extremum_typ = ExtremumTyp.MAXIMUM
            elif art == "Sattelpunkt":
                extremum_typ = ExtremumTyp.SATTELPUNKT
            else:
                # Fallback für unbekannte Typen
                extremum_typ = ExtremumTyp.SATTELPUNKT

            # Erstelle strukturiertes StationaereStelle-Objekt
            stationaere_stelle = StationaereStelle(
                x=x_wert,
                typ=extremum_typ,
                exakt=True,  # Exakte Berechnung garantiert
            )
            stationaere_stellen_liste.append(stationaere_stelle)

        return stationaere_stellen_liste

    def StationaereStellen(self) -> StationaereStellenListe:
        """Berechnet die stationären Stellen (Alias für stationaere_stellen)"""
        return self.stationaere_stellen

    @property
    @preserve_exact_types
    def sattelpunkte(self) -> SattelpunkteListe:
        """
        Berechnet die Sattelpunkte der Funktion mit exakten DataClasses.

        Sattelpunkte sind spezielle stationäre Stellen, die zusätzlich Wendepunkte sind:
        - f'(x) = 0 (stationär)
        - f''(x) = 0 (Wendepunkt)
        - f'''(x) ≠ 0 (echter Wendepunkt)

        Returns:
            SattelpunkteListe mit strukturierten Sattelpunkt-Objekten

        Examples:
            >>> f = Funktion("x^3")
            >>> sattelpunkte = f.sattelpunkte  # [Sattelpunkt(x=0, y=0, exakt=True)]
        """
        try:
            # Finde alle stationären Stellen (f'(x) = 0)
            stationaere_punkte = self.stationaere_stellen

            sattelpunkte = []
            fehlerhafte_punkte = []  # Für Debugging-Informationen

            for stationaere_stelle in stationaere_punkte:
                x_wert = stationaere_stelle.x

                # Verwende die sichere Prüfmethode
                ist_sattelpunkt, status = self._ist_sattelpunkt_sicher(x_wert)

                if ist_sattelpunkt:
                    try:
                        # Berechne y-Wert mit spezifischer Fehlerbehandlung
                        y_wert = self.wert(x_wert)

                        # Behalte exakte symbolische Ergebnisse bei
                        if x_wert.is_number and not x_wert.free_symbols:
                            # Prüfe, ob es sich um einen "schönen" exakten Wert handelt
                            if isinstance(x_wert, (sp.Rational, sp.Integer)) or (
                                hasattr(x_wert, "q")
                                and hasattr(x_wert, "p")  # Bruch-Form
                            ):
                                # Behalte exakte Form bei (Bruch, Integer)
                                x_final = x_wert
                            else:
                                # Konvertiere zu Float (für Dezimalzahlen)
                                x_final = float(x_wert)
                        else:
                            # Behalte symbolischen Ausdruck bei
                            x_final = x_wert

                        # Erstelle strukturiertes Sattelpunkt-Objekt
                        sattelpunkt = Sattelpunkt(
                            x=x_wert,  # Immer den ursprünglichen x_wert verwenden (T_Expr)
                            y=y_wert,
                            exakt=True,  # Exakte Berechnung garantiert
                        )
                        sattelpunkte.append(sattelpunkt)
                    except (ValueError, TypeError, ZeroDivisionError) as e:
                        # Spezifische Fehler bei y-Wert-Berechnung
                        fehlerhafte_punkte.append(
                            (x_wert, f"y-Wert Fehler: {type(e).__name__}")
                        )
                        continue
                else:
                    # Für Debugging: Punkte die keine Sattelpunkte sind
                    fehlerhafte_punkte.append((x_wert, status))

            return sorted(
                sattelpunkte,
                key=lambda p: p.x if isinstance(p.x, (int, float)) else 0,
            )

        except (ValueError, TypeError, AttributeError, sp.SympifyError):
            # Spezifische Fehler abfangen
            return []
        except Exception:
            # Nur für wirklich unerwartete Fehler
            return []

    def Sattelpunkte(self) -> SattelpunkteListe:
        """Berechnet die Sattelpunkte (Alias für sattelpunkte)"""
        return self.sattelpunkte

    def _ist_sattelpunkt_sicher(self, x_wert: Any) -> tuple[bool, str]:
        """
        Sichere Prüfung auf Sattelpunkt mit Status-Rückgabe.

        Mathematische Kriterien:
        - f'(x) = 0 (bereits durch stationaere_stellen erfüllt)
        - f''(x) = 0
        - f'''(x) ≠ 0

        Args:
            x_wert: Der zu prüfende x-Wert

        Returns:
            (ist_sattelpunkt, status_beschreibung)
        """
        try:
            # Zweite Ableitung muss null sein
            f2 = self.ableitung(2)
            f2_wert = f2.wert(x_wert)
            f2_simplified = sp.simplify(f2_wert)

            if not f2_simplified.equals(0):
                return False, "f''(x) ≠ 0"

            # Dritte Ableitung muss ungleich null sein
            f3 = self.ableitung(3)
            f3_wert = f3.wert(x_wert)
            f3_simplified = sp.simplify(f3_wert)

            if f3_simplified.is_number:
                # Numerisch prüfbar
                if f3_simplified != 0:
                    return True, "f'''(x) ≠ 0 (numerisch)"
                else:
                    return False, "f'''(x) = 0 (kein Sattelpunkt)"
            else:
                # Symbolisch prüfen
                if f3_simplified.equals(0):
                    return False, "f'''(x) = 0 (symbolisch, kein Sattelpunkt)"
                else:
                    # Nur als Sattelpunkt zählen wenn eindeutig ≠ 0
                    return True, "f'''(x) ≠ 0 (symbolisch)"

        except (ValueError, TypeError, ZeroDivisionError, sp.SympifyError) as e:
            return False, f"Berechnungsfehler: {type(e).__name__}"
        except Exception as e:
            return False, f"Unerwarteter Fehler: {type(e).__name__}"

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

    def ausmultiplizieren(self):
        """
        Multipliziert den aktuellen SymPy-Ausdruck aus und ersetzt ihn durch die expandierte Form.

        Diese Methode ist nützlich für pädagogische Zwecke, wenn Schüler die ausmultiplizierte
        Form einer Funktion sehen müssen, anstatt der faktorisierten Darstellung.

        Returns:
            Selbst (die Funktion mit ausmultipliziertem Term)

        Examples:
            >>> f = Funktion("(x+1)(x-2)")
            >>> print(f.term())  # (x + 1)*(x - 2)
            >>> f.ausmultiplizieren()
            >>> print(f.term())  # x^2 - x - 2

            >>> g = Funktion("(x+1)^3")
            >>> print(g.term())  # (x + 1)^3
            >>> g.ausmultiplizieren()
            >>> print(g.term())  # x^3 + 3*x^2 + 3*x + 1

        Didaktischer Hinweis:
            Das Ausmultiplizieren hilft bei der Umwandlung von Produktform in die
        Normalform und ist wichtig für das Verständnis von Polynom-Operationen.
        """
        import sympy as sp

        # Wende SymPy's expand-Funktion auf den aktuellen Term an
        expandierter_term = sp.expand(self.term_sympy)

        # Aktualisiere den internen SymPy-Ausdruck
        self.term_sympy = expandierter_term

        # Setze den Term-String zurück, damit er neu generiert wird
        if hasattr(self, "_term"):
            self._term = None

        # Setze auch den gecachten LaTeX-Ausdruck zurück
        if hasattr(self, "_latex_expr"):
            self._latex_expr = None

        return self

    # =============================================================================
    # ARITHMETISCHE OPERATIONEN - SymPy-basierte Funktionsoperationen
    # =============================================================================

    def __add__(self, other):
        """
        Addition: f + g

        Args:
            other: Andere Funktion, Zahl oder SymPy-Ausdruck

        Returns:
            Neue Funktion mit Ergebnis der Addition

        Examples:
            >>> f = Funktion("x^2")
            >>> g = Funktion("3x + 4")
            >>> h = f + g  # x^2 + 3x + 4
        """
        try:
            if isinstance(other, Funktion):
                # Funktion + Funktion
                result_expr = self.term_sympy + other.term_sympy
                return Funktion(result_expr)
            elif isinstance(other, (int, float)):
                # Funktion + Zahl
                result_expr = self.term_sympy + other
                return Funktion(result_expr)
            elif hasattr(other, "_sympy_") or isinstance(other, sp.Basic):
                # Funktion + SymPy-Ausdruck
                result_expr = self.term_sympy + other
                return Funktion(result_expr)
            else:
                return NotImplemented
        except Exception as e:
            raise ValueError(f"Fehler bei Addition: {e}")

    def __radd__(self, other):
        """
        Rechtsseitige Addition: other + f

        Args:
            other: Zahl oder SymPy-Ausdruck

        Returns:
            Neue Funktion mit Ergebnis der Addition

        Examples:
            >>> f = Funktion("x^2")
            >>> h = 5 + f  # 5 + x^2
        """
        try:
            if isinstance(other, (int, float)):
                # Zahl + Funktion
                result_expr = other + self.term_sympy
                return Funktion(result_expr)
            elif hasattr(other, "_sympy_") or isinstance(other, sp.Basic):
                # SymPy-Ausdruck + Funktion
                result_expr = other + self.term_sympy
                return Funktion(result_expr)
            else:
                return NotImplemented
        except Exception as e:
            raise ValueError(f"Fehler bei rechtsseitiger Addition: {e}")

    def __sub__(self, other):
        """
        Subtraktion: f - g

        Args:
            other: Andere Funktion, Zahl oder SymPy-Ausdruck

        Returns:
            Neue Funktion mit Ergebnis der Subtraktion

        Examples:
            >>> f = Funktion("x^2")
            >>> g = Funktion("3x + 4")
            >>> h = f - g  # x^2 - 3x - 4
        """
        try:
            if isinstance(other, Funktion):
                # Funktion - Funktion
                result_expr = self.term_sympy - other.term_sympy
                return Funktion(result_expr)
            elif isinstance(other, (int, float)):
                # Funktion - Zahl
                result_expr = self.term_sympy - other
                return Funktion(result_expr)
            elif hasattr(other, "_sympy_") or isinstance(other, sp.Basic):
                # Funktion - SymPy-Ausdruck
                result_expr = self.term_sympy - other
                return Funktion(result_expr)
            else:
                return NotImplemented
        except Exception as e:
            raise ValueError(f"Fehler bei Subtraktion: {e}")

    def __rsub__(self, other):
        """
        Rechtsseitige Subtraktion: other - f

        Args:
            other: Zahl oder SymPy-Ausdruck

        Returns:
            Neue Funktion mit Ergebnis der Subtraktion

        Examples:
            >>> f = Funktion("x^2")
            >>> h = 10 - f  # 10 - x^2
        """
        try:
            if isinstance(other, (int, float)):
                # Zahl - Funktion
                result_expr = other - self.term_sympy
                return Funktion(result_expr)
            elif hasattr(other, "_sympy_") or isinstance(other, sp.Basic):
                # SymPy-Ausdruck - Funktion
                result_expr = other - self.term_sympy
                return Funktion(result_expr)
            else:
                return NotImplemented
        except Exception as e:
            raise ValueError(f"Fehler bei rechtsseitiger Subtraktion: {e}")

    def __mul__(self, other):
        """
        Multiplikation: f * g

        Args:
            other: Andere Funktion, Zahl oder SymPy-Ausdruck

        Returns:
            Neue Funktion mit Ergebnis der Multiplikation

        Examples:
            >>> f = Funktion("x^2")
            >>> g = Funktion("3x + 4")
            >>> h = f * g  # x^2 * (3x + 4)
        """
        try:
            if isinstance(other, Funktion):
                # Funktion * Funktion
                result_expr = self.term_sympy * other.term_sympy
                return Funktion(result_expr)
            elif isinstance(other, (int, float)):
                # Funktion * Zahl
                result_expr = self.term_sympy * other
                return Funktion(result_expr)
            elif hasattr(other, "_sympy_") or isinstance(other, sp.Basic):
                # Funktion * SymPy-Ausdruck
                result_expr = self.term_sympy * other
                return Funktion(result_expr)
            else:
                return NotImplemented
        except Exception as e:
            raise ValueError(f"Fehler bei Multiplikation: {e}")

    def __rmul__(self, other):
        """
        Rechtsseitige Multiplikation: other * f

        Args:
            other: Zahl oder SymPy-Ausdruck

        Returns:
            Neue Funktion mit Ergebnis der Multiplikation

        Examples:
            >>> f = Funktion("x^2")
            >>> h = 5 * f  # 5 * x^2
        """
        try:
            if isinstance(other, (int, float)):
                # Zahl * Funktion
                result_expr = other * self.term_sympy
                return Funktion(result_expr)
            elif hasattr(other, "_sympy_") or isinstance(other, sp.Basic):
                # SymPy-Ausdruck * Funktion
                result_expr = other * self.term_sympy
                return Funktion(result_expr)
            else:
                return NotImplemented
        except Exception as e:
            raise ValueError(f"Fehler bei rechtsseitiger Multiplikation: {e}")

    def __truediv__(self, other):
        """
        Division: f / g

        Args:
            other: Andere Funktion, Zahl oder SymPy-Ausdruck

        Returns:
            Neue Funktion mit Ergebnis der Division

        Examples:
            >>> f = Funktion("x^2")
            >>> g = Funktion("3x + 4")
            >>> h = f / g  # x^2 / (3x + 4)
        """
        try:
            if isinstance(other, Funktion):
                # Funktion / Funktion
                result_expr = self.term_sympy / other.term_sympy
                return Funktion(result_expr)
            elif isinstance(other, (int, float)):
                if other == 0:
                    raise ZeroDivisionError("Division durch Null")
                # Funktion / Zahl
                result_expr = self.term_sympy / other
                return Funktion(result_expr)
            elif hasattr(other, "_sympy_") or isinstance(other, sp.Basic):
                # Funktion / SymPy-Ausdruck
                result_expr = self.term_sympy / other
                return Funktion(result_expr)
            else:
                return NotImplemented
        except ZeroDivisionError:
            raise
        except Exception as e:
            raise ValueError(f"Fehler bei Division: {e}")

    def __rtruediv__(self, other):
        """
        Rechtsseitige Division: other / f

        Args:
            other: Zahl oder SymPy-Ausdruck

        Returns:
            Neue Funktion mit Ergebnis der Division

        Examples:
            >>> f = Funktion("x^2")
            >>> h = 10 / f  # 10 / x^2
        """
        try:
            if isinstance(other, (int, float)):
                # Zahl / Funktion
                if self.term_sympy.is_zero:
                    raise ZeroDivisionError("Division durch Null")
                result_expr = other / self.term_sympy
                return Funktion(result_expr)
            elif hasattr(other, "_sympy_") or isinstance(other, sp.Basic):
                # SymPy-Ausdruck / Funktion
                if self.term_sympy.is_zero:
                    raise ZeroDivisionError("Division durch Null")
                result_expr = other / self.term_sympy
                return Funktion(result_expr)
            else:
                return NotImplemented
        except ZeroDivisionError:
            raise
        except Exception as e:
            raise ValueError(f"Fehler bei rechtsseitiger Division: {e}")

    def __pow__(self, exponent):
        """
        Potenzierung: f ** exponent

        Args:
            exponent: Zahl (int, float)

        Returns:
            Neue Funktion mit Ergebnis der Potenzierung

        Examples:
            >>> f = Funktion("sin(x)")
            >>> h = f ** 2  # sin(x)^2
        """
        try:
            if isinstance(exponent, (int, float)):
                # Funktion ** Zahl
                result_expr = self.term_sympy**exponent
                return Funktion(result_expr)
            elif hasattr(exponent, "_sympy_") or isinstance(exponent, sp.Basic):
                # Funktion ** SymPy-Ausdruck
                result_expr = self.term_sympy**exponent
                return Funktion(result_expr)
            else:
                return NotImplemented
        except Exception as e:
            raise ValueError(f"Fehler bei Potenzierung: {e}")

    def __rpow__(self, base):
        """
        Rechtsseitige Potenzierung: base ** f

        Args:
            base: Zahl oder SymPy-Ausdruck

        Returns:
            Neue Funktion mit Ergebnis der Potenzierung

        Examples:
            >>> f = Funktion("x")
            >>> h = 2 ** f  # 2^x
        """
        try:
            if isinstance(base, (int, float)):
                # Zahl ** Funktion
                result_expr = base**self.term_sympy
                return Funktion(result_expr)
            elif hasattr(base, "_sympy_") or isinstance(base, sp.Basic):
                # SymPy-Ausdruck ** Funktion
                result_expr = base**self.term_sympy
                return Funktion(result_expr)
            else:
                return NotImplemented
        except Exception as e:
            raise ValueError(f"Fehler bei rechtsseitiger Potenzierung: {e}")

    def __matmul__(self, other):
        """
        Funktionskomposition: f @ g (f ∘ g)

        Args:
            other: Andere Funktion

        Returns:
            Neue Funktion mit Ergebnis der Komposition

        Examples:
            >>> f = Funktion("x^2")
            >>> g = Funktion("sin(x)")
            >>> h = f @ g  # sin(x)^2
        """
        try:
            if isinstance(other, Funktion):
                # f ∘ g = f(g(x))
                result_expr = self.term_sympy.subs(
                    self._variable_symbol, other.term_sympy
                )
                return Funktion(result_expr)
            else:
                return NotImplemented
        except Exception as e:
            raise ValueError(f"Fehler bei Funktionskomposition: {e}")


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
