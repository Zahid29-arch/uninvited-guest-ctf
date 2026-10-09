# 🕵️ Uninvited Guest - CTF Play Box Suite
### SLIIT IE3132 Penetration Testing — Year 3 Semester 1 — Assignment 02

[![Platform](https://img.shields.io/badge/Platform-CTFd-red.svg)](https://ctfd.io/)
[![Environment](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![Network](https://img.shields.io/badge/Network-Isolated_uninvited__net-orange.svg)]()
[![Tests](https://img.shields.io/badge/Tests-7%2F7_Passing-brightgreen.svg)]()

**Uninvited Guest** is an end-to-end, multi-stage, narrative-driven Cybersecurity Capture The Flag (CTF) investigation developed for **SLIIT IE3132 Penetration Testing (Assignment 02)**. Players assume the role of digital forensics incident responders investigating an insider threat and covert data exfiltration pipeline orchestrated by infrastructure architect **Adrian Kessler** and rogue accomplice **Victor Hale**.

---

## 👥 Group Member Responsibilities & Allocation Matrix

Following the approved project plan and Assignment 02 specification (Page 4):

| Member | Role | Assigned Components & Responsibilities | Deliverables & Code |
| :--- | :--- | :--- | :--- |
| **Member 1** | **CTF Platform & Architecture** | • Deployment from scratch (`docker-compose.yml`, `start.sh`, `stop.sh`)<br>• Network segmentation & isolation (`uninvited_net`)<br>• Port access controls & security boundaries<br>• Platform provisioning, scoring engine, logging<br>• Resource management & container orchestration | • `docker-compose.yml`<br>• `start.sh`<br>• `stop.sh`<br>• Network topology & isolation config |
| **Member 2** | **Challenge Design A** *(Stages 1–3)* | • **Stage 1 (OSINT)**: Multi-source OSINT leak correlation (`Adrian Kessler`)<br>• **Stage 2 (Web Security)**: OWASP Juice Shop SQL Injection bypass (`adrian.kessler`)<br>• **Stage 3 (Cryptography)**: Evidence archive cracking with wordlist (`Kessler123!`)<br>• Challenge builds, artifact placement, hints, live walkthrough | • `stages/stage1_osint/`<br>• `stages/stage3_crypto/`<br>• `solvers/stage1_solver.py`<br>• `solvers/stage2_solver.py`<br>• `solvers/stage3_solver.py` |
| **Member 3** | **Challenge Design B** *(Stages 4–6)* | • **Stage 4 (Digital Forensics)**: Web proxy log analysis & outlier asset isolation (`apple_juice.jpg`)<br>• **Stage 5 (Steganography)**: Covert carrier image extraction via Steghide (`http://localhost:8086`)<br>• **Stage 6 (Networking / Capstone)**: PCAP inspection, multipart HTTP stream analysis, Base64 deobfuscation (`Victor Hale`) | • `stages/stage4_forensics/`<br>• `stages/stage5_stego/`<br>• `stages/stage6_pcap/`<br>• `platform/exchange-portal/`<br>• `solvers/stage4_solver.py`<br>• `solvers/stage5_solver.py`<br>• `solvers/stage6_solver.py` |
| **Member 4** | **Integration, Testing & Documentation** | • End-to-end progression & sequential prerequisite enforcement<br>• Automated test suite (`test_environment.py`: 7/7 tests)<br>• Reset and recovery mechanism (`reset.sh`)<br>• Unintended shortcut validation & defect resolution<br>• Record of design changes & technical justifications | • `tests/test_environment.py`<br>• `reset.sh`<br>• `platform/challenges.html`<br>• `README.md`<br>• `WRITEUP.md` |

---

## 📖 Storyline & Narrative Progression

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

| Stage | Domain | Difficulty | Challenge Name | Artifact / Target | Solution / Flag | CTFd Accepted Formats |
| :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| **1** | **OSINT** | Easy | *Find the Uninvited Guest* | `stages/stage1_osint/` | `Adrian Kessler` | `Adrian Kessler`<br>`uninvited{adrian_kessler}`<br>`adrian.kessler@uninvited.local` |
| **2** | **Web Security** | Easy | *Front Door* | `http://<SERVER_IP>:3000` | `adrian.kessler` | `adrian.kessler`<br>`uninvited{adrian.kessler}` |
| **3** | **Cryptography** | Moderate | *Locked Evidence* | `evidence_photos.zip` | `Kessler123!` | `Kessler123!`<br>`uninvited{Kessler123!}` |
| **4** | **Digital Forensics**| Moderate | *Follow the Clicks* | `proxy_history.xml` | `apple_juice.jpg` | `apple_juice.jpg`<br>`uninvited{apple_juice.jpg}` |
| **5** | **Steganography** | Mod-Hard | *Hidden in Plain Sight* | `apple_juice.jpg` | `http://localhost:8086` | `http://localhost:8086`<br>`uninvited{http://localhost:8086}` |
| **6** | **Networking** | Hard (Capstone)| *Unmasking the Uninvited Guest* | `upload_capture.pcap` | `Victor Hale` | `Victor Hale`<br>`uninvited{victor_hale}` |

> **Sequential Unlocking**: Stage 1 is unlocked by default. Stages 2 through 6 are shaded grey with lock icons (`🔒 LOCKED`) and unlock automatically in real-time as the preceding stage is solved.

---

## 🔑 Default Credentials & Endpoints

| Service | URL / Port | Credentials / Target | Description |
| :--- | :--- | :--- | :--- |
| **CTFd Scoring Engine** | `http://<SERVER_IP>:8000` | **Admin**: `Zahid` / `admin123`<br>*(Email: `musthafaz2002@gmail.com`)* | Tournament scoreboard, challenge downloads, hints, submission evaluation |
| **OWASP Juice Shop** | `http://<SERVER_IP>:3000` | **Target**: `adrian.kessler@uninvited.local`<br>*(Password bypassed via SQLi)* | Intentionally vulnerable storefront; hosts Evidence Vault at `/rest/admin/evidence_photos.zip` |
| **The Exchange Portal** | `http://<SERVER_IP>:8086` | **User**: `adrian.kessler@uninvited.local`<br>**Pass**: `Kessler123!` | Internal transfer vault hosting `upload_capture.pcap` and image gallery |

---

## 🏗️ Architecture & Network Isolation

```
+--------------------------------------------------------------------------+
|                       Ubuntu Server 22.04 LTS Host                       |
|                                                                          |
|   Port 8000                     Port 3000                    Port 8086   |
|       │                             │                            │       |
+-------┼─────────────────────────────┼────────────────────────────┼-------+
        ▼                             ▼                            ▼
+---------------+             +---------------+            +---------------+
|     ctfd      |             |  juice-shop   |            |exchange-portal|
| (CTFd v3.7.0) |             | (OWASP v17.1) |            | (Node/Express)|
+---------------+             +---------------+            +---------------+
        │                             │                            │
        +─────────────────────────────┴────────────────────────────+
                                      │
                            uninvited_net (Bridge)
```

- **Container Isolation**: All containers run on an isolated Docker user-defined bridge network (`uninvited_net`).
- **Host Exposure**: Only the three designated application ports (8000, 3000, 8086) are exposed to the host interface. No internal database ports or debug listeners are exposed.
- **VM Network**: Ubuntu Server runs on a VirtualBox Host-Only adapter (`192.168.60.10`) communicating exclusively with Kali Linux (`192.168.60.20`), completely isolated from campus/public networks.

---

## 🚀 Deployment Guide

### Step 1: Clone Repository on Ubuntu Server
```bash
git clone https://github.com/Zahid29-arch/uninvited-guest-ctf.git
cd uninvited-guest-ctf
```

### Step 2: Launch All Services
```bash
chmod +x start.sh stop.sh reset.sh
./start.sh
# Or directly: docker compose up -d
```

### Step 3: Verify Container Status
```bash
docker compose ps
```
All three services (`ctfd`, `juice-shop`, `exchange-portal`) should show `Up`.

### Step 4: Verify Network Connectivity
Identify your server IP:
```bash
hostname -I
```
From Kali Linux or host browser, verify access:
- CTFd: `http://<SERVER_IP>:8000`
- Juice Shop: `http://<SERVER_IP>:3000`
- Exchange Portal: `http://<SERVER_IP>:8086`

---

## 🔄 Reset & Recovery Mechanism (`reset.sh`)

To satisfy the rubric's requirement for a reliable reset/recovery mechanism, the suite includes `reset.sh`:

```bash
chmod +x reset.sh
```

### Options:

1. **Interactive Menu**:
   ```bash
   ./reset.sh
   ```
   Presents an interactive menu to reset the entire CTF, individual stages (1–6), or specific players.

2. **Full Box Reset (One Command)**:
   ```bash
   ./reset.sh all
   ```
   Clears all solves, submissions, IP tracking, and awards from CTFd, restarts all containers, and locks Stages 2–6 back to initial State 0.

3. **Stage-Specific Reset**:
   ```bash
   ./reset.sh stage 3
   ```
   Wipes solves and submissions for Stage 3 (and any dependent stages 4–6), leaving earlier stages intact.

4. **Player-Specific Reset**:
   ```bash
   ./reset.sh player <username>
   ```
   Clears progress for a single player without affecting other participants.

> **Credential Safety Guarantee**: The reset script **never modifies or deletes user accounts**. Admin credentials (`Zahid` / `admin123`) and registered player accounts remain permanently saved in the database.

---

## 🧪 Automated Testing & Reference Solvers (LO1–LO3)

### Automated Test Suite
Run the 7-point integration test suite from the repository root:
```bash
python3 tests/test_environment.py
```
**Test Coverage**:
1. `test_ctfd_up`: Confirms CTFd scoring server responds on port 8000.
2. `test_juice_shop_up`: Confirms OWASP Juice Shop responds on port 3000.
3. `test_juice_shop_target_account`: Confirms target account authentication.
4. `test_juice_shop_admin_evidence_vault`: Verifies evidence vault is protected with HTTP 401 and accessible only with Admin JWT.
5. `test_exchange_portal_up`: Confirms Exchange Portal responds on port 8086.
6. `test_exchange_portal_gallery_asset`: Verifies steganographic carrier image is hosted.
7. `test_exchange_portal_authentication_and_pcap`: Verifies portal login and PCAP download.

### Reference Solver Pipeline
Execute all self-developed exploit/solver scripts:
```bash
python3 solvers/stage1_solver.py   # Solves Stage 1 (OSINT) -> Adrian Kessler
python3 solvers/stage2_solver.py   # Solves Stage 2 (Web SQLi) -> adrian.kessler
python3 solvers/stage3_solver.py   # Solves Stage 3 (Crypto) -> Kessler123!
python3 solvers/stage4_solver.py   # Solves Stage 4 (Forensics) -> apple_juice.jpg
python3 solvers/stage5_solver.py   # Solves Stage 5 (Stego) -> http://localhost:8086
python3 solvers/stage6_solver.py   # Solves Stage 6 (Network) -> Victor Hale
```

---

## 📝 Record of Changes from Assignment 01 Design (with Technical Justifications)

As required by Assignment 02 rubric (Page 2 & 4), the following refinements were made to the original Assignment 01 proposal during implementation:

1. **User Registration Mode Adapted from Teams to Users**:
   - *Change*: Changed `user_mode` in CTFd configuration from `'teams'` to `'users'`.
   - *Technical Justification*: Eliminates the requirement for participants to create or join a team before viewing challenges, allowing players and evaluators to register and immediately proceed to Stage 1 without workflow friction.
2. **Visual Progressive Locking with Custom UI Theme**:
   - *Change*: Implemented custom `platform/challenges.html` template mounting into CTFd with grey shading (`opacity: 0.65`), dashed borders, yellow lock icon (`<i class="fas fa-lock"></i>`), and `🔒 LOCKED` badges.
   - *Technical Justification*: Prevents participants from attempting later challenges out of sequence, preserving the narrative arc and enforcing strict stage prerequisites.
3. **Multi-Format Flag Acceptance**:
   - *Change*: Configured dual-flag regex evaluation in CTFd database to accept both canonical strings (e.g. `Adrian Kessler`) and standardized CTF wrappers (e.g. `uninvited{adrian_kessler}`).
   - *Technical Justification*: Prevents participant frustration caused by minor casing or whitespace discrepancies during timed live walkthrough demonstrations.
4. **Isolated Static Upload Storage Mapping**:
   - *Change*: Configured `UPLOAD_FOLDER=/var/uploads` with explicit Docker volume mounting `./platform/ctfd-data/uploads:/var/uploads` and `user: root`.
   - *Technical Justification*: Resolves Docker overlay2 file permission mismatches that caused intermittent HTTP 404 errors during challenge artifact downloads in CTFd v3.7.0.

---

## 📚 Acknowledgments & References

In compliance with academic integrity guidelines (Assignment 02 Page 6), the following third-party frameworks, tools, and libraries are acknowledged:

- **CTFd** (v3.7.0): Open-source Capture The Flag framework by Kevin Chung ([https://ctfd.io](https://ctfd.io)).
- **OWASP Juice Shop** (v17.1.0): Open-source vulnerable web application by Bjoern Kimminich ([https://owasp-juice.shop](https://owasp-juice.shop)).
- **Express.js & Node.js**: REST and web service runtime used for the custom Exchange Portal.
- **Steghide**: Open-source steganography tool by Stefan Hetzl for embedding data into JPEG DCT coefficients.
- **Scapy & Wireshark**: Packet manipulation and packet analysis suites for network forensics.
- **SQLite3 & Python 3**: Embedded relational database engine and test orchestration framework.
- **Docker & Docker Compose**: Containerization platform providing host isolation and environment repeatability.
