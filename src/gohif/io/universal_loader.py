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

        elif ".fa" in suffixes or ".fasta" in suffixes:
            return self.load_text(path)

        elif ".txt" in suffixes:
            return self.load_text(path)

        else:
            return {
                "type":"unknown",
                "path":str(path)
            }

    def load_pdf(self,path):

        pages=0

        text=[]

        with pdfplumber.open(path) as pdf:

            pages=len(pdf.pages)

            for p in pdf.pages:

                t=p.extract_text()

                if t:
                    text.append(t)

        return {

            "type":"pdf",

            "pages":pages,

            "characters":len("\n".join(text))

        }

    def load_csv(self,path):

        df=pd.read_csv(path,nrows=5)

        return {

            "type":"csv",

            "rows_preview":len(df),

            "columns":list(df.columns)

        }

    def load_excel(self,path):

        xls=pd.ExcelFile(path)

        return {

            "type":"excel",

            "sheets":xls.sheet_names

        }

    def load_json(self,path):

        with open(path,encoding="utf-8") as f:

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

            f.read(100)

        return {

            "type":"gzip"

        }

    def load_tar(self,path):

        with tarfile.open(path) as tar:

            return {

                "type":"tar",

                "members":len(tar.getmembers())

            }

    def load_text(self,path):

        with open(path,errors="ignore") as f:

            txt=f.read(1000)

        return {

            "type":"text",

            "characters":len(txt)

        }


if __name__=="__main__":

    loader=UniversalLoader()

    samples=[

        "/mnt/g/My Drive/DATASETS/Animal/asf_situation_report_65.pdf",

        "/mnt/g/My Drive/DATASETS/Animal/cattle_qtldb.txt",

        "/mnt/g/My Drive/DATASETS/Human/studies.json",

        "/mnt/g/My Drive/DATASETS/Animal/aquapathogenx_template.zip",

    ]

    print("="*70)

    print("Universal Loader Test")

    print("="*70)

    for s in samples:

        try:

            print(Path(s).name)

            print(loader.load(s))

            print()

        except Exception as e:

            print(Path(s).name)

            print("ERROR:",e)

            print()
