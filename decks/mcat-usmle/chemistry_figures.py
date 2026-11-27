"""Draw the original MCAT line structures from the SMILES in chemistry-figures.tsv."""
import csv
from io import BytesIO
from pathlib import Path

from PIL import Image
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

ROOT = Path(__file__).resolve().parent


def draw(filename, structures):
    molecules = [Chem.MolFromSmiles(s) for s in structures]
    if any(mol is None for mol in molecules):
        raise ValueError(f"Invalid structure in {filename}")
    panels = len(molecules)
    diagram = rdMolDraw2D.MolDraw2DCairo(320 * panels, 200, 320, 200)
    options = diagram.drawOptions()
    options.useBWAtomPalette()
    options.legendFontSize = 20
    options.fixedBondLength = 35
    labels = [chr(ord("A") + i) for i in range(panels)] if panels > 1 else []
    diagram.DrawMolecules(molecules, legends=labels)
    diagram.FinishDrawing()
    with Image.open(BytesIO(diagram.GetDrawingText())) as im:
        im.convert("RGB").save(ROOT / "media" / filename, lossless=True, method=6)


if __name__ == "__main__":
    with (ROOT / "chemistry-figures.tsv").open() as source:
        for row in csv.DictReader(source, delimiter="\t"):
            draw(row["File"], row["SMILES"].split(";"))
