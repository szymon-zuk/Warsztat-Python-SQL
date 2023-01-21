from clcrypto import hash_password
import psycopg2
import datetime

conn = psycopg2.connect(user="postgres",
                        password="coderslab",
                        host="localhost",
                        database="workshop_db")

conn.autocommit = True
cursor = conn.cursor()


class User:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id;"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE users SET username = %s, hashed_password = %s
                           WHERE id=%s;"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        id_, username, hashed_password = data
        loaded_user = User(username)
        loaded_user._id = id_
        loaded_user._hashed_password = hashed_password
        return loaded_user

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        id_, username, hashed_password = data
        loaded_user = User(username)
        loaded_user._id = id_
        loaded_user._hashed_password = hashed_password
        return loaded_user

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True


class Messages:
    def __init__(self, from_id="", to_id="", text="", creation_date=None):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = creation_date

    def id(self):
        return self._id

    def save_to_db(self, cursor):
        current_date = datetime.date.today()
        self.creation_date = current_date
        if self._id == -1:
            sql = """INSERT INTO messages(from_id, to_id, text, creation_date) VALUES(%s, %s, %s, %s) RETURNING id;"""
            values = (int(self.from_id), int(self.to_id), self.text, self.creation_date)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE messages SET from_id = %s, to_id = %s, creation_date = %s, text = %s 
                           WHERE id=%s;"""
            values = (self.from_id, self.to_id, self.creation_date, self.text)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT id, from_id, to_id, creation_date, text FROM messages;"
        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id, from_id, to_id, creation_date, text = row
            loaded_user = Messages()
            loaded_user._id = id
            loaded_user.from_id = from_id
            loaded_user.to_id = to_id
            loaded_user.creation_date = creation_date
            loaded_user.text = text
            messages.append(loaded_user)
        return messages


conn.close()
