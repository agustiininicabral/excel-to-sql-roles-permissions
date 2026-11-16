import os
import mysql.connector

EXPECTED={"users":12,"roles":4,"permissions":8,"user_roles":14,"role_permissions":14}

def main():
    connection=mysql.connector.connect(host=os.getenv("DB_HOST","127.0.0.1"),
        port=int(os.getenv("DB_PORT","3306")),database=os.getenv("DB_NAME","authorization_migration"),
        user=os.getenv("DB_USER","root"),password=os.getenv("DB_PASSWORD",""))
    try:
        cursor=connection.cursor()
        for table,expected in EXPECTED.items():
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            actual=cursor.fetchone()[0]
            assert actual==expected, f"{table}: expected {expected}, got {actual}"
            print(f"{table}: {actual} rows verified")
        cursor.execute("""SELECT COUNT(*) FROM user_roles ur
            LEFT JOIN users u ON u.user_id=ur.user_id
            LEFT JOIN roles r ON r.role_code=ur.role_code
            WHERE u.user_id IS NULL OR r.role_code IS NULL""")
        assert cursor.fetchone()[0]==0, "Orphan user-role rows found"
        cursor.execute("""SELECT COUNT(*) FROM role_permissions rp
            LEFT JOIN roles r ON r.role_code=rp.role_code
            LEFT JOIN permissions p ON p.permission_code=rp.permission_code
            WHERE r.role_code IS NULL OR p.permission_code IS NULL""")
        assert cursor.fetchone()[0]==0, "Orphan role-permission rows found"
        print("Foreign-key integrity verified: no orphan relationships.")
    finally: connection.close()

if __name__=="__main__": main()
