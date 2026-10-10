# 🔬 Member 3: Challenge Design B — Stages 4, 5 & 6
### Student ID: Zahid29-arch (GitHub: https://github.com/Zahid29-arch)
### Module: SLIIT IE3132 Penetration Testing — Assignment 02
### Focus Area: Challenge Design B (Stages 4, 5 & 6), Forensics, Steganography & Network Packet Analysis

---

## 1. Executive Summary & Assigned Responsibilities

As **Member 3 (Repository Owner)**, I was responsible for the forensic storyline continuation, artifact synthesis, service implementation, and automated exploit development for **Challenge Design B**, comprising:
1. **Stage 4 (Digital Forensics)**: *Follow the Clicks* — Burp Suite HTTP proxy history analysis and outlier asset isolation.
2. **Stage 5 (Steganography)**: *Hidden in Plain Sight* — Steghide LSB payload extraction from evidence imagery.
3. **Stage 6 (Networking / Capstone)**: *Unmasking the Accomplice* — The Dark Exchange contraband portal and Wireshark PCAP multipart packet inspection.
4. **Automated Solvers & Hints**: Implementing reference exploit scripts (`solvers/stage4_solver.py`, `stage5_solver.py`, `stage6_solver.py`), hints, and reset capabilities.

---

## 2. Stage 4: Digital Forensics — Follow the Clicks

### A. How It Was Built
* **Synthesis Script**: `stages/stage4_forensics/generate_proxy_log.py`
* **Artifact**: `stages/stage4_forensics/proxy_history.xml` (114 KB of realistic Burp Suite XML proxy logs).
* **Vulnerability Logic**: Adrian Kessler's exfiltration activity focused on an outlier product image. In the proxy log, `apple_juice.jpg` exhibits disproportionate request spikes and anomalous cache behavior compared to other items.
* **Flag Placement**: The outlier image file $\to$ `apple_juice.jpg` (`uninvited{apple_juice.jpg}`).

### B. Live Solve Path
1. **Information Gathering**: Inspect XML elements using Python or text editor.
2. **Exploitation / Analysis**: Parse `<url>` nodes and count hit frequencies per `.jpg` resource:
   ```bash
   python3 -c "import xml.etree.ElementTree as ET, collections; root=ET.parse('proxy_history.xml').getroot(); c=collections.Counter([i.find('path').text.split('/')[-1] for i in root.findall('item') if '.jpg' in i.find('path').text]); print(c.most_common(1))"
   ```
3. **Result**: `apple_juice.jpg` has 87 requests (highest outlier).
4. **Automated Solver**: `solvers/stage4_solver.py` automatically parses XML and identifies the target asset.

---

## 3. Stage 5: Steganography — Hidden in Plain Sight

### A. How It Was Built
* **Carrier Image**: `stages/stage5_stego/apple_juice.jpg` (retrieved from Stage 3's evidence archive and isolated in Stage 4).
* **Stego Tool**: Steghide (`embed_stego.py`). Injected secret URL payload `http://localhost:8086` into JPEG DCT coefficients.
* **Passphrase**: Target password discovered in Stage 3 (`Kessler123!`).
* **Flag Placement**: Embedded contraband endpoint $\to$ `http://localhost:8086` (`uninvited{http://localhost:8086}`).

### B. Live Solve Path
1. **Tooling**: Steghide CLI or Python stego libraries.
2. **Extraction**:
   ```bash
   steghide extract -sf apple_juice.jpg -p "Kessler123!" -xf secret_url.txt
   cat secret_url.txt
   ```
3. **Result**: Extracted endpoint reveals: `http://localhost:8086`.
4. **Automated Solver**: `solvers/stage5_solver.py` runs extraction and parses the URL token.

---

## 4. Stage 6: Networking (Capstone) — Unmasking the Accomplice

### A. How It Was Built
* **Portal Service**: `platform/exchange-portal/` (Custom Node.js/Express service running on port `:8086`).
* **PCAP Trace Generator**: `stages/stage6_pcap/generate_pcap.py` synthesizes `upload_capture.pcap` with realistic background HTTP traffic, TCP handshakes, and a covert multipart upload.
* **Vulnerability**: Adrian Kessler exfiltrates encrypted project plans to his rogue accomplice `Victor Hale`. In the packet stream, a hidden HTTP POST request transmits a Base64-encoded collaborator identifier.
* **Flag Placement**: Accomplice identity $\to$ `Victor Hale` (`uninvited{victor_hale}`).

### B. Live Solve Path
1. **Access Exchange**: Navigate to `http://192.168.60.10:8086`, log in as `adrian.kessler@uninvited.local` / `Kessler123!`.
2. **Download Capture**: Download `upload_capture.pcap` from the repository file vault.
3. **Wireshark Analysis**:
   - Filter: `http.request.method == "POST"`
   - Follow TCP Stream on the multipart upload packet.
   - Inspect boundary headers to locate parameter: `X-Collaborator: VmljdG9yIEhhbGU=`
   - Base64 decode: `echo "VmljdG9yIEhhbGU=" | base64 -d` $\to$ `Victor Hale`.
4. **Automated Solver**: `solvers/stage6_solver.py` parses PCAP bytes with Scapy, extracts TCP streams, and decodes the accomplice name.

---

## 5. Hints & Stage Reset Policy

* **Stage 4 Hint (-10 pts)**: "Filter proxy requests by image extensions and count URI frequency."
* **Stage 5 Hint (-10 pts)**: "Use Steghide with the password discovered in Stage 3."
* **Stage 6 Hint (-20 pts)**: "Filter Wireshark for POST streams and decode Base64 payload headers."
* **Reset**: Integrated into `./reset.sh stage 4`, `./reset.sh stage 5`, `./reset.sh stage 6`.

---
*Authored by Member 3 (Zahid29-arch) — SLIIT IE3132 Penetration Testing.*
