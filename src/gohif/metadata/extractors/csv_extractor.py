from pathlib import Path
import pandas as pd
import chardet

from gohif.metadata.extractors.generic_extractor import GenericExtractor


class CSVExtractor(GenericExtractor):

    def supports(self, path):
        return Path(path).suffix.lower() == ".csv"

    def detect_encoding(self, path):

        with open(path, "rb") as f:
            raw = f.read(100000)

        result = chardet.detect(raw)

        return result["encoding"] or "utf-8"

    def detect_delimiter(self, path, encoding):

        try:

            with open(path, "r", encoding=encoding) as f:

                line = f.readline()

            delimiters = [",", "\t", ";", "|"]

            counts = {d: line.count(d) for d in delimiters}

            return max(counts, key=counts.get)

        except Exception:

            return ","

    def extract(self, path):

        meta = super().extract(path)

        try:

            encoding = self.detect_encoding(path)

            delimiter = self.detect_delimiter(path, encoding)

            df = pd.read_csv(
                path,
                encoding=encoding,
                sep=delimiter,
                low_memory=False,
            )

            meta.update({

                "encoding": encoding,

                "delimiter": delimiter,

                "rows": int(df.shape[0]),

                "columns": int(df.shape[1]),

                "column_names": list(df.columns),

                "dtypes": {
                    c: str(df[c].dtype)
                    for c in df.columns
                },

                "missing_values": {
                    c: int(df[c].isna().sum())
                    for c in df.columns
                },

                "duplicate_rows": int(df.duplicated().sum()),

                "memory_mb": round(
                    df.memory_usage(deep=True).sum() / 1024 / 1024,
                    2,
                ),

                "sample": df.head(5).to_dict(orient="records"),
            })

        except Exception as e:

            meta["error"] = str(e)

        return meta
