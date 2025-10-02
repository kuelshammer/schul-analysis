"""
Lineare Gleichungssysteme für Funktionen

Dieses Modul implementiert die Lösung linearer Gleichungssysteme für parametrische Funktionen.
Die Syntax LGS(f(3)==4, f(2)==0, f1(0)==0) ermöglicht die intuitive Bestimmung von Parametern
aus Funktionsbedingungen.

Basierend auf SymPy für symbolische Mathematik.
"""

from dataclasses import dataclass

import sympy as sp


@dataclass
class LineareGleichung:
    """Repräsentiert eine einzelne lineare Gleichung"""

    linke_seite: sp.Expr  # Symbolischer Ausdruck (z.B. 9*a + 3*b + c)
    rechte_seite: float  # Numerischer Wert (z.B. 4)
    beschreibung: str  # Beschreibung für pädagogische Zwecke

    def __post_init__(self):
        """Normalisiere die Gleichung auf die Form ... = 0"""
        self.gleichung = self.linke_seite - self.rechte_seite

    def extrahiere_koeffizienten(
        self, parameter: list[sp.Symbol]
    ) -> dict[sp.Symbol, float]:
        """
        Extrahiert die Koeffizienten der Parameter aus der Gleichung.

        Args:
            parameter: Liste der Parameter (z.B. [a, b, c])

        Returns:
            Dictionary mit Parameter -> Koeffizient
        """
        koeffizienten = {}

        for p in parameter:
            try:
                # Extrahiere Koeffizient für diesen Parameter
                koeff = self.gleichung.coeff(p)
                # Konvertiere zu float, falls möglich
                if koeff.is_number:
                    koeffizienten[p] = float(koeff)
                else:
                    koeffizienten[p] = koeff
            except (TypeError, AttributeError):
                koeffizienten[p] = 0.0

        return koeffizienten

    def __str__(self):
        """Didaktische String-Darstellung"""
        return f"{self.beschreibung}: {self.linke_seite} = {self.rechte_seite}"


class LineareGleichungssystem:
    """Repräsentiert ein lineares Gleichungssystem"""

    def __init__(self, gleichungen: list[LineareGleichung]):
        """
        Initialisiert das LGS mit einer Liste von Gleichungen.

        Args:
            gleichungen: Liste von LineareGleichung-Objekten
        """
        self.gleichungen = gleichungen
        self._parameter = None
        self._matrix = None
        self._vektor = None
        self._lösung = None

    def _finde_parameter(self) -> list[sp.Symbol]:
        """
        Findet alle Parameter in den Gleichungen.

        Returns:
            Liste der gefundenen Parameter-Symbole
        """
        alle_symbole = set()
        for gl in self.gleichungen:
            alle_symbole.update(gl.gleichung.free_symbols)

        # Filtere nur Parameter (keine Variablen oder andere Symbole)
        # Für jetzt nehmen wir an, dass alle Symbole Parameter sind
        return sorted(alle_symbole, key=lambda x: str(x))

    @property
    def parameter(self) -> list[sp.Symbol]:
        """Die Parameter des Gleichungssystems"""
        if self._parameter is None:
            self._parameter = self._finde_parameter()
        return self._parameter

    @property
    def anzahl_gleichungen(self) -> int:
        """Anzahl der Gleichungen"""
        return len(self.gleichungen)

    @property
    def anzahl_parameter(self) -> int:
        """Anzahl der Parameter"""
        return len(self.parameter)

    def erstelle_matrix_und_vektor(self) -> tuple[sp.Matrix, sp.Matrix]:
        """
        Erstellt die Koeffizientenmatrix und den Ergebnisvektor.

        Returns:
            Tuple (Matrix, Vektor)
        """
        if self._matrix is not None and self._vektor is not None:
            return self._matrix, self._vektor

        # n and m were unused, removing them

        # Initialisiere Matrix und Vektor
        matrix_data = []
        vektor_data = []

        for _i, gl in enumerate(self.gleichungen):
            koeffizienten = gl.extrahiere_koeffizienten(self.parameter)

            # Erstelle Zeile für die Matrix
            zeile = [koeffizienten.get(p, 0.0) for p in self.parameter]
            matrix_data.append(zeile)

            # Rechtes Seite der Gleichung (negiert, weil wir ...=0 Form haben)
            konstante = gl.gleichung
            for p in self.parameter:
                konstante = konstante.subs(p, 0)

            if konstante.is_number:
                vektor_data.append(-float(konstante))
            else:
                vektor_data.append(0.0)

        self._matrix = sp.Matrix(matrix_data)
        self._vektor = sp.Matrix(vektor_data)

        return self._matrix, self._vektor

    def löse(self) -> dict[sp.Symbol, float]:
        """
        Löse das lineare Gleichungssystem.

        Returns:
            Dictionary mit Parameter-Werten

        Raises:
            ValueError: Wenn das System keine eindeutige Lösung hat
        """
        if self._lösung is not None:
            return self._lösung

        A, b = self.erstelle_matrix_und_vektor()

        # Prüfe die Lösbarkeit
        if A.rows != A.cols:
            raise ValueError(
                f"Rechenfehler: Du hast {self.anzahl_parameter} Unbekannte, "
                f"aber {self.anzahl_gleichungen} Gleichungen angegeben. "
                f"Um eine eindeutige Lösung zu finden, brauchst du genauso viele "
                f"Gleichungen wie Unbekannte."
            )

        try:
            # Versuche zu lösen
            lösung_symbols = sp.linsolve((A, b), self.parameter)

            if lösung_symbols.is_EmptySet:
                raise ValueError(
                    "Logikfehler: Dieses Gleichungssystem hat keine Lösung. "
                    "Deine Bedingungen widersprechen sich. Überprüfe, ob du "
                    "zum Beispiel einem Punkt zwei verschiedene y-Werte zugewiesen hast."
                )

            # Extrahiere die Lösung
            if hasattr(lösung_symbols, "__iter__") and len(lösung_symbols) > 0:
                lösung_tuple = list(lösung_symbols)[0]

                if len(lösung_tuple) != len(self.parameter):
                    raise ValueError(
                        "Information fehlt: Dieses Gleichungssystem hat unendlich viele "
                        "Lösungen. Deine Bedingungen sind nicht alle voneinander abhängig. "
                        "Du hast nicht genügend Informationen für eine eindeutige Funktion."
                    )

                # Konvertiere zu Dictionary
                self._lösung = {}
                for param, wert in zip(self.parameter, lösung_tuple):
                    if wert.is_number:
                        self._lösung[param] = float(wert)
                    else:
                        self._lösung[param] = wert

            else:
                raise ValueError("Unerwartete Lösungsform von SymPy")

        except Exception as e:
            if "singular" in str(e).lower():
                raise ValueError(
                    "Das Gleichungssystem ist nicht eindeutig lösbar. "
                    "Die Bedingungen sind linear abhängig."
                )
            else:
                raise ValueError(f"Fehler beim Lösen: {str(e)}")

        return self._lösung

    def löse_für_funktion(self, funktion):
        """
        Erstellt eine neue Funktion mit den gelösten Parametern.

        Args:
            funktion: Die ursprüngliche parametrische Funktion

        Returns:
            Neue Funktion mit eingesetzten Parameterwerten
        """
        lösung = self.löse()

        # Ersetze Parameter in der Funktion
        if hasattr(funktion, "mit_wert"):
            return funktion.mit_wert(**{str(p): v for p, v in lösung.items()})
        else:
            # Fallback: Ersetze im symbolischen Ausdruck
            for param, wert in lösung.items():
                funktion = funktion.subs(param, wert)
            return funktion

    def zeige_gleichungen(self):
        """Zeigt die Gleichungen in didaktischer Form"""
        print("Extrahierte Gleichungen:")
        print("-" * 40)

        for i, gl in enumerate(self.gleichungen, 1):
            # Zeige die Gleichung in vereinfachter Form
            gl_str = str(gl.linke_seite)
            rhs_str = str(gl.rechte_seite)
            print(f"{chr(64 + i)}: {gl_str} = {rhs_str}")

        print()

    def zeige_matrix(self):
        """Zeigt die Matrix-Form des Gleichungssystems"""
        A, b = self.erstelle_matrix_und_vektor()

        print("Matrix-Form:")
        print("-" * 40)

        # Zeige Parameter-Namen
        param_names = [str(p) for p in self.parameter]
        print(f"    {' | '.join(param_names)}")
        print(f"    {'-' * (len(' | '.join(param_names)) + 4)}")

        # Zeige jede Zeile
        for i in range(A.rows):
            zeile_vals = [str(A[i, j]) for j in range(A.cols)]
            print(f"A = | {' | '.join(zeile_vals)} | {b[i, 0]}")

        print()

    def zeige_unbekannte(self):
        """Zeigt die erkannten Unbekannten"""
        print("Erkannte Parameter:")
        print("-" * 20)
        for param in self.parameter:
            print(f"- {param}")
        print()

    def __str__(self):
        """String-Darstellung des Gleichungssystems"""
        return f"Lineare Gleichungssystem mit {self.anzahl_gleichungen} Gleichungen und {self.anzahl_parameter} Unbekannten"


def LGS(*bedingungen) -> LineareGleichungssystem:
    """
    Haupt-Funktion zur Erstellung eines linearen Gleichungssystems.

    Args:
        *bedingungen: Liste von Gleichungen der Form f(x) == wert

    Returns:
        LineareGleichungssystem-Objekt

    Examples:
        >>> x = Variable("x")
        >>> a, b, c = Parameter("a"), Parameter("b"), Parameter("c")
        >>> f = ParametrischeFunktion("a*x^2 + b*x + c", x)
        >>> system = LGS(f(3) == 4, f(2) == 0, f.ableitung()(0) == 0)
        >>> lösungen = system.löse()
    """
    # Konvertiere alle Bedingungen zu LineareGleichung-Objekten
    gleichungen = []

    for i, bedingung in enumerate(bedingungen):
        if hasattr(bedingung, "gleichung") and isinstance(bedingung, LineareGleichung):
            gleichungen.append(bedingung)
        else:
            raise ValueError(f"Bedingung {i + 1} ist keine gültige Gleichung")

    return LineareGleichungssystem(gleichungen)


# Zusätzliche Hilfsfunktionen für komplexere Anwendungsfälle
def LGS_aus_matrix(
    matrix: list[list[float]], vektor: list[float]
) -> LineareGleichungssystem:
    """
    Erstellt ein LGS direkt aus einer Matrix und einem Vektor.

    Args:
        matrix: Koeffizientenmatrix als Liste von Listen
        vektor: Ergebnisvektor als Liste

    Returns:
        LineareGleichungssystem-Objekt
    """
    # Erstelle symbolische Parameter
    n_params = len(matrix[0]) if matrix else 0
    parameter = [sp.Symbol(f"p{i}") for i in range(n_params)]

    gleichungen = []
    for i, (zeile, wert) in enumerate(zip(matrix, vektor)):
        linke_seite = sp.sympify(
            sum(koeff * param for koeff, param in zip(zeile, parameter))
        )
        gleichung = LineareGleichung(
            linke_seite=linke_seite,
            rechte_seite=wert,
            beschreibung=f"Matrix-Gleichung {i + 1}",
        )
        gleichungen.append(gleichung)

    return LineareGleichungssystem(gleichungen)
