from pathlib import Path
import subprocess,sys
from roles_migration.transform import transform_workbook

ROOT=Path(__file__).resolve().parents[1]

def test_sample_workbook_relationship_validation():
    workbook=ROOT/"data/source/authorization_source.xlsx"
    if not workbook.exists():
        subprocess.run([sys.executable,"scripts/generate_sample_workbook.py"],cwd=ROOT,check=True)
    accepted,rejected,counts=transform_workbook(workbook)
    assert set(accepted)=={"users","roles","permissions","user_roles","role_permissions"}
    assert len(accepted["users"])==12
    assert len(accepted["roles"])==4
    assert len(accepted["permissions"])==8
    assert len(accepted["user_roles"])==14
    assert len(rejected["user_roles"])==4
    assert len(accepted["role_permissions"])==14
    assert len(rejected["role_permissions"])==2
    for key in accepted:
        assert len(accepted[key])+len(rejected[key])==counts[key]

def test_orphan_references_are_rejected():
    workbook=ROOT/"data/source/authorization_source.xlsx"
    if not workbook.exists():
        subprocess.run([sys.executable,"scripts/generate_sample_workbook.py"],cwd=ROOT,check=True)
    _,rejected,_=transform_workbook(workbook)
    reasons="|".join(rejected["user_roles"].rejection_reason)
    assert "unknown_user" in reasons
    assert "unknown_role" in reasons
    assert "invalid_assigned_at" in reasons
    assert "duplicate_user_role" in reasons
    rp_reasons="|".join(rejected["role_permissions"].rejection_reason)
    assert "unknown_permission" in rp_reasons
    assert "duplicate_role_permission" in rp_reasons
