#!/usr/bin/env python3
"""
Test für vordefinierte Variablen und Parameter
"""

import sys

sys.path.insert(0, "src")

# Importieren mit vordefinierten Variablen und Parametern
from schul_analysis import (
    x,
    t,
    a,
    k,
    Variable,
    Parameter,
    ParametrischeFunktion,
    Graph_parametrisiert,
)


def test_vordefinierte():
    print("=== Test Vordefinierte Variablen und Parameter ===")

    # 1. Prüfe vordefinierte Variablen
    print(f"Variable x: {x} (Typ: {type(x)})")
    print(f"Variable t: {t} (Typ: {type(t)})")

    # 2. Prüfe vordefinierte Parameter
    print(f"Parameter a: {a} (Typ: {type(a)})")
    print(f"Parameter k: {k} (Typ: {type(k)})")

    # 3. Teste Verwendung ohne explizite Definition
    print("\n=== Verwendung ohne explizite Definition ===")

    # Erstelle parametrische Funktion mit vordefinierten Variablen/Parametern
    f_param = ParametrischeFunktion([0, 1, a], [x])  # a*x^2 + x
    print(f"Parametrische Funktion: {f_param.term()}")

    # Teste konkrete Werte
    print("\n=== Konkrete Werte ===")
    for a_wert in [-1, 0, 1]:
        f_konkret = f_param.mit_wert(a=a_wert)
        print(f"a={a_wert}: f(x) = {f_konkret.term()}")
        print(f"  f(2) = {f_konkret.wert(2):.2f}")

    # 4. Teste Graph-Erstellung
    print("\n=== Graph-Erstellung ===")
    try:
        fig = Graph_parametrisiert(f_param, a=[-2, -1, 0, 1, 2])
        print("Graph_parametrisiert erfolgreich erstellt!")
        print(f"Titel: {fig.layout.title.text}")

        # Speichere als HTML
        fig.write_html("test_vordefiniert_graph.html")
        print("Graph als HTML gespeichert: test_vordefiniert_graph.html")

    except Exception as e:
        print(f"Fehler bei Graph_parametrisiert: {e}")
        import traceback

        traceback.print_exc()

    # 5. Teste mit anderen vordefinierten Variablen/Parametern
    print("\n=== Andere Kombinationen ===")

    # g_k(t) = k*t^2 + t
    g_param = ParametrischeFunktion([0, 1, k], [t])  # k*t^2 + t
    print(f"Parametrische Funktion g: {g_param.term()}")

    for k_wert in [-1, 1]:
        g_konkret = g_param.mit_wert(k=k_wert)
        print(f"k={k_wert}: g(t) = {g_konkret.term()}")
        print(f"  g(1) = {g_konkret.wert(1):.2f}")

    print("\n=== Test abgeschlossen ===")


if __name__ == "__main__":
    test_vordefinierte()
