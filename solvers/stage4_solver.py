#!/usr/bin/env python3
"""
Stage 4 Solver - Web Traffic Forensics (Burp Suite Proxy History)
Analyzes proxy_history.xml to discover the most clicked/requested Juice Shop product image.
Flag: apple_juice.jpg or uninvited{apple_juice.jpg}
"""

import os
import xml.etree.ElementTree as ET
from collections import Counter

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stage4_dir = os.path.join(script_dir, '..', 'stages', 'stage4_forensics')
    xml_path = os.path.join(stage4_dir, 'proxy_history.xml')

    if not os.path.exists(xml_path):
        print(f"[-] Missing proxy history file: {xml_path}")
        return None

    print(f"[*] Analyzing Burp Proxy log: {xml_path}...")
    
    tree = ET.parse(xml_path)
    root = tree.getroot()

    path_counter = Counter()

    for item in root.findall('item'):
        url_elem = item.find('url')
        path_elem = item.find('path')

        endpoint = ''
        if path_elem is not None and path_elem.text:
            endpoint = path_elem.text
        elif url_elem is not None and url_elem.text:
            endpoint = url_elem.text

        # Count jpg / image assets
        if endpoint:
            clean_path = endpoint.split('?')[0]
            if clean_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                filename = os.path.basename(clean_path)
                path_counter[filename] += 1

    print("\n[*] Image Access Distribution:")
    for img, count in path_counter.most_common():
        print(f"    - {img:<25}: {count} requests")

    top_image, top_count = path_counter.most_common(1)[0]
    flag_clean = top_image
    flag_wrapped = f"uninvited{{{top_image}}}"

    print(f"\n[SUCCESS] Stage 4 Solved!")
    print(f"Target Outlier Image: {flag_clean} (Accessed {top_count} times)")
    print(f"Flag (Standard): {flag_clean}")
    print(f"Flag (CTF format): {flag_wrapped}")
    return flag_clean

if __name__ == '__main__':
    solve()
