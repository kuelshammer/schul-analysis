"""
Vereinheitliche Funktionsklasse für ganzrationale und gebrochen-rationale Funktionen.

Diese Klasse vereint die Funktionalität von GanzrationaleFunktion und GebrochenRationaleFunktion
in einer einzigen, konsistenten API.
"""

import random
import re
from typing import Union

import sympy as sp
from sympy import diff, factor, latex, solve, symbols

from .symbolic import _Parameter, _Variable


class Funktion:
    """
    Vereinheitlichte Funktionsklasse für ganzrationale und gebrochen-rationale Funktionen.

    Repräsentiert eine Funktion f(x) = Z(x)/N(x) wobei Z und N ganzrational sind.
    Spezialfall: N(x) = 1 → ganzrationale Funktion

    Examples:
        >>> f = Funktion("x^2 + 1")              # ganzrational
        >>> g = Funktion("(x^2 + 1)/(x - 1)")    # gebrochen-rational
        >>> h = Funktion("x^2", "1")               # explizite Trennung
    """

    def __init__(
        self,
        eingabe: Union[str, sp.Basic, "Funktion", tuple[str, str]],
        nenner: Union[str, sp.Basic, "Funktion"] | None = None,
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
        # 🔥 AUTOMATISCHE FUNKTIONSTYP-ERKENNUNG 🔥

        # Prüfe zuerst auf Exponentialfunktionen
        if self._ist_exponential_funktion(eingabe):
            exp_funktion = self._parse_exponential_funktion(eingabe)
            # Delegiere alle Eigenschaften an die ExponentialRationaleFunktion
            self.__class__ = type(exp_funktion)
            self.__dict__ = exp_funktion.__dict__
            return

        self.x = symbols("x")

        # Interne Symbol-Verwaltung
        self.variablen: list[_Variable] = []
        self.parameter: list[_Parameter] = []
        self.hauptvariable: _Variable | None = None

        # Speichere die ursprüngliche Eingabe
        if isinstance(eingabe, tuple) and len(eingabe) == 2:
            self.original_eingabe = f"({eingabe[0]})/({eingabe[1]})"
        else:
            self.original_eingabe = str(eingabe)

        # Parse die Eingabe
        if isinstance(eingabe, tuple) and len(eingabe) == 2:
            # Explizite Trennung: (zaehler, nenner)
            zaehler_input, nenner_input = eingabe
            self.zaehler = self._parse_zaehler(zaehler_input)
            self.nenner = self._parse_nenner(nenner_input)
        elif isinstance(eingabe, Funktion):
            # Kopie eines existierenden Funktion-Objekts
            self.zaehler = eingabe.zaehler
            self.nenner = eingabe.nenner
            self.variablen = eingabe.variablen.copy()
            self.parameter = eingabe.parameter.copy()
            self.hauptvariable = eingabe.hauptvariable
        else:
            # Einziger String oder SymPy-Ausdruck
            if isinstance(eingabe, str) and "/" in eingabe:
                # Versuche, als Bruch zu parsen
                if self._ist_bruch_string(eingabe):
                    self.zaehler, self.nenner = self._parse_bruch_string(eingabe)
                else:
                    # Behandle als ganzrationalen Ausdruck
                    self.zaehler = self._parse_zaehler(eingabe)
                    self.nenner = self._parse_nenner("1")
            else:
                # Ganzrationaler Fall
                self.zaehler = self._parse_zaehler(eingabe)
                self.nenner = self._parse_nenner("1")

        # Erstelle SymPy-Ausdrücke
        self._erstelle_sympy_ausdruecke()

        # Vereinfache wenn möglich
        self.kürzen()


def erstelle_funktion_automatisch(
    eingabe: Union[str, sp.Basic, tuple[str, str]],
    nenner: Union[str, sp.Basic] | None = None,
):
    """
    Factory-Funktion zur automatischen Erkennung und Erstellung der richtigen Funktionsklasse.

    Dies ist die Hauptfunktion für Schüler - sie erkennen automatisch den Funktionstyp!

    Args:
        eingabe: Die mathematische Funktion als String, SymPy-Ausdruck oder Tuple
                 - "x^2 + 1" für ganzrationale Funktionen
                 - "(x^2 + 1)/(x - 1)" für gebrochen-rationale Funktionen
                 - "exp(x) + 1" für exponential-rationale Funktionen
        nenner: Optionaler Nenner für rationale Funktionen

    Returns:
        Die passende Funktionsklasse mit voller Funktionalität

    Examples:
        >>> f1 = erstelle_funktion_automatisch("x^2 + 2x + 1")  # GanzrationaleFunktion
        >>> f2 = erstelle_funktion_automatisch("(x+1)/(x-1)")  # GebrochenRationaleFunktion
        >>> f3 = erstelle_funktion_automatisch("exp(x) + 1")  # ExponentialRationaleFunktion
    """
    # Prüfe auf Exponentialfunktionen
    if _ist_exponential_funktion_static(eingabe):
        from .gebrochen_rationale import ExponentialRationaleFunktion

        return ExponentialRationaleFunktion._erstelle_aus_string(str(eingabe))

    # Prüfe auf rationale Funktionen
    if isinstance(eingabe, str) and "/" in eingabe and nenner is None:
        from .gebrochen_rationale import GebrochenRationaleFunktion

        try:
            return GebrochenRationaleFunktion(eingabe)
        except:
            # Fallback: Versuche es als ganzrationale Funktion
            pass

    # Standardfall: ganzrationale Funktion
    from .ganzrationale import GanzrationaleFunktion

    return GanzrationaleFunktion(eingabe)


def _ist_exponential_funktion_static(eingabe: Union[str, sp.Basic]) -> bool:
    """Statische Methode zur Prüfung auf Exponentialfunktionen"""
    if isinstance(eingabe, str):
        # Prüfe auf exp() in String
        return "exp(" in eingabe.lower() or "e^" in eingabe.lower()
    elif hasattr(eingabe, "has"):
        # Prüfe auf exp() in SymPy-Ausdruck
        return eingabe.has(sp.exp)

    def _ist_exponential_funktion(self, eingabe: str | sp.Basic) -> bool:
        """Prüft, ob die Eingabe eine Exponentialfunktion enthält"""
        if isinstance(eingabe, str):
            # Prüfe auf exp() in String
            return "exp(" in eingabe or "e^" in eingabe
        elif hasattr(eingabe, "has"):
            # Prüfe auf exp() in SymPy-Ausdruck
            return eingabe.has(sp.exp)
        return False

    def _parse_exponential_funktion(self, eingabe: str | sp.Basic):
        """Parst eine Exponentialfunktion und erstellt das entsprechende Objekt"""
        from .gebrochen_rationale import ExponentialRationaleFunktion

        if isinstance(eingabe, str):
            # Extrahiere den Exponentialparameter und erstelle ExponentialRationaleFunktion
            # Einfache Heuristik: Suche nach exp(x) oder exp(kx)
            import re

            # Finde alle exp() Ausdrücke
            exp_matches = re.findall(r"exp\(([^)]+)\)", eingabe)
            if exp_matches:
                # Bestimme den Exponentialparameter (vereinfacht: nehme den ersten)
                exp_arg = exp_matches[0].strip()

                # Prüfe ob es ein einfaches exp(x) oder exp(kx) ist
                if exp_arg == "x":
                    a_param = 1.0
                elif re.match(r"^\d*\.?\d*\s*\*?\s*x$", exp_arg):
                    # Form wie k*x oder kx
                    coeff_match = re.match(r"^(\d*\.?\d*)\s*\*?\s*x$", exp_arg)
                    if coeff_match:
                        a_param = float(
                            coeff_match.group(1) if coeff_match.group(1) else "1"
                        )
                    else:
                        a_param = 1.0
                else:
                    # Komplexerer Ausdruck - Standardwert verwenden
                    a_param = 1.0

                # Ersetze exp(...) durch temp Variable für die Verarbeitung
                temp_eingabe = re.sub(r"exp\([^)]+\)", "u", eingabe)

                # Erstelle ExponentialRationaleFunktion
                return ExponentialRationaleFunktion(
                    temp_eingabe, "1", exponent_param=a_param
                )

        # Fallback für SymPy-Eingabe
        return ExponentialRationaleFunktion("1", "1", exponent_param=1.0)

    def _parse_zaehler(self, eingabe: str | sp.Basic) -> "Funktion":
        """Parst den Zähler als Funktion-Objekt"""
        if isinstance(eingabe, str):
            # Validiere den mathematischen Ausdruck
            self._validiere_mathematischen_ausdruck(eingabe)

            # Erstelle temporäres Funktion-Objekt nur für den Zähler
            temp_funktion = Funktion.__new__(Funktion)
            temp_funktion.x = self.x
            temp_funktion.variablen = []
            temp_funktion.parameter = []
            temp_funktion.hauptvariable = None
            temp_funktion.original_eingabe = eingabe

            # Parse String zu SymPy
            temp_funktion.term_sympy = self._string_zu_sympy(eingabe)
            temp_funktion.term_str = str(temp_funktion.term_sympy)

            # Erkenne und klassifiziere Symbole
            temp_funktion._erkenne_und_klassifiziere_symbole(temp_funktion.term_sympy)

            return temp_funktion
        else:
            # SymPy-Ausdruck
            temp_funktion = Funktion.__new__(Funktion)
            temp_funktion.x = self.x
            temp_funktion.variablen = []
            temp_funktion.parameter = []
            temp_funktion.hauptvariable = None
            temp_funktion.original_eingabe = str(eingabe)
            temp_funktion.term_sympy = eingabe
            temp_funktion.term_str = str(eingabe)
            temp_funktion._erkenne_und_klassifiziere_symbole(eingabe)
            return temp_funktion

    def _parse_nenner(self, eingabe: str | sp.Basic) -> "Funktion":
        """Parst den Nenner als Funktion-Objekt"""
        return self._parse_zaehler(eingabe)  # Gleiche Logik wie Zähler

    def _ist_bruch_string(self, text: str) -> bool:
        """Prüft, ob ein String einen Bruch darstellt"""
        # Einfache Heuristik: genau ein / nicht in Klammern oder Exponenten
        slash_count = text.count("/")
        if slash_count != 1:
            return False

        # Prüfe, ob das / nicht in einem Exponenten ist
        slash_pos = text.find("/")
        before_slash = text[:slash_pos]
        after_slash = text[slash_pos + 1 :]

        # Keine ^ vor oder nach dem /
        return "^" not in before_slash and "^" not in after_slash

    def _parse_bruch_string(self, text: str) -> tuple["Funktion", "Funktion"]:
        """Parst einen String der Form "zaehler/nenner" """
        slash_pos = text.find("/")
        zaehler_str = text[:slash_pos].strip()
        nenner_str = text[slash_pos + 1 :].strip()

        # Entferne äußere Klammern wenn vorhanden
        zaehler_str = self._entferne_aeussere_klammern(zaehler_str)
        nenner_str = self._entferne_aeussere_klammern(nenner_str)

        return self._parse_zaehler(zaehler_str), self._parse_nenner(nenner_str)

    def _entferne_aeussere_klammern(self, text: str) -> str:
        """Entfernt äußere Klammern wenn sie den gesamten Ausdruck umschließen"""
        text = text.strip()
        if text.startswith("(") and text.endswith(")"):
            # Prüfe, ob die Klammern wirklich äußere sind
            klammer_zaehler = 0
            for i, char in enumerate(text):
                if char == "(":
                    klammer_zaehler += 1
                elif char == ")":
                    klammer_zaehler -= 1
                    if klammer_zaehler == 0 and i == len(text) - 1:
                        # Äußere Klammern gefunden
                        return text[1:-1]
        return text

    def _validiere_mathematischen_ausdruck(self, text: str):
        """Validiert einen mathematischen Ausdruck"""
        # Erlaubte Zeichen: Zahlen, Variablen, +-*^/(), Leerzeichen
        erlaubte_zeichen = set("0123456789xyzwtabcdefghijklmnopqrstuvwxyz+-*/^(). ")

        for char in text.lower():
            if char not in erlaubte_zeichen:
                raise ValueError(
                    f"Ungültiger Ausdruck '{text}': Ungültiges Zeichen '{char}'"
                )

        # Mindestens ein gültiges Zeichen
        if not text.strip():
            raise ValueError("Leerer Ausdruck")

    def _string_zu_sympy(self, text: str) -> sp.Basic:
        """Wandelt einen String in einen SymPy-Ausdruck um"""
        # Normalisiere den String
        text = text.strip()

        # Ersetze ^ durch ** (für SymPy)
        text = text.replace("^", "**")

        # Entferne überflüssige Leerzeichen
        text = re.sub(r"\s+", "", text)

        # 🔥 IMPLIZITE MULTIPLIKATION HANDHABEN 🔥
        # Wende Regex-Muster an, um implizite Multiplikation zu erkennen

        # Muster 0: Schütze mathematische Funktionen vor impliziter Multiplikation
        # Ersetze temporär Funktionen, um sie vor den Multiplikationsmustern zu schützen
        math_funktionen = [
            (r"\bsin\(", "__SIN__("),
            (r"\bcos\(", "__COS__("),
            (r"\btan\(", "__TAN__("),
            (r"\bexp\(", "__EXP("),
            (r"\blog\(", "__LOG("),
            (r"\babs\(", "__ABS("),
            (r"\bsqrt\(", "__SQRT("),
        ]

        for pattern, replacement in math_funktionen:
            text = re.sub(pattern, replacement, text)

        # Muster 1: Zahl gefolgt von Variable (z.B. "2x" → "2*x")
        text = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", text)

        # Muster 2: Variable gefolgt von Klammer (z.B. "x(" → "x*(")
        text = re.sub(r"([a-zA-Z])\(", r"\1*(", text)

        # Muster 3: Klammer gefolgt von Variable oder Zahl (z.B. ")x" → ")*x")
        text = re.sub(r"\)([a-zA-Z\d])", r")*\1", text)

        # Muster 4: Variable gefolgt von Variable (z.B. "ab" → "a*b")
        text = re.sub(r"([a-zA-Z])([a-zA-Z])", r"\1*\2", text)

        # Muster 5: Klammer gefolgt von Klammer (z.B. ")(" → ")*(")
        text = re.sub(r"\)\(", ")*(", text)

        # Muster 6: Zahl gefolgt von Klammer (z.B. "3(" → "3*(")
        text = re.sub(r"(\d)\(", r"\1*(", text)

        # Stelle mathematische Funktionen wieder her
        for pattern, replacement in math_funktionen:
            text = text.replace(
                replacement, pattern.replace("__", "").replace("\\", "")
            )

        try:
            return sp.sympify(text)
        except Exception as e:
            raise ValueError(f"Ungültiger mathematischer Ausdruck: '{text}'") from e

    def _erkenne_und_klassifiziere_symbole(self, term_sympy: sp.Basic):
        """Erkennt alle Symbole im Ausdruck und klassifiziert sie als Variablen oder Parameter"""
        alle_symbole = term_sympy.free_symbols

        if not alle_symbole:
            # Keine Symbole gefunden - konstante Funktion
            return

        # Heuristiken zur Klassifizierung
        for symbol in alle_symbole:
            symbol_name = str(symbol)

            if symbol_name == "x":
                # x ist immer die Hauptvariable
                var = _Variable(symbol_name)
                self.variablen.append(var)
                self.hauptvariable = var
            elif symbol_name in ["t", "y", "z"]:
                # t, y, z sind typische Variablen
                var = _Variable(symbol_name)
                self.variablen.append(var)
                if self.hauptvariable is None:
                    self.hauptvariable = var
            elif len(symbol_name) == 1 and symbol_name in [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "k",
                "m",
                "n",
                "p",
                "q",
                "r",
                "s",
                "u",
                "v",
                "w",
            ]:
                # Einzelne Buchstaben a-z (außer x,t,y,z) sind typischerweise Parameter
                param = _Parameter(symbol_name)
                self.parameter.append(param)
            else:
                # Mehrbuchstabige Symbole oder unbekannte: als Parameter behandeln
                param = _Parameter(symbol_name)
                self.parameter.append(param)

        # Falls keine Variable gefunden wurde, nimm x als Standard
        if not self.variablen:
            x_var = _Variable("x")
            self.variablen.append(x_var)
            self.hauptvariable = x_var

    def _erstelle_sympy_ausdruecke(self):
        """Erstelle die SymPy-Ausdrücke für die gesamte Funktion"""
        # Kombiniere Symbol-Informationen von Zähler und Nenner
        alle_variablen = []
        alle_parameter = []

        for teil in [self.zaehler, self.nenner]:
            alle_variablen.extend(teil.variablen)
            alle_parameter.extend(teil.parameter)

        # Entferne Duplikate
        self.variablen = []
        self.parameter = []

        seen_vars = set()
        for var in alle_variablen:
            if var.name not in seen_vars:
                self.variablen.append(var)
                seen_vars.add(var.name)
                if var.name == "x" or self.hauptvariable is None:
                    self.hauptvariable = var

        seen_params = set()
        for param in alle_parameter:
            if param.name not in seen_params:
                self.parameter.append(param)
                seen_params.add(param.name)

        # Erstelle den kombinierten SymPy-Ausdruck
        try:
            if self.nenner.term_sympy == 1:
                # Ganzrationaler Fall
                self.term_sympy = self.zaehler.term_sympy
            else:
                # Gebrochen-rationaler Fall
                self.term_sympy = self.zaehler.term_sympy / self.nenner.term_sympy
        except AttributeError:
            # Fallback für einfache Fälle
            self.term_sympy = self.zaehler.term_sympy

        self.term_str = str(self.term_sympy)

    @property
    def _variable_symbol(self) -> sp.Symbol:
        """Gibt das Symbol der Hauptvariable zurück, mit Fallback auf 'x'."""
        if self.hauptvariable:
            return self.hauptvariable.symbol
        return symbols("x")

    @property
    def ist_ganzrational(self) -> bool:
        """True wenn die Funktion ganzrational ist (Nenner = 1)"""
        try:
            return self.nenner.term_sympy == 1
        except AttributeError:
            # Fallback für rekursive Aufrufe
            return hasattr(self, "term_sympy") and not hasattr(self, "nenner")

    @property
    def hat_polstellen(self) -> bool:
        """True wenn die Funktion Polstellen hat (echt gebrochen-rational)"""
        return not self.ist_ganzrational

    @property
    def ist_exponential_rational(self) -> bool:
        """True wenn die Funktion eine Exponentialfunktion ist"""
        return self._ist_exponential_funktion(self.original_eingabe)

    def kürzen(self) -> "Funktion":
        """Kürzt die Funktion durch Faktorisierung"""
        # Vereinfache Zähler und Nenner separat
        self.zaehler.term_sympy = factor(self.zaehler.term_sympy)
        self.nenner.term_sympy = factor(self.nenner.term_sympy)

        # Erstelle SymPy-Ausdruck neu
        if self.ist_ganzrational:
            self.term_sympy = self.zaehler.term_sympy
        else:
            self.term_sympy = self.zaehler.term_sympy / self.nenner.term_sympy

        self.term_str = str(self.term_sympy)
        return self

    def __call__(self, x_wert: float) -> float | sp.Basic:
        """
        Macht die Funktion aufrufbar: f(2), f(0.5), etc.

        Args:
            x_wert: x-Wert, an dem die Funktion ausgewertet werden soll

        Returns:
            Der Funktionswert als float-Zahl oder symbolischer Ausdruck (bei Parametern)
        """
        if self.ist_ganzrational:
            # Optimierter Pfad für ganzrationale Funktionen
            return self.zaehler.wert(x_wert)
        else:
            # Allgemeiner Fall mit Division
            zaehler_wert = self.zaehler.wert(x_wert)
            nenner_wert = self.nenner.wert(x_wert)

            # Prüfe auf Polstelle
            if isinstance(nenner_wert, (int, float)) and abs(nenner_wert) < 1e-10:
                raise ValueError(f"x = {x_wert} ist eine Polstelle der Funktion")

            # Wenn beide Werte konkrete Zahlen sind, teile sie
            if isinstance(zaehler_wert, (int, float)) and isinstance(
                nenner_wert, (int, float)
            ):
                return float(zaehler_wert) / float(nenner_wert)

            # Andernfalls gib den symbolischen Ausdruck zurück
            return zaehler_wert / nenner_wert

    def wert(self, x_wert: float) -> float | sp.Basic:
        """Berechnet den Funktionswert an einer Stelle."""
        # Prüfe auf verbleibende freie Symbole (Parameter)
        free_syms = self.term_sympy.free_symbols
        if self.hauptvariable:
            free_syms.discard(self.hauptvariable.symbol)

        if free_syms:
            # Noch Parameter vorhanden - substituiere x-Wert und gib symbolischen Ausdruck zurück
            return self.term_sympy.subs(self._variable_symbol, x_wert)

        try:
            return float(self.term_sympy.subs(self._variable_symbol, x_wert))
        except (TypeError, ValueError) as e:
            raise ValueError(
                f"Fehler bei der Werteberechnung bei x={x_wert}: {e}"
            ) from e

    def term(self) -> str:
        """Gibt den Term als String zurück."""
        return str(self.term_sympy).replace("**", "^").replace("*", "").replace(" ", "")

    def term_latex(self) -> str:
        """Gibt den Term als LaTeX-String zurück."""
        return latex(self.term_sympy)

    def grad(self) -> int:
        """Gibt den Grad der Funktion zurück."""
        try:
            return sp.Poly(self.term_sympy, self._variable_symbol).degree()
        except (sp.SympifyError, TypeError, ValueError):
            # Fallback für konstante Funktionen
            return 0

    def ableitung(self, ordnung: int = 1) -> "Funktion":
        """Berechnet die Ableitung gegebener Ordnung."""
        abgeleitet = diff(self.term_sympy, self._variable_symbol, ordnung)

        # Erstelle neue Funktion direkt mit dem abgeleiteten Ausdruck
        neue_funktion = Funktion(abgeleitet)

        # Kopiere die Symbol-Informationen
        neue_funktion.variablen = self.variablen.copy()
        neue_funktion.parameter = self.parameter.copy()
        neue_funktion.hauptvariable = self.hauptvariable

        neue_funktion.original_eingabe = (
            f"Ableitung({self.original_eingabe}, {ordnung})"
        )

        return neue_funktion

    def pruefe_punktsymmetrie(
        self, x: float | sp.Basic = 0, y: float | sp.Basic = 0
    ) -> dict:
        """
        Detaillierte Prüfung der Punktsymmetrie zum Punkt (x, y) mit exakter algebraischer Verifikation.

        Args:
            x: x-Koordinate des Symmetriezentrums (Standard: 0 = Ursprung). Kann float oder SymPy-Ausdruck sein.
            y: y-Koordinate des Symmetriezentrums (Standard: 0 = Ursprung). Kann float oder SymPy-Ausdruck sein.

        Returns:
            dict: Detaillierte Analyseergebnisse mit:
                - ist_punktsymmetrisch: bool
                - details: str mit Erklärung
                - beispiele: list mit Testwerten

        Beispiele:
            >>> f = Funktion("x^3")
            >>> ergebnis = f.pruefe_punktsymmetrie()
            >>> ergebnis['ist_punktsymmetrisch']  # True

            >>> f = Funktion("(x-a)^3 + b")  # Parametrische Funktion
            >>> ergebnis = f.pruefe_punktsymmetrie(sp.Symbol('a'), sp.Symbol('b'))
            >>> ergebnis['ist_punktsymmetrisch']  # True
        """
        import random

        import sympy as sp

        details = []
        beispiele = []
        ist_punktsymmetrisch = True

        # Konvertiere x, y zu SymPy-Ausdrücken wenn nötig
        if isinstance(x, (int, float)):
            x_sym = sp.sympify(x)
        else:
            x_sym = x

        if isinstance(y, (int, float)):
            y_sym = sp.sympify(y)
        else:
            y_sym = y

        # Spezialfall: Betragsfunktion ist achsensymmetrisch, nicht punktsymmetrisch
        if "abs" in self.original_eingabe.lower():
            details.append("Betragsfunktion ist nicht punktsymmetrisch")
            return {
                "ist_punktsymmetrisch": False,
                "details": " | ".join(details),
                "beispiele": beispiele,
            }

        # 🔥 EXAKTE ALGEBRAISCHE ÜBERPRÜFUNG MIT SYMPY 🔥
        try:
            # Erstelle eine neue Variable für die Verschiebung
            h = sp.Symbol("h", real=True)

            # Berechne f(x + h) und f(x - h) symbolisch
            f_plus_h = self.term_sympy.subs(self._variable_symbol, x_sym + h)
            f_minus_h = self.term_sympy.subs(self._variable_symbol, x_sym - h)

            # Prüfe die Punktsymmetrie-Bedingung: f(x+h) + f(x-h) = 2y
            bedingung = sp.simplify(f_plus_h + f_minus_h - 2 * y_sym)

            if bedingung == 0:
                details.append("Exakte algebraische Prüfung: Bedingung erfüllt")
                beispiele.append(f"f({x_sym} + h) + f({x_sym} - h) = 2{y_sym}")
            else:
                # Versuche zu prüfen, ob der Ausdruck für alle h gleich 0 ist
                try:
                    # Prüfe ob alle Koeffizienten von h gleich 0 sind
                    if isinstance(bedingung, sp.Poly):
                        koeffizienten = bedingung.all_coeffs()
                        if all(k == 0 for k in koeffizienten):
                            details.append(
                                "Exakte algebraische Prüfung: Alle Koeffizienten gleich 0"
                            )
                        else:
                            ist_punktsymmetrisch = False
                            details.append(
                                f"Exakte algebraische Prüfung: Nicht alle Koeffizienten gleich 0: {bedingung}"
                            )
                    else:
                        # Versuche mit expand und collect
                        expanded = sp.expand(bedingung)
                        collected = sp.collect(expanded, h)
                        if collected == 0:
                            details.append(
                                "Exakte algebraische Prüfung: Expandiert und vereinfacht zu 0"
                            )
                        else:
                            ist_punktsymmetrisch = False
                            details.append(
                                f"Exakte algebraische Prüfung: {collected} ≠ 0"
                            )
                except (sp.SympifyError, TypeError, ValueError):
                    # Fallback auf numerische Tests
                    ist_punktsymmetrisch = False
                    details.append(
                        "Algebraische Prüfung nicht möglich, verwende numerische Tests"
                    )

                    # Numerische Tests als Fallback
                    for _i in range(5):
                        a = random.uniform(1, 5)
                        try:
                            wert_plus = (
                                self.wert(float(x_sym) + a)
                                if x_sym.is_number
                                else self.wert(a)
                            )
                            wert_minus = (
                                self.wert(float(x_sym) - a)
                                if x_sym.is_number
                                else self.wert(-a)
                            )

                            if isinstance(wert_plus, (int, float)) and isinstance(
                                wert_minus, (int, float)
                            ):
                                if (
                                    abs((wert_plus + wert_minus) - 2 * float(y_sym))
                                    > 1e-10
                                ):
                                    details.append(
                                        f"Numerische Abweichung bei h={a:.2f}"
                                    )
                                    break
                        except (ValueError, TypeError, ZeroDivisionError):
                            ist_punktsymmetrisch = False
                            break
        except Exception as e:
            # Fallback auf numerische Tests
            ist_punktsymmetrisch = False
            details.append(f"Algebraische Prüfung fehlgeschlagen: {e}")

            # Numerische Tests als Fallback
            for _i in range(5):
                a = random.uniform(1, 5)
                try:
                    wert_plus = (
                        self.wert(float(x_sym) + a) if x_sym.is_number else self.wert(a)
                    )
                    wert_minus = (
                        self.wert(float(x_sym) - a)
                        if x_sym.is_number
                        else self.wert(-a)
                    )

                    if isinstance(wert_plus, (int, float)) and isinstance(
                        wert_minus, (int, float)
                    ):
                        if abs((wert_plus + wert_minus) - 2 * float(y_sym)) > 1e-10:
                            details.append(f"Numerische Abweichung bei h={a:.2f}")
                            break
                except (ValueError, TypeError, ZeroDivisionError):
                    ist_punktsymmetrisch = False
                    break

        return {
            "ist_punktsymmetrisch": ist_punktsymmetrisch,
            "details": " | ".join(details)
            if details
            else "Keine Abweichungen gefunden",
            "beispiele": beispiele,
        }

    def pruefe_achsensymmetrie(self, x: float | sp.Basic = 0) -> dict:
        """
        Detaillierte Prüfung der Achsensymmetrie zur vertikalen Achse x = konst mit exakter algebraischer Verifikation.

        Args:
            x: x-Koordinate der Symmetrieachse (Standard: 0 = y-Achse). Kann float oder SymPy-Ausdruck sein.

        Returns:
            dict: Detaillierte Analyseergebnisse mit:
                - ist_achsensymmetrisch: bool
                - details: str mit Erklärung
                - beispiele: list mit Testwerten

        Beispiele:
            >>> f = Funktion("x^2")
            >>> ergebnis = f.pruefe_achsensymmetrie()
            >>> ergebnis['ist_achsensymmetrisch']  # True

            >>> f = Funktion("(x-a)^2")  # Parametrische Funktion
            >>> ergebnis = f.pruefe_achsensymmetrie(sp.Symbol('a'))
            >>> ergebnis['ist_achsensymmetrisch']  # True
        """
        import random

        import sympy as sp

        details = []
        beispiele = []
        ist_achsensymmetrisch = True

        # Konvertiere x zu SymPy-Ausdruck wenn nötig
        if isinstance(x, (int, float)):
            x_sym = sp.sympify(x)
        else:
            x_sym = x

        # Spezialfall: Betragsfunktion ist immer achsensymmetrisch zur y-Achse
        if "abs" in self.original_eingabe.lower() and x_sym == 0:
            details.append("Betragsfunktion ist achsensymmetrisch zur y-Achse")
            return {
                "ist_achsensymmetrisch": True,
                "details": " | ".join(details),
                "beispiele": beispiele,
            }

        # 🔥 EXAKTE ALGEBRAISCHE ÜBERPRÜFUNG MIT SYMPY 🔥
        try:
            # Erstelle eine neue Variable für die Verschiebung
            h = sp.Symbol("h", real=True)

            # Berechne f(x + h) und f(x - h) symbolisch
            f_plus_h = self.term_sympy.subs(self._variable_symbol, x_sym + h)
            f_minus_h = self.term_sympy.subs(self._variable_symbol, x_sym - h)

            # Prüfe die Achsensymmetrie-Bedingung: f(x+h) = f(x-h)
            bedingung = sp.simplify(f_plus_h - f_minus_h)

            if bedingung == 0:
                details.append("Exakte algebraische Prüfung: Bedingung erfüllt")
                beispiele.append(f"f({x_sym} + h) = f({x_sym} - h)")
            else:
                # Versuche zu prüfen, ob der Ausdruck für alle h gleich 0 ist
                try:
                    # Prüfe ob alle Koeffizienten von h gleich 0 sind
                    if isinstance(bedingung, sp.Poly):
                        koeffizienten = bedingung.all_coeffs()
                        if all(k == 0 for k in koeffizienten):
                            details.append(
                                "Exakte algebraische Prüfung: Alle Koeffizienten gleich 0"
                            )
                        else:
                            ist_achsensymmetrisch = False
                            details.append(
                                f"Exakte algebraische Prüfung: Nicht alle Koeffizienten gleich 0: {bedingung}"
                            )
                    else:
                        # Versuche mit expand und collect
                        expanded = sp.expand(bedingung)
                        collected = sp.collect(expanded, h)
                        if collected == 0:
                            details.append(
                                "Exakte algebraische Prüfung: Expandiert und vereinfacht zu 0"
                            )
                        else:
                            ist_achsensymmetrisch = False
                            details.append(
                                f"Exakte algebraische Prüfung: {collected} ≠ 0"
                            )
                except (sp.SympifyError, TypeError, ValueError):
                    # Fallback auf numerische Tests
                    ist_achsensymmetrisch = False
                    details.append(
                        "Algebraische Prüfung nicht möglich, verwende numerische Tests"
                    )

                    # Numerische Tests als Fallback
                    for _i in range(5):
                        h_val = random.uniform(1, 5)
                        try:
                            wert_plus = (
                                self.wert(float(x_sym) + h_val)
                                if x_sym.is_number
                                else self.wert(h_val)
                            )
                            wert_minus = (
                                self.wert(float(x_sym) - h_val)
                                if x_sym.is_number
                                else self.wert(-h_val)
                            )

                            if isinstance(wert_plus, (int, float)) and isinstance(
                                wert_minus, (int, float)
                            ):
                                if abs(wert_plus - wert_minus) > 1e-10:
                                    details.append(
                                        f"Numerische Abweichung bei h={h_val:.2f}"
                                    )
                                    break
                        except (ValueError, TypeError, ZeroDivisionError):
                            ist_achsensymmetrisch = False
                            break
        except Exception as e:
            # Fallback auf numerische Tests
            ist_achsensymmetrisch = False
            details.append(f"Algebraische Prüfung fehlgeschlagen: {e}")

            # Numerische Tests als Fallback
            for _i in range(5):
                h_val = random.uniform(1, 5)
                try:
                    wert_plus = (
                        self.wert(float(x_sym) + h_val)
                        if x_sym.is_number
                        else self.wert(h_val)
                    )
                    wert_minus = (
                        self.wert(float(x_sym) - h_val)
                        if x_sym.is_number
                        else self.wert(-h_val)
                    )

                    if isinstance(wert_plus, (int, float)) and isinstance(
                        wert_minus, (int, float)
                    ):
                        if abs(wert_plus - wert_minus) > 1e-10:
                            details.append(f"Numerische Abweichung bei h={h_val:.2f}")
                            break
                except (ValueError, TypeError, ZeroDivisionError):
                    ist_achsensymmetrisch = False
                    break

        return {
            "ist_achsensymmetrisch": ist_achsensymmetrisch,
            "details": " | ".join(details)
            if details
            else "Keine Abweichungen gefunden",
            "beispiele": beispiele,
        }

    def _is_symbolically_zero(
        self, condition: sp.Basic, check_variable: sp.Symbol
    ) -> bool:
        """
        Internal helper to robustly check if a SymPy expression is zero.

        Args:
            condition: The SymPy expression to check (e.g., f(x+h) - f(x-h)).
            check_variable: The variable (e.g., h) with respect to which the condition must hold.

        Returns:
            True if the expression is symbolically zero, False otherwise.
        """
        if condition.is_zero:
            return True

        # Try different simplification strategies
        try:
            # Simplification is often the most direct way
            simplified = sp.simplify(condition)
            if simplified.is_zero:
                return True

            # For polynomials, all coefficients of the check_variable must be zero
            if simplified.is_polynomial(check_variable):
                poly = sp.Poly(simplified, check_variable)
                return all(coeff.is_zero for coeff in poly.all_coeffs())

            # For other expressions, expand and collect terms
            expanded = sp.expand(simplified)
            collected = sp.collect(expanded, check_variable)
            if collected.is_zero:
                return True

        except (AttributeError, TypeError, ValueError, sp.SympifyError):
            # If any symbolic method fails, we cannot confirm symmetry this way
            return False

        return False

    def _numerical_symmetry_check(
        self, condition_func, test_values: list[float], tolerance: float = 1e-9
    ) -> bool:
        """
        Numerical fallback for symmetry verification.

        Args:
            condition_func: Function that takes a test value and returns the condition result
            test_values: List of values to test
            tolerance: Numerical tolerance for comparison

        Returns:
            True if all tests pass, False if any fail
        """
        for test_val in test_values:
            try:
                result = condition_func(test_val)
                if abs(result) > tolerance:
                    return False  # Found a counterexample
            except (ValueError, TypeError, ZeroDivisionError):
                return False  # Numerical evaluation failed
        return True

    def ist_punktsymmetrisch(
        self, x: float | sp.Basic = 0, y: float | sp.Basic = 0
    ) -> bool:
        """
        Prüft, ob die Funktion punktsymmetrisch zum Punkt (x, y) ist mit exakter algebraischer Verifikation.

        Eine Funktion f ist punktsymmetrisch zum Punkt (x, y), wenn für alle a gilt:
        f(x + a) + f(x - a) = 2y

        Args:
            x: x-Koordinate des Symmetriezentrums (Standard: 0 = Ursprung). Kann float oder SymPy-Ausdruck sein.
            y: y-Koordinate des Symmetriezentrums (Standard: 0 = Ursprung). Kann float oder SymPy-Ausdruck sein.

        Returns:
            bool: True wenn punktsymmetrisch, False sonst

        Beispiele:
            >>> f = Funktion("x^3")           # Ursprungssymmetrisch
            >>> f.ist_punktsymmetrisch()     # True
            >>> f.ist_punktsymmetrisch(1, 1) # False

            >>> g = Funktion("(x-1)^3 + 1")  # Punktsymmetrisch zu (1, 1)
            >>> g.ist_punktsymmetrisch(1, 1) # True

            >>> import sympy as sp
            >>> h = Funktion("(x-a)^3 + b")  # Parametrische Funktion
            >>> h.ist_punktsymmetrisch(sp.Symbol('a'), sp.Symbol('b'))  # True

            >>> k = Funktion("x^2")           # Nicht punktsymmetrisch
            >>> k.ist_punktsymmetrisch()     # False
        """
        # Konvertiere x, y zu SymPy-Ausdrücken wenn nötig
        x_sym = sp.sympify(x) if isinstance(x, (int, float)) else x
        y_sym = sp.sympify(y) if isinstance(y, (int, float)) else y

        # Erstelle eine neue Variable für die Verschiebung
        h = sp.Symbol("h", real=True, positive=True)

        # Berechne f(x + h) und f(x - h) symbolisch
        f_plus_h = self.term_sympy.subs(self._variable_symbol, x_sym + h)
        f_minus_h = self.term_sympy.subs(self._variable_symbol, x_sym - h)

        # Die Punktsymmetrie-Bedingung: f(x+h) + f(x-h) = 2y
        condition = f_plus_h + f_minus_h - 2 * y_sym

        # Prüfe symbolisch
        if self._is_symbolically_zero(condition, h):
            return True

        # Fallback auf numerische Prüfung
        # Note: Eine numerische Prüfung kann nur Nicht-Symmetrie beweisen, nicht Symmetrie
        try:
            x_c_float = float(x_sym) if x_sym.is_number else 0
            y_c_float = float(y_sym) if y_sym.is_number else 0

            def point_condition(test_val):
                val_plus = self.wert(x_c_float + test_val)
                val_minus = self.wert(x_c_float - test_val)
                return (val_plus + val_minus) - 2 * y_c_float

            # Teste mehrere zufällige Werte
            test_values = [random.uniform(0.1, 5.0) for _ in range(10)]
            if self._numerical_symmetry_check(point_condition, test_values):
                # Wenn numerische Tests alle bestehen, versuche nochmal die detaillierte Methode
                ergebnis = self.pruefe_punktsymmetrie(x, y)
                return ergebnis["ist_punktsymmetrisch"]
            else:
                return False  # Numerische Tests zeigen keine Symmetrie

        except (ValueError, TypeError, ZeroDivisionError, AttributeError):
            # Fallback auf die detaillierte Prüfmethode
            ergebnis = self.pruefe_punktsymmetrie(x, y)
            return ergebnis["ist_punktsymmetrisch"]

    def ist_achsensymmetrisch(self, x: float | sp.Basic = 0) -> bool:
        """
        Prüft, ob die Funktion achsensymmetrisch zur vertikalen Achse x = konst ist mit exakter algebraischer Verifikation.

        Eine Funktion f ist achsensymmetrisch zur Achse x = a, wenn für alle h gilt:
        f(a + h) = f(a - h)

        Args:
            x: x-Koordinate der Symmetrieachse (Standard: 0 = y-Achse). Kann float oder SymPy-Ausdruck sein.

        Returns:
            bool: True wenn achsensymmetrisch, False sonst

        Beispiele:
            >>> f = Funktion("x^2")           # y-achsensymmetrisch
            >>> f.ist_achsensymmetrisch()     # True
            >>> f.ist_achsensymmetrisch(1)    # False

            >>> g = Funktion("(x-1)^2")       # symmetrisch zu x=1
            >>> g.ist_achsensymmetrisch(1)    # True

            >>> import sympy as sp
            >>> h = Funktion("(x-a)^2")       # Parametrische Funktion
            >>> h.ist_achsensymmetrisch(sp.Symbol('a'))  # True

            >>> k = Funktion("x^3")           # Nicht achsensymmetrisch
            >>> k.ist_achsensymmetrisch()     # False
        """
        # Konvertiere x zu SymPy-Ausdruck wenn nötig
        x_sym = sp.sympify(x) if isinstance(x, (int, float)) else x

        # Erstelle eine neue Variable für die Verschiebung
        h = sp.Symbol("h", real=True, positive=True)

        # Berechne f(x + h) und f(x - h) symbolisch
        f_plus_h = self.term_sympy.subs(self._variable_symbol, x_sym + h)
        f_minus_h = self.term_sympy.subs(self._variable_symbol, x_sym - h)

        # Die Achsensymmetrie-Bedingung: f(x+h) = f(x-h)
        condition = f_plus_h - f_minus_h

        # Prüfe symbolisch
        if self._is_symbolically_zero(condition, h):
            return True

        # Fallback auf numerische Prüfung
        # Note: Eine numerische Prüfung kann nur Nicht-Symmetrie beweisen, nicht Symmetrie
        try:
            x_c_float = float(x_sym) if x_sym.is_number else 0

            def axis_condition(test_val):
                val_plus = self.wert(x_c_float + test_val)
                val_minus = self.wert(x_c_float - test_val)
                return val_plus - val_minus

            # Teste mehrere zufällige Werte
            test_values = [random.uniform(0.1, 5.0) for _ in range(10)]
            if self._numerical_symmetry_check(axis_condition, test_values):
                # Wenn numerische Tests alle bestehen, versuche nochmal die detaillierte Methode
                ergebnis = self.pruefe_achsensymmetrie(x)
                return ergebnis["ist_achsensymmetrisch"]
            else:
                return False  # Numerische Tests zeigen keine Symmetrie

        except (ValueError, TypeError, ZeroDivisionError, AttributeError):
            # Fallback auf die detaillierte Prüfmethode
            ergebnis = self.pruefe_achsensymmetrie(x)
            return ergebnis["ist_achsensymmetrisch"]

    def nullstellen(self, real: bool = True, runden=None) -> list[sp.Basic]:
        """Berechnet die Nullstellen der Funktion."""
        # Verwende direkt SymPy's solve
        lösungen = solve(self.term_sympy, self._variable_symbol)
        nullstellen_liste = []

        for lösung in lösungen:
            # Bei symbolischen Lösungen: is_real kann None sein
            if real and lösung.is_real is False:
                continue

            if lösung.is_real is True:
                nullstellen_liste.append(self._runde_wert(lösung, runden))
            else:
                # Symbolische Lösungen oder komplexe Zahlen
                if lösung.is_real is None:
                    # Symbolische Lösung - behalte als SymPy-Expr
                    nullstellen_liste.append(lösung)
                else:
                    # Komplexe Zahl - für jetzt überspringen
                    continue

        # Sortiere Nullstellen
        reelle_nullstellen = []
        symbolische_nullstellen = []

        for x in nullstellen_liste:
            if hasattr(x, "is_real"):
                if x.is_real is True:
                    reelle_nullstellen.append(x)
                else:
                    # Symbolische Ausdrücke
                    symbolische_nullstellen.append(x)

        # Sortiere reelle Nullstellen
        reelle_nullstellen.sort(key=lambda x: float(x))

        return reelle_nullstellen + symbolische_nullstellen

    def _runde_wert(self, wert, runden=None):
        """Hilfsfunktion zum Runden von Werten"""
        if runden is not None and hasattr(wert, "evalf"):
            return float(wert.evalf(n=runden))
        return wert

    def polstellen(self) -> list[float]:
        """Berechnet die Polstellen der Funktion (nur für echt gebrochen-rationale Funktionen)."""
        if self.ist_ganzrational:
            return []

        # Finde Nullstellen des Nenners
        nenner_nullstellen = self.nenner.nullstellen()

        # Konvertiere zu float und filtere
        polstellen = []
        for ns in nenner_nullstellen:
            try:
                x_val = float(ns)
                # Prüfe, dass es nicht auch eine Nullstelle des Zählers ist
                if not any(
                    abs(x_val - float(zs)) < 1e-10 for zs in self.zaehler.nullstellen()
                ):
                    polstellen.append(x_val)
            except (ValueError, TypeError):
                continue

        return sorted(polstellen)

    def __str__(self):
        """String-Repräsentation der Funktion."""
        return self.term()

    def __repr__(self):
        """Repräsentation für Debugging."""
        return f"Funktion('{self.original_eingabe}')"


# 🔥 WRAPPER-FUNKTIONEN FÜR SYMMETRIE-PRÜFUNG 🔥


def Achsensymmetrie(funktion: Funktion, x: float | sp.Basic = 0) -> bool:
    """
    Wrapper-Funktion zur Prüfung der Achsensymmetrie.

    Diese Funktion nutzt die Methode funktion.ist_achsensymmetrisch(x)
    zur Überprüfung der Achsensymmetrie.

    Args:
        funktion: Die zu prüfende Funktion (Funktion-Objekt)
        x: x-Koordinate der Symmetrieachse (Standard: 0 = y-Achse).
           Kann float oder SymPy-Ausdruck sein (z.B. 1+a)

    Returns:
        bool: True wenn achsensymmetrisch, False sonst

    Beispiele:
        >>> f = Funktion("x^2")
        >>> Achsensymmetrie(f)                    # True (y-Achse)
        >>> Achsensymmetrie(f, 1)                 # False

        >>> g = Funktion("(x-1)^2")
        >>> Achsensymmetrie(g, 1)                 # True (x=1)

        >>> import sympy as sp
        >>> a = sp.Symbol('a')
        >>> h = Funktion("(x-a)^2")
        >>> Achsensymmetrie(h, a)                 # True (x=a)
    """
    return funktion.ist_achsensymmetrisch(x)


def Punktsymmetrie(
    funktion: Funktion, x: float | sp.Basic = 0, y: float | sp.Basic = 0
) -> bool:
    """
    Wrapper-Funktion zur Prüfung der Punktsymmetrie.

    Diese Funktion nutzt die Methode funktion.ist_punktsymmetrisch(x, y)
    zur Überprüfung der Punktsymmetrie.

    Args:
        funktion: Die zu prüfende Funktion (Funktion-Objekt)
        x: x-Koordinate des Symmetriezentrums (Standard: 0 = Ursprung).
           Kann float oder SymPy-Ausdruck sein (z.B. 1+a)
        y: y-Koordinate des Symmetriezentrums (Standard: 0 = Ursprung).
           Kann float oder SymPy-Ausdruck sein (z.B. 2+b)

    Returns:
        bool: True wenn punktsymmetrisch, False sonst

    Beispiele:
        >>> f = Funktion("x^3")
        >>> Punktsymmetrie(f)                    # True (Ursprung)
        >>> Punktsymmetrie(f, 1, 1)             # False

        >>> g = Funktion("(x-1)^3 + 1")
        >>> Punktsymmetrie(g, 1, 1)             # True (Punkt (1,1))

        >>> import sympy as sp
        >>> a, b = sp.symbols('a b')
        >>> h = Funktion("(x-a)^3 + b")
        >>> Punktsymmetrie(h, a, b)              # True (Punkt (a,b))
    """
    return funktion.ist_punktsymmetrisch(x, y)


# 🔥 DETAILIERTE WRAPPER-FUNKTIONEN 🔥


def PruefeAchsensymmetrie(funktion: Funktion, x: float | sp.Basic = 0) -> dict:
    """
    Wrapper-Funktion für detaillierte Achsensymmetrie-Prüfung.

    Diese Funktion nutzt die Methode funktion.pruefe_achsensymmetrie(x)
    zur detaillierten Analyse der Achsensymmetrie.

    Args:
        funktion: Die zu prüfende Funktion (Funktion-Objekt)
        x: x-Koordinate der Symmetrieachse (Standard: 0 = y-Achse).
           Kann float oder SymPy-Ausdruck sein

    Returns:
        dict: Detaillierte Analyseergebnisse mit:
            - ist_achsensymmetrisch: bool
            - details: str mit Erklärung
            - beispiele: list mit Testwerten

    Beispiele:
        >>> f = Funktion("x^2")
        >>> ergebnis = PruefeAchsensymmetrie(f)
        >>> ergebnis['ist_achsensymmetrisch']     # True
        >>> ergebnis['details']                   # Erklärung
    """
    return funktion.pruefe_achsensymmetrie(x)


def PruefePunktsymmetrie(
    funktion: Funktion, x: float | sp.Basic = 0, y: float | sp.Basic = 0
) -> dict:
    """
    Wrapper-Funktion für detaillierte Punktsymmetrie-Prüfung.

    Diese Funktion nutzt die Methode funktion.pruefe_punktsymmetrie(x, y)
    zur detaillierten Analyse der Punktsymmetrie.

    Args:
        funktion: Die zu prüfende Funktion (Funktion-Objekt)
        x: x-Koordinate des Symmetriezentrums (Standard: 0 = Ursprung)
        y: y-Koordinate des Symmetriezentrums (Standard: 0 = Ursprung)

    Returns:
        dict: Detaillierte Analyseergebnisse mit:
            - ist_punktsymmetrisch: bool
            - details: str mit Erklärung
            - beispiele: list mit Testwerten

    Beispiele:
        >>> f = Funktion("x^3")
        >>> ergebnis = PruefePunktsymmetrie(f)
        >>> ergebnis['ist_punktsymmetrisch']      # True
        >>> ergebnis['details']                   # Erklärung
    """
    return funktion.pruefe_punktsymmetrie(x, y)
