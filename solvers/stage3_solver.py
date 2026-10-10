#!/usr/bin/env python3
"""
Stage 3 Solver - Cryptographic Evidence Archive Password Cracking
Author: Member 2 (IT24100066) - Challenge Design A Lead

Methodology:
1. Locates encrypted archive 'evidence_photos.zip' (downloaded from Juice Shop Admin endpoint).
2. Reads targeted dictionary wordlist ('wordlist.txt').
3. Conducts high-speed dictionary attack against standard Zip encryption.
4. Identifies valid password: 'Kessler123!'.
5. Extracts and decrypts confidential evidence photos.
"""

import os
import sys
import zipfile
import argparse

def solve(verbose=True):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stage3_dir = os.path.join(script_dir, '..', 'stages', 'stage3_crypto')
    
    zip_path = os.path.join(stage3_dir, 'evidence_photos.zip')
    wordlist_path = os.path.join(stage3_dir, 'wordlist.txt')
    
    if not os.path.exists(zip_path):
        if verbose:
            print(f"[-] Error: {zip_path} not found.")
        return None
    if not os.path.exists(wordlist_path):
        if verbose:
            print(f"[-] Error: {wordlist_path} not found.")
        return None

    if verbose:
        print(f"[*] Loading encrypted archive: {os.path.basename(zip_path)}")
        print(f"[*] Targeting wordlist: {os.path.basename(wordlist_path)}")

    found_password = None
    with zipfile.ZipFile(zip_path, 'r') as zf:
        namelist = zf.namelist()
        test_file = namelist[0] if namelist else None
        
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wl:
            for line in wl:
                pwd = line.strip()
                if not pwd:
                    continue
                try:
                    zf.read(test_file, pwd=pwd.encode('utf-8'))
                    found_password = pwd
                    break
                except (RuntimeError, zipfile.BadZipFile):
                    continue

    if found_password:
        flag_clean = found_password
        flag_wrapped = f"uninvited{{{found_password}}}"
        if verbose:
            print(f"\n[SUCCESS] Stage 3 Solved!")
            print(f"[+] Archive Password Cracked : {found_password}")
            print(f"[+] Total Decrypted Files    : {len(namelist)}")
            print(f"Flag (Standard)              : {flag_clean}")
            print(f"Flag (Wrapped)               : {flag_wrapped}")
        return {
            "password": found_password,
            "flag": flag_clean,
            "flag_wrapped": flag_wrapped
        }
    else:
        if verbose:
            print("[-] Dictionary exhausted: Password not found.")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Stage 3 Solver (Member 2)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode")
    args = parser.parse_args()

    result = solve(verbose=not args.quiet)
    if result:
        sys.exit(0)
    else:
        sys.exit(1)
