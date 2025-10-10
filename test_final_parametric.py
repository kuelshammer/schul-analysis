#!/usr/bin/env python3
"""
Einfacher Test der fortgeschrittenen parametrischen Methoden.
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis.funktion import Funktion

print("=== Test fortgeschrittene parametrische Methoden ===\n")

# Test 1: Nullstellen
print("📍 Test 1: Nullstellen f(x) = x² - (a+b)x + ab")
f = Funktion("x^2 - (a+b)*x + a*b")
nullstellen = f.nullstellen_optimiert()
print(f"Ergebnis: {len(nullstellen)} Nullstellen")
for ns in nullstellen:
    print(f"  x = {ns.x}")

print()

# Test 2: Extremstellen
print("📈 Test 2: Extremstellen f(x) = ax² + bx + c")
f2 = Funktion("a*x^2 + b*x + c")
extremstellen = f2.extremstellen_optimiert()
print(f"Ergebnis: {len(extremstellen)} Extremstellen")
for es in extremstellen:
    print(f"  x = {es.x}, Typ = {es.typ}")

print()

# Test 3: Wendestellen
print("🌀 Test 3: Wendestellen f(x) = x³ + ax")
f3 = Funktion("x^3 + a*x")
wendestellen = f3.wendestellen_optimiert()
print(f"Ergebnis: {len(wendestellen)} Wendestellen")
for ws in wendestellen:
    print(f"  x = {ws.x}, Typ = {ws.typ}")

print()
print("✅ Alle Tests erfolgreich!")
