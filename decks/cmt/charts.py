"""Render the additional CMT exercises as portable PNGs from original plotted observations."""
from pathlib import Path
from html import escape
from math import cos, sin, tau
import subprocess
import json

ROOT = Path(__file__).resolve().parent


def spectrogram_svg(panel):
    """Draw windowed Fourier power for selected periods in an original synthetic series."""
    window = 64
    hop = 32
    segments = panel["signal_periods"]
    values = []
    for period in segments:
        values.extend(sin(tau * t / period) for t in range(window))
    starts = range(0, len(values) - window + 1, hop)
    periods = [4, 8, 16, 32]
    taper = [0.5 - 0.5 * cos(tau * i / window) for i in range(window)]

    def power(start, period):
        sample = [v * w for v, w in zip(values[start:start + window], taper)]
        real = sum(v * cos(tau * i / period) for i, v in enumerate(sample))
        imag = sum(v * sin(tau * i / period) for i, v in enumerate(sample))
        return real * real + imag * imag

    rows = [[power(start, period) for start in starts] for period in periods]
    peak = max(max(row) for row in rows)
    left, top, width, height = 80, 45, 580 / len(starts), 32
    elements = ['<text x="18" y="20" font-size="16">Period (sessions) · selected frequency bins</text>']
    for j, row in enumerate(rows):
        y = top + j * height
        elements.append(f'<text x="{left-10}" y="{y+21}" text-anchor="end">{periods[j]}</text>')
        for i, value in enumerate(row):
            strength = round(100 * value / peak)
            light = 97 - 0.7 * strength
            x = left + i * width
            elements.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
                            f'fill="hsl(205,60%,{light}%)" stroke="white"/>')
            ink = "white" if strength >= 60 else "#23364a"
            elements.append(f'<text x="{x+width/2}" y="{y+21}" text-anchor="middle" '
                            f'font-size="14" fill="{ink}">{strength}</text>')
    for i, start in enumerate(starts):
        elements.append(f'<text x="{left+(i+0.5)*width}" y="193" text-anchor="middle">'
                        f'{start + window}</text>')
    elements.append('<text x="370" y="215" text-anchor="middle">Window end (session)</text>')
    elements.append('<text x="370" y="237" text-anchor="middle" font-size="13">'
                    'Power as % of plotted peak · darker = stronger</text>')
    return "".join(elements)


def panel_svg(p, top, height):
    if "signal_periods" in p:
        return spectrogram_svg(p)
    names = p["names"]
    series = p["series"]
    bars = p.get("bars", False)
    n = len(series[0])
    assert all(len(s) == n for s in series)
    labels = p.get("labels", [str(i + 1) for i in range(n)])
    assert len(labels) == n
    values = [v for s in series for v in s] + p.get("guides", [])
    lo, hi = p.get("limits", (min(values + ([0] if bars else [])), max(values)))
    if hi == lo:
        hi += 1
    h = height - 72
    left, width = 78, 590
    step = width / n
    def x(i):
        return left + (i + 0.5) * step
    def y(v):
        return top + 30 + (hi - v) * h / (hi - lo)
    def text(x, y, value, align="middle", size=14):
        return f'<text x="{x}" y="{y}" text-anchor="{align}" font-size="{size}">{escape(str(value))}</text>'
    def line(x1, y1, x2, y2, stroke, dash=""):
        return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{stroke}" stroke-dasharray="{dash}"/>'
    out = [text(12, top + 18, p["axis"], "start", 15)]
    for t in p.get("ticks", [lo, (lo + hi) / 2, hi]):
        out.extend([line(left, y(t), left + width, y(t), "#cbd5df", "4 4"), text(left-8, y(t)+4, f"{t:g}", "end")])
    colors = ["#195984", "#a04419", "#22745c"]
    for j, (name, ss) in enumerate(zip(names, series)):
        color = colors[j]
        if name:
            xx = left + width - 150 * (len(names) - j)
            out.extend([line(xx, top+13, xx+20, top+13, color, "5 3" if j else ""), text(xx+25, top+18, name, "start", 13)])
        if bars:
            assert len(series) == 1 and lo <= 0 <= hi
            for i, val in enumerate(ss):
                out.append(f'<rect x="{x(i)-step*.26}" y="{min(y(val),y(0))}" width="{step*.52}" height="{abs(y(val)-y(0))}" fill="{color}"/>')
        else:
            points = " ".join(f"{x(i)},{y(v)}" for i,v in enumerate(ss))
            dash = 'stroke-dasharray="8 4"' if j==1 else 'stroke-dasharray="2 4"' if j==2 else ''
            out.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3" {dash}/>')
            for i, v in enumerate(ss):
                out.append(f'<circle cx="{x(i)}" cy="{y(v)}" r="2.7" fill="{color}"/>')
    for v in p.get("guides",[]):
        out.append(line(left, y(v), left+width, y(v), "#443d53", "6 3"))
    for i,label in enumerate(labels):
        out.append(text(x(i),top+height-21,label))
    if p.get("x"):
        out.append(text(left+width/2,top+height-3,p["x"],size=13))
    return "".join(out)


def main():
    data = json.loads((ROOT / "chart-data.json").read_text())
    for number, panels in data.items():
        height = 195 if len(panels)>1 else 245
        size = height * len(panels)
        elements = "".join(panel_svg(p,i*height,height) for i,p in enumerate(panels))
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="686" height="{size}">'
               f'<rect width="100%" height="100%" fill="white"/>'
               f'<g font-family="DejaVu Sans,sans-serif" fill="#23364a">{elements}</g></svg>')
        subprocess.run(["rsvg-convert","-o",str(ROOT/"media"/f"cmt_study_{number}.png")],input=svg.encode(),check=True)


if __name__ == "__main__":
    main()
