"""
Wrapper-Funktionen für das Stochastik-Modul im deutschen Stil

Bieten eine intuitive, unterrichtsnahe Syntax für statistische Berechnungen
"""


import sympy as sp
from sympy import stats

from ..gemeinsam import *


def BinomialPDF(
    n: int | sp.Expr, p: float | sp.Expr, k: int | sp.Expr
) -> sp.Expr:
    """Berechnet P(X=k) für Binomialverteilung

    Args:
        n: Anzahl der Versuche
        p: Erfolgswahrscheinlichkeit
        k: Anzahl der Erfolge

    Returns:
        Wahrscheinlichkeit P(X=k)
    """
    X = stats.Binomial("X", n, p)
    return stats.density(X)(k)


def BinomialCDF(
    n: int | sp.Expr, p: float | sp.Expr, k: int | sp.Expr
) -> sp.Expr:
    """Berechnet P(X≤k) für Binomialverteilung

    Args:
        n: Anzahl der Versuche
        p: Erfolgswahrscheinlichkeit
        k: Obere Grenze (inklusive)

    Returns:
        Kumulative Wahrscheinlichkeit P(X≤k)
    """
    X = stats.Binomial("X", n, p)
    return stats.cdf(X)(k)


def NormalPDF(
    mu: float | sp.Expr, sigma: float | sp.Expr, x: float | sp.Expr
) -> sp.Expr:
    """Berechnet f(x) für Normalverteilung

    Args:
        mu: Erwartungswert
        sigma: Standardabweichung
        x: Stelle an der die Dichte berechnet wird

    Returns:
        Wahrscheinlichkeitsdichte f(x)
    """
    X = stats.Normal("X", mu, sigma)
    return stats.density(X)(x)


def NormalCDF(
    mu: float | sp.Expr, sigma: float | sp.Expr, x: float | sp.Expr
) -> sp.Expr:
    """Berechnet F(x) für Normalverteilung

    Args:
        mu: Erwartungswert
        sigma: Standardabweichung
        x: Stelle an der die Verteilungsfunktion berechnet wird

    Returns:
        Kumulative Wahrscheinlichkeit F(x) = P(X≤x)
    """
    X = stats.Normal("X", mu, sigma)
    return stats.cdf(X)(x)


def NormalIntervall(
    mu: float | sp.Expr,
    sigma: float | sp.Expr,
    a: float | sp.Expr,
    b: float | sp.Expr,
) -> sp.Expr:
    """Berechnet P(a ≤ X ≤ b) für Normalverteilung

    Args:
        mu: Erwartungswert
        sigma: Standardabweichung
        a: Untere Intervallgrenze
        b: Obere Intervallgrenze

    Returns:
        Wahrscheinlichkeit P(a ≤ X ≤ b)
    """
    X = stats.Normal("X", mu, sigma)
    return stats.P(a <= X <= b)


def StandardnormalPDF(x: float | sp.Expr) -> sp.Expr:
    """Berechnet f(x) für Standardnormalverteilung (μ=0, σ=1)

    Args:
        x: Stelle an der die Dichte berechnet wird

    Returns:
        Wahrscheinlichkeitsdichte φ(x)
    """
    return NormalPDF(0, 1, x)


def StandardnormalCDF(x: float | sp.Expr) -> sp.Expr:
    """Berechnet F(x) für Standardnormalverteilung (μ=0, σ=1)

    Args:
        x: Stelle an der die Verteilungsfunktion berechnet wird

    Returns:
        Kumulative Wahrscheinlichkeit Φ(x) = P(Z≤x)
    """
    return NormalCDF(0, 1, x)


# Komfort-Funktionen für häufige Berechnungen
def Sigma1Bereich(
    mu: float | sp.Expr = 0, sigma: float | sp.Expr = 1
) -> sp.Expr:
    """Berechnet P(μ-σ ≤ X ≤ μ+σ) für Normalverteilung (ca. 68%)"""
    return NormalIntervall(mu, sigma, mu - sigma, mu + sigma)


def Sigma2Bereich(
    mu: float | sp.Expr = 0, sigma: float | sp.Expr = 1
) -> sp.Expr:
    """Berechnet P(μ-2σ ≤ X ≤ μ+2σ) für Normalverteilung (ca. 95%)"""
    return NormalIntervall(mu, sigma, mu - 2 * sigma, mu + 2 * sigma)


def Sigma3Bereich(
    mu: float | sp.Expr = 0, sigma: float | sp.Expr = 1
) -> sp.Expr:
    """Berechnet P(μ-3σ ≤ X ≤ μ+3σ) für Normalverteilung (ca. 99.7%)"""
    return NormalIntervall(mu, sigma, mu - 3 * sigma, mu + 3 * sigma)
