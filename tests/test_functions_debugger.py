"""
Tests für den FunktionsDebugger und die Schritt-für-Schritt Berechnungsanzeige.

Dieses Modul testet die umfassenden Debugging-Funktionen für mathematische Berechnungen.
"""

import time
import pytest
import sympy as sp
from sympy import Symbol, simplify, diff, solve

from schul_mathematik.analysis.debugger import (
    FunktionsDebugger,
    DebugSession,
    BerechnungsSchritt,
    BerechnungsSchrittTyp,
    DetailGrad,
    BerechnungsStrategie,
    VereinfachungsStrategie,
    AbleitungsStrategie,
    debugger,
    DebuggeAbleitung,
    DebuggeNullstellen,
    DebuggeVereinfachung,
    ZeigeDebugSchritte,
)


class TestBerechnungsSchrittTyp:
    """Teste die BerechnungsSchrittTyp-Enum."""

    def test_alle_typen_vorhanden(self):
        """Teste, dass alle erwarteten Schritttypen vorhanden sind."""
        expected_typen = [
            "initialisierung",
            "transformation",
            "vereinfachung",
            "ableitung",
            "integration",
            "nullstellensuche",
            "extremwertsuche",
            "wendepunktsuche",
            "auswertung",
            "validierung",
            "ergebnis",
            "hinweis",
            "fehler",
        ]

        actual_typen = [typ.value for typ in BerechnungsSchrittTyp]
        assert set(actual_typen) == set(expected_typen)


class TestDetailGrad:
    """Teste die DetailGrad-Enum."""

    def test_alle_detailgrade_vorhanden(self):
        """Teste, dass alle erwarteten Detailgrade vorhanden sind."""
        expected_grade = ["minimal", "normal", "ausführlich", "pädagogisch"]

        actual_grade = [grad.value for grad in DetailGrad]
        assert set(actual_grade) == set(expected_grade)


class TestBerechnungsSchritt:
    """Teste die BerechnungsSchritt-Klasse."""

    def test_schritt_erstellung(self):
        """Teste die Erstellung eines Berechnungsschritts."""
        x = Symbol("x")
        formel_vorher = x**2 + 2 * x + 1
        formel_nachher = (x + 1) ** 2

        schritt = BerechnungsSchritt(
            typ=BerechnungsSchrittTyp.VEREINFACHUNG,
            beschreibung="Binomische Formel anwenden",
            formel_vorher=formel_vorher,
            formel_nachher=formel_nachher,
            ergebnis=formel_nachher,
            erläuterung="x² + 2x + 1 = (x + 1)²",
            lernhinweis="Erkenne binomische Formeln!",
        )

        assert schritt.typ == BerechnungsSchrittTyp.VEREINFACHUNG
        assert schritt.beschreibung == "Binomische Formel anwenden"
        assert schritt.formel_vorher == formel_vorher
        assert schritt.formel_nachher == formel_nachher
        assert schritt.ergebnis == formel_nachher
        assert schritt.erläuterung == "x² + 2x + 1 = (x + 1)²"
        assert schritt.lernhinweis == "Erkenne binomische Formeln!"
        assert isinstance(schritt.zeitstempel, float)
        assert schritt.schritt_nummer == 0  # Wird erst in Session gesetzt

    def test_latex_formatierung(self):
        """Teste die LaTeX-Formatierung von Formeln."""
        x = Symbol("x")
        formel = x**2 + 2 * x + 1

        schritt = BerechnungsSchritt(
            typ=BerechnungsSchrittTyp.VEREINFACHUNG,
            beschreibung="Test",
            formel_vorher=formel,
            formel_nachher=simplify(formel),
        )

        assert "x^{2}" in schritt.latex_vorher
        assert schritt.latex_nachher is not None

    def test_to_dict(self):
        """Teste die Serialisierung eines Schritts."""
        x = Symbol("x")
        schritt = BerechnungsSchritt(
            typ=BerechnungsSchrittTyp.VEREINFACHUNG,
            beschreibung="Test",
            formel_vorher=x**2,
            ergebnis=x**2,
        )

        schritt_dict = schritt.to_dict()

        assert schritt_dict["typ"] == "vereinfachung"
        assert schritt_dict["beschreibung"] == "Test"
        assert schritt_dict["formel_vorher"] == "x**2"
        assert schritt_dict["ergebnis"] == "x**2"
        assert "latex_vorher" in schritt_dict
        assert "zeitstempel" in schritt_dict


class TestDebugSession:
    """Teste die DebugSession-Klasse."""

    def test_session_erstellung(self):
        """Teste die Erstellung einer Debug-Session."""
        x = Symbol("x")
        funktion = x**2 + 2 * x + 1

        session = DebugSession(
            titel="Test-Session", start_funktion=funktion, detailgrad=DetailGrad.NORMAL
        )

        assert session.titel == "Test-Session"
        assert session.start_funktion == funktion
        assert session.detailgrad == DetailGrad.NORMAL
        assert len(session.schritte) == 0
        assert isinstance(session.startzeit, float)
        assert session.endzeit is None

    def test_schritt_hinzufuegen(self):
        """Teste das Hinzufügen von Schritten zur Session."""
        session = DebugSession("Test", Symbol("x"))

        # Erster Schritt
        schritt1 = BerechnungsSchritt(
            typ=BerechnungsSchrittTyp.INITIALISIERUNG, beschreibung="Erster Schritt"
        )
        session.add_schritt(schritt1)

        assert len(session.schritte) == 1
        assert session.schritte[0].schritt_nummer == 1
        assert session.schritte[0] is schritt1

        # Zweiter Schritt
        schritt2 = BerechnungsSchritt(
            typ=BerechnungsSchrittTyp.VEREINFACHUNG, beschreibung="Zweiter Schritt"
        )
        session.add_schritt(schritt2)

        assert len(session.schritte) == 2
        assert session.schritte[1].schritt_nummer == 2

    def test_get_schritte_by_typ(self):
        """Teste das Filtern von Schritten nach Typ."""
        session = DebugSession("Test", Symbol("x"))

        # Verschiedene Schritttypen hinzufügen
        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.INITIALISIERUNG, beschreibung="Init"
            )
        )
        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.VEREINFACHUNG, beschreibung="Vereinfachen"
            )
        )
        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.VEREINFACHUNG,
                beschreibung="Nochmal vereinfachen",
            )
        )

        init_schritte = session.get_schritte_by_typ(
            BerechnungsSchrittTyp.INITIALISIERUNG
        )
        vereinfachungs_schritte = session.get_schritte_by_typ(
            BerechnungsSchrittTyp.VEREINFACHUNG
        )

        assert len(init_schritte) == 1
        assert len(vereinfachungs_schritte) == 2

    def test_get_letzte_ergebnis(self):
        """Teste das Abrufen des letzten Ergebnisses."""
        session = DebugSession("Test", Symbol("x"))

        # Keine Schritte
        assert session.get_letzte_ergebnis() is None

        # Schritt mit Ergebnis
        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.ERGEBNIS, beschreibung="Ergebnis", ergebnis=42
            )
        )

        assert session.get_letzte_ergebnis() == 42

    def test_berechnungsdauer(self):
        """Teste die Berechnung der Session-Dauer."""
        session = DebugSession("Test", Symbol("x"))

        # Vor Endzeit
        dauer = session.berechnungsdauer()
        assert dauer >= 0

        # Mit Endzeit
        session.endzeit = session.startzeit + 1.5
        dauer = session.berechnungsdauer()
        assert dauer == 1.5

    def test_to_dict(self):
        """Teste die Serialisierung einer Session."""
        x = Symbol("x")
        session = DebugSession("Test", x**2)

        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.INITIALISIERUNG, beschreibung="Start"
            )
        )

        session_dict = session.to_dict()

        assert session_dict["titel"] == "Test"
        assert session_dict["start_funktion"] == "x**2"
        assert len(session_dict["schritte"]) == 1
        assert "dauer" in session_dict
        assert "anzahl_schritte" in session_dict


class TestVereinfachungsStrategie:
    """Teste die VereinfachungsStrategie."""

    def setup_method(self):
        """Setup für Testmethoden."""
        self.strategie = VereinfachungsStrategie()

    def test_kann_anwenden_immer(self):
        """Teste, dass die Strategie immer angewendet werden kann."""
        x = Symbol("x")
        assert self.strategie.kann_anwenden(x**2, {}) is True
        assert self.strategie.kann_anwenden(sp.sin(x), {}) is True

    def test_wende_an_einfache_funktion(self):
        """Teste die Anwendung auf eine einfache Funktion."""
        x = Symbol("x")
        funktion = (x + 1) ** 2

        session = DebugSession("Test", funktion, DetailGrad.NORMAL)
        ergebnis = self.strategie.wende_an(funktion, session, {})

        # Sollte expandiert und vereinfacht werden
        assert str(ergebnis) in ["x**2 + 2*x + 1", "x**2 + 2*x + 1"]

    def test_wende_an_mit_detailgrad(self):
        """Teste die Anwendung mit verschiedenen Detailgraden."""
        x = Symbol("x")
        funktion = (x + 1) * (x - 1)

        # Mit hohem Detailgrad
        session = DebugSession("Test", funktion, DetailGrad.PÄDAGOGISCH)
        ergebnis = self.strategie.wende_an(funktion, session, {})

        # Sollte mehrere Schritte haben
        assert len(session.schritte) >= 1


class TestAbleitungsStrategie:
    """Teste die AbleitungsStrategie."""

    def setup_method(self):
        """Setup für Testmethoden."""
        self.strategie = AbleitungsStrategie()

    def test_kann_anwenden_für_ableitung(self):
        """Teste, dass die Strategie für Ableitungen angewendet werden kann."""
        x = Symbol("x")
        kontext_ableitung = {"operation": "ableitung", "ordnung": 1, "variable": x}
        kontext_anders = {"operation": "integration"}

        assert self.strategie.kann_anwenden(x**2, kontext_ableitung) is True
        assert self.strategie.kann_anwenden(x**2, kontext_anders) is False

    def test_wende_an_erste_ableitung(self):
        """Teste die Berechnung der ersten Ableitung."""
        x = Symbol("x")
        funktion = x**3 + 2 * x**2 + x + 1

        session = DebugSession("Test", funktion)
        kontext = {"operation": "ableitung", "ordnung": 1, "variable": x}

        ergebnis = self.strategie.wende_an(funktion, session, kontext)

        # Überprüfe Ergebnis
        expected = diff(funktion, x)
        assert ergebnis == expected

        # Überprüfe, dass Schritte hinzugefügt wurden
        assert len(session.schritte) >= 2  # Initialisierung + Ableitung

    def test_wende_an_höhere_ableitung(self):
        """Teste die Berechnung höherer Ableitungen."""
        x = Symbol("x")
        funktion = x**4

        session = DebugSession("Test", funktion)
        kontext = {"operation": "ableitung", "ordnung": 3, "variable": x}

        ergebnis = self.strategie.wende_an(funktion, session, kontext)

        # Dritte Ableitung von x^4 sollte 24x sein
        expected = 24 * x
        assert ergebnis == expected


class TestFunktionsDebugger:
    """Teste die Haupt-FunktionsDebugger-Klasse."""

    def setup_method(self):
        """Setup für Testmethoden."""
        self.debugger = FunktionsDebugger(DetailGrad.NORMAL)

    def test_initialisierung(self):
        """Teste die Initialisierung des Debuggers."""
        assert self.debugger.detailgrad == DetailGrad.NORMAL
        assert len(self.debugger.strategien) >= 2
        assert self.debugger._aktive_session is None
        assert len(self.debugger._session_history) == 0

    def test_start_session(self):
        """Teste das Starten einer Session."""
        x = Symbol("x")
        funktion = x**2

        session = self.debugger.start_session("Test-Session", funktion)

        assert isinstance(session, DebugSession)
        assert session.titel == "Test-Session"
        assert session.start_funktion == funktion
        assert self.debugger._aktive_session is session
        assert len(self.debugger._session_history) == 1
        assert len(session.schritte) == 1  # Initialisierungsschritt

    def test_start_session_mit_string(self):
        """Teste das Starten einer Session mit String-Eingabe."""
        session = self.debugger.start_session("Test", "x**2 + 2*x + 1")

        assert isinstance(session.start_funktion, sp.Expr)
        assert str(session.start_funktion) == "x**2 + 2*x + 1"

    def test_start_session_ungueltiger_string(self):
        """Teste das Starten einer Session mit ungültigem String."""
        with pytest.raises(ValueError, match="Ungültiger Funktionsausdruck"):
            self.debugger.start_session("Test", "x^^2 + + invalid")

    def test_berechne_ableitung(self):
        """Teste die Ableitungsberechnung."""
        session = self.debugger.berechne_ableitung("x**3 + 2*x**2 + x + 1", ordnung=2)

        assert session.titel == "2. Ableitung"
        assert session.endzeit is not None
        assert len(session.schritte) >= 2

        # Überprüfe das Endergebnis
        ergebnis = session.get_letzte_ergebnis()
        expected = diff(
            diff(
                Symbol("x") ** 3 + 2 * Symbol("x") ** 2 + Symbol("x") + 1, Symbol("x")
            ),
            Symbol("x"),
        )
        assert ergebnis == expected

    def test_berechne_nullstellen(self):
        """Teste die Nullstellenberechnung."""
        session = self.debugger.berechne_nullstellen("x**2 - 4")

        assert session.titel == "Nullstellenberechnung"
        assert session.endzeit is not None

        # Überprüfe die gefundenen Nullstellen
        nullstellen_schritte = session.get_schritte_by_typ(
            BerechnungsSchrittTyp.NULLSTELLENSUCHE
        )
        assert len(nullstellen_schritte) >= 1

        ergebnis = nullstellen_schritte[0].ergebnis
        assert set(ergebnis) == {-2, 2}

    def test_berechne_nullstellen_keine_loesung(self):
        """Teste die Nullstellenberechnung ohne Lösung."""
        session = self.debugger.berechne_nullstellen("x**2 + 1")

        nullstellen_schritte = session.get_schritte_by_typ(
            BerechnungsSchrittTyp.NULLSTELLENSUCHE
        )
        assert len(nullstellen_schritte) >= 1

        ergebnis = nullstellen_schritte[0].ergebnis
        assert ergebnis == []

    def test_vereinfache_funktion(self):
        """Teste die Funktionsvereinfachung."""
        session = self.debugger.vereinfache_funktion("(x + 1)**2")

        assert session.titel == "Funktionsvereinfachung"
        assert session.endzeit is not None

        ergebnis = session.get_letzte_ergebnis()
        assert str(ergebnis) in ["x**2 + 2*x + 1", "x**2 + 2*x + 1"]

    def test_zeige_schritte_text(self):
        """Teste die Textausgabe von Schritten."""
        session = self.debugger.berechne_ableitung("x**2")

        text_output = self.debugger.zeige_schritte(session, format="text")

        assert isinstance(text_output, str)
        assert "1. Ableitung" in text_output
        assert "Schritt" in text_output

    def test_zeige_schritte_latex(self):
        """Teste die LaTeX-Ausgabe von Schritten."""
        session = self.debugger.berechne_ableitung("x**2")

        latex_output = self.debugger.zeige_schritte(session, format="latex")

        assert isinstance(latex_output, str)
        assert "\\section*" in latex_output
        assert "\\begin{enumerate}" in latex_output

    def test_zeige_schritte_dict(self):
        """Teste die Dict-Ausgabe von Schritten."""
        session = self.debugger.berechne_ableitung("x**2")

        dict_output = self.debugger.zeige_schritte(session, format="dict")

        assert isinstance(dict_output, dict)
        assert "titel" in dict_output
        assert "schritte" in dict_output
        assert "anzahl_schritte" in dict_output

    def test_zeige_schritte_keine_session(self):
        """Teste die Schrittanzeige ohne aktive Session."""
        output = self.debugger.zeige_schritte(None, format="text")
        assert "Keine aktive Session gefunden" in output

    def test_get_session_history(self):
        """Teste das Abrufen der Session-History."""
        # Erstelle mehrere Sessions
        self.debugger.berechne_ableitung("x**2")
        self.debugger.berechne_nullstellen("x**2 - 4")

        history = self.debugger.get_session_history()
        assert len(history) == 2
        assert history[0].titel == "1. Ableitung"
        assert history[1].titel == "Nullstellenberechnung"

    def test_clear_history(self):
        """Teste das Löschen der History."""
        self.debugger.berechne_ableitung("x**2")

        assert len(self.debugger._session_history) == 1

        self.debugger.clear_history()

        assert len(self.debugger._session_history) == 0
        assert self.debugger._aktive_session is None

    def test_set_detailgrad(self):
        """Teste das Setzen des Detailgrads."""
        self.debugger.set_detailgrad(DetailGrad.PÄDAGOGISCH)

        assert self.debugger.detailgrad == DetailGrad.PÄDAGOGISCH

        # Mit aktiver Session
        session = self.debugger.berechne_ableitung("x**2")
        assert session.detailgrad == DetailGrad.PÄDAGOGISCH


class TestGlobaleDebuggerInstanz:
    """Teste die globale Debugger-Instanz und API-Funktionen."""

    def test_globale_instanz(self):
        """Teste, dass die globale Instanz existiert."""
        assert debugger is not None
        assert isinstance(debugger, FunktionsDebugger)

    def test_debugge_ableitung(self):
        """Teste die bequeme DebuggeAbleitung-Funktion."""
        session = DebuggeAbleitung("x**3", ordnung=2)

        assert isinstance(session, DebugSession)
        assert "2. Ableitung" in session.titel
        assert session.get_letzte_ergebnis() == 6 * Symbol("x")

    def test_debugge_nullstellen(self):
        """Teste die bequeme DebuggeNullstellen-Funktion."""
        session = DebuggeNullstellen("x**2 - 9")

        assert isinstance(session, DebugSession)
        assert "Nullstellenberechnung" in session.titel

        nullstellen_schritte = session.get_schritte_by_typ(
            BerechnungsSchrittTyp.NULLSTELLENSUCHE
        )
        ergebnis = nullstellen_schritte[0].ergebnis
        assert set(ergebnis) == {-3, 3}

    def test_debugge_vereinfachung(self):
        """Teste die bequeme DebuggeVereinfachung-Funktion."""
        session = DebuggeVereinfachung("x**2 + 2*x + 1")

        assert isinstance(session, DebugSession)
        assert "Funktionsvereinfachung" in session.titel

    def test_zeige_debug_schritte(self):
        """Teste die bequeme ZeigeDebugSchritte-Funktion."""
        session = DebuggeAbleitung("x**2")

        text_output = ZeigeDebugSchritte(session, format="text")
        assert isinstance(text_output, str)
        assert "1. Ableitung" in text_output

        dict_output = ZeigeDebugSchritte(session, format="dict")
        assert isinstance(dict_output, dict)


class TestIntegration:
    """Integrationstests für den FunktionsDebugger."""

    def test_komplexe_berechnung(self):
        """Teste eine komplexe Berechnung mit mehreren Schritten."""
        session = DebuggeAbleitung("(x + 2)**3", ordnung=2)

        # Überprüfe, dass verschiedene Schritttypen vorhanden sind
        schritt_typen = {schritt.typ for schritt in session.schritte}
        assert BerechnungsSchrittTyp.INITIALISIERUNG in schritt_typen
        assert BerechnungsSchrittTyp.ABLEITUNG in schritt_typen
        assert len(session.schritte) >= 3

    def test_verschiedene_detailgrade(self):
        """Teste verschiedene Detailgrade."""
        # Minimal
        debugger_minimal = FunktionsDebugger(DetailGrad.MINIMAL)
        session_minimal = debugger_minimal.berechne_ableitung("x**2")

        # Pädagogisch
        debugger_pädagogisch = FunktionsDebugger(DetailGrad.PÄDAGOGISCH)
        session_pädagogisch = debugger_pädagogisch.berechne_ableitung("x**2")

        # Pädagogisch sollte mehr Schritte haben
        assert len(session_pädagogisch.schritte) >= len(session_minimal.schritte)

    def test_fehlerbehandlung(self):
        """Teste die Fehlerbehandlung bei ungültigen Eingaben."""
        # Ungültige Funktion
        session = debugger.berechne_nullstellen("invalid_function")

        fehler_schritte = session.get_schritte_by_typ(BerechnungsSchrittTyp.FEHLER)
        assert len(fehler_schritte) >= 1

    def test_performance(self):
        """Teste die Performance des Debuggers."""
        start_time = time.time()

        # Führe mehrere Berechnungen durch
        for i in range(5):
            debugger.berechne_ableitung(f"x**{i}", ordnung=2)

        end_time = time.time()
        duration = end_time - start_time

        # Sollte nicht zu lange dauern
        assert duration < 5.0  # Maximal 5 Sekunden

    def test_mathematische_korrektheit(self):
        """Teste die mathematische Korrektheit der Ergebnisse."""
        # Teste verschiedene Ableitungen
        test_fälle = [
            ("x**2", 1, 2 * Symbol("x")),
            ("x**3", 2, 6 * Symbol("x")),
            ("sin(x)", 1, sp.cos(Symbol("x"))),
            ("exp(x)", 1, sp.exp(Symbol("x"))),
        ]

        for funktion, ordnung, expected in test_fälle:
            session = DebuggeAbleitung(funktion, ordnung)
            ergebnis = session.get_letzte_ergebnis()
            assert ergebnis == expected, f"Fehler bei {funktion}, {ordnung}. Ableitung"
