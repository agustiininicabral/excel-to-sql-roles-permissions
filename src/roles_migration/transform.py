from __future__ import annotations
import re
from pathlib import Path
import pandas as pd

EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
SHEETS = {
 "users": ("Users", ["user_id","email","full_name","is_active"]),
 "roles": ("Roles", ["role_code","role_name","description"]),
 "permissions": ("Permissions", ["permission_code","resource","action"]),
 "user_roles": ("UserRoles", ["user_id","role_code","assigned_at"]),
 "role_permissions": ("RolePermissions", ["role_code","permission_code"]),
}

def _text(value):
    if pd.isna(value): return None
    value=str(value).strip()
    return value or None

def _date(value):
    if pd.isna(value): return None
    parsed=pd.to_datetime(value,format="mixed",dayfirst=True,errors="coerce")
    return None if pd.isna(parsed) else parsed.date()

def transform_workbook(path: str | Path):
    raw={}
    for key,(sheet,columns) in SHEETS.items():
        frame=pd.read_excel(path,sheet_name=sheet,dtype=str)
        missing=set(columns)-set(frame.columns)
        if missing: raise ValueError(f"{sheet} is missing columns: {', '.join(sorted(missing))}")
        raw[key]=frame[columns].copy()

    accepted={}; rejected={}
    users=[]; bad=[]; seen=set(); seen_emails=set()
    for row in raw["users"].to_dict("records"):
        uid=_text(row["user_id"]); email=(_text(row["email"]) or "").lower()
        name=_text(row["full_name"]); active=(_text(row["is_active"]) or "").lower()
        reasons=[]
        try: uid=int(uid)
        except (TypeError,ValueError): reasons.append("invalid_user_id"); uid=None
        if not email or not EMAIL.fullmatch(email): reasons.append("invalid_email")
        if not name: reasons.append("missing_full_name")
        if active not in {"0","1","true","false"}: reasons.append("invalid_is_active")
        if uid in seen and uid is not None: reasons.append("duplicate_user_id")
        if email and email in seen_emails: reasons.append("duplicate_email")
        record={"user_id":uid,"email":email,"full_name":name,"is_active":active in {"1","true"}}
        if reasons: bad.append({**record,"rejection_reason":"|".join(reasons)})
        else: seen.add(uid); seen_emails.add(email); users.append(record)
    accepted["users"]=pd.DataFrame(users); rejected["users"]=pd.DataFrame(bad)
    user_ids={r["user_id"] for r in users}

    roles=[]; bad=[]; seen=set()
    for row in raw["roles"].to_dict("records"):
        code=(_text(row["role_code"]) or "").lower(); name=_text(row["role_name"]); desc=_text(row["description"])
        reasons=[]
        if not code: reasons.append("missing_role_code")
        if not name: reasons.append("missing_role_name")
        if code in seen: reasons.append("duplicate_role_code")
        record={"role_code":code,"role_name":name,"description":desc or ""}
        if reasons: bad.append({**record,"rejection_reason":"|".join(reasons)})
        else: seen.add(code); roles.append(record)
    accepted["roles"]=pd.DataFrame(roles); rejected["roles"]=pd.DataFrame(bad)
    role_codes={r["role_code"] for r in roles}

    permissions=[]; bad=[]; seen=set(); seen_resource_actions=set()
    for row in raw["permissions"].to_dict("records"):
        code=(_text(row["permission_code"]) or "").lower()
        resource=(_text(row["resource"]) or "").lower(); action=(_text(row["action"]) or "").lower()
        reasons=[]
        if not code or not resource or not action: reasons.append("missing_permission_fields")
        if code in seen: reasons.append("duplicate_permission_code")
        if (resource,action) in seen_resource_actions: reasons.append("duplicate_resource_action")
        record={"permission_code":code,"resource":resource,"action":action}
        if reasons: bad.append({**record,"rejection_reason":"|".join(reasons)})
        else: seen.add(code); seen_resource_actions.add((resource,action)); permissions.append(record)
    accepted["permissions"]=pd.DataFrame(permissions); rejected["permissions"]=pd.DataFrame(bad)
    permission_codes={r["permission_code"] for r in permissions}

    assignments=[]; bad=[]; seen=set()
    for row in raw["user_roles"].to_dict("records"):
        try: uid=int(_text(row["user_id"]))
        except (TypeError,ValueError): uid=None
        role=(_text(row["role_code"]) or "").lower(); assigned=_date(row["assigned_at"])
        reasons=[]
        if uid not in user_ids: reasons.append("unknown_user")
        if role not in role_codes: reasons.append("unknown_role")
        if not assigned: reasons.append("invalid_assigned_at")
        key=(uid,role)
        if not reasons and key in seen: reasons.append("duplicate_user_role")
        record={"user_id":uid,"role_code":role,"assigned_at":assigned}
        if reasons: bad.append({**record,"rejection_reason":"|".join(reasons)})
        else: seen.add(key); assignments.append(record)
    accepted["user_roles"]=pd.DataFrame(assignments); rejected["user_roles"]=pd.DataFrame(bad)

    mappings=[]; bad=[]; seen=set()
    for row in raw["role_permissions"].to_dict("records"):
        role=(_text(row["role_code"]) or "").lower()
        permission=(_text(row["permission_code"]) or "").lower()
        reasons=[]
        if role not in role_codes: reasons.append("unknown_role")
        if permission not in permission_codes: reasons.append("unknown_permission")
        key=(role,permission)
        if not reasons and key in seen: reasons.append("duplicate_role_permission")
        record={"role_code":role,"permission_code":permission}
        if reasons: bad.append({**record,"rejection_reason":"|".join(reasons)})
        else: seen.add(key); mappings.append(record)
    accepted["role_permissions"]=pd.DataFrame(mappings); rejected["role_permissions"]=pd.DataFrame(bad)
    return accepted,rejected,{key:len(value) for key,value in raw.items()}
