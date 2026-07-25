from pathlib import Path
import json
import hashlib
import pandas as pd

ROOT = Path.home()/"GoogleDrive"/"GOHIF_DATA"/"00_RAW"
OUT  = Path.home()/"GoogleDrive"/"GOHIF_DATA"/"01_METADATA"/"Profiles"

OUT.mkdir(parents=True, exist_ok=True)

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        while True:
            b=f.read(1024*1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

for file in ROOT.rglob("*"):
    if not file.is_file():
        continue

    info={
        "file":str(file),
        "name":file.name,
        "extension":file.suffix,
        "size":file.stat().st_size,
        "sha256":sha256(file)
    }

    try:

        if file.suffix.lower()==".csv":

            df=pd.read_csv(file,nrows=500)

            info["type"]="csv"
            info["columns"]=list(df.columns)
            info["column_count"]=len(df.columns)
            info["sample_rows"]=len(df)

        elif file.suffix.lower()==".json":

            with open(file) as f:
                obj=json.load(f)

            info["type"]="json"

            if isinstance(obj,dict):
                info["keys"]=list(obj.keys())

            elif isinstance(obj,list):
                info["records"]=len(obj)

        elif file.suffix.lower() in [".fa",".fasta",".faa",".fna"]:

            n=0

            with open(file) as f:
                for line in f:
                    if line.startswith(">"):
                        n+=1

            info["type"]="fasta"
            info["sequence_count"]=n

        elif file.suffix.lower()==".zip":

            import zipfile

            z=zipfile.ZipFile(file)

            info["type"]="zip"
            info["files"]=z.namelist()

    except Exception as e:

        info["error"]=str(e)

    outfile=OUT/(file.name+".profile.json")

    with open(outfile,"w") as f:
        json.dump(info,f,indent=2)

print("DONE")
print("Profiles:",len(list(OUT.glob("*.json"))))
