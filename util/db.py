import sqlite3
DB = "data/accounts.db"


def add_user(username, hashed_num):
    '''adds users to use table'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "INSERT INTO users (username,numbers)VALUES(?,?);"
    c.execute(command, (username, hashed_num))
    db.commit()
    db.close()

def get_all_users():
    '''returns all the users and hashed passwords in dict {user:pass}'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "SELECT username,numbers from users;"
    c.execute(command)
    info = c.fetchall()
    users = {}
    for item in info:
        users[item[0]] = item[1]
    db.close()
    return users

def get_users_num(user):
    '''returns the user's num'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "SELECT numbers from users " + "WHERE username ='" + user + "';"
    c.execute(command)
    info = c.fetchall()
    db.close()
    print(info)
    return info

def get_users_type(user):
    '''returns the user's type'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "SELECT type from users " + "WHERE username ='" + user + "';"
    c.execute(command)
    info = c.fetchall()
    db.close()
    print(info)
    return info

def add_type(user, type):
    '''adds type to user'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "UPDATE users SET type ='" + type + "'WHERE username ='" + user + "';"
    c.execute(command)
    db.commit()
    db.close()


# MAKE TABLES AND DATABASE IF THEY DONT EXIST
db = sqlite3.connect(DB)
c = db.cursor()
commands = []
commands += ["CREATE TABLE IF NOT EXISTS users(username TEXT, numbers TEXT, type TEXT);"]
# commands += ["CREATE TABLE IF NOT EXISTS pages(link TEXT, weather TEXT, comic TEXT)"]
for command in commands:
    c.execute(command)
