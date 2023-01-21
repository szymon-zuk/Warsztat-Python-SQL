import psycopg2


conn = psycopg2.connect(user="postgres",
                        password="coderslab",
                        host="localhost",
                        database="postgres")

conn.autocommit = True
cursor = conn.cursor()
sql = '''CREATE DATABASE workshop_db;'''

try:
    cursor.execute(sql)
    print("Baza danych została utworzona!")
except psycopg2.errors.DuplicateDatabase:
    print("Taka baza danych już istnieje!")

conn.close()
