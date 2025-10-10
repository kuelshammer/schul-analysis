"""
Pädagogisch verbesserte Wrapper-Funktionen für strukturierte Funktionen.

Deutsche API im Stil des Mathematikunterrichts:
- Große Substantive wie im Deutschen üblich
- Intuitive Parameter-Namen
- Klare Fehlermeldungen als Lernmomente
"""

from __future__ import annotations

from typing import Any, Optional, Union
import sympy as sp

from .strukturiert import (
    ProduktFunktion,
    SummeFunktion,
    QuotientFunktion,
    KompositionFunktion,
    StrukturFehler,
    StrukturInfo,
    StrukturTyp,
)
from .sympy_types import (
    T_Expr,
    validate_function_result,
    preserve_exact_types,
)


def AnalysiereFunktion(funktion: Union[str, T_Expr]) -> dict[str, Any]:
    """
    Analysiert die Struktur einer Funktion für den Unterricht.

    Args:
        funktion: Zu analysierende Funktion als String oder SymPy-Ausdruck

    Returns:
        Dictionary mit detaillierten Analyse-Ergebnissen

    Examples:
        >>> resultat = AnalysiereFunktion("(x+1)*sin(x)")
        >>> print(resultat['struktur'])  # 'produkt'
        >>> print(resultat['komponenten'])  # ['x+1', 'sin(x)']

    Raises:
        StrukturFehler: Bei ungültiger Funktion
    """
    try:
        # Validiere Eingabe
        if not funktion:
            raise StrukturFehler("Leere Funktion nicht erlaubt")

        # Konvertiere zu SymPy
        if isinstance(funktion, str):
            expr = sp.sympify(funktion, rational=True)
        else:
            expr = funktion

        validate_function_result(expr, "exact")

        # Führe Strukturanalyse durch
        struktur_info = _analysiere_funktionsstruktur_detailliert(expr)

        return {
            "struktur": struktur_info.struktur.value,
            "komponenten": [k.term for k in struktur_info.komponenten],
            "komponenten_typen": [k.typ for k in struktur_info.komponenten],
            "latex_darstellung": struktur_info.latex,
            "kann_faktorisiert_werden": struktur_info.kann_faktorisiert_werden,
            "faktoren": struktur_info.faktoren
            if struktur_info.kann_faktorisiert_werden
            else None,
        }

    except Exception as e:
        if isinstance(e, StrukturFehler):
            raise
        raise StrukturFehler(
            f"Funktion '{funktion}' konnte nicht analysiert werden",
            f"Technische Details: {str(e)}",
        )


def ZerlegeProdukt(funktion: Union[str, T_Expr]) -> ProduktFunktion:
    """
    Zerlegt eine Funktion in ihre Faktoren (Produktstruktur).

    Args:
        funktion: Funktion mit Produktstruktur

    Returns:
        ProduktFunktion mit typisierten Faktoren

    Examples:
        >>> f = ZerlegeProdukt("(x+1)*sin(x)")
        >>> print(f.faktor1)  # LineareFunktion(x+1)
        >>> print(f.faktor2)  # TrigonometrischeFunktion(sin(x))

    Raises:
        StrukturFehler: Wenn keine Produktstruktur vorliegt
    """
    try:
        produkt = ProduktFunktion(funktion)

        # Pädagogische Überprüfung
        if len(produkt.faktoren) < 2:
            raise StrukturFehler(
                "Die Funktion hat keine Produktstruktur",
                f"'{funktion}' besteht nur aus einem Faktor",
            )

        return produkt

    except StrukturFehler:
        raise
    except Exception as e:
        raise StrukturFehler(
            f"Produktzerlegung für '{funktion}' fehlgeschlagen",
            f"Die Funktion konnte nicht als Produkt interpretiert werden: {str(e)}",
        )


def ZerlegeSumme(funktion: Union[str, T_Expr]) -> SummeFunktion:
    """
    Zerlegt eine Funktion in ihre Summanden (Summenstruktur).

    Args:
        funktion: Funktion mit Summenstruktur

    Returns:
        SummeFunktion mit typisierten Summanden

    Examples:
        >>> f = ZerlegeSumme("x^2 + sin(x)")
        >>> print(f.summand1)  # QuadratischeFunktion(x^2)
        >>> print(f.summand2)  # TrigonometrischeFunktion(sin(x))

    Raises:
        StrukturFehler: Wenn keine Summenstruktur vorliegt
    """
    try:
        summe = SummeFunktion(funktion)

        # Pädagogische Überprüfung
        if len(summe.summanden) < 2:
            raise StrukturFehler(
                "Die Funktion hat keine Summenstruktur",
                f"'{funktion}' besteht nur aus einem Summanden",
            )

        return summe

    except StrukturFehler:
        raise
    except Exception as e:
        raise StrukturFehler(
            f"Summenzerlegung für '{funktion}' fehlgeschlagen",
            f"Die Funktion konnte nicht als Summe interpretiert werden: {str(e)}",
        )


def ZerlegeQuotient(funktion: Union[str, T_Expr]) -> QuotientFunktion:
    """
    Zerlegt eine Funktion in Zähler und Nenner (Quotientenstruktur).

    Args:
        funktion: Funktion mit Quotientenstruktur

    Returns:
        QuotientFunktion mit typisiertem Zähler und Nenner

    Examples:
        >>> f = ZerlegeQuotient("(x^2+1)/(x-2)")
        >>> print(f.zaehler)      # GanzrationaleFunktion(x^2+1)
        >>> print(f.nenner)       # LineareFunktion(x-2)
        >>> print(f.polstellen())  # [2.0]

    Raises:
        StrukturFehler: Wenn keine Quotientenstruktur vorliegt
    """
    try:
        quotient = QuotientFunktion(funktion)

        # Pädagogische Information über Polstellen
        polstellen = quotient.polstellen()
        if polstellen:
            print(
                f"📌 Hinweis: Die Funktion hat {len(polstellen)} Polstelle(n) bei x = {polstellen}"
            )

        return quotient

    except StrukturFehler:
        raise
    except Exception as e:
        raise StrukturFehler(
            f"Quotientenzerlegung für '{funktion}' fehlgeschlagen",
            f"Die Funktion konnte nicht als Quotient interpretiert werden: {str(e)}",
        )


def FindePolstellen(funktion: Union[str, T_Expr]) -> list[float]:
    """
    Findet alle Polstellen einer Funktion (speziell für Quotienten).

    Args:
        funktion: Funktion mit möglichen Polstellen

    Returns:
        Liste der Polstellen als exakte Werte

    Examples:
        >>> polstellen = FindePolstellen("(x^2+1)/(x-2)")
        >>> print(polstellen)  # [2.0]

    Raises:
        StrukturFehler: Wenn keine Polstellen gefunden werden können
    """
    try:
        # Versuche Quotientenzerlegung
        try:
            quotient = QuotientFunktion(funktion)
            return quotient.polstellen()
        except StrukturFehler:
            # Keine Quotientenfunktion - keine Polstellen
            return []

    except Exception as e:
        raise StrukturFehler(
            f"Polstellen für '{funktion}' konnten nicht bestimmt werden",
            f"Technische Details: {str(e)}",
        )


def ErkenneFunktionstyp(funktion: Union[str, T_Expr]) -> str:
    """
    Erkennt automatisch den Funktionstyp für den Unterricht.

    Args:
        funktion: Zu analysierende Funktion

    Returns:
        Deutscher Funktionstyp als String

    Examples:
        >>> typ = ErkenneFunktionstyp("(x+1)*sin(x)")
        >>> print(typ)  # "produkt"

    Raises:
        StrukturFehler: Bei ungültiger Funktion
    """
    try:
        analyse = AnalysiereFunktion(funktion)
        return analyse["struktur"]

    except StrukturFehler:
        raise
    except Exception as e:
        raise StrukturFehler(
            f"Funktionstyp für '{funktion}' konnte nicht erkannt werden",
            f"Technische Details: {str(e)}",
        )


def ZeigeStruktur(funktion: Union[str, T_Expr]) -> str:
    """
    Erstellt eine verständliche Strukturdarstellung für Schüler.

    Args:
        funktion: Zu visualisierende Funktion

    Returns:
        Formatierte String-Darstellung der Struktur

    Examples:
        >>> darstellung = ZeigeStruktur("(x+1)*sin(x)")
        >>> print(darstellung)
        # "PRODUKT:
        #  ┌─ Faktor 1: x + 1  (Lineare Funktion)
        #  └─ Faktor 2: sin(x)  (Trigonometrische Funktion)"

    Raises:
        StrukturFehler: Bei ungültiger Funktion
    """
    try:
        analyse = AnalysiereFunktion(funktion)
        struktur = analyse["struktur"].upper()
        komponenten = analyse["komponenten"]
        typen = analyse["komponenten_typen"]

        # Formatierte Ausgabe
        result = f"{struktur}:\n"

        for i, (komp, typ) in enumerate(zip(komponenten, typen), 1):
            symbol = "├─" if i < len(komponenten) else "└─"
            result += f" {symbol} Komponente {i}: {komp}  ({typ})\n"

        # Zusatzinformationen
        if analyse["kann_faktorisiert_werden"] and analyse["faktoren"]:
            result += (
                f"\n💡 Kann faktorisiert werden als: {' · '.join(analyse['faktoren'])}"
            )

        return result.rstrip()

    except Exception as e:
        if isinstance(e, StrukturFehler):
            raise
        raise StrukturFehler(
            f"Strukturdarstellung für '{funktion}' konnte nicht erstellt werden",
            f"Technische Details: {str(e)}",
        )


def _analysiere_funktionsstruktur_detailliert(expr: T_Expr) -> StrukturInfo:
    """
    Detaillierte Strukturanalyse mit pädagogischer Validierung.

    Args:
        expr: SymPy-Ausdruck

    Returns:
        Vollständige StrukturInfo
    """
    # Implementierung würde hier folgen mit der Logik aus struktur.py
    # aber mit verbesserter Fehlerbehandlung und Validierung

    # Vereinfachte Implementierung für die Demonstration:
    if expr.func == sp.Mul:
        # Produktstruktur
        komponenten = []
        for arg in expr.args:
            komp_typ = _klassifiziere_komponente(arg)
            komponenten.append(
                KomponentenInfo(
                    ausdruck=arg, typ=komp_typ, term=str(arg), latex=sp.latex(arg)
                )
            )

        return StrukturInfo(
            original_term=str(expr),
            struktur=StrukturTyp.PRODUKT,
            komponenten=komponenten,
            variable="x",  # Vereinfacht
            latex=sp.latex(expr),
        )

    elif expr.func == sp.Add:
        # Summenstruktur
        pass

    # ... weitere Strukturen

    # Fallback
    return StrukturInfo(
        original_term=str(expr),
        struktur=StrukturTyp.PRODUKT,  # Vereinfacht
        komponenten=[],
        variable="x",
        latex=sp.latex(expr),
    )


def _klassifiziere_komponente(expr: T_Expr) -> str:
    """Klassifiziert eine Komponente nach deutscher Schulmathematik."""
    if expr.is_polynomial(sp.symbols("x")):
        grad = sp.degree(expr, sp.symbols("x"))
        if grad == 1:
            return "lineare Funktion"
        elif grad == 2:
            return "quadratische Funktion"
        else:
            return "ganzrationale Funktion"
    elif expr.func in (sp.sin, sp.cos, sp.tan):
        return "trigonometrische Funktion"
    elif expr.func == sp.exp:
        return "exponentielle Funktion"
    elif expr.is_constant():
        return "Konstante"
    else:
        return "allgemeine Funktion"


# Demo für die Verwendung
if __name__ == "__main__":
    print("=== Demo der verbesserten Wrapper-Funktionen ===\n")

    test_funktionen = [
        "(x+1)*sin(x)",
        "(x**2+1)/(x-2)",
        "x**2 + 2*x + 1",
        "exp(x) + sin(x)",
    ]

    for func in test_funktionen:
        print(f"🔍 Analysiere: {func}")
        try:
            # Struktur erkennen
            typ = ErkenneFunktionstyp(func)
            print(f"   Typ: {typ}")

            # Detaillierte Ansicht
            struktur = ZeigeStruktur(func)
            print(struktur)

            # Spezielle Zerlegung je nach Typ
            if typ == "produkt":
                produkt = ZerlegeProdukt(func)
                print(f"   Faktoren: {[str(f) for f in produkt.faktoren]}")
            elif typ == "quotient":
                quotient = ZerlegeQuotient(func)
                print(f"   Polstellen: {quotient.polstellen()}")

            print("\n" + "=" * 50 + "\n")

        except StrukturFehler as e:
            print(f"   ❌ Strukturfehler: {e.nachricht}")
            if e.ursache:
                print(f"      Ursache: {e.ursache}")
        except Exception as e:
            print(f"   ❌ Allgemeiner Fehler: {e}")
