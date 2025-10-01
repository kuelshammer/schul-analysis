# Schul-Analysis Framework

Ein Python Framework für Schul-Analysis mit exakter Berechnung und Marimo-Integration, entwickelt für Mathematiklehrer und Schüler.

## Features

- **Exakte mathematische Berechnungen** mit SymPy (keine numerischen Approximationen)
- **Flexible Konstruktoren**: String (`"x^3-2x+1"`), Liste (`[1, 0, -2, 1]`) oder Dictionary
- **Detaillierte Lösungswege** als Markdown mit LaTeX-Unterstützung
- **Marimo-Integration** für interaktive Notebooks
- **Pädagogische Darstellung** mit deutschen Methodennamen

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
uv sync --group viz      # Visualisierung (matplotlib, plotly)
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

- `viz`: matplotlib, plotly, numpy (für Visualisierungen)
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

f = GanzrationaleFunktion("x^2-4x+5")

# LaTeX-Darstellung in Marimo
mo.md(f"## Funktion: $$f(x) = {f.term_latex()}$$")

# Interaktiver Lösungsweg
f.zeige_nullstellen_marimo(real=True)
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
