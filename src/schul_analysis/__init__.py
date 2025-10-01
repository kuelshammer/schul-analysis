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


def Schnittpunkt(f1, f2):
    """Berechnet die Schnittpunkte zweier Funktionen

    Args:
        f1: Erste Funktion (GanzrationaleFunktion oder GebrochenRationaleFunktion)
        f2: Zweite Funktion (GanzrationaleFunktion oder GebrochenRationaleFunktion)

    Returns:
        list: Liste von Tupeln (x, y) mit den Schnittpunkten

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> g = GanzrationaleFunktion("x+2")
        >>> Schnittpunkt(f, g)
        [(-1.0, 1.0), (2.0, 4.0)]

        >>> h = GebrochenRationaleFunktion("1/x")
        >>> i = GanzrationaleFunktion("x")
        >>> Schnittpunkt(h, i)
        [(1.0, 1.0), (-1.0, -1.0)]
    """
    import sympy as sp
    from sympy import solve, Eq

    # Erstelle SymPy-Gleichung f1(x) = f2(x)
    x = sp.symbols("x")

    # Konvertiere beide Funktionen zu SymPy-Ausdrücken
    if hasattr(f1, "term_sympy"):
        f1_expr = f1.term_sympy
    else:
        f1_expr = f1

    if hasattr(f2, "term_sympy"):
        f2_expr = f2.term_sympy
    else:
        f2_expr = f2

    # Stelle Gleichung auf und löse
    gleichung = Eq(f1_expr, f2_expr)
    loesungen = solve(gleichung, x)

    # Berechne y-Koordinaten und filtere gültige Punkte
    schnittpunkte = []
    for loesung in loesungen:
        # Versuche, die Lösung in float umzuwandeln
        try:
            x_wert = float(loesung)

            # Prüfe, ob beide Funktionen an dieser Stelle definiert sind
            try:
                y_wert1 = f1.wert(x_wert)
                y_wert2 = f2.wert(x_wert)

                # Beide sollten den gleichen y-Wert geben (within tolerance)
                if abs(y_wert1 - y_wert2) < 1e-10:
                    schnittpunkte.append((x_wert, y_wert1))

            except (ZeroDivisionError, ValueError, AttributeError):
                # Überspringe Punkte, wo eine Funktion nicht definiert ist
                continue

        except (TypeError, ValueError):
            # Überspringe komplexe oder nicht-numerische Lösungen
            continue

    # Sortiere Schnittpunkte nach x-Koordinate
    schnittpunkte.sort(key=lambda punkt: punkt[0])

    return schnittpunkte


# ====================
# Typ-Aliases für bessere Lesbarkeit
# ====================

# Typ-Aliases für Kompatibilität
Polstellen = Polstellen  # Englische Variante auch verfügbar
Ableiten = Ableitung
Derivative = Ableitung
IntersectionPoints = Schnittpunkt

__all__ = [
    "GanzrationaleFunktion",
    "GebrochenRationaleFunktion",
    "Nullstellen",
    "Polstellen",
    "Ableitung",
    "Wert",
    "Graph",
    "Kürzen",
    "Schnittpunkt",
]
__version__ = "0.1.0"
