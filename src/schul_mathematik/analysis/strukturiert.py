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
from .sympy_types import Nullstelle, ExactNullstellenListe, validate_exact_results

from sympy import solve, simplify, solveset, S, Interval
from .sympy_types import preserve_exact_types


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
            # Vermeide Rekursion: Verwende die Strukturanalyse nur, wenn sie nicht bereits läuft
            from .struktur import analysiere_funktionsstruktur, StrukturAnalyseError

            try:
                self._struktur_info = analysiere_funktionsstruktur(eingabe)
            except StrukturAnalyseError:
                # Bei Rekursion oder Fehler, erstelle Basis-Strukturinfo
                self._struktur_info = {
                    "original_term": str(eingabe),
                    "struktur": "unbekannt",
                    "komponenten": [
                        {
                            "ausdruck": eingabe,
                            "typ": "unbekannt",
                            "term": str(eingabe),
                            "latex": str(eingabe),
                        }
                    ],
                    "variable": "x",
                    "latex": str(eingabe),
                    "kann_faktorisiert_werden": False,
                }
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

    def _erzeuge_typisierte_komponente(self, term: str, typ: str) -> Funktion | None:
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
                    expr = sp.sympify(term, rational=True)  # type: ignore
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
            expr = sp.sympify(term, rational=True)  # type: ignore

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
    def funktionstyp(self) -> str:
        """Gibt den Funktionstyp als String zurück"""
        return "produkt"

    @property
    def faktoren(self) -> list[Funktion]:
        """Gibt die typisierten Faktoren des Produkts zurück."""
        return self._faktoren

    @property
    def faktor1(self) -> Funktion | None:
        """Gibt den ersten Faktor zurück."""
        return self._faktoren[0] if len(self._faktoren) > 0 else None

    @property
    def faktor2(self) -> Funktion | None:
        """Gibt den zweiten Faktor zurück."""
        return self._faktoren[1] if len(self._faktoren) > 1 else None

    def __str__(self):
        return f"Produkt({', '.join(str(f) for f in self.faktoren)})"

    def nullstellen(
        self, real: bool = True, runden: int | None = None
    ) -> ExactNullstellenListe:
        """
        Berechnet Nullstellen unter Verwendung des Nullproduktsatzes.

        Für f(x) = F₁(x) × F₂(x) × ... × Fₙ(x) = 0 gilt:
        f(x) = 0 ⇔ mindestens ein Fᵢ(x) = 0

        Diese Methode nutzt Sympy's Vereinfachung für zuverlässige
        Duplikatserkennung bei symbolischen Ausdrücken.

        Args:
            real: Nur reelle Nullstellen zurückgeben (Standard: True)
            runden: Anzahl Dezimalstellen zum Runden (optional)

        Returns:
            Liste der Nullstellen mit korrekten Vielfachheiten
        """
        # Sammle alle Nullstellen von allen Faktoren
        alle_nullstellen = []

        for faktor in self.faktoren:
            if hasattr(faktor, "nullstellen"):
                # Alle Klassen verwenden jetzt konsistent die nullstellen() Methode
                faktor_nullstellen = faktor.nullstellen(real=real, runden=runden)
                alle_nullstellen.extend(faktor_nullstellen)

        # Kombiniere die Nullstellen mit Sympy-Vereinfachung
        return self._kombiniere_mit_sympy_simplify(alle_nullstellen)

    def _kombiniere_mit_sympy_simplify(
        self, alle_nullstellen: list[Nullstelle]
    ) -> ExactNullstellenListe:
        """
        Kombiniert Nullstellen mit Sympy's zuverlässiger Vereinfachung.

        Args:
            alle_nullstellen: Liste aller Nullstellen von allen Faktoren

        Returns:
            Kombinierte Liste mit korrekten Vielfachheiten
        """
        vereinfachte_map = {}

        for nullstelle in alle_nullstellen:
            # Handle verschiedene Formate von Nullstellen (alt und neu)
            # Altes Format: direktes SymPy-Objekt (z.B. Zero, Pi)
            # Neues Format: Nullstelle-Datenklasse mit .x Attribut

            if hasattr(nullstelle, "x"):
                # Neues Format: Nullstelle-Datenklasse
                x_wert = nullstelle.x
                multiplicitaet = nullstelle.multiplicitaet
                exakt = nullstelle.exakt
            else:
                # Altes Format: direktes SymPy-Objekt
                x_wert = nullstelle
                multiplicitaet = 1  # Standard-Vielfachheit
                exakt = True  # SymPy-Ergebnisse sind exakt

            # Versuche zu vereinfachen, aber handle Fehler gracefully
            try:
                if hasattr(x_wert, "is_Number") and x_wert.is_Number:
                    # Für numerische Werte: direkt verwenden
                    x_vereinfacht = x_wert
                else:
                    # Für symbolische Ausdrücke: vereinfachen
                    x_vereinfacht = simplify(x_wert)
            except Exception:
                # Bei Vereinfachungsfehlern: Originalwert verwenden
                x_vereinfacht = x_wert

            # Erstelle einen hashbaren Schlüssel
            try:
                # Versuche eine String-Repräsentation
                schlüssel = str(x_vereinfacht)
            except Exception:
                # Fallback: Verwende den Index als Schlüssel (sollte selten vorkommen)
                schlüssel = f"unbekannt_{id(nullstelle)}"

            if schlüssel in vereinfachte_map:
                # Addiere die Vielfachheiten zur bestehenden Nullstelle
                vorhandene = vereinfachte_map[schlüssel]
                neue_multiplicitaet = vorhandene.multiplicitaet + multiplicitaet

                # Ersetze die vorhandene Nullstelle mit neuer Vielfachheit
                vereinfachte_map[schlüssel] = Nullstelle(
                    x=x_vereinfacht,
                    multiplicitaet=neue_multiplicitaet,
                    exakt=vorhandene.exakt and exakt,
                )
            else:
                # Füge neue vereinfachte Nullstelle hinzu
                vereinfachte_map[schlüssel] = Nullstelle(
                    x=x_vereinfacht,
                    multiplicitaet=multiplicitaet,
                    exakt=exakt,
                )

        return list(vereinfachte_map.values())

    def _sind_symbolisch_gleich(self, ausdruck1: sp.Expr, ausdruck2: sp.Expr) -> bool:
        """
        Prüft ob zwei symbolische Ausdrücke äquivalent sind.

        Diese Methode erkennt äquivalente Ausdrücke auch in verschiedenen
        Darstellungsformen, was für die Multiplicity-Erkennung wichtig ist.

        Args:
            ausdruck1: Erster symbolischer Ausdruck
            ausdruck2: Zweiter symbolischer Ausdruck

        Returns:
            True wenn die Ausdrücke äquivalent sind
        """
        try:
            # Vereinfache beide Ausdrücke
            einfach1 = sp.simplify(ausdruck1)
            einfach2 = sp.simplify(ausdruck2)

            # Prüfe auf direkte Gleichheit
            if einfach1 == einfach2:
                return True

            # Prüfe ob eines das Negative des anderen ist (wichtig für Vorzeichen)
            if einfach1 == -einfach2:
                return True

            # Prüfe ob expandierte Formen gleich sind
            if sp.expand(einfach1) == sp.expand(einfach2):
                return True

            # Spezialfall: Verhältnisse wie -b/a == c
            # Dies erfordert Lösung von Gleichungen
            try:
                # Prüfe ob einfach1 - einfach2 = 0 für alle Werte gilt
                diff = sp.simplify(einfach1 - einfach2)
                if diff == 0:
                    return True

                # Prüfe ob die Differenz nach Expansion null ist
                if sp.expand(diff) == 0:
                    return True
            except:
                pass

            return False

        except Exception:
            # Bei Fehlern in der symbolischen Vereinfachung
            return False

    def _kombiniere_nullstellen_intelligent(
        self, alle_nullstellen: list[Nullstelle]
    ) -> ExactNullstellenListe:
        """
        Kombiniert Nullstellen von allen Faktoren mit intelligenter Multiplicity-Berechnung.

        Args:
            alle_nullstellen: Liste aller Nullstellen von allen Faktoren

        Returns:
            Kombinierte Liste mit korrekten Vielfachheiten
        """
        if not alle_nullstellen:
            return []

        kombinierte = []

        for aktuelle_nullstelle in alle_nullstellen:
            # Suche nach äquivalenten Nullstellen in der kombinierten Liste
            gefunden = False

            for i, vorhandene_nullstelle in enumerate(kombinierte):
                # Prüfe auf symbolische Gleichheit
                if self._sind_symbolisch_gleich(
                    aktuelle_nullstelle.x, vorhandene_nullstelle.x
                ):
                    # Addiere die Vielfachheiten
                    neue_multiplicitaet = (
                        vorhandene_nullstelle.multiplicitaet
                        + aktuelle_nullstelle.multiplicitaet
                    )

                    # Ersetze die vorhandene Nullstelle mit neuer Vielfachheit
                    kombinierte[i] = Nullstelle(
                        x=vorhandene_nullstelle.x,
                        multiplicitaet=neue_multiplicitaet,
                        exakt=vorhandene_nullstelle.exakt and aktuelle_nullstelle.exakt,
                    )
                    gefunden = True
                    break

            if not gefunden:
                # Füge neue Nullstelle hinzu
                kombinierte.append(aktuelle_nullstelle)

        return kombinierte


class SummeFunktion(StrukturierteFunktion):
    """Repräsentiert eine Summe von Funktionen mit typisierten Summanden."""

    def __init__(self, eingabe, struktur_info=None):
        super().__init__(eingabe, struktur_info)

        # Spezifische Eigenschaften für Summen
        self._summanden = self._komponenten

    @property
    def funktionstyp(self) -> str:
        """Gibt den Funktionstyp als String zurück"""
        return "summe"

    @property
    def summanden(self) -> list[Funktion]:
        """Gibt die typisierten Summanden der Summe zurück."""
        return self._summanden

    @property
    def summand1(self) -> Funktion | None:
        """Gibt den ersten Summanden zurück."""
        return self._summanden[0] if len(self._summanden) > 0 else None

    @property
    def summand2(self) -> Funktion | None:
        """Gibt den zweiten Summanden zurück."""
        return self._summanden[1] if len(self._summanden) > 1 else None

    def nullstellen(
        self, real: bool = True, runden: int | None = None
    ) -> ExactNullstellenListe:
        """
        Berechnet Nullstellen für Summenfunktionen mit verbessertem Ansatz.

        Strategie:
        1. Versuche Sympy's solve() direkt auf die Summe
        2. Bei Schwierigkeiten: Vereinfache die gesamte Summe und versuche es erneut
        3. Für trigonometrische Funktionen: Nutze solveset für allgemeine Lösungen
        4. Akzeptiere, dass einige Summen nicht exakt lösbar sind

        Args:
            real: Nur reelle Nullstellen zurückgeben (Standard: True)
            runden: Anzahl Dezimalstellen zum Runden (optional)

        Returns:
            Liste der gefundenen Nullstellen oder leere Liste
        """
        # Strategie 1: Sympy solve() direkt versuchen (aber nicht für trigonometrische Funktionen)
        try:
            # Überspringe trigonometrische Funktionen - die werden später mit solveset behandelt
            term_str = str(self.term_sympy).lower()
            if not any(func in term_str for func in ["sin", "cos", "tan"]):
                lösungen = solve(self.term_sympy, self._variable_symbol)
                if lösungen:
                    # Filtere reelle Lösungen wenn gewünscht
                    ergebnisse = []
                    for lösung in lösungen:
                        if not real or (hasattr(lösung, "is_real") and lösung.is_real):
                            ergebnisse.append(Nullstelle(x=lösung, exakt=True))
                    if ergebnisse:
                        return ergebnisse
        except Exception:
            # Bei Fehlern gehe zur nächsten Strategie
            pass

        # Strategie 2: Vereinfache die Summe und versuche es erneut (aber nicht für trigonometrische Funktionen)
        try:
            # Überspringe trigonometrische Funktionen - die werden später mit solveset behandelt
            term_str = str(self.term_sympy).lower()
            if not any(func in term_str for func in ["sin", "cos", "tan"]):
                vereinfachter_term = simplify(self.term_sympy)
                lösungen = solve(vereinfachter_term, self._variable_symbol)
                if lösungen:
                    # Filtere reelle Lösungen wenn gewünscht
                    ergebnisse = []
                    for lösung in lösungen:
                        if not real or (hasattr(lösung, "is_real") and lösung.is_real):
                            ergebnisse.append(Nullstelle(x=lösung, exakt=True))
                    if ergebnisse:
                        return ergebnisse
        except Exception:
            # Bei Fehlern gehe zur nächsten Strategie
            pass

        # Strategie 3: Für trigonometrische Funktionen - nutze solveset für bessere Lösungen
        try:
            term_str = str(self.term_sympy).lower()
            if any(func in term_str for func in ["sin", "cos", "tan"]):
                # Nutze solveset für bessere trigonometrische Lösungen
                allgemeine_lösungen = solveset(
                    self.term_sympy, self._variable_symbol, domain=S.Reals
                )

                ergebnisse = []

                # Hilfsfunktion zur Extraktion konkreter Lösungen aus ImageSet
                from sympy import pi

                def extrahiere_lösungen_aus_imageset(
                    image_set, x_bereich=(-2 * pi, 2 * pi)
                ):
                    """Extrahiert konkrete Lösungen aus einem ImageSet."""
                    if not hasattr(image_set, "lamda"):
                        return []

                    lambda_expr = image_set.lamda
                    n_symbol = lambda_expr.variables[0]  # Normalerweise _n
                    lösungen = []

                    # Probiere verschiedene n-Werte für Schulmathematik-Bereich
                    for n_val in range(-3, 4):
                        try:
                            lösung = lambda_expr.expr.subs(n_symbol, n_val)

                            # Prüfe, ob die Lösung im gewünschten Bereich liegt
                            if hasattr(lösung, "evalf"):
                                lösung_num = float(lösung.evalf())
                                if x_bereich[0] <= lösung_num <= x_bereich[1]:
                                    lösungen.append(lösung)
                            else:
                                # Symbolische Lösungen immer hinzufügen
                                lösungen.append(lösung)
                        except Exception:
                            continue

                    return lösungen

                # Verarbeite verschiedene solveset-Ergebnistypen
                try:
                    from sympy import ImageSet, Union

                    print(f"DEBUG: Verarbeite solveset-Ergebnis...")
                    if isinstance(allgemeine_lösungen, Union):
                        print(
                            f"DEBUG: Ist Union mit {len(allgemeine_lösungen.args)} Args"
                        )
                        # Behandle Union von mehreren ImageSets
                        for i, arg in enumerate(allgemeine_lösungen.args):
                            print(f"DEBUG: Arg {i}: {arg} (Typ: {type(arg)})")
                            if isinstance(arg, ImageSet):
                                print(f"DEBUG: Verarbeite ImageSet...")
                                lösungen = extrahiere_lösungen_aus_imageset(arg)
                                print(f"DEBUG: Gefundene Lösungen: {lösungen}")
                                for lösung in lösungen:
                                    if hasattr(lösung, "is_real") and lösung.is_real:
                                        ergebnisse.append(
                                            Nullstelle(x=lösung, exakt=True)
                                        )
                    elif isinstance(allgemeine_lösungen, ImageSet):
                        print(f"DEBUG: Ist einzelnes ImageSet")
                        # Einzelnes ImageSet
                        lösungen = extrahiere_lösungen_aus_imageset(allgemeine_lösungen)
                        for lösung in lösungen:
                            if hasattr(lösung, "is_real") and lösung.is_real:
                                ergebnisse.append(Nullstelle(x=lösung, exakt=True))
                except Exception as e:
                    print(f"DEBUG: Fehler bei der Verarbeitung: {e}")
                    import traceback

                    traceback.print_exc()

                if ergebnisse:
                    # Entferne Duplikate mit vereinfachtem Vergleich
                    vereinfachte_ergebnisse = []
                    seen = set()
                    for ergebnis in ergebnisse:
                        # Vereinfache und erstelle Schlüssel
                        vereinfacht = simplify(ergebnis.x)
                        schlüssel = str(vereinfacht)
                        if schlüssel not in seen:
                            seen.add(schlüssel)
                            # Ersetze mit vereinfachter Version
                            vereinfachte_ergebnisse.append(
                                Nullstelle(x=vereinfacht, exakt=True)
                            )

                    if vereinfachte_ergebnisse:
                        # Sortiere für bessere Darstellung
                        try:
                            from sympy import pi

                            vereinfachte_ergebnisse.sort(
                                key=lambda n: float(n.x.evalf())
                            )
                        except:
                            pass

                        return vereinfachte_ergebnisse
        except Exception as e:
            print(f"DEBUG: Exception in Strategy 3: {e}")
            import traceback

            traceback.print_exc()
            # Bei Fehlern gehe zur letzten Strategie
            pass

        # Strategie 4: Keine Lösung gefunden - akzeptiere dies und gib leere Liste zurück
        return []

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
    def funktionstyp(self) -> str:
        """Gibt den Funktionstyp als String zurück"""
        return "quotient"

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

            # Wenn der Nenner bereits eine Funktion ist, hole nullstellen als Property
            if hasattr(self.nenner, "nullstellen"):
                if callable(self.nenner.nullstellen):
                    self._cache["polstellen"] = self.nenner.nullstellen()
                else:
                    # nullstellen ist eine Property, konvertiere zu float-Werten
                    nullstellen_objekte = self.nenner.nullstellen
                    self._cache["polstellen"] = [
                        float(n.x) for n in nullstellen_objekte
                    ]
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

    @preserve_exact_types
    def nullstellen(
        self, real: bool = True, runden: int | None = None
    ) -> ExactNullstellenListe:
        """
        Berechnet die Nullstellen der Quotientenfunktion.

        Für f(x) = Z(x)/N(x) gilt: f(x) = 0 ⇔ Z(x) = 0 und N(x) ≠ 0
        Die Nullstellen sind also die Zähler-Nullstellen, die keine Polstellen sind.

        Args:
            real: Nur reelle Nullstellen zurückgeben (Standard: True)
            runden: Anzahl Dezimalstellen zum Runden (optional)

        Returns:
            Liste der gültigen Nullstellen als SymPy-Ausdrücke

        Examples:
            >>> f = QuotientFunktion([GanzrationaleFunktion([1, -1]), GanzrationaleFunktion([1, -2])])
            >>> # (x-1)/(x-2) hat Nullstelle bei x=1 (Polstelle bei x=2)
            >>> nullstellen = f.nullstellen()  # [1]
        """
        try:
            if self.zaehler is None:
                raise ValueError("QuotientFunktion hat keinen gültigen Zähler")

            # Hole Zähler-Nullstellen
            if hasattr(self.zaehler, "nullstellen") and callable(
                self.zaehler.nullstellen
            ):
                zaehler_nullstellen = self.zaehler.nullstellen(real=real, runden=runden)
            else:
                # Fallback: Leere Liste wenn keine Nullstellen ermittelbar
                zaehler_nullstellen = []

            # Hole Polstellen (Nenner-Nullstellen)
            try:
                polstellen = self.polstellen()
            except Exception:
                polstellen = []

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

            # Validiere die Ergebnisse
            validate_exact_results(gueltige_nullstellen, "Quotienten-Nullstellen")

            return gueltige_nullstellen

        except Exception as e:
            raise ValueError(
                f"Fehler bei der Nullstellenberechnung für Quotientenfunktion: {str(e)}\n"
                "Tipp: Überprüfe, ob Zähler und Nenner korrekt definiert sind."
            ) from e

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
    def funktionstyp(self) -> str:
        """Gibt den Funktionstyp als String zurück"""
        return "komposition"

    @property
    def basis(self) -> Funktion:
        """Gibt die typisierte Basis zurück."""
        return self._basis

    @property
    def exponent(self) -> Funktion:
        """Gibt den typisierten Exponenten zurück."""
        return self._exponent

    @preserve_exact_types
    def nullstellen(
        self, real: bool = True, runden: int | None = None
    ) -> ExactNullstellenListe:
        """
        Berechnet die Nullstellen der Kompositionsfunktion.

        Für f(x)^g(x) = 0 gilt: f(x)^g(x) = 0 ⇔ f(x) = 0 (wenn g(x) definiert ist)

        Args:
            real: Nur reelle Nullstellen zurückgeben (Standard: True)
            runden: Anzahl Dezimalstellen zum Runden (optional)

        Returns:
            Liste der Nullstellen als SymPy-Ausdrücke

        Examples:
            >>> f = KompositionFunktion([GanzrationaleFunktion([1, -1]), GanzrationaleFunktion([2])])
            >>> # (x-1)² hat Nullstelle bei x=1
            >>> nullstellen = f.nullstellen()  # [1]
        """
        try:
            if self.basis is None:
                raise ValueError("KompositionFunktion hat keine gültige Basis")

            # Für f(x)^g(x) = 0 gilt nur f(x) = 0 (wenn g(x) definiert ist)
            # Wir brauchen also nur die Nullstellen der Basisfunktion
            if hasattr(self.basis, "nullstellen") and callable(self.basis.nullstellen):
                basis_nullstellen = self.basis.nullstellen(real=real, runden=runden)
            else:
                # Fallback: Leere Liste wenn keine Nullstellen ermittelbar
                basis_nullstellen = []

            # TODO: Später erweitern für echte Kompositionen f(g(x))
            # Für f(g(x)) = 0:
            # 1. Löse f(u) = 0 ⇒ u₁, u₂, ..., uₙ
            # 2. Für jedes uᵢ: Löse g(x) = uᵢ
            # 3. Kombiniere alle Lösungen

            # Validiere die Ergebnisse
            validate_exact_results(basis_nullstellen, "Kompositions-Nullstellen")

            return basis_nullstellen

        except Exception as e:
            raise ValueError(
                f"Fehler bei der Nullstellenberechnung für Kompositionsfunktion: {str(e)}\n"
                "Tipp: Für Kompositionen f(g(x)) = 0, löse zuerst f(u) = 0, dann g(x) = u."
            ) from e

    def __str__(self):
        return f"Komposition({self.basis}, {self.exponent})"
