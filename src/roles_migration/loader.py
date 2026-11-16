import mysql.connector
from roles_migration.config import DatabaseConfig

STATEMENTS = {
 "users": """INSERT INTO users(user_id,email,full_name,is_active) VALUES(%s,%s,%s,%s)
 ON DUPLICATE KEY UPDATE email=VALUES(email),full_name=VALUES(full_name),is_active=VALUES(is_active)""",
 "roles": """INSERT INTO roles(role_code,role_name,description) VALUES(%s,%s,%s)
 ON DUPLICATE KEY UPDATE role_name=VALUES(role_name),description=VALUES(description)""",
 "permissions": """INSERT INTO permissions(permission_code,resource,action) VALUES(%s,%s,%s)
 ON DUPLICATE KEY UPDATE resource=VALUES(resource),action=VALUES(action)""",
 "user_roles": """INSERT INTO user_roles(user_id,role_code,assigned_at) VALUES(%s,%s,%s)
 ON DUPLICATE KEY UPDATE assigned_at=VALUES(assigned_at)""",
 "role_permissions": """INSERT INTO role_permissions(role_code,permission_code) VALUES(%s,%s)
 ON DUPLICATE KEY UPDATE permission_code=VALUES(permission_code)"""
}
COLUMNS={
 "users":["user_id","email","full_name","is_active"],
 "roles":["role_code","role_name","description"],
 "permissions":["permission_code","resource","action"],
 "user_roles":["user_id","role_code","assigned_at"],
 "role_permissions":["role_code","permission_code"]
}

def load_all(accepted,config: DatabaseConfig):
    connection=mysql.connector.connect(host=config.host,port=config.port,database=config.database,
                                       user=config.user,password=config.password)
    counts={}
    try:
        cursor=connection.cursor()
        for table in COLUMNS:
            frame=accepted[table]
            values=[tuple(getattr(row,col) for col in COLUMNS[table]) for row in frame.itertuples(index=False)]
            if values:
                cursor.executemany(STATEMENTS[table],values)
            counts[table]=len(values)
        connection.commit()
        return counts
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
