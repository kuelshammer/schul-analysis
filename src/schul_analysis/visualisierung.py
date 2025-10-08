"""
Visualisierungs-Module für das Schul-Analysis Framework

Dieses Modul enthält Funktionen zur graphischen Darstellung von Funktionen,
einschließlich intelligenter Skalierung und Plotly-Integration.
"""

import numpy as np
import plotly.graph_objects as go
import math

from .config import config
from .funktion import Funktion


# ====================
# Hilfsfunktionen für intelligente Achsenintervalle
# ====================


def _berechne_intelligenter_puffer(min_val, max_val, schrittweite=None):
    """Berechnet intelligenten Puffer mit 5% + Mindestpuffer

    Args:
        min_val, max_val: Wertebereich
        schrittweite: Optionale Schrittweite für Mindestpuffer

    Returns:
        float: Berechneter Puffer
    """
    if min_val == max_val:
        return 1.0  # Standardpuffer bei Einzelpunkt

    spanne = max_val - min_val
    if spanne <= 0:
        return 1.0

    # Prozentualer Puffer: 5% der Spanne
    prozentualer_puffer = spanne * 0.05

    # Mindestpuffer: 1.0 Einheit oder die aktuelle Schrittweite
    mindestpuffer = max(1.0, schrittweite if schrittweite is not None else 1.0)

    # Verwende das Maximum von beiden
    return max(prozentualer_puffer, mindestpuffer)


def _berechne_intervalle(min_val, max_val, max_ticks=8):
    """Berechnet optimale Intervalle für benutzerfreundliche Beschriftungen

    Args:
        min_val, max_val: Wertebereich
        max_ticks: Maximale Anzahl an Ticks (Standard: 8)

    Returns:
        float: Optimale Schrittweite
    """
    span = max_val - min_val
    if span <= 0:
        return 1.0

    # Bevorzugte Schrittweiten (runde Werte)
    moegliche_schritte = [1, 2, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100]

    # Berechne rohe Schrittweite
    raw_step = span / max_ticks

    # Finde die Größenordnung (10er-Potenz)
    magnitude = 10 ** math.floor(math.log10(raw_step))

    # Normalisiere auf 0-100 Bereich
    normalized_step = raw_step / magnitude

    # Finde die beste Schrittweite aus der Liste
    best_step = min(moegliche_schritte, key=lambda x: abs(x - normalized_step))

    return best_step * magnitude


def _optimiere_achse_einfach(min_val, max_val, max_ticks=8):
    """Optimiert Achsenbereich für runde Beschriftungen OHNE wichtige Punkte Puffer
    Args:
        min_val, max_val: Originaler Wertebereich
        max_ticks: Maximale Anzahl an Ticks (Standard: 8)
    Returns:
        tuple: (optimiertes_min, optimiertes_max, schrittweite)
    """
    if min_val == max_val:
        # Einzelpunkt: Bereich zentrieren
        return min_val - 1, max_val + 1, 1.0
    # Berechne optimale Schrittweite
    step = _berechne_intervalle(min_val, max_val, max_ticks)
    # Spezialfall: Wenn Grenzen nahe an ganzen Zahlen sind, bevorzuge ganzzahlige Grenzen
    if abs(min_val - round(min_val)) < 0.2 and abs(max_val - round(max_val)) < 0.2:
        # Beide Grenzen sind nahe an ganzen Zahlen
        min_rounded = round(min_val)
        max_rounded = round(max_val)
        span = max_rounded - min_rounded
        # Prüfe ob wir mit ganzzahliger Schrittweite auskommen oder ob es ein spezieller Fall ist
        if span <= max_ticks or (span <= 16 and max_ticks >= 6):
            # Bei größeren Bereichen bis 16 Einheiten: erlaube mehr Ticks für bessere Ästhetik
            new_min = min_rounded
            new_max = max_rounded
            step = 1.0
            # Stelle sicher dass Originalbereich enthalten ist
            if new_min > min_val:
                new_min -= 1
            if new_max < max_val:
                new_max += 1
        else:
            # Zu viele Ticks für Schrittweite 1, verwende normale Logik
            new_min = math.floor(min_val / step) * step
            new_max = math.ceil(max_val / step) * step
            # Stelle sicher dass Originalbereich enthalten ist
            if new_min > min_val:
                new_min -= step
            if new_max < max_val:
                new_max += step
    else:
        # Normale Logik für nicht-ganzzahlige Grenzen
        new_min = math.floor(min_val / step) * step
        new_max = math.ceil(max_val / step) * step
        # Stelle sicher dass Originalbereich enthalten ist
        if new_min > min_val:
            new_min -= step
        if new_max < max_val:
            new_max += step
    # Verhindere zu kleine Bereiche
    if new_max - new_min < step:
        new_min -= step
        new_max += step
    return new_min, new_max, step


def _optimiere_achse(min_val, max_val, max_ticks=8, wichtige_punkte=None):
    """Optimiert Achsenbereich für runde Beschriftungen

    Args:
        min_val, max_val: Originaler Wertebereich
        max_ticks: Maximale Anzahl an Ticks (Standard: 8)
        wichtige_punkte: Liste wichtiger X-Koordinaten (z.B. Nullstellen)

    Returns:
        tuple: (optimiertes_min, optimiertes_max, schrittweite)
    """
    if min_val == max_val:
        # Einzelpunkt: Bereich zentrieren
        return min_val - 1, max_val + 1, 1.0

    # Berechne optimale Schrittweite
    step = _berechne_intervalle(min_val, max_val, max_ticks)

    # Spezialfall: Wenn Grenzen nahe an ganzen Zahlen sind, bevorzuge ganzzahlige Grenzen
    if abs(min_val - round(min_val)) < 0.2 and abs(max_val - round(max_val)) < 0.2:
        # Beide Grenzen sind nahe an ganzen Zahlen
        min_rounded = round(min_val)
        max_rounded = round(max_val)
        span = max_rounded - min_rounded

        # Prüfe ob wir mit ganzzahliger Schrittweite auskommen oder ob es ein spezieller Fall ist
        if span <= max_ticks or (span <= 16 and max_ticks >= 6):
            # Bei größeren Bereichen bis 16 Einheiten: erlaube mehr Ticks für bessere Ästhetik
            new_min = min_rounded
            new_max = max_rounded
            step = 1.0

            # Stelle sicher dass Originalbereich enthalten ist
            if new_min > min_val:
                new_min -= 1
            if new_max < max_val:
                new_max += 1

            # Zusätzlicher Puffer für wichtige Punkte: verhindere dass wichtige Punkte am Rand liegen
            if wichtige_punkte:
                # Berechne intelligenten Puffer basierend auf 5% + Mindestpuffer
                int_puffer = _berechne_intelligenter_puffer(new_min, new_max, step)

                for punkt_x in wichtige_punkte:
                    if punkt_x is not None:
                        # Linker Rand
                        if abs(punkt_x - new_min) <= int_puffer:
                            new_min = math.floor(punkt_x - int_puffer)
                        # Rechter Rand
                        if abs(punkt_x - new_max) <= int_puffer:
                            new_max = math.ceil(punkt_x + int_puffer)
        else:
            # Zu viele Ticks für Schrittweite 1, verwende normale Logik
            new_min = math.floor(min_val / step) * step
            new_max = math.ceil(max_val / step) * step

            # Stelle sicher dass Originalbereich enthalten ist
            if new_min > min_val:
                new_min -= step
            if new_max < max_val:
                new_max += step
    else:
        # Normale Logik für nicht-ganzzahlige Grenzen
        new_min = math.floor(min_val / step) * step
        new_max = math.ceil(max_val / step) * step

        # Stelle sicher dass Originalbereich enthalten ist
        if new_min > min_val:
            new_min -= step
        if new_max < max_val:
            new_max += step

    # Verhindere zu kleine Bereiche
    if new_max - new_min < step:
        new_min -= step
        new_max += step

    return new_min, new_max, step


# ====================
# Vereinfachte Punktesammlung
# ====================


def _sammle_interessante_punkte(funktion):
    """Sammelt alle interessanten Punkte einer Funktion für die Bereichsberechnung

    Args:
        funktion: Die zu analysierende Funktion

    Returns:
        dict: Dictionary mit x_werten, y_werten und punkten_mit_koordinaten
    """
    punkte = {
        "x_werte": [],
        "y_werte": [],
        "punkte_mit_koordinaten": [],  # (art, x, y) für Warnungen
    }

    try:
        # Nullstellen
        if hasattr(funktion, "nullstellen"):
            for ns in funktion.nullstellen:
                try:
                    x_val = _formatiere_float(ns)
                    punkte["x_werte"].append(x_val)
                    punkte["y_werte"].append(0.0)
                    punkte["punkte_mit_koordinaten"].append(("Nullstelle", x_val, 0.0))
                except (ValueError, TypeError):
                    continue

        # Extremstellen
        if hasattr(funktion, "extremstellen"):
            for es in funktion.extremstellen:
                try:
                    if isinstance(es, tuple) and len(es) >= 1:
                        x_val = _formatiere_float(es[0])
                        y_val = _formatiere_float(funktion.wert(x_val))
                        art = es[1] if len(es) >= 2 else "Extremum"

                        punkte["x_werte"].append(x_val)
                        punkte["y_werte"].append(y_val)
                        punkte["punkte_mit_koordinaten"].append((art, x_val, y_val))
                    else:
                        # Einzelner Wert (x-Koordinate)
                        x_val = _formatiere_float(es)
                        y_val = _formatiere_float(funktion.wert(x_val))

                        punkte["x_werte"].append(x_val)
                        punkte["y_werte"].append(y_val)
                        punkte["punkte_mit_koordinaten"].append(
                            ("Extremum", x_val, y_val)
                        )
                except (ValueError, TypeError, ZeroDivisionError):
                    continue

        # Wendepunkte
        if hasattr(funktion, "wendepunkte"):
            for wp in funktion.wendepunkte:
                try:
                    if isinstance(wp, tuple) and len(wp) >= 2:
                        x_val = _formatiere_float(wp[0])
                        y_val = _formatiere_float(wp[1])
                        art = wp[2] if len(wp) >= 3 else "Wendepunkt"

                        punkte["x_werte"].append(x_val)
                        punkte["y_werte"].append(y_val)
                        punkte["punkte_mit_koordinaten"].append((art, x_val, y_val))
                except (ValueError, TypeError, IndexError):
                    continue

        # Polstellen (nur Y-Werte relevant für asymptotisches Verhalten)
        if hasattr(funktion, "polstellen"):
            try:
                polstellen_liste = funktion.polstellen()
                for ps in polstellen_liste:
                    try:
                        x_val = _formatiere_float(ps)
                        # Für Polstellen nur X-Werte speichern (Y geht gegen Unendlich)
                        punkte["x_werte"].append(x_val)
                        # Kein Y-Wert für Polstellen, da diese gegen Unendlich gehen
                        punkte["punkte_mit_koordinaten"].append(
                            ("Polstelle", x_val, None)
                        )
                    except (ValueError, TypeError):
                        continue
            except (AttributeError, TypeError):
                # Manche Funktionen haben keine polstellen() Methode
                pass

    except Exception as e:
        import logging

        logging.debug(f"Fehler beim Sammeln von Punkten: {e}")

    return punkte


def _filtere_sichtbare_punkte(punkte, x_min=None, x_max=None, y_min=None, y_max=None):
    """Filtert Punkte basierend auf Bereichsgrenzen und gibt Warnungen zurück

    Args:
        punkte: Ergebnis von _sammle_interessante_punkte
        x_min, x_max: X-Bereichsgrenzen (None = keine Begrenzung)
        y_min, y_max: Y-Bereichsgrenzen (None = keine Begrenzung)

    Returns:
        tuple: (sichtbare_punkte, abgeschnittene_punkte)
    """
    # Standardwerte: Unendlich = keine Begrenzung
    x_min_eff = x_min if x_min is not None else float("-inf")
    x_max_eff = x_max if x_max is not None else float("inf")
    y_min_eff = y_min if y_min is not None else float("-inf")
    y_max_eff = y_max if y_max is not None else float("inf")

    sichtbare_punkte = []
    abgeschnittene_punkte = []

    for art, x_val, y_val in punkte["punkte_mit_koordinaten"]:
        # Sonderbehandlung für Polstellen (kein Y-Wert)
        if art == "Polstelle":
            if x_min_eff <= x_val <= x_max_eff:
                sichtbare_punkte.append((art, x_val, y_val))
            else:
                abgeschnittene_punkte.append((art, x_val, y_val))
        else:
            # Normale Punkte mit X- und Y-Koordinaten
            if (x_min_eff <= x_val <= x_max_eff) and (y_min_eff <= y_val <= y_max_eff):
                sichtbare_punkte.append((art, x_val, y_val))
            else:
                abgeschnittene_punkte.append((art, x_val, y_val))

    return sichtbare_punkte, abgeschnittene_punkte


# ====================
# Hilfsfunktionen für intelligente Skalierung (Legacy)
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
            punkte["nullstellen"] = funktion.nullstellen

        # Extremstellen
        if hasattr(funktion, "extremstellen"):
            extremstellen = funktion.extremstellen
            # Extrahiere x-Koordinaten (könnten Tupel sein)
            punkte["extremstellen"] = [
                es[0] if isinstance(es, tuple) else es for es in extremstellen
            ]

        # Wendepunkte
        if hasattr(funktion, "wendepunkte"):
            wendepunkte = funktion.wendepunkte
            # Extrahiere x-Koordinaten (könnten Tupel sein)
            punkte["wendepunkte"] = [
                wp[0] if isinstance(wp, tuple) and len(wp) >= 1 else wp
                for wp in wendepunkte
            ]

        # Polstellen (nur für gebrochen-rationale Funktionen)
        if hasattr(funktion, "polstellen"):
            punkte["polstellen"] = funktion.polstellen()

    except (AttributeError, ValueError, TypeError):
        # Bei Fehlern leere Listen zurückgeben
        import logging

        logging.debug(
            f"Fehler beim Berechnen von Sonderpunkten für {getattr(funktion, 'term_str', str(funktion))}"
        )
        pass

    return punkte


def _berechne_optimalen_bereich(
    punkte_dict,
    default_range=(-5, 5),
    min_buffer=1.0,
    proportional_buffer=0.15,  # Reduziert von 0.2 auf 0.15
    min_span=5.0,
):
    """Berechnet optimalen x-Bereich basierend auf interessanten Punkten mit robuster Logik

    Args:
        punkte_dict: Dictionary mit interessanten Punkten
        default_range: Standardbereich wenn keine Punkte gefunden (Default: (-5, 5))
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
                    num_x = _formatiere_float(x_val)
                    # Schließe NaN und Unendlich-Werte aus
                    if num_x is not None:
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
    default_range=(-5, 5),
    punkte=100,
    puffer=0.15,
):
    """Berechnet optimalen y-Bereich basierend auf Funktionswerten

    Args:
        funktion: Die zu analysierende Funktion
        x_min, x_max: x-Bereich für die Auswertung
        interessante_punkte: Dictionary mit interessanten Punkten für bessere y-Berechnung
        default_range: Standardbereich wenn keine Werte gefunden (Default: (-5, 5))
        punkte: Anzahl der Auswertungspunkte
        puffer: Zusätzlicher Puffer (15%)

    Returns:
        tuple: (y_min, y_max)
    """
    try:
        # Sammle y-Werte aus interessanten Punkten
        interessante_y = []
        if interessante_punkte:
            for kategorie, punkte_liste in interessante_punkte.items():
                try:
                    for p in punkte_liste:
                        if p is not None:
                            if isinstance(p, tuple):
                                if kategorie == "extremstellen" and len(p) >= 2:
                                    # Bei Extremstellen (x, art): Berechne y-Wert durch Auswertung
                                    x_val = p[0]
                                    y_val = funktion.wert(x_val)
                                    if _ist_endlich(y_val):
                                        y_float = _formatiere_float(y_val)
                                        if y_float is not None:
                                            interessante_y.append(y_float)
                                elif kategorie == "wendepunkte" and len(p) >= 2:
                                    # Bei Wendepunkten (x, y, art): nimm den y-Wert
                                    y_val = p[1]  # y-Wert ist an Position 1
                                    if _ist_endlich(y_val):
                                        y_float = _formatiere_float(y_val)
                                        if y_float is not None:
                                            interessante_y.append(y_float)
                                elif len(p) >= 2:
                                    # Fallback für andere Tupel-Typen
                                    y_val = _formatiere_float(p[1])
                                    if y_val is not None:
                                        interessante_y.append(y_val)
                            else:
                                # Bei einzelnen Punkten: könnte y-Wert sein
                                y_val = _formatiere_float(p)
                                if y_val is not None:
                                    interessante_y.append(y_val)
                except (ValueError, TypeError, IndexError):
                    continue

        # Erstelle x-Werte für die Auswertung
        x_werte = np.linspace(x_min, x_max, punkte)
        y_werte = []

        # Berechne Funktionswerte, vermeide Probleme bei Polstellen
        for x in x_werte:
            try:
                y = funktion.wert(x)
                if _ist_endlich(y):
                    y_werte.append(_formatiere_float(y))
            except (ValueError, ZeroDivisionError, OverflowError):
                continue

        # Kombiniere alle y-Werte
        alle_y = y_werte + interessante_y

        if not alle_y:
            return default_range

        # EINFACHE ROBUSTE METHODE
        # 1. Berechne y-Werte aller wichtigen Punkte (Extremstellen, Wendepunkte)
        wichtige_y_werte = []

        # Hole y-Werte von Extremstellen
        if hasattr(funktion, "extremstellen"):
            for extremstelle in funktion.extremstellen:
                if isinstance(extremstelle, tuple) and len(extremstelle) >= 1:
                    x_val = extremstelle[0]
                    y_val = funktion.wert(x_val)
                    if _ist_endlich(y_val):
                        y_float = _formatiere_float(y_val)
                        if y_float is not None:
                            wichtige_y_werte.append(y_float)

        # Hole y-Werte von Wendepunkten
        if hasattr(funktion, "wendepunkte"):
            for wendepunkt in funktion.wendepunkte:
                if isinstance(wendepunkt, tuple) and len(wendepunkt) >= 2:
                    y_val = wendepunkt[1]  # y-Wert ist an Position 1
                    if _ist_endlich(y_val):
                        y_float = _formatiere_float(y_val)
                        if y_float is not None:
                            wichtige_y_werte.append(y_float)

        # 2. Berechne Basisbereich aus allen y-Werten (mit Ausreißer-Schutz)
        y_array = np.array([y for y in alle_y if y is not None])

        if len(y_array) > 0:
            # Verwende Quantile um Ausreißer zu ignorieren
            q10 = np.percentile(y_array, 10)
            q90 = np.percentile(y_array, 90)
            y_min_basis = q10
            y_max_basis = q90
        else:
            y_min_basis = -5
            y_max_basis = 5

        # 3. Erweitere Bereich um ALLE wichtigen Punkte einzuschließen (garantiert sichtbar)
        if wichtige_y_werte:
            y_min_wichtig = min(wichtige_y_werte)
            y_max_wichtig = max(wichtige_y_werte)

            # Starte mit einem Bereich der ALLE wichtigen Punkte einschließt
            y_min_auto = min(y_min_basis, y_min_wichtig)
            y_max_auto = max(y_max_basis, y_max_wichtig)

            # Erweitere ausreichend um alle Punkte garantiert sichtbar zu machen
            spanne_wichtig = y_max_wichtig - y_min_wichtig
            if spanne_wichtig > 0:
                # Füge genug Platz damit Punkte nicht am Rand kleben
                extra_puffer = max(
                    spanne_wichtig * 0.5, 10.0
                )  # Mindestens 10 Einheiten
                y_min_auto = min(y_min_auto, y_min_wichtig - extra_puffer)
                y_max_auto = max(y_max_auto, y_max_wichtig + extra_puffer)
        else:
            y_min_auto = y_min_basis
            y_max_auto = y_max_basis

        # 4. Füge zusätzlichen Puffer hinzu
        hoehe = y_max_auto - y_min_auto
        if hoehe > 0:
            puffer_wert = max(hoehe * puffer, 3.0)  # Mindestens 3 Einheiten Puffer
            y_min_auto -= puffer_wert
            y_max_auto += puffer_wert
        else:
            y_min_auto -= 3
            y_max_auto += 3

        # 5. Nur bei EXTREM großen Bereichen begrenzen, aber alle wichtigen Punkte erhalten
        gesamtbreite = y_max_auto - y_min_auto
        if (
            gesamtbreite > 400
        ):  # Reduziert von 800 auf 400 für pädagogisch angemessene Darstellung
            # Behalte alle wichtigen Punkte sichtbar, aber reduziere extreme Bereiche
            if wichtige_y_werte:
                # Finde den kleinsten Bereich der alle wichtigen Punkte abdeckt
                y_min_final = min(wichtige_y_werte)
                y_max_final = max(wichtige_y_werte)

                # Füge angemessenen Puffer hinzu - reduziert von 2.5x auf 2.0x
                noetige_spanne = (
                    y_max_final - y_min_final
                ) * 2.0  # 2.0x die nötige Spanne
                center = (y_min_final + y_max_final) / 2

                y_min_auto = center - noetige_spanne / 2
                y_max_auto = center + noetige_spanne / 2

        # 6. Absolutbegrenzung für pädagogische Eignung (neu)
        y_grenze = 400  # Maximale Ausdehnung in Y-Richtung (erhöht von 200 auf 400)
        if y_max_auto - y_min_auto > y_grenze:
            # Dynamische Bereichsanpassung: Stelle sicher dass alle wichtigen Punkte gut sichtbar sind
            if wichtige_y_werte:
                y_min_final = min(wichtige_y_werte)
                y_max_final = max(wichtige_y_werte)

                # Berechne notwendige Spanne mit ausreichend Puffer für gute Sichtbarkeit
                noetige_spanne = (
                    y_max_final - y_min_final
                ) * 3.0  # 3x Puffer für klare Sichtbarkeit

                # Wenn die notwendige Spanne kleiner als y_grenze ist, verwende sie
                if noetige_spanne <= y_grenze:
                    center = (y_min_final + y_max_final) / 2
                    y_min_auto = center - noetige_spanne / 2
                    y_max_auto = center + noetige_spanne / 2
                else:
                    # Ansonsten verwende die maximale Grenze, aber zentriere um wichtige Punkte
                    center = sum(wichtige_y_werte) / len(wichtige_y_werte)
                    y_min_auto = center - y_grenze / 2
                    y_max_auto = center + y_grenze / 2
            else:
                # Fallback: Zentriere um 0
                y_min_auto = -y_grenze / 2
                y_max_auto = y_grenze / 2

        return (y_min_auto, y_max_auto)

    except (ValueError, TypeError, AttributeError):
        # Bei Fehlern Default-Bereich zurückgeben
        import logging

        logging.debug(
            f"Fehler beim Berechnen des y-Bereichs für Funktion im Bereich ({x_min}, {x_max})"
        )
        return default_range


def _berechne_y_bereich_mehrfach(funktionen, x_min, x_max, default_range=(-5, 5)):
    """Berechnet optimalen y-Bereich für mehrere Funktionen mit intelligenter Logik

    Args:
        funktionen: Liste der zu analysierenden Funktionen
        x_min, x_max: x-Bereich für die Auswertung
        default_range: Standardbereich wenn keine Werte gefunden (Default: (-5, 5))

    Returns:
        tuple: (y_min, y_max)
    """
    try:
        # 1. Sammle wichtige Punkte von ALLEN Funktionen
        alle_wichtige_y_werte = []
        alle_y_werte = []

        for funktion in funktionen:
            # Sammle y-Werte von wichtigen Punkten dieser Funktion
            funktion_wichtige_y = []

            # Extremstellen
            if hasattr(funktion, "extremstellen"):
                for extremstelle in funktion.extremstellen:
                    if isinstance(extremstelle, tuple) and len(extremstelle) >= 1:
                        x_val = extremstelle[0]
                        y_val = funktion.wert(x_val)
                        if _ist_endlich(y_val):
                            y_float = _formatiere_float(y_val)
                            if y_float is not None:
                                funktion_wichtige_y.append(y_float)
                                alle_wichtige_y_werte.append(y_float)

            # Wendepunkte
            if hasattr(funktion, "wendepunkte"):
                for wendepunkt in funktion.wendepunkte:
                    if isinstance(wendepunkt, tuple) and len(wendepunkt) >= 2:
                        y_val = wendepunkt[1]  # y-Wert ist an Position 1
                        if _ist_endlich(y_val):
                            y_float = _formatiere_float(y_val)
                            if y_float is not None:
                                funktion_wichtige_y.append(y_float)
                                alle_wichtige_y_werte.append(y_float)

            # Sammle einige Funktionswerte für die Basisbereichsberechnung
            x_werte = np.linspace(
                x_min, x_max, 50
            )  # Reduziert von 200 auf 50 für Effizienz
            for x in x_werte:
                try:
                    y = funktion.wert(x)
                    if _ist_endlich(y):
                        y_float = _formatiere_float(y)
                        if y_float is not None:
                            alle_y_werte.append(y_float)
                except (ValueError, ZeroDivisionError, OverflowError):
                    continue

        # 2. Wenn keine wichtigen Punkte gefunden, verwende einfache Logik
        if not alle_wichtige_y_werte:
            if alle_y_werte:
                y_min_auto = min(alle_y_werte)
                y_max_auto = max(alle_y_werte)
                # Füge Puffer hinzu
                hoehe = y_max_auto - y_min_auto
                if hoehe > 0:
                    puffer = hoehe * 0.15
                    y_min_auto -= puffer
                    y_max_auto += puffer
                else:
                    y_min_auto -= 1
                    y_max_auto += 1
                return (y_min_auto, y_max_auto)
            else:
                return default_range

        # 3. Berechne Basisbereich mit Quantilen (wie bei einzelnen Funktionen)
        if alle_y_werte:
            y_array = np.array([y for y in alle_y_werte if y is not None])
            if len(y_array) > 0:
                q10 = np.percentile(y_array, 10)
                q90 = np.percentile(y_array, 90)
                y_min_basis = q10
                y_max_basis = q90
            else:
                y_min_basis = min(alle_wichtige_y_werte)
                y_max_basis = max(alle_wichtige_y_werte)
        else:
            y_min_basis = min(alle_wichtige_y_werte)
            y_max_basis = max(alle_wichtige_y_werte)

        # 4. Erweitere Bereich um ALLE wichtigen Punkte einzuschließen
        y_min_wichtig = min(alle_wichtige_y_werte)
        y_max_wichtig = max(alle_wichtige_y_werte)

        y_min_auto = min(y_min_basis, y_min_wichtig)
        y_max_auto = max(y_max_basis, y_max_wichtig)

        # 5. Füge ausreichend Puffer hinzu (3x wie bei einzelnen Funktionen)
        spanne_wichtig = y_max_wichtig - y_min_wichtig
        if spanne_wichtig > 0:
            noetige_spanne = spanne_wichtig * 3.0  # 3x Puffer für klare Sichtbarkeit
            center = (y_min_wichtig + y_max_wichtig) / 2
            y_min_auto = min(y_min_auto, center - noetige_spanne / 2)
            y_max_auto = max(y_max_auto, center + noetige_spanne / 2)

        # 6. Zusätzlicher Puffer
        hoehe = y_max_auto - y_min_auto
        if hoehe > 0:
            puffer_wert = max(hoehe * 0.15, 3.0)
            y_min_auto -= puffer_wert
            y_max_auto += puffer_wert
        else:
            y_min_auto -= 3
            y_max_auto += 3

        # 7. Absolutbegrenzung auf 400 Einheiten (wie bei einzelnen Funktionen)
        y_grenze = 400
        if y_max_auto - y_min_auto > y_grenze:
            # Zentriere um die wichtigen Punkte
            center = sum(alle_wichtige_y_werte) / len(alle_wichtige_y_werte)
            y_min_auto = center - y_grenze / 2
            y_max_auto = center + y_grenze / 2

        return (y_min_auto, y_max_auto)

    except (ValueError, TypeError, AttributeError):
        # Bei Fehlern Default-Bereich zurückgeben
        return default_range


def _ist_numerischer_wert(y):
    """Prüft, ob ein SymPy-Objekt ein numerischer Wert ist."""
    if hasattr(y, "is_number") and y.is_number:
        return True
    try:
        float(y)
        return True
    except (TypeError, ValueError):
        return False


def _ist_endlich(y):
    """Prüft, ob ein SymPy-Objekt endlich ist (kein inf oder nan)."""
    if not _ist_numerischer_wert(y):
        return False

    try:
        y_float = float(y)
        return not (math.isinf(y_float) or math.isnan(y_float))
    except (TypeError, ValueError):
        return False


def _formatiere_float(y):
    """Formatiert einen SymPy-Wert als Float für die Visualisierung."""
    try:
        return float(y)
    except (TypeError, ValueError):
        return None


def _erstelle_plotly_figur_mit_intelligenten_achsen(
    funktion, x_min, x_max, y_min, y_max, x_step=None, y_step=None, **kwargs
):
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
        polstellen = [_formatiere_float(ps) for ps in funktion.polstellen()]
    else:
        polstellen = []

    for x in x_werte:
        try:
            # Prüfe, ob x nahe einer Polstelle ist
            ist_nahe_polstelle = any(abs(x - ps) < 0.1 for ps in polstellen)
            if ist_nahe_polstelle:
                continue

            y = funktion.wert(x)
            if _ist_endlich(y):
                y_werte.append(_formatiere_float(y))
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
        nullstellen = funktion.nullstellen
        for ns in nullstellen:
            try:
                x_ns = _formatiere_float(ns)
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
        extremstellen = funktion.extremstellen
        for es in extremstellen:
            try:
                if isinstance(es, tuple):
                    x_es = _formatiere_float(es[0])
                    art = es[1]
                else:
                    x_es = _formatiere_float(es)
                    art = "Extremum"

                y_es = funktion.wert(x_es)
                if _ist_endlich(y_es) and x_min <= x_es <= x_max:
                    color = "green" if art == "Maximum" else "orange"
                    fig.add_trace(
                        go.Scatter(
                            x=[x_es],
                            y=[_formatiere_float(y_es)],
                            mode="markers",
                            name=f"{art} ({x_es:.3f}|{_formatiere_float(y_es):.3f})",
                            marker=config.get_marker_config(color_key=color, size=12),
                            showlegend=False,
                            hovertemplate=f"<b>{art}</b><br>x: {x_es:.3f}<br>f(x): {_formatiere_float(y_es):.3f}<extra></extra>",
                        )
                    )
            except (ValueError, TypeError):
                continue

    if hasattr(funktion, "wendepunkte") and zeige_wendepunkte:
        wendepunkte = funktion.wendepunkte
        for wp in wendepunkte:
            try:
                if isinstance(wp, tuple) and len(wp) >= 2:
                    x_ws = _formatiere_float(wp[0])
                    y_ws = _formatiere_float(wp[1])
                    art = wp[2] if len(wp) >= 3 else "Wendepunkt"
                else:
                    continue

                if _ist_endlich(y_ws) and x_min <= x_ws <= x_max:
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

    # 🔥 INTELLIGENTE ACHSENKONFIGURATION 🔥
    layout_config = config.get_plot_config()

    # Intelligente Achsenkonfiguration basierend auf Schrittweiten
    xaxis_config = {
        **config.get_axis_config(
            mathematical_mode=False
        ),  # Kein 1:1-Verhältnis für bessere Sichtbarkeit
        "range": [float(x_min), float(x_max)],
        "title": "x",
        "autorange": False,  # Stellt sicher dass unsere Range verwendet wird
        "uirevision": True,  # Verhindert dass Marimo die Layout-Einstellungen zurücksetzt
        "constraintoward": "center",  # Zentriert den Bereich
        "fixedrange": False,  # Erlaubt Zoom aber behält ursprünglichen Bereich
    }

    yaxis_config = {
        **config.get_axis_config(mathematical_mode=False),
        "range": [float(y_min), float(y_max)],
        "title": "f(x)",
        "autorange": False,  # Stellt sicher dass unsere Range verwendet wird
        "uirevision": True,  # Verhindert dass Marimo die Layout-Einstellungen zurücksetzt
        "constraintoward": "center",  # Zentriert den Bereich
        "fixedrange": False,  # Erlaubt Zoom aber behält ursprünglichen Bereich
    }

    # Füge optimierte Schrittweiten hinzu (nur für automatische Bereiche)
    if x_step is not None:
        xaxis_config["dtick"] = x_step
        xaxis_config["tick0"] = x_min  # Erster Tick bei Minimum

    if y_step is not None:
        yaxis_config["dtick"] = y_step
        yaxis_config["tick0"] = y_min  # Erster Tick bei Minimum

    layout_config.update(
        {
            "title": titel or f"Funktion: f(x) = {funktion.term()}",
            "xaxis": xaxis_config,
            "yaxis": yaxis_config,
            "showlegend": True,
            "hovermode": "x unified",
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
# Bereichsberechnung mit manueller Kontrolle
# ====================


def _berechne_finale_grenzen(funktion, x_min=None, x_max=None, y_min=None, y_max=None):
    """Berechnet finale Darstellungsgrenzen mit intelligenter Puffer-Logik

    Args:
        funktion: Die zu analysierende Funktion
        x_min, x_max: Manuelle X-Bereichsgrenzen (None = automatisch)
        y_min, y_max: Manuelle Y-Bereichsgrenzen (None = automatisch)

    Returns:
        tuple: (final_x_min, final_x_max, final_y_min, final_y_max, x_step, y_step)
    """
    # Sammle interessante Punkte
    punkte = _sammle_interessante_punkte(funktion)

    # === GRUNDBEREICH BERECHNEN ===
    # X-Basisbereich aus wichtigen Punkten
    if punkte["x_werte"]:
        basis_x_min = min(punkte["x_werte"])
        basis_x_max = max(punkte["x_werte"])
    else:
        basis_x_min, basis_x_max = -5, 5

    # Y-Basisbereich aus wichtigen Punkten
    if punkte["y_werte"]:
        basis_y_min = min(punkte["y_werte"])
        basis_y_max = max(punkte["y_werte"])
    else:
        basis_y_min, basis_y_max = -5, 5

    # === X-ACHSENBERECHNUNG MIT MODE-LOGIK ===
    if x_min is not None and x_max is not None:
        # MODE 1: Vollständig manuell - exakte Einhaltung, kein Puffer
        final_x_min, final_x_max = x_min, x_max
        x_step = None  # Keine optimierte Schrittweite bei manuellen Grenzen

    elif x_min is not None:
        # MODE 2: Nur x_min manuell - Minimum fest, Maximum automatisch mit Puffer
        final_x_min = x_min
        final_x_max = basis_x_max  # Automatisch maximum
        x_step = _berechne_intervalle(final_x_min, final_x_max)

        # Nur oberen Puffer anwenden (da Minimum fest)
        oberer_puffer = _berechne_intelligenter_puffer(final_x_min, final_x_max, x_step)
        final_x_max += oberer_puffer

    elif x_max is not None:
        # MODE 3: Nur x_max manuell - Maximum fest, Minimum automatisch mit Puffer
        final_x_max = x_max
        final_x_min = basis_x_min  # Automatisch minimum
        x_step = _berechne_intervalle(final_x_min, final_x_max)

        # Nur unteren Puffer anwenden (da Maximum fest)
        unterer_puffer = _berechne_intelligenter_puffer(
            final_x_min, final_x_max, x_step
        )
        final_x_min -= unterer_puffer

    else:
        # MODE 4: Vollständig automatisch - beidseitiger Puffer
        final_x_min, final_x_max = basis_x_min, basis_x_max
        x_step = _berechne_intervalle(final_x_min, final_x_max)

        # Beidseitiger Puffer mit wichtiger Punkte Optimierung
        final_x_min, final_x_max, x_step = _optimiere_achse(
            final_x_min, final_x_max, wichtige_punkte=punkte["x_werte"]
        )

        # Zusätzlichen prozentualen Puffer hinzufügen (auch bei optimierten Bereichen)
        int_puffer = _berechne_intelligenter_puffer(final_x_min, final_x_max, x_step)
        final_x_min -= int_puffer
        final_x_max += int_puffer
        # Schrittweite neu berechnen
        x_step = _berechne_intervalle(final_x_min, final_x_max)

    # === Y-ACHSENBERECHNUNG (ANALOG ZU X) ===
    if y_min is not None and y_max is not None:
        # MODE 1: Vollständig manuell - exakte Einhaltung, kein Puffer
        final_y_min, final_y_max = y_min, y_max
        y_step = None  # Keine optimierte Schrittweite bei manuellen Grenzen

    elif y_min is not None:
        # MODE 2: Nur y_min manuell - Minimum fest, Maximum automatisch mit Puffer
        final_y_min = y_min
        final_y_max = basis_y_max  # Automatisch maximum
        y_step = _berechne_intervalle(final_y_min, final_y_max)

        # Nur oberen Puffer anwenden (da Minimum fest)
        oberer_puffer = _berechne_intelligenter_puffer(final_y_min, final_y_max, y_step)
        final_y_max += oberer_puffer

    elif y_max is not None:
        # MODE 3: Nur y_max manuell - Maximum fest, Minimum automatisch mit Puffer
        final_y_max = y_max
        final_y_min = basis_y_min  # Automatisch minimum
        y_step = _berechne_intervalle(final_y_min, final_y_max)

        # Nur unteren Puffer anwenden (da Maximum fest)
        unterer_puffer = _berechne_intelligenter_puffer(
            final_y_min, final_y_max, y_step
        )
        final_y_min -= unterer_puffer

    else:
        # MODE 4: Vollständig automatisch - beidseitiger Puffer
        final_y_min, final_y_max = basis_y_min, basis_y_max
        y_step = _berechne_intervalle(final_y_min, final_y_max)

        # Beidseitiger Puffer mit wichtiger Punkte Optimierung
        final_y_min, final_y_max, y_step = _optimiere_achse(
            final_y_min, final_y_max, wichtige_punkte=punkte["y_werte"]
        )

        # Zusätzlichen prozentualen Puffer hinzufügen (auch bei optimierten Bereichen)
        int_puffer = _berechne_intelligenter_puffer(final_y_min, final_y_max, y_step)
        final_y_min -= int_puffer
        final_y_max += int_puffer
        # Schrittweite neu berechnen
        y_step = _berechne_intervalle(final_y_min, final_y_max)

    # === MINDESTBEREICHE SICHERSTELLEN ===
    # Verhindere zu kleine Bereiche
    if final_x_max - final_x_min < 1:
        center = (final_x_min + final_x_max) / 2
        final_x_min = center - 0.5
        final_x_max = center + 0.5
        x_step = 0.1

    if final_y_max - final_y_min < 1:
        center = (final_y_min + final_y_max) / 2
        final_y_min = center - 0.5
        final_y_max = center + 0.5
        y_step = 0.1

    return final_x_min, final_x_max, final_y_min, final_y_max, x_step, y_step


# ====================
# Haupt-Visualisierungsfunktionen
# ====================


def Graph(*funktionen, x_min=None, x_max=None, y_min=None, y_max=None, **kwargs):
    """Erzeugt einen Graphen für eine oder mehrere Funktionen mit vereinfachter Bereichskontrolle

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

        >>> # Manuel Y-Bereich: Strikte Einhaltung von y_max=10
        >>> fig = Graph(f, y_max=10)

        >>> # Halb-manuell: Nur x_min fest, y automatisch
        >>> fig = Graph(f, x_min=0)

        >>> # Vollständig manuell
        >>> fig = Graph(f, x_min=-5, x_max=5, y_min=-10, y_max=10)
    """
    if not funktionen:
        raise ValueError("Mindestens eine Funktion muss angegeben werden")

    # Validiere alle Funktionen
    for f in funktionen:
        if not isinstance(f, Funktion):
            raise TypeError("Alle Argumente müssen Funktionen sein")
        # Prüfe ob die Funktion parametrisiert ist
        if f.parameter:
            parameter_namen = [str(p.symbol) for p in f.parameter]
            parameter_beispiele = [f"{p.symbol}=1" for p in f.parameter]
            raise ValueError(
                f"Die Funktion '{f.term()}' enthält Parameter ({', '.join(parameter_namen)}). "
                f"Verwende zuerst setze_parameter() um Werte zuzuweisen, z.B.: "
                f"f.setze_parameter({', '.join(parameter_beispiele)})"
            )

    # Wenn nur eine Funktion übergeben wurde, wende die neue vereinfachte Logik an
    if len(funktionen) == 1:
        funktion = funktionen[0]

        # Berechne finale Grenzen mit der neuen vereinfachten Logik
        final_x_min, final_x_max, final_y_min, final_y_max, x_step, y_step = (
            _berechne_finale_grenzen(funktion, x_min, x_max, y_min, y_max)
        )

        # Prüfe auf abgeschnittene Punkte und gib Warnungen aus
        punkte = _sammle_interessante_punkte(funktion)
        sichtbare, abgeschnittene = _filtere_sichtbare_punkte(
            punkte, final_x_min, final_x_max, final_y_min, final_y_max
        )

        if abgeschnittene:
            # Formatiere Warnungen für bessere Lesbarkeit
            warnungen = []
            for art, x_val, y_val in abgeschnittene:
                if y_val is not None:
                    warnungen.append(f"{art} bei ({x_val:.2f}|{y_val:.2f})")
                else:
                    warnungen.append(f"{art} bei x={x_val:.2f}")

            print(f"⚠️  Hinweis: Abgeschnittene Punkte: {'; '.join(warnungen)}")

        return _erstelle_plotly_figur_mit_intelligenten_achsen(
            funktion,
            final_x_min,
            final_x_max,
            final_y_min,
            final_y_max,
            x_step,
            y_step,
            **kwargs,
        )

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

            x_min_auto, x_max_auto = _berechne_optimalen_bereich(kombinierte_punkte)

            if x_min is None:
                x_min = x_min_auto
            if x_max is None:
                x_max = x_max_auto

        # Berechne y-Bereich basierend auf allen Funktionen mit intelligenter Logik
        if y_min is None or y_max is None:
            y_min_auto, y_max_auto = _berechne_y_bereich_mehrfach(
                funktionen, x_min, x_max
            )

            if y_min is None:
                y_min = y_min_auto
            if y_max is None:
                y_max = y_max_auto

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
                    if _ist_endlich(y):
                        y_werte.append(_formatiere_float(y))
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
