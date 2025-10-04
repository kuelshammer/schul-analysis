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

from .api import (
    # Analyse-Funktionen - unterrichtsnahe Syntax
    nullstellen,
    ableitung,
    integral,
    extrema,
    wendepunkte,
    symmetrie,
    # Visualisierung
    zeichne,
    # Werteberechnung
    auswerten,
    # Helper-Funktionen für einfache Anwendung
    erstelle_polynom,
    erstelle_funktion,
    erstelle_lineares_gleichungssystem,
    erstelle_exponential_rationale_funktion,
    # Komfort-Funktionen für den Unterricht
    analysiere_funktion,
    zeige_analyse,
    # Funktionstypen für fortgeschrittene Nutzer
    GanzrationaleFunktion,
    GebrochenRationaleFunktion,
    ExponentialRationaleFunktion,
    ParametrischeFunktion,
    LGS,
    Taylor,
)

# =============================================================================
# FUNKTIONSKLASSEN (für direkte Verwendung)
# =============================================================================

from .funktion import (
    Funktion,
    Achsensymmetrie,
    Punktsymmetrie,
    PruefeAchsensymmetrie,
    PruefePunktsymmetrie,
    erstelle_funktion_automatisch,
)

from .ganzrationale import GanzrationaleFunktion
from .gebrochen_rationale import (
    GebrochenRationaleFunktion,
    ExponentialRationaleFunktion,
)
from .parametrisch import ParametrischeFunktion
from .lineare_gleichungssysteme import (
    LGS,
    LineareGleichung,
    interpolationspolynom,
    plotte_loesung,
)
from .taylor import (
    Taylor,
    MacLaurin,
    Taylorpolynom,
    TaylorKoeffizienten,
    TaylorRestglied,
    Konvergenzradius,
    TaylorVergleich,
    TaylorStandardbeispiele,
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

# =============================================================================
# SYMBOLISCHE KOMPONENTEN
# =============================================================================

from .symbolic import Parameter, Variable

# Vordefinierte Variablen und Parameter für schnellen Zugriff
x = Variable("x")
t = Variable("t")
a = Parameter("a")
k = Parameter("k")

# =============================================================================
# LEGACY-KOMPONENTEN (für Abwärtskompatibilität)
# =============================================================================

from .analysis import (
    AsymptotischesVerhalten,
    Ableitung,
    Extremstellen,
    Extrempunkte,
    Grenzwert,
    Integral,
    Kürzen,
    Polstellen,
    Schnittpunkt,
    Wert,
    Wendepunkte,
    Wendestellen,
)
from .visualisierung import Graph

# Typ-Aliases für bessere Lesbarkeit
Polstellen = Polstellen  # Englische Variante auch verfügbar
Ableiten = Ableitung
Derivative = Ableitung
IntersectionPoints = Schnittpunkt
Limit = Grenzwert
AsymptoticBehavior = AsymptotischesVerhalten

# =============================================================================
# VERSION
# =============================================================================

__version__ = "1.0.0"  # Hauptversion nach pädagogischer Optimierung

# =============================================================================
# EXPORTLISTE - WAS BEI `from schul_analysis import *` IMPORTIERT WIRD
# =============================================================================

__all__ = [
    # 🔥 SCHÜLERFREUNDLICHE API (Priorität für Unterricht)
    "nullstellen",
    "ableitung",
    "integral",
    "extrema",
    "wendepunkte",
    "symmetrie",
    "zeichne",
    "auswerten",
    "erstelle_polynom",
    "erstelle_funktion",
    "erstelle_lineares_gleichungssystem",
    "erstelle_exponential_rationale_funktion",
    "erstelle_funktion_automatisch",
    "analysiere_funktion",
    "zeige_analyse",
    # 🏗️ FUNKTIONSKLASSEN
    "Funktion",
    "GanzrationaleFunktion",
    "GebrochenRationaleFunktion",
    "ExponentialRationaleFunktion",
    "ParametrischeFunktion",
    "LGS",
    "Taylorpolynom",
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
    # 🧮 ANALYSE-FUNKTIONEN (Legacy)
    "Ableitung",
    "Wert",
    "Integral",
    "Kürzen",
    "Schnittpunkt",
    "Extremstellen",
    "Wendestellen",
    "Extrempunkte",
    "Wendepunkte",
    "Grenzwert",
    "AsymptotischesVerhalten",
    "Polstellen",
    # 📐 SPEZIALFUNKTIONEN
    "Achsensymmetrie",
    "Punktsymmetrie",
    "PruefeAchsensymmetrie",
    "PruefePunktsymmetrie",
    "Schmiegparabel",
    "Schmiegkegel",
    "Schmieggerade",
    "HermiteInterpolation",
    "SchmiegkurveAllgemein",
    "Schmiegkurve",
    # 📈 TAYLOR-FUNKTIONEN
    "Taylor",
    "MacLaurin",
    "TaylorKoeffizienten",
    "TaylorRestglied",
    "Konvergenzradius",
    "TaylorVergleich",
    "TaylorStandardbeispiele",
    # 📐 LINEARE GLEICHUNGSSYSTEME
    "LineareGleichung",
    "interpolationspolynom",
    "plotte_loesung",
]
