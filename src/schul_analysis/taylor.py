"""
Einfache Taylorpolynom und Tangente Wrapper für das Schul-Analysis Framework.

Diese Module bietet minimale Wrapper für Taylorpolynome und Tangenten,
die auf SymPy aufbauen und für den Schulunterricht optimiert sind.
"""


import sympy as sp

from .funktion import Funktion
from .ganzrationale import GanzrationaleFunktion


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
        ValueError: Wenn grad nicht positiv ist

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
        raise ValueError(f"Grad muss positiv sein, erhalten: {grad}")

    # Konvertiere Eingabe zu SymPy-Ausdruck
    if isinstance(funktion, Funktion):
        funktion_sympy = funktion.term_sympy
    elif isinstance(funktion, str):
        funktion_sympy = sp.sympify(funktion)
    else:
        funktion_sympy = funktion

    # Erstelle Variable
    x = sp.symbols("x")

    # Berechne Taylorpolynom mit SymPy
    try:
        # sp.series(funktion, variable, punkt, ordnung+1)
        taylor_expr = sp.series(
            funktion_sympy, x, entwicklungspunkt, grad + 1
        ).removeO()

        # Konvertiere zu GanzrationaleFunktion
        return GanzrationaleFunktion(taylor_expr)

    except Exception as e:
        raise ValueError(f"Konnte Taylorpolynom nicht berechnen: {e}")


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
    # Konvertiere Eingabe zu SymPy-Ausdruck
    if isinstance(funktion, Funktion):
        funktion_sympy = funktion.term_sympy
    elif isinstance(funktion, str):
        funktion_sympy = sp.sympify(funktion)
    else:
        funktion_sympy = funktion

    # Erstelle Variable
    x = sp.symbols("x")

    try:
        # Berechne Funktionswert an der Stelle
        f_stelle = funktion_sympy.subs(x, stelle)

        # Berechne erste Ableitung
        f_ableitung = sp.diff(funktion_sympy, x)

        # Berechne Ableitungswert an der Stelle
        f_strich_stelle = f_ableitung.subs(x, stelle)

        # Tangentengleichung: f(a) + f'(a)·(x-a)
        tangentengleichung = f_stelle + f_strich_stelle * (x - stelle)

        # Konvertiere zu GanzrationaleFunktion
        return GanzrationaleFunktion(tangentengleichung)

    except Exception as e:
        raise ValueError(f"Konnte Tangente nicht berechnen: {e}")


# Alternative Namen für bessere Lesbarkeit
taylor = taylorpolynom
tangente_an = tangente
