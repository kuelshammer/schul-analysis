"""
Erweiterte Tests für die verbesserte GebrochenRationaleFunktion
"""

import time

import pytest

from schul_analysis.gebrochen_rationale import GebrochenRationaleFunktion


def test_sicherheit():
    """Teste Sicherheitsvalidierung"""
    from schul_analysis.errors import (
        DivisionDurchNullError,
        SicherheitsError,
    )

    # Teste gefährliche Ausdrücke
    gefaehrliche_ausdruecke = [
        "import os",
        "exec('print(1)')",
        "__import__('sys')",
        "subprocess.run",
        "open('/etc/passwd')",
    ]

    for ausdruck in gefaehrliche_ausdruecke:
        with pytest.raises(SicherheitsError):
            GebrochenRationaleFunktion(ausdruck)

    # Teste Division durch Null
    with pytest.raises(DivisionDurchNullError):
        GebrochenRationaleFunktion("x", "0")

    print("✅ Sicherheitstests erfolgreich!")


def test_caching():
    """Teste Caching-Funktionalität"""
    f = GebrochenRationaleFunktion("(x^2-4)/(x-2)")

    # Erster Aufruf - sollte berechnet werden
    polstellen1 = f.polstellen()

    # Zweiter Aufruf - sollte aus Cache kommen
    polstellen2 = f.polstellen()

    assert polstellen1 == polstellen2

    # Teste Cache-Invalidierung nach Kürzen
    f.kürzen()
    assert f._cache["polstellen"] is None

    print("✅ Caching-Tests erfolgreich!")


def test_mathematische_genauigkeit():
    """Teste mathematische Genauigkeit und Randfälle"""

    # Teste Kürzung mit cancel()
    f = GebrochenRationaleFunktion("(x^2-4)/(x-2)")
    f.kürzen()

    # Nach Kürzung sollte einfacher sein
    assert "x-2" not in f.nenner.term().lower()

    # Teste asymptotisches Verhalten
    g = GebrochenRationaleFunktion("(x^2+1)/x")
    asymptoten = g._berechne_asymptoten()

    # Sollte schiefe Asymptote haben
    assert any(a["typ"] == "schief" for a in asymptoten)

    # Teste horizontale Asymptote
    h = GebrochenRationaleFunktion("(x+1)/(x^2+1)")
    asymptoten_h = h._berechne_asymptoten()

    # Sollte horizontale Asymptote bei y=0 haben
    assert any(a["typ"] == "horizontal" and a["y"] == 0 for a in asymptoten_h)

    print("✅ Mathematische Genauigkeitstests erfolgreich!")


def test_performance():
    """Teste Performance-Verbesserungen durch Caching"""
    f = GebrochenRationaleFunktion("(x^4-5x^2+4)/(x^2-1)")

    # Erster Aufruf
    start = time.time()
    f.polstellen()
    erste_zeit = time.time() - start

    # Zweiter Aufruf (sollte schneller sein)
    start = time.time()
    f.polstellen()
    zweite_zeit = time.time() - start

    # Zweiter Aufruf sollte deutlich schneller sein
    assert zweite_zeit < erste_zeit

    print("✅ Performance-Tests erfolgreich!")


def test_fehlerbehandlung():
    """Teste umfassende Fehlerbehandlung"""
    from schul_analysis.gebrochen_rationale import UngueltigeEingabeError

    # Teste ungültige Eingaben
    with pytest.raises(UngueltigeEingabeError):
        GebrochenRationaleFunktion(None)

    with pytest.raises(UngueltigeEingabeError):
        GebrochenRationaleFunktion("", "")

    # Teste ungültige mathematische Ausdrücke
    with pytest.raises(UngueltigeEingabeError):
        GebrochenRationaleFunktion("x+++", "x")

    # Teste Wertebereich-Checks
    f = GebrochenRationaleFunktion("1/x")

    # Sollte Exception bei Polstelle werfen
    with pytest.raises(ZeroDivisionError):
        f.wert(0)

    print("✅ Fehlerbehandlungs-Tests erfolgreich!")


if __name__ == "__main__":
    print("=== Teste erweiterte Funktionen ===")

    # Führe zusätzliche Tests durch
    test_sicherheit()
    test_caching()
    test_mathematische_genauigkeit()
    test_performance()
    test_fehlerbehandlung()

    print("🎉 Alle erweiterten Tests erfolgreich durchgeführt!")
