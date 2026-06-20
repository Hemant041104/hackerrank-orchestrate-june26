import pandas as pd
from pathlib import Path

from code.agent import analyze_claim
from code.normalizer import normalize_result

ROOT = Path.cwd()

claims_path = ROOT / "dataset" / "claims.csv"

df = pd.read_csv(claims_path)

results = []

for _, row in df.iterrows():

    image_paths = []

    for p in str(row["image_paths"]).split(";"):
        image_paths.append(
            str(ROOT / "dataset" / p)
        )

    result = analyze_claim(
        claim_text=row["user_claim"],
        claim_object=row["claim_object"],
        image_paths=image_paths,
    )
    result = normalize_result(result)
    output_row = {
        "user_id": row["user_id"],
        "image_paths": row["image_paths"],
        "user_claim": row["user_claim"],
        "claim_object": row["claim_object"],
        "evidence_standard_met": result.get("evidence_standard_met"),
        "evidence_standard_met_reason": result.get("evidence_standard_met_reason"),
        "risk_flags": result.get("risk_flags"),
        "issue_type": result.get("issue_type"),
        "object_part": result.get("object_part"),
        "claim_status": result.get("claim_status"),
        "claim_status_justification": result.get("claim_status_justification"),
        "supporting_image_ids": result.get("supporting_image_ids"),
        "valid_image": result.get("valid_image"),
        "severity": result.get("severity"),
    }

    results.append(output_row)

out_df = pd.DataFrame(results)

output_path = ROOT / "output.csv"

out_df.to_csv(output_path, index=False)

print(f"Saved: {output_path}")
print(f"Rows: {len(out_df)}")
