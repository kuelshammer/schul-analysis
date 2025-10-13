#!/usr/bin/env python3
"""Debug script to understand error handling"""

from src.schul_mathematik.analysis.debugger import debugger
import traceback

# Test error handling
print("=== Testing error handling ===")
try:
    session = debugger.berechne_nullstellen("invalid_function")
    print(f"Session created successfully")
    print(f"Anzahl schritte: {len(session.schritte)}")
    print(f"Schritte:")
    for i, schritt in enumerate(session.schritte):
        print(f"  {i + 1}. {schritt.typ}: {schritt.beschreibung}")

    fehler_schritte = session.get_schritte_by_typ("FEHLER")
    print(f"Fehler schritte: {len(fehler_schritte)}")

except Exception as e:
    print(f"Exception occurred: {e}")
    traceback.print_exc()

# Test with a really invalid expression
print("\n=== Testing with obviously invalid expression ===")
try:
    session = debugger.berechne_nullstellen("x**2 + * invalid syntax")
    print(f"Session created successfully")
    print(f"Anzahl schritte: {len(session.schritte)}")

    fehler_schritte = session.get_schritte_by_typ("FEHLER")
    print(f"Fehler schritte: {len(fehler_schritte)}")

except Exception as e:
    print(f"Exception occurred: {e}")
    traceback.print_exc()
