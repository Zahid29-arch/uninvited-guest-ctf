import sqlite3

conn = sqlite3.connect('platform/ctfd-data/ctfd.db')
c = conn.cursor()

# Stage 2: Remove (or http://localhost:3000)
c.execute("""
UPDATE challenges 
SET description = 'Use the corporate email discovered in Stage 1 to gain access to the administrator account on the OWASP Juice Shop portal at http://192.168.60.10:3000. Bypass the authentication mechanism on the login portal. Once logged into the admin dashboard, inspect the user profile section to find the administrator username.'
WHERE id = 2
""")

# Stage 3: Remove or http://localhost:3000
c.execute("""
UPDATE challenges 
SET description = 'As the administrator on OWASP Juice Shop (http://192.168.60.10:3000), access the restricted Evidence Vault backup to download the encrypted archive evidence_photos.zip (also attached below). The archive contains confidential case notes and Juice Shop product images. Use the provided wordlist to recover the master passphrase.'
WHERE id = 3
""")

# Stage 6: Remove (or http://localhost:8086)
c.execute("""
UPDATE challenges 
SET description = 'Access The Exchange Portal at http://192.168.60.10:8086 using the administrator credentials obtained in earlier stages. Retrieve the forensic network capture upload_capture.pcap. Perform packet inspection to uncover the real identity of the external accomplice operating under the alias DragonFly.'
WHERE id = 6
""")

conn.commit()

# Verify
c.execute("SELECT id, name, description FROM challenges")
for row in c.fetchall():
    print(f"Stage {row[0]}: {row[1]}")
    print(f"  {row[2]}\n")

conn.close()
