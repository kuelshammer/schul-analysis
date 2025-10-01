# Ableitungs-Methoden für ganzrationale Funktionen

## Übersicht

Dieses Dokument beschreibt die Implementierung der Ableitungs-Methoden für die Klasse `GanzrationaleFunktion`. Die Methoden ermöglichen die Berechnung von Ableitungen beliebiger Ordnung mit detaillierten Lösungswegen.

## Methoden-Signaturen

### Berechnungsmethoden

```python
def ableitung(self, ordnung: int = 1) -> 'GanzrationaleFunktion':
    """
    Berechnet die Ableitung gegebener Ordnung.

    Args:
        ordnung: Ordnung der Ableitung (Standard: 1)

    Returns:
        Neue GanzrationaleFunktion als Ableitung
    """
```

### Lösungsweg-Methoden

```python
def ableitung_weg(self, ordnung: int = 1) -> str:
    """
    Generiert detaillierten Lösungsweg für Ableitungsberechnung.

    Args:
        ordnung: Ordnung der Ableitung

    Returns:
        Markdown-String mit Schritt-für-Schritt-Erklärung
    """
```

### Interaktive Methoden

```python
def zeige_ableitung(self, ordnung: int = 1) -> marimo.Html:
    """
    Zeigt interaktive Ableitungsberechnung in Marimo.

    Args:
        ordnung: Ordnung der Ableitung

    Returns:
        Marimo-Objekt für interaktive Anzeige
    """
```

## Implementierungsvorschläge

### 1. ableitung() - Reine Berechnung

```python
def ableitung(self, ordnung: int = 1) -> 'GanzrationaleFunktion':
    """Berechnet die Ableitung gegebener Ordnung"""
    if ordnung <= 0:
        raise ValueError(f"Ordnung muss positiv sein, war: {ordnung}")

    if ordnung > self.grad:
        # Ableitung höheren Grades ist Nullfunktion
        return GanzrationaleFunktion([0])

    # Koeffizienten für Ableitung berechnen
    ableitung_koeffizienten = []
    for i, k in enumerate(self.koeffizienten[:-ordnung]):
        # Für Koeffizient a_i bei x^i wird a_i * (i + ordnung) bei x^(i)
        neuer_koeffizient = k * (i + ordnung)
        ableitung_koeffizienten.append(neuer_koeffizient)

    return GanzrationaleFunktion(ableitung_koeffizienten)
```

**Alternative Implementierung mit SymPy:**

```python
def ableitung(self, ordnung: int = 1) -> 'GanzrationaleFunktion':
    """Berechnet Ableitung mit SymPy"""
    if ordnung <= 0:
        raise ValueError(f"Ordnung muss positiv sein, war: {ordnung}")

    # Ableitung mit SymPy berechnen
    x = sympy.Symbol('x')
    term = sum(k * x**i for i, k in enumerate(reversed(self.koeffizienten)))
    abgeleiteter_term = term.diff(x, ordnung)

    # Zurück in Koeffizienten umwandeln
    abgeleitetes_poly = sympy.Poly(abgeleiteter_term, x)
    koeffizienten = [float(coef) for coef in reversed(abgeleitetes_poly.all_coeffs())]

    return GanzrationaleFunktion(koeffizienten)
```

### 2. ableitung_weg() - Detaillierter Lösungsweg

```python
def ableitung_weg(self, ordnung: int = 1) -> str:
    """Generiert detaillierten Lösungsweg als Markdown"""
    schritte = []

    # Schritt 1: Funktion und Aufgabe darstellen
    schritte.append(self._schritt_ableitung_darstellen(ordnung))

    # Schritt 2: Regeln anwenden
    if ordnung == 1:
        schritte.append(self._schritt_erste_ableitung())
    else:
        schritte.append(self._schritt_hoehere_ableitung(ordnung))

    # Schritt 3: Vereinfachung
    schritte.append(self._schritt_vereinfachung(ordnung))

    # Schritt 4: Ergebnis
    schritte.append(self._schritt_ableitung_ergebnis(ordnung))

    return "\n\n".join(schritte)
```

**Unterstützende Methoden:**

```python
def _schritt_ableitung_darstellen(self, ordnung: int) -> str:
    """Schritt 1: Funktion und Aufgabe darstellen"""
    ableitung_symbol = "f'" if ordnung == 1 else f"f^{ordnung}"
    return f"## {ordnung}. Ableitung von f(x) = {self.term()}\n\nGesucht: {ableitung_symbol}(x)"

def _schritt_erste_ableitung(self) -> str:
    """Schritt für erste Ableitung"""
    schritte = [
        "### Schritt 1: Ableitungsregeln anwenden",
        "",
        "**Potenzregel:** Für ax^n gilt (ax^n)' = a·n·x^(n-1)",
        "",
        "Anwendung auf jeden Summanden:"
    ]

    # Jeden Summanden ableiten
    for i, k in enumerate(reversed(self.koeffizienten)):
        if k != 0 and i > 0:  # Konstanten weglassen
            potenz = i
            if potenz == 1:
                abgeleitet = k
            else:
                abgeleitet = k * potenz
                neuer_potenz = potenz - 1
                if neuer_potenz == 1:
                    term = f"{abgeleitet}x"
                else:
                    term = f"{abgeleitet}x^{neuer_potenz}"
            else:
                if potenz == 1:
                    term = f"{k}x"
                else:
                    term = f"{k}x^{potenz}"

            schritte.append(f"- ({term})' = {abgeleitet}x^{neuer_potenz}" if neuer_potenz > 0 else f"- ({term})' = {abgeleitet}")

    return "\n".join(schritte)

def _schritt_hoehere_ableitung(self, ordnung: int) -> str:
    """Schritt für höhere Ableitungen"""
    schritte = [
        f"### Schritt 1: {ordnung}. Ableitung berechnen",
        "",
        f"Für die {ordnung}. Ableitung wenden wir die Potenzregel {ordnung}-mal an:",
        ""
    ]

    # Zeige den Prozess der schrittweisen Ableitung
    aktuelle_funktion = self
    for i in range(1, ordnung + 1):
        naechste_funktion = aktuelle_funktion.ableitung(1)
        if i == 1:
            symbol = "f'"
        elif i == 2:
            symbol = "f''"
        else:
            symbol = f"f^{i}"

        schritte.append(f"{symbol}(x) = {naechste_funktion.term()}")
        aktuelle_funktion = naechste_funktion

    return "\n".join(schritte)

def _schritt_vereinfachung(self, ordnung: int) -> str:
    """Schritt: Vereinfachung des Ergebnisses"""
    ableitung = self.ableitung(ordnung)
    return f"### Schritt {3 if ordnung == 1 else 3}: Vereinfachung\n\nf'{ableitung} = {ableitung.term()}"

def _schritt_ableitung_ergebnis(self, ordnung: int) -> str:
    """Schritt: Endergebnis"""
    ableitung = self.ableitung(ordnung)
    ableitung_symbol = "f'" if ordnung == 1 else f"f^{ordnung}"
    return f"### Ergebnis\n\n{ableitung_symbol}(x) = {ableitung.term()}"
```

### 3. zeige_ableitung() - Interaktive Marimo-Anzeige

```python
def zeige_ableitung(self, ordnung: int = 1) -> marimo.Html:
    """Zeigt interaktive Ableitungsberechnung in Marimo"""
    import marimo as mo

    # Berechnung durchführen
    ableitung = self.ableitung(ordnung)
    weg = self.ableitung_weg(ordnung)

    # Visualisierungen erstellen
    original_graph = self._erstelle_funktionsgraph()
    ableitungs_graph = ableitung._erstelle_funktionsgraph()

    # Ausgabe zusammenstellen
    output = mo.md(f"""
# Ableitungsberechnung

## Funktion: f(x) = {self.term()}
## {ordnung}. Ableitung: f'{"'" * (ordnung-1)}(x) = {ableitung.term()}

### Grafischer Vergleich

{mo.hstack([original_graph, ableitungs_graph])}

### Lösungsweg

{mo.md(weg)}

### Interaktive Elemente

{mo.ui.slider(1, min(5, self.grad), label="Ableitungsordnung")}
{mo.ui.checkbox(label="Zeige Regeln")}
{mo.ui.button(label="Neues Beispiel")}
""")

    return output
```

## Spezielle Fähigkeiten

### Ableitungsregeln implementieren
- **Potenzregel**: (x^n)' = n·x^(n-1)
- **Faktorregel**: (a·f(x))' = a·f'(x)
- **Summenregel**: (f(x) + g(x))' = f'(x) + g'(x)
- **Konstantenregel**: c' = 0

### Höhere Ableitungen
- Rekursive Berechnung
- Effiziente Implementierung
- Spezielle Notation (f', f'', f''', f⁴, ...)

### Spezialfälle
- **Konstante Funktionen**: Ableitung ist 0
- **Lineare Funktionen**: Ableitung ist konstant
- **Polynome mit hohem Grad**: Optimierungsmöglichkeiten

## Fehlerbehandlung

```python
class AbleitungsBerechnungFehler(MathematischeFunktionError):
    """Fehler bei der Ableitungsberechnung"""
    pass

class UngueltigeOrdnungFehler(AbleitungsBerechnungFehler):
    """Fehler bei ungültiger Ableitungsordnung"""
    pass
```

## Didaktische Aspekte

### Progressive Einführung
1. **Einfache Polynome**: Konstante, lineare, quadratische Funktionen
2. **Komplexe Polynome**: Höhere Grade, mehrere Summanden
3. **Höhere Ableitungen**: Zweite, dritte, vierte Ableitung
4. **Anwendungen**: Extremstellen, Wendepunkte, Kurvendiskussion

### Visualisierung
- Ursprüngliche Funktion und Ableitung im Vergleich
- Tangenten an ausgewählten Punkten
- Dynamische Darstellung mit veränderlichen Parametern

### Selbstkontrolle
- Schüler können Ableitungen überprüfen
- Schritt-für-Schritt-Vergleich möglich
- Automatische Fehlererkennung

## Testbeispiele

### Beispiel 1: Konstante Funktion
```python
f = GanzrationaleFunktion([5])  # f(x) = 5
f.ableitung()  # f'(x) = 0
```

### Beispiel 2: Lineare Funktion
```python
f = GanzrationaleFunktion([2, 3])  # f(x) = 2x + 3
f.ableitung()  # f'(x) = 2
```

### Beispiel 3: Quadratische Funktion
```python
f = GanzrationaleFunktion([1, -4, 3])  # f(x) = x² - 4x + 3
f.ableitung()  # f'(x) = 2x - 4
f.ableitung(2)  # f''(x) = 2
```

### Beispiel 4: Kubische Funktion
```python
f = GanzrationaleFunktion([1, 0, -3, 2])  # f(x) = x³ - 3x + 2
f.ableitung()  # f'(x) = 3x² - 3
f.ableitung(2)  # f''(x) = 6x
f.ableitung(3)  # f'''(x) = 6
```

## Weiterentwicklung

### Mögliche Erweiterungen
- **Partielle Ableitungen** für mehrdimensionale Funktionen
- **Implizite Ableitung** für implizit definierte Funktionen
- **Numerische Ableitung** als Näherungsverfahren
- **Ableitungsregeln** für spezielle Funktionen (Kettenregel, Produktregel)

### Performance-Optimierung
- Caching von Ableitungen
- Symbolische Vereinfachung mit SymPy
- Parallelisierung für komplexe Berechnungen

### Integration mit anderen Methoden
- **Extremstellenberechnung**: f'(x) = 0
- **Wendepunktberechnung**: f''(x) = 0
- **Kurvendiskussion**: Zusammenfassende Analyse
