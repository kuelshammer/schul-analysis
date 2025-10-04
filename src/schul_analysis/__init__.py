"""
Schul-Analysis Framework

Ein Python Framework für Schul-Analysis mit exakter Berechnung und Marimo-Integration.
"""

from .funktion import (
    Achsensymmetrie,
    Funktion,
    PruefeAchsensymmetrie,
    PruefePunktsymmetrie,
    Punktsymmetrie,
)
from .ganzrationale import GanzrationaleFunktion
from .gebrochen_rationale import GebrochenRationaleFunktion
from .lineare_gleichungssysteme import (
    LGS,
    LineareGleichung,
    interpolationspolynom,
    plotte_loesung,
)
from .parametrisch import ParametrischeFunktion
from .schmiegkurven import Schmiegkurve
from .schmiegung import (
    Graph_parametrisiert,
    HermiteInterpolation,
    Schmieggerade,
    Schmiegkegel,
    SchmiegkurveAllgemein,
    Schmiegparabel,
)
from .symbolic import Parameter, Variable
from .taylor import (
    Konvergenzradius,
    MacLaurin,
    Taylor,
    TaylorKoeffizienten,
    TaylorRestglied,
    TaylorStandardbeispiele,
    TaylorVergleich,
)
from .taylorpolynom import Taylorpolynom

# ====================
# Vordefinierte Variablen und Parameter
# ====================

# Standard-Variablen
x = Variable("x")
t = Variable("t")

# Standard-Parameter
a = Parameter("a")
k = Parameter("k")


# ====================
# Import von Analyse-Funktionen
# ====================

from .analysis import (
    AsymptotischesVerhalten,
    Ableitung,
    Extremstellen,
    Extrempunkte,
    Grenzwert,
    Integral,
    Kürzen,
    Nullstellen,
    Polstellen,
    Schnittpunkt,
    Wert,
    Wendepunkte,
    Wendestellen,
)
from .visualisierung import Graph


# ====================
# Typ-Aliases für bessere Lesbarkeit
# ====================

# Typ-Aliases für Kompatibilität
Polstellen = Polstellen  # Englische Variante auch verfügbar
Ableiten = Ableitung
Derivative = Ableitung
IntersectionPoints = Schnittpunkt
Integral = Integral
Limit = Grenzwert
AsymptoticBehavior = AsymptotischesVerhalten


__all__ = [
    "Funktion",
    "GanzrationaleFunktion",
    "GebrochenRationaleFunktion",
    "Schmiegkurve",
    "Taylorpolynom",
    "Variable",
    "Parameter",
    "ParametrischeFunktion",
    "x",
    "t",
    "a",
    "k",
    "Nullstellen",
    "Polstellen",
    "Ableitung",
    "Wert",
    "Graph",
    "Graph_parametrisiert",
    "Kürzen",
    "Schnittpunkt",
    "Extremstellen",
    "Wendestellen",
    "Extrempunkte",
    "Wendepunkte",
    "Integral",
    "Grenzwert",
    "AsymptotischesVerhalten",
    "Schmiegparabel",
    "Schmiegkegel",
    "Schmieggerade",
    "HermiteInterpolation",
    "SchmiegkurveAllgemein",
    "Taylor",
    "MacLaurin",
    "TaylorKoeffizienten",
    "TaylorRestglied",
    "Konvergenzradius",
    "TaylorVergleich",
    "TaylorStandardbeispiele",
    # 🔥 SYMMETRIE-FUNKTIONEN 🔥
    "Achsensymmetrie",
    "Punktsymmetrie",
    "PruefeAchsensymmetrie",
    "PruefePunktsymmetrie",
    # Lineare Gleichungssysteme
    "LGS",
    "LineareGleichung",
    "interpolationspolynom",
    "plotte_loesung",
]
__version__ = "0.1.0"
