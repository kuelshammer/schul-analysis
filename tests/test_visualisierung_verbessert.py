"""
Tests für die verbesserte Graph-Funktion mit manueller Bereichskontrolle
"""

import pytest
import numpy as np
from schul_analysis.ganzrationale import GanzrationaleFunktion
from schul_analysis.visualisierung import (
    _berechne_intervalle,
    _optimiere_achse,
    _sammle_interessante_punkte,
    _filtere_sichtbare_punkte,
    _berechne_finale_grenzen,
    Graph,
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
        assert -2.001 <= punkte["x_werte"][0] <= -1.999  # x≈-2
        assert 1.999 <= punkte["x_werte"][1] <= 2.001  # x≈2

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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
