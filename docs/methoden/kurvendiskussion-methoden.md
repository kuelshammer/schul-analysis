# Kurvendiskussion-Methoden für ganzrationale Funktionen

## Übersicht

Dieses Dokument beschreibt die Implementierung der Kurvendiskussion-Methoden für die Klasse `GanzratonaleFunktion`. Die Methoden ermöglichen eine vollständige Kurvendiskussion mit allen relevanten Eigenschaften.

## Methoden-Signaturen

### Berechnungsmethoden

```python
def kurvendiskussion(self) -> dict:
    """
    Führt vollständige Kurvendiskussion durch.

    Returns:
        Dictionary mit allen Ergebnissen der Kurvendiskussion
    """
```

### Lösungsweg-Methoden

```python
def kurvendiskussion_weg(self) -> str:
    """
    Generiert detaillierten Lösungsweg für Kurvendiskussion.

    Returns:
        Markdown-String mit vollständiger Schritt-für-Schritt-Erklärung
    """
```

### Interaktive Methoden

```python
def zeige_kurvendiskussion(self) -> marimo.Html:
    """
    Zeigt interaktive Kurvendiskussion in Marimo.

    Returns:
        Marimo-Objekt für interaktive Anzeige
    """
```

## Implementierungsvorschläge

### 1. kurvendiskussion() - Reine Berechnung

```python
def kurvendiskussion(self) -> dict:
    """Führt vollständige Kurvendiskussion durch"""
    ergebnisse = {
        'funktion': self.term(),
        'grad': self.grad,
        'definitionsbereich': "ℝ (alle reellen Zahlen)",
        'wertebereich': self.wertebereich(),
        'nullstellen': self.nullstellen(),
        'symmetrie': self.symmetrie(),
        'ableitungen': {},
        'extremstellen': self.extremstellen(),
        'wendepunkte': self.wendestellen(),
        'monotonie': self._analysiere_monotonie(),
        'krümmung': self._analysiere_kruemmung(),
        'verhalten_im_unendlichen': self._analysiere_verhalten_im_unendlichen(),
        'skizze_hinweise': self._generiere_skizze_hinweise()
    }

    # Ableitungen verschiedener Ordnungen
    for ordnung in range(1, min(4, self.grad + 1)):
        ergebnisse['ableitungen'][f"ordnung_{ordnung}"] = {
            'funktion': self.ableitung(ordnung).term(),
            'nullstellen': self.ableitung(ordnung).nullstellen()
        }

    return ergebnisse
```

### 2. kurvendiskussion_weg() - Detaillierter Lösungsweg

```python
def kurvendiskussion_weg(self) -> str:
    """Generiert detaillierten Lösungsweg als Markdown"""
    schritte = []

    # Schritt 1: Einleitung und Funktion
    schritte.append(self._schritt_kurvendiskussion_einleitung())

    # Schritt 2: Grundlegende Eigenschaften
    schritte.append(self._schritt_grundlegende_eigenschaften())

    # Schritt 3: Definitionsbereich
    schritte.append(self._schritt_definitionsbereich())

    # Schritt 4: Wertebereich
    schritte.append(self._schritt_wertebereich())

    # Schritt 5: Symmetrie
    schritte.append(self._schritt_symmetrie())

    # Schritt 6: Nullstellen
    schritte.append(self._schritt_nullstellen_kurvendiskussion())

    # Schritt 7: Ableitungen
    schritte.append(self._schritt_ableitungen_kurvendiskussion())

    # Schritt 8: Extremstellen
    schritte.append(self._schritt_extremstellen_kurvendiskussion())

    # Schritt 9: Monotonie
    schritte.append(self._schritt_monotonie())

    # Schritt 10: Wendepunkte und Krümmung
    schritte.append(self._schritt_wendepunkte())

    # Schritt 11: Verhalten im Unendlichen
    schritte.append(self._schritt_verhalten_im_unendlichen())

    # Schritt 12: Zusammenfassung und Skizze
    schritte.append(self._schritt_zusammenfassung_skizze())

    return "\n\n".join(schritte)
```

**Unterstützende Methoden:**

```python
def _schritt_kurvendiskussion_einleitung(self) -> str:
    """Schritt 1: Einleitung"""
    return f"# Kurvendiskussion für f(x) = {self.term()}\n\nIn diesem Dokument führen wir eine vollständige Kurvendiskussion durch."

def _schritt_grundlegende_eigenschaften(self) -> str:
    """Schritt 2: Grundlegende Eigenschaften"""
    return f"## Grundlegende Eigenschaften\n\n- **Funktionstyp**: Ganzrationale Funktion\n- **Grad**: {self.grad}\n- **Leitkoeffizient**: {self.koeffizienten[0]}"

def _schritt_definitionsbereich(self) -> str:
    """Schritt 3: Definitionsbereich"""
    return "## Definitionsbereich\n\nPolynomfunktionen sind auf ganz ℝ definiert.\n\n**Definitionsbereich**: D = ℝ"

def _schritt_wertebereich(self) -> str:
    """Schritt 4: Wertebereich"""
    min_wert, max_wert = self.wertebereich()

    if min_wert is None and max_wert is None:
        wertebereich = "ℝ (alle reellen Zahlen)"
    elif min_wert is None:
        wertebereich = f"(-∞, {max_wert}]"
    elif max_wert is None:
        wertebereich = f"[{min_wert}, ∞)"
    else:
        wertebereich = f"[{min_wert}, {max_wert}]"

    return f"## Wertebereich\n\n**Wertebereich**: W = {wertebereich}"

def _schritt_symmetrie(self) -> str:
    """Schritt 5: Symmetrie"""
    symmetrie = self.symmetrie()

    if symmetrie == "gerade":
        return "## Symmetrie\n\n**Achsensymmetrie zur y-Achse**\n\nf(-x) = f(x) für alle x ∈ ℝ"
    elif symmetrie == "ungerade":
        return "## Symmetrie\n\n**Punktsymmetrie zum Ursprung**\n\nf(-x) = -f(x) für alle x ∈ ℝ"
    else:
        return "## Symmetrie\n\n**Keine Symmetrie**\n\nDie Funktion ist weder achsen- noch punktsymmetrisch."

def _schritt_nullstellen_kurvendiskussion(self) -> str:
    """Schritt 6: Nullstellen"""
    nullstellen = self.nullstellen()

    if not nullstellen:
        return "## Nullstellen\n\n**Keine Nullstellen**\n\nDie Funktion schneidet die x-Achse nicht."

    schritte = ["## Nullstellen\n\n**Schnittpunkte mit der x-Achse**:"]

    for i, x in enumerate(nullstellen, 1):
        y = self.wert(x)
        schritte.append(f"- N{i}({x:.4f}|0)")

    return "\n".join(schritte)

def _schritt_ableitungen_kurvendiskussion(self) -> str:
    """Schritt 7: Ableitungen"""
    schritte = ["## Ableitungen\n\n"]

    for ordnung in range(1, min(4, self.grad + 1)):
        ableitung = self.ableitung(ordnung)
        if ordnung == 1:
            symbol = "f'"
        elif ordnung == 2:
            symbol = "f''"
        else:
            symbol = f"f^{ordnung}"

        schritte.append(f"**{symbol}(x) = {ableitung.term()}**")

        # Nullstellen der Ableitung
        nullstellen = ableitung.nullstellen()
        if nullstellen:
            schritte.append(f"- Nullstellen: {nullstellen}")
        schritte.append("")

    return "\n".join(schritte)

def _schritt_extremstellen_kurvendiskussion(self) -> str:
    """Schritt 8: Extremstellen"""
    extremstellen = self.extremstellen()

    if not extremstellen:
        return "## Extremstellen\n\n**Keine Extremstellen**"

    schritte = ["## Extremstellen\n\n**Lokale Maxima und Minima**:"]

    for i, (x, art) in enumerate(extremstellen, 1):
        y = self.wert(x)
        schritte.append(f"- {art} bei E{i}({x:.4f}|{y:.4f})")

    return "\n".join(schritte)

def _schritt_monotonie(self) -> str:
    """Schritt 9: Monotonie"""
    monotonie = self._analysiere_monotonie()

    schritte = ["## Monotonie\n\n**Intervalle, auf denen die Funktion monoton ist**:\n"]

    for intervall, eigenschaft in monotonie.items():
        schritte.append(f"- **{intervall}**: {eigenschaft}")

    return "\n".join(schritte)

def _schritt_wendepunkte(self) -> str:
    """Schritt 10: Wendepunkte"""
    wendepunkte = self.wendestellen()

    if not wendepunkte:
        return "## Wendepunkte\n\n**Keine Wendepunkte**"

    schritte = ["## Wendepunkte und Krümmung\n\n**Wendepunkte**:\n"]

    for i, x in enumerate(wendepunkte, 1):
        y = self.wert(x)
        dritte_ableitung = self.ableitung(3)
        if dritte_ableitung.wert(x) != 0:
            schritte.append(f"- W{i}({x:.4f}|{y:.4f})")
        else:
            schritte.append(f"- W{i}({x:.4f}|{y:.4f}) [kein einfacher Wendepunkt]")

    # Krümmungsanalyse
    kruemmung = self._analysiere_kruemmung()
    schritte.append("\n**Krümmung**:\n")

    for intervall, eigenschaft in kruemmung.items():
        schritte.append(f"- **{intervall}**: {eigenschaft}")

    return "\n".join(schritte)

def _schritt_verhalten_im_unendlichen(self) -> str:
    """Schritt 11: Verhalten im Unendlichen"""
    verhalten = self._analysiere_verhalten_im_unendlichen()

    schritte = ["## Verhalten im Unendlichen\n\n"]

    for richtung, beschreibung in verhalten.items():
        schritte.append(f"**{richtung}**: {beschreibung}")

    return "\n".join(schritte)

def _schritt_zusammenfassung_skizze(self) -> str:
    """Schritt 12: Zusammenfassung"""
    return "## Zusammenfassung und Skizze\n\n**Zusammenfassung der wichtigsten Eigenschaften:**\n\n- Alle berechneten Eigenschaften zusammenfassen\n- Hinweise für das Zeichnen des Graphen\n- Charakteristische Merkmale hervorheben"
```

### 3. zeige_kurvendiskussion() - Interaktive Marimo-Anzeige

```python
def zeige_kurvendiskussion(self) -> marimo.Html:
    """Zeigt interaktive Kurvendiskussion in Marimo"""
    import marimo as mo

    # Berechnung durchführen
    ergebnisse = self.kurvendiskussion()
    weg = self.kurvendiskussion_weg()

    # Hauptgraph erstellen
    graph = self._erstelle_kurvendiskussions_graph(ergebnisse)

    # Zusammenfassende Tabelle
    tabelle_daten = [
        ["Eigenschaft", "Wert"],
        ["Grad", str(ergebnisse['grad'])],
        ["Definitionsbereich", ergebnisse['definitionsbereich']],
        ["Wertebereich", str(ergebnisse['wertebereich'])],
        ["Symmetrie", ergebnisse['symmetrie']],
        ["Anzahl Nullstellen", str(len(ergebnisse['nullstellen']))],
        ["Anzahl Extremstellen", str(len(ergebnisse['extremstellen']))],
        ["Anzahl Wendepunkte", str(len(ergebnisse['wendepunkte']))]
    ]

    tabelle = mo.ui.table(tabelle_daten, label="Zusammenfassung")

    # Ausgabe zusammenstellen
    output = mo.md(f"""
# Kurvendiskussion: f(x) = {self.term()}

## Grafische Darstellung

{graph}

## Zusammenfassung

{tabelle}

## Vollständiger Lösungsweg

{mo.md(weg)}

### Interaktive Elemente

{mo.ui.tabs([
    mo.ui.tab("Graph", graph),
    mo.ui.tab("Eigenschaften", tabelle),
    mo.ui.tab("Lösungsweg", mo.md(weg))
])}

{mo.ui.button(label="Export als PDF")}
{mo.ui.button(label="Neues Beispiel")}
""")

    return output
```

## Spezielle Analysen

### Monotonieanalyse
```python
def _analysiere_monotonie(self) -> dict:
    """Analysiert die Monotonieintervalle"""
    if self.grad < 1:
        return {"ℝ": "konstant"}

    f_prime = self.ableitung(1)
    kritische_punkte = f_prime.nullstellen()

    # Kritische Punkte sortieren und Intervalle bilden
    punkte = sorted(kritische_punkte)
    if not punkte:
        # Keine kritischen Punkte, prüfe Vorzeichen von f'
        test_wert = f_prime.wert(0)
        if test_wert > 0:
            return {"ℝ": "streng monoton wachsend"}
        elif test_wert < 0:
            return {"ℝ": "streng monoton fallend"}
        else:
            return {"ℝ": "konstant"}

    # Intervalle analysieren
    monotonie = {}
    punkte = [-float('inf')] + punkte + [float('inf')]

    for i in range(len(punkte) - 1):
        links, rechts = punkte[i], punkte[i + 1]
        if links == -float('inf') and rechts == float('inf'):
            intervall = "ℝ"
        elif links == -float('inf'):
            intervall = f"(-∞, {rechts:.4f})"
        elif rechts == float('inf'):
            intervall = f"({links:.4f}, ∞)"
        else:
            intervall = f"({links:.4f}, {rechts:.4f})"

        # Testpunkt im Intervall
        testpunkt = (links + rechts) / 2
        if links == -float('inf'):
            testpunkt = rechts - 1
        elif rechts == float('inf'):
            testpunkt = links + 1

        wert = f_prime.wert(testpunkt)
        if wert > 0:
            monotonie[intervall] = "streng monoton wachsend"
        elif wert < 0:
            monotonie[intervall] = "streng monoton fallend"
        else:
            monotonie[intervall] = "konstant"

    return monotonie
```

### Krümmungsanalyse
```python
def _analysiere_kruemmung(self) -> dict:
    """Analysiert die Krümmungsintervalle"""
    if self.grad < 2:
        return {"ℝ": "keine Krümmung (lineare Funktion)"}

    f_double_prime = self.ableitung(2)
    wendepunkte = f_double_prime.nullstellen()

    # Ähnlich wie Monotonieanalyse
    punkte = sorted(wendepunkte)
    if not punkte:
        test_wert = f_double_prime.wert(0)
        if test_wert > 0:
            return {"ℝ": "rechtsgekrümmt (konvex)"}
        elif test_wert < 0:
            return {"ℝ": "linksgekrümmt (konkav)"}
        else:
            return {"ℝ": "keine Krümmung"}

    # Intervalle mit Krümmungsanalyse
    kruemmung = {}
    punkte = [-float('inf')] + punkte + [float('inf')]

    for i in range(len(punkte) - 1):
        links, rechts = punkte[i], punkte[i + 1]
        if links == -float('inf') and rechts == float('inf'):
            intervall = "ℝ"
        elif links == -float('inf'):
            intervall = f"(-∞, {rechts:.4f})"
        elif rechts == float('inf'):
            intervall = f"({links:.4f}, ∞)"
        else:
            intervall = f"({links:.4f}, {rechts:.4f})"

        # Testpunkt im Intervall
        testpunkt = (links + rechts) / 2
        if links == -float('inf'):
            testpunkt = rechts - 1
        elif rechts == float('inf'):
            testpunkt = links + 1

        wert = f_double_prime.wert(testpunkt)
        if wert > 0:
            kruemmung[intervall] = "rechtsgekrümmt (konvex)"
        elif wert < 0:
            kruemmung[intervall] = "linksgekrümmt (konkav)"
        else:
            kruemmung[intervall] = "Wendepunkt"

    return kruemmung
```

## Fehlerbehandlung

```python
class KurvendiskussionFehler(MathematischeFunktionError):
    """Fehler bei der Kurvendiskussion"""
    pass

class UnbekannteEigenschaftFehler(KurvendiskussionFehler):
    """Fehler bei unbekannter Funktionseigenschaft"""
    pass
```

## Didaktische Aspekte

### Strukturierter Aufbau
1. **Grundlegende Eigenschaften**: Was ist das für eine Funktion?
2. **Definitionsbereich**: Wo ist die Funktion definiert?
3. **Wertebereich**: Welche Werte kann die Funktion annehmen?
4. **Symmetrie**: Gibt es Symmetrieeigenschaften?
5. **Nullstellen**: Wo schneidet die Funktion die x-Achse?
6. **Ableitungen**: Wie ändert sich die Funktion?
7. **Extremstellen**: Wo hat die Funktion Maxima/Minima?
8. **Monotonie**: Wächst/fällt die Funktion?
9. **Krümmung**: Wie ist die Krümmung?
10. **Verhalten im Unendlichen**: Was passiert bei ±∞?

### Visualisierung
- Schrittweise Aufbau des Graphen
- Markierung aller wichtiger Punkte
- Interaktive Exploration
- Vergleich von mehreren Funktionen

### Progressive Komplexität
- **Einfache Funktionen**: Linear, quadratisch
- **Mittlere Komplexität**: Kubisch, quartisch
- **Hohe Komplexität**: Polynome höheren Grades
- **Spezialfälle**: Symmetrische Funktionen, spezielle Nullstellen

## Testbeispiele

### Beispiel 1: Quadratische Funktion
```python
f = GanzrationaleFunktion([1, -4, 3])  # f(x) = x² - 4x + 3
diskussion = f.kurvendiskussion()
```

### Beispiel 2: Kubische Funktion
```python
f = GanzrationaleFunktion([1, -3, 0, 2])  # f(x) = x³ - 3x + 2
diskussion = f.kurvendiskussion()
```

### Beispiel 3: Funktion mit Symmetrie
```python
f = GanzrationaleFunktion([1, 0, -4])  # f(x) = x² - 4 (gerade)
diskussion = f.kurvendiskussion()
```

## Weiterentwicklung

### Mögliche Erweiterungen
- **Automatische Berichterstellung** im PDF-Format
- **Vergleichsanalyse** mehrerer Funktionen
- **Optimierungsalgorithmen** für praktische Anwendungen
- **Export-Funktionen** für verschiedene Formate

### Integration mit anderen Methoden
- **Parameterstudien**: Wie ändern sich die Eigenschaften bei Parameteränderung?
- **Funktionsfitting**: Anpassung an Datenpunkte
- **Numerische Methoden** für nicht-exakte Lösungen
