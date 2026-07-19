"""
GOHIF Manifest Manager
"""

from pathlib import Path
from datetime import datetime

import pandas as pd


class ManifestManager:

    def __init__(self, manifest_path):

        self.manifest_path = Path(manifest_path)

        self.df = pd.read_csv(
            self.manifest_path,
            dtype=str,
            keep_default_na=False
        )

        string_columns = [
            "Download_Status",
            "Download_Date",
            "Local_File",
            "SHA256",
            "Error_Message",
            "Download_URL",
            "API_Base",
            "FTP_Path",
            "Git_Repo",
            "CLI_Command",
            "Authentication",
            "Local_Path",
            "Checksum",
        ]

        for col in string_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str)

    def datasets(self):
        return self.df.iterrows()

    def save(self):
        self.df.to_csv(self.manifest_path, index=False)

    def update(
        self,
        index,
        status,
        local_file="",
        sha256="",
        size_mb=None,
        error=""
    ):

        self.df.at[index, "Download_Status"] = str(status)
        self.df.at[index, "Download_Date"] = datetime.now().isoformat(timespec="seconds")
        self.df.at[index, "Local_File"] = str(local_file)
        self.df.at[index, "SHA256"] = str(sha256)
        self.df.at[index, "Error_Message"] = str(error)

        if size_mb is not None:
            self.df.at[index, "File_Size_MB"] = f"{float(size_mb):.3f}"

        self.save()

    def summary(self):

        success = (self.df["Download_Status"] == "Success").sum()

        return {
            "total": len(self.df),
            "success": int(success),
            "pending": len(self.df) - int(success),
        }


if __name__ == "__main__":

    m = ManifestManager(
        "metadata/downloads/GOHIF_Download_Manifest.csv"
    )

    print(m.summary())
