"""
Robustes Typ-System für die Schul-Analysis Framework mit SymPy-Integration.

Dieses Modul definiert präzise Typen für symbolische Mathematik im Schulunterricht,
mit Fokus auf Typsicherheit, pädagogische Klarheit und deutsche Fachsprache.
"""

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import (
    Any,
    Generic,
    Protocol,
    TypeGuard,
    TypeVar,
    overload,
)

import sympy as sp

# Import Self - wenn nicht verfügbar, überspringen wir die Self-typisierten Protokolle
_SELF_AVAILABLE = False
try:
    from typing import Self

    _SELF_AVAILABLE = True
except ImportError:
    try:
        from typing import Self

        _SELF_AVAILABLE = True
    except ImportError:
        # Self ist nicht verfügbar, wir definieren es nicht
        pass

# =============================================================================
# GRUNDLEGENDE MATHEMATISCHE TYPEVARIABLEN
# =============================================================================

# Core mathematical type variables with proper bounds
T_Expr = TypeVar("T_Expr", bound=sp.Expr)  # Generischer SymPy-Ausdruck
T_Num = TypeVar("T_Num", bound=sp.Number)  # Numerische SymPy-Werte
T_Func = TypeVar(
    "T_Func", bound=Any
)  # Funktionstyp (vorläufig Any wegen Forward-Reference)

# Specific mathematical type variables
T_Poly = TypeVar("T_Poly", bound=sp.Poly)  # Polynom-Typ
T_Trigo = TypeVar("T_Trigo", bound=sp.Expr)  # Trigonometrische Ausdrücke
T_Exp = TypeVar("T_Exp", bound=sp.Expr)  # Exponentielle Ausdrücke

# =============================================================================
# VALIDATIONSKONSTANTEN (STATT HARDCODED STRINGS)
# =============================================================================

# Validierungstypen für validate_function_result()
VALIDATION_EXACT = "exact"  # Exakte SymPy-Ausdrücke
VALIDATION_SYMBOLIC = "symbolic"  # Symbolische Ausdrücke ohne freie Variablen
VALIDATION_NUMERIC = "numeric"  # Exakte numerische Werte
VALIDATION_INEXACT = "inexact"  # Approximative Werte

# =============================================================================
# ENUMS FÜR MATHEMATISCHE KONZEPTE (STATT MAGIC STRINGS)
# =============================================================================


class ExtremumTyp(Enum):
    """Typen von Extremstellen für präzise Typisierung."""

    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"
    SATTELPUNKT = "Sattelpunkt"


class WendepunktTyp(Enum):
    """Typen von Wendepunkten für präzise Typisierung."""

    WENDEPUNKT = "Wendepunkt"
    SATTelpunkt = "Sattelpunkt"  # Kann sowohl Extremum als auch Wendepunkt sein


class PolstellenTyp(Enum):
    """Typen von Polstellen für präzise Typisierung."""

    POLE = "Pol"
    DEFINITIONSLÜCKE = "Definitionslosigkeit"
    UNENDLICHKEITSTELLE = "Unendlichkeitsstelle"


class AsymptotenTyp(Enum):
    """Typen von Asymptoten für präzise Typisierung."""

    WAAGERECHT = "Waagerechte Asymptote"
    SENKRECHT = "Senkrechte Asymptote"
    SCHIEG = "Schiefe Asymptote"
    KURVENASYMPTOTE = "Kurvenasymptote"


# =============================================================================
# DATACLASSES FÜR STRUKTURIERTE ERGEBNISSE
# =============================================================================


@dataclass(frozen=True)
class Nullstelle:
    """Präzise Typisierung für Nullstellen mit zusätzlichen Informationen."""

    x: T_Expr  # x-Koordinate der Nullstelle
    multiplicitaet: int = 1  # Vielfachheit der Nullstelle
    exakt: bool = True  # Ob exakt berechnet wurde

    def __str__(self) -> str:
        if self.multiplicitaet > 1:
            return f"x = {self.x} (Vielfachheit: {self.multiplicitaet})"
        return f"x = {self.x}"


@dataclass(frozen=True)
class Extremum:
    """Präzise Typisierung für Extremstellen mit vollständigen Informationen."""

    x: T_Expr  # x-Koordinate
    y: T_Expr  # y-Koordinate
    typ: ExtremumTyp  # Art des Extremums
    exakt: bool = True  # Ob exakt berechnet wurde

    def __str__(self) -> str:
        return f"{self.typ.value} bei P({self.x}|{self.y})"


@dataclass(frozen=True)
class Wendepunkt:
    """Präzise Typisierung für Wendepunkte mit vollständigen Informationen."""

    x: T_Expr  # x-Koordinate
    y: T_Expr  # y-Koordinate
    typ: WendepunktTyp = WendepunktTyp.WENDEPUNKT
    exakt: bool = True  # Ob exakt berechnet wurde

    def __str__(self) -> str:
        return f"{self.typ.value} bei P({self.x}|{self.y})"


@dataclass(frozen=True)
class StationaereStelle:
    """Präzise Typisierung für stationäre Stellen mit vollständigen Informationen."""

    x: T_Expr  # x-Koordinate
    typ: ExtremumTyp  # Art der stationären Stelle (Minimum, Maximum, Sattelpunkt)
    exakt: bool = True  # Ob exakt berechnet wurde

    def __str__(self) -> str:
        return f"Stationäre Stelle bei x = {self.x} ({self.typ.value})"


@dataclass(frozen=True)
class Sattelpunkt:
    """Präzise Typisierung für Sattelpunkte mit vollständigen Informationen."""

    x: T_Expr  # x-Koordinate
    y: T_Expr  # y-Koordinate
    exakt: bool = True  # Ob exakt berechnet wurde

    def __str__(self) -> str:
        return f"Sattelpunkt bei P({self.x}|{self.y})"


@dataclass(frozen=True)
class Polstelle:
    """Präzise Typisierung für Polstellen mit zusätzlichen Informationen."""

    x: T_Expr  # x-Koordinate der Polstelle
    typ: PolstellenTyp = PolstellenTyp.POLE
    ordnung: int = 1  # Ordnung der Polstelle
    asymptote: str | None = None  # Gleichung der Asymptote

    def __str__(self) -> str:
        return f"{self.typ.value} bei x = {self.x}"


@dataclass(frozen=True)
class Asymptote:
    """Präzise Typisierung für Asymptoten mit vollständigen Informationen."""

    typ: AsymptotenTyp
    gleichung: T_Expr  # Gleichung der Asymptote
    bedingung: str  # Bedingung (z.B. "x → ∞" oder "x → 2+")

    def __str__(self) -> str:
        return f"{self.typ.value}: {self.gleichung} für {self.bedingung}"


@dataclass(frozen=True)
class Schnittpunkt:
    """Präzise Typisierung für Schnittpunkte zwischen zwei Funktionen."""

    x: T_Expr  # x-Koordinate des Schnittpunkts
    y: T_Expr  # y-Koordinate des Schnittpunkts
    exakt: bool = True  # Ob exakt berechnet wurde

    def __str__(self) -> str:
        return f"Schnittpunkt bei P({self.x}|{self.y})"


@dataclass(frozen=True)
class IntegralResult:
    """Präzise Typisierung für Integral-Ergebnisse."""

    stammfunktion: T_Expr  # Die Stammfunktion
    wert: T_Expr | None = None  # Numerischer Wert bei bestimmtem Integral
    grenzen: tuple[T_Expr, T_Expr] | None = None  # Integrationsgrenzen

    def __str__(self) -> str:
        if self.wert is not None and self.grenzen is not None:
            return f"∫[{self.grenzen[0]}, {self.grenzen[1]}] = {self.wert}"
        return f"∫ = {self.stammfunktion}"


# =============================================================================
# ERWEITERTE LISTEN-TYPEN MIT PRÄZISER TYPISIERUNG
# =============================================================================

# Präzise Listen-Typen statt list[Any]
ExactNullstellenListe = list[Nullstelle]
ExtremaListe = list[Extremum]
WendepunkteListe = list[Wendepunkt]
StationaereStellenListe = list[StationaereStelle]
SattelpunkteListe = list[Sattelpunkt]
PolstellenListe = list[Polstelle]
AsymptotenListe = list[Asymptote]
SchnittpunkteListe = list[Schnittpunkt]

# Mathematische Punktelisten für graphische Darstellung
PunktListe = list[tuple[T_Expr, T_Expr]]  # (x, y) Koordinaten
StützstellenListe = list[tuple[float, float]]  # Für numerische Berechnungen

# Koeffizienten-Typen für Polynome
PolynomKoeffizienten = list[int | float | sp.Integer | sp.Rational]

# =============================================================================
# SPEZIALISIERTE FUNKTIONSTYPEN
# =============================================================================

# Typen für mathematische Funktionen mit präzisen Signaturen
MathematischeFunktion = Callable[[T_Expr], T_Expr]
AnalyseFunktion = Callable[
    [T_Func], ExactNullstellenListe | ExtremaListe | WendepunkteListe
]
ParameterFunktion = Callable[[T_Func, dict[str, Any]], T_Func]

# Typen für pädagogische Funktionen
SchrittweiseFunktion = Callable[
    ..., list[tuple[str, Any]]
]  # Schritt-für-Schritt-Berechnungen
InteraktiveFunktion = Callable[..., tuple[T_Expr, str]]  # Mit Erklärungen

# =============================================================================
# PROTOKOLLE MIT STARKER TYPSICHERHEIT
# =============================================================================


class Ableitbar(Protocol[T_Expr]):
    """Protokoll für ableitbare mathematische Objekte mit starker Typsicherheit."""

    @overload
    def ableitung(self) -> Self: ...

    @overload
    def ableitung(self, ordnung: int) -> Self: ...

    def ableitung(self, ordnung: int = 1) -> Self:
        """
        Berechnet die Ableitung mit exakten SymPy-Ergebnissen.

        Args:
            ordnung: Ordnung der Ableitung (Standard: 1)

        Returns:
            Abgeleitetes Objekt vom gleichen Typ
        """
        ...


class Integrierbar(Protocol[T_Expr]):
    """Protokoll für integrierbare mathematische Objekte mit starker Typsicherheit."""

    @overload
    def integral(self) -> IntegralResult: ...

    @overload
    def integral(self, grenzen: tuple[T_Expr, T_Expr]) -> IntegralResult: ...

    def integral(self, grenzen: tuple[T_Expr, T_Expr] | None = None) -> IntegralResult:
        """
        Berechnet das Integral mit exakten SymPy-Ergebnissen.

        Args:
            grenzen: Optionale Integrationsgrenzen (a, b)

        Returns:
            Integral-Ergebnis mit Stammfunktion und ggf. numerischem Wert
        """
        ...


class Analysierbar(Protocol[T_Expr]):
    """Protokoll für analysierbare mathematische Objekte mit starker Typsicherheit."""

    def nullstellen(self, real: bool = True) -> ExactNullstellenListe:
        """
        Berechnet Nullstellen mit exakten SymPy-Ergebnissen.

        Args:
            real: Nur reelle Nullstellen berechnen (Standard: True)

        Returns:
            Liste der Nullstellen mit Vielfachheit
        """
        ...

    def extrema(self) -> ExtremaListe:
        """
        Berechnet Extremstellen mit exakten SymPy-Ergebnissen.

        Returns:
            Liste der Extremstellen mit Art und Koordinaten
        """
        ...

    def wendepunkte(self) -> WendepunkteListe:
        """
        Berechnet Wendepunkte mit exakten SymPy-Ergebnissen.

        Returns:
            Liste der Wendepunkte mit Art und Koordinaten
        """
        ...


class Visualisierbar(Protocol[T_Expr]):
    """Protokoll für visualisierbare mathematische Objekte."""

    @overload
    def zeige_funktion(self) -> Any: ...

    @overload
    def zeige_funktion(self, x_bereich: tuple[float, float]) -> Any: ...

    def zeige_funktion(self, x_bereich: tuple[float, float] | None = None) -> Any:
        """
        Erstellt eine Visualisierung der Funktion.

        Args:
            x_bereich: Optionaler x-Bereich für die Darstellung

        Returns:
            Visualisierungsobjekt (z.B. Plotly-Figure)
        """
        ...


# =============================================================================
# TYPE GUARDS FÜR LAUFZEIT-TYPPRÜFUNG
# =============================================================================


def is_exact_sympy_expr(expr: Any) -> TypeGuard[T_Expr]:
    """
    Type Guard für exakte SymPy-Ausdrücke ohne numerische Approximation.

    Args:
        expr: Zu überprüfender Ausdruck

    Returns:
        True wenn es ein exakter SymPy-Ausdruck ist
    """
    if not isinstance(expr, sp.Expr):
        return False
    # Prüfe, ob der Ausdruck keine Float-Approximationen enthält
    return not any(isinstance(atom, sp.Float) for atom in expr.atoms(sp.Number))


def is_exact_schnittpunkt(schnittpunkt: Any) -> TypeGuard[Schnittpunkt]:
    """
    Type Guard für exakte Schnittpunkte ohne numerische Approximation.

    Args:
        schnittpunkt: Zu überprüfender Schnittpunkt

    Returns:
        True wenn der Schnittpunkt exakte Koordinaten hat
    """
    if not isinstance(schnittpunkt, Schnittpunkt):
        return False
    # Prüfe beide Koordinaten auf Exaktheit
    return is_exact_sympy_expr(schnittpunkt.x) and is_exact_sympy_expr(schnittpunkt.y)


def is_exact_numeric(expr: Any) -> TypeGuard[T_Num]:
    """
    Type Guard für exakte numerische SymPy-Werte.

    Args:
        expr: Zu überprüfender Wert

    Returns:
        True wenn es ein exakter numerischer Wert ist
    """
    return isinstance(expr, (sp.Integer, sp.Rational)) and not isinstance(
        expr, sp.Float
    )


def is_polynomial(expr: Any) -> TypeGuard[sp.Poly]:
    """
    Type Guard für Polynom-Ausdrücke.

    Args:
        expr: Zu überprüfender Ausdruck

    Returns:
        True wenn es ein Polynom ist
    """
    return isinstance(expr, sp.Poly)


def is_trigonometric(expr: Any) -> TypeGuard[T_Trigo]:
    """
    Type Guard für trigonometrische Ausdrücke.

    Args:
        expr: Zu überprüfender Ausdruck

    Returns:
        True wenn es ein trigonometrischer Ausdruck ist
    """
    if not isinstance(expr, sp.Expr):
        return False
    trig_functions = (sp.sin, sp.cos, sp.tan, sp.cot, sp.sec, sp.csc)
    return any(func in expr.atoms(sp.Function) for func in trig_functions)


def is_exponential(expr: Any) -> TypeGuard[T_Exp]:
    """
    Type Guard für exponentielle Ausdrücke.

    Args:
        expr: Zu überprüfender Ausdruck

    Returns:
        True wenn es ein exponentieller Ausdruck ist
    """
    if not isinstance(expr, sp.Expr):
        return False
    exp_functions = (sp.exp, sp.log, sp.ln)
    return any(func in expr.atoms(sp.Function) for func in exp_functions)


# =============================================================================
# VALIDIERUNGSFUNKTIONEN FÜR PÄDAGOGISCHE ANWENDUNGEN
# =============================================================================


def validate_exact_results(results: list[Any], analysis_type: str) -> bool:
    """
    Validiert, dass Analyse-Ergebnisse exakt sind (keine Float-Approximationen).

    Args:
        results: Zu validierende Ergebnisse
        analysis_type: Art der Analyse (z.B. "Nullstellen", "Extrema")

    Returns:
        True wenn alle Ergebnisse exakt sind

    Raises:
        ValueError: Wenn inexakte Ergebnisse gefunden werden
    """
    # Spezialbehandlung für Schnittpunkte
    if analysis_type == "Schnittpunkte":
        validations = [is_exact_schnittpunkt(result) for result in results]
        if not all(validations):
            raise ValueError(
                f"Die {analysis_type}-Analyse sollte exakte Ergebnisse liefern, "
                f"aber es wurden approximative Ergebnisse gefunden. "
                f"Verwenden Sie symbolische Berechnungen für genaue Ergebnisse."
            )
    else:
        # Standardbehandlung für andere Analyse-Typen
        validations = [is_exact_sympy_expr(result) for result in results]
        if not all(validations):
            raise ValueError(
                f"Die {analysis_type}-Analyse sollte exakte Ergebnisse liefern, "
                f"aber es wurden approximative Ergebnisse gefunden. "
                f"Verwenden Sie symbolische Berechnungen für genaue Ergebnisse."
            )
    return True


def validate_function_result(result: Any, expected_type: str) -> bool:
    """
    Validiert, dass ein Funktionsergebnis dem erwarteten Typ entspricht.

    Args:
        result: Zu validierendes Ergebnis
        expected_type: Erwarteter Typ ("exact", "symbolic", "numeric", "inexact")

    Returns:
        True wenn das Ergebnis dem Typ entspricht

    Raises:
        ValueError: Bei unerwartetem Typ
    """
    validators = {
        VALIDATION_EXACT: is_exact_sympy_expr,
        VALIDATION_SYMBOLIC: lambda x: isinstance(x, sp.Expr) and not x.free_symbols,
        VALIDATION_NUMERIC: is_exact_numeric,
        VALIDATION_INEXACT: lambda x: isinstance(x, (sp.Float, float)),
    }

    if expected_type not in validators:
        raise ValueError(f"Unbekannter erwarteter Typ: {expected_type}")

    if not validators[expected_type](result):
        actual_type = (
            "numerisch"
            if is_exact_numeric(result)
            else "symbolisch"
            if isinstance(result, sp.Expr)
            else "unbekannt"
        )
        raise ValueError(
            f"Erwarteter Typ: {expected_type}, "
            f"aber es wurde ein {actual_type}es Ergebnis gefunden: {result}"
        )

    return True


# =============================================================================
# DEKORATOREN FÜR LAUFZEIT-TYPPRÜFUNG
# =============================================================================


def preserve_exact_types(func: Callable) -> Callable:
    """
    Dekorator, der sicherstellt, dass Funktionen exakte Typen beibehalten.

    Args:
        func: Zu dekorierende Funktion

    Returns:
        Dekorierte Funktion mit Typsicherheit
    """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        # Prüfe, ob das Ergebnis exakt ist
        if isinstance(result, sp.Expr) and not is_exact_sympy_expr(result):
            func_name = getattr(func, "__name__", str(func))
            raise ValueError(
                f"Die Funktion {func_name} sollte exakte Ergebnisse liefern, "
                f"aber es wurde ein approximatives Ergebnis erzeugt: {result}"
            )

        return result

    return wrapper


def validate_analysis_results(analysis_type: str):
    """
    Dekorator für die Validierung von Analyse-Ergebnissen.

    Args:
        analysis_type: Art der Analyse

    Returns:
        Dekorator-Funktion
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Validiere, dass es sich um eine Liste handelt
            if not isinstance(result, list):
                raise ValueError(
                    f"Die {analysis_type}-Analyse sollte eine Liste zurückgeben, "
                    f"aber es wurde {type(result)} zurückgegeben"
                )

            # Validiere, dass alle Elemente exakt sind
            if analysis_type == "Schnittpunkte":
                # Spezialbehandlung für Schnittpunkte
                if not all(is_exact_schnittpunkt(item) for item in result):
                    raise ValueError(
                        f"Die {analysis_type}-Analyse sollte exakte Ergebnisse liefern, "
                        f"aber es wurden approximative Ergebnisse gefunden"
                    )
            else:
                # Standardbehandlung für andere Analyse-Typen
                if not all(
                    is_exact_sympy_expr(item) for item in result if hasattr(item, "x")
                ):
                    raise ValueError(
                        f"Die {analysis_type}-Analyse sollte exakte Ergebnisse liefern, "
                        f"aber es wurden approximative Ergebnisse gefunden"
                    )

            return result

        return wrapper

    return decorator


# =============================================================================
# GENERISCHE HILFSKLASSEN
# =============================================================================


class MathFunctionBase(Generic[T_Expr]):
    """Basisklasse für mathematische Funktionen mit Typ-Erhaltung."""

    def __init__(self, expression: T_Expr) -> None:
        self.expression = expression

    def ableiten(self, ordnung: int = 1) -> T_Expr:
        """Berechnet die Ableitung mit Typerhaltung."""
        return self.expression.diff(ordnung)

    def auswerten(self, punkt: float | sp.Expr) -> T_Expr:
        """Wertet die Funktion an einem Punkt aus mit Typerhaltung."""
        return self.expression.subs(self.expression.free_symbols.pop(), punkt)


class AnalyseResultBase(Generic[T_Expr]):
    """Basisklasse für Analyse-Ergebnisse mit Typ-Erhaltung."""

    def __init__(self, ergebnis: T_Expr, art: str) -> None:
        self.ergebnis = ergebnis
        self.art = art

    def get_ergebnis(self) -> T_Expr:
        """Gibt das Ergebnis zurück."""
        return self.ergebnis

    def get_art(self) -> str:
        """Gibt die Art der Analyse zurück."""
        return self.art


# =============================================================================
# TYPE ALIASES FÜR RÜCKWÄRTSKOMPATIBILITÄT
# =============================================================================

# Alte Typ-Aliase für Kompatibilität (werden in Zukunft deprecated)
ExactResultList = list[T_Expr]
ExactSymPyExpr = T_Expr
ExactNumericResult = T_Num
SymbolicResult = T_Expr
InexactResult = sp.Float
PositiveExactNumeric = T_Num
NegativeExactNumeric = T_Num

# =============================================================================
# ZUSAMMENFASSUNG DER TYPOLOGIE
# =============================================================================

"""
Dieses Typ-System bietet:

1. **Präzise Typsicherheit**: Statt list[Any] verwenden wir spezifische Typen wie ExactNullstellenListe
2. **Keine Magic Strings**: Enums für ExtremumTyp, WendepunktTyp, etc.
3. **Strukturierte Ergebnisse**: Dataclasses mit vollständigen Informationen
4. **Starke Protokolle**: Mit TypeVars und Überladungen für Compile-Time-Sicherheit
5. **Type Guards**: Für Laufzeit-Typprüfung mit TypeGuard
6. **Pädagogische Validierung**: Deutsche Fehlermeldungen und Erklärungen
7. **Rückwärtskompatibilität**: Alte Typ-Aliase für schrittweise Migration

Die Typen sind speziell auf die Bedürfnisse des Mathematikunterrichts zugeschnitten
und unterstützen sowohl die exakte symbolische Berechnung als auch die pädagogische
Vermittlung mathematischer Konzepte.
"""
