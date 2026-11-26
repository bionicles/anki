"""Plot original teaching traces or selected windows of CTU-UHB recordings."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

MEDIA = Path(__file__).resolve().parent / "media"
# Record, start in minutes. Each recorded excerpt is ten minutes at native 4 Hz.
WINDOWS = [(1001, 0), (1002, 13), (1003, 44), (1004, 38), (1003, 9), (1007, 16), (1008, 0)]


def pulse(time, center, half_width):
    phase = np.clip((time - center) / half_width, -1, 1)
    return (1 + np.cos(np.pi * phase)) / 2


def save(fig, code):
    fig.savefig(MEDIA / f"med_ob_{code}.png", dpi=145, facecolor="white")
    plt.close(fig)


def strip(code, time, heart, uterine, label, maternal=None):
    fig, (top, bottom) = plt.subplots(2, 1, sharex=True, figsize=(7, 3.7),
                                      height_ratios=(2, 1), layout="constrained")
    top.set_title(label, loc="left", fontsize=11)
    top.plot(time, heart, lw=1, color="#18475a", label="Monitor channel")
    if maternal is not None:
        top.plot(time, maternal, "--", lw=1.2, color="#bc5b24", label="Maternal pulse")
        top.legend(loc="upper right", fontsize=8)
    top.set(ylabel="Rate (beats/min)", ylim=(50, 200), yticks=(60, 90, 120, 150, 180))
    bottom.plot(time, uterine, color="#68455b", lw=1)
    bottom.set(ylabel="Uterine activity\n(relative units)", xlabel="Elapsed time (min)")
    start, end = round(time[0]), round(time[-1])
    bottom.set(xlim=(start, end), xticks=np.arange(start, end + 1, 1 if end-start <= 10 else 5))
    for ax in (top, bottom):
        ax.grid(alpha=.23)
    save(fig, code)


def teaching():
    cases = ["baseline", "accel", "early", "late", "variable", "prolonged",
             "absent", "minimal", "frequent", "sinus", "brady", "pulse"]
    for seed, case in enumerate(cases):
        duration = 30 if case == "frequent" else 25 if case == "sinus" else 10
        t = np.arange(0, duration, 1/240)
        centers = (np.arange(.75, 30, 5/3) if case == "frequent" else
                   np.arange(1.7, duration - .65, 3))
        uterine = sum(45 * pulse(t, c, .72) for c in centers) + 8
        rng = np.random.default_rng(seed + 851)
        knots = np.arange(0, duration+.02, .04)
        amplitude = {"absent": 0, "minimal": 1.4}.get(case, 7)
        heart = (100 if case == "brady" else 140) + amplitude * np.interp(
            t, knots, rng.uniform(-1, 1, len(knots)))
        maternal = None
        if case in ("early", "late", "absent", "frequent"):
            delay = 0 if case == "early" else .55
            heart -= sum(36 * pulse(t, c+delay, .72) for c in centers)
        elif case == "variable":
            for c, shift, width, depth in zip(centers, [-.4,.12,.56], [.22,.31,.24], [38,56,45]):
                heart -= depth * pulse(t, c+shift, width)
        elif case == "accel":
            for c in (2.8, 7.6):
                heart += 28 * pulse(t, c, .40)
        elif case == "prolonged":
            heart -= 39 * np.interp(t, [0,3,3.35,5.7,6.15,10], [0,0,1,1,0,0])
        elif case == "sinus":
            heart = 140 + 11*np.sin(2*np.pi*3.5*t)
        elif case == "pulse":
            maternal = 87 + 5*np.sin(t*1.6) + np.cos(t*7)
            heart = np.where(t < 4.5, heart, maternal)
        strip(case, t, heart, uterine, "Simulated intrapartum monitor", maternal)
    for code, cm in [("labor_a", [4,6,6,6]), ("labor_b", [2,4,5,5])]:
        fig, ax = plt.subplots(figsize=(5.5, 3.1), layout="constrained")
        ax.plot([0,2,4,6], cm, ".-", color="#18475a", markersize=12)
        ax.set(xlabel="Hours since admission", ylabel="Cervical dilation (cm)",
               title="Serial examinations", ylim=(0,10), xticks=range(7))
        ax.grid(alpha=.25)
        save(fig, code)
    t = np.arange(0,10,1/240)
    pressure = 12 + sum(h*pulse(t,c,.6) for c,h in [(1,48),(3.2,58),(5.6,53),(8.2,63)])
    fig, ax = plt.subplots(figsize=(7, 2.8), layout="constrained")
    ax.plot(t, pressure, color="#68455b")
    for c,h in [(1,60),(3.2,70),(5.6,65),(8.2,75)]:
        ax.text(c,h+2,str(h),ha="center")
    ax.axhline(12, color="#888", ls="--")
    ax.set(xlabel="Elapsed time (min)", ylabel="Pressure (mm Hg)", title="Intrauterine pressure catheter",
           xlim=(0,10), ylim=(0,90), yticks=[0,12,30,50,70,90])
    save(fig,"internal")


def recorded(folder):
    import wfdb
    for record, start in WINDOWS:
        rec = wfdb.rdrecord(str(folder / str(record)), sampfrom=240*start, sampto=240*(start+10))
        assert rec.fs == 4 and rec.sig_name == ["FHR","UC"] and rec.units == ["bpm","nd"]
        heart, uterine = rec.p_signal.T.copy()
        heart[heart <= 0] = np.nan
        t = start + np.arange(len(heart)) / 240
        strip(f"r{record}_{start}", t, heart, uterine, "Recorded intrapartum monitor")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, help="Render the recorded windows from .hea/.dat pairs")
    args = parser.parse_args()
    if args.records:
        recorded(args.records)
    else:
        teaching()
