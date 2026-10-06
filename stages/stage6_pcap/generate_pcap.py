from scapy.all import IP, TCP, Ether, Raw, wrpcap

# Generate background noise packets
noise1 = Ether()/IP(dst='8.8.8.8')/TCP(dport=443)
noise2 = Ether()/IP(dst='1.1.1.1')/TCP(dport=80)

# Generate the specific Stage 6 upload packet from Victor Hale (DragonFly)
# Source IP must be 10.5.5.15 as specified in the storyline[cite: 18]
payload = b'POST /upload HTTP/1.1\r\nHost: exchange-portal.local\r\n\r\nfile=consignment_new.jpg'
target_pkt = Ether()/IP(src='10.5.5.15', dst='192.168.1.50')/TCP(sport=54321, dport=8086)/Raw(load=payload)

# Write to PCAP file
wrpcap('/out/upload_capture.pcap', [noise1, noise2, target_pkt, noise1])
print('PCAP generated successfully.')
