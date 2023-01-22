import argparse
import psycopg2
from models import User
from psycopg2.errors import UniqueViolation
from clcrypto import check_password

conn = psycopg2.connect(user="postgres",
                        password="coderslab",
                        host="localhost",
                        database="workshop_db")

conn.autocommit = True
cursor = conn.cursor()

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new_pass (min 8 characters)")
parser.add_argument("-d", "--delete", help="delete", action="store_true")
parser.add_argument("-e", "--edit", help="edit", action="store_true")
parser.add_argument("-l", "--list", help="list", action="store_true")

args = parser.parse_args()


def list_users(cur):
    users = User.load_all_users(cur)
    for user in users:
        print(user.username)


def create_user(cur, username, password):
    if len(password) < 8:
        print("Password is too short! Type in min. 8 characters")
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cur)
            print("User created!")
        except UniqueViolation as e:
            print("User already exists!", e)


def delete_user(cur, username, password):
    user = User.load_user_by_username(cur, username)
    if user not in user.load_all_users():
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        user.delete(cur)
        print("User deleted!")
    else:
        print("Wrong password!")

def edit_user(cur, username, password, new_pass):
    user = User.load_user_by_username(cur, username)
    if user not in user.load_all_users():
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("Password is too short!")
        else:
            user.hashed_password = new_pass
            user.save_to_db(cur)
            print("Password changed!")
    else:
        print("Wrong password!")