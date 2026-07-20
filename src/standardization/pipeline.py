"""
GOHIF Universal Metadata Pipeline
Uses the dynamic parser registry.
"""

from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.standardization.parser_registry import (
    get_parser,
    supported_classes,
    parser_count,
)

def main():

    catalog = pd.read_csv(
        "metadata/schema/MASTER_FILE_CLASSIFICATION.csv"
    )

    records = []

    processed = 0
    skipped = 0
    failed = 0

    print("=" * 80)
    print("GOHIF UNIVERSAL STANDARDIZATION PIPELINE")
    print("=" * 80)
    print()

    print(f"Registered Parsers : {parser_count()}")
    print(f"Supported Classes  : {', '.join(supported_classes())}")
    print()

    for _, row in catalog.iterrows():

        parser = get_parser(row["File_Class"])

        if parser is None:
            skipped += 1
            continue

        path = Path("data/raw") / row["Relative_Path"]

        if not path.exists():
            print(f"[MISSING] {path}")
            failed += 1
            continue

        try:

            meta = parser.extract_metadata(path)

            meta["File_Class"] = row["File_Class"]
            meta["Relative_Path"] = row["Relative_Path"]

            records.append(meta)

            processed += 1

            print(f"[OK] {path.name}")

        except Exception as e:

            failed += 1

            print(f"[FAILED] {path.name}")
            print(e)

    df = pd.DataFrame(records)

    output = Path(
        "metadata/schema/MASTER_METADATA_CATALOG.csv"
    )

    output.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output, index=False)

    print()
    print("=" * 80)
    print("PIPELINE SUMMARY")
    print("=" * 80)

    print(f"Processed : {processed}")
    print(f"Skipped   : {skipped}")
    print(f"Failed    : {failed}")
    print()

    print(f"Rows : {len(df)}")
    print(f"Saved : {output}")
    print()

    if "File_Class" in df.columns:
        print(df["File_Class"].value_counts())

if __name__ == "__main__":
    main()
