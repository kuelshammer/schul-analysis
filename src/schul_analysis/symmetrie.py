"""
Symmetrie-Funktionen für das Schul-Analysis Framework.

Einfache Wrapper für Symmetrie-Erkennung mit intelligenter Heuristik.
"""

import sympy as sp

from .funktion import Funktion


def Achsensymmetrie(
    funktion: str | sp.Basic | Funktion,
) -> float | sp.Basic | None:
    """
    Ermittelt die Achse der Achsensymmetrie einer Funktion.

    Args:
        funktion: Die zu untersuchende Funktion

    Returns:
        Die x-Koordinate der Symmetrieachse oder None, wenn nicht achsensymmetrisch

    Examples:
        >>> Achsensymmetrie("x^2")           # 0
        >>> Achsensymmetrie("(x-1)^2")       # 1
        >>> Achsensymmetrie("x^3")           # None
    """
    # Konvertiere zu Funktion-Objekt
    if not isinstance(funktion, Funktion):
        f = Funktion(funktion)
    else:
        f = funktion

    # Spezialfall 1: Quadratische Funktionen
    if f.ist_quadratisch():
        try:
            # Konvertiere zu GanzrationaleFunktion für Koeffizienten-Zugriff
            from .ganzrationale import GanzrationaleFunktion

            if isinstance(f, GanzrationaleFunktion):
                a = f.get_oeffnungsfaktor()
                # Extrahiere b-Koeffizienten (zweiter von rechts)
                b = f.koeffizienten[-2] if len(f.koeffizienten) >= 2 else sp.Integer(0)
                x_s = -b / (2 * a)
                return x_s
            else:
                # Für allgemeine quadratische Funktionen: Extrahiere Koeffizienten aus Term
                x = f._variable_symbol
                poly = f.term_sympy.as_poly(x)
                if poly and poly.degree() == 2:
                    coeffs = poly.all_coeffs()
                    # coeffs sind [a, b, c] für ax² + bx + c
                    a_val, b_val = coeffs[0], coeffs[1]
                    x_s = -b_val / (2 * a_val)
                    return x_s
        except Exception:
            pass

    # Spezialfall 2: Gerade Funktionen (f(-x) = f(x))
    try:
        x = f._variable_symbol
        f_neg_x = f.term_sympy.subs(x, -x)
        if f_neg_x.equals(f.term_sympy):
            return 0  # Symmetrie zur y-Achse
    except Exception:
        pass

    # Allgemeiner Fall: Löse f(x) = f(2a - x)
    try:
        x = f._variable_symbol
        a = sp.symbols("a")  # Unbekannte Symmetrieachse

        # Gleichung aufstellen: f(x) = f(2a - x)
        f_substituted = f.term_sympy.subs(x, 2 * a - x)
        gleichung = sp.Eq(f.term_sympy, f_substituted)

        # Löse die Gleichung
        loesungen = sp.solve(gleichung, a)

        # Filtere gültige Lösungen (keine komplexen, abhängig von x)
        gueltige_loesungen = []
        for loesung in loesungen:
            if not loesung.has(x) and not loesung.has(sp.I):
                gueltige_loesungen.append(loesung)

        if gueltige_loesungen:
            return gueltige_loesungen[0]  # Erste gültige Lösung

    except Exception:
        pass

    return None


def Punktsymmetrie(
    funktion: str | sp.Basic | Funktion,
) -> tuple[float | sp.Basic, float | sp.Basic] | None:
    """
    Ermittelt den Punkt der Punktsymmetrie einer Funktion.

    Args:
        funktion: Die zu untersuchende Funktion

    Returns:
        Der Symmetriepunkt (x_s, y_s) oder None, wenn nicht punktsymmetrisch

    Examples:
        >>> Punktsymmetrie("x^3")           # (0, 0)
        >>> Punktsymmetrie("(x-1)^3 + 2")   # (1, 2)
        >>> Punktsymmetrie("x^2")           # None
    """
    # Konvertiere zu Funktion-Objekt
    if not isinstance(funktion, Funktion):
        f = Funktion(funktion)
    else:
        f = funktion

    # Spezialfall 1: Kubische Funktionen (IMMER punktsymmetrisch zum Wendepunkt)
    if f.ist_kubisch():
        try:
            # Berechne Wendepunkt: zweite Ableitung = 0
            f_strich = f.ableitung(1)
            f_strich_strich = f_strich.ableitung(1)

            # Löse f''(x) = 0
            wendepunkte = f_strich_strich.nullstellen()
            if wendepunkte:
                x_w = wendepunkte[0]
                y_w = f.wert(x_w)
                return (x_w, y_w)
        except Exception:
            pass

    # Spezialfall 2: Ungerade Funktionen (f(-x) = -f(x))
    try:
        x = f._variable_symbol
        f_neg_x = f.term_sympy.subs(x, -x)
        if f_neg_x.equals(-f.term_sympy):
            return (0, 0)  # Symmetrie zum Ursprung
    except Exception:
        pass

    # Allgemeiner Fall: Löse f(a + h) + f(a - h) = 2b
    try:
        x = f._variable_symbol
        a, b, h = sp.symbols("a b h")  # Unbekannter Symmetriepunkt (a,b)

        # Gleichung aufstellen: f(a + h) + f(a - h) = 2b
        f_plus_h = f.term_sympy.subs(x, a + h)
        f_minus_h = f.term_sympy.subs(x, a - h)
        gleichung = sp.Eq(f_plus_h + f_minus_h, 2 * b)

        # Vereinfache und löse
        vereinfacht = sp.simplify(gleichung)

        # Für viele Funktionen gilt: h muss sich herauskürzen
        # Teste spezielle Werte für h um b zu finden
        for test_h in [1, 2, sp.Symbol("h")]:
            try:
                gleichung_mit_h = vereinfacht.subs(h, test_h)

                # Löse nach b auf
                b_loesungen = sp.solve(gleichung_mit_h, b)
                if b_loesungen:
                    b_wert = b_loesungen[0]

                    # Setze b in die ursprüngliche Gleichung ein und löse nach a
                    final_gleichung = vereinfacht.subs(b, b_wert)
                    a_loesungen = sp.solve(final_gleichung, a)

                    if a_loesungen:
                        # Finde Lösungen ohne h
                        gueltige_a = [
                            a_loes for a_loes in a_loesungen if not a_loes.has(h)
                        ]
                        if gueltige_a:
                            return (gueltige_a[0], b_wert)
            except Exception:
                continue

    except Exception:
        pass

    return None
