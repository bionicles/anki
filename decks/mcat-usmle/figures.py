"""Draw the original review stimuli from their numerical models."""
from io import BytesIO
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

MEDIA = Path(__file__).resolve().parent / "media"
COLORS = ["#145a74", "#a34418"]
STYLES = ["-", "--"]


def axes(x, y):
    fig, ax = plt.subplots(figsize=(5.2, 3.3), layout="constrained")
    ax.set(xlabel=x, ylabel=y)
    ax.grid(alpha=.18)
    return fig, ax


def save(fig, name, *, indexed=False):
    path = MEDIA / f"med_{name}.png"
    if indexed:
        # Flat-color diagrams need few palette entries, even with antialiased labels.
        with BytesIO() as buffer:
            fig.savefig(buffer, format="png", dpi=145, facecolor="white")
            buffer.seek(0)
            with Image.open(buffer) as rendered:
                rendered.convert("RGB").quantize(colors=128).save(path, optimize=True)
    else:
        fig.savefig(path, dpi=145, facecolor="white")
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


def special_senses():
    from matplotlib.patches import Circle, Wedge

    # Angles describe visual space viewed by the patient, independent of eye.
    right, left = (-90, 90), (90, 270)
    fields = {
        "a": (right, right), "b": (left, left), "c": (left, right),
        "d": ((0, 360), None), "e": ((0, 90), (0, 90)),
        "f": ((180, 270), (180, 270)),
    }
    for code, sectors in fields.items():
        fig, panels = plt.subplots(1, 2, figsize=(5.2, 3.0))
        fig.subplots_adjust(top=.82, bottom=.20, wspace=.10)
        for ax, eye, sector in zip(panels, ("Left eye", "Right eye"), sectors):
            ax.add_patch(Circle((0, 0), 1, facecolor="white", edgecolor="none"))
            if sector:
                ax.add_patch(Wedge((0, 0), 1, *sector, facecolor="#526679"))
            ax.add_patch(Circle((0, 0), 1, fill=False, edgecolor="#263746", lw=1.5))
            ax.plot([-1, 1], [0, 0], ":", color="#91a2af")
            ax.plot([0, 0], [-1, 1], ":", color="#91a2af")
            ax.set(xlim=(-1.1, 1.1), ylim=(-1.1, 1.1), aspect="equal", title=eye)
            ax.axis("off")
        fig.text(.5, .04, "Patient’s view  •  Shaded area = field lost", ha="center")
        save(fig, "field_" + code)

    # Synthetic, single-ear thresholds. Slight horizontal symbol offsets keep
    # coincident or near-coincident measurements legible on narrow screens.
    audiograms = {
        "a": ([45, 45, 45, 50, 50], [5, 5, 10, 10, 10]),
        "b": ([20, 30, 45, 60, 70], [20, 30, 45, 55, 65]),
        "c": ([65, 65, 70, 80, 85], [30, 35, 40, 45, 50]),
        "d": ([15, 15, 15, 15, 20], [10, 10, 10, 10, 15]),
    }
    for code, (air, bone) in audiograms.items():
        fig, ax = axes("Frequency (Hz)", "Threshold (dB HL)")
        x = np.arange(5)
        ax.plot(x-.025, air, "o-", color=COLORS[0], mfc="white", label="Air")
        ax.plot(x+.025, bone, "s--", color=COLORS[1], mfc="white", label="Masked bone")
        ax.set(xticks=x, xticklabels=["250", "500", "1000", "2000", "4000"],
               ylim=(95, -10), yticks=np.arange(-10, 100, 10), title="Single-ear pure-tone thresholds")
        ax.legend(loc="lower left")
        save(fig, "audio_" + code)


def neurologic_monitoring():
    # Teaching traces emphasize bilateral versus unilateral onset. The zero
    # crossing and one-second bracket stay fixed across both recordings.
    t = np.linspace(-.7, 1.8, 1800)
    phase = (t + .03) % (1/3)
    cycle = np.exp(-((phase-.05)/.013)**2) - .50*np.exp(-((phase-.16)/.054)**2)
    for code, bilateral in [("a", True), ("b", False)]:
        fig, ax = plt.subplots(figsize=(5.5, 2.65), layout="constrained")
        for base, active, color in [(1.8, True, COLORS[0]), (0, bilateral, COLORS[1])]:
            baseline = .07*np.sin(2*np.pi*9*t + base) + .035*np.cos(2*np.pi*6*t)
            trace = np.where((t>=0) & active, cycle, baseline)
            ax.plot(t, base+trace, color=color, lw=1.4)
        ax.axvspan(0, 1.8, color="#d5dee6", alpha=.32, zorder=0)
        ax.plot([.15, .15, 1.15, 1.15], [3, 3.09, 3.09, 3], lw=1.3, color="black")
        ax.text(.65, 3.13, "1 second", ha="center", fontsize=9)
        ax.set(xlim=(-.7, 1.8), ylim=(-.7, 3.55), yticks=[1.8,0],
               yticklabels=["Left frontal", "Right frontal"], xlabel="Time from onset (seconds)",
               title="Schematic homologous EEG channels")
        ax.spines[["top","right","left"]].set_visible(False)
        save(fig, "neeg_" + code)

    for code, values in [("a", [32, 28, 21, 15]), ("b", [34, 33, 35, 34])]:
        fig, ax = axes("Time from first assessment (h)", "Vital capacity (mL/kg)")
        ax.plot([0, 2, 4, 6], values, "o-", color=COLORS[0], lw=2)
        for hour, value in zip([0, 2, 4, 6], values):
            ax.annotate(str(value), (hour, value), xytext=(0, 7), textcoords="offset points", ha="center")
        ax.set(xticks=[0,2,4,6], ylim=(0, 42), title="Serial bedside vital capacity")
        save(fig, "nvc_" + code)


def hematology():
    # Hypothetical 1:1 mixing studies. Each column uses the same reference
    # interval; the normal plasma control remains normal after incubation.
    for code, times in {"a": (78, 33, 34), "b": (77, 34, 65),
                        "c": (75, 63, 65)}.items():
        fig, ax = axes("", "aPTT (seconds)")
        values = [30, *times, 31]
        ax.bar(range(5), values, color=[COLORS[0], COLORS[1], COLORS[1], COLORS[1], COLORS[0]])
        ax.axhspan(25, 36, alpha=.20, color="#83bba4", label="Reference: 25–36 s")
        ax.set(xticks=range(5), xticklabels=["Control", "Patient", "1:1 mix\ninitial",
               "1:1 mix\nincubated", "Control\nincubated"], ylim=(0, 99),
               title="Mixing study • immediate and after incubation")
        ax.bar_label(ax.containers[0], padding=2)
        ax.legend(loc="upper right")
        save(fig, "he_mix_" + code)

    for code, fractions in {"a": (58, 39, 1, 2, 0), "b": (0, 92, 5, 3, 0),
                            "c": (0, 50, 2, 3, 45), "d": (40, 54, 4, 2, 0)}.items():
        fig, ax = axes("Hemoglobin fraction", "Share of total (%)")
        ax.bar(["A","S","F","A₂","C"], fractions, color=COLORS[0])
        ax.set(ylim=(0, 107), title="Quantitative hemoglobin analysis")
        ax.bar_label(ax.containers[0], padding=2)
        save(fig, "he_hb_" + code)

    # Idealized serum protein electrophoresis with the anode on the left.
    x = np.linspace(0, 1, 900)
    def peak(center, width, height):
        return height*np.exp(-.5*((x-center)/width)**2)
    common = peak(.11,.035,2.6) + peak(.26,.032,.32) + peak(.39,.044,.62) + peak(.57,.048,.61)
    for code, gamma in {"a": peak(.80,.011,1.8) + peak(.80,.08,.21),
                        "b": peak(.80,.09,1.18), "c": peak(.80,.085,.14)}.items():
        fig, ax = axes("Migration region", "Relative signal (arbitrary units)")
        ax.plot(x, common + gamma, color=COLORS[0], lw=2)
        ax.set(xticks=[.11,.26,.39,.57,.80], xticklabels=["Albumin","α₁","α₂","β","γ"],
               xlim=(0,1), ylim=(0,3), title="Serum protein electrophoresis • schematic")
        save(fig, "he_spep_" + code)

    lab_cases = {
        "a": ([185, 125, 60], [13, 17, 23], [330, 205, 95]),
        "b": ([80, 44, 18], [12, 13, 13], [340, 325, 335]),
        "c": ([46, 83, 132], [22, 17, 14], [95, 160, 240]),
    }
    for code, series in lab_cases.items():
        fig, panels = plt.subplots(1, 3, figsize=(6.6, 2.9), layout="constrained")
        for ax, values, name, unit, limits in zip(
            panels, series, ["Platelets", "Prothrombin time", "Fibrinogen"],
            ["×10⁹/L", "Seconds", "mg/dL"], [(0,210), (0,29), (0,405)]
        ):
            ax.plot([0, 6, 12], values, "o-", color=COLORS[0])
            for hour, v in zip([0,6,12], values):
                ax.annotate(str(v),(hour,v),xytext=(0,6),textcoords="offset points",ha="center",fontsize=8)
            ax.set(title=name, ylabel=unit, xlabel="Hours", xticks=[0,6,12], ylim=limits, xlim=(-2,14))
            ax.grid(alpha=.18)
        save(fig, "he_lab_" + code)


def quality_and_communication():
    # Each panel describes a separate cohort of 100 over the same year.
    for code, counts in {"a": (12, 6), "b": (4, 2)}.items():
        fig, panels = plt.subplots(1, 2, figsize=(5.3, 3.2))
        for ax, count, title in zip(panels, counts, ["Usual care", "New option"]):
            for index in range(100):
                event = index < count
                ax.scatter(index%10, 9-index//10, s=34, marker="s" if event else "o",
                           facecolors=COLORS[0] if event else "white", edgecolors=COLORS[0], linewidths=.8)
            ax.set(aspect="equal", title=title, xlim=(-.6,9.6), ylim=(-.6,9.6))
            ax.axis("off")
        fig.subplots_adjust(top=.85, bottom=.19, wspace=.12)
        fig.text(.5,.06,"Each symbol = 1 person   •   Filled square = event within 1 year",ha="center",fontsize=9)
        save(fig, "soc_risk_" + code)

    base = [46,54,48,53,45,51,47,55,49,52]
    for code, follow in {"a":[42,44,41,43,40,42,39], "b":[47,55,43,52,46,54,49]}.items():
        fig, ax = axes("Week", "Median time to result (minutes)")
        ax.plot(range(1,18), base+follow, "o-", color=COLORS[0], lw=1.7)
        ax.axhline(np.median(base), color="black", ls="--", label="Baseline median")
        ax.axvline(10.5, color=COLORS[1], ls=":", label="Pilot begins")
        ax.set(ylim=(32,67), xticks=[1,4,7,10,13,16]); ax.legend(loc="upper left",fontsize=8)
        save(fig, "soc_run_" + code)

    for code, delay in {"a":[16,16,17,16,16,28,35,37],
                        "b":[16,16,17,16,16,17,15,16]}.items():
        fig, panels = plt.subplots(2,1,figsize=(5.5,3.8),sharex=True,layout="constrained")
        for ax, values, label, bounds in zip(panels, [[8,9,7,8,8,4,3,2],delay],
            ["Errors per\n1,000 orders","Time to urgent\ndose (minutes)"],[(0,11),(0,43)]):
            ax.plot(range(1,9), values, "o-", color=COLORS[0], lw=1.8)
            ax.axvline(5.5,color=COLORS[1],ls=":"); ax.set(ylabel=label,ylim=bounds);ax.grid(alpha=.16)
        panels[0].set_title("Order verification pilot starts after week 5")
        panels[1].set(xlabel="Week",xticks=range(1,9))
        save(fig,"soc_balance_" + code)

    # p-chart expressed per 1,000 opportunities. The historical reference
    # probability is fixed at 0.02, with 1,000 observations in every subgroup.
    margin = 3*1000*np.sqrt(.02*.98/1000)
    for code, last in [("a", 38), ("b", 27)]:
        counts = [18,22,17,21,24,16,23,last]
        fig, ax = axes("Week", "Errors per 1,000 opportunities")
        ax.plot(range(1,9), counts, "o-", color=COLORS[0])
        ax.axhline(20,color="#555",ls=":",label="Historical mean")
        ax.axhline(20+margin,color=COLORS[1],ls="--",label="3-sigma limits")
        ax.axhline(20-margin,color=COLORS[1],ls="--")
        ax.set(ylim=(0,54),xticks=range(1,9),title="1,000 observations each week")
        ax.legend(loc="upper left",fontsize=8)
        save(fig,"soc_control_" + code)

    cases = {"a": ([60, 75], [60, 45]), "b": ([60, 75], [60, 72])}
    for code, (group_a, group_b) in cases.items():
        fig, ax = axes("", "Completed follow-up within 14 days (%)")
        for values, name, marker, style, color in zip([group_a,group_b],["No interpreter requested","Interpreter requested"],
                ["o","s"],["-","--"],COLORS):
            ax.plot([0,1], values, marker=marker, ls=style, color=color, label=name, lw=2)
            ax.annotate(str(values[1])+"%",(1,values[1]),xytext=(7,0),textcoords="offset points",va="center")
        ax.text(-.06,60,"60%",ha="right",va="center")
        ax.set(xticks=[0,1],xticklabels=["Before","After"],xlim=(-.25,1.24),ylim=(25,95))
        ax.legend(loc="lower left",fontsize=8)
        save(fig,"soc_access_" + code)


def reproductive():
    from matplotlib.patches import Circle, Polygon

    # The section marks cell type by color and dot so the boundary crossing
    # can also be read in monochrome.
    for code, invaded in [("a", False), ("b", True)]:
        fig, ax = plt.subplots(figsize=(5.2, 3.3), layout="constrained")
        ax.set_aspect("equal")
        ax.set(xlim=(-1.6, 2.05), ylim=(-1.22, 1.25), title="Schematic breast duct in cross-section")
        ax.axis("off")
        ax.add_patch(Circle((0, 0), 1, facecolor="#f5e8df", edgecolor="none"))
        angles = np.linspace(0, 2*np.pi, 220) if not invaded else np.linspace(.27, 2*np.pi-.27, 220)
        ax.plot(np.cos(angles), np.sin(angles), color="#233339", lw=3)
        coords = [(r*np.cos(t), r*np.sin(t)) for r, n in [(.76, 14), (.47, 9), (.17, 3)]
                  for t in np.linspace(0, 2*np.pi, n, endpoint=False)]
        if invaded:
            coords += [(.95,.03), (1.15,.08), (1.32,-.02), (1.52,-.05)]
        for x, y in coords:
            ax.add_patch(Circle((x,y), .105, facecolor="#efab82", edgecolor="#7b3c24"))
            ax.add_patch(Circle((x,y), .033, facecolor="#482a23"))
        ax.annotate("Duct boundary", xy=(-.82,.57), xytext=(-1.52,1.05), fontsize=8,
                    arrowprops={"arrowstyle":"-", "color":"#34434a"})
        ax.text(1.07,.73,"Stroma",fontsize=9)
        ax.text(-1.44,-1.15,"Dotted circles = atypical epithelial cells",fontsize=8)
        save(fig, "repro_duct_" + code)

    # Contrast outlines the lumen. Patient side is explicit in radiographic orientation.
    for code, tubes in [("a", ("spill","spill")), ("b", ("spill","closed")), ("c", ("proximal","proximal"))]:
        fig, ax = plt.subplots(figsize=(5.2, 3.1), layout="constrained")
        ax.set_aspect("equal")
        ax.set(xlim=(-2.55,2.55),ylim=(-1.0,1.55),title="Contrast study • end of injection")
        ax.axis("off")
        ax.add_patch(Polygon([(-.53,.54),(.53,.54),(.09,-.27),(.07,-.59),(-.07,-.59),(-.09,-.27)],
                             closed=True,facecolor=COLORS[0]))
        for sign, state in zip([-1,1],tubes):
            ax.text(sign*1.65,1.15,"Patient’s " + ("right" if sign<0 else "left"),ha="center",fontsize=10)
            if state=="proximal":
                continue
            x=np.array([.45,.68,.83,1,1.16,1.36,1.52,1.65])
            y=[.5,.58,.70,.64,.79,.68,.51,.52]
            ax.plot(sign*x,y,color=COLORS[0],lw=4,solid_capstyle="round")
            if state=="spill":
                for dx,dy in [(0,.03),(.15,-.12),(-.03,-.18),(.27,.09)]:
                    ax.add_patch(Circle((sign*(1.75+dx),.45+dy),.085,color=COLORS[0],alpha=.68))
        ax.text(0,-.88,"Schematic HSG  •  blue = contrast",ha="center",fontsize=9)
        save(fig, "repro_hsg_" + code)

    # A common early-follicular comparison interval is supplied for each assay.
    for code, fsh, estradiol in [("a",56,12),("b",2,14)]:
        fig, panels=plt.subplots(2,1,figsize=(5.2,3.0),layout="constrained")
        fig.suptitle("Amenorrhea evaluation • teaching laboratory", fontsize=12)
        for ax, label, ref, value, maximum in zip(panels,["FSH (IU/L)","Estradiol (pg/mL)"],
                                                   [(3,10),(25,100)],[fsh,estradiol],[65,120]):
            ax.axvspan(*ref,color="#b9d9c8",label="Follicular reference interval")
            ax.plot(value,.52,"D",color=COLORS[1])
            ax.text(value,.78,str(value),ha="center",va="center",fontsize=9)
            ax.set(xlim=(0,maximum),ylim=(0,1),yticks=[],xlabel=label)
            for side in ["left","right","top"]:
                ax.spines[side].set_visible(False)
        fig.text(.5,.015,"Shading = laboratory follicular reference interval",ha="center",fontsize=8)
        # Leave room for the definition when rendered inside a small card.
        fig.get_layout_engine().set(rect=(0,.07,1,.92))
        save(fig, "repro_axis_" + code)

    outer_smooth=[(-1.38,.78),(-1.18,.99),(-.65,1.08),(0,1.06),(.65,1.08),(1.18,.99),(1.38,.78)]
    outer_cleft=[(-1.38,.72),(-1.18,1.08),(-.86,1.12),(-.62,1.01),(0,.15),(.62,1.01),(.86,1.12),(1.18,1.08),(1.38,.72)]
    for code, outer in [("a",outer_cleft),("b",outer_smooth)]:
        fig, ax=plt.subplots(figsize=(4.7,3.4),layout="constrained")
        ax.set_aspect("equal")
        ax.set(xlim=(-1.6,1.6),ylim=(-1.34,1.32),title="Coronal uterine anatomy • schematic")
        ax.axis("off")
        ax.add_patch(Polygon(outer+[(1.13,.03),(.36,-.74),(.20,-1.11),(-.20,-1.11),(-.36,-.74),(-1.13,.03)],
                             closed=True,facecolor="#da9e92",edgecolor="#624846",lw=2))
        for sign in [-1,1]:
            ax.add_patch(Polygon([(sign*x,y) for x,y in [(1.06,.70),(.73,.59),(.14,-.03),(0,-.49),(.21,-.24),(.91,.37)]],
                                 closed=True,facecolor="#fff5d8",edgecolor="#796b58",lw=1))
        ax.plot([0,0],[-.47,-.98],color="#fff5d8",lw=3)
        ax.text(0,-1.29,"Light regions = uterine cavity and canal",ha="center",fontsize=8)
        save(fig, "repro_uterus_" + code)


def endocrine():
    # The insulin panels use values drawn during symptoms, before any glucose was given.
    for case, glucose, insulin, peptide, ketone, agent in [
        ("a", 42, 19, 2.5, .3, "None detected"),
        ("b", 39, 31, .12, .2, "None detected"),
        ("c", 44, 24, 3.1, .2, "Glipizide detected"),
    ]:
        fig, ax = plt.subplots(figsize=(5.0, 2.9), layout="constrained")
        ax.axis("off")
        ax.set_title("Fasting plasma sample during symptoms", fontsize=12)
        rows = [("Glucose", f"{glucose} mg/dL"), ("Insulin", f"{insulin} μU/mL"),
                ("C-peptide", f"{peptide:g} ng/mL"), ("β-hydroxybutyrate", f"{ketone:g} mmol/L"),
                ("Oral secretagogue screen", agent)]
        table = ax.table(cellText=rows, colLabels=["Measurement", "Result"],
                         cellLoc="left", colLoc="left", bbox=(0, .03, 1, .90))
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for (row, column), cell in table.get_celld().items():
            cell.set_edgecolor("#cad5d7")
            cell.set_facecolor("#d7e8eb" if row == 0 else "white")
        save(fig, "endo_ins_" + case)

    for case, glucose, ketones, ph in [
        ("a", [455, 285, 182], [6.5, 4.8, 2.6], [7.11, 7.18, 7.25]),
        ("b", [426, 256, 160], [5.2, 2.8, .4], [7.15, 7.22, 7.36]),
    ]:
        fig, panels = plt.subplots(3, 1, figsize=(5.2, 4.0), sharex=True, layout="constrained")
        for ax, series, units, bounds in zip(panels, [glucose, ketones, ph],
                ["Glucose\n(mg/dL)", "β-hydroxybutyrate\n(mmol/L)", "Venous pH"],
                [(80,560), (0,8.5), (7.04,7.42)]):
            ax.plot([0,3,6], series, "o-", color=COLORS[0])
            ax.set(ylabel=units, ylim=bounds, xlim=(-.5,6.5))
            ax.yaxis.label.set_size(8)
            ax.grid(alpha=.18)
            for hour, result in zip([0,3,6],series):
                ax.annotate(str(result), (hour,result), xytext=(3,4), textcoords="offset points", fontsize=8)
        panels[-1].set(xlabel="Hours of treatment", xticks=[0,3,6])
        save(fig, "endo_dka_" + case)

    for case, calcium, pth in [("a",11.7,53), ("b",12.8,4)]:
        fig, panels = plt.subplots(2,1,figsize=(5.0,3.1),layout="constrained")
        for ax, result, interval, limits, label in zip(panels, [calcium,pth],
                [(8.6,10.2),(15,65)], [(7,14),(0,80)], ["Adjusted calcium (mg/dL)","Intact PTH (pg/mL)"]):
            ax.axvspan(*interval,color="#c3dfd2")
            ax.plot(result,.5,"D",color=COLORS[1])
            ax.text(result,.79,str(result),ha="center",fontsize=9)
            ax.set(xlabel=label, xlim=limits, ylim=(0,1), yticks=[])
            for side in ("top","left","right"):
                ax.spines[side].set_visible(False)
        fig.suptitle("Paired blood draw • shading is the reference interval", fontsize=10)
        save(fig, "endo_pth_" + case)

    # Use the same scale in both schematics. Neither is a clinical scintigraph.
    y, x = np.mgrid[-1.45:1.45:180j, -1.55:1.55:200j]
    lobes = [((x-side*.54-.10*side*y)/.43)**2 + (y/.98)**2 < 1 for side in (-1,1)]
    gland = (lobes[0] | lobes[1] | ((abs(x)<.55) & (abs(y+.17)<.10)))
    for case, uptake in [("a",54),("b",37)]:
        rng = np.random.default_rng(52 if case=="a" else 26)
        activity = .06 + gland * (.76 if case=="a" else .08)
        if case=="b":
            activity += .80*np.exp(-((x-.57)**2+(y-.22)**2)/.095)
        fig, ax = plt.subplots(figsize=(4.2,3.4),layout="constrained")
        picture = ax.imshow(np.clip(activity+rng.normal(0,.035,x.shape),0,1),
                            cmap="inferno", origin="lower", vmin=0, vmax=1)
        bar = fig.colorbar(picture,ax=ax,ticks=[0,1],shrink=.68)
        bar.ax.set_yticklabels(["Low","High"])
        ax.set_title(f"Simulated thyroid study • 24-hour uptake {uptake}%",fontsize=11)
        ax.set_xlabel("Local reference interval 10–30%",fontsize=9)
        ax.set(xticks=[],yticks=[])
        save(fig, "endo_uptake_" + case)

    for case, values in [("a",[105,115,120,420,600]),("b",[112,119,125,128,134])]:
        fig, ax = axes("Time relative to desmopressin (hours)", "Urine osmolality (mOsm/kg)")
        ax.plot([-2,-1,0,1,2],values,"o-",color=COLORS[0])
        ax.axvline(0,ls="--",lw=1,color="#555")
        for hour in (0,2):
            val=values[hour+2]
            ax.annotate(str(val),(hour,val),xytext=(4,6),textcoords="offset points")
        ax.set(xlim=(-2.25,2.3),ylim=(0,710),xticks=[-2,-1,0,1,2],
               title="Supervised concentrating test")
        ax.text(.04,665,"Dose after hour 0 sample",size=8)
        save(fig, "endo_water_" + case)

    for case, levels in [("a", [2.1, .84, .32, .11, .16]), ("b", [6.8, 6.1, 5.9, 6.4, 6.6])]:
        times = [0, 30, 60, 90, 120]
        fig, ax = axes("Minutes after oral glucose", "Growth hormone (μg/L)")
        ax.plot(times, levels, "o-", color=COLORS[0])
        ax.axhline(.4, ls="--", color="#773e24")
        ax.set(xticks=times, ylim=(.07, 12), yscale="log",
               yticks=[.1, .4, 1, 3, 10], yticklabels=["0.1","0.4","1","3","10"],
               title="Adult GH suppression test • teaching assay")
        ax.text(117, .46, "Lab criterion: nadir <0.4", ha="right", fontsize=8)
        nadir = min(levels)
        ax.annotate(str(nadir), (times[levels.index(nadir)], nadir), xytext=(4,-10),
                    textcoords="offset points", fontsize=8)
        save(fig, "endo_gh_" + case)

    for case, heights in [("a", [111, 117, 119]), ("b", [108, 114, 120])]:
        fig, ax = axes("Age (years)", "Standing height (cm)")
        ax.plot([6, 7, 8], heights, "o-", color=COLORS[0])
        ax.set(xticks=[6, 7, 8], ylim=(104, 125), xlim=(5.8, 8.25),
               title="Serial measurements • prepubertal child")
        for age, height in zip([6, 7, 8], heights):
            ax.annotate(str(height), (age, height), xytext=(4, 5),
                        textcoords="offset points", fontsize=9)
        save(fig, "endo_growth_" + case)




def cardiovascular_studies():
    """Draw simulated segmental pressure, catheter oximetry and pacemaker studies."""
    pressures = {
        "a": ("Left", [140, 132, 84, 98]),
        "b": ("Right", [120, 128, 192, 178]),
        "c": ("Left", [134, 140, 147, 154]),
    }
    for case, (leg, values) in pressures.items():
        labels = ["Right arm", "Left arm", leg + " dorsalis pedis", leg + " posterior tibial"]
        fig, ax = axes("Systolic pressure (mm Hg)", "")
        y = np.arange(len(values))
        ax.barh(y, values, color=[COLORS[0]] * 2 + [COLORS[1]] * 2, height=.58)
        ax.set(yticks=y, yticklabels=labels, xlim=(0, 224), title="Resting Doppler pressures")
        ax.invert_yaxis()
        for pos, value in enumerate(values):
            ax.text(value + 3, pos, str(value), va="center")
        save(fig, "cvstudy_abi_" + case)

    sites = ["Superior vena cava", "Inferior vena cava", "Right atrium",
             "Right ventricle", "Pulmonary artery"]
    runs = {"a": [66, 68, 83, 83, 84], "b": [65, 67, 66, 83, 84],
            "c": [65, 67, 66, 68, 85]}
    for case, values in runs.items():
        fig, ax = axes("Oxygen saturation (%)", "Sampling site")
        ax.scatter(values, np.arange(5), color=COLORS[0], s=65)
        ax.set(yticks=np.arange(5), yticklabels=sites, xlim=(55, 98),
               ylim=(4.6, -.6), title="Catheter oximetry · room air")
        for pos, value in enumerate(values):
            ax.text(value + 1.2, pos, str(value), va="center")
        save(fig, "cvstudy_sat_" + case)

    # The tall thin vertical lines are stimulus artifacts. Native and paced
    # complexes intentionally differ in width in this single-lead schematic.
    t = np.arange(0, 4.1, .001)
    spikes = [.35, 1.35, 2.35, 3.35]
    for case in ("a", "b", "c"):
        fig, ax = axes("Time (s)", "Signal (mV)")
        trace = np.zeros_like(t)
        if case == "c":
            beats = [s - .095 for s in spikes]
            width = .70
        else:
            beats = [s + .05 for s in (spikes[::2] if case == "a" else spikes)]
            width = 1.35
        for beat in beats:
            for delay, height, sigma in [(-.025, -.16, .012), (0, 1.05, .020),
                                          (.035, -.33, .013), (.20, .18, .055)]:
                trace += height * np.exp(-.5 * ((t - beat - width * delay) / (sigma * width))**2)
        ax.plot(t, trace, color=COLORS[0], lw=1.3)
        for spike in spikes:
            base = np.interp(spike, t, trace)
            ax.vlines(spike, base, base + 1.42, color=COLORS[0], lw=1.0)
        ax.set(title="Single ventricular lead · simulated strip", xlim=(0, 4.1),
               ylim=(-.5, 1.65), xticks=np.arange(0, 4.1, .5))
        save(fig, "cvstudy_pace_" + case)


def vascular_anatomy():
    """Schematic transverse sections for diameter and compressibility exercises."""
    from matplotlib.patches import Ellipse

    for case, wall, channel in [("a", 5.0, 1.8), ("b", 2.0, 1.8)]:
        fig, ax = axes("Transverse position (cm)", "Depth (cm)")
        ax.add_patch(Ellipse((0, 3.5), wall, wall, facecolor="#cebec2",
                             edgecolor="#463d42", lw=2, label="Aortic wall boundary"))
        ax.add_patch(Ellipse((0, 3.5), channel, channel, facecolor="#304f64",
                             label="Flow channel"))
        ax.set_aspect("equal")
        ax.set(xlim=(-3.2, 3.2), ylim=(6.5, .5), yticks=np.arange(1, 6.5, .5),
               title="Abdominal aorta · transverse schematic")
        ax.tick_params(labelsize=8)
        ax.legend(loc="center left", bbox_to_anchor=(1, .5), fontsize=8)
        save(fig, "cvstudy_aorta_" + case)

    for case, final_height in [("a", .77), ("b", .035)]:
        fig, panels = plt.subplots(1, 2, figsize=(6, 2.9), layout="constrained")
        for panel, title, art_height, ven_height in zip(
                panels, ["Before compression", "During compression"],
                [1.0, .84], [1.0, final_height]):
            for x, name, width, height in [(1, "Artery", 1.2, art_height),
                                            (2.7, "Vein", 1.45, ven_height)]:
                panel.add_patch(Ellipse((x, 1.0), width, height, facecolor="#314e60",
                                        edgecolor="#223442", lw=2))
                panel.text(x, .16, name, ha="center", fontsize=10)
            panel.set(xlim=(0, 3.7), ylim=(-.1, 2.1), title=title, aspect="equal")
            panel.axis("off")
        fig.suptitle("Femoral vessels · same transverse plane", fontsize=12)
        save(fig, "cvstudy_vein_" + case)


def ventricular_loops():
    """Compare ejection and passive filling at a common end-diastolic volume."""
    for case, residual, filling, end_pressure in [("a", 85, 10, 90), ("b", 50, 25, 100)]:
        fig, ax = axes("LV volume (mL)", "LV pressure (mm Hg)")
        for label, esv, edp, esp, color, style in [
                ("Reference", 50, 10, 100, COLORS[0], "-"),
                ("Patient", residual, filling, end_pressure, COLORS[1], "--")]:
            edv = 120
            u = np.linspace(0, 1, 90)
            v_fill = esv + (edv - esv) * u
            p_fill = 3 + (edp - 3) * (np.exp(3 * u) - 1) / np.expm1(3)
            v_eject = edv - (edv - esv) * u
            p_eject = 80 + (esp - 80) * u + 26 * np.sin(np.pi * u)
            # Filling, isovolumetric contraction, ejection, relaxation.
            vol = np.r_[v_fill, edv, v_eject, esv]
            pressure = np.r_[p_fill, 80, p_eject, 3]
            ax.plot(vol, pressure, style, color=color, lw=2.4, label=label)
        ax.set(xlim=(35, 140), ylim=(0, 130), xticks=[35, 50, 65, 85, 100, 120, 135],
               title="Left ventricular cycle · simulated")
        ax.legend(loc="upper right", fontsize=8)
        save(fig, "cvstudy_pv_" + case)


def rhythm_studies():
    """AV event timing and simulated arrest strips, in seconds."""
    for case in ("a", "b"):
        atrial = np.arange(.2, 4.85, .76 if case == "a" else .57)
        ventricular = atrial + .28 if case == "a" else np.arange(.37, 5, 1.43)
        fig, ax = axes("Time (s)", "")
        for times, y, color in [(atrial, 1, COLORS[0]), (ventricular, 0, COLORS[1])]:
            ax.vlines(times, y - .15, y + .15, color=color, lw=2.6)
        ax.set(xlim=(0, 5), ylim=(-.55, 1.55), yticks=[0, 1],
               yticklabels=["QRS onset", "P onset"], xticks=np.arange(0, 5.1, .5),
               title="Atrial and ventricular timing · schematic")
        if case == "a":
            # Give exact first-pair timestamps while preserving the classification task.
            ax.text(atrial[0], 1.22, "0.20 s", ha="left")
            ax.text(ventricular[0], .21, "0.48 s", ha="left")
        save(fig, "cvstudy_av_" + case)

    t = np.arange(0, 4, .002)
    phase = 2 * np.pi * (4.7*t + .13*np.sin(2*np.pi*1.8*t) + .28*t**2)
    vf = (.40 + .16*np.sin(2*np.pi*.82*t)) * np.sin(phase)
    vf += .16*np.sin(2*np.pi*7.3*t + .74*np.sin(2*np.pi*1.3*t))
    organized = np.zeros_like(t)
    for beat in np.arange(.35, 4, .84):
        for delay, amp, width in [(-.17, .11, .025), (0, 1, .018),
                                  (.035, -.23, .015), (.23, .19, .05)]:
            organized += amp*np.exp(-.5*((t-beat-delay)/width)**2)
    for case, signal in [("a", vf), ("b", organized)]:
        fig, ax = axes("Time (s)", "Signal (mV)")
        ax.plot(t, signal, lw=1.5, color=COLORS[0])
        ax.set(title="Rhythm check · simulated monitor lead", xlim=(0, 4), ylim=(-.8, 1.2))
        save(fig, "cvstudy_arrest_" + case)


def renal_studies():
    """Draw paired laboratory reports and hourly urine-output records."""
    analytes = ["Serum Na (mEq/L)", "Serum Cl (mEq/L)", "Serum bicarbonate (mEq/L)",
                "Blood pH", "Serum K (mEq/L)", "Urine pH", "Plasma glucose (mg/dL)",
                "Urine glucose", "Phosphate handling"]
    panels = {
        "a": ["138", "112", "16", "7.29", "2.9", "6.6", "94", "Absent", "Appropriate"],
        "b": ["139", "114", "15", "7.30", "3.0", "5.1", "89", "Present", "Renal wasting"],
        "c": ["138", "112", "16", "7.31", "5.9", "5.1", "102", "Absent", "Appropriate"],
    }
    for case, values in panels.items():
        fig, ax = plt.subplots(figsize=(5, 3.65), layout="constrained")
        ax.axis("off")
        table = ax.table(cellText=list(zip(analytes, values)), colLabels=["Measurement", "Result"],
                         cellLoc="left", colLoc="left", colWidths=[.66, .32], loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.29)
        for (row, col), cell in table.get_celld().items():
            cell.set_edgecolor("#cbd3d7")
            if row == 0:
                cell.set_facecolor("#e5eff3")
                cell.set_text_props(weight="bold")
        ax.set_title("Blood and urine · simultaneous samples", fontsize=13)
        save(fig, "kidney_acid_" + case)

    outputs = {"a": [21, 28, 20, 27, 19, 25, 30, 28],
               "b": [18, 24, 20, 75, 74, 77, 70, 68]}
    for case, volumes in outputs.items():
        fig, ax = axes("Completed hourly interval", "Urine volume (mL)")
        hours = np.arange(1, 9)
        ax.bar(hours, volumes, color=COLORS[0], width=.68)
        for hour, value in zip(hours, volumes):
            ax.text(hour, value + 1.1, str(value), ha="center", fontsize=9)
        ax.set(xticks=hours, ylim=(0, 90), title="Eight-hour bedside record · 70-kg adult")
        save(fig, "kidney_output_" + case)


def renal_anatomy():
    """Simplified frontal diagrams of collecting-system continuity and drainage."""
    from matplotlib.patches import Ellipse, FancyBboxPatch
    for case in ("a", "b", "c", "d"):
        fig, ax = plt.subplots(figsize=(5.6, 4.1), layout="constrained")
        ax.set(xlim=(-3, 3), ylim=(-.2, 4.7), aspect="equal")
        ax.axis("off")
        ax.set_title("Urinary tract · frontal schematic")
        # Anterior view. The labels use the patient's side.
        for x, sign, label in [(-1.65, -1, "Right"), (1.65, 1, "Left")]:
            ax.text(x, 4.22, label, ha="center")
            ax.add_patch(Ellipse((x, 3.15), 1.32, 1.85, angle=-sign*10,
                                 facecolor="#e7c0a6", edgecolor="#725441", lw=1.8))
            dilated = case == "d" or (case == "c" and sign == 1)
            ink = "#28647b"
            width = 5 if dilated else 1.8
            pelvis = x - sign*.24
            ax.plot([pelvis, pelvis, x, x+sign*.18], [2.6, 3.12, 3.32, 3.55],
                    lw=width, color=ink, solid_capstyle="round")
            ax.plot([pelvis, x, x+sign*.19], [3.1, 3, 2.83], lw=width, color=ink)
            ax.plot([pelvis, x+sign*.22], [3.12, 3.19], lw=width, color=ink)
            ax.plot([pelvis, sign*.96, sign*.84], [2.66, 2.15, 1.23],
                    color=ink, lw=width, solid_capstyle="round")
            lower_width = 1.4 if case == "c" and sign == 1 else width
            ax.plot([sign*.84, sign*.52], [1.23, .72], color=ink, lw=lower_width)
            if sign == 1 and case in ("a", "b"):
                center = (x+.48, 3.55) if case == "a" else (pelvis, 3.10)
                ax.add_patch(Ellipse(center, .46 if case == "a" else .25,
                                     .42 if case == "a" else .25, facecolor="#8e4259",
                                     edgecolor="#50263a", zorder=5))
        bulge = case == "d"
        bladder = FancyBboxPatch((-.65, .27), 1.3, .62 if not bulge else 1.15,
                                 boxstyle="round,pad=.03,rounding_size=.24",
                                 facecolor="#b8dce4", edgecolor="#28647b", zorder=4)
        ax.add_patch(bladder)
        ax.plot([0, 0], [.3, 0], color="#28647b", lw=1.2 if bulge else 2)
        if case in ("a", "b"):
            ax.text(0, -.12, "Blue = urine pathway     Burgundy = lesion",
                    ha="center", va="top", fontsize=9)
        save(fig, "kidney_tract_" + case)


def perinatal_studies():
    """Paired simulated assessments. Each pair changes the evidence under review."""
    for case, dilation in [("a", [1, 2, 3]), ("b", [1, 1, 1])]:
        fig, ax = axes("Time after initial examination (hours)", "Cervical dilation (cm)")
        ax.plot([0, 1, 2], dilation, "o-", color=COLORS[0], lw=2.6, markersize=9)
        ax.set(xticks=[0, 1, 2], yticks=range(6), ylim=(-.25, 5.25),
               title="Patient at 31 weeks · regular contractions")
        save(fig, "perinatal_labor_" + case)

    def record(name, title, labels, observations):
        fig, ax = plt.subplots(figsize=(5.6, 3.0), layout="constrained")
        ax.axis("off")
        ax.set_title(title, loc="left", fontsize=14)
        table = ax.table(cellText=list(zip(labels, observations)), loc="center",
                         cellLoc="left", colWidths=[.50, .50])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 1.8)
        for (row, _), cell in table.get_celld().items():
            cell.set_facecolor("#edf5f6" if row % 2 == 0 else "white")
            cell.set_edgecolor("#c9d7dc")
        save(fig, "perinatal_" + name)

    profile = ["Nonstress test", "Breathing over 30 min", "Body movements / 30 min",
               "Extension → flexion", "Deepest fluid pocket"]
    record("bpp_a", "Biophysical profile · completed observation", profile,
           ["Reactive", "None", "4 discrete movements", "Present", "3.4 cm"])
    record("bpp_b", "Biophysical profile · completed observation", profile,
           ["Nonreactive", "None", "1 discrete movement", "Present", "4.0 cm"])
    for case, measured, median in [("a", 64, 40), ("b", 54, 45)]:
        record("mca_" + case, "Fetal middle cerebral artery · Doppler report",
               ["Measured peak systolic velocity", "Median for gestational age"],
               [f"{measured} cm/s", f"{median} cm/s"])
    for case, hand, foot in [("a", 98, 96), ("b", 98, 94)]:
        record("sat_" + case, "First newborn screen · room air · age 27 h",
               ["Right hand", "Foot"], [f"{hand}%", f"{foot}%"])

    for case in ("a", "b"):
        fig, ax = plt.subplots(figsize=(5.2, 3.6), layout="constrained")
        ax.set(aspect="equal", xlim=(-2.5, 3.45), ylim=(-.85, 2.85))
        ax.axis("off")
        ax.set_title("Lower uterine segment · sagittal schematic")
        # Inner outline tapers to the internal cervical os at (0, 0).
        x = np.array([-2.1, -1.9, -1.55, -.85, -.28, 0, .28, .85, 1.55, 1.9, 2.1])
        y = np.array([2.5, 1.55, .95, .45, .13, 0, .13, .45, .95, 1.55, 2.5])
        ax.plot(x, y, color="#945a57", lw=8, solid_capstyle="round")
        ax.plot([-.12, -.12], [-.7, -.04], color="#945a57", lw=4)
        ax.plot([.12, .12], [-.7, -.04], color="#945a57", lw=4)
        end = 7 if case == "a" else 3
        ax.plot(x[:end], y[:end]+.12, color="#463c78", lw=13, solid_capstyle="round")
        ax.annotate("Placenta", (-1.92, 1.8), (-1.0, 2.4),
                    arrowprops={"arrowstyle": "->"}, fontsize=11)
        ax.annotate("Internal os", (0, -.02), (1.25, -.34),
                    arrowprops={"arrowstyle": "->"}, fontsize=11)
        if case == "b":
            ax.text(.18, 1.24, "Edge–os distance\n35 mm on ultrasound", fontsize=10)
        save(fig, "perinatal_os_" + case)


def twin_fluid_studies():
    """Synthetic ultrasound measurement reports for independent twin sacs."""
    for case, pockets in [("a", [1.1, 9.3]), ("b", [1.2, 1.5])]:
        fig, ax = axes("Amniotic sac", "Deepest vertical pocket (cm)")
        ax.bar(["Twin A", "Twin B"], pockets, width=.43,
               color=[COLORS[0], COLORS[1]])
        for i, pocket in enumerate(pockets):
            ax.text(i, pocket+.16, f"{pocket:.1f} cm", ha="center", fontsize=12)
        ax.set(xlim=(-.65, 1.65), ylim=(0, 11), yticks=range(0, 11, 2),
               title="Monochorionic diamniotic twins · 19 weeks")
        save(fig, "perinatal_twin_" + case)


def fetal_atrium_calipers():
    """Magnified schematic of two opposing atrial walls, in a local coordinate frame."""
    for case in ("a", "b"):
        fig, ax = plt.subplots(figsize=(5.2, 3.1), layout="constrained")
        ax.set(xlim=(-3.2, 3.2), ylim=(-1.75, 1.75), aspect="equal")
        ax.axis("off")
        ax.set_title("Fetal ventricular atrium · local wall detail")
        for y in (-1.24, 1.0):
            ax.add_patch(plt.Rectangle((-3, y), 6, .24, color="#b7a8aa"))
        markers = [(-1.2, -1.2, 1., "A"), (1.25, 1.25, 1.23, "B")]
        if case == "b":
            markers = [(-1.45, -.45, 1., "A"), (1.25, 1.25, 1., "B")]
        for x0, x1, radius, label in markers:
            ax.plot([x0, x1], [-radius, radius], color="#145a74", lw=2, marker="+", ms=12)
            ax.text(x1+.16, .12, label, weight="bold")
        ax.text(-3, -1.61, "Shaded bands = ventricular walls", fontsize=10)
        save(fig, "perinatal_cal_" + case)


def evidence_studies():
    """Original study displays with explicit denominators, units and comparison groups."""
    for case, observations in [
        ("a", [(2, 1, 0), (4, 0, 1), (6, 2, 0), (8, 1, 0), (10, 1, 0)]),
        ("b", [(2, 0, 2), (4, 1, 0), (6, 0, 1), (8, 1, 0), (10, 0, 1)]),
    ]:
        fig, ax = axes("Follow-up (months)", "Estimated event-free probability")
        times, levels = [0], [1.]
        risk, survival = 8, 1.
        for time, events, censored in observations:
            survival *= 1 - events / risk
            times.append(time)
            levels.append(survival)
            if censored:
                ax.plot(time, survival, marker="+", ms=11, color=COLORS[0])
            risk -= events + censored
        ax.step(times, levels, where="post", color=COLORS[0], lw=2.4)
        ax.axhline(.5, color="#555", ls=":", lw=1)
        ax.set(xlim=(-.15, 10.4), ylim=(0, 1.06), xticks=range(0, 11, 2),
               yticks=[0, .25, .5, .75, 1], title="Event-free survival · 8 participants at entry")
        ax.text(.04, .08, "+  censoring time", transform=ax.transAxes, fontsize=10)
        save(fig, "evidence_km_" + case)

    for case, logs, ses in [
        ("a", [-.30, -.45, -.22], [.11, .18, .13]),
        ("b", [-.55, .42, .10], [.11, .12, .14]),
    ]:
        fig, ax = axes("Risk ratio for an adverse event (log scale)", "")
        for row, (estimate, se) in enumerate(zip(logs, ses)):
            lo, mid, hi = np.exp([estimate-1.96*se, estimate, estimate+1.96*se])
            ax.hlines(row, lo, hi, color=COLORS[0], linewidth=2)
            ax.plot(mid, row, "s", color=COLORS[0], markersize=5 + (.18-se)*40)
        ax.axvline(1, color="#555", ls="--")
        ax.set_xscale("log")
        ax.set(xlim=(.4, 2.2), yticks=[0, 1, 2], yticklabels=["Trial C", "Trial B", "Trial A"],
               xticks=[.5, .75, 1, 1.5, 2], xticklabels=["0.5", "0.75", "1", "1.5", "2"],
               ylim=(-.6, 2.6), title="Three independent trials · 95% confidence intervals")
        ax.minorticks_off()
        save(fig, "evidence_forest_" + case)

    for case, omit in [("a", False), ("b", True)]:
        fig, ax = axes("Estimated treatment effect (mean difference)", "Standard error")
        for se in [.05, .09, .13, .17, .21, .25]:
            for offset in [-1.3, -.4, .4, 1.3]:
                if omit and se >= .16 and offset > 0:
                    continue
                ax.plot(-.3+offset*se, se, "o", ms=5, color=COLORS[0])
        ax.axvline(-.3, ls=":", color="#555")
        ax.set(xlim=(-.7, .1), ylim=(.28, 0), title="Study estimates by precision")
        save(fig, "evidence_funnel_" + case)

    for case, xy in [("a", [(0, 0), (.1, .58), (.25, .82), (.5, .94), (1, 1)]),
                     ("b", [(0, 0), (.05, .35), (.15, .68), (.4, .90), (1, 1)])]:
        fig, ax = axes("False-positive rate", "True-positive rate")
        x, y = zip(*xy)
        ax.plot(x, y, "o-", color=COLORS[0])
        ax.plot([0, 1], [0, 1], "--", color="#999")
        for i, (px, py) in enumerate(xy[1:-1]):
            ax.annotate("ABC"[i], (px, py), xytext=(6, -11), textcoords="offset points")
        ax.set(xlim=(-.03, 1.04), ylim=(-.03, 1.07), title="Candidate test thresholds")
        ax.set_xticks(np.linspace(0, 1, 6))
        ax.set_aspect("equal")
        save(fig, "evidence_roc_" + case)

    for case, title, values in [
        ("a", "Treatment failure · new minus standard", [(-1, -3, 2)]),
        ("b", "Treatment failure · new minus standard", [(1, -2, 5)]),
        ("c", "Symptom change · new minus comparator", [(1, -1, 2)]),
        ("d", "Symptom change · new minus comparator", [(-1, -4, 1)]),
    ]:
        fig, ax = axes("Risk difference (percentage points)" if case in "ab" else "Mean difference (points)", "")
        for mid, lo, hi in values:
            ax.hlines(0, lo, hi, linewidth=3, color=COLORS[0])
            ax.plot(mid, 0, "s", color=COLORS[0])
            ax.text(lo, .18, str(lo), ha="center"); ax.text(hi, .18, str(hi), ha="center")
        ax.axvline(0, color="#888", ls=":")
        for bound in ([4] if case in "ab" else [-3, 3]):
            ax.axvline(bound, color=COLORS[1], ls="--")
        ax.set(xlim=(-6, 6), ylim=(-.6, .8), yticks=[], xticks=range(-6, 7, 2), title=title)
        ax.text(.5, .06, "Dashed lines mark prespecified margins",
                ha="center", transform=ax.transAxes, fontsize=9)
        save(fig, "evidence_margin_" + case)

    for case, y in [("a", [3, 4, 4, 6, 5, 7, 8, 8, 9]),
                    ("b", [11, 7, 4, 2, 1, 2, 4, 7, 11])]:
        fig, ax = axes("Exposure score", "Outcome score")
        ax.scatter(range(1, 10), y, color=COLORS[0], s=42)
        ax.set(xlim=(0, 10), ylim=(0, 12), title="Individual observations")
        save(fig, "evidence_scatter_" + case)

    for case, counts in [("a", [4, 7, 10, 12, 12, 8, 5, 2, 1]),
                         ("b", [18, 17, 16, 11, 8, 3, 2, 1, 1])]:
        fig, ax = axes("Length of stay (days)", "Number of patients")
        ax.bar(range(1, 10), counts, width=.88, color=COLORS[0])
        ax.set(xticks=range(1, 10), title="Discharge cohort · completed stays")
        save(fig, "evidence_stays_" + case)


def evidence_reports():
    """Redraw two published quantitative results and generate independent teaching reports."""
    for name, title, groups, rates, outcome, source in [
        ("dpp", "Diabetes Prevention Program", ["Placebo", "Metformin", "Lifestyle"],
         [11.0, 7.8, 4.8], "New diabetes cases per 100 person-years", "DPP Research Group, 2002"),
        ("sprint", "SPRINT · original randomized comparison", ["Standard target", "Intensive target"],
         [2.19, 1.65], "Primary composite events per 100 person-years", "SPRINT Research Group, 2015"),
    ]:
        fig, ax = plt.subplots(figsize=(6.1, 3.2), layout="constrained")
        bars = ax.barh(groups, rates, color=COLORS[0], height=.55)
        ax.bar_label(bars, labels=[str(x) for x in rates], padding=5)
        ax.set(xlabel=outcome, title=title, xlim=(0, max(rates)*1.2))
        ax.invert_yaxis()
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_xlabel(f"{outcome}\n{source}")
        save(fig, "evidence_" + name)

    for case, cells in [("a", [[72, 8], [18, 102]]), ("b", [[18, 2], [42, 238]])]:
        fig, ax = plt.subplots(figsize=(5.3, 2.4), layout="constrained")
        ax.axis("off")
        ax.set_title("Independent reference assessment in all participants")
        table = ax.table(cellText=[["Reference result", "Test +", "Test −"],
                                   ["Condition present", *cells[0]], ["Condition absent", *cells[1]]],
                         cellLoc="center", colWidths=[.48, .24, .24], loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(11); table.scale(1, 1.8)
        for (row, _), cell in table.get_celld().items():
            cell.set_facecolor("#cfe4e9" if row == 0 else "#f4f8fa")
        save(fig, "evidence_test_" + case)

    for case, counts in [("a", [[10, 100], [30, 100]]), ("b", [[8, 100], [24, 100]])]:
        fig, ax = plt.subplots(figsize=(5.5, 2.6), layout="constrained")
        ax.axis("off")
        ax.set_title("One-year events and participants at risk")
        table = ax.table(cellText=[["Age stratum", "Events", "Participants"],
                                   ["18–64 years", *counts[0]], ["65+ years", *counts[1]]],
                         cellLoc="center", colWidths=[.38, .25, .33], loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(11); table.scale(1, 1.8)
        for (row, _), cell in table.get_celld().items():
            cell.set_facecolor("#cfe4e9" if row == 0 else "#f4f8fa")
        save(fig, "evidence_age_" + case)


def population_and_decision_figures():
    """Age distributions and diagnostic probabilities in contrasting example populations."""
    for case, men, women in [("a", [17, 16, 15, 12, 8], [16, 15, 14, 12, 9]),
                                 ("b", [8, 10, 14, 16, 15], [8, 10, 14, 17, 17])]:
        fig, ax = axes("Residents (thousands)", "Age (years)")
        labels = ["0–19", "20–39", "40–59", "60–79", "80+"]
        ax.barh(labels, -np.array(men), label="Men", color=COLORS[0])
        ax.barh(labels, women, label="Women", color=COLORS[1])
        ax.set(xticks=[-20, -10, 0, 10, 20], xticklabels=[20, 10, 0, 10, 20],
               xlim=(-20, 20), title="Population by age group and sex")
        ax.legend(loc="upper center", bbox_to_anchor=(.5, -.2), ncol=2)
        save(fig, "evidence_pyramid_" + case)

    for case, disease, sensitivity, false_positive in [
        ("a", .10, .80, .10), ("b", .30, .80, .10)
    ]:
        fig, ax = plt.subplots(figsize=(6.0, 3.4), layout="constrained")
        ax.axis("off"); ax.set(xlim=(0, 1.05), ylim=(0, 1))
        ax.set_title("Diagnostic pathways · probabilities on branches")
        for y, prevalence, status, pos in [(.72, disease, "Disease", sensitivity),
                                           (.28, 1-disease, "No disease", false_positive)]:
            ax.plot([.08, .38], [.5, y], color="#758996")
            ax.text(.18, (.5+y)/2+.025, f"{prevalence:.0%}", ha="center")
            ax.text(.39, y, status, ha="left", va="center")
            for end, p, name in [(y+.12, pos, "Test positive"), (y-.12, 1-pos, "Test negative")]:
                ax.plot([.60, .82], [y, end], color="#758996")
                ax.text(.71, (y+end)/2+.018, f"{p:.0%}", ha="center")
                ax.text(.83, end, name, va="center")
        save(fig, "evidence_tree_" + case)


def hypothesis_error_regions():
    """Areas under two prespecified sampling distributions in a one-sided test."""
    from math import sqrt, pi
    x = np.linspace(-4, 6, 601)
    cutoff = 1.645
    null = np.exp(-x**2 / 2) / sqrt(2*pi)
    alternative = np.exp(-(x-2.5)**2 / 2) / sqrt(2*pi)
    for case in ("a", "b"):
        fig, ax = axes("Standardized estimate", "Density")
        ax.plot(x, null, color=COLORS[0], label="Null")
        ax.plot(x, alternative, ls="--", color=COLORS[1], label="Alternative")
        if case == "a":
            ax.fill_between(x, 0, null, where=x >= cutoff, color=COLORS[0], alpha=.55)
        else:
            ax.fill_between(x, 0, alternative, where=x < cutoff, color=COLORS[1], alpha=.55)
        ax.axvline(cutoff, color="#333", ls=":", lw=1.8)
        ax.set(xlim=(-3.7, 5.7), ylim=(0, .5), title="Reject the null to the right of the dotted line")
        ax.legend(loc="upper right")
        save(fig, "evidence_tails_" + case)


def agreement_figures():
    """Original paired-method data shown as differences versus means."""
    means = np.arange(10, 91, 10)
    noise = np.array([-.4, .2, .4, -.2, 0, .3, -.3, .2, -.2])
    for case, differences in [("a", 8+noise), ("b", .12*means+noise)]:
        fig, ax = axes("Mean of the two measurements (units)", "New minus reference (units)")
        ax.scatter(means, differences, color=COLORS[0], s=45)
        ax.axhline(0, color="#555", ls=":")
        ax.set(xlim=(0, 100), ylim=(-1, 13), title="Agreement of two measurement methods")
        save(fig, "evidence_agreement_" + case)


def immune_reports():
    """Synthetic laboratory reports and idealized gated neutrophil fluorescence."""
    panels = {
        "classic": ("Complement activity", ("CH50", "AH50"), ("Absent", "Normal")),
        "alt": ("Complement activity", ("CH50", "AH50"), ("Normal", "Absent")),
        "both": ("Complement activity", ("CH50", "AH50"), ("Absent", "Absent")),
        "normal": ("Complement activity", ("CH50", "AH50"), ("Normal", "Normal")),
        "hiv_pending": ("HIV testing", ("HIV-1/2 Ag/Ab screen", "Antibody differentiation"),
                        ("Reactive", "Negative")),
        "hiv_false": ("HIV testing", ("HIV-1/2 Ag/Ab screen", "Antibody differentiation", "HIV-1 RNA"),
                      ("Reactive", "Negative", "Not detected")),
    }
    for name, (title, analytes, results) in panels.items():
        fig, ax = plt.subplots(figsize=(5.1, 2.4), layout="constrained")
        ax.axis("off")
        ax.set_title(f"{title}  •  simulated patient report", fontsize=12)
        table = ax.table(cellText=list(zip(analytes, results)), colLabels=["Test", "Laboratory result"],
                         cellLoc="left", colLoc="left", loc="center", colWidths=[0.52, 0.45])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.55)
        save(fig, "immune_" + name)

    for name, values in [("iga", (1120, 3, 122)), ("multi", (285, 5, 110))]:
        fig, ax = plt.subplots(figsize=(5.1, 2.4), layout="constrained")
        ax.axis("off")
        ax.set_title("Serum immunoglobulins  •  simulated adult report", fontsize=12)
        rows = list(zip(["IgG", "IgA", "IgM"], values, ["700–1600", "70–400", "40–230"]))
        table = ax.table(cellText=rows, colLabels=["Analyte", "mg/dL", "Lab interval (mg/dL)"],
                         cellLoc="center", loc="center", colWidths=[0.23, 0.23, 0.47])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        save(fig, "immune_" + name)

    x = np.linspace(0, 4, 400)
    dim = np.exp(-0.5 * ((x - 0.8) / 0.21) ** 2)
    bright = np.exp(-0.5 * ((x - 3.05) / 0.27) ** 2)
    for name, response in [("low", dim), ("normal", bright), ("mosaic", 0.55 * dim + 0.45 * bright)]:
        fig, axes_pair = plt.subplots(2, 1, sharex=True, figsize=(5.2, 3.5), layout="constrained")
        for ax, label, curve in zip(axes_pair, ["Control", "Patient"], [bright, response]):
            ax.fill_between(x, dim, color="#aaa", alpha=0.45, label="Resting")
            ax.plot(x, curve, color=COLORS[0], lw=2.5, label="Stimulated")
            ax.set(yticks=[], ylabel=label, ylim=(0, 1.15))
        axes_pair[0].legend(loc="upper center", fontsize=8)
        axes_pair[1].set_xlabel("DHR fluorescence (log scale, arbitrary units)")
        axes_pair[1].set_xticks([0, 1, 2, 3, 4], ["1", "10", "100", "1,000", "10,000"])
        fig.suptitle("Neutrophil fluorescence distributions  •  simulated")
        save(fig, "immune_burst_" + name)


def musculoskeletal_reports():
    reports = {
        "dxa_low": ("Bone densitometry", ["Site", "T-score"],
                    [("Lumbar spine", "−1.5"), ("Total hip", "−2.1"), ("Femoral neck", "−2.7")]),
        "dxa_mid": ("Bone densitometry", ["Site", "T-score"],
                    [("Lumbar spine", "−0.9"), ("Total hip", "−1.8"), ("Femoral neck", "−2.2")]),
        "dxa_young": ("Lumbar spine densitometry", ["Reference comparison", "Score"],
                      [("Young adult reference (T)", "−2.7"), ("Age-matched reference (Z)", "−2.1")]),
        "press_rise": ("Limb perfusion measurements", ["Time", "Diastolic BP", "Compartment"],
                       [("09:00", "72 mm Hg", "28 mm Hg"), ("09:30", "70 mm Hg", "38 mm Hg"),
                        ("10:00", "70 mm Hg", "48 mm Hg")]),
        "press_fall": ("Limb perfusion measurements", ["Time", "Diastolic BP", "Compartment"],
                       [("13:10", "80 mm Hg", "33 mm Hg"), ("13:40", "68 mm Hg", "35 mm Hg"),
                        ("14:10", "52 mm Hg", "34 mm Hg")]),
        "joint_mixed": ("Synovial fluid report", ["Study", "Result"],
                        [("Leukocytes", "42,000/µL"), ("Crystals", "Needles, negative birefringence"),
                         ("Gram stain", "No organisms seen"), ("Bacterial culture", "Pending")]),
        "joint_gram": ("Synovial fluid report", ["Study", "Result"],
                       [("Leukocytes", "96,000/µL"), ("Gram stain", "Gram-positive cocci"),
                        ("Crystals", "None seen"), ("Bacterial culture", "Pending")]),
        "joint_cpp": ("Synovial fluid report", ["Study", "Result"],
                      [("Shape", "Short rods and rhomboids"), ("Birefringence", "Weak, positive"),
                       ("Bacterial culture", "Pending")]),
        "statin_high": ("Patient with new dark urine", ["Laboratory test", "Measured", "Usual / baseline"],
                        [("CK", "18,400 U/L", "40–200 U/L"), ("Creatinine", "2.3 mg/dL", "0.9 mg/dL*")]),
    }
    for name, (title, columns, rows) in reports.items():
        fig, ax = plt.subplots(figsize=(6.1, 2.7), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated report", fontsize=13)
        table = ax.table(cellText=rows, colLabels=columns, cellLoc="center", loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.6)
        if name == "statin_high":
            ax.text(0.99, 0.03, "* Patient's previous creatinine", ha="right", transform=ax.transAxes)
        save(fig, "msk_" + name)

    for name, active, passive in [("weak", [45, 35], [165, 75]), ("stiff", [65, 10], [75, 15])]:
        fig, ax = plt.subplots(figsize=(5.4, 3.4), layout="constrained")
        y = np.array([1, 0])
        for offset, values, label, color in [(.17, active, "Active", COLORS[0]),
                                             (-.17, passive, "Passive", COLORS[1])]:
            bars = ax.barh(y + offset, values, height=.28, color=color, label=label)
            ax.bar_label(bars, fmt="%g°", padding=3)
        ax.set(yticks=y, yticklabels=["Elevation", "External rotation"], xlim=(0, 190),
               xlabel="Range of motion (degrees)", title="Shoulder examination  •  simulated")
        ax.legend(loc="lower right")
        save(fig, "msk_rom_" + name)


def musculoskeletal_studies():
    for name, upper, lower in [("opposite", 14, -10), ("same", 26, 4)]:
        fig, ax = plt.subplots(figsize=(5.1, 3.4), layout="constrained")
        for y, angle, label in [(2, upper, "Superior"), (0, lower, "Inferior")]:
            x = np.array([-1.4, 1.4])
            dy = np.tan(np.deg2rad(angle)) * x
            ax.plot(x, [y, y], "--", color="#777", lw=1)
            ax.plot(x, y + dy, color=COLORS[0], lw=3)
            ax.text(1.52, y, f"{label}\n{angle:+d}°", va="center", fontsize=11)
        ax.set(xlim=(-1.6, 2.7), ylim=(-.6, 2.9), aspect="equal", title="Selected endplates  •  schematic")
        ax.axis("off")
        ax.text(-1.45, -.47, "Dashed lines = horizontal reference", fontsize=9)
        save(fig, "msk_curve_" + name)

    for name, negative in [("pos", False), ("neg", True)]:
        fig, ax = plt.subplots(figsize=(5, 3.1), layout="constrained")
        ax.set_facecolor("#b73973")
        for cx, cy, vertical in [(1, 1.5, False), (2, 2.4, True), (3.2, .9, True),
                                 (4.1, 2.15, False), (5.25, 1.25, True)]:
            if negative:
                shape = np.array([[-.70, 0], [0, .055], [.70, 0], [0, -.055]])
            else:
                shape = np.array([[-.60, -.12], [.30, -.12], [.60, .12], [-.30, .12]])
            if vertical:
                shape = np.column_stack([-shape[:, 1], shape[:, 0]])
            color = "#f9d44c" if negative != vertical else "#77cfff"
            ax.fill(shape[:, 0] + cx, shape[:, 1] + cy, fc=color, ec="#283741", lw=1)
        ax.set(xlim=(0, 6), ylim=(0, 3.3), aspect="equal", xticks=[], yticks=[],
               title="Compensated polarized light  •  schematic")
        ax.set_xlabel("Slow axis of compensator   ⟷   horizontal")
        save(fig, "msk_cryst_" + name)

    for name, covered in [("a", 12), ("b", 7)]:
        fig, ax = plt.subplots(figsize=(5.2, 3.2), layout="constrained")
        head = plt.Circle((10, 0), 10, facecolor="#e4f2f6", edgecolor=COLORS[0], lw=2)
        ax.add_patch(head)
        ax.plot([covered, covered], [-10, 12], ls="--", color=COLORS[1])
        ax.text(covered, 12.3, "Bony rim", ha="center", fontsize=9)
        for y, end, label in [(0, covered, f"Covered: {covered} mm"), (-13, 20, "Entire head: 20 mm")]:
            ax.annotate("", (end, y), (0, y), arrowprops={"arrowstyle": "<->", "lw": 1.8})
            ax.text(end/2, y+1, label, ha="center", fontsize=9, backgroundcolor="white")
        ax.set(xlim=(-2, 22), ylim=(-15, 15), aspect="equal", title="Femoral head coverage  •  coronal schematic")
        ax.axis("off")
        save(fig, "msk_cover_" + name)

    fig, ax = axes("Time at constant workload (min)", "Heart rate (beats/min)")
    ax.plot([0, 2, 4, 6, 8, 10, 12, 14], [80, 132, 158, 162, 139, 127, 124, 124],
            marker="o", lw=2.4, color=COLORS[0])
    ax.set_title("Constant-load exercise test  •  simulated")
    ax.annotate("Symptoms ease", (10, 127), (8, 100), arrowprops={"arrowstyle": "->"})
    save(fig, "msk_second_wind")

    fig, (top, bottom) = plt.subplots(2, 1, figsize=(5.1, 3.7), sharex=True, layout="constrained")
    minutes = [0, 2, 4, 6, 8]
    top.plot(minutes, [37, 41, 48, 59, 72], marker="o", color=COLORS[0])
    bottom.plot(minutes, [83, 94, 110, 124, 141], marker="s", color=COLORS[1])
    top.set(ylabel="End-tidal CO₂\n(mm Hg)", title="Operating room trends  •  simulated")
    bottom.set(ylabel="Heart rate\n(beats/min)", xlabel="Time (min)", xticks=minutes)
    save(fig, "msk_mh_monitor")


def cutaneous_studies():
    """Draw independent simulated observations for skin interpretation cards."""
    for name, temperatures, onset in [
        ("a", [39.5, 40.0, 39.8, 37.0, 36.9, 37.1], 4),
        ("b", [38.0, 38.6, 39.2, 40.1, 39.7, 38.8], 4),
    ]:
        fig, ax = axes("Day of illness", "Temperature (°C)")
        days = range(1, len(temperatures) + 1)
        ax.plot(days, temperatures, marker="o", lw=2.5, color=COLORS[0])
        ax.axvline(onset, color=COLORS[1], ls="--", label="Rash first observed")
        ax.set(xticks=list(days), ylim=(36.3, 40.7), title="Temperature diary  •  simulated")
        ax.legend(loc="lower left")
        save(fig, "skin_fever_" + name)

    for name, intervals in [("a", [(0, 5), (6, 14), (17, 23)]),
                            ("b", [(0, 36), (12, 19), (22, 29)])]:
        fig, ax = axes("Hours since first lesion appeared", "")
        for row, (start, end) in enumerate(intervals):
            ax.plot([start, end], [row, row], marker="|", markersize=14, lw=4, color=COLORS[0])
            ax.text((start + end) / 2, row + 0.15, f"{start}–{end} h", ha="center", fontsize=10)
        ax.set(yticks=[0, 1, 2], yticklabels=["Left wrist", "Right hip", "Left calf"],
               xlim=(-2, 39), ylim=(-0.4, 2.6), title="Time each lesion was visible  •  simulated")
        save(fig, "skin_wheal_" + name)

    for name, quantities in [("a", [4, 3, 28]), ("b", [19, 15, 8]), ("c", [10, 8, 20])]:
        fig, ax = axes("Percentage of total body surface", "")
        bars = ax.barh(["Detached", "Detachable", "Fixed erythema"], quantities,
                       color=[COLORS[0], "#467987", "#999999"])
        ax.bar_label(bars, labels=[f"{q}%" for q in quantities], padding=5)
        ax.invert_yaxis()
        ax.set(xlim=(0, 35), title="Skin examination  •  nonoverlapping areas")
        save(fig, "skin_detach_" + name)

    for name, regions in [
        ("a", [("Entire right arm", "Partial thickness"), ("Entire anterior trunk", "Superficial")]),
        ("b", [("Entire left arm", "Full thickness"), ("Entire right leg", "Partial thickness")]),
    ]:
        fig, ax = plt.subplots(figsize=(5.1, 2.2), layout="constrained")
        ax.axis("off")
        ax.set_title("Adult burn survey  •  simulated", pad=6)
        table = ax.table(cellText=regions, colLabels=["Region involved", "Depth on examination"],
                         cellLoc="left", colLoc="left", bbox=[0, 0.05, 1, 0.85])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(2):
            table[0, col].set_facecolor("#dcecf2")
        save(fig, "skin_burn_" + name)


def behavioral_courses():
    """Render independent, simulated clinical records for course interpretation."""
    def intervals(name, title, xlabel, xmax, labels, spans, ticks):
        fig, ax = axes(xlabel, "")
        for row, periods in enumerate(spans):
            for start, finish in periods:
                ax.barh(row, finish - start, left=start, height=0.35,
                        color=COLORS[row % len(COLORS)])
        ax.set(yticks=range(len(labels)), yticklabels=labels, ylim=(len(labels)-0.5, -0.5),
               xlim=(0, xmax), xticks=ticks, title=title)
        ax.set_axisbelow(True)
        save(fig, "bh_" + name)

    for name, mood_start, voices_end in [("a", 0, 6), ("b", 4, 10)]:
        intervals("course_" + name, "Complete illness record  •  simulated",
                  "Weeks since illness onset", 12, ["Major depression", "Hallucinations"],
                  [[(mood_start, 12)], [(0, voices_end)]], range(0, 13, 2))

    for name, vocals in [("a", [(12, 16)]), ("b", [])]:
        intervals("tic_" + name, "All recorded tics since onset  •  simulated",
                  "Months since first tic", 18, ["Eye blinking", "Shoulder jerk", "Throat clearing"],
                  [[(0, 10), (14, 18)] if name == "b" else [(0, 10)],
                   [(2, 11), (16, 18)] if name == "b" else [(2, 11)], vocals], range(0, 19, 2))

    for name, baseline in [("a", 0.4), ("b", 2.7)]:
        days = np.arange(1, 61)
        cycle_day = (days - 1) % 28 + 1
        scores = baseline + (4.6-baseline) * np.clip((cycle_day - 18)/7, 0, 1)
        scores += 0.15*np.sin(days*1.6)
        fig, ax = axes("Diary day", "Mood symptom burden\n(0 = none, 5 = severe)")
        ax.plot(days, scores, lw=2.4, color=COLORS[0])
        for start in [1, 29, 57]:
            ax.axvspan(start, start + 4, color=COLORS[1], alpha=.17,
                       label="Menstrual bleeding" if start == 1 else None)
        ax.set(ylim=(0, 5.2), xlim=(1, 60), xticks=[1, 7, 14, 21, 29, 35, 42, 49, 57],
               title="Two-cycle daily mood diary  •  simulated")
        ax.legend(loc="upper left", fontsize=8)
        save(fig, "bh_cycle_" + name)

    for name, ph, co2, hco3 in [("a", "7.51", "27", "21"), ("b", "7.26", "23", "10")]:
        fig, ax = plt.subplots(figsize=(5.2, 2.5), layout="constrained")
        ax.axis("off")
        ax.set_title("Arterial blood gas  •  simulated")
        table = ax.table(cellText=[["pH", ph, "7.35–7.45"], ["PaCO₂ (mm Hg)", co2, "35–45"],
                                   ["HCO₃⁻ (mmol/L)", hco3, "22–26"]],
                         colLabels=["Measurement", "Result", "Reference interval"],
                         cellLoc="left", colLoc="left", bbox=[0, 0.05, 1, 0.85])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(3):
            table[0, col].set_facecolor("#dcecf2")
        save(fig, "bh_abg_" + name)

    for name, phosphate in [("a", [3.3, 2.8, 2.0, 1.3]), ("b", [3.2, 3.3, 3.1, 3.2])]:
        fig, ax = axes("Hours since feeds began", "Serum phosphate (mg/dL)")
        ax.axhspan(2.5, 4.5, alpha=.13, color=COLORS[0], label="Adult reference interval")
        ax.plot([0, 8, 16, 24], phosphate, marker="o", lw=2.4, color=COLORS[1])
        ax.set(ylim=(0.8, 4.9), xticks=[0, 8, 16, 24], title="Adult nutritional rehabilitation  •  simulated")
        ax.legend(loc="upper right", fontsize=8)
        save(fig, "bh_phos_" + name)

    for name, values in [("a", [5, 14, 15, 14]), ("b", [5, 15, 11, 6])]:
        fig, ax = axes("Minutes after naloxone", "Respiratory rate (breaths/min)")
        ax.plot([0, 3, 10, 20], values, marker="o", lw=2.4, color=COLORS[0])
        ax.set(xticks=[0, 3, 10, 20], yticks=[3, 6, 9, 12, 15, 18], ylim=(2, 20),
               title="Observed breathing after opioid reversal  •  simulated")
        ax.text(0.98, 0.07, "Depth at 20 min: " + ("adequate" if name == "a" else "shallow"),
                transform=ax.transAxes, ha="right", fontsize=9, backgroundcolor="white")
        save(fig, "bh_resp_" + name)


def urology_studies():
    """Render simulated patient measurements used in reproductive-system cases."""
    def lab_panel(name, title, rows, reference="Reference"):
        fig, ax = plt.subplots(figsize=(5.25, 2.45), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated")
        table = ax.table(cellText=rows, colLabels=["Measurement", "Result", reference],
                         colWidths=[0.47, 0.26, 0.27], cellLoc="left", colLoc="left",
                         bbox=[0, 0.05, 1, 0.83])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(3):
            table[0, col].set_facecolor("#dcecf2")
        save(fig, "male_" + name)

    for name, lh, fsh in [("a", "21", "26"), ("b", "0.6", "0.8")]:
        lab_panel("axis_" + name, "Morning hormone results confirmed on repeat",
                  [["Testosterone (ng/dL)", "145", "300–900"],
                   ["LH (IU/L)", lh, "1.5–9.3"], ["FSH (IU/L)", fsh, "1.4–18"]])

    for name, volume, count, motility in [("a", "2.0", "24", "50"), ("b", "0.8", "30", "25")]:
        lab_panel("semen_" + name, "Semen analysis  •  complete collection",
                  [["Volume", volume, "mL"], ["Concentration", count, "million/mL"],
                   ["Total motility", motility, "%"]], reference="Units")

    for name, ph, oxygen, co2 in [("a", "7.12", "18", "78"), ("b", "7.40", "97", "40")]:
        lab_panel("gas_" + name, "Initial corporal gas before intervention",
                  [["pH", ph, "7.35–7.45"], ["PO₂ (mm Hg)", oxygen, "80–100"],
                   ["PCO₂ (mm Hg)", co2, "35–45"]], reference="Arterial range")

    for name, initial, final in [("a", 32, 8), ("b", 16, 8)]:
        fig, ax = axes("Months after treatment", "RPR dilution titer")
        ax.plot([0, 6], [initial, final], marker="o", lw=2.4, color=COLORS[0])
        ax.set_yscale("log", base=2)
        dilutions = [2, 4, 8, 16, 32, 64]
        ax.set(yticks=dilutions, yticklabels=[f"1:{d}" for d in dilutions],
               xticks=[0, 6], xlim=(-0.5, 6.5), ylim=(1.8, 70),
               title="Quantitative RPR  •  same assay and laboratory")
        save(fig, "male_rpr_" + name)

    for name, values in [("a", [160, 80, 40, 20]), ("b", [160, 84, 83, 115])]:
        fig, ax = axes("Days after orchiectomy", "Serum AFP (ng/mL)")
        ax.plot([0, 6, 12, 18], values, marker="o", lw=2.4, color=COLORS[0])
        for x, y in zip([0, 6, 12, 18], values):
            ax.annotate(str(y), (x, y), xytext=(0, 7), textcoords="offset points", ha="center")
        ax.set(xticks=[0, 6, 12, 18], ylim=(0, 195), title="Serial tumor marker  •  simulated")
        save(fig, "male_afp_" + name)

    for name, left in [("a", [10, 11]), ("b", [10, 15])]:
        fig, ax = axes("Months after initial ultrasound", "Testicular volume (mL)")
        for values, label, marker, color in [(left, "Left (varicocele)", "o", COLORS[0]),
                                             ([14, 16], "Right", "s", COLORS[1])]:
            ax.plot([0, 6], values, label=label, marker=marker, lw=2.4, color=color)
            for x, y in zip([0, 6], values):
                ax.annotate(str(y), (x, y), xytext=(8 if x else -8, 0),
                            textcoords="offset points", va="center", ha="left" if x else "right")
        ax.set(xlim=(-0.8, 6.8), xticks=[0, 6], ylim=(6, 18),
               title="Serial ultrasound volumes  •  simulated")
        ax.legend(loc="lower right", fontsize=8)
        save(fig, "male_vol_" + name)

    for name, values in [("a", [4.0, 2.0, 2.0, 2.8, 3.0]), ("b", [4.0, 2.1, 2.0, 2.0, 2.0])]:
        fig, ax = axes("Months on continuous finasteride", "Serum PSA (ng/mL)")
        ax.plot([0, 6, 12, 18, 21], values, marker="o", lw=2.4, color=COLORS[0])
        ax.set(xticks=[0, 6, 12, 18, 21], ylim=(1.5, 4.5), title="PSA after starting therapy  •  simulated")
        save(fig, "male_psa_" + name)


def preventive_care_studies():
    """Draw practice records. Only the boys' reference percentiles are population data."""
    # WHO Child Growth Standards, simplified head circumference-for-age table for boys.
    months = [0, 2, 4, 6, 9, 12]
    for name, child in [("rise", [34.5, 39.5, 43.4, 46.6]),
                        ("track", [34.6, 39.1, 41.7, 43.4])]:
        fig, ax = axes("Age (months)", "Head circumference (cm)")
        for label, values, style in [
            ("P3", [32.1, 36.9, 39.4, 41.0, 42.6, 43.6], ":"),
            ("Median", [34.5, 39.1, 41.6, 43.3, 45.0, 46.1], "-"),
            ("P97", [36.9, 41.3, 43.9, 45.6, 47.4, 48.5], "--"),
        ]:
            ax.plot(months, values, ls=style, lw=1.7, color="#526677", label=label)
        ax.plot(months[:4], child, "o-", color=COLORS[1], lw=2.2, label="Patient")
        ax.annotate(f"{child[-1]:.1f}", (6, child[-1]), xytext=(5, -11),
                    textcoords="offset points", color=COLORS[1])
        ax.set(title="Head growth  •  term boy, simulated record", xticks=months)
        ax.legend(loc="lower right", fontsize=8, ncol=2)
        save(fig, "dev_hc_" + name)

    for name, hours in [("short", [6, 6.5, 6, 6.5, 6, 9, 9.5]),
                        ("full", [8.5, 8, 9, 8.5, 8, 9, 9.5])]:
        fig, ax = axes("", "Actual sleep (hours)")
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        ax.bar(days, hours, color=COLORS[0])
        for day, duration in enumerate(hours):
            ax.text(day, duration + .12, f"{duration:g}", ha="center", fontsize=9)
        ax.set(title="Adolescent sleep diary  •  simulated week", ylim=(0, 10.5))
        save(fig, "dev_sleep_" + name)

    def record(name, title, columns, rows, widths):
        fig, ax = plt.subplots(figsize=(5.5, 2.7), layout="constrained")
        ax.axis("off")
        ax.set_title(title, fontsize=13)
        table = ax.table(cellText=rows, colLabels=columns, colWidths=widths,
                         cellLoc="left", colLoc="left", bbox=[0, .05, 1, .84])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#dcecf2")
        save(fig, "dev_" + name)

    for name, moderate, vigorous, strength in [("high", 100, 30, 1), ("low", 90, 10, 2)]:
        record("activity_" + name, "Adult weekly activity  •  simulated log",
               ["Activity", "Week total"],
               [["Moderate aerobic activity", f"{moderate} min"],
                ["Vigorous aerobic activity", f"{vigorous} min"],
                ["Strength training", f"{strength} day" if strength == 1 else f"{strength} days"]],
               [.63, .37])

    for name, pressures in [
        ("sys", ["144/78", "120/74", "120/74"]),
        ("dia", ["138/80", "126/68", "126/68"]),
        ("small", ["132/78", "124/74", "124/74"]),
        ("sx", ["138/80", "130/74", "126/74"]),
    ]:
        record("bp_" + name, "Postural blood pressure  •  simulated test",
               ["Position and elapsed time", "BP (mm Hg)"],
               list(zip(["Supine after 5 min", "Standing at 1 min", "Standing at 3 min"], pressures)),
               [.63, .37])

    tasks = ["Bathing", "Dressing", "Taking medicines", "Paying bills"]
    for name, assisted in [("bills", "Paying bills"), ("bath", "Bathing")]:
        record("func_" + name, "Usual daily function  •  simulated interview",
               ["Task", "Current performance"],
               [[task, "Needs help" if task == assisted else "Independent"] for task in tasks],
               [.5, .5])

    for name, first, second, a, b in [("soup", "A", "B", 300, 450), ("soup_alt", "C", "D", 260, 480)]:
        record(name, "Two packaged soups  •  simulated labels",
               ["Label entry", "Soup " + first, "Soup " + second],
               [["Servings per container", "2", "1"], ["Sodium per serving", f"{a} mg", f"{b} mg"]],
               [.52, .24, .24])


def multisystem_physiology():
    """Render simulated case records for fluid, electrolyte and shock decisions."""
    def record(name, title, columns, rows, widths=(.46, .22, .32)):
        fig, ax = plt.subplots(figsize=(5.85, 2.85), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated", fontsize=12)
        table = ax.table(cellText=rows, colLabels=columns, colWidths=widths,
                         cellLoc="left", colLoc="left", bbox=[0, .04, 1, .84])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#dcecf2")
        save(fig, "msys_" + name)

    for name, co2 in [("fit", 26), ("low", 18), ("high", 40)]:
        bicarb = 12
        ph = 6.1 + np.log10(bicarb / (.03 * co2))
        record("gas_" + name, "Arterial blood gas", ["Arterial sample", "Result", "Usual interval"],
               [["pH", f"{ph:.2f}", "7.35–7.45"], ["PaCO₂ (mm Hg)", co2, "35–45"],
                ["HCO₃⁻ (mmol/L)", bicarb, "22–26"]])

    for name, sodium, chloride in [("hi", 140, 102), ("norm", 138, 116)]:
        record("gap_" + name, "Serum chemistry", ["Measurement", "Result", "Unit"],
               [["Sodium", sodium, "mmol/L"], ["Chloride", chloride, "mmol/L"],
                ["Bicarbonate", 12, "mmol/L"], ["Lab gap, no K", "8–12", "mmol/L"]],
               (.5, .20, .30))
    for name, value in [("low", 8), ("high", 54)]:
        record("cl_" + name, "Simultaneous blood and urine", ["Measurement", "Result", "Unit"],
               [["Arterial pH", "7.50", "—"], ["Serum bicarbonate", 35, "mmol/L"],
                ["Spot urine chloride", value, "mmol/L"]])

    for name, amounts in [("pos", [1100, 1900, 1000, 400]), ("neg", [900, 600, 850, 1750])]:
        record("io_" + name, "24-hour intake and measured output", ["Direction", "Source", "Volume (mL)"],
               list(zip(["Intake", "Intake", "Output", "Output"],
                        ["Oral", "IV", "Urine", "Gastrointestinal"], amounts)),
               (.28, .44, .28))

    for name, peak in [("rise", 60), ("flat", 51)]:
        fig, ax = axes("Time from start of maneuver (s)", "Stroke volume (mL)")
        times = [-30, 0, 30, 60, 90, 120]
        values = [50, 50, peak, peak, 50, 50]
        ax.axvspan(0, 60, color="#e0edf1", label="Legs raised")
        ax.plot(times, values, "o-", color=COLORS[0], lw=2)
        for j in (0, 2):
            ax.annotate(str(values[j]), (times[j], values[j]), xytext=(0, 7),
                        textcoords="offset points", ha="center")
        ax.set(title="Passive leg raise  •  simulated stroke volume", xticks=times, ylim=(46, 65))
        ax.legend(loc="upper right", fontsize=9)
        save(fig, "msys_plr_" + name)

    for name, wedge, ci in [("pump", 26, "1.6"), ("loss", 4, "1.5")]:
        record("hemo_" + name, "Invasive hemodynamics", ["Measurement", "Result", "Resting interval"],
               [["Wedge pressure (mm Hg)", wedge, "6–12"], ["Cardiac index (L/min/m²)", ci, "2.5–4.0"]],
               (.55, .16, .29))
    for name, uosm, una in [("dil", 65, 12), ("con", 490, 65)]:
        record("osm_" + name, "Paired serum and urine samples", ["Measurement", "Serum", "Urine"],
               [["Sodium (mmol/L)", 122, una], ["Osmolality (mOsm/kg)", 260, uosm]])
    for name, uosm, vol in [("con", 880, "0.8"), ("dil", 105, "5.8")]:
        record("ton_" + name, "Water balance over 24 hours", ["Measurement", "Result", "Unit"],
               [["Serum sodium", 153, "mmol/L"], ["Serum osmolality", 315, "mOsm/kg"],
                ["Urine osmolality", uosm, "mOsm/kg"], ["24-hour urine", vol, "L"]])
    for name, ion, alb in [("bound", "1.20", "2.1"), ("ion", "0.88", "4.0")]:
        record("ca_" + name, "Serum calcium fractions", ["Measurement", "Result", "Lab interval"],
               [["Total calcium (mg/dL)", "7.6", "8.5–10.5"], ["Ionized calcium (mmol/L)", ion, "1.15–1.30"],
                ["Albumin (g/dL)", alb, "3.5–5.0"]], (.56, .16, .28))
    for name, urine, oxygen in [("good", [12, 48], [5, 2]), ("bad", [24, 8], [2, 5])]:
        record("org_" + name, "Serial bedside observations", ["Measurement", "Hour 0", "Hour 4"],
               [["MAP (mm Hg)", 56, 70], ["Urine output (mL/h)", *urine],
                ["Nasal O₂ flow (L/min)", *oxygen]], (.56, .22, .22))


def multisystem_genetic_studies():
    """Draw simulated genetic, biochemical and electrophysiologic case records."""
    def report(name, title, columns, rows, widths):
        fig, ax = plt.subplots(figsize=(5.8, 2.65), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated", fontsize=12)
        table = ax.table(cellText=rows, colLabels=columns, colWidths=widths,
                         cellLoc="left", colLoc="left", bbox=[0, .04, 1, .83])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#dcecf2")
        save(fig, "mgen_" + name)

    for name, values in [("hi", [73, 69]), ("mid", [46, 52])]:
        report("sweat_" + name, "Quantitative sweat chloride",
               ["Collection", "Chloride (mmol/L)", "Sample quality"],
               [[f"Visit {n}", v, "Adequate"] for n, v in enumerate(values, 1)], [.26, .39, .35])
    for name, paternal in [("mat", "Absent"), ("both", "Present")]:
        report("imp_" + name, "SNRPN methylation assay",
               ["Patient signal", "Result", "Assay control"],
               [["Methylated (maternal)", "Present", "Valid"],
                ["Unmethylated (paternal)", paternal, "Valid"]], [.54, .20, .26])
    for name, copies in [("del", 1), ("two", 2)]:
        report("dos_" + name, "Chromosome 15 critical region",
               ["Study", "Patient finding"],
               [["Methylation", "Maternal-only pattern"],
                ["Genomic dosage", f"{copies} " + ("copy" if copies == 1 else "copies")]],
               [.48, .52])
    for name, hex_b in [("a", 105), ("ab", 3)]:
        fig, ax = axes("", "Activity (% of control mean)")
        ax.axhspan(70, 130, color="#ddebdc", label="Lab reference band")
        values = [2, hex_b]
        ax.bar(["Hex A", "Hex B"], values, width=.46, color=COLORS[0])
        for pos, value in enumerate(values):
            ax.text(pos, value + 3, str(value), ha="center")
        ax.set(title="Leukocyte isoenzyme activities  •  simulated", ylim=(0, 155))
        ax.legend(loc="upper center", fontsize=8)
        save(fig, "mgen_hex_" + name)

    for name, value in [("hi", 82), ("norm", 2)]:
        report("orot_" + name, "Neonatal urine metabolic panel",
               ["Analyte", "Result", "Lab interval"],
               [["Orotic acid (mmol/mol Cr)", str(value), "0–4"]], [.48, .20, .32])
    for name, sat, ferr, crp in [("high", 81, 760, 2), ("infl", 22, 810, 92)]:
        report("iron_" + name, "Serum iron and inflammatory indices",
               ["Analyte", "Result", "Lab interval"],
               [["Transferrin saturation (%)", sat, "20–45"], ["Ferritin (ng/mL)", ferr, "30–300"],
                ["CRP (mg/L)", crp, "<5"]], [.56, .16, .28])
    for name, peak in [("big", 4.4), ("small", 2.2)]:
        fig, ax = axes("", "CMAP amplitude (mV)")
        ax.bar(["At rest", "After brief exercise"], [2, peak], width=.46, color=COLORS)
        for pos, value in enumerate([2, peak]):
            ax.text(pos, value + .12, f"{value:.1f}", ha="center")
        ax.set(title="Motor response to stimulation  •  simulated", ylim=(0, 5.3))
        save(fig, "mgen_cmap_" + name)
    for name, pth in [("low", 5), ("keep", 51)]:
        report("pth_" + name, "Simultaneous serum measurements",
               ["Analyte", "Result", "Lab interval"],
               [["Ionized calcium (mmol/L)", "1.60", "1.15–1.30"],
                ["Intact PTH (pg/mL)", pth, "15–65"]], [.55, .16, .29])
    for name, lost in [("one", {"MLH1", "PMS2"}), ("two", {"MSH2", "MSH6"})]:
        report("ihc_" + name, "Colorectal tumor immunohistochemistry",
               ["Protein", "Tumor nuclei", "Internal control"],
               [[protein, "Absent" if protein in lost else "Retained", "Retained"]
                for protein in ["MLH1", "PMS2", "MSH2", "MSH6"]], [.25, .38, .37])
    for name, creat in [("ref", "1.00"), ("high", "0.10")]:
        report("pbg_" + name, "Spot urine during current symptoms",
               ["Measurement", "Patient / lab value"],
               [["Porphobilinogen (PBG)", "3 mg/L"], ["Creatinine", creat + " g/L"],
                ["Lab interval for PBG/creatinine", "0–4 mg/g"]], [.64, .36])


def clinical_nutrition_studies():
    """Render fictional nutrition assessments, laboratory reports and feeding records."""
    for name, mm in [("low", 112), ("mid", 120)]:
        fig, ax = plt.subplots(figsize=(5.6, 2.1), layout="constrained")
        ax.hlines(.35, 100, 135, color=COLORS[0], lw=2)
        for x in range(100, 136):
            height = .18 if x % 5 == 0 else .09
            ax.vlines(x, .35, .35 + height, color=COLORS[0])
            if x % 5 == 0:
                ax.text(x, .23, str(x), ha="center", fontsize=9)
        ax.annotate(f"{mm} mm", (mm, .54), xytext=(mm, 1.0), ha="center",
                    arrowprops={"arrowstyle": "-|>", "color": COLORS[1]}, color=COLORS[1])
        ax.set(xlim=(98, 137), ylim=(0, 1.32), title="Mid-upper arm circumference  •  simulated reading")
        ax.axis("off")
        save(fig, "nutri_mu_" + name)

    def report(name, title, headers, rows, widths):
        fig, ax = plt.subplots(figsize=(5.9, 2.65), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated", fontsize=12)
        table = ax.table(cellText=rows, colLabels=headers, colWidths=widths,
                         cellLoc="left", colLoc="left", bbox=[0, .04, 1, .82])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(headers)):
            table[0, col].set_facecolor("#dcecf2")
        save(fig, "nutri_" + name)

    for name, servings in [("one", 1), ("two", 2)]:
        report("b6_" + name, "Daily supplement history",
               ["Product", "B6 per serving", "Servings taken"],
               [["Multivitamin", "10 mg", "1"], ["B-complex", "50 mg", str(servings)]],
               [.36, .33, .31])
    for name, mma in [("fol", "0.20"), ("both", "1.10")]:
        report("met_" + name, "Serum metabolites",
               ["Measurement", "Result", "Lab interval"],
               [["Homocysteine (µmol/L)", "30", "5–15"], ["MMA (µmol/L)", mma, "0.08–0.40"]],
               [.55, .18, .27])
    for name, vit_d, pth, phosphate in [("d", "5", "156", "2.8"), ("p", "36", "35", "2.2")]:
        report("rick_" + name, "Pediatric mineral panel",
               ["Measurement", "Result", "Local age interval"],
               [["25-OH vitamin D (ng/mL)", vit_d, "20–50"], ["PTH (pg/mL)", pth, "15–65"],
                ["Phosphate (mg/dL)", phosphate, "4.0–6.5"], ["ALP (U/L)", "760", "140–400"]],
               [.53, .16, .31])
    for name, ferritin, saturation, crp in [("low", 7, 6, 1), ("infl", 325, 8, 85)]:
        report("iron_" + name, "Adult iron profile",
               ["Measurement", "Result", "Lab interval"],
               [["Ferritin (ng/mL)", ferritin, "20–250"], ["Transferrin saturation (%)", saturation, "20–45"],
                ["CRP (mg/L)", crp, "<5"]], [.55, .17, .28])
    for name, kg in [("a", "81.92"), ("b", "64.00")]:
        report("bmi_" + name, "Adult anthropometry", ["Measurement", "Result"],
               [["Standing height", "1.60 m"], ["Weight", kg + " kg"]], [.55, .45])
    for name, held in [("full", 0), ("stop", 5)]:
        report("pump_" + name, "Enteral pump log", ["Item", "Value"],
               [["Prescribed feeding window", "20 hours"], ["Rate while running", "60 mL/hour"],
                ["Time paused within window", f"{held} hours"], ["Catch-up volume", "None"]],
               [.64, .36])
    for name, amounts in [("iv", [400, 800, 800]), ("gi", [800, 1200, 0])]:
        report("energy_" + name, "24-hour delivered energy", ["Route or goal", "Energy (kcal)"],
               list(zip(["Oral", "Enteral tube", "Parenteral", "Daily goal"], amounts + [2000])),
               [.57, .43])
    for name, dose, device in [("ml", "400 IU per mL", "Oral syringe (mL)"),
                               ("drop", "400 IU per drop", "Drop dispenser")]:
        report("drops_" + name, "Infant vitamin D product label", ["Label entry", "Value"],
               [["Vitamin D concentration", dose], ["Supplied device", device]], [.54, .46])
    for name, edema, feeding in [("down", ["+++", "++", "+"], ["Poor", "Better", "Alert, eating"]),
                                 ("ill", ["++", "++", "++"], ["Poor", "Less alert", "Lethargic, poor intake"])]:
        report("edema_" + name, "Therapeutic nutrition follow-up",
               ["Day", "Weight (kg)", "Edema grade", "Observation"],
               [[day, wt, e, f] for day, wt, e, f in zip([1, 2, 3], [8.6, 8.4, 8.2], edema, feeding)],
               [.10, .21, .25, .44])


def multisystem_symptom_studies():
    """Render fictional cases for the interpretation of multisystem symptoms."""
    def table(name, title, columns, rows, widths):
        fig, ax = plt.subplots(figsize=(5.95, 2.75), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated", fontsize=12)
        grid = ax.table(cellText=rows, colLabels=columns, colWidths=widths,
                        cellLoc="left", colLoc="left", bbox=[0, .04, 1, .82])
        grid.auto_set_font_size(False)
        grid.set_fontsize(9.8)
        for col in range(len(columns)):
            grid[0, col].set_facecolor("#dcecf2")
        save(fig, "sympt_" + name)

    for name, values in [("rise", [13, 90, 59]), ("flat", [33, 34, 33])]:
        fig, ax = axes("Hours from first sample", "hs-troponin I (ng/L)")
        ax.plot([0, 2, 6], values, "o-", lw=2, color=COLORS[0])
        ax.axhline(20, ls="--", color="#6d3942", label="Assay upper reference limit")
        for x, y in zip([0, 2, 6], values):
            ax.annotate(str(y), (x, y), xytext=(0, 6), textcoords="offset points", ha="center")
        ax.set(title="Serial troponin  •  simulated", xticks=[0, 2, 6], ylim=(0, 110))
        ax.legend(loc="upper right", fontsize=8)
        save(fig, "sympt_trop_" + name)

    for name, hb, sat in [("anemia", "6.5", "98"), ("hypox", "14.2", "82")]:
        table("oxy_" + name, "Breathlessness assessment at sea level", ["Measure", "Result", "Local interval"],
              [["Hemoglobin (g/dL)", hb, "12–16"], ["SpO₂ on room air (%)", sat, "95–100"]], [.53, .19, .28])
    for name, ph, co2, oxygen in [("good", "7.36", 46, 95), ("bad", "7.19", 79, 95)]:
        table("vent_" + name, "Gas exchange on supplemental oxygen", ["Measure", "Arrival", "1 hour"],
              [["Arterial pH", "7.27", ph], ["PaCO₂ (mm Hg)", 62, co2],
               ["SpO₂ (%)", 90, oxygen]], [.54, .23, .23])
    for name, temps in [("doc", [38.6, 37.2, 38.8, 38.5, 37.1, 38.7]),
                        ("none", [36.9, 37.2, 37.0, 37.3, 36.8, 37.1])]:
        fig, ax = axes("Day of illness", "Oral temperature (°C)")
        days = [1, 5, 9, 15, 21, 28]
        ax.scatter(days, temps, s=45, color=COLORS[0])
        ax.set(title="Documented temperature readings  •  simulated", xticks=days, ylim=(36.5, 39.2))
        save(fig, "sympt_feb_" + name)
    for name, prior in [("ind", ["Independent", "Independent", "Independent"]),
                        ("dep", ["Needs help", "Needs help", "Needs help"])]:
        table("frail_" + name, "Function around an acute admission",
              ["Task", "Usual, 2 weeks prior", "Today"],
              [[task, before, "Needs help"] for task, before in zip(["Dressing", "Transfers", "Shopping"], prior)],
              [.25, .43, .32])
    for name, values in [("track", [-1.5, -1.55, -1.48, -1.5]),
                         ("fall", [-.15, -.45, -1.0, -1.65])]:
        fig, ax = axes("Age (months)", "Weight-for-age z score")
        ax.plot([3, 4, 5, 6], values, "o-", color=COLORS[0], lw=2)
        ax.axhline(0, color="#66717b", ls=":", label="Reference median")
        ax.set(title="Term infant, serial measurements  •  simulated",
               xticks=[3, 4, 5, 6], yticks=[-2, -1.5, -1, -.5, 0], ylim=(-2.2, .45))
        ax.legend(loc="lower left", fontsize=8)
        save(fig, "sympt_grow_" + name)
    for name, start, stop in [("match", 8, 13), ("apart", 18, 23)]:
        fig, ax = plt.subplots(figsize=(5.8, 2.75), layout="constrained")
        ax.broken_barh([(start, stop-start)], (1.6, .5), facecolors=COLORS[0])
        ax.plot(10, 1, "D", color=COLORS[1], ms=9)
        ax.axvline(10, color=COLORS[1], lw=1, ls=":")
        ax.set(xlim=(0, 30), ylim=(.6, 2.55), xlabel="Minutes from start of recording",
               yticks=[1, 1.85], yticklabels=["Symptom mark", "Tachycardia"],
               title="Ambulatory ECG event log  •  simulated")
        ax.set_xticks(range(0, 31, 5))
        ax.text(29.8, 2.25, "Sinus rhythm outside the shaded interval", ha="right", fontsize=8)
        save(fig, "sympt_palp_" + name)
    for name, start in [("60", 60), ("120", 120)]:
        table("wt_" + name, "Comparable clinic weights", ["Visit", "Weight"],
              [["Month 0", f"{start} kg"], ["Month 4", f"{start - 6} kg"]], [.55, .45])
    for name, sat, rr, air in [("ok", "97%", "18", "Clears secretions"),
                               ("bad", "84%", "34", "Cannot clear blood")]:
        table("hem_" + name, "Observations during hemoptysis",
              ["Finding", "Arrival", "20 min later"],
              [["SpO₂ on same O₂", "96%", sat], ["Respiratory rate/min", "20", rr],
               ["Airway", "Clears secretions", air]], [.35, .30, .35])
    for name, last in [("more", 32), ("same", 29)]:
        table("limb_" + name, "Upper arm circumference at fixed landmark",
              ["Visit", "Affected arm", "Opposite arm"],
              [["Baseline", "28 cm", "27 cm"], ["6 weeks", f"{last} cm", "28 cm"]], [.34, .33, .33])
    for name, scores in [("short", [2, 5, 2, 2, 2]), ("late", [2, 3, 4, 8, 6])]:
        fig, ax = axes("Time relative to usual activity", "Fatigue severity (0–10)")
        ax.plot(range(5), scores, "o-", color=COLORS[0], lw=2)
        ax.set(title="Activity and symptom diary  •  simulated", ylim=(0, 10),
               xticks=range(5), xticklabels=["Before", "After", "Evening", "Day +1", "Day +2"])
        save(fig, "sympt_fat_" + name)


def safeguarding_and_emergency_studies():
    """Render fictional chart excerpts paired by a change in clinical evidence."""
    def report(name, title, headers, rows, widths):
        fig, ax = plt.subplots(figsize=(6.6, 2.65), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated", fontsize=12)
        table = ax.table(cellText=rows, colLabels=headers, colWidths=widths,
                         cellLoc="left", colLoc="left", bbox=[0, .04, 1, .82])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(headers)):
            table[0, col].set_facecolor("#dcecf2")
        save(fig, "safecare_" + name)

    for name, last in [("echo", "Quotes referring note about yesterday"),
                       ("obs", "Saw a new spell at bedside just now")]:
        report("reports_" + name, "Pediatric record excerpts",
               ["Entry", "Documented observation"],
               [["Caregiver, yesterday", "Saw an episode at home"],
                ["Referring clinician", "Records caregiver's account"],
                ["Bedside nurse, 10 a.m.", last]], [.40, .60])
    for name, last in [("recover", ["Coordinated", "Swallows normally"]),
                       ("worse", ["Uncoordinated", "Unable to clear saliva"])]:
        report("sc_" + name, "Post-treatment bedside observations",
               ["Time", "Movement", "Swallowing"],
               [["Initial", "Uncoordinated", "Difficult"], ["Reassessment", *last]],
               [.23, .34, .43])
    for name, readings in [("stable", [["122/76", 88, "Alert"], ["120/74", 86, "Alert"],
                                       ["122/74", 84, "Alert"]]),
                           ("fall", [["94/62", 112, "Alert"], ["112/70", 100, "Alert"],
                                     ["76/48", 138, "Confused"]])]:
        report("tra_" + name, "Trauma resuscitation record",
               ["Time (min)", "BP (mm Hg)", "Pulse (/min)", "Mental status"],
               [[time, *values] for time, values in zip([0, 15, 30], readings)],
               [.21, .26, .24, .29])
    for name, distances in [("stay", [3, 3, 3]), ("move", [3, 7, 12])]:
        fig, ax = plt.subplots(figsize=(5.7, 2.9), layout="constrained")
        ax.plot([0, 30, 60], distances, marker="o", color="#186684", lw=2)
        ax.set(xticks=[0, 30, 60], ylim=(0, 15), yticks=[0, 3, 6, 9, 12, 15],
               title="Leading edge of limb swelling  •  simulated",
               xlabel="Minutes after initial examination", ylabel="cm proximal to landmark")
        ax.grid(axis="y", alpha=.25)
        save(fig, "safecare_sn_" + name)
    for name, last in [("labok", [205, 295]), ("labbad", [68, 95])]:
        report("sn_" + name, "Serial laboratory results",
               ["Analyte", "Initial", "2 hours", "Lab interval"],
               [["Platelets (×10³/µL)", 210, last[0], "150–400"],
                ["Fibrinogen (mg/dL)", 300, last[1], "200–400"]], [.36, .17, .18, .29])


def environmental_exposure_studies():
    """Render fictional examination records and laboratory courses for environmental illness."""
    def report(name, title, columns, rows, widths):
        fig, ax = plt.subplots(figsize=(6.5, 2.8), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated", fontsize=12)
        table = ax.table(cellText=rows, colLabels=columns, colWidths=widths,
                         cellLoc="left", colLoc="left", bbox=[0, .03, 1, .84])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#dcecf2")
        save(fig, "environ_" + name)

    for name, depths in [("a", ["Superficial", "Superficial partial", "Superficial"]),
                         ("b", ["Superficial partial", "Superficial", "Deep partial"])]:
        report("tbsa_" + name, "Adult burn survey",
               ["Nonoverlapping region", "Area (% body surface)", "Depth"],
               [[region, area, depth] for region, area, depth in
                zip(["A", "B", "C"], [10, 8, 3], depths)], [.34, .33, .33])
    for name, last in [("ok", ["<10", "310", "1.2"]), ("ill", ["<10", "1,240", "2.4"])]:
        report("nac_" + name, "Acetylcysteine monitoring",
               ["Laboratory result", "Earlier", "End of planned course"],
               [["Acetaminophen (µg/mL)", "32", last[0]], ["ALT (U/L)", "800", last[1]],
                ["INR", "1.7", last[2]]], [.40, .27, .33])
    for name, method in [("cap", "Capillary fingerstick"), ("ven", "Venipuncture")]:
        report("lead_" + name, "Childhood lead screening",
               ["Report field", "Result"], [["Collection method", method],
               ["Whole blood lead", "12 µg/dL"], ["Previous result", "None"]], [.50, .50])
    for name, values in [("early", ["7.49", "30", "22", "11"]),
                         ("mixed", ["7.45", "20", "13", "24"])]:
        report("sal_" + name, "Arterial gas and serum chemistry",
               ["Measurement", "Result", "Reference interval"],
               [[label, value, ref] for label, value, ref in zip(
                   ["Arterial pH", "PaCO₂ (mm Hg)", "Bicarbonate (mmol/L)", "Anion gap (mmol/L)"],
                   values, ["7.35–7.45", "35–45", "22–26", "8–12"])], [.43, .20, .37])
    for name, course in [("better", ["7.38", "7.44", "Alert", "Alert"]),
                         ("worse", ["7.38", "7.23", "Alert", "Confused"])]:
        report("sal_" + name, "Salicylate treatment observations",
               ["Measurement", "Initial", "Reassessment"],
               [["Serum salicylate (mg/dL)", 58, 44], ["Arterial pH", *course[:2]],
                ["Mental status", *course[2:]]], [.49, .23, .28])
    for name, values in [("walk", ["Keeps pace", "Breathing comfortably", "Clear", "90% / 91%"]),
                         ("rest", ["Falls behind", "Breathless seated", "Crackles", "72% / 91%"])]:
        report("alt_" + name, "Clinical observations at 3,500 m",
               ["Assessment", "Observation"],
               list(zip(["Hiking with group", "After resting", "Lung examination",
                         "SpO₂ (patient / companion)"], values)), [.55, .45])
    fig, ax = plt.subplots(figsize=(5.9, 3), layout="constrained")
    ax.plot([2, 8, 14, 20], [2.1, 1.6, 1.0, .5], marker="o", color=COLORS[0], lw=2)
    ax.set(xticks=[2, 8, 14, 20], ylim=(0, 2.5), xlabel="Hours after suspected exposure",
           ylabel="Absolute lymphocytes (×10⁹/L)", title="Serial differential counts  •  simulated")
    ax.grid(axis="y", alpha=.25)
    save(fig, "environ_rad_alc")


def systemic_inflammation_studies():
    """Plot simulated pediatric coronary z scores from consecutive clinical assessments."""
    for name, last in [("norm", 1.2), ("rise", 3.1)]:
        fig, ax = plt.subplots(figsize=(5.8, 3.1), layout="constrained")
        ax.plot([1, 2], [1.4, last], marker="o", color=COLORS[0], lw=2)
        for x, y in [(1, 1.4), (2, last)]:
            ax.annotate(f"{y:+.1f}", (x, y), xytext=(0, 8),
                        textcoords="offset points", ha="center")
        ax.set(xlim=(.65, 2.35), ylim=(0, 4), xticks=[1, 2],
               xticklabels=["Initial echo", "Follow-up echo"],
               ylabel="Proximal LAD z score", title="Coronary echocardiography  •  simulated")
        ax.grid(axis="y", alpha=.25)
        save(fig, "inflam_cor_" + name)


def multisystem_rheumatology_studies():
    """Render simulated morphology, hemodynamics and longitudinal clinical observations."""
    def report(name, title, columns, rows, widths):
        fig, ax = plt.subplots(figsize=(6.6, 2.85), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated", fontsize=12)
        table = ax.table(cellText=rows, colLabels=columns, colWidths=widths,
                         cellLoc="left", colLoc="left", bbox=[0, .02, 1, .85])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#dcecf2")
        save(fig, "rheum_" + name)

    for name, later in [("titer", ["68", "1.0", "No casts"]),
                        ("kidney", ["19", "2.7", "Red cell casts"])]:
        report("anca_" + name, "Vasculitis surveillance",
               ["Measurement", "Two weeks ago", "Now"],
               [["PR3 antibody (assay units)", "18", later[0]],
                ["Creatinine (mg/dL)", "1.0", later[1]],
                ["Urine microscopy", "No casts", later[2]]], [.47, .26, .27])
    # Identical loop boundaries and control in both stimuli. Only IgG signal varies.
    for name, bright in [("pauci", False), ("linear", True)]:
        fig, axs = plt.subplots(1, 2, figsize=(6.2, 2.65), layout="constrained")
        fig.suptitle("Glomerular IgG immunofluorescence  •  schematic", fontsize=12)
        theta = np.linspace(0, 2 * np.pi, 140)
        for ax, title, positive in zip(axs, ["Positive control", "Patient"], [True, bright]):
            ax.set(facecolor="#121b24", xlim=(-1.45, 1.45), ylim=(-1.02, 1.02),
                   aspect="equal", xticks=[], yticks=[])
            ax.set_title(title, fontsize=10)
            for x, y, rx, ry in [(-.70, .37, .34, .31), (.0, .43, .32, .36),
                                  (.69, .32, .32, .29), (-.42, -.30, .42, .34),
                                  (.48, -.36, .39, .32)]:
                ax.plot(x + rx * np.cos(theta), y + ry * np.sin(theta),
                        color="#a1ffc6" if positive else "#34424c",
                        lw=3 if positive else 1.2)
        save(fig, "rheum_if_" + name)
    for name, left in [("even", 122), ("low", 84)]:
        fig, ax = plt.subplots(figsize=(5.7, 3.0), layout="constrained")
        vals = [124, left, 136, 138]
        bars = ax.bar(["Right arm", "Left arm", "Right leg", "Left leg"], vals, color=COLORS[0])
        ax.bar_label(bars, padding=3)
        ax.set(ylim=(0, 165), ylabel="Systolic pressure (mm Hg)",
               title="Resting limb pressures  •  simulated")
        save(fig, "rheum_bp_" + name)
    for name, loss in [("norm", False), ("loss", True)]:
        fig, ax = plt.subplots(figsize=(5.9, 2.45), layout="constrained")
        ax.set(xlim=(0, 12), ylim=(0, 2.5), aspect="equal")
        ax.axis("off")
        ax.set_title("Distal nailfold capillary row  •  schematic", fontsize=12)
        theta = np.linspace(0, np.pi, 60)
        for i in range(11):
            if loss and i in (3, 4, 5, 9):
                continue
            giant = loss and i in (2, 7)
            x = i + 1
            radius = .31 if giant else .12
            height = 1.64 + .14 * np.sin(i)
            line_x = [x + radius, *(x + radius * np.cos(theta)), x - radius]
            line_y = [.40, *(height + radius * np.sin(theta)), .41]
            ax.plot(line_x, line_y, color="#813c54", lw=5 if giant else 1.9,
                    solid_capstyle="round")
        save(fig, "rheum_cap_" + name)
    for name, later in [("stable", ["112/70", "0.8"]), ("rise", ["182/108", "2.3"])]:
        report("src_" + name, "Systemic sclerosis surveillance",
               ["Measurement", "Last week", "Today"],
               [["Blood pressure (mm Hg)", "110/68", later[0]],
                ["Creatinine (mg/dL)", "0.8", later[1]]], [.48, .25, .27])
    for name, vals in [("ild", ["58%", "48%", "Basal fibrosis", "No RV enlargement"]),
                       ("ph", ["94%", "36%", "Minimal fibrosis", "RV enlargement; high RVSP"])]:
        report("lung_" + name, "Pulmonary evaluation",
               ["Measurement", "Observation"],
               list(zip(["TLC (% predicted)", "DLCO (% predicted)", "High-resolution CT",
                         "Echocardiography"], vals)), [.51, .49])
    for name, vals in [("water", ["309", "87", "92", "Absent"]),
                       ("solute", ["318", "645", "560", "Marked"])]:
        report("di_" + name, "Paired serum and urine studies",
               ["Measurement", "Result", "Reference / context"],
               [[label, val, ref] for label, val, ref in zip(
                   ["Serum osmolality (mOsm/kg)", "Urine osmolality (mOsm/kg)",
                    "Serum glucose (mg/dL)", "Urine glucose"], vals,
                   ["275–295", "Interpret with serum", "70–99 (fasting)", "Absent"])],
               [.48, .15, .37])
    report("aps_ca", "Endocrine studies", ["Measurement", "Result", "Lab interval"],
           [["Ionized calcium (mmol/L)", "0.84", "1.12–1.32"],
            ["Intact PTH (pg/mL)", "5", "15–65"], ["Potassium (mmol/L)", "4.2", "3.5–5.0"]],
           [.49, .19, .32])
    report("aps_ad", "Morning endocrine studies", ["Measurement", "Result", "Lab interval"],
           [["Cortisol (µg/dL)", "1.4", "5–25"], ["ACTH (pg/mL)", "315", "10–60"],
            ["Sodium (mmol/L)", "127", "135–145"], ["Potassium (mmol/L)", "5.8", "3.5–5.0"]],
           [.48, .20, .32])
    for name, vals in [("clear", [86, 4, 5]), ("persist", [86, 48, 53])]:
        report("fmf_" + name, "Serum amyloid A (lab reference <10 mg/L)",
               ["Visit", "Diary entry", "SAA (mg/L)"],
               [[visit, state, val] for visit, state, val in
                zip([1, 2, 3], ["Fever and serositis", "Well between attacks", "Well between attacks"], vals)],
               [.17, .53, .30])
    for name, urine in [("renal", ["6.5", "+24"]), ("gi", ["5.0", "−36"])]:
        report("rta_" + name, "Acid-base evaluation", ["Measurement", "Result"],
               [["Serum HCO₃⁻ (mmol/L)", 15], ["Serum anion gap (mmol/L)", 10],
                ["Serum potassium (mmol/L)", "2.9"], ["Urine pH", urine[0]],
                ["Urine anion gap (mmol/L)", urine[1]]], [.65, .35])
    for name, vals in [("pre", [34, 9, "5.0"]), ("post", [34, 24, "2.0"])]:
        report("rhc_" + name, "Right-heart catheterization",
               ["Measurement", "Result"],
               list(zip(["Mean pulmonary artery pressure (mm Hg)",
                         "Pulmonary artery wedge pressure (mm Hg)",
                         "Pulmonary vascular resistance (Wood units)"], vals)), [.76, .24])


def systemic_infection_studies():
    """Draw simulated patient records for comparing clinical courses and timing."""
    def report(name, title, columns, rows, widths):
        fig, ax = plt.subplots(figsize=(6.5, 2.8), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated", fontsize=12)
        t = ax.table(cellText=rows, colLabels=columns, colWidths=widths,
                     cellLoc="left", colLoc="left", bbox=[0, .02, 1, .83])
        t.auto_set_font_size(False)
        t.set_fontsize(10)
        for col in range(len(columns)):
            t[0, col].set_facecolor("#dcecf2")
        save(fig, "sysinf_" + name)

    for name, intervals in [("short", [222, 228, 230]), ("long", [242, 282, 344])]:
        fig, ax = plt.subplots(figsize=(5.7, 2.95), layout="constrained")
        ax.plot([0, 1, 2], intervals, marker="o", lw=2, color=COLORS[0])
        for t, val in enumerate(intervals):
            ax.annotate(str(val), (t, val), xytext=(0, 6), textcoords="offset points", ha="center")
        ax.set(xlim=(-.2, 2.2), ylim=(180, 380), xticks=[0, 1, 2],
               xlabel="Observation time (hours)", ylabel="PR interval (ms)",
               title="Serial ECG measurements  •  simulated")
        ax.grid(axis="y", alpha=.25)
        save(fig, "sysinf_pr_" + name)
    report("lep_organ", "Laboratory course", ["Measurement", "Initial", "Now"],
           [["Total bilirubin (mg/dL)", "1.1", "8.6"],
            ["Creatinine (mg/dL)", "0.9", "3.4"]], [.50, .25, .25])
    for name, art, visits in [("iris", "Day 15", ["Less fever", "Painful enlarging nodes"]),
                              ("other", "Not started", ["Persistent fever", "Persistent fever and wasting"])]:
        report("tb_" + name, "Clinical timeline", ["Entry", "Observation"],
               [["TB therapy started", "Day 0"], ["Day 12 review", visits[0]],
                ["ART started", art], ["Day 28 review", visits[1]]], [.44, .56])
    for name, bp, cr in [("stable", "118/74", "0.9"), ("worse", "76/42", "2.3")]:
        report("ts_" + name, "Serial observations", ["Measurement", "Earlier", "Current"],
               [["Blood pressure (mm Hg)", "116/72", bp], ["Creatinine (mg/dL)", "0.9", cr]],
               [.52, .22, .26])
    report("q_acute", "Paired immunofluorescence titers", ["Antibody", "Day 5", "Week 5"],
           [["Phase I IgG", "<1:16", "1:32"], ["Phase II IgG", "1:64", "1:256"]], [.44, .28, .28])
    report("q_focus", "Endocarditis evaluation", ["Measurement", "Finding"],
           [["Phase I IgG titer", "1:4096"], ["Phase II IgG titer", "1:512"],
            ["Echocardiogram", "New vegetation on prosthetic valve"]], [.42, .58])
    for name, vals in [("low", ["2.9", "78", "92"]), ("norm", ["6.8", "202", "31"])]:
        report("an_" + name, "Day-one laboratory studies", ["Analyte", "Result", "Lab interval"],
               [[k, v, ref] for k, v, ref in zip(
                ["Leukocytes (×10⁹/L)", "Platelets (×10⁹/L)", "ALT (U/L)"],
                vals, ["4.0–11.0", "150–400", "7–55"])], [.49, .19, .32])
    for name, results in [("recent", ["Positive", "Positive", "Negative"]),
                          ("old", ["Negative", "Positive", "Positive"])]:
        report("eb_" + name, "EBV antibody panel", ["Serum marker", "Result"],
               list(zip(["VCA IgM", "VCA IgG", "EBNA IgG"], results)), [.56, .44])
    for name, vals in [("early", ["Day 4", "Positive", "Day 6", "Positive"]),
                       ("late", ["Not obtained", "—", "Week 8", "Positive"])]:
        report("cm_" + name, "CMV testing record", ["Specimen", "Age at collection", "PCR"],
               [["Saliva", *vals[:2]], ["Urine", *vals[2:]]], [.30, .37, .33])
    for name, last in [("rec", ["Afebrile", "Resuming activities", "Normal"]),
                       ("severe", ["Fever recurs", "Jaundice", "Low urine output"])]:
        report("yf_" + name, "Traveler follow-up", ["Interval", "Clinical course"],
               [["Initial illness", "Fever, myalgias"], ["Next day", "Brief improvement"],
                ["Later assessment", last[0] + ", " + last[1].lower()],
                ["Renal status then", last[2]]], [.36, .64])
    for name, vals, status in [("better", [14, 6, 2], "Fever resolves, gaining weight"),
                               ("recur", [14, 2, 9], "Recurrent fever and weight loss")]:
        report("hist_" + name, "Urine Histoplasma antigen (same assay)",
               ["Visit", "Antigen (ng/mL)", "Clinical status"],
               [["Initial", vals[0], "Fever, weight loss"], ["On treatment", vals[1], "Improving"],
                ["Later follow-up", vals[2], status]], [.24, .25, .51])
    for name, history, test in [("early", "First freshwater exposure on July 1", "July 4: negative"),
                                ("late", "Treated three years ago", "Current: positive")]:
        report("sch_" + name, "Travel clinic record", ["Item", "Details"],
               [["History", history], ["Schistosoma antibody", test]], [.39, .61])
    for name, counts in [("rec", [145, 188, 213]), ("low", [63, 71, 79])]:
        fig, ax = plt.subplots(figsize=(5.7, 2.95), layout="constrained")
        ax.plot([0, 2, 4], counts, marker="o", color=COLORS[0], lw=2)
        ax.set(xlim=(-.2, 4.2), ylim=(0, 260), xticks=[0, 2, 4],
               xlabel="Months of follow-up", ylabel="CD4 count (cells/µL)",
               title="Immune recovery on ART  •  simulated")
        ax.grid(axis="y", alpha=.25)
        save(fig, "sysinf_cd_" + name)
    for name, observations in [("clear", ["Negative", "Negative", "Negative"]),
                               ("again", ["Negative", "Positive", "Negative"])]:
        report("cand_" + name, "Bloodstream infection follow-up",
               ["Blood collected", "Clinical microbiology report"],
               list(zip(["June 2", "June 3", "June 4", "June 5"],
                        ["Positive for Candida", *observations])), [.41, .59])


def clinical_otology_studies():
    """Render simulated single-ear audiometry and tympanometry for ear cases."""
    for name, pressure in [("neg", -200), ("normal", 0), ("pressure_cold", -245), ("pressure_flight", 15)]:
        fig, ax = axes("Ear canal pressure (daPa)", "Admittance (mL)")
        sweep = np.linspace(-350, 200, 240)
        ax.plot(sweep, 0.08 + 0.85 * np.exp(-0.5 * ((sweep - pressure) / 44) ** 2),
                color=COLORS[0], lw=2.5)
        ax.set(title="Tympanogram  •  simulated", ylim=(0, 1.2),
               xticks=[-300, -200, -100, 0, 100, 200])
        save(fig, "ear_" + name)

    def audiogram(name, frequencies, series):
        fig, ax = axes("Frequency (kHz)", "Threshold (dB HL)")
        for j, (label, values) in enumerate(series):
            ax.plot(frequencies, values, STYLES[j], marker=["o", "s"][j],
                    mfc="white", lw=2, color=COLORS[j], label=label)
        ax.set_xscale("log", base=2)
        ax.set_xticks(frequencies, [f"{f:g}" for f in frequencies])
        ax.minorticks_off()
        ax.set(ylim=(80, -5), yticks=range(0, 81, 10), title="Pure-tone thresholds  •  simulated")
        ax.legend(loc="lower left", fontsize=8)
        save(fig, "ear_" + name)

    routine = [.25, .5, 1, 2, 4]
    for name, air, bone in [
        ("gap", [45, 45, 40, 40, 40], [10, 10, 10, 15, 10]),
        ("sn", [45, 45, 45, 55, 60], [40, 45, 40, 50, 55]),
        ("family", [45, 40, 35, 35, 30], [5, 10, 10, 15, 10]),
        ("worker", [40, 45, 35, 30, 35], [5, 10, 10, 5, 10]),
        ("chemo", [35, 35, 30, 35, 25], [5, 5, 10, 10, 5]),
        ("wax", [30, 40, 35, 40, 35], [0, 10, 5, 10, 5]),
        ("cleared", [35, 40, 45, 55, 65], [35, 35, 45, 50, 65]),
        ("tear", [30, 30, 25, 20, 15], [5, 5, 5, 5, 5]),
        ("injury", [45, 50, 55, 65, 70], [45, 50, 50, 65, 65]),
        ("salicylate", [35, 40, 35, 30, 30], [10, 10, 5, 5, 5]),
    ]:
        audiogram(name, routine, [("Air", air), ("Masked bone", bone)])

    audiogram("notch", [.5, 1, 2, 3, 4, 6, 8], [
        ("Air", [15, 15, 20, 35, 55, 40, 30]),
        ("Masked bone", [10, 10, 15, 35, 50, np.nan, np.nan]),
    ])
    audiogram("airnotch", [.5, 1, 2, 3, 4, 6, 8], [
        ("Air", [10, 10, 15, 35, 55, 40, 25])])
    audiogram("operator", [.5, 1, 2, 3, 4, 6, 8], [
        ("Air", [15, 15, 20, 40, 60, 45, 30])])
    audiogram("low", [.25, .5, 1, 2, 4, 8], [
        ("Between attacks", [15, 15, 15, 15, 20, 20]),
        ("During symptoms", [50, 45, 30, 15, 20, 20]),
    ])
    audiogram("ciscurve", [.25, .5, 1, 2, 4, 8], [
        ("Baseline air", [10, 10, 10, 15, 20, 20]),
        ("Current air", [10, 10, 15, 20, 45, 65]),
    ])
    for name, current in [("shift", [10, 10, 15, 30, 30, 20]),
                          ("isolated", [10, 10, 15, 30, 20, 20])]:
        audiogram(name, [.5, 1, 2, 4, 6, 8], [
            ("Baseline air", [10, 10, 15, 20, 20, 20]), ("Current air", current)])


def visual_function_studies():
    """Render schematic eye examinations and simulated optics and psychophysics data."""
    def record(name, title, columns, rows):
        fig, ax = plt.subplots(figsize=(5.8, 2.7), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated")
        table = ax.table(cellText=rows, colLabels=columns, cellLoc="center",
                         bbox=[.02, .1, .96, .73])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#e2edf1")
        save(fig, "eye_" + name)

    record("pupil_l", "Equal illumination in alternating eyes",
           ["Light on", "Right pupil", "Left pupil"],
           [["Right eye", "2 mm", "2 mm"], ["Left eye", "4 mm", "4 mm"],
            ["Right eye again", "2 mm", "2 mm"]])
    record("ethacuity", "Best-corrected distance acuity",
           ["Visit", "Right eye", "Left eye", "Both open"],
           [["Baseline", "20/20", "20/20", "20/20"], ["Today", "20/60", "20/20", "20/20"]])
    record("iop", "Applanation tonometry",
           ["IOP (mm Hg)", "Before drops", "Week 1", "Week 3"],
           [["Right (untreated)", "16", "15", "16"], ["Left (treated)", "15", "20", "29"]])
    record("meridian", "Corneal optical power",
           ["Principal meridian", "Measured power"],
           [["Horizontal (180°)", "42.0 D"], ["Vertical (90°)", "45.0 D"]])
    record("criterion", "Yes/no flash experiment",
           ["Instructions", "Hits / 100 flashes", "False alarms / 100 blanks"],
           [["Neutral", "58", "12"], ["Say seen if unsure", "78", "28"]])

    for name, right, left in [("stablefield", [-4.2, -4.5, -4.1], [-3.5, -3.2, -3.6]),
                              ("fallfield", [-3, -7.4, -13], [-2.5, -6.8, -11.5])]:
        fig, ax = axes("Week of follow-up", "Mean deviation (dB)")
        for j, (eye, series) in enumerate([("Right", right), ("Left", left)]):
            ax.plot([0, 1, 2], series, STYLES[j], marker=["o", "s"][j], label=eye,
                    color=COLORS[j], lw=2)
        ax.set(title="Reliable automated visual fields  •  simulated", ylim=(-16, 0), xticks=[0, 1, 2])
        ax.legend()
        save(fig, "eye_" + name)

    fig, ax = plt.subplots(figsize=(4, 4), layout="constrained")
    line = np.linspace(-5, 5, 180)
    for level in np.arange(-5, 5.1, .5):
        warp = .55 * np.exp(-((line - .9) ** 2 + (level - .4) ** 2) / 1.2)
        ax.plot(line, level + warp, color="#294651", lw=.8)
        ax.plot(level + warp, line, color="#294651", lw=.8)
    ax.plot(0, 0, "ko", ms=4)
    ax.set(aspect="equal", title="Patient's monocular grid drawing")
    ax.axis("off")
    save(fig, "eye_grid")

    for name, center_seen in [("island", True), ("centralmap", False)]:
        fig, ax = plt.subplots(figsize=(4.3, 3.7), layout="constrained")
        for y in range(-30, 31, 5):
            for x in range(-30, 31, 5):
                radius = np.hypot(x, y)
                if radius <= 30:
                    seen = (radius <= 10) == center_seen
                    ax.plot(x, y, marker="o", ms=6, mec="#344a52", mfc="white" if seen else "#344a52")
        ax.set(title="Single-eye field responses  •  simulated", xlabel="Horizontal position (degrees)",
               ylabel="Vertical position (degrees)", aspect="equal", xticks=[-30, 0, 30], yticks=[-30, 0, 30])
        ax.text(.5, -.21, "Open = seen     Filled = missed", ha="center", transform=ax.transAxes)
        save(fig, "eye_" + name)

    for name, focus, retina in [("myoray", 3.25, 4.2), ("mcathyper", 4.65, 3.65)]:
        fig, ax = plt.subplots(figsize=(5.6, 2.8), layout="constrained")
        ax.axhline(0, color="#999999", lw=.8, ls=":")
        ax.plot([0, 0], [-1.25, 1.25], color="#438392", lw=5)
        ax.plot([retina, retina], [-1.25, 1.25], color="#563550", lw=3)
        for h in [-.85, -.42, .42, .85]:
            ax.plot([-1.4, 0, retina], [h, h, h * (1 - retina / focus)], lw=1.5, color=COLORS[0])
            if focus > retina:
                ax.plot([retina, focus], [h * (1 - retina / focus), 0], ls="--", color=COLORS[0], lw=1)
        ax.text(0, -1.45, "Eye optics", ha="center")
        ax.text(retina, -1.45, "Retina", ha="center")
        ax.set(xlim=(-1.6, 5), ylim=(-1.7, 1.55), title="Parallel light from the left  •  relaxed model eye")
        ax.axis("off")
        save(fig, "eye_" + name)

    fig, ax = axes("1 / object distance (m⁻¹)", "1 / image distance (m⁻¹)")
    x = np.array([.5, 1, 1.5, 2, 2.5, 3])
    ax.plot([0, 3.25], [4, .75], color=COLORS[0], label="Fitted line")
    ax.scatter(x, [3.48, 3.04, 2.47, 2.03, 1.49, 1.01], color=COLORS[1], label="Measurements")
    ax.set(title="Converging lens bench  •  simulated", xlim=(0, 3.3), ylim=(0, 4.5))
    ax.legend()
    save(fig, "eye_bench")

    fig, ax = axes("Flash intensity (arbitrary units)", "Trials reported seen (of 40)")
    ax.plot([1, 2, 3, 4, 5, 6, 7], [1, 3, 9, 20, 32, 37, 39], "o-", color=COLORS[0])
    ax.set(title="Monocular flash detection  •  simulated", yticks=[0, 10, 20, 30, 40])
    save(fig, "eye_half")
    fig, ax = axes("Flash intensity (arbitrary units)", "Trials reported seen (%)")
    x = np.linspace(0, 10, 160)
    for j, (label, mid) in enumerate([("Session A", 6), ("Session B", 3)]):
        ax.plot(x, 100 / (1 + np.exp(-(x - mid) * 1.3)), STYLES[j], color=COLORS[j], label=label)
    ax.set(title="Detection across sessions  •  simulated", yticks=[0, 25, 50, 75, 100])
    ax.legend()
    save(fig, "eye_sensshift")

    for name, delay in [("darkrod", 8), ("darkcross", 5)]:
        fig, ax = axes("Time in darkness (minutes)", "Detection threshold (relative units)")
        t = np.arange(31)
        cone = .10 + 1.8 * np.exp(-t / 1.55)
        rod = .001 + 3.0 * np.exp(-np.maximum(t - delay, 0) / 1.46)
        ax.semilogy(t, cone, lw=2, color=COLORS[0], label="Cone pathway")
        ax.semilogy(t, rod, "--", lw=2, color=COLORS[1], label="Rod pathway")
        ax.set(title="Peripheral light detection  •  teaching model", xticks=range(0, 31, 5))
        ax.legend()
        save(fig, "eye_" + name)


def eye_injury_and_experiment_studies():
    """Draw simulated clinical records and data from model MCAT experiments."""
    def record(name, title, columns, rows):
        fig, ax = plt.subplots(figsize=(6.1, 2.65), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated")
        table = ax.table(cellText=rows, colLabels=columns, loc="center",
                         cellLoc="center", bbox=[.01, .08, .98, .76])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#e2edf1")
        save(fig, "acuteeye_" + name)

    for name, values in [("rebound", ["11.0", "7.2", "8.5"]),
                         ("neutral", ["10.5", "7.2", "7.2"])]:
        record(name, "Ocular surface checks", ["Sample time", "Surface pH"],
               [[time, value] for time, value in zip(
                   ["Before irrigation", "At pause", "5 minutes later"], values)])

    for name, levels, pressures in [
        ("clearhyp", ["2 mm", "1 mm", "Trace"], [17, 16, 15]),
        ("rehyp", ["2 mm", "1 mm", "4 mm"], [16, 17, 32]),
    ]:
        record(name, "Closed-globe injury follow-up", ["Day", "Blood layer", "IOP (mm Hg)"],
               list(zip([1, 2, 4], levels, pressures)))

    for name, motion, position, vision in [
        ("preexam", "Full and painless", "No proptosis", "20/20"),
        ("orbitexam", "Painful, limited", "Proptosis", "20/40"),
    ]:
        record(name, "Affected eye examination", ["Function", "Finding"],
               [["Distance acuity", vision], ["Eye movements", motion], ["Globe position", position]])

    for name, heights in [("melstable", [1.2, 1.2, 1.2]), ("melgrow", [1.4, 2.0, 2.8])]:
        fig, ax = axes("Follow-up (months)", "Lesion thickness (mm)")
        ax.plot([0, 6, 12], heights, "o-", color=COLORS[0], lw=2)
        ax.set(title="Serial ocular ultrasound  •  simulated", xticks=[0, 6, 12], ylim=(0, 3.5))
        save(fig, "acuteeye_" + name)
    record("uveiticpressure", "Treated eye at follow-up", ["Visit", "Aqueous cell grade", "IOP (mm Hg)"],
           [["Initial", "3+", "14"], ["Week 2", "1+", "21"], ["Week 4", "Trace", "30"]])
    record("ptergrowth", "Corneal follow-up", ["Visit", "Extension past limbus", "Refractive cylinder"],
           [["Initial", "1.5 mm", "0.50 D"], ["Month 8", "2.2 mm", "1.25 D"],
            ["Month 16", "3.1 mm", "2.00 D"]])

    def experiment(name, title, xlabel, ylabel, x, series):
        fig, ax = axes(xlabel, ylabel)
        for i, (label, y) in enumerate(series):
            ax.plot(x, y, STYLES[i], marker=["o", "s"][i], lw=2, label=label, color=COLORS[i])
        ax.set_title(title + "  •  simulated")
        ax.legend()
        save(fig, "acuteeye_" + name)

    experiment("flow", "Steady laminar flow", "Pressure difference (kPa)", "Flow (mL/s)",
               [0, 1, 2, 3], [("Tube A", [0, 2, 4, 6]), ("Tube B", [0, 1, 2, 3])])
    t = np.arange(0, 5.5, .5)
    experiment("rc", "Discharge through equal resistors", "Time (s)", "Voltage / initial voltage",
               t, [("Capacitor A", np.exp(-t)), ("Capacitor B", np.exp(-t / 2.5))])
    experiment("buffer", "Acid added to equal buffer volumes", "Strong acid added (mmol)", "pH",
               [0, .5, 1, 1.5], [("Sample A", [7.00, 6.96, 6.91, 6.87]),
                                  ("Sample B", [7.00, 6.85, 6.68, 6.40])])
    experiment("vap", "Equilibrium above pure liquids", "Temperature (°C)", "Vapor pressure (kPa)",
               [20, 25, 30, 35], [("Liquid X", [2.3, 3.1, 4.2, 5.6]),
                                   ("Liquid Y", [5.9, 7.9, 10.5, 13.8])])
    record("dual", "Within-participant visual search", ["Condition", "Mean accuracy"],
           [["Search alone", "92%"], ["Search plus tone monitoring", "80%"]])
    record("cont", "Picture occurrence by cue", ["Group", "P(picture | tone)", "P(picture | no tone)"],
           [["A", "0.80", "0.20"], ["B", "0.50", "0.50"]])
    fig, ax = axes("Trial (F = familiar, N = novel)", "Orienting duration (s)")
    ax.plot(range(1, 8), [8, 6, 4, 2, 1, 9, 7], "o-", lw=2, color=COLORS[0])
    ax.set(xticks=range(1, 8), xticklabels=["1 F", "2 F", "3 F", "4 F", "5 F", "6 N", "7 F"],
           ylim=(0, 10), title="Orienting during repeated sounds  •  simulated")
    save(fig, "acuteeye_hab")

    from matplotlib.patches import Ellipse, Polygon

    # Cross sections use the same reference anatomy so the learner can compare the lens position.
    for name, lens_x, lens_y, tilt in [("lens_front", -.77, 0, 0), ("lens_back", .54, -.61, -30)]:
        fig, ax = plt.subplots(figsize=(5.6, 3.25), layout="constrained")
        ax.add_patch(Ellipse((0, 0), 2.9, 2.15, facecolor="#f0f5f7", edgecolor="#42525d", lw=2))
        arc = np.linspace(-1.05, 1.05, 70)
        ax.plot(-1.45 * np.cos(arc), 1.075 * np.sin(arc), color="#238497", lw=3.5)
        for sign in [-1, 1]:
            ax.plot([-.43, -.43], [sign * .94, sign * .32], lw=7, color="#946731")
        ax.add_patch(Ellipse((lens_x, lens_y), .32, .8, angle=tilt,
                             facecolor="#b8dbe6", edgecolor="#215a75", lw=2))
        ax.annotate("Lens", xy=(lens_x, lens_y), xytext=(.98, .85), ha="center",
                    arrowprops=dict(arrowstyle="->", color="#3e4950"))
        ax.annotate("Iris", xy=(-.43, -.64), xytext=(.0, -1.22), ha="center",
                    arrowprops=dict(arrowstyle="->", color="#3e4950"))
        ax.text(-1.55, 0, "Cornea", rotation=90, va="center", ha="center", color="#176173")
        ax.set(title="Injured eye in cross section  •  schematic", aspect="equal",
               xlim=(-1.7, 1.55), ylim=(-1.34, 1.14))
        ax.axis("off")
        save(fig, "acuteeye_" + name)

    # Locations are projected onto the face. The medial canthus is next to the nose.
    for name, point, callout in [("sacsite", (.94, -.21), (1.25, -.94)),
                                 ("glandsite", (-.80, .58), (-.85, 1.03))]:
        fig, ax = plt.subplots(figsize=(5.4, 3.3), layout="constrained")
        x = np.linspace(-1, .82, 110)
        arch = np.sin(np.pi * (x + 1) / 1.82)
        ax.fill_between(x, -.26 * arch, .35 * arch, color="#edf4f5")
        ax.plot(x, -.26 * arch, color="#53616a", lw=2)
        ax.plot(x, .35 * arch, color="#53616a", lw=2)
        ax.add_patch(Ellipse((-.10, .04), .50, .49, facecolor="#74a0a6", edgecolor="#486873"))
        ax.add_patch(Ellipse((-.10, .04), .17, .17, color="#344a52"))
        ax.plot([1.18, 1.31, 1.44], [.52, -.19, -.65], lw=2, color="#8f786b")
        ax.text(1.36, -.8, "Nose", ha="center", fontsize=9)
        ax.add_patch(Ellipse(point, .25, .20, fc="#e6a183", ec="#953f26", lw=2))
        ax.annotate("Tender swelling", point, xytext=callout, ha="center", fontsize=10,
                    arrowprops=dict(arrowstyle="->", color="#953f26"))
        ax.set(title="Site of maximal swelling  •  schematic", aspect="equal",
               xlim=(-1.6, 1.85), ylim=(-1.1, 1.17))
        ax.axis("off")
        save(fig, "acuteeye_" + name)

    for name, onto_cornea in [("limbus_cross", True), ("limbus_spared", False)]:
        fig, ax = plt.subplots(figsize=(5.2, 3.05), layout="constrained")
        x = np.linspace(-1.8, 1.8, 150)
        arch = np.cos(np.pi * x / 3.6)
        ax.fill_between(x, -.69 * arch, .72 * arch, color="#f4f4eb", ec="#59636a", lw=2)
        ax.add_patch(Ellipse((0, 0), 1.33, 1.33, fc="#86a8ad", ec="#365468", lw=2.0))
        ax.add_patch(Ellipse((0, 0), .47, .47, fc="#344a52"))
        if onto_cornea:
            ax.add_patch(Polygon([(-1.49, -.18), (-.34, .04), (-1.38, .22)],
                                 closed=True, fc="#d59d92", ec="#9f6058", lw=1.5))
            for y in [-.13, -.04, .11]:
                ax.plot([-1.34, -.93, -.52], [y, y * .62, .04], lw=1, color="#a45146")
        else:
            ax.add_patch(Ellipse((-.94, .03), .38, .22, fc="#daca81", ec="#9e8855", lw=1.5))
        ax.annotate("Limbus", xy=(.53, .40), xytext=(1.24, .7), ha="center",
                    arrowprops=dict(arrowstyle="->", color="#43555f"))
        ax.set(title="Anterior ocular surface  •  schematic", aspect="equal",
               xlim=(-1.95, 1.95), ylim=(-.88, .98))
        ax.axis("off")
        save(fig, "acuteeye_" + name)


def neuroinfection_studies():
    """Draw simulated clinical records and data from model MCAT experiments."""
    def record(name, title, columns, rows):
        fig, ax = plt.subplots(figsize=(6.1, 2.65), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated")
        table = ax.table(cellText=rows, colLabels=columns, loc="center",
                         cellLoc="center", bbox=[.01, .08, .98, .76])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#e2edf1")
        save(fig, "neuroinf_" + name)

    for name, blood, csf in [("lowratio", 120, 24), ("normratio", 50, 30)]:
        record(name, "Paired glucose measurements", ["Sample", "Glucose (mg/dL)"],
               [["Blood", blood], ["CSF", csf]])
    for name, wbc, differential, protein, ratio in [
        ("viralcsf", 160, "88% lymphocytes", 65, "0.64"),
        ("bacscsf", 1940, "91% neutrophils", 220, "0.19"),
    ]:
        record(name, "Lumbar puncture", ["CSF measurement", "Result"],
               [["Leukocytes per µL", wbc], ["Differential", differential],
                ["Protein (mg/dL)", protein], ["CSF / blood glucose", ratio]])
    record("cryptpress", "Lumbar puncture in lateral decubitus",
           ["Measurement", "Result"],
           [["Opening pressure", "39 cm H₂O"], ["Leukocytes", "4/µL"]])
    record("eoscount", "CSF cell count and differential", ["Measurement", "Result"],
           [["Leukocytes", "200/µL"], ["Lymphocytes", "68%"],
            ["Eosinophils", "20%"], ["Other leukocytes", "12%"]])
    record("level", "Pinprick sensation on examination", ["Site", "Left", "Right"],
           [["Hand", "Normal", "Normal"], ["Upper chest", "Normal", "Normal"],
            ["Below umbilicus", "Reduced", "Reduced"], ["Foot", "Reduced", "Reduced"]])
    record("pulse", "Heart rate in two model preparations",
           ["Condition", "Before (beats/min)", "During (beats/min)"],
           [["Vagal stimulation", "82", "62"], ["Sham stimulation", "80", "78"]])
    record("receptor", "Hormone-responsive reporter (arbitrary units)",
           ["Cell line", "Vehicle", "Hormone"], [["A", 2, 9], ["B", 5, 6]])
    record("respfall", "Respiratory observations during myelitis",
           ["Time", "Vital capacity (L)", "Room-air SpO₂"],
           [["08:00", "2.8", "97%"], ["10:00", "2.0", "97%"], ["12:00", "1.2", "96%"]])
    record("toxfail", "Serial right arm examination",
           ["Day of therapy", "Shoulder abduction", "Elbow flexion"],
           [[1, "3/5", "3/5"], [7, "3/5", "3/5"], [14, "2/5", "2/5"]])
    record("msfever", "Course during a urinary tract infection",
           ["Observation", "Temperature (°C)", "Right leg strength"],
           [["Usual baseline", "36.8", "5/5"], ["During fever", "39.1", "4/5"],
            ["After recovery", "36.9", "5/5"]])
    fig, ax = axes("Time after stimulation (ms)", "Signal (offset traces)")
    for t, y, label in [(2, 1.2, "Proximal"), (4, 0, "Distal")]:
        ax.plot([0, t - .3, t, t + .35, t + .6, 6],
                [y, y, y + .8, y - .1, y, y], label=label, lw=2)
        ax.axvline(t, color="#999999", lw=.8, ls=":")
    ax.set(title="Axonal recordings  •  simulated", yticks=[], xticks=range(7))
    ax.legend(loc="upper right")
    save(fig, "neuroinf_latency")
    fig, ax = axes("Time after stimulus (ms)", "Fraction of own peak")
    ax.plot([0, 2, 5, 10, 20, 35, 60, 80], [0, 0, 1, .84, .4, .09, 0, 0],
            "o-", label="Cytosolic calcium")
    ax.plot([0, 5, 10, 20, 35, 50, 65, 80], [0, 0, .08, .6, 1, .66, .22, 0],
            "s--", label="Force")
    ax.set(title="Single muscle twitch  •  simulated")
    ax.legend()
    save(fig, "neuroinf_twitch")


def pleural_and_gas_exchange_studies():
    """Draw simulated clinical records and data from model MCAT experiments."""
    def record(name, title, columns, rows):
        fig, ax = plt.subplots(figsize=(6.1, 2.65), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated")
        table = ax.table(cellText=rows, colLabels=columns, loc="center",
                         cellLoc="center", bbox=[.01, .08, .98, .76])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#e2edf1")
        save(fig, "pleural_" + name)

    for name, residual in [("hemoclear", "Trace fluid"), ("hemoremain", "Large collection")]:
        record(name, "Follow-up after drainage of pleural blood",
               ["Observation", "First hour", "Later assessment"],
               [["Drain output (mL/h)", "180", "10"],
                ["Pleural ultrasound", "Large collection", residual]])
    record("chyllip", "Pleural fluid lipid measurements", ["Analyte", "Concentration"],
           [["Triglycerides", "248 mg/dL"], ["Total cholesterol", "65 mg/dL"]])
    record("hemohi", "Paired hematocrits", ["Specimen", "Hematocrit"],
           [["Pleural fluid", "18%"], ["Peripheral blood", "30%"]])
    for name, after, pressure in [("pzero", "After leak", 0), ("pback", "After drainage", -5)]:
        record(name, "End-expiratory pressures (cm H₂O)",
               ["State", "Alveolar pressure", "Pleural pressure"],
               [["Before", 0, -5 if name == "pzero" else 0], [after, 0, pressure]])
    fig, ax = axes("Model membrane", "Thickness (µm)")
    ax.bar(["A", "B"], [1, 2], color=COLORS, width=.48)
    ax.set(title="Equal area and oxygen gradient  •  simulated", ylim=(0, 2.3), yticks=[0, 1, 2])
    save(fig, "pleural_thick")
    record("hbcontent", "Arterial oxygen measurements", ["Patient", "PaO₂", "SaO₂", "Hemoglobin"],
           [["A", "96 mm Hg", "98%", "15 g/dL"], ["B", "96 mm Hg", "98%", "6 g/dL"]])
    record("co2trend", "Respiratory observations on oxygen",
           ["Time", "SpO₂", "PaCO₂ (mm Hg)", "pH"],
           [["09:00", "96%", 50, "7.33"], ["09:30", "96%", 66, "7.25"],
            ["10:00", "97%", 78, "7.19"]])
    fig, ax = axes("Forced expiratory time (s)", "Exhaled volume (L)")
    time = np.linspace(0, 7, 170)
    for rate, label, style in [(2.1, "A", "-"), (.65, "B", "--")]:
        ax.plot(time, 4 * (1 - np.exp(-rate * time)), style, label=label, lw=2.5)
    ax.axvline(1, color="0.5", lw=1, ls=":")
    ax.set(title="Two forced expirations  •  simulated", xticks=range(8), ylim=(0, 4.4))
    ax.legend(title="Curve")
    save(fig, "pleural_airflow")
    fig, ax = axes("Month", "Calendar year")
    for row, active in enumerate([[0, 1, 2, 11], [0, 1, 2, 3]]):
        ax.scatter(range(1, 13), [row] * 12, color="0.85", marker="s", s=65)
        ax.scatter([m + 1 for m in active], [row] * len(active), color=COLORS[0], marker="s", s=65)
    ax.set(title="Dark squares mark months with productive cough", xticks=range(1, 13),
           yticks=[0, 1], yticklabels=["Year 1", "Year 2"], ylim=(-.6, 1.6))
    save(fig, "pleural_coughpass")
    record("lymphtab", "Fluid movement in one tissue bed",
           ["Process", "Rate (mL/min)"],
           [["Filtration into tissue", 12], ["Reabsorption into capillaries", 8],
            ["Lymphatic drainage", 2]])
    fig, ax = plt.subplots(figsize=(5.4, 2.8), layout="constrained")
    ax.axis("off")
    for start, end, width in [((.07, .50), (.46, .50), 5),
                              ((.46, .50), (.86, .83), 3), ((.46, .50), (.86, .17), 3)]:
        ax.annotate("", xy=end, xytext=start, xycoords="axes fraction",
                    arrowprops=dict(arrowstyle="->", color=COLORS[0], lw=width))
    for x, y, label in [(.24,.56,"Inlet: 12 mL/s"), (.76,.86,"A: 5 mL/s"), (.74,.07,"B: ?")]:
        ax.text(x, y, label, transform=ax.transAxes, ha="center")
    ax.set_title("Steady incompressible flow  •  model")
    save(fig, "pleural_branchfig")
    fig, ax = axes("Time (min)", "Oxygen transferred (µmol)")
    for speed, label, marker in [(4, "A", "o-"), (2, "B", "s--")]:
        ax.plot([0, 1, 2, 3], [speed * t for t in range(4)], marker, label=label)
    ax.set(title="Cumulative oxygen transfer  •  simulated", xticks=range(4), yticks=range(0, 13, 2))
    ax.legend(title="Membrane")
    save(fig, "pleural_diffslope")
    record("mix", "Dry ideal gas mixtures", ["Mixture", "O₂ fraction", "Total pressure"],
           [["A", "0.20", "100 kPa"], ["B", "0.40", "50 kPa"]])
    fig, ax = axes("Position in vessel bed", "Mean pressure (mm Hg)")
    sites = ["Artery\n(inlet)", "Arteriole\n(inlet)", "Capillary\n(inlet)", "Venule\n(inlet)"]
    ax.plot(range(4), [95, 85, 35, 20], "o-", color=COLORS[0], lw=2.4)
    for i, value in enumerate([95, 85, 35, 20]):
        ax.annotate(str(value), (i, value), xytext=(0, 6), textcoords="offset points", ha="center")
    ax.set(title="Vascular bed pressure profile  •  simulated", xticks=range(4),
           xticklabels=sites, ylim=(0, 110))
    save(fig, "pleural_pressfall")


def aspiration_courses():
    """Generate two independent postoperative oxygen-requirement records."""
    for name, flows in [("asprecover", [4, 2, 0, 0]), ("asprelapse", [4, 1, 0, 3])]:
        fig, ax = axes("Hours after aspiration", "Nasal oxygen flow (L/min)")
        ax.plot([0, 12, 24, 72], flows, "o-", lw=2.2, color=COLORS[0])
        ax.set(title="Flow needed to maintain target SpO₂  •  simulated",
               xticks=[0, 12, 24, 48, 72], yticks=range(5), ylim=(-.2, 4.6))
        save(fig, "pleural_" + name)


def abdominal_emergency_studies():
    """Draw simulated clinical records and data from model MCAT experiments."""
    def record(name, title, columns, rows):
        fig, ax = plt.subplots(figsize=(6.1, 2.65), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated")
        table = ax.table(cellText=rows, colLabels=columns, loc="center",
                         cellLoc="center", bbox=[.01, .08, .98, .76])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#e2edf1")
        save(fig, "abdomen_" + name)

    for name, cells, percent in [("pmna", 640, 50), ("pmnb", 900, 20)]:
        record(name, "Ascitic fluid analysis", ["Measurement", "Result"],
               [["Nucleated cells", f"{cells}/mm³"], ["Neutrophils", f"{percent}%"]])
    record("sbpfall", "Absolute ascitic neutrophil counts", ["Time", "Neutrophils per mm³"],
           [["Before treatment", "1,200"], ["48 hours", "600"]])
    record("diffuse", "Postoperative abdominal CT",
           ["Structure", "Finding"], [["Small bowel", "Mild diffuse dilatation"],
           ["Colon", "Gas visible to rectum"], ["Focal transition", "None seen"]])
    record("transition", "CT after recurrent postoperative vomiting",
           ["Region", "Finding"], [["Proximal small bowel", "Dilated loops"],
           ["Distal ileum", "Abrupt change in caliber"], ["Beyond the change", "Collapsed bowel"]])
    record("pylchem", "Preoperative venous chemistry",
           ["Analyte", "Result"], [["Chloride", "84 mmol/L"],
           ["Bicarbonate", "38 mmol/L"], ["Potassium", "3.0 mmol/L"]])
    record("gallct", "CT in a patient with vomiting and distension", ["Site", "Finding"],
           [["Small bowel", "Dilated proximal loops"], ["Distal ileal transition", "Laminated stone in lumen"],
            ["Biliary tree", "Gas in bile ducts"]])
    record("trauma", "Observation after abdominal impact", ["Time", "BP (mm Hg)", "Exam"],
           [["Arrival", "118/76", "Localized tenderness"], ["2 hours", "108/64", "Pain increasing"],
            ["4 hours", "84/50", "Diffuse rigidity"]])
    record("pressure", "After an episode of systemic hypoperfusion", ["Observation", "Finding"],
           [["BP during procedure", "70/38 mm Hg"], ["Later symptoms", "Left-sided cramps, red stool"],
            ["CT distribution", "Segment at splenic flexure"]])
    record("resolve", "Hospital course after colonic ischemia", ["Time", "Abdominal exam", "BP (mm Hg)"],
           [["Arrival", "Left-sided tenderness", "99/64"], ["Six hours", "Less tender, soft", "119/70"]])
    fig, ax = axes("Time after injection (min)", "Activity (relative units)")
    times = [0, 5, 10, 15, 20, 25]
    for label, vals, style in [("Stomach", [0, 1, 4, 6, 8, 9], "o-"),
                               ("Focus A", [0, .8, 3.6, 5.3, 6.7, 7.8], "s--"),
                               ("Focus B", [0, 0, 0, .1, 2, 4], "^:")]:
        ax.plot(times, vals, style, label=label, lw=2)
    ax.set_title("Sequential pertechnetate activity  •  simulated")
    ax.legend()
    save(fig, "abdomen_meckcurve")
    for name, diameters in [("onepoint", [3.4, 3.4, 3.4, .65, .8, .8, .8]),
                            ("twopoint", [1.0, .55, 3.3, 3.4, 3.3, .55, 1.0])]:
        fig, ax = plt.subplots(figsize=(5.3, 2.8), layout="constrained")
        positions = np.arange(len(diameters))
        radius = np.asarray(diameters) / 2
        ax.fill_between(positions, -radius, radius, color="#dcecf0", edgecolor=COLORS[0], lw=2)
        ax.set(xlim=(-.1, 6.1), ylim=(-2, 2), xticks=[0, 6],
               xticklabels=["Proximal", "Distal"], yticks=[], xlabel="Distance along bowel",
               title="Lumen profile along a bowel segment  •  schematic")
        for edge in ["top", "right", "left"]:
            ax.spines[edge].set_visible(False)
        save(fig, "abdomen_" + name)
    fig, ax = axes("Time (min)", "Fatty acids released (µmol)")
    for vals, marker, label in [([0, 6, 12, 16], "o-", "Finely dispersed"),
                                ([0, 2, 4, 6], "s--", "Coarse droplets")]:
        ax.plot([0, 1, 2, 3], vals, marker, label=label, lw=2)
    ax.set(title="Lipase assay  •  simulated", xticks=range(4), yticks=range(0, 17, 2))
    ax.legend()
    save(fig, "abdomen_lipcurve")
    record("blankrate", "Product in an enzyme assay", ["Condition", "At 0 min", "At 4 min"],
           [["Active enzyme", "2 µmol", "18 µmol"], ["No active enzyme", "2 µmol", "6 µmol"]])
    fig, ax = axes("Substrate concentration (mM)", "Initial rate (µmol/min)")
    concentrations = np.linspace(0, 20, 201)
    for km, label, style in [(1, "A", "-"), (4, "B", "--")]:
        ax.plot(concentrations, 10 * concentrations / (km + concentrations), style, label=label, lw=2)
    ax.axhline(10, color="0.45", ls=":", label="Common maximum")
    ax.axhline(5, color="0.65", ls="-.", label="Half-maximum")
    ax.set(title="Initial-rate curves  •  simulated", ylim=(0, 11), xticks=[0, 1, 4, 10, 15, 20])
    ax.legend(loc="lower right")
    save(fig, "abdomen_km")
    record("glucose", "Apical glucose uptake in a model",
           ["Sodium gradient", "Uptake (nmol/min)"], [["Present", 9], ["Removed", 2]])
    record("buff", "Response to a matched acid challenge",
           ["Buffer", "Initial pH", "Final pH"], [["A", "6.80", "6.72"], ["B", "6.80", "6.46"]])


def hepatobiliary_studies():
    """Draw simulated clinical records and data from model MCAT experiments."""
    def record(name, title, columns, rows):
        fig, ax = plt.subplots(figsize=(6.1, 2.65), layout="constrained")
        ax.axis("off")
        ax.set_title(title + "  •  simulated")
        table = ax.table(cellText=rows, colLabels=columns, loc="center",
                         cellLoc="center", bbox=[.01, .08, .98, .76])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#e2edf1")
        save(fig, "hepatobiliary_" + name)

    record("persist", "Respiratory course in acute pancreatitis", ["Time from onset", "Respiratory organ failure"],
           [["0 hours", "Present"], ["24 hours", "Present"], ["54 hours", "Still present"]])
    record("mirreport", "Biliary imaging report", ["Structure", "Finding"],
           [["Gallbladder neck", "Impacted stone"], ["Common hepatic duct", "Compressed beside the stone"],
            ["Intrahepatic ducts", "Dilated"], ["Distal common duct", "Normal caliber"]])
    for name, free in [("hvhigh", 6), ("hvlow", 13)]:
        record(name, "Hepatic venous catheterization", ["Measurement", "Pressure"],
               [["Wedged hepatic venous", "18 mm Hg"], ["Free hepatic venous", f"{free} mm Hg"]])
    record("rotorlab", "Urinary coproporphyrin profile", ["Measurement", "Finding"],
           [["Total coproporphyrins", "3 times upper limit"], ["Fraction of isomer I", "65%"]])
    record("hempanel", "Blood tests for jaundice", ["Measurement", "Result"],
           [["Total / direct bilirubin", "5.1 / 0.4 mg/dL"], ["Hemoglobin", "8.1 g/dL"],
            ["Reticulocytes", "9%"], ["Alkaline phosphatase", "Within reference range"]])
    record("cholpanel", "Blood tests for jaundice", ["Measurement", "Result"],
           [["Total / direct bilirubin", "5.1 / 4.4 mg/dL"], ["Hemoglobin", "14.2 g/dL"],
            ["Alkaline phosphatase", "5 × upper limit"], ["ALT", "1.5 × upper limit"]])
    record("rhigh", "Liver tests at presentation", ["Analyte", "Result", "Upper limit"],
           [["ALT", "640 U/L", "40 U/L"], ["Alkaline phosphatase", "240 U/L", "120 U/L"]])
    record("pscmrcp", "MR cholangiography", ["Ducts assessed", "Observation"],
           [["Intrahepatic", "Multiple short narrow segments"], ["Extrahepatic", "Irregular caliber and focal strictures"],
            ["Common duct stone", "None identified"]])
    record("pbcstudy", "Evaluation of persistent cholestasis", ["Study", "Result"],
           [["MR cholangiography", "Smooth, patent large ducts"], ["Antimitochondrial antibody", "Strongly positive"]])
    for name, score in [("lillea", "0.19"), ("lilleb", "0.71")]:
        record(name, "Treatment response assessment", ["Time after starting prednisolone", "Lille score"],
               [["Day 7", score]])
    fig, ax = axes("Heartbeats after right atrial opacification", "Contrast intensity (relative)")
    ax.plot(range(8), [1, .9, .8, .7, .6, .45, .3, .2], "o-", label="Right atrium")
    ax.plot(range(8), [0, 0, 0, 0, 0, .25, .4, .42], "s--", label="Left atrium")
    ax.set_title("Agitated-saline study  •  schematic")
    ax.legend()
    save(fig, "hepatobiliary_bubble")

    for name, distal in [("cystblock", False), ("distblock", True)]:
        fig, ax = plt.subplots(figsize=(5, 3.6), layout="constrained")
        ax.set(xlim=(0, 8), ylim=(0, 6.4), aspect="equal")
        ax.axis("off")
        def channel(x, y):
            ax.plot(x, y, lw=5, color=COLORS[0], solid_capstyle="round")
        for x, y in [([1.5, 2.5, 4, 4], [5.5, 5, 4.3, .9]),
                     ([2.3, 2.5], [5.9, 5]), ([5.2, 4.7, 4], [5.6, 5.1, 4.3]),
                     ([5.8, 4.7], [5.35, 5.1])]:
            channel(x, y)
        ax.text(.25, 5.98, "Liver ducts")
        if distal:
            channel([3.55, 4], [3.1, 2.8])
            ax.text(.1, 3.1, "Cystic duct stump")
        else:
            channel([2.15, 3, 4], [3.75, 3.45, 2.8])
            from matplotlib.patches import Ellipse
            ax.add_patch(Ellipse((1.73, 3.92), 1.3, .8, angle=22,
                                 facecolor="#deebd5", edgecolor=COLORS[0], lw=2))
            ax.text(.05, 4.55, "Gallbladder")
        x, y = (4, 1.85) if distal else (3.1, 3.39)
        ax.scatter([x], [y], marker="X", s=160, facecolor="#b44428", edgecolor="white", zorder=3)
        ax.text(4, .42, "To duodenum", ha="center")
        ax.set_title("Site of obstruction  •  schematic")
        save(fig, "hepatobiliary_" + name)

    record("genocount", "Genotyping results", ["Genotype", "Offspring"],
           [["AA", "27"], ["Aa", "48"], ["aa", "25"]])
    record("testcross", "Progeny of a single testcross", ["Phenotype", "Offspring"],
           [["Tall", "49"], ["Short", "51"]])
    record("hormone", "Cultured hepatocytes", ["Exposure", "Glucose released (nmol/h)"],
           [["Vehicle", "6"], ["Hormone", "18"]])
    for name, xname, yname, x, series in [
        ("lipdiff", "Temperature (°C)", "Diffusion coefficient (µm²/s)", [15, 25, 35],
         {"Preparation A": [.5, .8, 1.3], "Preparation B": [1.0, 1.7, 2.4]}),
        ("fastgraph", "Hours of fasting", "Glucose output (arbitrary units)", [6, 12, 18, 24],
         {"Glycogen breakdown": [8, 6, 4, 2], "New synthesis": [2, 4, 6, 7]}),
        ("reserves", "Elapsed time (hours)", "Glycogen (arbitrary units)", [0, 4, 8],
         {"Liver": [60, 38, 20], "Resting muscle": [60, 54, 50]})]:
        fig, ax = axes(xname, yname)
        for (label, values), style, color in zip(series.items(), STYLES, COLORS):
            ax.plot(x, values, ls=style, color=color, marker="o", lw=2, label=label)
        ax.set_xticks(x)
        ax.legend()
        save(fig, "hepatobiliary_" + name)


def postpartum_studies():
    """Draw postpartum teaching records, published trial estimates and MCAT experiments."""
    from matplotlib.patches import Circle, Rectangle

    def record(name, title, columns, rows, source="simulated"):
        fig, ax = plt.subplots(figsize=(6.1, 2.7), layout="constrained")
        ax.axis("off")
        ax.set_title(f"{title}  •  {source}")
        table = ax.table(cellText=rows, colLabels=columns, loc="center",
                         cellLoc="center", bbox=[.01, .08, .98, .76])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#e2edf1")
        save(fig, "postpartum_" + name)

    record("intake", "Newborn at five days", ["Finding", "Observation"],
           [["Weight, day 0 → 3 → 5", "3.40 → 3.18 → 3.25 kg"],
            ["Observed feeding", "Alert, audible swallows"], ["Last 24 hours", "6 wet diapers, 4 yellow stools"]])
    record("lochiadiary", "Patient bleeding diary", ["Day after birth", "Observed discharge"],
           [["2", "Moderate, red"], ["6", "Lighter, pink-brown"], ["10", "Scant, pale"]])
    for name, edv, esv in [("eflow", 160, 104), ("efhigh", 120, 48)]:
        record(name, "Left ventricular volume measurements", ["Timing", "Volume"],
               [["End diastole", f"{edv} mL"], ["End systole", f"{esv} mL"]])
    record("moodcourse", "New parent's symptom diary", ["Day after birth", "Diary entry"],
           [["3", "Tearful several times, accepting help"], ["7", "Occasional brief tearfulness"],
            ["13", "Mood back to usual"]])
    for name, now in [("txaearly", "09:40"), ("txalate", "11:35")]:
        record(name, "Postpartum hemorrhage record", ["Event", "Time today"],
               [["Birth", "08:00"], ["Current assessment", now],
                ["Tranexamic acid administered", "None"]])
    for name, pulse in [("lossstable", 84), ("losstachy", 114)]:
        record(name, "Twenty minutes after a vaginal birth", ["Measurement", "Current value"],
               [["Measured cumulative loss", "360 mL"], ["Blood pressure", "118/76 mm Hg"],
                ["Pulse", f"{pulse}/min"]])
    for name, flow in [("rvascular", "Internal vascular flow"), ("ravascular", "No flow detected within mass")]:
        record(name, "Postpartum pelvic ultrasound", ["Finding", "Observation"],
               [["Gray scale", "Focal endometrial mass"], ["Color Doppler", flow]])
    for name, tip in [("increta", 1.75), ("percreta", .58)]:
        fig, ax = plt.subplots(figsize=(5.6, 3.1), layout="constrained")
        ax.set(xlim=(0, 6.8), ylim=(0, 3.8), aspect="equal")
        ax.axis("off")
        ax.add_patch(Rectangle((.2, 1), 4.15, 2, facecolor="#e9c5b2", edgecolor="none"))
        ax.add_patch(Rectangle((.2, 3), 4.15, .42, facecolor="#ecdfbb", edgecolor="none"))
        ax.plot([.2, 4.35], [1, 1], color="#663d36", lw=2)
        ax.text(4.48, 3.16, "Placental side", va="center")
        ax.text(4.48, 2.18, "Myometrium", va="center")
        ax.text(4.48, 1, "Serosa", va="center")
        color = "#823a68"
        ax.plot([1.9, 1.9, 2.15, 2.15], [3.32, 2.86, 2.55, tip], lw=6, color=color)
        ax.plot([2.15, 2.63, 2.78], [2.48, 2.24, 2.02], lw=4, color=color)
        ax.plot([2.15, 1.65], [2.35, 2.05], lw=4, color=color)
        ax.text(.36, 3.1, "Villi", color=color, weight="bold")
        ax.set_title("Placental bed  •  schematic section")
        save(fig, "postpartum_" + name)

    record("emotive", "E-MOTIVE after vaginal birth", ["Composite outcome", "Participants with event"],
           [["Usual care", "4.3%"], ["Early detection and treatment bundle", "1.6%"]],
           source="published results")
    fig, ax = plt.subplots(figsize=(6.6, 3), layout="constrained")
    labels = ["Death or hysterectomy\n(all participants)", "Bleeding death\n(treated within 3 h)"]
    for y, estimate, low, high in [(1, .97, .87, 1.09), (0, .69, .52, .91)]:
        ax.errorbar(estimate, y, xerr=[[estimate-low], [high-estimate]],
                    fmt="o", lw=2, color=COLORS[0], capsize=5)
    ax.axvline(1, color="#595959", ls="--", lw=1)
    ax.set(yticks=[1, 0], yticklabels=labels, ylim=(-.5, 1.5), xlim=(.45, 1.16),
           xlabel="Risk ratio for tranexamic acid vs placebo (95% CI)",
           title="WOMAN trial  •  published estimates")
    save(fig, "postpartum_woman")

    record("polar", "Secondary oocytes in culture", ["Condition", "Second polar body", "Total oocytes"],
           [["No sperm", "4", "40"], ["Sperm exposure", "30", "40"]])
    fig, panels = plt.subplots(1, 3, figsize=(6.5, 2.7), layout="constrained")
    for ax, label in zip(panels, ["A", "B", "C"]):
        ax.set(xlim=(-1.2, 1.2), ylim=(-1.2, 1.2), aspect="equal", title=label)
        ax.axis("off")
        ax.add_patch(Circle((0, 0), 1, fc="#f3eee4", ec="#666", lw=1.3))
    # A central section through the compact morula, before cavitation.
    for row, count in enumerate([3, 4, 5, 4, 3]):
        y = (row - 2) * .34
        for column in range(count):
            x = (column - (count - 1) / 2) * .39
            panels[0].add_patch(Circle((x, y), .21, fc="#b4cfc8", ec=COLORS[0], lw=1))
    panels[1].add_patch(Circle((0, 0), .82, fc="#fcfaf0", ec=COLORS[0]))
    for theta in np.linspace(0, 2*np.pi, 18, endpoint=False):
        panels[1].add_patch(Circle((.89*np.cos(theta), .89*np.sin(theta)),
                                   .13, fc="#b4cfc8", ec=COLORS[0], lw=.75))
    for x, y in [(-.6, .26), (-.45, .45), (-.38, .22), (-.56, .06)]:
        panels[1].add_patch(Circle((x, y), .16, fc="#b4cfc8", ec=COLORS[0]))
    for x in [-.44, .44]:
        panels[2].add_patch(Circle((x, 0), .49, fc="#b4cfc8", ec=COLORS[0]))
    fig.suptitle("Mammalian embryonic stages  •  schematics")
    save(fig, "postpartum_stages")
    record("fate", "Transcripts per matched cell sample", ["Transcript", "Culture A", "Culture B"],
           [["Muscle marker", "2", "44"], ["Reference", "20", "20"]])
    fig, ax = axes("Minutes after ligand added", "Intracellular cAMP (relative units)")
    x = [0, 1, 2, 4, 6]
    ax.plot(x, [1, 3, 6, 4, 2], "o-", label="Ligand")
    ax.plot(x, [1, 1.1, 1.2, 1.1, 1], "s--", label="Ligand + blocker")
    ax.set_xticks(x)
    ax.legend()
    ax.set_title("Gland-cell response  •  simulated")
    save(fig, "postpartum_camp")
    record("ox", "Hormone measurements", ["Normalized signal", "Tissue A", "Tissue B"],
           [["Precursor mRNA", "95", "2"], ["Stored peptide", "32", "91"]])


def gestational_exposure_studies():
    """Draw comparative prenatal growth, dosimetry and cohort reports."""
    def record(name, title, columns, rows, source="simulated"):
        fig, ax = plt.subplots(figsize=(5.9, 2.6), layout="constrained")
        ax.axis("off")
        ax.set_title(f"{title}  •  {source}")
        table = ax.table(cellText=rows, colLabels=columns, loc="center",
                         cellLoc="center", bbox=[.015, .08, .97, .76])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#e2edf1")
        save(fig, "gestexposure_" + name)

    for name, weight, ac in [("fgrlow", "6th", "8th"), ("fgrnormal", "45th", "48th")]:
        record(name, "Third-trimester growth scan", ["Measurement", "Percentile for gestational age"],
               [["Estimated fetal weight", weight], ["Abdominal circumference", ac]])
    for name, dose in [("radev", "200 mGy"), ("radlow", "1 mGy")]:
        record(name, "Physicist's exposure reconstruction", ["Parameter", "Estimate"],
               [["Timing after conception", "8 days"], ["Absorbed dose to embryo", dose]])
    for name, label, value, lo, hi in [
        ("sscrude", "All pregnancies, unadjusted", 1.25, 1.13, 1.38),
        ("ssadjust", "Depression cohort, adjusted", 1.06, .93, 1.22)]:
        fig, ax = plt.subplots(figsize=(5.7, 2.55), layout="constrained")
        ax.axvline(1, ls="--", color="#585858")
        ax.errorbar(value, 0, xerr=[[value-lo], [hi-value]], fmt="o", capsize=6, color=COLORS[0], lw=2)
        ax.set(xlim=(.85, 1.45), ylim=(-.7, .7), yticks=[],
               xlabel="Risk ratio for any cardiac defect (95% CI)", title=label)
        ax.text(value, .2, f"{value:.2f} ({lo:.2f}–{hi:.2f})", ha="center")
        save(fig, "gestexposure_" + name)


def neonatal_and_mechanics_studies():
    """Render original neonatal studies, published trial results and mechanics exercises."""
    from matplotlib.patches import Circle, Polygon, Rectangle

    def record(name, title, columns, rows, source="simulated"):
        fig, ax = plt.subplots(figsize=(6.1, 2.65), layout="constrained")
        ax.axis("off")
        ax.set_title(f"{title}  •  {source}")
        table = ax.table(cellText=rows, colLabels=columns, loc="center",
                         cellLoc="center", bbox=[.01, .08, .98, .76])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#e2edf1")
        save(fig, "neonatal_" + name)

    for name, minute in [("sat5", 5), ("sat10", 10)]:
        record(name, "Delivery-room observations", ["Time since birth", "Right-hand SpO₂", "Heart rate"],
               [[f"{minute} minutes", "82%", "146/min"]])
    for name, hand, foot in [("postlow", "97%", "89%"), ("prelow", "89%", "97%")]:
        record(name, "Paired newborn oximetry", ["Sample site", "Oxygen saturation"],
               [["Right hand", hand], ["Foot", foot]])
    record("mask", "Mask ventilation at birth", ["Observation", "Initial", "After mask breaths"],
           [["Heart rate", "78/min", "76/min"], ["Chest movement", "Absent", "Absent"]])
    for name, support in [("bpdcpap", "Nasal CPAP"), ("bpdvent", "Endotracheal ventilation")]:
        record(name, "Very preterm infant at 36 weeks PMA", ["Observation", "Finding"],
               [["Respiratory support", support], ["FiO₂", "0.25"]])
    for name, dilation, turns in [("ropquiet", "Within expected limits", "Within expected limits"),
                                  ("ropplus", "Marked dilation", "Marked tortuosity")]:
        record(name, "Retinal specialist report", ["Posterior pole assessment", "Finding"],
               [["Veins", dilation], ["Arterioles", turns],
                ["Overall plus criteria", "Met" if name == "ropplus" else "Absent"]])
    for name, total, direct in [("indirect", "12.0", "0.4"), ("direct", "6.0", "4.2")]:
        record(name, "Serum bilirubin fractions", ["Measurement", "Result"],
               [["Total", total + " mg/dL"], ["Direct", direct + " mg/dL"]])
    record("rhtrend", "Follow-up after immune hemolysis", ["Measurement", "Day 7", "Week 4"],
           [["Hemoglobin", "13.8 g/dL", "7.6 g/dL"], ["Total bilirubin", "10.0 mg/dL", "2.2 mg/dL"]])
    record("glucose", "Day five, regular feeds continue", ["IV glucose delivery", "Plasma glucose"],
           [["Higher rate", "78 mg/dL"], ["After reducing rate", "39 mg/dL"]])
    record("sizes", "Birthweight reference for two newborn boys", ["Infant", "Birth weight", "Gestation", "Chart percentile"],
           [["A", "2.40 kg", "35 weeks", "40th"], ["B", "2.40 kg", "39 weeks", "2nd"]])

    fig, ax = axes("Distending pressure (arbitrary units)", "Lung volume (arbitrary units)")
    x = [0, 1, 2, 3, 4]
    for label, vals, style in [("A", [0, 2, 4, 6, 8], "o-"), ("B", [0, 1, 2, 3, 4], "s--")]:
        ax.plot(x, vals, style, lw=2, label=label)
    ax.set_title("Model lung inflation over a limited pressure range")
    ax.legend()
    save(fig, "neonatal_compliance")
    fig, panels = plt.subplots(1, 2, figsize=(6.2, 2.9), layout="constrained")
    for ax, label in zip(panels, ["One sphere • radius r", "Eight spheres • radius r/2"]):
        ax.set(xlim=(-2.2, 2.2), ylim=(-1.35, 1.35), aspect="equal", title=label)
        ax.axis("off")
    panels[0].add_patch(Circle((0, 0), 1, fc="#d8e9ed", ec=COLORS[0], lw=2))
    for y in [-.53, .53]:
        for x in [-1.56, -.52, .52, 1.56]:
            panels[1].add_patch(Circle((x, y), .5, fc="#d8e9ed", ec=COLORS[0], lw=1.5))
    fig.suptitle("Equal total gas volume • spherical model")
    save(fig, "neonatal_alveoli")
    record("esctime", "ESC-NOW trial, infants born at ≥36 weeks",
           ["Care approach", "Birth to medical readiness"], [["Usual care", "14.9 days"], ["Eat, Sleep, Console", "8.2 days"]],
           source="published means")
    record("coolprob", "Cooling trial, infants born at 33–35 weeks",
           ["Outcome", "Posterior probability of harm"], [["Death or disability", "74%"], ["Death", "87%"]],
           source="published estimates")

    fig, ax = axes("Time (s)", "Position (m)")
    times = [0, 1, 2, 3, 4]
    ax.plot(times, [1, 3, 3, 0, 1], "o-", color=COLORS[0], lw=2)
    for x, y, label in [(.5, 1.75, "A"), (1.5, 3.12, "B"), (2.6, 1.65, "C"), (3.5, .7, "D")]:
        ax.text(x, y, label, weight="bold")
    ax.set(xticks=times, ylim=(-.2, 3.55))
    save(fig, "neonatal_motion")
    fig, ax = plt.subplots(figsize=(5.8, 2.6), layout="constrained")
    ax.set(xlim=(-3.2, 4.2), ylim=(-1.4, 1.5), aspect="equal")
    ax.axis("off")
    ax.add_patch(Rectangle((-.65, -.45), 1.3, .9, fc="#d8e9ed", ec=COLORS[0]))
    ax.text(0, 0, "3 kg", ha="center", va="center")
    for end, edge, label in [(3.7, .65, "10 N"), (-1.87, -.65, "4 N")]:
        ax.annotate("", xy=(end, 0), xytext=(edge, 0), arrowprops=dict(arrowstyle="-|>", lw=2.6))
        ax.text((end+edge)/2, .25, label, ha="center")
    ax.set_title("Horizontal forces acting on the cart")
    save(fig, "neonatal_arrows")
    record("netdata", "Matched cart mass", ["Trial", "Rightward force", "Leftward force"],
           [["A", "9 N", "5 N"], ["B", "5 N", "6 N"], ["C", "3 N", "0 N"]])
    fig, ax = plt.subplots(figsize=(6, 2.7), layout="constrained")
    ax.set(xlim=(-.31, .52), ylim=(-.15, .26), aspect="equal")
    ax.axis("off")
    ax.plot([-.24, .44], [0, 0], lw=5, color=COLORS[0])
    ax.add_patch(Polygon([(-.04,-.067),(.04,-.067),(0,-.005)], color="#666"))
    for x, label in [(-.2, "12 N"), (.4, "X")]:
        ax.annotate("",xy=(x,.002),xytext=(x,.15),arrowprops=dict(arrowstyle="-|>",lw=2))
        ax.text(x,.17,label,ha="center")
    ax.text(-.12,-.05,"0.20 m",ha="center")
    ax.text(.2,-.05,"0.40 m",ha="center")
    ax.set_title("Massless beam with a frictionless pivot")
    save(fig, "neonatal_beam")
    for name, xlab, ylab, xv, yv in [
        ("torread", "Perpendicular distance (m)", "Torque magnitude (N·m)", [0,.1,.2,.3], [0,.8,1.6,2.4]),
        ("workarea", "Position (m)", "Pull in direction of travel (N)", [0,1,2,3], [0,2,4,6])]:
        fig, ax = axes(xlab, ylab)
        ax.plot(xv, yv, "o-", color=COLORS[0], lw=2)
        ax.set(xticks=xv, yticks=yv)
        save(fig, "neonatal_" + name)
    record("energies", "Cart on a rough track", ["Energy", "Start", "Finish"],
           [["Kinetic", "2 J", "7 J"], ["Gravitational potential", "10 J", "2 J"]])
    fig, ax = axes("Time (s)", "Displacement (cm)")
    t = np.linspace(0,6,181)
    ax.plot(t, 2*np.cos(np.pi*t), color=COLORS[0], lw=2)
    ax.set(xticks=range(7), yticks=[-2,-1,0,1,2])
    save(fig, "neonatal_wave")


def nursery_studies():
    """Render neonatal case data, congenital CMV trial outcomes and MCAT study figures."""

    def record(name, title, columns, rows, source="simulated"):
        fig, ax = plt.subplots(figsize=(6.1, 2.65), layout="constrained")
        ax.axis("off")
        ax.set_title(f"{title}  •  {source}")
        table = ax.table(cellText=rows, colLabels=columns, loc="center",
                         cellLoc="center", bbox=[.01, .08, .98, .76])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#e2edf1")
        save(fig, "nursery_" + name)

    for name, antibody in [("hbimmune", 65), ("hblow", 4)]:
        record(name, "Postvaccination testing at ten months", ["Test", "Infant serum"],
               [["HBsAg", "Negative"], ["Anti-HBs", f"{antibody} mIU/mL"]])
    for name, infant in [("syhigh", 32), ("sylow", 16)]:
        record(name, "Serum at delivery • same laboratory", ["Specimen", "Quantitative RPR"],
               [["Mother", "1:8"], ["Infant", f"1:{infant}"]])
    record("parvohigh", "Fetal ultrasound series", ["Gestational age", "MCA peak velocity", "Hydrops"],
           [["21 weeks", "1.10 MoM", "Absent"], ["24 weeks", "1.80 MoM", "Present"]])
    record("cmvstudy", "Valganciclovir duration trial", ["Outcome and time", "P value"],
           [["Best-ear change, 6 mo (primary)", "0.41"],
            ["Total-ear result, 12 mo (secondary)", "0.01"]], "Kimberlin et al.")
    fig, ax = axes("Assigned treatment duration", "Evaluable ears (%)")
    bars = ax.bar(["6 weeks", "6 months"], [57, 73], color=COLORS[:2], width=.55)
    ax.bar_label(bars, fmt="%d%%")
    ax.set(ylim=(0,100), title="Improved or normal hearing at 12 months")
    save(fig, "nursery_cmvears")
    fig, ax = axes("Temperature (°C)", "Fraction folded")
    temp = np.arange(20, 91)
    for midpoint, label, style in [(65, "A", "-"), (45, "B", "--")]:
        ax.plot(temp, 1/(1 + np.exp((temp-midpoint)/4)), style, lw=2, label=label)
    ax.axhline(.5, color="0.55", lw=1, ls=":")
    ax.set_title("Thermal unfolding • simulated")
    ax.legend(title="Preparation")
    save(fig, "nursery_melt")
    fig, ax = axes("Time (s)", "Corrected position (µm)")
    ax.plot([0,2,4,6,8], [0,1,2,3,3], "o-")
    ax.set(xticks=[0,2,4,6,8], yticks=[0,1,2,3], title="Motion along a track • simulated")
    save(fig, "nursery_motor")
    fig, ax = axes("Days after exposure", "Antibody concentration (a.u.)")
    times = [0,2,4,6,8,10,12]
    ax.plot(times, [0,0,0,1,2,3,4], "o-", label="A")
    ax.plot(times, [1,3,7,11,14,16,16], "s--", label="B")
    ax.set_title("Antigen-specific antibody • simulated")
    ax.legend(title="Group")
    save(fig, "nursery_antibody")
    record("renal", "Renal balance of solute X", ["Period", "Filtered (mg/min)", "Excreted (mg/min)"],
           [["A", "12", "7"], ["B", "10", "14"]])
    record("screen", "Screening records", ["Clinic", "Eligible", "Completed"],
           [["A", "200", "120"], ["B", "400", "180"]])


def coagulation_studies():
    """Render simulated hematology and MCAT studies and published bleeding-trial outcomes."""

    def record(name, title, columns, rows, source="simulated"):
        fig, ax = plt.subplots(figsize=(6.1, 2.65), layout="constrained")
        ax.axis("off")
        ax.set_title(f"{title}  •  {source}")
        table = ax.table(cellText=rows, colLabels=columns, loc="center",
                         cellLoc="center", bbox=[.01, .08, .98, .76])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for col in range(len(columns)):
            table[0, col].set_facecolor("#e2edf1")
        save(fig, "coag_" + name)

    for name, recipient, unit in [("aboerr", "O positive", "A positive"),
                                  ("abook", "A positive", "O positive")]:
        record(name, "Red-cell transfusion record", ["Specimen", "ABO and RhD"],
               [["Recipient", recipient], ["Donor red cells", unit]])
    for name, viii, ix in [("ha", "1", "98"), ("hb", "96", "1")]:
        record(name, "Plasma activity and antigen", ["Assay", "Patient (%)", "Reference (%)"],
               [["Factor VIII activity", viii, "50–150"], ["Factor IX activity", ix, "50–150"],
                ["VWF antigen", "95", "50–150"], ["VWF activity", "91", "50–150"]])
    record("vwratio", "VWF testing at baseline health", ["Test", "Result (IU/dL)"],
           [["VWF antigen", "60"], ["Platelet-dependent VWF activity", "24"]])
    record("glanz", "Platelet function panel", ["Agonist", "Response"],
           [["ADP", "Absent"], ["Collagen", "Absent"], ["Arachidonic acid", "Absent"],
            ["Ristocetin", "Preserved"]])
    fig, ax = axes("Day of heparin exposure", "Platelets (thousands/µL)")
    ax.plot([0,2,4,5,6,7], [295,301,288,241,162,102], "o-")
    ax.set(ylim=(0,350), title="Serial platelet counts • simulated")
    save(fig, "coag_hitcount")
    record("cbs", "Amino-acid evaluation", ["Analyte", "Patient (µmol/L)", "Lab reference"],
           [["Total homocysteine", "182", "5–15"], ["Methionine", "112", "15–45"]])
    for name, weeks in [("acl8", 8), ("acl14", 14)]:
        record(name, "Anticardiolipin IgG • same assay", ["Time after first draw", "Laboratory category"],
               [["Baseline", "High positive"], [f"Week {weeks}", "High positive"]])
    record("loss", "After hemorrhage control", ["Time", "Hemoglobin", "Crystalloid since control"],
           [["At control", "12.1 g/dL", "None"], ["Two hours later", "10.3 g/dL", "2 L"]])
    fig, ax = axes("Assigned transfusion threshold", "Estimated six-week survival (%)")
    bars = ax.bar(["Hb <7 g/dL", "Hb <9 g/dL"], [95,91], color=COLORS[:2], width=.55)
    ax.bar_label(bars, fmt="%d%%")
    ax.set(ylim=(0,106), title="Acute upper GI bleeding • Villanueva et al.")
    save(fig, "coag_survive")
    record("ionprod", "Silver chloride • Ksp = 1.8 × 10⁻¹⁰", ["Sample", "Ion product Q"],
           [["A", "1.0 × 10⁻¹¹"], ["B", "5.0 × 10⁻¹⁰"]])
    # Solve charge balance for a monoprotic acid titrated with strong base.
    volumes = np.linspace(0, 30, 301)
    ph = []
    ka = 10**-4.8
    for volume in volumes:
        acid_total = 0.1 * 20 / (20 + volume)
        sodium = 0.1 * volume / (20 + volume)
        lo, hi = 0., 14.
        for _ in range(55):
            mid = (lo + hi) / 2
            h = 10**-mid
            if h + sodium > acid_total * ka / (ka + h) + 1e-14 / h:
                lo = mid
            else:
                hi = mid
        ph.append((lo + hi) / 2)
    fig, ax = axes("Strong base added (mL)", "pH")
    ax.plot(volumes, ph, lw=2)
    ax.axvline(20, color=COLORS[1], ls="--", label="Equivalence")
    ax.plot(10, ph[100], "o", color=COLORS[0])
    ax.annotate(f"pH {ph[100]:.1f}", xy=(10,ph[100]), xytext=(8,7),
                arrowprops={"arrowstyle":"->"})
    ax.set(ylim=(0,14), xticks=[0,5,10,15,20,25,30], title="Titration of a weak acid • simulated")
    ax.legend()
    save(fig, "coag_titr")
    fig, ax = axes("Chase time (min)", "Labeled protein (relative units)")
    times = [0,5,10,20,30,40]
    ax.plot(times, [90,82,63,25,10,3], "o-", label="ER")
    ax.plot(times, [3,10,29,56,41,21], "s--", label="Golgi")
    ax.set_title("Secretory protein pulse–chase • simulated")
    ax.legend()
    save(fig, "coag_pulse")
    record("cilia", "Ciliary motion", ["Measurement", "Control", "Treated"],
           [["Cilia per cell", "42", "42"], ["Mean beats per second", "12", "3"]])
    record("committee", "Committee decisions", ["Group", "Seats", "Submitted", "Adopted"],
           [["A", "12", "10", "2"], ["B", "4", "10", "8"]])
    record("allocation", "Employee development budget", ["Job grade", "Employees", "Annual funds"],
           [["H", "40", "$24,000"], ["L", "80", "$24,000"]])


def study_table(name, title, columns, rows, source="simulated", *, indexed=False):
    fig, ax = plt.subplots(figsize=(6.1, 2.65), layout="constrained")
    ax.axis("off")
    ax.set_title(f"{title}  •  {source}")
    table = ax.table(cellText=rows, colLabels=columns, loc="center",
                     cellLoc="center", bbox=[.01, .08, .98, .76])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for col in range(len(columns)):
        table[0, col].set_facecolor("#e2edf1")
    save(fig, name, indexed=indexed)


def blood_cell_studies():
    """Render blood-cell cases, published trial comparisons and MCAT metabolism figures."""

    def comparison(name, title, ylabel, groups, vals, ceiling):
        fig, ax = axes("Trial group", ylabel)
        bars = ax.bar(groups, vals, color=COLORS[:len(vals)], width=.55)
        ax.bar_label(bars, labels=[f"{v:g}%" for v in vals], padding=3)
        ax.set(ylim=(0,ceiling), title=title)
        save(fig, "bloodcell_" + name)

    comparison("pktrial", "Sustained hemoglobin response • ACTIVATE",
               "Participants meeting endpoint (%)", ["Mitapivat", "Placebo"], [40,0], 100)
    comparison("cytopv", "CV death or major thrombosis • CYTO-PV",
               "Participants with an event (%)", ["Hct target <45%", "Hct target 45–50%"], [2.7,9.8], 13)
    from matplotlib.patches import Circle
    fig, panels = plt.subplots(1, 2, figsize=(5.5,2.3), layout="constrained")
    for ax,title in zip(panels,["Cell A", "Cell B"]):
        ax.set(aspect="equal", xlim=(-1.55,1.55), ylim=(-1.06,1.06), title=title)
        ax.axis("off")
    # Biconcave cross-section and sphere of equal volume. Radial integration
    # of twice the half-thickness gives the model disc volume.
    r = np.linspace(0, 1.4, 801)
    u = r / r[-1]
    h = np.sqrt(1-u*u) * (.24 + .84*u*u)
    vol = 4 * np.pi * np.trapezoid(r*h, r)
    x = np.r_[-r[:0:-1],r]
    y = np.r_[h[:0:-1],h]
    panels[0].fill_between(x, -y, y, color="#d98a85", edgecolor="#783534")
    panels[1].add_patch(Circle((0,0),(3*vol/(4*np.pi))**(1/3),
                               facecolor="#d98a85",edgecolor="#783534"))
    fig.suptitle("Equal cell volumes • schematic cross sections")
    save(fig, "bloodcell_shapes")
    study_table("bloodcell_sideriron", "Iron studies", ["Test","Result","Laboratory interval"],
           [["Iron saturation","78%","20–50%"],["Ferritin","490 µg/L","30–300 µg/L"]])
    study_table("bloodcell_thala", "Hemoglobin fractions • untransfused adult", ["Fraction","Result","Lab interval"],
           [["HbA","93.5%","95–98%"],["HbA₂","5.5%","2.0–3.5%"],["HbF","1.0%","0–2%"]])
    for name,seg,band in [("wbcA",58,2),("wbcB",8,2)]:
        study_table("bloodcell_" + name, "Manual differential", ["WBC","Segmented neutrophils","Bands"],
               [["3,000/µL",f"{seg}%",f"{band}%"]])
    for name,neut,lymph in [("leukA",85,10),("leukB",20,75)]:
        study_table("bloodcell_" + name, "White-cell differential", ["WBC","Neutrophils","Lymphocytes"],
               [["24,000/µL",f"{neut}%",f"{lymph}%"]])
    days = np.arange(0, 43, 2)
    cycle = np.maximum(.05, 2.4 - 2.55*np.exp(-((days-7)/3.3)**2)
                                   - 2.55*np.exp(-((days-28)/3.3)**2))
    persistent = .15 + .055*np.cos(days/4)
    for key, vals in [("cycle",cycle),("persist",persistent)]:
        fig, ax = axes("Day", "ANC (×10⁹/L)")
        ax.plot(days, vals, "o-", lw=1.5, ms=3)
        ax.axhline(.5, ls=":", color="0.5", label="0.5 ×10⁹/L")
        ax.set(ylim=(0,3),xticks=[0,7,14,21,28,35,42],title="Serial differentials • simulated")
        ax.legend()
        save(fig, "bloodcell_" + key)
    study_table("bloodcell_panret", "Adult CBC and reticulocytes", ["Measurement","Patient","Lab interval"],
           [["Hemoglobin","7.0 g/dL","12–16"],["WBC","2,100/µL","4,000–11,000"],
            ["Platelets","42,000/µL","150,000–400,000"],["Absolute reticulocytes","8,000/µL","25,000–100,000"]])
    study_table("bloodcell_aplaanc", "Two patients with severe aplastic anemia", ["Measurement","Patient A","Patient B"],
           [["Marrow cellularity","10%","10%"],["Platelets (/µL)","12,000","12,000"],
            ["Reticulocytes (/µL)","15,000","15,000"],["ANC (/µL)","350","120"]])
    study_table("bloodcell_couple", "Reaction over one minute", ["Preparation","ATP used (nmol)","Product (nmol)"],
           [["A","25","24"],["B","25","0.2"]])
    study_table("bloodcell_flux", "Liver glucose release from labeled lactate", ["Condition","Labeled glucose (nmol/min)"],
           [["Baseline","2"],["After hormone","7"]])
    study_table("bloodcell_citrate", "Citrate formed from labeled acetyl groups", ["Isotope class","Molecules per 100"],
           [["M+0","30"],["M+1","0"],["M+2","70"]])
    study_table("bloodcell_substrate", "Tracer carbon balance", ["Substrate","Label supplied","Label in CO₂"],
           [["Palmitate","100 units","24 units"],["Alanine","100 units","36 units"]])
    study_table("bloodcell_resp", "Isolated mitochondria • equal assay times", ["Condition","ATP produced (nmol)","O₂ used (nmol)"],
           [["A","100","20"],["B","70","35"]])
    study_table("bloodcell_pairs", "Free-energy changes (kJ/mol)", ["Pair","First reaction","Second reaction"],
           [["A","+6","−2"],["B","+6","−11"]])
    fig, ax = axes("Temperature (K)", "ΔG° (kJ/mol)")
    temp = np.arange(250,551,5)
    ax.plot(temp, 40 - .1*temp)
    ax.axhline(0, ls=":", color="0.4")
    ax.set(xticks=[250,300,350,400,450,500,550],title="Reaction at standard conditions • model")
    save(fig, "bloodcell_therm")
    fig, ax = axes("Time (s)", "Product concentration (mM)")
    t = np.linspace(0,12,160)
    for label, k, style in [("A",1.1,"-"),("B",.65,"--")]:
        ax.plot(t, 5*(1-np.exp(-k*t)),style,lw=2,label=label)
    ax.set(ylim=(0,6),title="Two closed reaction mixtures • simulated")
    ax.legend()
    save(fig, "bloodcell_plateau")


def splenic_studies():
    """Render clinical records for mechanical hemolysis and splenic sequestration."""

    study_table("splenic_leak", "Follow-up after valve leak closure", ["Measurement","Before repair","Week 4","Reference"],
           [["LDH (U/L)","1,450","1,320","120–250"],["Haptoglobin (mg/dL)","<10","<10","30–200"]])
    study_table("splenic_splpool", "Cytopenias in portal hypertension", ["Finding","Result"],
           [["Spleen length","19 cm"],["Platelets","84,000/µL"],["WBC","3,100/µL"],
            ["Marrow","Preserved trilineage production"]])
    study_table("splenic_splchange", "Change from chronic baseline", ["Observation","Baseline","Today"],
           [["Platelets (/µL)","85,000","16,000"],["Hemoglobin (g/dL)","11.8","7.6"],
            ["Schistocytes","Absent","Numerous"]])


def blood_drug_studies():
    """Render co-oximetry findings and a mitochondrial energetics experiment."""

    study_table("blooddrug_coox", "Arterial sample during supplemental oxygen",
           ["Measurement","Result"], [["PaO₂","225 mm Hg"],
           ["Methemoglobin (co-oximetry)","29%"],["Carboxyhemoglobin","1%"]])
    study_table("blooddrug_passage", "Mitochondrial experiment (six donors)",
           ["Condition","O₂ (nmol/mg)","ATP (nmol/mg)","Relative ΔpH"],
           [["Vehicle","20","100","1.0"],["U","30","60","0.4"],["I","5","15","0.3"]],
           source="simulated")


def hematologic_neoplasm_studies():
    """Draw quantitative study records used by the oncology and MCAT cases."""
    for suffix, counts in [("a", [["0", "8.2", "6.4"], ["4", "8.5", "6.7"]]),
                           ("b", [["0", "7.1", "2.0"], ["4", "7.2", "2.1"]])]:
        study_table("onco_cll_" + suffix, "Peripheral blood and flow cytometry",
                    ["Month", "Lymphocytes (10⁹/L)", "Clonal B cells (10⁹/L)"], counts)

    for suffix, results in [
        ("a", [["0", "0.06", "Taking as prescribed"], ["3", "0.4", "Taking as prescribed"],
               ["4", "1.6", "Taking as prescribed"]]),
        ("b", [["0", "0.04", "Taking as prescribed"], ["3", "0.05", "Coverage ends"],
               ["4.5", "0.8", "Out of tablets for 6 weeks"]])]:
        study_table("onco_cml_" + suffix, "CML monitoring record",
                    ["Month", "BCR::ABL1 (% IS)", "Treatment history"], results)
    study_table("onco_mds_a", "Marrow and peripheral blood", ["Measure", "Patient A", "Patient B"],
                [["Marrow blasts (%)", "2", "8"], ["Hemoglobin (g/dL)", "9.2", "9.2"],
                 ["Platelets (10⁹/L)", "92", "92"]])
    study_table("onco_mds_b", "Monitoring during transfusion support",
                ["Measure", "First visit", "Repeat visit"],
                [["Hemoglobin (g/dL)", "7.6", "9.0"], ["Interval transfusion", "—", "2 RBC units"],
                 ["Marrow blasts (%)", "3", "11"]])
    study_table("onco_trial", "Early ibrutinib versus placebo in CLL",
                ["Endpoint", "Randomized comparison"],
                [["Symptomatic progression", "HR 0.276 (95% CI 0.188–0.407)"],
                 ["5-year survival", "93.3% vs 93.6%"], ["Overall survival test", "P = 0.562"]],
                source="CLL12")
    study_table("onco_cohort", "Five-year overall survival in CLL12",
                ["Cohort", "Baseline progression risk", "Survival (%)"],
                [["Ibrutinib (randomized)", "Increased", "93.3"],
                 ["Placebo (randomized)", "Increased", "93.6"],
                 ["Observation (separate)", "Lower", "97.9"]], source="CLL12")
    fig, ax = axes("DNA content per single cell", "Cells counted")
    bars = ax.bar(["2C", ">2C to 3C", ">3C to <4C", "4C"], [55, 10, 15, 20],
                  color=[COLORS[0], COLORS[1], COLORS[1], COLORS[0]])
    ax.bar_label(bars, padding=2)
    ax.set(ylim=(0, 65), title="DNA-content bins • simulated, n = 100")
    save(fig, "onco_hist")
    study_table("onco_growth", "Cells entering S phase (%)", ["Cells", "Mitogen", "Mitogen + R inhibitor"],
                [["Wild type", "62", "12"], ["Constitutively active K", "75", "70"]])
    plot("onco_repair", "Hours after UV exposure (simulated)", "Photoproducts per unit DNA",
         [0, 2, 4, 8], {"Sample A": [100, 68, 32, 10], "Sample B": [100, 96, 90, 86]})
    study_table("onco_chrom", "Accessibility signal (arbitrary units)", ["Locus", "Before", "After"],
                [["A", "48", "46"], ["B", "15", "65"], ["C", "36", "34"]])
    plot("onco_visc", "Pressure drop (kPa, simulated)", "Flow (mL/min)", [0, 1, 2, 3],
         {"Fluid A": [0, 4, 8, 12], "Fluid B": [0, 2, 4, 6]})
    study_table("onco_cycle", "Mean fractions of viable single cells",
                ["Condition", "4C DNA (%)", "Mitotic marker positive (%)"],
                [["Vehicle", "20", "5"], ["Compound X", "60", "6"]])


def hematologic_infection_studies():
    """Simulated records for clinical decisions in immune and infectious disorders."""
    study_table("bloodimmune_deng_a", "Dengue at defervescence",
                ["Measure", "First exam", "After initial fluid"],
                [["Hematocrit (%)", "43", "50"], ["BP (mm Hg)", "92/68", "86/69"],
                 ["Capillary refill (s)", "4", "4"], ["Overt bleeding", "None", "None"]])
    study_table("bloodimmune_deng_b", "Dengue during resuscitation",
                ["Measure", "First exam", "After initial fluid"],
                [["Hematocrit (%)", "44", "31"], ["BP (mm Hg)", "90/66", "80/58"],
                 ["Capillary refill (s)", "4", "5"], ["Overt bleeding", "None", "Hematemesis"]])
    study_table("bloodimmune_sab", "Monitoring during antimicrobial therapy",
                ["Measure", "At diagnosis", "48 hours later"],
                [["Temperature (°C)", "39.0", "37.1"], ["Blood cultures", "S. aureus", "S. aureus"]])
    study_table("bloodimmune_pnh", "Blood lineage flow cytometry",
                ["Cells", "GPI-deficient (%)"], [["Red cells", "8"], ["Granulocytes", "52"],
                 ["Monocytes", "50"]])
    study_table("bloodimmune_ttp", "Pretreatment microangiopathy evaluation",
                ["Test", "Result"], [["ADAMTS13 activity", "65% (reference 50–150%)"],
                 ["Platelets", "45 × 10⁹/L"], ["Blood film", "Schistocytes"]])
    study_table("bloodimmune_cryo", "Kidney function during a vasculitic flare",
                ["Measure", "Day 1", "Day 6"], [["Creatinine (mg/dL)", "1.2", "3.0"],
                 ["Urine microscopy", "Dysmorphic RBCs", "Red-cell casts"]])
    study_table("bloodimmune_bland", "Kidney findings during cutaneous purpura",
                ["Measure", "Baseline", "Today"], [["Creatinine (mg/dL)", "0.8", "0.8"],
                 ["Urine RBCs (/HPF)", "0–1", "0–1"], ["Urine protein", "Negative", "Negative"]])


def lymphoma_staging():
    """Schematic nodal distributions above and below the diaphragm."""
    for name, involved in [("a", {"Cervical", "Mediastinal"}),
                           ("b", {"Cervical", "Inguinal"})]:
        fig, ax = plt.subplots(figsize=(4.8, 3.6), layout="constrained")
        ax.set(xlim=(-1, 5), ylim=(-0.8, 4.6), title="Nodal disease • schematic")
        ax.axis("off")
        ax.axhline(2.15, color="#425663", ls="--", lw=1)
        ax.text(3.8, 2.27, "Diaphragm", ha="center", fontsize=9)
        positions = [("Cervical", 4), ("Mediastinal", 3), ("Para-aortic", 1.35), ("Inguinal", .35)]
        for label, y in positions:
            active = label in involved
            ax.scatter([.5], [y], s=150, marker="s" if active else "o",
                       facecolors=COLORS[0] if active else "white", edgecolors=COLORS[0])
            ax.text(.9, y, label, va="center")
        ax.text(.45, -.45, "Filled square = involved region", va="center", fontsize=9)
        save(fig, "depthcase_stage_" + name)


def communication_decision_records():
    """Simulated decision aids and operative inventories for independent reviews."""
    for name, risks in [("rhigh", [40, 20]), ("rlow", [10, 5])]:
        study_table("visit_" + name, "One-year outcomes per 1,000 people",
                    ["Outcome", "Usual care", "With treatment"],
                    [["Stroke", *risks], ["Major bleed", 3, 8]])
    for name, final, note in [("counta", 14, "No packing planned"),
                              ("countb", 15, "Possible sponge seen in wound")]:
        study_table("visit_" + name, "Closing sponge inventory",
                    ["Record entry", "Quantity or finding"],
                    [["First pack opened", 10], ["Second pack opened", 5],
                     ["Recovered at final count", final], ["Team observation", note]])


def medication_safety_records():
    """Draw the order and documentation exhibits and two published study summaries."""
    for name, supplied in [("dform", ["20 mg", "extended release"]),
                           ("dstrength", ["40 mg", "immediate release"])]:
        study_table("safecare_" + name, "Dispensing record for training medicine A",
                    ["Source", "Strength per tablet", "Formulation"],
                    [["Prescription", "20 mg", "immediate release"], ["Supplied", *supplied]])
    for name, amount, vol in [("calc1", 300, 100), ("calc2", 200, 100)]:
        study_table("safecare_" + name, "Training infusion preparation",
                    ["Finished bag", "Amount"], [["Total drug (mg)", amount], ["Final volume (mL)", vol]])
    study_table("safecare_copy_a", "Two signed skin assessments",
                ["Signed", "Description", "Source of finding"],
                [["Monday", "Blanching rash", "Bedside examination"],
                 ["Tuesday", "Blanching rash", "Copied from Monday"]])
    study_table("safecare_copy_b", "Laboratory result timeline",
                ["Event", "Day"], [["Specimen collected", "Monday"], ["Result posted", "Thursday"]])
    study_table("safecare_flag", "Validation of an electronic ordering signal",
                ["Order sessions", "Count"], [["Evaluated positive flags", 223],
                ["Confirmed wrong-patient events", 170]], source="Adelman et al.")
    study_table("safecare_ipass", "Events per 100 pediatric admissions",
                ["Event", "Before", "After"], [["Medical errors", 24.5, 18.8],
                 ["Preventable adverse events", 4.7, 3.3]], source="I-PASS study")


def social_psychology_studies():
    """Simulated comparisons for independently graded MCAT questions."""
    study_table("socialstudy_aud", "Accurate responses (%)", ["Task", "Alone", "With audience"],
                [["Practiced", 80, 88], ["Unfamiliar", 65, 55]])
    study_table("socialstudy_polar", "Private mean rating: −5 oppose to +5 favor",
                ["Group", "Before discussion", "After discussion"],
                [["A", "+2", "+1"], ["B", "−1", "−3"]])
    study_table("socialstudy_threat", "Mean test scores • focal group",
                ["Test framing", "Score out of 100"], [["Neutral", 74], ["Identity relevant", 68]])
    fig, ax = plt.subplots(figsize=(5.4, 2.6), layout="constrained")
    points = {"A": (0, 1), "B": (0, 0), "C": (1.2, .5), "D": (2.4, 1), "E": (2.4, 0)}
    for left, right in [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("C", "E"), ("D", "E")]:
        ax.plot(*zip(points[left], points[right]), color="#65787c", lw=2)
    for name, (x, y) in points.items():
        ax.scatter(x, y, s=430, color=COLORS[0], zorder=2)
        ax.text(x, y, name, va="center", ha="center", color="white", weight="bold")
    ax.set(xlim=(-.4, 2.8), ylim=(-.35, 1.4), title="Collaboration ties • simulated")
    ax.axis("off")
    save(fig, "socialstudy_network")
    study_table("socialstudy_model", "Participants demonstrating the target action (%)",
                ["Group", "Spontaneous", "With incentive"], [["Observed model", 20, 75], ["No model", 8, 12]])
    study_table("socialstudy_argument", "Endorsement after a message (%)",
                ["Argument", "Low prestige", "High prestige"], [["Weak", 25, 38], ["Strong", 55, 64]])
    study_table("socialstudy_public", "Switches to an incorrect answer (%)",
                ["Peer responses", "Private answer", "Public answer"],
                [["None shown", 5, 6], ["Unanimously wrong", 9, 30]])


def goals_of_care_records():
    """Simulated handoff and observation timelines."""
    study_table("caregoals_vent", "Time-limited treatment trial", ["Record", "Documented finding"],
                [["Patient's goal", "Recover from a reversible illness"],
                 ["Review milestone", "Improving with less support"],
                 ["At review", "Awake; passing breathing trials"]])
    study_table("caregoals_times", "Expected inpatient death", ["Event", "Clock time"],
                [["Last seen alive", "06:00"], ["Found unresponsive", "06:55"],
                 ["Death pronounced after examination", "07:10"]])


def quality_improvement_studies():
    """Simulated quality reports, care timelines and weekly run charts."""
    for suffix, returns in [("a", 9), ("b", 4)]:
        study_table("quality_bal_" + suffix, "Discharge pilot", ["Measure", "Before", "During pilot"],
                    [["Discharge time (hours)", 4, 3], ["Urgent returns", 4, returns],
                     ["Eligible discharges", 100, 100]])
    for suffix, steps in [("a", [("Yes", "Yes"), ("No", "No")]),
                          ("b", [("Yes", "No"), ("No", "Yes")])]:
        study_table("quality_bundle_" + suffix, "Two-step care bundle", ["Patient", "Step A", "Step B"],
                    [[1, "Yes", "Yes"], [2, "Yes", "Yes"], [3, *steps[0]], [4, *steps[1]]])
    baseline = [49, 51, 48, 52, 50, 50, 49, 51, 50, 50]
    for suffix, followup in [("a", [48, 46, 47, 45, 46, 44]), ("b", [40, 52, 48, 51, 47, 53])]:
        fig, ax = axes("Week", "Median wait (minutes)")
        ax.plot(range(1, 17), baseline + followup, "o-", color=COLORS[0], markersize=4)
        ax.axhline(50, ls="--", color="#954a26", label="Baseline median")
        ax.axvline(10.5, ls=":", color="#444444", label="Pilot begins")
        ax.set(title="Weekly waiting times • simulated", ylim=(39, 58), xticks=[1, 4, 7, 10, 13, 16])
        ax.legend(loc="upper left", fontsize=8, ncols=2)
        save(fig, "quality_run_" + suffix)
    study_table("quality_core", "Process measure report", ["Clinician", "Met measure", "Eligible"],
                [["A", 48, 60], ["B", 27, 30]])
    for suffix, assessment in [("a", "09:10"), ("b", "08:15")]:
        study_table("quality_wait_" + suffix, "Urgent clinic timeline", ["Event", "Clock time"],
                    [["Arrival", "08:00"], ["Assessment", assessment], ["Result", "09:30"]])


def coronary_ischemia_studies():
    """Coronary flow, clinical observations, and published trial comparisons."""
    fig, ax = axes("Exercise workload (relative units)", "Coronary flow (relative units)")
    for label, values, color in [("Vessel A", [1, 1.5, 2.1, 2.7, 3.3], COLORS[0]),
                                 ("Vessel B", [1, 1.3, 1.5, 1.5, 1.5], COLORS[1])]:
        ax.plot(range(5), values, "o-", label=label, color=color)
    ax.set(title="Coronary response to exercise • simulated", xticks=range(5), ylim=(0, 3.6))
    ax.legend()
    save(fig, "coronary_reserve")
    for suffix, final in [("a", ["Two flights", "3 min with rest"]), ("b", ["At rest", "25 min, ongoing"])]:
        study_table("coronary_diary_" + suffix, "Chest pressure diary", ["When", "Onset", "Duration"],
                    [["4 weeks ago", "Two flights", "3 min with rest"],
                     ["2 weeks ago", "Two flights", "3 min with rest"], ["Today", *final]])
    for suffix, narrowing in [("a", "95%"), ("b", "20%")]:
        study_table("coronary_prov_" + suffix, "Coronary provocation study", ["Finding", "During acetylcholine"],
                    [["Symptoms", "Usual chest pain"], ["ECG", "Transient ST depression"],
                     ["Epicardial narrowing", narrowing]])
    for suffix, values in [("v", [61, 61, 83, 82]), ("a", [60, 80, 81, 80])]:
        fig, ax = axes("Sampling location", "Oxygen saturation (%)")
        ax.plot(["SVC", "RA", "RV", "PA"], values, "o-", color=COLORS[0], lw=2)
        for i, value in enumerate(values):
            ax.annotate(f"{value}%", (i, value), xytext=(0, 7), textcoords="offset points", ha="center")
        ax.set(ylim=(50, 95), title="Catheter oximetry • simulated")
        save(fig, "coronary_sat_" + suffix)
    for suffix, late in [("a", ["78/50", "Larger collection", "Present"]),
                         ("b", ["120/76", "Small, unchanged", "Absent"])]:
        study_table("coronary_tam_" + suffix, "Postinfarction observations", ["Observation", "Earlier", "Now"],
                    [["Blood pressure", "118/74", late[0]], ["Pericardial fluid", "Small", late[1]],
                     ["RV diastolic collapse", "Absent", late[2]]])
    study_table("coronary_oxygen", "Trial population", ["Study characteristic", "DETO2X-AMI"],
                [["Presentation", "Suspected MI"], ["Entry oxygen saturation", "At least 90%"],
                 ["Comparison", "Routine oxygen vs ambient air"]], source="Hofmann et al.")
    fig, ax = axes("Initial PCI strategy", "Patients with an event (%)")
    bars = ax.bar(["Culprit only", "Immediate multivessel"], [45.9, 55.4], width=.56, color=COLORS[:2])
    ax.bar_label(bars, fmt="%.1f%%", padding=3)
    ax.set(ylim=(0, 70), title="Death or renal-replacement therapy at 30 days\nCULPRIT-SHOCK")
    save(fig, "coronary_culprit")
    fig, ax = axes("Relative risk of renal-replacement therapy", "")
    ax.axvline(1, color="#555555", linestyle="--", label="Equal risks")
    ax.errorbar(.71, 0, xerr=[[.22], [.32]], fmt="o", capsize=5, color=COLORS[0])
    ax.text(.71, .25, "0.71 (95% CI 0.49–1.03)", ha="center")
    ax.set(xlim=(.35, 1.2), ylim=(-.8, .8), yticks=[], title="Renal replacement at 30 days • CULPRIT-SHOCK")
    ax.legend(loc="lower right")
    save(fig, "coronary_renal")
    for suffix, rest in [("a", "Normal"), ("b", "Reduced")]:
        study_table("coronary_perfusion_" + suffix, "Relative tracer uptake", ["Region", "Stress", "Rest"],
                    [["Anterior", "Reduced", rest], ["Inferior", "Normal", "Normal"],
                     ["Lateral", "Normal", "Normal"]])


def electric_membrane_studies():
    """Original physical models and simulated observations for MCAT science."""
    fig, ax = axes("Position (cm)", "")
    for x, voltage in [(0, 8), (1, 6), (2, 4), (5, 2), (8, 0)]:
        ax.axvline(x, color=COLORS[0], lw=2)
        ax.text(x, .94, f"{voltage} V", ha="center", va="top", backgroundcolor="white")
    for x, name in [(.5, "A"), (6.5, "B")]:
        ax.text(x, .48, name, ha="center", fontsize=14, weight="bold")
    ax.set(xlim=(-.6, 8.6), ylim=(0, 1), yticks=[], title="Equipotential map • simulated")
    save(fig, "electric_equip")
    t = np.linspace(0, 50, 301)
    fig, ax = axes("Time (ms)", "Capacitor voltage (V)")
    ax.plot(t, 8 * np.exp(-t/10), lw=2, color=COLORS[0])
    ax.set(xlim=(0, 35), ylim=(0, 8.4), xticks=range(0,36,5), title="Discharge through a resistor")
    save(fig, "electric_discharge")
    fig, ax = axes("Horizontal position", "Vertical position")
    angle = np.linspace(0, np.pi/2, 80)
    for sign, label, color in [(1, "A", COLORS[0]), (-1, "B", COLORS[1])]:
        ax.plot(np.sin(angle), sign * (1 - np.cos(angle)), lw=2, color=color)
        ax.text(1.04, sign * .96, label, color=color, weight="bold")
    ax.annotate("", xy=(0, 0), xytext=(-.62, 0), arrowprops=dict(arrowstyle="->", lw=2))
    ax.set(aspect="equal", xlim=(-.7, 1.28), ylim=(-1.15, 1.15), xticks=[], yticks=[],
           title="Particle tracks • magnetic field into page")
    save(fig, "electric_track")
    study_table("electric_mass", "Galvanic cell electrodes", ["Electrode", "Start mass", "End mass"],
                [["Zinc", "2.00 g", "1.87 g"], ["Copper", "2.00 g", "2.13 g"]])
    fig, ax = axes("Time after current step (ms)", "Voltage change from rest (mV)")
    for plateau, time_constant, label, color, style in [(10, 10, "A", COLORS[0], "-"), (5, 5, "B", COLORS[1], "--")]:
        ax.plot(t, plateau * (1 - np.exp(-t/time_constant)), style, label=label, color=color, lw=2.3)
    ax.set(xlim=(0, 50), ylim=(0, 10.5), xticks=range(0, 51, 5), title="Passive membrane response • simulated")
    ax.legend()
    save(fig, "electric_pulse")
    study_table("electric_flow", "Isolated organ perfusion", ["Run", "Inlet (mm Hg)", "Outlet (mm Hg)", "Flow (mL/min)"],
                [["A", 45, 25, 5], ["B", 65, 25, 5]])


def ventricular_failure_studies():
    """Simulated hemodynamic records and sectional mitral valve diagrams."""
    for suffix, wedge in [("pre", 8), ("post", 25)]:
        study_table("ventricle_ph_" + suffix, "Right-heart catheterization", ["Measurement", "Value"],
                    [["Mean PA pressure", "32 mm Hg"], ["Wedge pressure", f"{wedge} mm Hg"], ["Cardiac output", "4 L/min"]])
    for suffix, data in [("t", ["<0.01", "3.8", "14.0"]), ("a", ["1.7", "1.1", "5.4"])]:
        study_table("ventricle_high_" + suffix, "High-output heart failure", ["Measurement", "Patient", "Reference interval"],
                    [["TSH (mIU/L)", data[0], "0.4–4.0"], ["Free T4 (ng/dL)", data[1], "0.8–1.8"],
                     ["Hemoglobin (g/dL)", data[2], "12–16"]])
    for suffix, values in [("a", [28, 44, 54]), ("b", [28, 28, 28])]:
        study_table("ventricle_rate_" + suffix, "LV function after rhythm control",
                    ["Measurement", "Before", "8 weeks", "6 months"],
                    [["Mean HR (/min)", 136, 72, 73], ["LVEF (%)", *values]])
    for suffix, values in [("a", [150, 105]), ("b", [75, 30])]:
        study_table("ventricle_ef_" + suffix, "LV volume measurements", ["Timing", "Volume (mL)"],
                    [["End diastole", values[0]], ["End systole", values[1]]])
    for suffix in ("flail", "tether"):
        fig, ax = plt.subplots(figsize=(5.1, 3.6), layout="constrained")
        ax.axhline(0, color="#848484", ls="--", lw=1)
        ax.text(-1.28, 1.06, "Left atrium")
        ax.text(-1.28, -1.61, "Left ventricle")
        ax.text(1.20, .06, "Annulus", ha="right", color="#555555", fontsize=8)
        for x in [-1, 1]:
            ax.scatter(x, 0, s=38, color="#343b3d", zorder=3)
        if suffix == "flail":
            leaves = [([-1, -.72, -.44, -.16], [0, -.13, -.10, .37]),
                      ([1, .66, .30, .03], [0, -.10, -.18, -.23])]
            chords = [([-.16, -.33], [.37, .17]), ([-.57, -.73], [-.75, -1.0]),
                      ([.03, .72], [-.23, -1.0])]
            muscle_y = -1.0
        else:
            leaves = [([-1, -.73, -.43, -.12], [0, -.23, -.48, -.61]),
                      ([1, .73, .43, .12], [0, -.23, -.48, -.61])]
            chords = [([-.12, -.73], [-.61, -1.30]), ([.12, .72], [-.61, -1.30])]
            muscle_y = -1.30
        for x, y in leaves:
            ax.plot(x, y, color=COLORS[0], lw=5, solid_capstyle="round")
        for x, y in chords:
            ax.plot(x, y, color=COLORS[1], lw=2)
        ax.scatter([-.73, .72], [muscle_y, muscle_y], marker="^", s=160, color=COLORS[1])
        ax.set(aspect="equal", xlim=(-1.45, 1.45), ylim=(-1.72, 1.37), title="Mitral apparatus in systole • schematic")
        ax.axis("off")
        save(fig, "ventricle_" + suffix)


def posterior_lead_study():
    """Simulated supplementary leads during ischemic symptoms."""
    study_table("coronary_ecg_post", "Posterior ECG during chest pain", ["Lead", "J-point level vs baseline"],
                [["V7", "+1.5 mm"], ["V8", "+2.0 mm"], ["V9", "+1.5 mm"]])


def atrial_and_ventricular_rhythm_studies():
    """Original timing diagrams and simulated rhythm assessments."""
    p_times = [.2, 1., 1.47, 2.27, 3.07]
    fig, ax = axes("Time (s)", "")
    for times, level, color in [(p_times, 1, COLORS[0]), (np.array(p_times) + .16, 0, COLORS[1])]:
        ax.vlines(times, level - .13, level + .13, color=color, lw=3)
    for number, x in enumerate(p_times, 1):
        ax.text(x, 1.2, str(number), ha="center")
    ax.set(xlim=(0, 3.5), ylim=(-.4, 1.55), yticks=[0, 1], yticklabels=["QRS onset", "P onset"],
           title="Atrial and ventricular events • simulated")
    save(fig, "rhythm_pac")
    for name, rate in [("fast", 126), ("slow", 78)]:
        study_table("rhythm_mat_" + name, "Single-lead atrial observations", ["Finding", "Observation"],
                    [["Atrial rate", f"{rate}/min"], ["P shapes", "Three distinct contours"],
                     ["P–P intervals", "Irregular"], ["Between P waves", "Isoelectric intervals"]])
    for name, pulse, bp, state in [("pulse", "Present", "68/40 mm Hg", "Confused"),
                                   ("arrest", "Absent", "No waveform", "Unresponsive")]:
        study_table("rhythm_vt_" + name, "Bedside assessment during tachycardia", ["Observation", "Finding"],
                    [["Central pulse", pulse], ["Arterial pressure", bp], ["Mental status", state]])
    study_table("rhythm_delta", "Sinus rhythm measurements", ["Finding", "Observation"],
                [["PR interval", "90 ms"], ["QRS onset", "Slurred upstroke"], ["QRS duration", "128 ms"]])


def conduction_and_device_studies():
    """Simulated PR sequences, P/QRS timing and paired right/lateral QRS views."""
    for name, durations in [("wenck", ["160", "200", "240", "No QRS", "160"]),
                            ("mobitz", ["170", "170", "170", "No QRS", "170"])]:
        study_table("conduct_" + name, "Consecutive sinus impulses", ["P wave", "PR interval (ms)"],
                    [[str(i), duration] for i, duration in enumerate(durations, 1)])
    for name, atrial in [("sinpause", [.25, 1.05, 3.45, 4.25]),
                         ("avpause", [.25, 1.05, 1.85, 2.65, 3.45, 4.25])]:
        ventricular = np.array([.25, 1.05, 3.45, 4.25]) + .17
        fig, ax = axes("Time (s)", "")
        for times, level, color in [(atrial, 1, COLORS[0]), (ventricular, 0, COLORS[1])]:
            ax.vlines(times, level - .15, level + .15, color=color, lw=3)
        ax.set(xlim=(0, 4.7), ylim=(-.45, 1.45), yticks=[0, 1], yticklabels=["QRS onset", "P onset"],
               title="Atrial and ventricular events • simulated")
        save(fig, "conduct_" + name)
    # The knots specify an idealized QRS only. Both leads use identical axes.
    for name, duration, leads in [
            ("left", 158, [[0, .13, -.40, -.96, -.88, -.77, -.47, 0],
                           [0, .31, .70, .91, .75, .91, .62, 0]]),
            ("right", 150, [[0, .33, -.47, -.30, .52, .91, .42, 0],
                            [0, .83, .97, .38, -.31, -.46, -.33, 0]])]:
        fig, panels = plt.subplots(2, 1, figsize=(5.3, 3.5), layout="constrained", sharex=True)
        t = np.array([0, .12, .25, .39, .53, .69, .85, 1]) * duration
        for ax, lead, values in zip(panels, ["V1", "V6"], leads):
            ax.plot([-40, *t, duration+45], [0, *values, 0], color=COLORS[0], lw=2.5)
            ax.axhline(0, color="#666666", alpha=.3, lw=.7)
            ax.set(ylim=(-1.2, 1.2), ylabel=lead + " (mV)", yticks=[-1, 0, 1])
            ax.grid(alpha=.18)
        panels[0].set_title("Ventricular depolarization • schematic")
        panels[-1].set_xlabel("Time from QRS onset (ms)")
        save(fig, "conduct_" + name)


def wave_and_signaling_studies():
    """Original simulated studies of sound, infrared absorption, lenses and cell signals."""
    distances = np.array([1, 2, 3])
    fig, ax = axes("One-way distance (cm)", "Echo round-trip time (μs)")
    for slope, name, color, marker in [(10, "Gel A", COLORS[0], "o"), (15, "Gel B", COLORS[1], "s")]:
        ax.plot(distances, slope*distances, marker=marker, color=color, lw=2, label=name)
    ax.set(title="Ultrasound in two gels • simulated", xticks=distances, yticks=range(0, 51, 5), ylim=(0, 50))
    ax.legend()
    save(fig, "wavesignal_echo")
    wavenumber = np.linspace(1500, 1850, 351)
    fig, ax = axes("Wavenumber (cm⁻¹)", "Absorbance (relative units)")
    for height, name, color, linestyle in [(.13, "A", COLORS[0], "--"), (.78, "B", COLORS[1], "-")]:
        y = .08 + height * np.exp(-.5*((wavenumber-1710)/10)**2)
        ax.plot(wavenumber, y, linestyle=linestyle, lw=2, color=color, label=name)
    ax.set(title="Infrared absorption window • simulated", xlim=(1850, 1500), ylim=(0, 1))
    ax.legend()
    save(fig, "wavesignal_ir")
    fig, ax = axes("1 / object distance (m⁻¹)", "1 / image distance (m⁻¹)")
    inverse_distance = np.array([1, 2, 3, 4])
    ax.plot([0, 4.5], [5, .5], color=COLORS[0], label="Fit")
    ax.scatter(inverse_distance, 5-inverse_distance, color=COLORS[1], label="Measurements", zorder=3)
    ax.set(xlim=(-.1, 4.7), ylim=(0, 5.5), title="Converging lens • simulated")
    ax.legend()
    save(fig, "wavesignal_lens")
    fig, ax = axes("Membrane potential (mV)", "Outward current (pA)")
    voltage = np.arange(-120, -39, 10)
    ax.plot(voltage, (voltage+80)*.5, "o-", color=COLORS[0])
    ax.axhline(0, linestyle=":", color="#555555")
    ax.set(title="Isolated channel current • simulated", xticks=voltage)
    save(fig, "wavesignal_ion")
    study_table("wavesignal_lipid", "Prostaglandin output • relative units", ["Preparation", "Vehicle", "Free arachidonic acid"],
                [["A (inhibited)", 1, 8], ["B (inhibited)", 1, 1]])
    study_table("wavesignal_axis", "Thyroid hormone secretion • relative units", ["Preparation", "Baseline", "After TSH"],
                [["A", 2, 8], ["B", 2, 2.1]])


def rhythm_trial_results():
    """Published endpoints from REVERT and RACE II."""
    study_table("rhevidence_revert", "Sinus rhythm one minute after intervention",
                ["Assigned maneuver", "Sinus rhythm", "Analyzed"], [["Standard", 37, 214], ["Modified", 93, 214]],
                source="REVERT")
    study_table("rhevidence_race_rates", "Composite outcome at three years",
                ["Rate-control strategy", "Estimated incidence"], [["Lenient", "12.9%"], ["Strict", "14.9%"]],
                source="RACE II")
    fig, ax = axes("Difference in risk (percentage points), lenient minus strict", "")
    ax.axvline(0, color="#555555", linestyle="--", label="Equal risks")
    ax.errorbar(-2, 0, xerr=[[5.6], [5.5]], fmt="o", capsize=5, color=COLORS[0])
    ax.text(-2, .26, "−2.0 (90% CI −7.6 to +3.5)", ha="center")
    ax.set(xlim=(-10, 8), ylim=(-.8, .8), yticks=[], title="Composite outcome at three years • RACE II")
    ax.legend(loc="lower right")
    save(fig, "rhevidence_race_ci")


def valve_lesion_studies():
    """Illustrative pressure and flow records. ICAP is observed trial data."""
    phase = np.linspace(0, 1, 121)
    fig, ax = axes("Fraction of diastole", "Pressure (mm Hg)")
    ax.plot(phase, 19 - 4 * phase + 1.5 * np.cos(2*np.pi*phase),
            label="Left atrium", color=COLORS[0])
    ax.plot(phase, 5 + 4 * phase + 2*np.exp(-10*phase),
            ls="--", label="Left ventricle", color=COLORS[1])
    ax.set(title="Simultaneous pressures after valve opening • simulated", ylim=(0, 24))
    ax.legend(loc="best")
    save(fig, "valves_inflow")
    study_table("valves_gradients", "Mean diastolic pressures at the same flow",
                ["Chamber", "Atrium (mm Hg)", "Ventricle (mm Hg)"],
                [["Right heart", "12", "4"], ["Left heart", "9", "8"]])
    study_table("valves_leftgradient", "Mean pressures during diastole",
                ["Right atrium", "Right ventricle", "Left atrium", "Left ventricle"],
                [["5 mm Hg", "4 mm Hg", "20 mm Hg", "8 mm Hg"]])
    for key, rows in [
        ("dobutamine", [["Rest", "44", "0.82", "26"], ["Dobutamine", "62", "0.85", "45"]]),
        ("dobutamine_b", [["Rest", "42", "0.85", "25"], ["Dobutamine", "63", "1.35", "29"]]),
    ]:
        study_table("valves_" + key, "Low-dose dobutamine echo • reduced LVEF",
                    ["Stage", "Stroke volume\n(mL)", "Valve area\n(cm²)", "Mean gradient\n(mm Hg)"], rows)
    fig, ax = axes("Fraction of cardiac cycle", "Pulmonary flow (mL/s)")
    forward = 250*np.sin(np.pi*np.minimum(phase/.4, 1))
    back = np.sin(np.pi*np.maximum((phase-.4)/.6, 0))
    for label, flow, style, color in [("A", forward-94*back, "-", COLORS[0]),
                                      ("B", forward-4*back, "--", COLORS[1])]:
        ax.plot(phase, flow, ls=style, lw=2, label=label, color=color)
    ax.axhline(0, color="#555555", lw=.8)
    ax.set(title="Main pulmonary artery • simulated flow")
    ax.legend(title="Profile")
    save(fig, "valves_pulmflow")
    fig, panels = plt.subplots(1, 2, figsize=(6.5, 3.1), layout="constrained", sharey=True)
    for ax, name, left in zip(panels, ["A", "B"], [[120, 100, 120], [120, 126, 120]]):
        ax.plot([0, 1, 2], left, "o-", color=COLORS[0], label="LV")
        ax.plot([0, 1, 2], [40, 53, 40], "s--", color=COLORS[1], label="RV")
        ax.set(xticks=[0, 1, 2], xticklabels=["Exp.", "Insp.", "Exp."], title="Record " + name,
               ylim=(25, 140))
        ax.legend(fontsize=8, loc="center left")
    panels[0].set_ylabel("Systolic pressure (mm Hg)")
    fig.suptitle("Simultaneous ventricular pressures • simulated")
    save(fig, "valves_resp")
    fig, ax = axes("Pericardial fluid volume (mL)", "Pericardial pressure (mm Hg)")
    vol = np.linspace(0, 210, 101)
    for name, scale, style, color in [("A", 62, "-", COLORS[0]), ("B", 124, "--", COLORS[1])]:
        ax.plot(vol, np.expm1(vol/scale), ls=style, color=color, label=name)
    ax.axvline(180, ls=":", color="#555555", lw=.8)
    ax.set(title="Two pericardial pressure responses • illustrative", ylim=(0, 30))
    ax.legend(title="Patient")
    save(fig, "valves_reserve")
    fig, ax = axes("Assigned add-on treatment", "Patients meeting endpoint (%)")
    bars = ax.bar(["Colchicine", "Placebo"], [16.7, 37.5], color=COLORS, width=.55)
    ax.bar_label(bars, labels=["16.7%", "37.5%"], padding=3)
    ax.set(title="ICAP • incessant or recurrent pericarditis", ylim=(0, 50))
    save(fig, "valves_icap")


def atomic_measurement_studies():
    """Original teaching figures for MCAT atomic structure and chemical measurements."""
    hours = np.arange(0, 13, 3)
    fig, ax = axes("Time (hours)", "Gross counts per minute")
    ax.plot(hours, 20 + 160 * .5**(hours/3), "o-", color=COLORS[0], label="Sample in holder")
    ax.axhline(20, ls="--", color=COLORS[1], label="Empty holder")
    ax.set(title="Tracer counting experiment • simulated", xticks=hours, ylim=(0, 202))
    ax.legend()
    save(fig, "atomic_decay")
    study_table("atomic_photo", "Photoelectrons at a fixed photon energy",
                ["Subshell", "Photon energy (eV)", "Kinetic energy (eV)"],
                [["X", "100", "25"], ["Y", "100", "80"]])
    fig, ax = axes("Electron removed (in order)", "Ionization energy (relative units)")
    ax.plot([1, 2, 3, 4], [1.0, 2.0, 10.5, 13.2], "o-", color=COLORS[0])
    ax.set(title="Successive ionizations • illustrative", xticks=[1, 2, 3, 4], ylim=(0, 15))
    save(fig, "atomic_jump")
    study_table("atomic_period", "First ionization energies • gas-phase atoms",
                ["Atom", "Na", "Mg", "Al", "Si"], [["kJ/mol", "496", "738", "578", "787"]],
                source="rounded")
    study_table("atomic_mass", "Gravimetric chloride assay",
                ["Weighing", "Filter + precipitate (mg)"],
                [["Dry filter alone", "101.0"], ["After first drying", "389.1"],
                 ["After second drying", "387.6"], ["After third drying", "387.6"]])


def rheumatic_af_outcomes():
    """Published restricted mean times to the INVICTUS primary composite outcome."""
    study_table("valvefollow_inv", "INVICTUS • time free of primary event",
                ["Assigned treatment", "Restricted mean time (days)"],
                [["Rivaroxaban", "1,599"], ["Vitamin K antagonist", "1,675"]],
                source="trial data")


def acute_airway_records():
    """Simulated outpatient cough and pediatric croup observations."""
    study_table("airwaycase_cough", "Acute cough • day 5",
                ["Observation", "Measurement"],
                [["Temperature / pulse", "37.2 °C / 82 per min"],
                 ["Respiratory rate / SpO₂", "16 per min / 98% on air"],
                 ["Chest exam", "No focal crackles, egophony or dullness"]])
    study_table("airwaycase_observe", "After dexamethasone and nebulized epinephrine",
                ["Time since epinephrine", "Stridor at rest", "Retractions"],
                [["Before treatment", "Present", "Moderate"],
                 ["30 minutes", "Absent", "Absent"], ["2 hours", "Absent", "Absent"],
                 ["4 hours", "Absent", "Absent"]])


def upper_respiratory_records():
    """Simulated longitudinal measurements for two independent clinical decisions."""
    fig, ax = axes("Day of illness", "Sinonasal symptom score (0–10)")
    for label, score, style, color in [
        ("A", [7, 8, 7, 5, 3, 2, 1, 0, 0], "o-", COLORS[0]),
        ("B", [7, 7, 5, 3, 2, 2, 5, 7, 8], "s--", COLORS[1]),
    ]:
        ax.plot(range(1, 10), score, style, color=color, label=label)
    ax.set(title="Adults with congestion and facial pressure • simulated", ylim=(-.3, 10),
           xticks=range(1, 10))
    ax.legend(title="Patient")
    save(fig, "upperair_sinus")
    study_table("upperair_peak", "Peak expiratory flow during a cold",
                ["Personal best", "Yesterday", "Today"], [["400 L/min", "330 L/min", "200 L/min"]])


def organic_reasoning_studies():
    """Original measurements, Fischer projections and heteroaromatic structures."""
    temp = np.linspace(25, 80, 160)
    fig, ax = axes("Temperature (°C)", "Fraction unfolded")
    for name, midpoint, color, style in [("Mutant", 50, COLORS[0], "-"),
                                         ("Wild type", 60, COLORS[1], "--")]:
        ax.plot(temp, 1/(1+np.exp(-(temp-midpoint)/3)), color=color, ls=style, label=name)
    ax.axhline(.5, color="#444444", ls=":", lw=1)
    ax.set(title="Thermal denaturation • simulated", xticks=range(30, 81, 5))
    ax.legend()
    save(fig, "orgstudy_fold", indexed=True)
    ligand = np.linspace(0, 20, 150)
    fig, ax = axes("Free ligand (μmol/L)", "Fraction of sites occupied")
    for name, kd, color, style in [("A", 2, COLORS[0], "-"), ("B", 8, COLORS[1], "--")]:
        ax.plot(ligand, ligand/(kd+ligand), color=color, ls=style, label=name)
    ax.axhline(.5, color="#444444", ls=":", lw=1)
    ax.set(title="Equilibrium binding • simulated", ylim=(0, 1), xticks=range(0, 21, 2))
    ax.legend(title="Carrier")
    save(fig, "orgstudy_binding", indexed=True)
    fig, panels = plt.subplots(2, 1, figsize=(5, 3.1), sharex=True, layout="constrained")
    for ax, name, peaks in zip(panels, ["A", "B"], [[(9.8, 1), (2.4, 2), (1.1, 3)], [(2.1, 3)]]):
        ax.axhline(0, lw=.7, color="#555555")
        for shift, height in peaks:
            ax.vlines(shift, 0, height, color=COLORS[0], lw=2)
        ax.set(yticks=[], ylim=(-.1, 3.5), ylabel="Unknown " + name)
    panels[-1].set(xlabel="Chemical shift (ppm)", xlim=(11, 0), xticks=range(0, 12))
    fig.suptitle("Proton NMR • illustrative peak positions only")
    save(fig, "orgstudy_nmr", indexed=True)
    fig, ax = axes("Time (min)", "Leaving group released (μmol/L)")
    time = np.arange(5)
    for label, rate, style, color in [("With amine", 6, "o-", COLORS[0]),
                                      ("Buffer only", 2, "s--", COLORS[1])]:
        ax.plot(time, rate*time, style, color=color, label=label)
    ax.set(title="Activated ester assay • simulated", xticks=time, yticks=range(0, 25, 4))
    ax.legend()
    save(fig, "orgstudy_acyl", indexed=True)
    fig, panels = plt.subplots(1, 2, figsize=(4.9, 2.9), layout="constrained")
    for ax, n, label in zip(panels, (5, 6), ("A", "B")):
        angles = np.pi/2 + np.arange(n)*2*np.pi/n
        vertices = np.array([np.cos(angles), np.sin(angles)]).T
        ax.plot(*np.vstack((vertices, vertices[0])).T, color="#25353d", lw=2)
        # The five-membered N–H and six-membered N have different ring pi bonds.
        for i in ([1, 3] if n==5 else [0, 2, 4]):
            a, b = vertices[i], vertices[(i+1)%n]
            inner = np.array([.85*a+.15*b, .15*a+.85*b])*.81
            ax.plot(*inner.T, color="#25353d", lw=1.4)
        ax.text(0, 1, "NH" if n==5 else "N", color=COLORS[0], fontsize=16, ha="center",
                va="center", bbox=dict(facecolor="white", edgecolor="none", pad=1))
        ax.set(aspect="equal", xlim=(-1.25, 1.25), ylim=(-1.2, 1.4), title="Nitrogen " + label)
        ax.axis("off")
    fig.suptitle("Neutral heteroaromatic rings")
    save(fig, "orgstudy_rings", indexed=True)
    fig, panels = plt.subplots(1, 2, figsize=(4.5, 3.25), layout="constrained")
    for ax, pattern, label in zip(panels, ["RLRR", "LLRR"], ["A", "B"]):
        ax.plot([0, 0], [.2, 4.7], color="#25353d")
        for y, side in zip([4, 3, 2, 1], pattern):
            ax.plot([-.43, .43], [y, y], color="#25353d")
            ax.text(-.48, y, "HO" if side=="L" else "H", ha="right", va="center")
            ax.text(.48, y, "OH" if side=="R" else "H", ha="left", va="center")
        ax.text(0, 4.8, "CHO", ha="center", va="bottom")
        ax.text(0, .15, "CH₂OH", ha="center", va="top")
        ax.set(xlim=(-1.1, 1.1), ylim=(-.5, 5.45), title="Sugar " + label)
        ax.axis("off")
    fig.suptitle("Fischer projections • aldehyde at C1")
    save(fig, "orgstudy_fischer", indexed=True)


def severe_cap_trial():
    """Observed primary mortality outcome of the CAPE COD randomized trial."""
    study_table("lungfocus_captrial", "CAPE COD • ICU patients with severe CAP",
                ["Group", "Deaths by day 28", "Participants", "Mortality"],
                [["Hydrocortisone", 25, 400, "6.2%"], ["Placebo", 47, 395, "11.9%"]],
                source="trial data")


def pneumonia_distributions():
    """Illustrative regional distributions of consolidation; not a radiograph."""
    from matplotlib.patches import Ellipse, Polygon

    fig, panels = plt.subplots(1, 2, figsize=(5.6, 3.15), layout="constrained")
    outline = np.array([[.14, 1.69], [.41, 1.95], [.63, 1.76], [.90, 1.06],
                        [1.03, .30], [.81, .17], [.31, .23], [.12, .45]])
    for ax, name in zip(panels, ("A", "B")):
        for side in (-1, 1):
            ax.add_patch(Polygon(outline*[side, 1], closed=True,
                                 facecolor="#f2f5f6", edgecolor="#354d58", lw=1.25))
            ax.plot([0, 0, .36*side], [2.05, 1.57, 1.29], color="#607783")
            for x, y in [(0.53, 1.59), (.72, .94), (.47, .60)]:
                ax.plot([side*.36, side*x], [1.29, y], color="#607783", lw=1.35)
        if name == "A":
            ax.add_patch(Polygon([(.24, .71), (.92, .88), (1.01, .31),
                                  (.80, .19), (.32, .25), (.15, .46)],
                                 closed=True, facecolor=COLORS[1], alpha=.75))
        else:
            for x, y, width in [(-.52, 1.60, .30), (-.48, .62, .24), (.70, .96, .35),
                                (.48, .58, .32), (-.70, .99, .26)]:
                ax.add_patch(Ellipse((x,y), width, .18, angle=20, facecolor=COLORS[1], alpha=.8))
        ax.set(aspect="equal", xlim=(-1.12, 1.12), ylim=(.06, 2.13), title="Pattern " + name)
        ax.axis("off")
    fig.suptitle("Shaded areas indicate consolidation • schematic")
    save(fig, "lungbreadth_patches", indexed=True)


def diarrhea_timelines():
    study_table("enteric_meal", "After a shared meal", ["Group", "Onset", "Main symptom", "Course"],
                [["A", "2 hours", "Vomiting", "Well next day"], ["B", "3 days", "Bloody stool", "Fever on day 4"]])


def gene_expression_records():
    """Original teaching records for melting, pulse–chase and gel interpretation."""
    temp = np.linspace(50, 92, 180)
    fig, ax = axes("Temperature (°C)", "Fraction separated")
    for name, mid, color, style in [("A", 64, COLORS[0], "-"), ("B", 76, COLORS[1], "--")]:
        ax.plot(temp, 1/(1+np.exp(-(temp-mid)/2)), color=color, ls=style, label=name)
    ax.set(xticks=range(52, 93, 4), title="Duplex melting • simulated")
    ax.axhline(.5, ls=":", lw=1, color="#555555")
    ax.legend(title="Duplex")
    save(fig, "genread_melt", indexed=True)
    study_table("genread_chase", "Label recovered in short DNA fragments",
                ["Sample", "End of pulse", "After chase"], [["A", "75%", "8%"], ["B", "74%", "70%"]])
    fig, ax = axes("Hours after chase begins", "Labeled protein remaining (%)")
    times = np.arange(0, 9)
    for name, half, st, color in [("A", 2, "o-", COLORS[0]), ("B", 4, "s--", COLORS[1])]:
        ax.plot(times, 100*.5**(times/half), st, label=name, color=color)
    ax.set(title="Protein pulse–chase • simulated", xticks=range(0, 9, 2), yticks=range(0, 101, 25))
    ax.legend(title="Cell type")
    save(fig, "genread_protein", indexed=True)
    fig, ax = plt.subplots(figsize=(4.0, 2.9), layout="constrained")
    ax.set(xlim=(-.6, 2.05), ylim=(0, 5.1))
    ax.axis("off")
    for i, bp in enumerate([200, 400, 600, 1000]):
        y=.65+i
        ax.plot([.1, .65], [y, y], lw=4, color=COLORS[0])
        ax.text(.03, y, str(bp), va="center", ha="right")
    ax.plot([1.1, 1.65], [2.65, 2.65], lw=4, color=COLORS[1])
    ax.text(.37, 4.35, "Reference (bp)", ha="center")
    ax.text(1.38, 4.35, "Sample X", ha="center")
    ax.set_title("Linear DNA fragments • schematic gel")
    save(fig, "genread_gel", indexed=True)


def gi_liver_studies():
    study_table("gutinfect_hbv", "HBV screening results", ["Patient", "HBsAg", "Anti-HBs", "Total anti-HBc"],
                [["A", "Negative", "Positive", "Negative"], ["B", "Negative", "Positive", "Positive"]])
    study_table("gutinfect_hcv", "HCV testing record", ["Patient", "Anti-HCV", "HCV RNA"],
                [["A", "Reactive", "Undetected"], ["B", "Reactive", "Detected"]])


def gi_localization_and_trial():
    """Original anatomical schematic and published randomized trial medians."""
    from matplotlib.patches import Ellipse, Polygon

    fig, ax = plt.subplots(figsize=(5.2, 3), layout="constrained")
    ax.set(xlim=(0, 10), ylim=(0, 6), aspect="equal")
    ax.axis("off")
    ax.add_patch(Polygon([(1, 2.4), (1.5, 3.65), (3, 4.2), (4.5, 4.35),
                          (6, 4.05), (7.4, 3.45), (6, 2.6), (3.2, 1.4), (1.4, 1.3)],
                         closed=True, facecolor="#e6bc9d", edgecolor="#624637"))
    ax.plot([.7, 1.5, 3, 4.5, 6, 7.7], [3.8, 4.6, 5.15, 5.25, 4.9, 3.85],
            color=COLORS[0], lw=3)
    ax.text(7.15, 4.65, "Diaphragm", color=COLORS[0])
    ax.text(5.1, 3.15, "Liver", ha="center")
    for x, y, label in [(2.6, 2.85, "A"), (4.3, 4.79, "B")]:
        ax.add_patch(Ellipse((x, y), 1.05, .53, facecolor="#fff3bb", edgecolor="#684c0e"))
        ax.text(x, y, label, ha="center", va="center", weight="bold")
    ax.set_title("Right upper quadrant • schematic")
    save(fig, "gilocal_anatomy", indexed=True)
    study_table("gilocal_trial", "Early treatment of oral HSV", ["Median duration", "Acyclovir", "Placebo"],
                [["Oral lesions", "4 days", "10 days"], ["Difficulty drinking", "3 days", "6 days"]],
                source="Amir et al., 1997")


def gi_monitoring_records():
    study_table("gimon_hus", "After bloody diarrhea", ["Time", "Hgb (g/dL)", "Plt (×10³/µL)", "Cr (mg/dL)"],
                [["Day 2", "12.6", "260", "0.5"], ["Day 6", "9.0", "68", "1.9"]])
    study_table("gimon_balance", "Two-hour fluid measurements", ["Interval", "Intake", "Stool", "Urine"],
                [["A", "1500 mL", "2300 mL", "100 mL"], ["B", "1500 mL", "1150 mL", "150 mL"]],
                source="no emesis")


def liver_contrast_record():
    phases = ["Precontrast", "Arterial", "Portal venous", "Delayed"]
    fig, ax = axes("Contrast phase", "Attenuation (HU)")
    for values, name, style, color in [([49, 131, 85, 67], "Nodule", "o-", COLORS[0]),
                                       ([55, 75, 110, 94], "Liver", "s--", COLORS[1])]:
        ax.plot(phases, values, style, color=color, lw=2, label=name)
    ax.set(ylim=(35, 150), title="Multiphasic CT • simulated")
    ax.legend()
    save(fig, "gionc_contrast", indexed=True)


def ovarian_cycle_record():
    days = [8, 11, 14, 17, 20, 23, 26]
    fig, ax = axes("Cycle day sampled", "Relative concentration")
    for series, name, style, color in [([1, 2, 9, 2, 1, 1, 1], "LH", "o-", COLORS[0]),
                                       ([1, 1, 1.5, 4, 8, 6, 2], "Progesterone", "s--", COLORS[1])]:
        ax.plot(days, series, style, lw=2, color=color, label=name)
    ax.set(xticks=days, ylim=(0, 11), title="Ovarian cycle • simulated samples")
    ax.legend()
    save(fig, "organread_cycle", indexed=True)


def gastrointestinal_trial_outcomes():
    for name, title, group_names, values, label, upper in [
        ("flot", "FLOT4 • resectable gastric or junctional cancer",
         ["Perioperative FLOT", "Perioperative ECF/ECX"], [50, 35], "Median overall survival (months)", 62),
        ("cross", "CROSS • resectable esophageal or junctional cancer",
         ["Chemoradiation + surgery", "Surgery alone"], [92, 69], "Margin-negative resections (%)", 107),
    ]:
        fig, ax = axes("", label)
        bars = ax.bar(group_names, values, color=COLORS, width=.55)
        ax.bar_label(bars, padding=3)
        ax.set(ylim=(0, upper), title=title)
        save(fig, "gitrial_" + name, indexed=True)


def skin_patch_record():
    study_table("skinflare_patch", "Patch site readings", ["Site", "Day 2", "Day 4"],
                [["Nickel", "Red, infiltrated papules", "Infiltrated papules"],
                 ["Fragrance mix", "Clear", "Clear"], ["Vehicle", "Clear", "Clear"]])


def skin_treatment_evidence():
    study_table("skinevidence_edema", "Recurrent leg cellulitis",
                ["Assigned care", "Participants with recurrence"],
                [["Compression + education", "6/41 (15%)"], ["Education alone", "17/43 (40%)"]],
                source="Webb et al.")
    study_table("skinevidence_blister", "Bullous pemphigoid strategies",
                ["Initial strategy", "≤3 blisters,\nweek 6", "Serious related harm,\nby week 52"],
                [["Doxycycline", "74%", "18%"], ["Prednisolone", "91%", "36%"]],
                source="BLISTER")


def cognition_records():
    """Original hypothetical records for reasoning about cognition experiments."""
    study_table("cogread_strategy", "Novel problem • shortcut use",
                ["Practice", "Used shortcut", "Tested"],
                [["Long strategy", "9", "30"], ["Comparison", "18", "24"]])
    study_table("cogread_sleep", "One scored sleep record",
                ["State", "Minutes"],
                [["Awake", "40"], ["N1", "20"], ["N2", "175"], ["N3", "75"], ["REM", "90"]])
    study_table("cogread_intrusion", "Recall test • list-A intrusions",
                ["List similarity", "Intrusions", "Participants"],
                [["High", "16", "4"], ["Low", "9", "6"]])
    fig, ax = axes("Test token", "Mean increase (sucks/min)")
    ax.bar(["Repeat", "Within", "Across"], [1, 2, 8], color=COLORS[:3])
    ax.set(title="Infant sucking recovery • simulated", ylim=(0, 10), yticks=range(0, 11, 2))
    save(fig, "cogread_infant", indexed=True)


def trial_interpretation_records():
    """Teaching models of statistical uncertainty, selection and causal structure."""
    from statistics import NormalDist

    normal = NormalDist()
    critical = normal.inv_cdf(.975)
    effects = np.linspace(0, .65, 150)
    fig, ax = axes("True difference (population SDs)", "Rejection probability")
    for n, color, style in [(30, COLORS[0], "--"), (120, COLORS[1], "-")]:
        shifts = effects * np.sqrt(n / 2)
        power = [normal.cdf(-critical - mu) + normal.cdf(mu - critical) for mu in shifts]
        ax.plot(effects, power, ls=style, color=color, label=f"{n} per arm")
    ax.set(title="Two-sided z test • known common variance", ylim=(0, 1.04))
    ax.legend()
    save(fig, "trialread_power", indexed=True)

    fig, ax = axes("Standardized test statistic under the null", "Density")
    z = np.linspace(-4, 4, 600)
    density = np.exp(-z**2 / 2) / np.sqrt(2 * np.pi)
    ax.plot(z, density, color=COLORS[0], label="Both designs")
    for boundary in [-critical, critical]:
        ax.axvline(boundary, color=COLORS[1], ls="--", lw=1)
    ax.fill_between(z, 0, density, where=abs(z)>=critical, color=COLORS[1])
    ax.set(title="Two-sided 5% tests • null distributions", xticks=[-3, -1.96, 0, 1.96, 3])
    ax.legend()
    save(fig, "trialread_powernull", indexed=True)

    for key, low, mean, high in [("small", .6, 1.2, 1.8), ("large", 3.4, 4.3, 5.2)]:
        fig, ax = axes("Mean symptom benefit (points)", "")
        ax.errorbar(mean, 0, xerr=[[mean-low], [high-mean]], fmt="o", capsize=6,
                    color=COLORS[0], label="Mean and 95% CI")
        ax.axvline(3, color=COLORS[1], ls="--", label="Worthwhile benefit")
        ax.axvline(0, color="#444444", lw=1)
        ax.set(title="Between-group comparison • simulated", yticks=[], ylim=(-1, 1),
               xlim=(-1, 6), xticks=range(-1, 7))
        ax.legend(loc="upper left")
        save(fig, "trialread_" + key, indexed=True)

    for key, events, missing, controls in [("missA", 6, 8, 10), ("missB", 4, 4, 12)]:
        study_table("trialread_" + key, "Final binary outcome",
                    ["Arm", "Allocated", "Known events", "Unknown"],
                    [["Intervention", "100", str(events), str(missing)],
                     ["Control", "100", str(controls), "0"]])
    for key, rows in [
        ("strataA", [["Mild", "2 / 20", "8 / 80"], ["Severe", "32 / 80", "8 / 20"]]),
        ("strataB", [["Mild", "5 / 100", "10 / 100"], ["Severe", "25 / 100", "30 / 100"]]),
    ]:
        study_table("trialread_" + key, "Events / patients in each severity stratum",
                    ["Severity", "Treated", "Comparison"], rows)
    for key, top, edges in [
        ("backdoor", "Baseline severity", [(0, 1), (0, 2), (1, 2)]),
        ("mediator", "Intermediate response", [(1, 0), (0, 2), (1, 2)]),
    ]:
        fig, ax = plt.subplots(figsize=(4.5, 2.8), layout="constrained")
        xy = [(.5, .83), (.18, .2), (.82, .2)]
        nodes = [ax.text(x, y, label, ha="center", va="center",
                         bbox=dict(boxstyle="round,pad=.42", fc="#eef5f6", ec=COLORS[0]))
                 for (x, y), label in zip(xy, [top, "Treatment", "Outcome"])]
        for start, end in edges:
            ax.annotate("", xy=xy[end], xytext=xy[start],
                        arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLORS[1],
                                        patchA=nodes[start].get_bbox_patch(),
                                        patchB=nodes[end].get_bbox_patch(),
                                        shrinkA=4, shrinkB=4))
        ax.set(xlim=(0, 1), ylim=(0, 1), title="Assumed causal diagram")
        ax.axis("off")
        save(fig, "trialread_" + key, indexed=True)
    for key, values in [("doseA", [3, 5, 9, 15]), ("doseB", [4, 10, 16, 7])]:
        fig, ax = axes("Exposure category", "Observed event risk (%)")
        ax.plot(["None", "Low", "Moderate", "High"], values, "o-", color=COLORS[0])
        ax.set(title="Exposure and outcome • simulated cohort", ylim=(0, 20), yticks=range(0, 21, 5))
        save(fig, "trialread_" + key, indexed=True)
    study_table("trialread_cast", "Arrhythmic death or nonfatal cardiac arrest",
                ["Assignment", "Events", "Participants"],
                [["Encainide or flecainide", "33", "730"], ["Placebo", "9", "725"]],
                source="CAST, 1989")


def sensory_behavior_records():
    """Synthetic psychophysics and behavioral-study displays."""
    position = np.linspace(0, 100, 240)
    fig, ax = axes("Distance from base toward apex (%)", "Relative displacement")
    for center, label, color, style in [(24, "Tone A", COLORS[0], "-"), (75, "Tone B", COLORS[1], "--")]:
        ax.plot(position, np.exp(-.5 * ((position-center)/9)**2), ls=style, color=color, label=label)
    ax.set(title="Cochlear response profiles • schematic", xticks=range(0, 101, 25))
    ax.legend()
    save(fig, "percept_cochlea", indexed=True)

    fig, ax = plt.subplots(figsize=(3.8, 3.0), layout="constrained")
    for col in range(8):
        ax.scatter(np.full(4, col*.47), np.arange(4), marker="o" if col%2==0 else "s",
                   s=45, facecolors="none", edgecolors=COLORS[0], linewidths=1.6)
    ax.set(xlim=(-.35, 3.65), ylim=(-.35, 3.35), aspect="equal", title="Array • narrow horizontal gaps")
    ax.axis("off")
    save(fig, "percept_array", indexed=True)
    study_table("percept_rowvotes", "Perceived grouping", ["Horizontal gaps", "Reported rows"],
                [["Narrow", "68%"], ["Wide", "32%"]])
    study_table("percept_flavor", "Identification accuracy", ["Task", "Open nose", "Nose occluded"],
                [["Flavor identity", "85%", "45%"], ["Basic taste", "92%", "90%"]])
    study_table("percept_trait", "Six-month test–retest correlation", ["Measure", "Correlation"],
                [["Trait inventory", "0.76"], ["Momentary rating", "0.24"]])
    study_table("percept_ocd", "Symptom severity • lower is better", ["Participant", "Baseline", "Follow-up"],
                [["A", "25", "15"], ["B", "32", "24"]])
    study_table("percept_play", "Mean free-choice play (minutes)", ["Group", "Before", "After"],
                [["Promised reward", "8", "5"], ["Comparison", "8", "7"]])


def peripheral_nerve_records():
    """Paired bedside findings and electrodiagnostic records; all are simulated."""
    for key, bright, dark in [("dark", (2.5, 3), (3, 5.5)), ("light", (2, 5), (5.5, 6))]:
        fig, ax = plt.subplots(figsize=(4.5, 3.0), layout="constrained")
        for y, vals in [(1, bright), (0, dark)]:
            for x, diameter in enumerate(vals):
                ax.scatter(x, y, s=300, facecolor="#d9e7e9", edgecolor=COLORS[0])
                ax.scatter(x, y, s=6 * diameter**2, facecolor="#202733", edgecolor="none")
                ax.text(x, y-.26, f"{diameter:g} mm", ha="center", va="center", fontsize=9)
        ax.set(xticks=[0, 1], xticklabels=["Patient's right", "Patient's left"],
               yticks=[0, 1], yticklabels=["Dark", "Bright"], xlim=(-.5, 1.5), ylim=(-.45, 1.4),
               title="Pupil diameters • simulated")
        ax.tick_params(length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        save(fig, "nerveloc_" + key, indexed=True)
    for key, rows in [
        ("gazeR", [["Left", "Poor adduction", "Abducting nystagmus"], ["Right", "Full abduction", "Full adduction"]]),
        ("gazeL", [["Left", "Full adduction", "Full abduction"], ["Right", "Abducting nystagmus", "Poor adduction"]]),
    ]:
        study_table("nerveloc_" + key, "Horizontal gaze examination",
                    ["Target moves", "Patient's right eye", "Patient's left eye"], rows)
    fig, ax = axes("Time (hours)", "Vital capacity (mL/kg)")
    ax.plot([0, 2, 4, 6, 8], [38, 39, 37, 38, 39], "o-", color=COLORS[0])
    ax.set(title="Bedside spirometry • simulated", xticks=range(0, 9, 2),
           yticks=range(30, 45, 2), ylim=(29, 45))
    for x, y in zip([0, 2, 4, 6, 8], [38, 39, 37, 38, 39]):
        ax.annotate(str(y), (x, y), xytext=(0, 7), textcoords="offset points", ha="center")
    save(fig, "nerveloc_vc", indexed=True)
    for key, velocities in [("elbow", [58, 36]), ("diffuse", [35, 34])]:
        study_table("nerveloc_" + key, "Ulnar motor study",
                    ["Segment", "Velocity (m/s)"],
                    [["Forearm", str(velocities[0])], ["Across elbow", str(velocities[1])]])


def obstetric_pressure_record():
    """Serial blood pressure and time in a simulated postpartum assessment."""
    study_table("oborgan_severebp", "Postpartum blood pressure",
                ["Time", "Systolic (mm Hg)", "Diastolic (mm Hg)"],
                [["09:00", "165", "103"], ["09:08", "168", "104"], ["09:15", "166", "102"]])


def anorectal_fold_patterns():
    """Schematic end-on patterns of protruding rectal or hemorrhoidal tissue."""
    from matplotlib.patches import Ellipse

    for key in ("folds", "columns"):
        fig, ax = plt.subplots(figsize=(3.5, 2.7), layout="constrained")
        if key == "folds":
            for width in (2.7, 2.15, 1.58, 1.0, .42):
                ax.add_patch(Ellipse((0, 0), width, .68*width,
                                     facecolor="#f2c4b1", edgecolor="#843e38", lw=2))
        else:
            for angle in (90, 210, 330):
                rad = np.radians(angle)
                center = (.65*np.cos(rad), .65*np.sin(rad))
                ax.add_patch(Ellipse(center, 1.5, .95, angle=angle, facecolor="#f2c4b1",
                                     edgecolor="#843e38", lw=2))
        ax.set(xlim=(-1.6, 1.6), ylim=(-1.4, 1.4), aspect="equal",
               title="Protruding tissue • schematic")
        ax.axis("off")
        save(fig, "bowelcase_" + key, indexed=True)


def angiodysplasia_study():
    """Mean combined red-cell and parenteral iron support in the OCEAN trial."""
    study_table("bowelcase_ocean", "Mean support units over one year",
                ["Group", "Red-cell + parenteral iron units"],
                [["Octreotide", "11.0"], ["Standard care", "21.2"]],
                source="OCEAN")


def mcat_science_and_society_records():
    """Independent teaching records and a shared, fictitious population study."""
    fig, ax = axes("pH", "Fraction protonated")
    ph = np.linspace(3, 9, 140)
    ax.plot(ph, 1/(1+10**(ph-6)), color=COLORS[0], lw=2)
    ax.axhline(.5, ls=":", lw=1, color="#555555")
    ax.set(title="Histidine side chain • model", xticks=range(3, 10), yticks=[0,.25,.5,.75,1])
    save(fig, "mcatmix_his", indexed=True)
    records = [
        ("meiosis", "Scored meiotic products", ["Markers", "Count"],
         [["AB","88"], ["ab","82"], ["Ab","16"], ["aB","14"]]),
        ("fitness", "One generation of snails", ["Type", "Parents", "Surviving offspring"],
         [["A","20","40"], ["B","30","90"]]),
        ("matrix", "Microscopic point counts", ["Field", "Cell", "Matrix"],
         [["A","80","20"], ["B","35","65"]]),
        ("track", "Cell tracking • complete observation", ["Event", "Count"],
         [["One divides into two","3"], ["Cell enters field","5"], ["Cell exits or dies","0"]]),
        ("lineage", "Recorded marker states", ["Parent", "Daughter 1", "Daughter 2"],
         [["A","A","A"], ["B","B","A"]]),
        ("visits", "Marker record • detection ≥5 units", ["Visit", "Reported units"],
         [["1","9"], ["2","<5"], ["3","8"], ["4","12"]]),
        ("activity", "Same ion and standard state", ["Sample", "Concentration", "Activity coefficient"],
         [["A","0.020 mol/L","0.90"], ["B","0.020 mol/L","0.72"]]),
        ("emotion", "Labels at matched arousal", ["Context", "Excitement", "Responses"],
         [["Celebration","28","40"], ["Tense","12","40"]]),
        ("pulse", "Heart rate (beats/min)", ["Participant", "Baseline", "Task", "10 min later"],
         [["A","66","106","80"], ["B","78","118","80"]]),
        ("identity", "Independently coded statements", ["Primary reference", "Statements"],
         [["Personal attribute","42"], ["Group membership","18"]]),
        ("feedback", "Academic self-concept • mean score", ["Feedback", "Before", "After"],
         [["Frequent","4","6"], ["Comparison","5","6"]]),
        ("credential", "Interpreter credential records", ["Clinic", "Credentialed", "Eligible"],
         [["A","24","60"], ["B","18","30"]]),
        ("meals", "Two definitions of a shared meal", ["Classification", "Interviews"],
         [["Both definitions","22"], ["Broad definition only","12"], ["Neither","16"]]),
        ("district", "Year before transit change", ["District", "Age (years)", "Residents", "Admissions"],
         [["East","<65","500","20"], ["East","65+","500","100"],
          ["West","<65","800","32"], ["West","65+","200","40"]]),
        ("register", "Annual register • fixed boundary", ["Event", "Residents"],
         [["Births","55"], ["Deaths","70"], ["Arrivals","160"], ["Departures","90"]]),
        ("bus", "Median scheduled trip to clinic", ["District", "Before", "After"],
         [["East","46 min","28 min"], ["West","24 min","25 min"]]),
    ]
    for key, title, columns, rows in records:
        study_table("mcatmix_" + key, title, columns, rows)
    from matplotlib.patches import FancyBboxPatch
    fig, ax = plt.subplots(figsize=(3.9, 2.2), layout="constrained")
    ax.add_patch(FancyBboxPatch((0, .4), 3, .8, boxstyle="round,pad=0,rounding_size=.4",
                                facecolor="#ddeef1", edgecolor=COLORS[0], lw=2))
    ax.plot([0, 1], [0, 0], lw=3, color="#242a30")
    ax.text(.5, -.14, "1 µm", ha="center", va="top")
    ax.set(aspect="equal", xlim=(-.35, 3.35), ylim=(-.42, 1.52), title="Cell and scale • schematic")
    ax.axis("off")
    save(fig, "mcatmix_rod", indexed=True)
    fig, ax = axes("x component", "y component")
    for x, color in [(-1, COLORS[0]), (1, COLORS[1])]:
        ax.annotate("", (x, 1), (0, 0), arrowprops=dict(arrowstyle="-|>", color=color, lw=2))
    ax.set(aspect="equal", xlim=(-1.4, 1.4), ylim=(-.25, 1.4), xticks=[-1,0,1],
           yticks=[0,1], title="Bond-dipole vectors • arbitrary units")
    save(fig, "mcatmix_vectors", indexed=True)


def mcat_transfer_records():
    study_table("mcatagain_acid", "Carboxyl side chain • model titration",
                ["pH", "Fraction carrying charge −1"],
                [["4", "50%"], ["5", "91%"], ["6", "99%"]])


def study_design_cases():
    """Independent study displays for reading uncertainty, allocation and measurement."""
    for key, estimates in [
        ("forest1", [(0.74, 0.56, 0.98), (0.72, 0.59, 0.88), (0.91, 0.76, 1.09)]),
        ("forest2", [(0.82, 0.68, 0.99), (0.96, 0.70, 1.32), (1.08, 0.88, 1.33)]),
        ("concord", [(0.77, 0.66, 0.90), (0.79, 0.69, 0.90), (0.80, 0.68, 0.94)]),
    ]:
        fig, ax = axes("Risk ratio for complications (log scale)", "")
        for y, (mid, lo, hi) in enumerate(estimates):
            ax.hlines(y, lo, hi, color=COLORS[0], lw=2)
            ax.plot(mid, y, "s", color=COLORS[0])
        ax.axvline(1, color="#555", ls="--")
        ax.set_xscale("log")
        ax.set(xlim=(.49, 1.52), xticks=[.5, .65, .8, 1, 1.25, 1.5],
               xticklabels=["0.5", "0.65", "0.8", "1", "1.25", "1.5"],
               ylim=(2.5, -.5), yticks=[0, 1, 2], yticklabels=["Trial A", "Trial B", "Trial C"],
               title="Independent trials • simulated 95% intervals")
        ax.minorticks_off()
        save(fig, "design_" + key, indexed=True)

    fig, ax = axes("Symptomatic VTE risk difference (percentage points)", "")
    ax.hlines(0, .54, 3.41, lw=3, color=COLORS[0])
    ax.plot(1.97, 0, "s", color=COLORS[0])
    for x, label in [(.54, "0.54"), (1.97, "1.97"), (3.41, "3.41")]:
        ax.text(x, .12, label, ha="center")
    ax.axvline(0, ls=":", color="#555", label="Equal risks")
    ax.axvline(1, ls="--", color=COLORS[1], label="Noninferiority margin")
    ax.set(xlim=(-.6, 4.1), ylim=(-.7, .9), yticks=[], title="CRISTAL • aspirin minus enoxaparin • 95% CI")
    ax.legend(loc="lower right")
    save(fig, "design_cristal", indexed=True)

    study_table("design_registry", "Prespecified endpoint at 90 days",
                ["Registered trials", "Completed", "Public results"], [["12", "12", "8"]])
    study_table("design_credit", "Sessions with identical reminders",
                ["Invitation", "Assigned", "Attended"], [["Public credit", "80", "36"], ["Private", "80", "24"]])

    fig, ax = axes("Horizontal position (m)", "Height above finish (m)")
    for height, color, name in [(2, COLORS[0], "Track A"), (1, COLORS[1], "Track B")]:
        ax.plot([0, 4], [height, 0], lw=2.4, label=name, color=color)
        ax.plot(0, height, "o", color=color)
    ax.set(xlim=(-.4, 4.4), ylim=(-.2, 2.4), yticks=[0, 1, 2], title="Carts released from rest • schematic")
    ax.legend()
    save(fig, "design_tracks", indexed=True)

    fig, ax = axes("Time (s)", "Position (m)")
    t = np.linspace(0, 4, 150)
    ax.plot(t, 4 - (t - 2)**2, color=COLORS[0], lw=2.3)
    ax.plot([1.45, 2.55], [4, 4], ls="--", color=COLORS[1], label="Tangent at 2 s")
    ax.set(xlim=(0, 4), ylim=(-.2, 4.6), title="Cart motion • simulated")
    ax.legend()
    save(fig, "design_turn", indexed=True)


def airway_tumor_studies():
    """Clinical lung function models, the published NLST rates and exchange experiments."""
    for name, expiration_cap, inspiration_cap in [("fixed", 2, 1.8), ("variable", 7, 1.5)]:
        volume = np.linspace(0, 4.5, 240)
        fraction = volume / volume[-1]
        expiratory = np.minimum(8 * (1 - np.exp(-fraction * 30)) * (1 - fraction), expiration_cap)
        inspiratory = -np.minimum(5 * np.sin(np.pi * fraction)**.65, inspiration_cap)
        fig, ax = axes("Volume expired (L)", "Flow (L/s)")
        ax.plot(volume, expiratory, color=COLORS[0], lw=2.5, label="Expiration")
        ax.plot(volume, inspiratory, color=COLORS[1], lw=2.5, label="Inspiration")
        ax.axhline(0, color="#555", lw=.8)
        ax.set(ylim=(-4.5, 7.5), title="Maximal flow–volume loop • schematic")
        ax.legend()
        save(fig, "airmass_" + name, indexed=True)

    fig, ax = axes("Screening assignment", "Lung cancer deaths\nper 100,000 person-years")
    bars = ax.bar(["Low-dose CT", "Chest radiography"], [247, 309], color=COLORS)
    ax.bar_label(bars)
    ax.set(ylim=(0, 365), title="National Lung Screening Trial")
    save(fig, "airmass_nlst", indexed=True)
    study_table("airmass_adaura", "Five-year overall survival • stage IB–IIIA",
                ["Assignment", "Estimated survival"], [["Osimertinib", "88%"], ["Placebo", "78%"]],
                source="ADAURA")
    study_table("airmass_counter", "Cumulative oxygen entering the receiver",
                ["Time (min)", "Counter (µmol)"], [["2", "7"], ["5", "16"]])
    study_table("airmass_perfusion", "Two perfusion runs",
                ["Run", "Pressure drop (mm Hg)", "Flow (mL/min)"], [["A", "40", "8"], ["B", "60", "12"]])
    study_table("airmass_gases", "Dry gas mixtures at the same temperature",
                ["Sample", "Oxygen fraction", "Total pressure (mm Hg)"], [["A", "0.30", "400"], ["B", "0.20", "700"]])
    study_table("airmass_blank", "Receiver oxygen gain",
                ["Holder", "Gross rate (µmol/min)"], [["Impermeable sheet", "1"], ["Membrane A", "5"], ["Membrane B", "3"]])


def shift_safety_studies():
    study_table("safesys_hours", "Intern serious errors per 1,000 patient-days",
                ["Schedule", "Error rate"], [["Traditional", "136.0"], ["Intervention", "100.1"]],
                source="ICU trial, 2004")
    study_table("safesys_workload", "Pediatric ICU schedules",
                ["Schedule", "Patients per resident", "Errors per 1,000 pt-days"],
                [["Control", "6.7", "79.0"], ["No 24-hour shifts", "8.8", "97.1"]],
                source="ROSTERS, 2020")
    study_table("safesys_attention", "Visual search accuracy", ["Task", "Correct", "Trials"],
                [["Search only", "45", "50"], ["Search and tone monitoring", "72", "90"]])
    study_table("safesys_sleep", "Overnight sleep record", ["Interval", "Minutes"],
                [["Recording", "480"], ["Awake", "80"], ["REM sleep", "60"]])
    study_table("safesys_census", "Coverage at evening handoff", ["Unit census", "Assigned clinicians"],
                [["24 patients", "4 clinicians"]])
    study_table("safesys_relief", "Coverage after redeployment", ["Unit census", "Assigned clinicians"],
                [["21 patients", "3 clinicians"]])


def reproductive_infection_studies():
    """Render bedside records, published trial results and MCAT experiments."""
    labels = ["Discharge", "Vaginal pH", "Clue cells", "Whiff test"]
    for name, values in [("bv", ["Thin, uniform", "5.3", "Present", "Negative"]),
                         ("ph", ["No typical coating", "5.2", "Absent", "Negative"])]:
        study_table("gynex_" + name, "Bedside assessment", ["Finding", "Result"],
                    list(zip(labels, values)))

    study_table("gynex_stepup", "BV recurrence within 12 weeks",
                ["Partner group", "Recurrences", "Proportion"],
                [["Concurrent treatment", "24 / 69", "35%"], ["Standard care alone", "43 / 68", "63%"]],
                source="StepUp, 2025")
    study_table("gynex_word", "Analgesic use in the first 24 hours",
                ["Word catheter", "Marsupialization"], [["33%", "74%"]], source="WoMan trial")
    study_table("gynex_recur", "Recurrence within one year",
                ["Word catheter", "Marsupialization", "RR (95% CI)"],
                [["12%", "10%", "1.1 (0.64–1.91)"]], source="WoMan trial")

    study_table("gynex_rprfall", "Quantitative RPR • same laboratory", ["Visit", "Titer"],
                [["Start of treatment", "1:32"], ["Six-month follow-up", "1:8"]])
    study_table("gynex_rprrise", "Quantitative RPR • same laboratory", ["Visit", "Titer"],
                [["After prior treatment", "1:4"], ["Current visit", "1:16"], ["Three weeks later", "1:16"]])
    study_table("gynex_cycle", "Hormone sampling during one cycle",
                ["Cycle day", "LH (IU/L)", "Progesterone (ng/mL)"],
                [["10", "5", "0.5"], ["13", "38", "0.8"], ["16", "8", "4"], ["20", "5", "12"]])

    fig, ax = axes("Aqueous buffer pH", "Recovered compound in organic layer (%)")
    values = [78, 65, 27]
    bars = ax.bar(["3.8", "4.8", "5.8"], values, color=COLORS[0], width=.55)
    ax.bar_label(bars, labels=[f"{v}%" for v in values], padding=3)
    ax.set(ylim=(0, 100), title="Weak acid partitioning • simulated experiment")
    save(fig, "gynex_extract", indexed=True)


def cerebrovascular_studies():
    """Draw simulated flow records and the published ARUBA and CREST-2 outcomes."""
    fig, ax = plt.subplots(figsize=(5.7, 3), layout="constrained")
    ax.set(xlim=(-.4, 6.4), ylim=(-.5, 3.8))
    ax.axis("off")
    # The cervical branch connects to the arm side of the obstruction.
    ax.fill_between([0, .9, 1.2, 1.45, 1.7, 6],
                    [-.11, -.11, -.025, -.025, -.11, -.11],
                    [.11, .11, .025, .025, .11, .11], color=COLORS[0])
    ax.plot([3.5, 3.5], [0, 2.65], color=COLORS[0], lw=6)
    ax.text(0, .37, "Aorta", ha="center")
    ax.text(1.25, -.32, "Stenosis", ha="center")
    ax.text(5.45, .38, "Left arm\n55 mmHg", ha="center")
    ax.text(3.67, 1.53, "Left vertebral artery", va="center")
    ax.text(3.5, 2.85, "Vertebrobasilar circulation\n80 mmHg", ha="center")
    ax.set_title("Exercise pressure measurements • simplified anatomy")
    save(fig, "nvas_steal", indexed=True)

    t = np.linspace(0, 3, 301)
    wave = 15 + 23 * np.maximum(np.sin(2 * np.pi * t), 0) ** 3 + 3 * np.sin(2 * np.pi * t - .7)
    for name, velocity in [("reverse", -wave), ("forward", .85 * wave)]:
        fig, ax = axes("Time (s)", "Vertebral flow velocity (cm/s)")
        ax.axhline(0, color="#333333", lw=1)
        ax.plot(t, velocity, color=COLORS[0], lw=2.3)
        ax.set(xlim=(0, 3), ylim=(-50, 50), title="Simulated Doppler • positive = toward brain")
        save(fig, "nvas_" + name, indexed=True)

    study_table("nvas_aruba", "Death or symptomatic stroke", ["Strategy", "Per 100 patient-years"],
                [["Medical management", "3.39"], ["Medical + intervention", "12.32"]],
                source="ARUBA follow-up")
    study_table("nvas_stent", "Four-year primary endpoint", ["Medical therapy", "Stent + medical therapy"],
                [["6.0%", "2.8%"]], source="CREST-2 stenting trial")
    study_table("nvas_parallel", "Four-year primary endpoint",
                ["Randomized trial", "Medical arm", "Procedure + medical"],
                [["Stenting", "6.0%", "2.8%"], ["Endarterectomy", "5.3%", "3.7%"]], source="CREST-2")
    study_table("nvas_map", "Initial monitored treatment", ["Time", "Mean arterial pressure"],
                [["Baseline", "160 mmHg"], ["Reassessment", "128 mmHg"]])
    study_table("nvas_pretreat", "BP during acute stroke evaluation",
                ["Time", "Systolic", "Diastolic"],
                [["Before adjustment", "198 mmHg", "122 mmHg"], ["Reassessment", "179 mmHg", "114 mmHg"]])
    study_table("nvas_repair", "Skin-cell lesion counts", ["Sample", "Initial", "After six hours"],
                [["A", "100", "40"], ["B", "40", "20"]])

    temperature = np.linspace(50, 90, 241)
    fig, ax = axes("Temperature (°C)", "Fraction remaining duplex")
    ax.plot(temperature, 1 / (1 + np.exp((temperature - 70) / 3)), color=COLORS[0], lw=2.4)
    ax.axhline(.5, color="#666666", ls="--", lw=1)
    ax.set(xlim=(50, 90), ylim=(0, 1), yticks=[0, .25, .5, .75, 1],
           title="Equilibrium DNA melting • simulated")
    save(fig, "nvas_melt", indexed=True)

    study_table("nvas_core", "Acute perfusion imaging • volume estimates",
                ["Tissue measurement", "Volume"], [["Delayed perfusion", "80 mL"], ["Estimated core", "20 mL"]])

    fig, ax = plt.subplots(figsize=(5.6, 2.6), layout="constrained")
    x = np.linspace(0, 8, 321)
    diameter = 4 - 3 * np.exp(-((x - 2.5) / .65) ** 2)
    ax.fill_between(x, -diameter / 2, diameter / 2, color="#d1e6ed")
    ax.plot(x, diameter / 2, color=COLORS[0])
    ax.plot(x, -diameter / 2, color=COLORS[0])
    for position, width, label in [(2.5, 1, "Minimum: 1.0 mm"), (6.1, 4, "Distal reference: 4.0 mm")]:
        ax.annotate("", (position, width / 2), (position, -width / 2),
                    arrowprops=dict(arrowstyle="<->", color="#222222"))
        ax.text(position, 2.5, label, ha="center", va="center")
    ax.set(xlim=(0, 8), ylim=(-2.5, 3), title="Internal carotid lumen • schematic")
    ax.axis("off")
    save(fig, "nvas_nascet", indexed=True)


def obstetric_complication_studies():
    """Draw simulated prenatal reports, Doppler signals and an MCAT unfolding curve."""
    for name, length in (("crl9", 9), ("crl4", 4)):
        study_table("obloss_" + name, "First transvaginal study",
                    ["Observation", "Result"],
                    [["Location", "Intrauterine embryo"], ["Crown–rump length", f"{length} mm"],
                     ["Cardiac activity", "Absent on adequate observation"]])

    for name, final in (("iron", ["9.1", "70", "5"]), ("dilution", ["11.3", "88", "56"])):
        study_table("obloss_" + name, "Prenatal laboratory record",
                    ["Gestation", "Hb (g/dL)", "MCV (fL)", "Ferritin (ng/mL)"],
                    [["10 weeks", "12.4", "89", "62"], ["26 weeks", *final]])

    for name, nadir in (("forward", 12), ("reversed", -8)):
        fig, ax = axes("Time (cardiac cycles)", "Velocity (cm/s)")
        phase = np.array([0, .15, .28, .45, .72, 1])
        velocity = np.array([nadir, 52, 35, 24, 12, nadir])
        for cycle in range(3):
            ax.plot(phase + cycle, velocity, color=COLORS[0], lw=2.5)
        ax.axhline(0, color="#333333", lw=1)
        ax.set(xlim=(0, 3), ylim=(-15, 60), xticks=[0, 1, 2, 3],
               title="Umbilical artery • positive is toward placenta")
        save(fig, "obloss_" + name, indexed=True)

    study_table("obloss_county", "County surveillance • annual review",
                ["Measure", "Count"], [["Live births", "40,000"],
                ["Deaths within pregnancy or 1 year after", "13"],
                ["Deaths judged pregnancy-related", "8"]])

    study_table("obloss_trial", "Early pregnancy loss • treatment success",
                ["Regimen", "Success", "Percent"],
                [["Mifepristone + misoprostol", "124 / 148", "83.8%"],
                 ["Misoprostol alone", "100 / 149", "67.1%"]],
                source="Schreiber et al.")

    fig, ax = axes("Temperature (°C)", "Fraction unfolded")
    temperature = np.linspace(29, 59, 180)
    ax.plot(temperature, 1 / (1 + np.exp(-(temperature - 44) / 2.4)),
            color=COLORS[0], lw=2.5)
    ax.set(xticks=[32, 36, 40, 44, 48, 52, 56], yticks=[0, .25, .5, .75, 1],
           title="Thermal unfolding • simulated measurement")
    save(fig, "obloss_fold", indexed=True)


def vascular_flow_studies():
    """Draw venous physiology, junction measurements, trial results and metabolic data."""
    for name, plateau in (("pump", 27), ("reflux", 78)):
        fig, ax = axes("Time (s)", "Ankle venous pressure (mm Hg)")
        time = np.linspace(0, 40, 400)
        walking = time > 10
        pressure = np.full(time.shape, 92.0)
        elapsed = time[walking] - 10
        pressure[walking] = plateau + (92 - plateau) * np.exp(-elapsed / 4)
        pressure[walking] += 2 * np.sin(2 * np.pi * elapsed / 2)
        ax.plot(time, pressure, color=COLORS[0], lw=2)
        ax.axvline(10, color="#555555", ls=":")
        ax.set(xlim=(0, 40), ylim=(0, 110), title="Quiet standing, then walking at 10 s")
        save(fig, "vleg_" + name, indexed=True)

    for name, distance in (("junction6", 6), ("junction2", 2)):
        fig, ax = plt.subplots(figsize=(6.6, 3), layout="constrained")
        ax.set(xlim=(-.9, 12), ylim=(-1.7, 3.4), title="Great saphenous vein • duplex map")
        ax.axis("off")
        ax.plot([0, 0], [-1.2, 2.5], color=COLORS[0], lw=8)
        ax.plot([0, 11.6], [0, 0], color=COLORS[0], lw=6)
        ax.plot([distance, 11.6], [0, 0], color=COLORS[1], lw=5)
        ax.text(.35, 2.15, "Common femoral vein")
        ax.text(.38, -.92, "Junction", ha="left")
        ax.text(distance + .3, .48, "Proximal clot tip")
        ax.annotate("", xy=(0, 1.05), xytext=(distance, 1.05),
                    arrowprops=dict(arrowstyle="<->", color="#333333"))
        ax.text(distance/2, 1.24, f"{distance} cm", ha="center")
        ax.text(11.6, -.9, "To knee →", ha="right")
        save(fig, "vleg_" + name, indexed=True)

    study_table("vleg_evra", "Time to healing with compression",
                ["Timing of superficial ablation", "Median time to healing"],
                [["Early", "56 days"], ["Deferred", "82 days"]], source="EVRA")
    study_table("vleg_calisto", "Primary composite events by day 47",
                ["Randomized group", "With event", "Event rate"],
                [["Fondaparinux", "13 of 1,502", "0.9%"], ["Placebo", "88 of 1,500", "5.9%"]],
                source="CALISTO")
    study_table("vleg_sat", "Paired forearm blood samples",
                ["Site", "Arterial O₂ sat.", "Draining venous O₂ sat."],
                [["Left arm", "98%", "68%"], ["Right arm", "98%", "91%"]])
    study_table("vleg_fast", "Sources of hepatic glucose • relative rates",
                ["Hours fasted", "Glycogen breakdown", "New glucose synthesis"],
                [["8", "7", "3"], ["16", "5", "5"], ["24", "2", "6"]])
    study_table("vleg_trace", "Carbon-13 tracer balance",
                ["Substrate", "Input (μmol ¹³C)", "In CO₂ (μmol ¹³C)"],
                [["Palmitate", "20", "12"], ["Alanine", "50", "20"]])

    fig, ax = axes("Minutes after exercise", "Ankle–brachial index")
    ax.plot([0, 1, 3, 5, 10], [1.02, .61, .70, .85, 1.0], "o-", color=COLORS[0])
    ax.set(xticks=[0, 1, 3, 5, 10], xticklabels=["Rest", "1", "3", "5", "10"],
           xlabel="Resting measurement and time after exercise (min)",
           ylim=(.45, 1.15), title="Exercise arterial pressure study • simulated")
    save(fig, "vleg_exercise", indexed=True)

    fig, ax = plt.subplots(figsize=(3.8, 3.9), layout="constrained")
    ax.set(xlim=(-1.5, 1.5), ylim=(-.7, 5.65), aspect="equal",
           title="Fischer projection")
    ax.axis("off")
    ax.plot([0, 0], [.35, 4.65], color="#222222", lw=1.7)
    ax.text(0, 5, "CHO", ha="center", va="center")
    ax.text(0, 0, "CH₂OH", ha="center", va="center")
    for y, left, right in [(4, "HO", "H"), (3, "H", "OH"),
                           (2, "HO", "H"), (1, "HO", "H")]:
        ax.plot([-.52, .52], [y, y], color="#222222", lw=1.7)
        ax.text(-.65, y, left, ha="right", va="center")
        ax.text(.65, y, right, ha="left", va="center")
    save(fig, "vleg_fischer", indexed=True)

    for name, top, bottom in (("aldor", "CHO", "CH₂OH"), ("aldos", "CH₂OH", "CHO")):
        fig, ax = plt.subplots(figsize=(3.4, 3.1), layout="constrained")
        ax.set(xlim=(-1.7, 1.7), ylim=(-1.4, 1.4), aspect="equal", title="Fischer projection")
        ax.axis("off")
        ax.plot([0, 0], [-.66, .66], lw=2, color="#222222")
        ax.plot([-.6, .6], [0, 0], lw=2, color="#222222")
        for x, y, label in ((0, .91, top), (0, -.91, bottom), (-.86, 0, "H"), (.92, 0, "OH")):
            ax.text(x, y, label, ha="center", va="center", fontsize=14)
        save(fig, "vleg_" + name, indexed=True)


def prenatal_visit_studies():
    """Draw prenatal measurement records, trial results and developmental biology figures."""
    for name, value, median in (("afpa", 84, 30), ("afpb", 90, 60)):
        study_table("previsit_" + name, "Singleton AFP screen",
                    ["Quantity", "AFP (ng/mL)"],
                    [["Maternal sample", value], ["Gestational reference median", median]])
    for name, affected, unaffected in (("ppva", 80, 20), ("ppvb", 6, 18)):
        study_table("previsit_" + name, "Diagnostic follow-up of positive screens",
                    ["Diagnostic result", "Pregnancies"],
                    [["Condition present", affected], ["Condition absent", unaffected]])
    for name, igg in (("bimmune", "Detected"), ("bsus", "Not detected")):
        study_table("previsit_" + name, "Maternal parvovirus B19 serology",
                    ["Test", "Serum result"], [["IgG", igg], ["IgM", "Not detected"]])
    for name, baseline, rise in (("nst30", 135, 12), ("nst36", 145, 13)):
        fig, ax = axes("Time (seconds)", "Fetal heart rate (beats/min)")
        times = [0, 5, 8, 11, 14, 17, 20, 25, 28]
        rates = [baseline, baseline, baseline, baseline+rise*.65,
                 baseline+rise, baseline+rise*.65, baseline, baseline, baseline]
        ax.plot(times, rates, color=COLORS[0], lw=2.5)
        ax.set(xticks=[0, 4, 8, 12, 16, 20, 24, 28],
               yticks=[baseline, baseline+5, baseline+10, baseline+rise, baseline+20],
               ylim=(baseline-3, baseline+22), title="Acceleration • simplified measurement")
        ax.axhline(baseline, color="#555555", ls=":", lw=1)
        save(fig, "previsit_" + name, indexed=True)

    study_table("previsit_mrc", "Neural tube defect recurrence", ["Group", "Affected", "Known outcomes"],
                [["With folic acid", "6", "593"], ["Without folic acid", "21", "602"]],
                source="MRC Vitamin Study")
    study_table("previsit_gdyield", "Gestational diabetes diagnoses",
                ["Strategy assigned", "Diagnosed"], [["One step", "16.5%"], ["Two steps", "8.5%"]],
                source="Hillier et al.")
    study_table("previsit_gdbirth", "Large-for-gestational-age birth", ["Measure", "One step vs. two steps"],
                [["Risk ratio", "0.95"], ["97.5% confidence interval", "0.87 to 1.05"]],
                source="Hillier et al.")

    fig, ax = axes("DNA content per cell", "Number of cells")
    ax.bar(["2C", "Between 2C and 4C", "4C"], [100, 60, 40], color=COLORS[0])
    ax.set(ylim=(0, 120), title="DNA content in 200 single cells • simulated")
    save(fig, "previsit_hist", indexed=True)
    for name, late_poles, late_chromosomes in (
            ("spindleA", (-5, 5), (-4, 4)), ("spindleB", (-7, 7), (-4, 4))):
        fig, ax = axes("Position on spindle axis (µm)", "Observation")
        for y, poles, chromosomes in ((1, (-5, 5), (-2, 2)),
                                      (0, late_poles, late_chromosomes)):
            ax.plot(poles, [y, y], color="#aab8bd", lw=2)
            ax.scatter(poles, [y, y], marker="o", color=COLORS[0], s=70,
                       label="Pole" if y else None)
            ax.scatter(chromosomes, [y, y], marker="X", color=COLORS[1], s=90,
                       label="Daughter chromosome" if y else None)
        ax.set(ylim=(-.65, 1.7), xlim=(-8, 8), xticks=range(-8, 9),
               yticks=[0, 1], yticklabels=["Later", "Earlier"], title="Mitotic spindle • simplified")
        ax.legend(loc="upper center", ncol=2, fontsize=8)
        save(fig, "previsit_" + name, indexed=True)
    study_table("previsit_lineage", "Precursor differentiation assay",
                ["Readout", "Culture A", "Culture B"], [["Myosin (units)", "7", "10"],
                ["Muscle actin (units)", "8", "1"], ["Stimulated contraction", "Present", "Absent"]])
    fig, ax = axes("Position along tissue (arbitrary units)", "Local cell–landmark pair")
    for y, start, end, marker in [(3, 1, 4, "o"), (2.65, 2, 5, "D"),
                                  (1.65, 1, 7, "o"), (1.3, 2, 4, "D")]:
        ax.annotate("", xy=(end, y), xytext=(start, y),
                    arrowprops=dict(arrowstyle="->", color=COLORS[0], lw=1.8))
        ax.scatter(start, y, marker=marker, facecolors="white", edgecolors=COLORS[0], s=50)
        ax.scatter(end, y, marker=marker, color=COLORS[0], s=50)
    ax.set(xlim=(0, 8), ylim=(.8, 3.5), yticks=[3, 2.65, 1.65, 1.3],
           yticklabels=["Cell A", "Landmark A", "Cell B", "Landmark B"],
           title="Cell and landmark positions")
    save(fig, "previsit_migration", indexed=True)

    for name, closed in (("foldclosed", True), ("foldopen", False)):
        fig, ax = plt.subplots(figsize=(4.5, 2.5), layout="constrained")
        if closed:
            ax.plot([-3, 3], [0.75, 0.75], color=COLORS[0], lw=4)
            theta = np.linspace(0, 2*np.pi, 180)
            ax.plot(.57*np.cos(theta), .56*np.sin(theta), color=COLORS[1], lw=5)
        else:
            for sign in (-1, 1):
                ax.plot([3*sign, 1.5*sign, .72*sign, .47*sign],
                        [.55, .55, .68, .91], color=COLORS[0], lw=4)
                ax.plot([.47*sign, .49*sign, .48*sign, .34*sign, 0],
                        [.91, .45, -.1, -.4, -.51], color=COLORS[1], lw=5)
        ax.set(xlim=(-3.1, 3.1), ylim=(-1.2, 1.5), aspect="equal",
               title="Transverse section • dorsal side above")
        ax.axis("off")
        ax.plot([], [], color=COLORS[0], lw=4, label="Surface ectoderm")
        ax.plot([], [], color=COLORS[1], lw=4, label="Neuroectoderm")
        ax.legend(loc="lower center", bbox_to_anchor=(.5, -.18), ncol=2, fontsize=8)
        save(fig, "previsit_" + name, indexed=True)

    for name, centers in (("aligned", (0, 0, 0)), ("aligning", (-.8, .9, 0))):
        fig, ax = plt.subplots(figsize=(4.5, 2.5), layout="constrained")
        theta = np.linspace(0, 2*np.pi, 160)
        ax.plot(2.65*np.cos(theta), 1.3*np.sin(theta), color="#737373", lw=1)
        ax.plot([0, 0], [-1.23, 1.23], color="#737373", ls=":", lw=1.3)
        ax.scatter([-2.1, 2.1], [0, 0], s=80, color=COLORS[0], marker="*", label="Spindle pole")
        for x, y in zip(centers, [-.7, 0, .7]):
            for sign in (-1, 1):
                ax.plot([x-.16, x+.16], [y+sign*.23, y-sign*.23], color=COLORS[1], lw=3)
        ax.set(xlim=(-2.85, 2.85), ylim=(-1.55, 1.55), aspect="equal",
               title="Positions of replicated chromosomes")
        ax.axis("off")
        ax.plot([], [], color="#737373", ls=":", label="Equatorial plane")
        ax.legend(loc="lower center", bbox_to_anchor=(.5, -.23), ncol=2, fontsize=8)
        save(fig, "previsit_" + name, indexed=True)



def occupational_lung_studies():
    """Render occupational spirometry, published respiratory outcomes and model-circuit data."""
    for name, values in (("cotfall", (3.20, 2.80)), ("cotstable", (2.70, 2.70))):
        fig, ax = axes("First shift after days away", "FEV₁ (L)")
        ax.plot([0, 1], values, "o-", color=COLORS[0], lw=2.2)
        for x, y in enumerate(values):
            ax.annotate(f"{y:.2f}", (x, y), xytext=(0, 9),
                        textcoords="offset points", ha="center")
        ax.set(xticks=[0, 1], xticklabels=["Before shift", "After shift"], xlim=(-.3, 1.3),
               ylim=(2.25, 3.55), title="Worker spirometry • simulated")
        save(fig, "dustlung_" + name, indexed=True)
    fig, ax = axes("Flow (mL/s)", "Pressure drop (kPa)")
    for i, (label, resistance) in enumerate((("Circuit A", 4), ("Circuit B", 2))):
        flow = np.array([0, 1, 2])
        ax.plot(flow, resistance * flow, STYLES[i], marker=("o", "s")[i],
                color=COLORS[i], lw=2, label=label)
    ax.set(xticks=[0, 1, 2], yticks=range(0, 9, 2), title="Steady laminar flow • simulated")
    ax.legend()
    save(fig, "dustlung_resist", indexed=True)
    study_table("dustlung_ipftrial", "Annual FVC slope", ["Randomized arm", "Adjusted mL/year"],
                [["Nintedanib", "−114.7"], ["Placebo", "−239.9"]], source="INPULSIS-1")
    fig, ax = axes("Surveys with an across-shift FEV₁ drop >5%", "Mean five-year FEV₁ loss (mL)")
    bars = ax.bar(["Neither", "One", "Both"], [180, 224, 267], color=COLORS[0], width=.55)
    ax.bar_label(bars, padding=2)
    ax.set(ylim=(0, 305), title="Cotton worker cohort • Christiani et al.")
    ax.text(.02, .96, "Group comparison: nonsignificant", fontsize=8,
            va="top", transform=ax.transAxes)
    save(fig, "dustlung_cohort", indexed=True)

    fig, ax = plt.subplots(figsize=(5.4, 2.9), layout="constrained")
    for y, label in [(1.25, "A"), (-1.25, "B")]:
        ax.plot([1, 1, 5, 5], [0, y, y, 0], color=COLORS[0], lw=3)
        ax.annotate("", (3.5, y), (2.5, y), arrowprops=dict(arrowstyle="->", lw=2))
        ax.text(3, y+.13, label, ha="center")
    ax.plot([0, 1], [0, 0], color=COLORS[0], lw=3)
    ax.plot([5, 6], [0, 0], color=COLORS[0], lw=3)
    ax.text(0, -.25, "Inlet")
    ax.text(6, -.25, "Outlet", ha="right")
    ax.set(xlim=(-.2, 6.2), ylim=(-1.6, 1.75), title="Two model vessels share pressure nodes")
    ax.axis("off")
    save(fig, "dustlung_parallel", indexed=True)

    fig, ax = plt.subplots(figsize=(5, 2.5), layout="constrained")
    xs = [0, 1.4, 2.5, 3.5, 4.6, 6]
    wall = np.array([.7, .7, .31, .31, .7, .7])
    ax.fill_between(xs, -wall, wall, color="#e3eff4")
    ax.plot(xs, wall, color=COLORS[0], lw=2.5)
    ax.plot(xs, -wall, color=COLORS[0], lw=2.5)
    for x, y, label in [(1, .7, "A"), (3, .31, "B")]:
        ax.plot([x, x], [y, 1.02], color=COLORS[1], lw=2)
        ax.text(x, 1.08, label, ha="center", fontweight="bold")
    ax.annotate("Flow", (2.1, 0), (.6, 0), va="center",
                arrowprops=dict(arrowstyle="->", lw=2))
    ax.set(xlim=(-.2, 6.2), ylim=(-1, 1.42), title="Static pressure taps • horizontal tube")
    ax.axis("off")
    save(fig, "dustlung_venturi", indexed=True)
    fig, ax = axes("Static transpulmonary pressure (cm H₂O)", "Volume change (L)")
    for i, (slope, label) in enumerate(((.12, "A"), (.04, "B"))):
        pressure = np.array([0, 5, 10])
        ax.plot(pressure, slope * pressure, STYLES[i], marker=("o", "s")[i],
                color=COLORS[i], lw=2, label=label)
    ax.set(xticks=[0, 5, 10], yticks=[0, .4, .8, 1.2], title="Static inflation • model lungs")
    ax.legend()
    save(fig, "dustlung_elastic", indexed=True)
    fig, ax = plt.subplots(figsize=(4.6, 3), layout="constrained")
    ax.fill_between([.2, 2.7], [0, 0], [.5, .5], color="#899aa4")
    ax.plot([.2, .2, 2.7, 2.7], [1, 0, 0, 1], color=COLORS[0], lw=2)
    ax.fill_between([1.65, 1.95], [.4, .4], [2.25, 2.25], color="#899aa4")
    ax.plot([1.65, 1.65, 1.95, 1.95], [.27, 2.75, 2.75, .27], color=COLORS[0], lw=2)
    ax.annotate("", xy=(1.3, 2.25), xytext=(1.3, .5), arrowprops=dict(arrowstyle="<->"))
    ax.text(1.17, 1.35, "h", ha="right");ax.text(2.04, 2.53, "Vacuum", va="center")
    ax.text(.25, .58, "Open to air", fontsize=9)
    ax.set(aspect="equal", xlim=(0, 3.2), ylim=(-.15, 2.96), title="Liquid-column barometer")
    ax.axis("off")
    save(fig, "dustlung_barometer", indexed=True)

    for name, values in (("fvc6", (72, 66)), ("fvc3", (48, 45))):
        fig, ax = axes("Months since baseline", "FVC (% predicted)")
        ax.plot([0, 9], values, "o-", color=COLORS[0], lw=2.2)
        for x, y in zip((0, 9), values):
            ax.annotate(str(y), (x, y), xytext=(0, 8), textcoords="offset points", ha="center")
        ax.set(xticks=[0, 9], xlim=(-1, 10), ylim=(35, 85), title="Serial spirometry • fibrotic NSIP")
        save(fig, "dustlung_" + name, indexed=True)



def thermodynamics_outline_studies():
    """Illustrate work, phase transitions and activation barriers for named outline objectives."""
    for name, clockwise in [("engine", True), ("reversed", False)]:
        fig, ax = axes("Volume (L)", "Pressure (kPa)")
        corners = [(1, 100), (1, 300), (3, 300), (3, 100), (1, 100)]
        if not clockwise:
            corners.reverse()
        ax.plot(*zip(*corners), color=COLORS[0], lw=2)
        for a, b in zip(corners, corners[1:]):
            start = tuple(.6*x + .4*y for x, y in zip(a, b))
            end = tuple(.4*x + .6*y for x, y in zip(a, b))
            ax.annotate("", xy=end, xytext=start,
                        arrowprops={"arrowstyle": "->", "color": COLORS[0], "lw": 2})
        ax.set(xlim=(.5, 3.5), ylim=(40, 360), xticks=[1, 2, 3], yticks=[100, 200, 300],
               title="One cycle of an idealized gas")
        save(fig, "cvdrug_" + name, indexed=True)

    for name, energies in [("barrier", [10, 70, -10]), ("reversebar", [10, 55, 30])]:
        fig, ax = axes("Reaction coordinate", "Enthalpy (kJ/mol)")
        for i, (left, right) in enumerate(zip(energies, energies[1:])):
            u = np.linspace(0, 1, 101)
            ax.plot(i+u, left+(right-left)*(1-np.cos(np.pi*u))/2, lw=2.4, color=COLORS[0])
        for i, energy in enumerate(energies):
            ax.annotate(str(energy), (i, energy), xytext=(0, 8), textcoords="offset points", ha="center")
        ax.set(xticks=[0, 1, 2], xticklabels=["Reactants", "Peak", "Products"],
               ylim=(-22, 88), title="Single-step reaction • schematic")
        save(fig, "cvdrug_" + name, indexed=True)

    for name, pressure, begin, end in [("boil", 2, 1.65, 3.6), ("sublime", .4, .3, 2.0)]:
        fig, ax = axes("Temperature (arbitrary units)", "Pressure (arbitrary units)")
        ax.plot([.1, .6, 1.1, 1.4], [.08, .32, .7, 1], color=COLORS[0])
        ax.plot([1.4, 1.9, 2.5, 3.1, 3.65], [1, 1.2, 1.65, 2.35, 3.25], color=COLORS[0])
        ax.plot([1.4, 1.8], [1, 3.5], color=COLORS[0])
        ax.scatter([begin], [pressure], s=24, color=COLORS[1])
        ax.annotate("", xy=(end, pressure), xytext=(begin, pressure),
                    arrowprops={"arrowstyle": "->", "lw": 2.6, "color": COLORS[1]})
        for x, y, label in [(.65, 2.6, "Solid"), (2.2, 2.8, "Liquid"), (2.85, .6, "Gas")]:
            ax.text(x, y, label, ha="center")
        ax.set(xlim=(0, 4), ylim=(0, 3.5), title="Heating path • schematic phase diagram")
        save(fig, "cvdrug_" + name, indexed=True)


def kinetic_equilibrium_studies():
    """Draw simulated standard free energies and rates for independent MCAT cases."""
    fig, ax = axes("Temperature (K)", "Standard Gibbs energy (kJ/mol)")
    ax.axhline(0, color="#777", linewidth=1)
    ax.plot([280, 340, 400], [-3, 0, 3], "o-", color=COLORS[0])
    ax.set(xticks=[280, 340, 400], yticks=[-3, 0, 3], ylim=(-4.5, 4.5),
           title="Simulated free-energy measurements")
    save(fig, "cvdrug_thermo", indexed=True)

    fig, ax = axes("Time (s)", "Product concentration (mmol/L)")
    for label, slope, color in [("A", .2, COLORS[0]), ("B", .3, COLORS[1])]:
        ax.plot([0, 2, 4], [0, 2*slope, 4*slope], "o-", label=label, color=color)
    ax.set(xticks=[0, 2, 4], ylim=(0, 1.4), title="Initial product formation • simulated samples")
    ax.legend()
    save(fig, "cvdrug_rates", indexed=True)


def social_decision_tables():
    records = [
        ("patcha", "Simulated patch returns", ["Patch", "Net gain (kJ)", "Total time (min)"],
         [["A", "18", "3"], ["B", "30", "6"]]),
        ("patchb", "Simulated patch returns", ["Patch", "Net gain (kJ)", "Total time (min)"],
         [["A", "18", "6"], ["B", "24", "4"]]),
        ("gamea", "Payoff to focal bird (points)", ["Focal action", "Partner searches", "Partner waits"],
         [["Search", "2", "5"], ["Wait", "4", "1"]]),
        ("gameb", "Payoff to focal bird (points)", ["Focal action", "Partner searches", "Partner waits"],
         [["Search", "3", "4"], ["Wait", "6", "2"]]),
    ]
    for name, title, headers, rows in records:
        fig, ax = plt.subplots(figsize=(5.4, 2.2), layout="constrained")
        ax.axis("off")
        ax.set_title(title)
        grid = ax.table(cellText=rows, colLabels=headers, cellLoc="center",
                        bbox=[0.02, 0.06, 0.96, 0.86])
        grid.auto_set_font_size(False)
        grid.set_fontsize(10)
        for (r, _), cell in grid.get_celld().items():
            cell.set_edgecolor("#73828a")
            if r == 0:
                cell.set_facecolor(COLORS[0])
                cell.get_text().set_color("white")
        save(fig, "socialdecision_" + name, indexed=True)


def social_access_studies():
    fig, ax = plt.subplots(figsize=(5.2, 3.3), layout="constrained")
    positions = {"A": (1, 2), "B": (1, 0), "C": (0, 1),
                 "D": (3, 2), "E": (3, 0), "F": (4, 1)}
    for start, end in ["AB", "AC", "BC", "DE", "DF", "EF", "AD", "BE"]:
        ax.plot(*zip(positions[start], positions[end]), color="#666", lw=2, zorder=1)
    for label, (x, y) in positions.items():
        ax.scatter(x, y, s=650, color=COLORS[int(x > 2)], zorder=2)
        ax.text(x, y, label, color="white", weight="bold", va="center", ha="center")
    for x, label in [(0.6, "Team 1"), (3.4, "Team 2")]:
        ax.text(x, 2.6, label, ha="center", weight="bold")
    ax.set(xlim=(-0.6, 4.6), ylim=(-0.5, 3), title="Reported contacts between team members")
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "socialaccess_network", indexed=True)

    # Bisgaier and Rhodes, 2011. Each clinic received a call in each condition.
    fig, ax = axes("Insurance described by caller", "Appointments denied (%)")
    denied = [179, 29]
    bars = ax.bar(["Medicaid or CHIP", "Private"], [100 * n / 273 for n in denied],
                  color=COLORS, width=0.56)
    ax.bar_label(bars, labels=[f"{n}/273" for n in denied], padding=4)
    ax.set(ylim=(0, 100), title="Pediatric specialty clinic calls, Cook County, 2010")
    save(fig, "socialaccess_denials", indexed=True)


def reproductive_diagnosis_studies():
    for name, values in [("flat", [420, 422, 417, 421]), ("fall", [420, 290, 180, 110])]:
        fig, ax = axes("Weeks after first sample", "Serum hCG (IU/L)")
        ax.plot(range(4), values, marker="o", color=COLORS[0], lw=2.5)
        for week, value in enumerate(values):
            ax.annotate(str(value), (week, value), xytext=(0, 8),
                        textcoords="offset points", ha="center")
        ax.set(xticks=range(4), ylim=(0, 500), title="Simulated post-evacuation measurements")
        save(fig, "gynstudy_" + name, indexed=True)

    # Consensus classification of complete moles, Vang et al., Table 2.
    fig, ax = axes("Diagnostic reading round", "Sensitivity (%)")
    bars = ax.bar(["Morphology 1", "Morphology 2", "With p57"], [70, 81, 96], color=COLORS[0])
    ax.bar_label(bars, padding=3)
    ax.set(ylim=(0, 108), title="Detection of genotype-confirmed complete moles")
    save(fig, "gynstudy_readers", indexed=True)

    fig, ax = axes("Time (ms)", "Signal (% of own peak)")
    time = [0, 10, 25, 45, 75, 100, 130]
    for i, (label, values) in enumerate([("Cytosolic calcium", [0, 40, 100, 35, 0, 0, 0]),
                                        ("Force", [0, 0, 20, 100, 65, 25, 0])]):
        ax.plot(time, values, STYLES[i], marker="o", color=COLORS[i], label=label)
    ax.legend()
    ax.set(title="Simulated skeletal muscle twitch")
    save(fig, "gynstudy_twitch", indexed=True)


def membrane_recovery_records():
    for label, after, plateau in [("a", 20, 80), ("b", 40, 70)]:
        fig, ax = axes("Time relative to bleaching (s)", "Fluorescence (% of prebleach level)")
        t = np.linspace(0, 40, 101)
        signal = after + (plateau - after) * (1 - np.exp(-t / 4))
        ax.plot([-8, 0, 0], [100, 100, after], color=COLORS[0], lw=2.4)
        ax.plot(t, signal, color=COLORS[0], lw=2.4)
        ax.set(xticks=[-8, 0, 10, 20, 30, 40], yticks=range(0, 101, 10),
               ylim=(-3, 105), title="Simulated membrane photobleaching")
        save(fig, "cellcheck_recovery_" + label, indexed=True)


def consciousness_assessments():
    # Wannez et al., Table 1, six-assessment reference (123 participants).
    fig, ax = axes("Number of assessments included", "Patients below reference category")
    counts = [44, 30, 21, 11, 6]
    bars = ax.bar(range(1, 6), counts, color=COLORS[0], width=.62)
    ax.bar_label(bars, padding=3)
    ax.set(xticks=range(1, 6), ylim=(0, 52), title="Repeated behavioral assessments (n = 123)")
    save(fig, "neurocheck_study", indexed=True)

    for name, crossing in [("early", 6), ("late", 16)]:
        fig, ax = axes("Hours since monitoring began", "Core temperature (°C)")
        hours = [0, crossing, 24, 32]
        ax.plot(hours, [34, 36, 36.4, 36.4], color=COLORS[0], marker="o", lw=2.5)
        ax.axhline(36, ls="--", lw=1, color="#555555")
        ax.set(xticks=sorted(set([0, crossing, 8, 16, 24, 32])),
               yticks=[34, 35, 36, 37], ylim=(33.6, 37.1),
               title="Simulated continuous temperature record")
        save(fig, "neurocheck_" + name, indexed=True)


def tumor_and_gene_evidence():
    fig, ax = axes("", "Median survival (months)")
    values = [15.3, 21.7]
    bars = ax.bar([0, 1], values, color=COLORS)
    ax.set(xticks=[0, 1], xticklabels=["Radiotherapy", "Radiotherapy + TMZ"],
           ylim=(0, 26), title="MGMT-methylated subgroup · Hegi et al.")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    save(fig, "genestudy_survival", indexed=True)

    fig, ax = axes("", "Normalized accessibility")
    x = np.arange(4)
    ax.bar(x - .18, [3, 3, 8, 4], width=.36, color=COLORS[0], label="Before")
    ax.bar(x + .18, [4, 6, 2, 4], width=.36, color=COLORS[1], hatch="//", label="After")
    ax.set(xticks=x, xticklabels=["Promoter A", "Promoter B", "Promoter C", "Reference"],
           ylim=(0, 10), title="Simulated promoter accessibility")
    ax.legend(loc="upper right", ncol=2)
    save(fig, "genestudy_access", indexed=True)

    fig, ax = plt.subplots(figsize=(3.7, 3.2), layout="constrained")
    ax.set(xlim=(0, 3), ylim=(4.6, 0), title="Simulated DNA gel")
    ax.set_facecolor("#273641")
    ax.set_xticks([1, 2], ["Marker", "Sample Y"])
    ax.xaxis.tick_top()
    ax.set_yticks([1, 2, 3.1, 4.1], ["1,200", "900", "600", "400"])
    ax.set_ylabel("Marker length (bp)")
    for y in [1, 2, 3.1, 4.1]:
        ax.plot([.7, 1.3], [y, y], color="white", lw=4)
    ax.plot([1.7, 2.3], [2, 2], color="white", lw=4)
    save(fig, "genestudy_gel", indexed=True)

    for n, duplexes in enumerate([["HL", "HL"], ["HL", "LL", "HL", "LL"]]):
        fig, ax = plt.subplots(figsize=(4.2, 2.4), layout="constrained")
        for i, pair in enumerate(duplexes):
            x = i * 1.25
            for j, strand in enumerate(pair):
                heavy = strand == "H"
                ax.plot([x, x + .85], [1.05 - .15*j] * 2,
                        color=COLORS[int(heavy)], ls="-" if heavy else "--", lw=3)
            ax.text(x + .42, .66, str(i + 1), ha="center")
        ax.plot([], [], "-", color=COLORS[1], lw=3, label="Heavy strand")
        ax.plot([], [], "--", color=COLORS[0], lw=3, label="Light strand")
        ax.legend(loc="lower center", ncol=2, frameon=False, fontsize=9)
        ax.set(xlim=(-.25, (len(duplexes)-1)*1.25 + 1.1), ylim=(0, 1.5),
               title="Strand labels in daughter duplexes")
        ax.axis("off")
        save(fig, "genestudy_density" + str(n), indexed=True)


def pain_and_sensation():
    fig, ax = axes("Vibration amplitude (µm)", "Trials detected (%)")
    ax.plot([0, 2, 4, 6, 8, 10, 12], [0, 5, 20, 50, 80, 95, 100], "o-", color=COLORS[0])
    ax.set(xticks=range(0, 13, 2), yticks=[0, 25, 50, 75, 100], title="Simulated vibration detection")
    save(fig, "sensory_vibration", indexed=True)

    for i, rates in enumerate(([48, 26, 8, 25], [23, 51, 22, 7])):
        fig, ax = axes("Bar orientation (degrees)", "Mean firing rate (spikes/s)")
        angles = [0, 45, 90, 135]
        ax.bar(angles, rates, width=19, color=COLORS[0])
        ax.set(xticks=angles, ylim=(0, 60), title=f"Simulated recording · unit {'XY'[i]}")
        save(fig, f"sensory_orient{i}", indexed=True)

    for example in ("closure", "continuation"):
        fig, ax = plt.subplots(figsize=(3.3, 2.4), layout="constrained")
        if example == "closure":
            for start in np.arange(0, 360, 72):
                t = np.deg2rad(np.linspace(start, start + 48, 80))
                ax.plot(np.cos(t), np.sin(t), lw=3, color="#243745")
        else:
            t = np.linspace(-1.3, 1.3, 120)
            ax.plot(t, .55 * np.sin(t), lw=3, color="#243745")
            ax.plot(t, -.55 * np.sin(t), lw=3, color="#243745")
        ax.set(xlim=(-1.5, 1.5), ylim=(-1.16, 1.16), aspect="equal")
        ax.axis("off")
        save(fig, "sensory_" + example, indexed=True)

    fig, ax = axes("", "Patients correctly classified (%)")
    positions = np.arange(2)
    for offset, values, title, hatch in [
        (-.18, [100, 41], "Earlier IASP", ""),
        (.18, [99, 68], "Budapest clinical", "//"),
    ]:
        ax.bar(positions + offset, values, width=.36, label=title,
               color=COLORS[int(offset > 0)], hatch=hatch)
    ax.set(xticks=positions, xticklabels=["With CRPS", "Other neuropathic pain"],
           ylim=(0, 127), yticks=[0, 25, 50, 75, 100], title="CRPS diagnostic validation cohort")
    ax.legend(loc="upper right", ncol=2, fontsize=8)
    save(fig, "sensory_budapest", indexed=True)


def neuroendocrine_measurements():
    for name, times in [("close", [10, 14, 18]), ("apart", [10, 35, 60])]:
        fig, ax = axes("Time (ms)", "Membrane potential (mV)")
        t = np.linspace(0, 85, 851)
        v = np.full_like(t, -70.0)
        for onset in times:
            dt = np.maximum(t - onset, 0)
            v += 8.5 * (1 - np.exp(-dt / 0.7)) * np.exp(-dt / 13)
            ax.plot(onset, -72, "^", color=COLORS[1], ms=5)
        ax.plot(t, v, color=COLORS[0], lw=2.3)
        ax.axhline(-55, color="#494f54", ls="--", label="Threshold")
        ax.set(ylim=(-74, -48), title="Simulated graded response to three inputs")
        ax.legend(loc="upper right")
        save(fig, "neuroend_" + name, indexed=True)

    fig, ax = axes("", "Defined daily doses")
    ax.errorbar([0, 1], [3, 3], yerr=[[2, 1.9], [2, 2.9]], fmt="o", color=COLORS[0],
                capsize=6, lw=2.3, label="Median and interquartile range")
    ax.set(xticks=[0, 1], xticklabels=["CT strategy", "AVS strategy"], xlim=(-0.6, 1.6),
           ylim=(0, 7.2), title="SPARTACUS · treatment at one year")
    ax.legend(loc="upper left")
    save(fig, "neuroend_spartacus", indexed=True)


def demographic_and_ulcer_studies():
    for name, left, right in [
        ("young", [27, 23, 18, 14, 10, 6], [26, 22, 18, 14, 11, 7]),
        ("older", [12, 14, 16, 22, 20, 14], [12, 14, 17, 22, 20, 17]),
    ]:
        fig, ax = axes("Residents (thousands)", "Age group (years)")
        y = np.arange(6)
        ax.barh(y, -np.array(left), color=COLORS[0], label="Male")
        ax.barh(y, right, color=COLORS[1], label="Female")
        ax.set(yticks=y, yticklabels=["0–14", "15–29", "30–44", "45–59", "60–74", "75+"],
               xticks=[-30, -20, -10, 0, 10, 20, 30],
               xticklabels=["30", "20", "10", "0", "10", "20", "30"],
               xlim=(-31, 31), title="Age distribution of simulated residents")
        ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, -0.23))
        save(fig, "demopattern_" + name, indexed=True)

    fig, ax = axes("", "13-month recurrent bleeding incidence (%)")
    bars = ax.bar(["Celecoxib + placebo", "Celecoxib + esomeprazole"], [8.9, 0], color=COLORS)
    ax.bar_label(bars, labels=["8.9%", "0%"], padding=4)
    ax.set(ylim=(0, 11), title="After a healed NSAID-associated ulcer bleed")
    save(fig, "gidrug_bleeding", indexed=True)


def myocardial_and_bonding_studies():
    for name, values in [("low", [200, 150]), ("athlete", [200, 80])]:
        fig, ax = axes("", "Left ventricular volume (mL)")
        bars = ax.bar(["End diastole", "End systole"], values, color=COLORS)
        ax.bar_label(bars, padding=4)
        ax.set_ylim(0, 235)
        ax.set_title("Ventricular volumes in a simulated study")
        save(fig, "myostudy_" + name, indexed=True)

    fig, ax = axes("", "Participants meeting relapse criteria (%)")
    bars = ax.bar(["Phased withdrawal", "Continued therapy"], [44, 0], color=COLORS)
    ax.bar_label(bars, labels=["11 / 25", "0 / 26"], padding=5)
    ax.set(ylim=(0, 55), title="TRED-HF · first six months after randomization")
    save(fig, "myostudy_tred", indexed=True)

    for name, top_right, bottom_right in [("same", "Cl", "F"), ("opposite", "F", "Cl")]:
        fig, ax = plt.subplots(figsize=(4.5, 2.8), layout="constrained")
        ax.set(xlim=(-1.8, 1.8), ylim=(-1.1, 1.1), aspect="equal")
        ax.axis("off")
        for y in [-0.06, 0.06]:
            ax.plot([-0.43, 0.43], [y, y], color="#20252b", lw=2.3)
        for x, side, upper, lower in [(-0.52, -1, "Br", "H"), (0.52, 1, top_right, bottom_right)]:
            ax.text(x, 0, "C", va="center", ha="center", fontsize=20, backgroundcolor="white")
            for sign, atom in [(1, upper), (-1, lower)]:
                ax.plot([x + side*0.12, x + side*0.52], [sign*0.13, sign*0.59], color="#20252b", lw=2)
                ax.text(x + side*0.68, sign*0.75, atom, ha="center", va="center", fontsize=18)
        save(fig, "bondstudy_" + name, indexed=True)


    # Newman projections along butane C2–C3, looking from front carbon to back.
    for name, back_methyl in [("anti", 270), ("gauche", 30)]:
        fig, ax = plt.subplots(figsize=(3.8, 3.3), layout="constrained")
        ax.set(xlim=(-1.6, 1.6), ylim=(-1.5, 1.5), aspect="equal")
        ax.axis("off")
        ax.add_patch(plt.Circle((0, 0), 0.38, fill=False, color="#425461", lw=2))
        for is_front, angles, methyl in [(False, (30, 150, 270), back_methyl), (True, (90, 210, 330), 90)]:
            for angle in angles:
                x, y = np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))
                start = 0 if is_front else 0.38
                ax.plot([start*x, 0.99*x], [start*y, 0.99*y], color="#253843", lw=2)
                ax.text(1.22*x, 1.22*y, "CH₃" if angle == methyl else "H",
                        ha="center", va="center", fontsize=17)
        ax.plot(0, 0, "o", color="#253843", ms=5)
        save(fig, "bondstudy_" + name, indexed=True)


def cardiovascular_drug_studies():
    """Draw simulated clinical measurements and observed STOP-CA trial outcomes."""
    for name, systolic, diastolic in [
        ("postural", [132, 103, 102], [76, 63, 62]),
        ("stable", [132, 125, 124], [76, 74, 73]),
    ]:
        fig, ax = axes("Position and time", "Blood pressure (mm Hg)")
        for values, label, color in [(systolic, "Systolic", COLORS[0]), (diastolic, "Diastolic", COLORS[1])]:
            ax.plot(["Supine", "Standing 1 min", "Standing 3 min"], values, "o-", label=label, color=color)
            for i, value in enumerate(values):
                ax.annotate(str(value), (i, value), xytext=(0, 7), textcoords="offset points", ha="center")
        ax.set(ylim=(45, 155), title="Postural blood pressures • simulated readings")
        ax.legend(loc="lower left", ncol=2)
        save(fig, "cvdrug_" + name, indexed=True)

    for name, end in [("strain20", 16), ("strain5", 19)]:
        fig, ax = axes("Study", "GLS magnitude (%)")
        ax.plot(["Baseline", "Follow-up"], [20, end], "o-", color=COLORS[0], lw=2.5)
        for i, value in enumerate((20, end)):
            ax.annotate(str(value), (i, value), xytext=(0, 8), textcoords="offset points", ha="center")
        ax.set(xlim=(-.3, 1.3), ylim=(12, 24), title="Simulated longitudinal strain")
        save(fig, "cvdrug_" + name, indexed=True)

    fig, ax = axes("", "Participants meeting the LVEF endpoint (%)")
    counts = (13, 33)
    bars = ax.bar(["Atorvastatin", "Placebo"], [100 * n / 150 for n in counts], color=COLORS)
    ax.bar_label(bars, labels=[f"{n}/150" for n in counts], padding=4)
    ax.set(ylim=(0, 30), title="STOP-CA • 12-month primary outcome")
    save(fig, "cvdrug_stopca", indexed=True)


def spine_and_separation_studies():
    """Plot simulated blood pressure and chromatography records and the Nordsten-DS estimate."""
    for name, context, values in [
        ("rise", ["Usual seated", "Headache", "Repeat"], [94, 136, 138]),
        ("fall", ["Supine", "Seated 1 min", "Seated 3 min"], [116, 92, 86]),
    ]:
        fig, ax = axes("Observation", "Systolic blood pressure (mm Hg)")
        ax.plot(context, values, "o-", color=COLORS[0])
        for i, value in enumerate(values):
            ax.annotate(str(value), (i, value), xytext=(0, 7), textcoords="offset points", ha="center")
        ax.set(ylim=(65, 158), xlim=(-.2, 2.2), title="Blood pressure record • high spinal injury")
        save(fig, "spinestudy_" + name, indexed=True)

    time = np.linspace(0, 12, 420)
    for name, width in [("resolved", .32), ("overlap", 1.10)]:
        fig, ax = axes("Retention time (min)", "Detector response (arbitrary units)")
        response = (np.exp(-.5 * ((time-4.8)/width)**2)
                    + .9 * np.exp(-.5 * ((time-7.2)/width)**2))
        ax.plot(time, response, color=COLORS[0], linewidth=2.3)
        ax.set(xlim=(0, 12), ylim=(-.03, 1.25), title="Two-analyte mixture • simulated detector trace")
        save(fig, "spinestudy_" + name, indexed=True)

    fig, ax = axes("Responder difference (percentage points)", "")
    ax.axvline(-15, color=COLORS[1], linestyle="--", label="Prespecified boundary (−15)")
    ax.axvline(0, color="#777", linestyle=":", label="Equal response rates")
    ax.errorbar(.4, 0, xerr=[[11.6], [11.5]], fmt="o", color=COLORS[0],
                capsize=6, linewidth=2.3)
    ax.text(.4, .18, "+0.4 (95% CI −11.2 to +11.9)", ha="center", fontsize=9)
    ax.set(yticks=[], xlim=(-22, 19), ylim=(-.7, .85),
           title="Nordsten-DS • decompression alone minus fusion")
    ax.legend(loc="lower center", fontsize=8)
    save(fig, "spinestudy_nord", indexed=True)


def abdominal_wall_and_equity_studies():
    """Show groin landmarks, reported INCA outcomes and simulated population comparisons."""
    from matplotlib.patches import Ellipse

    for name, neck in [("indirect", (3.15, 1.80)), ("direct", (1.55, 1.14))]:
        fig, ax = plt.subplots(figsize=(5.6, 3.5), layout="constrained")
        ax.set(xlim=(-.15, 4.6), ylim=(-.40, 3.10), aspect="equal",
               title="Groin landmarks • X marks the hernia neck")
        ax.axis("off")
        ax.plot([.25, 4.30], [.12, 1.88], color="#555", lw=4, solid_capstyle="round")
        ax.text(2.9, .82, "Inguinal ligament", ha="center", rotation=23, color="#454545")
        ax.plot([2.83, 2.48, 1.72], [1.22, 1.92, 2.69], lw=3, color=COLORS[1])
        ax.annotate("Inferior epigastric vessels", (2.03, 2.38), xytext=(2.45, 2.82),
                    arrowprops=dict(arrowstyle="-", color="#555"), fontsize=9)
        ax.add_patch(Ellipse((3.15, 1.80), .54, .26, angle=20, fill=False, ec="#444", lw=2))
        ax.annotate("Deep ring", (3.29, 1.94), xytext=(3.55, 2.25),
                    arrowprops=dict(arrowstyle="-", color="#555"), fontsize=9)
        ax.plot(*neck, marker="X", markersize=11, color=COLORS[0])
        ax.text(.10, -.24, "Medial", weight="bold")
        ax.text(4.42, -.24, "Lateral", ha="right", weight="bold")
        save(fig, "wallstudy_" + name, indexed=True)

    for name, values in [("even", [50, 50, 50, 50]), ("sorted", [90, 90, 10, 10])]:
        fig, ax = axes("Neighborhood (equal population sizes)", "Residents in group A (%)")
        bars = ax.bar(["North", "South", "East", "West"], values, width=.60, color=COLORS[0])
        ax.bar_label(bars, labels=[f"{v}%" for v in values], padding=3)
        ax.set(ylim=(0, 109), yticks=range(0,101,20), title="Neighborhood composition")
        save(fig, "wallstudy_" + name, indexed=True)

    for name, values in [("gradient", [16, 12, 8, 4]), ("threshold", [16, 6, 6, 6])]:
        fig, ax = axes("Income group", "Residents with illness (%)")
        bars = ax.bar(["Lowest", "Lower middle", "Upper middle", "Highest"], values,
                      width=.60, color=COLORS[0])
        ax.bar_label(bars, labels=[f"{v}%" for v in values], padding=3)
        ax.set(ylim=(0, 20), title="Observed prevalence by income group")
        save(fig, "wallstudy_" + name, indexed=True)

    fig, ax = axes("Symptoms at entry to observation", "Estimated crossover to surgery (%)")
    bars = ax.bar(["Asymptomatic", "Mildly symptomatic"], [60.4, 71.7], width=.55, color=COLORS)
    ax.bar_label(bars, labels=["60.4%", "71.7%"], padding=3)
    ax.set(ylim=(0, 100), title="INCA trial • 12-year follow-up")
    save(fig, "wallstudy_inca", indexed=True)


def congenital_and_identity_studies():
    """Draw original spinal schematics, longitudinal studies and the MOMS trial comparison."""
    from matplotlib.patches import Ellipse

    for name, exposed in [("meningo", False), ("myelo", True)]:
        fig, ax = plt.subplots(figsize=(5.0, 3.3), layout="constrained")
        ax.set(xlim=(-2.6, 2.6), ylim=(-1.1, 2.6), aspect="equal",
               title="Spinal defect in cross-section • posterior at top")
        ax.axis("off")
        # A posterior sac communicates with the spinal canal through the bony gap.
        x = [-.40, -.45, -.74, -.87, -.75, -.42, 0, .42, .75, .87, .74, .45, .40,
              .76, .83, .55, 0, -.55, -.83, -.76, -.40]
        y = [.42, .83, 1.10, 1.48, 1.82, 2.04, 2.11, 2.04, 1.82, 1.48, 1.10,
             .83, .42, .20, -.22, -.54, -.65, -.54, -.22, .20, .42]
        ax.fill(x, y, facecolor="#d7ecf2", edgecolor="#317288", linewidth=2)
        ax.plot([-.44, -.84, -1.04, -.86, -.5, 0, .5, .86, 1.04, .84, .44],
                [.50, .36, -.10, -.52, -.77, -.87, -.77, -.52, -.10, .36, .50],
                color="#696866", linewidth=8, solid_capstyle="butt")
        neural_y = 1.47 if exposed else -.10
        ax.add_patch(Ellipse((0, neural_y), .51, .29, facecolor="#bc591d", edgecolor="#793510"))
        if exposed:
            ax.plot([0, -.05, -.17, -.31], [1.42, 1.03, .65, .27], color="#bc591d", lw=2)
        for label, xy, pos in [("Neural tissue", (.20, neural_y), (1.38, neural_y+.12)),
                               ("Bony arch", (-.95, -.13), (-1.45, -.55)),
                               ("Meningeal sac", (-.73, 1.81), (-1.35, 2.14))]:
            ax.annotate(label, xy, xytext=pos, ha="left" if pos[0]>0 else "right",
                        va="center", fontsize=9, arrowprops=dict(arrowstyle="-", color="#444"))
        save(fig, "congenstudy_" + name, indexed=True)

    for name, zscores in [("smallbirth", [-2.65, -2.61, -2.56, -2.62]),
                          ("smalllater", [.15, -.65, -1.64, -2.81])]:
        fig, ax = axes("Age (months)", "Head circumference z score")
        ax.axhline(-2, color="#666", linestyle=":", label="−2 SD reference")
        ax.plot([0, 2, 4, 6], zscores, "o-", color=COLORS[0], label="Infant")
        ax.set(xticks=[0, 2, 4, 6], ylim=(-3.5, 1.5), title="Serial measurements • term infant")
        ax.legend()
        save(fig, "congenstudy_" + name, indexed=True)

    for name, a, b in [("stiff", [5, 7, 9, 11], [5, 14, 23, 32]),
                       ("flex", [6, 16, 26, 36], [6, 9, 12, 15])]:
        fig, ax = axes("Volume added (mL)", "Detrusor pressure (cm H₂O)")
        for vals, label, style, color in [(a, "A", "o-", COLORS[0]), (b, "B", "s--", COLORS[1])]:
            ax.plot([0, 30, 60, 90], vals, style, color=color, label="Bladder " + label)
        ax.set(xticks=[0, 30, 60, 90], ylim=(0, 42), title="Controlled filling measurements")
        ax.legend()
        save(fig, "congenstudy_" + name, indexed=True)

    fig, ax = axes("Assigned repair", "Received a CSF shunt (%)")
    bars = ax.bar(["Prenatal", "Postnatal"], [40, 82], color=COLORS, width=.55)
    ax.bar_label(bars, labels=["40%", "82%"], padding=3)
    ax.set(ylim=(0, 100), title="MOMS trial • actual shunt placement by 12 months")
    save(fig, "congenstudy_moms", indexed=True)

    fig, ax = axes("Assessment", "Mean self-concept score")
    ax.plot([0, 1], [2, 4], "o-", color=COLORS[0], label="Group A")
    ax.plot([0, 1], [4, 6], "s--", color=COLORS[1], label="Group B")
    ax.set(xticks=[0, 1], xticklabels=["Before", "After"], yticks=range(1, 8),
           ylim=(.5, 7.5), xlim=(-.2, 1.2), title="Self-concept in two mentoring groups")
    ax.legend()
    save(fig, "congenstudy_equalgain", indexed=True)

    for name, rows in [("switches", [["A at visit 1", 20, 10], ["B at visit 1", 10, 20]]),
                       ("stays", [["A at visit 1", 30, 0], ["B at visit 1", 0, 30]])]:
        study_table("congenstudy_" + name, "Preferred identity label • paired respondents",
                    ["Initial response", "A at visit 2", "B at visit 2"], rows, indexed=True)


def motor_and_inheritance_studies():
    """Draw clinical records, inheritance diagrams and the Clarity AD and ENDEAR results."""
    for name, durations in [("qrsrecover", [158, 138, 106, 92]),
                            ("qrsworse", [116, 138, 162, 180])]:
        fig, ax = axes("Minutes of monitored treatment", "QRS duration (ms)")
        ax.plot([0, 10, 20, 30], durations, "o-", color=COLORS[0])
        ax.set(title="Serial ECG measurements", ylim=(70, 205), xticks=[0, 10, 20, 30])
        save(fig, "neuromus_" + name, indexed=True)

    for name, rows in [
        ("independent", [["Bills", "Pays accurately using a checklist"],
                         ["Medicines", "Fills pillbox without help"],
                         ["Shopping", "Uses own list independently"]]),
        ("dependent", [["Six months ago", "Managed own medicines"],
                       ["Last month", "Forgot doses, then repeated them"],
                       ["Now", "Needs another person to give doses"]]),
    ]:
        study_table("neuromus_" + name, "Collateral functional record",
                    ["Task or interval", "Observation"], rows, indexed=True)

    fig, ax = axes("Seconds from start of grip", "Grip force (% of initial hold)")
    ax.plot([0, 1.9, 2, 2.3, 3, 4, 5, 6], [100, 100, 100, 78, 52, 27, 9, 0],
            "o-", color=COLORS[0], label="Patient")
    ax.plot([0, 1.9, 2, 2.3, 3, 4, 5, 6], [100, 100, 100, 2, 0, 0, 0, 0],
            "--", color=COLORS[1], label="Comparison")
    ax.axvline(2, color="#555", linestyle=":")
    ax.set(ylim=(-6, 112), title="Instruction to release the grip at 2 seconds")
    ax.legend()
    save(fig, "neuromus_grip", indexed=True)

    for name, rows in [
        ("peak", [["07:00", "Levodopa dose", "Stiff, slow"],
                  ["08:00", "Best mobility", "Excess flowing movements"],
                  ["10:45", "Benefit waning", "Excess movements gone"]]),
        ("off", [["08:00", "Levodopa dose", "Slow before dose"],
                 ["09:00", "Usual walking speed", "No stiffness"],
                 ["11:45", "Before next dose", "Slow and stiff again"]]),
    ]:
        study_table("neuromus_" + name, "Patient motor diary",
                    ["Time", "Medication or function", "Observation"], rows, indexed=True)

    fig, ax = plt.subplots(figsize=(4.7, 3.1), layout="constrained")
    ax.set(xlim=(-.2, 3.2), ylim=(-.3, 2.9), title="Paired replicated homologs in prophase I")
    ax.axis("off")
    for center, labels, group, color in [(.6, "AB", "Homolog 1", COLORS[0]),
                                         (2.4, "CD", "Homolog 2", COLORS[1])]:
        for sign, letter in zip([-1, 1], labels):
            outer = center + .30 * sign
            ax.plot([outer, center + .045 * sign, outer], [.35, 1.3, 2.3],
                    color=color, linewidth=5, solid_capstyle="round")
            ax.text(outer, 2.48, letter, ha="center", weight="bold")
        ax.plot(center, 1.3, "o", color=color, markersize=6)
        ax.text(center, 0, group, ha="center")
    save(fig, "neuromus_tetrad", indexed=True)

    study_table("neuromus_double", "Three-marker testcross",
                ["Parental haplotypes", "Rare reciprocal products"],
                [["ABC", "AbC"], ["abc", "aBc"]], indexed=True)

    for name, counts in [("deficit", [40, 20, 40]), ("hw", [25, 50, 25])]:
        fig, ax = axes("Observed genotype", "Number of plants")
        bars = ax.bar(["AA", "Aa", "aa"], counts, color=COLORS[0], width=.6)
        ax.bar_label(bars, padding=3)
        ax.set(ylim=(0, 65), title="Diploid population sample · 100 plants")
        save(fig, "neuromus_" + name, indexed=True)

    for name, title, ylabel, groups, values, upper, labels in [
        ("clarity", "Clarity AD · 18 months", "Adjusted mean change in CDR-SB",
         ["Lecanemab", "Placebo"], [1.21, 1.66], 2, ["+1.21", "+1.66"]),
        ("endear", "ENDEAR · final analysis", "Motor milestone responders (%)",
         ["Nusinersen", "Sham procedure"], [100 * 37 / 73, 0], 65,
         ["37/73 (51%)", "0/37 (0%)"]),
    ]:
        fig, ax = axes("Randomized group", ylabel)
        bars = ax.bar(groups, values, color=COLORS, width=.55)
        ax.bar_label(bars, labels=labels, padding=4)
        ax.set(ylim=(0, upper), title=title)
        save(fig, "neuromus_" + name, indexed=True)


def sleep_and_headache_studies():
    """Render original patient diaries, a cognition experiment and two published comparisons."""
    for name, responses in [("ltp", [99, 101, 100, 164, 154, 151, 150]),
                            ("transient", [100, 99, 101, 160, 122, 102, 99])]:
        fig, ax = axes("Minutes relative to conditioning", "Test response (% of baseline)")
        ax.plot([-15, -10, -5], responses[:3], "o-", color=COLORS[0])
        ax.plot([2, 15, 30, 45], responses[3:], "o-", color=COLORS[0])
        ax.axvline(0, linestyle="--", color="#68747a", linewidth=1.3)
        ax.axhline(100, linestyle=":", color="#68747a", linewidth=1)
        ax.set(ylim=(75, 180), xticks=[-15, 0, 15, 30, 45],
               title="Fixed test stimulus · conditioning train at 0 min")
        save(fig, "sleepstudy_" + name, indexed=True)

    for name, migraine, pressure in [
        ("distinct", [1, 5, 10], [2, 4, 7, 8]),
        ("overlap", [1, 3, 6, 9], [2, 3, 4, 6, 7, 8]),
    ]:
        fig, ax = axes("Day of observation", "")
        for y, days, color, marker in [(1, migraine, COLORS[0], "o"), (0, pressure, COLORS[1], "s")]:
            ax.scatter(days, [y] * len(days), c=color, marker=marker, s=64)
        ax.set(yticks=[0, 1], yticklabels=["Pressure-type", "Migraine"],
               xticks=range(1, 11), ylim=(-.6, 1.6), xlim=(.6, 10.4),
               title="Headache diary · one mark per type per date")
        save(fig, "sleepstudy_" + name, indexed=True)

    fig, ax = axes("Time of day", "Day of bout")
    for day, start, minutes in [(1, 1.0, 60), (2, 1.2, 55), (3, 1.0, 70),
                                (4, 1.35, 65), (5, 1.1, 60)]:
        ax.broken_barh([(start, minutes / 60)], (day - .3, .6), facecolors=COLORS[0])
    ax.set(xlim=(0, 6), xticks=range(7), xticklabels=[f"{h:02d}:00" for h in range(7)],
           ylim=(5.6, .4), yticks=range(1, 6), title="Recorded painful intervals")
    save(fig, "sleepstudy_cluster", indexed=True)

    for name, starts in [("delay", [26.75, 27.25, 27.0, 27.5]),
                         ("advance", [18.75, 19.25, 19.0, 19.5])]:
        fig, ax = axes("Clock time from evening to midday", "Free day")
        for day, start in enumerate(starts, 1):
            ax.broken_barh([(start, 8)], (day - .28, .56), facecolors=COLORS[0])
        times = [18, 21, 24, 27, 30, 33, 36]
        ax.set(xlim=(18, 36), xticks=times, xticklabels=[f"{h % 24:02d}:00" for h in times],
               ylim=(4.6, .4), yticks=[1, 2, 3, 4], title="Sleep diary · bars show time asleep")
        save(fig, "sleepstudy_" + name, indexed=True)

    for name, labels, rates, outcome, title in [
        ("absence", ["Ethosuximide", "Valproate", "Lamotrigine"], [53, 58, 29],
         "Freedom from treatment failure (%)", "Childhood absence epilepsy trial"),
        ("oxygen", ["Oxygen", "Air"], [78, 20], "Attacks meeting endpoint (%)",
         "Cluster headache trial · relief at 15 minutes"),
    ]:
        fig, ax = axes("Randomized treatment", outcome)
        bars = ax.bar(labels, rates, color=COLORS[0], width=.6)
        ax.bar_label(bars, labels=[f"{v}%" for v in rates], padding=3)
        ax.set(ylim=(0, 100), title=title)
        save(fig, "sleepstudy_" + name, indexed=True)

    fig, ax = plt.subplots(figsize=(4.8, 2.0), layout="constrained")
    ax.axis("off")
    ax.set_title("Recall of a new list · simulated experiment")
    table = ax.table(cellText=[["A", "30", "20"], ["B", "24", "8"]],
                     colLabels=["Group", "Old-list intrusions", "Participants"],
                     cellLoc="center", colWidths=[.19, .48, .33], loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.6)
    save(fig, "sleepstudy_intrusions", indexed=True)


def trauma_and_neural_signals():
    """Draw simulated contusions, CSF pathways and cell recordings, plus the PENS trial result."""
    for name, volumes in [("contstable", [6, 6, 6]), ("contgrow", [4, 11, 22])]:
        fig, ax = axes("Hours after injury", "Hemorrhagic volume (mL)")
        ax.plot([1, 4, 8], volumes, "o-", color=COLORS[0], linewidth=2)
        ax.set(xticks=[1, 4, 8], ylim=(0, 25), title="Serial CT estimates")
        save(fig, "neurotrauma_" + name, indexed=True)

    for name, sizes in [("aqueduct", [1.0, 1.0, .8, .4]), ("monro", [1.0, .4, .4, .4])]:
        from matplotlib.patches import Ellipse
        fig, ax = plt.subplots(figsize=(5.0, 3.2), layout="constrained")
        ax.set(xlim=(-2.4, 2.4), ylim=(-.44, 2.9), aspect="equal",
               title="Ventricular size relative to baseline")
        ax.axis("off")
        coords = [(-1.05, 2.0), (1.05, 2.0), (0, 1.1), (0, .15)]
        for start, end in [(0, 2), (1, 2), (2, 3)]:
            x, y = zip(coords[start], coords[end])
            ax.plot(x, y, color="#64748b", zorder=1)
        for (x, y), size, label in zip(coords, sizes, ["Left lateral", "Right lateral", "Third", "Fourth"]):
            ax.add_patch(Ellipse((x, y), size, size * .65, facecolor="#a6d7e5",
                                 edgecolor=COLORS[0], linewidth=2, zorder=2))
            ax.add_patch(Ellipse((x, y), .4, .26, facecolor="none", edgecolor="#182c34",
                                 linestyle=":", linewidth=1.3, zorder=3))
            if y > 1.5:
                ax.text(x, y + .42, label, ha="center", va="center")
            else:
                ax.text(x + .65, y, label, ha="left", va="center")
        ax.text(-2.3, -.40, "Dotted outline = baseline size", fontsize=9)
        save(fig, "neurotrauma_" + name, indexed=True)

    fig, ax = axes("Time (ms)", "Membrane potential (mV)")
    xs = np.array([-.5, -.18, 0, .28, .5, .8])
    for peak, label, color, style in [(1, "Site A", COLORS[0], "-"), (3, "Site B", COLORS[1], "--")]:
        ax.plot([0, *(xs + peak), 4.4], [-70, -70, -52, 32, -42, -78, -70, -70],
                style, color=color, label=label, linewidth=2.1)
    ax.set(xticks=[0, 1, 2, 3, 4], title="Same axon, sites 30 mm apart")
    ax.legend()
    save(fig, "neurotrauma_axon", indexed=True)

    fig, ax = axes("Membrane potential (mV)", "Net current (pA)")
    ax.axhline(0, color="#6b7280", lw=1)
    ax.plot([30, 40, 50, 60, 70], [-16, -8, 0, 8, 16], "o-", color=COLORS[0])
    ax.set(xticks=[30, 40, 50, 60, 70], yticks=[-16, -8, 0, 8, 16], title="Voltage-clamp recording")
    save(fig, "neurotrauma_reverse", indexed=True)

    fig, ax = plt.subplots(figsize=(5.0, 2.0), layout="constrained")
    ax.axvline(0, color="#555", linestyle="--", linewidth=1.1)
    ax.errorbar(.21, 0, xerr=[[.09], [.10]], fmt="o", color=COLORS[0], capsize=6)
    ax.set(xlim=(-.06, .36), ylim=(-1, 1), yticks=[], xticks=[0, .1, .2, .3],
           xlabel="Open minus placebo setting (m/s), 95% CI",
           title="PENS trial · Difference in three-month gait velocity change")
    save(fig, "neurotrauma_pens", indexed=True)


def mood_course_and_arousal():
    """Independent clinical timelines, a trial outcome and a simulated physiology study."""
    for name, xlabel, end, ticks, tracks in [
        ("brief", "Days since onset", 30, [0, 5, 10, 15, 20, 25, 30],
         [("Delusions and\ndisorganized speech", 0, 12), ("Usual functioning", 12, 30)]),
        ("long", "Months since first disturbance", 8, list(range(9)),
         [("Functional decline and\ncontinuous disturbance", 0, 8),
          ("Delusions and\ndisorganized speech", 4, 5.5)]),
    ]:
        fig, ax = plt.subplots(figsize=(5.7, 2.15), layout="constrained")
        for i, (label, start, finish) in enumerate(tracks):
            ax.barh(i, finish-start, left=start, height=.43, color=COLORS[i])
        ax.set(yticks=[0,1], yticklabels=[t[0] for t in tracks], xticks=ticks,
               xlim=(0,end), ylim=(1.55,-.55), xlabel=xlabel, title="Collateral history")
        ax.grid(axis="x", alpha=.22)
        save(fig, "bhmood_"+name, indexed=True)

    for name, alternating in [("low", False), ("both", True)]:
        fig, ax = plt.subplots(figsize=(5.4, 2.5), layout="constrained")
        months = np.arange(36)
        levels = np.tile([-1,-1,-1,0,-1,-1], 6)
        if alternating:
            levels = np.tile([-1,-1,0,1,1,0], 6)
        ax.step(months, levels, where="mid", color=COLORS[0], lw=1.9)
        ax.set(xlim=(0,35), xticks=[0,6,12,18,24,30,35], xlabel="Month of follow-up",
               ylim=(-1.45,1.45), yticks=[-1,0,1], yticklabels=["Low", "Usual", "Elevated"],
               title="Monthly predominant mood")
        ax.grid(alpha=.18)
        save(fig, "bhmood_"+name, indexed=True)

    fig, ax = axes("Randomized continuation treatment", "Relapsed within 36 weeks (%)")
    bars = ax.bar(["Olanzapine", "Placebo"], [20.3,54.8], width=.5, color=COLORS)
    ax.bar_label(bars, labels=["13/64 (20.3%)","34/62 (54.8%)"], padding=4)
    ax.set(ylim=(0,70), title="STOP-PD II: both groups continued sertraline")
    save(fig, "bhmood_trial", indexed=True)

    fig, ax = axes("Observation", "Mean heart rate (beats/min)")
    for i, (name, means) in enumerate([("Fear reported", [71, 96, 77]),
                                      ("Joy reported", [70, 95, 76])]):
        ax.plot(range(3), means, STYLES[i], color=COLORS[i], marker=["o","s"][i],
                lw=2, label=name)
    ax.set(xticks=[0,1,2], xticklabels=["Before","During","After"], ylim=(60,110),
           title="Two contexts in a simulated study")
    ax.legend(loc="upper center", ncol=2)
    save(fig, "bhmood_arousal", indexed=True)


def immunodeficiency_and_learning():
    """Draw immune test results, two illustrative tissue patterns and study outcomes."""
    from matplotlib.patches import Circle, Ellipse
    fig, ax = plt.subplots(figsize=(5.0, 2.5), layout="constrained")
    ax.axis("off")
    ax.set_title("Immune evaluation at 14 months", fontsize=14)
    panel = ax.table(cellText=[["CD19+ B cells", "<1% of lymphocytes"],
                               ["T-cell count", "Within age range"],
                               ["IgG, IgA, IgM", "All below age range"]],
                     colLabels=["Test", "Finding"], cellLoc="center",
                     bbox=[.02, .09, .96, .77])
    panel.set_fontsize(11)
    save(fig, "defstudy_bcells", indexed=True)

    for name, suppurative in [("abscess", True), ("gran", False)]:
        fig, ax = plt.subplots(figsize=(5.0, 2.6), layout="constrained")
        ax.set(aspect="equal", xlim=(-1.7, 3.9), ylim=(-1.35, 1.4))
        ax.axis("off")
        ax.set_title("Schematic tissue section", fontsize=13)
        ax.add_patch(Ellipse((0, 0), 2.9, 2.18,
                             facecolor="#fdf0d6", edgecolor="#9c7161", lw=2))
        if suppurative:
            for x, y in [(-.82,.2),(-.26,.63),(.57,.31),(.69,-.44),(-.44,-.50)]:
                ax.add_patch(Circle((x,y), .21, facecolor="#e5d9ed", edgecolor="#927d9f"))
                for dx, dy in [(-.07,.04),(.02,-.04),(.09,.04)]:
                    ax.add_patch(Circle((x+dx,y+dy), .065, facecolor="#6b427c"))
            for x, y in [(-.7,.63),(.05,.07),(.05,-.38),(.5,.7),(-.75,-.31)]:
                ax.plot(x,y,"x",color="#937b60",ms=4)
            ax.annotate("Neutrophil", xy=(.59,.31), xytext=(1.7,.6),
                        arrowprops={"arrowstyle":"->"}, va="center")
            ax.annotate("Cellular debris", xy=(.07,-.38), xytext=(1.7,-.52),
                        arrowprops={"arrowstyle":"->"}, va="center")
        else:
            for angle in np.linspace(0, 2*np.pi, 11, endpoint=False):
                x, y = 1.04*np.cos(angle), .78*np.sin(angle)
                ax.add_patch(Ellipse((x,y), .50, .29, angle=np.degrees(angle)+90,
                                     facecolor="#d7b49f",edgecolor="#95665b"))
                ax.add_patch(Circle((x,y), .078,facecolor="#795683"))
            ax.add_patch(Ellipse((0,0),1.04,.76,facecolor="#d4a899",edgecolor="#95665b"))
            for x,y in [(-.28,.02),(-.11,.17),(.12,.15),(.27,-.03)]:
                ax.add_patch(Circle((x,y), .078,facecolor="#795683"))
            ax.annotate("Macrophages", xy=(.96,.32), xytext=(1.7,.64),
                        arrowprops={"arrowstyle":"->"}, va="center")
            ax.annotate("Giant cell", xy=(.25,0), xytext=(1.7,-.53),
                        arrowprops={"arrowstyle":"->"}, va="center")
        save(fig, "defstudy_" + name, indexed=True)

    fig, ax = axes("Status at transplantation after age 3.5 months", "Five-year survival (%)")
    bars = ax.bar(["Never infected", "Resolved infection", "Active infection"],
                  [90,82,50], width=.59, color=[COLORS[0], "#708897", COLORS[1]])
    ax.set(ylim=(0,105), title="SCID transplant cohort, 2000–2009")
    ax.bar_label(bars, padding=3)
    save(fig, "defstudy_cohort", indexed=True)

    fig, ax = axes("Argument quality", "Audience endorsement (%)")
    for j, (label, value) in enumerate([("Low prestige",30),("High prestige",50)]):
        ax.plot([0,1], [value,value], STYLES[j], marker=["o","s"][j], color=COLORS[j],
                lw=2.3, label=label)
    ax.set(xticks=[0,1], xticklabels=["Weak","Strong"], xlim=(-.2,1.2), ylim=(0,80),
           title="Simulated message experiment")
    ax.legend(loc="upper center",ncol=2)
    save(fig, "defstudy_arguments", indexed=True)


def hiv_and_circuit_studies():
    """Display serial observations, paired laboratory findings, trial risks and a circuit."""
    fig, ax = axes("Month", "CD4 cells/µL")
    ax.plot([0, 3, 6, 9], [620, 490, 350, 230], marker="o", lw=2.4, color=COLORS[0])
    ax.set(xticks=[0, 3, 6, 9], ylim=(0, 700),
           title="HIV-2 follow-up")
    ax.text(.03, .09, "HIV-2 RNA below detection at all four visits",
            transform=ax.transAxes, fontsize=10)
    save(fig, "hivstudy_cd4", indexed=True)

    fig, ax = plt.subplots(figsize=(5.3, 2.6), layout="constrained")
    ax.axis("off")
    ax.set_title("Paired blood and urine tests", fontsize=14)
    table = ax.table(cellText=[["Plasma glucose", "92 mg/dL", "70–99"],
                               ["Urine glucose", "2+", "Negative"],
                               ["Serum phosphate", "1.6 mg/dL", "2.5–4.5"],
                               ["Phosphate excretion*", "26%", "<5% when low"]],
                     colLabels=["Measurement", "Result", "Reference"],
                     cellLoc="center", colWidths=[.38,.27,.35], bbox=[0, .14, 1, .76])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    ax.text(.01, .035, "*Fractional excretion during hypophosphatemia", transform=ax.transAxes)
    save(fig, "hivstudy_renal", indexed=True)

    fig, ax = axes("Timing of ART after cryptococcal meningitis diagnosis",
                   "Deaths by week 26 (%)")
    bars = ax.bar(["1–2 weeks", "About 5 weeks"], [45, 30], color=COLORS, width=.5)
    ax.bar_label(bars, labels=["45% (40/88)", "30% (27/89)"], padding=3)
    ax.set(ylim=(0, 56), title="COAT randomized trial")
    save(fig, "hivstudy_trial", indexed=True)

    fig, ax = plt.subplots(figsize=(4.8, 2.4), layout="constrained")
    ax.axis("off")
    ax.set(xlim=(-.9, 4.2), ylim=(-.4, 2.6), aspect="equal")
    ax.plot([0, 3.2], [0, 0], color="black")
    ax.plot([0, 3.2], [2, 2], color="black")
    for x, value in [(1.45, "3 Ω"), (3.2, "6 Ω")]:
        ax.plot([x, x], [0, .56], color="black")
        ax.plot([x, x], [1.40, 2], color="black")
        ax.add_patch(plt.Rectangle((x-.14, .56), .28, .84,
                                   facecolor="#e0eef2", edgecolor=COLORS[0], lw=2))
        ax.text(x+.24, 1, value, va="center")
    for y, halfwidth, end in [(.83, .20, 0), (1.15, .38, 2)]:
        ax.plot([0, 0], [end, y], color="black")
        ax.plot([-halfwidth, halfwidth], [y, y], color="black", lw=2)
    ax.text(-.55, 1.25, "+")
    ax.set_title("Circuit before the branch opens")
    save(fig, "hivstudy_branches", indexed=True)


def immunotherapy_and_electricity():
    """Independent review stimuli for drug safety and electric or magnetic fields."""
    fig, ax = axes("", "Platelets (thousands/µL)")
    bars = ax.bar(["EDTA", "Citrate", "Heparin"], [18, 212, 215],
                  color=[COLORS[1], COLORS[0], COLORS[0]], width=.55)
    ax.bar_label(bars, padding=3)
    ax.set(title="Simultaneous platelet measurements", xlabel="Collection tube",
           ylim=(0, 255))
    save(fig, "immunerx_tubes", indexed=True)

    fig, ax = axes("", "Observed reactivation (%)")
    counts = [(1, 41), (7, 39)]
    bars = ax.bar(["Preventive entecavir", "Treat on reactivation"],
                  [100 * x / n for x, n in counts], color=COLORS, width=.5)
    ax.bar_label(bars, labels=[f"{x} of {n}" for x, n in counts], padding=5)
    ax.set(title="HBV reactivation during follow-up", ylim=(0, 23))
    save(fig, "immunerx_trial", indexed=True)

    fig, ax = plt.subplots(figsize=(5.4, 2.0), layout="constrained")
    ax.axis("off")
    ax.set_title("Home medication record", fontsize=14)
    grid = ax.table(cellText=[["15 mg", "15 mg", "15 mg", "15 mg", "—"]],
                    colLabels=["Mon", "Tue", "Wed", "Thu", "Fri"],
                    cellLoc="center", bbox=[.02, .10, .96, .58])
    grid.set_fontsize(11)
    ax.text(.02, .81, "Prescription: methotrexate 15 mg every Monday for arthritis",
            transform=ax.transAxes, fontsize=10)
    save(fig, "immunerx_log", indexed=True)

    fig, ax = axes("Time from discharge onset (ms)", "Capacitor voltage (V)")
    time = np.linspace(0, 65, 200)
    ax.plot(time, 6 * 2 ** (-time / 20), color=COLORS[0], lw=2.5)
    ax.set(xlim=(0, 65), ylim=(0, 6.4), xticks=range(0, 61, 10),
           yticks=range(7))
    save(fig, "immunerx_discharge", indexed=True)

    fig, ax = plt.subplots(figsize=(4.8, 2.6), layout="constrained")
    ax.set(aspect="equal", xlim=(-1.5, 3.1), ylim=(-2.0, .8))
    ax.axis("off")
    xx, yy = np.meshgrid(np.arange(.1, 3, .4), np.arange(-1.9, .6, .4))
    ax.scatter(xx, yy, s=13, color="#82959d")
    angle = np.linspace(0, np.pi / 2, 100)
    ax.plot(1.6 * np.sin(angle), 1.6 * (np.cos(angle) - 1), lw=3, color=COLORS[1])
    ax.annotate("", xy=(.05, 0), xytext=(-1.25, 0),
                arrowprops={"arrowstyle": "->", "lw": 2, "color": COLORS[1]})
    ax.text(-1.4, .22, "Entry velocity", fontsize=10)
    ax.set_title("Uniform magnetic field out of the page")
    save(fig, "immunerx_track", indexed=True)


def immune_reaction_and_fuel_studies():
    """Sample compartments, paired clinical observations and simulated chemistry data."""
    from matplotlib.patches import Ellipse, FancyBboxPatch

    for name, cells in [("cells", True), ("plasma", False)]:
        fig, ax = plt.subplots(figsize=(5.0, 2.7), layout="constrained")
        ax.set(xlim=(0, 6.1), ylim=(-.12, 3.15), aspect="equal")
        ax.axis("off")
        ax.add_patch(FancyBboxPatch((.42, .26), 1.12, 2.49,
                     boxstyle="round,pad=0.02,rounding_size=0.12",
                     facecolor="#f3e3a8", edgecolor="#494648", lw=1.7))
        ax.fill_between([.45, 1.51], .35, 1.29, color="#ab4b4f")
        for x, y in [(.66, .61), (1.14, .67), (.87, 1.03)]:
            ax.add_patch(Ellipse((x, y), .28, .16, angle=-18,
                                 facecolor="#efad9f", edgecolor="#80393d"))
        ax.text(.98, 2.98, "Patient sample", ha="center", va="center", fontsize=10)
        ax.text(1.78, 2.44, "Plasma", fontsize=10)
        ax.text(1.78, .30, "Red cells", fontsize=10)
        y = .88 if cells else 1.94
        ax.annotate("", xy=(2.85, y), xytext=(1.58, y),
                    arrowprops={"arrowstyle": "->", "color": COLORS[0], "lw": 2})
        question = ("Already coated in\nthe circulation?" if cells else
                    "Antibody that binds\nreagent red cells?")
        ax.text(2.95, y, question, va="center", fontsize=11)
        save(fig, "immunelearn_" + name, indexed=True)

    for name, labels, values, ylabel, title in [
        ("trial", ["Omalizumab", "Placebo"], [67, 7], "Met endpoint (%)",
         "Peanut challenge after treatment"),
        ("tryptase", ["Acute (1 hour)", "Baseline after recovery"], [14, 5],
         "Tryptase (ng/mL)", "Paired serum samples"),
    ]:
        fig, ax = axes("", ylabel)
        bars = ax.bar(labels, values, color=COLORS, width=.55)
        ax.set_ylim(0, 100 if name == "trial" else 20)
        ax.set_title(title)
        ax.bar_label(bars, padding=3)
        if name == "trial":
            ax.set_xlabel("Single dose ≥600 mg peanut protein without dose-limiting symptoms",
                          fontsize=8)
        save(fig, "immunelearn_" + name, indexed=True)

    fig, ax = plt.subplots(figsize=(2.5, 3.1), layout="constrained")
    ax.set(xlim=(-1.1, 1.1), ylim=(-.5, 4.5), aspect="equal")
    ax.axis("off")
    ax.plot([0, 0], [.25, 3.77], color="#303030", lw=1.7)
    ax.text(0, 4, "CHO", ha="center", va="center")
    ax.text(0, 0, "CH₂OH", ha="center", va="center")
    for y in (1, 2, 3):
        ax.plot([-.55, .55], [y, y], color="#303030", lw=1.6)
        ax.text(-.62, y, "H", ha="right", va="center")
        ax.text(.62, y, "OH", ha="left", va="center")
    save(fig, "immunelearn_fischer", indexed=True)

    fig, ax = axes("Time (min)", "Released fatty acids (µmol)")
    for label, values, style, color in [("A", [0, 4, 8, 12], "-", COLORS[0]),
                                          ("B", [3, 5, 7, 9], "--", COLORS[1])]:
        ax.plot(range(4), values, style, color=color, lw=2.4, marker="o", label=label)
    ax.set(xticks=range(4), yticks=[0, 3, 5, 7, 9, 12], ylim=(-.6, 13),
           title="Two model fat-digestion vessels")
    ax.legend()
    save(fig, "immunelearn_lip", indexed=True)


def renal_inflammation_studies():
    """Simplified compartments for abscess localization and comparison of GBM widths."""
    from matplotlib.patches import Ellipse

    for name, site in [("inside", (2.1, 2.15)), ("outside", (3.54, 2.20))]:
        fig, ax = plt.subplots(figsize=(5.2, 2.8), layout="constrained")
        ax.set(xlim=(0, 6.3), ylim=(0, 3.6), aspect="equal")
        ax.axis("off")
        ax.add_patch(Ellipse((2.14, 1.81), 3.75, 3.2, facecolor="#f3e6c9",
                             edgecolor="#705c43", linewidth=2.1))
        ax.add_patch(Ellipse((2.04, 1.75), 2.48, 2.34, facecolor="#d8a898",
                             edgecolor="#783d37", linewidth=2.2))
        ax.add_patch(Ellipse((2.1, 1.42), .8, .40, angle=12,
                             facecolor="#eeeeeb", edgecolor="#827c75"))
        ax.add_patch(Ellipse(site, .50, .45, facecolor="#185e75",
                             edgecolor="#133b4b", linewidth=1.4))
        for title, boundary, label in [
            ("Renal fascia", (3.64, 2.77), (4.24, 3.12)),
            ("Renal capsule", (3.11, 1.18), (4.24, 1.08)),
        ]:
            ax.annotate(title, xy=boundary, xytext=label, va="center",
                        arrowprops={"arrowstyle": "-", "color": "#454545"})
        ax.text(4.24, .47, "●  Collection", color="#185e75", fontsize=10)
        ax.set_title("Renal cross-section (schematic)", fontsize=11)
        save(fig, "renalinfect_" + name, indexed=True)

    fig, ax = plt.subplots(figsize=(5.3, 2.7), layout="constrained")
    ax.set(xlim=(0, 5.9), ylim=(0, 3.5))
    ax.axis("off")
    x = np.linspace(1.45, 5.65, 160)
    for label, y, thickness in [("Reference", 2.75, .34), ("A", 1.68, .62),
                                ("B", .65, .13)]:
        center = y + .06 * np.sin(2.1 * x)
        ax.fill_between(x, center-thickness/2, center+thickness/2, color="#475369")
        ax.text(.12, y, label, va="center", fontsize=11)
    ax.set_title("Glomerular basement membrane profiles at equal scale", fontsize=11)
    save(fig, "renalinfect_gbm", indexed=True)


    for name, start, end in [("assaya", (0, 0), (12, 6)),
                             ("assayb", (4, 0), (12, 8))]:
        fig, ax = axes("Time (min)", "NADH in assay (nmol)")
        for i, label in enumerate(("A", "B")):
            ax.plot([0, 2], [start[i], end[i]], STYLES[i], color=COLORS[i],
                    label=label, lw=2.5, marker="o")
        ax.set(xlim=(-.1, 2.1), ylim=(-.6, 13), xticks=[0, 1, 2],
               yticks=np.arange(0, 13, 2), title="Isocitrate dehydrogenase assay")
        ax.legend()
        save(fig, "renalinfect_" + name, indexed=True)


def urinary_trauma_and_filling():
    """Teaching cystograms and pressure-volume curves, plus bladder CT study counts."""
    from matplotlib.patches import Ellipse

    for name, intraperitoneal in [("low", False), ("high", True)]:
        fig, ax = plt.subplots(figsize=(5.0, 3.1), layout="constrained")
        ax.set(xlim=(0, 6.6), ylim=(0, 4.3), aspect="equal")
        ax.axis("off")
        contrast = "#087991"
        ax.add_patch(Ellipse((2.4, 1.22), 2.0, 1.55,
                             facecolor=contrast, edgecolor="#313b42", linewidth=2))
        ax.text(2.4, 1.05, "Bladder", color="white", ha="center")
        x = np.linspace(.1, 4.7, 100)
        reflection = 1.53 + .54 * np.exp(-((x - 2.4) / 1.2) ** 2)
        ax.plot(x, reflection, ls="--", color="#555555", lw=1.6, zorder=4)
        ax.text(4.8, 1.55, "Peritoneal\nreflection", va="center", fontsize=9)
        for bx, by in [(1.35, 3.04), (2.54, 3.33), (3.72, 2.94)]:
            ax.add_patch(Ellipse((bx, by), 1.03, .69, angle=15,
                                 edgecolor="#804f3c", facecolor="#f0ddcb", lw=1.6))
        ax.text(4.8, 3.05, "Bowel loops", va="center", fontsize=9)
        if intraperitoneal:
            ax.plot([2.4, 2.4, 2.08, 1.96, 2.0], [1.88, 2.34, 2.79, 3.14, 3.4],
                    lw=4, color=contrast)
            ax.plot([2.42, 2.91, 3.17, 3.06], [2.28, 2.52, 2.86, 3.19],
                    lw=3, color=contrast)
        else:
            ax.plot([3.23, 3.52, 3.88, 4.24], [1.12, 1.21, .99, 1.11],
                    lw=5, color=contrast)
            ax.plot([3.66, 3.9, 4.27], [1.11, .79, .67], lw=3, color=contrast)
        ax.text(.12, .04, "Blue-green = bladder contrast", fontsize=10)
        save(fig, "urostudy_" + name, indexed=True)

    fig, ax = axes("Volume added (mL)", "Detrusor pressure (cm H₂O)")
    for mark, end, color in [("A", 10, COLORS[0]), ("B", 25, COLORS[1])]:
        ax.plot([0, 200], [5, end], color=color, lw=2.5, marker="o")
        ax.text(204, end, mark, color=color, va="center", fontweight="bold")
    ax.set(xticks=[0, 50, 100, 150, 200], yticks=[0, 5, 10, 15, 20, 25],
           xlim=(-8, 225), ylim=(0, 28), title="Two quiet bladder-filling studies")
    save(fig, "urostudy_fill", indexed=True)

    fig, ax = plt.subplots(figsize=(4.9, 2.1), layout="constrained")
    ax.axis("off")
    grid = ax.table(cellText=[["Rupture", "42", "2"], ["No rupture", "0", "272"]],
                    colLabels=["Final diagnosis", "CT positive", "CT negative"],
                    loc="center", cellLoc="center")
    grid.auto_set_font_size(False)
    grid.set_fontsize(11)
    grid.scale(1, 1.65)
    ax.set_title("CT cystography in 316 blunt trauma patients", fontsize=11)
    save(fig, "urostudy_ct", indexed=True)


def renal_medication_studies():
    """Clinical sampling times, published kidney outcomes and simulated ion data."""
    fig, ax = axes("Hours from first infusion start", "")
    ax.grid(False)
    ax.set(xlim=(-.35, 8.9), ylim=(-.55, .9), yticks=[], xticks=[0, 1, 2, 4, 6, 8])
    ax.axhline(0, color="0.6", lw=1)
    for start in (0, 8):
        ax.plot([start, start + .5], [0, 0], color=COLORS[0], lw=9,
                solid_capstyle="butt")
    ax.annotate("Blood drawn", xy=(1, .04), xytext=(2.3, .5),
                arrowprops={"arrowstyle": "->"}, ha="center")
    ax.text(4, -.25, "Blue bars = 30-minute IV infusions", ha="center")
    ax.set_title("Gentamicin administration and sampling")
    save(fig, "rxkid_gent", indexed=True)

    for name, labels, values, ylabel, title, limit in [
        ("walsh", ["Conventional", "Liposomal"], [34, 19], "Patients (%)",
         "Amphotericin B: creatinine twice the upper limit of normal", 50),
        ("eos", ["Sensitivity", "Specificity"], [30.8, 68.2], "Percent",
         "Urine eosinophils at a 1% cutoff vs kidney biopsy", 100),
    ]:
        fig, ax = axes("", ylabel)
        bars = ax.bar(labels, values, color=COLORS, width=.52, zorder=2)
        ax.bar_label(bars, labels=[f"{v:g}%" for v in values], padding=3)
        ax.set_ylim(0, limit)
        ax.set_title(title, fontsize=10)
        save(fig, "rxkid_" + name, indexed=True)

    fig, ax = plt.subplots(figsize=(4.5, 1.85), layout="constrained")
    ax.axis("off")
    grid = ax.table(cellText=[["A", "1.0", "2.0"], ["B", "2.0", "3.0"]],
                    colLabels=["Mixture", "M²⁺ (mmol/L)", "X⁻ (mmol/L)"],
                    loc="center", cellLoc="center")
    grid.auto_set_font_size(False)
    grid.set_fontsize(11)
    grid.scale(1, 1.6)
    ax.set_title("Initial free-ion concentrations")
    save(fig, "rxkid_mix", indexed=True)


def renal_pathology_and_inheritance():
    """Schematic tumor depth and simulated genotype/phenotype observations."""
    for name, depth, shoulder in [("bl1", 1.4, .95), ("bl2", 2.55, 1.55)]:
        fig, ax = plt.subplots(figsize=(5.3, 2.65), layout="constrained")
        ax.set(xlim=(0, 6), ylim=(3.55, -.65)); ax.axis("off")
        for top, bottom, color, label in [
            (0, .55, "#e6c2be", "Urothelium"),
            (.55, 1.65, "#f9dfbc", "Lamina propria"),
            (1.65, 3, "#dda6a5", "Detrusor muscle"),
            (3, 3.55, "#f5eed6", "Perivesical tissue"),
        ]:
            ax.axhspan(top, bottom, facecolor=color)
            ax.text(.18, (top+bottom)/2, label, va="center", fontsize=11)
        ax.axhline(3, ls=":", color="#474747", lw=1.7)
        ax.fill([3.0, 3.0, 3.25, 3.48, 3.65, 3.85, 4.05, 4.25, 4.45, 4.65,
                 4.65, 4.32, 4.16, 3.96, 3.75, 3.58, 3.30],
                [0, -.25, -.38, -.23, -.48, -.30, -.52, -.22, -.36, -.21,
                 .12, .38, shoulder, depth, shoulder, shoulder+.1, .34],
                color="#653d72", zorder=3)
        ax.text(5.0, -.23, "Tumor", color="#653d72", va="center", ha="center")
        save(fig, "nephrstudy_" + name, indexed=True)

    fig, ax = plt.subplots(figsize=(4.2, 1.85), layout="constrained")
    ax.axis("off")
    grid = ax.table(cellText=[["Rr", "36", "24"], ["rr", "0", "60"]],
                    colLabels=["Genotype", "Trait present", "Trait absent"], loc="center",
                    cellLoc="center")
    grid.auto_set_font_size(False); grid.set_fontsize(11); grid.scale(1, 1.7)
    ax.set_title("Adult offspring assessed at the same age")
    save(fig, "nephrstudy_cohort", indexed=True)


def renal_vascular_studies():
    """Renal arterial anatomy, two trial readouts and a simulated antibody response."""
    for name in ("beads", "plaque"):
        fig, ax = plt.subplots(figsize=(4.2, 2.2), layout="constrained")
        ax.set(xlim=(0, 5), ylim=(0, 2)); ax.axis("off")
        ax.fill_betweenx([0.12, 1.85], .33, .96, color="#dbebed")
        x = np.linspace(.8, 4.75, 240)
        radius = np.full_like(x, .22)
        if name == "beads":
            envelope = np.exp(-((x - 3.25) / .93) ** 4)
            radius += .105 * np.cos(8 * (x - 3.25)) * envelope
        ax.fill_between(x, 1-radius, 1+radius, color="#dbebed")
        ax.plot(x, 1-radius, color=COLORS[0], lw=2)
        ax.plot(x, 1+radius, color=COLORS[0], lw=2)
        ax.plot([.33, .33], [.12, 1.85], color=COLORS[0], lw=2)
        for lo, hi in [(.12, .78), (1.22, 1.85)]:
            ax.plot([.96, .96], [lo, hi], color=COLORS[0], lw=2)
        if name == "plaque":
            ax.fill([.88, .88, 1.03, 1.18, 1.45, 1.82, 1.35, .96],
                    [1.81, 1.08, .99, .94, 1.09, 1.22, 1.22, 1.22],
                    color=COLORS[1])
        ax.text(.33, .02, "Aorta", va="bottom", fontsize=10)
        ax.text(3.65, .42, "Renal artery", ha="center", fontsize=10)
        save(fig, "renalmap_" + name, indexed=True)

    for name, cross in [("main", (1.35, 2)), ("segment", (2.48, 2.75))]:
        fig, ax = plt.subplots(figsize=(3.6, 2.8), layout="constrained")
        ax.set(xlim=(0, 4.3), ylim=(.3, 3.65), aspect="equal"); ax.axis("off")
        ax.add_patch(plt.matplotlib.patches.Ellipse((2.95, 2), 2.1, 2.9,
                     facecolor="#edf4f5", edgecolor=COLORS[0], linewidth=1.5))
        ax.plot([.36, 2.1], [2, 2], color=COLORS[0], lw=4)
        for end in [.95, 2.0, 3.05]:
            ax.plot([2.1, 2.63, 3.38], [2, end, end], color=COLORS[0], lw=3)
        ax.plot(*cross, marker="x", markersize=12, markeredgewidth=3, color=COLORS[1])
        ax.text(.28, 1.52, "Inflow", fontsize=10)
        ax.text(.28, .45, "×   Site of occlusion", color=COLORS[1], fontsize=10)
        save(fig, "renalmap_" + name, indexed=True)

    fig, ax = axes("", "Patients with primary event (%)")
    bars = ax.bar(["Stent + medical", "Medical alone"], [35.1, 35.8], color=COLORS)
    ax.bar_label(bars, fmt="%.1f%%", padding=3); ax.set_ylim(0, 46)
    ax.set_title("CORAL composite outcome")
    save(fig, "renalmap_coral", indexed=True)

    fig, ax = plt.subplots(figsize=(4.3, 1.9), layout="constrained")
    ax.axis("off")
    table = ax.table(cellText=[["Prophylaxis", 39, 302], ["Placebo", 72, 305]],
                     colLabels=["Group", "With recurrence", "Assigned"], loc="center",
                     cellLoc="center", colWidths=[.32, .39, .26])
    table.auto_set_font_size(False); table.set_fontsize(10); table.scale(1, 1.65)
    ax.set_title("RIVUR: children with recurrent UTI")
    save(fig, "renalmap_rivur", indexed=True)

    fig, ax = axes("Study visit", "Median A-binding antibody (units/mL)")
    for values, label, style, color in [([3, 24, 18], "A booster", "-", COLORS[0]),
                                        ([3, 4, 3], "Other vaccine", "--", COLORS[1])]:
        ax.plot([0, 7, 28], values, marker="o", ls=style, color=color, lw=2, label=label)
    ax.set(xticks=[0, 7, 28], xticklabels=["Baseline", "Day 7", "Day 28"], ylim=(0, 28))
    ax.legend()
    save(fig, "renalmap_antibody", indexed=True)


def renal_filtration_and_obstruction():
    """Simulated traces and ureter diagrams used for paired localization questions."""
    hours = np.arange(25)
    for name, baseline, target in [("fall", 1, 2.5), ("recover", 3, 1)]:
        fig, ax = axes("Hours after change in filtration", "Serum creatinine (mg/dL)")
        evolving = target + (baseline - target) * np.exp(-hours / 12)
        steady = np.full(25, baseline)
        curves = (steady, evolving) if name == "fall" else (evolving, steady)
        for label, values, color, style in zip(("A", "B"), curves, COLORS, STYLES):
            ax.plot(hours, values, color=color, ls=style, lw=2.5, label="Curve " + label)
        ax.set(xlim=(0, 24), xticks=[0, 6, 12, 18, 24], ylim=(0.6, 3.5))
        ax.legend()
        save(fig, "renaltrend_" + name, indexed=True)

    for name, stone in [("distal", (2.15, 0.85)), ("proximal", (1.68, 3.3))]:
        fig, ax = plt.subplots(figsize=(3.8, 3.4), layout="constrained")
        ax.set(xlim=(0, 4), ylim=(0, 4.3), aspect="equal")
        ax.axis("off")
        ax.plot([0.5, 1, 1.55, 1.68], [3.9, 3.6, 3.55, 3.3], lw=3, color=COLORS[0])
        ax.plot([0.5, 1, 1.55], [3.2, 3.5, 3.55], lw=3, color=COLORS[0])
        ax.plot([1.68, 1.72, 1.9, 2.15], [3.3, 2.65, 1.85, 0.85], lw=3, color=COLORS[0])
        ax.add_patch(plt.matplotlib.patches.Ellipse((2.45, 0.65), 1.3, 0.55,
                     facecolor="none", edgecolor=COLORS[0], linewidth=2))
        ax.text(1.4, 3.98, "Collecting system", fontsize=11)
        ax.text(0.6, 2.0, "Ureter", fontsize=11)
        ax.text(2.45, 0.14, "Bladder", ha="center", fontsize=11)
        ax.scatter(*stone, s=95, color=COLORS[1], zorder=3)
        ax.annotate("Stone", xy=stone, xytext=(3.05, stone[1]+0.35),
                    arrowprops={"arrowstyle": "->"}, fontsize=11)
        save(fig, "renaltrend_" + name, indexed=True)


def respiratory_injury_studies():
    """Draw simulated clinical and behavioral records and the NoPAC trial estimate."""
    for name, sinus, ambient in (("squeeze", 110, 125), ("reverse", 120, 110)):
        study_table("airinj_" + name, "Sinus pressure at symptom onset",
                    ["Location", "Absolute pressure (kPa)"], [["Sinus", sinus], ["Ambient", ambient]])
    for name, flows in (("room", (2, 1, 0)), ("oxygen", (0, 2, 4))):
        study_table("airinj_" + name, "Observation after submersion",
                    ["Hour", "Nasal O₂ (L/min)", "SpO₂ (%)"],
                    [[str(i), str(flow), str(sat)] for i, flow, sat in zip((1, 3, 5), flows, (94, 96, 97))])
    study_table("airinj_nopaceffect", "Anterior packing at index ED visit",
                ["Comparison", "Odds ratio", "95% CI"],
                [["Topical TXA vs placebo", "1.107", "0.769–1.594"]], source="NoPAC")
    study_table("airinj_nopacrates", "Anterior packing after study treatment",
                ["Randomized arm", "Packed", "Participants"],
                [["Topical TXA", "111", "254"], ["Placebo", "100", "242"]], source="NoPAC")
    study_table("airinj_frame", "Mean score by test framing",
                ["Group", "Neutral", "Identity cue"], [["A", "76", "72"], ["B", "82", "78"]])
    fig, ax = axes("Respiratory phase", "Regional gas volume (arbitrary units)")
    ax.plot([0, 1], [90, 49], "o-", color=COLORS[0], lw=2, label="Left lung")
    ax.plot([0, 1], [94, 89], "s--", color=COLORS[1], lw=2, label="Right lung")
    ax.set(xticks=[0, 1], xticklabels=["End inspiration", "End expiration"],
           ylim=(35, 105), xlim=(-.15, 1.15), title="Paired lung volumes • simplified model")
    ax.legend(loc="lower left")
    save(fig, "airinj_trap", indexed=True)

    study_table("airinj_hot", "90-day mortality • lower vs higher target",
                ["Effect measure", "Estimate"], [["Adjusted risk ratio", "1.02"],
                ["95% confidence interval", "0.94–1.11"]], source="HOT-ICU")
    study_table("airinj_hotcounts", "90-day outcomes by oxygenation target",
                ["Target PaO₂", "Deaths", "Assessed"], [["60 mm Hg", "618", "1,441"],
                ["90 mm Hg", "613", "1,447"]], source="HOT-ICU")
    study_table("airinj_induction", "Atelectasis on one basal CT slice",
                ["O₂ at induction", "Mean area after induction and apnea"],
                [["60%", "0.3 cm²"], ["80%", "1.3 cm²"], ["100%", "9.8 cm²"]],
                source="Edmark et al.")
    fig, ax = plt.subplots(figsize=(5.5, 3), layout="constrained")
    for y, label, color in ((1.2, "A", COLORS[0]), (-.75, "B", COLORS[1])):
        ax.plot([1, 1.7, 4.4, 5], [0, y, y, 0], color=color, lw=3)
        ax.annotate("", (3.6, y), (2.7, y), arrowprops=dict(arrowstyle="->", lw=2))
        ax.text(2.25, y+.16, label, fontweight="bold")
    ax.plot([.2, 1], [0, 0], color="#555555", lw=2)
    ax.plot([5, 5.8], [0, 0], color="#555555", lw=2)
    ax.text(.12, -.24, "Pulmonary\nartery", ha="left", va="top")
    ax.text(5.98, -.24, "Pulmonary\nvein", ha="right", va="top")
    ax.text(3.2, 1.65, "Ventilated alveolus", ha="center")
    ax.annotate("", (3.2, 1.28), (3.2, 1.58), arrowprops=dict(arrowstyle="<->"))
    ax.set(xlim=(-.1, 6.15), ylim=(-1.3, 2.3), title="Two routes for pulmonary blood flow")
    ax.axis("off")
    save(fig, "airinj_bypass", indexed=True)


def main():
    MEDIA.mkdir(exist_ok=True)
    mcat_chemistry()
    cardiovascular()
    renal_studies()
    renal_anatomy()
    perinatal_studies()
    twin_fluid_studies()
    fetal_atrium_calipers()
    evidence_studies()
    evidence_reports()
    immune_reports()
    musculoskeletal_reports()
    musculoskeletal_studies()
    cutaneous_studies()
    behavioral_courses()
    urology_studies()
    preventive_care_studies()
    multisystem_physiology()
    multisystem_genetic_studies()
    clinical_nutrition_studies()
    multisystem_symptom_studies()
    safeguarding_and_emergency_studies()
    environmental_exposure_studies()
    systemic_inflammation_studies()
    multisystem_rheumatology_studies()
    systemic_infection_studies()
    clinical_otology_studies()
    visual_function_studies()
    eye_injury_and_experiment_studies()
    neuroinfection_studies()
    pleural_and_gas_exchange_studies()
    aspiration_courses()
    abdominal_emergency_studies()
    hepatobiliary_studies()
    postpartum_studies()
    gestational_exposure_studies()
    neonatal_and_mechanics_studies()
    nursery_studies()
    coagulation_studies()
    blood_cell_studies()
    splenic_studies()
    blood_drug_studies()
    hematologic_neoplasm_studies()
    hematologic_infection_studies()
    lymphoma_staging()
    communication_decision_records()
    medication_safety_records()
    social_psychology_studies()
    goals_of_care_records()
    quality_improvement_studies()
    coronary_ischemia_studies()
    electric_membrane_studies()
    ventricular_failure_studies()
    posterior_lead_study()
    atrial_and_ventricular_rhythm_studies()
    conduction_and_device_studies()
    wave_and_signaling_studies()
    rhythm_trial_results()
    valve_lesion_studies()
    atomic_measurement_studies()
    rheumatic_af_outcomes()
    acute_airway_records()
    upper_respiratory_records()
    organic_reasoning_studies()
    severe_cap_trial()
    pneumonia_distributions()
    diarrhea_timelines()
    gene_expression_records()
    gi_liver_studies()
    gi_localization_and_trial()
    gi_monitoring_records()
    liver_contrast_record()
    ovarian_cycle_record()
    gastrointestinal_trial_outcomes()
    skin_patch_record()
    skin_treatment_evidence()
    cognition_records()
    trial_interpretation_records()
    sensory_behavior_records()
    peripheral_nerve_records()
    obstetric_pressure_record()
    anorectal_fold_patterns()
    angiodysplasia_study()
    mcat_science_and_society_records()
    mcat_transfer_records()
    study_design_cases()
    airway_tumor_studies()
    shift_safety_studies()
    reproductive_infection_studies()
    cerebrovascular_studies()
    obstetric_complication_studies()
    vascular_flow_studies()
    prenatal_visit_studies()
    occupational_lung_studies()
    thermodynamics_outline_studies()
    kinetic_equilibrium_studies()
    cardiovascular_drug_studies()
    myocardial_and_bonding_studies()
    demographic_and_ulcer_studies()
    social_decision_tables()
    social_access_studies()
    reproductive_diagnosis_studies()
    membrane_recovery_records()
    consciousness_assessments()
    tumor_and_gene_evidence()
    pain_and_sensation()
    neuroendocrine_measurements()
    spine_and_separation_studies()
    abdominal_wall_and_equity_studies()
    congenital_and_identity_studies()
    motor_and_inheritance_studies()
    sleep_and_headache_studies()
    trauma_and_neural_signals()
    mood_course_and_arousal()
    immunodeficiency_and_learning()
    hiv_and_circuit_studies()
    immunotherapy_and_electricity()
    immune_reaction_and_fuel_studies()
    renal_inflammation_studies()
    urinary_trauma_and_filling()
    renal_medication_studies()
    renal_pathology_and_inheritance()
    renal_vascular_studies()
    renal_filtration_and_obstruction()
    respiratory_injury_studies()
    hypothesis_error_regions()
    agreement_figures()
    population_and_decision_figures()
    cardiovascular_studies()
    vascular_anatomy()
    ventricular_loops()
    rhythm_studies()
    respiratory()
    gastrointestinal()
    special_senses()
    neurologic_monitoring()
    hematology()
    quality_and_communication()
    reproductive()
    endocrine()
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
