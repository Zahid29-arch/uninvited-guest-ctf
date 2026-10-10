import sqlite3

db_path = r'platform/ctfd-data/ctfd.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Set all flags to case_insensitive
c.execute("UPDATE flags SET data='case_insensitive'")

existing = set((row[0], row[1].lower()) for row in c.execute('SELECT challenge_id, content FROM flags'))

flags_to_add = [
    # Stage 1
    (1, 'adrian_kessler'),
    (1, 'adrian.kessler'),
    (1, 'adrian kessler'),
    (1, 'Adrian Kessler'),
    (1, 'uninvited{adrian kessler}'),
    (1, 'uninvited{adrian.kessler}'),
    (1, 'adrian.kessler@uninvited.local'),
    # Stage 2
    (2, 'adrian.kessler'),
    (2, 'uninvited{adrian.kessler}'),
    (2, 'adrian_kessler'),
    (2, 'uninvited{adrian_kessler}'),
    (2, 'adrian kessler'),
    (2, 'Adrian Kessler'),
    (2, 'uninvited{Adrian Kessler}'),
    (2, 'uninvited{adrian kessler}'),
    (2, 'adrian.kessler@uninvited.local'),
    (2, 'uninvited{adrian.kessler@uninvited.local}'),
    # Stage 3
    (3, 'Kessler123!'),
    (3, 'kessler123!'),
    # Stage 4
    (4, 'apple_juice.jpg'),
    (4, 'apple_juice'),
    (4, 'uninvited{apple_juice}'),
    # Stage 5
    (5, 'http://localhost:8086'),
    (5, 'http://192.168.60.10:8086'),
    (5, 'http://10.67.110.77:8086'),
    (5, '8086'),
    (5, 'uninvited{8086}'),
    # Stage 6
    (6, 'victor_hale'),
    (6, 'Victor Hale'),
    (6, 'victor.hale'),
    (6, 'uninvited{victor.hale}'),
]

added_count = 0
for ch_id, content in flags_to_add:
    if (ch_id, content.lower()) not in existing:
        c.execute('INSERT INTO flags (challenge_id, type, content, data) VALUES (?, ?, ?, ?)',
                  (ch_id, 'static', content, 'case_insensitive'))
        existing.add((ch_id, content.lower()))
        added_count += 1

conn.commit()
print(f"Successfully added {added_count} new flag variations. Total flags: {c.execute('SELECT count(*) FROM flags').fetchone()[0]}")

print("\n--- Current Flags by Challenge ---")
for row in c.execute('SELECT challenge_id, content, data FROM flags ORDER BY challenge_id, id'):
    print(f"Stage {row[0]}: {row[1]} ({row[2]})")
