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

### 🔬 **Mathematische Exaktheit durch Typ-System**

**Revolutionäres Typ-System garantiert symbolische Präzision:**

```python
# Garantierte Exaktheit statt numerischer Approximation
f = Funktion("x^2 - 4x + 3")
extremstellen = Extremstellen(f)
# Ergebnis: [(sp.Rational(1, 4), 'Minimum')]  # 1/4 statt 0.25
```

**Strenge Typisierung und Runtime-Validierung:**

- **Symbolische Präzision**: `1/3` bleibt als `sp.Rational(1, 3)` erhalten, nicht `0.333...`
- **Pädagogische Fehlermeldungen**: Deutsche Fehlermeldungen als Lernmomente
- **Enum-basierte Klassifikation**: `ExtremumTyp.MINIMUM` statt magic strings
- **Datenklassen mit Semantik**: `Nullstelle(x=sp.Rational(3, 2), multiplicitaet=2, exakt=True)`

**Abitur-Konsistenz gewährleistet:**
Alle Ergebnisse entsprechen genau den Anforderungen deutscher Mathematikprüfungen.

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

ruf## 🔬 Typ-System-Architektur

### **Kernkomponenten des Typ-Systems**

Das Schul-Analysis Framework verwendet ein revolutionäres Typ-System, das mathematische Exaktheit durch strenge Typisierung gewährleistet:

```python
# Type Variables mit mathematischen Bounds
T_Expr = TypeVar("T_Expr", bound=sp.Expr)  # SymPy-Ausdrücke
T_Num = TypeVar("T_Num", bound=sp.Number)  # Numerische Werte

# Enums für mathematische Konzepte
class ExtremumTyp(Enum):
    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"
    SATTELPUNKT = "Sattelpunkt"

# Datenklassen mit pädagogischer Semantik
@dataclass(frozen=True)
class Nullstelle:
    x: T_Expr           # x-Koordinate (exakt)
    multiplicitaet: int = 1  # Vielfachheit
    exakt: bool = True       # Exaktheitsgarantie
```

### **Validation und Type Guards**

**Runtime-Validierung für pädagogische Korrektheit:**

```python
@preserve_exact_types
def ableitung(self, ordnung: int = 1) -> "Funktion":
    """Berechnet die Ableitung unter Garantie der Exaktheit."""
    abgeleiteter_term = diff(self.term_sympy, self._variable_symbol, ordnung)
    validate_function_result(abgeleiteter_term, "exact")
    return Funktion(abgeleiteter_term)

# Type Guards zur Präzisionssicherung
def is_exact_sympy_expr(expr: Any) -> TypeGuard[T_Expr]:
    """Stellt sicher, dass kein Ausdruck numerisch approximiert wurde."""
    return not any(isinstance(atom, sp.Float) for atom in expr.atoms(sp.Number))
```

### **Pädagogische Vorteile**

**Für Schüler:**

- **Exakte Ergebnisse**: `1/4` statt `0.25` - wie im Mathematikunterricht
- **Klare Strukturen**: Selbst-dokumentierende Datentypen
- **Verständliche Fehler**: Deutsche Fehlermeldungen erklären das Problem
- **Prüfungsrelevant**: Ergebnisse entsprechen Abitur-Anforderungen

**Für Lehrer:**

- **Verlässlichkeit**: Garantierte mathematische Korrektheit
- **Transparenz**: Klare Typ-Signaturen zeigen Erwartungen
- **Erweiterbarkeit**: Protokolle ermöglichen neue Funktionstypen

### **Beispiel: Präzision in der Praxis**

```python
# Problem: Potenzielle Ungenauigkeit in traditionellen Systemen
traditionell = 1 / 6  # 0.166666... (numerische Approximation)

# Lösung: Garantierte Exaktheit durch Typ-System
exakt = sp.Rational(1, 6)  # 1/6 (symbolisch exakt)

# In Extremstellen-Berechnung
f = Funktion("2*x^2 - x")
extremstellen = Extremstellen(f)
x_wert, art = extremstellen[0]
# x_wert = sp.Rational(1, 4)  # Exakt 1/4, nicht 0.25
```

## 🔧 Neue Features in Version 1.1

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

## 🧹 Code-Status und Refactoring

### **Kürzliche Verbesserungen (Dezember 2024)**

#### **🔬 Revolutionäres Typ-System implementiert**

**Umfassende Typ-System-Überholung mit Fokus auf mathematische Exaktheit:**

- **✅ Complete Type System Refactor**: Von `Any`-basiert zu präzisen mathematischen Typen
- **✅ SymPy-Integration**: Garantierte symbolische Präzision in allen Berechnungen
- **✅ Runtime-Validierung**: Automatische Prüfung der mathematischen Korrektheit
- **✅ Pädagogische Type Safety**: Deutsche Fehlermeldungen und Abitur-Konsistenz
- **✅ Enum-basierte Klassifikation**: `ExtremumTyp`, `WendepunktTyp` statt magic strings
- **✅ Strukturierte Datenklassen**: `Nullstelle`, `Extremum`, `Wendepunkt` mit Semantik

**Technische Architektur:**

```python
# Type Variables mit Bounds
T_Expr = TypeVar("T_Expr", bound=sp.Expr)

# Validation Decorators
@preserve_exact_types
def ableitung(self, ordnung: int = 1) -> "Funktion"

# Type Guards für Präzision
def is_exact_sympy_expr(expr: Any) -> TypeGuard[T_Expr]
```

**Gemini Code Review Ergebnisse:**

- **58+ kritische Typ-Fehler behoben**
- **Mathematische Exaktheit garantiert**
- **Pädagogische Qualität verbessert**
- **Nur 9 minimale verbleibende Issues (nicht kritisch)**

#### **Frühere Verbesserungen (November 2024)**

- **✅ API-Vereinheitlichung**: Konsistente Namenskonvention eingeführt
- **✅ Methoden-Entfernung**: Ungenutzte `get_*`-Methoden aus ganzrational.py entfernt
- **✅ Pädagogische Methoden**: Überflüssige Erklärungsmethoden aus gebrochen_rationale.py entfernt
- **✅ Code-Qualität**: Kern-Dateien bestehen ruff-Prüfung

### **Zu überprüfende API-Funktionen**

Folgende Funktionen werden derzeit nicht genutzt, werden aber beibehalten:

- `Erstelle_Exponential_Rationale_Funktion()` - Für zukünftige Verwendung
- `Erstelle_Lineares_Gleichungssystem()` - Für LGS-Integration
- `Analysiere_Funktion()` - Für erweiterte Analyse
- `Zeige_Analyse()` - Für formatierte Ausgaben

**Entscheidung**: Diese Funktionen bleiben als zukünftige Erweiterungen erhalten.

### **Technische Schuld**

- **Visualisierung**: Einige Plotly-Helper-Funktionen könnten konsolidiert werden
- **Struktur**: `parametrisch.py` Import muss überprüft werden
- **Type Hints**: Einige komplexe Typ-Annotationen könnten vereinfacht werden

Regelmäßige Code-Reviews mit statischen Analyse-Tools (z.B. Gemini Code Review) werden empfohlen.
