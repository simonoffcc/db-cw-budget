import hashlib

class UserService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username, password):
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("SELECT id, login, password_hash, role FROM users WHERE login = %s", (username,))
            user = cursor.fetchone()
            if user and user[2] == self.hash_password(password):
                return {
                    'id': user[0],
                    'login': user[1],
                    'role': user[3]
                }
        return None

    def add_user(self, username, password, role):
        password_hash = self.hash_password(password)
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("INSERT INTO users (login, password_hash, role) VALUES (%s, %s, %s)",
                           (username, password_hash, role))
            self.db_manager.conn.commit()
