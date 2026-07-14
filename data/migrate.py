from pathlib import Path
import sqlite3

DB = "data/missions.db"
MIGRATIONS = "data/migrations"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS schema_migrations(
    filename TEXT PRIMARY KEY,
    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

executed = {
    row[0]
    for row in cursor.execute(
        "SELECT filename FROM schema_migrations"
    )
}

for file in sorted(Path(MIGRATIONS).glob("*.sql")):

    if file.name in executed:
        continue

    print(f"Applying {file.name}")

    sql = file.read_text(encoding="utf8")

    cursor.executescript(sql)

    cursor.execute(
        "INSERT INTO schema_migrations(filename) VALUES(?)",
        (file.name,)
    )

conn.commit()
conn.close()

print("Done.")