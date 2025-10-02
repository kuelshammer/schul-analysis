"""
Schul-Analysis Framework

Ein Python Framework für Schul-Analysis mit exakter Berechnung und Marimo-Integration.
"""

from .ganzrationale import GanzrationaleFunktion
from .gebrochen_rationale import GebrochenRationaleFunktion
from .schmiegkurven import Schmiegkurve
from .taylorpolynom import Taylorpolynom

# ====================
# Schülerfreundliche Funktionen
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


def Extremstellen(funktion, typ: bool = True, runden=None):
    """Berechnet die Extremstellen einer Funktion

    Args:
        funktion: Eine GanzrationaleFunktion
        typ: Wenn True (Standard), werden die Extremstellen klassifiziert.
             Wenn False, werden nur die x-Werte zurückgegeben.
        runden: Anzahl Nachkommastellen für Rundung (None = exakt)

    Returns:
        list: Liste von Tupeln (x, art) mit den Extremstellen (typ=True)
              oder Liste der x-Werte (typ=False)

    Beispiele:
        >>> f = GanzrationaleFunktion("x^3-3x")
        >>> Extremstellen(f)
        [(-1, 'Maximum'), (1, 'Minimum')]
        >>> Extremstellen(f, typ=False)
        [-1, 1]
        >>> Extremstellen(f, runden=2)
        [(-1.0, 'Maximum'), (1.0, 'Minimum')]
    """
    return funktion.extremstellen(typ=typ, runden=runden)


def Wendestellen(funktion, typ: bool = True, runden=None):
    """Berechnet die Wendestellen einer Funktion

    Args:
        funktion: Eine GanzrationaleFunktion
        typ: Wenn True (Standard), werden die Wendestellen klassifiziert.
             Wenn False, werden nur die x-Werte zurückgegeben.
        runden: Anzahl Nachkommastellen für Rundung (None = exakt)

    Returns:
        list: Liste von Tupeln (x, art) mit den Wendestellen (typ=True)
              oder Liste der x-Werte (typ=False)

    Beispiele:
        >>> f = GanzrationaleFunktion("x^3")
        >>> Wendestellen(f)
        [(0, 'L→R')]
        >>> Wendestellen(f, typ=False)
        [0]
        >>> Wendestellen(f, runden=3)
        [(0.0, 'L→R')]

        >>> g = GanzrationaleFunktion("x^4-4x^3")
        >>> Wendestellen(g)
        [(0, 'R→L'), (2, 'L→R')]
        >>> Wendestellen(g, typ=False)
        [0, 2]
    """
    return funktion.wendestellen(typ=typ, runden=runden)


def Extrempunkte(funktion, typ: bool = True, runden=None):
    """Berechnet die Extrempunkte einer Funktion

    Args:
        funktion: Eine GanzrationaleFunktion
        typ: Wenn True (Standard), werden die Extrempunkte klassifiziert.
             Wenn False, werden nur die Koordinaten zurückgegeben.
        runden: Anzahl Nachkommastellen für Rundung (None = exakt)

    Returns:
        list: Liste von Tupeln (x, y, art) mit den Extrempunkten (typ=True)
              oder Liste der Koordinaten (x, y) (typ=False)

    Beispiele:
        >>> f = GanzrationaleFunktion("x^3-3x")
        >>> Extrempunkte(f)
        [(-1, 2.0, 'Maximum'), (1, -2.0, 'Minimum')]
        >>> Extrempunkte(f, typ=False)
        [(-1, 2.0), (1, -2.0)]
        >>> Extrempunkte(f, runden=4)
        [(-1.0, 2.0, 'Maximum'), (1.0, -2.0, 'Minimum')]
    """
    return funktion.extrempunkte(typ=typ, runden=runden)


def Wendepunkte(funktion):
    """Berechnet die Wendepunkte einer Funktion

    Args:
        funktion: Eine GanzrationaleFunktion

    Returns:
        list: Liste von Tupeln (x, art) mit den Wendepunkten

    Beispiele:
        >>> f = GanzrationaleFunktion("x^3")
        >>> Wendepunkte(f)
        [(0.0, 'Wendepunkt')]

        >>> g = GanzrationaleFunktion("x^4-4x^3")
        >>> Wendepunkte(g)
        [(0.0, 'Wendepunkt'), (2.0, 'Wendepunkt')]
    """
    return funktion.wendepunkte()


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
# Schmiegkurven-Funktionen
# ====================


def Schmiegparabel(punkt1, punkt2, punkt3, tangente1=None, tangente3=None):
    """Erzeugt eine Schmiegparabel durch 3 Punkte mit optionalen Tangenten

    Args:
        punkt1, punkt2, punkt3: Drei (x, y) Punkte durch die die Parabel verläuft
        tangente1: Optionale Tangentensteigung an punkt1
        tangente3: Optionale Tangentensteigung an punkt3

    Returns:
        Schmiegkurve: Schmiegparabel als Schmiegkurven-Objekt

    Beispiele:
        >>> # Parabel durch drei Punkte
        >>> p1, p2, p3 = (0, 1), (1, 4), (2, 9)  # auf y = x² + 1
        >>> parabel = Schmiegparabel(p1, p2, p3)
        >>> print(parabel.term)

        >>> # Parabel mit Tangentenbedingungen
        >>> parabel_mit_t = Schmiegparabel((0, 0), (1, 1), (2, 0), tangente1=0)
        >>> print(parabel_mit_t.term)
    """
    return Schmiegkurve.schmiegparabel(punkt1, punkt2, punkt3, tangente1, tangente3)


def Schmiegkegel(punkte, tangenten=None, grad=3):
    """Erzeugt einen Schmiegkegel (kubisches Polynom) durch bis zu 4 Punkte

    Args:
        punkte: Liste von (x, y) Punkten (maximal 4)
        tangenten: Optionale Liste von Tangentensteigungen
        grad: Grad des Polynoms (Standard 3)

    Returns:
        Schmiegkurve: Schmiegkegel als Schmiegkurven-Objekt

    Beispiele:
        >>> # Kubische Kurve durch 4 Punkte
        >>> punkte = [(0, 0), (1, 1), (2, 8), (3, 27)]
        >>> kegel = Schmiegkegel(punkte)
        >>> print(kegel.term)

        >>> # Mit Tangentenbedingung
        >>> kegel_mit_t = Schmiegkegel([(0, 0), (2, 4)], tangenten=[1])
        >>> print(kegel_mit_t.term)
    """
    return Schmiegkurve.schmiegkegel(punkte, tangenten, grad)


def Schmieggerade(punkt, tangente):
    """Erzeugt eine Schmieggerade durch einen Punkt mit gegebener Tangente

    Args:
        punkt: (x, y) Punkt durch den die Gerade verläuft
        tangente: Steigung der Geraden

    Returns:
        Schmiegkurve: Schmieggerade als Schmiegkurven-Objekt

    Beispiele:
        >>> # Gerade durch (0, 0) mit Steigung 2
        >>> gerade = Schmieggerade((0, 0), 2)
        >>> print(gerade.term)  # Erwartet: 2x
    """
    return Schmiegkurve.schmieggerade(punkt, tangente)


def HermiteInterpolation(punkte, werte, ableitungen):
    """Erzeugt eine Schmiegkurve mittels Hermite-Interpolation

    Args:
        punkte: Liste der Stützstellen x_i
        werte: Liste der Funktionswerte f(x_i)
        ableitungen: Liste der Ableitungswerte f'(x_i)

    Returns:
        Schmiegkurve: Hermite-Interpolationspolynom

    Beispiele:
        >>> # Hermite-Interpolation mit Werten und Ableitungen
        >>> x_vals = [0, 1]
        >>> y_vals = [0, 1]
        >>> y_derivs = [0, 0]
        >>> hermite = HermiteInterpolation(x_vals, y_vals, y_derivs)
        >>> print(hermite.term)
    """
    return Schmiegkurve.hermite_interpolation(punkte, werte, ableitungen)


def SchmiegkurveAllgemein(punkte, tangenten=None, normalen=None, grad=None):
    """Erzeugt eine allgemeine Schmiegkurve mit beliebigen Bedingungen

    Args:
        punkte: Liste von (x, y) Punkten
        tangenten: Optionale Liste von Tangentensteigungen
        normalen: Optionale Liste von Normalensteigungen
        grad: Gewünschter Grad des Polynoms

    Returns:
        Schmiegkurve: Allgemeine Schmiegkurve

    Beispiele:
        >>> # Allgemeine Schmiegkurve durch 2 Punkte mit Normalen
        >>> kurve = SchmiegkurveAllgemein(
        ...     [(0, 0), (2, 4)],
        ...     normalen=[-1, -0.5]  # Senkrechte zu y = x und y = 0.5x
        ... )
        >>> print(kurve.term)
    """
    return Schmiegkurve(punkte, tangenten, normalen, grad)


# ====================
# Taylorpolynom-Funktionen
# ====================


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
    "Schmiegkurve",
    "Taylorpolynom",
    "Nullstellen",
    "Polstellen",
    "Ableitung",
    "Wert",
    "Graph",
    "Kürzen",
    "Schnittpunkt",
    "Extremstellen",
    "Wendestellen",
    "Extrempunkte",
    "Wendepunkte",
    "Integral",
    "Grenzwert",
    "AsymptotischesVerhalten",
    "Schmiegparabel",
    "Schmiegkegel",
    "Schmieggerade",
    "HermiteInterpolation",
    "SchmiegkurveAllgemein",
    "Taylor",
    "MacLaurin",
    "TaylorKoeffizienten",
    "TaylorRestglied",
    "Konvergenzradius",
    "TaylorVergleich",
    "TaylorStandardbeispiele",
]
__version__ = "0.1.0"
