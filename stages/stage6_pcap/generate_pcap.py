#!/usr/bin/env python3
"""
Synthetic PCAP Generator using Scapy
Generates: upload_capture.pcap
Simulates background network noise (DNS queries/responses, TCP SYN/ACK handshakes,
DHCP leases, ARP queries, routine HTTP GETs) hiding exactly ONE rogue HTTP POST request to an /upload endpoint
originating from IP 10.5.5.15 (MAC: 00:1c:42:8a:b1:15, Hostname: VH-WORKSTATION),
representing the target accomplice 'Victor Hale'.
"""

import logging
# Suppress scapy runtime warnings
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import os
import random
from scapy.all import (
    Ether, IP, TCP, UDP, DNS, DNSQR, DNSRR, BOOTP, DHCP, ARP, Raw, wrpcap
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "upload_capture.pcap")

# Network Node Mapping
GATEWAY_IP = "10.5.5.1"
GATEWAY_MAC = "52:54:00:12:34:01"

SERVER_IP = "10.5.5.80"
SERVER_MAC = "52:54:00:12:34:80"
SERVER_PORT = 80

# Target Host (Victor Hale)
TARGET_IP = "10.5.5.15"
TARGET_MAC = "00:1c:42:8a:b1:15"
TARGET_HOSTNAME = "VH-WORKSTATION"
TARGET_PORT = 52134

# Decoy Background Hosts
NOISE_HOSTS = [
    {"ip": "10.5.5.21", "mac": "00:1c:42:8a:b1:21", "hostname": "SEC-DESK-21"},
    {"ip": "10.5.5.34", "mac": "00:1c:42:8a:b1:34", "hostname": "OPS-NODE-34"},
    {"ip": "10.5.5.42", "mac": "00:1c:42:8a:b1:42", "hostname": "BUILD-RUNNER-42"},
    {"ip": "10.5.5.58", "mac": "00:1c:42:8a:b1:58", "hostname": "QA-RELAY-58"}
]

DNS_DOMAINS = [
    ("exchange.uninvited.local", SERVER_IP),
    ("portal.uninvited.local", SERVER_IP),
    ("auth.uninvited.local", "10.5.5.85"),
    ("ntp.pool.org", "162.159.200.1"),
    ("api.internal.local", "10.5.5.90"),
    ("updates.corp.local", "10.5.5.95")
]

def create_dns_transaction(client_ip, client_mac, qname, answer_ip, base_time):
    """Creates a paired DNS query and answer."""
    packets = []
    txid = random.randint(1000, 65000)
    sport = random.randint(40000, 65000)

    # DNS Query
    q_pkt = (
        Ether(src=client_mac, dst=GATEWAY_MAC) /
        IP(src=client_ip, dst=GATEWAY_IP) /
        UDP(sport=sport, dport=53) /
        DNS(id=txid, rd=1, qd=DNSQR(qname=qname))
    )
    q_pkt.time = base_time
    packets.append(q_pkt)

    # DNS Response
    r_pkt = (
        Ether(src=GATEWAY_MAC, dst=client_mac) /
        IP(src=GATEWAY_IP, dst=client_ip) /
        UDP(sport=53, dport=sport) /
        DNS(
            id=txid, qr=1, rd=1, ra=1,
            qd=DNSQR(qname=qname),
            an=DNSRR(rrname=qname, ttl=300, rdata=answer_ip)
        )
    )
    r_pkt.time = base_time + random.uniform(0.005, 0.025)
    packets.append(r_pkt)

    return packets

def create_dhcp_lease(client_ip, client_mac, hostname, base_time):
    """Creates DHCP Request and ACK binding MAC and IP to a Hostname."""
    packets = []
    mac_bytes = bytes.fromhex(client_mac.replace(":", ""))

    # DHCP Request
    req = (
        Ether(src=client_mac, dst="ff:ff:ff:ff:ff:ff") /
        IP(src="0.0.0.0", dst="255.255.255.255") /
        UDP(sport=68, dport=67) /
        BOOTP(chaddr=mac_bytes + b'\x00'*10, xid=0x4291823) /
        DHCP(options=[
            ("message-type", "request"),
            ("requested_addr", client_ip),
            ("hostname", hostname),
            ("end")
        ])
    )
    req.time = base_time
    packets.append(req)

    # DHCP ACK
    ack = (
        Ether(src=GATEWAY_MAC, dst=client_mac) /
        IP(src=GATEWAY_IP, dst=client_ip) /
        UDP(sport=67, dport=68) /
        BOOTP(chaddr=mac_bytes + b'\x00'*10, yiaddr=client_ip, xid=0x4291823) /
        DHCP(options=[
            ("message-type", "ack"),
            ("server_id", GATEWAY_IP),
            ("lease_time", 86400),
            ("hostname", hostname),
            ("end")
        ])
    )
    ack.time = base_time + 0.005
    packets.append(ack)
    return packets

def create_arp_resolution(client_ip, client_mac, base_time):
    """Creates an ARP who-has query and is-at reply."""
    packets = []
    # Request
    req = (
        Ether(src=GATEWAY_MAC, dst="ff:ff:ff:ff:ff:ff") /
        ARP(op=1, hwsrc=GATEWAY_MAC, psrc=GATEWAY_IP, hwdst="00:00:00:00:00:00", pdst=client_ip)
    )
    req.time = base_time
    packets.append(req)

    # Reply
    rep = (
        Ether(src=client_mac, dst=GATEWAY_MAC) /
        ARP(op=2, hwsrc=client_mac, psrc=client_ip, hwdst=GATEWAY_MAC, pdst=GATEWAY_IP)
    )
    rep.time = base_time + 0.002
    packets.append(rep)
    return packets

def create_tcp_http_get_session(client_ip, client_mac, path, base_time):
    """Creates a standard TCP 3-way handshake, HTTP GET request/response, and teardown."""
    packets = []
    sport = random.randint(40000, 65000)
    c_seq = random.randint(100000, 900000)
    s_seq = random.randint(100000, 900000)

    t = base_time

    # 1. SYN
    syn = Ether(src=client_mac, dst=SERVER_MAC)/IP(src=client_ip, dst=SERVER_IP)/TCP(sport=sport, dport=SERVER_PORT, flags="S", seq=c_seq)
    syn.time = t
    packets.append(syn)
    c_seq += 1

    # 2. SYN/ACK
    t += random.uniform(0.001, 0.004)
    syn_ack = Ether(src=SERVER_MAC, dst=client_mac)/IP(src=SERVER_IP, dst=client_ip)/TCP(sport=SERVER_PORT, dport=sport, flags="SA", seq=s_seq, ack=c_seq)
    syn_ack.time = t
    packets.append(syn_ack)
    s_seq += 1

    # 3. ACK
    t += random.uniform(0.001, 0.003)
    ack1 = Ether(src=client_mac, dst=SERVER_MAC)/IP(src=client_ip, dst=SERVER_IP)/TCP(sport=sport, dport=SERVER_PORT, flags="A", seq=c_seq, ack=s_seq)
    ack1.time = t
    packets.append(ack1)

    # 4. HTTP GET Request
    t += random.uniform(0.002, 0.006)
    get_payload = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: exchange.uninvited.local\r\n"
        f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
        f"Accept: text/html,application/xhtml+xml,*/*\r\n"
        f"Connection: keep-alive\r\n\r\n"
    ).encode()

    get_pkt = Ether(src=client_mac, dst=SERVER_MAC)/IP(src=client_ip, dst=SERVER_IP)/TCP(sport=sport, dport=SERVER_PORT, flags="PA", seq=c_seq, ack=s_seq)/Raw(load=get_payload)
    get_pkt.time = t
    packets.append(get_pkt)
    c_seq += len(get_payload)

    # 5. Server ACK
    t += random.uniform(0.001, 0.003)
    ack2 = Ether(src=SERVER_MAC, dst=client_mac)/IP(src=SERVER_IP, dst=client_ip)/TCP(sport=SERVER_PORT, dport=sport, flags="A", seq=s_seq, ack=c_seq)
    ack2.time = t
    packets.append(ack2)

    # 6. HTTP 200 OK Response
    t += random.uniform(0.004, 0.015)
    resp_body = b"<html><body>OK</body></html>"
    resp_payload = (
        b"HTTP/1.1 200 OK\r\n"
        b"Server: nginx/1.24.0\r\n"
        b"Content-Type: text/html; charset=UTF-8\r\n"
        b"Content-Length: " + str(len(resp_body)).encode() + b"\r\n"
        b"Connection: keep-alive\r\n\r\n" + resp_body
    )
    resp_pkt = Ether(src=SERVER_MAC, dst=client_mac)/IP(src=SERVER_IP, dst=client_ip)/TCP(sport=SERVER_PORT, dport=sport, flags="PA", seq=s_seq, ack=c_seq)/Raw(load=resp_payload)
    resp_pkt.time = t
    packets.append(resp_pkt)
    s_seq += len(resp_payload)

    # 7. Client ACK
    t += random.uniform(0.001, 0.003)
    ack3 = Ether(src=client_mac, dst=SERVER_MAC)/IP(src=client_ip, dst=SERVER_IP)/TCP(sport=sport, dport=SERVER_PORT, flags="A", seq=c_seq, ack=s_seq)
    ack3.time = t
    packets.append(ack3)

    return packets

def create_target_upload_session(base_time):
    """
    Creates the target session from Victor Hale (10.5.5.15 / MAC 00:1c:42:8a:b1:15):
    - DHCP lease & ARP binding host 10.5.5.15 and MAC to VH-WORKSTATION
    - Pre-flight DNS
    - Full TCP handshake to SERVER_IP:80
    - Exactly ONE HTTP POST request to /upload
    - Operator token VmljdG9yIEhhbGU= (Victor Hale)
    - Clean connection teardown
    """
    packets = []
    sport = TARGET_PORT
    c_seq = 20491820
    s_seq = 80194820
    t = base_time

    # Pre-flight DHCP Lease & ARP
    dhcp_pkts = create_dhcp_lease(TARGET_IP, TARGET_MAC, TARGET_HOSTNAME, t)
    packets.extend(dhcp_pkts)
    t += 0.02

    arp_pkts = create_arp_resolution(TARGET_IP, TARGET_MAC, t)
    packets.extend(arp_pkts)
    t += 0.02

    # Pre-flight DNS for exchange.uninvited.local
    dns_pkts = create_dns_transaction(TARGET_IP, TARGET_MAC, "exchange.uninvited.local", SERVER_IP, t)
    packets.extend(dns_pkts)
    t += 0.05

    # 1. SYN
    syn = Ether(src=TARGET_MAC, dst=SERVER_MAC)/IP(src=TARGET_IP, dst=SERVER_IP)/TCP(sport=sport, dport=SERVER_PORT, flags="S", seq=c_seq)
    syn.time = t
    packets.append(syn)
    c_seq += 1

    # 2. SYN/ACK
    t += 0.002
    syn_ack = Ether(src=SERVER_MAC, dst=TARGET_MAC)/IP(src=SERVER_IP, dst=TARGET_IP)/TCP(sport=SERVER_PORT, dport=sport, flags="SA", seq=s_seq, ack=c_seq)
    syn_ack.time = t
    packets.append(syn_ack)
    s_seq += 1

    # 3. ACK
    t += 0.002
    ack1 = Ether(src=TARGET_MAC, dst=SERVER_MAC)/IP(src=TARGET_IP, dst=SERVER_IP)/TCP(sport=sport, dport=SERVER_PORT, flags="A", seq=c_seq, ack=s_seq)
    ack1.time = t
    packets.append(ack1)

    # 4. HTTP POST /upload by accomplice (10.5.5.15, MAC: 00:1c:42:8a:b1:15)
    t += 0.005
    boundary = "---------------------------39281749281739281749"
    post_body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"operator_token\"\r\n\r\n"
        f"VmljdG9yIEhhbGU=\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"destination_agent\"\r\n\r\n"
        f"Adrian Kessler <adrian.kessler@uninvited.local>\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"confidential_exfil_manifest.json\"\r\n"
        f"Content-Type: application/json\r\n\r\n"
        f'{{"manifest_id":"EXFIL-99201","sender_identity":"VmljdG9yIEhhbGU=","encoding":"base64","alias":"DragonFly","source_ip":"10.5.5.15","source_mac":"00:1c:42:8a:b1:15","device_hostname":"VH-WORKSTATION","status":"dispatched"}}\r\n'
        f"--{boundary}--\r\n"
    ).encode()

    post_headers = (
        f"POST /upload HTTP/1.1\r\n"
        f"Host: exchange.uninvited.local\r\n"
        f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36\r\n"
        f"X-Exfil-Operator: VmljdG9yIEhhbGU=\r\n"
        f"X-Host-IP: 10.5.5.15\r\n"
        f"X-Host-MAC: 00:1c:42:8a:b1:15\r\n"
        f"X-Device-Hostname: VH-WORKSTATION\r\n"
        f"X-Agent-Alias: DragonFly\r\n"
        f"Accept: application/json, text/plain, */*\r\n"
        f"Origin: http://exchange.uninvited.local\r\n"
        f"Referer: http://exchange.uninvited.local/portal\r\n"
        f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
        f"Content-Length: {len(post_body)}\r\n"
        f"Connection: keep-alive\r\n\r\n"
    ).encode()

    full_http_post = post_headers + post_body

    post_pkt = Ether(src=TARGET_MAC, dst=SERVER_MAC)/IP(src=TARGET_IP, dst=SERVER_IP)/TCP(sport=sport, dport=SERVER_PORT, flags="PA", seq=c_seq, ack=s_seq)/Raw(load=full_http_post)
    post_pkt.time = t
    packets.append(post_pkt)
    c_seq += len(full_http_post)

    # 5. Server TCP ACK
    t += 0.003
    ack2 = Ether(src=SERVER_MAC, dst=TARGET_MAC)/IP(src=SERVER_IP, dst=TARGET_IP)/TCP(sport=SERVER_PORT, dport=sport, flags="A", seq=s_seq, ack=c_seq)
    ack2.time = t
    packets.append(ack2)

    # 6. Server HTTP 200 OK Response
    t += 0.015
    resp_body = b'{"status":"success","upload_id":"UP-88412","received_from_ip":"10.5.5.15","received_from_mac":"00:1c:42:8a:b1:15","received_from_token":"VmljdG9yIEhhbGU=","encoding":"base64","file":"confidential_exfil_manifest.json"}'
    resp_payload = (
        b"HTTP/1.1 200 OK\r\n"
        b"Date: Sun, 27 Sep 2026 15:42:11 GMT\r\n"
        b"Server: nginx/1.24.0\r\n"
        b"Content-Type: application/json; charset=UTF-8\r\n"
        b"Content-Length: " + str(len(resp_body)).encode() + b"\r\n"
        b"Connection: keep-alive\r\n\r\n" + resp_body
    )
    resp_pkt = Ether(src=SERVER_MAC, dst=TARGET_MAC)/IP(src=SERVER_IP, dst=TARGET_IP)/TCP(sport=SERVER_PORT, dport=sport, flags="PA", seq=s_seq, ack=c_seq)/Raw(load=resp_payload)
    resp_pkt.time = t
    packets.append(resp_pkt)
    s_seq += len(resp_payload)

    # 7. Client ACK
    t += 0.002
    ack3 = Ether(src=TARGET_MAC, dst=SERVER_MAC)/IP(src=TARGET_IP, dst=SERVER_IP)/TCP(sport=sport, dport=SERVER_PORT, flags="A", seq=c_seq, ack=s_seq)
    ack3.time = t
    packets.append(ack3)

    # 8. Teardown (FIN/ACK)
    t += 0.05
    fin = Ether(src=TARGET_MAC, dst=SERVER_MAC)/IP(src=TARGET_IP, dst=SERVER_IP)/TCP(sport=sport, dport=SERVER_PORT, flags="FA", seq=c_seq, ack=s_seq)
    fin.time = t
    packets.append(fin)
    c_seq += 1

    t += 0.002
    fin_ack = Ether(src=SERVER_MAC, dst=TARGET_MAC)/IP(src=SERVER_IP, dst=TARGET_IP)/TCP(sport=SERVER_PORT, dport=sport, flags="FA", seq=s_seq, ack=c_seq)
    fin_ack.time = t
    packets.append(fin_ack)
    s_seq += 1

    t += 0.002
    final_ack = Ether(src=TARGET_MAC, dst=SERVER_MAC)/IP(src=TARGET_IP, dst=SERVER_IP)/TCP(sport=sport, dport=SERVER_PORT, flags="A", seq=c_seq, ack=s_seq)
    final_ack.time = t
    packets.append(final_ack)

    return packets

def generate_pcap():
    all_packets = []
    base_timestamp = 1790523600.0  # e.g. Sun, Sep 27 2026 15:40:00 UTC

    # 1. Background Noise: DHCP and DNS
    current_time = base_timestamp
    for host in NOISE_HOSTS:
        dhcp_noise = create_dhcp_lease(host["ip"], host["mac"], host["hostname"], current_time)
        all_packets.extend(dhcp_noise)
        current_time += random.uniform(0.1, 0.4)

    for _ in range(12):
        host = random.choice(NOISE_HOSTS)
        domain, ip = random.choice(DNS_DOMAINS)
        dns_batch = create_dns_transaction(host["ip"], host["mac"], domain, ip, current_time)
        all_packets.extend(dns_batch)
        current_time += random.uniform(0.5, 2.5)

    # 2. Background HTTP GET and TCP Handshake Noise
    decoy_paths = [
        "/", "/index.html", "/static/app.css", "/static/bundle.js",
        "/api/health", "/favicon.ico", "/gallery/catalog", "/assets/logo.png"
    ]
    for _ in range(10):
        host = random.choice(NOISE_HOSTS)
        path = random.choice(decoy_paths)
        http_batch = create_tcp_http_get_session(host["ip"], host["mac"], path, current_time)
        all_packets.extend(http_batch)
        current_time += random.uniform(1.0, 3.5)

    # 3. Inject TARGET HTTP POST from Victor Hale (10.5.5.15)
    target_time = current_time + random.uniform(1.0, 2.0)
    target_packets = create_target_upload_session(target_time)
    all_packets.extend(target_packets)
    current_time = target_time + 0.5

    # 4. Post-Target Noise
    for _ in range(8):
        host = random.choice(NOISE_HOSTS)
        path = random.choice(decoy_paths)
        http_batch = create_tcp_http_get_session(host["ip"], host["mac"], path, current_time)
        all_packets.extend(http_batch)
        current_time += random.uniform(1.0, 3.0)

    for _ in range(8):
        host = random.choice(NOISE_HOSTS)
        domain, ip = random.choice(DNS_DOMAINS)
        dns_batch = create_dns_transaction(host["ip"], host["mac"], domain, ip, current_time)
        all_packets.extend(dns_batch)
        current_time += random.uniform(0.4, 2.0)

    # Sort packets strictly chronologically by timestamp
    all_packets.sort(key=lambda p: float(p.time))

    # Write PCAP using Scapy
    wrpcap(OUTPUT_FILE, all_packets)

    print(f"[+] Successfully wrote {len(all_packets)} packets to '{OUTPUT_FILE}'.")
    
    # Verification
    post_count = 0
    post_ips = []
    for p in all_packets:
        if p.haslayer(Raw):
            load = p[Raw].load
            if b"POST " in load:
                post_count += 1
                if p.haslayer(IP):
                    post_ips.append((p[IP].src, p[IP].dst))

    print(f"[+] Total HTTP POST requests in capture: {post_count}")
    print(f"[+] POST Originating IP(s):             {post_ips}")
    assert post_count == 1, "There must be exactly ONE HTTP POST request."
    assert post_ips[0][0] == TARGET_IP, f"POST must originate from {TARGET_IP}."
    print(f"[+] Verified: Exactly one HTTP POST request from Victor Hale ({TARGET_IP}) to {SERVER_IP}.")

if __name__ == "__main__":
    generate_pcap()
