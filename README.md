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
2. **OWASP Juice Shop (`port 3000`)**: Seeded with target account `adrian.kessler@uninvited.local` (`admin` privilege). Evidence Vault at `/rest/admin/evidence_photos.zip`.
3. **The Exchange Portal (`port 8086`)**: Restricted Node.js/Express service hosting the authenticated transfer vault (`/portal`) and forensic Wireshark capture (`/upload_capture.pcap`).

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.10+

### 2. Launch the Environment
```bash
docker compose up -d --build
```

### 3. Verify Health
Run the automated integration test suite:
```bash
python -m unittest tests/test_environment.py
```

### 4. Run Automated Solvers
Execute end-to-end solvers from Stage 1 to Stage 6:
```bash
python solvers/stage1_solver.py
python solvers/stage2_solver.py
python solvers/stage3_solver.py
python solvers/stage4_solver.py
python solvers/stage5_solver.py
python solvers/stage6_solver.py
```
