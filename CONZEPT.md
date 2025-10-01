# Konzept: Python Framework für Schul-Analysis mit Marimo-Integration

## 1. Ausgangssituation und Zielsetzung

### 1.1 Problemstellung

Als Mathematiklehrer benötige ich ein Python-System, das:

- Typische Schul-Analysis Aufgaben exakt berechnen kann
- Detaillierte Lösungswege als Markdown in Marimo-Notebooks ausgibt
- Für den Unterricht geeignet ist und Schülern Schritt-für-Schritt-Erklärungen liefert

### 1.2 Kernanforderungen

- Exakte mathematische Berechnungen (keine numerischen Approximationen)
- Pädagogisch wertvolle Darstellung von Lösungswegen
- Integration mit Marimo-Notebooks für interaktive Nutzung
- Unterstützung typischer Schul-Analysis Themen

## 2. Forschungsergebnisse

### 2.1 Typische Schul-Analysis Aufgaben (ganzrationale Funktionen)

Basierend auf der Analyse von Schulmaterialien:

**Hauptmethoden für Nullstellenberechnung:**

- Ausklammern und Satz vom Nullprodukt
- Polynomdivision und Horner-Schema
- Substitution bei höheren Graden
- Lineare Faktorzerlegung
- Mitternachtsformel (quadratische Funktionen)
- Spezielle Verfahren für kubische Funktionen (Cardano)

**Typische Aufgabenstellungen:**

- Nullstellenbestimmung bis 4. Grades
- Schnittstellen mit Koordinatenachsen
- Kurvendiskussion (Wertebereich, Extremstellen, Wendepunkte)
- Funktionsgleichungen aus Eigenschaften rekonstruieren

### 2.2 Technologie-Stack

#### 2.2.1 SymPy als Kernbibliothek

**Vorteile für den Bildungsbereich:**

- Open-source und kostenlos
- Symbolische Berechnungen (exakte Ergebnisse)
- Ausgereifte Polynom-Operationen
- LaTeX-Ausgabe für mathematische Darstellung
- Gut dokumentiert und aktiv gepflegt

**Relevante Features:**

- `sympy.Poly` für Polynom-Operationen
- `sympy.solve` für Gleichungslösungen
- `sympy.diff` für Ableitungen
- `sympy.factor` für Faktorisierung
- `sympy.expand` für Ausmultiplizieren

#### 2.2.2 Marimo-Notebooks für die Präsentation

**Key Features für den Matheunterricht:**

- Reaktive Ausführung (automatische Updates)
- Git-freundlich (reine Python-Dateien)
- Interaktive Elemente möglich
- Markdown-Integration mit LaTeX-Unterstützung
- Export zu verschiedenen Formaten

**Markdown-Funktionalitäten:**

- `mo.md()` für dynamische Markdown-Ausgabe
- LaTeX-Integration für mathematische Formeln
- Unterstützung für Tabellen und strukturierten Inhalt
- Bilder aus `public/` Ordner einbindbar

## 3. Architektur-Entwurf

### 3.1 Klassenhierarchie

#### 3.1.1 Basisklasse `MathematischeFunktion`

```python
class MathematischeFunktion(ABC):
    """Abstrakte Basisklasse für alle mathematischen Funktionen"""

    @abstractmethod
    def term(self) -> str:
        """Gibt den Funktionsterm als String zurück"""
        pass

    @abstractmethod
    def ableitung(self, ordnung: int = 1) -> 'MathematischeFunktion':
        """Berechnet die Ableitung gegebener Ordnung"""
        pass

    @abstractmethod
    def nullstellen(self, real: bool = True) -> List[Union[float, complex]]:
        """Berechnet alle Nullstellen exakt

        Args:
            real: Wenn True, werden nur reelle Nullstellen zurückgegeben
                   Wenn False, werden auch komplexe Nullstellen berücksichtigt
        """
        pass

    @abstractmethod
    def wertebereich(self) -> Tuple[Optional[float], Optional[float]]:
        """Bestimmt den Wertebereich"""
        pass
```

#### 3.1.2 Klasse `GanzrationaleFunktion`

```python
class GanzrationaleFunktion(MathematischeFunktion):
    """Klasse für ganzrationale Funktionen (Polynome)"""

    def __init__(self, input_data):
        """
        Flexibler Konstruktor, der verschiedene Eingabeformate unterstützt

        Args:
            input_data: Kann sein:
                - String: "x^3-x^2+5" oder "x**3-x**2+5"
                - Liste: [1, -1, 0, 5] für x³ - x² + 0x + 5
                - Dictionary: {3: 1, 2: -1, 0: 5} für x³ - x² + 5
        """
        if isinstance(input_data, str):
            self.koeffizienten = self._parse_string_to_coeffs(input_data)
        elif isinstance(input_data, list):
            self.koeffizienten = input_data
        elif isinstance(input_data, dict):
            self.koeffizienten = self._dict_to_coeffs(input_data)
        else:
            raise TypeError("Nur String, Liste oder Dictionary unterstützt")

        self.grad = len(self.koeffizienten) - 1
        self._sympy_poly = None  # Internes SymPy-Polynom

    def _parse_string_to_coeffs(self, term_str: str) -> List[float]:
        """Konvertiert mathematischen String zu Koeffizientenliste"""
        import sympy as sp

        # Syntax bereinigen: ^ -> **
        cleaned_str = term_str.replace('^', '**')

        try:
            # String zu SymPy-Ausdruck konvertieren
            expr = sp.sympify(cleaned_str)
            x = sp.Symbol('x')

            # Polynom erstellen und Koeffizienten extrahieren
            poly = sp.Poly(expr, x)
            return poly.all_coeffs()
        except Exception as e:
            raise ValueError(f"Ungültiger Term '{term_str}': {e}")

    def _dict_to_coeffs(self, coeff_dict: dict) -> List[float]:
        """Konvertiert {Potenz: Koeffizient} zu Koeffizientenliste"""
        if not coeff_dict:
            return [0]

        max_grad = max(coeff_dict.keys())
        coeffs = [0.0] * (max_grad + 1)

        for potenz, koeff in coeff_dict.items():
            coeffs[max_grad - potenz] = koeff

        return coeffs

    @property
    def sympy_poly(self) -> sympy.Poly:
        """Lazy-Initialisierung des SymPy-Polynoms"""
        if self._sympy_poly is None:
            x = sympy.Symbol('x')
            term = sum(k * x**i for i, k in enumerate(reversed(self.koeffizienten)))
            self._sympy_poly = sympy.Poly(term, x)
        return self._sympy_poly
```

### 3.2 Methoden für Lösungswege

#### 3.2.1 Lösungswege-Konzept

Jede mathematische Operation hat zwei Methoden:

1. **Berechnungsmethode**: Gibt nur das Ergebnis zurück
2. **Lösungsweg-Methode**: Gibt detaillierte Schritt-für-Schritt-Erklärung als Markdown

#### 3.2.2 Beispiel: Nullstellenberechnung

```python
def nullstellen(self, real: bool = True) -> List[Union[float, complex]]:
    """Berechnet Nullstellen (nur Ergebnis)"""
    if real:
        # Nur reelle Nullstellen zurückgeben
        alle_nullstellen = [complex(n) for n in self.sympy_poly.all_roots()]
        return [n for n in alle_nullstellen if n.imag == 0]
    else:
        # Alle Nullstellen (auch komplexe)
        return [complex(n) for n in self.sympy_poly.all_roots()]

def nullstellen_weg(self, real: bool = True) -> str:
    """Generiert detaillierten Lösungsweg als Markdown

    Args:
        real: Steuert, ob komplexe Nullstellen im Lösungsweg erklärt werden
    """
    schritte = []

    # Schritt 1: Funktion darstellen
    schritte.append(f"## Nullstellenberechnung für f(x) = {self.term()}")

    # Schritt 2: Grad analysieren
    schritte.append(f"### Schritt 1: Grad der Funktion bestimmen")
    schritte.append(f"Die Funktion hat Grad {self.grad}.")

    # Schritt 3: Spezielle Fälle behandeln
    if self.grad == 1:
        schritte.append(self._linearer_weg())
    elif self.grad == 2:
        schritte.append(self._quadratischer_weg())
    elif self.grad >= 3:
        schritte.append(self._hoherer_grad_weg())

    return "\n\n".join(schritte)
```

### 3.3 Marimo-Integration

#### 3.3.1 Marimo-Anzeige Methoden

```python
class GanzrationaleFunktion(MathematischeFunktion):
    # ... vorhandene Methoden ...

    def zeige_nullstellen(self, real: bool = True):
        """Zeigt Nullstellenberechnung in Marimo mit Lösungsweg

        Args:
            real: Steuert die Art der Nullstellendarstellung
        """
        import marimo as mo

        # Berechnung durchführen
        nullstellen = self.nullstellen(real)
        weg = self.nullstellen_weg(real)

        # Interaktive Ausgabe
        output = f"""
# {self.term()}
## Nullstellen: {nullstellen}

{mo.md(weg)}
"""
        return mo.md(output)
```

## 4. Implementierungsstrategie

### 4.1 Phase 1: Grundlegende Struktur

1. **Basisklassen** implementieren
2. **SymPy-Integration** aufbauen
3. **Grundlegende Polynom-Operationen**

### 4.2 Phase 2: Kernfunktionen

1. **Nullstellenberechnung** für alle Grade
2. **Ableitungen** beliebiger Ordnung
3. **Funktionsanalyse** (Wertebereich, Symmetrie)

### 4.3 Phase 3: Lösungswege

1. **Schritt-für-Schritt-Dokumentation**
2. **Mathematische Erklärungen**
3. **Beispiele und Gegenbeispiele**

### 4.4 Phase 4: Marimo-Integration

1. **Interaktive Notebooks**
2. **Visualisierungen**
3. **Export-Funktionalitäten**

## 5. Detaillierte Methodenplanung

### 5.1 Ganzrationale Funktionen - Kompletter Methodensatz

#### 5.1.1 Konstruktoren

```python
def __init__(self, input_data):
    """
    Flexibler Konstruktor für verschiedene Eingabeformate

    Args:
        input_data: Kann sein:
            - String: "x^3-x^2+5" oder "x**3-x**2+5"
            - Liste: [1, -1, 0, 5] für x³ - x² + 0x + 5
            - Dictionary: {3: 1, 2: -1, 0: 5} für x³ - x² + 5

    Examples:
        >>> f1 = GanzrationaleFunktion("x^3-2x+1")
        >>> f2 = GanzrationaleFunktion([1, 0, -2, 1])
        >>> f3 = GanzrationaleFunktion({3: 1, 1: -2, 0: 1})
    """
    # Automatische Erkennung und Konvertierung des Eingabeformats

@classmethod
def aus_koeffizienten(cls, koeffizienten: List[float]) -> 'GanzrationaleFunktion':
    """Erstellt Funktion aus Koeffizientenliste (Alternative Syntax)"""

@classmethod
def aus_nullstellen(cls, nullstellen: List[float], faktor: float = 1) -> 'GanzrationaleFunktion':
    """Erstellt Funktion aus Nullstellen (Lineare Faktorzerlegung)"""

@classmethod
def aus_term(cls, term_str: str) -> 'GanzrationaleFunktion':
    """Alternative Methode zum Parsen aus mathematischem Term-String"""
```

#### 5.1.2 Analytische Methoden

```python
def wert(self, x: float) -> float:
    """Berechnet Funktionswert an Stelle x"""

def ableitung(self, ordnung: int = 1) -> 'GanzrationaleFunktion':
    """Berechnet Ableitung gegebener Ordnung"""

def nullstellen(self) -> List[Union[float, complex]]:
    """Berechnet alle Nullstellen exakt"""

def extremstellen(self) -> List[Tuple[float, str]]:
    """Berechnet Extremstellen mit Art (Maximum/Minimum)"""

def wendestellen(self) -> List[float]:
    """Berechnet Wendestellen"""

def wertebereich(self) -> Tuple[Optional[float], Optional[float]]:
    """Bestimmt den Wertebereich"""

def symmetrie(self) -> str:
    """Überprüft Symmetrie (ungerade/gerade/keine)"""
```

#### 5.1.3 Lösungswege-Methoden

```python
def ableitung_weg(self, ordnung: int = 1) -> str:
    """Generiert Lösungsweg für Ableitungsberechnung"""

def nullstellen_weg(self, real: bool = True) -> str:
    """Generiert Lösungsweg für Nullstellenberechnung

    Args:
        real: Steuert, ob komplexe Nullstellen erklärt werden
    """

def extremstellen_weg(self) -> str:
    """Generiert Lösungsweg für Extremstellenberechnung"""

def kurvendiskussion_weg(self) -> str:
    """Vollständige Kurvendiskussion mit Lösungsweg"""
```

### 5.2 Spezielle Lösungsstrategien nach Grad

#### 5.2.1 Lineare Funktionen (Grad 1)

```python
def _linearer_weg(self) -> str:
    """Lösungsweg für lineare Funktionen"""
    a, b = self.koeffizienten[0], self.koeffizienten[1]

    schritte = [
        "### Schritt 2: Lineare Gleichung lösen",
        f"f(x) = {a}x + {b} = 0",
        f"{a}x = {-b}",
        f"x = {-b/a}"
    ]

    return "\n".join(schritte)
```

### 5.3 Methodengruppen und detaillierte Dokumentation

Für jede Hauptfunktionalität des Frameworks gibt es separate Dokumentationen mit detaillierten Implementierungsvorschlägen:

#### 5.3.1 Nullstellen-Methoden

**Datei:** `docs/methoden/nullstellen-methoden.md`

**Methoden:**

- `nullstellen(real: bool = True)` - Reine Berechnung mit Option für reelle/ komplexe Lösungen
- `nullstellen_weg(real: bool = True)` - Detaillierter Lösungsweg als Markdown
- `zeige_nullstellen(real: bool = True)` - Interaktive Marimo-Anzeige

**Besonderheiten:**

- Unterschiedliche Lösungsstrategien je nach Grad (linear, quadratisch, höher)
- Diskriminantenanalyse für quadratische Funktionen
- Optionale Darstellung komplexer Lösungen
- Schritt-für-Schritt-Erklärungen mit Mitternachtsformel

#### 5.3.2 Ableitungs-Methoden

**Datei:** `docs/methoden/ableitungs-methoden.md`

**Methoden:**

- `ableitung(ordnung: int = 1)` - Ableitung beliebiger Ordnung
- `ableitung_weg(ordnung: int = 1)` - Lösungsweg mit Ableitungsregeln
- `zeige_ableitung(ordnung: int = 1)` - Interaktive Ableitungsdarstellung

**Besonderheiten:**

- Potenzregel, Faktorregel, Summenregel
- Höhere Ableitungen (f', f'', f''', ...)
- Rekursive Berechnung
- Visualisierung von Funktion und Ableitung

#### 5.3.3 Extremstellen-Methoden

**Datei:** `docs/methoden/extremstellen-methoden.md`

**Methoden:**

- `extremstellen()` - Berechnung aller Maxima/Minima
- `extremstellen_weg()` - Lösungsweg mit f'(x) = 0 und f''(x) Analyse
- `zeige_extremstellen()` - Interaktive Darstellung mit Graph

**Besonderheiten:**

- Kritische Punkte finden (f'(x) = 0)
- Artbestimmung durch zweite Ableitung oder Vorzeichenwechsel
- Behandlung von Sattelpunkten
- Monotonieanalyse

#### 5.3.4 Kurvendiskussion-Methoden

**Datei:** `docs/methoden/kurvendiskussion-methoden.md`

**Methoden:**

- `kurvendiskussion()` - Vollständige Analyse als Dictionary
- `kurvendiskussion_weg()` - Kompletter Lösungsweg als Markdown
- `zeige_kurvendiskussion()` - Umfassende interaktive Präsentation

**Besonderheiten:**

- Strukturierter Ablauf: Definitionsbereich → Wertebereich → Symmetrie → Nullstellen → Ableitungen → Extremstellen → Monotonie → Krümmung → Verhalten im Unendlichen
- Zusammenfassende Tabelle aller Eigenschaften
- Schrittweiser Aufbau des Funktionsgraphen
- Export-Funktionalitäten

## 5.4 Didaktischer Nutzen der Methodenstruktur

### 5.4.1 Dreistufiger Methodenaufbau

Jede Funktionalität folgt dem gleichen Muster:

1. **Berechnungsmethode** (`methode()`) - Schnelle Ergebnisrückgabe
2. **Lösungsweg-Methode** (`methode_weg()`) - Detaillierte Schritt-für-Schritt-Erklärung
3. **Interaktive Methode** (`zeige_methode()`) - Marimo-Integration mit Visualisierung

### 5.4.2 Progressive Einführung komplexer Zahlen

- **real=True (Standard)**: Fokus auf reelle Lösungen für Einsteiger
- **real=False**: Komplexe Lösungen für Fortgeschrittene und Oberstufe
- **Flexible Anpassung**: Lehrer kann je nach Klasse und Thema wählen

### 5.4.3 Unterschiedliche Einsatzszenarien

- **Frontalunterricht**: zeige_methode() für Demonstration am Beamer
- **Individualarbeit**: methode() für Selbstkontrolle von Lösungen
- **Gruppenarbeit**: methode_weg() als Referenz für Lösungsansätze

## 5.5 Konkrete Beispiele und Anwendung

Detaillierte Beispiele für die Anwendung aller Methoden finden Sie in den separaten Dokumentationsdateien:

- **Nullstellen**: `docs/methoden/nullstellen-methoden.md`
- **Ableitungen**: `docs/methoden/ableitungs-methoden.md`
- **Extremstellen**: `docs/methoden/extremstellen-methoden.md`
- **Kurvendiskussion**: `docs/methoden/kurvendiskussion-methoden.md`

Jede Datei enthält:

- Vollständige Methodensignaturen und Implementierungsvorschläge
- Detaillierte Code-Beispiele und Testfälle
- Didaktische Hinweise für den Unterrichtseinsatz
- Fehlerbehandlung und Spezialfälle

#### 5.2.2 Quadratische Funktionen (Grad 2)

```python
def _quadratischer_weg(self) -> str:
    """Lösungsweg für quadratische Funktionen mit Mitternachtsformel"""
    a, b, c = self.koeffizienten[0], self.koeffizienten[1], self.koeffizienten[2]

    schritte = [
        "### Schritt 2: Mitternachtsformel anwenden",
        f"f(x) = {a}x² + {b}x + {c} = 0",
        "",
        "**Mitternachtsformel:**",
        "$$x = \\frac{{-b \\pm \\sqrt{{b^2 - 4ac}}}}{{2a}}$$",
        "",
        f"Einsetzen: a = {a}, b = {b}, c = {c}",
        f"**Diskriminante:** D = b² - 4ac = {b}² - 4·{a}·{c} = {b**2 - 4*a*c}"
    ]

    # Analyse der Diskriminante
    D = b**2 - 4*a*c
    if D > 0:
        schritte.extend([
            f"D > 0, also gibt es zwei reelle Nullstellen:",
            f"$x_1 = \\frac{{-{b} + \\sqrt{{{D}}}}}{{2·{a}}} = \\frac{{-{b} + \\sqrt{{{D}}}}}{{{2*a}}}$",
            f"$x_2 = \\frac{{-{b} - \\sqrt{{{D}}}}}{{2·{a}}} = \\frac{{-{b} - \\sqrt{{{D}}}}}{{{2*a}}}$"
        ])
    elif D == 0:
        schritte.extend([
            f"D = 0, also gibt es eine doppelte Nullstelle:",
            f"$x = \\frac{{-{b}}}{{2·{a}}} = \\frac{{-{b}}}{{{2*a}}}$"
        ])
    else:
        schritte.extend([
            f"D < 0, also gibt es keine reellen Nullstellen",
            f"Komplexe Nullstellen: $x = \\frac{{-{b} \\pm i\\sqrt{{{|D|}}}}}{{2·{a}}}$"
        ])

    return "\n".join(schritte)
```

#### 5.2.3 Höhere Grade (≥ 3)

```python
def _hoherer_grad_weg(self) -> str:
    """Lösungsweg für Funktionen höheren Grades"""
    schritte = [
        "### Schritt 2: Strategie für höhere Grade",
        f"Für Polynome vom Grad {self.grad} wenden wir folgende Strategie an:",
        ""
    ]

    # Suche nach rationalen Nullstellen
    schritte.append("#### a) Suche nach rationalen Nullstellen")
    schritte.append("Mögliche rationale Nullstellen sind Teiler des absoluten Glieds durch Teiler des Leitkoeffizienten.")

    # Polynomdivision
    schritte.append("#### b) Polynomdivision")
    schritte.append("Gefundene Nullstellen werden ausdividiert, um den Grad zu reduzieren.")

    # Spezialfälle
    if self.grad == 3:
        schritte.append("#### c) Kubische Gleichung")
        schritte.append("Nach Reduktion auf quadratische Gleichung kann die Mitternachtsformel angewendet werden.")

    return "\n".join(schritte)
```

## 6. Didaktische Konzeption

### 6.1 Pädagogische Prinzipien

#### 6.1.1 Schritt-für-Schritt-Erklärungen

- **Mathematische Korrektheit**: Exakte Berechnungen, keine Vereinfachungen
- **Verständlichkeit**: Klare Sprache, angemessene Fachbegriffe
- **Progression**: Von einfachen zu komplexen Konzepten
- **Visualisierung**: Graphische Darstellungen wo sinnvoll

#### 6.1.2 Deutsche Methodennamen für bessere Verständlichkeit

- **Intuitive Bedienung**: Deutsche Begriffe entsprechen dem Schulunterricht
- **Kognitive Entlastung**: Keine zusätzlichen englischen Fachbegriffe nötig
- **Konsistenz**: Alle Methoden folgen dem gleichen Benennungsschema
  - `nullstellen()` für reine Berechnung
  - `nullstellen_weg()` für Lösungswege
  - `zeige_nullstellen()` für interaktive Darstellung
- **Transferfähigkeit**: Schüler können Methodennamen leicht merken und übertragen

#### 6.1.3 Interaktive Elemente

- **Veränderliche Parameter**: Schüler können Koeffizienten ändern
- **Sofortiges Feedback**: Ergebnisse und Lösungswege aktualisieren sich
- **Selbstkontrolle**: Möglichkeit, eigene Lösungen zu überprüfen

### 6.2 Unterrichtsszenarien

#### 6.2.1 Frontalunterricht

- **Demonstration**: Lehrer zeigt Lösungswege am Beamer
- **Gemeinsames Lösen**: Interaktive Bearbeitung mit Klasse
- **Ergebnissicherung**: Ausdrucke als Referenzmaterial

#### 6.2.2 Individualarbeit

- **Übungen**: Schüler bearbeiten Aufgaben selbstständig
- **Selbstüberprüfung**: Automatische Kontrolle der Ergebnisse
- **Differenzierung**: Unterschiedliche Schwierigkeitsgrade

#### 6.2.3 Gruppenarbeit

- **Problem-Based Learning**: Komplexe Aufgaben in Gruppen lösen
- **Präsentation**: Ergebnisse und Lösungswege präsentieren
- **Diskussion**: Vergleich verschiedener Lösungsansätze

## 7. Technische Umsetzungsdetails

### 7.1 Abhängigkeiten und Setup

#### 7.1.1 Python-Pakete

```python
# requirements.txt
sympy>=1.12
marimo>=0.1.0
numpy>=1.21.0
matplotlib>=3.5.0
```

#### 7.1.2 Projektstruktur

```
schul-analysis/
├── schul_analysis/
│   ├── __init__.py
│   ├── basis/
│   │   ├── __init__.py
│   │   ├── mathematische_funktion.py
│   │   └── ausnahmen.py
│   ├── ganzrationale/
│   │   ├── __init__.py
│   │   ├── ganzrationale_funktion.py
│   │   └── loesungswege.py
│   ├── exponential/
│   │   └── exponential_funktion.py
│   ├── trigonometrisch/
│   │   └── trigonometrische_funktion.py
│   └── utils/
│       ├── markdown_generator.py
│       └── math_formatter.py
├── notebooks/
│   ├── grundlagen_ganzrationale.py
│   ├── nullstellen_berechnung.py
│   └── kurvendiskussion.py
├── tests/
│   ├── test_ganzrationale.py
│   └── test_loesungswege.py
└── setup.py
```

### 7.2 Code-Qualität und Testing

#### 7.2.1 Typ-Hints

```python
from typing import List, Tuple, Union, Optional
import sympy as sp

class GanzrationaleFunktion:
    def nullstellen(self) -> List[Union[float, complex]]:
        """Berechnet alle Nullstellen exakt"""
        pass
```

#### 7.2.2 Fehlerbehandlung

```python
class MathematischeFunktionError(Exception):
    """Basisklasse für mathematische Fehler"""
    pass

class NullstellenBerechnungFehler(MathematischeFunktionError):
    """Fehler bei der Nullstellenberechnung"""
    pass

class GradZuHochFehler(MathematischeFunktionError):
    """Fehler bei zu hohem Grad für bestimmte Methoden"""
    pass
```

#### 7.2.3 Teststrategie

```python
# tests/test_ganzrationale_funktion.py
import pytest
from schul_analysis.ganzrationale import GanzrationaleFunktion

class TestGanzrationaleFunktion:
    def test_lineare_funktion(self):
        f = GanzrationaleFunktion([2, -4])  # 2x - 4
        assert f.nullstellen() == [2.0]

    def test_quadratische_funktion(self):
        f = GanzratonaleFunktion([1, -3, 2])  # x² - 3x + 2
        nullstellen = f.nullstellen()
        assert sorted(nullstellen) == [1.0, 2.0]
```

## 8. Erweiterungsmöglichkeiten

### 8.1 Weitere Funktionstypen

#### 8.1.1 Exponentialfunktionen

```python
class ExponentialFunktion(MathematischeFunktion):
    def __init__(self, basis: float, koeffizient: float = 1):
        self.basis = basis
        self.koeffizient = koeffizient

    def term(self) -> str:
        return f"{self.koeffizient} · {self.basis}^x"
```

#### 8.1.2 Trigonometrische Funktionen

```python
class SinusFunktion(MathematischeFunktion):
    def __init__(self, amplitude: float, phase: float = 0):
        self.amplitude = amplitude
        self.phase = phase

    def term(self) -> str:
        return f"{self.amplitude} · sin(x + {self.phase})"
```

### 8.2 Erweiterte Features

#### 8.2.1 Graphische Darstellungen

- **Plotting-Integration** mit matplotlib
- **Interaktive Graphen** in Marimo
- **Animationsmöglichkeiten**

#### 8.2.2 KI-Unterstützung

- **Fehlererkennung** in Schülerlösungen
- **Personalisierte Hinweise**
- **Schwierigkeitsgrad-Adaption**

#### 8.2.3 Export-Funktionen

- **PDF-Export** für Arbeitsblätter
- **LaTeX-Export** für Dokumentationen
- **HTML-Export** für Webintegration

## 9. Implementierungsplan

### 9.1 Meilensteine

#### Meilenstein 1: Grundgerüst (Woche 1-2)

- [ ] Projektsetup und Abhängigkeiten
- [ ] Basisklassen und abstrakte Methoden
- [ ] Grundlegende SymPy-Integration
- [ ] Einfache Tests

#### Meilenstein 2: Ganzrationale Funktionen (Woche 3-4)

- [ ] GanzrationaleFunktion Klasse
- [ ] Nullstellenberechnung für Grad 1-2
- [ ] Grundlegende Lösungswege
- [ ] Unit Tests

#### Meilenstein 3: Erweiterte Funktionen (Woche 5-6)

- [ ] Nullstellen für höhere Grade
- [ ] Ableitungen und Kurvendiskussion
- [ ] Komplexe Lösungswege
- [ ] Marimo-Integration

#### Meilenstein 4: Dokumentation und Examples (Woche 7-8)

- [ ] Umfassende Dokumentation
- [ ] Beispiel-Notebooks
- [ ] Benutzerhandbuch
- [ ] Performance-Optimierung

### 9.2 Risikobewertung

#### 9.2.1 Technische Risiken

- **SymPy-Komplexität**: Einarbeitungszeit erforderlich
- **Marimo-Integration**: Neue Technologie, mögliche Kompatibilitätsprobleme
- **Performance**: Symbolische Berechnungen können langsam sein

#### 9.2.2 Didaktische Risiken

- **Überfrachtung**: Zu viele Features können verwirren
- **Abstraktion**: Zu technische Darstellung für Schüler
- **Flexibilität**: Muss verschiedene Lehrpläne unterstützen

## 10. Zusammenfassung und Ausblick

### 10.1 Kernvorteile des Konzepts

1. **Exakte Mathematik**: Keine Kompromisse bei mathematischer Korrektheit
2. **Pädagogischer Wert**: Detaillierte Lösungswege für besseres Verständnis
3. **Technologische Aktualität**: Nutzung moderner Python-Ökosysteme
4. **Flexibilität**: Erweiterbar für weitere Funktionstypen und Anwendungen

### 10.2 Langfristige Vision

Das Framework soll sich zu einer umfassenden Plattform für mathematische Bildung entwickeln, die über die reine Analysis hinausgeht und weitere Bereiche der Schulmathematik abdeckt.

### 10.3 Nächste Schritte

1. **Konzeptvalidierung**: Diskussion mit anderen Mathematiklehrern
2. **Prototyp-Entwicklung**: Erste implementierte Version
3. **Unterrichtstests**: Einsatz in echten Unterrichtsszenarien
4. **Iterative Verbesserung**: Basierend auf Nutzerfeedback

---

**Erstellt:** 30.09.2025
**Status:** Konzeptphase
**Nächster Schritt:** Implementierungsbeginn nach Freigabe
