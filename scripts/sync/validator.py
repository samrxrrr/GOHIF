from pathlib import Path
from utils import info, ok, fail

ROOT = Path(__file__).resolve().parents[2]

DOMAINS = [
    "human_health",
    "animal_health",
    "environmental_health",
    "food_chain",
]

def validate():

    info("Validating frozen domains...")

    success = True

    for d in DOMAINS:

        cov = ROOT / "docs" / "coverage_analysis" / d
        srr = ROOT / "docs" / "SRR" / d

        if not cov.exists():
            fail(f"Coverage missing: {d}")
            success = False
        else:
            ok(f"Coverage: {d}")

        if not srr.exists():
            fail(f"SRR missing: {d}")
            success = False
        else:
            ok(f"SRR: {d}")

    return success
