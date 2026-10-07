#!/usr/bin/env python3
"""
Stage 6 Solver - Network Traffic Analysis & Accomplice Attribution
Parses upload_capture.pcap, isolates the HTTP POST upload transaction,
and identifies the antagonist / accomplice identity.
Flag: Victor Hale or uninvited{victor_hale}
"""

import os
import json
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
    antagonist_name = None

    for pkt in packets:
        if pkt.haslayer(TCP) and pkt.haslayer(Raw):
            payload = bytes(pkt[Raw].load)

            # Check for the rogue HTTP POST request
            if b'POST /upload' in payload:
                if pkt.haslayer(IP):
                    upload_src_ip = pkt[IP].src
                    print(f"[+] Found Rogue HTTP POST Request!")
                    print(f"[+] Exfiltration Source IP: {upload_src_ip}")

            # Check for the server response identifying the sender
            if b'received_from' in payload:
                text = payload.decode(errors='ignore')
                m = re.search(r'"received_from"\s*:\s*"([^"]+)"', text)
                if m:
                    antagonist_name = m.group(1)
                    print(f"[+] Found Antagonist Identity in API Receipt: {antagonist_name}")

    if not antagonist_name:
        # Fallback check if Victor Hale appears directly in bytes
        for pkt in packets:
            if pkt.haslayer(Raw) and b'Victor Hale' in bytes(pkt[Raw].load):
                antagonist_name = "Victor Hale"
                break

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
