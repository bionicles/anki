"""Embed a curated figure in the existing note fields, leaving note types intact."""
import csv
import html
from pathlib import Path

START = '<div class="study-figure">'
END = '</div>'


def read_figures(folder):
    with (folder/"figures.tsv").open(encoding="utf-8",newline="") as f:
        mapping={}
        for row in csv.DictReader(f,delimiter="\t"):
            key=row["CardID"]
            if key in mapping or row["Side"] not in {"front","back"}:
                raise ValueError(f"Invalid figure mapping for {key}")
            if Path(row["Filename"]).name!=row["Filename"] or not (folder/"media"/row["Filename"]).is_file():
                raise ValueError(f"Missing figure for {key}")
            if bool(row["Cue"]) != (row["Side"]=="front"):
                raise ValueError(f"Missing or misplaced visual question for {key}")
            mapping[key]=row
    return mapping


def apply_figure(fields, tags, figure):
    """Fields are already Anki HTML. Remove our old block when rebuilding an export."""
    for field in ("Question","Explanation"):
        fields[field]=fields[field].partition(START)[0]
    tag_list=[t for t in tags.split() if t not in ("medium::figure","visual::question","visual::worked")]
    if figure:
        front=figure["Side"]=="front"
        field="Question" if front else "Explanation"
        if front:
            fields[field]=html.escape(figure["Cue"],quote=False)
        alt=html.escape(figure["Description"],quote=True)
        filename=html.escape(figure["Filename"],quote=True)
        img=f'<img src="{filename}" alt="{alt}" style="max-width:100%;height:auto">'
        caption="" if front else f'<br><small>Illustrative example. {html.escape(figure["Description"],quote=False)}</small>'
        fields[field]+=START+img+caption+END
        tag_list.extend(["medium::figure","visual::question" if front else "visual::worked"])
    return " ".join(tag_list)
