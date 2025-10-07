"""
Automatische Funktionszerlegung für das Schul-Analysis Framework.

Vereinfachte Version, die zuverlässig die Grundstrukturen erkennt.
"""

from enum import Enum
from typing import Any

import sympy as sp

from .errors import SchulAnalysisError
from .funktion import Funktion


class FunktionsTyp(Enum):
    """Enumeration für die verschiedenen Funktionstypen."""

    GANZRATIONAL = "ganzrational"
    TRIGONOMETRISCH = "trigonometrisch"
    EXPONENTIELL = "exponentiell"
    LOGARITHMISCH = "logarithmisch"
    KONSTANTE = "konstante"
    SUMME = "summe"
    PRODUKT = "produkt"
    QUOTIENT = "quotient"
    KOMPOSITION = "komposition"
    UNBEKANNT = "unbekannt"


class StrukturAnalyseError(SchulAnalysisError):
    """Fehler bei der Strukturanalyse von Funktionen."""

    pass


def _klassifiziere_einfache_funktion(
    expr: sp.Basic, variable: sp.Symbol
) -> FunktionsTyp:
    """Klassifiziert eine einfache Funktion ohne komplexe Struktur."""
    # Konstante prüfen (inkl. Zahlen)
    try:
        # Typ-Annotation für SymPy-Objekte
        if hasattr(expr, "is_constant") and callable(expr.is_constant):
            if expr.is_constant():  # type: ignore
                return FunktionsTyp.KONSTANTE
    except Exception:
        # Falls is_constant fehlschlägt, prüfe auf Zahl
        if isinstance(expr, (sp.Integer, sp.Float, sp.Rational, int)):
            return FunktionsTyp.KONSTANTE

    # Polynom prüfen (ganzrational)
    if hasattr(expr, "is_polynomial") and callable(expr.is_polynomial):
        if expr.is_polynomial(variable):  # type: ignore
            return FunktionsTyp.GANZRATIONAL

    # Trigonometrische Funktionen
    if hasattr(expr, "func") and expr.func in (sp.sin, sp.cos, sp.tan, sp.cot):
        return FunktionsTyp.TRIGONOMETRISCH

    # Exponentielle Funktionen
    if hasattr(expr, "func") and expr.func == sp.exp:
        return FunktionsTyp.EXPONENTIELL

    # Logarithmische Funktionen
    if hasattr(expr, "func") and expr.func in (sp.log, sp.ln):
        return FunktionsTyp.LOGARITHMISCH

    return FunktionsTyp.UNBEKANNT


def _vereinfache_pythagoreische_identitaet(expr: sp.Basic) -> sp.Basic:
    """
    Erkennt und vereinfacht die Pythagoreische Identität sin²(x) + cos²(x) = 1.
    Dies ist die einzige trigonometrische Identität, die Schüler üblicherweise kennen.

    Args:
        expr: Zu vereinfachender Ausdruck

    Returns:
        Vereinfachter Ausdruck oder Original, wenn keine Vereinfachung möglich
    """
    # Prüfe, ob es sich um eine Summe handelt
    if not isinstance(expr, sp.Add):
        return expr

    # Prüfe, ob genau zwei Terme vorhanden sind
    if len(expr.args) != 2:
        return expr

    term1, term2 = expr.args

    # Prüfe verschiedene Formen der Pythagoreischen Identität
    patterns = [
        # sin²(x) + cos²(x) = 1
        (
            lambda t1, t2: (
                (
                    isinstance(t1, sp.Pow)
                    and t1.func == sp.Pow
                    and t1.args[1] == 2
                    and isinstance(t1.args[0], sp.sin)
                )
                and (
                    isinstance(t2, sp.Pow)
                    and t2.func == sp.Pow
                    and t2.args[1] == 2
                    and isinstance(t2.args[0], sp.cos)
                )
            )
        ),
        # cos²(x) + sin²(x) = 1 (umgekehrte Reihenfolge)
        (
            lambda t1, t2: (
                (
                    isinstance(t1, sp.Pow)
                    and t1.func == sp.Pow
                    and t1.args[1] == 2
                    and isinstance(t1.args[0], sp.cos)
                )
                and (
                    isinstance(t2, sp.Pow)
                    and t2.func == sp.Pow
                    and t2.args[1] == 2
                    and isinstance(t2.args[0], sp.sin)
                )
            )
        ),
        # Allgemeiner: Prüfe auf a*sin²(x) + a*cos²(x) = a
        (
            lambda t1, t2: (
                isinstance(t1, sp.Mul)
                and isinstance(t2, sp.Mul)
                and len(t1.args) == 2
                and len(t2.args) == 2
                and t1.args[0] == t2.args[0]  # Gleicher Koeffizient
                and (
                    (
                        isinstance(t1.args[1], sp.Pow)
                        and t1.args[1].func == sp.Pow
                        and t1.args[1].args[1] == 2
                        and isinstance(t1.args[1].args[0], sp.sin)
                        and isinstance(t2.args[1], sp.Pow)
                        and t2.args[1].func == sp.Pow
                        and t2.args[1].args[1] == 2
                        and isinstance(t2.args[1].args[0], sp.cos)
                    )
                    or (
                        isinstance(t1.args[1], sp.Pow)
                        and t1.args[1].func == sp.Pow
                        and t1.args[1].args[1] == 2
                        and isinstance(t1.args[1].args[0], sp.cos)
                        and isinstance(t2.args[1], sp.Pow)
                        and t2.args[1].func == sp.Pow
                        and t2.args[1].args[1] == 2
                        and isinstance(t2.args[1].args[0], sp.sin)
                    )
                )
            )
        ),
    ]

    for pattern in patterns:
        if pattern(term1, term2):
            # Extrahiere den Koeffizienten (falls vorhanden)
            if isinstance(term1, sp.Mul):
                koeffizient = term1.args[0]
            else:
                koeffizient = 1
            return koeffizient

    return expr


def _erkenne_quotientenstruktur(expr: sp.Basic) -> tuple[bool, sp.Basic, sp.Basic]:
    """
    Prüft, ob es sich um einen Quotienten handelt und gibt (ist_quotient, zaehler, nenner) zurück.
    """
    if expr.func == sp.Pow and len(expr.args) == 2:
        # Einfache negative Potenz wie x^(-1)
        base, exp = expr.args
        if exp == -1:
            return True, sp.Integer(1), base
    elif expr.func == sp.Mul:
        # Komplexere Quotientenstruktur suchen
        zaehler_faktoren = []
        nenner_faktoren = []

        for arg in expr.args:
            if arg.func == sp.Pow and len(arg.args) == 2:
                base, exp = arg.args
                if hasattr(exp, "is_negative") and exp.is_negative:
                    # Negativer Exponent -> in den Nenner
                    nenner_faktoren.append(sp.Pow(base, -exp))  # type: ignore
                else:
                    zaehler_faktoren.append(arg)
            else:
                zaehler_faktoren.append(arg)

        if nenner_faktoren:
            zaehler = sp.Mul(*zaehler_faktoren) if zaehler_faktoren else sp.Integer(1)
            nenner = sp.Mul(*nenner_faktoren) if nenner_faktoren else sp.Integer(1)
            return True, zaehler, nenner

    return False, expr, sp.Integer(1)


def analysiere_funktionsstruktur(
    funktion: str | sp.Basic | Funktion,
) -> dict[str, Any]:
    """
    Analysiert die Struktur einer Funktion und gibt detaillierte Informationen zurück.

    Args:
        funktion: Zu analysierende Funktion

    Returns:
        Dictionary mit Strukturinformationen

    Examples:
        >>> ergebnis = analysiere_funktionsstruktur("(x+1)*sin(x)")
        >>> print(ergebnis['struktur'])
        'produkt'
    """
    try:
        # Konvertiere zu SymPy-Ausdruck
        if isinstance(funktion, Funktion):
            expr = funktion.term_sympy
            variable = funktion._variable_symbol
        elif isinstance(funktion, str):
            expr = sp.sympify(funktion, rational=True)
            # Finde die Variable automatisch
            freie_variablen = expr.free_symbols
            if len(freie_variablen) == 1:
                variable = next(iter(freie_variablen))
            else:
                variable = sp.symbols("x")  # Standardvariable
        else:
            expr = funktion
            freie_variablen = expr.free_symbols
            if len(freie_variablen) == 1:
                variable = next(iter(freie_variablen))
            else:
                variable = sp.symbols("x")

        # Hauptstruktur erkennen - PRIORISIERE POLYNOMIALE FUNKTIONEN
        haupt_typ = FunktionsTyp.UNBEKANNT
        komponenten = []

        # Schritt 1: Prüfe zuerst, ob es ein Polynom ist (wichtig für pädagogische Analyse)
        if (
            hasattr(expr, "is_polynomial")
            and callable(expr.is_polynomial)
            and expr.is_polynomial(variable)
        ):  # type: ignore
            # Unterscheide zwischen echten Polynomen und Konstanten
            try:
                if (
                    hasattr(expr, "is_constant")
                    and callable(expr.is_constant)
                    and expr.is_constant()
                ):  # type: ignore
                    haupt_typ = FunktionsTyp.KONSTANTE
                    komponenten = [expr]
                elif isinstance(expr, (sp.Integer, sp.Float, sp.Rational)):
                    haupt_typ = FunktionsTyp.KONSTANTE
                    komponenten = [expr]
                else:
                    haupt_typ = FunktionsTyp.GANZRATIONAL
                    # Für Polynome: Behalte die expandierte Form für bessere Analyse
                    expr_analyse = expr.expand()  # type: ignore
                    if expr_analyse.func == sp.Add:
                        komponenten = list(expr_analyse.args)
                    else:
                        komponenten = [expr_analyse]
            except Exception:
                # Fallback auf ganzrational bei Fehlern
                haupt_typ = FunktionsTyp.GANZRATIONAL
                expr_analyse = expr.expand()  # type: ignore
                if expr_analyse.func == sp.Add:
                    komponenten = list(expr_analyse.args)
                else:
                    komponenten = [expr_analyse]
        else:
            # Schritt 2: Für nicht-polynomiale Funktionen, analysiere die Struktur
            # Verwende Originalausdruck um Struktur zu erhalten, ohne aggressive Vereinfachung
            expr_analyse = expr

            # Prüfe auf Quotientenstruktur
            ist_quotient, zaehler, nenner = _erkenne_quotientenstruktur(expr_analyse)
            if ist_quotient:
                haupt_typ = FunktionsTyp.QUOTIENT
                komponenten = [zaehler, nenner]
            # Prüfe auf verschiedene Strukturen
            elif expr_analyse.func == sp.Add:
                # Prüfe auf Pythagoreische Identität (einzige erlaubte trigonometrische Vereinfachung)
                vereinfacht = _vereinfache_pythagoreische_identitaet(expr_analyse)
                if vereinfacht != expr_analyse:
                    # Pythagoreische Identität erkannt und vereinfacht
                    if (
                        hasattr(vereinfacht, "is_constant")
                        and callable(vereinfacht.is_constant)
                        and vereinfacht.is_constant()  # type: ignore
                    ):
                        haupt_typ = FunktionsTyp.KONSTANTE
                        komponenten = [vereinfacht]
                    else:
                        haupt_typ = FunktionsTyp.KONSTANTE  # Koeffizient
                        komponenten = [vereinfacht]
                else:
                    haupt_typ = FunktionsTyp.SUMME
                    komponenten = list(expr_analyse.args)
            elif expr_analyse.func == sp.Mul:
                haupt_typ = FunktionsTyp.PRODUKT
                komponenten = list(expr_analyse.args)
            elif expr_analyse.func == sp.Pow:
                basis, exponent = expr_analyse.args
                if exponent == -1:
                    # Einfacher Kehrwert
                    haupt_typ = FunktionsTyp.QUOTIENT
                    komponenten = [sp.Integer(1), basis]
                else:
                    haupt_typ = FunktionsTyp.KOMPOSITION
                    komponenten = [basis, exponent]
            elif expr_analyse.func in (sp.sin, sp.cos, sp.tan, sp.cot):
                haupt_typ = FunktionsTyp.TRIGONOMETRISCH
                komponenten = list(expr_analyse.args)
            elif expr_analyse.func == sp.exp:
                haupt_typ = FunktionsTyp.EXPONENTIELL
                komponenten = list(expr_analyse.args)
            elif expr_analyse.func in (sp.log, sp.ln):
                haupt_typ = FunktionsTyp.LOGARITHMISCH
                komponenten = list(expr_analyse.args)
            else:
                # Einfache Funktion
                haupt_typ = _klassifiziere_einfache_funktion(expr_analyse, variable)
                komponenten = [expr_analyse]

        # Komponenten detailliert analysieren
        detaillierte_komponenten = []
        for komp in komponenten:
            komp_typ = _klassifiziere_einfache_funktion(komp, variable)
            detaillierte_komponenten.append(
                {
                    "ausdruck": komp,
                    "typ": komp_typ.value,
                    "term": str(komp),
                    "latex": sp.latex(komp),
                }
            )

        # Zusätzliche Informationen sammeln
        ergebnis = {
            "original_term": str(expr),
            "struktur": haupt_typ.value,
            "komponenten": detaillierte_komponenten,
            "variable": str(variable),
            "latex": sp.latex(expr),
            "kann_faktorisiert_werden": False,
        }

        # Prüfen, ob Faktorisierung sinnvoll ist
        if haupt_typ == FunktionsTyp.GANZRATIONAL:
            try:
                faktorisiert = sp.factor(expr)
                if faktorisiert != expr and isinstance(faktorisiert, sp.Mul):
                    ergebnis["kann_faktorisiert_werden"] = True
                    ergebnis["faktoren"] = [str(f) for f in faktorisiert.args]
            except Exception:
                pass

        return ergebnis

    except Exception as e:
        raise StrukturAnalyseError(
            f"Konnte die Funktion '{funktion}' nicht analysieren: {e}"
        )


def erstelle_strukturierte_funktion(
    funktion: str | sp.Basic | Funktion,
) -> Funktion:
    """
    Erstellt eine Funktion mit erkannter Struktur.

    Args:
        funktion: Zu analysierende Funktion

    Returns:
        Funktion mit Strukturinformationen
    """
    # Führe die Strukturanalyse durch
    struktur_info = analysiere_funktionsstruktur(funktion)

    # Erstelle die Basisfunktion
    if isinstance(funktion, Funktion):
        basis_funktion = funktion
    else:
        basis_funktion = Funktion(funktion)

    # Speichere Strukturinformationen in der Funktion
    basis_funktion._struktur_info = struktur_info

    return basis_funktion


def teste_strukturanalyse():
    """Testfunktion zur Demonstration der Strukturanalyse."""
    test_funktionen = [
        "(x+1)*sin(x)",
        "(x**2+1)/(x**3+4*x)",
        "x + sin(x)",
        "x**3 - x",
        "exp(x**2)",
        "sin(x)**2 + cos(x)**2",
        "1/x",
        "x**2 + 2*x + 1",
    ]

    for func_str in test_funktionen:
        print(f"\\n=== {func_str} ===")
        try:
            ergebnis = analysiere_funktionsstruktur(func_str)
            print(f"Struktur: {ergebnis['struktur']}")
            print(f"Komponenten: {[k['term'] for k in ergebnis['komponenten']]}")
            if ergebnis.get("kann_faktorisiert_werden"):
                print(f"Faktoren: {ergebnis['faktoren']}")
        except Exception as e:
            print(f"Fehler: {e}")


if __name__ == "__main__":
    teste_strukturanalyse()
