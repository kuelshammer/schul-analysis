"""
Abstrakte Basisklasse für alle Funktionen im Schul-Analysis Framework.

Diese Klasse definiert das Interface, das alle Funktionsklassen implementieren müssen.
Sie stellt sicher, dass alle Funktionen konsistente Methoden und Eigenschaften haben.

Author: Claude AI Assistant
Created: 2025-01-10
"""

from abc import ABC, abstractmethod
from typing import Any, Union
import sympy as sp

from .errors import UngueltigeFunktionError
from .sympy_types import ExactNullstellenListe, SchnittpunkteListe, preserve_exact_types


class BasisFunktion(ABC):
    """
    Abstrakte Basisklasse für alle mathematischen Funktionen im Schul-Analysis Framework.

    Diese Klasse definiert das minimale Interface, das alle Funktionen implementieren müssen.
    Sie sorgt für konsistente API-Verfügbarkeit über alle Funktionstypen hinweg.

    Abstrakte Methoden müssen von konkreten Unterklassen implementiert werden.
    """

    def __init__(self):
        """Initialisiere die Basiskomponenten für alle Funktionen."""
        self._cache = {}  # Zentrales Caching für Performance
        self._initialisiert = False

    # === ABSTRAKTE METHODEN (müssen implementiert werden) ===

    @abstractmethod
    def term(self) -> str:
        """
        Gibt den Funktionsterm als String zurück.

        Returns:
            String-Repräsentation des Funktionsterms
        """
        pass

    @abstractmethod
    def term_latex(self) -> str:
        """
        Gibt den Funktionsterm als LaTeX-String zurück.

        Returns:
            LaTeX-Repräsentation des Funktionsterms
        """
        pass

    @abstractmethod
    def wert(self, x_wert: Union[float, sp.Expr]) -> Union[float, sp.Expr]:
        """
        Berechnet den Funktionswert an einer Stelle x.

        Args:
            x_wert: Einsetzwert für die Variable

        Returns:
            Funktionswert f(x)
        """
        pass

    @abstractmethod
    def ableitung(self, ordnung: int = 1) -> "BasisFunktion":
        """
        Bildet die Ableitung der Funktion.

        Args:
            ordnung: Ordnung der Ableitung (Standard: 1)

        Returns:
            Neue Funktion, die die Ableitung darstellt
        """
        pass

    @abstractmethod
    def nullstellen(
        self, real: bool = True, runden: int = None
    ) -> ExactNullstellenListe:
        """
        Berechnet die Nullstellen der Funktion.

        Args:
            real: Nur reelle Nullstellen zurückgeben (Standard: True)
            runden: Anzahl Dezimalstellen zum Runden (optional)

        Returns:
            Liste der Nullstellen
        """
        pass

    @abstractmethod
    def extrema(
        self, real: bool = True, runden: int = None
    ) -> list[tuple[Any, Any, str]]:
        """
        Berechnet die Extremstellen der Funktion.

        Args:
            real: Nur reelle Extremstellen (Standard: True)
            runden: Anzahl Dezimalstellen zum Runden (optional)

        Returns:
            Liste der Extremstellen als (x, y, typ) Tupel
        """
        pass

    @abstractmethod
    def wendepunkte(
        self, real: bool = True, runden: int = None
    ) -> list[tuple[Any, Any, str]]:
        """
        Berechnet die Wendepunkte der Funktion.

        Args:
            real: Nur reelle Wendepunkte (Standard: True)
            runden: Anzahl Dezimalstellen zum Runden (optional)

        Returns:
            Liste der Wendepunkte als (x, y, typ) Tupel
        """
        pass

    # === OPTIONALE METHODEN MIT STANDARDIMPLEMENTIERUNGEN ===

    def setze_parameter(self, **parameter) -> "BasisFunktion":
        """
        Setze Parameter für die Funktion.

        Diese Methode kann von Unterklassen überschrieben werden,
        um parametrisierte Funktionen zu unterstützen.

        Args:
            **parameter: Parameter-Wert Paare

        Returns:
            Neue Funktion mit gesetzten Parametern

        Raises:
            UngueltigeFunktionError: Wenn die Funktion keine Parameter unterstützt
        """
        raise UngueltigeFunktionError(
            "Diese Funktion unterstützt keine Parameter. "
            "Verwende parametrisierbare Funktionstypen für Parameter-Simulation."
        )

    def graph(self, **kwargs) -> Any:
        """
        Zeichnet die Funktion.

        Args:
            **kwargs: Zusätzliche Parameter für die Visualisierung

        Returns:
            Plotly-Graph oder andere Visualisierung

        Raises:
            UngueltigeFunktionError: Wenn Visualisierung nicht unterstützt wird
        """
        raise UngueltigeFunktionError(
            "Diese Funktion unterstützt keine Visualisierung. "
            "Installiere die optionalen Abhängigkeiten für Plotly-Unterstützung."
        )

    # === MAGIC METHODS ===

    @abstractmethod
    def __str__(self) -> str:
        """
        String-Repräsentation der Funktion.

        Returns:
            Lesbare Darstellung der Funktion
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Entwickler-Repräsentation der Funktion.

        Returns:
        Technische Darstellung der Funktion
        """
        pass

    def __call__(self, x_wert: Union[float, sp.Expr]) -> Union[float, sp.Expr]:
        """
        Erlaubt die Syntax f(x) für Funktionsaufrufe.

        Args:
            x_wert: Einsetzwert für die Variable

        Returns:
            Funktionswert f(x)
        """
        return self.wert(x_wert)

    # === HILFSMETHODEN ===

    def _cache_schluessel(self, methode: str, *args, **kwargs) -> str:
        """
        Erzeugt einen Cache-Schlüssel für Methoden-Ergebnisse.

        Args:
            methode: Name der Methode
            *args: Positionsargumente
            **kwargs: Schlüsselwortargumente

        Returns:
            Eindeutiger Cache-Schlüssel
        """
        import hashlib

        # Erstelle String aus allen Argumenten
        key_str = f"{methode}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def _aus_cache(self, schluessel: str) -> Any:
        """
        Holt ein Ergebnis aus dem Cache.

        Args:
            schluessel: Cache-Schlüssel

        Returns:
            Gecachtes Ergebnis oder None
        """
        return self._cache.get(sluessel)

    def _im_cache_speichern(self, schluessel: str, ergebnis: Any) -> None:
        """
        Speichert ein Ergebnis im Cache.

        Args:
            schluessel: Cache-Schlüssel
            ergebnis: Zu speicherndes Ergebnis
        """
        self._cache[sluessel] = ergebnis

    def _cache_leeren(self) -> None:
        """Leert den gesamten Cache."""
        self._cache.clear()

    # === TYPE-SAFETY UND VALIDIERUNG ===

    def _validiere_zahl(self, wert: Any, name: str) -> None:
        """
        Validiert, dass ein Wert eine Zahl ist.

        Args:
            wert: Zu validierender Wert
            name: Name des Parameters für Fehlermeldungen

        Raises:
            TypeError: Wenn der Wert keine Zahl ist
        """
        if not isinstance(wert, (int, float, sp.Number)):
            raise TypeError(f"{name} muss eine Zahl sein, nicht {type(wert).__name__}")

    def _validiere_ordnung(self, ordnung: int) -> None:
        """
        Validiert die Ableitungsordnung.

        Args:
            ordnung: Zu validierende Ordnung

        Raises:
            ValueError: Wenn die Ordnung ungültig ist
        """
        if not isinstance(ordnung, int) or ordnung < 1:
            raise ValueError("Die Ableitungsordnung muss eine positive ganze Zahl sein")

    # === DEUTSCHE FEHLERMELDUNGEN ===

    def _fehler_keine_nullstellen(self) -> str:
        """Standard-Fehlermeldung für Funktionen ohne Nullstellen."""
        return "Diese Funktion hat keine reellen Nullstellen."

    def _fehler_keine_extrema(self) -> str:
        """Standard-Fehlermeldung für Funktionen ohne Extremstellen."""
        return "Diese Funktion hat keine Extremstellen."

    def _fehler_keine_wendepunkte(self) -> str:
        """Standard-Fehlermeldung für Funktionen ohne Wendepunkte."""
        return "Diese Funktion hat keine Wendepunkte."

    # === PÄDAGOGISCHE FEATURES ===

    def beschreibung(self) -> str:
        """
        Gibt eine pädagogische Beschreibung der Funktion zurück.

        Kann von Unterklassen überschrieben werden für spezifische Erklärungen.

        Returns:
            Beschreibung des Funktionstyps
        """
        return "Eine mathematische Funktion"


# Typ-Definition für alle Funktionsklassen
Funktionstyp = Union[
    "BasisFunktion",
    # Wird später durch konkrete Klassen erweitert
]
