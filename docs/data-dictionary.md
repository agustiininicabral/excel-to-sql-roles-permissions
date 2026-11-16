# Data dictionary

| Worksheet | Destination table | Primary key / natural key |
|---|---|---|
| Users | users | user_id; unique email |
| Roles | roles | role_code |
| Permissions | permissions | permission_code; unique resource/action |
| UserRoles | user_roles | (user_id, role_code) |
| RolePermissions | role_permissions | (role_code, permission_code) |

The two junction tables model many-to-many relationships. The database enforces referential integrity with foreign keys; the Python stage catches unknown references early and records rejection reasons before loading.
