from pathlib import Path

def build(source_dir, output_file, title):

    src = Path(source_dir)

    files = sorted(src.glob("*.md"))

    with open(output_file,"w",encoding="utf-8") as out:

        out.write("# " + title + "\n\n")
        out.write("> GENERATED FILE\n\n")
        out.write("> Do not edit directly.\n")
        out.write("> Edit chapter files instead.\n\n")
        out.write("---\n\n")

        for f in files:

            out.write(f"\n<!-- BEGIN {f.name} -->\n\n")

            out.write(f.read_text(encoding="utf-8"))

            out.write(f"\n\n<!-- END {f.name} -->\n\n")


build(
    "docs/MRD/chapters",
    "docs/MRD/master_research_document.md",
    "GOHIF Master Research Document"
)

build(
    "docs/MDD/chapters",
    "docs/MDD/master_development_document.md",
    "GOHIF Master Development Document"
)

print("MRD generated.")
print("MDD generated.")
