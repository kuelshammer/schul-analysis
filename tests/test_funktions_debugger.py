"""
Tests für den FunktionsDebugger und Schritt-für-Schritt Berechnungsanzeige.

Dieses Modul testet die umfassende Debugging-Funktionalität für mathematische
Berechnungen mit pädagogischem Fokus.
"""

import time
from unittest.mock import patch

import pytest
import sympy as sp

from schul_mathematik.analysis.debugger import (
    FunktionsDebugger,
    BerechnungsSchrittTyp,
    DetailGrad,
    DebugSession,
    BerechnungsSchritt,
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
    """Teste die BerechnungsSchrittTyp Enum."""

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
    """Teste die DetailGrad Enum."""

    def test_alle_detailgrade_vorhanden(self):
        """Teste, dass alle erwarteten Detailgrade vorhanden sind."""
        expected_grade = ["minimal", "normal", "ausführlich", "pädagogisch"]

        actual_grade = [grad.value for grad in DetailGrad]
        assert set(actual_grade) == set(expected_grade)


class TestBerechnungsSchritt:
    """Teste die BerechnungsSchritt Datenklasse."""

    def test_schritt_erstellung(self):
        """Teste die Erstellung eines Berechnungsschritts."""
        formel = sp.sympify("x**2 + 2*x + 1")
        schritt = BerechnungsSchritt(
            typ=BerechnungsSchrittTyp.VEREINFACHUNG,
            beschreibung="Testvereinfachung",
            formel_vorher=formel,
            formel_nachher=sp.sympify("(x + 1)**2"),
            ergebnis="(x + 1)**2",
            erläuterung="Ausdruck wurde faktorisiert",
            lernhinweis="Dies ist ein perfektes Quadrat!",
        )

        assert schritt.typ == BerechnungsSchrittTyp.VEREINFACHUNG
        assert schritt.beschreibung == "Testvereinfachung"
        assert schritt.formel_vorher == formel
        assert schritt.ergebnis == "(x + 1)**2"
        assert (
            schritt.schritt_nummer == 0
        )  # Wird in __post_init__ nicht automatisch gesetzt
        assert "x^{2} + 2 x + 1" in schritt.latex_vorher

    def test_schritt_to_dict(self):
        """Teste die Konvertierung eines Schritts in ein Dictionary."""
        formel = sp.sympify("x**2")
        schritt = BerechnungsSchritt(
            typ=BerechnungsSchrittTyp.ABLEITUNG,
            beschreibung="Ableitung bilden",
            formel_vorher=formel,
            formel_nachher=sp.sympify("2*x"),
            ergebnis="2*x",
        )

        schritt_dict = schritt.to_dict()

        assert schritt_dict["typ"] == "ableitung"
        assert schritt_dict["beschreibung"] == "Ableitung bilden"
        assert schritt_dict["formel_vorher"] == "x**2"
        assert schritt_dict["formel_nachher"] == "2*x"
        assert schritt_dict["ergebnis"] == "2*x"
        assert "zeitstempel" in schritt_dict
        assert "latex_vorher" in schritt_dict


class TestDebugSession:
    """Teste die DebugSession Klasse."""

    def test_session_erstellung(self):
        """Teste die Erstellung einer Debug-Session."""
        funktion = sp.sympify("x**2 + 3*x + 2")
        session = DebugSession(
            titel="Testsession", start_funktion=funktion, detailgrad=DetailGrad.NORMAL
        )

        assert session.titel == "Testsession"
        assert session.start_funktion == funktion
        assert len(session.schritte) == 0
        assert session.detailgrad == DetailGrad.NORMAL
        assert session.startzeit > 0

    def test_schritt_hinzufuegen(self):
        """Teste das Hinzufügen von Schritten zu einer Session."""
        session = DebugSession("Test", sp.sympify("x"))

        schritt1 = BerechnungsSchritt(
            typ=BerechnungsSchrittTyp.INITIALISIERUNG, beschreibung="Erster Schritt"
        )

        schritt2 = BerechnungsSchritt(
            typ=BerechnungsSchrittTyp.VEREINFACHUNG, beschreibung="Zweiter Schritt"
        )

        session.add_schritt(schritt1)
        session.add_schritt(schritt2)

        assert len(session.schritte) == 2
        assert session.schritte[0].schritt_nummer == 1
        assert session.schritte[1].schritt_nummer == 2

    def test_get_schritte_by_typ(self):
        """Teste das Filtern von Schritten nach Typ."""
        session = DebugSession("Test", sp.sympify("x"))

        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.INITIALISIERUNG, beschreibung="Init"
            )
        )

        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.VEREINFACHUNG, beschreibung="Vereinfachung 1"
            )
        )

        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.VEREINFACHUNG, beschreibung="Vereinfachung 2"
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
        assert all(
            s.typ == BerechnungsSchrittTyp.VEREINFACHUNG
            for s in vereinfachungs_schritte
        )

    def test_get_letzte_ergebnis(self):
        """Teste das Abrufen des letzten Ergebnisses."""
        session = DebugSession("Test", sp.sympify("x"))

        assert session.get_letzte_ergebnis() is None

        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.VEREINFACHUNG,
                beschreibung="Test",
                ergebnis="Ergebnis 1",
            )
        )

        assert session.get_letzte_ergebnis() == "Ergebnis 1"

        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.VEREINFACHUNG,
                beschreibung="Test 2",
                ergebnis="Ergebnis 2",
            )
        )

        assert session.get_letzte_ergebnis() == "Ergebnis 2"

    def test_berechnungsdauer(self):
        """Teste die Berechnung der Session-Dauer."""
        session = DebugSession("Test", sp.sympify("x"))

        # Teste ohne Endzeit - sollte positive Dauer sein
        dauer = session.berechnungsdauer()
        assert dauer >= 0

        # Teste mit gesetzter Endzeit
        session.endzeit = session.startzeit + 10
        assert session.berechnungsdauer() == 10

    def test_session_to_dict(self):
        """Teste die Konvertierung einer Session in ein Dictionary."""
        funktion = sp.sympify("x**2")
        session = DebugSession("Test", funktion)

        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.INITIALISIERUNG, beschreibung="Start"
            )
        )

        session_dict = session.to_dict()

        assert session_dict["titel"] == "Test"
        assert session_dict["start_funktion"] == "x**2"
        assert len(session_dict["schritte"]) == 1
        assert session_dict["anzahl_schritte"] == 1
        assert "dauer" in session_dict


class TestVereinfachungsStrategie:
    """Teste die VereinfachungsStrategie."""

    def test_kann_anwenden_immer(self):
        """Teste, dass die Vereinfachungsstrategie immer angewendet werden kann."""
        strategie = VereinfachungsStrategie()
        funktion = sp.sympify("x**2 + 2*x + 1")

        assert strategie.kann_anwenden(funktion, {}) is True

    def test_wende_an_einfacher_fall(self):
        """Teste die Anwendung der Vereinfachungsstrategie auf einen einfachen Fall."""
        strategie = VereinfachungsStrategie()
        session = DebugSession(
            "Test", sp.sympify("(x + 1)**2"), detailgrad=DetailGrad.NORMAL
        )

        ergebnis = strategie.wende_an(session.start_funktion, session, {})

        # Sollte vereinfacht werden
        assert ergebnis == sp.sympify("x**2 + 2*x + 1")
        assert len(session.schritte) >= 1

    def test_wende_an_mit_ausmultiplizieren(self):
        """Teste die Strategie mit Ausmultiplizieren im ausführlichen Modus."""
        strategie = VereinfachungsStrategie()
        session = DebugSession(
            "Test", sp.sympify("(x + 1)*(x - 1)"), detailgrad=DetailGrad.AUSFÜHRLICH
        )

        ergebnis = strategie.wende_an(session.start_funktion, session, {})

        # Sollte ausmultipliziert und dann vereinfacht werden
        assert ergebnis == sp.sympify("x**2 - 1")

        # Sollte mehrere Schritte haben
        assert len(session.schritte) >= 2

        # Prüfe, ob ein Ausmultiplizierungsschritt vorhanden ist
        transform_schritte = session.get_schritte_by_typ(
            BerechnungsSchrittTyp.TRANSFORMATION
        )
        assert len(transform_schritte) >= 1


class TestAbleitungsStrategie:
    """Teste die AbleitungsStrategie."""

    def test_kann_anwenden_fuer_ableitung(self):
        """Teste, dass die Strategie für Ableitungen angewendet werden kann."""
        strategie = AbleitungsStrategie()
        funktion = sp.sympify("x**2")
        kontext = {"operation": "ableitung"}

        assert strategie.kann_anwenden(funktion, kontext) is True

    def test_kann_nicht_anwenden_fuer_andere_operationen(self):
        """Teste, dass die Strategie für andere Operationen nicht angewendet werden kann."""
        strategie = AbleitungsStrategie()
        funktion = sp.sympify("x**2")
        kontext = {"operation": "integration"}

        assert strategie.kann_anwenden(funktion, kontext) is False

    def test_wende_an_erste_ableitung(self):
        """Teste die Berechnung der ersten Ableitung."""
        strategie = AbleitungsStrategie()
        session = DebugSession("Test", sp.sympify("x**2"), detailgrad=DetailGrad.NORMAL)
        kontext = {"operation": "ableitung", "ordnung": 1, "variable": sp.Symbol("x")}

        ergebnis = strategie.wende_an(session.start_funktion, session, kontext)

        assert ergebnis == sp.sympify("2*x")
        assert len(session.schritte) >= 2  # Initialisierung + Ableitung + Ergebnis

        # Prüfe, ob ein Ableitungsschritt vorhanden ist
        ableitung_schritte = session.get_schritte_by_typ(
            BerechnungsSchrittTyp.ABLEITUNG
        )
        assert len(ableitung_schritte) >= 1

    def test_wende_an_hoehere_ableitung(self):
        """Teste die Berechnung höherer Ableitungen."""
        strategie = AbleitungsStrategie()
        session = DebugSession("Test", sp.sympify("x**3"), detailgrad=DetailGrad.NORMAL)
        kontext = {"operation": "ableitung", "ordnung": 3, "variable": sp.Symbol("x")}

        ergebnis = strategie.wende_an(session.start_funktion, session, kontext)

        assert ergebnis == sp.sympify("6")  # d³/dx³(x³) = 6

        # Sollte mehrere Ableitungsschritte haben
        ableitung_schritte = session.get_schritte_by_typ(
            BerechnungsSchrittTyp.ABLEITUNG
        )
        assert len(ableitung_schritte) >= 3


class TestFunktionsDebugger:
    """Teste die Haupt-FunktionsDebugger Klasse."""

    def test_initialisierung(self):
        """Teste die Initialisierung des Debuggers."""
        debugger = FunktionsDebugger(DetailGrad.NORMAL)

        assert debugger.detailgrad == DetailGrad.NORMAL
        assert len(debugger.strategien) >= 2
        assert debugger._aktive_session is None
        assert len(debugger._session_history) == 0

    def test_start_session_mit_string(self):
        """Teste das Starten einer Session mit String-Eingabe."""
        debugger = FunktionsDebugger()

        session = debugger.start_session("Test", "x**2 + 3*x + 2")

        assert session.titel == "Test"
        assert session.start_funktion == sp.sympify("x**2 + 3*x + 2")
        assert len(session.schritte) == 1  # Initialisierungsschritt
        assert session.schritte[0].typ == BerechnungsSchrittTyp.INITIALISIERUNG
        assert debugger._aktive_session is session

    def test_start_session_mit_sympy(self):
        """Teste das Starten einer Session mit SymPy-Eingabe."""
        debugger = FunktionsDebugger()
        funktion = sp.sympify("sin(x)")

        session = debugger.start_session("Test", funktion)

        assert session.start_funktion == funktion
        assert len(session.schritte) == 1

    def test_start_session_mit_ungueltigem_string(self):
        """Teste das Starten einer Session mit ungültigem String."""
        debugger = FunktionsDebugger()

        with pytest.raises(ValueError, match="Ungültiger Funktionsausdruck"):
            debugger.start_session("Test", "ungültiger ausdruck #!&")

    def test_berechne_ableitung(self):
        """Teste die Ableitungsberechnung."""
        debugger = FunktionsDebugger(DetailGrad.NORMAL)

        session = debugger.berechne_ableitung("x**3", 2)

        assert session.titel == "2. Ableitung"
        assert session.start_funktion == sp.sympify("x**3")
        assert len(session.schritte) >= 1  # Mindestens Initialisierungsschritt
        assert session.get_letzte_ergebnis() == sp.sympify("6*x")
        assert session.endzeit is not None

    def test_berechne_nullstellen(self):
        """Teste die Nullstellenberechnung."""
        debugger = FunktionsDebugger()

        session = debugger.berechne_nullstellen("x**2 - 4")

        assert session.titel == "Nullstellenberechnung"
        assert len(session.schritte) >= 2

        # Finde Nullstellenschritt
        nullstellen_schritte = session.get_schritte_by_typ(
            BerechnungsSchrittTyp.NULLSTELLENSUCHE
        )
        assert len(nullstellen_schritte) >= 1

        ergebnis = nullstellen_schritte[0].ergebnis
        assert -2 in ergebnis or 2 in ergebnis

    def test_berechne_nullstellen_keine_loesung(self):
        """Teste die Nullstellenberechnung ohne Lösungen."""
        debugger = FunktionsDebugger()

        session = debugger.berechne_nullstellen("x**2 + 1")

        nullstellen_schritte = session.get_schritte_by_typ(
            BerechnungsSchrittTyp.NULLSTELLENSUCHE
        )
        assert len(nullstellen_schritte) >= 1
        assert nullstellen_schritte[0].ergebnis == []

    def test_vereinfache_funktion(self):
        """Teste die Funktionsvereinfachung."""
        debugger = FunktionsDebugger(DetailGrad.AUSFÜHRLICH)

        session = debugger.vereinfache_funktion("(x + 1)**2 + 2*(x + 1)")

        assert session.titel == "Funktionsvereinfachung"
        assert len(session.schritte) >= 2

        # Sollte vereinfacht werden
        ergebnis = session.get_letzte_ergebnis()
        assert ergebnis == sp.sympify("x**2 + 4*x + 3")

    def test_zeige_schritte_text_format(self):
        """Teste die Anzeige von Schritten im Textformat."""
        debugger = FunktionsDebugger()
        session = debugger.berechne_ableitung("x**2", 1)

        text_output = debugger.zeige_schritte(session, format="text")

        assert isinstance(text_output, str)
        assert "1. Ableitung" in text_output
        assert "Schritt 1:" in text_output or "Schritt 2:" in text_output
        assert "2*x" in text_output

    def test_zeige_schritte_latex_format(self):
        """Teste die Anzeige von Schritten im LaTeX-Format."""
        debugger = FunktionsDebugger()
        session = debugger.berechne_ableitung("x**2", 1)

        latex_output = debugger.zeige_schritte(session, format="latex")

        assert isinstance(latex_output, str)
        assert "\\section*" in latex_output
        assert "\\begin{enumerate}" in latex_output
        assert "\\end{enumerate}" in latex_output

    def test_zeige_schritte_dict_format(self):
        """Teste die Anzeige von Schritten im Dict-Format."""
        debugger = FunktionsDebugger()
        session = debugger.berechne_ableitung("x**2", 1)

        dict_output = debugger.zeige_schritte(session, format="dict")

        assert isinstance(dict_output, dict)
        assert "titel" in dict_output
        assert "schritte" in dict_output
        assert "anzahl_schritte" in dict_output
        assert len(dict_output["schritte"]) >= 1

    def test_zeige_schritte_ohne_session(self):
        """Teste die Anzeige ohne aktive Session."""
        debugger = FunktionsDebugger()

        output = debugger.zeige_schritte(None, format="text")
        assert output == "Keine aktive Session gefunden"

    def test_session_history(self):
        """Teste die Verwaltung der Session-History."""
        debugger = FunktionsDebugger()

        # Erstelle mehrere Sessions
        session1 = debugger.start_session("Test1", "x")
        session2 = debugger.start_session("Test2", "x**2")
        session3 = debugger.start_session("Test3", "sin(x)")

        history = debugger.get_session_history()

        assert len(history) == 3
        assert history[0] == session1
        assert history[1] == session2
        assert history[2] == session3

        # History sollte Kopien sein
        history[0] = None
        assert debugger._session_history[0] is not None

    def test_clear_history(self):
        """Teste das Löschen der Session-History."""
        debugger = FunktionsDebugger()

        debugger.start_session("Test", "x")
        assert len(debugger._session_history) == 1

        debugger.clear_history()

        assert len(debugger._session_history) == 0
        assert debugger._aktive_session is None

    def test_set_detailgrad(self):
        """Teste das Setzen des Detailgrads."""
        debugger = FunktionsDebugger(DetailGrad.NORMAL)

        # Ändere Detailgrad
        debugger.set_detailgrad(DetailGrad.PÄDAGOGISCH)
        assert debugger.detailgrad == DetailGrad.PÄDAGOGISCH

        # Mit aktiver Session
        session = debugger.start_session("Test", "x")
        assert session.detailgrad == DetailGrad.PÄDAGOGISCH


class TestGlobaleDebuggerInstanz:
    """Teste die globale Debugger-Instanz und API-Funktionen."""

    def test_globale_instanz_existiert(self):
        """Teste, dass die globale Debugger-Instanz existiert."""
        from schul_mathematik.analysis.debugger import debugger

        assert isinstance(debugger, FunktionsDebugger)

    def test_api_funktionen(self):
        """Teste die bequemen API-Funktionen."""
        # Teste Ableitung
        session = DebuggeAbleitung("x**3", 2)
        assert isinstance(session, DebugSession)
        assert session.get_letzte_ergebnis() == sp.sympify("6*x")

        # Teste Nullstellen
        session = DebuggeNullstellen("x**2 - 9")
        assert isinstance(session, DebugSession)
        ergebnis = session.get_letzte_ergebnis()
        assert -3 in ergebnis or 3 in ergebnis

        # Teste Vereinfachung
        session = DebuggeVereinfachung("(x + 2)**2")
        assert isinstance(session, DebugSession)
        assert session.get_letzte_ergebnis() == sp.sympify("x**2 + 4*x + 4")

    def test_zeige_debug_schritte_api(self):
        """Teste die ZeigeDebugSchritte API-Funktion."""
        session = DebuggeAbleitung("x**2", 1)

        # Text-Format
        text_output = ZeigeDebugSchritte(session, "text")
        assert isinstance(text_output, str)

        # Dict-Format
        dict_output = ZeigeDebugSchritte(session, "dict")
        assert isinstance(dict_output, dict)

        # Ungültiges Format
        with pytest.raises(ValueError, match="Unbekanntes Format"):
            ZeigeDebugSchritte(session, "ungültig")


class TestIntegration:
    """Integrationstests für den Debugger."""

    def test_komplexe_berechnung(self):
        """Teste eine komplexe Berechnung mit mehreren Strategien."""
        debugger = FunktionsDebugger(DetailGrad.AUSFÜHRLICH)

        # Komplexe Funktion: (x+1)² + 2(x+1) + 1
        session = debugger.vereinfache_funktion("(x + 1)**2 + 2*(x + 1) + 1")

        assert len(session.schritte) >= 3

        # Prüfe, ob verschiedene Schritttypen vorhanden sind
        typen = {schritt.typ for schritt in session.schritte}
        assert BerechnungsSchrittTyp.TRANSFORMATION in typen
        assert BerechnungsSchrittTyp.VEREINFACHUNG in typen
        assert BerechnungsSchrittTyp.ERGEBNIS in typen

        # Endergebnis sollte vereinfacht sein
        assert session.get_letzte_ergebnis() == sp.sympify("x**2 + 4*x + 4")

    def test_zeitmessung(self):
        """Teste die Zeitmessung bei Sessions."""
        debugger = FunktionsDebugger()

        start_time = time.time()
        session = debugger.berechne_ableitung("x**5", 3)
        end_time = time.time()

        assert session.startzeit >= start_time
        assert session.endzeit <= end_time
        assert session.berechnungsdauer() > 0
        assert session.berechnungsdauer() < (
            end_time - start_time + 0.1
        )  # Kleiner Toleranz

    def test_fehlerbehandlung(self):
        """Teste die Fehlerbehandlung bei ungültigen Eingaben."""
        debugger = FunktionsDebugger()

        # Ungültige Funktion für Nullstellen
        session = debugger.berechne_nullstellen("ungültig")

        # Sollte Fehler-Schritt enthalten
        fehler_schritte = session.get_schritte_by_typ(BerechnungsSchrittTyp.FEHLER)
        assert len(fehler_schritte) >= 1

    def test_pädagogischer_modus(self):
        """Teste den pädagogischen Modus mit zusätzlichen Erklärungen."""
        debugger = FunktionsDebugger(DetailGrad.PÄDAGOGISCH)

        session = debugger.vereinfache_funktion("(x + 1)*(x - 1)")

        # Sollte Lernhinweise enthalten
        lernhinweise = [s.lernhinweis for s in session.schritte if s.lernhinweis]
        assert len(lernhinweise) >= 1

        # Sollte mehr Schritte haben als im normalen Modus
        assert len(session.schritte) >= 3


class TestLeistungsaspekte:
    """Tests für Leistungsaspekte des Debuggers."""

    def test_viele_sessions(self):
        """Teste die Handhabung vieler Sessions."""
        debugger = FunktionsDebugger()

        # Erstelle viele Sessions
        for i in range(100):
            debugger.start_session(f"Session {i}", f"x**{i}")

        assert len(debugger._session_history) == 100

        # History sollte nicht zu langsam sein
        history = debugger.get_session_history()
        assert len(history) == 100

    def test_komplexe_funktionen(self):
        """Teste die Verarbeitung komplexer Funktionen."""
        debugger = FunktionsDebugger(DetailGrad.MINIMAL)

        # Komplexe Funktion
        komplexe_funktion = "x**10 + 5*x**9 - 3*x**8 + 2*x**7 - x**6 + 4*x**5 - 2*x**4 + x**3 - 7*x**2 + 3*x - 1"

        session = debugger.berechne_ableitung(komplexe_funktion, 2)

        # Sollte erfolgreich verarbeitet werden
        assert session is not None
        assert session.get_letzte_ergebnis() is not None
        assert len(session.schritte) >= 1
