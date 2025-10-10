"""
Stochastik-Modul des Schul-Mathematik Frameworks

Enthält alle Funktionalitäten für Wahrscheinlichkeitsrechnung,
statistische Verteilungen, Datenanalyse, etc.
"""

from .verteilungen import (
    Binomialverteilung,
    Normalverteilung,
    StatistischeVerteilung,
)
from .visualisierung import (
    zeichne_binomialverteilung,
    zeichne_normalverteilung,
)
from .wrapper import (
    BinomialCDF,
    BinomialPDF,
    NormalCDF,
    NormalIntervall,
    NormalPDF,
)

__all__ = [
    # Verteilungsklassen
    "Binomialverteilung",
    "Normalverteilung",
    "StatistischeVerteilung",
    # Wrapper-Funktionen
    "BinomialPDF",
    "BinomialCDF",
    "NormalPDF",
    "NormalCDF",
    "NormalIntervall",
    # Visualisierung
    "zeichne_binomialverteilung",
    "zeichne_normalverteilung",
]
