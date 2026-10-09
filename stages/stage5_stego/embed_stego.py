#!/usr/bin/env python3
"""
Challenge Generation Script: Stage 5 (Hidden in Plain Sight)
Embeds the covert Exchange Portal URL (link.txt) into the carrier image
'apple_juice.jpg' using Steghide with an empty passphrase.
"""

import os
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COVER_IMAGE = os.path.join(SCRIPT_DIR, 'apple_juice.jpg')
PAYLOAD_FILE = os.path.join(SCRIPT_DIR, 'link.txt')

def embed_payload():
    print(f"[*] Embedding covert payload from {PAYLOAD_FILE} into {COVER_IMAGE}...")
    
    # Ensure payload exists
    if not os.path.exists(PAYLOAD_FILE):
        with open(PAYLOAD_FILE, 'w') as f:
            f.write('http://localhost:8086')
            
    # Try native steghide
    steghide_cmd = shutil.which('steghide')
    if steghide_cmd:
        print("[*] Using native steghide binary...")
        cmd = [steghide_cmd, 'embed', '-cf', COVER_IMAGE, '-ef', PAYLOAD_FILE, '-p', '', '-f']
        subprocess.run(cmd, check=True)
        print("[+] Embedded covert payload successfully via native steghide!")
        return

    # Fallback to docker container
    docker_cmd = shutil.which('docker')
    if docker_cmd:
        print("[*] Native steghide not found. Using Docker container fallback...")
        abs_dir = SCRIPT_DIR.replace('\\', '/')
        if abs_dir.startswith('C:'):
            abs_dir = '/c' + abs_dir[2:]
            
        docker_run = [
            'docker', 'run', '--rm',
            '-v', f"{SCRIPT_DIR}:/data",
            '-w', '/data',
            'debian:bookworm-slim',
            'bash', '-c',
            "sed -i 's|http://|https://|g' /etc/apt/sources.list.d/debian.sources && "
            "apt-get -o Acquire::https::Verify-Peer=false update && "
            "apt-get -o Acquire::https::Verify-Peer=false install -y steghide && "
            "steghide embed -cf apple_juice.jpg -ef link.txt -p '' -f"
        ]
        res = subprocess.run(docker_run, capture_output=True, text=True)
        if res.returncode == 0:
            print("[+] Embedded covert payload successfully via Docker steghide container!")
        else:
            print(f"[!] Docker steghide failed:\n{res.stderr}")
    else:
        print("[!] Neither steghide nor docker is available in PATH.")

if __name__ == '__main__':
    embed_payload()
