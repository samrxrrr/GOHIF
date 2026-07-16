from pathlib import Path

def build(src_dir, outfile):
    src = Path(src_dir)

    files = sorted(src.glob("*.md"))

    with open(outfile, "w", encoding="utf-8") as out:

        out.write("<!-- GENERATED FILE -->\n")
        out.write("<!-- DO NOT EDIT DIRECTLY -->\n\n")

        for f in files:

            out.write("\n")
            out.write("="*80)
            out.write("\n\n")

            out.write(f.read_text(encoding="utf-8"))

            out.write("\n\n")

print("Building MRD...")
build(
    "docs/MRD/sections",
    "docs/MRD/master_research_document.md"
)

print("Building MDD...")
build(
    "docs/MDD/sections",
    "docs/MDD/master_development_document.md"
)

print()

print("Done.")
