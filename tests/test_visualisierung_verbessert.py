"""
Tests für die verbesserte Graph-Funktion mit manueller Bereichskontrolle
"""

import pytest
import numpy as np
from schul_analysis.ganzrationale import GanzrationaleFunktion
from schul_analysis.exponential import ExponentialFunktion
from schul_analysis.visualisierung import (
    _berechne_intervalle,
    _optimiere_achse,
    _sammle_interessante_punkte,
    _filtere_sichtbare_punkte,
    _berechne_finale_grenzen,
    Graph,
    _berechne_kombinierten_intelligenten_bereich,
)


class TestIntervallberechnung:
    """Testet die Funktionen für intelligente Achsenintervalle"""

    def test_berechne_intervalle_einfach(self):
        """Testet einfache Intervallberechnung"""
        step = _berechne_intervalle(0, 10, max_ticks=8)
        assert step in [1, 2, 5]  # Sollte eine runde Zahl sein

    def test_berechne_intervalle_kleiner_bereich(self):
        """Testet Intervallberechnung für kleine Bereiche"""
        step = _berechne_intervalle(0.5, 2.5, max_ticks=8)
        assert step <= 0.5  # Sollte kleiner als 0.5 sein

    def test_berechne_intervalle_großer_bereich(self):
        """Testet Intervallberechnung für große Bereiche"""
        step = _berechne_intervalle(-100, 200, max_ticks=8)
        assert step >= 25  # Sollte eine große runde Zahl sein

    def test_optimiere_achse_normale_funktion(self):
        """Testet Achsenoptimierung für normale Funktion"""
        x_min, x_max, step = _optimiere_achse(1.2, 8.7, max_ticks=8)
        assert x_min <= 1.2
        assert x_max >= 8.7
        assert step > 0
        # Schrittweite sollte eine runde Zahl sein
        assert step in [1, 2, 5, 10] or step % 1 == 0

    def test_optimiere_achse_gleiche_werte(self):
        """Testet Achsenoptimierung bei gleichen Werten"""
        x_min, x_max, step = _optimiere_achse(5, 5, max_ticks=8)
        assert x_min == 4  # Sollte um den Punkt zentriert werden
        assert x_max == 6
        assert step == 1


class TestPunktesammlung:
    """Testet die Sammlung von interessanten Punkten"""

    def test_sammle_punkte_parabel(self):
        """Testet Punktesammlung für eine einfache Parabel"""
        f = GanzrationaleFunktion("x^2 - 4")
        punkte = _sammle_interessante_punkte(f)

        # Sollte Nullstellen bei x=2 und x=-2 haben
        assert len(punkte["x_werte"]) >= 2
        # Sortiere die x-Werte für konsistente Tests
        sortierte_x = sorted(punkte["x_werte"])
        # Finde die Nullstellen in der sortierten Liste
        nullstellen = [x for x in sortierte_x if abs(x) > 1.5]  # x≈-2 und x≈2
        assert len(nullstellen) >= 2
        assert -2.001 <= nullstellen[0] <= -1.999  # x≈-2
        assert 1.999 <= nullstellen[1] <= 2.001  # x≈2

        # Sollte Extremstelle bei x=0 haben
        assert any(abs(x - 0) < 0.001 for x in punkte["x_werte"])

        # Sollte Y-Werte haben
        assert len(punkte["y_werte"]) >= 3
        assert any(abs(y - 0) < 0.001 for y in punkte["y_werte"])  # Nullstellen bei y=0

    def test_sammle_punkte_lineare_funktion(self):
        """Testet Punktesammlung für eine lineare Funktion"""
        f = GanzrationaleFunktion("2x + 1")
        punkte = _sammle_interessante_punkte(f)

        # Sollte nur eine Nullstelle bei x=-0.5 haben
        assert len(punkte["x_werte"]) >= 1
        assert -0.501 <= punkte["x_werte"][0] <= -0.499  # x≈-0.5

    def test_sammle_punkte_konstante_funktion(self):
        """Testet Punktesammlung für eine konstante Funktion"""
        f = GanzrationaleFunktion("5")
        punkte = _sammle_interessante_punkte(f)

        # Sollte keine interessanten Punkte haben
        assert len(punkte["x_werte"]) == 0
        assert len(punkte["y_werte"]) == 0


class TestPunktefilterung:
    """Testet das Filtern von sichtbaren Punkten"""

    def test_filtere_punkte_alle_sichtbar(self):
        """Testet Filterung wenn alle Punkte sichtbar sind"""
        f = GanzrationaleFunktion("x^2 - 4")
        punkte = _sammle_interessante_punkte(f)

        sichtbare, abgeschnittene = _filtere_sichtbare_punkte(
            punkte, x_min=-5, x_max=5, y_min=-5, y_max=5
        )

        # Alle Punkte sollten sichtbar sein
        assert len(sichtbare) >= 3  # Mindestens 2 Nullstellen + 1 Extremstelle
        assert len(abgeschnittene) == 0

    def test_filtere_punkte_teilweise_sichtbar(self):
        """Testet Filterung wenn einige Punkte abgeschnitten sind"""
        f = GanzrationaleFunktion("x^2 - 4")
        punkte = _sammle_interessante_punkte(f)

        # Setze Y-Bereich so dass nur positive Y-Werte sichtbar sind
        sichtbare, abgeschnittene = _filtere_sichtbare_punkte(
            punkte, x_min=-5, x_max=5, y_min=0, y_max=10
        )

        # Extremstelle bei (0|-4) sollte abgeschnitten sein
        assert len(abgeschnittene) >= 1
        assert any(
            art == "Minimum" and abs(y_val - (-4)) < 0.001
            for art, x_val, y_val in abgeschnittene
        )

        # Nullstellen sollten sichtbar sein
        assert len(sichtbare) >= 2
        assert all(art == "Nullstelle" for art, x_val, y_val in sichtbare)


class TestFinaleGrenzen:
    """Testet die Berechnung der finalen Grenzen"""

    def test_finale_grenzen_vollstaendig_automatic(self):
        """Testet vollständig automatische Grenzberechnung"""
        f = GanzrationaleFunktion("x^2 - 4")
        x_min, x_max, y_min, y_max, x_step, y_step = _berechne_finale_grenzen(f)

        # Sollte alle wichtigen Punkte umfassen
        assert x_min <= -2  # Linke Nullstelle
        assert x_max >= 2  # Rechte Nullstelle
        assert y_min <= -4  # Extremstelle
        assert y_max >= 0  # Nullstellen

        # Schrittweiten sollten optimiert sein
        assert x_step is not None
        assert y_step is not None
        assert x_step > 0
        assert y_step > 0

    def test_finale_grenzen_manuelles_y(self):
        """Testet manuelle Y-Grenzen"""
        f = GanzrationaleFunktion("x^2 - 4")
        x_min, x_max, y_min, y_max, x_step, y_step = _berechne_finale_grenzen(
            f, y_min=0, y_max=5
        )

        # Y-Grenzen sollten exakt eingehalten werden
        assert y_min == 0
        assert y_max == 5

        # X sollte automatisch berechnet werden
        assert x_min <= -2
        assert x_max >= 2

        # Y-Schrittweite sollte None sein (manueller Bereich)
        assert y_step is None

    def test_finale_grenzen_halb_manuell(self):
        """Testet halb-manuelle Grenzen (nur eine Grenze festgelegt)"""
        f = GanzrationaleFunktion("x^2 - 4")
        x_min, x_max, y_min, y_max, x_step, y_step = _berechne_finale_grenzen(
            f, x_min=0
        )

        # X-Minimum sollte exakt eingehalten werden
        assert x_min == 0

        # X-Maximum sollte automatisch berechnet werden
        assert x_max >= 2

        # Beide Achsen sollten optimierte Schrittweiten haben
        assert x_step is not None
        assert y_step is not None

    def test_finale_grenzen_strikt_manuell(self):
        """Testet strikte manuelle Grenzen"""
        f = GanzrationaleFunktion("x^2 - 4")
        x_min, x_max, y_min, y_max, x_step, y_step = _berechne_finale_grenzen(
            f, x_min=1, x_max=3, y_min=-1, y_max=1
        )

        # Alle Grenzen sollten exakt eingehalten werden
        assert x_min == 1
        assert x_max == 3
        assert y_min == -1
        assert y_max == 1

        # Keine optimierten Schrittweiten bei manuellen Grenzen
        assert x_step is None
        assert y_step is None


class TestGraphFunktion:
    """Testet die Haupt-Graph-Funktion"""

    def test_graph_automatic(self, capsys):
        """Testet Graph-Funktion mit automatischen Grenzen"""
        f = GanzrationaleFunktion("x^2 - 4")
        fig = Graph(f)

        # Sollte eine gültige Plotly-Figur zurückgeben
        assert hasattr(fig, "data")
        assert hasattr(fig, "layout")

        # Keine Warnungen erwartet (alle Punkte sichtbar)
        captured = capsys.readouterr()
        assert "Abgeschnittene Punkte" not in captured.out

    def test_graph_manuelle_grenzen(self, capsys):
        """Testet Graph-Funktion mit manuellen Grenzen"""
        f = GanzrationaleFunktion("x^2 - 4")
        fig = Graph(f, y_max=-1)  # Schneidet Extremstelle ab bei y=-1

        # Sollte eine gültige Plotly-Figur zurückgeben
        assert hasattr(fig, "data")
        assert hasattr(fig, "layout")

        # Sollte Warnung über abgeschnittene Punkte anzeigen
        captured = capsys.readouterr()
        assert "Hinweis: Abgeschnittene Punkte" in captured.out
        # Entweder Minimum oder Nullstellen können abgeschnitten sein, je nach Bereichskalkulation
        assert "Minimum" in captured.out or "Nullstelle" in captured.out

    def test_graph_fehlerhafte_funktion(self):
        """Testet Graph-Funktion mit ungültigen Parametern"""
        with pytest.raises(
            ValueError, match="Mindestens eine Funktion muss angegeben werden"
        ):
            Graph()

        with pytest.raises(TypeError, match="Alle Argumente müssen Funktionen sein"):
            Graph("keine Funktion")

    def test_graph_parametrisierte_funktion(self):
        """Testet Graph-Funktion mit parametrisierter Funktion"""
        f = GanzrationaleFunktion("a*x^2 + b*x + c")

        with pytest.raises(ValueError, match="enthält Parameter"):
            Graph(f)


# Integrationstests für verschiedene Szenarien
class TestIntegrationSzenarien:
    """Testet verschiedene reale Anwendungsszenarien"""

    def test_szenario_parabel_mit_optimierung(self):
        """Testet eine Parabel mit automatischer Optimierung"""
        f = GanzrationaleFunktion("x^2 - 6x + 8")  # Nullstellen bei x=2, x=4
        fig = Graph(f)

        # X-Bereich sollte Nullstellen umfassen
        x_range = fig.layout.xaxis.range
        assert x_range[0] <= 2
        assert x_range[1] >= 4

        # Y-Bereich sollte Extremstelle umfassen
        y_range = fig.layout.yaxis.range
        assert y_range[0] <= -1  # Minimum bei x=3, y=-1
        assert y_range[1] >= 0  # Nullstellen bei y=0

        # Sollte optimierte Schrittweiten haben
        assert "dtick" in fig.layout.xaxis
        assert "dtick" in fig.layout.yaxis

    def test_szenario_hohe_extremwerte(self):
        """Testet Funktion mit hohen Extremwerten"""
        f = GanzrationaleFunktion(
            "x^3 - 12x^2 + 36x - 25"
        )  # Extremwerte bei hohen y-Werten
        fig = Graph(f, y_max=10)  # Beschränke y auf 10

        # Y-Bereich sollte genau eingehalten werden
        y_range = fig.layout.yaxis.range
        assert y_range[1] == 10

        # Sollte Warnung über abgeschnittene Punkte anzeigen
        # (dies wird im Haupttest geprüft)

    def test_szenario_linke_begrenzung(self):
        """Testet halb-manuelle Modus mit nur linker Begrenzung"""
        f = GanzrationaleFunktion("x^2 - 4x + 3")  # Nullstellen bei x=1, x=3
        fig = Graph(f, x_min=2)  # Nur x_min festgelegt

        # X-Minimum sollte exakt eingehalten werden
        x_range = fig.layout.xaxis.range
        assert x_range[0] == 2

        # X-Maximum sollte automatisch rechte Nullstelle umfassen
        assert x_range[1] >= 3

    def test_szenario_puffer_bei_nullstellen_am_rand(self):
        """Testet dass Nullstellen am Rand ausreichend Puffer erhalten

        Dieser Test stellt sicher dass die automatische Bereichsberechnung
        für Funktionen wie f = (x+3)(x+1)(x-10) einen angemessenen
        Puffer um die äußersten Nullstellen herum einfügt.
        """
        # Testfunktion mit Nullstellen bei x=-3, x=-1, x=10
        f = GanzrationaleFunktion("(x+3)(x+1)(x-10)")
        nullstellen = sorted(f.nullstellen)
        assert nullstellen == [-3, -1, 10]

        # Automatische Bereichsberechnung
        fig = Graph(f)
        x_range = fig.layout.xaxis.range

        # Überprüfe dass die äußersten Nullstellen ausreichend Puffer haben
        linkeste_nullstelle = nullstellen[0]
        rechtste_nullstelle = nullstellen[-1]

        linker_puffer = linkeste_nullstelle - x_range[0]
        rechter_puffer = x_range[1] - rechtste_nullstelle

        # Sollte mindestens 5% + 1 Einheit Puffer auf jeder Seite haben
        # Bei Spanne von 13 Einheiten (-3 bis 10): 5% = 0.65, also mindestens 1.0 Einheit
        erwarteter_min_puffer = max(13 * 0.05, 1.0)
        assert linker_puffer >= erwarteter_min_puffer, (
            f"Linker Puffer zu klein: {linker_puffer} < {erwarteter_min_puffer}"
        )
        assert rechter_puffer >= erwarteter_min_puffer, (
            f"Rechter Puffer zu klein: {rechter_puffer} < {erwarteter_min_puffer}"
        )

        # Sollte etwa 5% Puffer auf jeder Seite haben (Gesamtbereich ca. 14.3 Einheiten)
        gesamtbereich = x_range[1] - x_range[0]
        prozentualer_puffer_links = linker_puffer / gesamtbereich
        prozentualer_puffer_rechts = rechter_puffer / gesamtbereich

        assert prozentualer_puffer_links >= 0.04, (
            f"Linker prozentualer Puffer zu klein: {prozentualer_puffer_links:.3f} < 0.04"
        )
        assert prozentualer_puffer_rechts >= 0.04, (
            f"Rechter prozentualer Puffer zu klein: {prozentualer_puffer_rechts:.3f} < 0.04"
        )
        assert prozentualer_puffer_links <= 0.15, (
            f"Linker prozentualer Puffer zu groß: {prozentualer_puffer_links:.3f} > 0.15"
        )
        assert prozentualer_puffer_rechts <= 0.15, (
            f"Rechter prozentualer Puffer zu groß: {prozentualer_puffer_rechts:.3f} > 0.15"
        )

    def test_szenario_puffer_fuer_verschiedene_funktionen(self):
        """Testet Pufferlogik für verschiedene Funktionstypen mit prozentualer Berechnung"""
        test_cases = [
            ("(x+1)(x-5)", [-1, 5]),  # Einfache quadratische Funktion, Spanne=6
            ("(x+2)(x-1)(x-8)", [-2, 1, 8]),  # Kubische Funktion, Spanne=10
            ("(x+4)(x+2)(x-3)(x-7)", [-4, -2, 3, 7]),  # Quartische Funktion, Spanne=11
        ]

        for func_str, expected_zeros in test_cases:
            f = GanzrationaleFunktion(func_str)
            fig = Graph(f)
            x_range = fig.layout.xaxis.range

            linkeste_nullstelle = min(expected_zeros)
            rechtste_nullstelle = max(expected_zeros)

            linker_puffer = linkeste_nullstelle - x_range[0]
            rechter_puffer = x_range[1] - rechtste_nullstelle

            # Berechne erwarteten prozentualen Puffer
            spanne = rechtste_nullstelle - linkeste_nullstelle
            erwarteter_min_puffer = max(spanne * 0.05, 1.0)  # 5% + min 1 Einheit

            # Teste Mindestpuffer
            assert linker_puffer >= erwarteter_min_puffer, (
                f"{func_str}: Linker Puffer {linker_puffer} < Minimum {erwarteter_min_puffer}"
            )
            assert rechter_puffer >= erwarteter_min_puffer, (
                f"{func_str}: Rechter Puffer {rechter_puffer} < Minimum {erwarteter_min_puffer}"
            )

            # Teste dass Puffer nicht zu groß ist (sollte vernünftig sein)
            gesamtbereich = x_range[1] - x_range[0]
            max_akzeptabler_puffer = (
                gesamtbereich * 0.25
            )  # Maximal 25% vom Gesamtbereich

            assert linker_puffer <= max_akzeptabler_puffer, (
                f"{func_str}: Linker Puffer {linker_puffer} > Maximum {max_akzeptabler_puffer}"
            )
            assert rechter_puffer <= max_akzeptabler_puffer, (
                f"{func_str}: Rechter Puffer {rechter_puffer} > Maximum {max_akzeptabler_puffer}"
            )

    def test_szenario_intelligenter_puffer_kleine_spanne(self):
        """Testet den intelligenten Puffer bei kleinen Spannen (sollte Mindestpuffer verwenden)"""
        # Funktion mit kleiner Spanne (2 Einheiten)
        f = GanzrationaleFunktion("(x-1)(x-3)")  # Nullstellen bei x=1, x=3, Spanne=2
        fig = Graph(f)
        x_range = fig.layout.xaxis.range

        linker_puffer = 1 - x_range[0]  # Puffer um linke Nullstelle
        rechter_puffer = x_range[1] - 3  # Puffer um rechte Nullstelle

        # Bei kleiner Spanne sollte der Mindestpuffer (1.0) dominant sein
        assert linker_puffer >= 1.0, (
            f"Linker Puffer sollte Mindestpuffer erreichen: {linker_puffer} < 1.0"
        )
        assert rechter_puffer >= 1.0, (
            f"Rechter Puffer sollte Mindestpuffer erreichen: {rechter_puffer} < 1.0"
        )

    def test_szenario_intelligenter_puffer_grosse_spanne(self):
        """Testet den intelligenten Puffer bei großen Spannen (sollte prozentualen Puffer verwenden)"""
        # Funktion mit großer Spanne (100 Einheiten)
        f = GanzrationaleFunktion(
            "(x+50)(x-50)"
        )  # Nullstellen bei x=-50, x=50, Spanne=100
        fig = Graph(f)
        x_range = fig.layout.xaxis.range

        linker_puffer = -50 - x_range[0]  # Puffer um linke Nullstelle
        rechter_puffer = x_range[1] - 50  # Puffer um rechte Nullstelle

        # Bei großer Spanne sollte der prozentuale Puffer (5% = 5 Einheiten) dominant sein
        erwarteter_prozentualer_puffer = 100 * 0.05  # 5 Einheiten

        assert linker_puffer >= erwarteter_prozentualer_puffer, (
            f"Linker Puffer sollte prozentualen Puffer erreichen: {linker_puffer} < {erwarteter_prozentualer_puffer}"
        )
        assert rechter_puffer >= erwarteter_prozentualer_puffer, (
            f"Rechter Puffer sollte prozentualen Puffer erreichen: {rechter_puffer} < {erwarteter_prozentualer_puffer}"
        )

    def test_graph_mehrfach_kombinierter_bereich(self):
        """Testet Graph(f, g) mit kombiniertem intelligentem Bereich"""
        # Beispiel vom Benutzer: f = (x+4)(x-1), g = (x+3)(x-3)
        f = GanzrationaleFunktion("(x+4)(x-1)")  # Nullstellen bei x=-4, x=1
        g = GanzrationaleFunktion("(x+3)(x-3)")  # Nullstellen bei x=-3, x=3

        fig = Graph(f, g)
        x_range = fig.layout.xaxis.range

        # Erwarteter kombinierte Bereich: -4 bis 3 (90% Kern)
        # Mit 5% Puffer auf jeder Seite: ca. -4.35 bis 3.35
        erwarteter_min = -4.35
        erwarteter_max = 3.35

        assert x_range[0] <= erwarteter_min, (
            f"Linker Bereich sollte mindestens {erwarteter_min} sein: {x_range[0]}"
        )
        assert x_range[1] >= erwarteter_max, (
            f"Rechter Bereich sollte mindestens {erwarteter_max} sein: {x_range[1]}"
        )

        # Prüfe, dass alle Nullstellen sichtbar sind
        assert x_range[0] <= -4, "Linke Nullstelle von f sollte sichtbar sein"
        assert x_range[0] <= -3, "Linke Nullstelle von g sollte sichtbar sein"
        assert x_range[1] >= 1, "Rechte Nullstelle von f sollte sichtbar sein"
        assert x_range[1] >= 3, "Rechte Nullstelle von g sollte sichtbar sein"

        # Prüfe, dass beide Funktionen angezeigt werden
        assert len(fig.data) == 2, "Es sollten zwei Funktionen angezeigt werden"

    def test_graph_mehrfach_mit_manuellen_grenzen(self):
        """Testet Graph(f, g) mit teilweisen manuellen Grenzen"""
        f = GanzrationaleFunktion("(x+4)(x-1)")
        g = GanzrationaleFunktion("(x+3)(x-3)")

        # Nur x_max manuell gesetzt
        fig = Graph(f, g, x_max=5)
        x_range = fig.layout.xaxis.range

        # Rechter Grenze sollte exakt 5 sein
        assert abs(x_range[1] - 5) < 0.001, (
            f"Rechte Grenze sollte exakt 5 sein: {x_range[1]}"
        )

        # Linke Grenze sollte automatisch berechnet werden (mit Puffer)
        assert x_range[0] <= -4, "Linke Nullstellen sollten sichtbar sein"

    def test_graph_mehrfach_vollstaendig_manuell(self):
        """Testet Graph(f, g) mit vollständig manuellen Grenzen"""
        f = GanzrationaleFunktion("(x+4)(x-1)")
        g = GanzrationaleFunktion("(x+3)(x-3)")

        # Vollständig manuelle Grenzen
        fig = Graph(f, g, x_min=-10, x_max=10, y_min=-20, y_max=20)
        x_range = fig.layout.xaxis.range
        y_range = fig.layout.yaxis.range

        # Grenzen sollten exakt eingehalten werden
        assert abs(x_range[0] - (-10)) < 0.001, (
            f"Linke Grenze sollte -10 sein: {x_range[0]}"
        )
        assert abs(x_range[1] - 10) < 0.001, (
            f"Rechte Grenze sollte 10 sein: {x_range[1]}"
        )
        assert abs(y_range[0] - (-20)) < 0.001, (
            f"Untere y-Grenze sollte -20 sein: {y_range[0]}"
        )
        assert abs(y_range[1] - 20) < 0.001, (
            f"Obere y-Grenze sollte 20 sein: {y_range[1]}"
        )

    def test_graph_mehrfach_drei_funktionen(self):
        """Testet Graph(f, g, h) mit drei Funktionen"""
        f = GanzrationaleFunktion("(x+4)(x-1)")  # Bereich: -4 bis 1
        g = GanzrationaleFunktion("(x+3)(x-3)")  # Bereich: -3 bis 3
        h = GanzrationaleFunktion("(x+5)(x-2)")  # Bereich: -5 bis 2

        fig = Graph(f, g, h)
        x_range = fig.layout.xaxis.range

        # Kombinierter Bereich sollte -5 bis 3 umfassen (größter Bereich)
        assert x_range[0] <= -5, "Linke Nullstelle von h sollte sichtbar sein"
        assert x_range[1] >= 3, "Rechte Nullstelle von g sollte sichtbar sein"

        # Alle drei Funktionen sollten angezeigt werden
        assert len(fig.data) == 3, "Es sollten drei Funktionen angezeigt werden"

        # Prüfe, dass verschiedene Farben verwendet werden
        farben = [trace.line.color for trace in fig.data]
        assert len(set(farben)) == 3, "Jede Funktion sollte eine andere Farbe haben"

    def test_graph_mehrfach_exponentielle_funktionen(self):
        """Testet Graph(f, g) mit exponentiellen Funktionen"""
        f = ExponentialFunktion("2^x")  # Wachstum für x > 0
        g = ExponentialFunktion("0.5^x")  # Decay für x > 0

        fig = Graph(f, g, x_min=-2, x_max=4)
        x_range = fig.layout.xaxis.range
        y_range = fig.layout.yaxis.range

        # X-Bereich sollte manuell eingehalten werden
        assert abs(x_range[0] - (-2)) < 0.001, (
            f"Linke Grenze sollte -2 sein: {x_range[0]}"
        )
        assert abs(x_range[1] - 4) < 0.001, f"Rechte Grenze sollte 4 sein: {x_range[1]}"

        # Y-Bereich sollte automatisch berechnet werden
        assert y_range[0] > 0, "Y-Bereich sollte positiv sein"
        assert y_range[1] > 1, "Y-Bereich sollte Werte > 1 enthalten"

    def test_berechne_kombinierten_intelligenten_bereich(self):
        """Testet die Hilfsfunktion _berechne_kombinierten_intelligenten_bereich direkt"""
        f = GanzrationaleFunktion("(x+4)(x-1)")  # Bereich: -4 bis 1
        g = GanzrationaleFunktion("(x+3)(x-3)")  # Bereich: -3 bis 3

        x_min, x_max, x_step = _berechne_kombinierten_intelligenten_bereich([f, g])

        # Kombinierter Bereich sollte -4 bis 3 umfassen
        assert x_min <= -4, f"Min sollte <= -4 sein: {x_min}"
        assert x_max >= 3, f"Max sollte >= 3 sein: {x_max}"

        # Puffer sollte angewendet werden
        gesamt_spanne = x_max - x_min
        kern_spanne = 3 - (-4)  # 7 Einheiten
        assert gesamt_spanne > kern_spanne, "Puffer sollte angewendet werden"

        # Schrittweite sollte berechnet werden
        assert x_step is not None, "Schrittweite sollte berechnet werden"
        assert x_step > 0, "Schrittweite sollte positiv sein"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
