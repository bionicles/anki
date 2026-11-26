"""Render selected clinician-reviewed PTB-XL v1.0.3 waveforms in their original units."""
import argparse
import csv
import hashlib
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import wfdb


ROOT = Path(__file__).resolve().parent


def render(dataset):
    with (ROOT / "ptbxl.tsv").open() as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            record = dataset / row["Record"]
            for extension, key in [(".hea", "HeaderSHA256"), (".dat", "SignalSHA256")]:
                if hashlib.sha256(record.with_suffix(extension).read_bytes()).hexdigest() != row[key]:
                    raise ValueError(f"Unexpected {extension} checksum for {record.name}")
            header = wfdb.rdheader(str(record))
            leads = row["Leads"].split()
            start = round(float(row["StartSeconds"]) * header.fs)
            end = round(float(row["EndSeconds"]) * header.fs)
            sample = wfdb.rdrecord(str(record), sampfrom=start, sampto=end, channel_names=leads)
            if sample.sig_name != leads or sample.units != ["mV"] * len(leads):
                raise ValueError(f"Unexpected signal calibration for {record.name}")
            t = np.arange(sample.sig_len) / sample.fs
            fig, panels = plt.subplots(len(leads), 1, figsize=(6.9, 3.1), sharex=True,
                                       layout="constrained", squeeze=False)
            for index, ax in enumerate(panels[:, 0]):
                ax.plot(t, sample.p_signal[:, index], color="#154f64", lw=1.05)
                ax.set(ylabel=f"{leads[index]} (mV)", xlim=(0, len(t) / sample.fs))
                ax.grid(alpha=.25)
            panels[0, 0].set_title("Simultaneous ECG leads")
            panels[-1, 0].set_xlabel("Time from start of excerpt (s)")
            fig.savefig(ROOT / "media" / row["Figure"], dpi=135, facecolor="white")
            plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path, help="PTB-XL root containing records500/")
    render(parser.parse_args().dataset)
