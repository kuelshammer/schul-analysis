"""
Quadratische Funktionen für das Schul-Analysis Framework.

Spezialisierte Klasse für quadratische Funktionen der Form f(x) = ax² + bx + c.
"""

import sympy as sp

from .ganzrationale import GanzrationaleFunktion


class QuadratischeFunktion(GanzrationaleFunktion):
    """
    Pädagogischer Wrapper für quadratische Funktionen.

    Diese Klasse bietet spezialisierte Methoden für quadratische Funktionen
    der Form f(x) = ax² + bx + c mit deutschen Fehlermeldungen.

    Examples:
        >>> f = QuadratischeFunktion("x^2 - 4x + 3")
        >>> g = QuadratischeFunktion([1, -4, 3])  # x² - 4x + 3
        >>> h = QuadratischeFunktion(a=1, b=-4, c=3)  # x² - 4x + 3
    """

    def __init__(
        self,
        eingabe: str | list[float] | dict[int, float] | sp.Basic | None = None,
        a: float | None = None,
        b: float | None = None,
        c: float | None = None,
        variable: str | None = None,
        parameter: list[str] | None = None,
    ):
        """
        Konstruktor für quadratische Funktionen.

        Args:
            eingabe: String ("x^2-4x+3"), Liste ([1, -4, 3]), oder SymPy-Ausdruck
            a: Öffnungsfaktor (alternativ zur eingabe)
            b: Koeffizient von x (alternativ zur eingabe)
            c: Konstanter Term (alternativ zur eingabe)
            variable: Variablenname (Standard: x)
            parameter: Liste von Parameternamen
        """
        # Konstruiere eingabe aus a, b, c, falls angegeben
        if a is not None and b is not None and c is not None:
            if eingabe is not None:
                raise ValueError("Entweder eingabe ODER a,b,c angeben, nicht beides!")

            # Baue den Term mit korrekten Vorzeichen
            teile = []
            if a != 0:
                teile.append(f"{a}x^2" if abs(a) != 1 else ("x^2" if a > 0 else "-x^2"))
            if b != 0:
                if b > 0:
                    teile.append(f"+ {b}x" if abs(b) != 1 else "+ x") if a != 0 else (
                        f"{b}x" if abs(b) != 1 else "x"
                    )
                else:
                    teile.append(f"- {abs(b)}x" if abs(b) != 1 else "- x")
            if c != 0:
                if c > 0:
                    teile.append(f"+ {c}") if len(teile) > 0 else f"{c}"
                else:
                    teile.append(f"- {abs(c)}")

            eingabe = " ".join(teile) if teile else "0"
        elif a is not None or b is not None or c is not None:
            raise ValueError(
                "Bei Angabe von a,b,c müssen alle drei Werte angegeben werden!"
            )
        elif eingabe is None:
            raise ValueError("Entweder eingabe ODER a,b,c angeben!")

        # Speichere a, b, c für direkten Zugriff
        self._a = a
        self._b = b
        self._c = c

        super().__init__(eingabe, variable, parameter)

        # 🔥 PÄDAGOGISCHE VALIDIERUNG - muss quadratisch sein! 🔥
        if not self.ist_quadratisch():
            raise TypeError(
                f"Die Eingabe '{self.original_eingabe}' ist keine quadratische Funktion! "
                "Eine quadratische Funktion muss die Form f(x) = ax² + bx + c haben und darf nicht linear sein. "
                "Hast du vielleicht eine lineare Funktion (ohne x²) oder eine höhergradige Funktion gemeint?"
            )

    @property
    def oeffnungsfaktor(self) -> float | sp.Basic:
        """Gibt den Öffnungsfaktor a zurück"""
        if self._a is not None:
            return self._a
        # Extrahiere x²-Koeffizient aus den Koeffizienten
        if len(self.koeffizienten) >= 3:
            return self.koeffizienten[-1]  # x²-Koeffizient
        else:
            return 0

    @property
    def scheitelpunkt(self) -> tuple[float | sp.Basic, float | sp.Basic]:
        """Gibt den Scheitelpunkt (x_s, y_s) zurück"""
        # Für quadratische Funktion: x_s = -b/(2a), y_s = f(x_s)
        a = self.oeffnungsfaktor
        if a == 0:
            raise ValueError("Eine konstante Funktion hat keinen Scheitelpunkt")

        # Extrahiere b-Koeffizient
        b_koeff = 0
        if len(self.koeffizienten) >= 2:
            b_koeff = self.koeffizienten[-2]

        x_s = -b_koeff / (2 * a)
        y_s = self.wert(x_s)
        return (x_s, y_s)

    def ist_offen_nach_oben(self) -> bool:
        """Prüft, ob die Parabel nach oben geöffnet ist"""
        return self.oeffnungsfaktor > 0

    def ist_offen_nach_unten(self) -> bool:
        """Prüft, ob die Parabel nach unten geöffnet ist"""
        return self.oeffnungsfaktor < 0

    def hat_scheitelpunkt_minimum(self) -> bool:
        """Prüft, ob der Scheitelpunkt ein Minimum ist"""
        return self.ist_offen_nach_oben()

    def hat_scheitelpunkt_maximum(self) -> bool:
        """Prüft, ob der Scheitelpunkt ein Maximum ist"""
        return self.ist_offen_nach_unten()

    def anzahl_nullstellen(self) -> int:
        """Gibt die Anzahl der reellen Nullstellen zurück"""
        try:
            nullstellen = self.nullstellen
            return len(nullstellen)
        except Exception:
            return 0

    def diskriminante(self) -> float | sp.Basic:
        """Berechnet die Diskriminante D = b² - 4ac"""
        if self._a is not None and self._b is not None and self._c is not None:
            return self._b**2 - 4 * self._a * self._c

        # Extrahiere Koeffizienten aus der Funktion
        a = self.oeffnungsfaktor
        b_koeff = (
            self.koeffizienten[-2] if len(self.koeffizienten) >= 2 else sp.Integer(0)
        )
        c_koeff = (
            self.koeffizienten[0] if len(self.koeffizienten) >= 1 else sp.Integer(0)
        )

        return b_koeff**2 - 4 * a * c_koeff

    def hat_zwei_nullstellen(self) -> bool:
        """Prüft, ob die Funktion zwei reelle Nullstellen hat"""
        return self.diskriminante() > 0

    def hat_eine_nullstelle(self) -> bool:
        """Prüft, ob die Funktion genau eine reelle Nullstelle hat"""
        return self.diskriminante() == 0

    def hat_keine_nullstellen(self) -> bool:
        """Prüft, ob die Funktion keine reellen Nullstellen hat"""
        return self.diskriminante() < 0

    def achse_symmetrie_x(self) -> float | sp.Basic:
        """Gibt die x-Koordinate der Symmetrieachse zurück"""
        x_s, _ = self.scheitelpunkt
        return x_s

    def ist_symmetrisch_zur_y_achse(self) -> bool:
        """Prüft, ob die Funktion zur y-Achse symmetrisch ist (b = 0)"""
        if self._b is not None:
            return self._b == 0
        b_koeff = float(self.koeffizienten[-2]) if len(self.koeffizienten) >= 2 else 0
        return b_koeff == 0

    def __str__(self):
        return self.term()

    def __repr__(self):
        return f"QuadratischeFunktion('{self.term()}')"
