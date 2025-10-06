"""
Komprehensive Demonstration der modernen Magic Factory API

Dieses Beispiel zeigt alle Funktionen der neuen API mit automatischer Funktionserkennung
und wie sie im Unterricht eingesetzt werden können.
"""

from schul_analysis import Funktion, ableitung, extrema, nullstellen, symmetrie

# =============================================================================
# 1. BEISPIEL: Quadratische Funktion (Magic Factory)
# =============================================================================

print("\n📐 BEISPIEL 1: Quadratische Funktion mit Magic Factory")
print("-" * 55)

# Automatische Funktionserkennung
f = Funktion("3x^2 - 4x + 1")
print(f"f(x) = {f.term()}")
print(f"Funktionstyp: {f.funktionstyp}")

# Analysiere die Funktion mit der neuen Syntax
print(f"Nullstellen: {nullstellen(f)}")
print(f"1. Ableitung: {ableitung(f).term()}")
print(f"2. Ableitung: {ableitung(f, 2).term()}")
print(f"Extrema: {extrema(f)}")
print(f"Symmetrie: {symmetrie(f)}")

# Werteberechnung mit natürlicher Syntax
print(f"f(0) = {f(0)}")
print(f"f(1) = {f(1)}")

# =============================================================================
# 2. BEISPIEL: Kubische Funktion
# =============================================================================

print("\n🎲 BEISPIEL 2: Kubische Funktion")
print("-" * 40)

# Erstelle kubische Funktion
g = Funktion("x^3 - 3x^2 - 4x + 12")
print(f"g(x) = {g.term()}")
print(f"Funktionstyp: {g.funktionstyp}")

# Analyse der kubischen Funktion
print(f"Nullstellen: {nullstellen(g)}")
print(f"1. Ableitung: {ableitung(g).term()}")
print(f"2. Ableitung: {ableitung(ableitung(g)).term()}")

# Extremstellen analysieren
ext = extrema(g)
if ext:
    print("Extremstellen:")
    for x_ext, art in ext:
        y_ext = g(x_ext)
        print(f"  {art} bei ({x_ext:.2f}, {y_ext:.2f})")

# =============================================================================
# 3. BEISPIEL: Lineare Funktionen und Schnittpunkte
# =============================================================================

print("\n📏 BEISPIEL 3: Lineare Funktionen")
print("-" * 35)

# Zwei lineare Funktionen
f1 = Funktion("2x + 3")  # 2x + 3
f2 = Funktion("-x + 5")  # -x + 5

print(f"f1(x) = {f1.term()}")
print(f"f2(x) = {f2.term()}")

# Schnittpunkt berechnen (Nullstellen der Differenz)
differenz = Funktion("(2x + 3) - (-x + 5)")  # 3x - 2
schnittpunkt = nullstellen(differenz)
print(f"Schnittpunkt bei x = {schnittpunkt}")

if schnittpunkt:
    y_schnitt = f1(schnittpunkt[0])
    print(f"Schnittpunkt: ({schnittpunkt[0]:.2f}, {y_schnitt:.2f})")

# =============================================================================
# 4. BEISPIEL: Gebrochen-rationale Funktion
# =============================================================================

print("\n🔢 BEISPIEL 4: Gebrochen-rationale Funktion")
print("-" * 45)

h = Funktion("(x^2 - 4)/(x - 2)")
print(f"h(x) = {h.term()}")
print(f"Funktionstyp: {h.funktionstyp}")

# Spezielle Eigenschaften
print(f"Definitionsbereich: {h.definitionsbereich()}")

try:
    pol = h.polstellen()
    print(f"Polstellen: {pol}")
except AttributeError:
    print("Polstellen: Nicht verfügbar für diesen Funktionstyp")

print(f"Nullstellen: {nullstellen(h)}")

# =============================================================================
# 5. BEISPIEL: Wertetabelle erstellen
# =============================================================================

print("\n📊 BEISPIEL 5: Wertetabelle")
print("-" * 25)

# Funktion für Wertetabelle
tabellen_funktion = Funktion("x^2 - 2x - 3")
print(f"Funktion: f(x) = {tabellen_funktion.term()}")

# Wertetabelle
x_werte = [-2, -1, 0, 1, 2, 3, 4]
print("Wertetabelle für f(x) = x² - 2x - 3:")
for x, y in zip(x_werte, [tabellen_funktion(x) for x in x_werte], strict=False):
    print(f"f({x:4.1f}) = {y:6.2f}")

# =============================================================================
# 6. BEISPIEL: Parameter-Bestimmung
# =============================================================================

print("\n🎯 BEISPIEL 6: Parameter-Bestimmung")
print("-" * 38)

# Parabel durch Punkte f(1)=2, f(2)=3, f(0)=6
print("Gesucht: Parabel f(x) = ax² + bx + c mit:")
print("  f(1) = 2")
print("  f(2) = 3")
print("  f(0) = 6")

# Lösung: c = 6, a + b + 6 = 2 → a + b = -4, 4a + 2b + 6 = 3 → 4a + 2b = -3
# Aus a + b = -4 folgt b = -4 - a
# Einsetzen: 4a + 2(-4 - a) = -3 → 4a - 8 - 2a = -3 → 2a = 5 → a = 2.5, b = -6.5

print("\nLösung:")
print("  c = 6 (aus f(0) = 6)")
print("  a + b = -4 (aus f(1) = 2)")
print("  4a + 2b = -3 (aus f(2) = 3)")
print("  → a = 2.5, b = -6.5, c = 6")

# Ergebnis als konkrete Funktion
ergebnis_funktion = Funktion("2.5x^2 - 6.5x + 6")
print(f"\nGefundene Parabel: f(x) = {ergebnis_funktion.term()}")

# Verifizierung
print("\nVerifizierung:")
print(f"  f(1) = {ergebnis_funktion(1)} (sollte 2 sein)")
print(f"  f(2) = {ergebnis_funktion(2)} (sollte 3 sein)")

# =============================================================================
# 7. BEISPIEL: Ableitungs-Kette
# =============================================================================

print("\n🔗 BEISPIEL 7: Ableitungs-Kette")
print("-" * 35)

# Ausgangsfunktion
original = Funktion("x^4 - 2x^3 + x^2 - 4x + 1")
print(f"Original: f(x) = {original.term()}")

# Ableitungen mit automatischer Namensgebung
f1 = ableitung(original)  # f'
f2 = ableitung(f1)  # f''
f3 = ableitung(f2)  # f'''

print(f"f'(x) = {f1.term()} (Name: {f1.name})")
print(f"f''(x) = {f2.term()} (Name: {f2.name})")
print(f"f'''(x) = {f3.term()} (Name: {f3.name})")

# =============================================================================
# 8. BEISPIEL: Physikalische Anwendung
# =============================================================================

print("\n🚀 BEISPIEL 8: Physikalische Anwendung")
print("-" * 40)

# Höhenfunktion: h(t) = -5t² + 20t (g ≈ 10 m/s²)
h = Funktion("-5t^2 + 20t")
print(f"Höhe: h(t) = {h.term()} m")

# Wann erreicht der Ball die maximale Höhe?
max_zeit = extrema(h)[0][0] if extrema(h) else None
if max_zeit is not None:
    max_hoehe = h(max_zeit)
    print(f"  Maximale Höhe von {max_hoehe} m nach {max_zeit} s")

# Wann landet der Ball wieder?
landezeiten = nullstellen(h)
if len(landezeiten) > 1:
    print(f"  Landung nach {landezeiten[1]} s")

# Geschwindigkeit als 1. Ableitung
v = ableitung(h)
print(f"  Geschwindigkeit: v(t) = {v.term()} m/s")

# =============================================================================
# ZUSAMMENFASSUNG
# =============================================================================

print("\n" + "=" * 60)
print("🎉 ZUSAMMENFASSUNG DER MAGIC FACTORY API")
print("=" * 60)

print("✨ NEUE FEATURES:")
print("• 🎯 Magic Factory: Funktion('term') - automatische Typenerkennung")
print("• 📝 LaTeX-Darstellung: f zeigt automatisch f(x) = term an")
print("• 🏷️  Automatische Namensgebung: f → f' → f''")
print("• 🧮 Natürliche Syntax: f(2) statt auswerten(f, 2)")
print("• 🔍 Kleingeschriebene Funktionen: nullstellen(), ableitung(), extrema()")
print("• 📊 Plotly-Integration: mathematisch korrekte Graphen")

print("\n🎓 PÄDAGOGISCHE VORTEILE:")
print("• Einfache, intuitive Syntax für Schüler")
print("• Automatische Funktionsklassen-Erkennung")
print("• Deutsche Fehlermeldungen")
print("• Mathematisch korrekte Darstellung")
print("• Perfekt für interaktiven Unterricht")

print("\n" + "=" * 60)
