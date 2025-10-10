"""
Analysis-Modul des Schul-Mathematik Frameworks

Enthält alle Funktionalitäten für differential- und integralrechnung,
Funktionsanalyse, Nullstellenberechnung, etc.
"""

# Importiere alle wichtigen Klassen und Funktionen
from .api import *
from .aspect_ratio import *
from .basis_funktion import BasisFunktion

# Unused imports removed
from .exponential import ExponentialFunktion
from .funktion import Funktion, erstelle_funktion_automatisch
from .ganzrationale import GanzrationaleFunktion
from .gebrochen_rationale import GebrochenRationaleFunktion
from .lineare_gleichungssysteme import (
    LGS,
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

# Weitere wichtige Klassen
from .strukturiert import (
    KompositionFunktion,
    ProduktFunktion,
    QuotientFunktion,
    StrukturierteFunktion,
    SummeFunktion,
)
from .symbolic import Parameter, Variable
from .symmetrie import (
    Achsensymmetrie,
    Punktsymmetrie,
)
from .sympy_types import *

# Unused imports removed
from .test_utils import assert_gleich, assert_wert_gleich
from .trigonometrisch import TrigonometrischeFunktion
from .lineare import LineareFunktion
from .quadratisch import QuadratischeFunktion
from .visualisierung import Graph

# Vordefinierte Variablen und Parameter
x = Variable("x")
t = Variable("t")
a = Parameter("a")
k = Parameter("k")

# Typ-Aliases für bessere Lesbarkeit
Ableiten = Ableitung
Derivative = Ableitung

# Abwärtskompatibilitäts-Aliase
Extrema = Extremstellen  # Für alte Tests und Dokumentation

__all__ = [
    # 🔥 KERN-ANALYSE-FUNKTIONEN (Haupt-API für Schüler)
    "Nullstellen",
    "Ableitung",
    "Integral",
    "Flaeche",
    "FlaecheZweiFunktionen",
    "Extremstellen",
    "Extrempunkte",
    "Extrema",  # Alias für Abwärtskompatibilität
    "Wendepunkte",
    "Sattelpunkte",
    "Schnittpunkte",
    # 🔍 SYMMETRIE-FUNKTIONEN
    "Achsensymmetrie",
    "Punktsymmetrie",
    "Symmetrie",  # Für Abwärtskompatibilität
    # 📊 VISUALISIERUNG
    "Graph",
    "Zeichne",  # Für Abwärtskompatibilität
    "Term",
    "Ausmultiplizieren",
    # 📈 TAYLOR-FUNKTIONEN
    "Tangente",
    "Taylorpolynom",
    # 🏗️ FUNKTIONSKLASSEN
    "BasisFunktion",  # Neue abstrakte Basisklasse
    "Funktion",
    "GanzrationaleFunktion",
    "GebrochenRationaleFunktion",
    "ExponentialFunktion",
    "TrigonometrischeFunktion",
    "LineareFunktion",
    "QuadratischeFunktion",
    "StrukturierteFunktion",
    "ProduktFunktion",
    "SummeFunktion",
    "QuotientFunktion",
    "KompositionFunktion",
    # 🔤 SYMBOLISCHE KOMPONENTEN
    "Variable",
    "Parameter",
    "x",
    "t",
    "a",
    "k",
    # 📊 VISUALISIERUNG (erweitert)
    "Graph_parametrisiert",
    # 📐 SPEZIALFUNKTIONEN
    "Schmiegparabel",
    "Schmiegkegel",
    "Schmieggerade",
    "HermiteInterpolation",
    "SchmiegkurveAllgemein",
    "Schmiegkurve",
    # 📐 LINEARE GLEICHUNGSSYSTEME
    "LineareGleichung",
    "LGS",
    "interpolationspolynom",
    "plotte_loesung",
    # 🎯 ASPECT-RATIO-KONTROLLE
    "AspectRatioType",
    "AspectRatioController",
    "aspect_ratio_controller",
    "setze_aspect_ratio",
    "get_aspect_ratio_info",
    "wende_aspect_ratio_an",
    "erstelle_aspect_ratio_buttons",
    # 🧪 TEST-UTILS
    "assert_gleich",
    "assert_wert_gleich",
]
