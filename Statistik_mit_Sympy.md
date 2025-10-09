# Statistik mit SymPy - Analyse der statistischen Verteilungsfunktionalität

## 📊 Überblick

SymPy bietet umfangreiche Funktionalität für symbolische Statistik und Wahrscheinlichkeitsrechnung. Dieses Dokument analysiert die Implementierung und Verwendung statistischer Verteilungen, insbesondere für die Binomial- und Normalverteilung, im Kontext des Schul-Analysis Frameworks.

## 🔧 Grundlagen der Statistik in SymPy

### Import und Grundstruktur

```python
import sympy as sp
from sympy.stats import *

# SymPy's Statistik-Modul bietet symbolische Wahrscheinlichkeitsrechnung
# Alle Verteilungen sind symbolisch exakt - keine numerischen Approximationen
```

### Kernkonzepte

1. **Symbolische Exaktheit**: Alle Berechnungen bleiben symbolisch exakt
2. **Zufallsvariablen**: Werden mit `density()` oder `sample()` definiert
3. **Verteilungsparameter**: Können symbolisch oder numerisch sein
4. **Wahrscheinlichkeitsfunktionen**: PDF, CDF, SF, PPF usw.

## 🎲 Binomialverteilung

### Definition und Grundparameter

```python
import sympy as sp
from sympy.stats import Binomial, P, E, variance

# Symbolische Parameter
n, k = sp.symbols('n k', integer=True, positive=True)
p = sp.symbols('p', real=True, positive=True)

# Binomialverteilte Zufallsvariable
X = Binomial('X', n, p)

# Alternativ mit konkreten Werten
Y = Binomial('Y', 10, 0.3)  # 10 Versuche, p=0.3
```

### Wahrscheinlichkeitsfunktionen

#### Wahrscheinlichkeitsfunktion (PMF - Probability Mass Function)

```python
# PMF für einen bestimmten Wert k
pmf_k = sp.stats.density(X)(k)
print(f"PMF: P(X=k) = {pmf_k}")

# Vereinfachte Form
pmf_simplified = sp.simplify(pmf_k)
# Ergebnis: binomial(n, k) * p^k * (1-p)^(n-k)
```

#### Kumulative Verteilungsfunktion (CDF)

```python
# CDF für Wert k
cdf_k = sp.stats.cdf(X)(k)
print(f"CDF: P(X≤k) = {cdf_k}")

# Berechnet als Summe: Σ_{i=0}^k binomial(n,i) * p^i * (1-p)^(n-i)
```

#### Überlebensfunktion (SF - Survival Function)

```python
# SF: P(X > k)
sf_k = 1 - cdf_k
print(f"SF: P(X>k) = {sf_k}")
```

### Momente und Kenngrößen

```python
# Erwartungswert
erwartung = E(X)
print(f"E[X] = {erwartung}")  # Ergebnis: n*p

# Varianz
var = variance(X)
print(f"Var[X] = {var}")      # Ergebnis: n*p*(1-p)

# Standardabweichung
std = sp.sqrt(var)
print(f"σ[X] = {std}")

# Schiefe (Skewness)
skew = sp.stats.skewness(X)
print(f"Schiefe = {skew}")

# Kurtosis
kurt = sp.stats.kurtosis(X)
print(f"Kurtosis = {kurt}")
```

### Konkrete Berechnungen

```python
# Konkrete Binomialverteilung
n_val, p_val = 10, 0.3
X_konkret = Binomial('X_konkret', n_val, p_val)

# Einzelwahrscheinlichkeiten
P_X_3 = P(X_konkret > 3)
print(f"P(X>3) = {P_X_3.evalf()}")

# Erwartungswert
E_X_konkret = E(X_konkret)
print(f"E[X] = {E_X_konkret.evalf()}")

# Varianz
Var_X_konkret = variance(X_konkret)
print(f"Var[X] = {Var_X_konkret.evalf()}")
```

### Bedingte Wahrscheinlichkeiten

```python
# Bedingte Wahrscheinlichkeit P(X≤5 | X≥2)
bedingte_wahrscheinlichkeit = P(X <= 5, X >= 2)
print(f"P(X≤5|X≥2) = {bedingte_wahrscheinlichkeit}")
```

## 📈 Normalverteilung

### Definition und Grundparameter

```python
import sympy as sp
from sympy.stats import Normal

# Symbolische Parameter
mu, sigma = sp.symbols('μ σ', real=True, positive=True)
x = sp.symbols('x', real=True)

# Normalverteilte Zufallsvariable
Z = Normal('Z', mu, sigma)

# Standardnormalverteilung
Z_std = Normal('Z_std', 0, 1)

# Konkrete Normalverteilung
N_konkret = Normal('N_konkret', 5, 2)  # μ=5, σ=2
```

### Wahrscheinlichkeitsdichtefunktion (PDF)

```python
# PDF der Normalverteilung
pdf = sp.stats.density(Z)(x)
print(f"PDF: f(x) = {pdf}")

# Vereinfachte Form
pdf_simplified = sp.simplify(pdf)
# Ergebnis: sqrt(2)*exp(-(x-μ)^2/(2*σ^2))/(2*sqrt(pi)*σ)

# PDF der Standardnormalverteilung
pdf_std = sp.stats.density(Z_std)(x)
print(f"Standardnormal-PDF: φ(x) = {pdf_std}")
# Ergebnis: sqrt(2)*exp(-x^2/2)/(2*sqrt(pi))
```

### Kumulative Verteilungsfunktion (CDF)

```python
# CDF der Normalverteilung
cdf = sp.stats.cdf(Z)(x)
print(f"CDF: F(x) = {cdf}")

# CDF der Standardnormalverteilung (Φ-Funktion)
cdf_std = sp.stats.cdf(Z_std)(x)
print(f"Φ(x) = {cdf_std}")

# Konkrete Werte
P_Z_lt_2 = P(N_konkret < 7)
print(f"P(Z<7) = {P_Z_lt_2.evalf()}")
```

### Quantilfunktion (PPF - Percent Point Function)

```python
# Inverse CDF (Quantilfunktion)
# Für symbolische Berechnungen kann dies komplex sein
# Für konkrete Werte:
from scipy.stats import norm  # Numerische Alternative

# Konkretes Quantil (75%-Quantil)
quantil_75 = sp.stats.quantile(N_konkret)(0.75)
print(f"75%-Quantil: {quantil_75.evalf()}")
```

### Momente und Kenngrößen

```python
# Erwartungswert
E_Z = E(Z)
print(f"E[Z] = {E_Z}")  # Ergebnis: μ

# Varianz
Var_Z = variance(Z)
print(f"Var[Z] = {Var_Z}")  # Ergebnis: σ^2

# Standardabweichung
Std_Z = sp.sqrt(Var_Z)
print(f"σ[Z] = {Std_Z}")  # Ergebnis: σ

# Momente höherer Ordnung
moment_3 = E(Z**3)
print(f"E[Z³] = {moment_3}")

moment_4 = E(Z**4)
print(f"E[Z⁴] = {moment_4}")
```

### Spezielle Eigenschaften der Normalverteilung

```python
# Standardisierung: (X-μ)/σ ~ N(0,1)
X_standardisiert = (Z - mu) / sigma
print(f"Standardisiert: {X_standardisiert}")

# Additionsstabilität: X1+X2 ~ N(μ1+μ2, σ1²+σ2²)
X1 = Normal('X1', mu1, sigma1)
X2 = Normal('X2', mu2, sigma2)
X_summe = X1 + X2
print(f"X1+X2 ~ {X_summe}")
```

## 🔗 Gemeinsame Verteilungen und Abhängigkeiten

### Korrelation und Kovarianz

```python
from sympy.stats import covariance, correlation

# Zwei Zufallsvariablen mit Korrelation ρ
rho = sp.symbols('ρ', real=True)
X, Y = sp.symbols('X Y', cls=sp.RandomSymbol)

# Kovarianz
cov_XY = covariance(X, Y)
print(f"Cov(X,Y) = {cov_XY}")

# Korrelationskoeffizient
corr_XY = correlation(X, Y)
print(f"Corr(X,Y) = {corr_XY}")
```

### Gemeinsame Normalverteilung

```python
# Mehrdimensionale Normalverteilung (konzeptionell)
# In SymPy kann man mit gemeinsamen Verteilungen arbeiten
from sympy.stats import MultivariateNormal

# Parameter für zweidimensionale Normalverteilung
mu1, mu2 = sp.symbols('μ1 μ2', real=True)
sigma1, sigma2 = sp.symbols('σ1 σ2', real=True, positive=True)
rho = sp.symbols('ρ', real=True)

# Kovarianzmatrix
cov_matrix = sp.Matrix([
    [sigma1**2, rho*sigma1*sigma2],
    [rho*sigma1*sigma2, sigma2**2]
])

# Gemeinsame Normalverteilung
X_joint = MultivariateNormal('X_joint', [mu1, mu2], cov_matrix)
```

## 📐 Approximationen und Grenzwertsätze

### Normalapproximation der Binomialverteilung

```python
# Binomialverteilung B(n,p) ≈ N(np, np(1-p)) für große n
mu_approx = n * p
sigma_approx = sp.sqrt(n * p * (1 - p))

# Approximierte Normalverteilung
X_approx = Normal('X_approx', mu_approx, sigma_approx)

# Kontinuitätskorrektur für bessere Approximation
# P(X ≤ k) ≈ P(Y ≤ k + 0.5) wobei Y ~ N(np, np(1-p))
k_wert = sp.symbols('k', integer=True)
P_binomial_approx = P(X_approx <= k_wert + 0.5)
print(f"Approximierte Wahrscheinlichkeit: {P_binomial_approx}")
```

### Zentraler Grenzwertsatz

```python
# Konzept: Summe von n unabhängigen Zufallsvariablen
# konvergiert gegen Normalverteilung für n → ∞

# Beispiel: Summe von Bernoulli-Variablen → Binomial → Normal
from sympy.stats import Bernoulli

# n unabhängige Bernoulli(p)-Variablen
bernoullis = [Bernoulli(f'B_{i}', p) for i in range(n)]
summe = sum(bernoullis)

# Für große n: Summe ≈ N(np, np(1-p))
print(f"Summe ~ {summe} ≈ N({mu_approx}, {sigma_approx**2})")
```

## 🧮 Konkrete Berechnungen und Beispiele

### Beispiel 1: Binomialverteilung - Münzwürfe

```python
# 10 Münzwürfe, p=0.5 (faire Münze)
n_muenze, p_muenze = 10, sp.Rational(1, 2)
X_muenze = Binomial('X_muenze', n_muenze, p_muenze)

# Wahrscheinlichkeit für genau 5 Köpfe
P_genau_5 = P(X_muenze == 5)
print(f"P(X=5) = {P_genau_5.evalf()}")  # ≈ 0.246

# Wahrscheinlichkeit für mindestens 6 Köpfe
P_mindestens_6 = P(X_muenze >= 6)
print(f"P(X≥6) = {P_mindestens_6.evalf()}")  # ≈ 0.377

# Erwartungswert und Varianz
print(f"E[X] = {E(X_muenze).evalf()}")  # 5
print(f"Var[X] = {variance(X_muenze).evalf()}")  # 2.5
```

### Beispiel 2: Normalverteilung - IQ-Verteilung

```python
# IQ-Verteilung: μ=100, σ=15
X_iq = Normal('X_iq', 100, 15)

# Wahrscheinlichkeit für IQ > 130 (hochbegabt)
P_iq_gt_130 = P(X_iq > 130)
print(f"P(IQ>130) = {P_iq_gt_130.evalf()}")  # ≈ 0.0228

# 95%-Konfidenzintervall
from scipy.stats import norm
quantil_025 = norm.ppf(0.025, 100, 15)
quantil_975 = norm.ppf(0.975, 100, 15)
print(f"95%-KI: [{quantil_025:.1f}, {quantil_975:.1f}]")  # ≈ [70.6, 129.4]
```

### Beispiel 3: Hypothesentest

```python
# Einstichproben-Gauß-Test
# H0: μ = μ0 vs. H1: μ ≠ μ0

# Teststatistik
mu0 = sp.symbols('μ0', real=True)
x_stichprobe = sp.symbols('x̄', real=True)
n_stichprobe = sp.symbols('n', integer=True, positive=True)

# Teststatistik Z = (x̄ - μ0) / (σ/√n)
teststatistik = (x_stichprobe - mu0) / (sigma / sp.sqrt(n_stichprobe))
print(f"Teststatistik: Z = {teststatistik}")

# Kritischer Wert für α=0.05 (zweiseitig)
alpha = 0.05
kritischer_wert = sp.stats.quantile(Z_std)(1 - alpha/2)
print(f"Kritischer Wert: z_{1-alpha/2} = {kritischer_wert.evalf()}")
```

## 🔍 Symbolische vs. Numerische Berechnungen

### Vorteile der symbolischen Berechnung

1. **Exakte Ergebnisse**: Keine Rundungsfehler
2. **Parametrische Lösungen**: Formeln mit symbolischen Parametern
3. **Verständnis**: Mathematische Struktur bleibt sichtbar
4. **Verifizierung**: Numerische Ergebnisse können überprüft werden

### Grenzen der symbolischen Berechnung

1. **Komplexität**: Ausdrücke können sehr komplex werden
2. **Geschwindigkeit**: Numerische Methoden sind oft schneller
3. **Konvergenz**: Manche Integrale haben keine geschlossene Form

### Hybrider Ansatz

```python
# Symbolische Herleitung, numerische Auswertung
# 1. Symbolische Formel herleiten
formel = sp.stats.density(Z)(x)

# 2. Für konkrete Werte numerisch auswerten
werte = [(i, formel.subs({mu: 0, sigma: 1, x: i}).evalf())
         for i in range(-3, 4)]

print("x | f(x)")
print("---------")
for x_val, fx_val in werte:
    print(f"{x_val:2d} | {fx_val:.4f}")
```

## 🎯 Schulrelevante Anwendungen

### Abiturrelevante Themen

1. **Binomialverteilung**
   - Bernoulli-Kette
   - Wahrscheinlichkeitsberechnung
   - Erwartungswert und Varianz
   - Approximation durch Normalverteilung

2. **Normalverteilung**
   - Standardnormalverteilung
   - Sigma-Regeln
   - Konfidenzintervalle
   - Hypothesentests

### Pädagogische Vorteile

1. **Exakte Berechnungen**: Keine "Black Box" numerischer Methoden
2. **Formelverständnis**: Schüler sehen die mathematische Struktur
3. **Parameterverständnis**: Auswirkungen von Parameteränderungen sichtbar
4. **Vorbereitung auf Studium**: Symbolische Mathematik wie an Universitäten

### Unterrichtseinheiten

#### Einheit 1: Diskrete Verteilungen

- Bernoulli-Experimente
- Binomialverteilung
- Wahrscheinlichkeitsfunktion
- Kumulative Verteilung

#### Einheit 2: Stetige Verteilungen

- Normalverteilung als Grenzwert
- Dichtefunktion
- Verteilungsfunktion
- Standardisierung

#### Einheit 3: Schätzverfahren

- Punkt- und Intervallschätzung
- Konfidenzintervalle
- Hypothesentests
- Fehler 1. und 2. Art

## 💡 Integration in SchulAnalysis Framework

### Vorgeschlagene Module

```python
# src/schul_analysis/stochastik/__init__.py
from .binomial import Binomialverteilung
from .normal import Normalverteilung
from .verteilungen import Verteilung

# API-Funktionen (Wrapper)
from .api import (
    Binomialverteilung,
    Normalverteilung,
    Wahrscheinlichkeit,
    Erwartungswert,
    Varianz,
    Standardabweichung,
    Quantil,
    ZeichneVerteilung,
)
```

### Beispiel-API für SchulAnalysis

```python
from schul_analysis.stochastik import *

# Binomialverteilung
B = Binomialverteilung(n=10, p=0.3)
P_B = Wahrscheinlichkeit(B, k=5)
E_B = Erwartungswert(B)

# Normalverteilung
N = Normalverteilung(mu=100, sigma=15)
P_N = Wahrscheinlichkeit(N, x_bereich=(85, 115))
quantile_N = Quantil(N, alpha=0.95)

# Visualisierung
ZeichneVerteilung(B, typ="balken")  # Balkendiagramm
ZeichneVerteilung(N, typ="kurve")  # Dichtekurve
```

### Pädagogische Methoden

```python
# Schritt-für-Schritt Erklärungen
B.erkläre_wahrscheinlichkeit(k=5)
B.zeige_approximation_durch_normal()
N.zeige_sigma_regeln()
N.erkläre_konfidenzintervall()
```

## 🔮 Weiterführende Themen

### Andere Verteilungen in SymPy

1. **Poisson-Verteilung**: Für seltene Ereignisse
2. **Exponentialverteilung**: Wartezeiten
3. **Chi-Quadrat-Verteilung**: Varianzanalyse
4. **t-Verteilung**: Kleine Stichproben
5. **F-Verteilung**: Varianzquotienten

### Multivariate Statistik

1. **Mehrdimensionale Normalverteilung**
2. **Korrelationsanalyse**
3. **Regressionsanalyse**
4. **Varianzanalyse (ANOVA)**

### Stochastische Prozesse

1. **Markov-Ketten**
2. **Poisson-Prozesse**
3. **Brown'sche Bewegung**
4. **Zeitreihenanalyse**

## 📚 Zusammenfassung

SymPy bietet leistungsfähige Werkzeuge für die symbolische Statistik, die sich hervorragend für den schulischen Einsatz eignen:

### Stärken:

- **Exakte Berechnungen** ohne numerische Approximation
- **Symbolische Parameter** für allgemeine Formeln
- **Pädagogische Klarheit** durch sichtbare mathematische Struktur
- **Abitur-Relevanz** durch exakte Ergebnisse
- **Integration** mit bestehender symbolischer Mathematik

### Anwendungsmöglichkeiten:

- **Unterrichtsvorbereitung** mit exakten Berechnungen
- **Prüfungsbeispiele** mit symbolischen Lösungen
- **Selbstlernmaterial** mit interaktiven Beispielen
- **Projektarbeiten** mit statistischer Analyse
- **Brücke zu universitärer Mathematik**

Die Integration in SchulAnalysis würde das Framework zu einem umfassenden SchulMathematik-System erweitern, das die gesamte Oberstufenmathematik abdeckt.

---

_Erstellt für das Schul-Analysis Framework_
_Stand: Oktober 2025_
