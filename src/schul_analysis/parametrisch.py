"""
Parametrische Funktionen mit Variablen und Parametern

Dieses Modul ermöglicht die Arbeit mit parametrischen Funktionen wie
f_a(x) = a x² + x, wobei 'a' ein Parameter und 'x' eine Variable ist.
"""

from typing import Union, List, Tuple, Optional, Any
import sympy as sp
from dataclasses import dataclass


@dataclass
class Variable:
    """
    Repräsentiert eine symbolische Variable (z.B. x, y, t)

    Args:
        name: Name der Variable (z.B. "x")

    Beispiele:
        >>> x = Variable("x")
        >>> t = Variable("t")
    """

    name: str

    def __post_init__(self):
        """Erstellt ein SymPy-Symbol bei der Initialisierung"""
        self._symbol = sp.Symbol(self.name)

    @property
    def symbol(self) -> sp.Symbol:
        """Gibt das SymPy-Symbol zurück"""
        return self._symbol

    def __repr__(self) -> str:
        return f"Variable('{self.name}')"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if isinstance(other, Variable):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Parameter:
    """
    Repräsentiert einen symbolischen Parameter (z.B. a, b, c)

    Args:
        name: Name des Parameters (z.B. "a")

    Beispiele:
        >>> a = Parameter("a")
        >>> b = Parameter("b")
    """

    name: str

    def __post_init__(self):
        """Erstellt ein SymPy-Symbol bei der Initialisierung"""
        self._symbol = sp.Symbol(self.name)

    @property
    def symbol(self) -> sp.Symbol:
        """Gibt das SymPy-Symbol zurück"""
        return self._symbol

    def __repr__(self) -> str:
        return f"Parameter('{self.name}')"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if isinstance(other, Parameter):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)


class ParametrischeFunktion:
    """
    Repräsentiert eine parametrische Funktion mit symbolischen Parametern

    Diese Klasse kann Funktionen wie f_a(x) = a x² + x verarbeiten und
    sowohl symbolische als auch numerische Berechnungen durchführen.

    Args:
        koeffizienten: Liste der Koeffizienten (können Parameter oder Zahlen enthalten)
        variablen: Liste der Variablen (normalerweise nur [x])

    Beispiele:
        >>> x = Variable("x")
        >>> a = Parameter("a")
        >>> f = ParametrischeFunktion([a, 1, 0], [x])  # a*x² + x
    """

    def __init__(
        self,
        koeffizienten: List[Union[Parameter, int, float]],
        variablen: List[Variable],
    ):
        self.koeffizienten = koeffizienten
        self.variablen = variablen
        self._term_sympy = None
        self._parameternamen = set()
        self._variablennamen = set()

        # Parameter und Variablen extrahieren
        self._extrahiere_symbolische_objekte()

    def _extrahiere_symbolische_objekte(self):
        """Extrahiert alle Parameter und Variablen aus den Koeffizienten"""
        self._parameternamen = set()
        self._variablennamen = set()

        for var in self.variablen:
            self._variablennamen.add(var.name)

        for koeff in self.koeffizienten:
            if isinstance(koeff, Parameter):
                self._parameternamen.add(koeff.name)

    @property
    def term_sympy(self) -> sp.Expr:
        """Erzeugt den SymPy-Term der Funktion"""
        if self._term_sympy is None:
            self._term_sympy = self._erzeuge_term()
        return self._term_sympy

    def _erzeuge_term(self) -> sp.Expr:
        """Erzeugt den SymPy-Term aus den Koeffizienten und Variablen"""
        if not self.variablen:
            raise ValueError("Mindestens eine Variable erforderlich")

        # Für den Fall einer Variable (normalerweise x)
        if len(self.variablen) == 1:
            x = self.variablen[0].symbol
            term = 0

            for i, koeff in enumerate(self.koeffizienten):
                if isinstance(koeff, Parameter):
                    koeff_symbol = koeff.symbol
                else:
                    koeff_symbol = koeff

                if i == 0:
                    # Konstanter Term
                    term += koeff_symbol
                elif i == 1:
                    # Linearer Term
                    term += koeff_symbol * x
                else:
                    # Höhere Potenzen
                    term += koeff_symbol * (x**i)

            return term
        else:
            # Mehrere Variablen - komplexerer Fall
            # Dies würde eine allgemeine Implementation erfordern
            raise NotImplementedError("Mehrere Variablen noch nicht implementiert")

    @classmethod
    def term(
        cls, term_string: str, *args: Union[Parameter, Variable]
    ) -> "ParametrischeFunktion":
        """
        Erstellt eine parametrische Funktion aus einem String

        Args:
            term_string: Mathematischer Ausdruck als String (z.B. "a*x^2 + x")
            *args: Parameter und Variablen, die im String verwendet werden

        Beispiele:
            >>> x = Variable("x")
            >>> a = Parameter("a")
            >>> f = ParametrischeFunktion.term("a*x^2 + x", a, x)
        """
        # Erstelle Mapping von Namen zu Symbolen
        symbol_mapping = {}
        variablen = []

        for arg in args:
            if isinstance(arg, Variable):
                symbol_mapping[arg.name] = arg.symbol
                variablen.append(arg)
            elif isinstance(arg, Parameter):
                symbol_mapping[arg.name] = arg.symbol

        # Parse den String mit SymPy
        try:
            term_sympy = sp.sympify(term_string, locals=symbol_mapping)
        except Exception as e:
            raise ValueError(f"Konnte Term '{term_string}' nicht parsen: {e}")

        # Konvertiere zurück zur Koeffizienten-Darstellung
        # Dies ist eine Vereinfachung - in einer vollständigen Implementation
        # müsste man den Term analysieren und in Polynomform bringen
        raise NotImplementedError("String-Parsing noch nicht implementiert")

    def __repr__(self) -> str:
        return f"ParametrischeFunktion({self.koeffizienten}, {self.variablen})"

    def __str__(self) -> str:
        return self.term()

    def term(self) -> str:
        """Gibt den Term als lesbaren String zurück"""
        if len(self.variablen) != 1:
            return str(self.term_sympy)

        var_name = self.variablen[0].name
        termbestandteile = []

        for i, koeff in enumerate(self.koeffizienten):
            if koeff == 0:
                continue

            if isinstance(koeff, Parameter):
                koeff_str = koeff.name
            else:
                koeff_str = str(koeff)

            if i == 0:
                # Konstanter Term
                termbestandteile.append(koeff_str)
            elif i == 1:
                # Linearer Term
                if koeff == 1:
                    termbestandteile.append(var_name)
                elif koeff == -1:
                    termbestandteile.append(f"-{var_name}")
                else:
                    termbestandteile.append(f"{koeff_str}{var_name}")
            else:
                # Höhere Potenzen
                if koeff == 1:
                    termbestandteile.append(f"{var_name}^{i}")
                elif koeff == -1:
                    termbestandteile.append(f"-{var_name}^{i}")
                else:
                    termbestandteile.append(f"{koeff_str}{var_name}^{i}")

        return " + ".join(termbestandteile).replace(" + -", " - ")

    def mit_wert(self, **werte) -> "GanzrationaleFunktion":
        """
        Erzeugt eine konkrete Funktion durch Einsetzen von Parameterwerten

        Args:
            **werte: Parameter-Wert-Paare (z.B. a=2)

        Beispiele:
            >>> x = Variable("x")
            >>> a = Parameter("a")
            >>> f = ParametrischeFunktion([a, 1, 0], [x])
            >>> f_konkret = f.mit_wert(a=2)  # 2x² + x
        """
        # Import hier, um zyklische Abhängigkeiten zu vermeiden
        from .ganzrationale import GanzrationaleFunktion

        # Ersetze Parameter durch konkrete Werte
        konkrete_koeffizienten = []

        for koeff in self.koeffizienten:
            if isinstance(koeff, Parameter):
                if koeff.name in werte:
                    konkrete_koeffizienten.append(werte[koeff.name])
                else:
                    raise ValueError(
                        f"Parameter '{koeff.name}' nicht in werten angegeben"
                    )
            else:
                konkrete_koeffizienten.append(koeff)

        # Erstelle konkrete Funktion
        return GanzrationaleFunktion(konkrete_koeffizienten)

    def ableitung(self, ordnung: int = 1) -> "ParametrischeFunktion":
        """
        Berechnet die symbolische Ableitung der Funktion

        Args:
            ordnung: Ordnung der Ableitung (1 = erste, 2 = zweite, etc.)

        Beispiele:
            >>> x = Variable("x")
            >>> a = Parameter("a")
            >>> f = ParametrischeFunktion([a, 1, 0], [x])  # a*x² + x
            >>> f_strich = f.ableitung()  # 2*a*x + 1
        """
        if ordnung <= 0:
            return self

        # Berechne Ableitung mit SymPy
        abgeleitet = sp.diff(self.term_sympy, self.variablen[0].symbol, ordnung)

        # Konvertiere zurück zur Koeffizienten-Darstellung
        # Dies ist eine Vereinfachung - in der Praxis müsste man
        # den abgeleiteten Term analysieren
        raise NotImplementedError(
            "Symbolische Ableitung noch nicht vollständig implementiert"
        )

    def nullstellen(self) -> List[Union[sp.Expr, Tuple[sp.Expr, str]]]:
        """
        Berechnet die symbolischen Nullstellen der Funktion

        Returns:
            Liste der Nullstellen als SymPy-Ausdrücke oder mit Bedingungen

        Beispiele:
            >>> x = Variable("x")
            >>> a = Parameter("a")
            >>> f = ParametrischeFunktion([a, 1, 0], [x])  # a*x² + x
            >>> nullstellen = f.nullstellen()  # [0, -1/a]
        """
        try:
            # Löse die Gleichung f(x) = 0
            gleichung = sp.Eq(self.term_sympy, 0)
            loesungen = sp.solve(gleichung, self.variablen[0].symbol)

            # Füge Bedingungen hinzu
            nullstellen_mit_bedingungen = []
            for loesung in loesungen:
                if loesung.is_real:
                    # Prüfe auf Division durch Parameter
                    if loesung.has(sp.Symbol):
                        # Finde alle Nenner mit Parametern
                        nenner = []
                        for symbol in loesung.free_symbols:
                            if symbol.name in self._parameternamen:
                                # Füge Bedingung "Parameter ≠ 0" hinzu
                                bedingung = f"({symbol.name} ≠ 0)"
                                nullstellen_mit_bedingungen.append((loesung, bedingung))
                            else:
                                nullstellen_mit_bedingungen.append((loesung, None))
                    else:
                        nullstellen_mit_bedingungen.append((loesung, None))

            return nullstellen_mit_bedingungen
        except Exception:
            return []

    def extremstellen(self) -> List[Tuple[sp.Expr, str]]:
        """
        Berechnet die symbolischen Extremstellen der Funktion

        Returns:
            Liste von (x_wert, art) Tupeln mit Bedingungen

        Beispiele:
            >>> x = Variable("x")
            >>> a = Parameter("a")
            >>> f = ParametrischeFunktion([a, 1, 0], [x])  # a*x² + x
            >>> extremstellen = f.extremstellen()  # [(-1/(2a), "Minimum" wenn a > 0)]
        """
        try:
            # Berechne erste Ableitung
            f_strich = sp.diff(self.term_sympy, self.variablen[0].symbol)

            # Löse f'(x) = 0
            gleichung = sp.Eq(f_strich, 0)
            loesungen = sp.solve(gleichung, self.variablen[0].symbol)

            extremstellen_mit_bedingungen = []

            for loesung in loesungen:
                if loesung.is_real:
                    # Bestimme die Art des Extrempunkts durch zweite Ableitung
                    f_strich_strich = sp.diff(f_strich, self.variablen[0].symbol)

                    # Setze die Lösung in die zweite Ableitung ein
                    try:
                        zweite_ableitung_wert = f_strich_strich.subs(
                            self.variablen[0].symbol, loesung
                        )

                        if zweite_ableitung_wert.is_positive:
                            art = "Minimum"
                        elif zweite_ableitung_wert.is_negative:
                            art = "Maximum"
                        else:
                            art = "Sattelpunkt"

                        # Füge Bedingungen hinzu
                        bedingungen = []
                        for symbol in loesung.free_symbols:
                            if symbol.name in self._parameternamen:
                                if symbol in zweite_ableitung_wert.free_symbols:
                                    if zweite_ableitung_wert.is_positive:
                                        bedingungen.append(f"{symbol.name} > 0")
                                    elif zweite_ableitung_wert.is_negative:
                                        bedingungen.append(f"{symbol.name} < 0")
                                bedingungen.append(f"{symbol.name} ≠ 0")

                        if bedingungen:
                            bedingung = ", ".join(bedingungen)
                            extremstellen_mit_bedingungen.append(
                                (loesung, f"{art} wenn {bedingung}")
                            )
                        else:
                            extremstellen_mit_bedingungen.append((loesung, art))
                    except:
                        extremstellen_mit_bedingungen.append((loesung, "Extremstelle"))

            return extremstellen_mit_bedingungen
        except Exception:
            return []

    def wendepunkte(self) -> List[Tuple[sp.Expr, sp.Expr, str]]:
        """
        Berechnet die symbolischen Wendepunkte der Funktion

        Returns:
            Liste von (x_wert, y_wert, art) Tupeln mit Bedingungen
        """
        try:
            # Berechne zweite Ableitung
            f_strich_strich = sp.diff(self.term_sympy, self.variablen[0].symbol, 2)

            # Löse f''(x) = 0
            gleichung = sp.Eq(f_strich_strich, 0)
            loesungen = sp.solve(gleichung, self.variablen[0].symbol)

            wendepunkte_mit_bedingungen = []

            for loesung in loesungen:
                if loesung.is_real:
                    # Berechne y-Wert
                    try:
                        y_wert = self.term_sympy.subs(self.variablen[0].symbol, loesung)

                        # Analysiere Krümmungsänderung
                        # (Vereinfachte Analyse - in der Praxis müsste man
                        # die dritte Ableitung oder Testpunkte verwenden)
                        art = "Wendepunkt"

                        # Füge Bedingungen hinzu
                        bedingungen = []
                        for symbol in loesung.free_symbols:
                            if symbol.name in self._parameternamen:
                                bedingungen.append(f"{symbol.name} ≠ 0")

                        if bedingungen:
                            bedingung = ", ".join(bedingungen)
                            wendepunkte_mit_bedingungen.append(
                                (loesung, y_wert, f"{art} wenn {bedingung}")
                            )
                        else:
                            wendepunkte_mit_bedingungen.append((loesung, y_wert, art))
                    except:
                        wendepunkte_mit_bedingungen.append((loesung, 0, "Wendepunkt"))

            return wendepunkte_mit_bedingungen
        except Exception:
            return []


# Convenience-Funktionen für häufige Anwendungsfälle
def create_variable(name: str) -> Variable:
    """Erstellt eine Variable (Convenience-Funktion)"""
    return Variable(name)


def create_parameter(name: str) -> Parameter:
    """Erstellt einen Parameter (Convenience-Funktion)"""
    return Parameter(name)
