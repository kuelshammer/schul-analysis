"""
Gebrochen-rationale Funktionen für das Schul-Analysis Framework.

Unterstützt verschiedene Konstruktor-Formate und mathematisch korrekte
Visualisierung mit Plotly für Marimo-Notebooks.
"""

import re
from typing import Any

import plotly.graph_objects as go
import sympy as sp
from sympy import (
    Rational,
    fraction,
    latex,
    symbols,
)

from .errors import (
    DivisionDurchNullError,
    EingabeSyntaxError,
    SicherheitsError,
    UngueltigerAusdruckError,
)
from .ganzrationale import GanzrationaleFunktion


def _validiere_mathematischen_ausdruck(ausdruck: str) -> bool:
    """Validiert, ob ein Ausdruck sicher für mathematische Auswertung ist"""
    # Erlaubte mathematische Zeichen und Funktionen
    erlaubte_muster = r"^[0-9+\-*/^()x\s.]+$|^[a-zA-Z_][a-zA-Z0-9_]*\s*\("

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


class GebrochenRationaleFunktion:
    """
    Repräsentiert eine gebrochen-rationale Funktion f(x) = Z(x)/N(x)
    mit Zähler und Nenner als ganzrationale Funktionen.
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
        # Validiere Konstruktorparameter
        _validiere_konstruktor_parameter(zaehler, nenner)

        # Sicherheitsprüfung für String-Eingaben
        if isinstance(zaehler, str):
            _validiere_mathematischen_ausdruck(zaehler)
        if isinstance(nenner, str):
            _validiere_mathematischen_ausdruck(nenner)
            # Spezielle Prüfung für Division durch Null
            if nenner.strip() == "0":
                raise DivisionDurchNullError()

        self.x = symbols("x")

        # Cache für wiederholte Berechnungen
        self._cache = {
            "polstellen": None,
            "asymptoten": None,
            "nullstellen": None,
            "term_str": None,
            # Cache für Schmiegkurve/Störfunktion Zerlegung
            "_schmiegkurve": None,
            "_stoerfunktion": None,
            "_zerlegung_berechnet": False,
        }

        # Parser für String-Eingabe im Format "(zaehler)/(nenner)"
        if isinstance(zaehler, str) and nenner is None:
            self._parse_string_eingabe(zaehler)
        elif isinstance(zaehler, str) and isinstance(nenner, str):
            # Beide als String übergeben
            self.zaehler = GanzrationaleFunktion(zaehler)
            self.nenner = GanzrationaleFunktion(nenner)
        elif isinstance(zaehler, (GanzrationaleFunktion, sp.Basic)) and isinstance(
            nenner, (GanzrationaleFunktion, sp.Basic)
        ):
            # Zaehler und Nenner einzeln übergeben
            self.zaehler = self._convert_to_ganzrationale(zaehler)
            self.nenner = self._convert_to_ganzrationale(nenner)
        else:
            raise TypeError(
                "Ungültige Eingabeparameter für gebrochen-rationale Funktion"
            )

        # Validiere, dass Nenner nicht Null ist
        if self.nenner.term_sympy == 0:
            raise UngueltigerAusdruckError(
                "Nullfunktion", "Nenner darf nicht die Nullfunktion sein"
            )

        # Erstelle SymPy-Ausdruck für die gesamte Funktion
        self.term_sympy = self.zaehler.term_sympy / self.nenner.term_sympy

        # Kürze die Funktion automatisch
        self._kuerzen()

    def _clear_cache(self):
        """Leert den Cache nach Änderungen an der Funktion"""
        for key in self._cache:
            self._cache[key] = None

    def _parse_string_eingabe(self, eingabe: str):
        """Parst String-Eingabe im Format '(x^2+1)/(x-1)'"""
        eingabe = eingabe.strip()

        if "/" not in eingabe:
            raise EingabeSyntaxError(eingabe, "(zaehler)/(nenner)")

        # Trenne Zaehler und Nenner
        teile = eingabe.split("/", 1)
        zaehler_str = teile[0].strip().lstrip("(").rstrip(")")
        nenner_str = teile[1].strip().lstrip("(").rstrip(")")

        self.zaehler = GanzrationaleFunktion(zaehler_str)
        self.nenner = GanzrationaleFunktion(nenner_str)

    def _convert_to_ganzrationale(
        self, eingabe: GanzrationaleFunktion | str | sp.Basic
    ) -> GanzrationaleFunktion:
        """Konvertiert Eingabe zu GanzrationaleFunktion"""
        if isinstance(eingabe, GanzrationaleFunktion):
            return eingabe
        elif isinstance(eingabe, str):
            return GanzrationaleFunktion(eingabe)
        elif isinstance(eingabe, sp.Basic):
            return GanzrationaleFunktion(eingabe)
        else:
            raise TypeError(
                f"Kann {type(eingabe)} nicht in GanzrationaleFunktion umwandeln"
            )

    def _kuerzen(self):
        """Kürzt die Funktion durch Zähler und Nenner mit ihrem ggT"""
        # Nutze SymPy's cancel() Funktion für robuste Kürzung
        gekuerzter_term = sp.cancel(self.term_sympy)

        # Wenn sich etwas geändert hat, extrahiere Zähler und Nenner neu
        if gekuerzter_term != self.term_sympy:
            self.term_sympy = gekuerzter_term

            # Extrahiere Zähler und Nenner aus dem gekürzten Term
            if gekuerzter_term.is_rational_function(self.x):
                # Zerlege in Zähler und Nenner
                zaehler_expr, nenner_expr = gekuerzter_term.as_numer_denom()

                # Aktualisiere Zähler und Nenner
                self.zaehler = GanzrationaleFunktion(zaehler_expr)
                self.nenner = GanzrationaleFunktion(nenner_expr)

                # Cache leeren nach Änderung
                self._clear_cache()

    def kürzen(self) -> "GebrochenRationaleFunktion":
        """Kürzt die Funktion und gibt sich selbst zurück"""
        self._kuerzen()
        # Stelle sicher, dass der Cache immer geleert wird, auch wenn keine Änderung
        self._clear_cache()
        return self

    def term(self) -> str:
        """Gibt den Term als String zurück"""
        if self._cache["term_str"] is None:
            zaehler_str = self.zaehler.term()
            nenner_str = self.nenner.term()
            self._cache["term_str"] = f"({zaehler_str})/({nenner_str})"
        return self._cache["term_str"]

    def term_latex(self) -> str:
        """Gibt den Term als LaTeX-String zurück"""
        return latex(self.term_sympy)

    def wert(self, x_wert: float) -> float | sp.Basic:
        """
        Berechnet den Funktionswert an einer Stelle.

        Args:
            x_wert: x-Wert an dem die Funktion ausgewertet werden soll

        Returns:
            Funktionswert als float oder symbolischer Ausdruck (bei Parametern)

        Raises:
            ValueError: Wenn x_wert eine Polstelle ist (Division durch Null)
        """
        # Prüfe, ob x_wert eine Polstelle ist
        if self._ist_polstelle(x_wert):
            raise ValueError(f"x = {x_wert} ist eine Polstelle der Funktion")

        # Berechne Zähler und Nenner separat, um symbolische Unterstützung zu nutzen
        zaehler_wert = self.zaehler.wert(x_wert)
        nenner_wert = self.nenner.wert(x_wert)

        # Wenn beide Werte konkrete Zahlen sind, teile sie
        if isinstance(zaehler_wert, (int, float)) and isinstance(
            nenner_wert, (int, float)
        ):
            return float(zaehler_wert) / float(nenner_wert)

        # Andernfalls gib den symbolischen Ausdruck zurück
        return zaehler_wert / nenner_wert

    def __call__(self, x_wert: float) -> float | sp.Basic:
        """
        Macht die Funktion aufrufbar: f(2), f(0.5), etc.

        Args:
            x_wert: x-Wert, an dem die Funktion ausgewertet werden soll

        Returns:
            Der Funktionswert als float-Zahl oder symbolischer Ausdruck (bei Parametern)

        Beispiele:
            >>> f = GebrochenRationaleFunktion(GanzrationaleFunktion("x^2 + 1"), GanzrationaleFunktion("x - 1"))
            >>> f(2)    # (2^2 + 1)/(2 - 1) = 5.0
            >>> g = GebrochenRationaleFunktion(GanzrationaleFunktion("a x^2 + 1"), GanzrationaleFunktion("x"))
            >>> g(1)    # (a*1^2 + 1)/1 = a + 1 (symbolisch)

        Didaktischer Hinweis:
            Diese Methode ermöglicht die natürliche mathematische Notation f(x),
            die Schüler aus dem Unterricht kennen.
        """
        return self.wert(x_wert)

    def _ist_polstelle(self, x_wert: float) -> bool:
        """Prüft, ob x_wert eine Polstelle ist"""
        try:
            # Versuche, den Nenner auszuwerten
            nenner_wert = self.nenner.wert(x_wert)
            if isinstance(nenner_wert, (int, float)):
                return abs(nenner_wert) < 1e-10
            # Bei symbolischen Ausdrücken: keine Polstelle erkennbar
            return False
        except (ValueError, TypeError, AttributeError):
            # Bei Fehlern: keine Polstelle erkennbar
            return False

    def nullstellen(self, real: bool = True, runden=None) -> list[float]:
        """
        Berechnet die Nullstellen der Funktion (Zähler-Nullstellen).

        Args:
            real: Nur reelle Nullstellen zurückgeben
            runden: Anzahl Nachkommastellen für Rundung (None = exakt)

        Returns:
            Liste der Nullstellen, wobei Definitionslücken entfernt wurden
        """
        zaehler_nullstellen = self.zaehler.nullstellen(real=real, runden=runden)
        polstellen = self.polstellen()

        # Entferne Nullstellen, die gleichzeitig Polstellen sind
        eigentliche_nullstellen = [
            ns
            for ns in zaehler_nullstellen
            if not any(abs(ns - ps) < 1e-10 for ps in polstellen)
        ]

        return eigentliche_nullstellen

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

    def plotly(
        self,
        x_range: tuple = (-5, 5),
        punkte: int = 200,
        zeige_polstellen: bool = True,
        zeige_asymptoten: bool = True,
    ) -> go.Figure:
        """[DEPRECATED] Erzeugt eine Plotly-Visualisierung der gebrochen-rationalen Funktion.
        Bitte verwende stattdessen f.graph() für konsistente API.

        Args:
            x_range: Tupel (xmin, xmax) für den x-Bereich
            punkte: Anzahl der zu berechneten Punkte
            zeige_polstellen: Ob vertikale Asymptoten bei Polstellen eingezeichnet werden sollen
            zeige_asymptoten: Ob horizontale/schiefe Asymptoten eingezeichnet werden sollen

        Returns:
            Plotly Figure-Objekt
        """
        import warnings

        warnings.warn(
            "plotly() is deprecated. Use f.graph() instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        # Verwende die neue graph() Methode
        return self.graph(x_min=x_range[0], x_max=x_range[1])

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
            if quotient.is_polynomial(self.x):
                quotient_poly = sp.poly(quotient, self.x)
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

    def validiere_zerlegung(self) -> bool:
        """
        Validiert, ob die Zerlegung f(x) = Schmiegkurve(x) + Störfunktion(x) korrekt ist.

        Returns:
            bool: True, wenn die Zerlegung mathematisch korrekt ist

        Beispiele:
            >>> f = GebrochenRationaleFunktion("x^3+2x+1", "x^2+1")
            >>> f.validiere_zerlegung()  # True
            >>> # Manuelle Überprüfung: f = (x) + (x+1)/(x^2+1)

        Didaktischer Hinweis:
            Diese Methode hilft Schülern, ihre Ergebnisse zu überprüfen und
            das Verständnis der mathematischen Beziehung zu vertiefen.
        """
        # Berechne beide Seiten
        linke_seite = self.term_sympy
        rechte_seite = self.schmiegkurve().term_sympy + self.stoerfunktion().term_sympy

        # Vereinfache die rechte Seite und vergleiche
        vereinfachte_rechte_seite = sp.simplify(rechte_seite)

        return sp.simplify(linke_seite - vereinfachte_rechte_seite) == 0

    def zeige_zerlegung(self) -> str:
        """
        Gibt eine formatierte Darstellung der Zerlegung zurück.

        Returns:
            str: Formatierter Text mit der Zerlegung

        Beispiele:
            >>> f = GebrochenRationaleFunktion("x^2+3x+2", "x+1")
            >>> print(f.zeige_zerlegung())
            # Ausgabe:
            # Funktion: f(x) = (x^2 + 3x + 2)/(x + 1)
            # Zerlegung: f(x) = (x + 2) + 0/(x + 1)
            # Schmiegkurve: s(x) = x + 2
            # Störfunktion: r(x) = 0
        """
        s = self.schmiegkurve()
        r = self.stoerfunktion()

        text = f"Funktion: f(x) = {self.term()}\n"
        text += f"Zerlegung: f(x) = {s.term()} + {r.term()}\n"
        text += f"Schmiegkurve: s(x) = {s.term()}\n"
        text += f"Störfunktion: r(x) = {r.term()}\n"

        if self.validiere_zerlegung():
            text += "✅ Validierung: Zerlegung ist mathematisch korrekt"
        else:
            text += "❌ Validierung: Zerlegung enthält Fehler"

        return text

    # =============================================================================
    # PHASE 2: PÄDAGOGISCHE METHODEN
    # =============================================================================

    def erkläre_schritt_für_schritt(self) -> dict:
        """
        Erklärt die Zerlegung Schritt für Schritt für das Verständnis von Schülern.

        Returns:
            dict: Detaillierte schrittweise Erklärung mit mathematischen Operationen

        Beispiele:
            >>> f = GebrochenRationaleFunktion("x^2+4x+3", "x+1")
            >>> erklaerung = f.erkläre_schritt_für_schritt()
            >>> print(erklaerung['schritte'][0]['titel'])
            'Schritt 1: Grade bestimmen'
        """
        grad_z = self.zaehler.grad()
        grad_n = self.nenner.grad()
        s = self.schmiegkurve()
        r = self.stoerfunktion()

        schritte = []

        # Schritt 1: Grade bestimmen
        schritte.append(
            {
                "titel": "Schritt 1: Grade von Zähler und Nenner bestimmen",
                "beschreibung": "Wir bestimmen zunächst die Grade des Zählers und Nenners.",
                "formel": f"grad(Zähler) = {grad_z}, grad(Nenner) = {grad_n}",
                "erklaerung": "Der Grad sagt uns, wie das asymptotische Verhalten aussieht.",
            }
        )

        # Schritt 2: Fallunterscheidung
        fall_typ = ""
        if grad_z < grad_n:
            fall_typ = "grad(Z) < grad(N)"
            schritte.append(
                {
                    "titel": "Schritt 2: Horizontale Asymptote y = 0",
                    "beschreibung": f"Da {fall_typ}, nähert sich die Funktion an y = 0 an.",
                    "formel": "lim_{x->oo} f(x) = 0",
                    "erklaerung": "Für große |x| wird die Funktion sehr klein.",
                }
            )
        elif grad_z == grad_n:
            fall_typ = "grad(Z) = grad(N)"
            lkh_z = self.zaehler.leitkoeffizient()
            lkh_n = self.nenner.leitkoeffizient()
            asymptote = lkh_z / lkh_n
            schritte.append(
                {
                    "titel": "Schritt 2: Horizontale Asymptote durch Leitkoeffizienten",
                    "beschreibung": f"Da {fall_typ}, bilden wir das Verhältnis der Leitkoeffizienten.",
                    "formel": f"lim_{{x->oo}} f(x) = {lkh_z}/{lkh_n} = {asymptote}",
                    "erklaerung": "Die Funktion nähert sich an den Quotienten der höchsten Koeffizienten an.",
                }
            )
        else:
            fall_typ = "grad(Z) > grad(N)"
            schritte.append(
                {
                    "titel": "Schritt 2: Polynomdivision durchführen",
                    "beschreibung": f"Da {fall_typ}, müssen wir eine Polynomdivision durchführen.",
                    "formel": f"{self.zaehler.term()} ÷ {self.nenner.term()} = {s.term()} + {r.term()}",
                    "erklaerung": "Wir teilen Zähler durch Nenner, um den polynomialen Anteil zu finden.",
                }
            )

        # Schritt 3: Störfunktion berechnen
        schritte.append(
            {
                "titel": "Schritt 3: Störfunktion bestimmen",
                "beschreibung": "Die Störfunktion ist der Rest nach Abzug der Schmiegkurve.",
                "formel": f"r(x) = f(x) - s(x) = {r.term()}",
                "erklaerung": "Die Störfunktion geht für große |x| gegen 0.",
            }
        )

        # Schritt 4: Zusammenfassung
        schritte.append(
            {
                "titel": "Schritt 4: Zusammenfassung",
                "beschreibung": "Die vollständige Zerlegung lautet:",
                "formel": f"f(x) = {s.term()} + {r.term()}",
                "erklaerung": f"Schmiegkurve: {s.term()} (globales Verhalten), Störfunktion: {r.term()} (lokales Verhalten)",
            }
        )

        return {
            "funktion": self.term(),
            "schritte": schritte,
            "ergebnis": {
                "schmiegkurve": s.term(),
                "stoerfunktion": r.term(),
                "zerlegung": f"f(x) = {s.term()} + {r.term()}",
            },
        }

    def zeige_asymptotisches_verhalten(self) -> dict:
        """
        Analysiert und erklärt das asymptotische Verhalten detailliert.

        Returns:
            dict: Umfassende Analyse des asymptotischen Verhaltens

        Beispiele:
            >>> f = GebrochenRationaleFunktion("x^2+1", "x-1")
            >>> analyse = f.zeige_asymptotisches_verhalten()
            >>> print(analyse['asymptoten']['schief']['beschreibung'])
        """
        grad_z = self.zaehler.grad()
        grad_n = self.nenner.grad()
        s = self.schmiegkurve()
        r = self.stoerfunktion()

        analyse = {
            "funktion": self.term(),
            "grade": {
                "zaehler": grad_z,
                "nenner": grad_n,
                "differenz": grad_z - grad_n,
            },
            "asymptoten": {},
            "verhalten": {},
        }

        # Vertikale Asymptoten (Polstellen)
        polstellen = self.polstellen()
        if polstellen:
            analyse["asymptoten"]["vertikal"] = [
                {
                    "stelle": ps,
                    "beschreibung": f"x = {ps} ist Polstelle, da Nenner = 0 und Zähler ≠ 0",
                }
                for ps in polstellen
            ]

        # Horizontale/Schiefe Asymptoten
        if grad_z < grad_n:
            analyse["asymptoten"]["horizontal"] = {
                "y_wert": 0,
                "beschreibung": "Horizontale Asymptote y = 0, da grad(Z) < grad(N)",
            }
        elif grad_z == grad_n:
            lkh_z = self.zaehler.leitkoeffizient()
            lkh_n = self.nenner.leitkoeffizient()
            asymptote = lkh_z / lkh_n
            analyse["asymptoten"]["horizontal"] = {
                "y_wert": asymptote,
                "beschreibung": f"Horizontale Asymptote y = {asymptote}, Verhältnis der Leitkoeffizienten",
            }
        else:
            # Schiefe Asymptote = Schmiegkurve
            analyse["asymptoten"]["schief"] = {
                "funktion": s.term(),
                "beschreibung": f"Schiefe Asymptote {s.term()}, Ergebnis der Polynomdivision",
            }

        # Verhalten für x -> oo und x -> -oo
        analyse["verhalten"]["x_positiv_unendlich"] = {
            "beschreibung": f"Für x -> ∞ nähert sich f(x) an {s.term()} an",
            "mathematisch": f"lim_{{x->∞}} f(x) = {s.term()}",
        }

        analyse["verhalten"]["x_negativ_unendlich"] = {
            "beschreibung": f"Für x -> -∞ nähert sich f(x) an {s.term()} an",
            "mathematisch": f"lim_{{x->-∞}} f(x) = {s.term()}",
        }

        # Einfluss der Störfunktion
        analyse["störfunktion_einfluss"] = {
            "term": r.term(),
            "beschreibung": f"Die Störfunktion {r.term()} wird für große |x| vernachlässigbar",
            "eigenschaft": "lim_{x->±∞} r(x) = 0",
        }

        return analyse

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


# =============================================================================
# PHASE 3: EXPONENTIALL-RATIONALE FUNKTIONEN
# =============================================================================


class ExponentialRationaleFunktion:
    """
    Repräsentiert eine exponential-rationale Funktion f(x) = P(e^{ax})/Q(e^{ax}),
    wobei P und Q Polynome sind und a ein reeller Parameter.

    Diese Funktionen lassen sich durch Substitution u = e^{ax} in rationale
    Funktionen transformieren, was die Analyse asymptotischen Verhaltens ermöglicht.
    """

    @classmethod
    def _erstelle_aus_string(cls, eingabe: str):
        """
        Factory-Methode zur Erstellung aus einem String mit exp()-Funktionen.

        Args:
            eingabe: String wie "exp(x) + 1", "(exp(x)+1)/(exp(x)-1)", etc.

        Returns:
            ExponentialRationaleFunktion
        """
        # Finde alle exp() Ausdrücke
        import re

        # Finde alle exp() Ausdrücke und extrahiere deren Argumente
        exp_matches = re.findall(r"exp\(([^)]+)\)", eingabe)
        if not exp_matches:
            raise ValueError(f"Keine exp() Funktion in Eingabe gefunden: {eingabe}")

        # Bestimme den Exponentialparameter (vereinfacht: nehme den ersten)
        exp_arg = exp_matches[0].strip()

        # Prüfe ob es ein einfaches exp(x) oder exp(kx) ist
        if exp_arg == "x":
            a_param = 1.0
        elif re.match(r"^\d*\.?\d*\s*\*?\s*x$", exp_arg):
            # Form wie k*x oder kx
            coeff_match = re.match(r"^(\d*\.?\d*)\s*\*?\s*x$", exp_arg)
            if coeff_match:
                a_param = float(coeff_match.group(1) if coeff_match.group(1) else "1")
            else:
                a_param = 1.0
        else:
            # Komplexerer Ausdruck - Standardwert verwenden
            a_param = 1.0

        # Ersetze exp(...) durch x für die rationale Funktion
        verarbeitete_eingabe = re.sub(r"exp\([^)]+\)", "x", eingabe)

        # Prüfe ob es ein Bruch ist
        if "/" in verarbeitete_eingabe:
            # Trenne in Zähler und Nenner
            teile = verarbeitete_eingabe.split("/", 1)
            zaehler_str = teile[0].strip()
            nenner_str = teile[1].strip()

            # Entferne Klammern wenn vorhanden
            zaehler_str = zaehler_str.strip("()")
            nenner_str = nenner_str.strip("()")

            return cls(zaehler_str, nenner_str, exponent_param=a_param)
        else:
            # Nur Zähler
            zaehler_str = verarbeitete_eingabe.strip("()")
            return cls(zaehler_str, "1", exponent_param=a_param)

    def __init__(
        self,
        zaehler: GanzrationaleFunktion | str | sp.Basic,
        nenner: GanzrationaleFunktion | str | sp.Basic,
        exponent_param: float = 1.0,
    ):
        """
        Konstruktor für exponential-rationale Funktionen.

        Args:
            zaehler: Polynom in e^{ax} als GanzrationaleFunktion, String oder SymPy-Ausdruck
            nenner: Polynom in e^{ax} als GanzrationaleFunktion, String oder SymPy-Ausdruck
            exponent_param: Parameter a in e^{ax} (Standard: 1.0)
        """
        # Validiere Konstruktorparameter
        _validiere_konstruktor_parameter(zaehler, nenner)

        # Sicherheitsprüfung für String-Eingaben
        if isinstance(zaehler, str):
            _validiere_mathematischen_ausdruck(zaehler)
        if isinstance(nenner, str):
            _validiere_mathematischen_ausdruck(nenner)
            # Spezielle Prüfung für Division durch Null
            if nenner.strip() == "0":
                raise DivisionDurchNullError()

        self.x = symbols("x")
        self.a = exponent_param  # Parameter für e^{ax}

        # Cache für wiederholte Berechnungen
        self._cache = {
            "transformierte_funktion": None,
            "schmiegkurve": None,
            "stoerfunktion": None,
            "zerlegung_berechnet": False,
            "asymptoten": None,
        }

        # Erstelle Zähler und Nenner
        self.zaehler = self._convert_to_ganzrationale(zaehler)
        self.nenner = self._convert_to_ganzrationale(nenner)

        # Validiere, dass Nenner nicht Null ist
        if self.nenner.term_sympy == 0:
            raise UngueltigerAusdruckError(
                "Nullfunktion", "Nenner darf nicht die Nullfunktion sein"
            )

        # Erstelle SymPy-Ausdruck für die gesamte Funktion
        self.term_sympy = self._erzeuge_exponential_funktion()

    def _convert_to_ganzrationale(
        self, eingabe: GanzrationaleFunktion | str | sp.Basic
    ) -> GanzrationaleFunktion:
        """Konvertiert Eingabe zu GanzrationaleFunktion"""
        if isinstance(eingabe, GanzrationaleFunktion):
            return eingabe
        elif isinstance(eingabe, str):
            return GanzrationaleFunktion(eingabe)
        elif isinstance(eingabe, sp.Basic):
            return GanzrationaleFunktion(eingabe)
        else:
            raise TypeError(
                f"Kann {type(eingabe)} nicht in GanzrationaleFunktion umwandeln"
            )

    def _erzeuge_exponential_funktion(self) -> sp.Basic:
        """
        Erzeugt die exponential-rationale Funktion f(x) = P(e^{ax})/Q(e^{ax}).

        Returns:
            SymPy-Ausdruck der exponential-rationalen Funktion
        """
        # Substituiere x -> e^{ax} in Zähler und Nenner
        exp_sub = sp.exp(self.a * self.x)

        zaehler_exp = self.zaehler.term_sympy.subs(self.x, exp_sub)
        nenner_exp = self.nenner.term_sympy.subs(self.x, exp_sub)

        return zaehler_exp / nenner_exp

    def _transformiere_zu_rational(self) -> GebrochenRationaleFunktion:
        """
        Transformiert die exponential-rationale Funktion in eine rationale Funktion
        durch Substitution u = e^{ax}.

        Returns:
            GebrochenRationaleFunktion: Transformierte rationale Funktion
        """
        if self._cache["transformierte_funktion"] is None:
            # Erstelle rationale Funktion mit gleichen Koeffizienten
            self._cache["transformierte_funktion"] = GebrochenRationaleFunktion(
                self.zaehler, self.nenner
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
            # Für ganzrationale Funktionen: Nenner = 1
            return ExponentialRationaleFunktion(
                rationale_funktion, GanzrationaleFunktion("1"), self.a
            )
        elif isinstance(rationale_funktion, GebrochenRationaleFunktion):
            # Für gebrochen-rationale Funktionen: Zähler und Nenner extrahieren
            return ExponentialRationaleFunktion(
                rationale_funktion.zaehler, rationale_funktion.nenner, self.a
            )
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

    def validiere_zerlegung(self) -> bool:
        """
        Validiert, ob die Zerlegung korrekt ist.

        Returns:
            bool: True, wenn die Zerlegung mathematisch korrekt ist
        """
        try:
            # Berechne beide Seiten symbolisch
            linke_seite = self.term_sympy
            rechte_seite = (
                self.schmiegkurve().term_sympy + self.stoerfunktion().term_sympy
            )

            # Vereinfache und vergleiche
            differenz = sp.simplify(linke_seite - rechte_seite)
            return differenz == 0
        except Exception:
            return False

    def term(self) -> str:
        """
        Gibt den Term als String zurück.

        Returns:
            str: String-Darstellung der Funktion
        """
        zaehler_str = self.zaehler.term().replace("x", f"e^{{{self.a}x}}")
        nenner_str = self.nenner.term().replace("x", f"e^{{{self.a}x}}")
        return f"({zaehler_str})/({nenner_str})"

    def term_latex(self) -> str:
        """
        Gibt den Term als LaTeX-String zurück.

        Returns:
            str: LaTeX-Darstellung der Funktion
        """
        return latex(self.term_sympy)

    def wert(self, x_wert: float) -> float:
        """
        Berechnet den Funktionswert an einer Stelle.

        Args:
            x_wert: x-Wert an dem die Funktion ausgewertet werden soll

        Returns:
            float: Funktionswert

        Raises:
            ValueError: Wenn der Wert nicht berechnet werden kann oder Polstelle vorliegt
        """
        # Prüfe, ob x_wert eine Polstelle ist
        if self._ist_polstelle(x_wert):
            raise ValueError(f"x = {x_wert} ist eine Polstelle der Funktion")

        try:
            # Substituiere x-Wert in den SymPy-Ausdruck
            result = self.term_sympy.subs(self.x, x_wert)

            # Versuche, zu float zu konvertieren
            if hasattr(result, "evalf"):
                eval_result = result.evalf()
                # Prüfe auf komplexe Ergebnisse
                if hasattr(eval_result, "imag") and abs(eval_result.imag) > 1e-10:
                    raise ValueError(f"Komplexes Ergebnis bei x = {x_wert}")
                return float(eval_result)
            else:
                return float(result)
        except Exception as e:
            raise ValueError(
                f"Kann Funktionswert bei x = {x_wert} nicht berechnen: {e}"
            )

    def _ist_polstelle(self, x_wert: float) -> bool:
        """
        Prüft, ob x_wert eine Polstelle der exponential-rationalen Funktion ist.
        Für exponential-rationale Funktionen f(x) = P(e^{ax})/Q(e^{ax}) ist x eine
        Polstelle, wenn Q(e^{ax}) = 0.
        """
        try:
            # Berechne e^{ax} für den gegebenen x-Wert
            exp_wert = sp.exp(self.a * x_wert)

            # Substituiere in den Nenner
            nenner_bei_exp = self.nenner.term_sympy.subs(self.x, exp_wert)

            # Prüfe, ob der Nenner nahe bei Null ist
            if hasattr(nenner_bei_exp, "evalf"):
                nenner_float = float(nenner_bei_exp.evalf())
            else:
                nenner_float = float(nenner_bei_exp)

            return abs(nenner_float) < 1e-10
        except (ValueError, TypeError, AttributeError):
            # Bei Fehlern: Polstelle nicht erkennbar
            return False

    def __call__(self, x_wert: float) -> float:
        """
        Macht die Funktion aufrufbar: f(2), f(0.5), etc.

        Args:
            x_wert: x-Wert, an dem die Funktion ausgewertet werden soll

        Returns:
            float: Der Funktionswert
        """
        return self.wert(x_wert)

    def __str__(self) -> str:
        """String-Repräsentation"""
        return self.term()

    def __repr__(self) -> str:
        """Repräsentation für debugging"""
        return f"ExponentialRationaleFunktion({self.zaehler.term()}, {self.nenner.term()}, exponent_param={self.a})"

    def _repr_latex_(self) -> str:
        """LaTeX-Darstellung für Jupyter/Marimo Notebooks"""
        return self.term_sympy._repr_latex_()

    def zeige_zerlegung(self) -> str:
        """
        Gibt eine formatierte Darstellung der Zerlegung zurück.

        Returns:
            str: Formatierter Text mit der Zerlegung
        """
        s = self.schmiegkurve()
        r = self.stoerfunktion()

        text = f"Exponential-rationale Funktion: f(x) = {self.term()}\n"
        text += f"Zerlegung: f(x) = {s.term()} + {r.term()}\n"
        text += f"Schmiegkurve: s(x) = {s.term()}\n"
        text += f"Störfunktion: r(x) = {r.term()}\n"

        if self.validiere_zerlegung():
            text += "✅ Validierung: Zerlegung ist mathematisch korrekt"
        else:
            text += "❌ Validierung: Zerlegung enthält Fehler"

        return text

    def erkläre_transformation(self) -> dict:
        """
        Erklärt die Substitutionsmethode u = e^{ax} Schritt für Schritt.

        Returns:
            dict: Detaillierte Erklärung der Transformation

        Beispiele:
            >>> f = ExponentialRationaleFunktion("x+1", "x-1", exponent_param=1)
            >>> erklaerung = f.erkläre_transformation()
        """
        rationale_funktion = self._transformiere_zu_rational()

        schritte = [
            {
                "titel": "Schritt 1: Substitution vorbereiten",
                "beschreibung": "Wir substituieren u = e^{ax} um die exponential-rationale in eine rationale Funktion umzuwandeln.",
                "formel": f"u = e^{{{self.a}x}}",
                "erklaerung": "Dadurch wird f(x) = P(e^{ax})/Q(e^{ax}) zu P(u)/Q(u).",
            },
            {
                "titel": "Schritt 2: Transformierte Funktion erstellen",
                "beschreibung": "Ersetzen von e^{ax} durch u in Zähler und Nenner.",
                "formel": f"f(x) = {self.zaehler.term().replace('x', 'u')}/{self.nenner.term().replace('x', 'u')}",
                "erklaerung": "Die rationale Funktion in u können wir mit bekannten Methoden analysieren.",
            },
            {
                "titel": "Schritt 3: Zerlegung durchführen",
                "beschreibung": "Zerlegung der rationalen Funktion in Schmiegkurve und Störfunktion.",
                "formel": f"P(u)/Q(u) = {rationale_funktion.schmiegkurve().term().replace('x', 'u')} + {rationale_funktion.stoerfunktion().term().replace('x', 'u')}",
                "erklaerung": "Dies ist die Standard-Zerlegung für rationale Funktionen.",
            },
            {
                "titel": "Schritt 4: Rücktransformation",
                "beschreibung": "Ersetzen von u durch e^{ax} um zur ursprünglichen Variable zurückzukehren.",
                "formel": f"f(x) = {self.schmiegkurve().term()} + {self.stoerfunktion().term()}",
                "erklaerung": "Damit haben wir die Zerlegung für die exponential-rationale Funktion.",
            },
        ]

        return {
            "original_funktion": self.term(),
            "transformierte_funktion": rationale_funktion.term(),
            "substitution": f"u = e^{{{self.a}x}}",
            "schritte": schritte,
            "ergebnis": {
                "schmiegkurve": self.schmiegkurve().term(),
                "stoerfunktion": self.stoerfunktion().term(),
            },
        }

    def analysiere_asymptotisches_verhalten(self) -> dict:
        """
        Analysiert das asymptotische Verhalten für x -> ∞ und x -> -∞.

        Returns:
            dict: Umfassende Analyse des asymptotischen Verhaltens
        """
        rationale_funktion = self._transformiere_zu_rational()
        s_rational = rationale_funktion.schmiegkurve()
        r_rational = rationale_funktion.stoerfunktion()

        analyse = {
            "funktion": self.term(),
            "parameter": f"a = {self.a}",
            "transformierte_funktion": rationale_funktion.term(),
            "verhalten": {},
        }

        # Analyse für x -> ∞
        # u = e^{ax} -> ∞, wenn a > 0
        # u = e^{ax} -> 0, wenn a < 0
        if self.a > 0:
            # Für x -> ∞: u -> ∞
            grad_z = self.zaehler.grad()
            grad_n = self.nenner.grad()

            if grad_z < grad_n:
                verhalten_pos = "0 (horizontale Asymptote y = 0)"
            elif grad_z == grad_n:
                lkh_z = (
                    self.zaehler.koeffizienten[-1] if self.zaehler.koeffizienten else 0
                )
                lkh_n = (
                    self.nenner.koeffizienten[-1] if self.nenner.koeffizienten else 1
                )
                verhalten_pos = f"{lkh_z / lkh_n} (horizontale Asymptote)"
            else:
                verhalten_pos = f"{s_rational.term().replace('x', f'e^{{{self.a}x}}')} (Wachstum wie Polynom in e^{{{self.a}x}})"

            analyse["verhalten"]["x_positiv_unendlich"] = {
                "substitution": f"u = e^{{{self.a}x}} -> ∞",
                "transformiertes_verhalten": verhalten_pos,
                "beschreibung": f"Für x -> ∞ verhält sich f(x) wie {verhalten_pos}",
            }

            # Für x -> -∞: u -> 0
            verhalten_neg = f"{self.zaehler.koeffizienten[0] if self.zaehler.koeffizienten else 0}/{self.nenner.koeffizienten[0] if self.nenner.koeffizienten else 1}"
            analyse["verhalten"]["x_negativ_unendlich"] = {
                "substitution": f"u = e^{{{self.a}x}} -> 0",
                "transformiertes_verhalten": verhalten_neg,
                "beschreibung": f"Für x -> -∞ nähert sich f(x) an {verhalten_neg} an",
            }

        else:  # a < 0
            # Für x -> ∞: u -> 0
            verhalten_pos = f"{self.zaehler.koeffizienten[0] if self.zaehler.koeffizienten else 0}/{self.nenner.koeffizienten[0] if self.nenner.koeffizienten else 1}"
            analyse["verhalten"]["x_positiv_unendlich"] = {
                "substitution": f"u = e^{{{self.a}x}} -> 0",
                "transformiertes_verhalten": verhalten_pos,
                "beschreibung": f"Für x -> ∞ nähert sich f(x) an {verhalten_pos} an",
            }

            # Für x -> -∞: u -> ∞
            grad_z = self.zaehler.grad()
            grad_n = self.nenner.grad()

            if grad_z < grad_n:
                verhalten_neg = "0 (horizontale Asymptote y = 0)"
            elif grad_z == grad_n:
                lkh_z = (
                    self.zaehler.koeffizienten[-1] if self.zaehler.koeffizienten else 0
                )
                lkh_n = (
                    self.nenner.koeffizienten[-1] if self.nenner.koeffizienten else 1
                )
                verhalten_neg = f"{lkh_z / lkh_n} (horizontale Asymptote)"
            else:
                verhalten_neg = f"{s_rational.term().replace('x', f'e^{{{self.a}x}}')} (Wachstum wie Polynom in e^{{{self.a}x}})"

            analyse["verhalten"]["x_negativ_unendlich"] = {
                "substitution": f"u = e^{{{self.a}x}} -> ∞",
                "transformiertes_verhalten": verhalten_neg,
                "beschreibung": f"Für x -> -∞ verhält sich f(x) wie {verhalten_neg}",
            }

        return analyse
