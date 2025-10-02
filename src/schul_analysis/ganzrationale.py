"""
Ganzrationale Funktionen (Polynome) für das Schul-Analysis Framework.

Unterstützt verschiedene Konstruktor-Formate und mathematisch korrekte
Visualisierung mit Plotly für Marimo-Notebooks.
"""

import logging
from typing import TYPE_CHECKING, Any, Union

import numpy as np

if TYPE_CHECKING:
    from .gebrochen_rationale import GebrochenRationaleFunktion

import marimo as mo
import plotly.express as px
import plotly.graph_objects as go
import sympy as sp
from plotly.subplots import make_subplots
from sympy import Poly, Rational, diff, factor, latex, solve, symbols, sympify

from .config import config

# Logger instance for the module
log = logging.getLogger(__name__)

# Constants for better maintainability
DEFAULT_TOLERANCE = 1e-9
MAX_DERIVATIVE_ORDER_CHECK = 15


def _runde_wert(wert, runden=None):
    """Hilfsfunktion zum Rundung von SymPy-Werten

    Args:
        wert: SymPy-Ausdruck oder numerischer Wert
        runden: Anzahl Nachkommastellen (None = exakt, int = gerundet)

    Returns:
        Exakter Wert (wenn runden=None) oder gerundeter float-Wert
    """
    if runden is None:
        return wert  # Behalte SymPy-Objekt bei

    try:
        # Konvertiere zu float und runde
        float_wert = float(wert)
        return round(float_wert, runden)
    except (TypeError, ValueError):
        # Bei Konvertierungsfehler, gebe Original zurück
        return wert


class GanzrationaleFunktion:
    """
    Repräsentiert eine ganzrationale Funktion (Polynom) mit verschiedenen
    Konstruktor-Optionen und Visualisierungsmethoden.
    """

    def __init__(self, eingabe: str | list[float] | dict[int, float] | sp.Basic):
        """
        Konstruktor für ganzrationale Funktionen.

        Args:
            eingabe: String ("x^3-2x+1"), Liste ([1, 0, -2, 1]), Dictionary ({3: 1, 1: -2, 0: 1}) oder SymPy-Ausdruck
        """
        self.x = symbols("x")
        self.original_eingabe = str(eingabe)  # Original eingabe speichern

        if isinstance(eingabe, str):
            # String-Konstruktor mit robuster Verarbeitung
            self.term_str, self.term_sympy = self._parse_string_eingabe(eingabe)
        elif isinstance(eingabe, list):
            # Listen-Konstruktor: [1, 0, -2, 1] für x³ - 2x + 1
            self.term_str = self._liste_zu_string(eingabe)
            self.term_sympy = self._liste_zu_sympy(eingabe)
        elif isinstance(eingabe, dict):
            # Dictionary-Konstruktor: {3: 1, 1: -2, 0: 1} für x³ - 2x + 1
            self.term_str = self._dict_zu_string(eingabe)
            self.term_sympy = self._dict_zu_sympy(eingabe)
        elif isinstance(eingabe, sp.Basic):
            # SymPy-Ausdruck-Konstruktor
            self.term_str = str(eingabe)
            self.term_sympy = eingabe
            # Validiere, dass es wirklich ein Polynom ist
            if not self.term_sympy.is_polynomial(self.x):
                raise TypeError("SymPy-Ausdruck ist kein Polynom in x")
        else:
            raise TypeError(
                "Eingabe muss String, Liste, Dictionary oder SymPy-Ausdruck sein"
            )

        # Koeffizienten extrahieren (als exakte SymPy-Objekte)
        self.koeffizienten = self._extrahiere_koeffizienten()

    def _parse_string_eingabe(self, eingabe: str) -> tuple[str, sp.Basic]:
        """
        Vereinfachter Parser für String-Eingaben von ganzrationalen Funktionen.

        Unterstützt:
        - "x^2+4x-2" (Standard-Schreibweise)
        - "$x^2+4x-2$" (LaTeX-Format)
        - "x**2+4*x-2" (Python-Syntax)
        - "2x" (implizite Multiplikation)
        - "x^2 + 4x - 2" (mit Leerzeichen)

        Args:
            eingabe: String-Eingabe in verschiedenen Formaten

        Returns:
            Tuple aus (original_string, sympy_ausdruck)
        """
        # Spezialfall: Linearfaktoren-Format
        if self._ist_linearfaktor_format(eingabe):
            return self._parse_linearfaktoren(eingabe)

        # Für alle anderen Strings: sympify die Arbeit machen lassen
        try:
            # Bereinige die Eingabe für bessere Kompatibilität
            import re

            bereinigt = eingabe.strip().replace("$", "").replace("^", "**")

            # Implizite Multiplikation hinzufügen (2x -> 2*x)
            bereinigt = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", bereinigt)
            # Leerzeichen um Operatoren normalisieren
            bereinigt = re.sub(r"\s+", "", bereinigt)

            # sympify mit korrekter Variable
            term_sympy = sympify(bereinigt, locals={"x": self.x})

            # Wichtig: Validiere, dass das Ergebnis wirklich ein Polynom in x ist
            if not term_sympy.is_polynomial(self.x):
                raise ValueError(
                    f"Eingabe '{eingabe}' ist keine ganzrationale Funktion in x."
                )

            # Expandiere den Ausdruck für konsistente Darstellung
            term_sympy = sp.expand(term_sympy)

            return eingabe, term_sympy

        except (sp.SympifyError, TypeError, ValueError) as e:
            raise ValueError(f"Ungültiger mathematischer Ausdruck: '{eingabe}'") from e

    def _ist_linearfaktor_format(self, eingabe: str) -> bool:
        """Prüft, ob die Eingabe im Linearfaktoren-Format vorliegt."""
        import re

        # Pattern für Linearfaktoren: (x±a), (x±b), etc.
        # Auch mit Potenzen: (x±a)^n
        # Auch mit Koeffizienten: k(x±a)
        # Auch mit expliziten Multiplikationszeichen: (x±a)*(x±b)
        # Auch mit impliziten Multiplikationszeichen: (x±a)(x±b)
        pattern = r"^(\d*\(x[+\-]\d+\)(\^\d+)?[*]*)*\d*\(x[+\-]\d+\)(\^\d+)?$"

        return bool(re.match(pattern, eingabe.replace(" ", "")))

    def _parse_linearfaktoren(self, eingabe: str) -> tuple[str, sp.Basic]:
        """Parst Linearfaktoren in expandierte Form."""
        import re

        # Leerzeichen entfernen
        bereinigt = eingabe.replace(" ", "")

        # Entferne explizite Multiplikationszeichen und extrahiere alle Faktoren
        bereinigt = bereinigt.replace("*", "")
        faktoren = re.findall(r"(\d*)\(x([+\-])(\d+)\)(\^\d+)?", bereinigt)

        if not faktoren:
            raise ValueError(f"Ungültiges Linearfaktoren-Format: '{eingabe}'")

        # Baue den Ausdruck direkt mit SymPy zusammen
        x = self.x
        ergebnis = 1

        for koeff, vorzeichen, zahl, potenz in faktoren:
            # Koeffizient verarbeiten
            if koeff:
                koeff_int = sp.Integer(int(koeff))
            else:
                koeff_int = sp.Integer(1)

            # Vorzeichen und Zahl verarbeiten
            if vorzeichen == "+":
                konstante = -sp.Integer(int(zahl))  # (x+1) bedeutet (x - (-1))
            else:
                konstante = sp.Integer(int(zahl))  # (x-1) bedeutet (x - 1)

            # Linearfaktor erstellen
            linearfaktor = x - konstante

            if potenz:
                # Mit Potenz
                potenz_wert = int(potenz[1:])  # ^n extrahieren
                faktor = koeff_int * linearfaktor**potenz_wert
            else:
                # Ohne Potenz
                faktor = koeff_int * linearfaktor

            ergebnis = ergebnis * faktor

        try:
            # Expandiere zu Standardform
            term_expanded = sp.expand(ergebnis)
            term_string = str(ergebnis)

            return term_string, term_expanded
        except Exception as e:
            raise ValueError(
                f"Konnte Linearfaktoren '{eingabe}' nicht verarbeiten: {e}"
            )

    def _liste_zu_string(self, koeff: list[float]) -> str:
        """Wandelt Koeffizienten-Liste in Term-String um."""
        terme = []
        for i, k in enumerate(koeff):
            if k == 0:
                continue
            if i == 0:
                terme.append(str(k))
            elif i == 1:
                if k == 1:
                    terme.append("x")
                elif k == -1:
                    terme.append("-x")
                else:
                    terme.append(f"{k}x")
            else:
                if k == 1:
                    terme.append(f"x^{i}")
                elif k == -1:
                    terme.append(f"-x^{i}")
                else:
                    terme.append(f"{k}x^{i}")

        if not terme:
            return "0"

        return "+".join(terme).replace("+-", "-")

    def _liste_zu_sympy(self, koeff: list[float]) -> sp.Basic:
        """Wandelt Koeffizienten-Liste in SymPy-Ausdruck um."""
        term = 0
        for i, k in enumerate(koeff):
            term += k * self.x**i
        return term

    def _dict_zu_string(self, koeff: dict[int, float]) -> str:
        """Wandelt Koeffizienten-Dictionary in Term-String um."""
        # Sortiere nach absteigendem Grad
        sortierte_koeff = sorted(koeff.items(), key=lambda x: -x[0])

        terme = []
        for grad, k in sortierte_koeff:
            if k == 0:
                continue
            if grad == 0:
                terme.append(str(k))
            elif grad == 1:
                if k == 1:
                    terme.append("x")
                elif k == -1:
                    terme.append("-x")
                else:
                    terme.append(f"{k}x")
            else:
                if k == 1:
                    terme.append(f"x^{grad}")
                elif k == -1:
                    terme.append(f"-x^{grad}")
                else:
                    terme.append(f"{k}x^{grad}")

        if not terme:
            return "0"

        return "+".join(terme).replace("+-", "-")

    def _format_koeffizient(self, koeff: sp.Basic, grad: int) -> str:
        """Formatiert einen Koeffizienten für saubere Ausgabe."""
        if koeff == 0:
            return ""

        # Special cases for grade 0 (constant term)
        if grad == 0:
            return str(koeff)

        # Handle coefficient 1 and -1
        if koeff == 1:
            if grad == 1:
                return "x"
            else:
                return f"x^{grad}"
        elif koeff == -1:
            if grad == 1:
                return "-x"
            else:
                return f"-x^{grad}"

        # Handle general case
        if grad == 1:
            return f"{koeff}x"
        else:
            return f"{koeff}x^{grad}"

    def _dict_zu_sympy(self, koeff: dict[int, float]) -> sp.Basic:
        """Wandelt Koeffizienten-Dictionary in SymPy-Ausdruck um."""
        term = 0
        for grad, k in koeff.items():
            term += k * self.x**grad
        return term

    def _extrahiere_koeffizienten(self) -> list[sp.Basic]:
        """Extrahiert Koeffizienten aus SymPy-Ausdruck."""
        # Durch die Polynom-Validierung im Konstruktor ist dies immer möglich
        poly = Poly(self.term_sympy, self.x)

        # all_coeffs() gibt Koeffizienten von höchstem zu niedrigstem Grad zurück
        # Wir kehren die Reihenfolge um für [c0, c1, c2, ...] Format
        coeffs = poly.all_coeffs()
        coeffs.reverse()

        return coeffs

    def term(self) -> str:
        """Gibt den Term als String zurück."""
        # Single source of truth: Use self.term_sympy directly
        return str(self.term_sympy).replace("**", "^").replace("*", "").replace(" ", "")

    def term_latex(self) -> str:
        """Gibt den Term als LaTeX-String zurück."""
        return latex(self.term_sympy)

    def wert(self, x_wert: float) -> float:
        """Berechnet den Funktionswert an einer Stelle."""
        return float(self.term_sympy.subs(self.x, x_wert))

    def grad(self) -> int:
        """Gibt den Grad des Polynoms zurück"""
        return sp.Poly(self.term_sympy, self.x).degree()

    def kürzen(self) -> "GanzrationaleFunktion":
        """Kürzt die Funktion durch Faktorisierung"""
        self.term_sympy = sp.factor(self.term_sympy)
        self.term_str = str(self.term_sympy)
        return self

    def ableitung(self, ordnung: int = 1) -> "GanzrationaleFunktion":
        """Berechnet die Ableitung gegebener Ordnung."""
        abgeleitet = diff(self.term_sympy, self.x, ordnung)

        # Erstelle neue Funktion direkt mit dem abgeleiteten Ausdruck
        neue_funktion = GanzrationaleFunktion.__new__(GanzrationaleFunktion)
        neue_funktion.x = self.x
        neue_funktion.term_sympy = abgeleitet
        neue_funktion.term_str = str(abgeleitet)
        neue_funktion.koeffizienten = neue_funktion._extrahiere_koeffizienten()

        # Stelle sicher, dass die Koeffizientenliste die richtige Länge hat
        # (füge führende Nullen hinzu, wenn nötig)
        erwartete_laenge = max(0, len(self.koeffizienten) - ordnung)
        while len(neue_funktion.koeffizienten) < erwartete_laenge:
            neue_funktion.koeffizienten.insert(0, 0.0)

        return neue_funktion

    def nullstellen(self, real: bool = True, runden=None) -> list[sp.Basic]:
        """Berechnet die Nullstellen der Funktion.

        Args:
            real: Nur reelle Nullstellen zurückgeben
            runden: Anzahl Nachkommastellen für Rundung (None = exakt)

        Returns:
            Liste der Nullstellen als exakte symbolische Ausdrücke oder gerundete Zahlen
        """
        try:
            # Für höhere Grade (≥ 3) zuerst versuchen, rationale Nullstellen zu finden
            grad = len(self.koeffizienten) - 1
            if grad >= 3:
                rationale_nullstellen = self._rationale_nullstellen()
                if rationale_nullstellen:
                    # Lineare Faktoren abspalten
                    linearfaktoren, rest_polynom = self._faktorisiere()

                    nullstellen_liste = []

                    # Gefundene rationale Nullstellen hinzufügen
                    for nullstelle in rationale_nullstellen:
                        nullstellen_liste.append(_runde_wert(nullstelle, runden))

                    # Restpolynom lösen (kann quadratisch oder höher sein)
                    if rest_polynom != 1 and rest_polynom.degree(self.x) > 0:
                        rest_lösungen = solve(rest_polynom, self.x)

                        for lösung in rest_lösungen:
                            if real and not lösung.is_real:
                                continue

                            if lösung.is_real:
                                nullstellen_liste.append(_runde_wert(lösung, runden))
                            else:
                                # Komplexe Zahlen werden immer zu floats konvertiert
                                komplex_wert = complex(lösung)
                                if runden is not None:
                                    # Runde Real- und Imaginärteil
                                    komplex_wert = complex(
                                        round(komplex_wert.real, runden),
                                        round(komplex_wert.imag, runden),
                                    )
                                nullstellen_liste.append(komplex_wert)

                    # Sortiere Nullstellen (reelle zuerst, dann komplexe nach Realteil)
                    reelle_nullstellen = [
                        x
                        for x in nullstellen_liste
                        if hasattr(x, "is_real") and x.is_real
                    ]
                    komplexe_nullstellen = [
                        x
                        for x in nullstellen_liste
                        if not hasattr(x, "is_real") or not x.is_real
                    ]

                    # Sortiere reelle Nullstellen
                    reelle_nullstellen.sort(key=lambda x: float(x))

                    # Sortiere komplexe Nullstellen nach Realteil
                    komplexe_nullstellen.sort(key=lambda x: complex(x).real)

                    return reelle_nullstellen + komplexe_nullstellen

            # Für niedrigere Grade oder wenn Faktorisierung nicht funktioniert
            lösungen = solve(self.term_sympy, self.x)
            nullstellen_liste = []

            for lösung in lösungen:
                if real and not lösung.is_real:
                    continue

                if lösung.is_real:
                    nullstellen_liste.append(_runde_wert(lösung, runden))
                else:
                    # Komplexe Zahlen werden immer zu floats konvertiert
                    komplex_wert = complex(lösung)
                    if runden is not None:
                        # Runde Real- und Imaginärteil
                        komplex_wert = complex(
                            round(komplex_wert.real, runden),
                            round(komplex_wert.imag, runden),
                        )
                    nullstellen_liste.append(komplex_wert)

            # Sortiere Nullstellen (reelle zuerst, dann komplexe nach Realteil)
            reelle_nullstellen = [
                x for x in nullstellen_liste if hasattr(x, "is_real") and x.is_real
            ]
            komplexe_nullstellen = [
                x
                for x in nullstellen_liste
                if not hasattr(x, "is_real") or not x.is_real
            ]

            # Sortiere reelle Nullstellen
            reelle_nullstellen.sort(key=lambda x: float(x))

            # Sortiere komplexe Nullstellen nach Realteil
            komplexe_nullstellen.sort(key=lambda x: complex(x).real)

            return reelle_nullstellen + komplexe_nullstellen
        except Exception as e:
            print(f"Fehler bei Nullstellenberechnung: {e}")
            return []

    def _berechne_stationäre_stellen(self) -> list[sp.Basic]:
        """Berechnet alle stationären Stellen (f'(x) = 0)."""
        try:
            # Erste Ableitung
            f_strich = self.ableitung(1)

            # Kritische Punkte
            kritische_punkte = solve(f_strich.term_sympy, self.x)

            stationäre_stellen = []

            for punkt in kritische_punkte:
                if punkt.is_real:
                    stationäre_stellen.append(punkt)

            return sorted(stationäre_stellen, key=lambda x: float(x))
        except Exception:
            return []

    def _klassifiziere_extremum(self, x_wert: sp.Basic) -> str:
        """Klassifiziert eine stationäre Stelle als Minimum, Maximum oder Sattelpunkt."""
        try:
            # Zweite Ableitung
            f_doppelstrich = self.ableitung(2)
            y_wert = f_doppelstrich.wert(float(x_wert))

            if y_wert > 0:
                return "Minimum"
            elif y_wert < 0:
                return "Maximum"
            else:
                return "Sattelpunkt"
        except Exception:
            return "Unbestimmbar"

    def extremstellen(
        self, typ: bool = True, runden=None
    ) -> list[sp.Basic] | list[tuple[sp.Basic, str]]:
        """Berechnet die Extremstellen der Funktion.

        Args:
            typ: Wenn True, liefert (x_wert, art) Tupel. Wenn False, nur x_werte.
            runden: Anzahl Nachkommastellen für Rundung (None = exakt)
        """
        stationäre_stellen = self._berechne_stationäre_stellen()

        # Wende Rundung an wenn nötig
        if runden is not None:
            stationäre_stellen = [
                _runde_wert(stelle, runden) for stelle in stationäre_stellen
            ]

        if not typ:
            return stationäre_stellen

        # Mit Klassifikation
        extremstellen = []
        for x_wert in stationäre_stellen:
            art = self._klassifiziere_extremum(x_wert)
            extremstellen.append((x_wert, art))

        return extremstellen

    def _berechne_wendestellen(self) -> list[sp.Basic]:
        """Berechnet alle Wendestellen (f''(x) = 0)."""
        try:
            # Zweite Ableitung
            f_second_deriv = self.ableitung(2)

            # Kandidaten für Wendestellen (f''(x) = 0)
            candidates = solve(f_second_deriv.term_sympy, self.x)

            wendestellen = []

            for point in candidates:
                if not point.is_real:
                    continue

                # Prüfe höhere Ableitungen
                first_nonzero_deriv_order = 0
                for order in range(3, MAX_DERIVATIVE_ORDER_CHECK + 1):
                    higher_deriv = self.ableitung(order)
                    value = higher_deriv.wert(float(point))

                    if not np.isclose(value, 0, atol=DEFAULT_TOLERANCE):
                        first_nonzero_deriv_order = order
                        break

                # Wendepunkt existiert, wenn erste nicht-null Ableitung ungerade Ordnung hat
                if first_nonzero_deriv_order > 0 and first_nonzero_deriv_order % 2 != 0:
                    wendestellen.append(point)

            return sorted(wendestellen, key=lambda x: float(x))

        except Exception as e:
            log.error(
                f"Could not calculate wendestellen for {self.term_sympy}. Reason: {e}"
            )
            return []

    def _klassifiziere_wendepunkt(self, x_wert: sp.Basic) -> str:
        """Analysiert die Krümmungsänderung an einem Wendepunkt."""
        try:
            # Testpunkte links und rechts vom Wendepunkt
            delta = 0.01
            x_links = float(x_wert) - delta
            x_rechts = float(x_wert) + delta

            # Zweite Ableitung für Krümmungsanalyse
            f_second_deriv = self.ableitung(2)
            y_links = f_second_deriv.wert(x_links)
            y_rechts = f_second_deriv.wert(x_rechts)

            if y_links < 0 and y_rechts > 0:
                return "L→R"  # Linksgekrümmt → Rechtsgekrümmt
            elif y_links > 0 and y_rechts < 0:
                return "R→L"  # Rechtsgekrümmt → Linksgekrümmt
            else:
                return "Keine Änderung"
        except Exception:
            return "Unbestimmbar"

    def wendestellen(
        self, typ: bool = True, runden=None
    ) -> list[sp.Basic] | list[tuple[sp.Basic, str]]:
        """Berechnet die Wendestellen der Funktion.

        Args:
            typ: Wenn True, liefert (x_wert, krümmungsänderung) Tupel. Wenn False, nur x_werte.
            runden: Anzahl Nachkommastellen für Rundung (None = exakt)
        """
        wendestellen = self._berechne_wendestellen()

        # Wende Rundung an wenn nötig
        if runden is not None:
            wendestellen = [_runde_wert(stelle, runden) for stelle in wendestellen]

        if not typ:
            return wendestellen

        # Mit Krümmungsanalyse
        klassifizierte_wendestellen = []
        for x_wert in wendestellen:
            krümmung = self._klassifiziere_wendepunkt(x_wert)
            klassifizierte_wendestellen.append((x_wert, krümmung))

        return klassifizierte_wendestellen

    def extrempunkte(
        self, typ: bool = True, runden=None
    ) -> list[tuple[sp.Basic, sp.Basic]] | list[tuple[sp.Basic, sp.Basic, str]]:
        """Berechnet die Extrempunkte (x, y-Koordinaten).

        Args:
            typ: Wenn True, liefert (x, y, art) Tupel. Wenn False, nur (x, y) Tupel.
            runden: Anzahl Nachkommastellen für Rundung (None = exakt)
        """
        # Hole x-Koordinaten
        extremstellen = self.extremstellen(typ=False, runden=runden)

        # Berechne y-Koordinaten
        punkte = []
        for x_wert in extremstellen:
            if runden is None:
                # Exakte Berechnung mit SymPy
                y_wert = self.term_sympy.subs(self.x, x_wert)
            else:
                # Numerische Berechnung mit Rundung
                y_wert = self.wert(float(x_wert))
                y_wert = _runde_wert(y_wert, runden)
            punkte.append((x_wert, y_wert))

        if not typ:
            return punkte

        # Füge Klassifikation hinzu
        klassifizierte_punkte = []
        for x_wert, y_wert in punkte:
            art = self._klassifiziere_extremum(x_wert)
            klassifizierte_punkte.append((x_wert, y_wert, art))

        return klassifizierte_punkte

    def wendepunkte(
        self, typ: bool = True, runden=None
    ) -> list[tuple[sp.Basic, sp.Basic]] | list[tuple[sp.Basic, sp.Basic, str]]:
        """Berechnet die Wendepunkte (x, y-Koordinaten).

        Args:
            typ: Wenn True, liefert (x, y, krümmungsänderung) Tupel. Wenn False, nur (x, y) Tupel.
            runden: Anzahl Nachkommastellen für Rundung (None = exakt)
        """
        # Hole x-Koordinaten
        wendestellen = self.wendestellen(typ=False, runden=runden)

        # Berechne y-Koordinaten
        punkte = []
        for x_wert in wendestellen:
            if runden is None:
                # Exakte Berechnung mit SymPy
                y_wert = self.term_sympy.subs(self.x, x_wert)
            else:
                # Numerische Berechnung mit Rundung
                y_wert = self.wert(float(x_wert))
                y_wert = _runde_wert(y_wert, runden)
            punkte.append((x_wert, y_wert))

        if not typ:
            return punkte

        # Füge Krümmungsanalyse hinzu
        klassifizierte_punkte = []
        for x_wert, y_wert in punkte:
            krümmung = self._klassifiziere_wendepunkt(x_wert)
            klassifizierte_punkte.append((x_wert, y_wert, krümmung))

        return klassifizierte_punkte

    def _rationale_nullstellen(self) -> list[sp.Rational]:
        """
        Berechnet rationale Nullstellen mit Rational Root Theorem.

        Für ein Polynom a_n*x^n + ... + a_1*x + a_0 sind mögliche rationale
        Nullstellen p/q, wobei p Teiler von a_0 und q Teiler von a_n ist.
        """
        if len(self.koeffizienten) <= 2:  # Linear oder konstant
            return []

        # Letzter Koeffizient (a_0) und führender Koeffizient (a_n)
        a0 = self.koeffizienten[0]
        an = self.koeffizienten[-1]

        # Wenn a0 oder an Null sind,定理 nicht anwendbar
        if a0 == 0 or an == 0:
            return []

        # Teiler von a0 (p) und an (q) finden
        def finde_teiler(zahl):
            if isinstance(zahl, Rational):
                zaehler = int(zahl.p)
                nenner = int(zahl.q)
                teiler_zaehler = {
                    t
                    for t in range(-abs(zaehler), abs(zaehler) + 1)
                    if t != 0 and zaehler % t == 0
                }
                teiler_nenner = {
                    t for t in range(1, abs(nenner) + 1) if nenner % t == 0
                }
                return teiler_zaehler, teiler_nenner
            else:
                return {
                    t
                    for t in range(-abs(int(zahl)), abs(int(zahl)) + 1)
                    if t != 0 and int(zahl) % t == 0
                }, {1}

        # Teiler für a0 und an finden
        if isinstance(a0, Rational):
            teiler_p_zaehler, teiler_p_nenner = finde_teiler(a0)
            teiler_p = {
                sp.Rational(p_z, p_n)
                for p_z in teiler_p_zaehler
                for p_n in teiler_p_nenner
            }
        else:
            teiler_p_zaehler, _ = finde_teiler(a0)
            teiler_p = {sp.Rational(t, 1) for t in teiler_p_zaehler}

        if isinstance(an, Rational):
            teiler_q_zaehler, teiler_q_nenner = finde_teiler(an)
            teiler_q = {
                sp.Rational(q_z, q_n)
                for q_z in teiler_q_zaehler
                for q_n in teiler_q_nenner
            }
        else:
            teiler_q_zaehler, _ = finde_teiler(an)
            teiler_q = {sp.Rational(t, 1) for t in teiler_q_zaehler}

        # Mögliche rationale Nullstellen: p/q für alle p in teiler_p, q in teiler_q
        moegliche_kandidaten = set()
        for p in teiler_p:
            for q in teiler_q:
                if q != 0:
                    kandidat = p / q
                    moegliche_kandidaten.add(kandidat)

        # Kandidaten testen
        gefundene_nullstellen = []
        for kandidat in sorted(moegliche_kandidaten):
            # Substituiere kandidat in das Polynom
            ergebnis = self.term_sympy.subs(self.x, kandidat)
            if ergebnis == 0:
                gefundene_nullstellen.append(kandidat)

        return gefundene_nullstellen

    def _faktorisiere(self) -> tuple[list[sp.Basic], sp.Basic]:
        """
        Versucht, das Polynom zu faktorisieren.

        Returns:
            Tuple[List[sp.Basic], sp.Basic]: (Linearfaktoren, Restpolynom)
        """
        # Zuerst versuchen, das gesamte Polynom zu faktorisieren
        faktorisiert = factor(self.term_sympy)

        if faktorisiert != self.term_sympy:
            # Erfolgreich faktorisiert
            return [faktorisiert], sp.Integer(1)

        # Wenn vollständige Faktorisierung nicht funktioniert,
        # versuche rationale Nullstellen zu finden und abzuspalten
        rationale_nullstellen = self._rationale_nullstellen()

        if not rationale_nullstellen:
            return [], self.term_sympy

        linearfaktoren = []
        rest_polynom = self.term_sympy

        for nullstelle in rationale_nullstellen:
            # Linearfaktor (x - nullstelle)
            if nullstelle == 0:
                linearfaktor = self.x
            else:
                linearfaktor = self.x - nullstelle

            # Testen, ob dieser Faktor tatsächlich teilt
            quotient, rest = sp.div(rest_polynom, linearfaktor)
            if rest == 0:
                linearfaktoren.append(linearfaktor)
                rest_polynom = quotient

        return linearfaktoren, rest_polynom

    def _kubische_spezialfaelle(self) -> tuple[bool, list[sp.Basic], str]:
        """
        Erkennt und löst spezielle kubische Formen.

        Returns:
            Tuple[bool, List[sp.Basic], str]: (erfolgreich, nullstellen, erkennungsmethode)
        """
        if len(self.koeffizienten) != 4:  # Nicht kubisch
            return False, [], ""

        a, b, c, d = (
            self.koeffizienten[3],
            self.koeffizienten[2],
            self.koeffizienten[1],
            self.koeffizienten[0],
        )

        # Spezialfall 1: x³ + px + q = 0 (fehlendes x²-Glied)
        if b == 0:
            try:
                # Lösungsformel für reduzierte kubische Gleichung
                # x³ + px + q = 0
                p = c / a
                q = d / a

                discriminant = (q / 2) ** 2 + (p / 3) ** 3

                if discriminant >= 0:
                    # Eine reelle Nullstelle
                    u = (-q / 2 + sp.sqrt(discriminant)) ** (sp.Rational(1, 3))
                    v = (-q / 2 - sp.sqrt(discriminant)) ** (sp.Rational(1, 3))
                    x1 = u + v

                    # Komplexe Nullstellen berechnen
                    omega = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / sp.Rational(2)
                    x2 = omega * u + omega**2 * v
                    x3 = omega**2 * u + omega * v

                    return (
                        True,
                        [x1, x2, x3],
                        "Reduzierte kubische Gleichung (x³ + px + q = 0)",
                    )
                else:
                    # Drei reelle Nullstellen (Cardanische Formel mit trigonometrischer Lösung)
                    # Hier vereinfacht durch Rückgriff auf SymPy
                    return False, [], ""
            except Exception:
                return False, [], ""

        # Spezialfall 2: (x - a)³ = x³ - 3ax² + 3a²x - a³
        # Prüfe, ob es sich um eine vollständige dritte Potenz handelt
        try:
            # Versuche, die Form zu erkennen
            if b == -3 * a and c == 3 * a**2 and d == -(a**3):
                x1 = a
                return True, [x1, x1, x1], "Vollständige dritte Potenz"
        except Exception:
            pass

        # Spezialfall 3: Rationale Nullstelle vorhanden
        rationale_nullstellen = self._rationale_nullstellen()
        if rationale_nullstellen:
            return True, rationale_nullstellen, "Rationale Nullstellen gefunden"

        return False, [], ""

    def _intelligente_loesungsanalyse(self) -> dict[str, Any]:
        """
        Nutzt SymPy's Intelligenz zur Identifikation menschlich nachvollziehbarer Lösungswege.
        """
        term = self.term_sympy
        grad = len(self.koeffizienten) - 1

        analyse = {
            "grad": grad,
            "sympy_factor": None,
            "sympy_roots": None,
            "muster": [],
            "loesungswege": [],
            "empfohlener_weg": None,
        }

        # 1. SymPy's Faktorisierung und Nullstellen abfragen
        try:
            analyse["sympy_factor"] = factor(term)
            analyse["sympy_roots"] = sp.roots(term)
        except Exception:
            pass

        # 2. Muster-Liste initialisieren
        muster = []

        # 3. Partielle Faktorisierung analysieren
        if analyse["sympy_factor"] and isinstance(analyse["sympy_factor"], sp.Mul):
            partial_analysis = self._analysiere_partielle_faktorisierung(
                analyse["sympy_factor"]
            )
            if partial_analysis["einfache_faktoren"]:
                analyse["partielle_faktorisierung"] = partial_analysis
                muster.append("partielle_faktorisierung")

        # 4. Weitere Muster erkennen

        # Muster 1: Differenz von Quadraten
        if self._ist_differenz_von_quadraten(term):
            muster.append("differenz_von_quadraten")

        # Muster 2: Perfekte Potenzen
        if self._ist_perfekte_potenz(analyse["sympy_factor"]):
            muster.append("perfekte_potenz")

        # Muster 3: Symmetrische Nullstellen
        if self._ist_symmetrisch(analyse["sympy_roots"]):
            muster.append("symmetrisch")

        # Muster 4: Rationale Nullstellen
        if self._hat_rationale_nullstellen(analyse["sympy_roots"]):
            muster.append("rationale_nullstellen")

        # Muster 5: Linearfaktoren
        if self._ist_linearfaktorisiert(analyse["sympy_factor"]):
            muster.append("linearfaktoren")

        analyse["muster"] = muster

        # 3. Lösungswege priorisieren
        analyse["empfohlener_weg"] = self._waehle_empfohlenen_weg(muster, grad)

        return analyse

    def _ist_differenz_von_quadraten(self, term: sp.Basic) -> bool:
        """Prüft, ob der Term eine Differenz von Quadraten ist."""
        if term.is_polynomial():
            try:
                # Prüfe auf Form a² - b² durch Koeffizientenanalyse
                koeffizienten = self.koeffizienten
                grad = len(koeffizienten) - 1

                # Differenz von Quadraten: x^n - a (wobei n gerade)
                if grad % 2 == 0 and grad >= 2:
                    # Prüfe ob nur zwei von null verschiedene Koeffizienten existieren
                    nicht_null = [i for i, k in enumerate(koeffizienten) if k != 0]
                    if len(nicht_null) == 2:
                        # Form: x^n - a oder a - x^n
                        return (nicht_null[0] == 0 and nicht_null[1] == grad) or (
                            nicht_null[0] == grad and nicht_null[1] == 0
                        )

                # Prüfe durch Faktorisierung
                faktorisiert = factor(term)
                if isinstance(faktorisiert, sp.Mul):
                    faktoren = sp.Mul.make_args(faktorisiert)
                    if len(faktoren) == 2:
                        f1, f2 = faktoren
                        # Prüfe auf (a+b)(a-b) Form
                        if (
                            f1.is_Add
                            and len(f1.args) == 2
                            and f2.is_Add
                            and len(f2.args) == 2
                        ):
                            # Extrahiere Terme aus beiden Faktoren
                            f1_terme = [arg for arg in f1.args if arg.has(self.x)]
                            f2_terme = [arg for arg in f2.args if arg.has(self.x)]
                            if len(f1_terme) == 1 and len(f2_terme) == 1:
                                # Prüfe ob einer negativ des anderen ist
                                return f1_terme[0] == -f2_terme[0]
            except Exception:
                pass
        return False

    def _ist_perfekte_potenz(self, faktorisiert: sp.Basic) -> bool:
        """Prüft, ob es sich um eine perfekte Potenz handelt."""
        if isinstance(faktorisiert, sp.Pow):
            return True
        return False

    def _ist_symmetrisch(self, roots_dict: dict) -> bool:
        """Prüft, ob Nullstellen symmetrisch sind."""
        if not roots_dict:
            return False

        nullstellen = list(roots_dict.keys())
        # Prüfe ob für jede Nullstelle a auch -a existiert (bis auf Vielfachheit)
        for nullstelle in nullstellen:
            if nullstelle != 0 and -nullstelle not in nullstellen:
                return False
        return True

    def _hat_rationale_nullstellen(self, roots_dict: dict) -> bool:
        """Prüft, ob rationale Nullstellen vorhanden sind."""
        if not roots_dict:
            return False

        for nullstelle in roots_dict.keys():
            if nullstelle.is_rational:
                return True
        return False

    def _ist_linearfaktorisiert(self, faktorisiert: sp.Basic) -> bool:
        """Prüft, ob vollständig in Linearfaktoren zerlegt."""
        if isinstance(faktorisiert, sp.Mul):
            faktoren = sp.Mul.make_args(faktorisiert)
            for faktor in faktoren:
                # Prüfe ob Linearfaktor (Grad 1)
                try:
                    if not (
                        faktor.is_polynomial() and Poly(faktor, self.x).degree() == 1
                    ):
                        return False
                except Exception:
                    return False
            return True
        return False

    def _waehle_empfohlenen_weg(self, muster: list[str], grad: int) -> str:
        """Wählt den empfohlenen Lösungswege."""
        # Priorisierte Strategien nach "menschlicher Einfachheit"
        strategie_prio = [
            "differenz_von_quadraten",  # Sehr einfach
            "perfekte_potenz",  # Sehr einfach
            "symmetrisch",  # Mittel (Substitution)
            "rationale_nullstellen",  # Mittel (Systematisch)
            "linearfaktoren",  # Einfach
        ]

        for strategie in strategie_prio:
            if strategie in muster:
                return strategie

        return "allgemein"

    def _analysiere_partielle_faktorisierung(
        self, faktorisiert: sp.Basic
    ) -> dict[str, list[tuple[str, sp.Basic]]]:
        """
        Analysiert partielle Faktorisierungen und klassifiziert Faktoren.

        Returns:
            Dict mit 'einfache_faktoren' und 'komplexe_faktoren'
        """
        if not isinstance(faktorisiert, sp.Mul):
            return {
                "einfache_faktoren": [],
                "komplexe_faktoren": [("unbekannt", faktorisiert)],
            }

        faktoren = sp.Mul.make_args(faktorisiert)
        einfache_faktoren = []
        komplexe_faktoren = []

        # Konstanten für Faktor-Typen
        TYP_LINEAR = "linear"
        TYP_QUADRATISCH_REELL = "quadratisch_reell"
        TYP_QUADRATISCH_KOMPLEX = "quadratisch_komplex"
        TYP_PERFEKTE_POTENZ = "perfekte_potenz"
        TYP_DIFFERENZ_QUADRATEN = "differenz_quadraten"
        TYP_HOCH_GRAD = "hoch_grad"
        TYP_NICHT_POLYNOM = "nicht_polynom"
        TYP_UNBEKANNT = "unbekannt"

        for faktor in faktoren:
            try:
                # Prüfe auf Konstanten
                if faktor.is_constant():
                    continue

                # Prüfe, ob es überhaupt ein Polynom in unserer Variable ist
                if not isinstance(faktor, sp.Expr) or self.x not in faktor.free_symbols:
                    komplexe_faktoren.append((TYP_NICHT_POLYNOM, faktor))
                    continue

                if not faktor.is_polynomial(self.x):
                    komplexe_faktoren.append((TYP_NICHT_POLYNOM, faktor))
                    continue

                # Poly-Objekt einmal erstellen und wiederverwenden
                try:
                    poly_faktor = Poly(faktor, self.x)
                except (sp.PolynomialError, sp.CoercionFailed):
                    komplexe_faktoren.append((TYP_NICHT_POLYNOM, faktor))
                    continue

                grad = poly_faktor.degree()

                if grad == 1:
                    # Linearfaktor - immer einfach
                    einfache_faktoren.append((TYP_LINEAR, faktor))
                elif grad == 2:
                    # Quadratischer Faktor - prüfe auf reelle Nullstellen
                    try:
                        coeffs = poly_faktor.all_coeffs()
                        # Koeffizienten sicher extrahieren
                        if len(coeffs) == 3:
                            a, b, c = coeffs
                        elif len(coeffs) == 2:
                            a, b = coeffs
                            c = 0
                        else:
                            raise ValueError("Unerwartete Anzahl von Koeffizienten")

                        if a == 0:  # Eigentlich linear
                            komplexe_faktoren.append((TYP_HOCH_GRAD, faktor))
                            continue

                        diskriminante = b**2 - 4 * a * c
                        if diskriminante >= 0:
                            einfache_faktoren.append((TYP_QUADRATISCH_REELL, faktor))
                        else:
                            komplexe_faktoren.append((TYP_QUADRATISCH_KOMPLEX, faktor))
                    except (IndexError, ValueError, TypeError):
                        komplexe_faktoren.append((TYP_QUADRATISCH_KOMPLEX, faktor))
                else:
                    # Höhergradiger Faktor - prüfe auf spezielle Formen
                    if self._ist_perfekte_potenz(faktor):
                        einfache_faktoren.append((TYP_PERFEKTE_POTENZ, faktor))
                    elif self._ist_differenz_von_quadraten(faktor):
                        einfache_faktoren.append((TYP_DIFFERENZ_QUADRATEN, faktor))
                    else:
                        komplexe_faktoren.append((TYP_HOCH_GRAD, faktor))

            except (sp.PolynomialError, sp.CoercionFailed):
                # Spezifische SymPy-Fehler behandeln
                komplexe_faktoren.append(("fehler_polynom", faktor))
            except Exception:
                # Unerwartete Fehler - in echter Anwendung hier logging verwenden
                # import logging
                # logging.warning(f"Unerwarteter Fehler bei Faktor {faktor}: {e}")
                komplexe_faktoren.append((TYP_UNBEKANNT, faktor))

        return {
            "einfache_faktoren": einfache_faktoren,
            "komplexe_faktoren": komplexe_faktoren,
        }

    def _berechne_lineare_nullstelle(self, faktor: sp.Basic) -> list[sp.Expr]:
        """Berechnet Nullstelle für linearen Faktor."""
        try:
            a, b = Poly(faktor, self.x).all_coeffs()
            if a == 0:
                return []
            return [-b / a]
        except (ValueError, TypeError, IndexError):
            return []

    def _berechne_quadratische_nullstellen(self, faktor: sp.Basic) -> list[sp.Expr]:
        """Berechnet reelle Nullstellen für quadratischen Faktor."""
        try:
            a, b, c = Poly(faktor, self.x).all_coeffs()
            if a == 0:
                return []
            diskriminante = b**2 - 4 * a * c
            if diskriminante >= 0:
                x1 = (-b + sp.sqrt(diskriminante)) / (2 * a)
                x2 = (-b - sp.sqrt(diskriminante)) / (2 * a)
                return sorted({x1, x2})
            return []
        except (ValueError, TypeError, IndexError):
            return []

    def nullstellen_weg(self) -> str:
        """Gibt detaillierten Lösungsweg für Nullstellen als Markdown zurück."""
        weg = f"# Nullstellen von f(x) = {self.original_eingabe}\n\n"
        weg += f"Gegeben ist die Funktion: $$f(x) = {self.term_latex()}$$\n\n"

        # Intelligente Analyse mit SymPy-Mustererkennung
        analyse = self._intelligente_loesungsanalyse()
        weg += "## Intelligente Mustererkennung\n\n"
        weg += f"Erkannte Muster: {', '.join(analyse['muster']) if analyse['muster'] else 'Keine speziellen Muster'}\n"
        weg += f"Empfohlener Lösungsweg: **{analyse['empfohlener_weg'].replace('_', ' ').title()}**\n\n"

        # Spezielle Lösungswege basierend auf erkannten Mustern

        # Differenz von Quadraten
        if "differenz_von_quadraten" in analyse["muster"]:
            weg += "## Lösungsweg: Differenz von Quadraten\n\n"
            weg += "### Formel: a² - b² = (a+b)(a-b)\n\n"

            # Zeige die Faktorisierung
            if analyse["sympy_factor"]:
                weg += "### Schritt 1: Anwenden der Formel\n\n"
                weg += f"$$f(x) = {latex(analyse['sympy_factor'])}$$\n\n"

                # Zeige die Nullstellen aus der Faktorisierung
                if analyse["sympy_roots"]:
                    weg += "### Schritt 2: Nullstellen berechnen\n\n"
                    weg += "Setze jeden Faktor gleich null:\n\n"

                    for nullstelle, vielfachheit in analyse["sympy_roots"].items():
                        weg += f"- $$x = {nullstelle}"
                        if vielfachheit > 1:
                            weg += f" \\text{{ (Vielfachheit {vielfachheit})}}"
                        weg += "$$\n"

        # Perfekte Potenzen
        elif "perfekte_potenz" in analyse["muster"]:
            weg += "## Lösungsweg: Perfekte Potenz\n\n"
            weg += "### Formel: (x-a)ⁿ = 0 ⇒ x = a\n\n"

            if analyse["sympy_roots"]:
                weg += "Die Funktion hat eine Nullstelle mit Vielfachheit:\n\n"
                for nullstelle, vielfachheit in analyse["sympy_roots"].items():
                    weg += f"- $$x = {nullstelle} \\text{{ (Vielfachheit {vielfachheit})}}$$\n"

        # Symmetrische Polynome
        elif "symmetrisch" in analyse["muster"]:
            weg += "## Lösungsweg: Symmetrisches Polynom\n\n"
            weg += "### Erkenntnis: Die Nullstellen sind symmetrisch\n\n"
            weg += "Bei symmetrischen Polynomen kann oft die Substitution z = x² verwendet werden.\n\n"

            if analyse["sympy_roots"]:
                weg += "### Nullstellen:\n\n"
                for nullstelle, vielfachheit in analyse["sympy_roots"].items():
                    weg += f"- $$x = {nullstelle}"
                    if vielfachheit > 1:
                        weg += f" \\text{{ (Vielfachheit {vielfachheit})}}"
                    weg += "$$\n"

        # Partielle Faktorisierung
        elif (
            "partielle_faktorisierung" in analyse["muster"]
            and "partielle_faktorisierung" in analyse
        ):
            weg += "## Lösungsweg: Partielle Faktorisierung\n\n"
            weg += "### Erkenntnis: Die Funktion lässt sich teilweise faktorisieren\n\n"
            weg += "Einige Faktoren sind einfach zu lösen, während andere komplexer bleiben.\n\n"

            partial = analyse["partielle_faktorisierung"]

            # Konstanten für Faktor-Typen (müssen mit der Analyse-Methode übereinstimmen)
            TYP_LINEAR = "linear"
            TYP_QUADRATISCH_REELL = "quadratisch_reell"

            # Mapping von Faktor-Typ zu Berechnungsfunktion
            faktor_loeser = {
                TYP_LINEAR: self._berechne_lineare_nullstelle,
                TYP_QUADRATISCH_REELL: self._berechne_quadratische_nullstellen,
            }

            if partial["einfache_faktoren"]:
                weg += "### Einfach lösbare Faktoren:\n\n"
                for typ, faktor in partial["einfache_faktoren"]:
                    weg += (
                        f"**{typ.replace('_', ' ').title()}**: $${sp.latex(faktor)}$$\n"
                    )

                    # Verwende das Mapping für die Berechnung
                    loeser_func = faktor_loeser.get(typ)
                    if loeser_func:
                        try:
                            nullstellen = loeser_func(faktor)
                            if nullstellen:
                                # Formatiere die Nullstellen mit LaTeX
                                if len(nullstellen) == 1:
                                    weg += f"   - Nullstelle: $$x = {sp.latex(nullstellen[0])}$$\n"
                                else:
                                    formatted_nullstellen = ", \\quad ".join(
                                        [
                                            f"x_{i + 1} = {sp.latex(n)}"
                                            for i, n in enumerate(nullstellen)
                                        ]
                                    )
                                    weg += f"   - Nullstellen: $${formatted_nullstellen}$$\n"
                            else:
                                weg += "   - Dieser Faktor hat keine reellen Nullstellen.\n"
                        except Exception:
                            weg += (
                                "   - Konnte Nullstellen nicht automatisch berechnen.\n"
                            )
                    else:
                        weg += "   - Kein spezifisches Lösungsverfahren für diesen Faktortyp.\n"

            if partial["komplexe_faktoren"]:
                weg += "### Komplexe Faktoren:\n\n"
                for typ, faktor in partial["komplexe_faktoren"]:
                    weg += (
                        f"**{typ.replace('_', ' ').title()}**: $${sp.latex(faktor)}$$\n"
                    )
                    weg += "   - Dieser Faktor erfordert fortgeschrittenere Methoden.\n"

            # Zusammenfassung aller gefundenen Nullstellen
            if analyse["sympy_roots"]:
                weg += "### Alle Nullstellen der Funktion:\n\n"
                for nullstelle, vielfachheit in analyse["sympy_roots"].items():
                    weg += f"- $$x = {nullstelle}"
                    if vielfachheit > 1:
                        weg += f" \\text{{ (Vielfachheit {vielfachheit})}}"
                    weg += "$$\n"

        # Verschiedene Lösungswege je nach Grad
        grad = len(self.koeffizienten) - 1

        if grad == 0:
            weg += "Bei einer konstanten Funktion gibt es keine Nullstellen.\n"
        elif grad == 1:
            weg += "## Lineare Funktion (Grad 1)\n\n"
            weg += f"$$f(x) = {self.term_latex()} = 0$$\n\n"

            a, b = self.koeffizienten[1], self.koeffizienten[0]
            ergebnis = -b / a
            weg += f"$$x = -\\frac{{{b}}}{{{a}}} = {ergebnis}$$\n"

        elif grad == 2:
            weg += "## Quadratische Funktion (Grad 2)\n\n"
            weg += f"$$f(x) = {self.term_latex()} = 0$$\n\n"

            a, b, c = (
                self.koeffizienten[2],
                self.koeffizienten[1],
                self.koeffizienten[0],
            )

            # Mitternachtsformel
            diskriminante = b**2 - 4 * a * c

            weg += "### Mitternachtsformel\n\n"
            weg += "$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$\n\n"
            weg += f"Mit a = {a}, b = {b}, c = {c}:\n\n"
            weg += f"$$x = \\frac{{-{b} \\pm \\sqrt{{{b}^2 - 4 \\cdot {a} \\cdot {c}}}}}{{2 \\cdot {a}}}$$\n\n"
            weg += (
                f"$$x = \\frac{{-{b} \\pm \\sqrt{{{diskriminante}}}}}{{{2 * a}}}$$\n\n"
            )

            if diskriminante > 0:
                weg += "### Zwei reelle Nullstellen\n\n"
                sqrt_d = sp.sqrt(diskriminante)
                x1 = (-b + sqrt_d) / (2 * a)
                x2 = (-b - sqrt_d) / (2 * a)
                weg += f"$$x_1 = \\frac{{-{b} + \\sqrt{{{diskriminante}}}}}{{{2 * a}}} = {x1}$$\n\n"
                weg += f"$$x_2 = \\frac{{-{b} - \\sqrt{{{diskriminante}}}}}{{{2 * a}}} = {x2}$$\n\n"
            elif diskriminante == 0:
                weg += "### Eine doppelte Nullstelle\n\n"
                x = -b / (2 * a)
                weg += f"$$x = \\frac{{-{b}}}{{{2 * a}}} = {x}$$\n\n"
            else:
                weg += "### Keine reellen Nullstellen\n\n"
                weg += f"Da die Diskriminante D = {diskriminante} < 0 ist, gibt es keine reellen Nullstellen.\n\n"

                # Quadratische Ergänzung zeigen
                weg += "### Quadratische Ergänzung\n\n"
                weg += f"$$f(x) = {self.term_latex()}$$\n\n"
                weg += f"$$= {a}x^2 {b if b >= 0 else f'-{abs(b)}'}x {c if c >= 0 else f'-{abs(c)}'}$$\n\n"
                weg += f"$$= {a}\\left(x^2 {float(b / a):+}x\\right) {float(c):+}$$\n\n"
                weg += f"$$= {a}\\left(x^2 {float(b / a):+}x + \\left({float(b / (2 * a)):.3f}\\right)^2 - \\left({float(b / (2 * a)):.3f}\\right)^2\\right) {float(c):+}$$\n\n"
                weg += f"$$= {a}\\left(\\left(x {float(b / (2 * a)):+.3f}\\right)^2 - {float(b**2 / (4 * a**2)):.3f}\\right) {float(c):+}$$\n\n"
                weg += f"$$= {a}\\left(x {float(b / (2 * a)):+.3f}\\right)^2 - {float(b**2 / (4 * a)):.3f} {float(c):+}$$\n\n"
                weg += f"$$= {a}\\left(x {float(b / (2 * a)):+.3f}\\right)^2 {float(c - b**2 / (4 * a)):+.3f}$$\n\n"
                weg += f"Da {a} > 0 und der Term {a}(x {float(b / (2 * a)):+.3f})² ≥ 0 ist, ergibt sich:\n\n"
                weg += f"$$f(x) \\geq {float(c - b**2 / (4 * a)):+.3f} > 0$$\n\n"
                weg += "Somit hat die Funktion keine reellen Nullstellen.\n"

        elif grad == 3:
            weg += "## Kubische Funktion (Grad 3)\n\n"

            # Spezialfälle für kubische Funktionen überprüfen
            erfolgreich, spezial_nullstellen, methode = self._kubische_spezialfaelle()

            if erfolgreich:
                weg += f"### Spezialfall: {methode}\n\n"
                weg += (
                    f"Die Funktion lässt sich als Spezialfall erkennen: {methode}\n\n"
                )
                weg += "Die Nullstellen sind:\n\n"

                for i, nullstelle in enumerate(spezial_nullstellen, 1):
                    if hasattr(nullstelle, "is_real") and nullstelle.is_real:
                        weg += f"- x_{i} = {nullstelle}\n"
                    else:
                        weg += f"- x_{i} = {nullstelle} (komplex)\n"
                weg += "\n"
            else:
                weg += "### Allgemeine kubische Gleichung\n\n"
                weg += "Für die allgemeine kubische Gleichung verwenden wir den Rational Root Theorem:\n\n"

                # Fallback auf die allgemeine Methode für höhere Grade
                rationale_nullstellen = self._rationale_nullstellen()

                if rationale_nullstellen:
                    weg += "### Rational Root Theorem\n\n"
                    weg += "Für rationale Nullstellen p/q gilt:\n"
                    weg += "- p ist Teiler des absoluten Glieds (a₀)\n"
                    weg += "- q ist Teiler des Leitkoeffizienten (aₙ)\n\n"

                    a0 = self.koeffizienten[0]
                    an = self.koeffizienten[-1]
                    weg += f"Mit a₀ = {a0} und aₙ = {an}:\n\n"

                    weg += "### Gefundene rationale Nullstellen\n\n"
                    for nullstelle in rationale_nullstellen:
                        weg += f"- x = {nullstelle}\n"
                    weg += "\n"

                    # Faktorisierung zeigen
                    linearfaktoren, rest_polynom = self._faktorisiere()

                    if linearfaktoren:
                        weg += "### Faktorisierung\n\n"
                        weg += "Das Polynom lässt sich faktorisieren als:\n\n"

                        faktor_darstellung = ""
                        for faktor in linearfaktoren:
                            if faktor_darstellung:
                                faktor_darstellung += " · "
                            faktor_darstellung += f"({latex(faktor)})"

                        if rest_polynom != 1:
                            faktor_darstellung += f" · {latex(rest_polynom)}"

                        weg += f"$$f(x) = {faktor_darstellung}$$\n\n"

                        # Restpolynom lösen
                        if rest_polynom != 1 and rest_polynom.degree(self.x) > 0:
                            weg += "### Lösung des Restpolynoms\n\n"
                            weg += f"Das Restpolynom {latex(rest_polynom)} hat die Nullstellen:\n\n"

                            rest_lösungen = solve(rest_polynom, self.x)
                            for i, lösung in enumerate(rest_lösungen, 1):
                                if lösung.is_real:
                                    weg += f"- x_{i} = {lösung}\n"
                                else:
                                    weg += f"- x_{i} = {lösung} (komplex)\n"

                # Allgemeine Lösung mit SymPy
                weg += "### Allgemeine Lösung\n\n"
                weg += f"$$f(x) = {self.term_latex()} = 0$$\n\n"

                alle_nullstellen = self.nullstellen(real=False, exakt=True)
                weg += "Die Nullstellen sind:\n\n"

                for i, nullstelle in enumerate(alle_nullstellen, 1):
                    if hasattr(nullstelle, "is_real") and nullstelle.is_real:
                        weg += f"- x_{i} = {nullstelle}\n"
                    else:
                        weg += f"- x_{i} = {nullstelle} (komplex)\n"

        elif grad >= 4:
            weg += f"## Polynom höheren Grades (Grad {grad})\n\n"

            # Zuerst versuchen, rationale Nullstellen zu finden
            rationale_nullstellen = self._rationale_nullstellen()

            if rationale_nullstellen:
                weg += "### Rational Root Theorem\n\n"
                weg += "Für rationale Nullstellen p/q gilt:\n"
                weg += "- p ist Teiler des absoluten Glieds (a₀)\n"
                weg += "- q ist Teiler des Leitkoeffizienten (aₙ)\n\n"

                a0 = self.koeffizienten[0]
                an = self.koeffizienten[-1]
                weg += f"Mit a₀ = {a0} und aₙ = {an}:\n\n"

                weg += "Mögliche rationale Nullstellen: "

                # Zeige mögliche Kandidaten
                def finde_teiler_einfach(zahl):
                    if isinstance(zahl, Rational):
                        zaehler = abs(int(zahl.p))
                        nenner = abs(int(zahl.q))
                        teiler_zaehler = [
                            t for t in range(1, zaehler + 1) if zaehler % t == 0
                        ]
                        teiler_nenner = [
                            t for t in range(1, nenner + 1) if nenner % t == 0
                        ]
                        return teiler_zaehler, teiler_nenner
                    else:
                        return [
                            t
                            for t in range(1, abs(int(zahl)) + 1)
                            if int(zahl) % t == 0
                        ], [1]

                if isinstance(a0, Rational):
                    teiler_p_zaehler, teiler_p_nenner = finde_teiler_einfach(a0)
                    teiler_p = [
                        f"±{p_z}/{p_n}"
                        for p_z in teiler_p_zaehler
                        for p_n in teiler_p_nenner
                    ]
                else:
                    teiler_p_zaehler, _ = finde_teiler_einfach(a0)
                    teiler_p = [f"±{t}" for t in teiler_p_zaehler]

                if isinstance(an, Rational):
                    teiler_q_zaehler, teiler_q_nenner = finde_teiler_einfach(an)
                else:
                    teiler_q_zaehler, _ = finde_teiler_einfach(an)

                weg += (
                    ", ".join(sorted(teiler_p[:5])) + "..."
                    if len(teiler_p) > 5
                    else ", ".join(teiler_p)
                )
                weg += "\n\n"

                weg += "### Gefundene rationale Nullstellen\n\n"
                for nullstelle in rationale_nullstellen:
                    weg += f"- x = {nullstelle}\n"
                weg += "\n"

                # Faktorisierung zeigen
                linearfaktoren, rest_polynom = self._faktorisiere()

                if linearfaktoren:
                    weg += "### Faktorisierung\n\n"
                    weg += "Das Polynom lässt sich faktorisieren als:\n\n"

                    faktor_darstellung = ""
                    for faktor in linearfaktoren:
                        if faktor_darstellung:
                            faktor_darstellung += " · "
                        faktor_darstellung += f"({latex(faktor)})"

                    if rest_polynom != 1:
                        faktor_darstellung += f" · {latex(rest_polynom)}"

                    weg += f"$$f(x) = {faktor_darstellung}$$\n\n"

                    # Restpolynom lösen
                    if rest_polynom != 1 and rest_polynom.degree(self.x) > 0:
                        weg += "### Lösung des Restpolynoms\n\n"
                        weg += f"Das Restpolynom {latex(rest_polynom)} hat die Nullstellen:\n\n"

                        rest_lösungen = solve(rest_polynom, self.x)
                        for i, lösung in enumerate(rest_lösungen, 1):
                            if lösung.is_real:
                                weg += f"- x_{i} = {lösung}\n"
                            else:
                                weg += f"- x_{i} = {lösung} (komplex)\n"
                else:
                    weg += "### Keine Faktorisierung möglich\n\n"
                    weg += "Das Polynom lässt sich nicht mit rationalen Koeffizienten faktorisieren.\n\n"

            # Allgemeine Lösung mit SymPy
            weg += "### Allgemeine Lösung\n\n"
            weg += f"$$f(x) = {self.term_latex()} = 0$$\n\n"

            alle_nullstellen = self.nullstellen(real=False, exakt=True)
            weg += "Die Nullstellen sind:\n\n"

            for i, nullstelle in enumerate(alle_nullstellen, 1):
                if hasattr(nullstelle, "is_real") and nullstelle.is_real:
                    weg += f"- x_{i} = {nullstelle}\n"
                else:
                    weg += f"- x_{i} = {nullstelle} (komplex)\n"

        return weg

    # ============================================
    # 🔥 PLOTLY VISUALISIERUNGSMETHODEN 🔥
    # ============================================

    def plotly(
        self,
        x_range: tuple = (-10, 10),
        punkte: int = 200,
        zeige_nullstellen: bool = True,
        zeige_extremstellen: bool = True,
        zeige_wendepunkte: bool = True,
        titel: str = None,
        farbe: str = "blue",
        marimo_mode: bool = False,
    ) -> Any:
        """
        Erzeugt eine verbesserte Plotly-Visualisierung der ganzrationalen Funktion.

        Args:
            x_range: Tupel (xmin, xmax) für den x-Bereich
            punkte: Anzahl der zu berechnenden Punkte
            zeige_nullstellen: Ob Nullstellen markiert werden sollen
            zeige_extremstellen: Ob Extremstellen markiert werden sollen
            zeige_wendepunkte: Ob Wendepunkte markiert werden sollen
            titel: Benutzerdefinierter Titel
            farbe: Farbe der Hauptkurve
            marimo_mode: Wenn True, gibt mo.ui.plotly zurück

        Returns:
            Plotly Figure-Objekt oder mo.ui.plotly
        """
        xmin, xmax = x_range

        # Erstelle x-Werte für die Berechnung
        x_werte = np.linspace(xmin, xmax, punkte)
        y_werte = [self.wert(xi) for xi in x_werte]

        # Erstelle die Figur
        fig = go.Figure()

        # Hauptkurve
        fig.add_trace(
            go.Scatter(
                x=x_werte,
                y=y_werte,
                mode="lines",
                name=f"f(x) = {self.term()}",
                line=config.get_line_config(color_key=farbe),
                hovertemplate="<b>x</b>: %{x:.3f}<br><b>f(x)</b>: %{y:.3f}<extra></extra>",
            )
        )

        # Füge Nullstellen hinzu
        if zeige_nullstellen:
            nullstellen = self.nullstellen()
            for ns in nullstellen:
                try:
                    x_ns = float(ns)
                    if xmin <= x_ns <= xmax:
                        fig.add_trace(
                            go.Scatter(
                                x=[x_ns],
                                y=[0],
                                mode="markers",
                                name=f"Nullstelle x={x_ns:.3f}",
                                marker=config.get_marker_config(
                                    color_key="secondary", size=10
                                ),
                                showlegend=False,
                                hovertemplate=f"<b>Nullstelle</b><br>x: {x_ns:.3f}<br>f(x): 0<extra></extra>",
                            )
                        )
                except (ValueError, TypeError):
                    continue

        # Füge Extremstellen hinzu
        if zeige_extremstellen:
            extremstellen = self.extremstellen()
            for xs, art in extremstellen:
                try:
                    x_es = float(xs)
                    y_es = self.wert(x_es)
                    if xmin <= x_es <= xmax:
                        color = "green" if art == "Maximum" else "orange"
                        fig.add_trace(
                            go.Scatter(
                                x=[x_es],
                                y=[y_es],
                                mode="markers",
                                name=f"{art} ({x_es:.3f}|{y_es:.3f})",
                                marker=config.get_marker_config(
                                    color_key=color, size=12
                                ),
                                showlegend=False,
                                hovertemplate=f"<b>{art}</b><br>x: {x_es:.3f}<br>f(x): {y_es:.3f}<extra></extra>",
                            )
                        )
                except (ValueError, TypeError):
                    continue

        # Füge Wendepunkte hinzu
        if zeige_wendepunkte:
            wendepunkte = self.wendepunkte()
            for x_ws, y_ws, art in wendepunkte:
                try:
                    x_ws_float = float(x_ws)
                    y_ws_float = float(y_ws)
                    if xmin <= x_ws_float <= xmax:
                        fig.add_trace(
                            go.Scatter(
                                x=[x_ws_float],
                                y=[y_ws_float],
                                mode="markers",
                                name=f"Wendepunkt ({x_ws_float:.3f}|{y_ws_float:.3f})",
                                marker=config.get_marker_config(
                                    color_key="tertiary", size=10
                                ),
                                showlegend=False,
                                hovertemplate=f"<b>Wendepunkt</b><br>x: {x_ws_float:.3f}<br>f(x): {y_ws_float:.3f}<br>Krümmung: {art}<extra></extra>",
                            )
                        )
                except (ValueError, TypeError):
                    continue

        # Layout-Optionen mit improved Konfiguration
        fig.update_layout(
            **config.get_plot_config(),
            title=titel or f"Ganzrationale Funktion: f(x) = {self.term()}",
            xaxis={
                **config.get_axis_config(mathematical_mode=True),
                "range": x_range,
                "title": "x",
            },
            yaxis={
                **config.get_axis_config(mathematical_mode=False),
                "title": "f(x)",
            },
            showlegend=True,
            hovermode="x unified",
        )

        return mo.ui.plotly(fig) if marimo_mode else fig

    def zeige_funktion_plotly(self, x_range: tuple = None, punkte: int = 200) -> Any:
        """Zeigt interaktiven Funktionsgraph mit Plotly - MATHEMATISCH KORREKT"""
        if x_range is None:
            x_range = config.DEFAULT_PLOT_RANGE

        x = np.linspace(x_range[0], x_range[1], punkte)
        y = [self.wert(xi) for xi in x]

        fig = px.line(
            x=x,
            y=y,
            title=f"Funktionsgraph: f(x) = {self.term()}",
            labels={"x": "x", "y": f"f(x) = {self.term()}"},
        )

        # 🔥 PERFECT MATHEMATICAL CONFIGURATION 🔥
        fig.update_layout(
            **config.get_plot_config(),
            xaxis={
                **config.get_axis_config(mathematical_mode=True),
                "range": x_range,
                "title": "x",
            },
            yaxis={
                **config.get_axis_config(mathematical_mode=False),
                "title": f"f(x) = {self.term()}",
            },
            showlegend=False,
        )

        return mo.ui.plotly(fig)

    def __str__(self) -> str:
        """String-Darstellung der Funktion"""
        return str(self.term_sympy)

    def __repr__(self) -> str:
        """Repräsentation der Funktion"""
        return str(self.term_sympy)

    def _repr_latex_(self) -> str:
        """LaTeX-Darstellung für Jupyter/Marimo Notebooks"""
        return self.term_sympy._repr_latex_()

    def __eq__(self, other) -> bool:
        """Vergleich zweier Funktionen auf Gleichheit"""
        if not isinstance(other, GanzrationaleFunktion):
            return False
        return self.term_sympy.equals(other.term_sympy)

    def _create_from_operation(self, sympy_expr: sp.Basic) -> "GanzrationaleFunktion":
        """
        Factory-Methode zur Erstellung einer neuen Funktion aus einem SymPy-Ausdruck.
        Führt Validierung durch und stellt sicher, dass das Ergebnis ein Polynom ist.
        """
        # Ausdruck expandieren für Standardform
        expanded_expr = sp.expand(sympy_expr)

        # Validiere, dass Ergebnis ein Polynom ist
        if not expanded_expr.is_polynomial(self.x):
            raise TypeError("Ergebnis ist keine ganzrationale Funktion")

        # Erstelle neue Instanz mit dem validierten Ausdruck
        return GanzrationaleFunktion(expanded_expr)

    def __add__(self, other) -> "GanzrationaleFunktion":
        """Addition: f + g"""
        if isinstance(other, GanzrationaleFunktion):
            result_sympy = self.term_sympy + other.term_sympy
        elif isinstance(other, (int, float, Rational)):
            result_sympy = self.term_sympy + other
        else:
            return NotImplemented

        return self._create_from_operation(result_sympy)

    def __radd__(self, other) -> "GanzrationaleFunktion":
        """Rechtsseitige Addition: z + f"""
        return self.__add__(other)

    def __sub__(self, other) -> "GanzrationaleFunktion":
        """Subtraktion: f - g"""
        if isinstance(other, GanzrationaleFunktion):
            result_sympy = self.term_sympy - other.term_sympy
        elif isinstance(other, (int, float, Rational)):
            result_sympy = self.term_sympy - other
        else:
            return NotImplemented

        return self._create_from_operation(result_sympy)

    def __rsub__(self, other) -> "GanzrationaleFunktion":
        """Rechtsseitige Subtraktion: z - f"""
        if isinstance(other, (int, float, Rational)):
            result_sympy = other - self.term_sympy
            return self._create_from_operation(result_sympy)
        return NotImplemented

    def __mul__(self, other) -> "GanzrationaleFunktion":
        """Multiplikation: f * g"""
        if isinstance(other, GanzrationaleFunktion):
            result_sympy = self.term_sympy * other.term_sympy
        elif isinstance(other, (int, float, Rational)):
            result_sympy = self.term_sympy * other
        else:
            return NotImplemented

        return self._create_from_operation(result_sympy)

    def __rmul__(self, other) -> "GanzrationaleFunktion":
        """Rechtsseitige Multiplikation: z * f"""
        return self.__mul__(other)

    def __truediv__(
        self, other
    ) -> Union["GanzrationaleFunktion", "GebrochenRationaleFunktion"]:
        """Division: f / g"""
        from .gebrochen_rationale import GebrochenRationaleFunktion

        if isinstance(other, GanzrationaleFunktion):
            if other.term_sympy == 0:
                raise ZeroDivisionError("Division durch Nullfunktion")

            # Wenn Ergebnis ein Polynom ist, gib ganzrationale Funktion zurück
            result_sympy = self.term_sympy / other.term_sympy
            result_sympy_simplified = sp.simplify(result_sympy)

            if result_sympy_simplified.is_polynomial(self.x):
                return GanzrationaleFunktion(result_sympy_simplified)
            else:
                # Ansonsten gib gebrochen-rationale Funktion zurück
                return GebrochenRationaleFunktion(self, other)

        elif isinstance(other, (int, float, Rational)):
            if other == 0:
                raise ZeroDivisionError("Division durch Null")

            result_sympy = self.term_sympy / other
            return self._create_from_operation(result_sympy)
        else:
            return NotImplemented

    def __rtruediv__(self, other) -> "GanzrationaleFunktion":
        """Rechtsseitige Division: z / f"""
        if isinstance(other, (int, float, Rational)):
            if self.term_sympy == 0:
                raise ZeroDivisionError("Division durch Nullfunktion")

            result_sympy = other / self.term_sympy
            return self._create_from_operation(result_sympy)
        else:
            return NotImplemented

    def __pow__(self, other) -> "GanzrationaleFunktion":
        """Potenzierung: f ** n"""
        if isinstance(other, int) and other >= 0:
            if other == 0:
                return GanzrationaleFunktion("1")
            result_sympy = self.term_sympy**other
            return self._create_from_operation(result_sympy)
        else:
            return NotImplemented

    # --- In-place Operationen ---

    def __iadd__(self, other) -> "GanzrationaleFunktion":
        """In-place Addition: f += g"""
        result = self + other
        self.term_sympy = result.term_sympy
        return self

    def __isub__(self, other) -> "GanzrationaleFunktion":
        """In-place Subtraktion: f -= g"""
        result = self - other
        self.term_sympy = result.term_sympy
        return self

    def __imul__(self, other) -> "GanzrationaleFunktion":
        """In-place Multiplikation: f *= g"""
        result = self * other
        self.term_sympy = result.term_sympy
        return self

    def __itruediv__(self, other) -> "GanzrationaleFunktion":
        """In-place Division: f /= g"""
        result = self / other
        self.term_sympy = result.term_sympy
        return self

    # --- Unäre Operationen ---

    def __neg__(self) -> "GanzrationaleFunktion":
        """Negation: -f"""
        result_sympy = -self.term_sympy
        return self._create_from_operation(result_sympy)

    def __pos__(self) -> "GanzrationaleFunktion":
        """Positiv: +f"""
        return self._create_from_operation(self.term_sympy)

    def perfekte_parabel_plotly(
        self, x_range: tuple = (-5, 5), punkte: int = 200
    ) -> Any:
        """PERFEKTE Parabel-Darstellung entsprechend Schul-Konventionen"""
        # Perfekte symmetrische Datenpunkte um den Scheitelpunkt
        x = np.linspace(x_range[0], x_range[1], punkte)
        y = [self.wert(xi) for xi in x]

        fig = go.Figure()

        # Hauptkurve
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=f"f(x) = {self.term()}",
                line={"color": "blue", "width": 3},
            )
        )

        # Scheitelpunkt berechnen und markieren
        try:
            # Für quadratische Funktionen: Scheitelpunkt bei x = -b/(2a)
            if len(self.koeffizienten) >= 3:
                a, b = self.koeffizienten[0], self.koeffizienten[1]
                s_x = -b / (2 * a)
                s_y = self.wert(s_x)

                fig.add_trace(
                    go.Scatter(
                        x=[s_x],
                        y=[s_y],
                        mode="markers",
                        name="Scheitelpunkt",
                        marker={"size": 15, "color": "red", "symbol": "diamond"},
                        text=[f"S({s_x:.2f}|{s_y:.2f})"],
                        hovertemplate="%{text}<extra></extra>",
                    )
                )
        except Exception:
            pass

        # 🔥 ABSOLUT PERFEKTE MATHEMATISCHE KONFIGURATION 🔥
        fig.update_layout(
            title=f"Parabel: f(x) = {self.term()}",
            xaxis={
                "scaleanchor": "y",  # 🔥 1:1 Aspect Ratio - KEINE VERZERRUNG!
                "scaleratio": 1,  # 🔥 Perfekte Kreisverwandtschaft!
                "zeroline": True,  # 🔥 Achse im Ursprung sichtbar
                "zerolinewidth": 2,  # 🔥 Deutliche Null-Linie
                "zerolinecolor": "black",  # 🔥 Schwarze Achse
                "showgrid": True,  # 🔥 Gitterlinien helfen beim Ablesen
                "gridwidth": 1,  # 🔥 Dünne Gitterlinien
                "gridcolor": "lightgray",  # 🔥 Dezentes Gitter
                "range": x_range,  # 🔥 Symmetrischer Bereich
                "title": "x",  # 🔥 Achsenbeschriftung
                "ticks": "outside",  # 🔥 Ticks außerhalb
                "tickwidth": 2,  # 🔥 Deutliche Ticks
                "showline": True,  # 🔥 Achsenlinie sichtbar
                "linewidth": 2,  # 🔥 Deutliche Achsenlinie
            },
            yaxis={
                "zeroline": True,
                "zerolinewidth": 2,
                "zerolinecolor": "black",
                "showgrid": True,
                "gridwidth": 1,
                "gridcolor": "lightgray",
                "title": f"f(x) = {self.term()}",
                "ticks": "outside",
                "tickwidth": 2,
                "showline": True,
                "linewidth": 2,
                "scaleanchor": "x",  # 🔥 Bidirektionale Verzerrungs-Verhinderung!
            },
            plot_bgcolor="white",  # 🔥 Weißer Hintergrund für Schule
            paper_bgcolor="white",
            showlegend=True,
            width=700,
            height=500,
            font={"size": 14},  # 🔥 Gute Lesbarkeit
        )

        return mo.ui.plotly(fig)

    def zeige_nullstellen_plotly(
        self, real: bool = True, x_range: tuple = (-10, 10)
    ) -> Any:
        """Zeigt Funktion mit interaktiven Nullstellen-Markierungen - MATHEMATISCH KORREKT"""
        # Hauptfunktion
        x = np.linspace(x_range[0], x_range[1], 300)
        y = [self.wert(xi) for xi in x]

        # Plotly Figure erstellen
        fig = go.Figure()

        # Hauptfunktion hinzufügen
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=f"f(x) = {self.term()}",
                line={"color": "blue", "width": 2},
            )
        )

        # Nullstellen hinzufügen
        nullstellen = self.nullstellen(real)
        if nullstellen:
            ns_x = [ns for ns in nullstellen if x_range[0] <= ns <= x_range[1]]
            ns_y = [0] * len(ns_x)
            ns_labels = [f"Nullstelle: {ns:.2f}" for ns in ns_x]

            fig.add_trace(
                go.Scatter(
                    x=ns_x,
                    y=ns_y,
                    mode="markers",
                    name="Nullstellen",
                    marker={"size": 12, "color": "red", "symbol": "circle"},
                    text=ns_labels,
                    hovertemplate="%{text}<extra></extra>",
                )
            )

            title = f"Nullstellen von f(x) = {self.term()}"
        else:
            title = f"Keine reellen Nullstellen für f(x) = {self.term()}"

        # 🔥 PERFECT MATHEMATICAL CONFIGURATION 🔥
        fig.update_layout(
            title=title,
            xaxis={
                "scaleanchor": "y",  # 1:1 Aspect Ratio
                "scaleratio": 1,  # Keine Verzerrung!
                "zeroline": True,  # Achse im Ursprung
                "showgrid": True,  # Gitterlinien
                "range": x_range,
                "title": "x",
            },
            yaxis={
                "zeroline": True,
                "showgrid": True,
                "title": f"f(x) = {self.term()}",
            },
            showlegend=True,
            width=600,
            height=400,
        )

        return mo.ui.plotly(fig)

    def zeige_ableitung_plotly(
        self, ordnung: int = 1, x_range: tuple = (-10, 10)
    ) -> Any:
        """Zeigt Funktion und Ableitung im Vergleich - MATHEMATISCH KORREKT"""
        # Daten generieren
        x = np.linspace(x_range[0], x_range[1], 300)

        # Originalfunktion
        y_orig = [self.wert(xi) for xi in x]

        # Ableitung
        ableitung = self.ableitung(ordnung)
        y_abl = [ableitung.wert(xi) for xi in x]

        # Plotly Subplots
        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=[
                f"f(x) = {self.term()}",
                f"f^{ordnung}(x) = {ableitung.term()}",
            ],
            vertical_spacing=0.1,
        )

        # Originalfunktion
        fig.add_trace(
            go.Scatter(
                x=x, y=y_orig, mode="lines", name="f(x)", line={"color": "blue"}
            ),
            row=1,
            col=1,
        )

        # Ableitung
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y_abl,
                mode="lines",
                name=f"f^{ordnung}(x)",
                line={"color": "red"},
            ),
            row=2,
            col=1,
        )

        # 🔥 PERFECT MATHEMATICAL CONFIGURATION 🔥
        fig.update_layout(
            title=f"Funktion vs. {ordnung}. Ableitung",
            height=600,
            showlegend=False,
            xaxis={
                "scaleanchor": "y",  # 1:1 Aspect Ratio
                "scaleratio": 1,  # Keine Verzerrung!
                "zeroline": True,
                "showgrid": True,
                "range": x_range,
                "title": "x",
            },
            xaxis2={
                "scaleanchor": "y2",  # 1:1 Aspect Ratio für zweite Achse
                "scaleratio": 1,
                "zeroline": True,
                "showgrid": True,
                "range": x_range,
                "title": "x",
            },
            yaxis={"zeroline": True, "showgrid": True, "title": "f(x)"},
            yaxis2={"zeroline": True, "showgrid": True, "title": f"f^{ordnung}(x)"},
        )

        return mo.ui.plotly(fig)
