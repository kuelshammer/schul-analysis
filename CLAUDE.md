# Schul-Analysis Framework - Development Guidelines

## 🎯 Projekt-Überblick

Python Framework für Schul-Analysis mit exakten Berechnungen, Marimo-Integration und mathematisch korrekter Visualisierung. Entwickelt für Mathematiklehrer und Schüler.

## 🔧 Entwicklungstools & Prinzipien

### **Package Management: uv**
- **Immer `uv` für Python-Pakete verwenden**
- Installation: `uv sync` (Core) oder `uv sync --group viz-math` (für Plotly)
- Neue Pakete hinzufügen: `uv add <package>`
- Dev-Pakete: `uv add --group dev <package>`

### **Code Quality: ruff**
- **Linting**: `uv run ruff check`
- **Formatting**: `uv run ruff format`
- Vor jedem Commit ausführen!
- Konfiguration in `pyproject.toml`

### **Type Checking: ty (Astral)**
- **Type checking**: `uv run ty check`
- Vor jedem Commit ausführen!
- Typos statt mypy verwenden

### **Testing: pytest**
- **Tests ausführen**: `uv run pytest`
- **Mit Coverage**: `uv run pytest --cov=schul_analysis`
- Vor jedem Merge ausführen!

## 🔄 Git Workflow

### **Grundprinzip: Jedes Feature = eigener Branch**
```bash
# 1. Aktuellen Stand commiten
git add .
git commit -m "feat: Implementiere Basis-Klasse"

# 2. Neuen Feature-Branch erstellen
git checkout -b feature/plotly-visualisierung

# 3. Am Feature arbeiten
# ... Code schreiben, testen, commiten ...

# 4. Feature fertigstellen
git checkout main
git merge feature/plotly-visualisierung
git branch -d feature/plotly-visualisierung
```

### **Commit-Konvention**
- **feat**: Neues Feature
- **fix**: Bugfix
- **docs**: Dokumentation
- **style**: Code-Formatierung (ruff)
- **refactor**: Refactoring
- **test**: Tests hinzugefügt/geändert
- **chore**: Build/Tool-Änderungen

**Beispiele:**
```bash
git commit -m "feat: Implementiere perfekte Parabel-Darstellung mit Plotly"
git commit -m "fix: Korrigiere Aspect Ratio in Visualisierung"
git commit -m "docs: Aktualisiere README mit Installationsanleitung"
git commit -m "style: Führe ruff format aus"
```

### **Regelmäßiges Commiten**
- **Vor jeder größeren Änderung**: Stand commiten
- **Nach jedem Feature**: Commit erstellen
- **Vor Merge/Rebase**: Sicherstellen, dass alles committet ist
- **Rollback immer möglich** durch regelmäßige Commits

## 📦 Wichtige Module für die Entwicklung

### **Core Dependencies (immer installiert)**
- `sympy>=1.14.0` - Symbolische Mathematik
- `marimo>=0.16.3` - Interaktive Notebooks

### **Visualization Groups**
- **viz-math**: `plotly>=6.3.0`, `numpy>=2.3.3` (🔥 EMPFOHLEN)
- **viz-stats**: `altair>=5.5.0`, `pandas>=2.3.3` (für Statistik)
- **viz-static**: `matplotlib>=3.8.0` (für Exporte)

### **Development Tools**
- `ruff>=0.13.2` - Linting & Formatting
- `ty>=0.0.1a21` - Type checking (Astral)
- `pytest>=8.4.2` - Testing
- `pytest-cov>=7.0.0` - Coverage

### **Dokumentation**
- `sphinx>=7.0.0` - Dokumentations-Generator
- `sphinx-rtd-theme>=1.3.0` - Theme

## 🏗️ Projektstruktur

```
schul-analysis/
├── src/schul_analysis/          # Source code
│   ├── __init__.py
│   ├── basis/                   # Base classes
│   │   └── __init__.py
│   ├── ganzrationale/           # Polynomial functions
│   │   ├── __init__.py
│   │   └── funktion.py
│   ├── exponential/             # Exponential functions
│   │   ├── __init__.py
│   │   └── funktion.py
│   └── trigonometrisch/         # Trigonometric functions
│       ├── __init__.py
│       └── funktion.py
├── tests/                       # Test files
│   ├── __init__.py
│   ├── test_ganzrationale.py
│   └── fixtures/
├── docs/                        # Documentation
│   ├── conf.py
│   └── source/
├── examples/                    # Example notebooks
│   ├── perfekte_parabel_plotly.py
│   └── grundlagen.py
├── notebooks/                   # Marimo notebooks
├── .gitignore
├── pyproject.toml
├── README.md
└── CLAUDE.md                   # Diese Datei
```

## 🧪 Testing-Strategie

### **Test-Dateien erstellen**
- Jedes Modul bekommt eigene Test-Datei
- Tests in `tests/` Verzeichnis
- Fixtures für häufig genutzte Test-Daten

### **Test-Beispiele**
```python
# tests/test_ganzrationale.py
import pytest
from schul_analysis.ganzrationale import GanzrationaleFunktion

def test_konstruktor_string():
    f = GanzrationaleFunktion("x^2-4x+3")
    assert f.term() == "x^2-4x+3"

def test_nullstellen():
    f = GanzrationaleFunktion([1, -4, 3])
    assert f.nullstellen() == [1.0, 3.0]
```

### **Test-Coverage**
- Mindestens 80% Coverage anstreben
- Regelmäßig mit `pytest --cov` prüfen

## 📋 Entwicklungs-Checkliste

### **Vor dem Coden**
- [ ] Feature-Branch erstellen
- [ ] Letzten Stand commiten
- [ ] Benötigte Pakete mit `uv` installieren

### **Während des Codens**
- [ ] Typos mit `uv run ty check` prüfen
- [ ] Ruff mit `uv run ruff check` und `uv run ruff format` ausführen
- [ ] Tests schreiben und mit `uv run pytest` prüfen

### **Vor dem Commit**
- [ ] Alle Tests bestehen
- [ ] Code formatiert (ruff)
- [ ] Types geprüft (ty)
- [ ] Commit-Nachricht folgt Konvention

### **Nach dem Feature**
- [ ] Branch zu main mergen
- [ ] Feature-Branch löschen
- [ ] Dokumentation aktualisieren

## 🔍 Code-Style-Regeln

### **Python Style**
- PEP 8 konform
- Maximale Zeilenlänge: 88 Zeichen
- Docstrings für alle öffentlichen Methoden
- Type hints verwenden

### **Namenskonventionen**
- Klassen: `PascalCase` (`GanzrationaleFunktion`)
- Methoden: `snake_case` (`zeige_funktion_plotly`)
- Variablen: `snake_case` (`koeffizienten`)
- Konstanten: `UPPER_SNAKE_CASE` (`MAX_POINTS`)

### **Dokumentation**
- Deutsch für pädagogische Methoden
- Englisch für technische Dokumentation
- LaTeX in Docstrings für mathematische Formeln

## 🚀 Deployment

### **Veröffentlichung mit uv**
```bash
# Build
uv build

# Publish zu PyPI
uv publish
```

### **Versionierung**
- Semantic Versioning: `MAJOR.MINOR.PATCH`
- `__version__` in `__init__.py` pflegen
- Changelog in `CHANGELOG.md` führen

## 💡 Best Practices

### **Mathematische Korrektheit**
- Immer SymPy für exakte Berechnungen verwenden
- Keine numerischen Approximationen ohne Warnung
- Aspect Ratio Control bei Plotly Visualisierungen

### **Performance**
- SymPy-Ausdrücke cachen wo möglich
- Komplexe Berechnungen nur bei Bedarf ausführen
- Plotly-Graphen mit vernünftiger Punktanzahl

### **User Experience**
- Intuitive Konstruktoren für Schüler
- Klare Fehlermeldungen
- Gute Visualisierungen mit Erklärungen

---

**Wichtig:** Diese Guidelines immer aktuell halten und bei Änderungen am Workflow anpassen!
