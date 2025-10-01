# Nullstellen-Methoden für ganzrationale Funktionen

## Übersicht

Dieses Dokument beschreibt die Implementierung der Nullstellen-Methoden für die Klasse `GanzrationaleFunktion`. Jede Methode hat zwei Varianten: eine reine Berechnungsmethode und eine detaillierte Lösungsweg-Methode.

## Methoden-Signaturen

### Berechnungsmethoden

```python
def nullstellen(self, real: bool = True) -> List[Union[float, complex]]:
    """
    Berechnet alle Nullstellen der Funktion.

    Args:
        real: Wenn True, werden nur reelle Nullstellen zurückgegeben
              Wenn False, werden auch komplexe Nullstellen berücksichtigt

    Returns:
        Liste der Nullstellen (reelle oder komplexe Zahlen)
    """
```

### Lösungsweg-Methoden

```python
def nullstellen_weg(self, real: bool = True) -> str:
    """
    Generiert detaillierten Lösungsweg als Markdown.

    Args:
        real: Steuert, ob komplexe Nullstellen im Lösungsweg erklärt werden

    Returns:
        Markdown-String mit Schritt-für-Schritt-Erklärung
    """
```

### Interaktive Methoden

```python
def zeige_nullstellen(self, real: bool = True) -> marimo.Html:
    """
    Zeigt interaktive Nullstellenberechnung in Marimo.

    Args:
        real: Steuert die Art der Nullstellendarstellung

    Returns:
        Marimo-Objekt für interaktive Anzeige
    """
```

## LaTeX-Integration für Marimo

### Grundlagen der LaTeX-Darstellung

Marimo unterstützt vollständiges LaTeX-Rendering in Markdown mit `mo.md()`:

```python
import marimo as mo
import sympy as sp

# Inline-Mathematik
mo.md(r'Die Ableitung von $f(x) = x^2$ ist $f\'(x) = 2x$')

# Block-Mathematik
mo.md(r'$$\int_{0}^{\pi} \sin(x) dx = 2$$')

# Mit SymPy-Integration
x = sp.symbols('x')
expr = sp.exp(x) + sp.sin(x)
mo.md(f'SymPy Ausdruck: $${sp.latex(expr)}$$')
```

### Best Practices für LaTeX in Lösungswegen

**1. SymPy für LaTeX-Generierung nutzen:**

```python
def term_latex(self) -> str:
    """Gibt den Funktionsterm als LaTeX-String zurück"""
    return sp.latex(self.sympy_poly.as_expr())

def nullstellen_weg(self, real: bool = True) -> str:
    """Generiert Lösungsweg mit LaTeX für Marimo"""
    weg = f"## Nullstellenberechnung für $$f(x) = {self.term_latex()}$$"
    # ... weitere LaTeX-Formeln
    return weg
```

**2. Raw-Strings für Backslash-Probleme:**

```python
# Statt: mo.md("$$\int f(x) dx$$")  # Fehler wegen Backslash
mo.md(r"$$\int f(x) dx$$")         # Korrekt mit Raw-String
```

**3. F-Strings für Variablen:**

```python
a, b, c = self.koeffizienten[0], self.koeffizienten[1], self.koeffizienten[2]
mo.md(f"$$f(x) = {a}x^2 + {b}x + {c}$$")
```

### LaTeX-Formeln für typische Schulmathematik

**Mitternachtsformel:**

```latex
$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$
```

**Quadratische Ergänzung:**

```latex
$$ax^2 + bx + c = a\left(x + \frac{b}{2a}\right)^2 + \left(c - \frac{b^2}{4a}\right)$$
```

**Ableitungsregeln:**

```latex
$$\frac{d}{dx}[x^n] = nx^{n-1}$$
$$\frac{d}{dx}[e^x] = e^x$$
```

## Implementierungsvorschläge

### 1. Flexibler Konstruktor

```python
def __init__(self, input_data):
    """
    Flexibler Konstruktor für verschiedene Eingabeformate

    Args:
        input_data: String, Liste oder Dictionary mit Polynom-Daten

    Examples:
        >>> f1 = GanzrationaleFunktion("x^3-2x+1")     # String-Format
        >>> f2 = GanzrationaleFunktion([1, 0, -2, 1])   # Koeffizienten-Liste
        >>> f3 = GanzrationaleFunktion({3: 1, 1: -2, 0: 1})  # Potenz:Koeffizient
    """
    if isinstance(input_data, str):
        self.koeffizienten = self._parse_string_to_coeffs(input_data)
    elif isinstance(input_data, list):
        self.koeffizienten = self._validate_coeff_list(input_data)
    elif isinstance(input_data, dict):
        self.koeffizienten = self._dict_to_coeffs(input_data)
    else:
        raise TypeError(f"Unsupported type: {type(input_data)}")

    self.grad = len(self.koeffizienten) - 1
    self._sympy_poly = None

def _parse_string_to_coeffs(self, term_str: str) -> List[float]:
    """Konvertiert mathematischen String zu Koeffizientenliste"""
    import sympy as sp

    # Syntax bereinigen und normalisieren
    cleaned = self._clean_string_syntax(term_str)

    try:
        # SymPy-Ausdruck erstellen
        x = sp.Symbol('x')
        expr = sp.sympify(cleaned)

        # Polynom extrahieren und Koeffizienten erhalten
        poly = sp.Poly(expr, x)
        coeffs = poly.all_coeffs()

        # In float konvertieren für Konsistenz
        return [float(c) for c in coeffs]

    except (sp.SympifyError, sp.PolynomialError) as e:
        raise ValueError(f"Cannot parse '{term_str}': {e}")

def term_latex(self) -> str:
    """Gibt den Funktionsterm als LaTeX-String zurück"""
    import sympy as sp
    return sp.latex(self.sympy_poly.as_expr())

def nullstellen_latex(self, real: bool = True) -> str:
    """Gibt Nullstellen als LaTeX-String zurück"""
    nullstellen = self.nullstellen(real)

    if not nullstellen:
        return r"\text{keine reellen Nullstellen}"

    latex_list = []
    for ns in nullstellen:
        if isinstance(ns, complex) and ns.imag != 0:
            # Komplexe Nullstelle
            real_part = f"{ns.real:.2f}" if ns.real != 0 else ""
            imag_part = f"{abs(ns.imag):.2f}"

            if ns.real == 0:
                latex_list.append(f"{imag_part}i")
            elif ns.imag > 0:
                latex_list.append(f"{real_part} + {imag_part}i")
            else:
                latex_list.append(f"{real_part} - {imag_part}i")
        else:
            # Reelle Nullstelle
            latex_list.append(f"{ns.real:.2f}" if isinstance(ns, complex) else f"{ns:.2f}")

    return ", ".join(latex_list)

def _clean_string_syntax(self, term_str: str) -> str:
    """Bereinigt mathematische Syntax für SymPy"""
    # Leerzeichen entfernen
    cleaned = term_str.replace(" ", "")

    # ^ -> ** für Potenzen
    cleaned = cleaned.replace("^", "**")

    # Implizite Multiplikation ergänzen: 2x -> 2*x
    import re
    cleaned = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', cleaned)
    cleaned = re.sub(r'(\))([a-zA-Z(])', r'\1*\2', cleaned)

    return cleaned

def _validate_coeff_list(self, coeffs: List[float]) -> List[float]:
    """Validiert Koeffizientenliste"""
    if not coeffs:
        raise ValueError("Coefficient list cannot be empty")

    # Führende Nullen entfernen
    while len(coeffs) > 1 and coeffs[0] == 0:
        coeffs = coeffs[1:]

    return coeffs

def _dict_to_coeffs(self, coeff_dict: dict) -> List[float]:
    """Konvertiert {Potenz: Koeffizient} zu Koeffizientenliste"""
    if not coeff_dict:
        return [0]

    max_grad = max(coeff_dict.keys())
    coeffs = [0.0] * (max_grad + 1)

    for potenz, koeff in coeff_dict.items():
        if potenz < 0:
            raise ValueError("Negative exponents not supported")
        coeffs[max_grad - potenz] = koeff

    return self._validate_coeff_list(coeffs)
```

### 2. nullstellen() - Reine Berechnung

```python
def nullstellen(self, real: bool = True) -> List[Union[float, complex]]:
    """Berechnet alle Nullstellen exakt"""
    # Alle Nullstellen mit SymPy berechnen
    alle_nullstellen = [complex(n) for n in self.sympy_poly.all_roots()]

    if real:
        # Nur reelle Nullstellen filtern
        return [float(n.real) for n in alle_nullstellen if abs(n.imag) < 1e-10]
    else:
        # Alle Nullstellen zurückgeben
        return alle_nullstellen
```

**Besonderheiten:**

- Verwendung von SymPy für exakte Berechnungen
- Toleranzprüfung für reelle Zahlen (1e-10)
- Rückgabetyp je nach Parameter

### 3. nullstellen_weg() - Detaillierter Lösungsweg

```python
def nullstellen_weg(self, real: bool = True) -> str:
    """Generiert detaillierten Lösungsweg als Markdown"""
    schritte = []

    # Schritt 1: Funktion darstellen
    schritte.append(self._schritt_funktion_darstellen())

    # Schritt 2: Grad bestimmen
    schritte.append(self._schritt_grad_bestimmen())

    # Schritt 3: Spezielle Methode wählen
    if self.grad == 1:
        schritte.append(self._schritt_linear_gleichung())
    elif self.grad == 2:
        schritte.append(self._schritt_quadratische_gleichung(real))
    elif self.grad >= 3:
        schritte.append(self._schritt_hoherer_grad(real))

    # Schritt 4: Zusammenfassung
    schritte.append(self._schritt_zusammenfassung(real))

    return "\n\n".join(schritte)
```

**Unterstützende Methoden:**

```python
def _schritt_funktion_darstellen(self) -> str:
    """Schritt 1: Funktion darstellen"""
    return f"## Nullstellenberechnung für $$f(x) = {self.term_latex()}$$"

def _schritt_grad_bestimmen(self) -> str:
    """Schritt 2: Grad bestimmen"""
    return f"### Schritt 1: Grad der Funktion bestimmen\n\nDie Funktion $$f(x) = {self.term_latex()}$$ hat Grad {self.grad}."

def _schritt_linear_gleichung(self) -> str:
    """Schritt für lineare Gleichungen (Grad 1)"""
    a, b = self.koeffizienten[0], self.koeffizienten[1]

    schritte = [
        "### Schritt 2: Lineare Gleichung lösen",
        f"$$f(x) = {a}x + {b} = 0$$",
        f"$${a}x = {-b}$$",
        f"$$x = \\frac{{{-b}}}{{{a}}} = {-b/a}$$"
    ]
    return "\n".join(schritte)

def _schritt_quadratische_gleichung(self, real: bool = True) -> str:
    """Schritt für quadratische Gleichungen (Grad 2) - mit Vieta'schen Formeln"""
    a, b, c = self.koeffizienten[0], self.koeffizienten[1], self.koeffizienten[2]

    # Zuerst versuchen wir Faktorisierung mit Vieta'schen Formeln
    schritte = [
        "### Schritt 2: Quadratische Gleichung lösen",
        f"f(x) = {a}x² + {b}x + {c} = 0",
        "",
        "**Versuch der Faktorisierung mit Vieta'schen Formeln:**",
        "Wir suchen Zahlen a, b mit: (x + m)(x + n) = x² + (m+n)x + m·n",
        f"Also müssen gelten: m + n = {b/a} und m·n = {c/a}"
    ]

    # Überprüfen, ob wir ganzzahlige Lösungen finden können
    # Suche nach m, n mit m+n = b/a und m*n = c/a
    # Für a=1: suche Faktoren von c, die zu b addieren

    if a == 1:
        # Einfacher Fall: Suche ganzzahlige Faktoren
        faktoren_paare = []
        for i in range(1, abs(c) + 1):
            if c % i == 0:
                if c > 0:
                    faktoren_paare.extend([(i, c//i), (-i, -c//i)])
                else:
                    faktoren_paare.extend([(i, c//i), (-i, c//i), (i, -c//i)])

        # Prüfen, ob ein Paar die Summe b ergibt
        for m, n in faktoren_paare:
            if m + n == b and m * n == c:
                schritte.extend([
                    f"Gefunden: m = {m}, n = {n}",
                    f"Also: (x + {m})(x + {n}) = 0",
                    f"Nullstellen: x₁ = {-m}, x₂ = {-n}"
                ])
                return "\n".join(schritte)

    # Keine einfache Faktorisierung möglich, quadratische Ergänzung
    schritte.extend([
        "",
        "**Keine einfache Faktorisierung möglich, daher quadratische Ergänzung:**",
        f"f(x) = {a}x² + {b}x + {c} = 0",
        f": {a}(x² + {b/a}x) + {c} = 0",
        f": {a}(x² + {b/a}x + {(b/(2*a))**2} - {(b/(2*a))**2}) + {c} = 0",
        f": {a}((x + {b/(2*a)})² - {(b/(2*a))**2}) + {c} = 0",
        f": {a}(x + {b/(2*a)})² - {a*(b/(2*a))**2} + {c} = 0",
        f": {a}(x + {b/(2*a)})² + {c - a*(b/(2*a))**2} = 0"
    ])

    # Jetzt die quadratische Gleichung lösen
    D = b**2 - 4*a*c

    if D >= 0:
        # Reelle Nullstellen existieren
        x1 = (-b + (D)**0.5) / (2*a)
        x2 = (-b - (D)**0.5) / (2*a)

        schritte.extend([
            f": (x + {b/(2*a)})² = {-(c - a*(b/(2*a))**2)/a}",
            f": x + {b/(2*a)} = ±{(-(c - a*(b/(2*a))**2)/a)**0.5}",
            f": x = {-b/(2*a)} ± {(-(c - a*(b/(2*a))**2)/a)**0.5}",
            "",
            f"**Nullstellen:** x₁ = {x1}, x₂ = {x2}"
        ])
    else:
        # Keine reellen Nullstellen
        schritte.extend([
            f": (x + {b/(2*a)})² = {-(c - a*(b/(2*a))**2)/a}",
            "",
            f"Da {-(c - a*(b/(2*a))**2)/a} < 0, gibt es keine reellen Lösungen.",
            f"Der Ausdruck {a}x² + {b}x + {c} = {a}(x + {b/(2*a)})² + {c - a*(b/(2*a))**2} ≥ {c - a*(b/(2*a))**2} > 0"
        ])

        if not real:
            # Komplexe Nullstellen zeigen
            schritte.extend([
                "",
                "### Schritt 3: Komplexe Nullstellen",
                f"Für komplexe Nullstellen gilt:",
                f"x = {-b/(2*a)} ± i·{(-D)**0.5/(2*a)}",
                f"Also: x₁ = {-b/(2*a)} + {(-D)**0.5/(2*a)}i, x₂ = {-b/(2*a)} - {(-D)**0.5/(2*a)}i"
            ])

    return "\n".join(schritte)
```

### 4. zeige_nullstellen() - Interaktive Marimo-Anzeige

````python
def zeige_nullstellen(self, real: bool = True) -> marimo.Html:
    """Zeigt interaktive Nullstellenberechnung in Marimo"""
    import marimo as mo

    # Berechnung durchführen
    nullstellen = self.nullstellen(real)
    weg = self.nullstellen_weg(real)

    # Interaktive Elemente
    if real:
        visualisierung = self._erstelle_reellen_graph()
    else:
        visualisierung = self._erstelle_komplexen_graph()

    # Ausgabe zusammenstellen
    output = mo.md(f"""
# {self.term()}

## Nullstellen: {nullstellen}

{visualisierung}

### Lösungsweg

{mo.md(weg)}

### Interaktive Elemente

{mo.ui.slider(1, 10, label="Schritt-für-Schritt")}
{mo.ui.checkbox(label="Zeige Erklärungen")}
{mo.ui.button(label="Neues Beispiel")}
""")

    return output

### 5. Marimo-optimierte Methoden mit LaTeX

```python
def zeige_nullstellen_marimo(self, real: bool = True) -> marimo.Html:
    """Optimierte Marimo-Anzeige mit voller LaTeX-Unterstützung"""
    import marimo as mo

    # LaTeX-bereiter Lösungsweg
    weg_latex = self.nullstellen_weg_latex(real)

    return mo.md(weg_latex)

def nullstellen_weg_latex(self, real: bool = True) -> str:
    """Generiert LaTeX-optimierten Lösungsweg für Marimo"""
    schritte = [
        f"# Nullstellenberechnung für $$f(x) = {self.term_latex()}$$",
        "",
        f"### Schritt 1: Grad bestimmen",
        f"Die Funktion $$f(x) = {self.term_latex()}$$ hat Grad {self.grad}.",
        ""
    ]

    if self.grad == 1:
        schritte.extend(self._linear_gleichung_latex())
    elif self.grad == 2:
        schritte.extend(self._quadratische_gleichung_latex(real))
    else:
        schritte.extend(self._hoherer_grad_latex(real))

    return "\n".join(schritte)

def _linear_gleichung_latex(self) -> List[str]:
    """LaTeX-optimierte lineare Gleichung"""
    a, b = self.koeffizienten[0], self.koeffizienten[1]

    return [
        "### Schritt 2: Lineare Gleichung lösen",
        f"$$f(x) = {a}x + {b} = 0$$",
        f"$${a}x = {-b}$$",
        f"$$x = \\frac{{{-b}}}{{{a}}} = {-b/a}$$",
        "",
        f"**Ergebnis:** Die Nullstelle ist bei $$x = {-b/a}$$"
    ]

def _quadratische_gleichung_latex(self, real: bool = True) -> List[str]:
    """LaTeX-optimierte quadratische Gleichung mit Vieta"""
    a, b, c = self.koeffizienten[0], self.koeffizienten[1], self.koeffizienten[2]

    schritte = [
        "### Schritt 2: Quadratische Gleichung lösen",
        f"$$f(x) = {a}x^2 + {b}x + {c} = 0$$",
        "",
        "### Schritt 3: Faktorisierungsversuch mit Vieta'schen Formeln",
        "Wir suchen Zahlen $$m, n$$ mit: $$(x + m)(x + n) = x^2 + (m+n)x + m \\cdot n$$",
        f"Also müssen gelten: $$m + n = {b/a}$$ und $$m \\cdot n = {c/a}$$"
    ]

    # Versuche Faktorisierung (vereinfacht für die Dokumentation)
    if a == 1:
        D = b**2 - 4*a*c
        if D >= 0:
            x1 = (-b + D**0.5) / (2*a)
            x2 = (-b - D**0.5) / (2*a)
            schritte.extend([
                f"**Gefunden:** $$m = {-x1}, n = {-x2}$$",
                f"Also: $$(x {x1:+})(x {x2:+}) = 0$$",
                f"**Nullstellen:** $$x_1 = {x1:.2f}, x_2 = {x2:.2f}$$"
            ])
        else:
            schritte.extend([
                "**Keine reelle Faktorisierung möglich**",
                "### Schritt 4: Quadratische Ergänzung",
                f"$$f(x) = {a}x^2 + {b}x + {c} = {a}\\left(x + {b/(2*a):.2f}\\right)^2 + {c - b**2/(4*a):.2f}$$",
                "",
                f"Da $${c - b**2/(4*a):.2f} > 0$$, gibt es keine reellen Nullstellen."
            ])

            if not real:
                # Komplexe Lösungen
                schritte.extend([
                    "",
                    "### Schritt 5: Komplexe Lösungen",
                    f"$$x = {-b/(2*a):.2f} \\pm {(-D)**0.5/(2*a):.2f}i$$"
                ])

    return schritte
````

## Spezielle Lösungsstrategien

### Lineare Funktionen (Grad 1)

- Direktes Auflösen der Gleichung ax + b = 0
- Einfache Umformungsschritte

### Quadratische Funktionen (Grad 2)

- **Primär**: Faktorisierung mit Vieta'schen Formeln: (x+a)(x+b) = x² + (a+b)x + a·b
- **Sekundär**: Quadratische Ergänzung für komplexe Fälle
- **Für real=True**: Beweis der Nicht-Existenz durch Umformung zu (x-p)² + q > 0
- Komplexe Lösungen optional, mit konjugiert komplexen Paaren

### Kubische Funktionen (Grad 3)

- Suche nach rationalen Nullstellen
- Polynomdivision zur Reduktion
- Lösungsformeln oder Näherungsverfahren

### Funktionen höheren Grades (≥ 4)

- Strategie: Rationale Nullstellen suchen → Ausdividieren → Reduktion
- Horner-Schema für effiziente Berechnung
- Numerische Methoden für exakte Lösungen

## Fehlerbehandlung

### Konstruktor-Fehler

```python
class PolynomParseError(ValueError):
    """Fehler beim Parsen von Polynom-Strings"""
    pass

class UngueltigesKoeffizientenFormatError(ValueError):
    """Fehler bei ungültigen Koeffizientenformaten"""
    pass
```

### Typische Fehler und Lösungen

**1. Syntaxfehler in Strings:**

```python
# Fehlerhaft
f = GanzrationaleFunktion("x^3+-2x+1")  # Doppeltes Vorzeichen

# Korrekt
f = GanzrationaleFunktion("x^3-2x+1")
```

**2. Ungültige Zeichen:**

```python
# Fehlerhaft
f = GanzrationaleFunktion("x³ + 2x")  # Spezielle Zeichen

# Korrekt
f = GanzrationaleFunktion("x**3 + 2*x")
```

**3. Leere Eingaben:**

```python
# Fehlerhaft
f = GanzrationaleFunktion("")  # Leerer String
f = GanzrationaleFunktion([])  # Leere Liste

# Korrekt
f = GanzrationaleFunktion("0")  # Null-Funktion
f = GanzrationaleFunktion([0])  # Null-Funktion
```

### Fehlerbehandlungs-Methoden

```python
class NullstellenBerechnungFehler(MathematischeFunktionError):
    """Fehler bei der Nullstellenberechnung"""
    pass

class GradZuHochFehler(MathematischeFunktionError):
    """Fehler bei zu hohem Grad für bestimmte Methoden"""
    pass

class KonstruktorFehler(MathematischeFunktionError):
    """Fehler bei der Konstruktion der Funktion"""
    pass
```

## Didaktische Aspekte

### Differenzierung

- **real=True**: Fokus auf reelle Lösungen (Standard)
- **real=False**: Einführung komplexer Zahlen
- **Progressive Darstellung**: Von einfach zu komplex

### Visualisierung

- Graphische Darstellung der Funktion
- Markierung der Nullstellen
- Interaktive Parameteränderung

### Selbstkontrolle

- Schüler können Lösungen überprüfen
- Detaillierte Fehleranalyse möglich
- Schritt-für-Schritt-Vergleich

## Testbeispiele

### Beispiel 1: Verschiedene Konstruktor-Formate

```python
# String-Format (intuitiv für Schüler)
f1 = GanzrationaleFunktion("x^3-2x+1")
f1.nullstellen()  # Berechnet automatisch

# Koeffizienten-Liste (traditionell)
f2 = GanzrationaleFunktion([1, 0, -2, 1])
f2.nullstellen()  # Gleiche Ergebnisse wie f1

# Dictionary-Format (experte)
f3 = GanzrationaleFunktion({3: 1, 1: -2, 0: 1})
f3.nullstellen()  # Gleiche Ergebnisse wie f1, f2
```

### Beispiel 2: Marimo-Integration mit LaTeX

```python
import marimo as mo

# Funktion erstellen
f = GanzrationaleFunktion("x^2-4x+5")

# LaTeX-Ausgabe in Marimo
mo.md(f"## Funktion: $$f(x) = {f.term_latex()}$$")

# Lösungsweg mit LaTeX
weg_latex = f.nullstellen_weg_latex(real=True)
mo.md(weg_latex)

# Interaktive Anzeige
f.zeige_nullstellen_marimo(real=True)
```

**Ausgabe in Marimo:**

- ## Funktion: f(x) = x² - 4x + 5 (schön gerendert)
- Detaillierter Lösungsweg mit LaTeX-Formeln
- Quadratische Ergänzung: (x-2)² + 1 ≥ 1 > 0
- Professionelle mathematische Darstellung

### Beispiel 3: Quadratische Funktion mit Faktorisierung

```python
# Schülerfreundliche Eingabe
f = GanzrationaleFunktion("x^2-3x+2")

# LaTeX-optimierter Lösungsweg
print(f.nullstellen_weg_latex(real=True))

# Erzeugt LaTeX-Code für Marimo:
"""
# Nullstellenberechnung für $$f(x) = x^{2} - 3 x + 2$$

### Schritt 1: Grad bestimmen
Die Funktion $$f(x) = x^{2} - 3 x + 2$$ hat Grad 2.

### Schritt 2: Quadratische Gleichung lösen
$$f(x) = x^2 - 3x + 2 = 0$$

### Schritt 3: Faktorisierungsversuch mit Vieta'schen Formeln
Wir suchen Zahlen $$m, n$$ mit: $$(x + m)(x + n) = x^2 + (m+n)x + m \cdot n$$
Also müssen gelten: $$m + n = -3.0$$ und $$m \cdot n = 2.0$$

**Gefunden:** $$m = -1.0, n = -2.0$$
Also: $$(x - 1.0)(x - 2.0) = 0$$
**Nullstellen:** $$x_1 = 1.00, x_2 = 2.00$$
"""
```

### Beispiel 4: Komplexe Nullstellen in Marimo

```python
import marimo as mo
import sympy as sp

# Funktion mit komplexen Nullstellen
f = GanzrationaleFunktion("x^2-4x+5")

# Vergleich der Darstellungen
mo.md("""
## Vergleich der Darstellungen

### Textdarstellung (alt):
f(x) = x^2 - 4x + 5

### LaTeX-Darstellung (neu):
$$f(x) = x^{2} - 4 x + 5$$

### Nullstellen als Text:
Keine reellen Nullstellen

### Nullstellen als LaTeX:
$$\\text{keine reellen Nullstellen}$$

### Komplexe Lösungen:
$$x = 2.00 \\pm 1.00i$$
""")

# Vollständiger interaktiver Lösungsweg
f.zeige_nullstellen_marimo(real=False)
```

### Beispiel 5: Fehlerbehandlung in Marimo

```python
try:
    # Fehlerhafter String
    f = GanzrationaleFunktion("x^3+-2x+1")
except ValueError as e:
    mo.md(f"**Fehler:** ${e}$")

try:
    # Leere Liste
    f = GanzrationaleFunktion([])
except ValueError as e:
    mo.md(f"**Fehler:** ${e}$")
```

## Weiterentwicklung

### Mögliche Erweiterungen

- Numerische Nullstellenberechnung für hohe Grade
- Grafische Nullstellensuche
- Fehlerabschätzung bei Näherungsverfahren
- Mehrdimensionale Darstellung

### Performance-Optimierung

- Caching von Berechnungsergebnissen
- Parallelisierung für komplexe Polynome
- Effiziente Implementierung von Algorithmen
