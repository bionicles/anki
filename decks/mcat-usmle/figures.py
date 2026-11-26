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


def mcat_chemistry():
    # Idealized spectral windows. The axes distinguish absorption from transmission.
    fig, ax = axes("Wavenumber (cm⁻¹)", "Transmittance (%)")
    w = np.linspace(1500, 3900, 1100)
    for label, center, width, color, style in [
        ("A", 1715, 19, COLORS[0], "-"), ("B", 3330, 165, COLORS[1], "--")
    ]:
        y = 94 - 62*np.exp(-0.5*((w-center)/width)**2) - 10*np.exp(-0.5*((w-2940)/33)**2)
        ax.plot(w, y, ls=style, color=color, label=label, lw=2.4)
    ax.set(xlim=(3900, 1500), ylim=(0, 102))
    ax.legend()
    save(fig, "ir")

    fig, panels = plt.subplots(1, 2, figsize=(6.0, 2.8), sharey=True, layout="constrained")
    for ax, center, lines, area in zip(panels, [4.1, 1.3], [[1,3,3,1], [1,2,1]], [2,3]):
        x = np.linspace(center-.07, center+.07, 800)
        peaks = (np.arange(len(lines))-(len(lines)-1)/2)*.018
        y = sum(h*np.exp(-((x-center-offset)/.004)**2) for h, offset in zip(lines,peaks))
        ax.plot(x, area*y/sum(lines), color=COLORS[0], lw=2)
        ax.set(xlim=(x[-1], x[0]), xlabel="Chemical shift (ppm)", yticks=[],
               title=f"Relative integral {area}")
    save(fig, "multiplets")

    fig, ax = axes("Wavelength (nm)", "Absorbance")
    x = np.linspace(200, 370, 500)
    for label, center, style, color in [("A",240,"-",COLORS[0]),("B",310,"--",COLORS[1])]:
        ax.plot(x, .75*np.exp(-.5*((x-center)/13)**2), ls=style, color=color, label=label, lw=2.4)
    ax.legend()
    save(fig, "uv")

    fig, panels = plt.subplots(1, 2, figsize=(5.4, 2.7), layout="constrained")
    for i, ax in enumerate(panels):
        ax.set(xlim=(-1.3,1.3), ylim=(-1.2,1.2), aspect="equal", title="AB"[i])
        ax.axis("off")
        ax.plot([-.55,.55], [0,0], color="#222")
        ax.plot([0,0], [-.53,.53], color="#222")
        for x,y,label in [(0,.78,"CO₂H"),(0,-.78,"CH₃"),(-.8,0,["H","OH"][i]),(.8,0,["OH","H"][i])]:
            ax.text(x,y,label,ha="center",va="center",fontsize=14)
    save(fig, "fischer")

    fig, ax = plt.subplots(figsize=(4.2, 2.5), layout="constrained")
    ax.set(xlim=(-1.4,1.4),ylim=(-1,1),aspect="equal")
    ax.axis("off")
    for y in [-.045,.045]:
        ax.plot([-.4,.4],[y,y],color="#242424",lw=2)
    for side,upper,lower in [(-1,"Br","CH₃"),(1,"Cl","H")]:
        for sign,label in [(1,upper),(-1,lower)]:
            ax.plot([side*.4,side*.87],[0,.48*sign],color="#242424",lw=2)
            ax.text(side*1.04,sign*.6,label,ha="center",va="center",fontsize=16)
    save(fig,"alkene")

    fig, ax = plt.subplots(figsize=(4.4,3.4), layout="constrained")
    ax.set(xlim=(0,4),ylim=(-.6,5.5),ylabel="Distance from origin (cm)",xticks=[1,2,3],
           xticklabels=["Standard A","Mixture","Standard B"],yticks=range(6))
    ax.axhline(0,color="#333")
    ax.axhline(5,color="#666",ls="--")
    ax.text(2,5.08,"Solvent front",ha="center")
    ax.scatter([1,2,2,3],[1,1,4,4],s=110,color=COLORS[0])
    save(fig,"tlc")


def cardiovascular():
    # Idealized envelopes from two separate fictional Doppler examinations.
    t = np.linspace(0, 1.8, 900)
    for code, maximum, period in [("a", 4.5, .80), ("b", 3.0, .68)]:
        phase = np.mod(t, period)
        v = maximum * np.sin(np.pi*np.minimum(phase/.32, 1))**1.25
        fig, ax = axes("Time (s)", "Aortic jet velocity (m/s)")
        ax.plot(t, v, color=COLORS[0])
        ax.set(ylim=(0,5), yticks=np.arange(0,5.1,.5), title="Simulated Doppler envelope")
        save(fig, f"cv_jet_{code}")
    for code, values in [("a",[1,1.12,1.15]), ("b",[1.2,1.55,1.8])]:
        fig, ax = axes("Days since starting ACE inhibitor", "Creatinine (mg/dL)")
        ax.plot([0,7,14],values,"o-",color=COLORS[0]); ax.set(xticks=[0,7,14],ylim=(.7,2.15))
        for x,y in zip([0,7,14],values):
            ax.annotate(f"{y:.2f}",(x,y),xytext=(0,8),textcoords="offset points",ha="center")
        save(fig,f"cv_renal_{code}")
    for code, sbp, dbp in [("a",[140,113,112],[80,70,68]), ("b",[132,130,128],[80,79,78])]:
        fig, ax = axes("Position and time", "Blood pressure (mm Hg)")
        for vals, label, color in [(sbp,"Systolic",COLORS[0]),(dbp,"Diastolic",COLORS[1])]:
            ax.plot([0,1,3],vals,"o-",color=color,label=label)
            for x,y in zip([0,1,3],vals):
                ax.annotate(str(y),(x,y),xytext=(0,7),textcoords="offset points",ha="center")
        ax.set(xticks=[0,1,3],xticklabels=["Supine","Standing, 1 min","Standing, 3 min"],ylim=(55,160))
        ax.legend(loc="center right")
        save(fig,f"cv_stand_{code}")
    for code, previous, current in [("a",28,52),("b",58,55)]:
        fig, ax = axes("Echocardiogram", "LV ejection fraction (%)")
        ax.bar(["Earlier","Current"],[previous,current],width=.5,color=COLORS[0])
        for x,y in enumerate([previous,current]):
            ax.text(x,y+2,f"{y}%",ha="center")
        ax.set(ylim=(0,75),title="Two examinations of the same patient")
        save(fig,f"cv_ef_{code}")


def respiratory():
    for case, mpa, wedge, output in [("a", 30, 10, 4), ("b", 30, 22, 5), ("c", 40, 22, 4)]:
        fig, ax = axes("Resting right-heart catheterization", "Pressure (mm Hg)")
        bars = ax.bar(["Mean pulmonary artery", "Pulmonary artery wedge"], [mpa, wedge],
                      color=COLORS, width=.5)
        ax.bar_label(bars, padding=4)
        ax.set(ylim=(0, 48), title=f"Simulated measurements · cardiac output {output} L/min")
        save(fig, f"lung_ph_{case}")

    # Positive flow is expiration. Negative flow is inspiration back toward TLC.
    for case, fvc, peak, exp_limit, insp_limit in [
        ("neck", 4.3, 7.2, 8, 1.6), ("chest", 3.9, 6.4, 2, 8),
        ("fixed", 4.5, 7.4, 2.6, 2.1), ("scoop", 4.1, 4.5, 8, 8)
    ]:
        x = np.linspace(0, 1, 500)
        fall = 2.4 if case == "scoop" else 1.05
        expired = peak*np.where(x < .13, x/.13, ((1-x)/.87)**fall)
        inspired = -4.7*np.sin(np.pi*x)**.65
        fig, ax = axes("Volume expired from full inspiration (L)", "Flow (L/s)")
        ax.axhline(0, color="0.4", lw=.8)
        ax.plot(x*fvc, np.minimum(expired, exp_limit), color=COLORS[0], label="Expiration")
        ax.plot(x*fvc, np.maximum(inspired, -insp_limit), color=COLORS[1], ls="--", label="Inspiration")
        ax.set(xlim=(-.1,5),ylim=(-6,8.5),title="Simulated maximal flow–volume loop")
        ax.legend(loc="upper right", fontsize=8)
        save(fig, f"lung_loop_{case}")

    # Identical axes allow direct comparison when studying separate fictional patients.
    for case, volumes in [("a", [0, .90, 1.50, 2.25, 2.70, 3.00, 3.00]),
                          ("b", [0, 1.50, 2.40, 2.88, 3.00, 3.00, 3.00])]:
        fig, ax = axes("Time since start of forced expiration (s)", "Expired volume (L)")
        ax.plot([0, .5, 1, 2, 3, 5, 6], volumes, "o-", color=COLORS[0])
        ax.axvline(1, ls=":", color="0.4")
        ax.set(xticks=range(7), ylim=(0, 3.4), yticks=np.arange(0, 3.1, .3),
               title="Simulated forced expiration")
        save(fig, f"lung_spiro_{case}")

    for case, start, length, effort, period in [("a", 9, 15, True, 3.2), ("b", 11, 13, False, 3.6)]:
        t = np.linspace(0, 34, 1361)
        pause = (t >= start) & (t <= start + length)
        signal = np.sin(2*np.pi*t/period)
        fig, axs = plt.subplots(2, 1, sharex=True, figsize=(6.4, 3.4), layout="constrained")
        for ax, label, y in zip(axs, ["Airflow", "Chest effort"],
                                [np.where(pause, 0, signal), np.where(pause, 1.15 if effort else 0, 1)*signal]):
            ax.plot(t, y, color=COLORS[0])
            ax.axvspan(start, start+length, color="#e1e8eb", zorder=-1)
            ax.set(ylabel=label, ylim=(-1.4, 1.4), yticks=[])
        axs[0].set_title("Simulated adult sleep study")
        axs[-1].set(xlabel="Time (s)", xlim=(0, 34))
        save(fig, f"lung_sleep_{case}")

    for case, peak, plateau in [("a", 38, 18), ("b", 39, 33)]:
        fig, ax = axes("Time within one breath (s)", "Airway pressure (cm H₂O)")
        ax.plot([0,.15,.15,.85,.85,1.25,1.25,1.45,1.8],
                [8,8,8+peak-plateau,peak,plateau,plateau,14,8,8], color=COLORS[0], lw=2.4)
        ax.axvspan(.85,1.25,color="#e1e8eb",zorder=-1)
        ax.text(1.05, 2,"Hold",ha="center")
        for x, y in [(.82,peak),(1.08,plateau)]:
            ax.annotate(str(y),(x,y),xytext=(0,5),textcoords="offset points",ha="center")
        ax.set(ylim=(0,46),title="Simulated passive volume-controlled breath")
        save(fig, f"lung_hold_{case}")

    for case, perfusion, ventilation in [("a", 0, 1.2), ("b", 1.4, 0)]:
        fig, ax = axes("One lung region", "Flow (L/min)")
        values = [ventilation, perfusion]
        bars = ax.bar(["Alveolar ventilation", "Perfusion"], values, color=COLORS, width=.55)
        ax.bar_label(bars, fmt="%.1f", padding=4)
        ax.set(ylim=(0,1.8),title="Simulated regional measurements")
        save(fig, f"lung_vq_{case}")

    for case, ph, rr in [("a", [7.28,7.31,7.35],[32,27,22]),
                         ("b", [7.29,7.25,7.20],[31,34,39])]:
        fig, axs = plt.subplots(2,1,sharex=True,figsize=(5.7,3.9),layout="constrained")
        for ax, label, values, lim in zip(axs, ["Arterial pH","Breaths/min"],[ph,rr],[(7.17,7.43),(17,44)]):
            ax.plot([0,1,2],values,"o-",color=COLORS[0])
            ax.set(ylabel=label,ylim=lim)
            for x,y in enumerate(values):
                ax.annotate(str(y),(x,y),xytext=(0,5),textcoords="offset points",ha="center")
        axs[0].set_title("Simulated course during bilevel support")
        axs[-1].set(xticks=[0,1,2],xlabel="Hours since NIV started")
        save(fig, f"lung_niv_{case}")


def gastrointestinal():
    panels = [
        ("enzymes", "liver chemistry", "Multiple of upper limit of normal",
         ["ALT", "Alkaline phosphatase"], [(18, 2), (3, 6), (9, 3)], 21),
        ("gap", "stool electrolytes", "Concentration (mmol/L)",
         ["Sodium", "Potassium"], [(35, 30), (100, 30)], 120),
        ("saag", "same-day albumin levels", "Albumin (g/dL)",
         ["Serum", "Ascitic fluid"], [(3.2, 1.4), (3.0, 2.4)], 4),
    ]
    for name, title, unit, labels, cases, ymax in panels:
        for code, values in zip("abc", cases):
            fig, ax = axes("", unit)
            bars = ax.bar(labels, values, color=COLORS, width=.5)
            ax.bar_label(bars, fmt="%g", padding=4)
            ax.set(ylim=(0,ymax), title=f"Simulated {title}")
            save(fig, f"gi_{name}_{code}")

    for code, values in [("a", [100, 79, 55, 26]), ("b", [100, 68, 45, 5])]:
        fig, ax = axes("Time after standardized meal (hours)", "Meal retained (%)")
        ax.plot([0,1,2,4], values, "o-", color=COLORS[0])
        for x, y in zip([0,1,2,4],values):
            ax.annotate(f"{y}%",(x,y),xytext=(0,5),textcoords="offset points",ha="center")
        ax.set(xticks=[0,1,2,3,4],ylim=(0,116),title="Simulated solid-meal gastric emptying study")
        save(fig,f"gi_empty_{code}")

    for code, heights in [("a", [12, 10, 8]), ("b", [6, 2, 0])]:
        fig, ax = axes("Time after swallowing barium (min)", "Column height (cm)")
        ax.plot([1,2,5], heights, "o-", color=COLORS[0])
        for x, y in zip([1,2,5], heights):
            ax.annotate(str(y),(x,y),xytext=(0,6),textcoords="offset points",ha="center")
        ax.set(xticks=[1,2,5],ylim=(-.6,14),title="Simulated timed barium esophagram measurements")
        save(fig,f"gi_barium_{code}")


def main():
    MEDIA.mkdir(exist_ok=True)
    mcat_chemistry()
    cardiovascular()
    respiratory()
    gastrointestinal()
    plot("refeed", "Hours after starting nutrition", "Serum phosphate (mg/dL)",
         [0,12,24,36,48], {"Patient A": [3.2,2.9,2.4,1.8,1.6],
                            "Patient B": [3.1,3.2,3.0,3.1,3.1]})
    plot("weights", "Month", "Measured weight (kg)", [0,1,2,3,4],
         {"Patient A": [80,78,75,73,72], "Patient B": [74,74,73,74,74]})
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
