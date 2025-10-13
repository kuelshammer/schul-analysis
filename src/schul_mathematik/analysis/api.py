"""
Schülerfreundliche API für das Schul-Analysis Framework

Diese Datei stellt Wrapper-Funktionen bereit, die eine intuitive,
unterrichtsnahe Syntax ermöglichen: Nullstellen(f) statt f.Nullstellen()

Alle Funktionen unterstützen Duck-Typing und funktionieren mit allen
verfügbaren Funktionstypen (ganzrational, gebrochen rational, etc.)
"""

from typing import Any

import sympy as sp

from .errors import SchulAnalysisError, UngueltigeFunktionError
from .visualisierung_errors import DatenpunktBerechnungsError

# Importiere alle verfügbaren Funktionstypen
from .ganzrationale import GanzrationaleFunktion
from .strukturiert import (
    KompositionFunktion,
    ProduktFunktion,
    QuotientFunktion,
    SummeFunktion,
)
from .sympy_types import (
    ExactNullstellenListe,
    ExactSymPyExpr,
    SattelpunkteListe,
    SchnittpunkteListe,
    StationaereStellenListe,
    WendepunkteListe,
    preserve_exact_types,
    validate_analysis_results,
    validate_exact_results,
)
from .visualisierung import Graph

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
        # Handle both property and method cases (check lowercase first)
        if hasattr(funktion, "nullstellen"):
            attr = funktion.nullstellen
            if callable(attr):
                # It's a method - try with parameters first
                try:
                    result = funktion.nullstellen(real=real, runden=runden)
                except TypeError:
                    # Method doesn't accept parameters, call without them
                    result = funktion.nullstellen()
            else:
                # It's a property - access it directly
                result = funktion.nullstellen

                # Apply filtering and rounding if needed
                if real:
                    # Keep only real nullstellen - filter out complex ones
                    filtered_result = []
                    for n in result:
                        if hasattr(n, "x"):
                            # It's a Nullstelle object
                            x_val = n.x
                            if hasattr(x_val, "is_real") and x_val.is_real:
                                filtered_result.append(n)
                        elif hasattr(n, "is_real") and n.is_real:
                            # It's already a SymPy expression
                            filtered_result.append(n)
                    result = filtered_result

                if runden is not None:
                    # Convert to floats for rounding
                    if result and hasattr(result[0], "x"):
                        result = [float(n.x) for n in result]
                    result = [
                        round(float(n), runden) if hasattr(n, "__float__") else n
                        for n in result
                    ]
                elif result and hasattr(result[0], "x"):
                    # Keep exact SymPy values when no rounding needed
                    result = [n.x for n in result]

                return result
        elif hasattr(funktion, "Nullstellen"):
            # Fallback to uppercase for backward compatibility
            attr = funktion.Nullstellen
            if callable(attr):
                try:
                    result = funktion.Nullstellen(real=real, runden=runden)
                except TypeError:
                    result = funktion.Nullstellen()
            else:
                result = funktion.Nullstellen
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


def NullstellenMitWiederholungen(
    funktion: Funktionstyp, real: bool = True, runden: int | None = None
) -> list:
    """
    Berechnet die Nullstellen mit Wiederholungen gemäß Vielfachheit.

    Diese Methode expandiert Nullstellen mit Vielfachheit > 1 zu mehreren
    Einträgen in der Liste, um Kompatibilität mit bestehenden Tests
    und der traditionellen Darstellung zu gewährleisten.

    Args:
        funktion: Eine beliebige Funktion
        real: Nur reelle Nullstellen zurückgeben (Standard: True)
        runden: Anzahl Dezimalstellen zum Runden (optional)

    Returns:
        Liste der Nullstellen mit Wiederholungen für Vielfachheiten

    Beispiele:
        >>> f = ErstellePolynom([1, -2, 1])  # (x-1)²
        >>> xs = NullstellenMitWiederholungen(f)  # [1, 1] (doppelte Nullstelle)
    """
    try:
        # Verwende die neue Methode der Funktion
        if hasattr(funktion, "nullstellen_mit_wiederholungen"):
            attr = funktion.nullstellen_mit_wiederholungen
            if callable(attr):
                # It's a method - try with parameters first
                try:
                    result = funktion.nullstellen_mit_wiederholungen(
                        real=real, runden=runden
                    )
                except TypeError:
                    # Method doesn't accept parameters, call without them
                    result = funktion.nullstellen_mit_wiederholungen()
            else:
                # It's a property - access it directly
                result = funktion.nullstellen_mit_wiederholungen
        elif hasattr(funktion, "NullstellenMitWiederholungen"):
            attr = funktion.NullstellenMitWiederholungen
            if callable(attr):
                # It's a method - try with parameters first
                try:
                    result = funktion.NullstellenMitWiederholungen(
                        real=real, runden=runden
                    )
                except TypeError:
                    # Method doesn't accept parameters, call without them
                    result = funktion.NullstellenMitWiederholungen()
            else:
                # It's a property - access it directly
                result = funktion.NullstellenMitWiederholungen
        else:
            raise AttributeError(
                "Keine nullstellen_mit_wiederholungen Eigenschaft oder Methode gefunden"
            )

        return result
    except AttributeError:
        raise UngueltigeFunktionError(
            "Nullstellenberechnung mit Wiederholungen",
            f"Die Funktion vom Typ '{type(funktion).__name__}' "
            "unterstützt die Nullstellen-Berechnung mit Wiederholungen nicht.",
        )
    except Exception as e:
        raise SchulAnalysisError(
            f"Fehler bei der Nullstellenberechnung mit Wiederholungen: {str(e)}"
        )


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


def Achsensymmetrie(funktion: Funktionstyp) -> float | sp.Basic | None:
    """
    Bestimmt die Achsensymmetrie einer Funktion.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        x-Koordinate der Symmetrieachse, wenn die Funktion achsensymmetrisch ist, sonst None
        Für x² wird 0 zurückgegeben (Symmetrie zur y-Achse)
        Für (x-2)² wird 2 zurückgegeben (Symmetrie zur Geraden x=2)

    Beispiele:
        >>> f = Funktion("x^2")      # x²
        >>> sym = Achsensymmetrie(f)  # 0 (Symmetrie zur y-Achse)
        >>> g = Funktion("(x-2)^2")  # (x-2)²
        >>> sym = Achsensymmetrie(g)  # 2 (Symmetrie zur Geraden x=2)
        >>> h = Funktion("x^3")      # x³
        >>> sym = Achsensymmetrie(h)  # None (nicht achsensymmetrisch)
    """
    from .symmetrie import Achsensymmetrie as SymmetrieCheck

    try:
        return SymmetrieCheck(funktion)
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Achsensymmetrie-Bestimmung: {str(e)}")


def Punktsymmetrie(
    funktion: Funktionstyp,
) -> tuple[float | sp.Basic, float | sp.Basic] | None:
    """
    Bestimmt die Punktsymmetrie einer Funktion.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Tupel (x_s, y_s) des Symmetripunkts, wenn die Funktion punktsymmetrisch ist, sonst None
        Für x³ wird (0, 0) zurückgegeben (Symmetrie zum Ursprung)

    Beispiele:
        >>> f = Funktion("x^3")      # x³
        >>> sym = Punktsymmetrie(f)  # (0, 0) (Symmetrie zum Ursprung)
        >>> g = Funktion("(x-1)^3 + 2")  # (x-1)³ + 2
        >>> sym = Punktsymmetrie(g)  # (1, 2) (Symmetrie zum Punkt (1, 2))
        >>> h = Funktion("x^2")      # x²
        >>> sym = Punktsymmetrie(h)  # None (nicht punktsymmetrisch)
    """
    from .symmetrie import Punktsymmetrie as SymmetrieCheck

    try:
        return SymmetrieCheck(funktion)
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Punktsymmetrie-Bestimmung: {str(e)}")


def HatAchsensymmetrie(funktion: Funktionstyp) -> bool:
    """
    Prüft, ob eine Funktion achsensymmetrisch ist.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        True, wenn die Funktion achsensymmetrisch ist, sonst False

    Beispiele:
        >>> f = Funktion("x^2")      # x²
        >>> sym = HatAchsensymmetrie(f)  # True
        >>> g = Funktion("x^3")      # x³
        >>> sym = HatAchsensymmetrie(g)  # False
    """
    return Achsensymmetrie(funktion) is not None


def HatPunktsymmetrie(funktion: Funktionstyp) -> bool:
    """
    Prüft, ob eine Funktion punktsymmetrisch ist.

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        True, wenn die Funktion punktsymmetrisch ist, sonst False

    Beispiele:
        >>> f = Funktion("x^3")      # x³
        >>> sym = HatPunktsymmetrie(f)  # True
        >>> g = Funktion("x^2")      # x²
        >>> sym = HatPunktsymmetrie(g)  # False
    """
    return Punktsymmetrie(funktion) is not None


# Für Abwärtskompatibilität
def Symmetrie(funktion: Funktionstyp) -> str:
    """
    Bestimmt die Symmetrie einer Funktion (veraltet, nutze Achsensymmetrie/Punktsymmetrie).

    Args:
        funktion: Eine beliebige Funktion

    Returns:
        Beschreibung der Symmetrie

    Beispiele:
        >>> f = Funktion("x^2")      # x²
        >>> sym = Symmetrie(f)       # "Achsensymmetrisch zur y-Achse"
    """
    achsensymmetrie_wert = Achsensymmetrie(funktion)
    punktsymmetrie_wert = Punktsymmetrie(funktion)

    if achsensymmetrie_wert is not None:
        if achsensymmetrie_wert == 0:
            return "Achsensymmetrisch zur y-Achse"
        else:
            return f"Achsensymmetrisch zur Geraden x={achsensymmetrie_wert}"
    elif punktsymmetrie_wert is not None:
        x_s, y_s = punktsymmetrie_wert
        if x_s == 0 and y_s == 0:
            return "Punktsymmetrisch zum Ursprung"
        else:
            return f"Punktsymmetrisch zum Punkt ({x_s}, {y_s})"
    else:
        return "Keine einfache Symmetrie"


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


def Graph(
    funktion: Any,
    x_bereich: tuple[float, float] | None = None,
    y_bereich: tuple[float, float] | None = None,
    *weitere_funktionen,
    **kwargs,
) -> Any:
    """
    Zeichnet eine oder mehrere Funktionen im gegebenen Bereich mit intelligenter Typ-Erkennung.

    Args:
        funktion: Eine beliebige Funktion (auch Python-Funktionen)
        x_bereich: x-Bereich als (von, bis) - Standard: automatisch
        y_bereich: y-Bereich als (von, bis) - Standard: automatisch
        weitere_funktionen: Zusätzliche Funktionen, die gezeichnet werden sollen
        **kwargs: Zusätzliche Parameter für die Visualisierung
            aspect_ratio: Seitenverhältnis ('auto', 'quadratisch', 'goldener_schnitt', etc.)
            titel: Diagrammtitel
            achsen_beschriftung: Beschriftung der Achsen

    Returns:
        Interaktiver Plotly-Graph

    Beispiele:
        >>> f = Funktion("x^2 - 4x + 3")  # x² - 4x + 3
        >>> Graph(f, (-2, 6))               # Zeichnet Funktion von x=-2 bis x=6

        # Mit spezifischem Seitenverhältnis:
        >>> Graph(f, (-2, 6), aspect_ratio='quadratisch')

        # Mehrere Funktionen:
        >>> g = Funktion("2*x + 1")
        >>> Graph(f, g, (-2, 6))            # Zeichnet beide Funktionen

        # Auch mit normalen Python-Funktionen möglich:
        >>> Graph(lambda x: x**2, (-5, 5))
    """
    try:
        # Importiere Fehlerbehandlung und Aspect-Ratio-Controller
        from .visualisierung_errors import (
            PlotBereichError,
            DatenpunktBerechnungsError,
            VisualisierungsError,
        )
        from .aspect_ratio import AspectRatioController

        # Validiere Bereiche
        if x_bereich and len(x_bereich) != 2:
            raise PlotBereichError(
                "x_bereich muss ein Tupel mit zwei Werten sein: (von, bis)"
            )
        if y_bereich and len(y_bereich) != 2:
            raise PlotBereichError(
                "y_bereich muss ein Tupel mit zwei Werten sein: (von, bis)"
            )

        # Konvertiere x_bereich zu x_min/x_max für Graph-Funktion
        if x_bereich:
            kwargs["x_min"] = x_bereich[0]
            kwargs["x_max"] = x_bereich[1]
        if y_bereich:
            kwargs["y_min"] = y_bereich[0]
            kwargs["y_max"] = y_bereich[1]

        # Aspect-Ratio-Handling
        aspect_ratio = kwargs.pop("aspect_ratio", "auto")
        if aspect_ratio != "auto":
            controller = AspectRatioController()
            # Use the correct method name - create aspect ratio configuration
            ratio_kwargs = controller.create_mathematical_aspect_config()
            kwargs.update(ratio_kwargs)

        # Wenn mehrere Funktionen übergeben wurden
        if weitere_funktionen:
            from .visualisierung import Graph as VisualisierungsGraph

            return VisualisierungsGraph(funktion, *weitere_funktionen, **kwargs)
        else:
            # Intelligente Funktionserkennung für einzelne Funktionen
            return _zeichne_einzelne_funktion(funktion, x_bereich, kwargs)

    except (PlotBereichError, DatenpunktBerechnungsError, VisualisierungsError):
        # Spezialisierte Fehler durchreichen
        raise
    except Exception as e:
        # Generische Fehler mit Kontext
        raise SchulAnalysisError(
            f"Fehler bei der Visualisierung von {getattr(funktion, '__name__', str(funktion))}: {str(e)}"
        )


def _zeichne_einzelne_funktion(
    funktion: Any, x_bereich: tuple[float, float] | None, kwargs: dict
) -> Any:
    """Hilfsfunktion zum Zeichnen einzelner Funktionen mit Typ-spezifischer Behandlung."""

    # Typ-spezifische Behandlung
    if hasattr(funktion, "graph"):
        # Moderne Funktion mit graph-Methode
        return funktion.graph(**kwargs)

    elif hasattr(funktion, "zeige_funktion"):
        # Legacy-Funktion mit zeige_funktion-Methode
        if x_bereich:
            return funktion.zeige_funktion(x_bereich, **kwargs)
        else:
            return funktion.zeige_funktion(**kwargs)

    elif hasattr(funktion, "plot"):
        # Plotly-kompatible Funktion
        return funktion.plot(**kwargs)

    elif callable(funktion):
        # Normale Python-Funktion
        try:
            from .visualisierung import Graph

            if x_bereich is not None:
                return Graph(funktion, x_min=x_bereich[0], x_max=x_bereich[1], **kwargs)
            else:
                return Graph(funktion, **kwargs)
        except Exception as e:
            raise DatenpunktBerechnungsError(
                getattr(funktion, "__name__", "anonymous"),
                f"Kann Datenpunkte nicht berechnen: {str(e)}",
            )

    else:
        raise TypeError(
            f"Das übergebene Objekt vom Typ {type(funktion).__name__} ist keine zeichnenbare Funktion. "
            "Erwartet wird eine Funktion mit graph(), zeige_funktion(), plot() Methode oder ein callable."
        )


# Für Abwärtskompatibilität
Zeichne = Graph


# =============================================================================
# WERTEBERECHNUNG
# =============================================================================


# =============================================================================
# HELPER-FUNKTIONEN FÜR SCHÜLER
# =============================================================================


# =============================================================================
# FLÄCHENBERECHNUNG
# =============================================================================


def Flaeche(*args, anzeigen: bool = False, **kwargs) -> Any:
    """
    Berechnet Flächen mit automatischer Erkennung des Aufruftyps und optionaler Visualisierung.

    Unterstützte Aufrufe:
    - Flaeche(f, a, b): Fläche zwischen Funktion f und x-Achse über [a, b]
    - Flaeche(f1, f2, a, b): Fläche zwischen zwei Funktionen über [a, b]
    - Flaeche(c, a, b): Fläche der konstanten Funktion f(x) = c über [a, b]
    - Flaeche(c1, c2, a, b): Fläche zwischen zwei konstanten Funktionen

    Intelligente Parametererkennung:
    - Bei 3 Argumenten: Flaeche(funktion, a, b)
    - Bei 4 Argumenten, wenn die letzten beiden Zahlen sind:
      * Flaeche(f1, f2, a, b) - wenn erste beiden Funktionen sind
      * Flaeche(f, c, a, b) - wenn erstes Funktion, zweites Zahl
      * Flaeche(c, f, a, b) - wenn erstes Zahl, zweites Funktion
      * Flaeche(c1, c2, a, b) - wenn beide Zahlen

    Parameters:
    - *args: Variable Argumentliste, wird automatisch analysiert
    - anzeigen: Ob der Graph direkt angezeigt werden soll (Standard: False)
    - **kwargs: Zusätzliche Parameter für die Visualisierung
        - flaeche_farbe: Farbe für Flächenfüllung (Standard: "rgba(0, 100, 255, 0.3)")
        - titel: Benutzerdefinierter Titel für den Graphen

    Returns:
    - Bei anzeigen=False: Plotly-Figure-Objekt
    - Bei anzeigen=True: Plotly-Figure-Objekt (zeigt den Graphen an)
    """

    # Fall 1: 3 Argumente -> Flaeche(f, a, b)
    if len(args) == 3:
        funktion, a, b = args
        zweite_funktion = None
        modus = "eine_funktion"

        # Berechne den numerischen Wert der Fläche
        flaechen_wert = Integral(funktion, a, b)

        # Standardparameter für Flächenvisualisierung
        flaeche_farbe = kwargs.pop("flaeche_farbe", "rgba(0, 100, 255, 0.3)")
        titel = kwargs.pop("titel", f"Fläche unter f(x) von {a} bis {b}")

        # Bereich für die Darstellung automatisch erweitern für bessere Sichtbarkeit
        bereich_erweiterung = (b - a) * 0.2  # 20% Puffer auf jeder Seite
        x_min = a - bereich_erweiterung
        x_max = b + bereich_erweiterung

        # Erstelle Visualisierung mit Flächenfüllung
        fig = Graph(
            funktion,
            x_min=x_min,
            x_max=x_max,
            flaeche=True,
            flaeche_grenzen=(a, b),
            flaeche_farbe=flaeche_farbe,
            titel=titel,
            **kwargs,
        )

    # Fall 2: 4 Argumente -> automatische Erkennung
    elif len(args) == 4:
        arg1, arg2, arg3, arg4 = args

        # Prüfe, ob die letzten beiden Argumente Zahlen sind
        if isinstance(arg3, (int, float)) and isinstance(arg4, (int, float)):
            a, b = arg3, arg4

            from .funktion import Funktion

            # Fall 2a: Flaeche(f1, f2, a, b) - zwei Funktionen
            if isinstance(arg1, Funktion) and isinstance(arg2, Funktion):
                funktion1, funktion2 = arg1, arg2
                modus = "zwei_funktionen"

                # Berechne numerischen Wert der Fläche zwischen zwei Funktionen
                try:
                    # Stelle sicher, dass beide Funktionen die gleiche Variable verwenden
                    if funktion1._variable_symbol != funktion2._variable_symbol:
                        term2 = funktion2.term_sympy.subs(
                            funktion2._variable_symbol, funktion1._variable_symbol
                        )
                    else:
                        term2 = funktion2.term_sympy

                    # Berechne Differenz der Terme
                    differenz_term = funktion1.term_sympy - term2

                    # Erstelle neue Funktion für die Differenz
                    differenz_funktion = Funktion(differenz_term)

                    # Berechne numerischen Wert
                    flaechen_wert = Integral(differenz_funktion, a, b)

                except Exception as e:
                    raise SchulAnalysisError(
                        f"Fehler bei der Flächenberechnung zwischen zwei Funktionen: {str(e)}"
                    )

                # Standardparameter für Flächenvisualisierung
                flaeche_farbe = kwargs.pop("flaeche_farbe", "rgba(0, 100, 255, 0.3)")
                titel = kwargs.pop(
                    "titel", f"Fläche zwischen f₁(x) und f₂(x) von {a} bis {b}"
                )

                # Bereich für die Darstellung automatisch erweitern
                bereich_erweiterung = (b - a) * 0.2
                x_min = a - bereich_erweiterung
                x_max = b + bereich_erweiterung

                # Erstelle Visualisierung mit Flächenfüllung zwischen zwei Funktionen
                fig = Graph(
                    funktion1,
                    funktion2,
                    x_min=x_min,
                    x_max=x_max,
                    flaeche_zwei_funktionen=True,
                    flaeche_grenzen=(a, b),
                    flaeche_farbe=flaeche_farbe,
                    titel=titel,
                    **kwargs,
                )

            # Fall 2b: Flaeche(f, c, a, b) - Funktion und Konstante
            elif isinstance(arg1, Funktion) and isinstance(arg2, (int, float)):
                funktion = arg1
                konstante_funktion = Funktion(arg2)
                modus = "funktion_konstante"

                # Berechne numerischen Wert
                try:
                    if funktion._variable_symbol != konstante_funktion._variable_symbol:
                        term2 = konstante_funktion.term_sympy.subs(
                            konstante_funktion._variable_symbol,
                            funktion._variable_symbol,
                        )
                    else:
                        term2 = konstante_funktion.term_sympy

                    differenz_term = funktion.term_sympy - term2
                    differenz_funktion = Funktion(differenz_term)
                    flaechen_wert = Integral(differenz_funktion, a, b)

                except Exception as e:
                    raise SchulAnalysisError(
                        f"Fehler bei der Flächenberechnung zwischen Funktion und Konstante: {str(e)}"
                    )

                # Standardparameter für Flächenvisualisierung
                flaeche_farbe = kwargs.pop("flaeche_farbe", "rgba(0, 100, 255, 0.3)")
                titel = kwargs.pop(
                    "titel", f"Fläche zwischen f(x) und {arg2} von {a} bis {b}"
                )

                # Bereich für die Darstellung automatisch erweitern
                bereich_erweiterung = (b - a) * 0.2
                x_min = a - bereich_erweiterung
                x_max = b + bereich_erweiterung

                # Erstelle Visualisierung
                fig = Graph(
                    funktion,
                    konstante_funktion,
                    x_min=x_min,
                    x_max=x_max,
                    flaeche_zwei_funktionen=True,
                    flaeche_grenzen=(a, b),
                    flaeche_farbe=flaeche_farbe,
                    titel=titel,
                    **kwargs,
                )

            # Fall 2c: Flaeche(c, f, a, b) - Konstante und Funktion
            elif isinstance(arg1, (int, float)) and isinstance(arg2, Funktion):
                konstante_funktion = Funktion(arg1)
                funktion = arg2
                modus = "konstante_funktion"

                # Berechne numerischen Wert
                try:
                    if konstante_funktion._variable_symbol != funktion._variable_symbol:
                        term2 = funktion.term_sympy.subs(
                            funktion._variable_symbol,
                            konstante_funktion._variable_symbol,
                        )
                    else:
                        term2 = funktion.term_sympy

                    differenz_term = konstante_funktion.term_sympy - term2
                    differenz_funktion = Funktion(differenz_term)
                    flaechen_wert = Integral(differenz_funktion, a, b)

                except Exception as e:
                    raise SchulAnalysisError(
                        f"Fehler bei der Flächenberechnung zwischen Konstante und Funktion: {str(e)}"
                    )

                # Standardparameter für Flächenvisualisierung
                flaeche_farbe = kwargs.pop("flaeche_farbe", "rgba(0, 100, 255, 0.3)")
                titel = kwargs.pop(
                    "titel", f"Fläche zwischen {arg1} und f(x) von {a} bis {b}"
                )

                # Bereich für die Darstellung automatisch erweitern
                bereich_erweiterung = (b - a) * 0.2
                x_min = a - bereich_erweiterung
                x_max = b + bereich_erweiterung

                # Erstelle Visualisierung
                fig = Graph(
                    konstante_funktion,
                    funktion,
                    x_min=x_min,
                    x_max=x_max,
                    flaeche_zwei_funktionen=True,
                    flaeche_grenzen=(a, b),
                    flaeche_farbe=flaeche_farbe,
                    titel=titel,
                    **kwargs,
                )

            # Fall 2d: Flaeche(c1, c2, a, b) - zwei Konstanten
            elif isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
                konstante_funktion1 = Funktion(arg1)
                konstante_funktion2 = Funktion(arg2)
                modus = "zwei_konstanten"

                # Berechne numerischen Wert (einfache Rechtecksfläche)
                flaechen_wert = abs(arg1 - arg2) * (b - a)

                # Standardparameter für Flächenvisualisierung
                flaeche_farbe = kwargs.pop("flaeche_farbe", "rgba(0, 100, 255, 0.3)")
                titel = kwargs.pop(
                    "titel", f"Fläche zwischen {arg1} und {arg2} von {a} bis {b}"
                )

                # Bereich für die Darstellung automatisch erweitern
                bereich_erweiterung = (b - a) * 0.2
                x_min = a - bereich_erweiterung
                x_max = b + bereich_erweiterung

                # Erstelle Visualisierung
                fig = Graph(
                    konstante_funktion1,
                    konstante_funktion2,
                    x_min=x_min,
                    x_max=x_max,
                    flaeche_zwei_funktionen=True,
                    flaeche_grenzen=(a, b),
                    flaeche_farbe=flaeche_farbe,
                    titel=titel,
                    **kwargs,
                )

            else:
                raise ValueError(
                    "Bei 4 Argumenten müssen die letzten beiden Zahlen (a, b) sein"
                )

        else:
            raise ValueError(
                "Bei 4 Argumenten müssen die letzten beiden Zahlen (a, b) sein"
            )

    else:
        raise ValueError(
            f"Ungültige Anzahl an Argumenten: {len(args)}. Erwartet: 3 oder 4"
        )

    # Zeige den Graphen an, wenn gewünscht
    if anzeigen:
        fig.show()

    return fig


def Tangente(funktion: Funktionstyp, stelle: float) -> GanzrationaleFunktion:
    """
    Berechnet die Tangente an eine Funktion an einer gegebenen Stelle.

    Dies ist ein Spezialfall des Taylorpolynoms 1. Grades.

    Args:
        funktion: Die Funktion, an der die Tangente berechnet werden soll
        stelle: Die Stelle, an der die Tangente berührt

    Returns:
        GanzrationaleFunktion: Die Tangente als Funktion

    Beispiele:
        >>> f = ErstellePolynom([1, 0, 0])  # x²
        >>> t = Tangente(f, 1)             # Tangente bei x=1
        >>> print(t.term)                   # 2*x - 1
        >>> print(t(0))                     # -1 (Achsenabschnitt)

    Didaktischer Hinweis:
        Die Tangente ist die beste lineare Näherung an eine Funktion an einer Stelle.
        Sie berührt die Funktion und hat die gleiche Steigung wie die Funktion an dieser Stelle.
    """
    # Taylor-Modul wurde entfernt, implementiere Tangente direkt

    # Implementiere Tangentenberechnung direkt
    if not hasattr(funktion, "ableitung"):
        raise SchulAnalysisError("Funktion hat keine Ableitungsmethode")

    try:
        stelle_expr = sp.sympify(stelle)
        y_wert = funktion.wert(stelle_expr)
        ableitung = funktion.ableitung()
        steigung = ableitung.wert(stelle_expr)

        # Tangentengleichung: y = m(x - x₀) + y₀
        x_sym = sp.Symbol("x")
        tangentengleichung = steigung * (x_sym - stelle_expr) + y_wert

        return Funktion(tangentengleichung)
    except Exception as e:
        raise SchulAnalysisError(
            f"Fehler bei der Tangentenberechnung: {str(e)}\n"
            "Stelle sicher, dass die Funktion an dieser Stelle definiert und differenzierbar ist."
        )


def Taylorpolynom(
    funktion: Funktionstyp, grad: int, entwicklungspunkt: float = 0
) -> GanzrationaleFunktion:
    """
    Berechnet das Taylorpolynom für eine Funktion.

    Args:
        funktion: Die zu approximierende Funktion
        grad: Grad des Taylorpolynoms
        entwicklungspunkt: Entwicklungspunkt (Standard: 0 für MacLaurin-Reihe)

    Returns:
        GanzrationaleFunktion: Das Taylorpolynom als Funktion

    Beispiele:
        >>> f = ErstellePolynom([1, 0, 0])  # x²
        >>> t = Taylorpolynom(f, grad=2)     # Taylorpolynom 2. Grades um x=0
        >>> print(t.term)                   # x^2

        >>> g = Funktion("sin(x)")
        >>> t = Taylorpolynom(g, grad=3)     # x - x³/6 (Approximation von sin(x))

    Didaktischer Hinweis:
        Taylorpolynome nähern Funktionen durch Polynome an.
        Je höher der Grad, desto besser die Näherung (in der Nähe des Entwicklungspunkts).
    """
    # Taylor-Modul wurde entfernt, implementiere Taylorpolynom direkt

    # Implementiere Taylorpolynom-Berechnung direkt
    try:
        entwicklungspunkt_expr = sp.sympify(entwicklungspunkt)
        x_sym = sp.Symbol("x")

        # Taylorpolynom: f(x₀) + f'(x₀)(x-x₀) + f''(x₀)/2!(x-x₀)² + ...
        taylor_term = sp.Integer(0)

        for n in range(grad + 1):
            # n-te Ableitung berechnen
            if n == 0:
                # 0-te Ableitung = Funktion selbst
                wert = funktion.wert(entwicklungspunkt_expr)
            else:
                ableitung = funktion.ableitung(n)
                wert = ableitung.wert(entwicklungspunkt_expr)

            # n! berechnen
            n_fakultaet = sp.factorial(n)

            # Term addieren: f⁽ⁿ⁾(x₀)/n! * (x-x₀)ⁿ
            taylor_term += (wert / n_fakultaet) * (x_sym - entwicklungspunkt_expr) ** n

        return Funktion(taylor_term)
    except Exception as e:
        raise SchulAnalysisError(
            f"Fehler bei der Taylorpolynom-Berechnung: {str(e)}\n"
            "Stelle sicher, dass die Funktion am Entwicklungspunkt definiert und"
            "die angeforderten Ableitungen existieren."
        )


# =============================================================================
# EXPORT: ALLE FUNKTIONEN, DIE IMPORTIERT WERDEN SOLLEN
# =============================================================================

__all__ = [
    # 🔥 KERN-ANALYSE-FUNKTIONEN (Haupt-API für Schüler)
    "Nullstellen",
    "NullstellenMitWiederholungen",
    "Ableitung",
    "Integral",
    "Flaeche",
    "Extremstellen",
    "Extrempunkte",
    "Extrema",  # Alias für Abwärtskompatibilität
    "Wendepunkte",
    "Sattelpunkte",
    "Schnittpunkte",
    # 🔍 SYMMETRIE-FUNKTIONEN
    "Achsensymmetrie",
    "Punktsymmetrie",
    "HatAchsensymmetrie",
    "HatPunktsymmetrie",
    "Symmetrie",  # Für Abwärtskompatibilität
    # 📊 VISUALISIERUNG
    "Graph",
    "Zeichne",  # Für Abwärtskompatibilität
    "Term",
    "Ausmultiplizieren",
    # 📊 STOCHASTIK-VISUALISIERUNG
    "ZeichneBinomialverteilung",
    "ZeichneNormalverteilung",
    "ZeichneNormalverteilungsVergleich",
    # 📐 GEOMETRIE-VISUALISIERUNG
    "ZeichnePunkt",
    "ZeichneGerade",
    "ZeichneZweiPunkteUndGerade",
    "ZeichneSchnittpunktZweierGeraden",
    "ZeichneAbstandZweiPunkte",
    # 📈 TAYLOR-FUNKTIONEN
    "Tangente",
    "Taylorpolynom",
    "FlaecheZweiFunktionen",  # Für Tests
    # Type-Hints
    "Funktionstyp",
]


# =============================================================================
# SPECIELLE FUNKTIONEN FÜR TESTS
# =============================================================================


def FlaecheZweiFunktionen(
    f1: Funktionstyp, f2: Funktionstyp, a: float, b: float, anzeigen: bool = False
) -> float | None:
    """
    Berechnet die Fläche zwischen zwei Funktionen über dem Intervall [a, b].

    Args:
        f1: Erste Funktion (obere Funktion)
        f2: Zweite Funktion (untere Funktion)
        a: Untere Integrationsgrenze
        b: Obere Integrationsgrenze
        anzeigen: Ob die Visualisierung angezeigt werden soll

    Returns:
        float: Fläche zwischen den Funktionen (bei anzeigen=False)
        None: Wenn die Visualisierung angezeigt wird (bei anzeigen=True)

    Examples:
        >>> f1 = GanzrationaleFunktion("x^2")
        >>> f2 = GanzrationaleFunktion("x")
        >>> flaeche = FlaecheZweiFunktionen(f1, f2, 0, 1, anzeigen=False)
        >>> print(f"Fläche: {flaeche}")
    """
    import sympy as sp

    from .visualisierung import Graph as VisualisierungsGraph

    # Berechne Fläche numerisch: ∫[a,b] (f1(x) - f2(x)) dx
    x = sp.symbols("x")
    f1_expr = f1.term_sympy
    f2_expr = f2.term_sympy
    differenz = f1_expr - f2_expr

    # Berechne Integral für numerischen Wert
    flaechen_wert = sp.integrate(differenz, (x, a, b))

    # Behalte exaktes SymPy-Ergebnis bei - wichtig für pädagogische Exaktheit!
    # KEINE Konvertierung zu float, um Brüche wie 1/3 exakt zu erhalten

    # Wenn nur der Wert berechnet werden soll, gib ihn zurück
    if not anzeigen:
        return flaechen_wert

    # Erstelle Visualisierung mit korrekten Parametern
    bereich_erweiterung = (b - a) * 0.2
    x_min = a - bereich_erweiterung
    x_max = b + bereich_erweiterung

    fig = VisualisierungsGraph(
        f1,
        f2,
        x_min=x_min,
        x_max=x_max,
        flaeche_zwei_funktionen=True,
        flaeche_grenzen=(a, b),
        titel=f"Fläche zwischen f₁(x) und f₂(x) von {a} bis {b}",
    )

    # Zeige den Graphen an
    fig.show()
    return None


# =============================================================================
# VISUALISIERUNG FÜR STOCHASTIK
# =============================================================================


def ZeichneBinomialverteilung(
    n: int, p: float, k_max: int | None = None, farbe: str = "blue", **kwargs
) -> Any:
    """
    Zeichnet die Binomialverteilung.

    Args:
        n: Anzahl der Versuche
        p: Erfolgswahrscheinlichkeit
        k_max: Maximale Anzahl der Erfolge zur Darstellung (Standard: n)
        farbe: Farbe für die Balken
        **kwargs: Zusätzliche Parameter für die Visualisierung

    Returns:
        Interaktiver Plotly-Graph

    Beispiele:
        >>> ZeichneBinomialverteilung(n=10, p=0.3)
        >>> ZeichneBinomialverteilung(n=20, p=0.5, k_max=15, farbe="green")
    """
    try:
        from ..stochastik.visualisierung import zeichne_binomialverteilung

        # Konvertiere kwargs zu den erwarteten Parametern
        titel = kwargs.pop("titel", None)
        if titel:
            kwargs["title"] = titel

        return zeichne_binomialverteilung(n, p, k_max, farbe, **kwargs)
    except Exception as e:
        raise SchulAnalysisError(
            f"Fehler bei der Binomialverteilungs-Darstellung: {str(e)}"
        )


def ZeichneNormalverteilung(
    mu: float,
    sigma: float,
    x_bereich: tuple = (-4, 4),
    farbe: str = "blue",
    sigma_bereiche: bool = True,
    **kwargs,
) -> Any:
    """
    Zeichnet die Normalverteilung.

    Args:
        mu: Erwartungswert
        sigma: Standardabweichung
        x_bereich: Darstellungsbereich als (min, max) in Einheiten von sigma
        farbe: Farbe für die Kurve
        sigma_bereiche: Sigma-Bereiche hervorheben
        **kwargs: Zusätzliche Parameter für die Visualisierung

    Returns:
        Interaktiver Plotly-Graph

    Beispiele:
        >>> ZeichneNormalverteilung(mu=0, sigma=1)  # Standardnormalverteilung
        >>> ZeichneNormalverteilung(mu=100, sigma=15, x_bereich=(-3, 3))
        >>> ZeichneNormalverteilung(mu=50, sigma=10, sigma_bereiche=False)
    """
    try:
        from ..stochastik.visualisierung import zeichne_normalverteilung

        # Konvertiere kwargs zu den erwarteten Parametern
        titel = kwargs.pop("titel", None)
        if titel:
            kwargs["title"] = titel

        return zeichne_normalverteilung(
            mu, sigma, x_bereich, farbe, sigma_bereiche, **kwargs
        )
    except Exception as e:
        raise SchulAnalysisError(
            f"Fehler bei der Normalverteilungs-Darstellung: {str(e)}"
        )


def ZeichneNormalverteilungsVergleich(
    mu1: float,
    sigma1: float,
    mu2: float,
    sigma2: float,
    x_bereich: tuple | None = None,
    farbe1: str = "blue",
    farbe2: str = "red",
    **kwargs,
) -> Any:
    """
    Vergleicht zwei Normalverteilungen in einem Graphen.

    Args:
        mu1, sigma1: Parameter der ersten Verteilung
        mu2, sigma2: Parameter der zweiten Verteilung
        x_bereich: Darstellungsbereich (automatisch, wenn None)
        farbe1, farbe2: Farben für die Verteilungen
        **kwargs: Zusätzliche Parameter für die Visualisierung

    Returns:
        Interaktiver Plotly-Graph

    Beispiele:
        >>> # Vergleich von zwei Verteilungen
        >>> ZeichneNormalverteilungsVergleich(mu1=0, sigma1=1, mu2=2, sigma2=1.5)

        # Vergleich mit benutzerdefinierten Farben
        >>> ZeichneNormalverteilungsVergleich(mu1=100, sigma1=15, mu2=120, sigma2=20,
        ...                                 farbe1="green", farbe2="orange")
    """
    try:
        from ..stochastik.visualisierung import (
            zeichne_vergleich_zwei_normalverteilungen,
        )

        # Konvertiere kwargs zu den erwarteten Parametern
        titel = kwargs.pop("titel", None)
        if titel:
            kwargs["title"] = titel

        return zeichne_vergleich_zwei_normalverteilungen(
            mu1, sigma1, mu2, sigma2, x_bereich, farbe1, farbe2, **kwargs
        )
    except Exception as e:
        raise SchulAnalysisError(
            f"Fehler beim Vergleich der Normalverteilungen: {str(e)}"
        )


# =============================================================================
# VISUALISIERUNG FÜR GEOMETRIE
# =============================================================================


def ZeichnePunkt(punkt: Any, farbe: str = "red", groesse: int = 10, **kwargs) -> Any:
    """
    Zeichnet einen Punkt im 2D-Koordinatensystem.

    Args:
        punkt: Punkt-Objekt aus dem Geometrie-Modul
        farbe: Farbe des Punktes
        groesse: Größe des Punktes
        **kwargs: Zusätzliche Parameter für die Visualisierung

    Returns:
        Interaktiver Plotly-Graph

    Beispiele:
        >>> from schul_mathematik.geometrie import Punkt
        >>> P = Punkt([2, 3], "P")
        >>> ZeichnePunkt(P)

        >>> # Mit benutzerdefinierter Farbe
        >>> ZeichnePunkt(P, farbe="blue", groesse=15)
    """
    try:
        from ..geometrie.visualisierung import zeichne_punkt_2d

        # Konvertiere kwargs zu den erwarteten Parametern
        titel = kwargs.pop("titel", None)
        if titel:
            kwargs["title"] = titel

        return zeichne_punkt_2d(punkt, farbe, groesse, **kwargs)
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Punkt-Darstellung: {str(e)}")


def ZeichneGerade(
    gerade: Any,
    x_bereich: tuple[float, float] = (-10, 10),
    farbe: str = "blue",
    aufpunkt_farbe: str = "red",
    **kwargs,
) -> Any:
    """
    Zeichnet eine Gerade im 2D-Koordinatensystem.

    Args:
        gerade: Geraden-Objekt aus dem Geometrie-Modul
        x_bereich: x-Bereich für die Darstellung
        farbe: Farbe der Geraden
        aufpunkt_farbe: Farbe des Aufpunktes
        **kwargs: Zusätzliche Parameter für die Visualisierung

    Returns:
        Interaktiver Plotly-Graph

    Beispiele:
        >>> from schul_mathematik.geometrie import Punkt, Gerade, gerade_durch_zwei_punkte
        >>> P1 = Punkt([1, 2], "P1")
        >>> P2 = Punkt([4, 6], "P2")
        >>> g = gerade_durch_zwei_punkte(P1, P2, "g")
        >>> ZeichneGerade(g)

        >>> # Mit angepasstem Bereich
        >>> ZeichneGerade(g, x_bereich=(-5, 10), farbe="green")
    """
    try:
        from ..geometrie.visualisierung import zeichne_gerade_2d

        # Konvertiere kwargs zu den erwarteten Parametern
        titel = kwargs.pop("titel", None)
        if titel:
            kwargs["title"] = titel

        return zeichne_gerade_2d(gerade, x_bereich, farbe, aufpunkt_farbe, **kwargs)
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Geraden-Darstellung: {str(e)}")


def ZeichneZweiPunkteUndGerade(
    p1: Any, p2: Any, x_bereich: tuple[float, float] = (-10, 10), **kwargs
) -> Any:
    """
    Zeichnet zwei Punkte und die Gerade durch beide Punkte.

    Args:
        p1: Erster Punkt
        p2: Zweiter Punkt
        x_bereich: x-Bereich für die Darstellung
        **kwargs: Zusätzliche Parameter für die Visualisierung

    Returns:
        Interaktiver Plotly-Graph

    Beispiele:
        >>> from schul_mathematik.geometrie import Punkt
        >>> A = Punkt([1, 1], "A")
        >>> B = Punkt([5, 3], "B")
        >>> ZeichneZweiPunkteUndGerade(A, B)

        >>> # Mit angepasstem Bereich
        >>> ZeichneZweiPunkteUndGerade(A, B, x_bereich=(0, 8))
    """
    try:
        from ..geometrie.visualisierung import zeichne_zwei_punkte_und_gerade

        # Konvertiere kwargs zu den erwarteten Parametern
        titel = kwargs.pop("titel", None)
        if titel:
            kwargs["title"] = titel

        return zeichne_zwei_punkte_und_gerade(p1, p2, x_bereich, **kwargs)
    except Exception as e:
        raise SchulAnalysisError(
            f"Fehler bei der Darstellung von zwei Punkten und Gerade: {str(e)}"
        )


def ZeichneSchnittpunktZweierGeraden(
    g1: Any, g2: Any, x_bereich: tuple[float, float] = (-10, 10), **kwargs
) -> Any:
    """
    Zeichnet zwei Geraden und ihren Schnittpunkt.

    Args:
        g1: Erste Gerade
        g2: Zweite Gerade
        x_bereich: x-Bereich für die Darstellung
        **kwargs: Zusätzliche Parameter für die Visualisierung

    Returns:
        Interaktiver Plotly-Graph

    Beispiele:
        >>> from schul_mathematik.geometrie import Punkt, Gerade
        >>> g1 = Gerade(Punkt([0, 0], "A"), Punkt([1, 1], "V1"), "g1")
        >>> g2 = Gerade(Punkt([0, 2], "B"), Punkt([1, 0], "V2"), "g2")
        >>> ZeichneSchnittpunktZweierGeraden(g1, g2)
    """
    try:
        from ..geometrie.visualisierung import zeichne_schnittpunkt_zweier_geraden

        # Konvertiere kwargs zu den erwarteten Parametern
        titel = kwargs.pop("titel", None)
        if titel:
            kwargs["title"] = titel

        return zeichne_schnittpunkt_zweier_geraden(g1, g2, x_bereich, **kwargs)
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Schnittpunkt-Darstellung: {str(e)}")


def ZeichneAbstandZweiPunkte(
    p1: Any, p2: Any, x_bereich: tuple[float, float] = (-10, 10), **kwargs
) -> Any:
    """
    Zeichnet zwei Punkte und ihren Abstand.

    Args:
        p1: Erster Punkt
        p2: Zweiter Punkt
        x_bereich: x-Bereich für die Darstellung
        **kwargs: Zusätzliche Parameter für die Visualisierung

    Returns:
        Interaktiver Plotly-Graph

    Beispiele:
        >>> from schul_mathematik.geometrie import Punkt
        >>> P = Punkt([1, 2], "P")
        >>> Q = Punkt([4, 6], "Q")
        >>> ZeichneAbstandZweiPunkte(P, Q)

        >>> # Mit angepasstem Bereich
        >>> ZeichneAbstandZweiPunkte(P, Q, x_bereich=(0, 8))
    """
    try:
        from ..geometrie.visualisierung import zeichne_abstand_zwei_punkte

        # Konvertiere kwargs zu den erwarteten Parametern
        titel = kwargs.pop("titel", None)
        if titel:
            kwargs["title"] = titel

        return zeichne_abstand_zwei_punkte(p1, p2, x_bereich, **kwargs)
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei der Abstands-Darstellung: {str(e)}")


# =============================================================================
# ABWÄRTSKOMPATIBILITÄT: ALIASE FÜR ALTE API-NAMEN
# =============================================================================


def Extrema(funktion: Funktionstyp) -> list[tuple[Any, str]]:
    """
    Alias für Extremstellen zur Abwärtskompatibilität.

    Args:
        funktion: Die zu analysierende Funktion

    Returns:
        Liste der Extremstellen mit Typ-Informationen

    Note:
        Diese Funktion existiert nur für Abwärtskompatibilität
        mit älteren Tests und Dokumentation.
        Neue Code sollte Extremstellen() verwenden.
    """
    return Extremstellen(funktion)
