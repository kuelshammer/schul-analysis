"""
Trigonometrische Funktionen für das Schul-Analysis Framework.

Einfache Implementierung für trigonometrische Funktionen wie sin(x), cos(x), etc.
"""

from typing import Union

import sympy as sp
from sympy import diff, latex, solve

from .funktion import Funktion
from .sympy_types import VALIDATION_EXACT, validate_function_result


class TrigonometrischeFunktion(Funktion):
    """
    Pädagogischer Wrapper für trigonometrische Funktionen.

    Beispiele:
    - sin(x)
    - cos(2x) + sin(x)
    - tan(x/2)
    """

    def __init__(self, eingabe: Union[str, sp.Basic, "Funktion"]):
        """
        Konstruktor für trigonometrische Funktionen.

        Args:
            eingabe: String, SymPy-Ausdruck oder Funktion-Objekt
        """
        # 🔥 PÄDAGOGISCHER WRAPPER - Keine komplexe Logik mehr! 🔥

        # Speichere die ursprüngliche Eingabe für Validierung
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
        if not self.ist_trigonometrisch:
            raise TypeError(
                f"Die Eingabe '{self.original_eingabe}' ist keine trigonometrische Funktion! "
                "Eine trigonometrische Funktion muss sin(x), cos(x), tan(x) oder ähnliche Funktionen enthalten. "
                "Hast du vielleicht eine ganzrationale, gebrochen-rationale oder exponentiale Funktion gemeint?"
            )

        # 🔥 CACHE für wiederholte Berechnungen
        self._cache = {}

    def nullstellen(self, real: bool = True, runden=None) -> list[sp.Basic]:
        """
        Berechnet die Nullstellen der trigonometrischen Funktion.

        Args:
            real: Nur reelle Nullstellen zurückgeben
            runden: Anzahl Nachkommastellen für Rundung

        Returns:
            Liste der Nullstellen
        """
        # 🔥 UNIFIED ARCHITECTURE: Verwende Basis-Klassen-Properties 🔥
        try:
            # Verwende SymPy's solve für die Gleichung
            lösungen = solve(self.term_sympy, self._variable_symbol)

            nullstellen_liste = []
            for lösung in lösungen:
                if real and lösung.is_real is False:
                    continue

                if runden is not None and lösung.is_real:
                    nullstellen_liste.append(round(float(lösung), runden))
                else:
                    nullstellen_liste.append(lösung)

            return nullstellen_liste

        except (AttributeError, TypeError, ValueError) as e:
            # Für komplexe trigonometrische Funktionen: leere Liste zurückgeben
            # Logge den Fehler für Debugging-Zwecke
            import logging

            logging.debug(
                f"Nullstellen-Berechnung fehlgeschlagen für {self.term()}: {e}"
            )
            return []

    def ableitung(self, ordnung: int = 1) -> "TrigonometrischeFunktion":
        """
        Berechnet die Ableitung gegebener Ordnung.

        Args:
            ordnung: Ordnung der Ableitung (Standard: 1)

        Returns:
            Neue TrigonometrischeFunktion mit der abgeleiteten Funktion
        """
        # 🔥 UNIFIED ARCHITECTURE: Verwende Basis-Klassen-Properties 🔥
        abgeleitet = diff(self.term_sympy, self._variable_symbol, ordnung)
        # Validiere das Ergebnis für exakte Berechnungen
        validate_function_result(abgeleitet, VALIDATION_EXACT)
        return TrigonometrischeFunktion(abgeleitet)

    def term(self) -> str:
        """Gibt den Term als String zurück."""
        # 🔥 UNIFIED ARCHITECTURE: Verwende Basis-Klassen-Funktionalität 🔥
        return super().term()

    def term_latex(self) -> str:
        """Gibt den Term als LaTeX-String zurück."""
        return latex(self.term_sympy)

    def periodenlaenge(self) -> float:
        """
        Berechnet die Periodenlänge für einfache trigonometrische Funktionen.

        Returns:
            Periodenlänge als float (oder None wenn nicht bestimmbar)
        """
        try:
            # Einfache Heuristik für grundlegende Funktionen
            term_str = str(self.term_sympy)

            if "sin(" in term_str or "cos(" in term_str:
                # Suche nach Koeffizienten vor x
                import re

                pattern = r"sin\(([^)]+)\)|cos\(([^)]+)\)"
                matches = re.findall(pattern, term_str)

                if matches:
                    for match in matches:
                        arg = match[0] if match[0] else match[1]
                        if "x" in arg:
                            # Finde den Koeffizienten von x
                            coeff_pattern = r"([+-]?\d*\.?\d*)\s*\*?\s*x"
                            coeff_match = re.search(coeff_pattern, arg)
                            if coeff_match:
                                coeff_str = coeff_match.group(1)
                                if (
                                    not coeff_str
                                    or coeff_str == "+"
                                    or coeff_str == "-"
                                ):
                                    coeff = 1.0 if coeff_str != "-" else -1.0
                                else:
                                    coeff = float(coeff_str)

                                if coeff != 0:
                                    return 2 * abs(3.14159265359 / coeff)

            # Standardperiodenlänge für sin(x), cos(x)
            if term_str in ["sin(x)", "cos(x)"]:
                return 2 * 3.14159265359

            return 0.0  # type: ignore

        except (AttributeError, ValueError, TypeError) as e:
            # Logge den Fehler für Debugging-Zwecke
            import logging

            logging.debug(
                f"Periodenlängen-Berechnung fehlgeschlagen für {self.term()}: {e}"
            )
            return 0.0  # type: ignore

    def __str__(self):
        """String-Repräsentation."""
        return self.term()

    def __repr__(self):
        """Repräsentation für Debugging."""
        return f"TrigonometrischeFunktion('{self.original_eingabe}')"
