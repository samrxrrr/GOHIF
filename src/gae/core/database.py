from __future__ import annotations

import sqlite3
from pathlib import Path


DATABASE_PATH = Path("gae.db")


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(DATABASE_PATH)

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS acquisitions(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                dataset_id TEXT,

                dataset_name TEXT,

                version TEXT,

                plugin TEXT,

                url TEXT,

                destination TEXT,

                file_size INTEGER,

                sha256 TEXT,

                status TEXT,

                started_at TEXT,

                finished_at TEXT,

                duration REAL,

                error TEXT

            )
            """
        )

        self.connection.commit()

    def insert(
        self,
        record: tuple,
    ):

        self.connection.execute(
            """
            INSERT INTO acquisitions(

                dataset_id,
                dataset_name,
                version,
                plugin,
                url,
                destination,
                file_size,
                sha256,
                status,
                started_at,
                finished_at,
                duration,
                error

            )

            VALUES(

                ?,?,?,?,?,?,
                ?,?,?,?,?,?,
                ?

            )
            """,
            record,
        )

        self.connection.commit()

    def close(self):

        self.connection.close()
