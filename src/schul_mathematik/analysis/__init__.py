"""
Analysis-Modul des Schul-Mathematik Frameworks

Enthält alle Funktionalitäten für differential- und integralrechnung,
Funktionsanalyse, Nullstellenberechnung, etc.
"""

# Importiere alle wichtigen Klassen und Funktionen
from .api import *
from .funktion import Funktion, erstelle_funktion_automatisch
from .ganzrationale import GanzrationaleFunktion
from .exponential import ExponentialFunktion
from .trigonometrisch import TrigonometrischeFunktion
from .visualisierung import Graph
from .errors import SchulAnalysisError, UngueltigeFunktionError
from .sympy_types import *
from .symbolic import Variable, Parameter
from .test_utils import assert_gleich, assert_wert_gleich

# Weitere wichtige Klassen
from .strukturiert import (
    KompositionFunktion,
    ProduktFunktion,
    QuotientFunktion,
    StrukturierteFunktion,
    SummeFunktion,
)
from .lineare_gleichungssysteme import (
    LineareGleichung,
    interpolationspolynom,
    plotte_loesung,
    LGS,
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
from .symmetrie import (
    Achsensymmetrie,
    Punktsymmetrie,
)
from .taylor import (
    tangente,
    taylorpolynom,
)

# Vordefinierte Variablen und Parameter
x = Variable("x")
t = Variable("t")
a = Parameter("a")
k = Parameter("k")

# Typ-Aliases für bessere Lesbarkeit
Ableiten = Ableitung
Derivative = Ableitung

__all__ = [
    # 🔥 KERN-ANALYSE-FUNKTIONEN (Haupt-API für Schüler)
    "Nullstellen",
    "Ableitung",
    "Integral",
    "Flaeche",
    "Extremstellen",
    "Extrempunkte",
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
    "Funktion",
    "GanzrationaleFunktion",
    "ExponentialFunktion",
    "TrigonometrischeFunktion",
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
    # 🧪 TEST-UTILS
    "assert_gleich",
    "assert_wert_gleich",
]
