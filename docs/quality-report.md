# Sample quality report

The workbook is synthetic and includes a duplicate user-role pair, an unknown user ID, an unknown role, an invalid assignment date, a duplicate role-permission pair, and an unknown permission.

Expected dry-run reconciliation:
- Users: 12 accepted, 0 rejected.
- Roles: 4 accepted, 0 rejected.
- Permissions: 8 accepted, 0 rejected.
- UserRoles: 14 accepted, 4 rejected.
- RolePermissions: 14 accepted, 2 rejected.

Every source row is accounted for. These counts are only sample validation outcomes, not production metrics.
