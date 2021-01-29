from clcrypto import hash_password
from connection import connect


class User:
    def __init__(self, username=None, password='', salt=None):
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
        else:
            sql = f"""UPDATE users SET username='{self.username}', hashed_password = '{self.hashed_password}'                 
            WHERE id={self._id}                                                                                
            """
            conn = connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.close()
            return True

    @classmethod
    def load_user_by_id(cls, id_):
        sql = f"SELECT id, username, hashed_password FROM users WHERE id={id_};"
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = cls(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            conn.close()
            return loaded_user
        else:
            return None

    @classmethod
    def load_all_users(cls):
        sql = f"SELECT id, username, hashed_password FROM users;"
        users = []
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = cls()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
            conn.close()
            return users

    @classmethod
    def load_user_by_username(cls, username):
        sql = f"SELECT id, username, hashed_password FROM users WHERE username='{username}';"
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = cls(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            conn.close()
            return loaded_user
        else:
            return None

    @classmethod
    def load_user_by_username(cls, username):
        sql = f"SELECT id, username, hashed_password FROM users WHERE username='{username}';"
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = cls(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            conn.close()
            return loaded_user
        else:
            return None
