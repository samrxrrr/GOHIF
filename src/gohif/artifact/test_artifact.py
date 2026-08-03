import pandas as pd

from gohif.artifact.artifact import Artifact
from gohif.artifact.registry import Registry

df = pd.DataFrame({

    "gene":[
        "OXA-48",
        "NDM-1",
        "CTX-M-15"
    ],

    "score":[
        220,
        180,
        170
    ]

})

artifact = Artifact(

    name="test_prioritization",

    phase="46",

    artifact_type="table"

)

artifact.save(

    df,

    "analysis/results/phase46"

)

registry = Registry(

    "analysis/results/registry"

)

registry.register(

    "analysis/results/phase46/test_prioritization.metadata.json"

)

print("="*80)

print("GOHIF ARTIFACT FRAMEWORK TEST")

print("="*80)

print(pd.read_csv(

"analysis/results/registry/registry.csv"

))
