import sqlite3

connection = sqlite3.connect('data.sqlite')
cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'enaya11', 'test321')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
  (2, 'abbas22', 'cheehoo'),
  (3, 'bubba33', 'chikaro')
]
cursor.executemany(insert_query, users) # insert multiple users

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
  print(row)

connection.commit() # save changes into data.db
connection.close()
