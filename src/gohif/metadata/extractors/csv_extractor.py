import pandas as pd
from src.gohif.metadata.extractors.generic_extractor import GenericExtractor

class CSVExtractor(GenericExtractor):

    def supports(self, path):
        return path.lower().endswith(".csv")

    def extract(self, path):

        meta = super().extract(path)

        try:

            df = pd.read_csv(path, nrows=5)

            meta.update({

                "rows": None,

                "columns": len(df.columns),

                "headers": list(df.columns)

            })

        except Exception as e:

            meta["error"] = str(e)

        return meta
