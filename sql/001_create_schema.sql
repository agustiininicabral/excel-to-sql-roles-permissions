CREATE DATABASE IF NOT EXISTS authorization_migration CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE authorization_migration;

CREATE TABLE IF NOT EXISTS users (
 user_id BIGINT UNSIGNED PRIMARY KEY,
 email VARCHAR(254) NOT NULL UNIQUE,
 full_name VARCHAR(160) NOT NULL,
 is_active BOOLEAN NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS roles (
 role_code VARCHAR(40) PRIMARY KEY,
 role_name VARCHAR(100) NOT NULL,
 description VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS permissions (
 permission_code VARCHAR(80) PRIMARY KEY,
 resource VARCHAR(60) NOT NULL,
 action VARCHAR(40) NOT NULL,
 UNIQUE KEY uq_permission_resource_action (resource, action)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS user_roles (
 user_id BIGINT UNSIGNED NOT NULL,
 role_code VARCHAR(40) NOT NULL,
 assigned_at DATE NOT NULL,
 PRIMARY KEY (user_id, role_code),
 CONSTRAINT fk_user_roles_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
 CONSTRAINT fk_user_roles_role FOREIGN KEY (role_code) REFERENCES roles(role_code) ON DELETE RESTRICT,
 INDEX idx_user_roles_role (role_code)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS role_permissions (
 role_code VARCHAR(40) NOT NULL,
 permission_code VARCHAR(80) NOT NULL,
 PRIMARY KEY (role_code, permission_code),
 CONSTRAINT fk_role_permissions_role FOREIGN KEY (role_code) REFERENCES roles(role_code) ON DELETE RESTRICT,
 CONSTRAINT fk_role_permissions_permission FOREIGN KEY (permission_code) REFERENCES permissions(permission_code) ON DELETE RESTRICT,
 INDEX idx_role_permissions_permission (permission_code)
) ENGINE=InnoDB;
