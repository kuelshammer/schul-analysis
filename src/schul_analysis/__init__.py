"""
Schul-Analysis Framework

Ein Python Framework für Schul-Analysis mit exakter Berechnung und Marimo-Integration.
"""

import numpy as np
import plotly.graph_objects as go

from .config import config
from .ganzrationale import GanzrationaleFunktion
from .gebrochen_rationale import GebrochenRationaleFunktion
from .schmiegkurven import Schmiegkurve
from .taylorpolynom import Taylorpolynom

# ====================
# Hilfsfunktionen für intelligente Skalierung
# ====================


def _finde_interessante_punkte(funktion):
    """Sammelt alle interessanten Punkte einer Funktion für die automatische Skalierung

    Args:
        funktion: GanzrationaleFunktion oder GebrochenRationaleFunktion

    Returns:
        dict: Dictionary mit x_koordinaten und punkten Listen
    """
    punkte = {
        "nullstellen": [],
        "extremstellen": [],
        "wendepunkte": [],
        "polstellen": [],
    }

    try:
        # Nullstellen
        if hasattr(funktion, "nullstellen"):
            punkte["nullstellen"] = funktion.nullstellen()

        # Extremstellen
        if hasattr(funktion, "extremstellen"):
            extremstellen = funktion.extremstellen()
            # Extrahiere x-Koordinaten (könnten Tupel sein)
            punkte["extremstellen"] = [
                es[0] if isinstance(es, tuple) else es for es in extremstellen
            ]

        # Wendepunkte
        if hasattr(funktion, "wendepunkte"):
            wendepunkte = funktion.wendepunkte()
            # Extrahiere x-Koordinaten (könnten Tupel sein)
            punkte["wendepunkte"] = [
                wp[0] if isinstance(wp, tuple) and len(wp) >= 1 else wp
                for wp in wendepunkte
            ]

        # Polstellen (nur für gebrochen-rationale Funktionen)
        if hasattr(funktion, "polstellen"):
            punkte["polstellen"] = funktion.polstellen()

    except Exception:
        # Bei Fehlern leere Listen zurückgeben
        pass

    return punkte


def _berechne_optimalen_bereich(
    punkte_dict,
    default_range=(-10, 10),
    min_buffer=1.0,
    proportional_buffer=0.15,  # Reduziert von 0.2 auf 0.15
    min_span=5.0,
):
    """Berechnet optimalen x-Bereich basierend auf interessanten Punkten mit robuster Logik

    Args:
        punkte_dict: Dictionary mit interessanten Punkten
        default_range: Standardbereich wenn keine Punkte gefunden (Default: (-10, 10))
        min_buffer: Minimaler absoluter Puffer (Default: 1.0)
        proportional_buffer: Proportionaler Puffer (Default: 0.15 = 15%)
        min_span: Minimale Gesamtbreite der x-Achse (Default: 5.0)

    Returns:
        tuple: (x_min, x_max) optimaler Bereich
    """
    import math
    import statistics

    # 1. Sammle und bereinige alle x-Koordinaten
    alle_x = []
    for kategorie, punkte_liste in punkte_dict.items():
        if kategorie == "polstellen":
            continue  # Polstellen überspringen, da sie das Bild verzerren können

        # GEMINI FIX: Bessere Iterable-Handhabung
        if not isinstance(punkte_liste, (list, tuple)):
            # Wenn es kein Iterable ist, behandle es als einzelnen Punkt
            punkte_liste = [punkte_liste]

        for p in punkte_liste:
            if p is None:
                continue

            x_val = None
            if isinstance(p, (tuple, list)):
                if len(p) > 0:
                    x_val = p[0]
            else:
                x_val = p

            if x_val is not None:
                try:
                    num_x = float(x_val)
                    # Schließe NaN und Unendlich-Werte aus
                    if not math.isinf(num_x) and not math.isnan(num_x):
                        alle_x.append(num_x)
                except (ValueError, TypeError):
                    continue

    # 2. Behandle Edge Cases
    if not alle_x:
        return default_range

    # GEMINI FIX: Entferne redundante Einzel-Punkt-Logik (wird von Hauptlogik abgedeckt)

    # 3. Berechne Kernbereich
    x_min = min(alle_x)
    x_max = max(alle_x)
    span = x_max - x_min

    # Behandle den Fall dass alle Punkte auf dem gleichen x-Wert liegen
    if span == 0:
        return (x_min - min_span / 2, x_min + min_span / 2)

    # 4. GEMINI OPTIMIERUNG: Berechne adaptiven Puffer basierend auf Punkt-Dichte
    if len(alle_x) >= 2:
        # Sortiere Punkte und berechne Abstände
        sortierte_x = sorted(alle_x)
        abstaende = [
            sortierte_x[i + 1] - sortierte_x[i] for i in range(len(sortierte_x) - 1)
        ]

        if abstaende:
            # Verwende Median der Abstände als Basis für adaptiven Puffer
            median_abstand = statistics.median(abstaende)
            adaptiver_puffer = median_abstand * 1.5  # Faktor 1.5 für guten Sichtbereich

            # Hybrid-Buffer: Maximum aus adaptivem und proportionalem Puffer
            final_buffer = max(min_buffer, adaptiver_puffer, span * proportional_buffer)
        else:
            # Fallback auf alten Algorithmus
            final_buffer = max(min_buffer, span * proportional_buffer)
    else:
        # Für einzelnen Punkt oder keine Abstände
        final_buffer = max(min_buffer, span * proportional_buffer)

    # 5. Wende Puffer an
    final_min = x_min - final_buffer
    final_max = x_max + final_buffer

    # 6. GEMINI OPTIMIERUNG: Null-Punkt-Sicherheitsprüfung für pädagogischen Kontext
    # Stelle sicher dass der Ursprung sichtbar ist, wenn der Bereich nah an 0 ist
    if final_min > 0 and final_min / (final_max - final_min) < 0.2:
        final_min = 0
    elif final_max < 0 and abs(final_max) / (final_max - final_min) < 0.2:
        final_max = 0

    # 7. Erzwinge minimale Endspanne
    final_span = final_max - final_min
    if final_span < min_span:
        delta = (min_span - final_span) / 2
        final_min -= delta
        final_max += delta
        print(
            f"DEBUG: Final-Spanne zu klein ({final_span} < {min_span}), korrigiert auf: [{final_min}, {final_max}]"
        )

    # 8. GEMINI OPTIMIERUNG: Globale Limits zur Verhinderung von extremen Bereichen
    global_limit = 50  # Absolute Grenze
    if final_min < -global_limit:
        final_min = -global_limit
    if final_max > global_limit:
        final_max = global_limit

    return (final_min, final_max)


def _berechne_y_bereich(
    funktion,
    x_min,
    x_max,
    interessante_punkte=None,
    min_bereich=(-5, 5),
    punkte=100,
    puffer=0.1,
):
    """Berechnet optimalen y-Bereich basierend auf Funktionswerten

    Args:
        funktion: Die zu analysierende Funktion
        x_min, x_max: x-Bereich für die Auswertung
        interessante_punkte: Dictionary mit interessanten Punkten für bessere y-Berechnung
        min_bereich: Minimaler y-Bereich der garantiert wird
        punkte: Anzahl der Auswertungspunkte
        puffer: Zusätzlicher Puffer (10%)

    Returns:
        tuple: (y_min, y_max)
    """
    try:
        # Sammle y-Werte aus interessanten Punkten
        interessante_y = []
        if interessante_punkte:
            for _kategorie, punkte_liste in interessante_punkte.items():
                try:
                    for p in punkte_liste:
                        if p is not None:
                            if isinstance(p, tuple) and len(p) >= 2:
                                # Bei Tupeln (x, y, ...) die y-Koordinate nehmen
                                interessante_y.append(float(p[1]))
                except (ValueError, TypeError, IndexError):
                    continue

        # Erstelle x-Werte für die Auswertung
        x_werte = np.linspace(x_min, x_max, punkte)
        y_werte = []

        # Berechne Funktionswerte, vermeide Probleme bei Polstellen
        for x in x_werte:
            try:
                y = funktion.wert(x)
                if not np.isinf(y) and not np.isnan(y):
                    y_werte.append(y)
            except (ValueError, ZeroDivisionError, OverflowError):
                continue

        # Kombiniere alle y-Werte
        alle_y = y_werte + interessante_y

        if not alle_y:
            return min_bereich

        # Finde y-Bereich mit Puffer
        y_min_auto = min(alle_y)
        y_max_auto = max(alle_y)

        # Füge Puffer hinzu
        hoehe = y_max_auto - y_min_auto
        if hoehe > 0:
            puffer_wert = hoehe * puffer
            y_min_auto -= puffer_wert
            y_max_auto += puffer_wert
        else:
            # Falls alle y-Werte gleich sind
            y_min_auto -= 1
            y_max_auto += 1

        # Stelle sicher dass min_bereich eingehalten wird
        y_min_final = min(y_min_auto, min_bereich[0])
        y_max_final = max(y_max_auto, min_bereich[1])

        return (y_min_final, y_max_final)

    except Exception:
        return min_bereich


def _erstelle_plotly_figur(funktion, x_min, x_max, y_min, y_max, **kwargs):
    """Erstelle die eigentliche Plotly-Figur mit allen Features

    Args:
        funktion: Die zu darstellende Funktion
        x_min, x_max, y_min, y_max: Bereichsgrenzen
        **kwargs: Zusätzliche Optionen

    Returns:
        go.Figure: Plotly-Figur
    """
    # Optionen extrahieren
    zeige_nullstellen = kwargs.get("zeige_nullstellen", True)
    zeige_extremstellen = kwargs.get("zeige_extremstellen", True)
    zeige_wendepunkte = kwargs.get("zeige_wendepunkte", True)
    zeige_polstellen = kwargs.get("zeige_polstellen", True)
    titel = kwargs.get("titel")
    punkte_anzahl = kwargs.get("punkte", 200)

    # Erstelle x-Werte für die Berechnung
    x_werte = np.linspace(x_min, x_max, punkte_anzahl)
    y_werte = []
    gueltige_x = []

    # Berechne Funktionswerte, vermeide Polstellen
    if hasattr(funktion, "polstellen"):
        polstellen = [float(ps) for ps in funktion.polstellen()]
    else:
        polstellen = []

    for x in x_werte:
        try:
            # Prüfe, ob x nahe einer Polstelle ist
            ist_nahe_polstelle = any(abs(x - ps) < 0.1 for ps in polstellen)
            if ist_nahe_polstelle:
                continue

            y = funktion.wert(x)
            if not np.isinf(y) and not np.isnan(y):
                y_werte.append(y)
                gueltige_x.append(x)
        except (ValueError, ZeroDivisionError, OverflowError):
            continue

    # Erstelle die Figur
    fig = go.Figure()

    # Hauptkurve
    if gueltige_x and y_werte:
        fig.add_trace(
            go.Scatter(
                x=gueltige_x,
                y=y_werte,
                mode="lines",
                name=f"f(x) = {funktion.term()}",
                line=config.get_line_config(color_key="primary"),
                hovertemplate="<b>x</b>: %{x:.3f}<br><b>f(x)</b>: %{y:.3f}<extra></extra>",
            )
        )

    # Füge spezielle Punkte hinzu (nur für ganzrationale Funktionen)
    if hasattr(funktion, "nullstellen") and zeige_nullstellen:
        nullstellen = funktion.nullstellen()
        for ns in nullstellen:
            try:
                x_ns = float(ns)
                if x_min <= x_ns <= x_max:
                    fig.add_trace(
                        go.Scatter(
                            x=[x_ns],
                            y=[0],
                            mode="markers",
                            name=f"Nullstelle x={x_ns:.3f}",
                            marker=config.get_marker_config(
                                color_key="secondary", size=10
                            ),
                            showlegend=False,
                            hovertemplate=f"<b>Nullstelle</b><br>x: {x_ns:.3f}<br>f(x): 0<extra></extra>",
                        )
                    )
            except (ValueError, TypeError):
                continue

    if hasattr(funktion, "extremstellen") and zeige_extremstellen:
        extremstellen = funktion.extremstellen()
        for es in extremstellen:
            try:
                if isinstance(es, tuple):
                    x_es = float(es[0])
                    art = es[1]
                else:
                    x_es = float(es)
                    art = "Extremum"

                y_es = funktion.wert(x_es)
                if x_min <= x_es <= x_max:
                    color = "green" if art == "Maximum" else "orange"
                    fig.add_trace(
                        go.Scatter(
                            x=[x_es],
                            y=[y_es],
                            mode="markers",
                            name=f"{art} ({x_es:.3f}|{y_es:.3f})",
                            marker=config.get_marker_config(color_key=color, size=12),
                            showlegend=False,
                            hovertemplate=f"<b>{art}</b><br>x: {x_es:.3f}<br>f(x): {y_es:.3f}<extra></extra>",
                        )
                    )
            except (ValueError, TypeError):
                continue

    if hasattr(funktion, "wendepunkte") and zeige_wendepunkte:
        wendepunkte = funktion.wendepunkte()
        for wp in wendepunkte:
            try:
                if isinstance(wp, tuple) and len(wp) >= 2:
                    x_ws = float(wp[0])
                    y_ws = float(wp[1])
                    art = wp[2] if len(wp) >= 3 else "Wendepunkt"
                else:
                    continue

                if x_min <= x_ws <= x_max:
                    fig.add_trace(
                        go.Scatter(
                            x=[x_ws],
                            y=[y_ws],
                            mode="markers",
                            name=f"Wendepunkt ({x_ws:.3f}|{y_ws:.3f})",
                            marker=config.get_marker_config(
                                color_key="tertiary", size=10
                            ),
                            showlegend=False,
                            hovertemplate=f"<b>Wendepunkt</b><br>x: {x_ws:.3f}<br>f(x): {y_ws:.3f}<br>Krümmung: {art}<extra></extra>",
                        )
                    )
            except (ValueError, TypeError, IndexError):
                continue

    # Polstellen und Asymptoten für gebrochen-rationale Funktionen
    if hasattr(funktion, "polstellen") and zeige_polstellen:
        for ps in polstellen:
            if x_min <= ps <= x_max:
                # Berechne y-Werte für die Asymptote
                y_asymptote_range = np.linspace(y_min, y_max, 100)
                fig.add_trace(
                    go.Scatter(
                        x=[ps] * len(y_asymptote_range),
                        y=y_asymptote_range,
                        mode="lines",
                        line={"color": "red", "width": 2, "dash": "dash"},
                        name=f"Polstelle x={ps:.2f}",
                        showlegend=False,
                    )
                )

    # 🔥 MARIMO-KOMPATIBLE KONFIGURATION 🔥
    layout_config = config.get_plot_config()
    layout_config.update(
        {
            "title": titel or f"Funktion: f(x) = {funktion.term()}",
            "xaxis": {
                **config.get_axis_config(mathematical_mode=True),
                "range": [
                    float(x_min),
                    float(x_max),
                ],  # Explizite Konvertierung zu float
                "title": "x",
                "autorange": False,  # Stellt sicher dass unsere Range verwendet wird
                # Marimo-spezifische Parameter um Überschreibung zu verhindern
                "uirevision": True,  # Verhindert dass Marimo die Layout-Einstellungen zurücksetzt
                "constraintoward": "center",  # Zentriert den Bereich
                "fixedrange": False,  # Erlaubt Zoom aber behält ursprünglichen Bereich
            },
            "yaxis": {
                **config.get_axis_config(mathematical_mode=False),
                "range": [
                    float(y_min),
                    float(y_max),
                ],  # Explizite Konvertierung zu float
                "title": "f(x)",
                "autorange": False,  # Stellt sicher dass unsere Range verwendet wird
                # Marimo-spezifische Parameter um Überschreibung zu verhindern
                "uirevision": True,  # Verhindert dass Marimo die Layout-Einstellungen zurücksetzt
                "constraintoward": "center",  # Zentriert den Bereich
                "fixedrange": False,  # Erlaubt Zoom aber behält ursprünglichen Bereich
            },
            "showlegend": True,
            "hovermode": "x unified",
            # Globale Marimo-Kompatibilitätseinstellungen
            "uirevision": True,  # Verhindert dass Marimo das gesamte Layout zurücksetzt
        }
    )

    fig.update_layout(layout_config)

    # 🔥 MHRFACHE SICHERHEITSMASSNAHMEN FÜR MARIMO 🔥
    # Erzwinge Range-Update mit verschiedenen Methoden
    fig.update_xaxes(
        range=[float(x_min), float(x_max)], autorange=False, constraintoward="center"
    )
    fig.update_yaxes(
        range=[float(y_min), float(y_max)], autorange=False, constraintoward="center"
    )

    # Zusätzliche Sicherheitsmaßnahme: Setze die Ranges nochmal explizit
    fig.layout.xaxis.range = [float(x_min), float(x_max)]
    fig.layout.yaxis.range = [float(y_min), float(y_max)]

    return fig


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


def Graph(funktion, x_min=None, x_max=None, y_min=None, y_max=None, **kwargs):
    """Erzeugt einen Graphen der Funktion mit intelligenter automatischer Skalierung

    Args:
        funktion: Eine GanzrationaleFunktion oder GebrochenRationaleFunktion
        x_min: Untere x-Grenze (Standard: None = automatisch)
        x_max: Obere x-Grenze (Standard: None = automatisch)
        y_min: Untere y-Grenze (Standard: None = automatisch)
        y_max: Obere y-Grenze (Standard: None = automatisch)
        **kwargs: Zusätzliche Parameter für die plotly-Methode

    Returns:
        Plotly-Figure

    Beispiele:
        >>> f = GanzrationaleFunktion("x^2")
        >>> graph = Graph(f)  # Automatische Skalierung

        >>> # Manuelles Setzen von Grenzen
        >>> graph = Graph(f, x_min=0, x_max=5)

        >>> # Nur x-Grenzen festlegen, y automatisch
        >>> graph = Graph(f, x_min=-2, x_max=2)

        >>> # Alle Grenzen manuell
        >>> graph = Graph(f, x_min=-3, x_max=3, y_min=0, y_max=10)
    """
    # Finde interessante Punkte und berechne optimalen Bereich
    interessante_punkte = _finde_interessante_punkte(funktion)

    # Berechne x-Bereich
    if x_min is None or x_max is None:
        auto_x_min, auto_x_max = _berechne_optimalen_bereich(interessante_punkte)
        if x_min is None:
            x_min = auto_x_min
        if x_max is None:
            x_max = auto_x_max

    # Berechne y-Bereich
    if y_min is None or y_max is None:
        auto_y_min, auto_y_max = _berechne_y_bereich(
            funktion, x_min, x_max, interessante_punkte
        )
        if y_min is None:
            y_min = auto_y_min
        if y_max is None:
            y_max = auto_y_max

    # Erstelle Plotly-Figur
    return _erstelle_plotly_figur(funktion, x_min, x_max, y_min, y_max, **kwargs)


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


def Wendepunkte(funktion, typ: bool = True, runden=None):
    """Berechnet die Wendepunkte einer Funktion

    Args:
        funktion: Eine GanzrationaleFunktion
        typ: Wenn True (Standard), werden die Wendepunkte klassifiziert.
             Wenn False, werden nur die Koordinaten zurückgegeben.
        runden: Anzahl Nachkommastellen für Rundung (None = exakt)

    Returns:
        list: Liste von Tupeln (x, y, art) mit den Wendepunkten (typ=True)
              oder Liste der Koordinaten (x, y) (typ=False)

    Beispiele:
        >>> f = GanzrationaleFunktion("x^3")
        >>> Wendepunkte(f)
        [(0, 0, 'Wendepunkt')]
        >>> Wendepunkte(f, typ=False)
        [(0, 0)]
        >>> Wendepunkte(f, runden=2)
        [(0.0, 0.0, 'Wendepunkt')]

        >>> g = GanzrationaleFunktion("x^4-4x^3")
        >>> Wendepunkte(g)
        [(0.0, 0.0, 'Wendepunkt'), (2.0, -16.0, 'Wendepunkt')]
        >>> Wendepunkte(g, typ=False)
        [(0.0, 0.0), (2.0, -16.0)]
    """
    return funktion.wendepunkte(typ=typ, runden=runden)


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
) -> float | None:
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

        if (
            links_limit is not None
            and rechts_limit is not None
            and abs(links_limit - rechts_limit) < 1e-10
        ):
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
