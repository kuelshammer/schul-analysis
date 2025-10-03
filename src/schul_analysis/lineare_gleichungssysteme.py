"""
Lineare Gleichungssysteme für Funktionen

Dieses Modul implementiert die Lösung linearer Gleichungssysteme für parametrische Funktionen.
Die Syntax LGS(f(3)==4, f(2)==0, f1(0)==0) ermöglicht die intuitive Bestimmung von Parametern
aus Funktionsbedingungen.

Basierend auf SymPy für symbolische Mathematik.
"""

from dataclasses import dataclass
from typing import Protocol

import sympy as sp

# ====================
# Spezifische LGS-Fehlerklassen
# ====================


class LGSKeineLoesungError(ValueError):
    """Das Gleichungssystem hat keine Lösung"""

    pass


class LGSUnendlichVieleLoesungenError(ValueError):
    """Das Gleichungssystem hat unendlich viele Lösungen"""

    pass


class LGSNumerischeInstabilitaetError(ValueError):
    """Das Gleichungssystem ist numerisch instabil"""

    pass


class LGSInkonsistenzError(ValueError):
    """Die Gleichungen sind widersprüchlich"""

    pass


class ParametrischeFunktionProtocol(Protocol):
    """Protocol für Funktionen, die mit LGS kompatibel sein sollen"""

    def mit_wert(self, **kwargs) -> "ParametrischeFunktionProtocol":
        """Erstellt eine neue Funktion mit eingesetzten Parameterwerten"""
        ...

    def subs(self, param, wert):
        """SymPy-Substitutionsmethode als Fallback"""
        ...

    def wert(self, x: float) -> float:
        """Berechnet den Funktionswert an einer Stelle"""
        ...

    def term(self) -> str:
        """Gibt den Funktionsterm als String zurück"""
        ...

    def as_sympy_expr(self) -> sp.Expr:
        """Gibt den Funktionsterm als SymPy-Ausdruck zurück."""
        ...


@dataclass
class LineareGleichung:
    """Repräsentiert eine einzelne lineare Gleichung"""

    linke_seite: sp.Expr  # Symbolischer Ausdruck (z.B. 9*a + 3*b + c)
    rechte_seite: float  # Numerischer Wert (z.B. 4)
    beschreibung: str  # Beschreibung für pädagogische Zwecke

    def __post_init__(self):
        """Normalisiere die Gleichung auf die Form ... = 0 und validiere Typen."""
        if not isinstance(self.linke_seite, sp.Expr):
            try:
                # Versuche, eine Konvertierung zu ermöglichen
                self.linke_seite = sp.sympify(self.linke_seite)
            except (sp.SympifyError, TypeError):
                raise TypeError(
                    f"linke_seite muss ein SymPy-Ausdruck sein, ist aber {type(self.linke_seite)}"
                )

        # rechte_seite ist bereits als float typisiert, was eine gute Validierung ist.
        self.gleichung = self.linke_seite - self.rechte_seite

    def extrahiere_koeffizienten(
        self, parameter: list[sp.Symbol]
    ) -> dict[sp.Symbol, float]:
        """
        Extrahiert die Koeffizienten der Parameter aus der Gleichung.

        Stellt sicher, dass die Gleichung linear bezüglich der Parameter ist.

        Args:
            parameter: Liste der Parameter (z.B. [a, b, c])

        Returns:
            Dictionary mit Parameter -> Koeffizient

        Raises:
            ValueError: Wenn die Gleichung nicht linear in den Parametern ist
                        oder ein Koeffizient nicht in eine Zahl umgewandelt werden kann.
        """
        poly = self.gleichung.as_poly(*parameter)

        # Überprüfen, ob die Gleichung linear in den Parametern ist
        if poly is None or any(d > 1 for d in poly.degree_list()):
            raise ValueError(
                f"Gleichung '{self.gleichung} = 0' ist nicht linear in den Parametern {parameter}."
            )

        koeffizienten = {}
        for p in parameter:
            # Extrahiere den Koeffizienten für den Parameter p
            koeff = poly.coeff_monomial(p)
            try:
                # Versuche, den Koeffizienten in eine Gleitkommazahl umzuwandeln
                koeffizienten[p] = float(koeff)
            except (TypeError, ValueError):
                raise ValueError(
                    f"Der Koeffizient '{koeff}' für Parameter '{p}' ist nicht numerisch."
                )

        # Der konstante Term kann hier ignoriert werden, da er bereits durch
        # die Normalisierung der Gleichung (... - rechte_seite = 0) berücksichtigt ist.

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

        # Bekannte Variablennamen ausschließen (typische mathematische Variablen)
        ausgeschlossene_namen = {"x", "y", "z", "t", "u", "v"}
        gefilterte_symbole = []

        for symbol in alle_symbole:
            if str(symbol) not in ausgeschlossene_namen:
                gefilterte_symbole.append(symbol)
            else:
                # Prüfe, ob das Symbol tatsächlich in allen Gleichungen als Variable auftritt
                # Wenn es nur in einigen als Variable vorkommt, könnte es trotzdem ein Parameter sein
                ist_wirklich_variable = True
                for gl in self.gleichungen:
                    # Wenn der Koeffizient dieses Symbols nicht konstant ist, ist es wahrscheinlich ein Parameter
                    try:
                        koeff = gl.gleichung.coeff(symbol)
                        if not koeff.is_number:
                            ist_wirklich_variable = False
                            break
                    except (TypeError, AttributeError):
                        continue

                if not ist_wirklich_variable:
                    gefilterte_symbole.append(symbol)

        return sorted(gefilterte_symbole, key=lambda x: str(x))

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
            LGSKeineLoesungError: Wenn das System keine Lösung hat
            LGSUnendlichVieleLoesungenError: Wenn das System unendlich viele Lösungen hat
            LGSNumerischeInstabilitaetError: Wenn das System numerisch instabil ist
        """
        # Validierung vor dem Lösen
        warnungen = self.validiere_gleichungen()
        if warnungen:
            print("🔍 Validierungswarnungen:")
            for warnung in warnungen:
                print(f"   {warnung}")
            print()

        # Konsistenzprüfung
        ist_konsistent, nachricht = self.pruefe_konsistenz()
        if not ist_konsistent:
            raise LGSInkonsistenzError(f"Inkonsistentes System: {nachricht}")

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

            if lösung_symbols.is_empty:
                raise LGSKeineLoesungError(
                    "Logikfehler: Dieses Gleichungssystem hat keine Lösung. "
                    "Deine Bedingungen widersprechen sich. Überprüfe, ob du "
                    "zum Beispiel einem Punkt zwei verschiedene y-Werte zugewiesen hast."
                )

            # Extrahiere die Lösung
            if hasattr(lösung_symbols, "__iter__") and len(lösung_symbols) > 0:
                lösung_tuple = list(lösung_symbols)[0]

                if len(lösung_tuple) != len(self.parameter):
                    raise LGSUnendlichVieleLoesungenError(
                        "Information fehlt: Dieses Gleichungssystem hat unendlich viele "
                        "Lösungen. Deine Bedingungen sind nicht alle voneinander abhängig. "
                        "Du hast nicht genügend Informationen für eine eindeutige Funktion."
                    )

                # Konvertiere zu Dictionary
                self._lösung = {}
                for param, wert in zip(self.parameter, lösung_tuple, strict=False):
                    if wert.is_number:
                        self._lösung[param] = float(wert)
                    else:
                        self._lösung[param] = wert

            else:
                raise ValueError("Unerwartete Lösungsform von SymPy")

        except (ValueError, TypeError) as e:
            # SymPy-spezifische Fehler
            if "singular" in str(e).lower() or "not invertible" in str(e).lower():
                raise LGSNumerischeInstabilitaetError(
                    "Das Gleichungssystem ist nicht eindeutig lösbar. "
                    "Die Bedingungen sind linear abhängig."
                )
            else:
                raise ValueError(f"SymPy-Lösungsfehler: {str(e)}")
        except LGSKeineLoesungError:
            # Lässt unsere eigenen Fehler durchgehen
            raise
        except LGSUnendlichVieleLoesungenError:
            # Lässt unsere eigenen Fehler durchgehen
            raise
        except Exception as e:
            # Unerwartete Fehler
            raise ValueError(
                f"Unerwarteter Fehler beim Lösen des Gleichungssystems. "
                f"Dies könnte auf ein komplexes mathematisches Problem hindeuten. "
                f"Fehlerdetails: {str(e)}"
            )

        return self._lösung

    def löse_für_funktion(self, funktion: ParametrischeFunktionProtocol):
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

    def zeige_loesungsweg(self):
        """Zeigt den detaillierten Lösungsweg Schritt für Schritt"""
        print("📐 LÖSUNGSWEG")
        print("=" * 50)

        # Schritt 1: Gleichungen darstellen
        print("\n1️⃣  Gegebene Gleichungen:")
        print("-" * 30)
        for i, gl in enumerate(self.gleichungen, 1):
            print(f"   {chr(64 + i)}: {gl.linke_seite} = {gl.rechte_seite}")

        # Schritt 2: Parameter identifizieren
        print(f"\n2️⃣  Gesuchte Parameter: {', '.join(str(p) for p in self.parameter)}")
        print(f"   Anzahl Gleichungen: {self.anzahl_gleichungen}")
        print(f"   Anzahl Unbekannte: {self.anzahl_parameter}")

        # Schritt 3: Matrix erstellen
        print("\n3️⃣  Matrix-Form A·x = b:")
        print("-" * 30)
        A, b = self.erstelle_matrix_und_vektor()

        # Zeige Parameter-Namen
        param_names = [str(p) for p in self.parameter]
        print(f"   Parameter: {'  '.join(param_names)}")
        print("   " + "-" * (len("  ".join(param_names)) + 10))

        # Zeige jede Zeile
        for i in range(A.rows):
            zeile_vals = [f"{A[i, j]:8.3f}" for j in range(A.cols)]
            print(f"   A = | {'  '.join(zeile_vals)} | {b[i, 0]:8.3f}")

        # Schritt 4: Lösbarkeit prüfen
        print("\n4️⃣  Lösbarkeitsanalyse:")
        print("-" * 30)
        if A.rows != A.cols:
            print("   ⚠️  Nicht quadratische Matrix")
            print(f"   {A.rows} × {A.cols} System")
        else:
            try:
                det = A.det()
                print(f"   Determinante: det(A) = {det}")
                if abs(det) < 1e-10:
                    print("   ❌ Determinante ≈ 0 → Keine eindeutige Lösung")
                else:
                    print("   ✅ Determinante ≠ 0 → Eindeutige Lösung existiert")
            except Exception:
                print("   ⚠️  Determinante konnte nicht berechnet werden")

        # Schritt 5: Lösung berechnen (wenn möglich)
        print("\n5️⃣  Lösungsmethode: SymPy linsolve()")
        print("-" * 30)

        try:
            lösung = self.löse()
            print("   ✅ Lösung gefunden:")
            for param, wert in lösung.items():
                print(f"      {param} = {wert:.6f}")

            # Schritt 6: Verifikation
            print("\n6️⃣  Verifikation:")
            print("-" * 30)
            print("   Einsetzen der Lösung in die ursprünglichen Gleichungen:")

            for i, gl in enumerate(self.gleichungen, 1):
                # Substituiere die Lösung in die linke Seite
                linke_seite_mit_loesung = gl.linke_seite
                for param, wert in lösung.items():
                    linke_seite_mit_loesung = linke_seite_mit_loesung.subs(param, wert)

                # Berechne numerischen Wert
                try:
                    wert_links = float(linke_seite_mit_loesung)
                    wert_rechts = gl.rechte_seite
                    differenz = abs(wert_links - wert_rechts)

                    if differenz < 1e-10:
                        status = "✅"
                    else:
                        status = "❌"

                    print(
                        f"   {status} Gleichung {i}: {wert_links:.6f} ≈ {wert_rechts:.6f} (Diff: {differenz:.2e})"
                    )

                except Exception:
                    print(f"   ⚠️  Gleichung {i}: Konnte nicht verifiziert werden")

        except Exception as e:
            print(f"   ❌ Lösung fehlgeschlagen: {e}")

        print("\n" + "=" * 50)

    def validiere_gleichungen(self) -> list[str]:
        """
        Validiert die Gleichungen und gibt Warnungen zurück

        Returns:
            Liste der Warnungen und Fehlermeldungen
        """
        warnungen = []

        # Prüfe 1: Mindestens eine Gleichung
        if not self.gleichungen:
            warnungen.append("⚠️  Keine Gleichungen angegeben")
            return warnungen

        # Prüfe 2: Anzahl Gleichungen vs Parameter
        if self.anzahl_gleichungen < self.anzahl_parameter:
            warnungen.append(
                f"⚠️  Zu wenig Gleichungen: {self.anzahl_gleichungen} Gleichungen für {self.anzahl_parameter} Unbekannte"
            )
        elif self.anzahl_gleichungen > self.anzahl_parameter:
            warnungen.append(
                f"⚠️  Zu viele Gleichungen: {self.anzahl_gleichungen} Gleichungen für {self.anzahl_parameter} Unbekannte (überbestimmt)"
            )

        # Prüfe 3: Duplizierte Bedingungen
        gleichung_texte = [str(gl.linke_seite) for gl in self.gleichungen]
        for i, text1 in enumerate(gleichung_texte):
            for j, text2 in enumerate(gleichung_texte):
                if i < j and text1 == text2:
                    warnungen.append(
                        f"⚠️  Gleichung {i + 1} und {j + 1} haben identische linke Seiten: {text1}"
                    )

        # Prüfe 4: Numerische Stabilität (Konditionszahl)
        try:
            A, _ = self.erstelle_matrix_und_vektor()
            if hasattr(A, "condition_number"):
                cond = A.condition_number()
                if cond > 1000:
                    warnungen.append(
                        f"⚠️  Schlechte Konditionszahl: {cond:.2e} - numerisch instabil"
                    )
        except Exception:
            pass  # Fehler bei Konditionszahlberechnung ignorieren

        return warnungen

    def pruefe_konsistenz(self) -> tuple[bool, str]:
        """
        Prüft die Konsistenz des Gleichungssystems

        Returns:
            (ist_konsistent, nachricht) Tuple
        """
        # Prüfe offensichtliche Widersprüche
        for i, gl1 in enumerate(self.gleichungen):
            for j, gl2 in enumerate(self.gleichungen):
                if i >= j:
                    continue

                # Prüfe ob linke Seiten gleich aber rechte Seiten unterschiedlich
                if str(gl1.linke_seite) == str(gl2.linke_seite):
                    if abs(gl1.rechte_seite - gl2.rechte_seite) > 1e-10:
                        return (
                            False,
                            f"Widerspruch: Gleichung {i + 1} und {j + 1} haben gleiche linke Seiten aber unterschiedliche rechte Seiten",
                        )

        # Prüfe auf triviale Lösungen (alle Parameter = 0)
        if all(gl.rechte_seite == 0 for gl in self.gleichungen):
            return True, "Triviale Lösung möglich (alle Parameter = 0)"

        return True, "System scheint konsistent"

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


# ====================
# Hilfsfunktionen für spezielle Anwendungsfälle
# ====================


def interpolationspolynom(
    punkte: list[tuple[float, float]],
):
    """
    Erzeugt ein Interpolationspolynom durch gegebene Punkte mittels LGS

    Args:
        punkte: Liste von (x, y) Punkten, durch die das Polynom gehen soll

    Returns:
        Parametrische Funktion mit den gefundenen Parametern

    Raises:
        ValueError: Wenn zu wenige Punkte oder ungültige Punkte

    Examples:
        >>> # Parabel durch 3 Punkte
        >>> punkte = [(1, 2), (2, 3), (3, 6)]
        >>> f = interpolationspolynom(punkte)
        >>> print(f.term())  # Erwartet: x^2 - 2x + 3

        >>> # Gerade durch 2 Punkte
        >>> punkte = [(0, 1), (2, 5)]
        >>> f = interpolationspolynom(punkte)
        >>> print(f.term())  # Erwartet: 2x + 1
    """
    if len(punkte) < 2:
        raise ValueError("Mindestens 2 Punkte erforderlich")

    # Bestimme den Grad des Polynoms (n Punkte → n-1 Grad)
    n = len(punkte)
    grad = n - 1

    # Importiere benötigte Klassen
    from .parametrisch import Parameter, ParametrischeFunktion, Variable

    # Erstelle Variable und Parameter
    x = Variable("x")
    parameter = [Parameter(f"a{i}") for i in range(grad + 1)]

    # Erstelle allgemeine Polynom-Funktion
    # f(x) = a0 + a1*x + a2*x² + ... + an*x^n
    koeffizienten = parameter[::-1]  # Umgekehrt, damit a0 Konstante ist

    # Fülle mit Nullen auf, wenn nötig
    while len(koeffizienten) <= grad:
        koeffizienten.insert(0, 0)

    f = ParametrischeFunktion(koeffizienten, [x])

    # Erstelle Gleichungen aus den Punkten
    gleichungen = []
    for _i, (x_wert, y_wert) in enumerate(punkte):
        gl = f(x_wert) == y_wert
        gleichungen.append(gl)

    # Erstelle und löse LGS
    lgs = LGS(*gleichungen)

    print(f"🔍 Interpolation durch {n} Punkte:")
    print(f"   Polynomgrad: {grad}")
    print(f"   Gesuchte Parameter: {', '.join(str(p) for p in parameter)}")
    print()

    # Zeige Lösungsweg für pädagogischen Wert
    lgs.zeige_loesungsweg()

    # Löse das System
    lösung = lgs.löse()

    # Erstelle die konkrete Funktion
    f_konkret = f.mit_wert(**{str(p): v for p, v in lösung.items()})

    print("\n✅ Gefundenes Interpolationspolynom:")
    print(f"   f(x) = {f_konkret.term()}")

    # Verifikation
    print("\n🔍 Verifikation:")
    for x_wert, y_wert in punkte:
        y_berechnet = f_konkret.wert(x_wert)
        differenz = abs(y_berechnet - y_wert)
        status = "✅" if differenz < 1e-10 else "❌"
        print(
            f"   {status} f({x_wert}) = {y_berechnet:.6f} ≈ {y_wert} (Diff: {differenz:.2e})"
        )

    return f_konkret


# ====================
# Plotting und Visualisierung
# ====================


def plotte_loesung(
    funktion: ParametrischeFunktionProtocol,
    loesung: dict,
    x_range: tuple[float, float] = (-10, 10),
    punkte: list[tuple[float, float]] | None = None,
    titel: str | None = None,
):
    """
    Erzeugt eine Visualisierung der gefundenen Funktion mit optionalen Punkten

    Args:
        funktion: Die parametrische Funktion
        loesung: Dictionary mit Parameter-Werten
        x_range: x-Bereich für die Darstellung
        punkte: Optionale Punkte, die markiert werden sollen
        titel: Optionaler Titel für die Grafik

    Returns:
        Plotly-Figure Objekt
    """
    import numpy as np
    import plotly.graph_objects as go

    # Konkrete Funktion erstellen
    f_konkret = funktion.mit_wert(**{str(p): v for p, v in loesung.items()})

    # x-Werte für die Darstellung
    x_vals = np.linspace(x_range[0], x_range[1], 200)
    y_vals = []

    # Funktionswerte berechnen
    for x in x_vals:
        try:
            y = f_konkret.wert(x)
            if not np.isinf(y) and not np.isnan(y):
                y_vals.append(y)
            else:
                y_vals.append(None)
        except (ValueError, ZeroDivisionError, OverflowError):
            y_vals.append(None)

    # Figur erstellen
    fig = go.Figure()

    # Hauptkurve
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines",
            name=f"f(x) = {f_konkret.term()}",
            line=dict(color="blue", width=2),  # noqa: C408
            hovertemplate="<b>x</b>: %{x:.3f}<br><b>f(x)</b>: %{y:.3f}<extra></extra>",
        )
    )

    # Optionale Punkte markieren
    if punkte:
        punkte_x = [p[0] for p in punkte]
        punkte_y = [p[1] for p in punkte]

        fig.add_trace(
            go.Scatter(
                x=punkte_x,
                y=punkte_y,
                mode="markers",
                name="Gegebene Punkte",
                marker=dict(color="red", size=8, symbol="circle"),  # noqa: C408
                hovertemplate="<b>Punkt</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>",
            )
        )

    # Layout konfigurieren
    fig.update_layout(
        title=titel or f"Gefundene Funktion: f(x) = {f_konkret.term()}",
        xaxis_title="x",
        yaxis_title="f(x)",
        xaxis_range=x_range,
        showlegend=True,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(  # noqa: C408
            showgrid=True,
            gridwidth=1,
            gridcolor="lightgray",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
            showline=True,
            linewidth=2,
            linecolor="black",
        ),
        yaxis=dict(  # noqa: C408
            showgrid=True,
            gridwidth=1,
            gridcolor="lightgray",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
            showline=True,
            linewidth=2,
            linecolor="black",
        ),
        width=800,
        height=600,
    )

    return fig


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
    for i, (zeile, wert) in enumerate(zip(matrix, vektor, strict=False)):
        linke_seite = sp.sympify(
            sum(koeff * param for koeff, param in zip(zeile, parameter, strict=False))
        )
        gleichung = LineareGleichung(
            linke_seite=linke_seite,
            rechte_seite=wert,
            beschreibung=f"Matrix-Gleichung {i + 1}",
        )
        gleichungen.append(gleichung)

    return LineareGleichungssystem(gleichungen)
