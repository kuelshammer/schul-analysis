# Extremstellen-Methoden für ganzrationale Funktionen

## Übersicht

Dieses Dokument beschreibt die Implementierung der Extremstellen-Methoden für die Klasse `GanzrationaleFunktion`. Die Methoden ermöglichen die Berechnung von Extremstellen (Maxima und Minima) mit detaillierten Lösungswegen.

## Methoden-Signaturen

### Berechnungsmethoden

```python
def extremstellen(self) -> List[Tuple[float, str]]:
    """
    Berechnet alle Extremstellen der Funktion.

    Returns:
        Liste von Tupeln (x_koordinate, art) wobei art 'Maximum' oder 'Minimum' ist
    """
```

### Lösungsweg-Methoden

```python
def extremstellen_weg(self) -> str:
    """
    Generiert detaillierten Lösungsweg für Extremstellenberechnung.

    Returns:
        Markdown-String mit Schritt-für-Schritt-Erklärung
    """
```

### Interaktive Methoden

```python
def zeige_extremstellen(self) -> marimo.Html:
    """
    Zeigt interaktive Extremstellenberechnung in Marimo.

    Returns:
        Marimo-Objekt für interaktive Anzeige
    """
```

## Implementierungsvorschläge

### 1. extremstellen() - Reine Berechnung

```python
def extremstellen(self) -> List[Tuple[float, str]]:
    """Berechnet alle Extremstellen"""
    if self.grad < 2:
        return []  # Keine Extremstellen bei Grad < 2

    # Erste Ableitung berechnen
    f_prime = self.ableitung(1)

    # Nullstellen der ersten Ableitung finden
    kritische_punkte = f_prime.nullstellen()

    extremstellen = []

    # Zweite Ableitung für die Artbestimmung
    f_double_prime = self.ableitung(2)

    for x in kritische_punkte:
        # Wert der zweiten Ableitung an dieser Stelle
        wert = f_double_prime.wert(x)

        if wert < 0:
            art = "Maximum"
        elif wert > 0:
            art = "Minimum"
        else:
            # Bei f''(x) = 0: Vorzeichenwechsel der ersten Ableitung prüfen
            art = self._bestimme_art_durch_vorzeichenwechsel(f_prime, x)

        extremstellen.append((x, art))

    return extremstellen

def _bestimme_art_durch_vorzeichenwechsel(self, f_prime: 'GanzrationaleFunktion', x: float) -> str:
    """Bestimmt die Art durch Vorzeichenwechsel der ersten Ableitung"""
    epsilon = 1e-6
    links = f_prime.wert(x - epsilon)
    rechts = f_prime.wert(x + epsilon)

    if links > 0 and rechts < 0:
        return "Maximum"
    elif links < 0 and rechts > 0:
        return "Minimum"
    else:
        return "Sattelpunkt"
```

### 2. extremstellen_weg() - Detaillierter Lösungsweg

```python
def extremstellen_weg(self) -> str:
    """Generiert detaillierten Lösungsweg als Markdown"""
    schritte = []

    # Schritt 1: Funktion und Problemstellung
    schritte.append(self._schritt_extremstellen_einleitung())

    # Schritt 2: Voraussetzungen prüfen
    if self.grad < 2:
        schritte.append("### Schritt 1: Voraussetzungen prüfen")
        schritte.append(f"Die Funktion f(x) = {self.term()} hat Grad {self.grad} < 2.")
        schritte.append("Daher gibt es keine Extremstellen.")
        return "\n\n".join(schritte)

    # Schritt 3: Erste Ableitung berechnen
    schritte.append(self._schritt_erste_ableitung())

    # Schritt 4: Nullstellen der ersten Ableitung
    schritte.append(self._schritt_nullstellen_erster_ableitung())

    # Schritt 5: Art der Extremstellen bestimmen
    schritte.append(self._schritt_art_bestimmung())

    # Schritt 6: Zusammenfassung
    schritte.append(self._schritt_extremstellen_zusammenfassung())

    return "\n\n".join(schritte)
```

**Unterstützende Methoden:**

```python
def _schritt_extremstellen_einleitung(self) -> str:
    """Schritt 1: Einleitung"""
    return f"## Extremstellenberechnung für f(x) = {self.term()}\n\nGesucht: Alle lokalen Maxima und Minima"

def _schritt_erste_ableitung(self) -> str:
    """Schritt: Erste Ableitung berechnen"""
    f_prime = self.ableitung(1)
    return f"### Schritt 2: Erste Ableitung bilden\n\nf'(x) = {f_prime.term()}"

def _schritt_nullstellen_erster_ableitung(self) -> str:
    """Schritt: Nullstellen der ersten Ableitung"""
    f_prime = self.ableitung(1)
    kritische_punkte = f_prime.nullstellen()

    if not kritische_punkte:
        return "### Schritt 3: Kritische Punkte finden\n\nf'(x) = 0 hat keine Lösungen.\nDaher gibt es keine Extremstellen."

    schritte = [f"### Schritt 3: Kritische Punkte finden\n\nf'(x) = 0 lösen:"]

    for i, x in enumerate(kritische_punkte, 1):
        schritte.append(f"- x_{i} = {x:.4f}")

    schritte.append(f"\nKritische Punkte: {kritische_punkte}")
    return "\n".join(schritte)

def _schritt_art_bestimmung(self) -> str:
    """Schritt: Art der Extremstellen bestimmen"""
    f_prime = self.ableitung(1)
    f_double_prime = self.ableitung(2)
    kritische_punkte = f_prime.nullstellen()

    schritte = ["### Schritt 4: Art der Extremstellen bestimmen\n\n"]

    if f_double_prime.grad > 0:
        schritte.append("**Methode: Zweite Ableitung**")
        schritte.append(f"f''(x) = {f_double_prime.term()}")
        schritte.append("")

        for i, x in enumerate(kritische_punkte, 1):
            wert = f_double_prime.wert(x)
            if wert < 0:
                art = "Maximum"
            elif wert > 0:
                art = "Minimum"
            else:
                art = self._bestimme_art_durch_vorzeichenwechsel(f_prime, x)

            schritte.append(f"- Bei x = {x:.4f}: f''({x:.4f}) = {wert:.4f} → {art}")
    else:
        schritte.append("**Methode: Vorzeichenwechsel der ersten Ableitung**")
        for i, x in enumerate(kritische_punkte, 1):
            art = self._bestimme_art_durch_vorzeichenwechsel(f_prime, x)
            schritte.append(f"- Bei x = {x:.4f}: {art}")

    return "\n".join(schritte)

def _schritt_extremstellen_zusammenfassung(self) -> str:
    """Schritt: Zusammenfassung"""
    extremstellen = self.extremstellen()

    if not extremstellen:
        return "### Ergebnis\n\nDie Funktion hat keine Extremstellen."

    schritte = ["### Ergebnis\n\nGefundene Extremstellen:"]

    for i, (x, art) in enumerate(extremstellen, 1):
        y_wert = self.wert(x)
        schritte.append(f"- {art} bei P({x:.4f}|{y_wert:.4f})")

    return "\n".join(schritte)
```

### 3. zeige_extremstellen() - Interaktive Marimo-Anzeige

```python
def zeige_extremstellen(self) -> marimo.Html:
    """Zeigt interaktive Extremstellenberechnung in Marimo"""
    import marimo as mo

    # Berechnung durchführen
    extremstellen = self.extremstellen()
    weg = self.extremstellen_weg()

    # Visualisierung erstellen
    graph = self._erstelle_extremstellen_graph(extremstellen)

    # Tabelle mit Extremstellen
    if extremstellen:
        table_data = []
        for x, art in extremstellen:
            y = self.wert(x)
            table_data.append([f"{x:.4f}", f"{y:.4f}", art])

        table = mo.ui.table(
            data=table_data,
            columns=["x-Koordinate", "y-Koordinate", "Art"],
            label="Extremstellen"
        )
    else:
        table = mo.md("Keine Extremstellen gefunden")

    # Ausgabe zusammenstellen
    output = mo.md(f"""
# Extremstellenberechnung

## Funktion: f(x) = {self.term()}

### Grafische Darstellung

{graph}

### Extremstellen

{table}

### Lösungsweg

{mo.md(weg)}

### Interaktive Elemente

{mo.ui.checkbox(label="Zeige Tangenten")}
{mo.ui.checkbox(label="Zeige Ableitungen")}
{mo.ui.button(label="Neues Beispiel")}
""")

    return output
```

## Spezielle Lösungsstrategien

### Quadratische Funktionen (Grad 2)
- Immer genau einen Extrempunkt (Scheitelpunkt)
- Einfache Bestimmung durch f'(x) = 0
- Direkte Artbestimmung durch f''(x)

### Kubische Funktionen (Grad 3)
- Höchstens zwei Extremstellen
- Mögliche Sattelpunkte
- Komplexere Analyse nötig

### Funktionen höheren Grades
- Mehrere Extremstellen möglich
- Kombination verschiedener Methoden
- Numerische Stabilität beachten

## Fehlerbehandlung

```python
class ExtremstellenBerechnungFehler(MathematischeFunktionError):
    """Fehler bei der Extremstellenberechnung"""
    pass

class KeineExtremstellenFehler(ExtremstellenBerechnungFehler):
    """Fehler: Keine Extremstellen vorhanden"""
    pass
```

## Didaktische Aspekte

### Progressive Einführung
1. **Quadratische Funktionen**: Einfacher Fall mit genau einem Extrempunkt
2. **Kubische Funktionen**: Zwei Extremstellen, Sattelpunkte
3. **Höhere Polynome**: Komplexe Situationen mit mehreren Extremstellen
4. **Anwendungen**: Optimierungsprobleme, Kurvendiskussion

### Visualisierung
- Funktion mit markierten Extremstellen
- Tangenten an den Extremstellen
- Erste und zweite Ableitung im Vergleich
- Interaktive Exploration

### Selbstkontrolle
- Schüler können Extremstellen überprüfen
- Verständnis der Kriterien (f'(x) = 0, f''(x) ≠ 0)
- Fehleranalyse bei falschen Ergebnissen

## Testbeispiele

### Beispiel 1: Quadratische Funktion
```python
f = GanzrationaleFunktion([1, -4, 3])  # f(x) = x² - 4x + 3
f.extremstellen()  # [(2.0, "Minimum")]
```

### Beispiel 2: Kubische Funktion
```python
f = GanzrationaleFunktion([1, 0, -3, 1])  # f(x) = x³ - 3x + 1
f.extremstellen()  # [(-1.0, "Maximum"), (1.0, "Minimum")]
```

### Beispiel 3: Funktion ohne Extremstellen
```python
f = GanzrationaleFunktion([1, 2])  # f(x) = x + 2
f.extremstellen()  # [] (keine Extremstellen)
```

### Beispiel 4: Funktion mit Sattelpunkt
```python
f = GanzrationaleFunktion([1, 0, 0, 0])  # f(x) = x³
f.extremstellen()  # [(0.0, "Sattelpunkt")]
```

## Weiterentwicklung

### Mögliche Erweiterungen
- **Globale Extremstellen** auf gegebenem Intervall
- **Randextrema** bei beschränkten Definitionsbereichen
- **Numerische Optimierung** für komplexe Funktionen
- **Mehrdimensionale Extremstellen**

### Performance-Optimierung
- Effiziente Nullstellenberechnung für hohe Grade
- Caching von Ableitungen
- Parallele Berechnung bei vielen kritischen Punkten

### Integration mit anderen Methoden
- **Kurvendiskussion**: Zusammenfassende Analyse
- **Optimierungsprobleme**: Anwendungen in der Praxis
- **Wendepunkte**: Zusammenhang mit Krümmung
