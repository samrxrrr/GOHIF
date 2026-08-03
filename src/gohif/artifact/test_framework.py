import pandas as pd

from gohif.artifact.manager import ArtifactManager
from gohif.artifact.loader import ArtifactLoader
from gohif.artifact.validator import ArtifactValidator


df=pd.DataFrame({

"gene":["OXA48","NDM1","CTXM15"],

"score":[220,180,160]

})

manager=ArtifactManager()

manager.save(

df,

"priority_demo",

46

)

ArtifactValidator.validate(

"analysis/results/phase46/priority_demo.metadata.json"

)

loader=ArtifactLoader()

print()

print(loader.list())

print()

print(loader.load("priority_demo"))
