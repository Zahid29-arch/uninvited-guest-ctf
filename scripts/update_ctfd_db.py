import sqlite3

conn = sqlite3.connect('/opt/CTFd/CTFd/ctfd.db')
c = conn.cursor()

# 1. Update Challenge Descriptions
c.execute("""UPDATE challenges SET description = ? WHERE id = 1""", (
    "A rogue engineer calling himself 'k3ss_void' has been orchestrating the uninvited infrastructure. Investigate the public footprint across his team blog, leaked audit logs, and underground forum activity. Uncover his real identity and internal corporate email address. Keep the email safe for subsequent stages!",
))

c.execute("""UPDATE challenges SET description = ? WHERE id = 2""", (
    "Use the corporate email discovered in Stage 1 to gain access to the administrator account on the OWASP Juice Shop portal at http://192.168.60.10:3000 (or http://localhost:3000). Bypass the authentication mechanism on the login portal. Once logged into the admin dashboard, inspect the user profile section to find the administrator username.",
))

c.execute("""UPDATE challenges SET description = ? WHERE id = 3""", (
    "As the administrator on OWASP Juice Shop (http://192.168.60.10:3000 or http://localhost:3000), access the restricted Evidence Vault backup to download the encrypted archive evidence_photos.zip (also attached below). The archive contains confidential case notes and Juice Shop product images. Use the provided wordlist to recover the master passphrase.",
))

c.execute("""UPDATE challenges SET description = ? WHERE id = 4""", (
    "Analyze the provided proxy history log (proxy_history.xml) to audit administrator activity on OWASP Juice Shop. Identify which product image on the Juice Shop website was accessed significantly more than any other image.",
))

c.execute("""UPDATE challenges SET description = ? WHERE id = 5""", (
    "Inspect the outlier product image identified in Stage 4 from the decrypted Stage 3 archive. An accomplice covertly embedded access details inside this carrier image. Extract the hidden payload to discover the secret URL of the internal Exchange Portal.",
))

c.execute("""UPDATE challenges SET description = ? WHERE id = 6""", (
    "Access The Exchange Portal at http://192.168.60.10:8086 (or http://localhost:8086) using the administrator credentials obtained in earlier stages. Retrieve the forensic network capture upload_capture.pcap. Perform packet inspection to uncover the real identity of the external accomplice operating under the alias 'DragonFly'.",
))

# 2. Delete old flags and insert multi-format flags
c.execute("DELETE FROM flags")

flag_data = [
    # Challenge 1
    (1, 'static', 'Adrian Kessler', None),
    (1, 'static', 'adrian kessler', None),
    (1, 'static', 'uninvited{adrian_kessler}', None),
    (1, 'static', 'adrian.kessler@uninvited.local', None),
    (1, 'static', 'uninvited{adrian.kessler@uninvited.local}', None),

    # Challenge 2
    (2, 'static', 'adrian.kessler', None),
    (2, 'static', 'uninvited{adrian.kessler}', None),

    # Challenge 3
    (3, 'static', 'Kessler123!', None),
    (3, 'static', 'uninvited{Kessler123!}', None),
    (3, 'static', 'Password123!', None),
    (3, 'static', 'uninvited{Password123!}', None),

    # Challenge 4
    (4, 'static', 'apple_juice.jpg', None),
    (4, 'static', 'uninvited{apple_juice.jpg}', None),

    # Challenge 5
    (5, 'static', 'http://localhost:8086', None),
    (5, 'static', 'uninvited{http://localhost:8086}', None),
    (5, 'static', 'http://localhost:8086/portal', None),
    (5, 'static', 'uninvited{http://localhost:8086/portal}', None),

    # Challenge 6
    (6, 'static', 'Victor Hale', None),
    (6, 'static', 'victor hale', None),
    (6, 'static', 'victor_hale', None),
    (6, 'static', 'uninvited{victor_hale}', None),
]

for ch_id, f_type, content, data in flag_data:
    c.execute("INSERT INTO flags (challenge_id, type, content, data) VALUES (?, ?, ?, ?)",
              (ch_id, f_type, content, data))

# 3. Update Hints
c.execute("DELETE FROM hints")
hints_data = [
    # Challenge 1
    ('Hint 1', 'standard', 1, "The author's first name is listed on the engineering blog ('Notes from the Perimeter') alongside his alias k3ss_void.", 10, '{"prerequisites": []}'),
    ('Hint 2', 'standard', 1, "His surname is indexed on the internal deploy audit paste for handle k3ss_void. Combine them to form his corporate email.", 20, '{"prerequisites": []}'),

    # Challenge 2
    ('Hint 1', 'standard', 2, "Juice Shop login is vulnerable to classic SQL injection in the email field.", 10, '{"prerequisites": []}'),
    ('Hint 2', 'standard', 2, "Once logged into the admin account, check the user profile section in the navigation menu.", 20, '{"prerequisites": []}'),

    # Challenge 3
    ('Hint 1', 'standard', 3, "Download evidence_photos.zip directly from Juice Shop while authenticated as admin, or use the challenge attachment.", 10, '{"prerequisites": []}'),
    ('Hint 2', 'standard', 3, "Use wordlist.txt with a password cracking utility to recover the password.", 20, '{"prerequisites": []}'),

    # Challenge 4
    ('Hint 1', 'standard', 4, "Filter paths in proxy_history.xml for /assets/public/images/products/ to inspect product image traffic.", 10, '{"prerequisites": []}'),
    ('Hint 2', 'standard', 4, "Count the frequency of requests for each product image to find the outlier.", 20, '{"prerequisites": []}'),

    # Challenge 5
    ('Hint 1', 'standard', 5, "Take the outlier product image from the decrypted Stage 3 archive.", 10, '{"prerequisites": []}'),
    ('Hint 2', 'standard', 5, "Steganography tooling can extract embedded payloads with an empty passphrase.", 20, '{"prerequisites": []}'),

    # Challenge 6
    ('Hint 1', 'standard', 6, "Filter packets in Wireshark for HTTP POST requests.", 10, '{"prerequisites": []}'),
    ('Hint 2', 'standard', 6, "Follow the TCP stream from source IP 10.5.5.15 to inspect the upload payload.", 20, '{"prerequisites": []}'),
    ('Hint 3', 'standard', 6, "Look for base64 encoded strings in the transmission headers or payload.", 20, '{"prerequisites": []}')
]


for title, h_type, ch_id, content, cost, reqs in hints_data:
    c.execute("INSERT INTO hints (title, type, challenge_id, content, cost, requirements) VALUES (?, ?, ?, ?, ?, ?)",
              (title, h_type, ch_id, content, cost, reqs))

conn.commit()
print("CTFd database successfully updated with all challenges, flags, and hints!")
