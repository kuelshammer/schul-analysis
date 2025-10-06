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

from .analysis import (
    Ableitung,
    AsymptotischesVerhalten,
    Extrempunkte,
    Extremstellen,
    Grenzwert,
    Integral,
    Kürzen,
    Nullstellen,  # Add this
    Polstellen,
    Schnittpunkt,
    Wendepunkte,
    Wendestellen,
    Wert,
)
from .api import (
    LGS,
    ExponentialRationaleFunktion,
    # Funktionstypen für fortgeschrittene Nutzer
    GanzrationaleFunktion,
    GebrochenRationaleFunktion,
    GemischteFunktion,
    ParametrischeFunktion,
    taylorpolynom,
    tangente,
    ableitung,
    # Komfort-Funktionen für den Unterricht
    analysiere_funktion,
    # Werteberechnung
    auswerten,
    erstelle_exponential_rationale_funktion,
    erstelle_funktion,
    erstelle_lineares_gleichungssystem,
    # Helper-Funktionen für einfache Anwendung
    erstelle_polynom,
    extrema,
    integral,
    # Analyse-Funktionen - unterrichtsnahe Syntax
    nullstellen,
    symmetrie,
    wendepunkte,
    # Visualisierung
    zeichne,
    zeige_analyse,
)

# =============================================================================
# FUNKTIONSKLASSEN (für direkte Verwendung)
# =============================================================================
from .funktion import (
    Funktion,
    erstelle_funktion_automatisch,
)

# =============================================================================
# SYMBOLISCHE KOMPONENTEN
# =============================================================================
from .lineare_gleichungssysteme import (
    LineareGleichung,
    interpolationspolynom,
    plotte_loesung,
)

# Duplicate imports removed - these are already imported from .api above
# Duplicate import removed - already imported from .api
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

# =============================================================================
# SYMBOLISCHE KOMPONENTEN
# =============================================================================
from .taylor import (
    taylorpolynom,
    tangente,
)
from .visualisierung import Graph

# Vordefinierte Variablen und Parameter für schnellen Zugriff
x = Variable("x")
t = Variable("t")
a = Parameter("a")
k = Parameter("k")

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
    "GemischteFunktion",
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
    "Nullstellen",  # Add this
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
