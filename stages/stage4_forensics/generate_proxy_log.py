#!/usr/bin/env python3
"""
Burp Suite Proxy History Generator for OWASP Juice Shop Traffic Analysis
Generates realistic Burp Suite XML export (proxy_history.xml) where:
- juice-shop on port 3000 is browsed
- /assets/public/images/products/apple_juice.jpg is clicked/requested 45 times (Outlier)
- other product images are requested 2-4 times each (Decoys)
- standard API endpoints (/rest/products/search, /api/Challenges, etc.) are included
"""

import os
import base64
import random
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_proxy_history():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_xml = os.path.join(script_dir, 'proxy_history.xml')

    items = []

    products = [
        ("apple_juice.jpg", 45),          # Outlier Flag!
        ("orange_juice.jpg", 4),
        ("banana_juice.jpg", 3),
        ("eggfruit_juice.jpg", 3),
        ("lemon_juice.jpg", 2),
        ("green_smoothie.jpg", 3),
        ("raspberry_juice.jpg", 2),
        ("pomegranate_drink.jpg", 4),
        ("quince.jpg", 2),
        ("sea_buckthorn_juice.jpg", 3)
    ]

    base_time_sec = 1759000000 # Sep 2026

    # Generate image request items
    for img_name, count in products:
        for i in range(count):
            t_sec = base_time_sec + random.randint(100, 36000)
            items.append({
                "type": "image",
                "filename": img_name,
                "path": f"/assets/public/images/products/{img_name}",
                "time_sec": t_sec,
                "method": "GET"
            })

    # Add background API traffic
    api_endpoints = [
        "/rest/products/search?q=",
        "/rest/products/search?q=juice",
        "/api/Challenges/",
        "/rest/admin/application-version",
        "/rest/user/whoami",
        "/api/Feedbacks/",
        "/rest/captcha/",
        "/api/BasketItems/1",
        "/rest/track-order/5267-3392"
    ]

    for ep in api_endpoints:
        for _ in range(random.randint(2, 6)):
            t_sec = base_time_sec + random.randint(50, 35000)
            items.append({
                "type": "api",
                "path": ep,
                "time_sec": t_sec,
                "method": "GET"
            })

    # Sort items chronologically
    items.sort(key=lambda x: x["time_sec"])

    root = ET.Element("items", {
        "burpVersion": "2026.1.1",
        "exportTime": "Sun Sep 27 18:00:00 UTC 2026"
    })

    host = "localhost"
    port = "3000"

    for entry in items:
        item = ET.SubElement(root, "item")
        
        path = entry["path"]
        url = f"http://{host}:{port}{path}"
        method = entry["method"]

        time_str = "Sun Sep 27 14:00:00 UTC 2026"
        ET.SubElement(item, "time").text = time_str
        ET.SubElement(item, "url").text = url
        h_elem = ET.SubElement(item, "host", {"ip": "127.0.0.1"})
        h_elem.text = host
        ET.SubElement(item, "port").text = port
        ET.SubElement(item, "protocol").text = "http"
        ET.SubElement(item, "method").text = method
        ET.SubElement(item, "path").text = path
        
        ext = path.split('?')[0].split('.')[-1] if '.' in path else ''
        ET.SubElement(item, "extension").text = ext

        req_raw = (
            f"{method} {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\n"
            f"Accept: */*\r\n"
            f"Referer: http://{host}:{port}/\r\n"
            f"Connection: close\r\n\r\n"
        ).encode('utf-8')
        req_b64 = base64.b64encode(req_raw).decode('utf-8')
        ET.SubElement(item, "request", {"base64": "true"}).text = req_b64

        ET.SubElement(item, "status").text = "200"
        
        if entry["type"] == "image":
            resp_raw = (
                f"HTTP/1.1 200 OK\r\n"
                f"Server: Express\r\n"
                f"Content-Type: image/jpeg\r\n"
                f"Content-Length: 12004\r\n"
                f"Connection: close\r\n\r\n"
                f"[BINARY IMAGE DATA: {entry['filename']}]"
            ).encode('utf-8')
            mimetype = "JPEG"
            resplen = "12004"
        else:
            resp_raw = (
                f"HTTP/1.1 200 OK\r\n"
                f"Server: Express\r\n"
                f"Content-Type: application/json\r\n"
                f"Content-Length: 42\r\n"
                f"Connection: close\r\n\r\n"
                f'{{"status":"success","data":[]}}'
            ).encode('utf-8')
            mimetype = "JSON"
            resplen = "142"

        resp_b64 = base64.b64encode(resp_raw).decode('utf-8')
        ET.SubElement(item, "responselength").text = resplen
        ET.SubElement(item, "mimetype").text = mimetype
        ET.SubElement(item, "response", {"base64": "true"}).text = resp_b64
        ET.SubElement(item, "comment").text = ""

    xml_str = ET.tostring(root, encoding='utf-8')
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ", encoding="utf-8")

    with open(output_xml, 'wb') as f:
        f.write(pretty_xml)

    print(f"[+] Successfully generated {output_xml}")
    print(f"[+] Total items logged: {len(items)}")

if __name__ == '__main__':
    generate_proxy_history()
