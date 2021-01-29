from clcrypto import hash_password
from connection import connect


class User:
    def __init__(self, username = None, password = None, salt = None):
        self._id = None
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=None):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self):
        if self._id == None:
            sql = f"""INSERT INTO users (username, hashed_password)
            VALUES ('{self.username}','{self.hashed_password}')
            RETURNING id
            """
            conn = connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            self._id = cursor.fetchone()[0]
            conn.close()
            return True
        conn.close()
        return False

user1 = User('Jerzy Kurowski', 'skowronek')
user1.save_to_db()