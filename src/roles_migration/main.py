import argparse
from pathlib import Path
from roles_migration.config import DatabaseConfig
from roles_migration.transform import transform_workbook
from roles_migration.loader import load_all

ROOT=Path(__file__).resolve().parents[2]

def main():
    parser=argparse.ArgumentParser(description="Validate and migrate Excel RBAC data into MySQL.")
    parser.add_argument("--input",default=str(ROOT/"data/source/authorization_source.xlsx"))
    parser.add_argument("--dry-run",action="store_true")
    args=parser.parse_args()
    source=Path(args.input)
    if not source.exists():
        raise FileNotFoundError(f"Workbook not found: {source}. Run scripts/generate_sample_workbook.py first.")
    accepted,rejected,source_counts=transform_workbook(source)
    reports=ROOT/"reports"; reports.mkdir(exist_ok=True)
    print("Table                 Source   Accepted   Rejected")
    for table in accepted:
        a=len(accepted[table]); r=len(rejected[table])
        print(f"{table:<21} {source_counts[table]:>6} {a:>10} {r:>10}")
        accepted[table].to_csv(reports/f"{table}_accepted.csv",index=False)
        rejected[table].to_csv(reports/f"{table}_rejected.csv",index=False)
        assert a+r==source_counts[table], f"Row reconciliation failed for {table}"
    if args.dry_run:
        print("DRY RUN: no database connection was opened.")
        return 0
    print("MySQL rows loaded:",load_all(accepted,DatabaseConfig.from_env()))
    return 0

if __name__=="__main__": raise SystemExit(main())
