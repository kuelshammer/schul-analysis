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
from .sympy_types import (
    ExactNullstellenListe,
    ExactSymPyExpr,
    ExtremaListe,
    SattelpunkteListe,
    SchnittpunkteListe,
    StationaereStellenListe,
    WendepunkteListe,
    preserve_exact_types,
    validate_analysis_results,
    validate_exact_results,
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


@validate_analysis_results("Nullstellen")
def Nullstellen(
    funktion: Funktionstyp, real: bool = True, runden: int | None = None
) -> ExactNullstellenListe:
    """
    Berechnet die Nullstellen einer Funktion mit exakten SymPy-Ergebnissen.

    Args:
        funktion: Eine beliebige Funktion (ganzrational, gebrochen rational, etc.)
        real: Nur reelle Nullstellen zurückgeben (Standard: True)
        runden: Anzahl Nachkommastellen für Rundung (None = exakt)

    Returns:
        Liste der exakten Nullstellen als SymPy-Ausdrücke

    Beispiele:
        >>> f = ErstellePolynom([1, -4, 3])  # x² - 4x + 3
        >>> xs = Nullstellen(f)                 # [1, 3] als exakte SymPy-Ausdrücke

    Didaktischer Hinweis:
        Diese Funktion ermöglicht die natürliche mathematische Notation,
        die Schüler aus dem Unterricht kennen: "Berechne die Nullstellen von f"

    Typ-Sicherheit:
        Garantiert exakte symbolische Ergebnisse ohne numerische Approximation
    """
    try:
        # Handle both property and method cases
        if hasattr(funktion, "Nullstellen"):
            attr = funktion.nullstellen
            if callable(attr):
                # It's a method - try with parameters first
                try:
                    result = funktion.Nullstellen(real=real, runden=runden)
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

        # Ergebnis validieren
        if isinstance(result, list):
            validate_exact_results(result, "Nullstellen")
        else:
            # Einzelnes Ergebnis in Liste umwandeln
            result = [result]
            validate_exact_results(result, "Nullstellen")

        return result

    except AttributeError as e:
        raise UngueltigeFunktionError(
            "Nullstellenberechnung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "unterstützt die Nullstellen-Berechnung nicht.",
        ) from e
    except Exception as e:
        raise SchulAnalysisError(
            f"Fehler bei der Nullstellenberechnung: {str(e)}\n"
            "Tipp: Stelle sicher, dass die Funktion korrekt definiert ist "
            "und verwende symbolische Berechnung für exakte Ergebnisse."
        ) from e


@preserve_exact_types
def Ableitung(funktion: Funktionstyp, ordnung: int = 1) -> ExactSymPyExpr:
    """
    Berechnet die Ableitung einer Funktion mit exakten SymPy-Ergebnissen.

    Args:
        funktion: Eine beliebige Funktion
        ordnung: Ordnung der Ableitung (Standard: 1)

    Returns:
        Die abgeleitete Funktion als exakter SymPy-Ausdruck

    Beispiele:
        >>> f = ErstellePolynom([1, -4, 3])  # x² - 4x + 3
        >>> f1 = Ableitung(f, 1)             # 2x - 4 als exakter Ausdruck
        >>> f2 = Ableitung(f, 2)             # 2 als exakter Ausdruck

    Didaktischer Hinweis:
        Diese Notation ist näher an der mathematischen Schreibweise f'(x)
        und für Schüler intuitiver verständlich.

    Typ-Sicherheit:
        Garantiert exakte symbolische Ergebnisse ohne numerische Approximation
    """
    try:
        result = funktion.Ableitung(ordnung)
        return result
    except AttributeError:
        raise UngueltigeFunktionError(
            "Ableitung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "kann nicht abgeleitet werden.",
        )
    except Exception as e:
        raise SchulAnalysisError(
            f"Fehler bei der Ableitungsberechnung: {str(e)}\n"
            "Tipp: Stelle sicher, dass die Funktion differenzierbar ist "
            "und verwende symbolische Berechnung für exakte Ergebnisse."
        ) from e


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

    Diese Funktion liefert exakte symbolische Ergebnisse und rundet nicht fälschlicherweise
    zu Float-Werten. Bei parametrisierten Funktionen bleiben die Parameter erhalten,
    bei numerischen Funktionen werden Brüche und exakte Werte beibehalten.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Liste der Extremstellen als (x-Wert, Typ)-Tupel
        - x-Wert: Exakter symbolischer Ausdruck (bei Parametern) oder exakte Zahl (Bruch/Ganzzahl)
        - Typ: "Minimum", "Maximum", "Sattelpunkt" oder beschreibende Texte bei Parametern

    Beispiele:
        >>> f = Funktion("a*x^2 + x")             # Parametrisierte Funktion
        >>> ext = Extremstellen(f)                # [(-1/(2*a), 'Minimum/Maximum (abhängig von Parameter)')]

        >>> g = Funktion("2*x^2 - x")              # Numerische Funktion
        >>> ext = Extremstellen(g)                # [(1/4, 'Minimum')]  # Exakter Bruch, kein Float!

        >>> h = Funktion("x^2 - 4*x + 3")          # Einfache quadratische Funktion
        >>> ext = Extremstellen(h)                # [(2, 'Minimum')]    # Exakte Ganzzahl
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


@validate_analysis_results("Extrema")
def Extrema(funktion: Funktionstyp) -> ExtremaListe:
    """
    Findet die Extrempunkte einer Funktion mit exakten SymPy-Ergebnissen (Alias für Extremstellen).

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Liste der Extremstellen als (x-Wert, Typ)-Tupel mit exakten SymPy-Ausdrücken

    Beispiele:
        >>> f = ErstellePolynom([1, -3, -4, 12])  # x³ - 3x² - 4x + 12
        >>> ext = Extrema(f)                       # [(-1, 'Maximum'), ...] mit exakten Werten

    Typ-Sicherheit:
        Garantiert exakte symbolische Ergebnisse ohne numerische Approximation
    """
    # Extrema ist ein Alias für Extremstellen für Abwärtskompatibilität
    return Extremstellen(funktion)


@validate_analysis_results("Wendepunkte")
def Wendestellen(funktion: Funktionstyp) -> WendepunkteListe:
    """
    Findet die Wendestellen einer Funktion mit exakten SymPy-Ergebnissen (x-Werte mit Typ).

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Liste der Wendestellen als (x-Wert, Typ)-Tupel mit exakten SymPy-Ausdrücken

    Beispiele:
        >>> f = ErstellePolynom([1, 0, 0, 0])  # x³
        >>> ws = Wendestellen(f)                 # [(0, 'Wendepunkt')] mit exakten Werten

    Typ-Sicherheit:
        Garantiert exakte symbolische Ergebnisse ohne numerische Approximation
    """
    try:
        # Verwende die neue wendepunkte-Methode und extrahiere nur x-Werte mit Typ
        if hasattr(funktion, "wendepunkte"):
            attr = funktion.wendepunkte
            if callable(attr):
                wendepunkte = funktion.wendepunkte()
            else:
                wendepunkte = funktion.wendepunkte

            # Extrahiere nur (x-Wert, Typ) aus den (x, y, art) Tupeln
            wendestellen = []
            for x_wert, _y_wert, art in wendepunkte:
                wendestellen.append((x_wert, art))

            return wendestellen
        else:
            raise AttributeError("Keine wendepunkte Eigenschaft oder Methode gefunden")
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


@validate_analysis_results("Schnittpunkte")
def Schnittpunkte(
    funktion1: Funktionstyp, funktion2: Funktionstyp
) -> SchnittpunkteListe:
    """
    Berechnet die Schnittpunkte zwischen zwei Funktionen mit exakten SymPy-Ergebnissen.

    Diese Funktion liefert exakte symbolische Ergebnisse und rundet nicht fälschlicherweise
    zu Float-Werten. Bei parametrisierten Funktionen bleiben die Parameter erhalten,
    bei numerischen Funktionen werden Brüche und exakte Werte beibehalten.

    Args:
        funktion1: Erste Funktion
        funktion2: Zweite Funktion

    Returns:
        SchnittpunkteListe mit strukturierten Schnittpunkt-Objekten und exakten SymPy-Ausdrücken

    Beispiele:
        >>> f = Funktion("x^2")
        >>> g = Funktion("2*x")
        >>> schnittpunkte = Schnittpunkte(f, g)  # [Schnittpunkt(x=0, y=0), Schnittpunkt(x=2, y=4)]

        >>> f = Funktion("a*x^2 + b*x + c")
        >>> g = Funktion("d*x + e")
        >>> schnittpunkte = Schnittpunkte(f, g)  # Symbolische Ergebnisse mit Parametern

    Didaktischer Hinweis:
        Diese Funktion folgt der natürlichen mathematischen Sprache, die Schüler aus dem Unterricht kennen:
        "Berechne die Schnittpunkte von f und g"

    Typ-Sicherheit:
        Garantiert exakte symbolische Ergebnisse ohne numerische Approximation
    """
    try:
        # Handle both method and property access
        if hasattr(funktion1, "schnittpunkte"):
            attr = funktion1.schnittpunkte
            if callable(attr):
                # It's a method - call it with the other function
                return funktion1.schnittpunkte(funktion2)
            else:
                # It's a property - this shouldn't happen for schnittpunkte
                raise AttributeError(
                    "schnittpunkte sollte eine Methode sein, keine Property"
                )
        elif hasattr(funktion1, "Schnittpunkte"):
            attr = funktion1.Schnittpunkte
            if callable(attr):
                # It's a method - call it with the other function
                return funktion1.Schnittpunkte(funktion2)
            else:
                # It's a property - this shouldn't happen for Schnittpunkte
                raise AttributeError(
                    "Schnittpunkte sollte eine Methode sein, keine Property"
                )
        else:
            raise AttributeError("Keine schnittpunkte Methode gefunden")

    except AttributeError:
        raise UngueltigeFunktionError(
            "Schnittpunktberechnung",
            f"Die Funktion vom Typ '{type(funktion1).__name__}' "
            "unterstützt keine Schnittpunkt-Berechnung.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Schnittpunkt-Berechnung: {str(e)}")


def StationaereStellen(funktion: Funktionstyp) -> StationaereStellenListe:
    """
    Findet die stationären Stellen einer Funktion mit exakten SymPy-Ergebnissen.

    Stationäre Stellen sind alle Punkte, an denen die erste Ableitung null ist (f'(x) = 0).
    Dies entspricht mathematisch den kritischen Punkten, die in der Extremstellen-Berechnung
    gefunden werden. Der Unterschied liegt in der Interpretation:
    - Stationär = horizontale Tangente
    - Extrem = Max/Min/Sattelpunkt

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        StationaereStellenListe mit strukturierten StationaereStelle-Objekten und exakten SymPy-Ausdrücken

    Beispiele:
        >>> f = ErstellePolynom([1, 0, 0, 0])  # x³
        >>> ss = StationaereStellen(f)         # [StationaereStelle(x=0, typ=ExtremumTyp.SATTELPUNKT)]
        >>> f = ErstellePolynom([1, 0, 0])     # x²
        >>> ss = StationaereStellen(f)         # [StationaereStelle(x=0, typ=ExtremumTyp.MINIMUM)]

    Typ-Sicherheit:
        Garantiert exakte symbolische Ergebnisse ohne numerische Approximation
    """
    try:
        # Verwende die stationaere_stellen Methode der Funktion
        if hasattr(funktion, "stationaere_stellen"):
            # Bei Properties einfach zugreifen, nicht als Funktion aufrufen
            result = funktion.stationaere_stellen
            return result
        else:
            # Fallback: Verwende Extremstellen, da die Berechnung identisch ist
            if hasattr(funktion, "extremstellen"):
                # Bei Properties einfach zugreifen, nicht als Funktion aufrufen
                result = funktion.extremstellen

                # Konvertiere Tupel zu StationaereStelle-Objekten für Fallback
                from .sympy_types import ExtremumTyp, StationaereStelle

                stationaere_stellen_liste = []
                for x_wert, art in result:
                    # Konvertiere String zu ExtremumTyp Enum
                    if art == "Minimum":
                        extremum_typ = ExtremumTyp.MINIMUM
                    elif art == "Maximum":
                        extremum_typ = ExtremumTyp.MAXIMUM
                    elif art == "Sattelpunkt":
                        extremum_typ = ExtremumTyp.SATTELPUNKT
                    else:
                        extremum_typ = ExtremumTyp.SATTELPUNKT

                    stationaere_stelle = StationaereStelle(
                        x=x_wert, typ=extremum_typ, exakt=True
                    )
                    stationaere_stellen_liste.append(stationaere_stelle)

                return stationaere_stellen_liste
            else:
                raise AttributeError(
                    "Keine stationaere_stellen oder extremstellen Eigenschaft gefunden"
                )
    except AttributeError:
        raise UngueltigeFunktionError(
            "Stationäre Stellen Berechnung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "unterstützt keine Berechnung stationärer Stellen.",
        )
    except Exception as e:
        raise SchulAnalysisError(
            f"Fehler bei der Berechnung stationärer Stellen: {str(e)}"
        )


def Sattelpunkte(funktion: Funktionstyp) -> SattelpunkteListe:
    """
    Findet die Sattelpunkte einer Funktion mit exakten SymPy-Ergebnissen.

    Sattelpunkte sind spezielle stationäre Stellen, die zusätzlich Wendepunkte sind:
    - f'(x) = 0 (stationär)
    - f''(x) = 0 (Wendepunkt)
    - f'''(x) ≠ 0 (echter Wendepunkt)

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        SattelpunkteListe mit strukturierten Sattelpunkt-Objekten und exakten SymPy-Ausdrücken

    Beispiele:
        >>> f = ErstellePolynom([1, 0, 0, 0])  # x³
        >>> sp = Sattelpunkte(f)               # [Sattelpunkt(x=0, y=0, exakt=True)]

    Typ-Sicherheit:
        Garantiert exakte symbolische Ergebnisse ohne numerische Approximation
    """
    try:
        # Verwende die sattelpunkte Methode der Funktion
        if hasattr(funktion, "sattelpunkte"):
            # Bei Properties einfach zugreifen, nicht als Funktion aufrufen
            result = funktion.sattelpunkte
            return result
        else:
            raise AttributeError("Keine sattelpunkte Eigenschaft oder Methode gefunden")
    except AttributeError:
        raise UngueltigeFunktionError(
            "Sattelpunkteberechnung",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "unterstützt keine Sattelpunkte-Berechnung.",
        )
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Sattelpunkte-Berechnung: {str(e)}")


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


def Ausmultiplizieren(funktion: Funktionstyp) -> None:
    """
    Multipliziert eine Funktion aus (modifiziert das Original).

    Diese Funktion ist nützlich für pädagogische Zwecke, wenn Schüler die ausmultiplizierte
    Form einer Funktion sehen müssen, anstatt der faktorisierten Darstellung.
    Die Funktion wird direkt verändert (in-place).

    Args:
        funktion: Eine beliebige Funktion aus dem Schul-Analysis Framework

    Returns:
        None (die Funktion wird direkt verändert)

    Examples:
        >>> f = Funktion("(x+1)(x-2)")
        >>> print(f.term)  # (x + 1)*(x - 2)
        >>> Ausmultiplizieren(f)  # Modifiziert f direkt
        >>> print(f.term)  # x^2 - x - 2 (f ist jetzt verändert)

        # Für Method Chaining die Methode direkt verwenden:
        >>> g = Funktion("(x+1)^3")
        >>> ableitung = g.ausmultiplizieren().ableitung()
        >>> print(ableitung.term)  # 3*x^2 + 6*x + 3

        # Alternative Syntax:
        >>> h = Funktion("(x-1)(x+2)(x-3)")
        >>> h.ausmultiplizieren()  # Methode direkt am Objekt
        >>> print(h.term)  # x^3 - 2*x^2 - 5*x + 6

    Didaktischer Hinweis:
        Das Ausmultiplizieren hilft bei der Umwandlung von Produktform in die
        Normalform und ist wichtig für das Verständnis von Polynom-Operationen.
        Manchmal ist die faktorisierte Form besser für die Analyse (z.B. Nullstellen),
        manchmal die expandierte Form besser für weitere Berechnungen.
    """
    # Wende Ausmultiplizieren direkt auf die Funktion an (in-place)
    funktion.ausmultiplizieren()


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
    "StationaereStellen",
    "Sattelpunkte",
    "Symmetrie",
    "Schnittpunkte",
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
