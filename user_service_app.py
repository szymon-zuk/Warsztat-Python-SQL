import argparse
import psycopg2
import models

conn = psycopg2.connect(user="postgres",
                        password="coderslab",
                        host="localhost",
                        database="workshop_db")

conn.autocommit = True
cursor = conn.cursor()

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-n", "--new_pass", help="new_pass")
parser.add_argument("-d", "--delete", help="delete")
parser.add_argument("-e", "--edit", help="edit")
parser.add_argument("-l", "--list", help="list")


args = parser.parse_args()


def add_user(username, password):
    db_username = models.User.load_user_by_username(cursor, username)
    str_db_username = db_username.__str__()
    if username == str_db_username:

