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
    Polstellen,
    Schnittpunkt,
    Wendepunkte,
    Wendestellen,
    Wert,
)
from .api import (
    LGS,
    # Komfort-Funktionen für den Unterricht
    ableitung,
    analysiere_funktion,
    auswerten,
    erstelle_exponential_rationale_funktion,
    erstelle_funktion,
    erstelle_lineares_gleichungssystem,
    erstelle_polynom,
    extrema,
    integral,
    nullstellen,
    symmetrie,
    wendepunkte,
    zeichne,
    zeige_analyse,
)

# =============================================================================
# FUNKTIONSKLASSEN (für direkte Verwendung)
# =============================================================================
from .exponential import ExponentialFunktion
from .funktion import Funktion, erstelle_funktion_automatisch
from .ganzrationale import GanzrationaleFunktion
from .gebrochen_rationale import GebrochenRationaleFunktion
from .strukturiert import (
    KompositionFunktion,
    ProduktFunktion,
    QuotientFunktion,
    SummeFunktion,
    StrukturierteFunktion,
)

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
from .symbolic import Parameter, Variable
from .symmetrie import (
    Achsensymmetrie,
    Punktsymmetrie,
)
from .taylor import (
    tangente,
    taylorpolynom,
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
    "ableitung",
    "nullstellen",
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
]
