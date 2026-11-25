"""Render the original illustrative data for the two finance decks."""
import argparse
import csv
from pathlib import Path
import runpy
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parent
COLORS = ["#135f76", "#aa461c", "#496e36", "#774a80"]
STYLES = ["-", "--", "-.", ":"]
COLUMNS = ["CardID", "Side", "Filename", "Description", "Cue"]


def curves(x, series, xlabel, ylabel):
    def draw(ax):
        for i, (label, values) in enumerate(series.items()):
            ax.plot(x, values, STYLES[i], color=COLORS[i], lw=2.6, label=label,
                    marker="o" if len(x) <= 15 else None, markersize=4)
        ax.set(xlabel=xlabel, ylabel=ylabel)
        if len(series) > 1:
            ax.legend(fontsize=8.5)
        if len(x) <= 10:
            ax.set_xticks(x)
    return draw


def trace(values, ylabel="Price ($)", xlabel="Session"):
    return curves(range(1, len(values)+1), {"Series": values}, xlabel, ylabel)


def bars(labels, values, ylabel):
    def draw(ax):
        positions = np.arange(len(values))
        items = ax.bar(positions, values, width=.6, color=COLORS[0])
        ax.set_xticks(positions, [textwrap.fill(str(s), 13) for s in labels], fontsize=9)
        ax.bar_label(items, fmt="%.4g", padding=3, fontsize=10)
        ax.axhline(0, color="#52636a", lw=.8)
        ax.margins(y=.25)
        ax.set_ylabel(ylabel)
    return draw


def points(xs, ys, xlabel, ylabel):
    def draw(ax):
        ax.scatter(xs, ys, s=55, color=COLORS[0])
        ax.set(xlabel=xlabel, ylabel=ylabel)
    return draw


def sessions(ohlc, ticks=False):
    def draw(ax):
        for i, (o,h,l,c) in enumerate(ohlc, 1):
            assert l <= min(o,c) <= max(o,c) <= h
            ax.vlines(i,l,h,color=COLORS[0],lw=2.3)
            if ticks:
                ax.hlines(o,i-.25,i,color=COLORS[0],lw=2.5)
                ax.hlines(c,i,i+.25,color=COLORS[0],lw=2.5)
            else:
                ax.add_patch(Rectangle((i-.21,min(o,c)),.42,abs(c-o),
                             facecolor="white" if c>=o else COLORS[0],edgecolor=COLORS[0],lw=2))
                if o==c: ax.hlines(o,i-.21,i+.21,color=COLORS[0],lw=2)
        ax.set(xticks=range(1,len(ohlc)+1),xlim=(.4,len(ohlc)+.6),xlabel="Session",ylabel="Price ($)")
        ax.margins(y=.15)
        if len(ohlc)==1:
            ax.set_yticks(sorted(set(ohlc[0])))
    return draw


def generate(deck):
    folder=ROOT/deck
    prefix={"cmt":"CMT-", "series-65":"S65-"}[deck]
    media=folder/"media"
    media.mkdir(exist_ok=True)
    rows={}
    def add(ids, title, description, draw, *, cue=None):
        keys=[prefix+k for k in ids.split()]
        name=prefix.lower().replace("-","")+"_fig_"+keys[0][len(prefix):].lower()+".png"
        with plt.rc_context({"font.size":11,"axes.spines.top":False,"axes.spines.right":False}):
            fig, ax=plt.subplots(figsize=(5.0,3.65),layout="constrained")
            ax.grid(axis="y",alpha=.18)
            ax.set_axisbelow(True)
            draw(ax)
            ax.set_title(textwrap.fill(title,40),fontsize=14,weight="bold",loc="left",pad=10)
            fig.savefig(media/name,dpi=140,facecolor="white",metadata={"Software":"Finance study figures"})
            plt.close(fig)
        for key in keys:
            if key in rows: raise ValueError("Duplicate figure for "+key)
            rows[key]=[key,"front" if cue else "back",name,description,cue or ""]
    lessons = runpy.run_path(str(folder/"figures.py"))
    lessons["register"](add)
    for filename, ids, description in lessons.get("WORKED_CHARTS", []):
        if not (media / filename).is_file():
            raise ValueError("Missing source chart: " + filename)
        for short_id in ids.split():
            key = prefix + short_id
            if key in rows:
                raise ValueError("Duplicate figure for " + key)
            rows[key] = [key, "back", filename, description, ""]
    with (folder/"figures.tsv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f,delimiter="\t",lineterminator="\n"); w.writerow(COLUMNS); w.writerows(rows.values())


if __name__=="__main__":
    sys.modules["finance_figures"]=sys.modules[__name__]
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck",choices=["cmt","series-65"])
    generate(parser.parse_args().deck)
