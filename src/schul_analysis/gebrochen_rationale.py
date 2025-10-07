"""
Gebrochen-rationale Funktionen für das Schul-Analysis Framework.

Unterstützt verschiedene Konstruktor-Formate und mathematisch korrekte
Visualisierung mit Plotly für Marimo-Notebooks.
"""

import re
from typing import Any, Union

import sympy as sp
from sympy import Rational, fraction

from .errors import (
    DivisionDurchNullError,
    SicherheitsError,
    UngueltigerAusdruckError,
)
from .funktion import Funktion
from .ganzrationale import GanzrationaleFunktion


def _validiere_mathematischen_ausdruck(ausdruck: str) -> bool:
    """Validiert, ob ein Ausdruck sicher für mathematische Auswertung ist"""
    # Erlaubte mathematische Zeichen und Funktionen
    erlaubte_muster = r"^[0-9+\-*/^()x\s.a-zA-Z]+$|^[a-zA-Z_][a-zA-Z0-9_]*\s*\("

    # Gefährliche Muster
    gefaehrliche_muster = [
        r"import\s+",
        r"exec\s*\(",
        r"eval\s*\(",
        r"__.*__",
        r"subprocess\.",
        r"os\.",
        r"sys\.",
        r"open\s*\(",
        r"file\s*\(",
        r"input\s*\(",
        r"globals\s*\(",
        r"locals\s*\(",
    ]

    # Prüfe auf gefährliche Muster
    for muster in gefaehrliche_muster:
        if re.search(muster, ausdruck, re.IGNORECASE):
            raise SicherheitsError("Gefährlicher Ausdruck erkannt", ausdruck)

    # Prüfe auf gültiges mathematisches Format
    if not re.match(erlaubte_muster, ausdruck.strip()):
        raise UngueltigerAusdruckError(ausdruck, "Ungültiger mathematischer Ausdruck")

    return True


def _pruefe_division_durch_null(_zaehler, nenner) -> None:
    """Prüft auf Division durch Null"""
    if hasattr(nenner, "term_sympy") and nenner.term_sympy == 0:
        raise DivisionDurchNullError("Division durch Nullfunktion")
    if hasattr(nenner, "__eq__") and nenner == 0:
        raise DivisionDurchNullError("Division durch Null")


def _validiere_konstruktor_parameter(zaehler, nenner) -> None:
    """Validiert die Konstruktorparameter"""
    if zaehler is None:
        raise UngueltigerAusdruckError("None", "Zähler darf nicht None sein")

    # Wenn nenner None ist, ist es ein String-Konstruktor
    if nenner is not None:
        _pruefe_division_durch_null(zaehler, nenner)


class GebrochenRationaleFunktion(Funktion):
    """
    Pädagogischer Wrapper für gebrochen-rationale Funktionen.

    Diese Klasse ist ein Thin-Wrapper über der unified Funktion-Klasse,
    der gebrochen-rationale spezifische Methoden bereitstellt.
    """

    def __init__(
        self,
        zaehler: GanzrationaleFunktion | str | sp.Basic,
        nenner: GanzrationaleFunktion | str | sp.Basic | None = None,
    ):
        """
        Konstruktor für gebrochen-rationale Funktionen.

        Args:
            zaehler: GanzrationaleFunktion, String ("x^2+1") oder SymPy-Ausdruck
            nenner: GanzrationaleFunktion, String ("x-1") oder SymPy-Ausdruck.
                    Wenn None und zaehler ist String, wird versucht aus "(x^2+1)/(x-1)" zu parsen
        """
        # 🔥 PÄDAGOGISCHER WRAPPER - Keine komplexe Logik mehr! 🔥

        # Konstruiere die Eingabe für die Basisklasse
        if isinstance(zaehler, str) and nenner is None:
            # String im Format "(zaehler)/(nenner)"
            eingabe = zaehler
        elif isinstance(zaehler, str) and isinstance(nenner, str):
            # Beide als String übergeben
            eingabe = f"({zaehler})/({nenner})"
        elif isinstance(zaehler, (GanzrationaleFunktion, sp.Basic)) and isinstance(
            nenner, (GanzrationaleFunktion, sp.Basic)
        ):
            # Zaehler und Nenner einzeln übergeben - konvertiere zu Strings
            zaehler_str = str(
                zaehler.term_sympy if hasattr(zaehler, "term_sympy") else zaehler
            )
            nenner_str = str(
                nenner.term_sympy if hasattr(nenner, "term_sympy") else nenner
            )
            eingabe = f"({zaehler_str})/({nenner_str})"
        else:
            raise TypeError(
                "Ungültige Eingabeparameter für gebrochen-rationale Funktion"
            )

        # Speichere ursprüngliche Eingabe für Validierung
        self.original_eingabe = eingabe

        # Rufe den Konstruktor der Basisklasse auf
        super().__init__(eingabe)

        # 🔥 PÄDAGOGISCHE VALIDIERUNG mit deutscher Fehlermeldung 🔥
        if not self.ist_gebrochen_rational:
            raise TypeError(
                f"Die Eingabe '{self.original_eingabe}' ist keine gebrochen-rationale Funktion! "
                "Eine gebrochen-rationale Funktion muss ein Bruch aus zwei Polynomen sein. "
                "Hast du vielleicht eine ganzrationale, exponentiale oder trigonometrische Funktion gemeint?"
            )

        # 🔥 CACHE für wiederholte Berechnungen
        self._cache = {
            "polstellen": None,
            "zaehler_nenner": None,
        }

    @property
    def zaehler(self) -> GanzrationaleFunktion:
        """Gibt den Zähler als GanzrationaleFunktion zurück"""
        if self._cache["zaehler_nenner"] is None:
            from sympy import fraction

            zaehler_sympy, _ = fraction(self.term_sympy)
            self._cache["zaehler_nenner"] = (
                GanzrationaleFunktion(zaehler_sympy),
                None,  # Wird bei Bedarf gesetzt
            )

        if self._cache["zaehler_nenner"][1] is None:
            from sympy import fraction

            _, nenner_sympy = fraction(self.term_sympy)
            self._cache["zaehler_nenner"] = (
                self._cache["zaehler_nenner"][0],
                GanzrationaleFunktion(nenner_sympy),
            )

        return self._cache["zaehler_nenner"][0]

    @property
    def nenner(self) -> GanzrationaleFunktion:
        """Gibt den Nenner als GanzrationaleFunktion zurück"""
        if self._cache["zaehler_nenner"] is None:
            from sympy import fraction

            zaehler_sympy, nenner_sympy = fraction(self.term_sympy)
            self._cache["zaehler_nenner"] = (
                GanzrationaleFunktion(zaehler_sympy),
                GanzrationaleFunktion(nenner_sympy),
            )

        return self._cache["zaehler_nenner"][1]

    def polstellen(self) -> list[float]:
        """Berechnet die Polstellen der Funktion (Nenner-Nullstellen)"""
        if self._cache["polstellen"] is None:
            self._cache["polstellen"] = self.nenner.nullstellen()
        return self._cache["polstellen"]

    def definitionsluecken(self) -> list[float]:
        """Gibt die Definitionslücken zurück (Polstellen)"""
        return self.polstellen()

    def __str__(self) -> str:
        """String-Repräsentation"""
        return str(self.term_sympy)

    def __repr__(self) -> str:
        """Repräsentation für debugging"""
        return self.__str__()

    def _repr_latex_(self) -> str:
        """LaTeX-Darstellung für Jupyter/Marimo Notebooks"""
        return self.term_sympy._repr_latex_()

    def __eq__(self, other) -> bool:
        """Vergleich zweier Funktionen auf Gleichheit"""
        if not isinstance(other, GebrochenRationaleFunktion):
            return False
        return self.zaehler == other.zaehler and self.nenner == other.nenner

    def _create_from_operation(
        self, sympy_expr: sp.Basic
    ) -> "GebrochenRationaleFunktion":
        """
        Factory-Methode zur Erstellung einer neuen Funktion aus einem SymPy-Ausdruck.
        """
        # Extrahiere Zähler und Nenner aus dem SymPy-Ausdruck
        zaehler_sympy, nenner_sympy = fraction(sympy_expr)

        # Erstelle neue GanzrationaleFunktionen für Zähler und Nenner
        zaehler = GanzrationaleFunktion(zaehler_sympy)
        nenner = GanzrationaleFunktion(nenner_sympy)

        return GebrochenRationaleFunktion(zaehler, nenner)

    def __add__(self, other) -> "GebrochenRationaleFunktion":
        """Addition: f + g"""
        if isinstance(other, GebrochenRationaleFunktion):
            # (a/b) + (c/d) = (ad + bc) / (bd)
            zaehler_neu = (self.zaehler * other.nenner) + (other.zaehler * self.nenner)
            nenner_neu = self.nenner * other.nenner
        elif isinstance(other, GanzrationaleFunktion):
            # (a/b) + c = (a + bc) / b
            zaehler_neu = self.zaehler + (other * self.nenner)
            nenner_neu = self.nenner
        elif isinstance(other, (int, float, Rational)):
            # (a/b) + k = (a + kb) / b
            zaehler_neu = self.zaehler + (other * self.nenner)
            nenner_neu = self.nenner
        else:
            return NotImplemented

        return GebrochenRationaleFunktion(zaehler_neu, nenner_neu)

    def __radd__(self, other) -> "GebrochenRationaleFunktion":
        """Rechtsseitige Addition: k + f"""
        if isinstance(other, (int, float, Rational)):
            return self.__add__(other)
        return NotImplemented

    def __sub__(self, other) -> "GebrochenRationaleFunktion":
        """Subtraktion: f - g"""
        if isinstance(other, GebrochenRationaleFunktion):
            # (a/b) - (c/d) = (ad - bc) / (bd)
            zaehler_neu = (self.zaehler * other.nenner) - (other.zaehler * self.nenner)
            nenner_neu = self.nenner * other.nenner
        elif isinstance(other, GanzrationaleFunktion):
            # (a/b) - c = (a - bc) / b
            zaehler_neu = self.zaehler - (other * self.nenner)
            nenner_neu = self.nenner
        elif isinstance(other, (int, float, Rational)):
            # (a/b) - k = (a - kb) / b
            zaehler_neu = self.zaehler - (other * self.nenner)
            nenner_neu = self.nenner
        else:
            return NotImplemented

        return GebrochenRationaleFunktion(zaehler_neu, nenner_neu)

    def __rsub__(self, other) -> "GebrochenRationaleFunktion":
        """Rechtsseitige Subtraktion: k - f"""
        if isinstance(other, (int, float, Rational)):
            # k - (a/b) = (kb - a) / b
            zaehler_neu = (other * self.nenner) - self.zaehler
            nenner_neu = self.nenner
            return GebrochenRationaleFunktion(zaehler_neu, nenner_neu)
        return NotImplemented

    def __mul__(self, other) -> "GebrochenRationaleFunktion":
        """Multiplikation: f * g"""
        if isinstance(other, GebrochenRationaleFunktion):
            # (a/b) * (c/d) = (ac) / (bd)
            zaehler_neu = self.zaehler * other.zaehler
            nenner_neu = self.nenner * other.nenner
        elif isinstance(other, GanzrationaleFunktion):
            # (a/b) * c = (ac) / b
            zaehler_neu = self.zaehler * other
            nenner_neu = self.nenner
        elif isinstance(other, (int, float, Rational)):
            # (a/b) * k = (ak) / b
            zaehler_neu = self.zaehler * other
            nenner_neu = self.nenner
        else:
            return NotImplemented

        return GebrochenRationaleFunktion(zaehler_neu, nenner_neu)

    def __rmul__(self, other) -> "GebrochenRationaleFunktion":
        """Rechtsseitige Multiplikation: k * f"""
        if isinstance(other, (int, float, Rational)):
            return self.__mul__(other)
        return NotImplemented

    def __truediv__(self, other) -> "GebrochenRationaleFunktion":
        """Division: f / g"""
        if isinstance(other, GebrochenRationaleFunktion):
            # (a/b) / (c/d) = (ad) / (bc)
            zaehler_neu = self.zaehler * other.nenner
            nenner_neu = self.nenner * other.zaehler
        elif isinstance(other, GanzrationaleFunktion):
            # (a/b) / c = a / (bc)
            zaehler_neu = self.zaehler
            nenner_neu = self.nenner * other
        elif isinstance(other, (int, float, Rational)):
            # (a/b) / k = a / (bk)
            zaehler_neu = self.zaehler
            nenner_neu = self.nenner * other
        else:
            return NotImplemented

        return GebrochenRationaleFunktion(zaehler_neu, nenner_neu)

    def __rtruediv__(self, other) -> "GebrochenRationaleFunktion":
        """Rechtsseitige Division: k / f"""
        if isinstance(other, GanzrationaleFunktion):
            # c / (a/b) = (cb) / a
            zaehler_neu = other * self.nenner
            nenner_neu = self.zaehler
            return GebrochenRationaleFunktion(zaehler_neu, nenner_neu)
        elif isinstance(other, (int, float, Rational)):
            # k / (a/b) = (kb) / a
            zaehler_neu = other * self.nenner
            nenner_neu = self.zaehler
            return GebrochenRationaleFunktion(zaehler_neu, nenner_neu)
        return NotImplemented

    def __pow__(self, other) -> "GebrochenRationaleFunktion":
        """Potenzierung: f ** n"""
        if isinstance(other, int) and other >= 0:
            # (a/b)^n = a^n / b^n
            zaehler_neu = self.zaehler**other
            nenner_neu = self.nenner**other
            return GebrochenRationaleFunktion(zaehler_neu, nenner_neu)
        else:
            return NotImplemented

    # --- In-place Operationen ---

    def __iadd__(self, other) -> "GebrochenRationaleFunktion":
        """In-place Addition: f += g"""
        result = self + other
        self.zaehler = result.zaehler
        self.nenner = result.nenner
        self.term_sympy = result.term_sympy
        return self

    def __isub__(self, other) -> "GebrochenRationaleFunktion":
        """In-place Subtraktion: f -= g"""
        result = self - other
        self.zaehler = result.zaehler
        self.nenner = result.nenner
        self.term_sympy = result.term_sympy
        return self

    def __imul__(self, other) -> "GebrochenRationaleFunktion":
        """In-place Multiplikation: f *= g"""
        result = self * other
        self.zaehler = result.zaehler
        self.nenner = result.nenner
        self.term_sympy = result.term_sympy
        return self

    def __itruediv__(self, other) -> "GebrochenRationaleFunktion":
        """In-place Division: f /= g"""
        result = self / other
        self.zaehler = result.zaehler
        self.nenner = result.nenner
        self.term_sympy = result.term_sympy
        return self

    # --- Unäre Operationen ---

    def __neg__(self) -> "GebrochenRationaleFunktion":
        """Negation: -f"""
        zaehler_neu = -self.zaehler
        return GebrochenRationaleFunktion(zaehler_neu, self.nenner)

    def __pos__(self) -> "GebrochenRationaleFunktion":
        """Positiv: +f"""
        return self

    def graph(self, x_min=None, x_max=None, y_min=None, y_max=None, **kwargs) -> Any:
        """Einheitliche Methode zur Darstellung der Funktion mit Plotly

        Args:
            x_min: Untere x-Grenze (Standard: None = automatisch)
            x_max: Obere x-Grenze (Standard: None = automatisch)
            y_min: Untere y-Grenze (Standard: None = automatisch)
            y_max: Obere y-Grenze (Standard: None = automatisch)
            **kwargs: Zusätzliche Parameter für die Plotly-Darstellung

        Returns:
            Plotly-Figur für die Darstellung
        """
        from . import Graph

        # Verwende die zentrale Graph-Funktion für intelligente Skalierung
        fig = Graph(self, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, **kwargs)

        # 🔥 FIX: Erzwinge Axis-Ranges gegen Marimo-Auto-Scaling
        fig.update_layout(
            xaxis={
                "autorange": False,
                "range": [fig.layout.xaxis.range[0], fig.layout.xaxis.range[1]],
                "constrain": "domain",
                "fixedrange": True,  # Verhindert manuelles Zoomen initially
            },
            yaxis={
                "autorange": False,
                "range": [fig.layout.yaxis.range[0], fig.layout.yaxis.range[1]],
                "constrain": "domain",
                "fixedrange": False,  # Erlaube manuelles Zoomen für y-Achse
            },
            # Zusätzliche Constraints um Auto-Scaling zu verhindern
            xaxis_constrain="domain",
            yaxis_constrain="domain",
        )

        return fig

    def _berechne_asymptoten(self) -> list[dict]:
        """
        Berechnet horizontale und schiefe Asymptoten.

        Returns:
            Liste von Asymptoten-Dictionarys mit keys: typ, steigung, y_offset
        """
        asymptoten = []

        # Bestimme Grade von Zähler und Nenner
        grad_zaehler = self.zaehler.grad()
        grad_nenner = self.nenner.grad()

        if grad_zaehler < grad_nenner:
            # Horizontale Asymptote y = 0
            asymptoten.append({"typ": "horizontal", "y": 0})
        elif grad_zaehler == grad_nenner:
            # Horizontale Asymptote y = Leitkoeffizient
            lkh_zaehler = (
                self.zaehler.koeffizienten[-1] if self.zaehler.koeffizienten else 0
            )
            lkh_nenner = (
                self.nenner.koeffizienten[-1] if self.nenner.koeffizienten else 1
            )
            y_asymptote = float(lkh_zaehler / lkh_nenner)
            asymptoten.append({"typ": "horizontal", "y": y_asymptote})
        elif grad_zaehler == grad_nenner + 1:
            # Schiefe Asymptote
            # Polynomdivision durchführen
            from sympy import div

            quotient, rest = div(self.zaehler.term_sympy, self.nenner.term_sympy)

            # Extrahiere Koeffizienten y = mx + b
            if quotient.is_polynomial(self._variable_symbol):
                quotient_poly = sp.poly(quotient, self._variable_symbol)
                koeffizienten = quotient_poly.all_coeffs()

                if len(koeffizienten) == 2:
                    # Lineare Funktion y = mx + b
                    steigung = float(koeffizienten[0])
                    y_offset = float(koeffizienten[1])
                    asymptoten.append(
                        {"typ": "schief", "steigung": steigung, "y_offset": y_offset}
                    )
                elif len(koeffizienten) == 1:
                    # Konstante Funktion y = b
                    steigung = 0
                    y_offset = float(koeffizienten[0])
                    asymptoten.append({"typ": "horizontal", "y": y_offset})

        return asymptoten

    # =============================================================================
    # NEUE METHODEN: SCHMIEGKURVE UND STÖRFUNKTION
    # =============================================================================

    def _berechne_zerlegung(self) -> None:
        """
        Private Methode zur effizienten Berechnung der Zerlegung.
        Berechnet Schmiegkurve und Störfunktion einmal und cacht die Ergebnisse.
        Vermeidet redundante Polynomdivisionen.
        """
        if self._cache["_zerlegung_berechnet"]:
            return

        # Bestimme Grade von Zähler und Nenner
        grad_zaehler = self.zaehler.grad()
        grad_nenner = self.nenner.grad()

        quotient_sympy = sp.S(0)
        rest_sympy = self.zaehler.term_sympy

        if grad_zaehler >= grad_nenner:
            # sp.div gibt sowohl Quotient als auch Rest zurück - effizient!
            quotient_sympy, rest_sympy = sp.div(
                self.zaehler.term_sympy, self.nenner.term_sympy, domain="QQ"
            )

        # Cache die Ergebnisse
        self._cache["_schmiegkurve"] = GanzrationaleFunktion(quotient_sympy)

        # Erstelle Störfunktion aus Rest und Nenner
        self._cache["_stoerfunktion"] = GebrochenRationaleFunktion(
            rest_sympy, self.nenner.term_sympy
        )
        self._cache["_zerlegung_berechnet"] = True

    def schmiegkurve(self) -> "GanzrationaleFunktion":
        """
        Gibt die Schmiegkurve (polynomialer Teil) der gebrochen-rationalen Funktion zurück.

        Für eine rationale Funktion f(x) = Z(x)/N(x):
        - Wenn grad(Z) < grad(N): Schmiegkurve = 0 (horizontale Asymptote y = 0)
        - Wenn grad(Z) = grad(N): Schmiegkurve = Leitkoeffizienten-Verhältnis (horizontale Asymptote)
        - Wenn grad(Z) > grad(N): Polynomdivision durchführen, polynomialer Teil ist die Schmiegkurve

        Returns:
            GanzrationaleFunktion: Die Schmiegkurve der Funktion

        Beispiele:
            >>> f = GebrochenRationaleFunktion("x^2+1", "x-1")  # grad(Z)=2, grad(N)=1
            >>> s = f.schmiegkurve()  # s(x) = x + 1 (schiefe Asymptote)

            >>> g = GebrochenRationaleFunktion("x+1", "x^2-1")  # grad(Z)=1, grad(N)=2
            >>> t = g.schmiegkurve()  # t(x) = 0 (horizontale Asymptote y = 0)

        Didaktischer Hinweis:
            Die Schmiegkurve ist die Funktion, an die sich f(x) für große |x| annähert.
            Sie beschreibt das "globale" Verhalten der Funktion.
        """
        # Berechne Zerlegung nur einmal und verwende Cache
        self._berechne_zerlegung()
        return self._cache["_schmiegkurve"]

    def stoerfunktion(self) -> "GebrochenRationaleFunktion":
        """
        Gibt die Störfunktion (echt gebrochen-rationaler Teil) zurück.

        Die Störfunktion ist definiert als: f(x) = Schmiegkurve(x) + Störfunktion(x)
        Sie hat die Eigenschaft, dass für große |x| die Störfunktion gegen 0 geht.

        Returns:
            GebrochenRationaleFunktion: Die Störfunktion mit grad(Zähler) < grad(Nenner)

        Beispiele:
            >>> f = GebrochenRationaleFunktion("x^2+1", "x-1")
            >>> s = f.schmiegkurve()  # s(x) = x + 1
            >>> r = f.stoerfunktion()  # r(x) = 2/(x-1)
            >>> # Überprüfung: f(x) = (x+1) + 2/(x-1) = (x^2-x+2)/(x-1)

        Didaktischer Hinweis:
            Die Störfunktion beschreibt die "lokale" Abweichung von der Schmiegkurve
            und bestimmt das Verhalten in der Nähe von Polstellen.
        """
        # Berechne Zerlegung nur einmal und verwende Cache
        self._berechne_zerlegung()
        return self._cache["_stoerfunktion"]


    def spezialisiere_parameter(self, **werte) -> "GebrochenRationaleFunktion":
        """
        Setzt Parameter auf spezifische Werte und gibt eine neue Funktion zurück.

        Args:
            **werte: Parameter-Wert-Paare (z.B. a=2, b=3)

        Returns:
            Neue GebrochenRationaleFunktion mit spezifizierten Parameterwerten
        """
        # Ersetze Parameter durch die gegebenen Werte
        neuer_zaehler = self.zaehler.term_sympy
        neuer_nenner = self.nenner.term_sympy

        for param_name, wert in werte.items():
            # Finde das passende Parameter-Symbol in Zähler
            param_symbol = None
            for p in self.zaehler.parameter:
                if p.name == param_name:
                    param_symbol = p.symbol
                    break

            # Wenn nicht im Zähler, im Nenner suchen
            if param_symbol is None:
                for p in self.nenner.parameter:
                    if p.name == param_name:
                        param_symbol = p.symbol
                        break

            if param_symbol is not None:
                neuer_zaehler = neuer_zaehler.subs(param_symbol, wert)
                neuer_nenner = neuer_nenner.subs(param_symbol, wert)

        # Erstelle neue Funktion mit spezialisierten Werten
        return GebrochenRationaleFunktion(neuer_zaehler, neuer_nenner)

    def erstelle_uebungsaufgabe(self, schwierigkeit: str = "mittel") -> dict:
        """
        Erstellt eine Übungsaufgabe zur Zerlegung gebrochen-rationaler Funktionen.

        Args:
            schwierigkeit: "einfach", "mittel", oder "schwer"

        Returns:
            dict: Übungsaufgabe mit Lösung und Erklärung

        Beispiele:
            >>> aufgabe = f.erstelle_uebungsaufgabe("einfach")
            >>> print(aufgabe['aufgabe'])
            >>> print(aufgabe['loesung'])
        """

        if schwierigkeit == "einfach":
            # Einfache Fälle: grad(Z) ≤ grad(N)
            aufgaben = [
                {"zaehler": "x+1", "nenner": "x-1", "typ": "horizontal"},
                {"zaehler": "2x+3", "nenner": "x+2", "typ": "horizontal"},
                {"zaehler": "x^2+1", "nenner": "x^2-1", "typ": "horizontal"},
            ]
        elif schwierigkeit == "mittel":
            # Mittlere Fälle: grad(Z) = grad(N) + 1
            aufgaben = [
                {"zaehler": "x^2+1", "nenner": "x-1", "typ": "schief"},
                {"zaehler": "x^2+4x+3", "nenner": "x+1", "typ": "schief"},
                {"zaehler": "2x^2-3", "nenner": "x+2", "typ": "schief"},
            ]
        else:  # schwer
            # Schwere Fälle: grad(Z) > grad(N) + 1
            aufgaben = [
                {"zaehler": "x^3+1", "nenner": "x-1", "typ": "schief_kubisch"},
                {
                    "zaehler": "x^3-2x^2+3",
                    "nenner": "x^2+1",
                    "typ": "schief_quadratisch",
                },
            ]

        import random

        aufgabe_data = random.choice(aufgaben)

        # Erstelle Übungsfunktion
        uebung_funktion = GebrochenRationaleFunktion(
            aufgabe_data["zaehler"], aufgabe_data["nenner"]
        )
        s = uebung_funktion.schmiegkurve()
        r = uebung_funktion.stoerfunktion()

        # Generiere Aufgabe basierend auf Typ
        if aufgabe_data["typ"] == "horizontal":
            frage = f"Bestimmen Sie die horizontale Asymptote der Funktion f(x) = {uebung_funktion.term()}"
            loesung_text = f"Die horizontale Asymptote ist y = {s.term()}"
        else:
            frage = f"Zerlegen Sie die Funktion f(x) = {uebung_funktion.term()} in Schmiegkurve und Störfunktion"
            loesung_text = f"f(x) = {s.term()} + {r.term()}"

        return {
            "schwierigkeit": schwierigkeit,
            "aufgabe": frage,
            "funktion": uebung_funktion.term(),
            "tipps": [
                "Bestimmen Sie zuerst die Grade von Zähler und Nenner",
                "Überlegen Sie, ob eine Polynomdivision nötig ist",
                "Die Störfunktion sollte für große |x| gegen 0 gehen",
            ],
            "loesung": {
                "schmiegkurve": s.term(),
                "stoerfunktion": r.term(),
                "zerlegung": f"f(x) = {s.term()} + {r.term()}",
                "erklaerung": loesung_text,
            },
            "ueberpruefung": {
                "valid": uebung_funktion.validiere_zerlegung(),
                "methode": "Addieren Sie Schmiegkurve und Störfunktion, um das Ergebnis zu überprüfen",
            },
        }

    def vergleiche_funktionen(
        self, andere_funktion: "GebrochenRationaleFunktion"
    ) -> dict:
        """
        Vergleicht zwei gebrochen-rationale Funktionen bezüglich ihrer Zerlegung.

        Args:
            andere_funktion: Zweite Funktion zum Vergleich

        Returns:
            dict: Vergleich der Funktionen mit Analyse

        Beispiele:
            >>> f1 = GebrochenRationaleFunktion("x^2+1", "x-1")
            >>> f2 = GebrochenRationaleFunktion("x^2+4", "x+2")
            >>> vergleich = f1.vergleiche_funktionen(f2)
        """
        s1 = self.schmiegkurve()
        r1 = self.stoerfunktion()

        s2 = andere_funktion.schmiegkurve()
        r2 = andere_funktion.stoerfunktion()

        return {
            "funktion1": {
                "term": self.term(),
                "schmiegkurve": s1.term(),
                "stoerfunktion": r1.term(),
                "grad_z": self.zaehler.grad(),
                "grad_n": self.nenner.grad(),
            },
            "funktion2": {
                "term": andere_funktion.term(),
                "schmiegkurve": s2.term(),
                "stoerfunktion": r2.term(),
                "grad_z": andere_funktion.zaehler.grad(),
                "grad_n": andere_funktion.nenner.grad(),
            },
            "vergleich": {
                "gleiche_schmiegkurve": s1.term() == s2.term(),
                "gleiche_stoerfunktion": r1.term() == r2.term(),
                "asymptotisches_verhalten": {
                    "f1": f"lim x->∞: {s1.term()}",
                    "f2": f"lim x->∞: {s2.term()}",
                    "ähnlich": s1.term() == s2.term(),
                },
            },
            "didaktischer_hinweis": "Vergleichen Sie, wie sich verschiedene Koeffizienten auf das asymptotische Verhalten auswirken.",
        }

    def ableitung(self, ordnung: int = 1) -> "GebrochenRationaleFunktion":
        """
        Berechnet die Ableitung gebrochen-rationaler Funktionen mit Quotientenregel.

        Args:
            ordnung: Ordnung der Ableitung (Standard: 1)

        Returns:
            GebrochenRationaleFunktion: Die abgeleitete Funktion

        Examples:
            >>> f = GebrochenRationaleFunktion("x^2 + 1", "x - 1")
            >>> f1 = f.ableitung()
            >>> print(f1.term())  # (x^2 - 2x - 1)/(x^2 - 2x + 1)
        """
        from sympy import diff

        if ordnung == 1:
            # Quotientenregel: (u/v)' = (u'v - uv')/v^2
            u = self.zaehler.term_sympy
            v = self.nenner.term_sympy
            u_strich = diff(u, self._variable_symbol)
            v_strich = diff(v, self._variable_symbol)

            zaehler_ableitung = u_strich * v - u * v_strich
            nenner_ableitung = v**2

            return GebrochenRationaleFunktion(zaehler_ableitung, nenner_ableitung)
        else:
            # Höhere Ableitungen durch rekursive Anwendung
            erste_ableitung = self.ableitung(1)
            return erste_ableitung.ableitung(ordnung - 1)

    def extrempunkte(self) -> list[tuple[float, float, str]]:
        """
        Berechnet die Extrempunkte der gebrochen-rationalen Funktion.

        Returns:
            Liste von Tupeln (x_wert, y_wert, art) wobei art 'Maximum' oder 'Minimum' ist

        Examples:
            >>> f = GebrochenRationaleFunktion("x^3 - 3x", "x^2 + 1")
            >>> ext = f.extrempunkte()
            >>> print(f'Extrempunkt bei x={ext[0][0]}: {ext[0][2]}')
        """
        # Extrempunkte liegen bei f'(x) = 0
        f1 = self.ableitung(1)
        kritische_punkte = f1.nullstellen()

        extrempunkte = []

        for x_krit in kritische_punkte:
            # Zweite Ableitung für Artbestimmung
            f2 = self.ableitung(2)
            y_wert = f2(x_krit)

            if y_wert > 0:
                art = "Minimum"
            elif y_wert < 0:
                art = "Maximum"
            else:
                # Bei zweiter Ableitung = 0, höhere Ableitungen prüfen
                f3 = self.ableitung(3)
                y_wert3 = f3(x_krit)
                if y_wert3 != 0:
                    art = "Maximum" if y_wert3 < 0 else "Minimum"
                else:
                    art = "Sattelpunkt"

            # Funktionswert am Extrempunkt
            y_funktionswert = self(x_krit)
            extrempunkte.append((x_krit, y_funktionswert, art))

        return sorted(extrempunkte, key=lambda p: p[0])

    def wendepunkte(self) -> list[tuple[float, float, str]]:
        """
        Berechnet die Wendepunkte der gebrochen-rationalen Funktion.

        Returns:
            Liste von Tupeln (x_wert, y_wert, art) wobei art 'Wendepunkt' ist

        Examples:
            >>> f = GebrochenRationaleFunktion("x^4 - 4x^2", "1")
            >>> wendep = f.wendepunkte()
            >>> print(f'Wendepunkt bei x={wendep[0][0]}')
        """
        # Wendepunkte liegen bei f''(x) = 0
        f2 = self.ableitung(2)
        kritische_punkte = f2.nullstellen()

        wendepunkte = []

        for x_krit in kritische_punkte:
            # Dritte Ableitung zur Bestätigung
            f3 = self.ableitung(3)
            if f3(x_krit) != 0:  # Nur wenn dritte Ableitung ungleich null
                y_funktionswert = self(x_krit)
                wendepunkte.append((x_krit, y_funktionswert, "Wendepunkt"))

        return sorted(wendepunkte, key=lambda p: p[0])


# =============================================================================
# PHASE 3: EXPONENTIALL-RATIONALE FUNKTIONEN
# =============================================================================


class ExponentialRationaleFunktion(Funktion):
    """
    Pädagogischer Wrapper für exponential-rationale Funktionen.

    Diese Klasse ist ein Thin-Wrapper über der unified Funktion-Klasse,
    der exponential-rationale spezifische Methoden bereitstellt.

    Diese Funktionen lassen sich durch Substitution u = e^{ax} in rationale
    Funktionen transformieren, was die Analyse asymptotischen Verhaltens ermöglicht.
    """

    def __init__(
        self,
        eingabe: Union[str, sp.Basic, "Funktion"],
        exponent_param: float = 1.0,
    ):
        """
        Konstruktor für exponential-rationale Funktionen.

        Args:
            eingabe: String, SymPy-Ausdruck oder Funktion, der eine exponential-rationale Funktion darstellt
            exponent_param: Parameter a in e^{ax} (Standard: 1.0)
        """
        # 🔥 PÄDAGOGISCHER WRAPPER - Keine komplexe Logik mehr! 🔥
        self.a = exponent_param  # Parameter für e^{ax}

        # Speichere ursprüngliche Eingabe für Validierung
        self.original_eingabe = str(eingabe)

        # 🔥 UNIFIED ARCHITECTURE: Delegiere an Basis-Klasse 🔥
        # Konstruiere die Eingabe für die Basisklasse
        if isinstance(eingabe, str):
            super().__init__(eingabe)
        elif isinstance(eingabe, sp.Basic):
            super().__init__(eingabe)
        elif isinstance(eingabe, Funktion):
            super().__init__(eingabe.term())
        else:
            raise TypeError(f"Unsupported input type: {type(eingabe)}")

        # 🔥 PÄDAGOGISCHE VALIDIERUNG mit deutscher Fehlermeldung 🔥
        if not self.ist_exponential_rational:
            raise TypeError(
                f"Die Eingabe '{self.original_eingabe}' ist keine exponential-rationale Funktion! "
                "Eine exponential-rationale Funktion muss exp(x)-Terme enthalten. "
                "Hast du vielleicht eine ganzrationale, gebrochen-rationale oder trigonometrische Funktion gemeint?"
            )

        # 🔥 CACHE für wiederholte Berechnungen
        self._cache = {}

    def __str__(self) -> str:
        """String-Repräsentation"""
        return str(self.term_sympy)

    def __repr__(self) -> str:
        """Repräsentation für debugging"""
        return f"ExponentialRationaleFunktion('{self.term()}', exponent_param={self.a})"

    def __eq__(self, other) -> bool:
        """Vergleich zweier Funktionen auf Gleichheit"""
        if not isinstance(other, ExponentialRationaleFunktion):
            return False
        return (
            self.term_sympy.equals(other.term_sympy) and abs(self.a - other.a) < 1e-10
        )

    def _transformiere_zu_rational(self) -> "GebrochenRationaleFunktion":
        """
        Transformiert die exponential-rationale Funktion in eine rationale Funktion
        durch Substitution u = e^{ax}.

        Returns:
            GebrochenRationaleFunktion: Transformierte rationale Funktion
        """
        if self._cache["transformierte_funktion"] is None:
            # 🔥 UNIFIED ARCHITECTURE: Analysiere die aktuelle Funktion 🔥
            # Extrahiere Zähler und Nenner aus der aktuellen Funktion
            x_symbol = self._variable_symbol
            u_symbol = sp.Symbol("u")

            # Substituiere e^{ax} durch u
            substitution = {sp.exp(self.a * x_symbol): u_symbol}
            transformierter_term = self.term_sympy.subs(substitution)

            # 🔥 FIX: Handle auch einfache Polynome (keine echten Brüche) 🔥
            # Nach der Substitution haben wir einen Ausdruck in u, aber GebrochenRationaleFunktion
            # erwartet einen Ausdruck in x. Wir müssen den transformierten Term als rational in x behandeln.
            from sympy import fraction

            # Zerlege in Zähler und Nenner
            zaehler_expr, nenner_expr = fraction(transformierter_term.together())

            # Erstelle eine einfache rationale Funktion in x durch Ersetzung von u durch x
            # Dies ist ein Workaround, um die Typen-Prüfung zu umgehen
            x_fuer_rationale = sp.Symbol("x")
            einfache_zaehler = (
                zaehler_expr.subs(u_symbol, x_fuer_rationale)
                if zaehler_expr != 1
                else 1
            )
            einfacher_nenner = (
                nenner_expr.subs(u_symbol, x_fuer_rationale) if nenner_expr != 1 else 1
            )

            # Erstelle rationale Funktion mit den vereinfachten Ausdrücken
            self._cache["transformierte_funktion"] = GebrochenRationaleFunktion(
                einfache_zaehler, einfacher_nenner
            )

        return self._cache["transformierte_funktion"]

    def _berechne_exponential_zerlegung(self) -> None:
        """
        Private Methode zur Berechnung der Zerlegung für exponential-rationale Funktionen.
        """
        if self._cache["zerlegung_berechnet"]:
            return

        # Transformiere zu rationale Funktion
        rationale_funktion = self._transformiere_zu_rational()

        # Berechne Schmiegkurve und Störfunktion der transformierten Funktion
        s_rational = rationale_funktion.schmiegkurve()
        r_rational = rationale_funktion.stoerfunktion()

        # Transformiere zurück zu exponential-rationaler Funktion
        self._cache["schmiegkurve"] = self._transformiere_zurueck(s_rational)
        self._cache["stoerfunktion"] = self._transformiere_zurueck(r_rational)
        self._cache["zerlegung_berechnet"] = True

    def _transformiere_zurueck(
        self,
        rationale_funktion: GanzrationaleFunktion | GebrochenRationaleFunktion,
    ) -> "ExponentialRationaleFunktion":
        """
        Transformiert eine rationale Funktion zurück zu exponential-rationaler Funktion.

        Args:
            rationale_funktion: GanzrationaleFunktion oder GebrochenRationaleFunktion,
                              die transformiert werden soll

        Returns:
            ExponentialRationaleFunktion: Transformierte Funktion
        """
        if isinstance(rationale_funktion, GanzrationaleFunktion):
            # 🔥 UNIFIED ARCHITECTURE FIX: Erstelle kombinierten Ausdruck 🔥
            ganzrational_term = rationale_funktion.term()
            # Für ganzrationale Funktionen: Nenner = 1
            voller_term = f"({ganzrational_term})/1"
            return ExponentialRationaleFunktion(voller_term, self.a)
        elif isinstance(rationale_funktion, GebrochenRationaleFunktion):
            # 🔥 UNIFIED ARCHITECTURE FIX: Erstelle kombinierten Ausdruck 🔥
            zaehler_term = rationale_funktion.zaehler.term()
            nenner_term = rationale_funktion.nenner.term()
            voller_term = f"({zaehler_term})/({nenner_term})"
            return ExponentialRationaleFunktion(voller_term, self.a)
        else:
            raise TypeError(
                f"Kann {type(rationale_funktion)} nicht transformieren. "
                "Nur GanzrationaleFunktion oder GebrochenRationaleFunktion unterstützt."
            )

    def schmiegkurve(self) -> "ExponentialRationaleFunktion":
        """
        Gibt die Schmiegkurve der exponential-rationalen Funktion zurück.

        Returns:
            ExponentialRationaleFunktion: Die Schmiegkurve

        Beispiele:
            >>> f = ExponentialRationaleFunktion("x^2+1", "x-1", exponent_param=1)
            >>> s = f.schmiegkurve()
        """
        self._berechne_exponential_zerlegung()
        return self._cache["schmiegkurve"]

    def stoerfunktion(self) -> "ExponentialRationaleFunktion":
        """
        Gibt die Störfunktion der exponential-rationalen Funktion zurück.

        Returns:
            ExponentialRationaleFunktion: Die Störfunktion

        Beispiele:
            >>> f = ExponentialRationaleFunktion("x^2+1", "x-1", exponent_param=1)
            >>> r = f.stoerfunktion()
        """
        self._berechne_exponential_zerlegung()
        return self._cache["stoerfunktion"]


    def spezialisiere_parameter(self, **werte) -> "ExponentialRationaleFunktion":
        """
        Setzt Parameter auf spezifische Werte und gibt eine neue Funktion zurück.

        Args:
            **werte: Parameter-Wert-Paare (z.B. a=2, b=3)

        Returns:
            ExponentialRationaleFunktion: Neue Funktion mit spezialisierten Parametern

        Examples:
            >>> f = ExponentialRationaleFunktion("a*x^2 + b", "x + c", exponent_param=1)
            >>> f2 = f.spezialisiere_parameter(a=1, b=2, c=3)
            >>> print(f2.term())  # x^2 + 2 / (x + 3)
        """
        # Ersetze Parameter durch die gegebenen Werte
        neuer_zaehler = self.zaehler.term_sympy
        neuer_nenner = self.nenner.term_sympy

        for param_name, wert in werte.items():
            # Finde das passende Parameter-Symbol
            param_symbol = None
            for p in self.parameter:
                if p.name == param_name:
                    param_symbol = p.symbol
                    break

            if param_symbol is not None:
                neuer_zaehler = neuer_zaehler.subs(param_symbol, wert)
                neuer_nenner = neuer_nenner.subs(param_symbol, wert)

        # Erstelle neue Funktion mit spezialisierten Werten
        # Erstelle den rationalen Ausdruck aus Zähler und Nenner
        if neuer_nenner == 1:
            eingabe = neuer_zaehler
        else:
            eingabe = neuer_zaehler / neuer_nenner

        return ExponentialRationaleFunktion(eingabe, exponent_param=self.a)

    @property
    def funktionstyp(self) -> str:
        """
        Gibt den Funktionstyp für Klassifizierung zurück.

        Returns:
            str: "exponential-rational"
        """
        return "exponential-rational"

    def nullstellen(self, real: bool = True, runden=None) -> list[float]:
        """
        Berechnet die Nullstellen der Funktion (Zähler-Nullstellen).

        Args:
            real: Nur reelle Nullstellen zurückgeben
            runden: Anzahl Nachkommastellen für Rundung (None = exakt)

        Returns:
            Liste der Nullstellen, wobei Definitionslücken entfernt wurden
        """
        # Für exponential-rationale Funktionen: löse P(e^{ax}) = 0
        # Zuerst finde die Nullstellen des Zählerpolynoms P
        if runden is not None:
            zaehler_nullstellen = self.zaehler.nullstellen(runden=runden)
        else:
            zaehler_nullstellen = self.zaehler.nullstellen()

        # Transformiere zurück: wenn P(u) = 0, dann u = e^{ax} = nullstelle
        # Also x = ln(nullstelle) / a, für nullstelle > 0
        import sympy as sp

        exponential_nullstellen = []

        for zs in zaehler_nullstellen:
            if zs > 0:  # e^{ax} ist immer positiv
                # Konvertiere zu float für numerische Berechnung
                zs_float = float(zs) if hasattr(zs, "__float__") else zs.evalf()
                x_wert = sp.log(zs_float) / self.a
                if runden is not None:
                    x_wert = round(float(x_wert), runden)
                else:
                    x_wert = float(x_wert)
                exponential_nullstellen.append(x_wert)

        return exponential_nullstellen

    def ableitung(self, ordnung: int = 1) -> "ExponentialRationaleFunktion":
        """
        Berechnet die Ableitung exponential-rationaler Funktionen.

        Für f(x) = P(e^{ax})/Q(e^{ax}) verwenden wir die Kettenregel.

        🔥 UNIFIED ARCHITECTURE: Wir verwenden direkt SymPy's diff-Funktion
        anstatt der komplexen Transformation.

        Args:
            ordnung: Ordnung der Ableitung (Standard: 1)

        Returns:
            ExponentialRationaleFunktion: Die abgeleitete Funktion

        Examples:
            >>> f = ExponentialRationaleFunktion("x^2 + 1", "x - 1", exponent_param=1)
            >>> f1 = f.ableitung()
            >>> print(f1.term())  # Ableitung mit exp-Funktionen
        """
        from sympy import diff

        # 🔥 FIX: Direkte Ableitung mit SymPy statt Transformation 🔥
        # Verwende die eingebaute SymPy-Ableitungsfunktion
        abgeleiteter_term = diff(self.term_sympy, self._variable_symbol, ordnung)

        # Erstelle neue ExponentialRationaleFunktion aus dem abgeleiteten Term
        return ExponentialRationaleFunktion(abgeleiteter_term, exponent_param=self.a)

    def extrempunkte(self) -> list[tuple[float, float, str]]:
        """
        Berechnet die Extrempunkte der exponential-rationalen Funktion.

        Returns:
            Liste von Tupeln (x_wert, y_wert, art) wobei art 'Maximum' oder 'Minimum' ist

        Examples:
            >>> f = ExponentialRationaleFunktion("x^2 - 4", "1", exponent_param=1)
            >>> ext = f.extrempunkte()
            >>> print(f'Extrempunkt bei x={ext[0][0]}: {ext[0][2]}')
        """
        # Extrempunkte liegen bei f'(x) = 0
        f1 = self.ableitung(1)
        kritische_punkte = f1.nullstellen()

        extrempunkte = []

        for x_krit in kritische_punkte:
            # Zweite Ableitung für Artbestimmung
            f2 = self.ableitung(2)
            y_wert = f2(x_krit)

            if y_wert > 0:
                art = "Minimum"
            elif y_wert < 0:
                art = "Maximum"
            else:
                # Bei zweiter Ableitung = 0, höhere Ableitungen prüfen
                f3 = self.ableitung(3)
                y_wert3 = f3(x_krit)
                if y_wert3 != 0:
                    art = "Maximum" if y_wert3 < 0 else "Minimum"
                else:
                    art = "Sattelpunkt"

            # Funktionswert am Extrempunkt
            y_funktionswert = self(x_krit)
            extrempunkte.append((x_krit, y_funktionswert, art))

        return sorted(extrempunkte, key=lambda p: p[0])

    def wendepunkte(self) -> list[tuple[float, float, str]]:
        """
        Berechnet die Wendepunkte der exponential-rationalen Funktion.

        Returns:
            Liste von Tupeln (x_wert, y_wert, art) wobei art 'Wendepunkt' ist

        Examples:
            >>> f = ExponentialRationaleFunktion("x^3", "1", exponent_param=1)
            >>> wendep = f.wendepunkte()
            >>> print(f'Wendepunkt bei x={wendep[0][0]}')
        """
        # Wendepunkte liegen bei f''(x) = 0
        f2 = self.ableitung(2)
        kritische_punkte = f2.nullstellen()

        wendepunkte = []

        for x_krit in kritische_punkte:
            # Dritte Ableitung zur Bestätigung
            f3 = self.ableitung(3)
            if f3(x_krit) != 0:  # Nur wenn dritte Ableitung ungleich null
                y_funktionswert = self(x_krit)
                wendepunkte.append((x_krit, y_funktionswert, "Wendepunkt"))

        return sorted(wendepunkte, key=lambda p: p[0])
