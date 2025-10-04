"""
Trigonometrische Funktionen für das Schul-Analysis Framework.

Einfache Implementierung für trigonometrische Funktionen wie sin(x), cos(x), etc.
"""

from typing import Union

import sympy as sp
from sympy import diff, latex, solve, symbols

from .funktion import Funktion


class TrigonometrischeFunktion(Funktion):
    """
    Repräsentiert trigonometrische Funktionen.

    Beispiele:
    - sin(x)
    - cos(2x) + sin(x)
    - tan(x/2)
    """

    def __init__(self, eingabe: Union[str, sp.Basic, "TrigonometrischeFunktion"]):
        """
        Konstruktor für trigonometrische Funktionen.

        Args:
            eingabe: String, SymPy-Ausdruck oder bestehendes TrigonometrischeFunktion-Objekt
        """
        # Speichere die ursprüngliche Eingabe
        self.original_eingabe = str(eingabe)

        # Parse zu SymPy-Ausdruck
        if isinstance(eingabe, str):
            from sympy.parsing.sympy_parser import (
                implicit_multiplication_application,
                parse_expr,
                standard_transformations,
            )

            transformations = standard_transformations + (
                implicit_multiplication_application,
            )
            self.term_sympy = parse_expr(
                eingabe.replace("^", "**"), transformations=transformations
            )
        elif isinstance(eingabe, sp.Basic):
            self.term_sympy = eingabe
        elif isinstance(eingabe, TrigonometrischeFunktion):
            # Kopie
            self.term_sympy = eingabe.term_sympy
        else:
            raise TypeError(
                "Eingabe muss String, SymPy-Ausdruck oder TrigonometrischeFunktion sein"
            )

        # Bestimme die Hauptvariable
        self.x = self._erkenne_hauptvariable()

        # Erstelle lesbaren Term-String
        self.term_str = self._erstelle_term_string()

    def _erkenne_hauptvariable(self) -> sp.Symbol:
        """Erkennt die Hauptvariable im Ausdruck."""
        alle_symbole = self.term_sympy.free_symbols

        if not alle_symbole:
            return symbols("x")  # Fallback für konstante Funktionen

        # Prioritäten: x > t > y > z > andere
        for symbol_name in ["x", "t", "y", "z"]:
            for symbol in alle_symbole:
                if str(symbol) == symbol_name:
                    return symbol

        # Fallback: erstes Symbol
        return list(alle_symbole)[0]

    def _erstelle_term_string(self) -> str:
        """Erstellt einen lesbaren Term-String."""
        return str(self.term_sympy).replace("**", "^").replace("*", "")

    def wert(self, x_wert: float) -> float:
        """
        Berechnet den Funktionswert an einer Stelle.

        Args:
            x_wert: x-Wert an dem ausgewertet werden soll

        Returns:
            Funktionswert als float
        """
        try:
            return float(self.term_sympy.subs(self.x, x_wert))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Fehler bei der Werteberechnung bei x={x_wert}: {e}")

    def nullstellen(self, real: bool = True, runden=None) -> list[sp.Basic]:
        """
        Berechnet die Nullstellen der trigonometrischen Funktion.

        Args:
            real: Nur reelle Nullstellen zurückgeben
            runden: Anzahl Nachkommastellen für Rundung

        Returns:
            Liste der Nullstellen
        """
        try:
            # Verwende SymPy's solve für die Gleichung
            lösungen = solve(self.term_sympy, self.x)

            nullstellen_liste = []
            for lösung in lösungen:
                if real and lösung.is_real is False:
                    continue

                if runden is not None and lösung.is_real:
                    nullstellen_liste.append(round(float(lösung), runden))
                else:
                    nullstellen_liste.append(lösung)

            return nullstellen_liste

        except Exception:
            # Für komplexe trigonometrische Funktionen: leere Liste zurückgeben
            return []

    def ableitung(self, ordnung: int = 1) -> "TrigonometrischeFunktion":
        """
        Berechnet die Ableitung gegebener Ordnung.

        Args:
            ordnung: Ordnung der Ableitung (Standard: 1)

        Returns:
            Neue TrigonometrischeFunktion mit der abgeleiteten Funktion
        """
        abgeleitet = diff(self.term_sympy, self.x, ordnung)
        return TrigonometrischeFunktion(abgeleitet)

    def term(self) -> str:
        """Gibt den Term als String zurück."""
        return self.term_str

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

            return None

        except Exception:
            return None

    def __str__(self):
        """String-Repräsentation."""
        return self.term()

    def __repr__(self):
        """Repräsentation für Debugging."""
        return f"TrigonometrischeFunktion('{self.original_eingabe}')"
