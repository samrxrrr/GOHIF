import pandas as pd
import requests
import time

hits = pd.read_csv(
    "analysis/biological_annotation/uniprot_hits.csv"
)

records = []

for _, row in hits.iterrows():

    acc = row["accession"]

    result = {
        "protein": row["protein"],
        "pathogen": row["pathogen"],
        "accession": acc,
        "gene_symbol": "",
        "recommended_name": "",
        "organism": "",
        "go_terms": "",
        "keywords": "",
        "annotation_status": "failed"
    }

    if pd.isna(acc) or str(acc).strip() == "":
        records.append(result)
        continue

    url = f"https://rest.uniprot.org/uniprotkb/{acc}.json"

    try:
        r = requests.get(url, timeout=30)
        data = r.json()

        genes = data.get("genes", [])
        if genes:
            result["gene_symbol"] = genes[0].get("geneName", {}).get("value", "")

        pdesc = data.get("proteinDescription", {})
        if "recommendedName" in pdesc:
            result["recommended_name"] = pdesc["recommendedName"]["fullName"]["value"]

        result["organism"] = data.get("organism", {}).get("scientificName", "")

        kws = data.get("keywords", [])
        result["keywords"] = "; ".join(
            [k.get("name", "") for k in kws]
        )

        go = []
        for ref in data.get("uniProtKBCrossReferences", []):
            if ref.get("database") == "GO":
                go.append(ref.get("id"))

        result["go_terms"] = "; ".join(go)
        result["annotation_status"] = "completed"

    except Exception:
        pass

    records.append(result)
    time.sleep(0.5)

out = pd.DataFrame(records)

out.to_csv(
    "analysis/biological_annotation/functional_annotations.csv",
    index=False
)

print("=" * 80)
print("GOHIF FUNCTIONAL ANNOTATION COMPLETE")
print("=" * 80)
print(out.to_string(index=False))
