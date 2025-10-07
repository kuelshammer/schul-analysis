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
h = Funktion("(x^2 + 1)/(x - 1)")      # → QuotientFunktion
e = Funktion("e^x")                    # → ExponentialFunktion
```

### 🧮 **Symbolische Exaktheit**

- **SymPy-Integration**: Keine numerischen Approximationen
- **Exakte Ergebnisse**: Brüche, Wurzeln, Symbole bleiben erhalten
- **Symbolische Ableitungen**: Mathematisch präzise Differentiation

### 🎓 **Pädagogische Perfektion**

- **Deutsche API**: Alle Wrapper-Funktionen auf Deutsch (`Nullstellen(f)`, `Ableitung(f)`)
- **Konsistente Namenskonvention**: Wrapper großgeschrieben (wie deutsche Substantive), Methoden kleingeschrieben
- **Natürliche Syntax**: `f(2)` statt `f.wert(2)`, `f' = Ableitung(f)`
- **Lösungswege**: Schritt-für-Schritt-Erklärungen mit LaTeX
- **Schülerfreundliche Fehlermeldungen**

### 📊 **Mathematisch Korrekte Visualisierung**

- **Plotly-Integration**: Perfekte Aspect Ratio, keine verzerrten Parabeln
- **Interaktive Graphen**: Zoom, Analyse, Punkt-Ablesung
- **Marimo-Notebooks**: Moderne interaktive Unterrichtsmaterialien

## 🚀 Schnellstart

ruf## 🔧 Neue Features in Version 1.1

### 🎯 Intuitive `__call__`-Syntax für Funktionen

Das Framework unterstützt jetzt die natürliche mathematische Notation `f(x)`:

```python
# Ganzrationale Funktionen
f = GanzrationaleFunktion("x^2 + 2x - 3")
print(f(2))     # 5.0 (statt f.wert(2))
```

### 🔥 Konsistente Namenskonvention

**Wrapper-Funktionen (großgeschrieben wie deutsche Substantive):**

```python
# Natürliche mathematische Notation für Schüler
f = Funktion("x^2 - 4x + 3")
xs = Nullstellen(f)           # [1.0, 3.0]
ext_st = Extremstellen(f)     # [(-1, 'Maximum')]
ext_pt = Extrempunkte(f)      # [(-1, 14.0, 'Maximum')]
wend_st = Wendestellen(f)    # [(0, 'Wendepunkt')]
wend_pt = Wendepunkte(f)     # [(0, 0.0, 'Wendepunkt')]
f1 = Ableitung(f)             # 2x - 4
F_unbest = Integral(f)       # (1/3)x³
F_best = Integral(f, 0, 1)   # 1/3
graph = Graph(f)             # Automatische Skalierung
```

**Klassenmethoden (kleingeschrieben):**

```python
# Methoden der Funktionsobjekte
f = Funktion("x^2 - 4x + 3")
f1 = f.ableitung()            # 2x - 4
xs = f.nullstellen            # [1.0, 3.0] (Property)
y = f.wert(2)                 # -1.0
```

### 🔥 Prime-Notation für Ableitungen

Das Framework unterstützt die intuitive mathematische Notation für Ableitungen:

```python
# Mathematisch: f'(x) = 2x + 3, f'(2) = 7
f = GanzrationaleFunktion("x^2 + 3x - 2")
f_strich = Ableitung(f)        # f'(x) = 2x + 3
print(f_strich(2))            # 7.0

# Höhere Ableitungen
f_zwei_strich = Ableitung(f_strich)  # f''(x) = 2
print(f_zwei_strich(5))       # 2.0

# Kombination mit __call__ Syntax
f = GanzrationaleFunktion("x^3 - 2x^2 + 5x - 1")
f_strich = Ableitung(f)       # f'(x) = 3x² - 4x + 5
print(f_strich(1))            # 4.0

f_zwei_strich = Ableitung(f_strich)  # f''(x) = 6x - 4
print(f_zwei_strich(1))       # 2.0
```

### 📋 Gleichungssyntax (Vorbereitung für LGS)

Die Syntax `f(x) == wert` wird vorbereitet:

```python
# Wird in Zukunft Lineare Gleichungen für LGS erstellen
bedingung = f(3) == 7  # f(3) = 7
```

## 🔥 Visualisierungs-Strategie

### Plotly (🏆 Hauptpaket für Mathematik)

**Vorteile:**

- ✅ **Perfekte mathematische Korrektheit** durch Aspect Ratio Control
- ✅ **Keine verzerrten Parabeln** - `scaleanchor="y", scaleratio=1`
- ✅ **Interaktive Funktionen**: Zoom, pan, 3D-Rotation
- ✅ **Schul-Konventionen**: Achsen im Ursprung, Gitterlinien
- ✅ **Marimo-Integration**: `mo.ui.plotly()`

**Anwendungsbereiche:**

- 🔥 Funktionsgraphen (Parabeln, Polynome)
- 🔥 Nullstellen-Visualisierung
- 🔥 Extremstellen-Darstellung
- 🔥 Ableitungsvergleiche
- 🔥 Geometrische Konstruktionen

### Altair (📊 Sekundärpaket für Statistik)

**Vorteile:**

- ✅ **Data Selection** - interaktive Datenfilterung
- ✅ **Statistische Diagramme**: Balken, Boxplots, Streudiagramme
- ✅ **Datenanalyse**: Aggregation, Gruppierung
- ✅ **Marimo-Integration**: `mo.ui.altair_chart()`

**Einschränkungen:**

- ❌ **Kein Aspect Ratio Control** - Parabeln werden verzerrt
- ❌ **Nicht für mathematische Korrektheit geeignet**

### Matplotlib (🖼️ Statische Exporte)

**Vorteile:**

- ✅ **PDF/PNG Export** für Druckmaterialien
- ✅ **Vollständige Kontrolle** über Layout
- ✅ **Wissenschaftliche Publikationen**

**Einschränkungen:**

- ❌ **Nicht reaktiv** - keine Interaktivität
- ❌ **Keine Aspect Ratio Kontrolle**

### Wann welches Paket?

| Anwendung                  | Plotly     | Altair     | Matplotlib       |
| -------------------------- | ---------- | ---------- | ---------------- |
| **Funktionsgraphen**       | 🔥 **Ja**  | ❌ Nein    | ⚠️ Eingeschränkt |
| **Parabel-Darstellung**    | 🔥 **Ja**  | ❌ Nein    | ❌ Nein          |
| **Statistische Diagramme** | ⚠️ Möglich | 🔥 **Ja**  | ⚠️ Möglich       |
| **Interaktive Analyse**    | 🔥 **Ja**  | 🔥 **Ja**  | ❌ Nein          |
| **Druck-Export**           | ⚠️ Möglich | ⚠️ Möglich | 🔥 **Ja**        |

## Installation

### Basisinstallation (für Benutzer)

```bash
# Klonen des Repositories
git clone https://github.com/kuelshammer/schul-analysis.git
cd schul-analysis

# Installation mit uv
uv sync
```

### Für Entwickler

```bash
# Alle Entwicklungstools installieren
uv sync --all-groups

# Oder gruppenweise:
uv sync --group dev      # Entwicklungstools (ruff, ty, pytest)
uv sync --group docs     # Dokumentationstools (sphinx)
uv sync --group viz-math # Mathematische Visualisierung (Plotly) 🔥 EMPFOHLEN
uv sync --group viz-stats # Statistische Visualisierung (Altair)
uv sync --group viz-static # Statische Exporte (Matplotlib)
uv sync --group types    # Type stubs
```

### Nur Core Dependencies

```bash
# Nur die für den Betrieb notwendigen Pakete
uv sync --no-dev
```

## Paketstruktur

### Core Dependencies (werden immer installiert)

- `sympy>=1.14.0` - Symbolische Mathematik
- `marimo>=0.16.3` - Interaktive Notebooks

### Development Dependencies (nur für Entwickler)

- `ruff>=0.13.2` - Linting & Formatting
- `ty>=0.0.1a21` - Type checking (Astral)
- `pytest>=8.4.2` - Testing
- `pytest-cov>=7.0.0` - Test Coverage

### Optional Dependencies

- `viz-math`: **plotly**, numpy (🔥 EMPFOHLEN für mathematisch korrekte Graphen)
- `viz-stats`: altair, vega-datasets, pandas (für statistische Diagramme)
- `viz-static`: matplotlib (für statische Exporte)
- `docs`: sphinx, sphinx-rtd-theme (für Dokumentation)
- `types`: Type stubs für bessere Type Safety

## Quick Start

```python
from schul_analysis.ganzrationale import GanzrationaleFunktion

# Verschiedene Konstruktor-Formate
f1 = GanzrationaleFunktion("x^3-2x+1")     # String (intuitiv)
f2 = GanzrationaleFunktion([1, 0, -2, 1])   # Liste (traditionell)
f3 = GanzrationaleFunktion({3: 1, 1: -2, 0: 1})  # Dictionary

# Berechnungen
nullstellen = f1.nullstellen()           # [1.0, 2.0]
ableitung = f1.ableitung()               # GanzrationaleFunktion
extremstellen = f1.extremstellen()       # [(1.5, "Minimum")]

# Lösungsweg als Markdown
weg = f1.nullstellen_weg()
print(weg)  # Detaillierter Schritt-für-Schritt-Lösungsweg
```

## In Marimo Notebooks

```python
import marimo as mo
from schul_analysis.ganzrationale import GanzrationaleFunktion

# Mathematisch korrekte Visualisierung mit Plotly (EMPFOHLEN)
f = GanzrationaleFunktion("x^2-4x+3")

# LaTeX-Darstellung in Marimo
mo.md(f"## Funktion: $$f(x) = {f.term_latex()}$$")

# 🔥 Perfekte Parabel-Darstellung mit Plotly
mo.ui.plotly(f.perfekte_parabel_plotly())

# Interaktiver Lösungsweg
f.zeige_nullstellen_marimo(real=True)

# Alternative: Statistische Visualisierung mit Altair
f.zeige_funktion_altair()
```

### Visualisierungs-Pakete wählen

**🔥 Für Mathematik (EMPFOHLEN):**

```bash
uv sync --group viz-math  # Installiert Plotly für perfekte mathematische Darstellung
```

**📊 Für Statistik:**

```bash
uv sync --group viz-stats  # Installiert Altair für statistische Diagramme
```

**🖼️ Für statische Exporte:**

```bash
uv sync --group viz-static  # Installiert Matplotlib für PDF/PNG Export
```

## Entwicklung

### Setup für Entwicklung

```bash
# Repository klonen
git clone https://github.com/kuelshammer/schul-analysis.git
cd schul-analysis

# Entwicklungsumgebung einrichten
uv sync --all-groups
```

### Code Quality

```bash
# Type checking mit ty
uv run ty check

# Linting mit ruff
uv run ruff check
uv run ruff format

# Tests ausführen
uv run pytest

# Tests mit Coverage
uv run pytest --cov=schul_analysis
```

### Projektstruktur

```
schul-analysis/
├── src/schul_analysis/          # Source code
│   ├── basis/                   # Base classes
│   ├── ganzrationale/           # Polynomial functions
│   ├── exponential/             # Exponential functions
│   └── trigonometrisch/         # Trigonometric functions
├── tests/                       # Test files
├── docs/                        # Documentation
├── notebooks/                   # Marimo notebooks
└── pyproject.toml              # Project configuration
```

## Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## Contributing

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/amazing-feature`)
3. Commit deine Änderungen (`git commit -m 'Add amazing feature'`)
4. Push zum Branch (`git push origin feature/amazing-feature`)
5. Erstelle einen Pull Request

## Unterstützung

Bei Fragen oder Problemen erstelle bitte ein [Issue](https://github.com/kuelshammer/schul-analysis/issues).
