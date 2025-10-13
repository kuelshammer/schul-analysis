"""
Gebrochen-rationale Funktionen für das Schul-Analysis Framework.

Unterstützt verschiedene Konstruktor-Formate und mathematisch korrekte
Visualisierung mit Plotly für Marimo-Notebooks.
"""

import re
from typing import Any, Union

import sympy as sp

from .errors import (
    DivisionDurchNullError,
    SicherheitsError,
    UngueltigerAusdruckError,
)
from .funktion import Funktion
from .ganzrationale import GanzrationaleFunktion
from .sympy_types import (
    VALIDATION_EXACT,
    validate_function_result,
    validate_exact_results,
    preserve_exact_types,
    ExactNullstellenListe,
)


def _validiere_mathematischen_ausdruck(ausdruck: str) -> bool:
    """Validiert, ob ein Ausdruck sicher für mathematische Auswertung ist"""
    # Erlaubte mathematische Zeichen und Funktionen
    erlaubte_muster = r"^[0-9+\-*/^()x\s.a-zA-Z]+$|^[a-zA-Z_][a-zA-Z0-9_]*\s*\("

    # Gefährliche Muster
    gefaehrliche_muster = [
        r"import\s+",
        r"exec\s*\(",
        r"eval\s*\(",
        r"__.*__",
        r"subprocess\.",
        r"os\.",
        r"sys\.",
        r"open\s*\(",
        r"file\s*\(",
        r"input\s*\(",
        r"globals\s*\(",
        r"locals\s*\(",
    ]

    # Prüfe auf gefährliche Muster
    for muster in gefaehrliche_muster:
        if re.search(muster, ausdruck, re.IGNORECASE):
            raise SicherheitsError("Gefährlicher Ausdruck erkannt", ausdruck)

    # Prüfe auf gültiges mathematisches Format
    if not re.match(erlaubte_muster, ausdruck.strip()):
        raise UngueltigerAusdruckError(ausdruck, "Ungültiger mathematischer Ausdruck")

    return True


def _pruefe_division_durch_null(_zaehler, nenner) -> None:
    """Prüft auf Division durch Null"""
    import sympy as sp

    # Wenn nenner ein String ist, prüfe direkt auf "0"
    if isinstance(nenner, str):
        if nenner.strip() == "0":
            raise DivisionDurchNullError("Division durch Null")
        # Versuche, den String zu parsen
        try:
            from .funktion import Funktion

            temp_funktion = Funktion(nenner)
            if hasattr(temp_funktion, "term_sympy") and temp_funktion.term_sympy == 0:
                raise DivisionDurchNullError("Division durch Null")
        except Exception:
            pass  # Wenn Parsing fehlschlägt, prüfen wir später

    # Wenn nenner eine Zahl ist
    elif isinstance(nenner, (int, float)) and nenner == 0:
        raise DivisionDurchNullError("Division durch Null")

    # Wenn nenner eine SymPy-Zahl ist
    elif hasattr(nenner, "term_sympy") and nenner.term_sympy == 0:
        raise DivisionDurchNullError("Division durch Nullfunktion")

    # Wenn nenner direkt mit 0 vergleichbar ist
    elif hasattr(nenner, "__eq__") and nenner == 0:
        raise DivisionDurchNullError("Division durch Null")


def _validiere_konstruktor_parameter(zaehler, nenner) -> None:
    """Validiert die Konstruktorparameter"""
    if zaehler is None:
        raise UngueltigerAusdruckError("None", "Zähler darf nicht None sein")

    # Wenn nenner None ist, ist es ein String-Konstruktor
    if nenner is not None:
        _pruefe_division_durch_null(zaehler, nenner)


class GebrochenRationaleFunktion(Funktion):
    """
    Pädagogischer Wrapper für gebrochen-rationale Funktionen.

    Diese Klasse ist ein Thin-Wrapper über der unified Funktion-Klasse,
    der gebrochen-rationale spezifische Methoden bereitstellt.
    """

    def __init__(
        self,
        zaehler: GanzrationaleFunktion | str | sp.Basic,
        nenner: GanzrationaleFunktion | str | sp.Basic | None = None,
    ):
        """
        Konstruktor für gebrochen-rationale Funktionen.

        Args:
            zaehler: GanzrationaleFunktion, String ("x^2+1") oder SymPy-Ausdruck
            nenner: GanzrationaleFunktion, String ("x-1") oder SymPy-Ausdruck.
                    Wenn None und zaehler ist String, wird versucht aus "(x^2+1)/(x-1)" zu parsen
        """
        # 🔥 PÄDAGOGISCHER WRAPPER - Keine komplexe Logik mehr! 🔥

        # Konstruiere die Eingabe für die Basisklasse
        if isinstance(zaehler, str) and nenner is None:
            # String im Format "(zaehler)/(nenner)"
            eingabe = zaehler
        elif isinstance(zaehler, str) and isinstance(nenner, str):
            # Beide als String übergeben
            eingabe = f"({zaehler})/({nenner})"
        elif isinstance(zaehler, (GanzrationaleFunktion, sp.Basic)) and isinstance(
            nenner, (GanzrationaleFunktion, sp.Basic)
        ):
            # Zaehler und Nenner einzeln übergeben - konvertiere zu Strings
            zaehler_str = str(
                zaehler.term_sympy if hasattr(zaehler, "term_sympy") else zaehler
            )
            nenner_str = str(
                nenner.term_sympy if hasattr(nenner, "term_sympy") else nenner
            )
            eingabe = f"({zaehler_str})/({nenner_str})"
        else:
            raise TypeError(
                "Ungültige Eingabeparameter für gebrochen-rationale Funktion"
            )

        # Speichere ursprüngliche Eingabe für Validierung
        self.original_eingabe = eingabe

        # 🔥 SICHERHEITSPRÜFUNG: Division durch Null vor der Verarbeitung
        if nenner is not None:
            _pruefe_division_durch_null(zaehler, nenner)

        # Rufe den Konstruktor der Basisklasse auf
        super().__init__(eingabe)

        # 🔥 SICHERHEITSPRÜFUNG: Nach der Verarbeitung nochmal prüfen (für String-Konstruktor)
        try:
            from sympy import fraction

            _, nenner_sympy = fraction(self.term_sympy)
            if nenner_sympy == 0:
                raise DivisionDurchNullError("Division durch Null")
        except Exception:
            # Wenn fraction fehlschlägt, prüfe wir auf andere Weise
            if hasattr(self, "nenner") and hasattr(self.nenner, "term_sympy"):
                if self.nenner.term_sympy == 0:
                    raise DivisionDurchNullError("Division durch Null")

        # 🔥 PÄDAGOGISCHE VALIDIERUNG mit deutscher Fehlermeldung 🔥
        if not self.ist_gebrochen_rational:
            raise TypeError(
                f"Die Eingabe '{self.original_eingabe}' ist keine gebrochen-rationale Funktion! "
                "Eine gebrochen-rationale Funktion muss ein Bruch aus zwei Polynomen sein. "
                "Hast du vielleicht eine ganzrationale, exponentiale oder trigonometrische Funktion gemeint?"
            )

        # 🔥 CACHE für wiederholte Berechnungen
        self._cache = {
            "polstellen": None,
            "zaehler_nenner": None,
        }

    @property
    def zaehler(self) -> GanzrationaleFunktion:
        """Gibt den Zähler als GanzrationaleFunktion zurück"""
        if self._cache["zaehler_nenner"] is None:
            from sympy import fraction

            zaehler_sympy, _ = fraction(self.term_sympy)
            self._cache["zaehler_nenner"] = (
                GanzrationaleFunktion(zaehler_sympy),
                None,  # Wird bei Bedarf gesetzt
            )

        if self._cache["zaehler_nenner"][1] is None:
            from sympy import fraction

            _, nenner_sympy = fraction(self.term_sympy)
            self._cache["zaehler_nenner"] = (
                self._cache["zaehler_nenner"][0],
                GanzrationaleFunktion(nenner_sympy),
            )

        return self._cache["zaehler_nenner"][0]

    @property
    def nenner(self) -> GanzrationaleFunktion:
        """Gibt den Nenner als GanzrationaleFunktion zurück"""
        if self._cache["zaehler_nenner"] is None:
            from sympy import fraction

            zaehler_sympy, nenner_sympy = fraction(self.term_sympy)
            self._cache["zaehler_nenner"] = (
                GanzrationaleFunktion(zaehler_sympy),
                GanzrationaleFunktion(nenner_sympy),
            )

        return self._cache["zaehler_nenner"][1]

    def polstellen(self) -> list[float]:
        """Berechnet die Polstellen der Funktion (Nenner-Nullstellen)"""
        if self._cache["polstellen"] is None:
            polstellen = self.nenner.nullstellen
            # Convert Nullstelle objects to simple values
            if polstellen and hasattr(polstellen[0], "x"):
                self._cache["polstellen"] = [float(p.x) for p in polstellen]
            else:
                self._cache["polstellen"] = polstellen
        return self._cache["polstellen"]

    def definitionsluecken(self) -> list[float]:
        """Gibt die Definitionslücken zurück (Polstellen)"""
        return self.polstellen()

    @preserve_exact_types
    def nullstellen(
        self, real: bool = True, runden: int | None = None
    ) -> ExactNullstellenListe:
        """
        Berechnet die Nullstellen der gebrochen-rationalen Funktion.

        Delegiert an die QuotientFunktion-Implementierung für korrekte
        Berücksichtigung von Zähler-Nullstellen und Polstellen.

        Args:
            real: Nur reelle Nullstellen zurückgeben (Standard: True)
            runden: Anzahl Dezimalstellen zum Runden (optional)

        Returns:
            Liste der gültigen Nullstellen als SymPy-Ausdrücke

        Examples:
            >>> f = GebrochenRationaleFunktion("x^2-1", "x-1")
            >>> # (x²-1)/(x-1) = x+1 für x≠1, also keine Nullstellen (x=1 ist Polstelle)
            >>> nullstellen = f.nullstellen()  # []
        """
        try:
            # Hole Zähler-Nullstellen direkt als Property für exakte Ergebnisse
            zaehler_nullstellen = self.zaehler.nullstellen

            # Hole Polstellen (sind schon berechnet)
            polstellen = self.polstellen()

            # Konvertiere zu Sets für effizienten Vergleich
            # Handle sowohl alte als auch neue Formate
            polstelle_set = set()
            for p in polstellen:
                if hasattr(p, "x"):
                    polstelle_set.add(p.x)
                else:
                    polstelle_set.add(p)

            # Filtere Zähler-Nullstellen: nur die, die keine Polstellen sind
            gueltige_nullstellen = []
            for zn in zaehler_nullstellen:
                if hasattr(zn, "x"):
                    # Neues Format: Nullstelle-Datenklasse
                    if zn.x not in polstelle_set:
                        gueltige_nullstellen.append(zn)
                else:
                    # Altes Format: direktes SymPy-Objekt
                    if zn not in polstelle_set:
                        gueltige_nullstellen.append(zn)

            # Wende die real-Filterung an, falls angefordert
            if real:
                gueltige_nullstellen = [
                    zn
                    for zn in gueltige_nullstellen
                    if hasattr(zn, "x") and hasattr(zn.x, "is_real") and zn.x.is_real
                ]

            # Wende die Rundung an, falls angefordert
            if runden is not None:
                # Konvertiere zu float für die Rundung
                gerundete_nullstellen = []
                for zn in gueltige_nullstellen:
                    if hasattr(zn, "x"):
                        gerundeter_wert = round(float(zn.x), runden)
                        # Erstelle eine neue Nullstelle mit dem gerundeten Wert
                        from .sympy_types import Nullstelle

                        gerundete_nullstellen.append(
                            Nullstelle(
                                x=gerundeter_wert,
                                multiplicitaet=zn.multiplicitaet,
                                exakt=False,
                            )
                        )
                    else:
                        gerundete_nullstellen.append(round(float(zn), runden))
                gueltige_nullstellen = gerundete_nullstellen

            # Validiere die Ergebnisse nur, wenn wir exakte Ergebnisse behalten haben
            if runden is None:
                validate_exact_results(
                    gueltige_nullstellen, "Gebrochen-rationale Nullstellen"
                )

            # Konvertiere Nullstelle-Objekte zu einfachen Werten für Konsistenz
            if gueltige_nullstellen and hasattr(gueltige_nullstellen[0], "x"):
                if runden is not None:
                    # Bereits gerundet, als floats zurückgeben
                    ergebnis = [
                        float(zn.x) if hasattr(zn, "x") else zn
                        for zn in gueltige_nullstellen
                    ]
                else:
                    # Exakte Werte als floats konvertieren
                    ergebnis = [float(zn.x) for zn in gueltige_nullstellen]
            else:
                ergebnis = gueltige_nullstellen

            return ergebnis

        except Exception as e:
            raise ValueError(
                f"Fehler bei der Nullstellenberechnung für gebrochen-rationale Funktion: {str(e)}\n"
                "Tipp: Die Nullstellen entsprechen den Zähler-Nullstellen, die keine Polstellen sind."
            ) from e

    def __str__(self) -> str:
        """String-Repräsentation"""
        return str(self.term_sympy)

    def __repr__(self) -> str:
        """Repräsentation für debugging"""
        return self.__str__()

    def _repr_latex_(self) -> str:
        """LaTeX-Darstellung für Jupyter/Marimo Notebooks"""
        return self.term_sympy._repr_latex_()

    def __eq__(self, other) -> bool:
        """Vergleich zweier Funktionen auf Gleichheit"""
        if not isinstance(other, GebrochenRationaleFunktion):
            return False
        return self.zaehler == other.zaehler and self.nenner == other.nenner

    def graph(self, x_min=None, x_max=None, y_min=None, y_max=None, **kwargs) -> Any:
        """Einheitliche Methode zur Darstellung der Funktion mit Plotly

        Args:
            x_min: Untere x-Grenze (Standard: None = automatisch)
            x_max: Obere x-Grenze (Standard: None = automatisch)
            y_min: Untere y-Grenze (Standard: None = automatisch)
            y_max: Obere y-Grenze (Standard: None = automatisch)
            **kwargs: Zusätzliche Parameter für die Plotly-Darstellung

        Returns:
            Plotly-Figur für die Darstellung
        """
        from . import Graph

        # Verwende die zentrale Graph-Funktion für intelligente Skalierung
        fig = Graph(self, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, **kwargs)

        # 🔥 FIX: Erzwinge Axis-Ranges gegen Marimo-Auto-Scaling
        fig.update_layout(
            xaxis={
                "autorange": False,
                "range": [fig.layout.xaxis.range[0], fig.layout.xaxis.range[1]],
                "constrain": "domain",
                "fixedrange": True,  # Verhindert manuelles Zoomen initially
            },
            yaxis={
                "autorange": False,
                "range": [fig.layout.yaxis.range[0], fig.layout.yaxis.range[1]],
                "constrain": "domain",
                "fixedrange": False,  # Erlaube manuelles Zoomen für y-Achse
            },
            # Zusätzliche Constraints um Auto-Scaling zu verhindern
            xaxis_constrain="domain",
            yaxis_constrain="domain",
        )

        return fig

    def _berechne_asymptoten(self) -> list[dict]:
        """
        Berechnet horizontale und schiefe Asymptoten.

        Returns:
            Liste von Asymptoten-Dictionarys mit keys: typ, steigung, y_offset
        """
        asymptoten = []

        # Bestimme Grade von Zähler und Nenner
        grad_zaehler = self.zaehler.grad()
        grad_nenner = self.nenner.grad()

        if grad_zaehler < grad_nenner:
            # Horizontale Asymptote y = 0
            asymptoten.append({"typ": "horizontal", "y": 0})
        elif grad_zaehler == grad_nenner:
            # Horizontale Asymptote y = Leitkoeffizient
            lkh_zaehler = (
                self.zaehler.koeffizienten[-1] if self.zaehler.koeffizienten else 0
            )
            lkh_nenner = (
                self.nenner.koeffizienten[-1] if self.nenner.koeffizienten else 1
            )
            y_asymptote = float(lkh_zaehler / lkh_nenner)
            asymptoten.append({"typ": "horizontal", "y": y_asymptote})
        elif grad_zaehler == grad_nenner + 1:
            # Schiefe Asymptote
            # Polynomdivision durchführen
            from sympy import div

            quotient, rest = div(self.zaehler.term_sympy, self.nenner.term_sympy)

            # Extrahiere Koeffizienten y = mx + b
            if quotient.is_polynomial(self._variable_symbol):
                quotient_poly = sp.poly(quotient, self._variable_symbol)
                koeffizienten = quotient_poly.all_coeffs()

                if len(koeffizienten) == 2:
                    # Lineare Funktion y = mx + b
                    steigung = float(koeffizienten[0])
                    y_offset = float(koeffizienten[1])
                    asymptoten.append(
                        {"typ": "schief", "steigung": steigung, "y_offset": y_offset}
                    )
                elif len(koeffizienten) == 1:
                    # Konstante Funktion y = b
                    steigung = 0
                    y_offset = float(koeffizienten[0])
                    asymptoten.append({"typ": "horizontal", "y": y_offset})

        return asymptoten

    # =============================================================================
    # NEUE METHODEN: SCHMIEGKURVE UND STÖRFUNKTION
    # =============================================================================

    def _berechne_zerlegung(self) -> None:
        """
        Private Methode zur effizienten Berechnung der Zerlegung.
        Berechnet Schmiegkurve und Störfunktion einmal und cacht die Ergebnisse.
        Vermeidet redundante Polynomdivisionen.
        """
        if self._cache["_zerlegung_berechnet"]:
            return

        # Bestimme Grade von Zähler und Nenner
        grad_zaehler = self.zaehler.grad()
        grad_nenner = self.nenner.grad()

        quotient_sympy = sp.S(0)
        rest_sympy = self.zaehler.term_sympy

        if grad_zaehler >= grad_nenner:
            # sp.div gibt sowohl Quotient als auch Rest zurück - effizient!
            quotient_sympy, rest_sympy = sp.div(
                self.zaehler.term_sympy, self.nenner.term_sympy, domain="QQ"
            )

        # Cache die Ergebnisse
        self._cache["_schmiegkurve"] = GanzrationaleFunktion(quotient_sympy)

        # Erstelle Störfunktion aus Rest und Nenner
        self._cache["_stoerfunktion"] = GebrochenRationaleFunktion(
            rest_sympy, self.nenner.term_sympy
        )
        self._cache["_zerlegung_berechnet"] = True

    def schmiegkurve(self) -> "GanzrationaleFunktion":
        """
        Gibt die Schmiegkurve (polynomialer Teil) der gebrochen-rationalen Funktion zurück.

        Für eine rationale Funktion f(x) = Z(x)/N(x):
        - Wenn grad(Z) < grad(N): Schmiegkurve = 0 (horizontale Asymptote y = 0)
        - Wenn grad(Z) = grad(N): Schmiegkurve = Leitkoeffizienten-Verhältnis (horizontale Asymptote)
        - Wenn grad(Z) > grad(N): Polynomdivision durchführen, polynomialer Teil ist die Schmiegkurve

        Returns:
            GanzrationaleFunktion: Die Schmiegkurve der Funktion

        Beispiele:
            >>> f = GebrochenRationaleFunktion("x^2+1", "x-1")  # grad(Z)=2, grad(N)=1
            >>> s = f.schmiegkurve()  # s(x) = x + 1 (schiefe Asymptote)

            >>> g = GebrochenRationaleFunktion("x+1", "x^2-1")  # grad(Z)=1, grad(N)=2
            >>> t = g.schmiegkurve()  # t(x) = 0 (horizontale Asymptote y = 0)

        Didaktischer Hinweis:
            Die Schmiegkurve ist die Funktion, an die sich f(x) für große |x| annähert.
            Sie beschreibt das "globale" Verhalten der Funktion.
        """
        # Berechne Zerlegung nur einmal und verwende Cache
        self._berechne_zerlegung()
        return self._cache["_schmiegkurve"]

    def stoerfunktion(self) -> "GebrochenRationaleFunktion":
        """
        Gibt die Störfunktion (echt gebrochen-rationaler Teil) zurück.

        Die Störfunktion ist definiert als: f(x) = Schmiegkurve(x) + Störfunktion(x)
        Sie hat die Eigenschaft, dass für große |x| die Störfunktion gegen 0 geht.

        Returns:
            GebrochenRationaleFunktion: Die Störfunktion mit grad(Zähler) < grad(Nenner)

        Beispiele:
            >>> f = GebrochenRationaleFunktion("x^2+1", "x-1")
            >>> s = f.schmiegkurve()  # s(x) = x + 1
            >>> r = f.stoerfunktion()  # r(x) = 2/(x-1)
            >>> # Überprüfung: f(x) = (x+1) + 2/(x-1) = (x^2-x+2)/(x-1)

        Didaktischer Hinweis:
            Die Störfunktion beschreibt die "lokale" Abweichung von der Schmiegkurve
            und bestimmt das Verhalten in der Nähe von Polstellen.
        """
        # Berechne Zerlegung nur einmal und verwende Cache
        self._berechne_zerlegung()
        return self._cache["_stoerfunktion"]

    def spezialisiere_parameter(self, **werte) -> "GebrochenRationaleFunktion":
        """
        Setzt Parameter auf spezifische Werte und gibt eine neue Funktion zurück.

        Args:
            **werte: Parameter-Wert-Paare (z.B. a=2, b=3)

        Returns:
            Neue GebrochenRationaleFunktion mit spezifizierten Parameterwerten
        """
        # Ersetze Parameter durch die gegebenen Werte
        neuer_zaehler = self.zaehler.term_sympy
        neuer_nenner = self.nenner.term_sympy

        for param_name, wert in werte.items():
            # Finde das passende Parameter-Symbol in Zähler
            param_symbol = None
            for p in self.zaehler.parameter:
                if p.name == param_name:
                    param_symbol = p.symbol
                    break

            # Wenn nicht im Zähler, im Nenner suchen
            if param_symbol is None:
                for p in self.nenner.parameter:
                    if p.name == param_name:
                        param_symbol = p.symbol
                        break

            if param_symbol is not None:
                neuer_zaehler = neuer_zaehler.subs(param_symbol, wert)
                neuer_nenner = neuer_nenner.subs(param_symbol, wert)

        # Erstelle neue Funktion mit spezialisierten Werten
        return GebrochenRationaleFunktion(neuer_zaehler, neuer_nenner)

    def erstelle_uebungsaufgabe(self, schwierigkeit: str = "mittel") -> dict:
        """
        Erstellt eine Übungsaufgabe zur Zerlegung gebrochen-rationaler Funktionen.

        Args:
            schwierigkeit: "einfach", "mittel", oder "schwer"

        Returns:
            dict: Übungsaufgabe mit Lösung und Erklärung

        Beispiele:
            >>> aufgabe = f.erstelle_uebungsaufgabe("einfach")
            >>> print(aufgabe['aufgabe'])
            >>> print(aufgabe['loesung'])
        """

        if schwierigkeit == "einfach":
            # Einfache Fälle: grad(Z) ≤ grad(N)
            aufgaben = [
                {"zaehler": "x+1", "nenner": "x-1", "typ": "horizontal"},
                {"zaehler": "2x+3", "nenner": "x+2", "typ": "horizontal"},
                {"zaehler": "x^2+1", "nenner": "x^2-1", "typ": "horizontal"},
            ]
        elif schwierigkeit == "mittel":
            # Mittlere Fälle: grad(Z) = grad(N) + 1
            aufgaben = [
                {"zaehler": "x^2+1", "nenner": "x-1", "typ": "schief"},
                {"zaehler": "x^2+4x+3", "nenner": "x+1", "typ": "schief"},
                {"zaehler": "2x^2-3", "nenner": "x+2", "typ": "schief"},
            ]
        else:  # schwer
            # Schwere Fälle: grad(Z) > grad(N) + 1
            aufgaben = [
                {"zaehler": "x^3+1", "nenner": "x-1", "typ": "schief_kubisch"},
                {
                    "zaehler": "x^3-2x^2+3",
                    "nenner": "x^2+1",
                    "typ": "schief_quadratisch",
                },
            ]

        import random

        aufgabe_data = random.choice(aufgaben)

        # Erstelle Übungsfunktion
        uebung_funktion = GebrochenRationaleFunktion(
            aufgabe_data["zaehler"], aufgabe_data["nenner"]
        )
        s = uebung_funktion.schmiegkurve()
        r = uebung_funktion.stoerfunktion()

        # Generiere Aufgabe basierend auf Typ
        if aufgabe_data["typ"] == "horizontal":
            frage = f"Bestimmen Sie die horizontale Asymptote der Funktion f(x) = {uebung_funktion.term()}"
            loesung_text = f"Die horizontale Asymptote ist y = {s.term()}"
        else:
            frage = f"Zerlegen Sie die Funktion f(x) = {uebung_funktion.term()} in Schmiegkurve und Störfunktion"
            loesung_text = f"f(x) = {s.term()} + {r.term()}"

        return {
            "schwierigkeit": schwierigkeit,
            "aufgabe": frage,
            "funktion": uebung_funktion.term(),
            "tipps": [
                "Bestimmen Sie zuerst die Grade von Zähler und Nenner",
                "Überlegen Sie, ob eine Polynomdivision nötig ist",
                "Die Störfunktion sollte für große |x| gegen 0 gehen",
            ],
            "loesung": {
                "schmiegkurve": s.term(),
                "stoerfunktion": r.term(),
                "zerlegung": f"f(x) = {s.term()} + {r.term()}",
                "erklaerung": loesung_text,
            },
            "ueberpruefung": {
                "valid": uebung_funktion.validiere_zerlegung(),
                "methode": "Addieren Sie Schmiegkurve und Störfunktion, um das Ergebnis zu überprüfen",
            },
        }

    def vergleiche_funktionen(
        self, andere_funktion: "GebrochenRationaleFunktion"
    ) -> dict:
        """
        Vergleicht zwei gebrochen-rationale Funktionen bezüglich ihrer Zerlegung.

        Args:
            andere_funktion: Zweite Funktion zum Vergleich

        Returns:
            dict: Vergleich der Funktionen mit Analyse

        Beispiele:
            >>> f1 = GebrochenRationaleFunktion("x^2+1", "x-1")
            >>> f2 = GebrochenRationaleFunktion("x^2+4", "x+2")
            >>> vergleich = f1.vergleiche_funktionen(f2)
        """
        s1 = self.schmiegkurve()
        r1 = self.stoerfunktion()

        s2 = andere_funktion.schmiegkurve()
        r2 = andere_funktion.stoerfunktion()

        return {
            "funktion1": {
                "term": self.term(),
                "schmiegkurve": s1.term(),
                "stoerfunktion": r1.term(),
                "grad_z": self.zaehler.grad(),
                "grad_n": self.nenner.grad(),
            },
            "funktion2": {
                "term": andere_funktion.term(),
                "schmiegkurve": s2.term(),
                "stoerfunktion": r2.term(),
                "grad_z": andere_funktion.zaehler.grad(),
                "grad_n": andere_funktion.nenner.grad(),
            },
            "vergleich": {
                "gleiche_schmiegkurve": s1.term() == s2.term(),
                "gleiche_stoerfunktion": r1.term() == r2.term(),
                "asymptotisches_verhalten": {
                    "f1": f"lim x->∞: {s1.term()}",
                    "f2": f"lim x->∞: {s2.term()}",
                    "ähnlich": s1.term() == s2.term(),
                },
            },
            "didaktischer_hinweis": "Vergleichen Sie, wie sich verschiedene Koeffizienten auf das asymptotische Verhalten auswirken.",
        }


# =============================================================================
# SPEZIALISIERTE METHODEN FÜR GEBROCHEN-RATIONALE FUNKTIONEN
# =============================================================================
