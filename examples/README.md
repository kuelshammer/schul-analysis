# Schul-Analysis Framework Examples

Willkommen zur Beispielsammlung des Schul-Analysis Frameworks! Diese Beispiele demonstrieren die verschiedenen Anwendungsfälle und Funktionen des Frameworks.

## 📁 Verzeichnisstruktur

```
examples/
├── basic/                    # Grundlegende Beispiele
│   ├── getting_started.py   # Erste Schritte mit dem Framework
│   ├── gerade_parabel_analyse.py  # Analyse einer Parabel
│   └── test_precision_demo.py     # Präzisionstests
├── advanced/                 # Fortgeschrittene Analyse
│   ├── taylor_demo.py        # Taylor-Reihen
│   └── kurvendiskussion.py   # Vollständige Kurvendiskussion
├── visualization/            # Visualisierungsbeispiele
│   ├── perfekte_parabel_plotly.py   # Perfekte Parabel-Darstellung
│   ├── comprehensive_demo.py       # Umfassende Visualisierungs-Demos
│   └── *.html                  # Exportierte Visualisierungen
└── marimo_integration/       # Marimo-Notebook Integration
    └── marimo_examples.py    # Interaktive Marimo-Beispiele
```

## 🚀 Schnellstart

### 1. Grundlegende Nutzung

```python
from schul_analysis import Funktion, Nullstellen, Ableitung, Graph

# Funktion erstellen
f = Funktion("x^2 - 4x + 3")

# Analyse durchführen
print(f"Nullstellen: {Nullstellen(f)}")
print(f"Ableitung: {Ableitung(f).term()}")

# Visualisieren
graph = Graph(f)
graph.show()  # In interaktiven Umgebungen
```

### 2. Marimo-Notebook starten

```bash
# Marimo installieren (falls noch nicht geschehen)
pip install marimo

# Marimo-Notebook starten
marimo edit examples/marimo_integration/marimo_examples.py
```

## 📚 Beispielkategorien

### Basic Examples (`examples/basic/`)

- **getting_started.py**: Einführung in die grundlegenden Konzepte
- **gerade_parabel_analyse.py**: Detaillierte Analyse einer quadratischen Funktion
- **test_precision_demo.py**: Präzisionstests und numerische Genauigkeit

**Zielgruppe**: Einsteiger und Lehrkräfte

### Advanced Examples (`examples/advanced/`)

- **taylor_demo.py**: Taylor-Reihen und Approximationen
- **kurvendiskussion.py**: Vollständige Kurvendiskussion mit allen Analyseschritten

**Zielgruppe**: Fortgeschrittene Schüler und Studenten

### Visualization Examples (`examples/visualization/`)

- **perfekte_parabel_plotly.py**: Mathematisch korrekte Darstellung mit Plotly
- **comprehensive_demo.py**: Umfassende Demo aller Visualisierungsfeatures
- **HTML-Exporte**: Statische Visualisierungen zum Teilen

**Zielgruppe**: Alle, die visuelle Darstellungen benötigen

### Marimo Integration (`examples/marimo_integration/`)

- **marimo_examples.py**: Voll interaktives Notebook mit Sliders und Echtzeit-Analyse

**Zielgruppe**: Nutzer, die reaktive Interfaces bevorzugen

## 🔧 Wichtige Hinweise

### Funktionstypen

Das Framework unterstützt verschiedene Funktionstypen:

1. **Ganzrationale Funktionen** (Polynome)

   ```python
   f = Funktion("x^3 - 2x^2 + x - 1")
   ```

2. **Gebrochen-rationale Funktionen**

   ```python
   f = Funktion("(x^2 - 1)/(x - 2)")
   ```

3. **Vereinheitlichte API** (empfohlen)
   ```python
   f = Funktion("x^2 + 1")  # Ganzrational
   g = Funktion("(x^2 + 1)/(x - 1)")  # Gebrochen-rational
   ```

### Visualisierungsoptionen

Die `Graph()`-Funktion bietet viele Optionen:

```python
# Automatische Skalierung
graph = Graph(f)

# Manueller Bereich
graph = Graph(f, x_min=-5, x_max=5, y_min=-10, y_max=10)

# Mehrere Funktionen
graph = Graph(f1, f2, f3, titel="Vergleich")

# Spezielle Punkte ein/ausblenden
graph = Graph(f, zeige_nullstellen=True, zeige_extremstellen=False)
```

### Analysenfunktionen

Das Framework bietet zahlreiche Analysefunktionen:

```python
from schul_analysis import (
    Nullstellen, Ableitung, Extremstellen, Wendepunkte,
    Integral, Grenzwert, AsymptotischesVerhalten
)

# Nullstellen berechnen
nullstellen = Nullstellen(f)

# Ableitung bilden
f_strich = Ableitung(f)

# Extremstellen finden
extremstellen = Extremstellen(f)

# Wendepunkte bestimmen
wendepunkte = Wendepunkte(f)
```

## 🎓 Pädagogische Anwendung

### Für Lehrkräfte

1. **Demonstrationen**: Verwenden Sie die Beispiele im Unterricht
2. **Interaktive Aufgaben**: Nutzen Sie Marimo für Live-Demonstrationen
3. **Hausaufgaben**: Geben Sie angepasste Beispiele zur Übung

### Für Schüler

1. **Selbststudium**: Arbeiten Sie die basic-Beispiele durch
2. **Experimentieren**: Passen Sie Parameter an und beobachten Sie die Auswirkungen
3. **Vertiefung**: Nutzen Sie advanced-Beispiele für komplexe Themen

## 🔬 Technische Details

### Abhängigkeiten

- **Core**: SymPy, NumPy
- **Visualisierung**: Plotly
- **Interaktiv**: Marimo (optional)
- **Alles**: Python 3.8+

### Performance-Tipps

1. **Graph-Auflösung**: Passen Sie `punkte=` für die gewünschte Detailstufe an
2. **Bereichsgrenzen**: Engere Grenzen verbessern die Performance
3. **Mehrere Funktionen**: Kombinieren Sie bis zu 10 Funktionen in einem Graphen

## 🤝 Beiträge

Möchten Sie eigene Beispiele beitragen?

1. Erstellen Sie ein neues Beispiel im passenden Verzeichnis
2. Fügen Sie einen Docstring mit Beschreibung hinzu
3. Aktualisieren Sie diese README
4. Beachten Sie den Coding-Style des Projekts

## 📞 Support

Bei Fragen oder Problemen:

1. Prüfen Sie die [Dokumentation](../../docs/)
2. Schauen Sie sich existierende Beispiele an
3. Erstellen Sie ein Issue im GitHub-Repository

---

_Viel Erfolg mit dem Schul-Analysis Framework!_ 🎓
