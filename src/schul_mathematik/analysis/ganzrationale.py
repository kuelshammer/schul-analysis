"""
Ganzrationale Funktionen (Polynome) für das Schul-Analysis Framework.

Pädagogischer Wrapper mit spezialisierten Methoden für lineare und quadratische Funktionen.
"""

import sympy as sp

from .funktion import Funktion


class GanzrationaleFunktion(Funktion):
    """
    Pädagogischer Wrapper für ganzrationale Funktionen (Polynome).

    Diese Klasse bietet eine spezialisierte Schnittstelle für Polynome
    mit deutschen Fehlermeldungen und typspezifischen Methoden.

    Examples:
        >>> f = GanzrationaleFunktion("x^2 - 4x + 3")
        >>> g = GanzrationaleFunktion([1, -4, 3])  # x² - 4x + 3
        >>> h = GanzrationaleFunktion({2: 1, 1: -4, 0: 3})  # x² - 4x + 3
    """

    def __init__(
        self,
        eingabe: str | list[float] | dict[int, float] | sp.Basic,
        variable: str | None = None,
        parameter: list[str] | None = None,
    ):
        """
        Konstruktor für ganzrationale Funktionen.

        Args:
            eingabe: String ("x^3-2x+1"), Liste ([1, 0, -2, 1]), Dictionary ({3: 1, 1: -2, 0: 1}) oder SymPy-Ausdruck
            variable: Optional expliziter Variablenname (überschreibt automatische Erkennung)
            parameter: Optionale Liste von Parameternamen (überschreibt automatische Erkennung)
        """
        # 🔥 PÄDAGOGISCHER WRAPPER - Konvertiere verschiedene Eingabeformate 🔥

        # Speichere Original-Eingabe für deutsche Fehlermeldungen
        self.original_eingabe = str(eingabe)

        # Konvertiere verschiedene Eingabeformate zu String für die Basisklasse
        if isinstance(eingabe, (list, dict)):
            eingabe_str = self._konvertiere_eingabe_zu_string(eingabe)
            super().__init__(eingabe_str)
        else:
            super().__init__(eingabe)

        # 🔥 PÄDAGOGISCHE VALIDIERUNG mit deutscher Fehlermeldung 🔥
        if not self.ist_ganzrational:
            raise TypeError(
                f"Die Eingabe '{self.original_eingabe}' ist keine ganzrationale Funktion! "
                "Eine ganzrationale Funktion muss ein Polynom sein (nur Summen von x^n Termen). "
                "Hast du vielleicht eine gebrochen-rationale, exponentiale oder trigonometrische Funktion gemeint?"
            )

        # 🔥 SPEZIFISCHE ATTRIBUTE für ganzrationale Funktionen 🔥
        self.koeffizienten = self._extrahiere_koeffizienten()

    def _konvertiere_eingabe_zu_string(self, eingabe: list | dict) -> str:
        """Konvertiert Listen- oder Dictionary-Eingabe zu String"""
        if isinstance(eingabe, list):
            return self._liste_zu_string(eingabe)
        elif isinstance(eingabe, dict):
            return self._dict_zu_string(eingabe)
        else:
            raise TypeError("Eingabe muss Liste oder Dictionary sein")

    def _liste_zu_string(self, koeffizienten: list[float]) -> str:
        """Konvertiert Koeffizienten-Liste zu String-Repräsentation"""
        terme = []
        for i, koeff in enumerate(reversed(koeffizienten)):
            if koeff == 0:
                continue
            grad = len(koeffizienten) - 1 - i
            if grad == 0:
                terme.append(str(koeff))
            elif grad == 1:
                if koeff == 1:
                    terme.append("x")
                elif koeff == -1:
                    terme.append("-x")
                else:
                    terme.append(f"{koeff}x")
            else:
                if koeff == 1:
                    terme.append(f"x^{grad}")
                elif koeff == -1:
                    terme.append(f"-x^{grad}")
                else:
                    terme.append(f"{koeff}x^{grad}")

        if not terme:
            return "0"

        # Ersten Term ohne Vorzeichen, Rest mit Vorzeichen
        ergebnis = terme[0]
        for term in terme[1:]:
            if term.startswith("-"):
                ergebnis += f" - {term[1:]}"
            else:
                ergebnis += f" + {term}"

        return ergebnis

    def _dict_zu_string(self, koeffizienten: dict[int, float]) -> str:
        """Konvertiert Koeffizienten-Dictionary zu String-Repräsentation"""
        # Konvertiere zu Liste und verwende vorhandene Methode
        max_grad = max(koeffizienten.keys()) if koeffizienten else 0
        liste = [0.0] * (max_grad + 1)
        for grad, koeff in koeffizienten.items():
            liste[grad] = koeff
        return self._liste_zu_string(liste)

    def _extrahiere_koeffizienten(self) -> list[sp.Basic]:
        """Extrahiert Koeffizienten aus SymPy-Ausdruck"""
        try:
            poly = sp.Poly(self.term_sympy, self._variable_symbol)
            coeffs = poly.all_coeffs()
            coeffs.reverse()
            return coeffs
        except Exception:
            return []

    def __str__(self):
        return self.term()

    def __repr__(self):
        return f"GanzrationaleFunktion('{self.term()}')"
