"""
Parametrische Funktionen mit Variablen und Parametern

Dieses Modul ermöglicht die Arbeit mit parametrischen Funktionen wie
f_a(x) = a x² + x, wobei 'a' ein Parameter und 'x' eine Variable ist.
"""

from abc import ABC
from dataclasses import dataclass

import sympy as sp

from .ganzrationale import GanzrationaleFunktion


@dataclass
class SymbolischeGroesse(ABC):
    """
    Abstrakte Basisklasse für symbolische Größen (Variable und Parameter)

    Args:
        name: Name der symbolischen Größe (z.B. "x" oder "a")
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
        return f"{self.__class__.__name__}('{self.name}')"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Variable(SymbolischeGroesse):
    """
    Repräsentiert eine symbolische Variable (z.B. x, y, t)

    Args:
        name: Name der Variable (z.B. "x")

    Beispiele:
        >>> x = Variable("x")
        >>> t = Variable("t")
    """

    pass


@dataclass
class Parameter(SymbolischeGroesse):
    """
    Repräsentiert einen symbolischen Parameter (z.B. a, b, c)

    Args:
        name: Name des Parameters (z.B. "a")

    Beispiele:
        >>> a = Parameter("a")
        >>> b = Parameter("b")
    """

    pass


class ParametrischeFunktion:
    """
    Repräsentiert eine parametrische Funktion mit symbolischen Parametern

    Diese Klasse kann Funktionen wie f_a(x) = a x² + x verarbeiten und
    sowohl symbolische als auch numerische Berechnungen durchführen.
    Perfekt für den Mathematikunterricht zur Untersuchung von Funktionen
    mit variablen Parametern.

    Args:
        term_sympy: SymPy-Ausdruck der Funktion
        variablen: Liste der Variablen (normalerweise nur [x])
        parameter: Liste der Parameter

    Beispiele:
        # Einfache quadratische Funktion
        >>> x = Variable("x")
        >>> a = Parameter("a")
        >>> f = ParametrischeFunktion([a, 1, 0], [x])  # a*x² + x
        >>> print(f.term())
        a + x

        # Funktion mit mehreren Parametern
        >>> b = Parameter("b")
        >>> c = Parameter("c")
        >>> g = ParametrischeFunktion.from_string("a*x^2 + b*x + c", a, b, c, x)
        >>> print(g.term())
        c + bx + ax^2

        # Ableitung bilden
        >>> g_strich = g.ableitung()
        >>> print(g_strich.term())
        2.0ax + b

        # Konkrete Werte einsetzen
        >>> g_konkret = g.mit_wert(a=2, b=3, c=1)
        >>> print(g_konkret.term())
        1.0 + 3.0x + 2.0x^2
    """

    def __init__(
        self,
        eingabe: list[Parameter | int | float] | str,
        variablen: list[Variable] | Variable | None = None,
        *args: Parameter | Variable,
    ):
        """
        Initialisiert eine parametrische Funktion

        Args:
            eingabe: Entweder Koeffizienten-Liste [c0, c1, c2, ...] für c0 + c1*x + c2*x² + ...
                     oder Term-String wie "a*x^2 + b*x + c"
            variablen: Liste der Variablen oder einzelne Variable (bei String-Eingabe)
            *args: Zusätzliche Parameter/Variable (bei String-Eingabe)

        Beispiele:
            # Koeffizienten-Liste: 2 + 3x + x²
            f = ParametrischeFunktion([2, 3, 1], [x])

            # String-Eingabe mit Liste
            f = ParametrischeFunktion("a*x^2 + x", [x, a])

            # String-Eingabe mit einzelnen Objekten
            f = ParametrischeFunktion("a*x^2 + x", x, a)

        Hinweis für Lehrer:
            Die Koeffizienten-Liste beginnt mit dem konstanten Term (Grad 0),
            dann der lineare Term (Grad 1), dann quadratisch (Grad 2), etc.
        """
        if isinstance(eingabe, str):
            # String-Eingabe - verwende die from_string Klassenmethode
            if variablen is None:
                variablen = []
            elif isinstance(variablen, Variable):
                # Einzelne Variable in Liste umwandeln
                variablen = [variablen]

            alle_args = list(variablen) + list(args)
            string_funktion = self.from_string(eingabe, *alle_args)
            self._term_sympy = string_funktion._term_sympy
            self.variablen = string_funktion.variablen
            self.parameter_objekte = string_funktion.parameter_objekte
        else:
            # Koeffizienten-Liste (traditionelle Eingabe)
            self.koeffizienten_liste = eingabe
            self.variablen = variablen
            self.parameter_objekte = [k for k in eingabe if isinstance(k, Parameter)]
            # Erzeuge Sympy-Term aus Koeffizienten
            self._term_sympy = self._erzeuge_term_aus_koeffizienten()

        # Parameter- und Variablennamen extrahieren
        self._parameternamen = {p.name for p in self.parameter_objekte}
        self._variablennamen = {v.name for v in self.variablen}

        # Cache für Koeffizienten
        self._koeffizienten_cache = None

    def _erzeuge_term_aus_koeffizienten(self) -> sp.Expr:
        """Erzeugt den SymPy-Term aus den Koeffizienten und Variablen"""
        if not self.variablen:
            raise ValueError("Mindestens eine Variable erforderlich")

        # Für den Fall einer Variable (normalerweise x)
        if len(self.variablen) == 1:
            x = self.variablen[0].symbol
            term = 0

            for i, koeff in enumerate(self.koeffizienten_liste):
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

            return term  # type: ignore
        else:
            # Mehrere Variablen - komplexerer Fall
            raise NotImplementedError("Mehrere Variablen noch nicht implementiert")

    @property
    def koeffizienten(self) -> list:
        """Gibt die Koeffizienten als Liste zurück (gecached)"""
        if self._koeffizienten_cache is None:
            self._koeffizienten_cache = self._extrahiere_koeffizienten_aus_sympy()
        return self._koeffizienten_cache

    def _extrahiere_koeffizienten_aus_sympy(self) -> list:
        """Extrahiert Koeffizienten aus dem Sympy-Term"""
        if not self.variablen:
            raise ValueError("Mindestens eine Variable erforderlich")

        variable_symbol = self.variablen[0].symbol

        try:
            # Verwende sympy.Poly für robuste Koeffizienten-Extraktion
            poly = sp.Poly(self._term_sympy, variable_symbol)
            # Koeffizienten von höchstem zu niedrigstem Grad
            koeffizienten_sympy = poly.all_coeffs()
            # Umkehren für [c0, c1, c2, ...] Format
            koeffizienten_sympy.reverse()

            # Konvertiere Sympy-Koeffizienten zurück zu Parameter/Float
            finale_koeffizienten = []
            parameter_dict = {p.name: p for p in self.parameter_objekte}

            for koeff in koeffizienten_sympy:
                if koeff.is_number:
                    finale_koeffizienten.append(float(koeff))
                elif koeff.is_symbol and koeff.name in parameter_dict:
                    finale_koeffizienten.append(parameter_dict[koeff.name])
                else:
                    # Komplexerer Ausdruck - für jetzt als Fehler behandeln
                    raise ValueError(
                        f"Komplexer Koeffizient nicht unterstützt: {koeff}"
                    )

            # Fülle mit Nullen auf, um die Liste zu vervollständigen
            grad = len(koeffizienten_sympy) - 1
            while len(finale_koeffizienten) <= grad:
                finale_koeffizienten.append(0.0)

            return finale_koeffizienten
        except Exception as e:
            raise ValueError(f"Konnte Koeffizienten nicht extrahieren: {e}")

    @property
    def term_sympy(self) -> sp.Expr:
        """Gibt den SymPy-Term der Funktion zurück"""
        return self._term_sympy

    @classmethod
    def from_string(
        cls, term_string: str, *args: Parameter | Variable
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
        parameter_objekte = []

        for arg in args:
            if isinstance(arg, Variable):
                symbol_mapping[arg.name] = arg.symbol
                variablen.append(arg)
            elif isinstance(arg, Parameter):
                symbol_mapping[arg.name] = arg.symbol
                parameter_objekte.append(arg)

        if not variablen:
            raise ValueError("Mindestens eine Variable muss angegeben werden")

        # Parse den String mit SymPy
        try:
            term_sympy = sp.sympify(term_string, locals=symbol_mapping)  # type: ignore
        except Exception as e:
            raise ValueError(f"Konnte Term '{term_string}' nicht parsen: {e}")

        # Erstelle neue ParametrischeFunktion direkt mit Sympy-Term
        neue_funktion = cls.__new__(cls)
        neue_funktion._term_sympy = term_sympy
        neue_funktion.variablen = variablen
        neue_funktion.parameter_objekte = parameter_objekte
        neue_funktion._parameternamen = {p.name for p in parameter_objekte}
        neue_funktion._variablennamen = {v.name for v in variablen}
        neue_funktion._koeffizienten_cache = None

        return neue_funktion

    @classmethod
    def _extrahiere_koeffizienten_aus_term(
        cls, term_sympy: sp.Expr, variable: Variable, parameter_objekte: list
    ) -> "ParametrischeFunktion":
        """
        Extrahiert Koeffizienten aus einem SymPy-Term und erstellt ParametrischeFunktion

        Args:
            term_sympy: Geparster SymPy-Ausdruck
            variable: Die Hauptvariable des Terms
            parameter_objekte: Liste der Parameter-Objekte
        """
        # Erstelle eine Liste für die Koeffizienten
        koeffizienten = []

        # Bestimme den Grad des Polynoms
        try:
            grad = sp.degree(term_sympy, variable.symbol)
        except Exception:
            # Wenn es kein Polynom ist, versuchen wir es als konstanten Term
            grad = 0

        # Für jeden Grad von 0 bis max_grad den Koeffizienten extrahieren
        for i in range(grad + 1):
            koeffizient = term_sympy.coeff(variable.symbol, i)
            koeffizienten.append(koeffizient)

        # Ersetze numerische Koeffizienten durch floats
        finale_koeffizienten = []
        parameter_namen = {p.name: p for p in parameter_objekte}

        for koeff in koeffizienten:
            if koeff.is_number:
                # Numerischer Koeffizient
                finale_koeffizienten.append(float(koeff))
            elif koeff.is_symbol and koeff.name in parameter_namen:
                # Parameter
                finale_koeffizienten.append(parameter_namen[koeff.name])
            elif isinstance(koeff, sp.Mul):
                # Produkt aus Parameter und Zahl (z.B. 2*a)
                # Zerlege in Faktoren und finde den Parameter
                faktoren = sp.Mul.make_args(koeff)
                param_faktor = None
                zahl_faktor = 1

                for faktor in faktoren:
                    if (
                        faktor.is_symbol
                        and hasattr(faktor, "name")
                        and faktor.name in parameter_namen
                    ):
                        param_faktor = parameter_namen[faktor.name]
                    elif faktor.is_number:
                        zahl_faktor = float(faktor)

                if param_faktor is not None:
                    # Erstelle einen neuen Parameter mit dem Skalierungsfaktor
                    # Dies ist eine Vereinfachung - in einer vollständigen Implementation
                    # müsste man komplexere Ausdrücke handhaben
                    finale_koeffizienten.append(param_faktor)
                else:
                    # Kein Parameter gefunden, als Zahl behandeln
                    finale_koeffizienten.append(zahl_faktor)
            else:
                # Komplexerer Ausdruck - für jetzt als Fehler behandeln
                raise ValueError(f"Komplexer Koeffizient nicht unterstützt: {koeff}")

        # Erstelle die ParametrischeFunktion
        return cls(finale_koeffizienten, [variable])

    def __repr__(self) -> str:
        return f"ParametrischeFunktion({self.koeffizienten}, {self.variablen})"

    def __str__(self) -> str:
        return self.term()

    def term(self) -> str:
        """Gibt den Term als lesbaren String zurück"""
        # Verwende direkt den Sympy-Term für die Darstellung
        # Das ist robuster als die Koeffizienten-Extraktion
        return str(self.term_sympy)

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

        # Prüfe, ob alle benötigten Parameter angegeben wurden
        fehlende_parameter = []
        for param in self.parameter_objekte:
            if param.name not in werte:
                fehlende_parameter.append(param.name)

        if fehlende_parameter:
            raise ValueError(
                f"Es fehlen Parameter-Werte für: {', '.join(fehlende_parameter)}. "
                f"Bitte gib Werte für alle Parameter an: {', '.join(self._parameternamen)}"
            )

        # Ersetze Parameter durch konkrete Werte im Sympy-Term
        substitutions = {}
        for param_name, wert in werte.items():
            if param_name in self._parameternamen:
                substitutions[sp.Symbol(param_name)] = wert

        konkreter_term = self.term_sympy.subs(substitutions)

        # Extrahiere Koeffizienten aus dem konkreten Term
        try:
            variable_symbol = self.variablen[0].symbol
            poly = sp.Poly(konkreter_term, variable_symbol)
            koeffizienten_sympy = poly.all_coeffs()
            koeffizienten_sympy.reverse()  # [c0, c1, c2, ...]

            # Konvertiere zu float
            konkrete_koeffizienten = [float(k) for k in koeffizienten_sympy]

        except Exception:
            # Fallback: Konstante Funktion
            konkrete_koeffizienten = [float(konkreter_term)]

        return GanzrationaleFunktion(konkrete_koeffizienten)

    def löse_für_x(
        self,
        parameter_wert: float | dict[str, float],
        ziel_wert: float = 0,
        real: bool = True,
        runden=None,
    ) -> list:
        """Löst f_c(x) = ziel_wert für konkreten Parameterwert c

        Args:
            parameter_wert: Wert für den Parameter (float) oder Dict mit mehreren Parametern
            ziel_wert: Zielwert der Gleichung (Standard 0)
            real: Nur reelle Lösungen zurückgeben (Standard True)
            runden: Anzahl Nachkommastellen für Rundung (None = exakt)

        Returns:
            list: Liste der x-Lösungen

        Beispiele:
            >>> x = Variable("x")
            >>> a = Parameter("a")
            >>> f = ParametrischeFunktion([0, 1, a], [x])  # ax² + x
            >>> f.löse_für_x(3, 17)     # Löst 3x² + x = 17
            >>> f.löse_für_x(-1, 0)    # Löst -x² + x = 0
        """
        try:
            # Konvertiere parameter_wert zu Dictionary
            if isinstance(parameter_wert, (int, float)):
                if not self.parameter_objekte:
                    raise ValueError("Die Funktion hat keine Parameter")
                parameter_dict = {self.parameter_objekte[0].name: parameter_wert}
            elif isinstance(parameter_wert, dict):
                parameter_dict = parameter_wert
            else:
                raise ValueError(
                    "parameter_wert muss eine Zahl oder ein Dictionary sein"
                )

            # Erzeuge konkrete Funktion und löse Gleichung
            f_konkret = self.mit_wert(**parameter_dict)
            return f_konkret.löse_gleichung(ziel_wert, real, runden)
        except ValueError as e:
            # Schülerfreundliche Fehlermeldung
            if "Es fehlen Parameter-Werte" in str(e):
                raise e
            else:
                raise ValueError(
                    f"Konnte die Gleichung nicht lösen: {str(e)}. "
                    f"Bitte prüfe deine Parameterwerte und versuche es erneut."
                )
        except Exception as e:
            raise ValueError(
                f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}. "
                f"Bitte prüfe deine Eingabe und versuche es erneut."
            )

    def löse_für_parameter(
        self, x_wert: float | str | sp.Expr, ziel_wert: float = 0
    ) -> list:
        """Löst f_a(x_wert) = ziel_wert für Parameter a

        Args:
            x_wert: x-Wert (Zahl, String wie "a/2", oder SymPy-Ausdruck)
            ziel_wert: Zielwert der Gleichung (Standard 0)

        Returns:
            list: Liste der Parameter-Lösungen

        Beispiele:
            >>> x = Variable("x")
            >>> a = Parameter("a")
            >>> f = ParametrischeFunktion([0, 1, a], [x])  # ax² + x
            >>> f.löse_für_parameter("a/2", 1)  # Löst a(a/2)² + (a/2) = 1
            >>> f.löse_für_parameter(2, 5)      # Löst a(2)² + 2 = 5
        """
        try:
            # Finde Parameter und Variable automatisch
            parameter_objekte = [
                k for k in self.koeffizienten if isinstance(k, Parameter)
            ]
            if not parameter_objekte:
                raise ValueError("Keine Parameter in der Funktion gefunden")

            param_symbol = parameter_objekte[0].symbol
            var_symbol = self.variablen[0].symbol

            # Verarbeite x_wert: Konvertiere zu SymPy-Ausdruck
            if isinstance(x_wert, str):
                # Parse String zu SymPy-Ausdruck
                x_expr = sp.sympify(
                    x_wert,
                    locals={
                        param_symbol.name: param_symbol,
                        var_symbol.name: var_symbol,
                    },
                )  # type: ignore
            elif isinstance(x_wert, (int, float)):
                x_expr = sp.Number(x_wert)
            elif hasattr(x_wert, "is_symbol"):  # SymPy-Objekt
                x_expr = x_wert
            else:
                raise ValueError(f"Unbekannter Typ für x_wert: {type(x_wert)}")

            # Erzeuge Gleichung: f(x_wert) = ziel_wert
            gleichung = sp.Eq(self.term_sympy.subs(var_symbol, x_expr), ziel_wert)

            # Löse nach Parameter auf
            lösungen = sp.solve(gleichung, param_symbol)

            return lösungen if lösungen else []
        except Exception as e:
            print(f"Fehler bei löse_für_parameter mit x_wert={x_wert}: {e}")
            return []

    def ableitung(self, ordnung: int = 1) -> "ParametrischeFunktion":
        """
        Berechnet die symbolische Ableitung der Funktion

        Args:
            ordnung: Ordnung der Ableitung (1 = erste, 2 = zweite, etc.)

        Returns:
            Neue ParametrischeFunktion der abgeleiteten Funktion

        Beispiele:
            >>> x = Variable("x")
            >>> a = Parameter("a")
            >>> b = Parameter("b")
            >>> f = ParametrischeFunktion([a, b, 0], [x])  # ax² + bx
            >>> f_strich = f.ableitung()  # 2ax + b
            >>> f_strich_strich = f.ableitung(2)  # 2a

            # Mit der neuen __call__ Syntax:
            >>> f_strich(2)    # Wert der ersten Ableitung bei x=2
            >>> f.ableitung()(2)  # Direkte Berechnung

        Didaktischer Hinweis:
            Diese Methode ist besonders nützlich, um Schülern zu zeigen,
            wie sich die Koeffizienten einer Funktion beim Ableiten verändern.
            Bei quadratischen Funktionen wird linear, bei linearen wird konstant.
            Die neue __call__ Syntax ermöglicht intuitive Berechnungen wie f'(x).
        """
        if ordnung <= 0:
            return self

        # Berechne Ableitung mit SymPy
        abgeleitet_sympy = sp.diff(self.term_sympy, self.variablen[0].symbol, ordnung)

        # Erstelle neue ParametrischeFunktion mit dem abgeleiteten Term
        neue_funktion = self.__class__.__new__(self.__class__)
        neue_funktion._term_sympy = abgeleitet_sympy
        neue_funktion.variablen = self.variablen.copy()
        neue_funktion.parameter_objekte = self.parameter_objekte.copy()
        neue_funktion._parameternamen = self._parameternamen.copy()
        neue_funktion._variablennamen = self._variablennamen.copy()
        neue_funktion._koeffizienten_cache = None

        return neue_funktion

    def nullstellen(self) -> list[sp.Expr | tuple[sp.Expr, str]]:
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

    def extremstellen(self) -> list[tuple[sp.Expr, str]]:
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
                    except Exception:
                        extremstellen_mit_bedingungen.append((loesung, "Extremstelle"))

            return extremstellen_mit_bedingungen
        except Exception:
            return []

    def wendepunkte(self) -> list[tuple[sp.Expr, sp.Expr, str]]:
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
                    except Exception:
                        wendepunkte_mit_bedingungen.append((loesung, 0, "Wendepunkt"))

            return wendepunkte_mit_bedingungen
        except Exception:
            return []

    def __call__(self, *werte):
        """
        Macht die Funktion aufrufbar: f(2), f(0, 1), etc.

        Args:
            *werte: Numerische Werte für die Variablen in der Reihenfolge der Definition

        Returns:
            Der Funktionswert als SymPy-Ausdruck oder numerischer Wert

        Beispiele:
            >>> x = Variable("x")
            >>> a = Parameter("a")
            >>> f = ParametrischeFunktion([a, 1, 0], [x])  # a*x² + x
            >>> f(2)           # 4a + 2
            >>> f(0)           # 0
            >>> f.mit_wert(a=3)(2)  # 3*4 + 2 = 14

        Didaktischer Hinweis:
            Diese Methode ermöglicht die natürliche mathematische Notation f(x),
            die Schüler aus dem Unterricht kennen. Anstelle der technischen
            Substitution f.term_sympy.subs(x, wert) kann man einfach f(wert) schreiben.
        """
        if len(werte) != len(self.variablen):
            raise ValueError(
                f"Funktion erwartet {len(self.variablen)} Variable(n), "
                f"aber {len(werte)} Wert(e) wurden übergeben. "
                f"Variablen: {[v.name for v in self.variablen]}"
            )

        # Substituiere alle Variablen mit den gegebenen Werten
        ergebnis = self.term_sympy
        for variable, wert in zip(self.variablen, werte, strict=True):
            ergebnis = ergebnis.subs(variable.symbol, wert)

        return ergebnis

    def __eq__(self, anderer_wert):
        """
        Ermöglicht die Gleichungssyntax: f(3) == 7

        Args:
            anderer_wert: Der Wert, mit dem verglichen wird

        Returns:
            LineareGleichung oder NotImplemented

        Beispiele:
            >>> x = Variable("x")
            >>> a = Parameter("a")
            >>> f = ParametrischeFunktion([a, 1, 0], [x])  # a*x² + x
            >>> gleichung = f(3) == 7  # Erzeugt LineareGleichung für 9a + 3 = 7

        Didaktischer Hinweis:
            Diese Syntax ist sehr intuitiv für Schüler, da sie der mathematischen
            Schreibweise "f(x) = wert" entspricht. Das Ergebnis kann direkt für
            Lineare Gleichungssysteme verwendet werden.
        """
        if isinstance(anderer_wert, (int, float)):
            # Erstelle eine Gleichung: f(...) - anderer_wert = 0
            # Import hier, um zyklische Abhängigkeiten zu vermeiden
            try:
                from .lineare_gleichungssysteme import LineareGleichung

                return LineareGleichung.aus_funktion_wert(self, anderer_wert)
            except ImportError:
                # Fallback: NotImplemented zurückgeben, wenn LGS-Modul nicht existiert
                return NotImplemented
        return NotImplemented


# Convenience-Funktionen für häufige Anwendungsfälle
def create_variable(name: str) -> Variable:
    """Erstellt eine Variable (Convenience-Funktion)"""
    return Variable(name)


def create_parameter(name: str) -> Parameter:
    """Erstellt einen Parameter (Convenience-Funktion)"""
    return Parameter(name)


# Didaktische Exception-Klassen
class SchulAnalysisError(Exception):
    """Basis-Exception für das Schul-Analysis Framework"""

    pass


class ParameterFehler(SchulAnalysisError):
    """Exception für Parameter-bezogene Fehler"""

    pass


class EingabeFehler(SchulAnalysisError):
    """Exception für Eingabefehler"""

    pass


class BerechnungsFehler(SchulAnalysisError):
    """Exception für Berechnungsfehler"""

    pass
