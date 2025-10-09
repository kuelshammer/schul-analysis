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
from .wrapper import (
    BinomialPDF,
    BinomialCDF,
    NormalPDF,
    NormalCDF,
    NormalIntervall,
)
from .visualisierung import (
    zeichne_binomialverteilung,
    zeichne_normalverteilung,
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
