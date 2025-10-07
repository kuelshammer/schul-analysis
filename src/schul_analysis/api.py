"""
Schülerfreundliche API für das Schul-Analysis Framework

Diese Datei stellt Wrapper-Funktionen bereit, die eine intuitive,
unterrichtsnahe Syntax ermöglichen: Nullstellen(f) statt f.nullstellen()

Alle Funktionen unterstützen Duck-Typing und funktionieren mit allen
verfügbaren Funktionstypen (ganzrational, gebrochen rational, etc.)
"""

from typing import Any

import numpy as np

from .errors import SchulAnalysisError, UngueltigeFunktionError

# Importiere alle verfügbaren Funktionstypen
from .ganzrationale import GanzrationaleFunktion
from .strukturiert import (
    KompositionFunktion,
    ProduktFunktion,
    QuotientFunktion,
    SummeFunktion,
)
from .lineare_gleichungssysteme import LGS

# Type Hint für alle unterstützten Funktionstypen
Funktionstyp = (
    GanzrationaleFunktion
    | QuotientFunktion
    | ProduktFunktion
    | SummeFunktion
    | KompositionFunktion
)


# =============================================================================
# WRAPPER-FUNKTIONEN FÜR ANALYSE (unterrichtsnahe Syntax)
# =============================================================================


def nullstellen(
    funktion: Funktionstyp, real: bool = True, runden: int | None = None
) -> list[Any]:
    """
    Berechnet die Nullstellen einer Funktion.

    Args:
        funktion: Eine beliebige Funktion (ganzrational, gebrochen rational, etc.)
        real: Nur reelle Nullstellen zurückgeben (Standard: True)
        runden: Anzahl Nachkommastellen für Rundung (None = exakt)

    Returns:
        Liste der Nullstellen

    Beispiele:
        >>> f = erstelle_polynom([1, -4, 3])  # x² - 4x + 3
        >>> xs = nullstellen(f)                 # [1.0, 3.0]

    Didaktischer Hinweis:
        Diese Funktion ermöglicht die natürliche mathematische Notation,
        die Schüler aus dem Unterricht kennen: "Berechne die Nullstellen von f"
    """
    try:
        # Handle both property and method cases
        if hasattr(funktion, "nullstellen"):
            attr = funktion.nullstellen
            if callable(attr):
                # It's a method - try with parameters first
                try:
                    return funktion.nullstellen(real=real, runden=runden)
                except TypeError:
                    # Method doesn't accept parameters, call without them
                    result = funktion.nullstellen()
            else:
                # It's a property - access it directly
                result = funktion.nullstellen
                # Apply filtering and rounding if needed
                if real:
                    result = [n for n in result if hasattr(n, "is_real") and n.is_real]
                if runden is not None:
                    result = [
                        round(float(n), runden) if hasattr(n, "__float__") else n
                        for n in result
                    ]
                return result
        else:
            raise AttributeError("Keine nullstellen Eigenschaft oder Methode gefunden")
    except AttributeError:
        raise UngueltigeFunktionError(
            "Nullstellenberechnung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "unterstützt die Nullstellen-Berechnung nicht.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Nullstellenberechnung: {str(e)}")


def ableitung(funktion: Funktionstyp, ordnung: int = 1) -> Any:
    """
    Berechnet die Ableitung einer Funktion.

    Args:
        funktion: Eine beliebige Funktion
        ordnung: Ordnung der Ableitung (Standard: 1)

    Returns:
        Die abgeleitete Funktion

    Beispiele:
        >>> f = erstelle_polynom([1, -4, 3])  # x² - 4x + 3
        >>> f1 = ableitung(f, 1)             # 2x - 4
        >>> f2 = ableitung(f, 2)             # 2

    Didaktischer Hinweis:
        Diese Notation ist näher an der mathematischen Schreibweise f'(x)
        und für Schüler intuitiver verständlich.
    """
    try:
        return funktion.ableitung(ordnung)
    except AttributeError:
        raise UngueltigeFunktionError(
            "Ableitung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "kann nicht abgeleitet werden.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Ableitungsberechnung: {str(e)}")


def integral(funktion: Funktionstyp, ordnung: int = 1) -> Any:
    """
    Berechnet das Integral einer Funktion.

    Args:
        funktion: Eine beliebige Funktion
        ordnung: Ordnung des Integrals (Standard: 1)

    Returns:
        Die integrierte Funktion

    Beispiele:
        >>> f = erstelle_polynom([1, 0, 0])  # x²
        >>> F = integral(f, 1)              # (1/3)x³
    """
    try:
        return funktion.integral(ordnung)
    except AttributeError:
        raise UngueltigeFunktionError(
            "Integration",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "kann nicht integriert werden.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Integrationsberechnung: {str(e)}")


def extrema(funktion: Funktionstyp) -> list[tuple[Any, str]]:
    """
    Findet die Extrempunkte einer Funktion.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Liste der Extrempunkte als (x-Wert, Typ)-Tupel

    Beispiele:
        >>> f = erstelle_polynom([1, -3, -4, 12])  # x³ - 3x² - 4x + 12
        >>> ext = extrema(f)                       # [(-1, 'Maximum'), ...]
    """
    try:
        return funktion.extremstellen()
    except AttributeError:
        raise UngueltigeFunktionError(
            "Extremwertberechnung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "unterstützt keine Extrema-Berechnung.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Extrema-Berechnung: {str(e)}")


def wendepunkte(funktion: Funktionstyp) -> list[tuple[Any, str]]:
    """
    Findet die Wendepunkte einer Funktion.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Liste der Wendepunkte als (x-Wert, Typ)-Tupel

    Beispiele:
        >>> f = erstelle_polynom([1, 0, 0, 0])  # x³
        >>> wp = wendepunkte(f)                 # [(0, 'Wendepunkt')]
    """
    try:
        return funktion.wendepunkte()
    except AttributeError:
        raise UngueltigeFunktionError(
            "Wendepunkteberechnung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "unterstützt keine Wendepunkte-Berechnung.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Wendepunkte-Berechnung: {str(e)}")


def symmetrie(funktion: Funktionstyp) -> str:
    """
    Bestimmt die Symmetrie einer Funktion.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Beschreibung der Symmetrie

    Beispiele:
        >>> f = erstelle_polynom([1, 0, 0])      # x²
        >>> sym = symmetrie(f)                   # "Achsensymmetrisch zur y-Achse"
    """
    try:
        # Versuche zuerst die symmetrie() Methode
        return funktion.symmetrie()
    except AttributeError:
        # Fallback: Prüfe auf alte syme property
        try:
            return funktion.syme
        except AttributeError:
            raise UngueltigeFunktionError(
                "Symmetrieanalyse",
                f"Die Funktion vom Typ '{type(funktion).__name__}' "
                "unterstützt keine Symmetrie-Analyse.",
            )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Symmetrie-Analyse: {str(e)}")


# =============================================================================
# VISUALISIERUNGS-FUNKTIONEN
# =============================================================================


def zeichne(
    funktion: Any,
    x_bereich: tuple[float, float] | None = None,
    y_bereich: tuple[float, float] | None = None,
    **kwargs,
) -> Any:
    """
    Zeichnet eine Funktion im gegebenen Bereich.

    Args:
        funktion: Eine beliebige Funktion (auch Python-Funktionen)
        x_bereich: x-Bereich als (von, bis) - Standard: automatisch
        y_bereich: y-Bereich als (von, bis) - Standard: automatisch
        **kwargs: Zusätzliche Parameter für die Visualisierung

    Returns:
        Interaktiver Plotly-Graph

    Beispiele:
        >>> f = erstelle_polynom([1, -4, 3])  # x² - 4x + 3
        >>> zeichne(f, (-2, 6))               # Zeichnet Funktion von x=-2 bis x=6

        # Auch mit normalen Python-Funktionen möglich:
        >>> zeichne(lambda x: x**2, (-5, 5))
    """
    try:
        # Versuche zuerst die graph() Methode (neue API)
        if hasattr(funktion, "graph"):
            if x_bereich:
                kwargs["x_min"] = x_bereich[0]
                kwargs["x_max"] = x_bereich[1]
            if y_bereich:
                kwargs["y_min"] = y_bereich[0]
                kwargs["y_max"] = y_bereich[1]
            return funktion.graph(**kwargs)

        # Fallback: zeige_funktion Methode (alte API)
        elif hasattr(funktion, "zeige_funktion"):
            if x_bereich:
                return funktion.zeige_funktion(x_bereich, **kwargs)
            else:
                return funktion.zeige_funktion(**kwargs)

        # Fallback für beliebige callable Objekte
        elif callable(funktion):
            from .visualisierung import zeige_funktion

            return zeige_funktion(funktion, x_bereich, **kwargs)
        else:
            raise TypeError("Das übergebene Objekt ist keine zeichnenbare Funktion.")

    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Visualisierung: {str(e)}")


# =============================================================================
# WERTEBERECHNUNG
# =============================================================================


def auswerten(funktion: Any, x_wert: float | np.ndarray) -> float | np.ndarray:
    """
    Wertet eine Funktion an einem Punkt oder Array aus.

    Args:
        funktion: Eine beliebige Funktion
        x_wert: Der x-Wert oder Array von x-Werten

    Returns:
        Der y-Wert oder Array von y-Werten

    Beispiele:
        >>> f = erstelle_polynom([1, -4, 3])  # x² - 4x + 3
        >>> y = auswerten(f, 2)               # f(2) = -1
        >>> y_array = auswerten(f, [1, 2, 3]) # [f(1), f(2), f(3)] = [0, -1, 0]
    """
    try:
        return funktion(x_wert)
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Auswertung: {str(e)}")


# =============================================================================
# HELPER-FUNKTIONEN FÜR SCHÜLER
# =============================================================================


def erstelle_polynom(koeffizienten: list[float | int]) -> "GanzrationaleFunktion":
    """
    Erstellt ein Polynom aus Koeffizienten.

    Args:
        koeffizienten: Liste der Koeffizienten [a₀, a₁, a₂, ...]
                     für a₀ + a₁x + a₂x² + ...

    Returns:
        Eine ganzrationale Funktion

    Beispiele:
        >>> f = erstelle_polynom([3, -4, 1])     # 3 - 4x + x²
        >>> g = erstelle_polynom([0, 1])        # x
        >>> h = erstelle_polynom([5])           # 5 (konstant)

    Didaktischer Hinweis:
        Diese Funktion ist besonders für Anfänger geeignet,
        da sie die Polynom-Erstellung sehr einfach macht.

    Magic Factory Hinweis:
        Alternativ kann jetzt auch Funktion("x^2 - 4x + 3") verwendet werden,
        was automatisch die richtige Funktionstyp zurückgibt.
    """
    from .funktion import Funktion

    # Erstelle String aus Koeffizienten und verwende Magic Factory
    if not koeffizienten:
        raise ValueError("Koeffizientenliste darf nicht leer sein")

    # Erstelle Term aus Koeffizienten
    termbestandteile = []
    for i, koeff in enumerate(koeffizienten):
        if koeff == 0:
            continue
        if i == 0:
            termbestandteile.append(str(koeff))
        elif i == 1:
            if koeff == 1:
                termbestandteile.append("x")
            elif koeff == -1:
                termbestandteile.append("-x")
            else:
                termbestandteile.append(f"{koeff}*x")
        else:
            if koeff == 1:
                termbestandteile.append(f"x^{i}")
            elif koeff == -1:
                termbestandteile.append(f"-x^{i}")
            else:
                termbestandteile.append(f"{koeff}*x^{i}")

    if not termbestandteile:
        term = "0"
    else:
        term = " + ".join(termbestandteile).replace("+ -", "- ")

    return Funktion(term)


def erstelle_funktion(term: str) -> Any:
    """
    Erstellt eine Funktion aus einem Term-String.

    Args:
        term: Der mathematische Term als String

    Returns:
        Eine Funktion (automatisch typisiert durch Magic Factory)

    Beispiele:
        >>> f = erstelle_funktion("x^2 - 4x + 3")    # x² - 4x + 3
        >>> g = erstelle_funktion("2*x + 5")          # 2x + 5
        >>> h = erstelle_funktion("(x-2)*(x+1)")     # (x-2)(x+1) = x² - x - 2
        >>> i = erstelle_funktion("x^2/(x+1)")      # QuotientFunktion!

    Didaktischer Hinweis:
        Unterstützt verschiedene Schreibweisen, die Schüler aus dem Unterricht kennen.

    Magic Factory Hinweis:
        Diese Funktion nutzt jetzt die Magic Factory und gibt automatisch den
        richtigen Funktionstyp zurück (QuadratischeFunktion, ProduktFunktion, etc.)
    """
    from .funktion import Funktion

    return Funktion(term)


def erstelle_lineares_gleichungssystem(
    koeffizienten: list[list[float | int]], ergebnisse: list[float | int]
) -> LGS:
    """
    Erstellt ein lineares Gleichungssystem.

    Args:
        koeffizienten: Matrix der Koeffizienten [[a₁₁, a₁₂], [a₂₁, a₂₂], ...]
        ergebnisse: Vektor der Ergebnisse [b₁, b₂, ...]

    Returns:
        Ein lineares Gleichungssystem

    Beispiele:
        >>> lgs = erstelle_lineares_gleichungssystem(
        ...     [[2, 3], [1, -2]],    # 2x + 3y = 8, x - 2y = -3
        ...     [8, -3]
        ... )
        >>> lösung = lgs.loese()        # [2, 1.333...]
    """
    return LGS(koeffizienten, ergebnisse)


def erstelle_exponential_rationale_funktion(
    zaehler: GanzrationaleFunktion | str,
    nenner: GanzrationaleFunktion | str,
    exponent_param: float = 1.0,
) -> Funktion:
    """
    Erstellt eine exponential-rationale Funktion f(x) = P(e^{ax})/Q(e^{ax}).

    Args:
        zaehler: Polynom in e^{ax} als GanzrationaleFunktion oder String
        nenner: Polynom in e^{ax} als GanzrationaleFunktion oder String
        exponent_param: Parameter a in e^{ax} (Standard: 1.0)

    Returns:
        ExponentialRationaleFunktion

    Beispiele:
        >>> f = erstelle_exponential_rationale_funktion("x+1", "x-1")
        >>> s = f.schmiegkurve()  # Schmiegkurve berechnen
        >>> r = f.stoerfunktion()  # Störfunktion berechnen
    """
    # 🔥 UNIFIED ARCHITECTURE FIX: Erstelle kombinierten Ausdruck statt separater Parameter 🔥
    if exponent_param == 1.0:
        # Für a=1: Standardfall e^x
        zaehler_expr = (
            zaehler.replace("x", "(exp(x)") if isinstance(zaehler, str) else zaehler
        )
        nenner_expr = (
            nenner.replace("x", "(exp(x)") if isinstance(nenner, str) else nenner
        )
    else:
        # Für a≠1: Ersetze x mit exp(a*x)
        replacement = f"(exp({exponent_param}*x)"
        zaehler_expr = (
            zaehler.replace("x", replacement) if isinstance(zaehler, str) else zaehler
        )
        nenner_expr = (
            nenner.replace("x", replacement) if isinstance(nenner, str) else nenner
        )

    # Kombiniere zu vollständigen Term
    if isinstance(zaehler_expr, str) and isinstance(nenner_expr, str):
        voller_term = f"({zaehler_expr})/({nenner_expr})"
    else:
        voller_term = f"({zaehler_expr})/({nenner_expr})"

    return Funktion(voller_term)


# =============================================================================
# KOMFORT-FUNKTIONEN FÜR DEN UNTERRICHT
# =============================================================================


def analysiere_funktion(funktion: Funktionstyp) -> dict[str, Any]:
    """
    Führt eine vollständige Funktionsanalyse durch.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Dictionary mit allen Analyse-Ergebnissen

    Beispiele:
        >>> f = erstelle_polynom([1, -4, 3])  # x² - 4x + 3
        >>> analyse = analysiere_funktion(f)
        >>> print(analyse['nullstellen'])      # [1.0, 3.0]
        >>> print(analyse['extrema'])           # []
        >>> print(analyse['symmetrie'])         # "Keine einfache Symmetrie"
    """
    ergebnisse = {}

    try:
        ergebnisse["term"] = funktion.term()
    except (AttributeError, ValueError, TypeError):
        ergebnisse["term"] = str(funktion)

    try:
        ergebnisse["nullstellen"] = nullstellen(funktion)
    except (AttributeError, ValueError, TypeError, ZeroDivisionError):
        ergebnisse["nullstellen"] = "Nicht berechenbar"

    try:
        ergebnisse["extrema"] = extrema(funktion)
    except (AttributeError, ValueError, TypeError, ZeroDivisionError):
        ergebnisse["extrema"] = "Nicht berechenbar"

    try:
        ergebnisse["wendepunkte"] = wendepunkte(funktion)
    except (AttributeError, ValueError, TypeError, ZeroDivisionError):
        ergebnisse["wendepunkte"] = "Nicht berechenbar"

    try:
        ergebnisse["symmetrie"] = symmetrie(funktion)
    except (AttributeError, ValueError, TypeError):
        ergebnisse["symmetrie"] = "Nicht bestimmbar"

    return ergebnisse


def zeige_analyse(funktion: Funktionstyp) -> str:
    """
    Erstellt eine übersichtliche Zusammenfassung der Funktionsanalyse.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Formatierter Text mit allen Analyse-Ergebnissen

    Beispiele:
        >>> f = erstelle_polynom([1, -4, 3])
        >>> print(zeige_analyse(f))
        Funktionsanalyse für f(x) = x^2 - 4x + 3

        Nullstellen: [1.0, 3.0]
        Extrema: []
        Wendepunkte: []
        Symmetrie: Keine einfache Symmetrie
    """
    analyse = analysiere_funktion(funktion)

    text = f"Funktionsanalyse für f(x) = {analyse['term']}\n\n"

    text += f"Nullstellen: {analyse['nullstellen']}\n"
    text += f"Extrema: {analyse['extrema']}\n"
    text += f"Wendepunkte: {analyse['wendepunkte']}\n"
    text += f"Symmetrie: {analyse['symmetrie']}"

    return text


# =============================================================================
# EXPORT: ALLE FUNKTIONEN, DIE IMPORTIERT WERDEN SOLLEN
# =============================================================================

__all__ = [
    # Analyse-Funktionen (Haupt-API)
    "nullstellen",
    "ableitung",
    "integral",
    "extrema",
    "wendepunkte",
    "symmetrie",
    # Visualisierung
    "zeichne",
    # Werteberechnung
    "auswerten",
    # Helper-Funktionen
    "erstelle_polynom",
    "erstelle_funktion",
    "erstelle_lineares_gleichungssystem",
    # Komfort-Funktionen
    "analysiere_funktion",
    "zeige_analyse",
    # Funktionstypen (für direkten Zugriff)
    "GanzrationaleFunktion",
    "QuotientFunktion",
    "ProduktFunktion",
    "SummeFunktion",
    "KompositionFunktion",
    "LGS",
    # Type-Hints
    "Funktionstyp",
]
