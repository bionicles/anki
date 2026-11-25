"""Draw worked examples at review-card scale. Each panel carries its own data and units."""
from pathlib import Path
import csv
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

ROOT = Path(__file__).resolve().parent
COLORS = ("#176487", "#b64916", "#417346", "#753f88")
STYLES = ("-", "--", "-.", ":")
EXAMPLES = []


def add(cards, title, takeaway, *panels):
    """Attach one worked example to the listed cards; the first ID names its PNG."""
    EXAMPLES.append((cards.split(), title, takeaway, panels))


def matrix(title, values, xlabel="", ylabel=""):
    def draw(ax):
        data = np.asarray(values, dtype=float)
        limit = max(abs(data).max(), 1)
        ax.imshow(data, cmap="RdBu", vmin=-limit, vmax=limit)
        for (i, j), val in np.ndenumerate(data):
            ax.text(j, i, f"{val:.3g}", ha="center", va="center",
                    color="white" if abs(val) > .65*limit else "#152e3a", fontsize=13)
        ax.set(xticks=range(data.shape[1]), yticks=range(data.shape[0]),
               xlabel=xlabel, ylabel=ylabel)
    draw.description = "Matrix rows are " + str(np.asarray(values).tolist()) + "."
    return title, draw


def bars(title, labels, values, ylabel=""):
    def draw(ax):
        x = np.arange(len(labels))
        rects = ax.bar(x, values, color=[COLORS[i % len(COLORS)] for i in x], width=.62)
        ax.bar_label(rects, fmt="%.3g", fontsize=12, padding=2)
        ax.set_xticks(x, labels)
        ax.tick_params(axis="x", labelsize=10)
        ax.set_ylabel(ylabel)
        ax.margins(y=.22)
        ax.axhline(0, color="#737d85", lw=.7)
    return title, draw


def lines(title, x, series, xlabel, ylabel):
    def draw(ax):
        for i, (label, y) in enumerate(series):
            ax.plot(x, y, STYLES[i % 4], color=COLORS[i % 4], lw=2,
                    marker="o" if len(x) <= 10 else None, markersize=4, label=label)
        ax.set(xlabel=xlabel, ylabel=ylabel)
        ax.grid(alpha=.18)
        if len(series) > 1:
            ax.legend(fontsize=9)
    return title, draw


def arrows(title, segments):
    """Segments are (name, start, end). Use equal axis units for angles and lengths."""
    def draw(ax):
        points = np.array([p for _, a, b in segments for p in (a,b)] + [(0,0)])
        for i, (label,a,b) in enumerate(segments):
            ax.annotate("", b, a, arrowprops=dict(arrowstyle="-|>", color=COLORS[i % 4], linestyle=STYLES[i % 4], lw=2.2))
            ax.plot([], [], color=COLORS[i % 4], ls=STYLES[i % 4], label=label, lw=2)
        low, high = points.min(axis=0), points.max(axis=0)
        pad = max(max(high-low)*.15,.5)
        ax.set(xlim=(low[0]-pad,high[0]+pad), ylim=(low[1]-pad,high[1]+pad),
               xlabel="Coordinate 1", ylabel="Coordinate 2", aspect="equal")
        ax.axhline(0, lw=.7, color="grey")
        ax.axvline(0, lw=.7, color="grey")
        ax.legend(fontsize=9, loc="best")
    return title, draw


def transform(title, array):
    """Overlay the original unit square and the genuine linear image of its grid."""
    def draw(ax):
        a = np.asarray(array)
        square = np.array([[0,0],[1,0],[1,1],[0,1]])
        dst = square @ a.T
        ax.add_patch(Polygon(square, closed=True, fill=False, ls="--", lw=2,
                             edgecolor=COLORS[1], label="Unit square"))
        ax.add_patch(Polygon(dst, closed=True, facecolor="#67b2c5", alpha=.45,
                             edgecolor=COLORS[0], label="After map"))
        for t in np.linspace(0,1,5):
            for segment in ([[t,0],[t,1]], [[0,t],[1,t]]):
                mapped = np.array(segment) @ a.T
                ax.plot(*mapped.T, color=COLORS[0], lw=1)
        ax.autoscale_view()
        ax.margins(.25)
        ax.set(aspect="equal", xlabel="Coordinate 1", ylabel="Coordinate 2")
        ax.legend(fontsize=8)
    return title, draw


def flow(title, stages):
    """Draw a short chain; place longer explanations in the takeaway."""
    def draw(ax):
        ax.axis("off")
        ys = np.linspace(.86,.13,len(stages))
        for i,(y,label) in enumerate(zip(ys,stages)):
            ax.text(.5,y,textwrap.fill(label,33),ha="center",va="center",transform=ax.transAxes,
                    fontsize=13,bbox=dict(boxstyle="round,pad=.28",fc="#edf5f7",ec=COLORS[0]))
            if i:
                ax.annotate("",(.5,y+.095),(.5,ys[i-1]-.10),xycoords="axes fraction",
                            arrowprops=dict(arrowstyle="->",color=COLORS[1],lw=1.5))
    return title, draw


def scatter(title, groups, xlabel, ylabel):
    def draw(ax):
        for i,(name,x,y) in enumerate(groups):
            ax.scatter(x,y,color=COLORS[i%4],marker=("o","^","s","x")[i%4],label=name,s=30)
        ax.set(xlabel=xlabel,ylabel=ylabel)
        if len(groups)>1:
            ax.legend(fontsize=9)
        ax.grid(alpha=.18)
    return title, draw


def render():
    import math_foundations
    import model_math
    import applied_math
    import evaluation_math
    import math_extensions
    import primer_math
    for module in (math_foundations, model_math, applied_math, evaluation_math, math_extensions):
        module.register()
    render_set(EXAMPLES, "worked")
    EXAMPLES.clear()
    primer_math.register()
    render_set(EXAMPLES, "primer")


def render_set(examples, side):
    out = ROOT / "media"
    out.mkdir(exist_ok=True)
    mapped = set()
    with (ROOT/f"{side}-figures.tsv").open("w", newline="") as file:
        writer = csv.writer(file, delimiter="\t", lineterminator="\n")
        writer.writerow(["CardID","Filename","Description"])
        for keys,title,takeaway,panels in examples:
            filename = f"fml_{side}_{keys[0]}.png"
            # Stack panels. Two side-by-side matrices are hard to read on small screens.
            wrapped = textwrap.wrap(takeaway, 41)
            title_lines = textwrap.wrap(title, 33)
            heights = [.42*len(title_lines)] + [2.72]*len(panels) + [.25*len(wrapped)+.16]
            fig = plt.figure(figsize=(5.1, sum(heights)+.85*len(panels)+.48))
            axes = fig.subplots(len(heights), 1, gridspec_kw={"height_ratios": heights}, squeeze=False)[:,0]
            fig.subplots_adjust(left=.17, right=.94, top=.98, bottom=.025, hspace=.62)
            axes[0].axis("off")
            axes[0].text(-.12,.5,"\n".join(title_lines),va="center",weight="bold",fontsize=16,transform=axes[0].transAxes)
            for ax,(label,draw) in zip(axes[1:-1],panels):
                draw(ax)
                ax.set_title(textwrap.fill(label, 39), fontsize=12, loc="left", pad=5)
            axes[-1].axis("off")
            axes[-1].text(-.12,.5,"\n".join(wrapped),va="center",fontsize=14,transform=axes[-1].transAxes)
            fig.savefig(out/filename,dpi=120,facecolor="white",bbox_inches="tight",pad_inches=.14,metadata={"Software":"Frontier ML figures"})
            plt.close(fig)
            for key in keys:
                if key in mapped:
                    raise ValueError(f"duplicate worked figure for {key}")
                mapped.add(key)
                description = title + ". " + takeaway
                if side == "primer":
                    for _, draw in panels:
                        if hasattr(draw, "description"):
                            description += " " + draw.description
                writer.writerow(["FML-"+key, filename, description])


if __name__ == "__main__":
    # Let the lesson modules import these helpers from the running module.
    import sys
    sys.modules["visual_examples"] = sys.modules[__name__]
    render()
