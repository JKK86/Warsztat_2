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

    def delete(self):
        if self.id != None:
            sql = f"DELETE FROM users WHERE id={self.id}"
            conn = connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            self._id = None
            return True


class Messages:
    def __init__(self, from_id, to_id, text):
        self._id = None
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_data = None

    @property
    def id(self):
        return self._id

    @property
    def creation_data(self):
        return self._creation_data

    def save_to_db(self):
        if self._id == None:
            sql = f"""INSERT INTO messages (from_id, to_id, text)                                                  
            VALUES ({self.from_id}, {self.to_id}, '{self.text}')                                                      
            RETURNING id                                                                                             
            """
            conn = connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            self._id = cursor.fetchone()[0]
            conn.close()
            return True
        else:
            sql = f"""UPDATE messages SET from_id={self.from_id}, to_id={self.to_id}, text = '{self.text}'        
            WHERE id={self._id}                                                                                                    
            """
            conn = connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.close()
            return True

    @classmethod
    def load_all_messages(cls):
        sql = f"SELECT id, from_id, to_id, text, creation_data FROM messages;"
        messages = []
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_data_ = row
            loaded_messages = cls(from_id, to_id, text)
            loaded_messages._id = id_
            loaded_messages._creation_data = creation_data_
            messages.append(loaded_messages)
            conn.close()
        return messages

    def __str__(self):
        return f"Wiadomość od {self.from_id} do {self.to_id} o treści {self.text}, utworzona: {self.creation_data}"

    def __repr__(self):
        return str(self)


# if __name__=='__main__':
#     a = Messages.load_all_messages()
#     a_string = '\n'.join([str(x) for x in a])
#     print(a_string)
#     B = Messages(1,2,"Dzień dobry")
#     print(B)



# m = Messages(3,4,"Cześć kolego!")
# n = Messages(4,3,"Siemanko")
# o = Messages(3,4,"Co tam słychać?")
# p = Messages(4,3,"W porządku")
#
# m.save_to_db()
# n.save_to_db()
# o.save_to_db()
# p.save_to_db()


