# 🕵️ Uninvited Guest - CTF Challenge Suite

[![CTF Framework](https://img.shields.io/badge/Platform-CTFd-red.svg)](https://ctfd.io/)
[![Environment](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()

**Uninvited Guest** is an end-to-end, multi-stage, narrative-driven Cybersecurity Capture The Flag (CTF) investigation. Players step into the shoes of a digital forensics incident responder investigating an insider threat and exfiltration campaign orchestrated by an accomplice inside an isolated enterprise network.

---

## 📖 Storyline & Narrative Arc

A confidential forensic audit leaks snippet records of an ongoing insider inquiry into infrastructure architect **Adrian Kessler** (handle: `k3ss_void`). As you retrace Kessler's digital footprint across public forums, the corporate web storefront, encrypted evidence archives, and enterprise web proxy logs, you uncover an active covert exfiltration channel operated by a rogue accomplice: **Victor Hale**.

```
[Stage 1: OSINT] ──► Target Discovered Across Multi-Source Leak (Adrian Kessler)
      │
      ▼
[Stage 2: Web]   ──► SQL Injection Bypass on Juice Shop (adrian.kessler)
      │
      ▼
[Stage 3: Crypto]──► Evidence Archive Cracked & Product Images Extracted (Kessler123!)
      │
      ▼
[Stage 4: Forensics]► Most Clicked Product Image Isolated from Logs (apple_juice.jpg)
      │
      ▼
[Stage 5: Stego] ──► Covert Exchange Portal URL Extracted (http://localhost:8086)
      │
      ▼
[Stage 6: Network] ─► Rogue Accomplice Unmasked via Packet Analysis (Victor Hale)
```

---

## 🎯 Challenges & Flags Summary

| Stage | Category | Challenge Name | Artifact / Target | Flag / Solution | CTFd Flag Format |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **OSINT** | *Find the Uninvited Guest* | `stages/stage1_osint/` | Real Name: `Adrian Kessler` | `Adrian Kessler` or `uninvited{adrian_kessler}` or `adrian.kessler@uninvited.local` |
| **2** | **Web Security** | *Front Door* | `http://localhost:3000` | Profile Name: `adrian.kessler` | `adrian.kessler` or `uninvited{adrian.kessler}` |
| **3** | **Cryptography** | *Locked Evidence* | `evidence_photos.zip` | Master Password: `Kessler123!` | `Kessler123!` or `uninvited{Kessler123!}` |
| **4** | **Digital Forensics** | *Follow the Clicks* | `proxy_history.xml` | Outlier Product Image: `apple_juice.jpg` | `apple_juice.jpg` or `uninvited{apple_juice.jpg}` |
| **5** | **Steganography** | *Hidden in Plain Sight* | `apple_juice.jpg` | Hidden Portal: `http://localhost:8086` | `http://localhost:8086` or `uninvited{http://localhost:8086}` |
| **6** | **Networking** | *Unmasking the Uninvited Guest*| `upload_capture.pcap` | Rogue Accomplice: `Victor Hale` | `Victor Hale` or `uninvited{victor_hale}` |

> **Note on Flag Formatting**: CTFd accepts both canonical answers (e.g., `Adrian Kessler`, `apple_juice.jpg`) and wrapped CTF format (e.g., `uninvited{adrian_kessler}`, `uninvited{apple_juice.jpg}`).

---

## 🖥️ Operating Environment

- **Host Server**: Ubuntu Server 22.04 LTS host (Docker Engine & Docker Compose).
- **Participant Machine**: Participant-side Kali Linux VM.
- **Network Mode**: Bridged or Host-Only / NAT Network connecting Kali Linux to the Ubuntu Server.

---

## 🏗️ Architecture & Infrastructure

The environment runs via Docker Compose on an isolated bridge network (`uninvited_net`):

```
+---------------------------------------------------------------+
|                 Ubuntu Server 22.04 LTS Host                  |
|                                                               |
|   Port 8000                 Port 3000             Port 8086   |
|       │                         │                     │       |
+-------┼─────────────────────────┼─────────────────────┼-------+
        ▼                         ▼                     ▼
+---------------+         +---------------+     +---------------+
|     ctfd      |         |  juice-shop   |     |exchange-portal|
| (CTFd Platform)         |  (OWASP Web)  |     | (Custom Node) |
+---------------+         +---------------+     +---------------+
        │                         │                     │
        +─────────────────────────┴─────────────────────+
                                  │
                            uninvited_net
```

### Services

1. **CTFd (`port 8000`)**: The official CTFd tournament scoring and challenge management interface. Pre-configured with all 6 stages, flags, hints, and challenge file downloads.
2. **OWASP Juice Shop (`port 3000`)**: Seeded with target account `adrian.kessler@uninvited.local` (`admin` privilege). Evidence Vault at `/rest/admin/evidence_photos.zip`.
3. **The Exchange Portal (`port 8086`)**: Restricted Node.js/Express service hosting the authenticated transfer vault (`/portal`) and forensic Wireshark capture (`/upload_capture.pcap`).

---

## 🚀 Lab Deployment Guide

### Part 1: Ubuntu Server 22.04 LTS Host Setup

1. **Install Prerequisites**:
   ```bash
   sudo apt-get update && sudo apt-get install -y git docker.io docker-compose-v2
   sudo systemctl enable --now docker
   sudo usermod -aG docker $USER
   ```

2. **Clone the CTF Repository**:
   ```bash
   git clone https://github.com/Zahid29-arch/uninvited-guest-ctf.git
   cd uninvited-guest-ctf
   ```

3. **Launch the CTF Services**:
   ```bash
   docker compose up -d
   ```

4. **Identify Ubuntu Server IP Address**:
   ```bash
   hostname -I
   # Example: 192.168.100.50
   ```

5. **Firewall / Port Permissions (if UFW enabled)**:
   ```bash
   sudo ufw allow 8000/tcp
   sudo ufw allow 3000/tcp
   sudo ufw allow 8086/tcp
   ```

---

### Part 2: Participant Kali Linux VM Workflow

The participant accesses all challenges and targets from their **Kali Linux VM**:

1. **Verify Connectivity**:
   ```bash
   ping -c 3 <UBUNTU_SERVER_IP>
   ```

2. **Access CTFd Scoring Platform**:
   - Open Firefox inside Kali Linux and navigate to:
     ```text
     http://<UBUNTU_SERVER_IP>:8000
     ```
   - Click **Register** to create a participant account.
   - Click **Challenges** to access Stages 1 through 6.
   - Download investigation artifacts directly from the challenge popups.

3. **Stage-by-Stage Tooling on Kali Linux**:
   - **Stage 1 (OSINT)**: Download leaked HTML dumps from CTFd, inspect employee directories and forum posts with Firefox or `grep`.
   - **Stage 2 (Web Security)**: Open `http://<UBUNTU_SERVER_IP>:3000` in Firefox or route requests through **Burp Suite** to exploit login SQL injection.
   - **Stage 3 (Cryptography)**: Use Kali's built-in cracking tools:
     ```bash
     fcrackzip -u -D -p wordlist.txt evidence_photos.zip
     ```
   - **Stage 4 (Digital Forensics)**: Inspect `proxy_history.xml` using `xmllint`, Python, or text utilities to isolate the outlier requested asset.
   - **Stage 5 (Steganography)**: Extract the hidden URL from `apple_juice.jpg`:
     ```bash
     steghide extract -sf apple_juice.jpg -p ''
     cat link.txt
     ```
   - **Stage 6 (Networking)**: Browse to `http://<UBUNTU_SERVER_IP>:8086`, log in, download `upload_capture.pcap`, and open in **Wireshark**:
     ```bash
     wireshark upload_capture.pcap &
     ```
     Filter by `http.request.method == "POST"` and decode the exfiltrated Base64 identity.

---

### Part 3: Automated Health Check & Solvers

From the Ubuntu Server or repository directory:
```bash
# Verify environment health
python3 -m unittest tests/test_environment.py

# Run reference automated solver pipeline
python3 solvers/stage1_solver.py
python3 solvers/stage2_solver.py
python3 solvers/stage3_solver.py
python3 solvers/stage4_solver.py
python3 solvers/stage5_solver.py
python3 solvers/stage6_solver.py
```
