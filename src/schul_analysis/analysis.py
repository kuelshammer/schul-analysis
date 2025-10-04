"""
Analysis-Module für das Schul-Analysis Framework

Dieses Modul enthält Kernfunktionen zur mathematischen Analyse von Funktionen,
einschließlich Nullstellenberechnung, Ableitungen, Extremstellen und Grenzwerten.
"""

import sympy as sp

from .funktion import Funktion


# ====================
# Grundlegende Analyse-Funktionen
# ====================


def Nullstellen(funktion, runden=None) -> list:
    """Berechnet die Nullstellen einer Funktion

    Args:
        funktion: Eine GanzrationaleFunktion oder GebrochenRationaleFunktion
        runden: Anzahl Nachkommastellen für Rundung (None = exakt)

    Returns:
        list: Liste der Nullstellen

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2-4")
        >>> Nullstellen(f)
        [-2, 2]
        >>> Nullstellen(f, runden=2)
        [-2.0, 2.0]

        >>> g = GebrochenRationaleFunktion("(x^2-1)/(x-2)")
        >>> Nullstellen(g)
        [-1, 1]
        >>> Nullstellen(g, runden=0)
        [-1.0, 1.0]
    """
    return funktion.nullstellen(runden=runden)


def Polstellen(funktion) -> list:
    """Berechnet die Polstellen einer Funktion

    Args:
        funktion: Eine Funktion mit möglichen Polstellen

    Returns:
        list: Liste der Polstellen

    Beispiele:
        >>> g = GebrochenRationaleFunktion("1/(x-2)")
        >>> Polstellen(g)
        [2]
    """
    return funktion.polstellen()


def Ableitung(funktion, ordnung: int = 1):
    """Berechnet die Ableitung einer Funktion

    Args:
        funktion: Eine ableitbare Funktion
        ordnung: Ordnung der Ableitung (Standard: 1)

    Returns:
        Funktion: Die abgeleitete Funktion

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> f_strich = Ableitung(f)
        >>> f_strich.term
        '2x'
    """
    return funktion.ableitung(ordnung)


def Wert(funktion, x_wert: float) -> float:
    """Berechnet den Funktionswert an einer Stelle

    Args:
        funktion: Eine Funktion
        x_wert: x-Wert an dem ausgewertet werden soll

    Returns:
        float: Funktionswert f(x_wert)

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> Wert(f, 3)
        9.0
    """
    return funktion.wert(x_wert)


# ====================
# Kurvendiskussion
# ====================


def Extremstellen(funktion, typ: bool = True, runden=None):
    """Berechnet Extremstellen einer Funktion

    Args:
        funktion: Eine Funktion
        typ: True für Maxima, False für Minima (Standard: True)
        runden: Anzahl Nachkommastellen für Rundung

    Returns:
        list: Liste der Extremstellen

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> Extremstellen(f, typ=False)  # Minimum
        [(0.0, 'Minimum')]
    """
    return funktion.extremstellen(typ=typ, runden=runden)


def Wendestellen(funktion, typ: bool = True, runden=None):
    """Berechnet Wendestellen einer Funktion

    Args:
        funktion: Eine Funktion
        typ: True für Links-rechts-Wendepunkte, False für Rechts-links-Wendepunkte
        runden: Anzahl Nachkommastellen für Rundung

    Returns:
        list: Liste der Wendestellen

    Beispiele:
        >>> f = GanzrationaleFunktion("x^3")
        >>> Wendestellen(f)
        [(0.0, 'Links-rechts-Wendepunkt')]
    """
    return funktion.wendestellen(typ=typ, runden=runden)


def Extrempunkte(funktion, typ: bool = True, runden=None):
    """Berechnet Extrempunkte einer Funktion

    Args:
        funktion: Eine Funktion
        typ: True für Maxima, False für Minima
        runden: Anzahl Nachkommastellen für Rundung

    Returns:
        list: Liste der Extrempunkte als (x, y, typ) Tupel

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> Extrempunkte(f, typ=False)
        [(0.0, 0.0, 'Minimum')]
    """
    return funktion.extrempunkte(typ=typ, runden=runden)


def Wendepunkte(funktion, typ: bool = True, runden=None):
    """Berechnet Wendepunkte einer Funktion

    Args:
        funktion: Eine Funktion
        typ: True für Links-rechts-Wendepunkte, False für Rechts-links-Wendepunkte
        runden: Anzahl Nachkommastellen für Rundung

    Returns:
        list: Liste der Wendepunkte als (x, y, typ) Tupel

    Beispiele:
        >>> f = GanzrationaleFunktion("x^3")
        >>> Wendepunkte(f)
        [(0.0, 0.0, 'Links-rechts-Wendepunkt')]
    """
    return funktion.wendepunkte(typ=typ, runden=runden)


# ====================
# Integralrechnung
# ====================


def Integral(funktion, a: float, b: float) -> float:
    """Berechnet das bestimmtes Integral einer Funktion

    Args:
        funktion: Eine integrierbare Funktion (GanzrationaleFunktion, GebrochenRationaleFunktion, etc.)
        a: Untere Integrationsgrenze
        b: Obere Integrationsgrenze

    Returns:
        float: Wert des bestimmten Integrals

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> Integral(f, 0, 1)
        0.3333333333333333
    """
    # Prüfe ob die Funktion die benötigten Methoden hat
    if not (hasattr(funktion, "term_sympy") and hasattr(funktion, "wert")):
        raise TypeError(
            "Argument muss eine Funktion mit term_sympy und wert Methoden sein"
        )

    # Symbolische Integration
    x = sp.Symbol("x")
    try:
        # Versuche symbolische Integration
        expr = funktion.term_sympy
        stammfunktion = sp.integrate(expr, x)

        # Werte das bestimmte Integral aus
        integral_wert = float(stammfunktion.subs(x, b) - stammfunktion.subs(x, a))
        return integral_wert
    except Exception:
        # Fallback: Numerische Integration mit scipy
        try:
            from scipy import integrate as scipy_integrate

            def integrand(x_val):
                return funktion.wert(x_val)

            integral_wert, _ = scipy_integrate.quad(integrand, a, b)
            return integral_wert
        except ImportError:
            # Fallback: Trapezregel
            n = 1000
            h = (b - a) / n
            summe = 0.5 * (funktion.wert(a) + funktion.wert(b))

            for i in range(1, n):
                summe += funktion.wert(a + i * h)

            return h * summe


# ====================
# Weitere Analyse-Funktionen
# ====================


def Kürzen(funktion):
    """Kürzt eine gebrochen rationale Funktion

    Args:
        funktion: Eine kürzbare Funktion

    Returns:
        Funktion: Gekürzte Funktion

    Beispiele:
        >>> g = GebrochenRationaleFunktion("(x^2-1)/(x-1)")
        >>> gekuerzt = Kürzen(g)
        >>> gekuerzt.term
        'x + 1'
    """
    if hasattr(funktion, "kürzen"):
        return funktion.kürzen()
    else:
        raise TypeError("Funktion kann nicht gekürzt werden")


def Schnittpunkt(f1, f2):
    """Berechnet Schnittpunkte zweier Funktionen

    Args:
        f1: Erste Funktion
        f2: Zweite Funktion

    Returns:
        list: Liste der Schnittpunkte als (x, y) Tupel

    Beispiele:
        >>> f1 = GanzrationaleFunktion("x^2")
        >>> f2 = GanzrationaleFunktion("x")
        >>> Schnittpunkt(f1, f2)
        [(0.0, 0.0), (1.0, 1.0)]
    """
    if not (isinstance(f1, Funktion) and isinstance(f2, Funktion)):
        raise TypeError("Beide Argumente müssen Funktionen sein")

    # Finde x-Werte wo f1(x) = f2(x)
    x = sp.Symbol("x")
    gleichung = sp.Eq(f1.term_sympy, f2.term_sympy)

    try:
        loesungen = sp.solve(gleichung, x)
        schnittpunkte = []

        for loesung in loesungen:
            if loesung.is_real:
                x_wert = float(loesung)
                y_wert = f1.wert(x_wert)
                schnittpunkte.append((x_wert, y_wert))

        return schnittpunkte
    except Exception:
        return []


# ====================
# Grenzwerte und asymptotisches Verhalten
# ====================


def Grenzwert(funktion, zielpunkt: float, richtung: str = "beidseitig") -> float | None:
    """Berechnet den Grenzwert einer Funktion

    Args:
        funktion: Eine Funktion mit term_sympy Methode
        zielpunkt: Punkt für den der Grenzwert berechnet werden soll
        richtung: "links", "rechts" oder "beidseitig" (Standard)

    Returns:
        float | None: Grenzwert oder None wenn nicht existent

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> Grenzwert(f, 2)
        4.0
    """
    # Prüfe ob die Funktion die benötigten Methoden hat
    if not hasattr(funktion, "term_sympy"):
        raise TypeError("Argument muss eine Funktion mit term_sympy Methode sein")

    x = sp.Symbol("x")
    expr = funktion.term_sympy

    try:
        if richtung == "links":
            limit_val = sp.limit(expr, x, zielpunkt, dir="-")
        elif richtung == "rechts":
            limit_val = sp.limit(expr, x, zielpunkt, dir="+")
        else:  # beidseitig
            limit_val = sp.limit(expr, x, zielpunkt)

        return float(limit_val) if limit_val.is_Number else None
    except Exception:
        # Fallback: Numerische Annäherung
        return _numerischer_grenzwert(funktion, zielpunkt, richtung)


def _numerischer_grenzwert(
    funktion, zielpunkt: float, richtung: str = "beidseitig"
) -> float | None:
    """Numerische Berechnung von Grenzwerten als Fallback"""
    epsilon = 1e-10

    try:
        if richtung == "links":
            return funktion.wert(zielpunkt - epsilon)
        elif richtung == "rechts":
            return funktion.wert(zielpunkt + epsilon)
        else:
            links = funktion.wert(zielpunkt - epsilon)
            rechts = funktion.wert(zielpunkt + epsilon)

            if abs(links - rechts) < 1e-8:
                return (links + rechts) / 2
            else:
                return None
    except Exception:
        return None


def AsymptotischesVerhalten(funktion) -> dict:
    """Analysiert das asymptotische Verhalten einer Funktion

    Args:
        funktion: Eine Funktion mit term_sympy Methode

    Returns:
        dict: Dictionary mit Grenzwerten für x->∞ und x->-∞

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> verhalten = AsymptotischesVerhalten(f)
        >>> print(verhalten)
        {'x->inf': 'oo', 'x->-inf': 'oo'}
    """
    # Prüfe ob die Funktion die benötigten Methoden hat
    if not hasattr(funktion, "term_sympy"):
        raise TypeError("Argument muss eine Funktion mit term_sympy Methode sein")

    x = sp.Symbol("x")
    expr = funktion.term_sympy
    verhalten = {}

    # Analyse für x -> ∞
    try:
        limit_inf = sp.limit(expr, x, sp.oo)
        verhalten["x->inf"] = str(limit_inf)
    except Exception:
        verhalten["x->inf"] = "undefiniert"

    # Analyse für x -> -∞
    try:
        limit_neg_inf = sp.limit(expr, x, -sp.oo)
        verhalten["x->-inf"] = str(limit_neg_inf)
    except Exception:
        verhalten["x->-inf"] = "undefiniert"

    # Analyse für Polstellen (falls vorhanden)
    if hasattr(funktion, "polstellen"):
        polstellen = funktion.polstellen()
        for pol in polstellen:
            # Linkseitiger Grenzwert
            try:
                links = sp.limit(expr, x, pol, dir="-")
                verhalten[f"x->{pol}-"] = str(links)
            except Exception:
                verhalten[f"x->{pol}-"] = "undefiniert"

            # Rechtseitiger Grenzwert
            try:
                rechts = sp.limit(expr, x, pol, dir="+")
                verhalten[f"x->{pol}+"] = str(rechts)
            except Exception:
                verhalten[f"x->{pol}+"] = "undefiniert"

    return verhalten
