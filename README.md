# 🕵️ Uninvited Guest - CTF Challenge Suite

[![CTF Framework](https://img.shields.io/badge/Platform-CTFd-red.svg)](https://ctfd.io/)
[![Environment](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()

**Uninvited Guest** is an end-to-end, multi-stage, narrative-driven Cybersecurity Capture The Flag (CTF) investigation. Players step into the shoes of a digital forensics incident responder investigating an insider threat and exfiltration campaign orchestrated by an accomplice inside an isolated enterprise network.

---

## 📖 Storyline & Narrative Arc

A confidential forensic audit leaks snippet records of an ongoing insider inquiry into investigator **Adrian Kessler** (handle: `k3ss_void`). As you retrace Kessler's digital footprint across public forums, the corporate web storefront, encrypted physical evidence dumps, and enterprise web proxy logs, you uncover an active covert exfiltration channel operated by a rogue accomplice: **Victor Hale**.

```
[Stage 1: OSINT] ──► Target Identified (Adrian Kessler)
      │
      ▼
[Stage 2: Web]   ──► Target Account Discovery (adrian.kessler)
      │
      ▼
[Stage 3: Crypto]──► Evidence Archive Cracked (Kessler123!)
      │
      ▼
[Stage 4: Forensics]► Anomaly Image Isolated (consignment_07.jpg)
      │
      ▼
[Stage 5: Stego] ──► Covert Portal Link Extracted (http://localhost:8086)
      │
      ▼
[Stage 6: Network] ─► Exfiltration Accomplice Unmasked (Victor Hale)
```

---

## 🎯 Challenges & Flags Summary

| Stage | Category | Challenge Name | Artifact / Target | Flag / Solution | CTFd Flag Format |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **OSINT** | *Perimeter Footprint* | `stages/stage1_osint/` | Real Name: `Adrian Kessler` | `Adrian Kessler` or `uninvited{adrian_kessler}` |
| **2** | **Web** | *The Target's Cart* | `http://localhost:3000` | Shop Username: `adrian.kessler` | `adrian.kessler` or `uninvited{adrian.kessler}` |
| **3** | **Crypto** | *Classified Vault* | `evidence_photos.zip` | Master Password: `Kessler123!` | `Kessler123!` or `uninvited{Kessler123!}` |
| **4** | **Forensics** | *Burp Anomaly* | `proxy_history.xml` | Outlier Image: `consignment_07.jpg` | `consignment_07.jpg` or `uninvited{consignment_07.jpg}` |
| **5** | **Stego** | *Covert Transmission* | `consignment_07.jpg` | Hidden Gateway: `http://localhost:8086` | `http://localhost:8086` or `uninvited{http://localhost:8086}` |
| **6** | **Network** | *The Uninvited Guest* | `upload_capture.pcap` | Rogue Accomplice: `Victor Hale` | `Victor Hale` or `uninvited{victor_hale}` |

> **Note on Flag Formatting**: The challenges are designed to accept either the direct canonical answer (e.g., `Adrian Kessler`, `consignment_07.jpg`) or the standard wrapped CTF format (e.g., `uninvited{adrian_kessler}`, `uninvited{consignment_07.jpg}`).

---

## 🏗️ Architecture & Infrastructure

The environment runs via Docker Compose on an isolated bridge network (`uninvited_net`):

```
+---------------------------------------------------------------+
|                       Host Machine                            |
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

1. **CTFd (`port 8000`)**: The official CTFd tournament scoring and challenge management interface.
2. **OWASP Juice Shop (`port 3000`)**: Seeded with target account `adrian.kessler@uninvited.local` (`admin` privilege).
3. **The Exchange Portal (`port 8086`)**: Custom Node.js/Express service serving the public gallery (`/gallery/consignment_07.jpg`), authenticated transit vault (`/portal`), and Wireshark capture download (`/upload_capture.pcap`).

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.10+ (for solver scripts and test suite)

### 2. Launch the Environment
```bash
docker compose up -d --build
```

### 3. Verify Health
Run the automated integration test suite:
```bash
python -m unittest tests/test_environment.py
```
Expected output:
```text
Ran 6 tests in 0.200s
OK
```

### 4. Access Services
- **CTFd Scoring Platform**: [http://localhost:8000](http://localhost:8000)
- **OWASP Juice Shop**: [http://localhost:3000](http://localhost:3000)
- **The Exchange Portal**: [http://localhost:8086](http://localhost:8086)

---

## 🛠️ Automated Solvers

Each challenge stage includes a standalone verification script in the `solvers/` directory:

```bash
# Stage 1: OSINT Extraction
python solvers/stage1_solver.py

# Stage 2: Juice Shop Account Verification
python solvers/stage2_solver.py

# Stage 3: Archive Dictionary Attack
python solvers/stage3_solver.py

# Stage 4: Burp Log Frequency Analysis
python solvers/stage4_solver.py

# Stage 5: Steganography URL Extraction
python solvers/stage5_solver.py

# Stage 6: PCAP Network Traffic Analysis
python solvers/stage6_solver.py
```

---

## 📂 Repository Layout

```
uninvited-guest-ctf/
├── docker-compose.yml              # Multi-container orchestration
├── platform/
│   ├── users.yml                   # Seed configuration for Juice Shop
│   └── exchange-portal/            # Custom Stage 5/6 challenge service
│       ├── server.js               # Express portal authentication & routing
│       ├── package.json
│       ├── Dockerfile
│       └── public/                 # Static gallery images & PCAP capture
├── stages/                         # Raw challenge artifacts provided to players
│   ├── stage1_osint/               # Leaked HTML dumps & blog pages
│   ├── stage3_crypto/              # evidence_photos.zip & wordlist.txt
│   ├── stage4_forensics/           # proxy_history.xml (Burp Suite export)
│   ├── stage5_stego/               # consignment_07.jpg & gallery_02.jpg
│   └── stage6_pcap/                # upload_capture.pcap & generator script
├── solvers/                        # Reference exploit & solution scripts
│   ├── stage1_solver.py
│   ├── stage2_solver.py
│   ├── stage3_solver.py
│   ├── stage4_solver.py
│   ├── stage5_solver.py
│   └── stage6_solver.py
├── tests/
│   └── test_environment.py         # Integration health checks
├── README.md                       # Platform documentation (this file)
└── WRITEUP.md                      # Complete author walkthrough
```

---

## 📄 License
MIT License. Created for CTF training, security research, and demonstration purposes.
