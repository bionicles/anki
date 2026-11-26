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
