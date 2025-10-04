"""
Symbolische Größen (Variable und Parameter) für das Schul-Analysis Framework.

Dieses Modul bietet konsistente Definitionen von symbolischen Variablen und Parametern,
die von allen anderen Modulen gemeinsam genutzt werden können.
"""

from abc import ABC
from dataclasses import dataclass

import sympy as sp


@dataclass
class SymbolischeGroesse(ABC):
    """
    Abstrakte Basisklasse für symbolische Größen (Variable und Parameter)

    Args:
        name: Name der symbolischen Größe (z.B. "x" oder "a")
    """

    name: str

    def __post_init__(self):
        """Erstellt ein SymPy-Symbol bei der Initialisierung"""
        self._symbol = sp.Symbol(self.name)

    @property
    def symbol(self) -> sp.Symbol:
        """Gibt das SymPy-Symbol zurück"""
        return self._symbol

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}')"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Variable(SymbolischeGroesse):
    """
    Repräsentiert eine symbolische Variable (z.B. x, y, t)

    Args:
        name: Name der Variable (z.B. "x")

    Beispiele:
        >>> x = Variable("x")
        >>> t = Variable("t")
    """

    pass


@dataclass
class Parameter(SymbolischeGroesse):
    """
    Repräsentiert einen symbolischen Parameter (z.B. a, b, c)

    Args:
        name: Name des Parameters (z.B. "a")

    Beispiele:
        >>> a = Parameter("a")
        >>> b = Parameter("b")
    """

    pass


# Interne Versionen zur Vermeidung von zirkulären Imports
@dataclass
class _Variable:
    """Interne Variable-Klasse für symbolische Berechnungen"""

    name: str

    def __post_init__(self):
        self._symbol = sp.Symbol(self.name)

    @property
    def symbol(self) -> sp.Symbol:
        return self._symbol

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"_Variable('{self.name}')"


@dataclass
class _Parameter:
    """Interne Parameter-Klasse für symbolische Berechnungen"""

    name: str

    def __post_init__(self):
        self._symbol = sp.Symbol(self.name)

    @property
    def symbol(self) -> sp.Symbol:
        return self._symbol

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"_Parameter('{self.name}')"
