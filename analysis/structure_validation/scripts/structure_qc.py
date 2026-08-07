#!/usr/bin/env python3

"""
=========================================================================
GOHIF Phase II
Structure Quality Control Pipeline
Version : 2.0
Author  : GOHIF
=========================================================================

Supports

• PDB structures
• mmCIF structures

Outputs

• Structure_QC_Report.csv
• Structure_QC_Report.html
• Structure_QC_Summary.txt

=========================================================================

"""

from pathlib import Path
import pandas as pd

from Bio.PDB import PDBParser
from Bio.PDB.MMCIFParser import MMCIFParser

import warnings

warnings.filterwarnings("ignore")

###############################################################################
# Project Directories
###############################################################################

BASE = Path.home() / "GOHIF" / "analysis" / "structure_validation"

RAW_DIR = BASE / "pdb" / "raw"

QC_DIR = BASE / "qc"

REPORT_DIR = BASE / "reports"

STAT_DIR = BASE / "statistics"

SCRIPT_DIR = BASE / "scripts"

QC_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
STAT_DIR.mkdir(parents=True, exist_ok=True)

###############################################################################
# Output Files
###############################################################################

CSV_REPORT = STAT_DIR / "Structure_QC_Report.csv"

HTML_REPORT = REPORT_DIR / "Structure_QC_Report.html"

TXT_REPORT = STAT_DIR / "Structure_QC_Summary.txt"

###############################################################################
# Parsers
###############################################################################

PDB_PARSER = PDBParser(QUIET=True)

MMCIF_PARSER = MMCIFParser(QUIET=True)

###############################################################################
# Helper Functions
###############################################################################

def detect_structure_files():

    pdb_files = sorted(RAW_DIR.glob("*.pdb"))

    cif_files = sorted(RAW_DIR.glob("*.cif"))

    files = pdb_files + cif_files

    files = sorted(files)

    return files


def get_parser(file_path):

    suffix = file_path.suffix.lower()

    if suffix == ".pdb":
        return PDB_PARSER

    if suffix == ".cif":
        return MMCIF_PARSER

    return None


def structure_format(file_path):

    if file_path.suffix.lower() == ".pdb":
        return "PDB"

    if file_path.suffix.lower() == ".cif":
        return "mmCIF"

    return "UNKNOWN"


###############################################################################
# QC Results Container
###############################################################################

RESULTS = []

###############################################################################
# Banner
###############################################################################

print("=" * 80)
print("GOHIF Phase II")
print("Advanced Structure Quality Control")
print("=" * 80)

FILES = detect_structure_files()

print(f"Structures detected : {len(FILES)}")

if len(FILES) == 0:

    raise RuntimeError(
        "No PDB/mmCIF files found inside analysis/structure_validation/pdb/raw"
    )

print("=" * 80)

###############################################################################
# Metadata Extraction
###############################################################################

def extract_structure_metadata(file_path):

    parser = get_parser(file_path)

    structure = parser.get_structure(file_path.stem, str(file_path))

    info = {}

    info["PDB_ID"] = file_path.stem

    info["Format"] = structure_format(file_path)

    info["Models"] = 0

    info["Chains"] = []

    info["Residues"] = 0

    info["Atoms"] = 0

    info["HETATM"] = 0

    info["Waters"] = 0

    info["Alternate_Locations"] = 0

    info["Experimental_Method"] = "Unknown"

    info["Resolution"] = "Unknown"

    info["QC_Status"] = "PASS"

    chain_ids = set()

    atom_count = 0

    residue_count = 0

    hetatm_count = 0

    water_count = 0

    altloc_count = 0

    model_count = 0

    for model in structure:

        model_count += 1

        for chain in model:

            chain_ids.add(chain.id)

            for residue in chain:

                hetflag = residue.id[0]

                if hetflag == " ":

                    residue_count += 1

                elif hetflag.startswith("H"):

                    hetatm_count += 1

                elif hetflag == "W":

                    water_count += 1

                for atom in residue:

                    atom_count += 1

                    if atom.is_disordered():

                        altloc_count += 1

    info["Models"] = model_count

    info["Chains"] = ",".join(sorted(chain_ids))

    info["Residues"] = residue_count

    info["Atoms"] = atom_count

    info["HETATM"] = hetatm_count

    info["Waters"] = water_count

    info["Alternate_Locations"] = altloc_count

    ###########################################################################
    # Read experimental method and resolution directly from file
    ###########################################################################

    try:

        if file_path.suffix.lower() == ".pdb":

            with open(file_path, "r", errors="ignore") as f:

                for line in f:

                    if line.startswith("EXPDTA"):

                        info["Experimental_Method"] = line[10:].strip()

                    if line.startswith("REMARK   2 RESOLUTION."):

                        tokens = line.split()

                        for token in tokens:

                            try:

                                float(token)

                                info["Resolution"] = float(token)

                                break

                            except:

                                pass

        else:

            with open(file_path, "r", errors="ignore") as f:

                for line in f:

                    if "_exptl.method" in line:

                        info["Experimental_Method"] = (
                            line.replace("_exptl.method", "")
                            .replace("'", "")
                            .strip()
                        )

                    if "_refine.ls_d_res_high" in line:

                        value = (
                            line.replace("_refine.ls_d_res_high", "")
                            .strip()
                        )

                        if value not in ["?", "."]:

                            try:

                                info["Resolution"] = float(value)

                            except:

                                info["Resolution"] = value

    except Exception:

        pass

    ###########################################################################
    # Simple QC rules
    ###########################################################################

    if residue_count < 100:

        info["QC_Status"] = "REVIEW"

    if atom_count == 0:

        info["QC_Status"] = "FAILED"

    return info

###############################################################################
# Main QC Processing
###############################################################################

print("\nStarting quality control...\n")

for file_path in FILES:

    try:

        metadata = extract_structure_metadata(file_path)

        RESULTS.append(metadata)

        print(
            f"{metadata['PDB_ID']:<8}"
            f"{metadata['Format']:<8}"
            f"{metadata['Experimental_Method'][:25]:<25}"
            f"{str(metadata['Resolution']):<10}"
            f"{metadata['QC_Status']}"
        )

    except Exception as e:

        RESULTS.append({

            "PDB_ID": file_path.stem,

            "Format": structure_format(file_path),

            "Models": 0,

            "Chains": "",

            "Residues": 0,

            "Atoms": 0,

            "HETATM": 0,

            "Waters": 0,

            "Alternate_Locations": 0,

            "Experimental_Method": "Unknown",

            "Resolution": "Unknown",

            "QC_Status": "FAILED",

            "Error": str(e)

        })

        print(f"{file_path.stem:<8} FAILED")

###############################################################################
# Convert Results to DataFrame
###############################################################################

QC = pd.DataFrame(RESULTS)

desired_columns = [

    "PDB_ID",

    "Format",

    "Experimental_Method",

    "Resolution",

    "Models",

    "Chains",

    "Residues",

    "Atoms",

    "HETATM",

    "Waters",

    "Alternate_Locations",

    "QC_Status"

]

for col in desired_columns:

    if col not in QC.columns:

        QC[col] = ""

QC = QC[desired_columns]

###############################################################################
# Save CSV
###############################################################################

QC.to_csv(

    CSV_REPORT,

    index=False

)

###############################################################################
# Summary Statistics
###############################################################################

summary = QC["QC_Status"].value_counts()

with open(TXT_REPORT, "w") as f:

    f.write("GOHIF Phase II\n")

    f.write("Advanced Structure Quality Control\n\n")

    f.write("Structures Analysed : ")

    f.write(str(len(QC)))

    f.write("\n\n")

    f.write(summary.to_string())

###############################################################################
# HTML Report
###############################################################################

html = []

html.append("<html>")

html.append("<head>")

html.append("<title>GOHIF QC Report</title>")

html.append(
"""
<style>

body{
font-family:Arial;
margin:40px;
}

table{
border-collapse:collapse;
width:100%;
}

th{
background:#1f4e79;
color:white;
padding:8px;
}

td{
border:1px solid #cccccc;
padding:6px;
text-align:center;
}

</style>
"""
)

html.append("</head>")

html.append("<body>")

html.append("<h1>GOHIF Phase II</h1>")

html.append("<h2>Advanced Structure Quality Control</h2>")

html.append(f"<p>Total Structures : {len(QC)}</p>")

html.append(QC.to_html(index=False))

html.append("</body>")

html.append("</html>")

with open(HTML_REPORT,"w") as f:

    f.write("\n".join(html))

###############################################################################
# Final Summary
###############################################################################

print("\n")

print("="*80)

print("GOHIF QC COMPLETE")

print("="*80)

print(summary)

print("\nCSV Report :")

print(CSV_REPORT)

print("\nHTML Report :")

print(HTML_REPORT)

print("\nSummary :")

print(TXT_REPORT)

print("="*80)
