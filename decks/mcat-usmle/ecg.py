"""Render selected six-second windows of MIT-BIH Arrhythmia Database v1.0.0."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import wfdb

# Each record's first channel is modified lead II. Windows start in seconds.
WINDOWS = [(100, 12), (119, 3), (119, 23), (228, 20), (202, 1186),
           (202, 1535), (231, 1211), (207, 43)]
MEDIA = Path(__file__).resolve().parent / "media"


def render(folder):
    for i, (record, start) in enumerate(WINDOWS, 1):
        header = wfdb.rdheader(str(folder / str(record)))
        rate = int(header.fs)
        data = wfdb.rdrecord(str(folder / str(record)), sampfrom=start * rate,
                             sampto=(start + 6) * rate, channels=[0])
        assert data.sig_name == ["MLII"] and data.units == ["mV"]
        voltage = data.p_signal[:, 0]
        time = np.arange(len(voltage)) / rate
        fig, ax = plt.subplots(figsize=(8.4, 2.5), layout="constrained")
        ax.set(xlabel="Time (s)", ylabel="MLII (mV)", xlim=(0, 6))
        ax.set_xticks(np.arange(0, 7))
        ax.set_xticks(np.arange(0, 6.01, .2), minor=True)
        ax.grid(axis="both", color="#cfacb3", lw=.6)
        ax.grid(which="minor", axis="x", color="#e5ccd1", lw=.5)
        ax.plot(time, voltage, color="#162b36", linewidth=1.1)
        fig.savefig(MEDIA / f"med_ecg_{i:02}.png", dpi=145, facecolor="white")
        plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path, help="Directory of PhysioNet .hea and .dat files")
    render(parser.parse_args().records)
