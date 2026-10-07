#!/usr/bin/env python3
"""
Stage 1 Solver - OSINT & Reconnaissance
Extracts the real name of target 'k3ss_void' / 'UninvitedGuest99' from OSINT artifacts.
Flag format: Adrian Kessler or uninvited{adrian_kessler}
"""

import os
import re

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stage1_dir = os.path.join(script_dir, '..', 'stages', 'stage1_osint')
    
    # Check leaked paste / blog / dump
    target_name = None
    files_to_check = ['leaked_paste.html', 'blog_about.html', 'paste_dump.txt']
    
    for filename in files_to_check:
        filepath = os.path.join(stage1_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Look for Adrian Kessler pattern
                m = re.search(r'Adrian\s+Kessler', content, re.IGNORECASE)
                if m:
                    target_name = m.group(0)
                    print(f"[+] Found Target Identity in {filename}: {target_name}")
                    break

    if target_name:
        flag_clean = target_name
        flag_wrapped = f"uninvited{{{target_name.lower().replace(' ', '_')}}}"
        print(f"\n[SUCCESS] Stage 1 Solved!")
        print(f"Target Name: {flag_clean}")
        print(f"Flag (Standard): {flag_clean}")
        print(f"Flag (CTF format): {flag_wrapped}")
        return flag_clean
    else:
        print("[-] Target name not found in Stage 1 files.")
        return None

if __name__ == '__main__':
    solve()
