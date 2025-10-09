"""
Punkte, Geraden und Ebenen für die Analytische Geometrie

Grundlegende Klassen für Vektoren, Punkte, Geraden und Ebenen
mit Operationen und Berechnungen im 2D und 3D Raum
"""

from typing import Union, List, Tuple
import sympy as sp
from sympy import symbols, Matrix, simplify, solve

from ..gemeinsam import *


class Punkt:
    """Klasse für Punkte im 2D oder 3D Raum"""

    def __init__(self, koordinaten: List[Union[float, sp.Expr]], name: str = "P"):
        """
        Args:
            koordinaten: Liste mit 2 oder 3 Koordinaten [x, y] oder [x, y, z]
            name: Name des Punktes (z.B. "P", "A", etc.)
        """
        if len(koordinaten) not in [2, 3]:
            raise ValueError("Punkt muss 2 oder 3 Koordinaten haben")

        self.koordinaten = koordinaten
        self.name = name
        self.dimension = len(koordinaten)

    def __str__(self) -> str:
        if self.dimension == 2:
            return f"{self.name}({self.koordinaten[0]}, {self.koordinaten[1]})"
        else:
            return f"{self.name}({self.koordinaten[0]}, {self.koordinaten[1]}, {self.koordinaten[2]})"

    def __repr__(self) -> str:
        return self.__str__()

    def als_matrix(self) -> Matrix:
        """Gibt den Punkt als Spaltenvektor zurück"""
        return Matrix(self.koordinaten)

    def abstand_zu(self, other: "Punkt") -> sp.Expr:
        """Berechnet den Abstand zu einem anderen Punkt"""
        if self.dimension != other.dimension:
            raise ValueError("Punkte müssen gleiche Dimension haben")

        sum_quadrate = 0
        for i in range(self.dimension):
            diff = self.koordinaten[i] - other.koordinaten[i]
            sum_quadrate += diff**2

        return sp.sqrt(sum_quadrate)

    def __add__(self, other: "Punkt") -> "Punkt":
        """Vektoraddition"""
        if self.dimension != other.dimension:
            raise ValueError("Punkte müssen gleiche Dimension haben")

        neue_koordinaten = [
            self.koordinaten[i] + other.koordinaten[i] for i in range(self.dimension)
        ]
        return Punkt(neue_koordinaten, f"{self.name}+{other.name}")

    def __sub__(self, other: "Punkt") -> "Punkt":
        """Vektorsubtraktion"""
        if self.dimension != other.dimension:
            raise ValueError("Punkte müssen gleiche Dimension haben")

        neue_koordinaten = [
            self.koordinaten[i] - other.koordinaten[i] for i in range(self.dimension)
        ]
        return Punkt(neue_koordinaten, f"{self.name}-{other.name}")

    def __mul__(self, skalar: Union[float, sp.Expr]) -> "Punkt":
        """Skalare Multiplikation"""
        neue_koordinaten = [self.koordinaten[i] * skalar for i in range(self.dimension)]
        return Punkt(neue_koordinaten, f"{skalar}·{self.name}")


class Gerade:
    """Klasse für Geraden in der Form g: X = A + r·V"""

    def __init__(self, aufpunkt: Punkt, richtungsvektor: Punkt, name: str = "g"):
        """
        Args:
            aufpunkt: Aufpunkt der Geraden
            richtungsvektor: Richtungsvektor der Geraden
            name: Name der Geraden (z.B. "g", "h", etc.)
        """
        if aufpunkt.dimension != richtungsvektor.dimension:
            raise ValueError(
                "Aufpunkt und Richtungsvektor müssen gleiche Dimension haben"
            )

        self.aufpunkt = aufpunkt
        self.richtungsvektor = richtungsvektor
        self.name = name
        self.dimension = aufpunkt.dimension

    def __str__(self) -> str:
        if self.dimension == 2:
            return f"{self.name}: X = {self.aufpunkt} + r·{self.richtungsvektor}"
        else:
            return f"{self.name}: X = {self.aufpunkt} + r·{self.richtungsvektor}"

    def __repr__(self) -> str:
        return self.__str__()

    def enthaelt_punkt(self, punkt: Punkt) -> bool:
        """Prüft, ob ein Punkt auf der Geraden liegt"""
        if self.dimension != punkt.dimension:
            return False

        # Löse A + r·V = P für r
        for i in range(self.dimension):
            gleichung = sp.Eq(
                self.aufpunkt.koordinaten[i]
                + symbols("r") * self.richtungsvektor.koordinaten[i],
                punkt.koordinaten[i],
            )
            loesung = solve(gleichung, symbols("r"))
            if loesung:
                return True
        return False

    def schnittpunkt_mit(self, other: "Gerade") -> Union[Punkt, None]:
        """Berechnet den Schnittpunkt mit einer anderen Geraden"""
        if self.dimension != other.dimension:
            raise ValueError("Geraden müssen gleiche Dimension haben")

        if self.dimension == 2:
            # 2D: Löse das Gleichungssystem
            r, s = symbols("r s")

            # Gleichungssystem: A1 + r·V1 = A2 + s·V2
            gleichungen = []
            for i in range(2):
                gl = sp.Eq(
                    self.aufpunkt.koordinaten[i]
                    + r * self.richtungsvektor.koordinaten[i],
                    other.aufpunkt.koordinaten[i]
                    + s * other.richtungsvektor.koordinaten[i],
                )
                gleichungen.append(gl)

            loesung = solve(gleichungen, [r, s])
            if loesung:
                r_wert = loesung[r]
                # Berechnung des Schnittpunkts
                schnitt_koordinaten = [
                    self.aufpunkt.koordinaten[i]
                    + r_wert * self.richtungsvektor.koordinaten[i]
                    for i in range(2)
                ]
                return Punkt(schnitt_koordinaten, f"{self.name}∩{other.name}")

        return None  # Kein Schnittpunkt gefunden oder parallel


class Ebene:
    """Klasse für Ebenen in der Form E: X = A + r·U + s·V"""

    def __init__(
        self,
        aufpunkt: Punkt,
        richtungsvektor1: Punkt,
        richtungsvektor2: Punkt,
        name: str = "E",
    ):
        """
        Args:
            aufpunkt: Aufpunkt der Ebene
            richtungsvektor1: Erster Richtungsvektor
            richtungsvektor2: Zweiter Richtungsvektor
            name: Name der Ebene (z.B. "E", "F", etc.)
        """
        if not (
            aufpunkt.dimension
            == richtungsvektor1.dimension
            == richtungsvektor2.dimension
            == 3
        ):
            raise ValueError("Ebenen müssen 3-dimensional sein")

        self.aufpunkt = aufpunkt
        self.richtungsvektor1 = richtungsvektor1
        self.richtungsvektor2 = richtungsvektor2
        self.name = name
        self.dimension = 3

    def __str__(self) -> str:
        return f"{self.name}: X = {self.aufpunkt} + r·{self.richtungsvektor1} + s·{self.richtungsvektor2}"

    def __repr__(self) -> str:
        return self.__str__()

    def normalenvektor(self) -> Punkt:
        """Berechnet den Normalenvektor der Ebene (Kreuzprodukt)"""
        v1 = self.richtungsvektor1.als_matrix()
        v2 = self.richtungsvektor2.als_matrix()

        # Kreuzprodukt in 3D
        kreuz = (
            Matrix([[0, -v1[2], v1[1]], [v1[2], 0, -v1[0]], [-v1[1], v1[0], 0]]) * v2
        )

        return Punkt([kreuz[0], kreuz[1], kreuz[2]], f"n_{self.name}")

    def enthaelt_punkt(self, punkt: Punkt) -> bool:
        """Prüft, ob ein Punkt in der Ebene liegt"""
        if self.dimension != punkt.dimension:
            return False

        # Löse A + r·U + s·V = P für r und s
        r, s = symbols("r s")
        gleichungen = []

        for i in range(3):
            gl = sp.Eq(
                self.aufpunkt.koordinaten[i]
                + r * self.richtungsvektor1.koordinaten[i]
                + s * self.richtungsvektor2.koordinaten[i],
                punkt.koordinaten[i],
            )
            gleichungen.append(gl)

        loesung = solve(gleichungen, [r, s])
        return bool(loesung)


# Komfort-Funktionen
def ursprung(dimension: int = 2) -> Punkt:
    """Erzeugt den Ursprungspunkt"""
    return Punkt([0] * dimension, "O")


def punkt_mit_koordinaten(
    x: Union[float, sp.Expr],
    y: Union[float, sp.Expr],
    z: Union[float, sp.Expr] = None,
    name: str = "P",
) -> Punkt:
    """Erzeugt einen Punkt mit gegebenen Koordinaten"""
    if z is None:
        return Punkt([x, y], name)
    else:
        return Punkt([x, y, z], name)


def gerade_durch_zwei_punkte(p1: Punkt, p2: Punkt, name: str = "g") -> Gerade:
    """Erzeugt eine Gerade durch zwei Punkte"""
    richtungsvektor = p2 - p1
    return Gerade(p1, richtungsvektor, name)


def ebene_durch_drei_punkte(p1: Punkt, p2: Punkt, p3: Punkt, name: str = "E") -> Ebene:
    """Erzeugt eine Ebene durch drei Punkte"""
    v1 = p2 - p1
    v2 = p3 - p1
    return Ebene(p1, v1, v2, name)
