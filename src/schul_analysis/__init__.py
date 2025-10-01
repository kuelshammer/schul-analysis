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
    from sympy import Eq, solve

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


def Integral(funktion, a: float, b: float) -> float:
    """Berechnet das bestimmte Integral einer Funktion von a bis b

    Args:
        funktion: Funktion (GanzrationaleFunktion oder GebrochenRationaleFunktion)
        a: Untere Integrationsgrenze
        b: Obere Integrationsgrenze

    Returns:
        float: Wert des bestimmten Integrals

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> Integral(f, 0, 1)
        0.3333333333333333

        >>> g = GebrochenRationaleFunktion("1/x")
        >>> Integral(g, 1, 2)
        0.6931471805599453
    """
    import sympy as sp
    from sympy import integrate

    x = sp.symbols("x")

    # Konvertiere Funktion zu SymPy-Ausdruck
    if hasattr(funktion, "term_sympy"):
        expr = funktion.term_sympy
    else:
        expr = funktion

    try:
        # Berechne unbestimmtes Integral
        unbestimmt_integral = integrate(expr, x)

        # Werte bestimmte Grenzen aus
        integral_wert = unbestimmt_integral.subs(x, b) - unbestimmt_integral.subs(x, a)

        # Konvertiere zu float
        return float(integral_wert)

    except (ValueError, TypeError, NotImplementedError):
        # Fallback: Numerische Integration mit scipy
        try:
            from scipy import integrate as scipy_integrate

            def integrand(x_val):
                try:
                    return funktion.wert(x_val)
                except (ZeroDivisionError, ValueError):
                    return 0.0

            # Numerische Integration
            ergebnis, fehler = scipy_integrate.quad(integrand, a, b)
            return ergebnis

        except ImportError:
            raise ImportError(
                "Für numerische Integration wird scipy benötigt. "
                "Installieren Sie mit: pip install scipy"
            )


def Grenzwert(funktion, zielpunkt: float, richtung: str = "beidseitig") -> float | None:
    """Berechnet den Grenzwert einer Funktion an einer Stelle

    Args:
        funktion: Funktion (GanzrationaleFunktion oder GebrochenRationaleFunktion)
        zielpunkt: Stelle, an der der Grenzwert berechnet werden soll
        richtung: "links", "rechts", oder "beidseitig" (Standard)

    Returns:
        float: Grenzwert oder None, wenn kein Grenzwert existiert

    Beispiele:
        >>> f = GebrochenRationaleFunktion("1/x")
        >>> Grenzwert(f, float('inf'))
        0.0

        >>> g = GebrochenRationaleFunktion("1/(x-1)")
        >>> Grenzwert(g, 1, "rechts")
        inf

        >>> h = GanzrationaleFunktion("x^2")
        >>> Grenzwert(h, 2)
        4.0
    """
    import sympy as sp
    from sympy import limit

    x = sp.symbols("x")

    # Konvertiere Funktion zu SymPy-Ausdruck
    if hasattr(funktion, "term_sympy"):
        expr = funktion.term_sympy
    else:
        expr = funktion

    try:
        if richtung == "links":
            # Linkseitiger Grenzwert
            result = limit(expr, x, zielpunkt, dir="-")
        elif richtung == "rechts":
            # Rechtseitiger Grenzwert
            result = limit(expr, x, zielpunkt, dir="+")
        else:
            # Beidseitiger Grenzwert
            result = limit(expr, x, zielpunkt)

        # Konvertiere Ergebnis zu float, wenn möglich
        try:
            return float(result)
        except (TypeError, ValueError):
            # Behandle spezielle Werte
            if result == sp.oo:
                return float("inf")
            elif result == -sp.oo:
                return float("-inf")
            elif result == sp.nan:
                return None
            else:
                return float(result)

    except (ValueError, NotImplementedError):
        # Numerische Approximation für schwierige Fälle
        return _numerischer_grenzwert(funktion, zielpunkt, richtung)


def _numerischer_grenzwert(
    funktion, zielpunkt: float, richtung: str = "beidseitig"
) -> float:
    """Numerische Approximation von Grenzwerten"""

    if richtung == "links":
        # Nähere dich von links an
        werte = [zielpunkt - 1 / 10**i for i in range(1, 10)]
    elif richtung == "rechts":
        # Nähere dich von rechts an
        werte = [zielpunkt + 1 / 10**i for i in range(1, 10)]
    else:
        # Beidseitig - teste beide Richtungen
        links_limit = _numerischer_grenzwert(funktion, zielpunkt, "links")
        rechts_limit = _numerischer_grenzwert(funktion, zielpunkt, "rechts")

        if abs(links_limit - rechts_limit) < 1e-10:
            return links_limit
        else:
            return None  # Kein beidseitiger Grenzwert

    # Berechne Funktionswerte
    funktions_werte = []
    for x in werte:
        try:
            y = funktion.wert(x)
            funktions_werte.append(y)
        except (ZeroDivisionError, ValueError):
            continue

    if not funktions_werte:
        return None

    # Prüfe auf Konvergenz
    if len(funktions_werte) >= 2:
        if abs(funktions_werte[-1] - funktions_werte[-2]) < 1e-10:
            return funktions_werte[-1]
        elif abs(funktions_werte[-1]) > 1e6:
            return float("inf") if funktions_werte[-1] > 0 else float("-inf")

    return None


def AsymptotischesVerhalten(funktion) -> dict:
    """Analysiert das asymptotische Verhalten einer Funktion

    Args:
        funktion: Funktion (GanzrationaleFunktion oder GebrochenRationaleFunktion)

    Returns:
        dict: Dictionary mit asymptotischem Verhalten

    Beispiele:
        >>> f = GebrochenRationaleFunktion("1/x")
        >>> verhalten = AsymptotischesVerhalten(f)
        >>> print(verhalten["x->inf"])
        '0'
        >>> print(verhalten["x->-inf"])
        '0'
    """
    import sympy as sp
    from sympy import limit, oo

    x = sp.symbols("x")

    # Konvertiere Funktion zu SymPy-Ausdruck
    if hasattr(funktion, "term_sympy"):
        expr = funktion.term_sympy
    else:
        expr = funktion

    verhalten = {}

    # Analyse für x -> ∞
    try:
        limit_inf = limit(expr, x, oo)
        verhalten["x->inf"] = str(limit_inf)
    except Exception:
        verhalten["x->inf"] = "undefiniert"

    # Analyse für x -> -∞
    try:
        limit_neg_inf = limit(expr, x, -oo)
        verhalten["x->-inf"] = str(limit_neg_inf)
    except Exception:
        verhalten["x->-inf"] = "undefiniert"

    # Analyse für Polstellen (falls vorhanden)
    if hasattr(funktion, "polstellen"):
        polstellen = funktion.polstellen()
        for pol in polstellen:
            # Linkseitiger Grenzwert
            try:
                links = limit(expr, x, pol, dir="-")
                verhalten[f"x->{pol}-"] = str(links)
            except Exception:
                verhalten[f"x->{pol}-"] = "undefiniert"

            # Rechtseitiger Grenzwert
            try:
                rechts = limit(expr, x, pol, dir="+")
                verhalten[f"x->{pol}+"] = str(rechts)
            except Exception:
                verhalten[f"x->{pol}+"] = "undefiniert"

    return verhalten


# ====================
# Typ-Aliases für bessere Lesbarkeit
# ====================

# Typ-Aliases für Kompatibilität
Polstellen = Polstellen  # Englische Variante auch verfügbar
Ableiten = Ableitung
Derivative = Ableitung
IntersectionPoints = Schnittpunkt
Integral = Integral
Limit = Grenzwert
AsymptoticBehavior = AsymptotischesVerhalten

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
    "Integral",
    "Grenzwert",
    "AsymptotischesVerhalten",
]
__version__ = "0.1.0"
