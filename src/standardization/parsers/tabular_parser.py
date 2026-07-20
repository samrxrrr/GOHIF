"""
GOHIF Tabular Parser
Supports TSV and CSV files.
"""

from pathlib import Path
import pandas as pd

from src.standardization.base_parser import BaseParser


class TabularParser(BaseParser):

    def detect(self, path):
        return Path(path).suffix.lower() in [".tsv", ".csv"]

    def extract_metadata(self, path):
        path = Path(path)

        sep = "\t" if path.suffix.lower() == ".tsv" else ","

        df = pd.read_csv(path, sep=sep, low_memory=False)

        return {
            "Filename": path.name,
            "Rows": len(df),
            "Columns": len(df.columns),
            "Column_Names": list(df.columns),
            "File_Size_MB": round(path.stat().st_size / 1024 / 1024, 3),
            "SHA256": self.sha256(path)
        }

    def validate(self, path):
        try:
            self.extract_metadata(path)
            return True
        except Exception:
            return False

    def standardize(self, path, output_dir):
        path = Path(path)

        sep = "\t" if path.suffix.lower() == ".tsv" else ","

        df = pd.read_csv(path, sep=sep, low_memory=False)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        out = output_dir / (path.stem + ".csv")

        df.to_csv(out, index=False)

        return out

    def summarize(self, path):
        return self.extract_metadata(path)
