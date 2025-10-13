# CHANGELOG

Alle wichtigen Änderungen am Schul-Analysis Framework werden in dieser Datei dokumentiert.

Das Format folgt [Keep a Changelog](https://keepachangelog.com/de-DE/1.0.0/),
und dieses Projekt hält sich an [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unveröffentlicht]

### Removed

- 🗑️ **Legacy System**: Komplette Entfernung der BackwardCompatibilityAdapter-Klasse
- 🧹 **Legacy Properties**: Entfernung des `legacy` Property aus der Funktion-Klasse
- 📋 **Legacy Mapping**: Entfernung des `_backward_compatibility_map` für doppelte API-Zugriffe
- 🔥 **Code Cleanup**: Entfernung von ~133 Zeilen veralteten Legacy-Codes
- 🎯 **API-Vereinheitlichung**: Klare, konsistente API ohne Legacy-Baggage

### Geplant

- Umfassende Sphinx-Dokumentation
- Jupyter Notebook Integration
- Erweiterte Statistik-Funktionen
- Performance-Optimierungen für große Funktionen

## [0.2.0] - 2024-10-06

### Added

- 🔥 **Magic Factory Pattern**: Automatische Funktionstyp-Erkennung mit `Funktion()` Klasse
- 🆕 **setze_parameter() Methode**: Intuitive Parameter-Substitution für parametrisierte Funktionen
- 🎯 **Prime-Notation**: `f' = Ableitung(f)` für natürliche mathematische Notation
- 📊 **Erweiterte Visualisierung**: Perfekte Plotly-Darstellungen mit Aspect Ratio Control
- 🧮 **Taylor-Reihen**: Vollständige Integration von Taylor-Polynomen und Approximation
- 🔍 **Schmiegkurven**: Automatische Erzeugung von Schmiegparabeln durch Punkte
- ⚖️ **Lineare Gleichungssysteme**: Intuitive LGS-Lösung mit Funktionsbedingungen
- 📐 **Trigonometrische Funktionen**: Umfassende Unterstützung für sin, cos, tan etc.
- 🎓 **Deutsche Wrapper-API**: `Nullstellen(f)`, `Ableitung(f)`, `Extrema(f)` etc.

### Changed

- 🏗️ **Komplette Architektur-Überarbeitung**: Migration zu Magic Factory Pattern
- 🔧 **Modernes Toolchain**: Umstellung auf uv als Paketmanager mit dependency groups
- 📚 **Dokumentation**: Komplette Überarbeitung von README.md und Entwickler-Richtlinien
- 🧪 **Testing-Strategie**: Umstellung auf pytest mit Coverage und modernen Test-Patterns
- 🎨 **Visualisierungs-Strategie**: Klare Trennung zwischen Plotly (Mathematik) und Altair (Statistik)
- 🏷️ **API-Konsistenz**: Durchgängig deutsche Methoden- und Funktionsnamen

### Fixed

- ✅ **Aspect Ratio Probleme**: Plotly zeigt jetzt perfekte mathematisch korrekte Graphen
- 🔢 **Numerische Genauigkeit**: SymPy-Integration vermeidet Approximationsfehler
- 🚫 **Fehlerbehandlung**: Deutliche deutsche Fehlermeldungen anstelle technischer Meldungen
- 📋 **String-Vergleiche**: SymPy.equals() statt String-Vergleichen in Tests
- 🔗 **Import-Struktur**: Klare Modul-Hierarchie mit zentraler **init**.py

### Technical Details

- **21 Module**: Vollständige Modularisierung mit spezialisierten Funktionstypen
- **80+ Funktionen**: Umfassende mathematische Analyse-Bibliothek
- **32 Testdateien**: >80% Test-Coverage mit modernen Test-Patterns
- **uv Integration**: Moderne Paketverwaltung mit dependency groups
- **Type Safety**: Vollständige Type Hinting und ty-Integration

### Migration Guide für 0.1.0 → 0.2.0

#### Alte Syntax (veraltet)

```python
# Funktionserstellung mit spezifischen Klassen
f = GanzrationaleFunktion("x^2 - 4x + 3")
g = LineareFunktion("2x + 3")

# Methodenaufrufe
nullstellen = f.nullstellen()
ableitung = f.ableitung()
```

#### Neue Syntax (empfohlen)

```python
# Automatische Typ-Erkennung mit Magic Factory
f = Funktion("x^2 - 4x + 3")        # → GanzrationaleFunktion
g = Funktion("2x + 3")             # → LineareFunktion

# Natürliche mathematische Syntax
xs = Nullstellen(f)                 # Funktion statt Methode
f_strich = Ableitung(f)             # f' = df/dx
print(f(2))                        # f(2) statt f.wert(2)

# Parameter-Substitution
param_f = Funktion("a*x^2 + b*x + c")
f2 = param_f.setze_parameter(a=2, b=3)
result = param_f.setze_parameter(a=2)(4)  # f[2](4)
```

#### Installation

```bash
# Alte Methode (veraltet)
pip install -e .

# Neue Methode mit uv
uv sync --group viz-math    # Mit Visualisierung
uv sync --all-groups        # Vollständige Entwicklungsumgebung
```

## [0.1.0] - 2024-09-30

### Added

- 🎉 **Initial Release**: Erstes öffentliches Release des Frameworks
- 📊 **Grundlegende Funktionalitäten**: Lineare, quadratische und polynomiale Funktionen
- 🎨 **Plotly-Integration**: Erste mathematische Visualisierungen
- 🧮 **SymPy-Integration**: Symbolische Mathematik-Engine
- 📝 **Dokumentation**: Initiale README.md und Entwickler-Richtlinien

### Features

- Ganzrationale Funktionen beliebigen Grades
- Nullstellenberechnung mit Lösungswege
- Ableitungen aller Ordnungen
- Extremstellen- und Wendepunktanalyse
- Einfache Plotly-Visualisierungen
- Marimo-Notebook Integration

### Technical Stack

- Python 3.11+
- SymPy für symbolische Berechnungen
- Plotly für Visualisierungen
- Marimo für interaktive Notebooks
- pytest für Testing

---

## 📋 Versions-Strategie

### MAJOR Version (X.0.0)

- Breaking Changes in der API
- Grundlegende Architekturänderungen
- Entfernung von veralteten Funktionen

### MINOR Version (X.Y.0)

- Neue Features (rückwärtskompatibel)
- Erweiterung der Funktionalität
- Verbesserung der Benutzererfahrung

### PATCH Version (X.Y.Z)

- Bugfixes und Fehlerkorrekturen
- Performance-Verbesserungen
- Dokumentations-Updates

## 🔄 Update-Empfehlungen

### Für Lehrer

- **Stabile Versionen**: MAJOR.MINOR (z.B. 0.2.x)
- **Feature-Updates**: MINOR-Versionen enthalten neue nützliche Funktionen
- **Sicherheits-Updates**: Immer PATCH-Versionen installieren

### Für Entwickler

- **Latest Stable**: Aktuellste stabile Version für neue Entwicklungen
- **Breaking Changes**: MAJOR-Versionen erfordern Code-Anpassungen
- **Test-Compatibility**: Neue Versionen immer mit Test-Suite prüfen

### Für Systemadministratoren

- **Production**: Nur getestete MAJOR.MINOR Versionen
- **Development**: Latest Stable mit vollständiger Test-Abdeckung
- **Dependencies**: Immer `uv.lock` für reproduzierbare Builds verwenden

---

**Hinweis**: Diese CHANGELOG wird bei jedem Release automatisch aktualisiert.
Für genauere Informationen über spezifische Commits siehe [Git History](https://github.com/kuelshammer/schul-analysis/commits/main).
