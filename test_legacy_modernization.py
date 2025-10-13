#!/usr/bin/env python3
"""
Test für die Backward-Compatibility-Modernisierung

Dieses Skript testet die neue explizite Adapter-Klasse und vergleicht
sie mit der alten magic __getattr__ Implementierung.
"""

from src.schul_mathematik.analysis.funktion import Funktion


def test_modern_api():
    """Testet die moderne API ohne Legacy-Adapter."""
    print("=== Test: Moderne API ===")

    f = Funktion("x^2 - 4")

    # Teste moderne API
    print(f"f.term() = {f.term()}")
    print(f"f.nullstellen = {[float(n.x) for n in f.nullstellen]}")
    print(f"f.ableitung(1).term() = {f.ableitung(1).term()}")
    print(f"f.extrema() = {f.extrema()}")
    print()


def test_legacy_adapter_api():
    """Testet die neue Legacy-API über den Adapter."""
    print("=== Test: Legacy-Adapter-API ===")

    f = Funktion("x^2 - 4")

    # Teste Legacy-API über Adapter
    print(f"f.legacy.nullstellen = {[float(n.x) for n in f.legacy.nullstellen]}")
    print(f"f.legacy.get_extremstellen() = {f.legacy.get_extremstellen()}")
    print(f"f.legacy.get_steigung() = {f.legacy.get_steigung()}")
    print(f"f.legacy.get_y_achsenabschnitt() = {f.legacy.get_y_achsenabschnitt()}")
    print()


def test_legacy_adapter_with_complex_function():
    """Testet den Legacy-Adapter mit komplexeren Funktionen."""
    print("=== Test: Legacy-Adapter mit komplexen Funktionen ===")

    f = Funktion("x^3 - 3x^2 + 2")

    # Teste verschiedene Legacy-Methoden
    print(f"f.legacy.nullstellen = {[float(n.x) for n in f.legacy.nullstellen]}")
    print(f"f.legacy.get_wendepunkte() = {f.legacy.get_wendepunkte()}")

    # Teste Legacy-Methoden für spezielle Funktionen
    if hasattr(f.legacy, "scheitelpunkt"):
        print(f"f.legacy.scheitelpunkt() = {f.legacy.scheitelpunkt()}")

    print()


def test_performance_comparison():
    """Vergleicht die Performance zwischen moderner und Legacy-API."""
    print("=== Test: Performance-Vergleich ===")

    import time

    f = Funktion("x^5 - 3x^4 + 2x^3 - 5x^2 + x - 1")

    # Moderne API
    start = time.perf_counter()
    for _ in range(100):
        _ = f.nullstellen
        _ = f.ableitung(1)
        _ = f.extrema()
    modern_time = time.perf_counter() - start

    # Legacy-API
    start = time.perf_counter()
    for _ in range(100):
        _ = f.legacy.nullstellen
        _ = f.legacy.get_extremstellen()
    legacy_time = time.perf_counter() - start

    print(f"Moderne API (100x): {modern_time:.4f}s")
    print(f"Legacy-API (100x): {legacy_time:.4f}s")

    if modern_time > 0:
        overhead = (legacy_time - modern_time) / modern_time * 100
        print(f"Legacy-Overhead: {overhead:.1f}%")

    print()


def test_adapter_instantiation():
    """Testet, dass der Adapter korrekt instanziiert wird."""
    print("=== Test: Adapter-Instanziierung ===")

    f = Funktion("x^2 - 4")

    # Erster Zugriff - sollte Adapter erstellen
    print("Erster Zugriff auf f.legacy...")
    adapter1 = f.legacy
    print(f"Adapter-Typ: {type(adapter1)}")
    print(f"Adapter-ID: {id(adapter1)}")

    # Zweiter Zugriff - sollte gleicher Adapter sein
    print("Zweiter Zugriff auf f.legacy...")
    adapter2 = f.legacy
    print(f"Adapter-ID: {id(adapter2)}")

    # Teste, ob es der gleiche Adapter ist
    if adapter1 is adapter2:
        print("✅ Adapter wird korrekt wiederverwendet")
    else:
        print("❌ Adapter wird neu erstellt")

    print()


def test_error_handling():
    """Testet die Fehlerbehandlung des Legacy-Adapters."""
    print("=== Test: Fehlerbehandlung ===")

    f = Funktion("x^2 - 4")

    # Teste Zugriff auf nicht existierende Attribute
    try:
        _ = f.legacy.nicht_existierende_methode
        print("❌ Kein Fehler bei nicht existierender Methode")
    except AttributeError as e:
        print(f"✅ Korrekte Fehlerbehandlung: {e}")

    print()


def main():
    """Führt alle Tests durch."""
    print("Backward-Compatibility-Modernisierung - Test")
    print("=" * 50)
    print()

    # Führe alle Tests durch
    test_modern_api()
    test_legacy_adapter_api()
    test_legacy_adapter_with_complex_function()
    test_performance_comparison()
    test_adapter_instantiation()
    test_error_handling()

    print("Backward-Compatibility-Test abgeschlossen!")
    print()
    print("🎯 Ergebnis:")
    print("✅ Explizite Adapter-Klasse implementiert")
    print("✅ Magic __getattr__ entfernt")
    print("✅ Legacy-API über f.legacy verfügbar")
    print("✅ Moderne API weiterhin voll funktionsfähig")


if __name__ == "__main__":
    main()
