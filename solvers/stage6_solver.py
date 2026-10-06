from scapy.all import rdpcap, TCP, IP, Raw

print('Parsing upload_capture.pcap...')
try:
    packets = rdpcap('../platform/exchange-portal/public/upload_capture.pcap')
    for pkt in packets:
        if pkt.haslayer(TCP) and pkt.haslayer(Raw):
            payload = pkt[Raw].load.decode(errors='ignore')
            if 'POST /upload' in payload:
                print('[+] Found Upload Request!')
                print(f'[+] True Source IP (DragonFly / Victor Hale): {pkt[IP].src}')
                print('Flag: CTF{UNINVITED_GUEST}')
                break
except FileNotFoundError:
    print('Error: upload_capture.pcap not found. Check the path.')
