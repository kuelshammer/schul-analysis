"""
Exponentialfunktionen für das Schul-Analysis Framework.

Einfache Implementierung für exponentialfunktionen wie exp(x), e^x, a^x etc.
"""

from typing import Union

import sympy as sp
from sympy import diff

from .funktion import Funktion
from .sympy_types import VALIDATION_EXACT, validate_function_result


class ExponentialFunktion(Funktion):
    """
    Pädagogischer Wrapper für exponentialfunktionen.

    Beispiele:
    - exp(x)
    - e^x
    - 2^x
    - exp(2x) + 1
    """

    def __init__(self, eingabe: Union[str, sp.Basic, "Funktion"]):
        """
        Konstruktor für exponentialfunktionen.

        Args:
            eingabe: String, SymPy-Ausdruck oder Funktion-Objekt
        """
        super().__init__(eingabe)

    def ist_exponentiell(self) -> bool:
        """
        Prüft, ob es sich um eine exponentialfunktion handelt.
        """
        # Prüfe, ob exp oder ähnliche Funktionen enthalten sind
        exponential_funktionen = {"exp", "E"}
        return any(
            str(func).split("(")[0] in exponential_funktionen
            for func in self.term_sympy.atoms(sp.Function)
        ) or any(
            str(base) in ["E", "exp"]
            for expr in self.term_sympy.atoms(sp.Pow)
            for base in [expr.base]
        )

    def ableitung(self, ordnung: int = 1) -> sp.Basic:
        """
        Berechnet die Ableitung gegebener Ordnung.
        Für exponentialfunktionen gelten spezielle Regeln.
        """
        if ordnung < 1:
            raise ValueError("Die Ordnung muss mindestens 1 sein")

        # Für exp(f(x)) ist die Ableitung exp(f(x)) * f'(x)
        ableitung = diff(self.term_sympy, self._variable_symbol, ordnung)
        # Validiere das Ergebnis für exakte Berechnungen
        validate_function_result(ableitung, VALIDATION_EXACT)
        return ableitung

    def nullstellen(self) -> list:
        """
        Berechnet die Nullstellen der exponentialfunktion.
        Exponentialfunktionen haben keine reellen Nullstellen.
        """
        return []

    def definitionsbereich(self) -> str:
        """
        Gibt den Definitionsbereich zurück.
        """
        return "ℝ (alle reellen Zahlen)"

    def wertebereich(self) -> str:
        """
        Gibt den Wertebereich zurück.
        """
        try:
            # Prüfe, ob es sich um exp(x) oder ähnliches handelt
            if self.term_sympy == sp.exp(self._variable_symbol):
                return "(0, ∞)"
            elif self.term_sympy == sp.exp(-self._variable_symbol):
                return "(0, ∞)"
            else:
                # Für allgemeine exponentialfunktionen
                return "(0, ∞) oder abhängig vom konkreten Term"
        except Exception:
            return "(0, ∞)"

    def asymptoten(self) -> dict:
        """
        Berechnet die Asymptoten der exponentialfunktion.
        """
        asymptoten = {"horizontal": [], "vertikal": [], "schräg": []}

        try:
            # Prüfe auf horizontale Asymptoten
            if self.term_sympy == sp.exp(self._variable_symbol):
                asymptoten["horizontal"].append("y = 0")  # exp(x) → 0 für x → -∞
            elif self.term_sympy == sp.exp(-self._variable_symbol):
                asymptoten["horizontal"].append("y = 0")  # exp(-x) → 0 für x → ∞
        except Exception:
            pass

        return asymptoten

    def __str__(self) -> str:
        """String-Repräsentation"""
        return f"Exponentialfunktion({super().__str__()})"

    def __repr__(self) -> str:
        """Repräsentation"""
        return f"Exponentialfunktion('{super().__str__()}')"


# Hilfsfunktion zur Erkennung von exponentialfunktionen
def ist_exponentialfunktion(ausdruck: str | sp.Basic) -> bool:
    """
    Prüft, ob es sich bei einem Ausdruck um eine exponentialfunktion handelt.

    Args:
        ausdruck: Der zu prüfende Ausdruck

    Returns:
        True, wenn es eine exponentialfunktion ist, sonst False
    """
    if isinstance(ausdruck, str):
        # Konvertiere zu SymPy für die Analyse
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations

        try:
            expr = parse_expr(
                ausdruck.replace("^", "**"), transformations=standard_transformations
            )
        except Exception:
            return False
    else:
        expr = ausdruck

    # Prüfe auf exp-Funktionen
    exponential_funktionen = {"exp", "E"}

    # Prüfe Funktionen
    for func in expr.atoms(sp.Function):
        if str(func).split("(")[0] in exponential_funktionen:
            return True

    # Prüfe Potenzen mit e oder exp
    for power_expr in expr.atoms(sp.Pow):
        base = power_expr.base
        if str(base) in ["E", "exp"]:
            return True

    return False
