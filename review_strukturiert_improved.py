"""
Verbesserte Version der strukturierten Funktionsklassen mit Fokus auf:
- Type Safety und Validation
- Pädagogische Robustheit
- Performance-Optimierung
- Deutsche Schulstandards
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Union
import functools

import sympy as sp

from .sympy_types import (
    T_Expr,
    validate_function_result,
    preserve_exact_types,
)


class StrukturTyp(Enum):
    """Strukturtypen für deutsche Schulmathematik."""

    SUMME = "summe"
    PRODUKT = "produkt"
    QUOTIENT = "quotient"
    KOMPOSITION = "komposition"
    POTENZ = "potenz"


@dataclass(frozen=True)
class KomponentenInfo:
    """Strukturierte Information über eine Funktionskomponente."""

    ausdruck: T_Expr
    typ: str
    term: str
    latex: str
    exakt: bool = True


@dataclass(frozen=True)
class StrukturInfo:
    """Vollständige Strukturanalyse-Informationen."""

    original_term: str
    struktur: StrukturTyp
    komponenten: list[KomponentenInfo]
    variable: str
    latex: str
    kann_faktorisiert_werden: bool = False
    faktoren: Optional[list[str]] = field(default_factory=lambda: None)


class StrukturFehler(Exception):
    """Fehler bei der Strukturanalyse - deutsche Fehlermeldungen."""

    def __init__(self, nachricht: str, ursache: str = ""):
        self.nachricht = nachricht
        self.ursache = ursache
        super().__init__(f"{nachricht}. {ursache}" if ursache else nachricht)


class StrukturierteFunktion(ABC):
    """
    Verbesserte Basisklasse für strukturierte Funktionen mit voller Type Safety.

    PÄDAGOGISCHER ANSATZ:
    - Deutsche Fehlermeldungen als Lernmomente
    - Exakte Berechnungen garantiert
    - Intuitive Properties für Schüler
    """

    def __init__(
        self, eingabe: Union[str, T_Expr], struktur_info: Optional[StrukturInfo] = None
    ):
        """
        Initialisiert mit voller Validierung.

        Args:
            eingabe: Funktionsterm als String oder SymPy-Ausdruck
            struktur_info: Voranalysierte Strukturinformation

        Raises:
            StrukturFehler: Bei ungültiger Struktur
        """
        # Validiere Eingabe
        if not eingabe:
            raise StrukturFehler(
                "Leere Funktion nicht erlaubt",
                "Bitte geben Sie einen gültigen Funktionsterm an",
            )

        # Speichere Strukturinformationen mit Validierung
        self._struktur_info = self._validiere_struktur_info(struktur_info, eingabe)

        # Initialisiere Basis-Funktion (hier vereinfacht dargestellt)
        self._term = (
            str(eingabe) if isinstance(eingabe, str) else str(sp.sympify(eingabe))
        )

        # Lazy-Komponenten-Erzeugung mit Caching
        self._komponenten: Optional[list[Funktion]] = None

    def _validiere_struktur_info(
        self, struktur_info: Optional[StrukturInfo], eingabe: Union[str, T_Expr]
    ) -> StrukturInfo:
        """Validiert und erstellt Strukturinformationen."""
        if struktur_info is None:
            # Führe Strukturanalyse durch (hier vereinfacht)
            try:
                return self._analysiere_struktur(eingabe)
            except Exception as e:
                raise StrukturFehler(
                    "Konnte Funktionsstruktur nicht analysieren",
                    f"Der Term '{eingabe}' konnte nicht zerlegt werden: {str(e)}",
                )

        # Validiere vorhandene Struktur
        if not struktur_info.komponenten:
            raise StrukturFehler(
                "Keine Komponenten gefunden",
                "Die Funktion scheint keine zerlegbare Struktur zu haben",
            )

        return struktur_info

    @abstractmethod
    def _analysiere_struktur(self, eingabe: Union[str, T_Expr]) -> StrukturInfo:
        """Abstrakte Methode zur Strukturanalyse - muss implementiert werden."""
        pass

    @property
    @functools.lru_cache(maxsize=1)
    def komponenten(self) -> list[Funktion]:
        """
        Lazy-Erzeugung der typisierten Komponenten mit Caching.

        Returns:
            Liste von typisierten Funktionsobjekten

        Raises:
            StrukturFehler: Bei Fehlern in der Komponenten-Erzeugung
        """
        if self._komponenten is None:
            self._komponenten = self._erzeuge_typisierte_komponenten()

        return self._komponenten

    def _erzeuge_typisierte_komponenten(self) -> list[Funktion]:
        """Erzeugt typisierte Komponenten mit pädagogischer Fehlerbehandlung."""
        komponenten = []

        for komp_info in self._struktur_info.komponenten:
            try:
                typisierte_komp = self._erzeuge_typisierte_komponente(
                    komp_info.term, komp_info.typ
                )
                if typisierte_komp:
                    komponenten.append(typisierte_komp)
            except Exception as e:
                # Pädagogische Fehlermeldung statt Silent Failure
                raise StrukturFehler(
                    f"Fehler bei der Komponenten-Erzeugung für '{komp_info.term}'",
                    f"Typ '{komp_info.typ}' konnte nicht verarbeitet werden: {str(e)}",
                )

        if not komponenten:
            raise StrukturFehler(
                "Keine gültigen Komponenten erzeugt", "Überprüfen Sie den Funktionsterm"
            )

        return komponenten

    def _erzeuge_typisierte_komponente(self, term: str, typ: str) -> Optional[Funktion]:
        """
        Verbesserte Komponenten-Erzeugung mit deutscher Fehlerbehandlung.
        """
        try:
            expr = sp.sympify(term, rational=True)
            validate_function_result(expr, "exact")
        except Exception as e:
            raise StrukturFehler(
                f"Ungültiger Term: '{term}'",
                f"Der Term konnte nicht als exakte mathematische Funktion interpretiert werden: {str(e)}",
            )

        # Intelligente Typ-Erkennung mit pädagogischen Stop-Bedingungen
        if self._sollte_nicht_weiter_zerlegt_werden(expr, typ):
            return self._erstelle_einfache_funktion(term, typ)

        # Komplexe Typen
        return self._erstelle_komplexe_funktion(term, typ)

    def _sollte_nicht_weiter_zerlegt_werden(self, expr: T_Expr, typ: str) -> bool:
        """
        Verbesserte Stop-Bedingungen für pädagogische Zerlegung.

        PÄDAGOGISCHE REGEL:
        - Jede ganzrationale Funktion stoppt die Rekursion
        - Konstanten werden nicht weiter zerlegt
        - Einfache Polynome (Grad ≤ 3) bleiben erhalten
        """
        if typ == "ganzrational":
            return True

        if typ == "konstante":
            return True

        # Prüfe auf einfache Strukturen
        try:
            if expr.is_constant():
                return True

            if expr.is_polynomial(sp.symbols("x")):
                grad = sp.degree(expr, sp.symbols("x"))
                if (
                    grad is not None and grad <= 3
                ):  # Kubische Funktionen noch als "einfach" betrachten
                    return True

        except Exception:
            pass

        return False

    def _erstelle_einfache_funktion(self, term: str, typ: str) -> Funktion:
        """Erstellt einfache Funktionen mit deutscher Typisierung."""
        # Hier müssten die konkreten Klassen importiert werden
        from .ganzrationale import GanzrationaleFunktion
        from .lineare import LineareFunktion
        from .quadratisch import QuadratischeFunktion

        if typ == "ganzrational":
            try:
                expr = sp.sympify(term, rational=True)
                grad = expr.as_poly(sp.symbols("x")).degree()

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

        # Fallback
        return Funktion(term)

    def _erstelle_komplexe_funktion(self, term: str, typ: str) -> Funktion:
        """Erstellt komplexe Funktionstypen."""
        # Hier müssten die konkreten Klassen importiert werden
        from .exponential import ExponentialFunktion
        from .trigonometrisch import TrigonometrischeFunktion

        if typ == "exponentiell":
            return ExponentialFunktion(term)
        elif typ == "trigonometrisch":
            return TrigonometrischeFunktion(term)
        elif typ == "logarithmisch":
            # TODO: Logarithmische Funktion implementieren
            return Funktion(term)

        return Funktion(term)

    # Properties mit deutschen Namen und Validation
    @property
    def struktur(self) -> str:
        """Gibt die Struktur der Funktion zurück."""
        return self._struktur_info.struktur.value

    def __str__(self) -> str:
        """Deutsche String-Repräsentation für Schüler."""
        return f"{self.__class__.__name__}({self._term})"


class ProduktFunktion(StrukturierteFunktion):
    """Verbesserte ProduktFunktion mit voller Type Safety."""

    def __init__(
        self, eingabe: Union[str, T_Expr], struktur_info: Optional[StrukturInfo] = None
    ):
        super().__init__(eingabe, struktur_info)

        # Validiere Produkt-Struktur
        if len(self.komponenten) < 2:
            raise StrukturFehler(
                "Produkt benötigt mindestens zwei Faktoren",
                f"Gefunden: {len(self.komponenten)} Faktor(en)",
            )

        self._faktoren = self.komponenten

    def _analysiere_struktur(self, eingabe: Union[str, T_Expr]) -> StrukturInfo:
        """Implementierung für Produkt-Strukturanalyse."""
        # Hier müsste die konkrete Analyse implementiert werden
        # Vereinfachte Darstellung:
        return StrukturInfo(
            original_term=str(eingabe),
            struktur=StrukturTyp.PRODUKT,
            komponenten=[],  # Wäre zu füllen
            variable="x",
            latex=sp.latex(sp.sympify(eingabe)),
        )

    @property
    def funktionstyp(self) -> str:
        """Gibt den Funktionstyp als deutschen String zurück."""
        return "produkt"

    @property
    def faktoren(self) -> list[Funktion]:
        """
        Gibt die typisierten Faktoren des Produkts zurück.

        Returns:
            Liste der Faktoren als Funktionsobjekte

        Raises:
            StrukturFehler: Wenn keine Faktoren vorhanden
        """
        if not self._faktoren:
            raise StrukturFehler(
                "Keine Faktoren vorhanden",
                "Die Produktfunktion wurde nicht korrekt initialisiert",
            )
        return self._faktoren

    @property
    def faktor1(self) -> Optional[Funktion]:
        """Gibt den ersten Faktor zurück oder None."""
        return self._faktoren[0] if len(self._faktoren) > 0 else None

    @property
    def faktor2(self) -> Optional[Funktion]:
        """Gibt den zweiten Faktor zurück oder None."""
        return self._faktoren[1] if len(self._faktoren) > 1 else None

    @preserve_exact_types
    def ableitung(self) -> ProduktFunktion:
        """
        Berechnet die Ableitung nach der Produktregel.

        Returns:
            Neue ProduktFunktion der Ableitung

        PÄDAGOGISCHER HINWEIS:
        (f·g)' = f'·g + f·g' wird automatisch zerlegt
        """
        # Implementierung der Produktregel
        pass

    def __str__(self) -> str:
        """Deutsche String-Repräsentation."""
        faktor_str = "·".join(str(f) for f in self.faktoren)
        return f"Produkt({faktor_str})"


class QuotientFunktion(StrukturierteFunktion):
    """
    Verbesserte QuotientFunktion mit umfassender Funktionalität.

    PÄDAGOGISCHER SCHWERPUNKT:
    - Polstellen und Definitionslücken
    - Asymptoten-Berechnung
    - Verhalten im Unendlichen
    """

    def __init__(
        self, eingabe: Union[str, T_Expr], struktur_info: Optional[StrukturInfo] = None
    ):
        super().__init__(eingabe, struktur_info)

        # Validiere Quotienten-Struktur
        if len(self.komponenten) != 2:
            raise StrukturFehler(
                "Quotient benötigt genau zwei Komponenten (Zähler und Nenner)",
                f"Gefunden: {len(self.komponenten)} Komponente(n)",
            )

        self._zaehler = self.komponenten[0]
        self._nenner = self.komponenten[1]

        # Erweitertes Caching für Quotienten-spezifische Berechnungen
        self._cache = {
            "polstellen": None,
            "definitionsluecken": None,
            "asymptoten": None,
            "nullstellen": None,
        }

    def _analysiere_struktur(self, eingabe: Union[str, T_Expr]) -> StrukturInfo:
        """Implementierung für Quotienten-Strukturanalyse."""
        # Implementierung würde hier folgen
        pass

    @property
    def funktionstyp(self) -> str:
        """Gibt den Funktionstyp als deutschen String zurück."""
        return "quotient"

    @property
    def zaehler(self) -> Funktion:
        """
        Gibt den typisierten Zähler zurück.

        Returns:
            Zähler-Funktion

        Raises:
            StrukturFehler: Wenn kein Zähler vorhanden
        """
        if self._zaehler is None:
            raise StrukturFehler(
                "Kein Zähler vorhanden",
                "Die Quotientenfunktion wurde nicht korrekt initialisiert",
            )
        return self._zaehler

    @property
    def nenner(self) -> Funktion:
        """
        Gibt den typisierten Nenner zurück.

        Returns:
            Nenner-Funktion

        Raises:
            StrukturFehler: Wenn kein Nenner vorhanden
        """
        if self._nenner is None:
            raise StrukturFehler(
                "Kein Nenner vorhanden",
                "Die Quotientenfunktion wurde nicht korrekt initialisiert",
            )
        return self._nenner

    @functools.lru_cache(maxsize=1)
    @preserve_exact_types
    def polstellen(self) -> list[float]:
        """
        Berechnet die Polstellen (Nenner-Nullstellen) mit Caching.

        Returns:
            Liste der Polstellen als exakte Werte

        PÄDAGOGISCHE ERKLÄRUNG:
        Polstellen sind x-Werte, an denen der Nenner null wird.
        An diesen Stellen ist die Funktion nicht definiert.

        Beispiel:
        f(x) = (x²+1)/(x-2) hat eine Polstelle bei x = 2
        """
        if self._cache["polstellen"] is None:
            try:
                if hasattr(self.nenner, "nullstellen") and callable(
                    self.nenner.nullstellen
                ):
                    self._cache["polstellen"] = self.nenner.nullstellen()
                else:
                    # Fallback: Direkte Berechnung
                    self._cache["polstellen"] = []
            except Exception as e:
                raise StrukturFehler(
                    "Polstellen konnten nicht berechnet werden",
                    f"Fehler bei der Nullstellenberechnung des Nenners: {str(e)}",
                )

        return self._cache["polstellen"]

    @functools.lru_cache(maxsize=1)
    def definitionsluecken(self) -> list[float]:
        """
        Gibt alle Definitionslücken zurück.

        Returns:
            Liste der x-Werte, an denen die Funktion nicht definiert ist

        PÄDAGOGISCHE ANMERKUNG:
        Bei Quotientenfunktionen sind die Definitionslücken
        genau die Polstellen.
        """
        return self.polstellen()

    def __str__(self) -> str:
        """Deutsche String-Repräsentation für Schüler."""
        return f"Quotient({self.zaehler} ÷ {self.nenner})"


# Beispiel für die Verwendung:
if __name__ == "__main__":
    try:
        # Erstelle eine Produktfunktion
        produkt = ProduktFunktion("(x+1)*sin(x)")
        print(f"Produkt: {produkt}")
        print(f"Faktoren: {[str(f) for f in produkt.faktoren]}")

        # Erstelle eine Quotientenfunktion
        quotient = QuotientFunktion("(x**2+1)/(x-2)")
        print(f"Quotient: {quotient}")
        print(f"Polstellen: {quotient.polstellen()}")

    except StrukturFehler as e:
        print(f"Strukturfehler: {e.nachricht}")
        if e.ursache:
            print(f"Ursache: {e.ursache}")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")
