#!/usr/bin/env python3
"""
Test für parametrische Funktionen
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik import (
    Graph_parametrisiert,
    Parameter,
    ParametrischeFunktion,
    Variable,
)


def test_parametrische_funktionen():
    print("=== Test Parametrische Funktionen ===")

    # 1. Erstelle Variable und Parameter
    x = Variable("x")
    a = Parameter("a")

    print(f"Variable: {x.name}")
    print(f"Parameter: {a.name}")

    # 2. Erstelle parametrische Funktion f_a(x) = a*x^2 + x
    f_param = ParametrischeFunktion([0, 1, a], [x])  # a*x^2 + x
    print(f"Parametrische Funktion: {f_param.term()}")

    # 3. Teste symbolische Berechnungen
    print("\n=== Symbolische Berechnungen ===")

    # Nullstellen (symbolisch)
    nullstellen_symbolisch = f_param.nullstellen()
    print(f"Symbolische Nullstellen: {nullstellen_symbolisch}")

    # Extremstellen (symbolisch mit Bedingungen)
    extremstellen_symbolisch = f_param.extremstellen()
    print(f"Symbolische Extremstellen: {extremstellen_symbolisch}")

    # 4. Teste konkrete Werte
    print("\n=== Konkrete Werte ===")

    # Für a = 1: f(x) = x^2 + x
    f_konkret = f_param.mit_wert(a=1)
    print(f"f_1(x) = {f_konkret.term()}")
    print(f"f_1(2) = {f_konkret.wert(2)}")

    # Nullstellen für a = 1
    nullstellen_konkret = f_konkret.nullstellen()
    print(f"Nullstellen für a=1: {nullstellen_konkret}")

    # Extremstellen für a = 1
    extremstellen_konkret = f_konkret.extremstellen()
    print(f"Extremstellen für a=1: {extremstellen_konkret}")

    # 5. Teste verschiedene Parameterwerte
    print("\n=== Verschiedene Parameterwerte ===")

    for a_wert in [-2, -1, 0, 1, 2]:
        f_a = f_param.mit_wert(a=a_wert)
        print(f"a={a_wert}: f(x) = {f_a.term()}")

        # Berechne einige Werte
        for x_wert in [-2, -1, 0, 1, 2]:
            try:
                y_wert = f_a.wert(x_wert)
                print(f"  f({x_wert}) = {y_wert:.2f}")
            except Exception:
                print(f"  f({x_wert}) = undefiniert")

    # 6. Teste Graph_parametrisiert
    print("\n=== Graph Parametrisiert ===")

    try:
        fig = Graph_parametrisiert(f_param, a=[-2, -1, 0, 1, 2])
        print("Graph_parametrisiert erfolgreich erstellt!")
        print(f"Titel: {fig.layout.title.text}")

        # Speichere als HTML zur Visualisierung
        fig.write_html("test_parametrisch_graph.html")
        print("Graph als HTML gespeichert: test_parametrisch_graph.html")

    except Exception as e:
        print(f"Fehler bei Graph_parametrisiert: {e}")
        import traceback

        traceback.print_exc()

    print("\n=== Test abgeschlossen ===")


if __name__ == "__main__":
    test_parametrische_funktionen()
