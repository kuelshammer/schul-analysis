"""
Strukturierte Funktionsklassen für das Schul-Analysis Framework.

Diese Klassen repräsentieren komplexe mathematische Strukturen wie Produkte, Summen,
Quotienten und Kompositionen mit automatisch typisierten Komponenten.

PÄDAGOGISCHER ANSATZ:
- Automatische Typisierung bei Verwendung von Funktion("...")
- Intelligente Zerlegungstiefe (keine Über-Zerlegung)
- Transparente Integration in bestehendes Framework
"""

import sympy as sp

from .funktion import Funktion
from .ganzrationale import GanzrationaleFunktion
from .struktur import analysiere_funktionsstruktur


class StrukturierteFunktion(Funktion):
    """
    Basisklasse für alle strukturierten Funktionen.

    Diese Klasse erweitert die Basis-Funktion um strukturierte Komponenten
    und sorgt für intelligente Typisierung der Komponenten.
    """

    def __init__(self, eingabe, struktur_info=None):
        """
        Initialisiert eine strukturierte Funktion.

        Args:
            eingabe: Der Funktionsterm als String oder SymPy-Ausdruck
            struktur_info: Bereits analysierte Strukturinformationen
        """
        # Speichere Strukturinformationen
        if struktur_info is None:
            self._struktur_info = analysiere_funktionsstruktur(eingabe)
        else:
            self._struktur_info = struktur_info

        # Initialisiere die Basis-Funktion
        super().__init__(eingabe)

        # Erstelle typisierte Komponenten
        self._komponenten = self._erzeuge_typisierte_komponenten()

    def _erzeuge_typisierte_komponenten(self) -> list[Funktion]:
        """
        Erzeugt automatisch typisierte Komponenten basierend auf der Strukturanalyse.

        Returns:
            Liste von typisierten Funktionsobjekten
        """
        komponenten = []

        for komp_info in self._struktur_info["komponenten"]:
            komp_term = komp_info["term"]
            komp_typ = komp_info["typ"]

            # Erstelle typisierte Komponente basierend auf dem Typ
            typisierte_komp = self._erzeuge_typisierte_komponente(komp_term, komp_typ)
            komponenten.append(typisierte_komp)

        return komponenten

    def _erzeuge_typisierte_komponente(self, term: str, typ: str) -> Funktion:
        """
        Erzeugt eine einzelne typisierte Komponente mit intelligenten Stop-Bedingungen.

        Args:
            term: Der Term als String
            typ: Der erkannte Typ

        Returns:
            Typisiertes Funktionsobjekt
        """
        # Importe hier, um zirkuläre Abhängigkeiten zu vermeiden
        from .exponential import ExponentialFunktion
        from .trigonometrisch import TrigonometrischeFunktion

        # Stop-Bedingungen: Nicht weiter zerlegen - Gibt spezifische Typen zurück
        if self._sollte_nicht_weiter_zerlegt_werden(term, typ):
            if typ == "ganzrational":
                # Für ganzrationale Funktionen: direkt spezifische Typen bestimmen
                import sympy as sp

                try:
                    expr = sp.sympify(term, rational=True)
                    grad = expr.as_poly(sp.symbols("x")).degree()

                    from .lineare import LineareFunktion
                    from .quadratisch import QuadratischeFunktion

                    if grad == 1:
                        return LineareFunktion(term)
                    elif grad == 2:
                        return QuadratischeFunktion(term)
                    else:
                        return GanzrationaleFunktion(term)
                except Exception:
                    return GanzrationaleFunktion(term)
            elif typ == "konstante":
                return GanzrationaleFunktion(term)

        # Für komplexe Typen: Erstelle spezifische Instanzen
        elif typ == "exponentiell":
            return ExponentialFunktion(term)
        elif typ == "trigonometrisch":
            return TrigonometrischeFunktion(term)
        elif typ == "logarithmisch":
            # TODO: Logarithmische Funktion implementieren
            return Funktion(term)
        else:
            # Für unbekannte Typen: Standard-Funktion
            return Funktion(term)

    def _sollte_nicht_weiter_zerlegt_werden(self, term: str, typ: str) -> bool:
        """
        Intelligente Stop-Bedingungen für die Zerlegungstiefe.

        Rekursion bricht ab, wenn eine ganzrationale Funktion erkannt wird!
        """
        # Jede ganzrationale Funktion stoppt die Rekursion
        if typ == "ganzrational":
            return True

        # Konstanten auch stoppen
        if typ == "konstante":
            return True

        # Prüfe, ob es sich um einen "einfachen" Ausdruck handelt
        try:
            expr = sp.sympify(term, rational=True)

            # Konstanten prüfen
            if hasattr(expr, "is_constant") and expr.is_constant():
                return True

            # Einfache Polynome (Grad <= 2) nicht weiter zerlegen
            if expr.is_polynomial(sp.symbols("x")):
                grad = sp.degree(expr, sp.symbols("x"))
                if grad <= 2:  # Lineare und quadratische Polynome
                    return True

        except Exception:
            pass

        return False

    @property
    def komponenten(self) -> list[Funktion]:
        """Gibt die typisierten Komponenten zurück."""
        return self._komponenten

    @property
    def struktur(self) -> str:
        """Gibt die Struktur der Funktion zurück."""
        return self._struktur_info["struktur"]


class ProduktFunktion(StrukturierteFunktion):
    """Repräsentiert ein Produkt von Funktionen mit typisierten Faktoren."""

    def __init__(self, eingabe, struktur_info=None):
        super().__init__(eingabe, struktur_info)

        # Spezifische Eigenschaften für Produkte
        self._faktoren = self._komponenten

    @property
    def faktoren(self) -> list[Funktion]:
        """Gibt die typisierten Faktoren des Produkts zurück."""
        return self._faktoren

    @property
    def faktor1(self) -> Funktion:
        """Gibt den ersten Faktor zurück."""
        return self._faktoren[0] if len(self._faktoren) > 0 else None

    @property
    def faktor2(self) -> Funktion:
        """Gibt den zweiten Faktor zurück."""
        return self._faktoren[1] if len(self._faktoren) > 1 else None

    def __str__(self):
        return f"Produkt({', '.join(str(f) for f in self.faktoren)})"


class SummeFunktion(StrukturierteFunktion):
    """Repräsentiert eine Summe von Funktionen mit typisierten Summanden."""

    def __init__(self, eingabe, struktur_info=None):
        super().__init__(eingabe, struktur_info)

        # Spezifische Eigenschaften für Summen
        self._summanden = self._komponenten

    @property
    def summanden(self) -> list[Funktion]:
        """Gibt die typisierten Summanden der Summe zurück."""
        return self._summanden

    @property
    def summand1(self) -> Funktion:
        """Gibt den ersten Summanden zurück."""
        return self._summanden[0] if len(self._summanden) > 0 else None

    @property
    def summand2(self) -> Funktion:
        """Gibt den zweiten Summanden zurück."""
        return self._summanden[1] if len(self._summanden) > 1 else None

    def __str__(self):
        return f"Summe({', '.join(str(s) for s in self.summanden)})"


class QuotientFunktion(StrukturierteFunktion):
    """
    Repräsentiert einen Quotienten von Funktionen mit typisiertem Zähler und Nenner.

    Dies ist die unified Klasse für alle Quotientenfunktionen - von gebrochen-rationalen
    bis hin zu komplexen Quotienten wie exp(x)/sin(x). Sie bietet alle notwendigen
    Methoden für die Arbeit mit Quotienten im Schulunterricht.

    Beispiele:
        - (x^2+1)/(x-1) → Quotient von ganzrationalen Funktionen
        - exp(x)/sin(x) → Quotient von Exponential- und trigonometrischen Funktionen
        - Alle haben polstellen(), definitionsluecken(), etc.
    """

    def __init__(self, eingabe, struktur_info=None):
        super().__init__(eingabe, struktur_info)

        # Spezifische Eigenschaften für Quotienten
        self._zaehler = self._komponenten[0] if len(self._komponenten) > 0 else None
        self._nenner = self._komponenten[1] if len(self._komponenten) > 1 else None

        # 🔥 PÄDAGOGISCHES CACHING FÜR QUOTIENTEN 🔥
        self._cache = {
            "polstellen": None,
            "definitionsluecken": None,
        }

    @property
    def zaehler(self) -> Funktion:
        """Gibt den typisierten Zähler zurück."""
        return self._zaehler

    @property
    def nenner(self) -> Funktion:
        """Gibt den typisierten Nenner zurück."""
        return self._nenner

    def polstellen(self) -> list[float]:
        """
        Berechnet die Polstellen der Funktion (Nenner-Nullstellen).

        Dies ist eine universelle Methode für alle Quotientenfunktionen:
        - Gebrochen-rationale: Polstellen des Nennerpolynoms
        - Andere Quotienten: Nullstellen der Nennerfunktion

        Returns:
            Liste der x-Werte, an denen der Nenner null wird
        """
        if self._cache["polstellen"] is None:
            if self.nenner is None:
                raise ValueError("QuotientFunktion hat keinen gültigen Nenner")

            # Wenn der Nenner bereits eine Funktion ist, rufe nullstellen() auf
            if hasattr(self.nenner, "nullstellen") and callable(
                getattr(self.nenner, "nullstellen")
            ):
                self._cache["polstellen"] = self.nenner.nullstellen()
            else:
                # Wenn der Nenner eine Liste von Nullstellen ist (bei einfacher Struktur)
                try:
                    self._cache["polstellen"] = list(self.nenner) if self.nenner else []
                except (TypeError, ValueError):
                    # Fallback: Leere Liste wenn keine Nullstellen ermittelbar
                    self._cache["polstellen"] = []
        return self._cache["polstellen"]

    def definitionsluecken(self) -> list[float]:
        """
        Gibt die Definitionslücken der Funktion zurück.

        Bei Quotientenfunktionen sind dies genau die Polstellen, da an diesen
        Stellen der Nenner null wird und die Funktion nicht definiert ist.

        Returns:
            Liste der x-Werte, an denen die Funktion nicht definiert ist
        """
        if self._cache["definitionsluecken"] is None:
            self._cache["definitionsluecken"] = self.polstellen()
        return self._cache["definitionsluecken"]

    def __str__(self):
        """String-Repräsentation für Schüler und Lehrer."""
        return f"Quotient({self.zaehler}, {self.nenner})"


class KompositionFunktion(StrukturierteFunktion):
    """Repräsentiert eine Komposition von Funktionen mit typisierter Basis und Exponent."""

    def __init__(self, eingabe, struktur_info=None):
        super().__init__(eingabe, struktur_info)

        # Spezifische Eigenschaften für Kompositionen
        self._basis = self._komponenten[0] if len(self._komponenten) > 0 else None
        self._exponent = self._komponenten[1] if len(self._komponenten) > 1 else None

    @property
    def basis(self) -> Funktion:
        """Gibt die typisierte Basis zurück."""
        return self._basis

    @property
    def exponent(self) -> Funktion:
        """Gibt den typisierten Exponenten zurück."""
        return self._exponent

    def __str__(self):
        return f"Komposition({self.basis}, {self.exponent})"
