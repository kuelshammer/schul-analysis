"""
Taylorpolynom-Funktionen für das Schul-Analysis Framework.

Dieses Modul bietet komfortable Funktionen zur Arbeit mit Taylorpolynomen
und MacLaurin-Reihen für mathematische Analyse und Approximation.
"""

from .taylorpolynom import Taylorpolynom


def Taylor(funktion, entwicklungspunkt=0, grad=3):
    """Erzeugt ein Taylorpolynom für eine Funktion

    Args:
        funktion: Zu approximierende Funktion
        entwicklungspunkt: Punkt um den entwickelt wird (Standard 0)
        grad: Grad des Taylorpolynoms (Standard 3)

    Returns:
        Taylorpolynom: Taylorpolynom-Objekt

    Beispiele:
        >>> # Taylorpolynom für e^x um 0 (MacLaurin-Reihe)
        >>> import sympy as sp
        >>> f = sp.exp(sp.symbols('x'))
        >>> taylor = Taylor(f, 0, 3)
        >>> print(taylor.term)  # Erwartet: 1 + x + x**2/2 + x**3/6

        >>> # Taylorpolynom für sin(x) um π/2
        >>> g = sp.sin(sp.symbols('x'))
        >>> taylor_sin = Taylor(g, sp.pi/2, 2)
        >>> print(taylor_sin.term)
    """
    return Taylorpolynom(funktion, entwicklungspunkt, grad)


def MacLaurin(funktion, grad=3):
    """Erzeugt ein MacLaurin-Polynom (Taylorpolynom um 0)

    Args:
        funktion: Zu approximierende Funktion
        grad: Grad des MacLaurin-Polynoms (Standard 3)

    Returns:
        Taylorpolynom: MacLaurin-Polynom-Objekt

    Beispiele:
        >>> # MacLaurin-Reihe für cos(x)
        >>> import sympy as sp
        >>> f = sp.cos(sp.symbols('x'))
        >>> mclaurin = MacLaurin(f, 4)
        >>> print(mclaurin.term)  # Erwartet: 1 - x**2/2 + x**4/24
    """
    return Taylorpolynom(funktion, 0, grad)


def TaylorKoeffizienten(funktion, entwicklungspunkt=0, grad=3):
    """Berechnet die Taylor-Koeffizienten einer Funktion

    Args:
        funktion: Zu analysierende Funktion
        entwicklungspunkt: Entwicklungspunkt (Standard 0)
        grad: Maximaler Grad (Standard 3)

    Returns:
        list: Liste von (Grad, Koeffizient) Tupeln

    Beispiele:
        >>> # Koeffizienten für e^x
        >>> import sympy as sp
        >>> f = sp.exp(sp.symbols('x'))
        >>> koeff = TaylorKoeffizienten(f, 0, 3)
        >>> print(koeff)  # [(0, 1.0), (1, 1.0), (2, 0.5), (3, 0.166...)]
    """
    taylor = Taylorpolynom(funktion, entwicklungspunkt, grad)
    return taylor.koeffizienten()


def TaylorRestglied(funktion, x_wert, entwicklungspunkt=0, grad=3):
    """Berechnet das Taylor-Restglied (Fehlerabschätzung)

    Args:
        funktion: Zu approximierende Funktion
        x_wert: Stelle an der das Restglied berechnet wird
        entwicklungspunkt: Entwicklungspunkt (Standard 0)
        grad: Grad des Taylorpolynoms (Standard 3)

    Returns:
        float: Wert des Restglieds

    Beispiele:
        >>> # Restglied für e^x Approximation
        >>> import sympy as sp
        >>> f = sp.exp(sp.symbols('x'))
        >>> restglied = TaylorRestglied(f, 1.0, 0, 2)
        >>> print(f"Maximaler Fehler: {restglied:.6f}")
    """
    taylor = Taylorpolynom(funktion, entwicklungspunkt, grad)
    return taylor.restglied_lagrange(x_wert)


def Konvergenzradius(funktion, entwicklungspunkt=0):
    """Bestimmt den Konvergenzradius der Taylorreihe

    Args:
        funktion: Funktion für die Taylorreihe
        entwicklungspunkt: Entwicklungspunkt (Standard 0)

    Returns:
        float: Konvergenzradius oder None wenn nicht bestimmbar

    Beispiele:
        >>> # Konvergenzradius für geometrische Reihe
        >>> import sympy as sp
        >>> f = 1/(1-sp.symbols('x'))
        >>> radius = Konvergenzradius(f, 0)
        >>> print(radius)  # Erwartet: 1.0
    """
    taylor = Taylorpolynom(funktion, entwicklungspunkt, 1)  # Grad 1 reicht
    return taylor.konvergenzradius()


def TaylorVergleich(funktion, entwicklungspunkt=0, max_grad=5):
    """Vergleicht Taylorpolynome verschiedenen Grades

    Args:
        funktion: Zu approximierende Funktion
        entwicklungspunkt: Entwicklungspunkt (Standard 0)
        max_grad: Höchster Grad für den Vergleich (Standard 5)

    Returns:
        dict: Dictionary mit Taylorpolynomen verschiedenen Grades

    Beispiele:
        >>> # Vergleich für sin(x)
        >>> import sympy as sp
        >>> f = sp.sin(sp.symbols('x'))
        >>> vergleich = TaylorVergleich(f, 0, 4)
        >>> for grad, taylor in vergleich.items():
        ...     print(f"Grad {grad}: {taylor.term}")
    """
    taylor_polynome = {}
    for grad in range(1, max_grad + 1):
        taylor_polynome[grad] = Taylorpolynom(funktion, entwicklungspunkt, grad)
    return taylor_polynome


def TaylorStandardbeispiele():
    """Gibt wichtige Standardfunktionen für Taylorpolynome zurück

    Returns:
        dict: Dictionary mit Standardfunktionen

    Beispiele:
        >>> standard = TaylorStandardbeispiele()
        >>> print(standard.keys())  # ['exp(x)', 'sin(x)', 'cos(x)', ...]
        >>> taylor_exp = Taylor(standard['exp(x)'], 0, 3)
    """
    return Taylorpolynom.standardfunktionen()
