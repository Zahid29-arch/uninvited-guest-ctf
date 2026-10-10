# 📦 CTF Play Box — Lecturer Deployment & Assessment Manual
### Module: SLIIT IE3132 Penetration Testing
### Assignment: Assignment 02 — Practical CTF Environment Deployment
### Project: Operation Uninvited Guest

---

## 📋 Evaluation Overview

This package contains the complete **CTF Play Box source files, Docker Compose deployment project, and automated verification suites** for **Operation Uninvited Guest**.

As per the assignment requirements, the evaluator/lecturer can deploy and assess this Play Box using either of two methods:
1. **Method 1 (Fastest / Recommended)**: Deploy directly from the included **Docker Compose project** in under 60 seconds on any host with Docker installed.
2. **Method 2 (Standalone Appliance)**: Import the pre-configured **VirtualBox VM Image (`.ova`)** using the provided cloud download link.

---

## 🌐 Services, Ports & Assessment Endpoints

When deployed, the box exposes three interconnected target portals:

| Service | Port / URL | Credentials / Target | Evaluation Function |
| :--- | :--- | :--- | :--- |
| **CTFd Scoring Engine** | `http://<SERVER_IP>:8000` | **Username**: `Zahid`<br>**Password**: `admin123` | Challenge board, flag submission, dynamic hint penalties (-10 / -20 pts), scoreboard |
| **OWASP Juice Shop** | `http://<SERVER_IP>:3000` | **Target**: `adrian.kessler@uninvited.local`<br>*(Bypassed via SQL injection)* | Web exploitation target (Stage 2) & Evidence Vault repository (Stage 3) |
| **The Dark Exchange** | `http://<SERVER_IP>:8086` | **User**: `adrian.kessler@uninvited.local`<br>**Password**: `Kessler123!` | Custom contraband file gateway hosting raw packet capture (Stages 5 & 6) |

---

## 🚀 METHOD 1: Direct Docker Compose Deployment (1-Click)

### 1. Prerequisites
* **Operating System**: Linux (Ubuntu 20.04/22.04 LTS recommended), macOS, or Windows (WSL2)
* **Required Tools**: `docker` (v20.10+) and `docker compose` (v2.0+)

### 2. Setup & Execution
From the root of this folder, run:

```bash
# Ensure execution permissions on management scripts
chmod +x start.sh stop.sh reset.sh

# Launch the CTF Play Box
./start.sh
```
*(Alternatively, execute standard Docker Compose directly)*:
```bash
docker compose up -d
```

### 3. Verification
Verify that all 3 services are running and healthy:
```bash
docker compose ps
```
**Expected Output**:
```text
NAME                                    STATUS         PORTS
uninvited-guest-ctf-ctfd-1              Up             0.0.0.0:8000->8000/tcp
uninvited-guest-ctf-juice-shop-1        Up             0.0.0.0:3000->3000/tcp
uninvited-guest-ctf-exchange-portal-1   Up             0.0.0.0:8086->8086/tcp
```

### 4. Access the Play Box
Open any web browser and navigate to:
* **CTFd Portal**: `http://localhost:8000` *(or `http://<HOST_IP>:8000`)*
* **Juice Shop**: `http://localhost:3000`
* **Dark Exchange**: `http://localhost:8086`

---

## 🖥️ METHOD 2: VirtualBox VM Appliance Deployment (.OVA)

If you prefer evaluating the pre-configured hybrid Ubuntu Server Virtual Machine:

### 1. Download VM Image
* **Format**: Open Virtualization Format Archive (`.ova`)
* **Download Link**: `[PASTE_GOOGLE_DRIVE_OR_ONEDRIVE_LINK_HERE]`
* **Default VM Credentials**:
  * **OS Username**: `zahid`
  * **OS Password**: `ubuntu` (or `zahid`)
  * **Sudo Access**: Enabled

### 2. Import into VirtualBox
1. Open **Oracle VM VirtualBox**.
2. Click **File** ➔ **Import Appliance...**
3. Select the downloaded `.ova` file and click **Finish**.
4. Under VM Settings ➔ **Network**:
   * **Adapter 1**: NAT (for internet/dependencies)
   * **Adapter 2**: Host-Only Adapter (`192.168.60.0/24` subnet)
5. Power on the VM. All Docker containers start automatically on boot.
6. The target server will be live at `http://192.168.60.10:8000`.

---

## 🔄 Reset & State Recovery Instructions

The playbox includes an automated reset engine (`reset.sh`) allowing the evaluator to quickly flush solves between test runs without rebuilding containers.

```bash
# Full Competition Reset (Clears solves, unlocks, submissions, resets scoreboard)
./reset.sh all
```

### Reset Options Summary:
* `./reset.sh all` — Wipes all submissions, locks Stages 2–6, clears the scoreboard, and resets containers to initial State 0.
* `./reset.sh stage <1-6>` — Resets a specific stage and relocks dependent stages.
* `./reset.sh player <username>` — Resets progress for an individual player while preserving others.
* `./reset.sh` — Interactive menu mode.

> **Note**: User and admin accounts (`Zahid` / `admin123`) are permanently preserved during resets.

---

## 🧪 Automated Grading & Verification Suite

To enable rapid grading and verify that all stages are 100% solvable without manual play, an automated test suite and individual stage solver scripts are included:

### 1. Full Environment Verification (7 Tests)
Run from the root directory:
```bash
python3 tests/test_environment.py
```
**Evaluates**:
- Port reachability (`:8000`, `:3000`, `:8086`)
- SQLite database integrity & challenge seeding
- Juice Shop Admin SQL injection authentication & evidence archive restrictions
- Exchange Portal token authentication & PCAP availability

### 2. Automated Reference Solvers (Stages 1 to 6)
Each stage has a standalone Python exploit/solver script in the `solvers/` directory:

```bash
python3 solvers/stage1_solver.py   # Solves OSINT (Adrian Kessler)
python3 solvers/stage2_solver.py   # Exploits SQLi & extracts JWT (adrian.kessler)
python3 solvers/stage3_solver.py   # Cracks evidence archive (Kessler123!)
python3 solvers/stage4_solver.py   # Analyzes proxy log metrics (apple_juice.jpg)
python3 solvers/stage5_solver.py   # Extracts stego payload (http://localhost:8086)
python3 solvers/stage6_solver.py   # Parses PCAP multipart stream (Victor Hale)
```

---

## 🎯 Master Flag Reference Table

| Stage | Domain | Challenge Name | Target / Artifact | Flag Value | CTFd Accepted Variants |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1** | OSINT | Find the Uninvited Guest | `stages/stage1_osint/` | `Adrian Kessler` | `Adrian Kessler`<br>`uninvited{adrian_kessler}`<br>`adrian.kessler@uninvited.local` |
| **2** | Web | Front Door | OWASP Juice Shop (`:3000`) | `adrian.kessler` | `adrian.kessler`<br>`uninvited{adrian.kessler}` |
| **3** | Crypto | Locked Evidence | `evidence_photos.zip` | `Kessler123!` | `Kessler123!`<br>`uninvited{Kessler123!}` |
| **4** | Forensics | Follow the Clicks | `proxy_history.xml` | `apple_juice.jpg` | `apple_juice.jpg`<br>`uninvited{apple_juice.jpg}` |
| **5** | Stego | Hidden in Plain Sight | `apple_juice.jpg` | `http://localhost:8086` | `http://localhost:8086`<br>`uninvited{http://localhost:8086}` |
| **6** | Network | Unmasking the Accomplice | `upload_capture.pcap` | `Victor Hale` | `Victor Hale`<br>`uninvited{victor_hale}` |

---

## 📁 Package Directory Structure

```text
ctf playbox files/
├── docker-compose.yml          # Container configuration (CTFd, Juice Shop, Exchange Portal)
├── start.sh                    # Automated 1-click startup script
├── stop.sh                     # Graceful shutdown script
├── reset.sh                    # Automated state reset engine
├── PLAYBOX_SETUP_GUIDE.md      # This evaluation guide
├── README.md                   # Full student architecture and design documentation
├── WRITEUP.md                  # Comprehensive official walkthrough for all 6 stages
├── EVIDENCE_OF_CONTRIBUTION.md # Workload allocation matrix and testing proof
├── platform/
│   ├── challenges.html         # Custom tactical CTFd challenge board template
│   ├── register.html           # Custom tactical CTFd registration template
│   ├── users.yml               # Seed configuration for Juice Shop target administrator
│   ├── ctfd-data/
│   │   ├── ctfd.db             # Pre-configured SQLite CTFd database with challenges & rules
│   │   └── uploads/            # Challenge downloadable artifacts
│   └── exchange-portal/        # Custom Node.js/Express contraband repository (Stage 6)
├── stages/                     # Source files for Stages 1 to 6
├── solvers/                    # Automated reference exploit scripts (Stages 1 to 6)
└── tests/                      # Automated environment validation test suite
```

---
*Developed for SLIIT IE3132 Penetration Testing — Assignment 02.*
