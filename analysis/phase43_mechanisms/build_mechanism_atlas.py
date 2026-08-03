import pandas as pd

df = pd.read_csv(
    "analysis/large_scale/prioritization/prioritized_targets.csv"
)

genes = df["normalized_gene"].fillna("").astype(str).str.lower()

def classify(g):

    if any(x in g for x in [
        "ctx","tem","shv","oxa","kpc","ndm","vim","imp","sme",
        "ges","carb","fox","bla","adc","cmy","acc","smb","tla",
        "vmb","pena"
    ]):
        return "Beta-lactamase"

    if any(x in g for x in [
        "aac","aph","ant","npm","rmt","arm","rmtb","rmtc","sgm"
    ]):
        return "Aminoglycoside-modifying enzyme"

    if any(x in g for x in [
        "tet","oqx","acr","mex","ade","emr","mdt","nor","qep",
        "cme","mux","mfs"
    ]):
        return "Efflux pump"

    if any(x in g for x in [
        "erm","cfr","vga","lsa","lnu","mph","msr"
    ]):
        return "Target modification"

    if any(x in g for x in [
        "qnr","fus","dfr","fol","gyr","par","rpo","mur"
    ]):
        return "Target protection / alteration"

    if "mcr" in g:
        return "Lipid A modification"

    if any(x in g for x in [
        "cat","arr","fos","sat","ble"
    ]):
        return "Drug inactivation"

    return "Other"

df["Resistance_mechanism"] = genes.apply(classify)

summary = (
    df.groupby("Resistance_mechanism")
      .size()
      .reset_index(name="Proteins")
      .sort_values("Proteins", ascending=False)
)

summary.to_csv(
    "analysis/phase43_mechanisms/resistance_mechanism_summary.csv",
    index=False
)

df.to_csv(
    "analysis/phase43_mechanisms/resistance_mechanism_atlas.csv",
    index=False
)

print("="*80)
print("GOHIF RESISTANCE MECHANISM ATLAS COMPLETE")
print("="*80)
print()
print(summary.to_string(index=False))
