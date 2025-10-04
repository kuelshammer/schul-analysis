"""
Visualisierungs-Module für das Schul-Analysis Framework

Dieses Modul enthält Funktionen zur graphischen Darstellung von Funktionen,
einschließlich intelligenter Skalierung und Plotly-Integration.
"""

import numpy as np
import plotly.graph_objects as go

from .config import config
from .funktion import Funktion

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
# Haupt-Visualisierungsfunktionen
# ====================


def Graph(*funktionen, x_min=None, x_max=None, y_min=None, y_max=None, **kwargs):
    """Erzeugt einen Graphen für eine oder mehrere Funktionen mit intelligenter Skalierung

    Args:
        *funktionen: Eine oder mehrere Funktionen (GanzrationaleFunktion, GebrochenRationaleFunktion)
        x_min, x_max: Optionale x-Bereichsgrenzen (werden automatisch berechnet wenn nicht angegeben)
        y_min, y_max: Optionale y-Bereichsgrenzen (werden automatisch berechnet wenn nicht angegeben)
        **kwargs: Zusätzliche Optionen:
            - titel: Titel für den Graphen
            - punkte: Anzahl der Berechnungspunkte (Standard: 200)
            - zeige_nullstellen: Zeige Nullstellen (Standard: True)
            - zeige_extremstellen: Zeige Extremstellen (Standard: True)
            - zeige_wendepunkte: Zeige Wendepunkte (Standard: True)
            - zeige_polstellen: Zeige Polstellen (Standard: True)

    Returns:
        plotly.graph_objects.Figure: Plotly-Figur mit der/den Funktion(en)

    Beispiele:
        >>> # Einzelne Funktion mit automatischer Skalierung
        >>> f = GanzrationaleFunktion("x^2 - 4")
        >>> fig = Graph(f)

        >>> # Mehrere Funktionen mit manuellem Bereich
        >>> g = GanzrationaleFunktion("2x + 1")
        >>> fig = Graph(f, g, x_min=-5, x_max=5, y_min=-10, y_max=20)

        >>> # Mit Titel und Optionen
        >>> fig = Graph(f, titel="Parabel f(x) = x² - 4", zeige_extremstellen=False)
    """
    if not funktionen:
        raise ValueError("Mindestens eine Funktion muss angegeben werden")

    # Validiere alle Funktionen
    for f in funktionen:
        if not isinstance(f, Funktion):
            raise TypeError("Alle Argumente müssen Funktionen sein")

    # Wenn nur eine Funktion übergeben wurde, wende die bestehende Logik an
    if len(funktionen) == 1:
        funktion = funktionen[0]

        # Automatische Bereichsberechnung wenn nicht angegeben
        if x_min is None or x_max is None:
            interessante_punkte = _finde_interessante_punkte(funktion)
            x_min_auto, x_max_auto = _berechne_optimalen_bereich(
                interessante_punkte, default_range=(-10, 10)
            )

            if x_min is None:
                x_min = x_min_auto
            if x_max is None:
                x_max = x_max_auto

        if y_min is None or y_max is None:
            interessante_punkte = _finde_interessante_punkte(funktion)
            y_min_auto, y_max_auto = _berechne_y_bereich(
                funktion, x_min, x_max, interessante_punkte
            )

            if y_min is None:
                y_min = y_min_auto
            if y_max is None:
                y_max = y_max_auto

        return _erstelle_plotly_figur(funktion, x_min, x_max, y_min, y_max, **kwargs)

    # Bei mehreren Funktionen: Kombinierte Logik
    else:
        # Sammle interessante Punkte von allen Funktionen
        alle_interessante_punkte = []
        for f in funktionen:
            punkte = _finde_interessante_punkte(f)
            alle_interessante_punkte.append(punkte)

        # Berechne kombinierten x-Bereich
        if x_min is None or x_max is None:
            # Kombiniere alle Punkte für die Bereichsberechnung
            kombinierte_punkte = {
                "nullstellen": [],
                "extremstellen": [],
                "wendepunkte": [],
                "polstellen": [],
            }

            for punkte_dict in alle_interessante_punkte:
                for kategorie, punkte_liste in punkte_dict.items():
                    kombinierte_punkte[kategorie].extend(punkte_liste)

            x_min_auto, x_max_auto = _berechne_optimalen_bereich(
                kombinierte_punkte, default_range=(-10, 10)
            )

            if x_min is None:
                x_min = x_min_auto
            if x_max is None:
                x_max = x_max_auto

        # Berechne y-Bereich basierend auf allen Funktionen
        if y_min is None or y_max is None:
            alle_y_werte = []

            for f in funktionen:
                x_werte = np.linspace(x_min, x_max, 200)
                for x in x_werte:
                    try:
                        y = f.wert(x)
                        if not np.isinf(y) and not np.isnan(y):
                            alle_y_werte.append(y)
                    except (ValueError, ZeroDivisionError, OverflowError):
                        continue

            if alle_y_werte:
                y_min_auto = min(alle_y_werte)
                y_max_auto = max(alle_y_werte)

                # Füge Puffer hinzu
                hoehe = y_max_auto - y_min_auto
                if hoehe > 0:
                    puffer = hoehe * 0.1
                    y_min_auto -= puffer
                    y_max_auto += puffer
                else:
                    y_min_auto -= 1
                    y_max_auto += 1

                if y_min is None:
                    y_min = y_min_auto
                if y_max is None:
                    y_max = y_max_auto
            else:
                # Fallback
                if y_min is None:
                    y_min = -5
                if y_max is None:
                    y_max = 5

        # Erstelle Figur für mehrere Funktionen
        fig = go.Figure()

        # Farben für verschiedene Funktionen
        farben = ["blue", "red", "green", "orange", "purple", "brown", "pink", "gray"]

        for i, funktion in enumerate(funktionen):
            farbe = farben[i % len(farben)]

            # Berechne Funktionswerte
            x_werte = np.linspace(x_min, x_max, 200)
            y_werte = []
            gueltige_x = []

            for x in x_werte:
                try:
                    y = funktion.wert(x)
                    if not np.isinf(y) and not np.isnan(y):
                        y_werte.append(y)
                        gueltige_x.append(x)
                except (ValueError, ZeroDivisionError, OverflowError):
                    continue

            if gueltige_x and y_werte:
                fig.add_trace(
                    go.Scatter(
                        x=gueltige_x,
                        y=y_werte,
                        mode="lines",
                        name=f"f{i + 1}(x) = {funktion.term()}",
                        line={"color": farbe, "width": 2},
                        hovertemplate=f"<b>x</b>: %{{x:.3f}}<br><b>f{i + 1}(x)</b>: %{{y:.3f}}<extra></extra>",
                    )
                )

        # Konfiguration
        layout_config = config.get_plot_config()
        layout_config.update(
            {
                "title": kwargs.get("titel", "Vergleich mehrerer Funktionen"),
                "xaxis": {
                    **config.get_axis_config(mathematical_mode=True),
                    "range": [float(x_min), float(x_max)],
                    "title": "x",
                    "autorange": False,
                    "uirevision": True,
                    "constraintoward": "center",
                    "fixedrange": False,
                },
                "yaxis": {
                    **config.get_axis_config(mathematical_mode=False),
                    "range": [float(y_min), float(y_max)],
                    "title": "y",
                    "autorange": False,
                    "uirevision": True,
                    "constraintoward": "center",
                    "fixedrange": False,
                },
                "showlegend": True,
                "hovermode": "x unified",
                "uirevision": True,
            }
        )

        fig.update_layout(layout_config)
        fig.update_xaxes(
            range=[float(x_min), float(x_max)],
            autorange=False,
            constraintoward="center",
        )
        fig.update_yaxes(
            range=[float(y_min), float(y_max)],
            autorange=False,
            constraintoward="center",
        )

        # Zusätzliche Sicherheitsmaßnahme
        fig.layout.xaxis.range = [float(x_min), float(x_max)]
        fig.layout.yaxis.range = [float(y_min), float(y_max)]

        return fig
