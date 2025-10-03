# Automatische Symbolerkennung in GanzrationaleFunktion

## Übersicht

Die `GanzrationaleFunktion`-Klasse wurde um eine **automatische Symbolerkennung** erweitert, die es Schülern ermöglicht, Funktionen intuitiv mit mathematischer Notation zu definieren. Das System erkennt automatisch Variablen und Parameter und klassifiziert sie entsprechend.

## 🎯 Hauptvorteile

- **Intuitive Syntax**: `GanzrationaleFunktion("a x^2 + 1")` funktioniert sofort
- **Automatische Klassifizierung**: Symbole werden intelligent als Variable oder Parameter erkannt
- **Schülerfreundlich**: Keine Notwendigkeit, Variable oder Parameter manuell zu definieren
- **Voll kompatibel**: Bestehender Code funktioniert weiterhin unverändert

## 🔧 Funktionsweise

### Automatische Erkennung

```python
from schul_analysis import GanzrationaleFunktion

# Quadratische Funktion mit Parameter
f = GanzrationaleFunktion("a x^2 + b x + c")
print(f"Variable: {[v.name for v in f.variablen]}")      # ['x']
print(f"Parameter: {[p.name for p in f.parameter]}")    # ['a', 'b', 'c']

# Lineare Funktion mit anderer Variable
g = GanzrationaleFunktion("100t + 20")
print(f"Variable: {[v.name for v in g.variablen]}")      # ['t']
print(f"Parameter: {[p.name for p in g.parameter]}")    # []
```

### Heuristik-basierte Klassifizierung

Das System verwendet intelligente Heuristiken zur Klassifizierung:

#### Als Variable erkannt:
- `x, y, z` (Standard-Variablen)
- `t, u, v, w` (Zeit- und andere Variablen)

#### Als Parameter erkannt:
- `a, b, c, d` (Standard-Parameter)
- `k, m, n` (Konstanten)
- `p, q, r` (Parameter)

#### Bei Unsicherheit:
- Symbole, die nicht in den Standard-Listen vorkommen, werden als Variable behandelt
- Bei mehreren Variablen wird die erste alphabetisch als Hauptvariable ausgewählt

## 📝 Verwendung

### 1. Einfache quadratische Funktion

```python
f = GanzrationaleFunktion("a x^2 + b x + c")
print(f.term())  # ax^2+bx+c
print(f.grad())  # 2
```

### 2. Lineare Funktion

```python
g = GanzrationaleFunktion("100t + 20")
print(g.term())  # 100t+20
print(g.grad())  # 1
```

### 3. Mehrere Variablen

```python
h = GanzrationaleFunktion("x^2 + y^2 + z^2")
print(h.term())  # x^2+y^2+z^2
print(f"Variablen: {[v.name for v in h.variablen]}")  # ['x', 'y', 'z']
```

### 4. Backward-Kompatibilität

```python
# Alte Syntax funktioniert weiterhin
f1 = GanzrationaleFunktion([1, 2, 3])      # x^2 + 2x + 3
f2 = GanzrationaleFunktion({0: 5, 2: 1})   # x^2 + 5
f3 = GanzrationaleFunktion("x^2 - 4")      # x^2 - 4
```

## 🔍 Methoden zur Symbol-Verwaltung

### Zugriff auf erkannte Symbole

```python
f = GanzrationaleFunktion("a x^2 + b x + c")

# Liste aller Variablen
variablen = [v.name for v in f.variablen]  # ['x']

# Liste aller Parameter
parameter = [p.name for p in f.parameter]  # ['a', 'b', 'c']

# Hauptvariable (für Berechnungen)
hauptvariable = f.hauptvariable.name  # 'x'
```

### Manuelle Überschreibung

```python
f = GanzrationaleFunktion("x^2 + y^2")

# Manuelles Setzen von Variablen und Parametern
f.variablen = [Variable('t')]  # t als Hauptvariable
f.parameter = [Parameter('a')] # a als Parameter
f.hauptvariable = f.variablen[0]
```

## 🧪 Typische Anwendungsfälle

### 1. Parameterstudien

```python
# Funktion mit Parameter definieren
f = GanzrationaleFunktion("a x^2 + b x + c")

# Verschiedene Parameterwerte testen
for a in [-2, -1, 0, 1, 2]:
    # Hier müsste man die Parameter manuell einsetzen
    print(f"a = {a}: Funktion wird zu ...")
```

### 2. Kurvendiskussion

```python
# Automatische Erkennung der Hauptvariable
f = GanzrationaleFunktion("x^3 - 3x^2 + 2x")
print(f"Hauptvariable: {f.hauptvariable.name}")  # 'x'

# Berechnungen durchführen
print(f"Nullstellen: {f.nullstellen()}")          # [0, 1, 2]
print(f"Extremstellen: {f.extremstellen()}")      # [(0, 'Maximum'), (2, 'Minimum')]
```

### 3. Ableitungen

```python
f = GanzrationaleFunktion("a x^2 + b x + c")
f1 = f.ableitung()
print(f"f'(x) = {f1.term()}")  # 2ax+b
```

## ⚠️ Einschränkungen

### 1. Komplexe Ausdrücke

```python
# Funktioniert NICHT (nicht ganzrational)
f = GanzrationaleFunktion("sin(x) + cos(x)")
# Fehler: Ungültiger mathematischer Ausdruck

# Funktioniert NICHT (Klammern mit Parametern)
f = GanzrationaleFunktion("a(x - 2)^2 + 3")
# Fehler: Ungültiger mathematischer Ausdruck
```

### 2. Symbol-Namen

```python
# Funktioniert nicht gut (mehrbuchstabige Symbole)
f = GanzrationaleFunktion("alpha + beta")
# Erkennt: ha, lp, et, a, b (falsche Zerlegung)
```

### 3. Keine automatische Wert-Einsetzung

```python
# NICHT möglich (nur bei ParametrischeFunktion)
f = GanzrationaleFunktion("a x^2 + b x + c")
f_konkret = f.mit_wert(a=1, b=2, c=1)  # AttributeError
```

## 🔧 Technische Details

### Interne Struktur

Die Klasse verwendet interne `_Variable` und `_Parameter` Klassen, um:

1. **Circular Imports zu vermeiden**: Keine Abhängigkeit vom `parametrisch`-Modul
2. **Performance zu optimieren**: Einfache Datenstrukturen für schnellen Zugriff
3. **Kompatibilität zu wahren**: Keine Änderung an der öffentlichen API

### SymPy-Integration

Die automatische Erkennung nutzt:

- `sp.sympify()` zur Umwandlung von Strings in SymPy-Ausdrücke
- `free_symbols` zur Extraktion aller Symbole
- `is_polynomial()` zur Validierung ganzrationaler Funktionen
- `degree()` zur Bestimmung des Funktionsgrades

## 📚 Beispiele aus der Praxis

### Beispiel 1: Quadratische Funktionen

```python
# Standardform
f1 = GanzrationaleFunktion("x^2 - 4")
# Ergebnis: Variable=['x'], Parameter=[], Grad=2

# Mit Parameter
f2 = GanzrationaleFunktion("a x^2 + b x + c")
# Ergebnis: Variable=['x'], Parameter=['a','b','c'], Grad=2
```

### Beispiel 2: Lineare Funktionen

```python
# Standard
f1 = GanzrationaleFunktion("2x + 5")
# Ergebnis: Variable=['x'], Parameter=[], Grad=1

# Mit anderer Variable
f2 = GanzrationaleFunktion("100t + 20")
# Ergebnis: Variable=['t'], Parameter=[], Grad=1
```

### Beispiel 3: Höherer Grad

```python
# Kubische Funktion
f = GanzrationaleFunktion("x^3 - 3x^2 + 2x")
# Ergebnis: Variable=['x'], Parameter=[], Grad=3

# Mit Parameter
f = GanzrationaleFunktion("a x^4 + b x^3 + c x^2 + d x + e")
# Ergebnis: Variable=['x'], Parameter=['a','b','c','d','e'], Grad=4
```

## 🎓 Pädagogischer Nutzen

1. **Intuitive Einstieg**: Schüler können natürliche mathematische Notation verwenden
2. **Fokus auf Mathematik**: Keine technischen Details zur Symbol-Verwaltung
3. **Schrittweise Komplexität**: Einfache Fälle sofort möglich, komplexe Fälle mit manueller Steuerung
4. **Fehlerfreundlich**: Klare Fehlermeldungen bei nicht ganzrationalen Ausdrücken

## 🔄 Migration bestehenden Codes

### Alte Code (funktioniert weiterhin)

```python
f = GanzrationaleFunktion([1, 2, 3])  # x^2 + 2x + 3
f = GanzrationaleFunktion("x^2 - 4")  # x^2 - 4
```

### Neue Code (mit automatischer Erkennung)

```python
f = GanzrationaleFunktion("a x^2 + b x + c")  # ax^2+bx+c
f = GanzrationaleFunktion("100t + 20")        # 100t+20
```

## 🚀 Zukunftsentwicklung

Mögliche Erweiterungen:

1. **Erweiterte Heuristiken**: Mehr Symbol-Muster für verschiedene Fachbereiche
2. **Wert-Einsetzung**: `mit_wert()`-Methode auch für GanzrationaleFunktion
3. **Mehrbuchstabige Symbole**: Unterstützung für `alpha`, `beta`, etc.
4. **Benutzerdefinierte Regeln**: Konfigurierbare Klassifizierungsregeln

## 📋 Zusammenfassung

Die automatische Symbolerkennung macht die `GanzrationaleFunktion` deutlich benutzerfreundlicher:

- **✅ Intuitive Syntax**: Mathematische Notation direkt verwendbar
- **✅ Automatische Klassifizierung**: Variable und Parameter werden intelligent erkannt
- **✅ Voll kompatibel**: Bestehender Code funktioniert unverändert
- **✅ Pädagogisch wertvoll**: Fokus auf Mathematik statt auf Technik

Die Funktion ist jetzt bereit für den Einsatz im Schulunterricht! 🎉
