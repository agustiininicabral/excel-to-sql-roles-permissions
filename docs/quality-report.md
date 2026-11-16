# Sample quality report

The workbook is synthetic and includes a duplicate user-role pair, an unknown user ID, an unknown role, an invalid assignment date, a duplicate role-permission pair, and an unknown permission.

Expected dry-run reconciliation:
- Users: 12 accepted, 0 rejected.
- Roles: 4 accepted, 0 rejected.
- Permissions: 8 accepted, 0 rejected.
- UserRoles: 14 accepted, 4 rejected.
- RolePermissions: 14 accepted, 2 rejected.

Every source row is accounted for. These counts are only sample validation outcomes, not production metrics.


## Database integration

The CI run performs a real load into a disposable MySQL 8.0 service and verifies 12 users, 4 roles, 8 permissions, 14 user-role assignments, 14 role-permission mappings, and zero orphan relationships. No production data or database is used.
