# Schul-Analysis Framework - Entwicklungshandbuch

## 🎯 Projekt-Überblick

Modernes Python Framework für symbolische Mathematik im Schulunterricht mit Magic Factory Architektur, entwickelt für deutsche Mathematiklehrer und Schüler. Kombiniert pädagogische Exaktheit mit technischer Überlegenheit.

### 🎓 **Pädagogische Kernprinzipien**

#### **Deutsche Schul-Mathematik (Durchgängig Konsistent)**

- **API auf Deutsch**: Alle öffentlichen Methoden und Klassen verwenden deutsche Fachbegriffe
- **Fehlermeldungen auf Deutsch**: Verständliche, konstruktive Fehlermeldungen für Schüler
- **Dokumentation auf Deutsch**: Alle Erklärungen in deutscher Fachsprache
- **Schulbuch-Konsistenz**: Begriffe und Notation entsprechen dem deutschen Unterricht

#### **Unterrichtsnahes API-Design (Magic Factory Pattern)**

```python
# Natürliche mathematische Syntax
f = Funktion("x^2 + 2x - 3")        # Automatische Typ-Erkennung
print(f(2))                         # f(2) statt f.wert(2)
xs = Nullstellen(f)                  # Funktion statt Methode
f_strich = Ableitung(f)              # f' = df/dx
Zeichne(f, x_bereich=(-5, 5))        # Visualisierung als Aktion
```

#### **Kognitive Entlastung**

- **Einfache Konstruktoren**: String, Liste, Dictionary - alles möglich
- **Intuitive Parameter**: Namen wie `ordnung`, `bereich`, `punkt`
- **Visuelle Unterstützung**: Plotly-Graphen mit perfekter mathematischer Darstellung
- **Exakte Berechnungen**: SymPy vermeidet numerische Verwirrung

## 🔧 Moderne Entwicklungstools & Workflow

### **Package Management: uv (Zentral)**

```bash
# Basis-Installation (Core Dependencies)
uv sync

# Vollständige Entwicklungsumgebung
uv sync --all-groups

# Selektive Installation
uv sync --group dev          # Entwicklungstools
uv sync --group viz-math      # Mathematische Visualisierung
uv sync --group viz-stats     # Statistische Diagramme
uv sync --group docs          # Dokumentation
uv sync --group types         # Type Stubs
```

### **Code Quality Pipeline**

```bash
# Vor jedem Commit ausführen!
uv run ty check               # Type Checking (Astral)
uv run ruff check            # Linting
uv run ruff format           # Formatting
uv run pytest                # Testing
uv run pytest --cov          # Testing mit Coverage
```

### **Quality Gates**

- **Type Safety**: 100% ty check bestanden
- **Code Style**: 100% ruff formatting
- **Test Coverage**: Mindestens 80%
- **Documentation**: Alle öffentlichen APIs dokumentiert

## 🏗️ Moderne Architektur (Magic Factory Pattern)

### **Kernkonzept: Automatische Typ-Erkennung**

```python
# Eine API für alle Funktionstypen
f = Funktion("x^2 + 1")           # → QuadratischeFunktion
g = Funktion("2x + 3")            # → LineareFunktion
h = Funktion("(x^2+1)/(x-1)")    # → GebrochenRationaleFunktion
e = Funktion("e^x")              # → ExponentialFunktion
t = Funktion("sin(x)")           # → TrigonometrischeFunktion
```

### **Aktuelle Module-Struktur (21 Module)**

```
src/schul_analysis/
├── __init__.py              # Haupt-API mit Magic Factory
├── api.py                   # Wrapper-Funktionen für Schüler
├── funktion.py              # Magic Factory Basisklasse
├── konfiguration.py         # Zentrale Konfiguration
├── fehler.py               # Fehlerbehandlung auf Deutsch
├── symbolisch.py           # Symbolische Hilfsfunktionen
├── visuell.py              # Visualisierungs-Koordination
│
├── ganzrationale.py         # Polynomfunktionen beliebigen Grades
├── quadratisch.py           # Quadratische Funktionen (spezialisiert)
├── lineare.py              # Lineare Funktionen
├── exponential.py           # Exponentialfunktionen
├── trigonometrisch.py       # Trigonometrische Funktionen
├── gebrochen_rationale.py   # Rationale Funktionen (Brüche)
├── gemischte.py            # Gemischte Ausdrücke (z.B. sin(x) + x²)
├── parametrisch.py         # Parametrisierte Funktionen
├── strukturiert.py         # Strukturierte Funktionen (Summen, Produkte)
│
├── analyse.py              # Umfassende Funktionsanalyse
├── ableitungen.py          # Ableitungen aller Ordnungen
├── nullstellen.py          # Nullstellenberechnung
├── extremstellen.py        # Extremwertanalyse
├── wendepunkte.py          # Wendepunktanalyse
├── symmetrie.py            # Symmetrieanalyse
├── taylor.py               # Taylor-Reihenentwicklung
├── schmiegkurven.py        # Schmiegkurven
├── lineare_gleichungssysteme.py  # LGS-Löser
└── visualisierung.py       # Plotly/Altair/Matplotlib Integration
```

### **Design-Prinzipien**

1. **Single Source of Truth**: Magic Factory als zentraler Einstiegspunkt
2. **Automatische Delegation**: Erkennung → Spezialisiertes Modul → Rückgabe
3. **Konsistente API**: Alle Funktionstypen haben gleiche Grundmethoden
4. **Deutsch als Default**: Alle öffentlichen APIs auf Deutsch

## 🔄 Git Workflow (uv-basiert)

### **Grundprinzip: Feature-Branch mit uv**

```bash
# 1. Aktuellen Stand sichern
git add .
git commit -m "feat: Implementiere Magic Factory Pattern"

# 2. Feature-Branch erstellen
git checkout -b feature/setze_parameter-methode

# 3. Am Feature arbeiten
# ... Code schreiben, testen, uv run checks ...

# 4. Regelmäßig commits
git commit -m "feat: setze_parameter() Methode hinzugefügt"
git commit -m "test: Tests für Parameter-Substitution"
git commit -m "docs: Dokumentation aktualisiert"

# 5. Feature fertigstellen
git checkout main
git merge feature/setze_parameter-methode
git branch -d feature/setze_parameter-methode
git push origin main
```

### **Commit-Konvention (Semantic Commit Messages)**

| Typ        | Beschreibung          | Beispiel                                                 |
| ---------- | --------------------- | -------------------------------------------------------- |
| `feat`     | Neues Feature         | `feat: Implementiere setze_parameter() Methode`          |
| `fix`      | Bugfix                | `fix: Korrigiere Aspect Ratio in Plotly-Darstellung`     |
| `docs`     | Dokumentation         | `docs: README.md mit Magic Factory erweitert`            |
| `style`    | Code-Formatierung     | `style: ruff format ausgeführt`                          |
| `refactor` | Refactoring           | `refactor: Funktionserkennung optimiert`                 |
| `test`     | Tests                 | `test: Tests für parametrisierte Funktionen hinzugefügt` |
| `chore`    | Build/Tool-Änderungen | `chore: uv.lock aktualisiert`                            |

### **Quality Checks vor jedem Commit**

```bash
# Vor dem Commit immer ausführen:
uv run ty check && uv run ruff check && uv run ruff format && uv run pytest
```

## 📦 Abhängigkeitsmanagement (uv groups)

### **Core Dependencies (Immer installiert)**

```toml
dependencies = [
    "marimo>=0.16.3",     # Interaktive Notebooks
    "plotly>=6.3.0",      # Mathematische Visualisierung
    "sympy>=1.14.0",      # Symbolische Mathematik
]
```

### **Development Groups**

```toml
[dependency-groups]
dev = [
    "ruff>=0.13.2",       # Linting & Formatting
    "ty>=0.0.1a21",       # Type Checking
    "pytest>=8.4.2",      # Testing Framework
    "pytest-cov>=7.0.0",  # Coverage
    "scipy>=1.16.2",      # Wissenschaftliche Berechnungen
]

viz-math = [
    "plotly>=6.3.0",      # Haupt-Visualisierung
    "numpy>=2.3.3",       # Numerische Grundlagen
]

viz-stats = [
    "altair>=5.5.0",      # Statistische Diagramme
    "pandas>=2.3.3",      # Datenmanipulation
]
```

### **Installationsstrategie**

```bash
# Für Endbenutzer (minimal)
uv sync --no-dev

# Für Lehrer (mit Visualisierung)
uv sync --group viz-math

# Für Entwickler (komplett)
uv sync --all-groups
```

## 🧪 Moderne Testing-Strategie

### **Test-Organisation**

```
tests/
├── test_funktion.py              # Magic Factory Tests
├── test_setze_parameter.py       # Parameter-Substitution
├── test_automatische_erkennung.py # Typ-Erkennung
├── test_ganzrationale.py         # Polynomfunktionen
├── test_gebrochen_rationale.py   # Rationale Funktionen
├── test_exponential.py           # Exponentialfunktionen
├── test_lineare_gleichungssysteme.py # LGS-Löser
├── test_visualisierung.py        # Plotly/Altair Tests
└── fixtures/                     # Testdaten
    ├── funktionen.py             # Standard-Funktionen
    └── parameter.py              # Parameter-Konfiguration
```

### **Test-Prinzipien**

1. **SymPy.equals()**: Für symbolische Vergleiche statt String-Vergleich
2. **Echte Testabdeckung**: Alle Code-Paths testen
3. **Deutsche Testnamen**: Verständlich für Entwickler
4. **Fixtures**: Wiederverwendbare Testdaten

### **Test-Beispiel (Moderne Struktur)**

```python
# tests/test_setze_parameter.py
import pytest
from schul_analysis import Funktion

class TestSetzeParameter:
    """Teste die setze_parameter() Methode für parametrisierte Funktionen."""

    def test_einfache_substitution(self):
        """Teste einfache Parameter-Substitution."""
        f = Funktion("a*x^2 + b*x + c")
        f2 = f.setze_parameter(a=2)
        expected = Funktion("2*x^2 + b*x + c")
        assert f2.term_sympy.equals(expected.term_sympy)

    def test_kombinierte_nutzung(self):
        """Teste kombinierte Nutzung f.setze_parameter(...)(x)."""
        f = Funktion("a*x^2 + b*x + c")
        result = f.setze_parameter(a=2, b=3)(4)
        expected = 2*16 + 3*4 + c  # 32 + 12 + c = 44 + c
        assert result == expected
```

### **Coverage-Ziele**

- **Minimum**: 80% Coverage
- **Ziel**: 90% Coverage für Kernmodule
- **Core Module**: 95% Coverage (funktion.py, analyse.py)

## 🎓 Pädagogische Entwicklungsrichtlinien

### **API-Design für Schüler**

#### **1. Funktion vor Methode**

```python
# ✅ GUT: Funktionale Syntax
xs = Nullstellen(f)
f1 = Ableitung(f, 1)
ext = Extrema(f)

# ❌ SCHLECHT: Methoden-basiert
xs = f.nullstellen()
f1 = f.ableitung(1)
ext = f.extrema()
```

#### **2. Natürliche mathematische Notation**

```python
# ✅ GUT: Mathematisch natürlich
f(2)                           # Funktionswert
f_strich = Ableitung(f)         # Ableitung f'
f2_strich = Ableitung(f_strich) # Zweite Ableitung f''

# ❌ SCHLECHT: Technisch
f.wert(2)
f.ableitung()
f.ableitung().ableitung()
```

#### **3. Deutsche Fachbegriffe durchgängig**

```python
# ✅ GUT: Deutsche Terminologie
f.setze_parameter(a=2, b=3)
f.zeige_nullstellen_weg()
f.scheitelpunkt()

# ❌ SCHLECHT: Englische Begriffe
f.set_parameters(a=2, b=3)
f.show_roots_path()
f.vertex()
```

### **Namenskonventionen**

| Element        | Konvention             | Beispiele                               |
| -------------- | ---------------------- | --------------------------------------- |
| **Klassen**    | `PascalCase` (Deutsch) | `GanzrationaleFunktion`, `Schmiegkurve` |
| **Methoden**   | `snake_case` (Deutsch) | `zeige_funktion`, `berechne_integral`   |
| **Funktionen** | `PascalCase` (Deutsch) | `Nullstellen`, `Ableitung`, `Extrema`   |
| **Variablen**  | `snake_case` (Deutsch) | `koeffizienten`, `nullstellen_liste`    |
| **Konstanten** | `UPPER_SNAKE_CASE`     | `MAX_PRECISION`, `DEFAULT_RANGE`        |

### **Fehlerbehandlung**

```python
# ✅ GUT: Pädagogische Fehlermeldungen
try:
    f.setze_parameter(x=5)  # x ist Variable, kein Parameter
except ValueError as e:
    # "Parameter 'x' kommt in der Funktion f(x) = a*x^2 + b*x + c nicht vor."
    # "Verfügbare Parameter: a, b, c"
    pass

# ❌ SCHLECHT: Technische Fehlermeldungen
except ValueError as e:
    # "Invalid parameter: x not in free_symbols"
    pass
```

## 🚀 Deployment & Veröffentlichung

### **Versionierung (Semantic Versioning)**

```python
# src/schul_analysis/__init__.py
__version__ = "0.2.0"  # MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking Changes (neue API)
- **MINOR**: Neue Features (rückwärtskompatibel)
- **PATCH**: Bugfixes (kleine Änderungen)

### **Build & Publish mit uv**

```bash
# Build
uv build

# Lokaler Test
uv run pip install dist/*.whl --force-reinstall

# Publish zu PyPI
uv publish
```

### **CHANGELOG Pflege**

```markdown
## [0.2.0] - 2024-10-06

### Added

- Magic Factory Pattern für automatische Funktionserkennung
- setze_parameter() Methode für parametrisierte Funktionen
- Prime-Notation für Ableitungen (f' = Ableitung(f))
- Umfassende Taylor-Reihen-Integration

### Changed

- Komplette Überarbeitung der API-Architektur
- Migration zu uv als Paketmanager
- Verbesserte Fehlermeldungen auf Deutsch

### Fixed

- Aspect Ratio Probleme in Plotly-Visualisierungen
- Numerische Ungenauigkeiten bei SymPy-Berechnungen
```

## 💡 Best Practices & Patterns

### **Magic Factory Implementierung**

```python
# funktion.py - Kern der Architektur
class Funktion:
    """Magic Factory für automatische Funktionserkennung."""

    def __new__(cls, eingabe, **kwargs):
        """Automatische Erkennung und Delegation."""
        # 1. Typ-Erkennung basierend auf Eingabe
        funktionstyp = cls._erkenne_funktionstyp(eingabe)

        # 2. Delegation an spezialisierte Klasse
        spezialisierte_klasse = cls._hole_spezialklasse(funktionstyp)

        # 3. Instanz erstellen und zurückgeben
        return spezialisierte_klasse(eingabe, **kwargs)
```

### **Wrapper-API Implementierung**

```python
# api.py - Schülerfreundliche Schnittstelle
def Nullstellen(funktion):
    """Berechne die Nullstellen einer Funktion.

    Args:
        funktion: Ein Funktionsobjekt

    Returns:
        list: Liste der Nullstellen

    Example:
        >>> f = Funktion("x^2 - 4")
        >>> xs = Nullstellen(f)  # [-2.0, 2.0]
    """
    return funktion.nullstellen()
```

### **Visuelle Konsistenz**

```python
# Alle Visualisierungsmethoden folgen dem gleichen Pattern
def zeige_funktion_plotly(self, x_bereich=None, **kwargs):
    """Erstelle Plotly-Visualisierung mit konsistentem Styling."""
    # 1. Standard-Konfiguration
    config = self._get_default_plot_config()

    # 2. Bereich anpassen
    if x_bereich is None:
        x_bereich = self._empfohlener_bereich()

    # 3. Plot erstellen
    fig = self._erstelle_plotly_figure(x_bereich, config)

    # 4. Mathematische Korrektheit sicherstellen
    fig.update_layout(
        scaleanchor="y",
        scaleratio=1,
        xaxis=dict(zeroline=True, zerolinewidth=2),
        yaxis=dict(zeroline=True, zerolinewidth=2)
    )

    return fig
```

## 🎯 Qualitätsstandards

### **Code Quality**

- [ ] **Type Safety**: 100% ty check bestanden
- [ ] **Style**: 100% ruff formatiert
- [ ] **Complexity**: Zyklomatische Komplexität < 10
- [ ] **Documentation**: Alle öffentlichen APIs dokumentiert

### **Test Quality**

- [ ] **Coverage**: > 80% für alle Module
- [ ] **Integration**: End-to-End Tests für kritische Pfade
- [ ] **Performance**: Tests mit großen Eingaben
- [ ] **Edge Cases**: Grenzwerte und Fehlerfälle testen

### **Documentation Quality**

- [ ] **API Docs**: Vollständige Funktionsbeschreibungen
- [ ] **Examples**: Ausführbare Beispiele für alle Features
- [ ] **Tutorials**: Schritt-für-Schritt Anleitungen
- [ ] **Changelog**: Regelmäßige Updates bei Änderungen

---

**Wichtig**: Dieses Development Handbook ist die zentrale Referenz für alleContributor:innen. Es muss bei Architekturänderungen始终保持 aktualisiert werden.

**Letztes Update**: Oktober 2024
**Maintainer**: Development Team
