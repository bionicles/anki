"""Render four short windows of MIT-BIH sleep recordings from local WFDB records."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import wfdb

MEDIA = Path(__file__).resolve().parent / "media"
# Record, window start in seconds, and interval to inspect on the elapsed-time axis.
WINDOWS = [
    ("slp32", 5635, (26, 49)),
    ("slp37", 4980, (41, 62)),
    ("slp60", 2745, (8, 24)),
    ("slp59", 6465, (16, 58)),
]


def render(directory, name, start, interval):
    path = str(directory / name)
    fs = int(wfdb.rdheader(path).fs)
    record = wfdb.rdrecord(path, sampfrom=start * fs, sampto=(start + 75) * fs)
    effort = next(i for i, label in enumerate(record.sig_name)
                  if label in ("Resp (chest)", "Resp (abdomen)", "Resp (abdominal)"))
    indices = [record.sig_name.index("Resp (nasal)"), effort]
    signals = record.p_signal[:, indices].reshape(-1, 10, 2).mean(axis=1)
    time = (np.arange(len(signals)) * 10 + 4.5) / fs
    effort_label = "Chest" if "chest" in record.sig_name[effort] else "Abdominal"
    fig, axes = plt.subplots(2, 1, sharex=True, figsize=(7, 3.3), layout="constrained")
    for ax, signal, label in zip(axes, signals.T, ("Nasal airflow", effort_label + " effort")):
        ax.axvspan(*interval, color="#f8dfa0", alpha=.65)
        ax.plot(time, signal, color="#233d4a", lw=.9)
        ax.set(ylabel=label, yticks=[], xlim=(0, 75))
        ax.grid(axis="x", alpha=.22)
    axes[0].set_title("Overnight recording · each channel in relative units", fontsize=11, loc="left")
    axes[1].set(xlabel="Elapsed time (seconds)", xticks=np.arange(0, 76, 5))
    fig.savefig(MEDIA / f"med_sleep_{name}.webp", dpi=130, facecolor="white",
                pil_kwargs={"lossless": True, "method": 6})
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="directory containing the four .hea/.dat pairs")
    args = parser.parse_args()
    for window in WINDOWS:
        render(args.directory, *window)
