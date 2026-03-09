import sqlite3

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO admin (USERNAME, password, email, phone) VALUES ('Ajay', '2611', 'ajaywadhvani9692', '7505879692')"
)

conn.commit()
conn.close()

print("tABEL CREATED successfully")