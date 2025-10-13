"""
FunktionsDebugger - Schritt-für-Schritt Berechnungsanzeige für mathematische Operationen.

Dieses Modul implementiert einen umfassenden Debugger für mathematische Berechnungen,
der Schritte im Detail anzeigt und für pädagogische Zwecke optimiert ist.
"""

import time
from typing import Any, Dict, List, Optional, Union, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

import sympy as sp
from sympy import (
    sympify,
    latex,
    pretty,
    simplify,
    expand,
    factor,
    solve,
    diff,
    integrate,
)

from .config import config
from .sympy_types import T_Expr, is_exact_sympy_expr


class BerechnungsSchrittTyp(Enum):
    """Typen von Berechnungsschritten für Klassifizierung."""

    INITIALISIERUNG = "initialisierung"
    TRANSFORMATION = "transformation"
    VEREINFACHUNG = "vereinfachung"
    ABLEITUNG = "ableitung"
    INTEGRATION = "integration"
    NULLSTELLENSUCHE = "nullstellensuche"
    EXTREMWERTSUCHE = "extremwertsuche"
    WENDEPUNKTSUCHE = "wendepunktsuche"
    AUSWERTUNG = "auswertung"
    VALIDIERUNG = "validierung"
    ERGEBNIS = "ergebnis"
    HINWEIS = "hinweis"
    FEHLER = "fehler"


class DetailGrad(Enum):
    """Detailgrade für die Debug-Ausgabe."""

    MINIMAL = "minimal"  # Nur wesentliche Schritte
    NORMAL = "normal"  # Standard-Detailgrad
    AUSFÜHRLICH = "ausführlich"  # Alle Zwischenschritte
    PÄDAGOGISCH = "pädagogisch"  # Mit Erklärungen und Lernhinweisen


@dataclass
class BerechnungsSchritt:
    """Ein einzelner Schritt in der Berechnungskette."""

    typ: BerechnungsSchrittTyp
    beschreibung: str
    formel_vorher: Optional[sp.Expr] = None
    formel_nachher: Optional[sp.Expr] = None
    ergebnis: Optional[Any] = None
    erläuterung: Optional[str] = None
    lernhinweis: Optional[str] = None
    zeitstempel: float = field(default_factory=time.time)
    schritt_nummer: int = 0

    def __post_init__(self):
        """Formatiere die Formeln für die Anzeige."""
        if self.formel_vorher is not None:
            self._latex_vorher = latex(self.formel_vorher)
            self._pretty_vorher = pretty(self.formel_vorher)
        else:
            self._latex_vorher = ""
            self._pretty_vorher = ""

        if self.formel_nachher is not None:
            self._latex_nachher = latex(self.formel_nachher)
            self._pretty_nachher = pretty(self.formel_nachher)
        else:
            self._latex_nachher = ""
            self._pretty_nachher = ""

    @property
    def latex_vorher(self) -> str:
        """LaTeX-Darstellung der Formel vor dem Schritt."""
        return self._latex_vorher

    @property
    def latex_nachher(self) -> str:
        """LaTeX-Darstellung der Formel nach dem Schritt."""
        return self._latex_nachher

    @property
    def pretty_vorher(self) -> str:
        """Pretty-Print-Darstellung der Formel vor dem Schritt."""
        return self._pretty_vorher

    @property
    def pretty_nachher(self) -> str:
        """Pretty-Print-Darstellung der Formel nach dem Schritt."""
        return self._pretty_nachher

    def to_dict(self) -> Dict[str, Any]:
        """Konvertiere den Schritt in ein Dictionary für Serialisierung."""
        return {
            "typ": self.typ.value,
            "beschreibung": self.beschreibung,
            "formel_vorher": str(self.formel_vorher) if self.formel_vorher else None,
            "formel_nachher": str(self.formel_nachher) if self.formel_nachher else None,
            "ergebnis": str(self.ergebnis) if self.ergebnis is not None else None,
            "erläuterung": self.erläuterung,
            "lernhinweis": self.lernhinweis,
            "latex_vorher": self.latex_vorher,
            "latex_nachher": self.latex_nachher,
            "zeitstempel": self.zeitstempel,
            "schritt_nummer": self.schritt_nummer,
        }


@dataclass
class DebugSession:
    """Eine komplette Debug-Sitzung mit allen Schritten."""

    titel: str
    start_funktion: sp.Expr
    schritte: List[BerechnungsSchritt] = field(default_factory=list)
    startzeit: float = field(default_factory=time.time)
    endzeit: Optional[float] = None
    detailgrad: DetailGrad = DetailGrad.NORMAL

    def add_schritt(self, schritt: BerechnungsSchritt):
        """Füge einen Schritt zur Session hinzu."""
        schritt.schritt_nummer = len(self.schritte) + 1
        self.schritte.append(schritt)

    def get_schritte_by_typ(
        self, typ: BerechnungsSchrittTyp
    ) -> List[BerechnungsSchritt]:
        """Gib alle Schritte eines bestimmten Typs zurück."""
        return [s for s in self.schritte if s.typ == typ]

    def get_letzte_ergebnis(self) -> Any:
        """Gib das Ergebnis des letzten Schritts zurück."""
        if self.schritte:
            return self.schritte[-1].ergebnis
        return None

    def berechnungsdauer(self) -> float:
        """Berechne die Dauer der Berechnung."""
        endzeit = self.endzeit or time.time()
        return endzeit - self.startzeit

    def to_dict(self) -> Dict[str, Any]:
        """Konvertiere die Session in ein Dictionary."""
        return {
            "titel": self.titel,
            "start_funktion": str(self.start_funktion),
            "schritte": [s.to_dict() for s in self.schritte],
            "startzeit": self.startzeit,
            "endzeit": self.endzeit,
            "dauer": self.berechnungsdauer(),
            "detailgrad": self.detailgrad.value,
            "anzahl_schritte": len(self.schritte),
        }


class BerechnungsStrategie(ABC):
    """Abstrakte Basisklasse für Berechnungsstrategien."""

    @abstractmethod
    def kann_anwenden(self, funktion: sp.Expr, kontext: Dict[str, Any]) -> bool:
        """Prüfe, ob diese Strategie auf die Funktion angewendet werden kann."""
        pass

    @abstractmethod
    def wende_an(
        self, funktion: sp.Expr, session: DebugSession, kontext: Dict[str, Any]
    ) -> sp.Expr:
        """Wende die Strategie an und dokumentiere die Schritte."""
        pass


class VereinfachungsStrategie(BerechnungsStrategie):
    """Strategie zur schrittweisen Vereinfachung von Ausdrücken."""

    def kann_anwenden(self, funktion: sp.Expr, kontext: Dict[str, Any]) -> bool:
        """Kann immer auf Vereinfachungsoperationen angewendet werden."""
        return True  # Vereinfachung ist immer möglich

    def wende_an(
        self, funktion: sp.Expr, session: DebugSession, kontext: Dict[str, Any]
    ) -> sp.Expr:
        """Wende Vereinfachungsstrategien an."""
        aktueller_ausdruck = funktion

        # Schritt 1: Ausmultiplizieren
        if session.detailgrad in [DetailGrad.AUSFÜHRLICH, DetailGrad.PÄDAGOGISCH]:
            expandiert = expand(aktueller_ausdruck)
            if expandiert != aktueller_ausdruck:
                session.add_schritt(
                    BerechnungsSchritt(
                        typ=BerechnungsSchrittTyp.TRANSFORMATION,
                        beschreibung="Ausmultiplizieren der Terme",
                        formel_vorher=aktueller_ausdruck,
                        formel_nachher=expandiert,
                        erläuterung="Alle Klammern werden ausmultipliziert",
                        lernhinweis="Achte auf die Vorzeichenregeln beim Ausmultiplizieren!",
                    )
                )
                aktueller_ausdruck = expandiert

        # Schritt 2: Zusammenfassen gleicher Terme
        vereinfacht = simplify(aktueller_ausdruck)
        if vereinfacht != aktueller_ausdruck:
            session.add_schritt(
                BerechnungsSchritt(
                    typ=BerechnungsSchrittTyp.VEREINFACHUNG,
                    beschreibung="Zusammenfassen gleicher Terme",
                    formel_vorher=aktueller_ausdruck,
                    formel_nachher=vereinfacht,
                    ergebnis=vereinfacht,
                    erläuterung="Gleichartige Terme werden zusammengefasst",
                    lernhinweis="Zähle die Exponenten und kombiniere gleiche Variablen!",
                )
            )
            aktueller_ausdruck = vereinfacht

        # Schritt 3: Faktorisieren (wenn sinnvoll)
        if session.detailgrad == DetailGrad.PÄDAGOGISCH:
            faktorisiert = factor(aktueller_ausdruck)
            if faktorisiert != aktueller_ausdruck and len(str(faktorisiert)) <= len(
                str(aktueller_ausdruck)
            ):
                session.add_schritt(
                    BerechnungsSchritt(
                        typ=BerechnungsSchrittTyp.TRANSFORMATION,
                        beschreibung="Faktorisieren des Ausdrucks",
                        formel_vorher=aktueller_ausdruck,
                        formel_nachher=faktorisiert,
                        ergebnis=faktorisiert,
                        erläuterung="Der Ausdruck wird in Faktoren zerlegt",
                        lernhinweis="Suche gemeinsame Faktoren in allen Termen!",
                    )
                )
                aktueller_ausdruck = faktorisiert

        return aktueller_ausdruck


class AbleitungsStrategie(BerechnungsStrategie):
    """Strategie zur schrittweisen Ableitung."""

    def kann_anwenden(self, funktion: sp.Expr, kontext: Dict[str, Any]) -> bool:
        """Kann auf differenzierbare Funktionen angewendet werden."""
        return kontext.get("operation") == "ableitung"

    def wende_an(
        self, funktion: sp.Expr, session: DebugSession, kontext: Dict[str, Any]
    ) -> sp.Expr:
        """Führe schrittweise Ableitung durch."""
        ordnung = kontext.get("ordnung", 1)
        variable = kontext.get("variable", sp.Symbol("x"))

        # Initialisierung
        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.INITIALISIERUNG,
                beschreibung=f"Beginne {ordnung}. Ableitung von f(x) = {funktion}",
                formel_vorher=funktion,
                erläuterung=f"Die {ordnung}. Ableitung wird mit den Ableitungsregeln berechnet",
            )
        )

        aktueller_ausdruck = funktion

        for i in range(1, ordnung + 1):
            # Schritt-für-Schritt Ableitung
            abgeleitet = diff(aktueller_ausdruck, variable)

            session.add_schritt(
                BerechnungsSchritt(
                    typ=BerechnungsSchrittTyp.ABLEITUNG,
                    beschreibung=f"{i}. Ableitung bilden",
                    formel_vorher=aktueller_ausdruck,
                    formel_nachher=abgeleitet,
                    ergebnis=abgeleitet,
                    erläuterung=f"Die {i}. Ableitung wird gebildet",
                    lernhinweis=self._get_ableitungs_lernhinweis(
                        aktueller_ausdruck, variable
                    ),
                )
            )

            # Vereinfachen nach der Ableitung
            vereinfacht = simplify(abgeleitet)
            if vereinfacht != abgeleitet:
                session.add_schritt(
                    BerechnungsSchritt(
                        typ=BerechnungsSchrittTyp.VEREINFACHUNG,
                        beschreibung="Ableitung vereinfachen",
                        formel_vorher=abgeleitet,
                        formel_nachher=vereinfacht,
                        ergebnis=vereinfacht,
                        erläuterung="Die Ableitung wird vereinfacht",
                    )
                )
                aktueller_ausdruck = vereinfacht
            else:
                aktueller_ausdruck = abgeleitet

        # Endergebnis
        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.ERGEBNIS,
                beschreibung=f"Die {ordnung}. Ableitung lautet:",
                formel_vorher=funktion,
                formel_nachher=aktueller_ausdruck,
                ergebnis=aktueller_ausdruck,
                erläuterung=f"f^{ordnung}{'(x)' if ordnung == 1 else f'({ordnung})(x)'} = {aktueller_ausdruck}",
            )
        )

        return aktueller_ausdruck

    def _get_ableitungs_lernhinweis(
        self, ausdruck: sp.Expr, variable: sp.Symbol
    ) -> str:
        """Gibt einen passenden Lernhinweis für die Ableitung."""
        if ausdruck.is_constant():
            return "Die Ableitung einer Konstanten ist immer 0!"
        elif ausdruck.is_polynomial(variable):
            return "Polynome werden mit der Potenzregel abgeleitet: (x^n)' = n·x^(n-1)"
        elif ausdruck.has(sp.exp):
            return "Die Exponentialfunktion e^x ist ihre eigene Ableitung!"
        elif ausdruck.has(sp.sin) or ausdruck.has(sp.cos):
            return "Trigonometrische Funktionen: (sin x)' = cos x, (cos x)' = -sin x"
        else:
            return "Verwende die entsprechenden Ableitungsregeln für jeden Term!"


class FunktionsDebugger:
    """
    Hauptklasse für das Debugging von Funktionsberechnungen.

    Diese Klasse bietet eine umfassende Debugging-Umgebung für mathematische
    Berechnungen mit Schritt-für-Schritt-Anzeigen und pädagogischen Features.
    """

    def __init__(self, detailgrad: DetailGrad = DetailGrad.NORMAL):
        self.detailgrad = detailgrad
        self.strategien = [
            VereinfachungsStrategie(),
            AbleitungsStrategie(),
        ]
        self._aktive_session: Optional[DebugSession] = None
        self._session_history: List[DebugSession] = []

    def start_session(self, titel: str, funktion: Union[str, sp.Expr]) -> DebugSession:
        """Starte eine neue Debug-Session."""
        if isinstance(funktion, str):
            try:
                funktion = sympify(funktion)
            except Exception as e:
                raise ValueError(f"Ungültiger Funktionsausdruck: {e}")

        session = DebugSession(
            titel=titel, start_funktion=funktion, detailgrad=self.detailgrad
        )

        self._aktive_session = session
        self._session_history.append(session)

        # Initialisierungsschritt
        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.INITIALISIERUNG,
                beschreibung=f"Debug-Session gestartet: {titel}",
                formel_vorher=funktion,
                erläuterung=f"Analyse der Funktion f(x) = {funktion}",
            )
        )

        return session

    def berechne_ableitung(
        self, funktion: Union[str, sp.Expr], ordnung: int = 1, variable: str = "x"
    ) -> DebugSession:
        """Berechne die Ableitung mit ausführlicher Schritt-für-Schritt-Anzeige."""
        session = self.start_session(f"{ordnung}. Ableitung", funktion)

        x = sp.Symbol(variable)
        kontext = {"operation": "ableitung", "ordnung": ordnung, "variable": x}

        # Finde passende Strategie
        strategie_gefunden = False
        for strategie in self.strategien:
            if strategie.kann_anwenden(session.start_funktion, kontext):
                ergebnis = strategie.wende_an(session.start_funktion, session, kontext)
                strategie_gefunden = True
                break

        if not strategie_gefunden:
            # Fallback: Direkte Berechnung
            ergebnis = diff(session.start_funktion, x, ordnung)
            session.add_schritt(
                BerechnungsSchritt(
                    typ=BerechnungsSchrittTyp.ABLEITUNG,
                    beschreibung=f"Direkte Berechnung der {ordnung}. Ableitung",
                    formel_vorher=session.start_funktion,
                    formel_nachher=ergebnis,
                    ergebnis=ergebnis,
                )
            )

        session.endzeit = time.time()
        return session

    def berechne_nullstellen(self, funktion: Union[str, sp.Expr]) -> DebugSession:
        """Berechne Nullstellen mit ausführlicher Anzeige."""
        session = self.start_session("Nullstellenberechnung", funktion)

        try:
            # Gleichung aufstellen
            gleichung = sp.Eq(session.start_funktion, 0)
            session.add_schritt(
                BerechnungsSchritt(
                    typ=BerechnungsSchrittTyp.INITIALISIERUNG,
                    beschreibung="Gleichung aufstellen",
                    formel_vorher=session.start_funktion,
                    formel_nachher=gleichung,
                    erläuterung="Gesucht: f(x) = 0",
                )
            )

            # Nullstellen berechnen
            nullstellen = solve(gleichung, sp.Symbol("x"))

            if nullstellen:
                session.add_schritt(
                    BerechnungsSchritt(
                        typ=BerechnungsSchrittTyp.NULLSTELLENSUCHE,
                        beschreibung="Nullstellen gefunden",
                        formel_vorher=gleichung,
                        ergebnis=nullstellen,
                        erläuterung=f"Die Gleichung hat {len(nullstellen)} Lösung(en): {nullstellen}",
                        lernhinweis="Überprüfe immer, ob die gefundenen Lösungen in der Definitionsmenge liegen!",
                    )
                )
            else:
                session.add_schritt(
                    BerechnungsSchritt(
                        typ=BerechnungsSchrittTyp.NULLSTELLENSUCHE,
                        beschreibung="Keine reellen Nullstellen",
                        formel_vorher=gleichung,
                        ergebnis=[],
                        erläuterung="Die Gleichung hat keine reellen Lösungen",
                        lernhinweis="Manche Funktionen schneiden die x-Achse nie!",
                    )
                )

        except Exception as e:
            session.add_schritt(
                BerechnungsSchritt(
                    typ=BerechnungsSchrittTyp.FEHLER,
                    beschreibung="Fehler bei der Nullstellenberechnung",
                    ergebnis=str(e),
                    erläuterung=f"Die Nullstellen konnten nicht berechnet werden: {e}",
                )
            )

        session.endzeit = time.time()
        return session

    def vereinfache_funktion(self, funktion: Union[str, sp.Expr]) -> DebugSession:
        """Vereinfache eine Funktion Schritt für Schritt."""
        session = self.start_session("Funktionsvereinfachung", funktion)

        # Vereinfachungsstrategie anwenden
        strategie = VereinfachungsStrategie()
        ergebnis = strategie.wende_an(session.start_funktion, session, {})

        session.add_schritt(
            BerechnungsSchritt(
                typ=BerechnungsSchrittTyp.ERGEBNIS,
                beschreibung="Vereinfachte Funktion",
                formel_vorher=session.start_funktion,
                formel_nachher=ergebnis,
                ergebnis=ergebnis,
                erläuterung="Die Funktion wurde maximal vereinfacht",
            )
        )

        session.endzeit = time.time()
        return session

    def zeige_schritte(
        self, session: Optional[DebugSession] = None, format: str = "text"
    ) -> Union[str, Dict]:
        """Zeige die Schritte einer Session in verschiedenen Formaten."""
        if session is None:
            session = self._aktive_session

        if session is None:
            return "Keine aktive Session gefunden"

        if format == "text":
            return self._format_text(session)
        elif format == "latex":
            return self._format_latex(session)
        elif format == "dict":
            return session.to_dict()
        else:
            raise ValueError(f"Unbekanntes Format: {format}")

    def _format_text(self, session: DebugSession) -> str:
        """Formatiere die Session als Text."""
        output = [f"=== {session.titel} ==="]
        output.append(f"Startfunktion: f(x) = {session.start_funktion}")
        output.append(f"Detailgrad: {session.detailgrad.value}")
        output.append(f"Dauer: {session.berechnungsdauer():.3f} Sekunden")
        output.append("")

        for schritt in session.schritte:
            output.append(f"Schritt {schritt.schritt_nummer}: {schritt.beschreibung}")
            if schritt.formel_vorher:
                output.append(f"  Vorher: {schritt.pretty_vorher}")
            if schritt.formel_nachher:
                output.append(f"  Nachher: {schritt.pretty_nachher}")
            if schritt.ergebnis is not None:
                output.append(f"  Ergebnis: {schritt.ergebnis}")
            if schritt.erläuterung:
                output.append(f"  Erklärung: {schritt.erläuterung}")
            if schritt.lernhinweis:
                output.append(f"  💡 Lernhinweis: {schritt.lernhinweis}")
            output.append("")

        return "\n".join(output)

    def _format_latex(self, session: DebugSession) -> str:
        """Formatiere die Session als LaTeX."""
        latex_parts = [
            "\\section*{" + session.titel + "}",
            f"Startfunktion: $f(x) = " + latex(session.start_funktion) + "$",
            "",
            "\\begin{enumerate}",
        ]

        for schritt in session.schritte:
            latex_parts.append(f"\\item \\textbf{{{schritt.beschreibung}}}")
            if schritt.formel_vorher:
                latex_parts.append(f"Vorher: ${schritt.latex_vorher}$")
            if schritt.formel_nachher:
                latex_parts.append(f"Nachher: ${schritt.latex_nachher}$")
            if schritt.erläuterung:
                latex_parts.append(f"\\textit{{{schritt.erläuterung}}}")
            if schritt.lernhinweis:
                latex_parts.append(f"\\textbf{{Lernhinweis:}} {schritt.lernhinweis}")
            latex_parts.append("")

        latex_parts.append("\\end{enumerate}")
        return "\n".join(latex_parts)

    def get_session_history(self) -> List[DebugSession]:
        """Gib die History aller Sessions zurück."""
        return self._session_history.copy()

    def clear_history(self):
        """Lösche die Session-History."""
        self._session_history.clear()
        self._aktive_session = None

    def set_detailgrad(self, detailgrad: DetailGrad):
        """Setze den Detailgrad für neue Sessions."""
        self.detailgrad = detailgrad
        if self._aktive_session:
            self._aktive_session.detailgrad = detailgrad


# Globale Debugger-Instanz
debugger = FunktionsDebugger()


# Bequemliche Funktionen für die API
def DebuggeAbleitung(funktion: Union[str, sp.Expr], ordnung: int = 1) -> DebugSession:
    """Bequeme Funktion für das Debugging von Ableitungen."""
    return debugger.berechne_ableitung(funktion, ordnung)


def DebuggeNullstellen(funktion: Union[str, sp.Expr]) -> DebugSession:
    """Bequeme Funktion für das Debugging von Nullstellen."""
    return debugger.berechne_nullstellen(funktion)


def DebuggeVereinfachung(funktion: Union[str, sp.Expr]) -> DebugSession:
    """Bequeme Funktion für das Debugging von Vereinfachungen."""
    return debugger.vereinfache_funktion(funktion)


def ZeigeDebugSchritte(session: DebugSession, format: str = "text") -> Union[str, Dict]:
    """Bequeme Funktion zur Anzeige von Debug-Schritten."""
    return debugger.zeige_schritte(session, format)
