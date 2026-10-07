#!/usr/bin/env python3
"""
Stage 3 Solver - Cryptography & Archive Password Recovery
Cracks evidence_photos.zip using the provided dictionary wordlist.txt to recover Adrian Kessler's password.
Flag: Kessler123! or uninvited{Kessler123!}
"""

import os
import zipfile

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stage3_dir = os.path.join(script_dir, '..', 'stages', 'stage3_crypto')
    zip_path = os.path.join(stage3_dir, 'evidence_photos.zip')
    wordlist_path = os.path.join(stage3_dir, 'wordlist.txt')

    if not os.path.exists(zip_path) or not os.path.exists(wordlist_path):
        print(f"[-] Missing files in {stage3_dir}")
        return None

    print(f"[*] Attacking encrypted archive: {zip_path}")
    print(f"[*] Wordlist: {wordlist_path}")

    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = [line.strip() for line in f if line.strip()]

    print(f"[*] Loaded {len(passwords)} candidate passwords.")

    with zipfile.ZipFile(zip_path) as z:
        for pwd in passwords:
            try:
                # Test decrypting the first member in the zip
                test_file = z.namelist()[0]
                content = z.read(test_file, pwd=pwd.encode('utf-8'))
                
                flag_clean = pwd
                flag_wrapped = f"uninvited{{{pwd}}}"
                print(f"\n[SUCCESS] Password Cracked!")
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
