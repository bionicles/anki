"""Render eight-beat heart sound excerpts and four-beat visual keys from CirCor 1.0.3."""
import argparse
import csv
import hashlib
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly

ROOT = Path(__file__).resolve().parent


def render(records):
    with (ROOT / "heart-sounds.tsv").open() as f:
        manifest = list(csv.DictReader(f, delimiter="\t"))
    for row in manifest:
        record = records / row["Record"]
        wav, timings = record.with_suffix(".wav"), record.with_suffix(".tsv")
        for path, key in [(wav, "SourceSHA256"), (timings, "AnnotationSHA256")]:
            if hashlib.sha256(path.read_bytes()).hexdigest() != row[key]:
                raise ValueError(f"Unexpected {path.name} checksum")
        rate, samples = wavfile.read(wav)
        assert rate == 4000 and samples.ndim == 1
        start, end = float(row["Start"]), float(row["End"])
        signal = samples[round(start*rate):round(end*rate)].astype(float)
        audio = resample_poly(signal, 4, 1)
        audio *= 27000 / np.max(np.abs(audio))
        base = ROOT / "media" / row["Clip"]
        wavfile.write(base.with_suffix(".wav"), 4*rate, np.rint(audio).astype(np.int16))

        boundaries = np.loadtxt(timings)
        beats = boundaries[(boundaries[:, 0] >= start) & (boundaries[:, 1] <= end)]
        assert list(beats[:, 2]) == [1, 2, 3, 4]*8
        length = round((beats[15, 1] - start)*rate)
        fig, ax = plt.subplots(figsize=(7.0, 2.7), layout="constrained")
        segment = signal[:length]
        ax.plot(np.arange(length)/rate, segment / np.max(np.abs(segment)), lw=.65, color="#18475a")
        for begin, finish, phase in beats[:16]:
            if phase in (1, 3):
                ax.axvspan(begin-start, finish-start, color="#aac6d3", alpha=.35)
                ax.text((begin+finish)/2-start, 1.05, "S1" if phase==1 else "S2",
                        ha="center", fontsize=9)
        ax.set(xlabel="Time from first S1 (s)", ylabel="Relative amplitude",
               xlim=(0, length/rate), ylim=(-1.08,1.24))
        fig.savefig(base.with_suffix(".png"), dpi=145, facecolor="white")
        plt.close(fig)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("record_dir", type=Path)
    render(p.parse_args().record_dir)
