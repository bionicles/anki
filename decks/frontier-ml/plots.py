"""Render the original math figures. Run with Matplotlib and NumPy; see the Justfile."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
BLUE, ORANGE, GREY = "#165a91", "#b54d16", "#576579"
plt.rcParams.update({"font.size": 13, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.labelcolor": "#263546", "lines.linewidth": 2.5, "legend.fontsize": 10})


def vector(ax, x, y):
    ax.annotate("", xy=(x, y), xytext=(0, 0),
                arrowprops={"arrowstyle": "-|>", "color": BLUE, "lw": 3})
    ax.plot(x, y, "o", color=BLUE)
    ax.set(xlim=(-0.25, 4.5), ylim=(-0.25, 4.8), aspect="equal", xlabel="x₁", ylabel="x₂")
    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.grid(alpha=.22)


def projection(ax):
    vector(ax, 3, 4)
    ax.axhline(0, color=ORANGE, label="target subspace")
    ax.plot([3, 3], [0, 4], "--", color=GREY)
    ax.legend(loc="upper left")


def singular_values(ax):
    ax.bar([1, 2, 3], [5, 3, 1], color=BLUE, width=.55)
    ax.set(xticks=[1, 2, 3], yticks=range(6), xlabel="Component", ylabel="Singular value")


def pca_labels(ax):
    x = np.linspace(-4, 4, 13)
    for sign, label, marker, color in [(1, "Class A", "o", BLUE), (-1, "Class B", "^", ORANGE)]:
        ax.scatter(x, sign * (.4 + .09 * np.cos(2*x)), label=label, marker=marker, color=color)
    ax.set(xlabel="Feature 1", ylabel="Feature 2", ylim=(-1.3, 1.3), aspect="equal")
    ax.legend(ncol=2, loc="upper center")


def curvature(ax):
    x, y = np.meshgrid(np.linspace(-3, 3, 210), np.linspace(-1.8, 1.8, 125))
    loss = (x*x + 8*y*y) / 2
    ax.contour(x, y, loss, levels=[.5, 1, 2, 3, 5, 8, 12], colors="#9cb2bf", linewidths=1)
    path = [np.array([2.8, 1.45])]
    for _ in range(11):
        path.append(path[-1] - .21 * np.array([1, 8])*path[-1])
    xy = np.array(path)
    ax.plot(xy[:, 0], xy[:, 1], "o-", ms=4, color=ORANGE)
    ax.set(xlabel="Parameter 1", ylabel="Parameter 2", aspect="equal")


def roc(ax):
    # Each vertex is an attainable operating point. The zero-FPR point is shared.
    fpr = [0, .01, .02, .04, .08, .15]
    ax.step(fpr, [0, .30, .45, .66, .80, .90], where="post", label="Detector A", color=BLUE)
    ax.step(fpr, [0, .43, .54, .62, .70, .78], where="post", label="Detector B", color=ORANGE, ls="--")
    ax.axvline(.02, color=GREY, ls=":", label="Allowed FPR")
    ax.set(xlabel="False-positive rate", ylabel="Recall", xlim=(0, .15), ylim=(0, 1))
    ax.set_xticks([0, .02, .05, .10, .15])
    ax.legend(loc="lower right")


def precision_recall(ax):
    labels = np.array([1, 1, 0, 1, 0, 0, 1, 0, 0, 0])
    cut = np.arange(1, len(labels)+1)
    found = np.cumsum(labels)
    recall, precision = found/labels.sum(), found/cut
    ax.plot(recall, precision, ".-", color=BLUE)
    for k in (4, 6):
        ax.plot(recall[k-1], precision[k-1], "o", color=ORANGE)
        ax.annotate(f"top {k}", (recall[k-1], precision[k-1]), xytext=(8, 7 if k == 4 else -13), textcoords="offset points")
    ax.set(xlabel="Recall", ylabel="Precision", xlim=(0, 1.1), ylim=(.28, 1.08))
    ax.set_xticks([0, .25, .5, .75, 1])
    ax.grid(alpha=.2)


def reliability(ax):
    p = np.array([.25, .50, .75])
    ax.plot([0, 1], [0, 1], ":", color=GREY, label="Perfect calibration")
    ax.plot(p, p + .12, "o-", color=BLUE, label="Group A")
    ax.plot(p, p - .12, "^--", color=ORANGE, label="Group B")
    ax.set(xlabel="Predicted probability", ylabel="Observed frequency", xlim=(0, 1), ylim=(0, 1))
    ax.legend(loc="upper left")


def clipping(ax):
    vector(ax, 3, 4)
    ax.add_patch(plt.Circle((0, 0), 2, fill=False, ls="--", color=ORANGE, lw=2))
    ax.text(.25, 2.15, "norm limit = 2", color=ORANGE)


def causal_attention(ax):
    weights = np.array([[1,0,0,0],[.2,.8,0,0],[.1,.2,.45,.25],[.1,.2,.3,.4]])
    ax.imshow(weights, cmap="Blues", vmin=0, vmax=1)
    for (i, j), value in np.ndenumerate(weights):
        ax.text(j, i, f"{value:g}", ha="center", va="center", color="white" if value>.55 else "#182d46")
    ax.set(xticks=range(4), yticks=range(4), xlabel="Key position", ylabel="Query position")


def nucleus(ax):
    probs = [.55, .25, .15, .05]
    ax.bar(list("ABCD"), probs, width=.6, color=BLUE)
    ax.bar_label(ax.containers[0], fmt="%.2f")
    ax.set(xlabel="Token in descending probability order", ylabel="Probability", ylim=(0, .68))


def roofline(ax):
    intensity = np.linspace(0, 160, 321)
    ax.plot(intensity, np.minimum(200, 2*intensity), color=BLUE)
    ax.set(xlabel="Arithmetic intensity (FLOP/byte)", ylabel="Bound (TFLOP/s)", ylim=(0, 230))
    ax.set_xticks([0, 25, 50, 75, 100, 125, 150])
    ax.grid(alpha=.2)


def saddle(ax):
    t = np.linspace(-2, 2, 121)
    ax.plot(t, t*t, color=BLUE, label="Direction A")
    ax.plot(t, -t*t, "--", color=ORANGE, label="Direction B")
    ax.axhline(0, lw=1, color=GREY)
    ax.set(xlabel="Step from stationary point", ylabel="Change in loss")
    ax.legend()


def robust_loss(ax):
    x = np.linspace(-2, 10, 241)
    residual = x[:, None] - np.array([0, 0, 9])
    for axnum, (values, label) in enumerate([(np.mean(residual**2, axis=1), "Squared"),
                                             (np.mean(abs(residual), axis=1), "Absolute")]):
        # Normalize the height of each curve so the distinct minima are legible.
        norm = (values - values.min()) / np.ptp(values)
        ax.plot(x, norm, ["-", "--"][axnum], color=[BLUE, ORANGE][axnum], label=label)
    ax.set(xlabel="Constant prediction", ylabel="Loss (rescaled per curve)", xticks=[-2, 0, 3, 6, 9])
    ax.legend()


def support(ax):
    x = np.arange(4)
    ax.bar(x-.18, [.25,.5,.25,0], width=.36, color=BLUE, label="Training")
    ax.bar(x+.18, [.15,.25,.30,.30], width=.36, color=ORANGE, label="Deployment", hatch="//")
    ax.set(xticks=x, xticklabels=list("ABCD"), xlabel="Input region", ylabel="Probability mass", ylim=(0,.65))
    ax.legend()


def comparisons(ax):
    xy = np.array([[0,0],[1,1],[2,0],[3.5,0],[4.5,1],[5.5,0]])
    for start, end in [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3)]:
        ax.plot(*xy[[start,end]].T, color=GREY, lw=2)
    ax.scatter(*xy.T, s=480, color=BLUE, zorder=3)
    for name, (x,y) in zip("ABCDEF", xy):
        ax.text(x,y,name,color="white",ha="center",va="center",zorder=4)
    ax.set(xlim=(-.6,6.1),ylim=(-.6,1.6),aspect="equal")
    ax.axis("off")


def standard_error(ax):
    n = np.arange(1, 101)
    ax.plot(n, 1/np.sqrt(n), color=BLUE)
    ax.plot(16, .25, "o", color=ORANGE)
    ax.set(xlabel="Independent samples", ylabel="Standard error (σ = 1)", xlim=(0, 100), ylim=(0,.6))
    ax.set_xticks([0,16,32,48,64,80,96])
    ax.set_yticks([0,.125,.25,.375,.5])
    ax.grid(alpha=.22)


def radial_kernel(ax):
    d = np.linspace(0, 3, 151)
    for gamma, label, color, style in [(.5, "A", BLUE, "-"), (2, "B", ORANGE, "--")]:
        ax.plot(d, np.exp(-gamma*d*d), style, color=color, label=f"Kernel {label}")
    ax.set(xlabel="Distance from training point", ylabel="Similarity")
    ax.legend()


def rotations(ax):
    angle = np.linspace(0, 2*np.pi, 181)
    ax.plot(np.cos(angle), np.sin(angle), lw=1, color="#b9c2c9")
    for deg, name, color, style in [(0, "q", BLUE, "-"), (60, "k", ORANGE, "-"),
                                    (90, "q′", BLUE, "--"), (150, "k′", ORANGE, "--")]:
        x, y = np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg))
        ax.plot([0,x], [0,y], style, color=color)
        ax.text(1.12*x, 1.12*y, name, ha="center", va="center", color=color)
    ax.set(xlim=(-1.35,1.35), ylim=(-1.2,1.27), aspect="equal", xlabel="Feature 1", ylabel="Feature 2")


def diffusion(ax):
    x = np.linspace(0, 2*np.pi, 75)
    clean = np.sin(x)
    noise = np.random.default_rng(15).normal(size=len(x))
    alpha_bar = .64
    noisy = np.sqrt(alpha_bar)*clean + np.sqrt(1-alpha_bar)*noise
    ax.plot(x, clean, color=BLUE, label="Clean training example")
    ax.plot(x, noisy, color=ORANGE, lw=1.4, label="Corrupted input")
    ax.set(xlabel="Signal coordinate", ylabel="Amplitude")
    ax.legend()


def compute_budget(ax):
    params = np.geomspace(.5, 8, 140)
    ax.plot(params, 40/params, color=BLUE)
    ax.scatter([2,4],[20,10],color=ORANGE)
    ax.set(xscale="log", yscale="log", xlabel="Parameters (billions)", ylabel="Training tokens (billions)")
    ax.set_xticks([.5,1,2,4,8], labels=["0.5","1","2","4","8"])
    ax.set_yticks([5,10,20,40,80], labels=["5","10","20","40","80"])
    ax.grid(alpha=.2)


def bellman(ax):
    ax.text(.06,.5,"current\nstate", ha="center", va="center", transform=ax.transAxes)
    ax.annotate("next state", (.55,.5), xycoords="axes fraction", ha="center", va="center")
    ax.annotate("", (.43,.5), (.16,.5), xycoords="axes fraction", arrowprops={"arrowstyle":"->","lw":2})
    ax.text(.30,.57,"reward +1", ha="center", transform=ax.transAxes)
    for y, label in [(.78,"Q(a) = 4"),(.22,"Q(b) = 2")]:
        ax.annotate("", (.86,y), (.67,.5), xycoords="axes fraction", arrowprops={"arrowstyle":"->","lw":2,"color":BLUE})
        ax.text(.88,y,label,transform=ax.transAxes,ha="center",va="bottom" if y>.5 else "top")
    ax.axis("off")


def frontier(ax):
    for name, cost, quality in [("A",2,.78),("B",4,.85),("C",5,.80)]:
        ax.scatter(cost,quality,color=BLUE,s=75)
        ax.annotate(name,(cost,quality),xytext=(7,3),textcoords="offset points")
    ax.set(xlim=(1,6),ylim=(.74,.9),xlabel="Cost per request (milli-dollars)",ylabel="Quality score")
    ax.grid(alpha=.2)


PLOTS = {
    "geometry-2":projection, "svd-2":singular_values, "pca-4":pca_labels,
    "curvature-3":curvature, "roc-3":roc, "imbalance-2":precision_recall,
    "calibration-4":reliability, "lr-2":clipping, "attention-4":causal_attention,
    "sampling-2":nucleus, "roof-2":roofline, "nonconvex-1":saddle,
    "robustloss-3":robust_loss, "shift-3":support, "bradley-1":comparisons,
    "variance-2":standard_error, "kernel-3":radial_kernel,
    "position-2":rotations, "diffusion-1":diffusion, "scaling-2":compute_budget,
    "bellman-2":bellman, "launch-atom7":frontier,
}

if __name__ == "__main__":
    out = HERE / "media"
    out.mkdir(exist_ok=True)
    for key, plot in PLOTS.items():
        fig, ax = plt.subplots(figsize=(5.2, 3.3), layout="constrained")
        plot(ax)
        fig.savefig(out / f"fml_{key}.png", dpi=155, facecolor="white",
                    metadata={"Software": "Frontier ML figures"})
        plt.close(fig)
