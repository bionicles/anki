"""Build or verify this curriculum with the repository's exam bundle workflow."""
import argparse
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT.parents[1] / 'deck-builder' / 'scripts'))
import build_exam
import genanki

# A distinct model keeps code indentation readable without changing other exam decks.
build_exam.MODEL = genanki.Model(
    1740198326, "Frontier ML · worked recall v1",
    fields=[{"name": name} for name in build_exam.FIELDS],
    templates=[{
        "name": "Retrieve",
        "qfmt": '<main><div class="cue">{{Question}}</div></main>',
        "afmt": '{{FrontSide}}<main><hr id="answer"><div class="response">{{Answer}}</div>'
                '{{#Explanation}}<p class="why">{{Explanation}}</p>{{/Explanation}}'
                '<footer>{{Source}}</footer></main>',
    }],
    css='''.card {font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        font-size: 20px; line-height: 1.5; text-align: left; padding: 12px;}
        main {max-width: 42rem; margin: 0 auto;}
        #answer {margin: 1rem 0; border: 0; border-top: 1px solid #888;}
        .response {white-space: pre-wrap; overflow-wrap: anywhere;}
        .why {font-size: .92em;}
        footer {margin-top: 1.3rem; font-size: .72em; opacity: .8; overflow-wrap: anywhere;}''',
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["build", "verify"])
    parser.add_argument("directory", type=Path, help="release directory, relative to the current directory")
    args = parser.parse_args()
    args.cards = PROJECT / "cards.tsv"
    args.components = PROJECT / "components.csv"
    args.namespace = "Frontier-ML"
    args.deck = "Frontier ML — Research and Engineering"
    def load_figures(name):
        rows = build_exam.table(PROJECT / name, ["CardID", "Filename", "Description"], "\t")
        figures = {r["CardID"]: (PROJECT / "media" / r["Filename"], r["Description"]) for r in rows}
        if len(figures) != len(rows):
            raise ValueError(f"duplicate card ID in {name}")
        return figures

    figures = load_figures("figure-cards.tsv")
    primer = load_figures("primer-figures.tsv")
    if figures.keys() & primer.keys():
        raise ValueError("a prompt has two competing front figures")
    figures.update(primer)
    worked = load_figures("worked-figures.tsv")
    if args.action == "build":
        args.output = args.directory
        args.coverage = args.components
        build_exam.publish(args, figures, worked)
    else:
        import verify_exam
        args.release = args.directory
        args.latest = False
        verify_exam.verify(args, figures, worked)


if __name__ == "__main__":
    main()
