"""
Gebrochen-rationale Funktionen für das Schul-Analysis Framework.

Unterstützt verschiedene Konstruktor-Formate und mathematisch korrekte
Visualisierung mit Plotly für Marimo-Notebooks.
"""

import re

import numpy as np
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


class GebrochenRationaleFunktionError(Exception):
    """Basisklasse für gebrochen-rationale Funktionsfehler"""

    pass
    """Fehler bei Sicherheitsverletzungen"""

    pass


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
            raise SicherheitsError(f"Gefährlicher Ausdruck erkannt: {ausdruck}")

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

        self.x = symbols("x")

        # Cache für wiederholte Berechnungen
        self._cache = {
            "polstellen": None,
            "asymptoten": None,
            "nullstellen": None,
            "term_str": None,
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
        self, eingabe: GanzrationaleFunktion | sp.Basic
    ) -> GanzrationaleFunktion:
        """Konvertiert Eingabe zu GanzrationaleFunktion"""
        if isinstance(eingabe, GanzrationaleFunktion):
            return eingabe
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

    def wert(self, x_wert: float) -> float:
        """
        Berechnet den Funktionswert an einer Stelle.

        Args:
            x_wert: x-Wert an dem die Funktion ausgewertet werden soll

        Returns:
            Funktionswert als float

        Raises:
            ValueError: Wenn x_wert eine Polstelle ist (Division durch Null)
        """
        # Prüfe, ob x_wert eine Polstelle ist
        if self._ist_polstelle(x_wert):
            raise ValueError(f"x = {x_wert} ist eine Polstelle der Funktion")

        return float(self.term_sympy.subs(self.x, x_wert))

    def _ist_polstelle(self, x_wert: float) -> bool:
        """Prüft, ob x_wert eine Polstelle ist"""
        return abs(self.nenner.term_sympy.subs(self.x, x_wert)) < 1e-10

    def nullstellen(self) -> list[float]:
        """
        Berechnet die Nullstellen der Funktion (Zähler-Nullstellen).

        Returns:
            Liste der Nullstellen, wobei Definitionslücken entfernt wurden
        """
        zaehler_nullstellen = self.zaehler.nullstellen()
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
        return self.term()

    def __repr__(self) -> str:
        """Repräsentation für debugging"""
        return self.__str__()

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

    def plotly(
        self,
        x_range: tuple = (-5, 5),
        punkte: int = 200,
        zeige_polstellen: bool = True,
        zeige_asymptoten: bool = True,
    ) -> go.Figure:
        """
        Erzeugt eine Plotly-Visualisierung der gebrochen-rationalen Funktion.

        Args:
            x_range: Tupel (xmin, xmax) für den x-Bereich
            punkte: Anzahl der zu berechnenden Punkte
            zeige_polstellen: Ob vertikale Asymptoten bei Polstellen eingezeichnet werden sollen
            zeige_asymptoten: Ob horizontale/schiefe Asymptoten eingezeichnet werden sollen

        Returns:
            Plotly Figure-Objekt
        """
        xmin, xmax = x_range

        # Erstelle x-Werte für die Berechnung
        x_werte = np.linspace(xmin, xmax, punkte)
        y_werte = []
        gueltige_x = []

        # Berechne Funktionswerte, vermeide Polstellen
        polstellen = self.polstellen()

        for x in x_werte:
            try:
                # Prüfe, ob x nahe einer Polstelle ist
                ist_nahe_polstelle = any(abs(x - ps) < 0.1 for ps in polstellen)
                if ist_nahe_polstelle:
                    continue

                y = self.wert(x)
                y_werte.append(y)
                gueltige_x.append(x)
            except ValueError:
                # Überspringe Polstellen
                continue

        # Erstelle die Figur
        fig = go.Figure()

        # Hauptkurve
        fig.add_trace(
            go.Scatter(
                x=gueltige_x,
                y=y_werte,
                mode="lines",
                name=f"f(x) = {self.term()}",
                line={"color": "blue", "width": 3},
            )
        )

        # Füge Polstellen als vertikale Asymptoten hinzu
        if zeige_polstellen:
            for ps in polstellen:
                if xmin <= ps <= xmax:
                    # Berechne y-Werte für die Asymptote
                    y_asymptote_range = np.linspace(
                        min(y_werte) if y_werte else -10,
                        max(y_werte) if y_werte else 10,
                        100,
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=[ps] * len(y_asymptote_range),
                            y=y_asymptote_range,
                            mode="lines",
                            line={"color": "red", "width": 2, "dash": "dash"},
                            name=f"Polstelle x={ps:.2f}",
                            showlegend=False,
                        )
                    )

        # Füge horizontale/schiefe Asymptoten hinzu
        if zeige_asymptoten:
            asymptoten = self._berechne_asymptoten()
            for asymptote in asymptoten:
                if asymptote["typ"] == "horizontal":
                    y_const = asymptote["y"]
                    fig.add_hline(
                        y=y_const,
                        line_dash="dash",
                        line_color="green",
                        annotation_text=f"y = {y_const:.2f}",
                    )
                elif asymptote["typ"] == "schief":
                    # Berechne Punkte für die schiefe Asymptote
                    x_asymptote = np.linspace(xmin, xmax, 100)
                    y_asymptote = (
                        asymptote["steigung"] * x_asymptote + asymptote["y_offset"]
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=x_asymptote,
                            y=y_asymptote,
                            mode="lines",
                            line={"color": "green", "width": 2, "dash": "dash"},
                            name=f"Asymptote: y = {asymptote['steigung']:.2f}x + {asymptote['y_offset']:.2f}",
                            showlegend=False,
                        )
                    )

        # Layout-Optionen
        fig.update_layout(
            title=f"Gebrochen-rationale Funktion: {self.term()}",
            xaxis_title="x",
            yaxis_title="f(x)",
            showlegend=True,
            width=800,
            height=600,
            xaxis={"showgrid": True, "zeroline": True},
            yaxis={"showgrid": True, "zeroline": True},
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
