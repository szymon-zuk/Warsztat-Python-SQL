import psycopg2


conn = psycopg2.connect(user="postgres",
                        password="coderslab",
                        host="localhost",
                        database="workshop_db")

conn.autocommit = True
cursor = conn.cursor()
sql = '''CREATE DATABASE workshop_db;'''

try:
    cursor.execute(sql)
    print("Baza danych została utworzona!")
except psycopg2.errors.DuplicateDatabase:
    print("Taka baza danych już istnieje!")

sql_2 = '''CREATE TABLE users
(
id SERIAL PRIMARY KEY,
username varchar(255),
hashed_password varchar(80)
);'''

try:
    cursor.execute(sql_2)
    print("Tablica 'users' została utworzona!")
except psycopg2.errors.DuplicateTable:
    print("Taka tablica już istnieje!")

sql_3 = '''CREATE TABLE messages
(
id SERIAL PRIMARY KEY,
from_id INT,
to_id INT,
creation_date TIMESTAMP DEFAULT current_date,
text varchar(255),
FOREIGN KEY(from_id) REFERENCES users(id),
FOREIGN KEY(to_id) REFERENCES users(id)
);'''

try:
    cursor.execute(sql_3)
    print("Tablica 'messages' została utworzona!")
except psycopg2.errors.DuplicateTable:
    print("Taka tablica już istnieje!")


conn.close()
