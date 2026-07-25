import sqlite3
from pathlib import Path

DB = Path.home()/"GoogleDrive"/"GOHIF_DATA"/"registry.db"

conn = sqlite3.connect(DB)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS datasets(

id INTEGER PRIMARY KEY AUTOINCREMENT,

dataset_id TEXT,

name TEXT,

domain TEXT,

provider TEXT,

version TEXT,

format TEXT,

size INTEGER,

sha256 TEXT,

path TEXT,

download_date TEXT,

profiled INTEGER DEFAULT 0,

validated INTEGER DEFAULT 0

)
""")

conn.commit()

conn.close()

print()
print("Registry Created")
print(DB)
