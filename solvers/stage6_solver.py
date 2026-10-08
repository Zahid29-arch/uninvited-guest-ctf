#!/usr/bin/env python3
"""
Stage 6 Solver - Network Traffic Analysis & Accomplice Attribution
Parses upload_capture.pcap, isolates the rogue HTTP POST upload from IP 10.5.5.15,
extracts the obfuscated operator token (Base64), and decodes the antagonist identity.
Flag: Victor Hale or uninvited{victor_hale}
"""

import os
import base64
import re
from scapy.all import rdpcap, TCP, IP, Raw

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, '..', 'stages', 'stage6_pcap', 'upload_capture.pcap'),
        os.path.join(script_dir, '..', 'platform', 'exchange-portal', 'public', 'upload_capture.pcap')
    ]

    pcap_path = None
    for c in candidates:
        if os.path.exists(c):
            pcap_path = c
            break

    if not pcap_path:
        print("[-] upload_capture.pcap not found.")
        return None

    print(f"[*] Parsing PCAP file: {pcap_path}...")
    packets = rdpcap(pcap_path)
    print(f"[*] Read {len(packets)} total frames.")

    upload_src_ip = None
    operator_token = None
    agent_alias = None

    for pkt in packets:
        if pkt.haslayer(TCP) and pkt.haslayer(Raw):
            payload = bytes(pkt[Raw].load)

            # Check for the rogue HTTP POST request
            if b'POST /upload' in payload:
                if pkt.haslayer(IP):
                    upload_src_ip = pkt[IP].src
                print(f"[+] Found Rogue HTTP POST Request!")
                print(f"[+] Exfiltration Source IP: {upload_src_ip}")

                # Extract header or form-data token
                text = payload.decode(errors='ignore')
                m_header = re.search(r'X-Exfil-Operator:\s*([A-Za-z0-9+/=]+)', text)
                m_alias = re.search(r'X-Agent-Alias:\s*([^\r\n]+)', text)
                m_body = re.search(r'"sender_identity"\s*:\s*"([A-Za-z0-9+/=]+)"', text)

                if m_header:
                    operator_token = m_header.group(1)
                elif m_body:
                    operator_token = m_body.group(1)

                if m_alias:
                    agent_alias = m_alias.group(1)

            # Check for server response token if not already found
            if not operator_token and b'received_from_token' in payload:
                text = payload.decode(errors='ignore')
                m_resp = re.search(r'"received_from_token"\s*:\s*"([A-Za-z0-9+/=]+)"', text)
                if m_resp:
                    operator_token = m_resp.group(1)

    antagonist_name = None
    if operator_token:
        try:
            decoded_name = base64.b64decode(operator_token).decode('utf-8', errors='ignore').strip()
            if decoded_name:
                antagonist_name = decoded_name
                print(f"[+] Extracted Transport Token: {operator_token}")
                print(f"[+] Decoded Accomplice Identity: {antagonist_name} (Alias: {agent_alias or 'DragonFly'})")
        except Exception as e:
            print(f"[-] Base64 decode failed: {e}")

    if antagonist_name:
        flag_clean = antagonist_name
        flag_wrapped = f"uninvited{{{antagonist_name.lower().replace(' ', '_')}}}"
        print(f"\n[SUCCESS] Stage 6 Solved!")
        print(f"Antagonist Name: {flag_clean}")
        print(f"Attacker Host IP: {upload_src_ip}")
        print(f"Flag (Standard): {flag_clean}")
        print(f"Flag (CTF format): {flag_wrapped}")
        return flag_clean
    else:
        print("[-] Antagonist could not be identified.")
        return None

if __name__ == '__main__':
    solve()
