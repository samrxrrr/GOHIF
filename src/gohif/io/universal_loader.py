from pathlib import Path
import json
import gzip
import zipfile
import tarfile
import pandas as pd
import pdfplumber

class UniversalLoader:

    def load(self, path):

        path = Path(path)

        try:

            suffixes = [s.lower() for s in path.suffixes]

            if ".pdf" in suffixes:
                return self.load_pdf(path)

            elif ".csv" in suffixes:
                return self.load_csv(path)

            elif ".xlsx" in suffixes:
                return self.load_excel(path)

            elif ".json" in suffixes:
                return self.load_json(path)

            elif ".zip" in suffixes:
                return self.load_zip(path)

            elif ".gz" in suffixes:
                return self.load_gzip(path)

            elif ".tar" in suffixes or ".bz2" in suffixes:
                return self.load_tar(path)

            elif ".fa" in suffixes or ".fasta" in suffixes or ".txt" in suffixes:
                return self.load_text(path)

            return {"type":"unknown"}

        except Exception as e:

            return {
                "type":"error",
                "error":str(e),
                "file":str(path)
            }

    def load_pdf(self,path):
        with pdfplumber.open(path) as pdf:
            return {
                "type":"pdf",
                "pages":len(pdf.pages)
            }

    def load_csv(self,path):
        df=pd.read_csv(path,nrows=5)
        return {
            "type":"csv",
            "columns":len(df.columns)
        }

    def load_excel(self,path):
        xls=pd.ExcelFile(path)
        return {
            "type":"excel",
            "sheets":len(xls.sheet_names)
        }

    def load_json(self,path):
        with open(path) as f:
            obj=json.load(f)
        return {
            "type":"json",
            "python_type":type(obj).__name__
        }

    def load_zip(self,path):
        with zipfile.ZipFile(path) as z:
            return {
                "type":"zip",
                "members":len(z.namelist())
            }

    def load_gzip(self,path):
        with gzip.open(path,"rb") as f:
            f.read(1)
        return {"type":"gzip"}

    def load_tar(self,path):
        with tarfile.open(path) as tar:
            return {
                "type":"tar",
                "members":len(tar.getmembers())
            }

    def load_text(self,path):
        with open(path,errors="ignore") as f:
            text=f.read(1000)
        return {
            "type":"text",
            "characters":len(text)
        }

if __name__=="__main__":

    loader=UniversalLoader()

    samples=[
        "/mnt/g/My Drive/DATASETS/Animal/asf_situation_report_65.pdf",
        "/mnt/g/My Drive/DATASETS/Animal/aquapathogenx_template.zip",
        "/mnt/g/My Drive/DATASETS/Human/studies.json",
        "/mnt/g/My Drive/DATASETS/Animal/cattle_qtldb.txt"
    ]

    print("="*70)

    for s in samples:
        print(Path(s).name)
        print(loader.load(s))
        print()
