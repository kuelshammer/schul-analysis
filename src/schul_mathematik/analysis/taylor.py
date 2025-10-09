"""
Einfache Taylorpolynom und Tangente Wrapper für das Schul-Analysis Framework.

Diese Module bietet minimale Wrapper für Taylorpolynome und Tangenten,
die auf SymPy aufbauen und für den Schulunterricht optimiert sind.
"""

import sympy as sp

from .errors import SchulAnalysisError
from .funktion import Funktion
from .ganzrationale import GanzrationaleFunktion


class DidaktischerFehler(SchulAnalysisError):
    """Basisklasse für alle didaktischen Fehlermeldungen."""

    def __init__(self, nachricht: str, tipp: str = ""):
        self.nachricht = nachricht
        self.tipp = tipp
        super().__init__(self.format_message())

    def format_message(self) -> str:
        msg = f"Problem: {self.nachricht}"
        if self.tipp:
            msg += f"\nTipp: {self.tipp}"
        return msg


class UngueltigerGradFehler(DidaktischerFehler):
    """Fehler bei ungültigem Grad des Taylorpolynoms."""

    pass


class UngueltigeFunktionFehler(DidaktischerFehler):
    """Fehler bei ungültiger Funktionseingabe."""

    pass


def _input_zu_sympy(funktion: str | sp.Basic | Funktion) -> tuple[sp.Basic, sp.Symbol]:
    """
    Hilfsfunktion zur Konvertierung verschiedener Eingabeformate zu SymPy.

    Args:
        funktion: Funktion als String, SymPy-Ausdruck oder Funktion-Objekt

    Returns:
        Tuple aus (SymPy-Ausdruck, Variable)

    Raises:
        UngueltigeFunktionFehler: Bei ungültiger Eingabe
    """
    try:
        if isinstance(funktion, Funktion):
            funktion_sympy = funktion.term_sympy
            variable = funktion._variable_symbol
        elif isinstance(funktion, str):
            funktion_sympy = sp.sympify(funktion)
            # Finde die Variable automatisch
            freie_variablen = funktion_sympy.free_symbols
            if len(freie_variablen) == 1:
                variable = next(iter(freie_variablen))
            else:
                # Standardmäßig x verwenden, wenn keine oder mehrere Variablen
                variable = sp.symbols("x")
        else:
            funktion_sympy = funktion
            # Finde die Variable automatisch
            freie_variablen = funktion_sympy.free_symbols
            if len(freie_variablen) == 1:
                variable = next(iter(freie_variablen))
            else:
                variable = sp.symbols("x")

        return funktion_sympy, variable

    except Exception:
        raise UngueltigeFunktionFehler(
            f"Die Funktion '{funktion}' konnte nicht verarbeitet werden.",
            "Stellen Sie sicher, dass die Funktion mathematisch korrekt ist. "
            "Beispiele: 'x^2', 'sin(x)', '(x-1)^3 + 2'",
        )


def taylorpolynom(
    funktion: str | sp.Basic | Funktion,
    grad: int,
    entwicklungspunkt: float | sp.Basic = 0,
) -> GanzrationaleFunktion:
    """
    Erstellt ein Taylorpolynom für eine Funktion.

    Args:
        funktion: Zu approximierende Funktion (String, SymPy-Ausdruck oder Funktion)
        grad: Grad des Taylorpolynoms (muss angegeben werden)
        entwicklungspunkt: Entwicklungspunkt (Standard: 0 für MacLaurin-Reihe)

    Returns:
        GanzrationaleFunktion: Das Taylorpolynom als Funktion

    Raises:
        UngueltigerGradFehler: Wenn grad nicht positiv ist
        UngueltigeFunktionFehler: Wenn die Funktion ungültig ist

    Examples:
        >>> # Taylorpolynom 2. Grades für x^2 um x=0
        >>> t = taylorpolynom('x^2', grad=2)
        >>> print(t.term)  # x^2

        >>> # Taylorpolynom 2. Grades für (x+a)^4 um x=a
        >>> import sympy as sp
        >>> a = sp.symbols('a')
        >>> t = taylorpolynom('(x+a)**4', grad=2, entwicklungspunkt=a)
        >>> print(t.term)  # a^4 + 4*a^3*(x - a) + 6*a^2*(x - a)^2
    """
    if grad <= 0:
        raise UngueltigerGradFehler(
            f"Der Grad muss positiv sein, aber du hast {grad} eingegeben.",
            "Für ein Taylorpolynom brauchst du mindestens Grad 1.",
        )

    try:
        # Konvertiere Eingabe zu SymPy-Ausdruck und finde Variable
        funktion_sympy, variable = _input_zu_sympy(funktion)

        # Berechne Taylorpolynom mit SymPy
        taylor_expr = sp.series(
            funktion_sympy, variable, entwicklungspunkt, grad + 1
        ).removeO()

        # Expandiere den Ausdruck, um die Taylor-Form beizubehalten
        taylor_expr = sp.expand(taylor_expr)

        # Konvertiere zu GanzrationaleFunktion
        return GanzrationaleFunktion(taylor_expr)

    except DidaktischerFehler:
        # Didaktische Fehler bereits formatiert durchreichen
        raise
    except Exception:
        raise UngueltigeFunktionFehler(
            f"Das Taylorpolynom für '{funktion}' konnte nicht berechnet werden.",
            "Überprüfe deine Funktion und den Entwicklungspunkt. "
            "Stelle sicher, dass die Funktion an der Entwicklungsstelle definiert ist.",
        )


def tangente(
    funktion: str | sp.Basic | Funktion, stelle: float | sp.Basic
) -> GanzrationaleFunktion:
    """
    Erstellt die Tangente an eine Funktion an einer gegebenen Stelle.

    Dies ist ein Spezialfall des Taylorpolynoms 1. Grades.

    Args:
        funktion: Funktion (String, SymPy-Ausdruck oder Funktion)
        stelle: Stelle, an der die Tangente berührt (kann symbolisch sein)

    Returns:
        GanzrationaleFunktion: Die Tangente als Funktion

    Raises:
        UngueltigeFunktionFehler: Wenn die Tangente nicht berechnet werden kann

    Examples:
        >>> # Tangente an x^2 bei x=1
        >>> t = tangente('x^2', 1)
        >>> print(t.term)  # 2*x - 1
        >>> print(t(0))    # -1 (Achsenabschnitt)

        >>> # Tangente mit symbolischer Stelle
        >>> import sympy as sp
        >>> a = sp.symbols('a')
        >>> t = tangente('x^2', a)
        >>> print(t.term)  # 2*a*x - a^2
        >>> # Kann für Parameteraufgaben verwendet werden
    """
    try:
        # Eine Tangente ist einfach ein Taylorpolynom 1. Grades
        # Diese Implementierung ist einfach, robust und didaktisch korrekt
        return taylorpolynom(funktion, grad=1, entwicklungspunkt=stelle)

    except DidaktischerFehler:
        # Didaktische Fehler bereits formatiert durchreichen
        raise
    except Exception:
        raise UngueltigeFunktionFehler(
            f"Die Tangente an '{funktion}' an der Stelle {stelle} konnte nicht berechnet werden.",
            "Stelle sicher, dass die Funktion an dieser Stelle definiert und differenzierbar ist. "
            "Bei Funktionen mit Lücken (z.B. 1/x) achte auf den Definitionsbereich.",
        )


# Alternative Namen für bessere Lesbarkeit
taylor = taylorpolynom
tangente_an = tangente
