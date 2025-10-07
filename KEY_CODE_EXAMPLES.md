# Key Code Examples for Gemini Review

## 🎯 Magic Factory Pattern (Kernfeature)

### Automatische Typ-Erkennung
```python
# src/schul_analysis/funktion.py - Haupt-Factory
def Funktion(term: Any, variable: str = "x") -> Funktion:
    """
    Magic Factory: Erkennt automatisch den Funktionstyp
    und erstellt die passende Instanz.
    """
    if isinstance(term, Funktion):
        return term

    # Konvertiere zu SymPy für Analyse
    if isinstance(term, str):
        expr = sp.sympify(term.replace("^", "**"))
    else:
        expr = sp.sympify(term)

    # Automatische Typ-Erkennung
    struktur_info = analysiere_funktion_struktur(expr, variable)

    if struktur_info.haupt_typ == FunktionsTyp.GANZRATIONAL:
        return GanzrationaleFunktion(term)
    elif struktur_info.haupt_typ == FunktionsTyp.QUOTIENT:
        return QuotientFunktion(term)
    elif struktur_info.haupt_typ == FunktionsTyp.EXPONENTIAL:
        return ExponentialFunktion(term)
    # ... weitere Typen
```

### Verwendung im Code
```python
# Automatische Erkennung funktioniert perfekt
f = Funktion("x^2 + 1")              # → GanzrationaleFunktion
g = Funktion("2x + 3")               # → LineareFunktion
h = Funktion("(x^2+1)/(x-1)")       # → QuotientFunktion
e = Funktion("e^x")                  # → ExponentialFunktion
```

## 🔧 Wrapper-API für Schüler

### Schülerfreundliche Syntax
```python
# src/schul_analysis/api.py - Wrapper-Funktionen
def nullstellen(funktion: Funktionstyp, real: bool = True, runden: int | None = None) -> list[float] | list[Any]:
    """Berechnet die Nullstellen einer Funktion."""
    try:
        if hasattr(funktion, "nullstellen"):
            attr = funktion.nullstellen
            if callable(attr):
                return funktion.nullstellen(real=real, runden=runden)
            else:
                result = funktion.nullstellen
                # Apply filtering and rounding...
        else:
            raise AttributeError("Keine nullstellen Eigenschaft oder Methode gefunden")
    except Exception as e:
        raise SchulAnalysisError(f"Fehler bei Nullstellenberechnung: {e}")

def ableitung(funktion: Funktionstyp, ordnung: int = 1) -> Funktion:
    """Berechnet die Ableitung einer Funktion."""
    return funktion.ableitung(ordnung)

def extrema(funktion: Funktionstyp) -> list[tuple[float, str]]:
    """Berechnet die Extremstellen einer Funktion."""
    return funktion.extremstellen()
```

### Natürliche mathematische Notation
```python
# Für Schüler intuitive Syntax
f = Funktion("x^2 - 4x + 3")
xs = nullstellen(f)              # [1.0, 3.0]
f1 = ableitung(f)                # 2x - 4
ext = extrema(f)                 # [(2.0, "Minimum")]
```

## 🧪 Test-Utilities mit mathematischer Exaktheit

### Robuster Vergleich von Ausdrücken
```python
# src/schul_analysis/test_utils.py - Mathematische Vergleichs-API
def assert_gleich(
    ausdruck1: str | sp.Basic | Funktion | float | int,
    ausdruck2: str | sp.Basic | Funktion | float | int,
    variable: str = "x",
    nachricht: str | None = None,
):
    """
    Überprüft, ob zwei mathematische Ausdrücke äquivalent sind.
    Nutzt sp.simplify(expr1 - expr2) == 0 für robusten Vergleich.
    """
    try:
        expr1 = _konvertiere_zu_sympy(ausdruck1, variable)
        expr2 = _konvertiere_zu_sympy(ausdruck2, variable)

        # Kern der mathematischen Äquivalenzprüfung
        differenz = sp.simplify(expr1 - expr2)  # type: ignore

        if differenz != 0:
            if nachricht is None:
                nachricht = f"Ausdrücke nicht äquivalent: '{ausdruck1}' ≠ '{ausdruck2}'"
            raise AssertionError(nachricht)
    except Exception as e:
        raise AssertionError(f"Fehler beim Vergleich: {e}")

def assert_wert_gleich(
    funktion: Funktion,
    x_wert: float,
    erwarteter_wert: float,
    toleranz: float | None = None,
):
    """Überprüft, ob ein Funktionswert dem erwarteten Wert entspricht."""
    actual = funktion.wert(x_wert)
    if hasattr(actual, "evalf"):
        actual_float = float(actual.evalf())
    else:
        actual_float = float(actual)

    if toleranz is None:
        if actual_float != erwarteter_wert:
            raise AssertionError(f"f({x_wert}) = {actual_float}, aber exakt {erwarteter_wert} erwartet")
    else:
        if abs(actual_float - erwarteter_wert) > toleranz:
            raise AssertionError(f"f({x_wert}) = {actual_float}, aber {erwarteter_wert} erwartet (Toleranz: ±{toleranz})")
```

### Verwendung in Tests
```python
# Exakte mathematische Vergleiche
def test_trigonometrische_identitaet():
    f1 = Funktion("sin(x)^2 + cos(x)^2")
    f2 = Funktion("1")
    assert_gleich(f1.term(), f2.term())  # sin²(x) + cos²(x) = 1

def test_wert_berechnung():
    f = Funktion("x^2")
    assert_wert_gleich(f, 3, 9.0)  # f(3) = 9
```

## 🏗️ Funktionstypen Architektur

### Basisklasse und Spezialierungen
```python
# src/schul_analysis/funktion.py - Basisklasse
class Funktion(ABC):
    """Abstrakte Basisklasse für alle mathematischen Funktionen."""

    @abstractmethod
    def wert(self, x: float) -> float:
        """Berechnet den Funktionswert an Stelle x."""
        pass

    @abstractmethod
    def ableitung(self, ordnung: int = 1) -> 'Funktion':
        """Berechnet die Ableitung."""
        pass

    def __call__(self, x: float) -> float:
        """Natürliche Syntax f(x) statt f.wert(x)."""
        return self.wert(x)

# src/schul_analysis/ganzrationale.py - Beispiel für konkrete Implementierung
class GanzrationaleFunktion(Funktion):
    """Repräsentiert ganzrationale Funktionen (Polynome)."""

    def __init__(self, term: str | list[float | int] | dict[int, float | int]):
        # Unterstützt verschiedene Konstruktoren
        if isinstance(term, str):
            self._term = term
        elif isinstance(term, list):
            # [1, -4, 3] → x² - 4x + 3
            self._koeffizienten = term
        # ...

    def nullstellen(self) -> list[float]:
        """Berechnet Nullstellen mit SymPy."""
        # Symbolische Berechnung für exakte Ergebnisse
        pass
```

### Strukturierte Funktionen (Summe, Produkt, Quotient)
```python
# src/schul_analysis/strukturiert.py - Zusammengesetzte Funktionen
class QuotientFunktion(StrukturierteFunktion):
    """Repräsentiert Quotienten von Funktionen f(x)/g(x)."""

    def __init__(self, zaehler, nenner=None):
        if nenner is None:
            # Automatische Analyse: "(x^2+1)/(x-1)"
            zaehler, nenner = self._analysiere_quotient(zaehler)
        self._zaehler = zaehler
        self._nenner = nenner

    def polstellen(self) -> list[float]:
        """Berechnet Polstellen (Nullstellen des Nenners)."""
        return self._nenner.nullstellen()
```

## 📊 Visualisierung mit mathematischer Korrektheit

### Plotly-Integration
```python
# src/schul_analysis/visualisierung.py - Perfekte Darstellung
class Graph:
    def __init__(self, funktion: Funktion, x_bereich: tuple[float, float] = (-10, 10)):
        self.funktion = funktion
        self.x_bereich = x_bereich

    def plotly(self) -> go.Figure:
        """Erzeugt mathematisch korrekten Plotly-Graph."""
        x_vals = np.linspace(self.x_bereich[0], self.x_bereich[1], 1000)
        y_vals = [self.funktion.wert(x) for x in x_vals]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines'))

        # 🎯 WICHTIG: Perfekte Aspect Ratio für mathematische Korrektheit
        fig.update_layout(
            xaxis=dict(scaleanchor="y", scaleratio=1),  # Keine verzerrten Parabeln!
            title=f"f(x) = {self.funktion.term()}",
            xaxis_title="x",
            yaxis_title="f(x)"
        )
        return fig

# Wrapper-Funktion für einfache Nutzung
def zeichne(funktion: Funktion, x_bereich: tuple[float, float] = (-10, 10)):
    """Zeichnet eine Funktion mit perfekter mathematischer Darstellung."""
    return Graph(funktion, x_bereich).plotly()
```

## 🔄 Architektur-Übersicht

```
schul_analysis/
├── funktion.py           # Magic Factory + Basisklasse
├── api.py               # Wrapper-API für Schüler (nullstellen, ableitung, etc.)
├── ganzrationale.py      # Polynom-Funktionen
├── strukturiert.py       # Summe/Produkt/Quotient Funktionen
├── exponential.py        # Exponentialfunktionen
├── trigonometrisch.py    # Trigonometrische Funktionen
├── visualisierung.py     # Plotly-Integration
├── test_utils.py         # Mathematische Test-Utilities
└── analyse/             # Struktur-Analyse für Magic Factory
```

## 🎯 Kernprinzipien im Code

1. **Deutsche Fachsprache**: Alle öffentlichen APIs auf Deutsch
2. **Symbolische Exaktheit**: SymPy für präzise Berechnungen
3. **Type Safety**: Vollständige Type Hints mit ty-Validierung
4. **Pädagogische Klarheit**: Einfache, intuitive Syntax
5. **Mathematische Korrektheit**: Perfekte Visualisierung ohne Verzerrungen
6. **Modern Python**: uv, ruff, ty, pytest mit 0 Fehlern
