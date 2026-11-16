from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/source/authorization_source.xlsx"

SHEETS={
 "Users":[
 [1,"ana.garcia@example.com","Ana García",1],[2,"bruno.perez@example.com","Bruno Pérez",1],
 [3,"carla.lopez@example.com","Carla López",1],[4,"diego.fernandez@example.com","Diego Fernández",1],
 [5,"elena.suarez@example.com","Elena Suárez",1],[6,"facundo.romero@example.com","Facundo Romero",1],
 [7,"gabriela.torres@example.com","Gabriela Torres",1],[8,"hugo.diaz@example.com","Hugo Díaz",1],
 [9,"ines.castro@example.com","Inés Castro",1],[10,"julian.molina@example.com","Julián Molina",0],
 [11,"karen.rojas@example.com","Karen Rojas",1],[12,"lucas.acosta@example.com","Lucas Acosta",1]],
 "Roles":[
 ["admin","Administrator","Full platform administration"],["analyst","Data Analyst","Read and export analytical reports"],
 ["support","Support Agent","Manage support workflows"],["viewer","Read-only Viewer","Read permitted resources"]],
 "Permissions":[
 ["users:read","users","read"],["users:write","users","write"],["reports:read","reports","read"],
 ["reports:export","reports","export"],["orders:read","orders","read"],["orders:update","orders","update"],
 ["settings:manage","settings","manage"],["tickets:manage","tickets","manage"]],
 "UserRoles":[
 [1,"admin","2025-01-01"],[2,"analyst","2025-01-02"],[3,"viewer","2025-01-03"],
 [4,"support","2025-01-04"],[5,"viewer","2025-01-05"],[6,"analyst","2025-01-06"],
 [7,"support","2025-01-07"],[8,"viewer","2025-01-08"],[9,"analyst","2025-01-09"],
 [10,"viewer","2025-01-10"],[11,"support","2025-01-11"],[12,"viewer","2025-01-12"],
 [1,"analyst","2025-02-01"],[2,"viewer","2025-02-02"],[3,"viewer","2025-01-03"],
 [999,"admin","2025-02-04"],[4,"ghost","2025-02-05"],[5,"admin","not-a-date"]],
 "RolePermissions":[
 ["admin","users:read"],["admin","users:write"],["admin","reports:read"],["admin","reports:export"],
 ["admin","orders:read"],["admin","orders:update"],["admin","settings:manage"],["admin","tickets:manage"],
 ["analyst","reports:read"],["analyst","reports:export"],["analyst","orders:read"],["analyst","reports:read"],
 ["support","tickets:manage"],["support","orders:read"],["viewer","users:read"],["viewer","bad:permission"]]
}
COLUMNS={
 "Users":["user_id","email","full_name","is_active"],
 "Roles":["role_code","role_name","description"],
 "Permissions":["permission_code","resource","action"],
 "UserRoles":["user_id","role_code","assigned_at"],
 "RolePermissions":["role_code","permission_code"]
}

def main():
    with pd.ExcelWriter(OUT,engine="openpyxl") as writer:
        for sheet,rows in SHEETS.items():
            pd.DataFrame(rows,columns=COLUMNS[sheet]).to_excel(writer,sheet_name=sheet,index=False)
    print(f"Generated {OUT} with {sum(len(v) for v in SHEETS.values())} source records across five sheets")

if __name__=="__main__": main()
