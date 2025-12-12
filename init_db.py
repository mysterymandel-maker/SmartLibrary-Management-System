import psycopg2
from database.db_connection import get_connection, release_connection
import os
import hashlib

def init_db():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Read schema.sql
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            
        cur.execute(schema_sql)
        conn.commit()
        print("Tables initialized successfully.")
        
        # Check if admin user exists, if not create one
        cur.execute("SELECT * FROM users WHERE username = 'admin'")
        if cur.fetchone() is None:
            # Simple hash for demo purposes. In production use bcrypt/argon2
            # For this demo, we'll store password as is or simple hash? 
            # Let's do a simple SHA256 for now as requested 'password_hash' in schema
            # Default admin password: 'admin'
            pw_hash = hashlib.sha256("admin".encode()).hexdigest()
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                ('admin', pw_hash, 'librarian')
            )
            print("Default admin user created (admin/admin).")
            
            # Default member
            pw_hash_member = hashlib.sha256("member".encode()).hexdigest()
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                ('member', pw_hash_member, 'member')
            )
            print("Default member user created (member/member).")
            
        conn.commit()
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error executing schema: {error}")
    finally:
        if conn:
            release_connection(conn)

if __name__ == "__main__":
    init_db()
