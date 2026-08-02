from pathlib import Path
import fitz
import json
import csv
from docx import Document
from openpyxl import load_workbook

class DocumentExtractor:

    def extract(self, path):

        path = Path(path)

        ext = path.suffix.lower()

        try:

            if ext == ".pdf":
                return self.pdf(path)

            elif ext in [".txt",".md",".log"]:
                return self.text(path)

            elif ext == ".json":
                return self.json(path)

            elif ext == ".csv":
                return self.csv(path)

            elif ext == ".docx":
                return self.docx(path)

            elif ext in [".xlsx",".xlsm"]:
                return self.xlsx(path)

            else:
                return {
                    "title": path.name,
                    "text": ""
                }

        except Exception as e:

            return {
                "title": path.name,
                "text": "",
                "error": str(e)
            }

    def pdf(self,path):

        doc=fitz.open(path)

        text=[]

        for page in doc:

            text.append(page.get_text())

        return {
            "title":path.stem,
            "pages":len(doc),
            "text":"\n".join(text)
        }

    def text(self,path):

        return {
            "title":path.stem,
            "text":path.read_text(errors="ignore")[:500000]
        }

    def json(self,path):

        obj=json.load(open(path,encoding="utf-8"))

        return {
            "title":path.stem,
            "text":json.dumps(obj,indent=2)[:500000]
        }

    def csv(self,path):

        rows=[]

        with open(path,newline="",errors="ignore") as f:

            reader=csv.reader(f)

            for i,row in enumerate(reader):

                rows.append(",".join(row))

                if i>300:
                    break

        return {
            "title":path.stem,
            "text":"\n".join(rows)
        }

    def docx(self,path):

        d=Document(path)

        return {
            "title":path.stem,
            "text":"\n".join(p.text for p in d.paragraphs)
        }

    def xlsx(self,path):

        wb=load_workbook(path,read_only=True)

        lines=[]

        for ws in wb.worksheets:

            lines.append(f"[Sheet] {ws.title}")

            for row in ws.iter_rows(values_only=True):

                lines.append(",".join("" if x is None else str(x) for x in row))

                if len(lines)>500:
                    break

        return {
            "title":path.stem,
            "text":"\n".join(lines)
        }


if __name__=="__main__":

    e=DocumentExtractor()

    for f in [
        "/mnt/g/My Drive/DATASETS/Human/studies.json",
        "/mnt/g/My Drive/DATASETS/Animal/cattle_qtldb.txt"
    ]:

        print("="*70)

        print(f)

        r=e.extract(f)

        print(r["title"])

        print(len(r["text"]))
