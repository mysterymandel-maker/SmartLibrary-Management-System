from daos.base_dao import BaseDAO

class UserDAO(BaseDAO):
    def create_user(self, username, password_hash, role='member'):
        query = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s) RETURNING id"
        result = self.execute_query(query, (username, password_hash, role), fetch_one=True)
        return result[0] if result else None

    def get_user_by_username(self, username):
        query = "SELECT id, username, password_hash, role FROM users WHERE username = %s"
        return self.execute_query(query, (username,), fetch_one=True)

    def get_all_users(self):
        query = "SELECT id, username, role, created_at FROM users"
        return self.execute_query(query, fetch_all=True)
