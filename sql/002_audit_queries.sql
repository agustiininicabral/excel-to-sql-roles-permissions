USE authorization_migration;

-- User-to-role assignments by role
SELECT r.role_code, r.role_name, COUNT(ur.user_id) AS assigned_users
FROM roles r LEFT JOIN user_roles ur ON ur.role_code = r.role_code
GROUP BY r.role_code, r.role_name ORDER BY r.role_code;

-- Effective permissions by user
SELECT u.user_id, u.full_name, r.role_code, p.permission_code
FROM users u
JOIN user_roles ur ON ur.user_id = u.user_id
JOIN roles r ON r.role_code = ur.role_code
JOIN role_permissions rp ON rp.role_code = r.role_code
JOIN permissions p ON p.permission_code = rp.permission_code
WHERE u.is_active = TRUE
ORDER BY u.user_id, r.role_code, p.permission_code;

-- Must return zero: orphaned user-role references
SELECT COUNT(*) AS orphan_user_role_rows
FROM user_roles ur LEFT JOIN users u ON u.user_id = ur.user_id
WHERE u.user_id IS NULL;

-- Must return zero: orphaned role-permission references
SELECT COUNT(*) AS orphan_role_permission_rows
FROM role_permissions rp
LEFT JOIN roles r ON r.role_code = rp.role_code
LEFT JOIN permissions p ON p.permission_code = rp.permission_code
WHERE r.role_code IS NULL OR p.permission_code IS NULL;
