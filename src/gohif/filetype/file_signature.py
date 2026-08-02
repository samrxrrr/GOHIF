from pathlib import Path

SIGNATURES = {
    b"%PDF": "PDF",
    b"PK\x03\x04": "ZIP",
    b"\x1f\x8b": "GZIP",
    b"BZh": "BZIP2",
    b"SQLite format 3": "SQLITE",
    b"{": "JSON",
    b"[": "JSON",
    b"<!DOCTYPE": "HTML",
    b"<html": "HTML",
    b"<?xml": "XML",
}

def detect_file_type(path):

    path = Path(path)

    with open(path, "rb") as f:
        header = f.read(64)

    for sig, name in SIGNATURES.items():

        if header.startswith(sig):
            return name

    return "UNKNOWN"


if __name__ == "__main__":

    samples = [

        "/mnt/g/My Drive/DATASETS/Animal/asf_situation_report_65.pdf",

        "/mnt/g/My Drive/DATASETS/Animal/aquapathogenx_template.zip",

        "/mnt/g/My Drive/DATASETS/Human/studies.json",

        "/mnt/g/My Drive/DATASETS/Animal/cattle_qtldb.txt"

    ]

    print("=" * 70)
    print("GOHIF File Signature Detector")
    print("=" * 70)

    for s in samples:

        print(Path(s).name)

        print(detect_file_type(s))

        print()
