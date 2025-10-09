"""
Schul-Mathematik Framework - Schülerfreundliche API

Ein Python Framework für Schul-Mathematik mit exakter Berechnung, Marimo-Integration
und intuitiver API für Mathematiklehrer und Schüler.

PÄDAGOGISCHE KERNPRINZIPIEN:
- Deutsche API-Namen für den Mathematikunterricht
- Unterrichtsnahe Syntax: nullstellen(f) statt f.nullstellen()
- Einfache Anwendung für Schüler durch Nähe zur mathematischen Notation
- Drei Kernbereiche: Analysis, Stochastik, Analytische Geometrie
"""

# =============================================================================
# IMPORTS AUS ALLEN MODULEN
# =============================================================================

# Analysis-Modul (Kernfunktionalität)
from .analysis import *

# Stochastik-Modul
from .stochastik import *

# Geometrie-Modul (später zu erweitern)
# from .geometrie import *

# Gemeinsame Basisfunktionalität
from .gemeinsam import *

# =============================================================================
# VERSION
# =============================================================================

__version__ = "1.0.0"  # Hauptversion nach Umstrukturierung

# =============================================================================
# EXPORTLISTE - WAS BEI `from schul_mathematik import *` IMPORTIERT WIRD
# =============================================================================

__all__ = [
    # 🔥 ANALYSIS: SCHÜLERFREUNDLICHE API (Priorität für Unterricht)
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
    # 🏗️ ANALYSIS: FUNKTIONSKLASSEN
    "Funktion",
    "GanzrationaleFunktion",
    "ExponentialFunktion",
    "TrigonometrischeFunktion",
    "StrukturierteFunktion",
    "ProduktFunktion",
    "SummeFunktion",
    "QuotientFunktion",
    "KompositionFunktion",
    # 🔤 ANALYSIS: SYMBOLISCHE KOMPONENTEN
    "Variable",
    "Parameter",
    "x",
    "t",
    "a",
    "k",
    # 📊 ANALYSIS: VISUALISIERUNG
    "Graph",
    "Graph_parametrisiert",
    # 📊 ANALYSIS: TAYLOR-FUNKTIONEN
    "taylorpolynom",
    "tangente",
    # 📊 ANALYSIS: SPEZIALFUNKTIONEN
    "Achsensymmetrie",
    "Punktsymmetrie",
    "Schmiegparabel",
    "Schmiegkegel",
    "Schmieggerade",
    "HermiteInterpolation",
    "SchmiegkurveAllgemein",
    "Schmiegkurve",
    # 📐 ANALYSIS: LINEARE GLEICHUNGSSYSTEME
    "LineareGleichung",
    "LGS",
    "interpolationspolynom",
    "plotte_loesung",
    # 🧪 ANALYSIS: TEST-UTILS
    "assert_gleich",
    "assert_wert_gleich",
    # 🎲 STOCHASTIK: VERTEILUNGSKLASSEN
    "Binomialverteilung",
    "Normalverteilung",
    "StatistischeVerteilung",
    # 🎲 STOCHASTIK: WRAPPER-FUNKTIONEN
    "BinomialPDF",
    "BinomialCDF",
    "NormalPDF",
    "NormalCDF",
    "NormalIntervall",
    "StandardnormalPDF",
    "StandardnormalCDF",
    "Sigma1Bereich",
    "Sigma2Bereich",
    "Sigma3Bereich",
    # 📊 STOCHASTIK: VISUALISIERUNG
    "zeichne_binomialverteilung",
    "zeichne_normalverteilung",
    "zeichne_vergleich_zwei_normalverteilungen",
    # 📐 GEOMETRIE (wird später gefüllt)
    # "Punkt", "Gerade", "Ebene", "abstand_punkt_gerade", etc.
]
