from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SOURCES = ROOT / "docs" / "MRD" / "sources"
OUTPUT = ROOT / "docs" / "MRD" / "Master_Research_Document.md"

OUTPUT.parent.mkdir(parents=True, exist_ok=True)


def build_document():

    chapter_files = sorted(
        SOURCES.glob("*.md"),
        key=lambda x: x.name
    )

    with open(OUTPUT, "w", encoding="utf-8") as out:

        out.write("# GOHIF Master Research Document\n\n")
        out.write("**Version:** 2.0\n")
        out.write("**Status:** Auto-generated\n\n")
        out.write("---\n\n")

        for chapter in chapter_files:

            out.write(chapter.read_text(encoding="utf-8"))

            out.write("\n\n")

    print(f"[OK] Generated {OUTPUT}")


if __name__ == "__main__":
    build_document()
