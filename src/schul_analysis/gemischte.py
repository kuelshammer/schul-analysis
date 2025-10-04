"""
Gemischte Funktionen für das Schul-Analysis Framework.

Unterstützt komplexe Ausdrücke mit mehreren Funktionstypen wie (x^2+1)sin(x)
oder exp(-x)(x^3+1). Kombiniert die Power von SymPy mit didaktischer Struktur.
"""

from typing import Union

import sympy as sp
from sympy import diff, latex, solve, symbols

from .funktion import Funktion


class GemischteFunktion(Funktion):
    """
    Repräsentiert gemischte Funktionen mit mehreren Funktionstypen.

    Beispiele:
    - (x^2 + 1)sin(x) - Polynom × Trigonometrisch
    - exp(-x)(x^3 + 1) - Exponential × Polynom
    - (x+1)/(exp(x)+1) - Rationale Funktion mit Exponential
    - sin(x) + cos(2x) - Trigonometrische Kombination
    """

    def __init__(self, eingabe: Union[str, sp.Basic, "GemischteFunktion"]):
        """
        Konstruktor für gemischte Funktionen.

        Args:
            eingabe: String, SymPy-Ausdruck oder bestehendes GemischteFunktion-Objekt
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
        elif isinstance(eingabe, GemischteFunktion):
            # Kopie
            self.term_sympy = eingabe.term_sympy
            self.komponenten = eingabe.komponenten.copy()
        else:
            raise TypeError(
                "Eingabe muss String, SymPy-Ausdruck oder GemischteFunktion sein"
            )

        # Analysiere die Komponenten der gemischten Funktion
        self.komponenten = self._analysiere_komponenten()

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

    def _analysiere_komponenten(self) -> dict:
        """
        Analysiert die verschiedenen Funktionstypen im gemischten Ausdruck.

        Returns:
            Dictionary mit Informationen über die erkannten Komponenten
        """
        komponenten = {
            "hat_polynom": False,
            "hat_trigonometrisch": False,
            "hat_exponential": False,
            "hat_logarithmisch": False,
            "hat_rational": False,
            "hat_wurzel": False,
            "konkrete_funktionen": [],
            "struktur": self._bestimme_struktur(),
        }

        # Prüfe auf polynomiale Anteile
        if self.term_sympy.is_polynomial(self.x):
            komponenten["hat_polynom"] = True

        # Prüfe auf rationale Funktion
        if self.term_sympy.is_rational_function(self.x):
            komponenten["hat_rational"] = True

        # Prüfe auf spezifische Funktionen
        if self.term_sympy.has(sp.sin, sp.cos, sp.tan, sp.cot, sp.sec, sp.csc):
            komponenten["hat_trigonometrisch"] = True
            # Finde konkrete trigonometrische Funktionen
            for func in [sp.sin, sp.cos, sp.tan]:
                if self.term_sympy.has(func):
                    komponenten["konkrete_funktionen"].append(str(func))

        # Prüfe auf exponentielle Funktionen
        if self.term_sympy.has(sp.exp):
            komponenten["hat_exponential"] = True
            komponenten["konkrete_funktionen"].append("exp")

        # Prüfe auf Potenzen mit Variable im Exponenten
        for potenz in self.term_sympy.atoms(sp.Pow):
            basis, exponent = potenz.as_base_exp()
            if self.x in exponent.free_symbols:
                komponenten["hat_exponential"] = True
                komponenten["konkrete_funktionen"].append("Potenz")

        # Prüfe auf logarithmische Funktionen
        if self.term_sympy.has(sp.log, sp.ln):
            komponenten["hat_logarithmisch"] = True
            komponenten["konkrete_funktionen"].append("log")

        # Prüfe auf Wurzelfunktionen
        if self.term_sympy.has(sp.sqrt):
            komponenten["hat_wurzel"] = True
            komponenten["konkrete_funktionen"].append("sqrt")

        return komponenten

    def _bestimme_struktur(self) -> str:
        """
        Bestimmt die mathematische Struktur der gemischten Funktion.

        Returns:
            Beschreibung der Struktur als String
        """
        # Prüfe auf Produkt-Struktur
        if self.term_sympy.is_Mul:
            return "Produkt"

        # Prüfe auf Summen-Struktur
        if self.term_sympy.is_Add:
            return "Summe"

        # Prüfe auf Quotienten-Struktur
        if self.term_sympy.is_rational_function(
            self.x
        ) and not self.term_sympy.is_polynomial(self.x):
            return "Quotient"

        # Prüfe auf Komposition
        if self._ist_komposition():
            return "Komposition"

        return "Komplex"

    def _ist_komposition(self) -> bool:
        """
        Prüft, ob es sich um eine Komposition f(g(x)) handelt.

        Returns:
            True wenn es eine Komposition ist
        """
        # Einfache Heuristik: suche nach Funktionen von Funktionen
        for func in [sp.sin, sp.cos, sp.tan, sp.exp, sp.log, sp.sqrt]:
            if self.term_sympy.has(func):
                # Prüfe ob das Argument der Funktion nicht nur die Variable ist
                for arg in self.term_sympy.atoms(func):
                    if len(arg.args) > 0:
                        arg_expr = arg.args[0]
                        if arg_expr != self.x and len(arg_expr.free_symbols) > 0:
                            return True
        return False

    def _erstelle_term_string(self) -> str:
        """Erstellt einen lesbaren Term-String."""
        return str(self.term_sympy).replace("**", "^").replace("*", "")

    def get_komponenten_info(self) -> dict:
        """
        Gibt detaillierte Informationen über die Funktionstypen zurück.

        Returns:
            Dictionary mit allen Komponenten-Informationen
        """
        info = self.komponenten.copy()
        info.update(
            {
                "term": self.term(),
                "latex": latex(self.term_sympy),
                "hauptvariable": str(self.x),
                "anzahl_komponenten": sum(
                    1
                    for k, v in self.komponenten.items()
                    if k.startswith("hat_") and v and k != "hat_rational"
                ),
            }
        )
        return info

    def nullstellen(self, real: bool = True, runden=None) -> list[sp.Basic]:
        """
        Berechnet die Nullstellen der gemischten Funktion.

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
            # Für komplexe gemischte Funktionen: numerische Annäherung
            return self._numerische_nullstellen()

    def _numerische_nullstellen(self) -> list[float]:
        """
        Numerische Nullstellensuche als Fallback.

        Returns:
            Liste der numerisch gefundenen Nullstellen
        """
        import numpy as np

        # Einfache Suche in einem reasonable Bereich
        x_werte = np.linspace(-10, 10, 1000)
        nullstellen = []

        for i in range(len(x_werte) - 1):
            try:
                y1 = float(self.term_sympy.subs(self.x, x_werte[i]))
                y2 = float(self.term_sympy.subs(self.x, x_werte[i + 1]))

                # Vorzeichenwechsel = Nullstelle dazwischen
                if y1 * y2 < 0:
                    # Lineare Interpolation für bessere Näherung
                    x0 = x_werte[i] - y1 * (x_werte[i + 1] - x_werte[i]) / (y2 - y1)
                    nullstellen.append(round(x0, 6))

            except (TypeError, ValueError):
                continue

        return sorted(list(set(nullstellen)))

    def ableitung(self, ordnung: int = 1) -> "GemischteFunktion":
        """
        Berechnet die Ableitung gegebener Ordnung.

        Args:
            ordnung: Ordnung der Ableitung (Standard: 1)

        Returns:
            Neue GemischteFunktion mit der abgeleiteten Funktion
        """
        abgeleitet = diff(self.term_sympy, self.x, ordnung)
        return GemischteFunktion(abgeleitet)

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

    def term(self) -> str:
        """Gibt den Term als String zurück."""
        return self.term_str

    def term_latex(self) -> str:
        """Gibt den Term als LaTeX-String zurück."""
        return latex(self.term_sympy)

    def grad(self) -> int:
        """
        Schätzt den "Grad" der gemischten Funktion.
        Für gemischte Funktionen wird dies als die höchste vorkommende
        Potenz der Variable definiert.

        Returns:
        Geschätzter Grad der Funktion
        """
        # Finde die höchste Potenz der Variable in beliebiger Form
        max_grad = 0

        # Durchsuche alle Terme nach Potenzen der Variable
        for term in sp.Add.make_args(self.term_sympy):
            for subterm in sp.Mul.make_args(term):
                if isinstance(subterm, sp.Pow) and subterm.base == self.x:
                    if isinstance(subterm.exp, (int, float)) and subterm.exp > max_grad:
                        max_grad = int(subterm.exp)
                elif subterm == self.x:
                    max_grad = max(max_grad, 1)

        return max_grad

    def __str__(self):
        """String-Repräsentation."""
        return self.term()

    def __repr__(self):
        """Repräsentation für Debugging."""
        return f"GemischteFunktion('{self.original_eingabe}')"
