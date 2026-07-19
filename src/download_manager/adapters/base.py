from pathlib import Path
from datetime import datetime
import hashlib
import logging


class BaseAdapter:

    def __init__(self):

        self.root = Path("datasets/raw")
        self.root.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def timestamp():
        return datetime.now().isoformat(timespec="seconds")

    @staticmethod
    def sha256(filepath):

        h = hashlib.sha256()

        with open(filepath, "rb") as f:

            while True:

                chunk = f.read(1024 * 1024)

                if not chunk:
                    break

                h.update(chunk)

        return h.hexdigest()

    @staticmethod
    def filesize(filepath):

        return Path(filepath).stat().st_size

    def dataset_directory(self, row):

        domain = str(row.get("Domain", "misc")).strip()

        domain = (
            domain.lower()
                  .replace("&", "and")
                  .replace("/", "_")
                  .replace(" ", "_")
        )

        folder = self.root / domain

        folder.mkdir(parents=True, exist_ok=True)

        return folder

    def result(
        self,
        success,
        row,
        filepath=None,
        message=""
    ):

        record = {

            "GOHIF_ID": row["GOHIF_ID"],

            "Dataset_Name": row["Dataset_Name"],

            "Timestamp": self.timestamp(),

            "Success": success,

            "Message": message,

            "Local_Path": "",

            "File_Size": "",

            "SHA256": ""

        }

        if filepath is not None and Path(filepath).exists():

            record["Local_Path"] = str(filepath)

            record["File_Size"] = self.filesize(filepath)

            record["SHA256"] = self.sha256(filepath)

        return record
