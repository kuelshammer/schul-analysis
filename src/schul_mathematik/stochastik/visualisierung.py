"""
Visualisierungsfunktionen für das Stochastik-Modul

Integration mit Plotly für interaktive statistische Graphen
"""

import plotly.graph_objects as go
import numpy as np
from sympy import lambdify
import sympy as sp

from .verteilungen import Binomialverteilung, Normalverteilung
from ..gemeinsam import *


def zeichne_binomialverteilung(
    n: int, p: float, k_max: int = None, farbe: str = "blue"
) -> go.Figure:
    """Zeichnet die Binomialverteilung

    Args:
        n: Anzahl der Versuche
        p: Erfolgswahrscheinlichkeit
        k_max: Maximale Anzahl der Erfolge zur Darstellung (Standard: n)
        farbe: Farbe für die Balken

    Returns:
        Plotly Figure-Objekt
    """
    if k_max is None:
        k_max = n

    k_vals = list(range(0, min(k_max, n) + 1))
    probabilities = []

    X = sp.stats.Binomial("X", n, p)
    for k in k_vals:
        prob = float(sp.stats.density(X)(k).evalf())
        probabilities.append(prob)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=k_vals,
            y=probabilities,
            name=f"B({n}, {p})",
            marker_color=farbe,
            opacity=0.7,
        )
    )

    # Erwartungswert als vertikale Linie
    erw = n * p
    fig.add_vline(
        x=erw, line_dash="dash", line_color="red", annotation_text=f"E[X] = {erw:.2f}"
    )

    fig.update_layout(
        title=f"Binomialverteilung B({n}, {p})",
        xaxis_title="k (Anzahl Erfolge)",
        yaxis_title="P(X=k)",
        showlegend=False,
        bargap=0.1,
    )

    return fig


def zeichne_normalverteilung(
    mu: float,
    sigma: float,
    x_bereich: tuple = (-4, 4),
    farbe: str = "blue",
    sigma_bereiche: bool = True,
) -> go.Figure:
    """Zeichnet die Normalverteilung

    Args:
        mu: Erwartungswert
        sigma: Standardabweichung
        x_bereich: Darstellungsbereich als (min, max) in Einheiten von sigma
        farbe: Farbe für die Kurve
        sigma_bereiche: Sigma-Bereiche hervorheben

    Returns:
        Plotly Figure-Objekt
    """
    # x-Werte im angegebenen Bereich
    x_min, x_max = mu + x_bereich[0] * sigma, mu + x_bereich[1] * sigma
    x_vals = np.linspace(x_min, x_max, 1000)

    # PDF berechnen
    x_sym = sp.Symbol("x")
    X = sp.stats.Normal("X", mu, sigma)
    pdf_func = lambdify(x_sym, sp.stats.density(X)(x_sym), "numpy")
    pdf_vals = pdf_func(x_vals)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=pdf_vals,
            mode="lines",
            name=f"N({mu}, {sigma}²)",
            line_color=farbe,
            line_width=2,
        )
    )

    # Erwartungswert als vertikale Linie
    fig.add_vline(x=mu, line_dash="dash", line_color="red", annotation_text=f"μ = {mu}")

    # Sigma-Bereiche hervorheben
    if sigma_bereiche:
        colors = ["rgba(255,255,0,0.2)", "rgba(255,165,0,0.2)", "rgba(255,0,0,0.2)"]
        ranges = [
            (mu - sigma, mu + sigma),
            (mu - 2 * sigma, mu + 2 * sigma),
            (mu - 3 * sigma, mu + 3 * sigma),
        ]

        for i, (x1, x2) in enumerate(ranges):
            if (
                x1 >= x_min and x2 <= x_max
            ):  # Nur wenn vollständig im sichtbaren Bereich
                fig.add_vrect(
                    x0=x1,
                    x1=x2,
                    fillcolor=colors[i],
                    opacity=0.3,
                    layer="below",
                    line_width=0,
                    annotation_text=f"±{i + 1}σ",
                )

    fig.update_layout(
        title=f"Normalverteilung N({mu}, {sigma}²)",
        xaxis_title="x",
        yaxis_title="f(x)",
        showlegend=False,
        yaxis_range=[0, max(pdf_vals) * 1.1],
    )

    return fig


def zeichne_vergleich_zwei_normalverteilungen(
    mu1: float,
    sigma1: float,
    mu2: float,
    sigma2: float,
    x_bereich: tuple = None,
    farbe1: str = "blue",
    farbe2: str = "red",
) -> go.Figure:
    """Vergleicht zwei Normalverteilungen in einem Graphen

    Args:
        mu1, sigma1: Parameter der ersten Verteilung
        mu2, sigma2: Parameter der zweiten Verteilung
        x_bereich: Darstellungsbereich (automatisch, wenn None)
        farbe1, farbe2: Farben für die Verteilungen

    Returns:
        Plotly Figure-Objekt
    """
    if x_bereich is None:
        # Automatischer Bereich, der beide Verteilungen abdeckt
        min_val = min(mu1 - 3 * sigma1, mu2 - 3 * sigma2)
        max_val = max(mu1 + 3 * sigma1, mu2 + 3 * sigma2)
        x_bereich = (min_val, max_val)

    x_vals = np.linspace(x_bereich[0], x_bereich[1], 1000)
    x_sym = sp.Symbol("x")

    # Beide PDFs berechnen
    X1 = sp.stats.Normal("X1", mu1, sigma1)
    X2 = sp.stats.Normal("X2", mu2, sigma2)

    pdf_func1 = lambdify(x_sym, sp.stats.density(X1)(x_sym), "numpy")
    pdf_func2 = lambdify(x_sym, sp.stats.density(X2)(x_sym), "numpy")

    pdf_vals1 = pdf_func1(x_vals)
    pdf_vals2 = pdf_func2(x_vals)

    fig = go.Figure()

    # Erste Verteilung
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=pdf_vals1,
            mode="lines",
            name=f"N({mu1}, {sigma1}²)",
            line_color=farbe1,
            line_width=2,
        )
    )

    # Zweite Verteilung
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=pdf_vals2,
            mode="lines",
            name=f"N({mu2}, {sigma2}²)",
            line_color=farbe2,
            line_width=2,
        )
    )

    # Erwartungswerte als vertikale Linien
    fig.add_vline(
        x=mu1, line_dash="dash", line_color=farbe1, annotation_text=f"μ₁ = {mu1}"
    )
    fig.add_vline(
        x=mu2, line_dash="dash", line_color=farbe2, annotation_text=f"μ₂ = {mu2}"
    )

    fig.update_layout(
        title="Vergleich zweier Normalverteilungen",
        xaxis_title="x",
        yaxis_title="f(x)",
        showlegend=True,
        yaxis_range=[0, max(max(pdf_vals1), max(pdf_vals2)) * 1.1],
    )

    return fig
