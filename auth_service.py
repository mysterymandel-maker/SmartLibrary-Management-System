from daos.user_dao import UserDAO
import hashlib

class AuthService:
    def __init__(self):
        self.user_dao = UserDAO()

    def login(self, username, password):
        user = self.user_dao.get_user_by_username(username)
        if user:
            # user: (id, username, password_hash, role)
            stored_hash = user[2]
            input_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if input_hash == stored_hash:
                return {"id": user[0], "username": user[1], "role": user[3]}
        return None

    def register(self, username, password, role='member'):
        # Check if user exists
        if self.user_dao.get_user_by_username(username):
            return False, "Username already exists"
            
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user_id = self.user_dao.create_user(username, password_hash, role)
        return True, user_id
