from pathlib import Path
import pandas as pd

OUTPUT = Path("metadata/registry/GOHIF_ANALYTICS_REPORT.txt")


def section(title):
    return "\n" + "=" * 80 + f"\n{title}\n" + "=" * 80 + "\n"


def load(path):
    p = Path(path)
    return pd.read_csv(p) if p.exists() else None


def build():

    registry = load("metadata/registry/GOHIF_MASTER_DATASET_REGISTRY.csv")
    validation = load("metadata/registry/GOHIF_VALIDATION_REPORT.csv")
    fair = load("metadata/registry/GOHIF_FAIR_SCORES.csv")
    scientific = load("metadata/registry/GOHIF_SCIENTIFIC_SCORES.csv")
    health = load("metadata/registry/GOHIF_HEALTH_REPORT.csv")
    evidence = load("metadata/registry/GOHIF_EVIDENCE_SUMMARY.csv")

    report = []

    report.append(section("GOHIF REGISTRY"))

    report.append(f"Datasets : {len(registry)}")
    report.append(f"Columns  : {len(registry.columns)}")
    report.append(f"Domains  : {registry['One_Health_Domain'].nunique()}")
    report.append(f"Organizations : {registry['Organization'].nunique()}")

    report.append(section("DOMAIN DISTRIBUTION"))
    report.append(
        registry["One_Health_Domain"].value_counts().to_string()
    )

    if validation is not None:
        report.append(section("VALIDATION"))
        report.append(validation["Severity"].value_counts().to_string())

    if fair is not None:
        report.append(section("FAIR"))
        report.append(fair["FAIR_Score"].describe().to_string())

    if scientific is not None:
        report.append(section("SCIENTIFIC"))
        report.append(scientific["Scientific_Score"].describe().to_string())

    if health is not None:
        report.append(section("HEALTH"))
        report.append(health["Health_Status"].value_counts().to_string())

    if evidence is not None:
        report.append(section("PRIMARY EVIDENCE"))
        report.append(
            evidence.groupby("Primary_Evidence_Layer")["Datasets"]
            .sum()
            .sort_values(ascending=False)
            .to_string()
        )

    OUTPUT.write_text("\n".join(report))

    print(f"\nReport written to:\n{OUTPUT}")


if __name__ == "__main__":
    build()
