import sqlite3

conn = sqlite3.connect('/opt/CTFd/CTFd/ctfd.db')
c = conn.cursor()

# 1. Update Challenge Descriptions
c.execute("""UPDATE challenges SET description = ? WHERE id = 1""", (
    "A rogue engineer calling himself 'k3ss_void' has been orchestrating the uninvited infrastructure. Investigate the public footprint across his team blog, leaked audit logs, and underground forum activity. Identify his real identity and internal corporate email address. Keep the email for the next stage!\n\nFlag format: Adrian Kessler or uninvited{adrian_kessler} (or adrian.kessler@uninvited.local)",
))

c.execute("""UPDATE challenges SET description = ? WHERE id = 2""", (
    "Use the corporate email discovered in Stage 1 to access the administrator account on the OWASP Juice Shop portal at http://localhost:3000. Exploit the classic authentication vulnerability (SQL Injection) in the login portal. Once logged into the admin dashboard, inspect the user profile section to confirm the administrator username.\n\nFlag format: adrian.kessler or uninvited{adrian.kessler}",
))

c.execute("""UPDATE challenges SET description = ? WHERE id = 3""", (
    "As the administrator on OWASP Juice Shop (http://localhost:3000), access the restricted Evidence Vault backup to download the encrypted archive evidence_photos.zip (also attached below). The archive contains confidential case notes and Juice Shop product images. Use the provided wordlist to recover Adrian's master passphrase.\n\nFlag format: Kessler123! or uninvited{Kessler123!}",
))

c.execute("""UPDATE challenges SET description = ? WHERE id = 4""", (
    "Analyze the provided Burp Suite proxy history log (proxy_history.xml) to audit administrator activity on OWASP Juice Shop. Identify which product image on the Juice Shop website was requested/clicked significantly more than any other image. Compare the filename against the decrypted product images from Stage 3's archive!\n\nFlag format: apple_juice.jpg or uninvited{apple_juice.jpg}",
))

c.execute("""UPDATE challenges SET description = ? WHERE id = 5""", (
    "Take the outlier product image identified in Stage 4 (apple_juice.jpg) from the decrypted Stage 3 archive. An accomplice covertly embedded access details inside this image using Steghide. Extract the hidden payload to discover the secret URL of the internal Exchange Portal!\n\nTooling Commands:\n- Linux/WSL: sudo apt-get install steghide then: steghide extract -sf apple_juice.jpg -p ''\n- Docker: docker run --rm -v $(pwd):/data -w /data debian:bookworm-slim sh -c 'apt-get update -qq && apt-get install -y -qq steghide >/dev/null && steghide extract -sf apple_juice.jpg -p \"\" && cat link.txt'\n- Windows: Use steghide.exe or WSL.\n\nFlag format: http://localhost:8086 or uninvited{http://localhost:8086}",
))

c.execute("""UPDATE challenges SET description = ? WHERE id = 6""", (
    "Log into The Exchange Portal at http://localhost:8086 using Adrian Kessler's credentials (adrian.kessler@uninvited.local / Kessler123!). Retrieve the forensic network capture upload_capture.pcap. Perform packet inspection on rogue HTTP POST exfiltration traffic to uncover the real identity of the external culprit/accomplice operating under the alias 'DragonFly'.\n\nFlag format: Victor Hale or uninvited{victor_hale}",
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
    ('Hint 1', 'standard', 1, "The author's first name is listed on the engineering blog ('Notes from the Perimeter') alongside his alias k3ss_void.", 0, '{"prerequisites": []}'),
    ('Hint 2', 'standard', 1, "His surname is indexed on the internal deploy audit paste for handle k3ss_void. Combine them to form his email using {firstname}.{lastname}@uninvited.local.", 0, '{"prerequisites": []}'),

    # Challenge 2
    ('Hint 1', 'standard', 2, "Juice Shop login is vulnerable to classic SQL injection in the email field: adrian.kessler@uninvited.local'--", 0, '{"prerequisites": []}'),
    ('Hint 2', 'standard', 2, "Once logged in, check the user profile section in the navigation menu to see the username: adrian.kessler", 0, '{"prerequisites": []}'),

    # Challenge 3
    ('Hint 1', 'standard', 3, "Download evidence_photos.zip directly from Juice Shop at /rest/admin/evidence_photos.zip while authenticated as admin, or use the challenge attachment.", 0, '{"prerequisites": []}'),
    ('Hint 2', 'standard', 3, "Use wordlist.txt with a zip cracking tool (python zipfile, fcrackzip, or john/zip2john) to recover the password.", 0, '{"prerequisites": []}'),

    # Challenge 4
    ('Hint 1', 'standard', 4, "Filter paths in proxy_history.xml for /assets/public/images/products/ to count how many times each product image was requested.", 0, '{"prerequisites": []}'),
    ('Hint 2', 'standard', 4, "One product image (apple_juice.jpg) has 45 requests, while other product images only have 2 to 4 requests.", 0, '{"prerequisites": []}'),

    # Challenge 5
    ('Hint 1', 'standard', 5, "Take apple_juice.jpg from the decrypted Stage 3 archive.", 0, '{"prerequisites": []}'),
    ('Hint 2', 'standard', 5, "Run 'steghide extract -sf apple_juice.jpg -p \"\"' with an empty passphrase. It will extract link.txt containing the hidden URL.", 0, '{"prerequisites": []}'),

    # Challenge 6
    ('Hint 1', 'standard', 6, "Filter packets in Wireshark with: http.request.method == \"POST\"", 0, '{"prerequisites": []}'),
    ('Hint 2', 'standard', 6, "Follow the TCP stream from source IP 10.5.5.15 to inspect the upload payload.", 0, '{"prerequisites": []}'),
    ('Hint 3', 'standard', 6, "The operator token 'VmljdG9yIEhhbGU=' is Base64 encoded. Decode it to find the accomplice's real name.", 0, '{"prerequisites": []}')
]

for title, h_type, ch_id, content, cost, reqs in hints_data:
    c.execute("INSERT INTO hints (title, type, challenge_id, content, cost, requirements) VALUES (?, ?, ?, ?, ?, ?)",
              (title, h_type, ch_id, content, cost, reqs))

conn.commit()
print("CTFd database successfully updated with all challenges, flags, and hints!")
