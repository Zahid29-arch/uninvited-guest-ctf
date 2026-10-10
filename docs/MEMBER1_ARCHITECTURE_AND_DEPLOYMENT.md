# 🏛️ Member 1: Platform Architecture, Deployment & Security Controls
### Student ID: IT24103264 (GitHub: https://github.com/IT24103264)
### Module: SLIIT IE3132 Penetration Testing — Assignment 02
### Focus Area: CTF Platform Architecture, Deployment & Environment Orchestration

---

## 1. Executive Summary & Assigned Responsibilities

As **Member 1**, I was responsible for designing, containerizing, provisioning, and securing the entire CTF target infrastructure from scratch in accordance with the Assignment 02 specification. My direct responsibilities encompass:
1. **Deployment from Scratch**: Authoring `docker-compose.yml`, `start.sh`, and `stop.sh` for zero-touch deployment on Ubuntu Server 22.04 LTS.
2. **Architecture Compliance**: Implementing the build to match the approved architecture diagram, including network segmentation, port binding, and service isolation.
3. **Flag Submission & Validation**: Configuring the CTFd scoring engine, canonical and regex flag validation formats, and dynamic hint deduction penalty rules.
4. **Security Controls**: Enforcing container privileges, read-only filesystem mounts, internal bridge networks, and operational logging.

---

## 2. Deployment from Scratch (VM / Docker / Hybrid)

### A. Environment Provisioning
The target platform is built as a hybrid containerized deployment hosted on an isolated Ubuntu Server 22.04 LTS Virtual Machine:

| Component | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| **Host OS** | Ubuntu Server LTS | 22.04 | Minimal host runtime hosting Docker Engine |
| **Container Engine** | Docker Compose | v2.20+ | Multi-service orchestration and bridge networking |
| **Service 1: CTFd** | `ctfd/ctfd` | v3.7.0 | Scoring engine, registration, hint manager |
| **Service 2: Juice Shop** | `bkimminich/juice-shop`| v17.1.0 | E-commerce web target & Evidence Vault |
| **Service 3: Exchange Portal**| Custom Node.js/Express | 18-alpine | Contraband file gateway & capstone target |

### B. Deployment Automation (`start.sh` & `stop.sh`)
To ensure the lecturer can deploy the box in under 60 seconds without manual configuration, I implemented:
* **`start.sh`**:
  ```bash
  #!/usr/bin/env bash
  set -e
  echo "[+] Initializing Operation Uninvited Guest CTF..."
  chmod -R 777 platform stages
  docker compose up -d
  echo "[+] All CTF services successfully deployed and listening!"
  ```
* **`stop.sh`**:
  ```bash
  #!/usr/bin/env bash
  docker compose down
  echo "[+] All CTF containers stopped and resources released."
  ```

---

## 3. Architecture as Built vs. Approved Diagram

```
+-------------------------------------------------------------------------------+
|                        Host Network (Ubuntu 22.04 LTS)                        |
|                                                                               |
|   Port 8000 (CTFd)             Port 3000 (Juice Shop)     Port 8086 (Exchange)|
+----------┼─────────────────────────────┼───────────────────────────┼---------+
           ▼                             ▼                           ▼
+---------------------+       +---------------------+     +---------------------+
|        ctfd         |       |     juice-shop      |     |   exchange-portal   |
| Container (Alpine)  |       | Container (Node 20) |     | Container (Node 18) |
+----------┼----------+       +----------┼----------+     +----------┼----------+
           │                             │                           │
           +─────────────────────────────┴───────────────────────────+
                                         │
                     uninvited_net (Isolated Docker Bridge)
```

### Network Segmentation & Port Matrix
* **Subnet Isolation**: Attacker VM (Kali Linux) resides on Host-Only subnet `192.168.60.0/24` (Kali IP: `192.168.60.20`, Server IP: `192.168.60.10`).
* **Inter-Container Communication**: Containers communicate strictly across `uninvited_net` bridge network. Internal databases (e.g. SQLite, Redis) are never bound to external interfaces.
* **External Port Access**:
  - `0.0.0.0:8000` $\to$ CTFd (HTTP)
  - `0.0.0.0:3000` $\to$ OWASP Juice Shop (HTTP)
  - `0.0.0.0:8086` $\to$ The Dark Exchange (HTTP)
  - `0.0.0.0:22`   $\to$ Ubuntu Host SSH Administration

---

## 4. Flag Submission & Validation Mechanism

To ensure player flexibility while preventing guessing attacks, I configured:
1. **Canonical Formats**: Both wrapped format (`uninvited{...}`) and raw tokens are evaluated using dynamic regex matching in CTFd.
2. **Hint Deduction Policy**:
   - First hint: **-10 points** deduction.
   - Second hint: **-20 points** deduction.
3. **Sequential Prerequisites**: Challenge requirements chain sequentially:
   $$\text{Stage 1} \to \text{Stage 2} \to \text{Stage 3} \to \text{Stage 4} \to \text{Stage 5} \to \text{Stage 6}$$

---

## 5. Security Controls & Privilege Restrictions

1. **Read-Only Bind Mounts**: Challenge artifacts inside containers are mounted with `:ro` to prevent players from tampering with source challenges.
2. **Non-Root Execution**: Application services run under unprivileged service users inside the containers.
3. **Logging & Observability**: Real-time access logs are forwarded to Docker daemon logs (`docker compose logs -f`) for complete auditability.

---
*Authored by Member 1 (IT24103264) — SLIIT IE3132 Penetration Testing.*
