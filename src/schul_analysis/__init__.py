"""
Schul-Analysis Framework - Schülerfreundliche API

Ein Python Framework für Schul-Analysis mit exakter Berechnung, Marimo-Integration
und intuitiver API für Mathematiklehrer und Schüler.

PÄDAGOGISCHE KERNPRINZIPIEN:
- Deutsche API-Namen für den Mathematikunterricht
- Unterrichtsnahe Syntax: nullstellen(f) statt f.nullstellen()
- Einfache Anwendung für Schüler durch Nähe zur mathematischen Notation
"""

# =============================================================================
# SCHÜLERFREUNDLICHE WRAPPER-API (Haupt-Import für Schüler)
# =============================================================================

# Wichtige symbolische Komponenten
from .api import (
    LGS,
    # Komfort-Funktionen für den Unterricht
    Ableitung,
    Ausmultiplizieren,
    Auswerten,
    ErstellePolynom,
    Extrema,
    Extrempunkte,
    Extremstellen,
    Integral,
    Flaeche,
    FlaecheZweiFunktionen,
    Nullstellen,
    Schnittpunkte,
    Symmetrie,
    Term,
    Wendepunkte,
    Wendestellen,
    Zeichne,
)

# =============================================================================
# FUNKTIONSKLASSEN (für direkte Verwendung)
# =============================================================================
from .exponential import ExponentialFunktion
from .funktion import Funktion, erstelle_funktion_automatisch
from .ganzrationale import GanzrationaleFunktion

# =============================================================================
# SPEZIALKOMPONENTEN
# =============================================================================
from .lineare_gleichungssysteme import (
    LineareGleichung,
    interpolationspolynom,
    plotte_loesung,
)
from .schmiegkurven import Schmiegkurve
from .schmiegung import (
    Graph_parametrisiert,
    HermiteInterpolation,
    Schmieggerade,
    Schmiegkegel,
    SchmiegkurveAllgemein,
    Schmiegparabel,
)
from .strukturiert import (
    KompositionFunktion,
    ProduktFunktion,
    QuotientFunktion,
    StrukturierteFunktion,
    SummeFunktion,
)
from .symbolic import (
    Parameter,
    Variable,
)
from .symmetrie import (
    Achsensymmetrie,
    Punktsymmetrie,
)
from .taylor import (
    tangente,
    taylorpolynom,
)

# 🧪 TEST-UTILS (optional, nur für Tests)
from .test_utils import (
    assert_gleich,
    assert_wert_gleich,
)
from .visualisierung import Graph

# Vordefinierte Variablen und Parameter für schnellen Zugriff
x = Variable("x")
t = Variable("t")
a = Parameter("a")
k = Parameter("k")

# Typ-Aliases für bessere Lesbarkeit
Ableiten = Ableitung
Derivative = Ableitung

# =============================================================================
# VERSION
# =============================================================================

__version__ = "1.0.0"  # Hauptversion nach pädagogischer Optimierung

# =============================================================================
# EXPORTLISTE - WAS BEI `from schul_analysis import *` IMPORTIERT WIRD
# =============================================================================

__all__ = [
    # 🔥 SCHÜLERFREUNDLICHE API (Priorität für Unterricht)
    "Ableitung",
    "Ausmultiplizieren",
    "Nullstellen",
    "Schnittpunkte",
    "Integral",
    "Flaeche",
    "FlaecheZweiFunktionen",
    "Extrema",
    "Wendepunkte",
    "Symmetrie",
    "Term",
    "Zeichne",
    "Auswerten",
    "ErstellePolynom",
    "erstelle_funktion_automatisch",
    # 🏗️ FUNKTIONSKLASSEN
    "Funktion",
    "GanzrationaleFunktion",
    "ExponentialFunktion",
    "StrukturierteFunktion",
    "ProduktFunktion",
    "SummeFunktion",
    "QuotientFunktion",
    "KompositionFunktion",
    "LGS",
    # 🔤 SYMBOLISCHE KOMPONENTEN
    "Variable",
    "Parameter",
    "x",
    "t",
    "a",
    "k",
    # 📊 VISUALISIERUNG
    "Graph",
    "Graph_parametrisiert",
    # 🧮 ANALYSE-FUNKTIONEN
    "Ableitung",
    "Integral",
    "Extrema",
    "Extremstellen",
    "Extrempunkte",
    "Wendepunkte",
    "Wendestellen",
    # 📊 VISUALISIERUNG
    "Graph",
    # 📐 SPEZIALFUNKTIONEN
    "Achsensymmetrie",
    "Punktsymmetrie",
    "Schmiegparabel",
    "Schmiegkegel",
    "Schmieggerade",
    "HermiteInterpolation",
    "SchmiegkurveAllgemein",
    "Schmiegkurve",
    # 📈 TAYLOR-FUNKTIONEN
    "taylorpolynom",
    "tangente",
    # 📐 LINEARE GLEICHUNGSSYSTEME
    "LineareGleichung",
    "interpolationspolynom",
    "plotte_loesung",
    # 🧪 TEST-UTILS (optional, nur für Tests)
    "assert_gleich",
    "assert_wert_gleich",
]
