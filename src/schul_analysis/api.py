"""
Schülerfreundliche API für das Schul-Analysis Framework

Diese Datei stellt Wrapper-Funktionen bereit, die eine intuitive,
unterrichtsnahe Syntax ermöglichen: Nullstellen(f) statt f.Nullstellen()

Alle Funktionen unterstützen Duck-Typing und funktionieren mit allen
verfügbaren Funktionstypen (ganzrational, gebrochen rational, etc.)
"""

from typing import Any

import numpy as np

from .errors import SchulAnalysisError, UngueltigeFunktionError
from .funktion import Funktion

# Importiere alle verfügbaren Funktionstypen
from .ganzrationale import GanzrationaleFunktion
from .lineare_gleichungssysteme import LGS
from .strukturiert import (
    KompositionFunktion,
    ProduktFunktion,
    QuotientFunktion,
    SummeFunktion,
)

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


def Nullstellen(
    funktion: Funktionstyp, real: bool = True, runden: int | None = None
) -> list[float] | list[Any]:
    """
    Berechnet die Nullstellen einer Funktion.

    Args:
        funktion: Eine beliebige Funktion (ganzrational, gebrochen rational, etc.)
        real: Nur reelle Nullstellen zurückgeben (Standard: True)
        runden: Anzahl Nachkommastellen für Rundung (None = exakt)

    Returns:
        Liste der Nullstellen

    Beispiele:
        >>> f = ErstellePolynom([1, -4, 3])  # x² - 4x + 3
        >>> xs = Nullstellen(f)                 # [1.0, 3.0]

    Didaktischer Hinweis:
        Diese Funktion ermöglicht die natürliche mathematische Notation,
        die Schüler aus dem Unterricht kennen: "Berechne die Nullstellen von f"
    """
    try:
        # Handle both property and method cases
        if hasattr(funktion, "Nullstellen"):
            attr = funktion.nullstellen
            if callable(attr):
                # It's a method - try with parameters first
                try:
                    return funktion.Nullstellen(real=real, runden=runden)
                except TypeError:
                    # Method doesn't accept parameters, call without them
                    result = funktion.Nullstellen()
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


def Ableitung(funktion: Funktionstyp, ordnung: int = 1) -> Any:
    """
    Berechnet die Ableitung einer Funktion.

    Args:
        funktion: Eine beliebige Funktion
        ordnung: Ordnung der Ableitung (Standard: 1)

    Returns:
        Die abgeleitete Funktion

    Beispiele:
        >>> f = ErstellePolynom([1, -4, 3])  # x² - 4x + 3
        >>> f1 = Ableitung(f, 1)             # 2x - 4
        >>> f2 = Ableitung(f, 2)             # 2

    Didaktischer Hinweis:
        Diese Notation ist näher an der mathematischen Schreibweise f'(x)
        und für Schüler intuitiver verständlich.
    """
    try:
        return funktion.Ableitung(ordnung)
    except AttributeError:
        raise UngueltigeFunktionError(
            "Ableitung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "kann nicht abgeleitet werden.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Ableitungsberechnung: {str(e)}")


def Integral(funktion: Funktionstyp, *args, **kwargs) -> Any:
    """
    Berechnet das bestimmte oder unbestimmte Integral einer Funktion.

    Args:
        funktion: Eine beliebige Funktion
        *args: Entweder (ordnung) für unbestimmtes Integral oder (a, b) für bestimmtes Integral
        **kwargs:
            - ordnung: Ordnung des Integrals (Standard: 1) für unbestimmtes Integral
            - a, b: Integrationsgrenzen für bestimmtes Integral

    Returns:
        Bei unbestimmtem Integral: Die integrierte Funktion
        Bei bestimmtem Integral: Der numerische Wert des Integrals

    Beispiele:
        # Unbestimmtes Integral
        >>> f = ErstellePolynom([1, 0, 0])  # x²
        >>> F = Integral(f)                  # (1/3)x³
        >>> F = Integral(f, ordnung=1)       # (1/3)x³

        # Bestimmtes Integral
        >>> f = ErstellePolynom([1, 0, 0])  # x²
        >>> wert = Integral(f, 0, 1)         # 1/3 (Fläche von 0 bis 1)
        >>> wert = Integral(f, 0, 1, ordnung=1)  # 1/3 (Fläche von 0 bis 1)
    """
    try:
        # Prüfe, ob bestimmtes Integral berechnet werden soll
        if len(args) == 2:
            a, b = args
            ordnung = kwargs.get("ordnung", 1)

            # Berechne unbestimmtes Integral
            integrierte_funktion = funktion.Integral(ordnung)

            # Werte die integrierte Funktion von a bis b aus
            try:
                F_b = integrierte_funktion(b)
                F_a = integrierte_funktion(a)
                return F_b - F_a
            except (ValueError, TypeError, ZeroDivisionError) as e:
                raise SchulAnalysisError(
                    f"Fehler bei der Auswertung des bestimmten Integrals von {a} bis {b}: {str(e)}"
                )

        elif len(args) == 1:
            # Nur ordnung angegeben
            ordnung = args[0]
            return funktion.Integral(ordnung)

        elif len(args) == 0:
            # Unbestimmtes Integral
            ordnung = kwargs.get("ordnung", 1)
            return funktion.Integral(ordnung)

        else:
            raise ValueError(
                "Integral: Ungültige Anzahl an Argumenten. "
                "Verwende Integral(f) für unbestimmtes Integral oder "
                "Integral(f, a, b) für bestimmtes Integral."
            )

    except AttributeError:
        raise UngueltigeFunktionError(
            "Integration",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "kann nicht integriert werden.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Integrationsberechnung: {str(e)}")


def Extremstellen(funktion: Funktionstyp) -> list[tuple[Any, str]]:
    """
    Findet die Extremstellen einer Funktion (x-Werte mit Typ).

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Liste der Extremstellen als (x-Wert, Typ)-Tupel

    Beispiele:
        >>> f = ErstellePolynom([1, -3, -4, 12])  # x³ - 3x² - 4x + 12
        >>> ext = Extremstellen(f)                # [(-1, 'Maximum'), ...]
    """
    try:
        # Handle both property and method cases
        if hasattr(funktion, "extremstellen"):
            attr = funktion.extremstellen
            if callable(attr):
                # It's a method - call it
                return funktion.extremstellen()
            else:
                # It's a property - access it directly
                return funktion.extremstellen
        elif hasattr(funktion, "Extremstellen"):
            attr = funktion.Extremstellen
            if callable(attr):
                # It's a method - call it
                return funktion.Extremstellen()
            else:
                # It's a property - access it directly
                return funktion.Extremstellen
        else:
            raise AttributeError(
                "Keine extremstellen Eigenschaft oder Methode gefunden"
            )
    except AttributeError:
        raise UngueltigeFunktionError(
            "Extremstellenberechnung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "unterstützt keine Extremstellen-Berechnung.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Extremstellen-Berechnung: {str(e)}")


def Extrempunkte(funktion: Funktionstyp) -> list[tuple[Any, Any, str]]:
    """
    Findet die Extrempunkte einer Funktion (x, y-Koordinaten mit Typ).

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Liste der Extrempunkte als (x-Wert, y-Wert, Typ)-Tupel

    Beispiele:
        >>> f = ErstellePolynom([1, -3, -4, 12])  # x³ - 3x² - 4x + 12
        >>> ext = Extrempunkte(f)                 # [(-1, 14.0, 'Maximum'), ...]
    """
    try:
        # Versuche zuerst die extrempunkte() Methode
        if hasattr(funktion, "extrempunkte"):
            attr = funktion.extrempunkte
            if callable(attr):
                return funktion.extrempunkte()
            else:
                return funktion.extrempunkte
        elif hasattr(funktion, "Extrapunkte"):
            attr = funktion.Extrempunkte
            if callable(attr):
                return funktion.Extrempunkte()
            else:
                return funktion.Extrempunkte

        # Fallback: Berechne aus extremstellen und werte die Funktion aus
        extremstellen = Extremstellen(funktion)
        if not extremstellen:
            return []

        extrempunkte = []
        for x_wert, typ in extremstellen:
            try:
                y_wert = funktion(x_wert)
                extrempunkte.append((x_wert, y_wert, typ))
            except (ValueError, TypeError, ZeroDivisionError):
                # Falls die Funktion an diesem Punkt nicht ausgewertet werden kann
                extrempunkte.append((x_wert, None, typ))

        return extrempunkte
    except AttributeError:
        raise UngueltigeFunktionError(
            "Extrempunkteberechnung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "unterstützt keine Extrempunkte-Berechnung.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Extrempunkte-Berechnung: {str(e)}")


def Extrema(funktion: Funktionstyp) -> list[tuple[Any, str]]:
    """
    Findet die Extrempunkte einer Funktion (Alias für Extremstellen).

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Liste der Extremstellen als (x-Wert, Typ)-Tupel

    Beispiele:
        >>> f = ErstellePolynom([1, -3, -4, 12])  # x³ - 3x² - 4x + 12
        >>> ext = Extrema(f)                       # [(-1, 'Maximum'), ...]
    """
    # Extrema ist ein Alias für Extremstellen für Abwärtskompatibilität
    return Extremstellen(funktion)


def Wendestellen(funktion: Funktionstyp) -> list[tuple[Any, str]]:
    """
    Findet die Wendestellen einer Funktion (x-Werte mit Typ).

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Liste der Wendestellen als (x-Wert, Typ)-Tupel

    Beispiele:
        >>> f = ErstellePolynom([1, 0, 0, 0])  # x³
        >>> ws = Wendestellen(f)                 # [(0, 'Wendepunkt')]
    """
    try:
        # Handle both property and method cases
        if hasattr(funktion, "wendestellen"):
            attr = funktion.wendestellen
            if callable(attr):
                # It's a method - call it
                return funktion.wendestellen()
            else:
                # It's a property - access it directly
                return funktion.wendestellen
        elif hasattr(funktion, "Wendestellen"):
            attr = funktion.Wendestellen
            if callable(attr):
                # It's a method - call it
                return funktion.Wendestellen()
            else:
                # It's a property - access it directly
                return funktion.Wendestellen
        else:
            raise AttributeError("Keine wendestellen Eigenschaft oder Methode gefunden")
    except AttributeError:
        raise UngueltigeFunktionError(
            "Wendestellenberechnung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "unterstützt keine Wendestellen-Berechnung.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Wendestellen-Berechnung: {str(e)}")


def Wendepunkte(funktion: Funktionstyp) -> list[tuple[Any, Any, str]]:
    """
    Findet die Wendepunkte einer Funktion (x, y-Koordinaten mit Typ).

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Liste der Wendepunkte als (x-Wert, y-Wert, Typ)-Tupel

    Beispiele:
        >>> f = ErstellePolynom([1, 0, 0, 0])  # x³
        >>> wp = Wendepunkte(f)                 # [(0, 0.0, 'Wendepunkt')]
    """
    try:
        # Versuche zuerst die wendepunkte() Methode (falls sie (x,y,Typ) zurückgibt)
        if hasattr(funktion, "wendepunkte"):
            attr = funktion.wendepunkte
            if callable(attr):
                result = funktion.wendepunkte()
            else:
                result = funktion.wendepunkte
            # Prüfe, ob das Ergebnis schon im richtigen Format ist
            if result and len(result[0]) == 3:
                return result

        # Fallback: Berechne aus wendestellen und werte die Funktion aus
        wendestellen = Wendestellen(funktion)
        if not wendestellen:
            return []

        wendepunkte = []
        for x_wert, typ in wendestellen:
            try:
                y_wert = funktion(x_wert)
                wendepunkte.append((x_wert, y_wert, typ))
            except (ValueError, TypeError, ZeroDivisionError):
                # Falls die Funktion an diesem Punkt nicht ausgewertet werden kann
                wendepunkte.append((x_wert, None, typ))

        return wendepunkte
    except AttributeError:
        raise UngueltigeFunktionError(
            "Wendepunkteberechnung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "unterstützt keine Wendepunkte-Berechnung.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Wendepunkte-Berechnung: {str(e)}")


def Symmetrie(funktion: Funktionstyp) -> str:
    """
    Bestimmt die Symmetrie einer Funktion.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Beschreibung der Symmetrie

    Beispiele:
        >>> f = ErstellePolynom([1, 0, 0])      # x²
        >>> sym = Symmetrie(f)                   # "Achsensymmetrisch zur y-Achse"
    """
    try:
        # Versuche zuerst die Symmetrie() Methode
        return funktion.Symmetrie()
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


def Term(funktion: Funktionstyp) -> Any:
    """
    Wrapper für die LaTeX-Darstellung einer Funktion in Marimo.

    Gibt ein Marimo-Markdown-Objekt zurück, das die Funktion
    in schöner LaTeX-Darstellung anzeigt.

    Args:
        funktion: Eine beliebige Funktion aus dem Schul-Analysis Framework

    Returns:
        Marimo-Markdown-Objekt mit LaTeX-Darstellung

    Examples:
        >>> f = Funktion("x^2 + 2*x + 1")
        >>> Term(f)  # Zeigt schöne LaTeX-Darstellung in Marimo

    Didaktischer Hinweis:
        Diese Funktion ermöglicht es, Funktionen in Marimo-Notebooks
        in schöner mathematischer Notation darzustellen, während die
        Funktionen selbst weiterhin SymPy-Ausdrücke zurückgeben,
        damit arithmetische Operationen wie f+g oder f/g funktionieren.
    """
    try:
        import marimo as mo

        return mo.md(funktion.latex_display())
    except ImportError:
        # Fallback, wenn Marimo nicht verfügbar ist
        return f"${funktion.term_latex()}$"
    except AttributeError:
        # Fallback, wenn latex_display() nicht verfügbar ist
        return f"${funktion.term_latex()}$"
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der LaTeX-Darstellung: {str(e)}")


def Ausmultiplizieren(funktion: Funktionstyp) -> Funktionstyp:
    """
    Multipliziert eine Funktion aus und gibt die expandierte Form zurück.

    Diese Funktion ist nützlich für pädagogische Zwecke, wenn Schüler die ausmultiplizierte
    Form einer Funktion sehen müssen, anstatt der faktorisierten Darstellung.

    Args:
        funktion: Eine beliebige Funktion aus dem Schul-Analysis Framework

    Returns:
        Die Funktion mit ausmultipliziertem Term

    Examples:
        >>> f = Funktion("(x+1)(x-2)")
        >>> print(f.term())  # (x + 1)*(x - 2)
        >>> f_expanded = Ausmultiplizieren(f)
        >>> print(f_expanded.term())  # x^2 - x - 2
        # Beachte: f_expanded ist eine NEUE Funktion, f bleibt unverändert

        >>> g = Funktion("(x+1)^3")
        >>> print(g.term())  # (x + 1)^3
        >>> g_expanded = Ausmultiplizieren(g)
        >>> print(g_expanded.term())  # x^3 + 3*x^2 + 3*x + 1

        # In-place Änderung:
        >>> h = Funktion("(x-1)(x+2)(x-3)")
        >>> h.ausmultiplizieren()  # Methode direkt am Objekt
        >>> print(h.term())  # x^3 - 2*x^2 - 5*x + 6

    Didaktischer Hinweis:
        Das Ausmultiplizieren hilft bei der Umwandlung von Produktform in die
        Normalform und ist wichtig für das Verständnis von Polynom-Operationen.
        Manchmal ist die faktorisierte Form besser für die Analyse (z.B. Nullstellen),
        manchmal die expandierte Form besser für weitere Berechnungen.
    """
    # Erstelle eine Kopie der Funktion, um das Original nicht zu verändern
    from . import Funktion

    # Erstelle neue Funktion mit dem gleichen Term
    neue_funktion = Funktion(funktion.term_sympy)

    # Wende Ausmultiplizieren auf die neue Funktion an
    neue_funktion.ausmultiplizieren()

    return neue_funktion


def Zeichne(
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
        >>> f = ErstellePolynom([1, -4, 3])  # x² - 4x + 3
        >>> Zeichne(f, (-2, 6))               # Zeichnet Funktion von x=-2 bis x=6

        # Auch mit normalen Python-Funktionen möglich:
        >>> Zeichne(lambda x: x**2, (-5, 5))
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


def Auswerten(funktion: Any, x_wert: float | np.ndarray) -> float | np.ndarray:
    """
    Wertet eine Funktion an einem Punkt oder Array aus.

    Args:
        funktion: Eine beliebige Funktion
        x_wert: Der x-Wert oder Array von x-Werten

    Returns:
        Der y-Wert oder Array von y-Werten

    Beispiele:
        >>> f = ErstellePolynom([1, -4, 3])  # x² - 4x + 3
        >>> y = Auswerten(f, 2)               # f(2) = -1
        >>> y_array = Auswerten(f, [1, 2, 3]) # [f(1), f(2), f(3)] = [0, -1, 0]
    """
    try:
        return funktion(x_wert)
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Auswertung: {str(e)}")


# =============================================================================
# HELPER-FUNKTIONEN FÜR SCHÜLER
# =============================================================================


def ErstellePolynom(koeffizienten: list[float | int]) -> Funktion:
    """
    Erstellt ein Polynom aus Koeffizienten.

    Args:
        koeffizienten: Liste der Koeffizienten [a₀, a₁, a₂, ...]
                     für a₀ + a₁x + a₂x² + ...

    Returns:
        Eine ganzrationale Funktion

    Beispiele:
        >>> f = ErstellePolynom([3, -4, 1])     # 3 - 4x + x²
        >>> g = ErstellePolynom([0, 1])        # x
        >>> h = ErstellePolynom([5])           # 5 (konstant)

    Didaktischer Hinweis:
        Diese Funktion ist besonders für Anfänger geeignet,
        da sie die Polynom-Erstellung sehr einfach macht.

    Magic Factory Hinweis:
        Alternativ kann jetzt auch Funktion("x^2 - 4x + 3") verwendet werden,
        was automatisch die richtige Funktionstyp zurückgibt.
    """

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

    return GanzrationaleFunktion(term)


def Erstelle_Funktion(term: str) -> Any:
    """
    Erstellt eine Funktion aus einem Term-String.

    Args:
        term: Der mathematische Term als String

    Returns:
        Eine Funktion (automatisch typisiert durch Magic Factory)

    Beispiele:
        >>> f = Erstelle_Funktion("x^2 - 4x + 3")    # x² - 4x + 3
        >>> g = Erstelle_Funktion("2*x + 5")          # 2x + 5
        >>> h = Erstelle_Funktion("(x-2)*(x+1)")     # (x-2)(x+1) = x² - x - 2
        >>> i = Erstelle_Funktion("x^2/(x+1)")      # QuotientFunktion!

    Didaktischer Hinweis:
        Unterstützt verschiedene Schreibweisen, die Schüler aus dem Unterricht kennen.

    Magic Factory Hinweis:
        Diese Funktion nutzt jetzt die Magic Factory und gibt automatisch den
        richtigen Funktionstyp zurück (QuadratischeFunktion, ProduktFunktion, etc.)
    """
    from .funktion import Funktion

    return Funktion(term)


def Erstelle_Lineares_Gleichungssystem(
    koeffizienten: list[list[float | int]], ergebnisse: list[float | int]
) -> Any:
    """
    Erstellt ein lineares Gleichungssystem.

    Args:
        koeffizienten: Matrix der Koeffizienten [[a₁₁, a₁₂], [a₂₁, a₂₂], ...]
        ergebnisse: Vektor der Ergebnisse [b₁, b₂, ...]

    Returns:
        Ein lineares Gleichungssystem

    Beispiele:
        >>> lgs = Erstelle_Lineares_Gleichungssystem(
        ...     [[2, 3], [1, -2]],    # 2x + 3y = 8, x - 2y = -3
        ...     [8, -3]
        ... )
        >>> lösung = lgs.loese()        # [2, 1.333...]
    """
    return LGS(koeffizienten, ergebnisse)


def Erstelle_Exponential_Rationale_Funktion(
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
        >>> f = Erstelle_Exponential_Rationale_Funktion("x+1", "x-1")
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


def Analysiere_Funktion(funktion: Funktionstyp) -> dict[str, Any]:
    """
    Führt eine vollständige Funktionsanalyse durch.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Dictionary mit allen Analyse-Ergebnissen

    Beispiele:
        >>> f = ErstellePolynom([1, -4, 3])  # x² - 4x + 3
        >>> analyse = Analysiere_Funktion(f)
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
        ergebnisse["Nullstellen"] = Nullstellen(funktion)
    except (AttributeError, ValueError, TypeError, ZeroDivisionError):
        ergebnisse["Nullstellen"] = "Nicht berechenbar"

    try:
        ergebnisse["Extrema"] = Extrema(funktion)
    except (AttributeError, ValueError, TypeError, ZeroDivisionError):
        ergebnisse["Extrema"] = "Nicht berechenbar"

    try:
        ergebnisse["Wendepunkte"] = Wendepunkte(funktion)
    except (AttributeError, ValueError, TypeError, ZeroDivisionError):
        ergebnisse["Wendepunkte"] = "Nicht berechenbar"

    try:
        ergebnisse["Symmetrie"] = Symmetrie(funktion)
    except (AttributeError, ValueError, TypeError):
        ergebnisse["Symmetrie"] = "Nicht bestimmbar"

    return ergebnisse


def Zeige_Analyse(funktion: Funktionstyp) -> str:
    """
    Erstellt eine übersichtliche Zusammenfassung der Funktionsanalyse.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Formatierter Text mit allen Analyse-Ergebnissen

    Beispiele:
        >>> f = ErstellePolynom([1, -4, 3])
        >>> print(Zeige_Analyse(f))
        Funktionsanalyse für f(x) = x^2 - 4x + 3

        Nullstellen: [1.0, 3.0]
        Extrema: []
        Wendepunkte: []
        Symmetrie: Keine einfache Symmetrie
    """
    analyse = Analysiere_Funktion(funktion)

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
    "Nullstellen",
    "Ableitung",
    "Integral",
    "Extrema",
    "Extremstellen",
    "Extrempunkte",
    "Wendestellen",
    "Wendepunkte",
    "Symmetrie",
    # Visualisierung
    "Term",
    "Ausmultiplizieren",
    "Zeichne",
    # Werteberechnung
    "Auswerten",
    # Helper-Funktionen
    "ErstellePolynom",
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
