import sqlite3

db = sqlite3.connect("S:\Learn-advanced-topics-in-Python\database\mydatabase.db")
# db.execute("CREATE TABLE IF NOT EXISTS skills(name text, progress integer, user_id integer )")
cr = db.cursor()


# cr.execute("INSERT INTO users(name, id) VALUES('Ahmed',1)")
# cr.execute("INSERT INTO skills(name, progress, user_id) VALUES('Python',50,1)")


skills = cr.execute("SELECT * FROM skills")
users = cr.execute("SELECT * FROM users")
print(skills.fetchall())
print(users.fetchone())


db.commit()
cr.close()

print('----------------------')
# print(users)
