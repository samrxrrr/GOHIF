import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB = Path.home()/"GoogleDrive"/"GOHIF_DATA"/"registry.db"

PROFILE_DIR = Path.home()/"GoogleDrive"/"GOHIF_DATA"/"01_METADATA"/"Profiles"

conn = sqlite3.connect(DB)

cur = conn.cursor()

for profile in PROFILE_DIR.glob("*.json"):

    p=json.load(open(profile))

    cur.execute("""

    INSERT INTO datasets(

        dataset_id,

        name,

        domain,

        provider,

        version,

        format,

        size,

        sha256,

        path,

        download_date,

        profiled

    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?)

    """,(

        p.get("name"),

        p.get("name"),

        "",

        "",

        "latest",

        p.get("type"),

        p.get("size"),

        p.get("sha256"),

        p.get("file"),

        datetime.now().isoformat(),

        1

    ))

conn.commit()

print("Inserted:",
      cur.execute("SELECT COUNT(*) FROM datasets").fetchone()[0])

conn.close()
