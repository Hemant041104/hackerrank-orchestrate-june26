import pandas as pd
from pathlib import Path

ROOT = Path.cwd()

sample_path = ROOT / "dataset" / "sample_claims.csv"

df = pd.read_csv(sample_path)

print("Evaluation Dataset")
print("==================")
print(f"Rows: {len(df)}")

if "claim_status" in df.columns:
    print("\nClaim Status Distribution:")
    print(df["claim_status"].value_counts())

if "issue_type" in df.columns:
    print("\nIssue Type Distribution:")
    print(df["issue_type"].value_counts())

print("\nEvaluation complete.")
