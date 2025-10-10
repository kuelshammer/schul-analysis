"""
Verteilungsklassen für das Stochastik-Modul

Basierend auf der Analyse von SymPy's statistischer Funktionalität
"""


import sympy as sp
from sympy import stats

from ..gemeinsam import *


class StatistischeVerteilung:
    """Basisklasse für statistische Verteilungen"""

    def __init__(self, name: str, verteilung_typ: str, parameter: dict):
        self.name = name
        self.verteilung_typ = verteilung_typ
        self.parameter = parameter

    def pdf(self, x: sp.Expr | float) -> sp.Expr:
        """Wahrscheinlichkeitsdichtefunktion oder Wahrscheinlichkeitsfunktion"""
        raise NotImplementedError("Muss in Unterklassen implementiert werden")

    def cdf(self, x: sp.Expr | float) -> sp.Expr:
        """Kumulative Verteilungsfunktion"""
        raise NotImplementedError("Muss in Unterklassen implementiert werden")

    def erwartungswert(self) -> sp.Expr:
        """Erwartungswert"""
        raise NotImplementedError("Muss in Unterklassen implementiert werden")

    def varianz(self) -> sp.Expr:
        """Varianz"""
        raise NotImplementedError("Muss in Unterklassen implementiert werden")

    def standardabweichung(self) -> sp.Expr:
        """Standardabweichung"""
        return sp.sqrt(self.varianz())


class Binomialverteilung(StatistischeVerteilung):
    """Binomialverteilung für Schul-Mathematik"""

    def __init__(self, name: str, n: int | sp.Expr, p: float | sp.Expr):
        super().__init__(name, "Binomial", {"n": n, "p": p})
        self.n = n
        self.p = p
        self.X = stats.Binomial(name, n, p)

    def pdf(self, k: sp.Expr | int) -> sp.Expr:
        """P(X=k) - Wahrscheinlichkeitsfunktion"""
        return stats.density(self.X)(k)

    def cdf(self, k: sp.Expr | int) -> sp.Expr:
        """P(X≤k) - Kumulative Verteilungsfunktion"""
        return stats.cdf(self.X)(k)

    def erwartungswert(self) -> sp.Expr:
        """E[X] = n*p"""
        return stats.E(self.X)

    def varianz(self) -> sp.Expr:
        """Var(X) = n*p*(1-p)"""
        return stats.variance(self.X)

    def __str__(self) -> str:
        return f"Binomialverteilung B({self.n}, {self.p})"


class Normalverteilung(StatistischeVerteilung):
    """Normalverteilung für Schul-Mathematik"""

    def __init__(
        self, name: str, mu: float | sp.Expr, sigma: float | sp.Expr
    ):
        super().__init__(name, "Normal", {"μ": mu, "σ": sigma})
        self.mu = mu
        self.sigma = sigma
        self.X = stats.Normal(name, mu, sigma)

    def pdf(self, x: sp.Expr | float) -> sp.Expr:
        """f(x) - Wahrscheinlichkeitsdichtefunktion"""
        return stats.density(self.X)(x)

    def cdf(self, x: sp.Expr | float) -> sp.Expr:
        """F(x) - Kumulative Verteilungsfunktion"""
        return stats.cdf(self.X)(x)

    def erwartungswert(self) -> sp.Expr:
        """E[X] = μ"""
        return stats.E(self.X)

    def varianz(self) -> sp.Expr:
        """Var(X) = σ²"""
        return stats.variance(self.X)

    def standardabweichung(self) -> sp.Expr:
        """σ"""
        return stats.std(self.X)

    def wahrscheinlichkeit_intervall(
        self, a: float | sp.Expr, b: float | sp.Expr
    ) -> sp.Expr:
        """P(a ≤ X ≤ b)"""
        return stats.P(a <= self.X <= b)

    def __str__(self) -> str:
        return f"Normalverteilung N({self.mu}, {self.sigma}²)"
