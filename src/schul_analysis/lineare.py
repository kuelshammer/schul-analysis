"""
Lineare Funktionen für das Schul-Analysis Framework.

Spezialisierte Klasse für lineare Funktionen der Form f(x) = mx + b.
"""


import sympy as sp

from .ganzrationale import GanzrationaleFunktion


class LineareFunktion(GanzrationaleFunktion):
    """
    Pädagogischer Wrapper für lineare Funktionen.

    Diese Klasse bietet spezialisierte Methoden für lineare Funktionen
    der Form f(x) = mx + b mit deutschen Fehlermeldungen.

    Examples:
        >>> f = LineareFunktion("2x + 3")
        >>> g = LineareFunktion([2, 3])  # 2x + 3
        >>> h = LineareFunktion(m=2, b=3)  # 2x + 3
    """

    def __init__(
        self,
        eingabe: str | list[float] | dict[int, float] | sp.Basic = None,
        m: float = None,
        b: float = None,
        variable: str = None,
        parameter: list[str] = None,
    ):
        """
        Konstruktor für lineare Funktionen.

        Args:
            eingabe: String ("2x+3"), Liste ([2, 3]), oder SymPy-Ausdruck
            m: Steigung (alternativ zur eingabe)
            b: y-Achsenabschnitt (alternativ zur eingabe)
            variable: Variablenname (Standard: x)
            parameter: Liste von Parameternamen
        """
        # Konstruiere eingabe aus m und b, falls angegeben
        if m is not None and b is not None:
            if eingabe is not None:
                raise ValueError("Entweder eingabe ODER m,b angeben, nicht beides!")
            eingabe = f"{m}x + {b}" if b >= 0 else f"{m}x - {abs(b)}"
        elif m is not None or b is not None:
            raise ValueError(
                "Bei Angabe von m und b müssen beide Werte angegeben werden!"
            )
        elif eingabe is None:
            raise ValueError("Entweder eingabe ODER m,b angeben!")

        # Speichere m und b für direkten Zugriff
        self._m = m
        self._b = b

        super().__init__(eingabe, variable, parameter)

        # 🔥 PÄDAGOGISCHE VALIDIERUNG - muss linear sein! 🔥
        if not self.ist_linear():
            raise TypeError(
                f"Die Eingabe '{self.original_eingabe}' ist keine lineare Funktion! "
                "Eine lineare Funktion muss die Form f(x) = mx + b haben. "
                "Hast du vielleicht eine quadratische Funktion (mit x²) gemeint?"
            )

    @property
    def steigung(self) -> float | sp.Basic:
        """Gibt die Steigung m zurück"""
        if self._m is not None:
            return self._m
        return self.get_steigung()

    @property
    def y_achsenabschnitt(self) -> float | sp.Basic:
        """Gibt den y-Achsenabschnitt b zurück"""
        if self._b is not None:
            return self._b
        return self.get_y_achsenabschnitt()

    @property
    def nullstelle(self) -> float | sp.Basic:
        """Gibt die Nullstelle zurück"""
        return self.get_nullstelle()

    def ist_steigend(self) -> bool:
        """Prüft, ob die Funktion steigend ist"""
        return self.steigung > 0

    def ist_fallend(self) -> bool:
        """Prüft, ob die Funktion fallend ist"""
        return self.steigung < 0

    def ist_horizontal(self) -> bool:
        """Prüft, ob die Funktion horizontal ist"""
        return self.steigung == 0

    def schnittpunkt_mit_y_achse(self) -> tuple[float | sp.Basic, float | sp.Basic]:
        """Gibt den Schnittpunkt mit der y-Achse zurück"""
        return (0, self.y_achsenabschnitt)

    def schnittpunkt_mit_x_achse(self) -> tuple[float | sp.Basic, float | sp.Basic]:
        """Gibt den Schnittpunkt mit der x-Achse zurück"""
        return (self.nullstelle, 0)

    def __str__(self):
        return self.term()

    def __repr__(self):
        return f"LineareFunktion('{self.term()}')"
