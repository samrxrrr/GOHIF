from pathlib import Path
import pandas as pd
from docx import Document

# Project directories
BASE_DIR = Path.home() / "GOHIF" / "analysis" / "structure_validation"
INPUT_DOCX = BASE_DIR / "selected_structures" / "GOHIF_Master_Receptor_Library.docx"
OUTPUT_CSV = BASE_DIR / "selected_structures" / "Selected_Structures.csv"

# Check input file
if not INPUT_DOCX.exists():
    raise FileNotFoundError(f"Input file not found:\n{INPUT_DOCX}")

# Load document
doc = Document(INPUT_DOCX)

if len(doc.tables) == 0:
    raise RuntimeError("No tables found in the DOCX file.")

# Use the first table
table = doc.tables[0]

# Extract header
headers = [cell.text.strip() for cell in table.rows[0].cells]

# Extract rows
rows = []
for row in table.rows[1:]:
    values = [cell.text.strip().replace("\n", " ") for cell in row.cells]

    # Skip completely empty rows
    if any(values):
        rows.append(values)

# Create DataFrame
df = pd.DataFrame(rows, columns=headers)

# Save CSV
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False)

print("=" * 60)
print("GOHIF Receptor Library Conversion Complete")
print("=" * 60)
print(f"Input : {INPUT_DOCX}")
print(f"Output: {OUTPUT_CSV}")
print(f"Rows  : {len(df)}")
print(f"Cols  : {len(df.columns)}")
print("\nColumns:")
print(df.columns.tolist())
print("\nFirst five entries:")
print(df.head())
