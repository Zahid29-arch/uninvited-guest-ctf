#!/usr/bin/env python3
"""
Stage 1 Solver - OSINT & Multi-Source Identity Correlation
1. Inspects blog_about.html to find the first name of lead architect handle 'k3ss_void' -> 'Adrian'.
2. Inspects leaked_paste.html to find the surname corresponding to handle 'k3ss_void' -> 'Kessler'.
3. Correlates the identity: Adrian Kessler.
4. Derives the internal corporate email: adrian.kessler@uninvited.local based on standard company policy.
Flags accepted: Adrian Kessler, uninvited{adrian_kessler}, adrian.kessler@uninvited.local, uninvited{adrian.kessler@uninvited.local}
"""

import os
import re

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stage1_dir = os.path.join(script_dir, '..', 'stages', 'stage1_osint')
    
    blog_path = os.path.join(stage1_dir, 'blog_about.html')
    paste_path = os.path.join(stage1_dir, 'leaked_paste.html')
    
    first_name = None
    last_name = None
    
    # 1. Extract first name associated with k3ss_void from blog
    if os.path.exists(blog_path):
        with open(blog_path, 'r', encoding='utf-8', errors='ignore') as f:
            blog_content = f.read()
            # Pattern matching Adrian alongside k3ss_void
            m_first = re.search(r'<span>([A-Za-z]+)</span>\s*<span class="team-handle">k3ss_void</span>', blog_content)
            if not m_first:
                m_first = re.search(r'([A-Za-z]+)\s*\([^\)]*k3ss_void[^\)]*\)', blog_content)
            if m_first:
                first_name = m_first.group(1).strip()
                print(f"[+] Identified First Name from team blog: {first_name}")

    # 2. Extract surname associated with k3ss_void from leaked staff roster
    if os.path.exists(paste_path):
        with open(paste_path, 'r', encoding='utf-8', errors='ignore') as f:
            paste_content = f.read()
            # Pattern matching Kessler alongside k3ss_void in the roster
            m_last = re.search(r'\|\s*([A-Za-z]+)\s*\|\s*k3ss_void', paste_content)
            if not m_last:
                m_last = re.search(r'Surname:\s*([A-Za-z]+)[^>]*Handle:\s*k3ss_void', paste_content)
            if m_last:
                last_name = m_last.group(1).strip()
                print(f"[+] Identified Surname from leaked audit roster: {last_name}")

    if first_name and last_name:
        full_name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}@uninvited.local"
        flag_clean = full_name
        flag_wrapped = f"uninvited{{{full_name.lower().replace(' ', '_')}}}"
        
        print(f"\n[SUCCESS] Stage 1 Solved!")
        print(f"Target Identity : {full_name}")
        print(f"Corporate Email : {email}")
        print(f"Flag (Name)     : {flag_clean}")
        print(f"Flag (CTF fmt)  : {flag_wrapped}")
        print(f"Flag (Email)    : {email}")
        return full_name
    else:
        print(f"[-] Identity correlation failed: first={first_name}, last={last_name}")
        return None

if __name__ == '__main__':
    solve()
