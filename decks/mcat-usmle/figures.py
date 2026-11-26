"""Draw the original review stimuli from their numerical models."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

MEDIA = Path(__file__).resolve().parent / "media"
COLORS = ["#145a74", "#a34418"]
STYLES = ["-", "--"]


def axes(x, y):
    fig, ax = plt.subplots(figsize=(5.2, 3.3), layout="constrained")
    ax.set(xlabel=x, ylabel=y)
    ax.grid(alpha=.18)
    return fig, ax


def save(fig, name):
    fig.savefig(MEDIA / f"med_{name}.png", dpi=145, facecolor="white")
    plt.close(fig)


def plot(name, xname, yname, x, curves):
    fig, ax = axes(xname, yname)
    for i, (label, y) in enumerate(curves.items()):
        ax.plot(x, y, STYLES[i], lw=2.4, color=COLORS[i], label=label,
                marker="o" if len(x) < 10 else None)
    if len(curves) > 1:
        ax.legend()
    save(fig, name)


def main():
    MEDIA.mkdir(exist_ok=True)
    x = np.arange(5)
    plot("flow", "Pressure difference (kPa)", "Flow (mL/s)", x, {"Tube A": 3*x, "Tube B": x})
    plot("current", "Voltage (V)", "Current (mA)", x, {"R1": 3*x, "R2": 1.5*x})
    t = np.linspace(0, 4, 101)
    plot("decay", "Time (half-lives)", "Activity relative to start (%)", t, {"Tracer": 100*0.5**t})
    x = np.linspace(0, 1, 201)
    plot("barrier", "Reaction coordinate", "Relative energy (kJ/mol)", x,
         {"Path A": 45*np.sin(np.pi*x)**2 - 10*x, "Path B": 23*np.sin(np.pi*x)**2 - 10*x})
    fig, ax = axes("Mean difference (points), with 95% interval", "")
    ax.errorbar([1, 4], [1, 0], xerr=[2.5, 2], fmt="o", capsize=6, color=COLORS[0], lw=2)
    ax.axvline(0, ls="--", color="#555"); ax.set(yticks=[1, 0], yticklabels=["A", "B"], ylim=(-.6, 1.6))
    save(fig, "interval")
    p = np.linspace(0, 100, 201)
    plot("oxygen", "Oxygen partial pressure (mm Hg)", "Hemoglobin saturation (%)", p,
         {"Curve A": 100*p**2.7/(25**2.7+p**2.7), "Curve B": 100*p**2.7/(38**2.7+p**2.7)})
    fig, ax = axes("Left ventricular volume (mL)", "Left ventricular pressure (mm Hg)")
    for i, (label, esv, edv, peak) in enumerate([("Beat A", 45, 135, 118), ("Beat B", 55, 110, 98)]):
        ax.plot([esv, (esv+edv)/2, edv, edv, (esv+edv)/2, esv, esv],
                [6+i, 8+i, 12+i, peak-14, peak, peak-26, 6+i], STYLES[i], color=COLORS[i], lw=2.4, label=label)
    ax.legend(); save(fig, "pv")
    x = np.linspace(-2, 2, 101)
    plot("dose", "Log₁₀ concentration (arbitrary units)", "Response (% of reference)", x,
         {"Drug A": 100/(1+10**(-x)), "Drug B": 55/(1+10**(-x))})
    plot("trop", "Time since first sample (hours)", "Troponin (ng/L)", [0, 3, 6, 12, 24],
         {"Series A": [15, 70, 150, 118, 52], "Series B": [60, 62, 59, 61, 60]})
    fig, ax = axes("Time after treatment starts (hours)", "Fraction of initial concentration (%)")
    for i, (label, y) in enumerate([("Glucose", [100, 67, 50, 46, 45]), ("Beta-hydroxybutyrate", [100, 84, 62, 36, 12])]):
        ax.plot([0, 2, 4, 6, 8], y, STYLES[i], marker="o", color=COLORS[i], lw=2.4, label=label)
    ax.legend(); save(fig, "ketones")
    plot("egfr", "Time after first visit (months)", "eGFR (mL/min/1.73 m²)", [0, 1, 3, 4],
         {"Patient A": [54, 52, 55, 53], "Patient B": [45, 72, 80, 76]})


if __name__ == "__main__":
    main()
