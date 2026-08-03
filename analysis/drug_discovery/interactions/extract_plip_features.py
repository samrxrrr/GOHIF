from pathlib import Path
import pandas as pd
import xml.etree.ElementTree as ET


xml_dir = Path(
"analysis/drug_discovery/interactions/plip_results"
)


results=[]


for xml_file in xml_dir.glob("*_report.xml"):

    try:

        tree=ET.parse(xml_file)

        root=tree.getroot()


        text=ET.tostring(
            root,
            encoding="unicode"
        )


        record={

        "complex":xml_file.stem.replace("_report",""),

        "hydrogen_bonds":text.count("hydrogen_bond"),

        "hydrophobic_contacts":text.count("hydrophobic_interaction"),

        "salt_bridges":text.count("salt_bridge"),

        "pi_stack":text.count("pi_stack"),

        "pi_cation":text.count("pi_cation"),

        }


        record["interaction_count"]=(
            record["hydrogen_bonds"]
            +
            record["hydrophobic_contacts"]
            +
            record["salt_bridges"]
            +
            record["pi_stack"]
            +
            record["pi_cation"]
        )


        results.append(record)


    except Exception as e:

        print(
        "Failed:",
        xml_file,
        e
        )


df=pd.DataFrame(results)


df.to_csv(
"analysis/drug_discovery/interactions/interaction_features.csv",
index=False
)


print("="*80)
print("GOHIF PLIP FEATURE EXTRACTION COMPLETE")
print("="*80)

print(df.head().to_string(index=False))

