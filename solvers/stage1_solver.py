#!/usr/bin/env python3
"""
Stage 1 Solver - OSINT & Multi-Source Identity Correlation
Author: Member 2 (IT24100066) - Challenge Design A Lead

Methodology:
1. Inspects blog_about.html to find the first name of lead architect handle 'k3ss_void' -> 'Adrian'.
2. Inspects leaked_paste.html to find the surname corresponding to handle 'k3ss_void' -> 'Kessler'.
3. Correlates the identity: Adrian Kessler.
4. Derives the internal corporate email: adrian.kessler@uninvited.local based on standard company policy.

Accepted Flags: Adrian Kessler, uninvited{adrian_kessler}, adrian.kessler@uninvited.local
"""

import os
import re
import sys
import argparse

def solve(verbose=True):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stage1_dir = os.path.join(script_dir, '..', 'stages', 'stage1_osint')
    
    blog_path = os.path.join(stage1_dir, 'blog_about.html')
    paste_path = os.path.join(stage1_dir, 'leaked_paste.html')
    
    first_name = None
    last_name = None
    
    # 1. Extract first name associated with k3ss_void from team blog
    if os.path.exists(blog_path):
        with open(blog_path, 'r', encoding='utf-8', errors='ignore') as f:
            blog_content = f.read()
            m_first = re.search(r'<span>([A-Za-z]+)</span>\s*<span class="team-handle">k3ss_void</span>', blog_content)
            if not m_first:
                m_first = re.search(r'([A-Za-z]+)\s*\([^\)]*k3ss_void[^\)]*\)', blog_content)
            if m_first:
                first_name = m_first.group(1).strip()
                if verbose:
                    print(f"[+] [OSINT] Identified First Name from team blog: {first_name}")

    # 2. Extract surname associated with k3ss_void from leaked staff roster
    if os.path.exists(paste_path):
        with open(paste_path, 'r', encoding='utf-8', errors='ignore') as f:
            paste_content = f.read()
            m_last = re.search(r'\|\s*([A-Za-z]+)\s*\|\s*k3ss_void', paste_content)
            if not m_last:
                m_last = re.search(r'Surname:\s*([A-Za-z]+)[^>]*Handle:\s*k3ss_void', paste_content)
            if m_last:
                last_name = m_last.group(1).strip()
                if verbose:
                    print(f"[+] [OSINT] Identified Surname from leaked audit roster: {last_name}")

    if first_name and last_name:
        full_name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}@uninvited.local"
        flag_clean = full_name
        flag_wrapped = f"uninvited{{{full_name.lower().replace(' ', '_')}}}"
        
        if verbose:
            print(f"\n[SUCCESS] Stage 1 Solved!")
            print(f"Target Identity : {full_name}")
            print(f"Corporate Email : {email}")
            print(f"Flag (Standard) : {flag_clean}")
            print(f"Flag (Wrapped)  : {flag_wrapped}")
        return {
            "name": full_name,
            "email": email,
            "flag": flag_clean,
            "flag_wrapped": flag_wrapped
        }
    else:
        if verbose:
            print("[-] Error: Unable to correlate OSINT artifacts.")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Stage 1 Solver (Member 2)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode")
    args = parser.parse_args()
    
    result = solve(verbose=not args.quiet)
    if result:
        sys.exit(0)
    else:
        sys.exit(1)
