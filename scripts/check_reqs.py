import sqlite3

conn = sqlite3.connect('platform/ctfd-data/ctfd.db')
c = conn.cursor()

tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print("Tables:", tables)

for t in ['requirements', 'prerequisites', 'unlocks', 'solves', 'submissions']:
    if t in tables:
        print(f"\n--- Table: {t} ---")
        c.execute(f"PRAGMA table_info({t})")
        print("Columns:", [col[1] for col in c.fetchall()])
        c.execute(f"SELECT * FROM {t} LIMIT 10")
        print("Rows:", c.fetchall())
