# 🔢 Schul-Analysis Framework

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Safety: ty](https://img.shields.io/badge/type%20safety-ty-000000.svg)](https://github.com/astral-sh/ty)
[![Tests: pytest](https://img.shields.io/badge/tests-pytest-32d656.svg)](https://pytest.org/)

Ein modernes Python Framework für symbolische Mathematik im Schulunterricht, entwickelt für Lehrer und Schüler mit Fokus auf pädagogische Klarheit und mathematische Exaktheit.

## ✨ Hauptmerkmale

### 🎯 **Magic Factory Architektur**

Automatische Erkennung des Funktionstyps - eine API für alle mathematischen Funktionen:

```python
# Automatische Typ-Erkennung
f = Funktion("x^2 + 1")                # → QuadratischeFunktion
g = Funktion("2x + 3")                 # → LineareFunktion
h = Funktion("(x^2 + 1)/(x - 1)")      # → GebrochenRationaleFunktion
e = Funktion("e^x")                    # → ExponentialFunktion
```

### 🧮 **Symbolische Exaktheit**

- **SymPy-Integration**: Keine numerischen Approximationen
- **Exakte Ergebnisse**: Brüche, Wurzeln, Symbole bleiben erhalten
- **Symbolische Ableitungen**: Mathematisch präzise Differentiation

### 🎓 **Pädagogische Perfektion**

- **Deutsche API**: Alle Methoden auf Deutsch (`Nullstellen(f)`, `Ableitung(f)`)
- **Natürliche Syntax**: `f(2)` statt `f.wert(2)`, `f' = Ableitung(f)`
- **Lösungswege**: Schritt-für-Schritt-Erklärungen mit LaTeX
- **Schülerfreundliche Fehlermeldungen**

### 📊 **Mathematisch Korrekte Visualisierung**

- **Plotly-Integration**: Perfekte Aspect Ratio, keine verzerrten Parabeln
- **Interaktive Graphen**: Zoom, Analyse, Punkt-Ablesung
- **Marimo-Notebooks**: Moderne interaktive Unterrichtsmaterialien

## 🚀 Schnellstart

### Installation

```bash
# Repository klonen
git clone https://github.com/kuelshammer/schul-analysis.git
cd schul-analysis

# Umgebung einrichten
uv sync

# Für Visualisierung (empfohlen)
uv sync --group viz-math
```

### Erste Schritte

```python
from schul_analysis import Funktion

# Funktion erstellen (automatische Typ-Erkennung)
f = Funktion("x^2 - 4x + 3")

# Natürliche mathematische Syntax
print(f(2))              # f(2) = -1
print(f.nullstellen())   # [1.0, 3.0]

# Ableitungen mit Prime-Notation
f_strich = Ableitung(f)  # f'(x) = 2x - 4
print(f_strich(2))       # f'(2) = 0

# Visualisierung
f.zeige_funktion_plotly()
```

## 🏗️ Umfassende Funktionsbibliothek

### 🔧 **Parametrisierte Funktionen**

```python
# Parameter setzen und analysieren
f = Funktion("a*x^2 + b*x + c")

# Parameter substituieren
f2 = f.setze_parameter(a=2, b=3)    # 2x² + 3x + c
f3 = f.setze_parameter(a=2)(4)       # f[2](4) = 32 + 4b + c

# Bedingungen lösen
from schul_analysis import LGS
lgs = LGS(f(1)==2, f(2)==3, f(3)==6)
lösung = lgs.löse()  # {a: 3, b: -2, c: 1}
```

### 📈 **Komplette Funktionsanalyse**

```python
f = Funktion("x^3 - 3x^2 - 9x + 5")

# Alle Analysen verfügbar
print(f.nullstellen())        # [x1, x2, x3]
print(f.extremstellen())      # [(x_min, "Minimum"), (x_max, "Maximum")]
print(f.wendepunkte())        # [(x_w, "Wendepunkt")]
print(f.symmetrie())          # Symmetrie-Eigenschaften
print(f.funktionsintervalle()) # Definitionsbereiche
```

### 🎯 **Deutsche Wrapper-API**

```python
# Pädagogische Syntax wie im Unterricht
xs = Nullstellen(f)           # statt f.nullstellen()
f1 = Ableitung(f)            # statt f.ableitung()
ext = Extrema(f)             # statt f.extrema()
wp = Wendepunkte(f)          # statt f.wendepunkte()

# Visualisierung
Zeichne(f, x_bereich=(-5, 5)) # statt f.zeige_funktion()
```

## 📊 Visualisierungs-Strategie

### 🔥 **Plotly (Empfohlen für Mathematik)**

- **Mathematisch korrekt**: Perfect Aspect Ratio
- **Interaktiv**: Zoom, Pan, Analyse-Tools
- **Schul-tauglich**: Achsenkreuz, Gitter, präzise Ablesung

```python
# Perfekte Parabel-Darstellung
f = Funktion("x^2 - 4x + 3")
f.perfekte_parabel_plotly()

# Nullstellen visualisieren
f.zeige_nullstellen_plotly()

# Ableitungsvergleich
f.zeige_ableitung_plotly(ordnung=1)
```

### 📊 **Altair (Statistische Diagramme)**

- **Data Exploration**: Interaktive Datenanalyse
- **Statistische Charts**: Boxplots, Histogramme, Streudiagramme

### 🖼️ **Matplotlib (Statische Exporte)**

- **PDF/PNG Export**: Für Druckmaterialien
- **Vollständige Kontrolle**: Publikationsqualität

## 🔬 Fortgeschrittene Features

### 📐 **Taylor-Reihenentwicklung**

```python
from schul_analysis import Taylorpolynom

f = Funktion("sin(x)")
taylor = Taylorpolynom(f, entwicklungspunkt=0, grad=5)
print(taylor.term())  # x - x³/6 + x⁵/120
```

### 🔍 **Schmiegkurven**

```python
from schul_analysis import Schmiegkurve

# Schmiegparabel durch drei Punkte
punkte = [(0, 1), (1, 3), (2, 2)]
schmieg = Schmiegkurve(punkte)
```

### ⚖️ **Lineare Gleichungssysteme**

```python
# LGS mit Funktionen lösen
f = Funktion("a*x^2 + b*x + c")
bedingungen = [f(1)==2, f(2)==3, f(3)==6]
lgs = LGS(*bedingungen)
lösung = lgs.löse()
```

## 📚 Unterstützte Funktionstypen

| Funktionstyp        | Beispiel           | Methoden                                              |
| ------------------- | ------------------ | ----------------------------------------------------- |
| **Linear**          | `2x + 3`           | `nullstellen()`, `steigung()`, `y_achsenabschnitt()`  |
| **Quadratisch**     | `x² - 4x + 3`      | `nullstellen()`, `scheitelpunkt()`, `extremstellen()` |
| **Polynom**         | `x³ - 2x² + 5`     | `nullstellen()`, `ableitungen()`, `wendepunkte()`     |
| **Rational**        | `(x² + 1)/(x - 1)` | `nullstellen()`, `polstellen()`, `asymptoten()`       |
| **Exponentiell**    | `e^x`, `2^x`       | `nullstellen()`, `ableitungen()`, `wachstum()`        |
| **Trigonometrisch** | `sin(x)`, `cos(x)` | `nullstellen()`, `perioden()`, `amplituden()`         |
| **Gemischt**        | `sin(x) + x²`      | Komplexe Analyse aller Komponenten                    |
| **Strukturiert**    | Summen, Produkte   | Automatische Zerlegung und Analyse                    |

## 🛠️ Entwicklung

### Setup für Entwicklung

```bash
# Entwicklungsumgebung einrichten
uv sync --all-groups

# Code Quality Checks
uv run ruff check      # Linting
uv run ruff format     # Formatting
uv run ty check        # Type Checking
uv run pytest         # Tests
uv run pytest --cov   # Tests mit Coverage
```

### Projektstruktur

```
schul_analysis/
├── src/schul_analysis/     # 21 Module mit voller Funktionalität
├── examples/               # Praktische Anwendungsbeispiele
├── tests/                  # 32 Testdateien mit umfassender Abdeckung
├── docs/                   # Methoden-Dokumentation
└── pyproject.toml          # Modernes Python-Packaging
```

## 📖 Anwendung im Unterricht

### 🔍 **Für Lehrer**

- **Interaktive Tafelbilder**: Marimo-Notebooks mit Live-Analyse
- **Lösungsgenerierung**: Automatische Schritt-für-Schritt-Erklärungen
- **Visualisierungshilfen**: Perfekte mathematische Darstellungen
- **Differentiation**: Aufgaben für verschiedene Leistungsniveaus

### 🎓 **Für Schüler**

- **Intuitive API**: Natürliche mathematische Syntax
- **Selbstkontrolle**: Sofortiges Feedback bei Aufgaben
- **Experimentierumgebung**: Parameter variation und Analyse
- **Verständliche Fehler**: Konstruktive Fehlermeldungen

## 🎯 Einsatzszenarien

### 📏 **Mittelstufe (Klasse 7-10)**

- Lineare und quadratische Funktionen
- Nullstellen, Extremstellen, Schnittpunkte
- Funktionsscharen und Parameteruntersuchung

### 📊 **Oberstufe (Klasse 11-13)**

- Kurvendiskussion ganzrationaler Funktionen
- Gebrochen-rationale Funktionen
- Exponential- und Logarithmusfunktionen
- Trigonometrische Funktionen
- Taylor-Reihen und Approximation

### 🎓 **Studienvorbereitung**

- Symbolische Manipulation
- Grenzwertuntersuchungen
- Integralrechnung
- Differentialgleichungen

## 🏆 Besondere Stärken

### ✨ **Pädagogische Excellence**

- Deutsche Fachterminologie durchgängig konsistent
- Mathematische Notation wie im Schulbuch
- Schritt-für-Schritt-Lösungen im Unterrichtsstil
- Fehleranalyse und -vermeidung

### 🔬 **Technische Überlegenheit**

- Magic Factory Pattern für intuitive Bedienung
- SymPy-Integration für symbolische Exaktheit
- Moderne Toolchain (uv, ruff, ty, pytest)
- Umfassende Testabdeckung (>80%)

### 🎨 **Visuelle Perfektion**

- Plotly für mathematisch korrekte Graphen
- Keine verzerrten Darstellungen
- Interaktive Analysemöglichkeiten
- Exportqualität für Unterrichtsmaterialien

## 🤝 Contributing

Wir freuen uns über Beiträge! Bitte beachten Sie:

1. **Fork** das Repository
2. **Feature Branch** erstellen: `git checkout -b feature/feature-name`
3. **Entwickeln** mit Tests und Dokumentation
4. **Pull Request** mit klarer Beschreibung

### Entwicklungstandards

- [ ] Typos mit `uv run ty check` prüfen
- [ ] Ruff mit `uv run ruff check` und `uv run ruff format`
- [ ] Tests mit `uv run pytest` erfolgreich
- [ ] Deutsche API und Dokumentation

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagung

- **SymPy-Team**: Für die hervorragende symbolische Mathematik-Bibliothek
- **Plotly-Team**: Für mathematisch korrekte Visualisierungen
- **Marimo-Team**: Für moderne interaktive Notebooks
- **Astral-Team**: Für hervorragende Entwicklungstools (uv, ruff, ty)

---

**🎯 Mission**: Mathematikunterricht durch symbolische Exaktheit und pädagogische Klarheit revolutionieren.

**📧 Kontakt**: Bei Fragen oder Anregungen gerne [Issue](https://github.com/kuelshammer/schul-analysis/issues) erstellen.
