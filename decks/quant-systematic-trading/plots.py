"""Render original, synthetic market observations as offline figures for Anki."""
import csv
import json
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from worked_examples import worked_examples

ROOT = Path(__file__).resolve().parent
PALETTE = ["#145974", "#ad4b1b", "#28765f", "#70599b"]
MARKERS = ["o", "s", "^", "D"]
STYLES = ["-", "--", "-.", ":"]


def wrap(value, width):
    return textwrap.fill(str(value), width, break_long_words=False, break_on_hyphens=False)


def numbers(labels):
    try:
        return np.array([float(s.replace("−", "-")) for s in labels])
    except ValueError:
        return np.arange(len(labels), dtype=float)


def plain(value):
    return f"{value:.5g}"


def evidence(s):
    descriptions = []
    for row in s["series"]:
        pairs = ", ".join(f"{label}: {plain(v)}" for label, v in zip(s["labels"], row["values"]))
        descriptions.append(f"{row['label']} ({pairs})")
    return f"{s['title']}. {s['xlabel']}. {s['ylabel']}. " + "; ".join(descriptions) + "."


def draw(ax, s):
    kind = s["kind"]
    labels = s["labels"]
    series = s["series"]
    xs = np.arange(len(labels))
    values = np.array([r["values"] for r in series])
    if kind == "scatter":
        xs = numbers(labels)
        ax.scatter(xs, values[0], s=65, color=PALETTE[0], zorder=3)
        ax.axhline(0, color="#66777e", lw=.8)
        ax.axvline(0, color="#66777e", lw=.8)
        ax.margins(.14)
    elif kind == "window":
        for i, (start, end) in enumerate(zip(*values)):
            ax.hlines(i, start, end, color=PALETTE[i % len(PALETTE)], lw=4)
            ax.scatter([start, end], [i, i], color=PALETTE[i % len(PALETTE)], s=55)
        ax.set_yticks(xs, labels)
        ax.invert_yaxis()
        ax.set_xticks(range(int(values.min()), int(values.max()) + 1))
        ax.margins(x=.08, y=.25)
    elif kind == "matrix":
        # Distinct measurement units may share a table. The printed values, not a
        # cross-row color scale, carry meaning in those cases.
        if s["objective"] in {"idempotency", "drift", "neighbors", "attribution", "replay"}:
            shade = np.tile(np.arange(len(series))[:, None] % 2, (1, len(labels)))
            ax.imshow(shade, cmap="Blues", vmin=-2, vmax=7, aspect="auto")
        else:
            ax.imshow(values, cmap="Blues", alpha=.43, aspect="auto")
        for (i, j), v in np.ndenumerate(values):
            ax.text(j, i, plain(v), ha="center", va="center", fontsize=13, color="#102530")
        ax.set_yticks(range(len(series)), [wrap(r["label"], 15) for r in series])
        ax.set_xticks(xs, [wrap(l, 11) for l in labels])
    elif kind == "interval":
        ax.hlines(xs, values[0], values[1], color=PALETTE[0], linewidth=4)
        ax.scatter(values[0], xs, color=PALETTE[0], marker="|", s=180)
        ax.scatter(values[1], xs, color=PALETTE[0], marker="|", s=180)
        ax.axvline(0, ls="--", color="#66777e")
        ax.set(yticks=xs, yticklabels=labels, xlabel=s["ylabel"], ylabel=s["xlabel"])
        return
    elif kind == "riskreturn":
        for i, label in enumerate(labels):
            ax.scatter(values[0,i], values[1,i], s=70, color=PALETTE[i])
            ax.annotate(label, (values[0,i],values[1,i]), xytext=(6,4), textcoords="offset points")
        ax.margins(.3)
        ax.set(xlabel="Annual volatility (%)", ylabel="Expected annual return (%)")
        return
    elif kind == "state-tree":
        ax.set_axis_off()
        for y, state, stock, payoff in zip([.20,.80], labels, *values):
            ax.annotate("", (.55,y), (.22,.5), xycoords="axes fraction",
                        arrowprops={"arrowstyle":"->", "color":PALETTE[0], "lw":2})
            ax.text(.57,y,f"{state}\nStock  ${plain(stock)}\nCall  ${plain(payoff)}", transform=ax.transAxes,
                    va="center", fontsize=13)
        ax.text(.05,.5,"Today", va="center", transform=ax.transAxes, fontsize=13)
        return
    elif kind == "queue":
        left = 0
        for i, (name, size) in enumerate(zip(labels, values[0])):
            ax.barh(0, size, left=left, color=PALETTE[i], height=.4)
            ax.text(left+size/2,0,f"{name}\n{plain(size)}",ha="center",va="center",color="white",fontsize=10)
            left += size
        ax.set(yticks=[], xlabel="Shares from front of queue", xlim=(0,left), ylim=(-.5,.5))
        return
    elif kind == "line":
        xs = numbers(labels)
        for i, r in enumerate(series):
            ax.plot(xs, r["values"], color=PALETTE[i], ls=STYLES[i], marker=MARKERS[i],
                    label=r["label"], lw=2.3, ms=5)
        ax.set_xticks(xs, [wrap(l, 12) for l in labels])
        # Explicit readouts keep short numerical exercises accessible at phone size.
        if len(series)==1 and len(labels)<=6:
            for x, val in zip(xs, values[0]):
                ax.annotate(plain(val), (x,val), xytext=(0,7), textcoords="offset points",
                            ha="center", fontsize=9)
        ax.margins(x=.08,y=.24)
    elif kind == "bars":
        width=.73/len(series)
        for i, r in enumerate(series):
            offsets=xs+(i-(len(series)-1)/2)*width
            items=ax.bar(offsets,r["values"],width=width,color=PALETTE[i],label=r["label"],
                         hatch=["","//","..","xx"][i])
            ax.bar_label(items,labels=[plain(v) for v in r["values"]],padding=3,fontsize=9)
        ax.axhline(0,color="#647781",lw=.7)
        ax.set_xticks(xs, [wrap(l, 11) for l in labels])
        ax.margins(y=.25)
    else:
        raise ValueError(f"Unknown figure kind: {kind}")
    ax.set(xlabel=wrap(s["xlabel"],54), ylabel=wrap(s["ylabel"],36))
    if kind != "matrix":
        ax.grid(axis="y",alpha=.17)
        ax.set_axisbelow(True)
        if len(series)>1 and kind != "window":
            ax.legend(fontsize=9, framealpha=.85)


def save_chart(filename, title, painter):
    with plt.rc_context({"font.size":11,"axes.spines.right":False,"axes.spines.top":False}):
        fig, ax=plt.subplots(figsize=(5.6,3.8),layout="constrained")
        painter(ax)
        ax.set_title(wrap(title, 42), loc="left", fontsize=15, weight="bold", pad=12)
        fig.savefig(ROOT/"media"/filename,dpi=135,facecolor="white",
                    bbox_inches="tight",pad_inches=.13,metadata={"Software":"Systematic trading study figures"})
        plt.close(fig)


def main():
    charts=json.loads((ROOT/"figure-data.json").read_text())
    (ROOT/"media").mkdir(exist_ok=True)
    mappings=[]
    for slug, spec in charts.items():
        filename=f"qt_{slug}_observations.png"
        save_chart(filename,spec["title"],lambda ax: draw(ax,spec))
        uses = spec.get("cards", {f"QT-{slug}-1": "back", f"QT-{slug}-4": "front"})
        for card_id, side in uses.items():
            mappings.append([card_id, side, filename, evidence(spec)])
    for key, title, description, painter in worked_examples():
        filename="qt_"+key.removeprefix("QT-")+"_worked.png"
        save_chart(filename,title,painter)
        mappings.append([key,"back",filename,description])
    with (ROOT/"figures.tsv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f,delimiter="\t",lineterminator="\n")
        w.writerow(["CardID","Side","Filename","Description"])
        w.writerows(mappings)
    print(f"{len(set(r[2] for r in mappings))} figures on {len(mappings)} cards")


if __name__=="__main__":
    main()
