"""
Schul-Analysis Framework

Ein Python Framework für Schul-Analysis mit exakter Berechnung und Marimo-Integration.
"""

from .ganzrationale import GanzrationaleFunktion
from .gebrochen_rationale import GebrochenRationaleFunktion

# ====================
# Schülerfreundliche Funktionen
# ====================


def Nullstellen(funktion) -> list:
    """Berechnet die Nullstellen einer Funktion

    Args:
        funktion: Eine GanzrationaleFunktion oder GebrochenRationaleFunktion

    Returns:
        list: Liste der Nullstellen

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2-4")
        >>> Nullstellen(f)
        [-2.0, 2.0]

        >>> g = GebrochenRationaleFunktion("(x^2-1)/(x-2)")
        >>> Nullstellen(g)
        [-1.0, 1.0]
    """
    return funktion.nullstellen()


def Polstellen(funktion) -> list:
    """Berechnet die Polstellen einer Funktion

    Args:
        funktion: Eine GebrochenRationaleFunktion

    Returns:
        list: Liste der Polstellen

    Beispiele:
        >>> f = GebrochenRationaleFunktion("1/(x-1)")
        >>> Polstellen(f)
        [1.0]
    """
    return funktion.polstellen()


def Ableitung(funktion, ordnung: int = 1):
    """Berechnet die Ableitung einer Funktion

    Args:
        funktion: Eine GanzrationaleFunktion oder GebrochenRationaleFunktion
        ordnung: Ordnung der Ableitung (Standard: 1)

    Returns:
        Abgeleitete Funktion

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> Ableitung(f)
        GanzrationaleFunktion('2*x')
    """
    return funktion.ableitung(ordnung)


def Wert(funktion, x_wert: float) -> float:
    """Berechnet den Funktionswert an einer Stelle

    Args:
        funktion: Eine GanzrationaleFunktion oder GebrochenRationaleFunktion
        x_wert: x-Wert an dem ausgewertet werden soll

    Returns:
        float: Funktionswert

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> Wert(f, 3)
        9.0
    """
    return funktion.wert(x_wert)


def Graph(funktion, x_bereich: tuple = (-5, 5)):
    """Erzeugt einen Graphen der Funktion

    Args:
        funktion: Eine GanzrationaleFunktion oder GebrochenRationaleFunktion
        x_bereich: x-Bereich für den Graphen (Standard: (-5, 5))

    Returns:
        Plotly-Figure

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> graph = Graph(f)
    """
    return funktion.plotly(x_bereich)


def Kürzen(funktion):
    """Kürzt eine Funktion (wenn möglich)

    Args:
        funktion: Eine GebrochenRationaleFunktion

    Returns:
        Gekürzte Funktion

    Beispiele:
        >>> f = GebrochenRationaleFunktion("(x^2-4)/(x-2)")
        >>> gekuerzt = Kürzen(f)
    """
    return funktion.kürzen()


# ====================
# Typ-Aliases für bessere Lesbarkeit
# ====================

# Typ-Aliases für Kompatibilität
Polstellen = Polstellen  # Englische Variante auch verfügbar
Ableiten = Ableitung
Derivative = Ableitung

__all__ = [
    "GanzrationaleFunktion",
    "GebrochenRationaleFunktion",
    "Nullstellen",
    "Polstellen",
    "Ableitung",
    "Wert",
    "Graph",
    "Kürzen",
]
__version__ = "0.1.0"
