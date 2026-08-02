from pathlib import Path
import pdfplumber


class PDFExtractor:

    def extract(self, pdf_file):

        result = {

            "title": "",

            "text": "",

            "pages": 0,

            "tables": []

        }

        try:

            with pdfplumber.open(pdf_file) as pdf:

                result["pages"] = len(pdf.pages)

                texts = []

                for page in pdf.pages:

                    txt = page.extract_text()

                    if txt:

                        texts.append(txt)

                    try:

                        tables = page.extract_tables()

                        if tables:

                            result["tables"].extend(tables)

                    except Exception:
                        pass

                result["text"] = "\n".join(texts)

                if texts:

                    first = texts[0].splitlines()

                    if first:

                        result["title"] = first[0][:300]

        except Exception as e:

            result["error"] = str(e)

        return result
