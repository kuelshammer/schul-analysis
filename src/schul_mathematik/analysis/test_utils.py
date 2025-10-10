"""
Test-Hilfsfunktionen für das Schul-Analysis Framework

Diese Datei stellt nützliche Hilfsfunktionen für Tests bereit, insbesondere
für den Vergleich von mathematischen Ausdrücken.

Die Funktionen sind optimiert für den Schulunterricht und verwenden exakte
symbolische Berechnungen mit SymPy.
"""

import sympy as sp

from .funktion import Funktion


def assert_gleich(
    ausdruck1: str | sp.Basic | Funktion | float | int,
    ausdruck2: str | sp.Basic | Funktion | float | int,
    variable: str = "x",
    nachricht: str | None = None,
):
    """
    Überprüft, ob zwei mathematische Ausdrücke äquivalent sind.

    Diese Funktion ist viel robuster als direkter Vergleich, da sie:
    - SymPy-Ausdrücke korrekt vereinfacht
    - Algebraische Äquivalenz erkennt (x^2 - 1 vs (x-1)(x+1))
    - Verschiedene Darstellungen desselben Ausdrucks erkennt

    Args:
        ausdruck1: Erster Ausdruck als String, SymPy-Basic, Funktion oder Zahl
        ausdruck2: Zweiter Ausdruck als String, SymPy-Basic, Funktion oder Zahl
        variable: Variable, die für die Vereinfachung verwendet wird (Standard: "x")
        nachricht: Optionale Fehlermeldung

    Raises:
        AssertionError: Wenn die Ausdrücke nicht äquivalent sind

    Examples:
        >>> assert_gleich("x^2 - 1", "(x-1)*(x+1)")
        # Bestehen (algebraisch äquivalent)
        >>> assert_gleich("2*x + 4", "2*(x + 2)")
        # Bestehen (vereinfacht gleich)
        >>> assert_gleich("sin(x)^2 + cos(x)^2", "1")
        # Bestehen (trigonometrische Identität)
        >>> assert_gleich("x + 1", "x + 2")
        # AssertionError: Ausdrücke nicht äquivalent
    """
    try:
        # Konvertiere beide Ausdrücke zu SymPy-Basic
        expr1 = _konvertiere_zu_sympy(ausdruck1, variable)
        expr2 = _konvertiere_zu_sympy(ausdruck2, variable)

        # Berechne die Differenz und vereinfache
        differenz = sp.simplify(expr1 - expr2)  # type: ignore

        # Prüfe, ob die Differenz Null ist
        if differenz != 0:
            if nachricht is None:
                nachricht = f"Ausdrücke nicht äquivalent: '{ausdruck1}' ≠ '{ausdruck2}'"
            raise AssertionError(nachricht)

    except Exception as e:
        # Bei Fehlern in der symbolischen Berechnung
        if nachricht is None:
            nachricht = f"Fehler beim Vergleich: {str(e)}"
        raise AssertionError(nachricht)


def assert_wert_gleich(
    funktion: Funktion,
    x_wert: float,
    erwarteter_wert: float,
    toleranz: float | None = None,
):
    """
    Überprüft, ob ein Funktionswert dem erwarteten Wert entspricht.

    Args:
        funktion: Zu testende Funktion
        x_wert: x-Wert für die Auswertung
        erwarteter_wert: Erwarteter Funktionswert
        toleranz: Optionale Toleranz für numerische Vergleiche.
                  Wenn None, wird exakter Vergleich verwendet.

    Raises:
        AssertionError: Wenn der Funktionswert nicht übereinstimmt

    Examples:
        >>> f = Funktion("x^2")
        >>> assert_wert_gleich(f, 3, 9)  # Exakter Vergleich
        # Bestehen
        >>> assert_wert_gleich(f, 3, 9.000001, toleranz=1e-5)  # Mit Toleranz
        # Bestehen
        >>> assert_wert_gleich(f, 3, 10)
        # AssertionError: f(3) = 9, aber 10 erwartet
    """
    try:
        actual = funktion.wert(x_wert)

        # Konvertiere zu float für Vergleich
        if hasattr(actual, "evalf"):
            actual_float = float(actual.evalf())
        else:
            actual_float = float(actual)

        if toleranz is None:
            # Exakter Vergleich
            if actual_float != erwarteter_wert:
                raise AssertionError(
                    f"f({x_wert}) = {actual_float}, aber exakt {erwarteter_wert} erwartet"
                )
        else:
            # Vergleich mit Toleranz
            if abs(actual_float - erwarteter_wert) > toleranz:
                raise AssertionError(
                    f"f({x_wert}) = {actual_float}, aber {erwarteter_wert} erwartet "
                    f"(Toleranz: ±{toleranz})"
                )

    except Exception as e:
        raise AssertionError(f"Fehler bei der Auswertung: {e}")


def _konvertiere_zu_sympy(
    ausdruck: str | sp.Basic | Funktion | float | int, variable: str
) -> sp.Basic:
    """Konvertiert verschiedene Eingabetypen zu SymPy-Basic"""

    if isinstance(ausdruck, sp.Basic):
        return ausdruck

    elif isinstance(ausdruck, Funktion):
        return ausdruck.term_sympy

    elif isinstance(ausdruck, (int, float)):
        return sp.Number(ausdruck)

    elif isinstance(ausdruck, str):
        # Erweiterte Schul-Mathematik-Syntax-Unterstützung
        import re
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations

        # Ersetze ^ mit ** für SymPy
        bereinigt = ausdruck.replace("^", "**")

        # Wende Regex-Transformationen an, bevor parse_expr verwendet wird
        # Implizite Multiplikation: 2x -> 2*x
        bereinigt = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", bereinigt)
        # x2 -> x*2 (nicht so häufig, aber manchmal von Schülern verwendet)
        bereinigt = re.sub(r"([a-zA-Z])(\d)", r"\1*\2", bereinigt)
        # (x+1)x -> (x+1)*x
        bereinigt = re.sub(r"(\))([a-zA-Z])", r"\1*\2", bereinigt)

        # x(x+1) -> x*(x+1) - aber nur für einfache Fälle, nicht für Funktionsaufrufe
        # Ersetze nur, wenn es sich nicht um bekannte Funktionsnamen handelt
        bekannte_funktionen = ["sin", "cos", "tan", "exp", "log", "sqrt", "abs"]
        for func in bekannte_funktionen:
            # Schütze Funktionsaufrufe vor der Transformation
            bereinigt = bereinigt.replace(f"{func}(", f"__{func}__(")

        # Wende die Transformation an
        bereinigt = re.sub(r"([a-zA-Z])\(", r"\1*(", bereinigt)

        # Stelle Funktionsaufrufe wieder her
        for func in bekannte_funktionen:
            bereinigt = bereinigt.replace(f"__{func}(", f"{func}(")

        # Versuche, den Ausdruck zu parsen
        try:
            return parse_expr(bereinigt, transformations=standard_transformations)
        except Exception as e:
            # Fallback: Versuche mit standard sympify
            try:
                return sp.sympify(bereinigt, locals={variable: x})
            except Exception:
                # Letzter Versuch: ohne spezielle Locals
                try:
                    return sp.sympify(bereinigt)
                except Exception as e2:
                    raise ValueError(
                        f"Konnte Ausdruck '{ausdruck}' nicht parsen. "
                        f"Original-Fehler: {e}. Fallback-Fehler: {e2}"
                    )

    else:
        raise TypeError(f"Unbekannter Ausdruckstyp: {type(ausdruck)}")
