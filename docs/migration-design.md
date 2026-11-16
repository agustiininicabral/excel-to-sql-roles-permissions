# Migration design

1. Read five Excel worksheets and validate required columns.
2. Normalize user emails, names, role codes, permission codes, and date values.
3. Validate entity keys and field requirements.
4. Build in-memory reference sets from accepted users, roles, and permissions.
5. Reject user-role and role-permission rows with missing references, invalid dates, or repeated composite keys.
6. Export accepted and rejected rows per destination table.
7. Load parent entities first (users, roles, permissions), then junction tables.
8. Commit all table loads in one transaction; rollback the transaction if any insert fails.

## Integrity controls
Composite primary keys prevent repeated assignments. Foreign keys prevent orphaned relationships even if the Python validation is bypassed. A real access-control migration also needs role-owner approval, least-privilege review, inactive-account policy, and a reconciliation of effective permissions before cutover.
