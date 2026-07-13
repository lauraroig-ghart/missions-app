import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import get_connection


conn = get_connection()
cursor = conn.cursor()


print("=== FAMÍLIA ===")

cursor.execute("SELECT * FROM families")

for row in cursor.fetchall():
    print(dict(row))


print("\n=== USUARIS ===")

cursor.execute("SELECT * FROM users")

for row in cursor.fetchall():
    print(dict(row))


print("\n=== CATEGORIES ===")

cursor.execute("SELECT * FROM categories")

for row in cursor.fetchall():
    print(dict(row))


conn.close()