import pandas as pd

ann=pd.read_csv(
"analysis/biological_annotation/functional_annotations.csv"
)

report=pd.DataFrame({
"Metric":[
"Targets",
"Annotated",
"GO Terms Available",
"Keyword Annotation"
],
"Value":[
len(ann),
(ann["annotation_status"]=="completed").sum(),
ann["go_terms"].astype(str).ne("").sum(),
ann["keywords"].astype(str).ne("").sum()
]
})

report.to_csv(
"analysis/validation/annotation_report.csv",
index=False
)

print("="*80)
print("GOHIF ANNOTATION VALIDATION")
print("="*80)
print(report.to_string(index=False))
