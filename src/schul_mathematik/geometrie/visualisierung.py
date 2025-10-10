"""
Visualisierungsfunktionen für das Geometrie-Modul

Integration mit Plotly für interaktive geometrische Graphen in 2D und 3D
"""

import numpy as np
import plotly.graph_objects as go
import sympy as sp
from sympy import lambdify

from ..gemeinsam import *
from .punkte_geraden import Punkt, Gerade, Ebene


def zeichne_punkt_2d(punkt: Punkt, farbe: str = "red", groesse: int = 10) -> go.Figure:
    """Zeichnet einen Punkt im 2D-Koordinatensystem

    Args:
        punkt: Punkt-Objekt
        farbe: Farbe des Punktes
        groesse: Größe des Punktes

    Returns:
        Plotly Figure-Objekt
    """
    if punkt.dimension != 2:
        raise ValueError("Punkt muss 2-dimensional sein")

    fig = go.Figure()

    # Punkt hinzufügen
    fig.add_trace(
        go.Scatter(
            x=[punkt.koordinaten[0]],
            y=[punkt.koordinaten[1]],
            mode="markers",
            name=str(punkt),
            marker=dict(color=farbe, size=groesse),
            text=str(punkt),
            textposition="top center",
        )
    )

    # Achsen konfigurieren
    fig.update_layout(
        title=f"Punkt {punkt.name}",
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="lightgray",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="lightgray",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
        ),
        width=600,
        height=600,
    )

    return fig


def zeichne_gerade_2d(
    gerade: Gerade,
    x_bereich: tuple[float, float] = (-10, 10),
    farbe: str = "blue",
    aufpunkt_farbe: str = "red",
) -> go.Figure:
    """Zeichnet eine Gerade im 2D-Koordinatensystem

    Args:
        gerade: Geraden-Objekt
        x_bereich: x-Bereich für die Darstellung
        farbe: Farbe der Geraden
        aufpunkt_farbe: Farbe des Aufpunktes

    Returns:
        Plotly Figure-Objekt
    """
    if gerade.dimension != 2:
        raise ValueError("Gerade muss 2-dimensional sein")

    # x-Werte für die Darstellung
    x_vals = np.linspace(x_bereich[0], x_bereich[1], 100)

    # Richtungsvektor und Aufpunkt extrahieren
    A = gerade.aufpunkt
    V = gerade.richtungsvektor

    # Parametrische Form: X = A + r·V
    # Für die Darstellung: x = A_x + r·V_x, y = A_y + r·V_y
    # Auflösen nach r: r = (x - A_x) / V_x (wenn V_x ≠ 0)

    y_vals = []
    for x in x_vals:
        if abs(V.koordinaten[0]) > 1e-10:  # V_x ≠ 0
            r = (x - A.koordinaten[0]) / V.koordinaten[0]
            y = A.koordinaten[1] + r * V.koordinaten[1]
        elif abs(V.koordinaten[1]) > 1e-10:  # V_y ≠ 0, vertikale Gerade
            # Spezialfall: vertikale Gerade
            y = np.linspace(x_bereich[0], x_bereich[1], 100)[
                50
            ]  # Mittlere y-Koordinate
        else:
            y = A.koordinaten[1]  # Konstante y-Koordinate
        y_vals.append(y)

    fig = go.Figure()

    # Gerade hinzufügen
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines",
            name=str(gerade),
            line=dict(color=farbe, width=2),
        )
    )

    # Aufpunkt hinzufügen
    fig.add_trace(
        go.Scatter(
            x=[A.koordinaten[0]],
            y=[A.koordinaten[1]],
            mode="markers",
            name=f"Aufpunkt {A.name}",
            marker=dict(color=aufpunkt_farbe, size=8),
        )
    )

    # Achsen konfigurieren
    fig.update_layout(
        title=f"Gerade {gerade.name}",
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="lightgray",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
            range=x_bereich,
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="lightgray",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
        ),
        width=600,
        height=600,
    )

    return fig


def zeichne_zwei_punkte_und_gerade(
    p1: Punkt, p2: Punkt, x_bereich: tuple[float, float] = (-10, 10)
) -> go.Figure:
    """Zeichnet zwei Punkte und die Gerade durch beide Punkte

    Args:
        p1: Erster Punkt
        p2: Zweiter Punkt
        x_bereich: x-Bereich für die Darstellung

    Returns:
        Plotly Figure-Objekt
    """
    if p1.dimension != 2 or p2.dimension != 2:
        raise ValueError("Beide Punkte müssen 2-dimensional sein")

    # Gerade durch die beiden Punkte erstellen
    from .punkte_geraden import gerade_durch_zwei_punkte

    gerade = gerade_durch_zwei_punkte(p1, p2, "g")

    # Gerade zeichnen
    fig = zeichne_gerade_2d(gerade, x_bereich)

    # Zusätzliche Punkte hinzufügen
    fig.add_trace(
        go.Scatter(
            x=[p2.koordinaten[0]],
            y=[p2.koordinaten[1]],
            mode="markers",
            name=str(p2),
            marker=dict(color="green", size=10),
            text=str(p2),
            textposition="top center",
        )
    )

    # Titel anpassen
    fig.update_layout(title=f"Gerade durch {p1.name} und {p2.name}")

    return fig


def zeichne_schnittpunkt_zweier_geraden(
    g1: Gerade, g2: Gerade, x_bereich: tuple[float, float] = (-10, 10)
) -> go.Figure:
    """Zeichnet zwei Geraden und ihren Schnittpunkt

    Args:
        g1: Erste Gerade
        g2: Zweite Gerade
        x_bereich: x-Bereich für die Darstellung

    Returns:
        Plotly Figure-Objekt
    """
    if g1.dimension != 2 or g2.dimension != 2:
        raise ValueError("Beide Geraden müssen 2-dimensional sein")

    # Beide Geraden zeichnen
    fig1 = zeichne_gerade_2d(g1, x_bereich, farbe="blue", aufpunkt_farbe="lightblue")
    fig2 = zeichne_gerade_2d(g2, x_bereich, farbe="red", aufpunkt_farbe="lightcoral")

    # Beide Figuren kombinieren
    fig = go.Figure(data=fig1.data + fig2.data)

    # Schnittpunkt berechnen und zeichnen
    schnittpunkt = g1.schnittpunkt_mit(g2)
    if schnittpunkt:
        fig.add_trace(
            go.Scatter(
                x=[schnittpunkt.koordinaten[0]],
                y=[schnittpunkt.koordinaten[1]],
                mode="markers",
                name=f"Schnittpunkt {schnittpunkt.name}",
                marker=dict(color="green", size=12),
                text=str(schnittpunkt),
                textposition="top center",
            )
        )

    # Layout konfigurieren
    fig.update_layout(
        title=f"Schnittpunkt von {g1.name} und {g2.name}",
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="lightgray",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
            range=x_bereich,
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="lightgray",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
        ),
        width=600,
        height=600,
    )

    return fig


def zeichne_abstand_zwei_punkte(
    p1: Punkt, p2: Punkt, x_bereich: tuple[float, float] = (-10, 10)
) -> go.Figure:
    """Zeichnet zwei Punkte und ihren Abstand

    Args:
        p1: Erster Punkt
        p2: Zweiter Punkt
        x_bereich: x-Bereich für die Darstellung

    Returns:
        Plotly Figure-Objekt
    """
    if p1.dimension != 2 or p2.dimension != 2:
        raise ValueError("Beide Punkte müssen 2-dimensional sein")

    fig = go.Figure()

    # Punkte hinzufügen
    fig.add_trace(
        go.Scatter(
            x=[p1.koordinaten[0]],
            y=[p1.koordinaten[1]],
            mode="markers",
            name=str(p1),
            marker=dict(color="red", size=10),
            text=str(p1),
            textposition="top center",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[p2.koordinaten[0]],
            y=[p2.koordinaten[1]],
            mode="markers",
            name=str(p2),
            marker=dict(color="blue", size=10),
            text=str(p2),
            textposition="top center",
        )
    )

    # Verbindungslinie (Abstand) hinzufügen
    fig.add_trace(
        go.Scatter(
            x=[p1.koordinaten[0], p2.koordinaten[0]],
            y=[p1.koordinaten[1], p2.koordinaten[1]],
            mode="lines",
            name=f"Abstand: {p1.abstand_zu(p2)}",
            line=dict(color="green", width=2, dash="dash"),
        )
    )

    # Mittelpunkt für Abstandsbeschriftung
    mittelpunkt_x = (p1.koordinaten[0] + p2.koordinaten[0]) / 2
    mittelpunkt_y = (p1.koordinaten[1] + p2.koordinaten[1]) / 2

    # Abstand als Text hinzufügen
    abstand = p1.abstand_zu(p2)
    fig.add_trace(
        go.Scatter(
            x=[mittelpunkt_x],
            y=[mittelpunkt_y],
            mode="text",
            text=[f"d = {abstand}"],
            textposition="middle center",
            showlegend=False,
        )
    )

    # Layout konfigurieren
    fig.update_layout(
        title=f"Abstand zwischen {p1.name} und {p2.name}",
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="lightgray",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
            range=x_bereich,
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="lightgray",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="black",
        ),
        width=600,
        height=600,
    )

    return fig
