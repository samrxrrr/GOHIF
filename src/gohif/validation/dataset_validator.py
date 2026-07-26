from pathlib import Path
import pandas as pd

ROOT = Path("/mnt/g/My Drive/DATASETS")
OUTPUT = Path("catalog/validated_catalog.csv")

IGNORED_NAMES = {
    "desktop.ini",
}

IGNORED_EXTENSIONS = {
    ".ini",
    ".sample",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".ico",
    ".tif",
}


def main():

    rows = []

    for file in ROOT.rglob("*"):

        if not file.is_file():
            continue

        if file.name in IGNORED_NAMES:
            continue

        if file.suffix.lower() in IGNORED_EXTENSIONS:
            continue

        try:

            stat = file.stat()

            rows.append(
                {
                    "domain": file.relative_to(ROOT).parts[0],
                    "relative_path": str(file.relative_to(ROOT)),
                    "filename": file.name,
                    "extension": file.suffix.lower(),
                    "size_bytes": stat.st_size,
                    "modified_time": stat.st_mtime,
                    "empty": stat.st_size == 0,
                }
            )

        except Exception as e:

            print(f"Skipped: {file}")
            print(e)

    df = pd.DataFrame(rows)

    df["duplicate"] = df.duplicated(
        subset=["filename", "size_bytes"],
        keep=False,
    )

    OUTPUT.parent.mkdir(exist_ok=True)

    df.to_csv(OUTPUT, index=False)

    print("\n==============================")
    print(" GOHIF DATASET VALIDATOR")
    print("==============================")

    print(f"Total files        : {len(df)}")
    print(f"Empty files        : {df['empty'].sum()}")
    print(f"Duplicate files    : {df['duplicate'].sum()}")

    print("\nFiles by domain:\n")
    print(df["domain"].value_counts())

    print("\nTop extensions:\n")
    print(df["extension"].value_counts().head(20))

    print(f"\nSaved to: {OUTPUT}")


if __name__ == "__main__":
    main()
