# 🎙️ Operation Uninvited Guest: 15-Minute CTF Demonstration Script
### SLIIT IE3132 Penetration Testing — Assignment 02 Final Assessment
**Total Allotted Time**: ~14 Minutes (allowing 1 minute buffer for Q&A)

---

## ⏱️ Presentation Timing Breakdown

| Role | Topic | Allocated Time |
| :--- | :--- | :--- |
| **Member 1** | **CTF Platform & Architecture** | 0:00 – 3:30 (3.5 mins) |
| **Member 2** | **Challenge Design A (Stages 1, 2, 3)** | 3:30 – 7:15 (3.75 mins) |
| **Member 3** | **Challenge Design B (Stages 4, 5, 6)** | 7:15 – 11:00 (3.75 mins) |
| **Member 4** | **Integration, Testing & Documentation** | 11:00 – 14:00 (3.0 mins) |
| **Team** | **Conclusion & Assessor Q&A** | 14:00 – 15:00 (1.0 min) |

---

## 👤 Member 1: CTF Platform & Architecture (0:00 – 3:30)

### 🎬 Screen Action:
> Display VirtualBox Ubuntu Server running Docker (`docker compose ps`) and the CTFd homepage at `http://192.168.60.10:8000`. Show the terminal and network interfaces (`ip a`).

### 🗣️ Spoken Script:

> "Good morning/afternoon, evaluators. Today, our team is presenting **Operation Uninvited Guest**, an end-to-end, multi-stage cyber warfare and digital forensics CTF. I am Member 1, and I will be demonstrating the underlying platform architecture, deployment model, isolation controls, and operational reset mechanisms.
>
> ### 1. Deployment & Hybrid VM-Docker Architecture
> Our target box is built as an isolated hybrid deployment on Ubuntu Server 22.04 LTS. Using Docker Compose, we containerized three interdependent services:
> 1. **CTFd (`:8000`)**: The scoring engine, registration portal, and progressive tactical HUD.
> 2. **OWASP Juice Shop (`:3000`)**: A customized corporate e-commerce portal acting as our web target.
> 3. **The Dark Exchange Portal (`:8086`)**: A custom-developed Node.js/Express contraband repository used in the later stages.
>
> Deployment is zero-touch: executing `./start.sh` automatically provisions the environment, binds container volumes, and launches the entire scenario in under 45 seconds.
>
> ### 2. Network Segmentation & Ports
> Comparing the build against our approved architecture diagram:
> - **Internal Isolation**: All three containers communicate over an isolated internal Docker bridge network (`uninvited_net`).
> - **External Exposure**: Only necessary host ports are exposed (`:8000`, `:3000`, `:8086`, and host SSH on `:22`). Container databases and inter-service channels remain unexposed to public or campus networks.
> - **IP Subnetting**: Players on the attacker VM (Kali Linux) interface with the box via the host-only subnet `192.168.60.0/24` (Target IP: `192.168.60.10`).
>
> ### 3. Flag Submission & Validation Mechanism
> In CTFd, we configured dynamic regex and canonical flag validation for both wrapped formats (`uninvited{...}`) and raw tokens. To incentivize strategic gameplay, we implemented a graduated hint deduction penalty: **-10 points** for the first hint and **-20 points** for subsequent hints, with sequential dependency unlocking enforcing that players cannot skip stages.
>
> ### 4. Security Controls & Reset Mechanism
> To guarantee complete safety and reproducibility:
> - The box runs in an isolated network segment without unauthorized outbound internet requirements.
> - Crucial binaries and files in Juice Shop and Exchange are mounted with `:ro` (read-only) flags to prevent container tampering.
> - For competition resets, we engineered an automated reset script: `./reset.sh`. Running this flushes transient solves, resets database sequences, cleans session tables, and restores the system to baseline state in under 5 seconds without requiring a VM reboot.
>
> I will now hand over to Member 2 to demonstrate Challenge Design A covering Stages 1 through 3."

---

## 👤 Member 2: Challenge Design A — Stages 1, 2, 3 (3:30 – 7:15)

### 🎬 Screen Action:
> Open browser on Kali Linux / Attacker machine. Show the three Stage 1 HTML files, then Juice Shop login page (`:3000/#/login`), and terminal showing `evidence_photos.zip` cracking.

### 🗣️ Spoken Script:

> "Thank you, Member 1. I am Member 2, responsible for the design, implementation, and automated exploit tooling for Stages 1, 2, and 3. These stages cover Open-Source Intelligence, Web Exploitation, and Cryptographic analysis.
>
> ---
>
> ### 🔍 Stage 1: OSINT — Unmasking the Target
> - **How it was built**: We synthesized three authentic OSINT evidence artifacts representing realistic digital breadcrumbs: an engineering blog (`blog_about.html`), a leaked staff pastebin (`leaked_paste.html`), and an underground forum profile (`forum_profile.html`). 
> - **Vulnerability & Exploitation**: 
>   - The player reviews the engineering blog and identifies the lead developer's first name, **Adrian**, and his handle, **`k3ss_void`**, with corporate email convention `{first}.{last}@uninvited.local`.
>   - Cross-referencing `k3ss_void` against the leaked staff paste reveals his surname: **Kessler** (Badge ID `EMP-4401`).
>   - By correlating both sources, the player uncovers the target's full identity and email: `adrian.kessler@uninvited.local`.
> - **Tools Used**: Web Browser, text inspection, grep.
> - **Flag**: `uninvited{adrian_kessler}`.
> - **Automation**: Our script `solvers/stage1_solver.py` automatically parses and correlates these HTML files.
>
> ---
>
> ### 🌐 Stage 2: Web Security — Front Door Authentication Bypass
> - **How it was built**: We modified OWASP Juice Shop's seed configuration (`users.yml`) to inject Adrian Kessler as the primary administrator with a custom corporate domain.
> - **Vulnerability & Exploitation**:
>   - On the Juice Shop login page (`http://192.168.60.10:3000/#/login`), we exploit a classic **SQL Injection Authentication Bypass** on the SQLite backend.
>   - In the email field, entering `adrian.kessler@uninvited.local'--` comments out the password validation check. Any password can be provided.
>   - Upon submitting, the player bypasses authentication into Adrian's administrator session. Inspecting the user profile badge reveals his registered username.
> - **Tools Used**: Burp Suite / Browser DevTools.
> - **Flag**: `uninvited{adrian.kessler}`.
> - **Automation**: `solvers/stage2_solver.py` sends the crafted JSON POST payload and extracts the returned administrator JWT token.
>
> ---
>
> ### 🔐 Stage 3: Cryptography — Evidence Vault Password Cracking
> - **How it was built**: Using our synthesis script `build_evidence_zip.py`, we created an encrypted Zip archive (`evidence_photos.zip`) restricted to authenticated Juice Shop administrators via an endpoint mounted into Juice Shop (`/rest/admin/evidence_photos.zip`).
> - **Vulnerability & Exploitation**:
>   - Once authenticated as administrator in Stage 2, the player downloads `evidence_photos.zip`.
>   - The archive is protected using standard Zip encryption with a target password derived from target profiling (`Kessler123!`).
>   - Using the provided targeted wordlist (`wordlist.txt`), the player conducts a dictionary attack.
>   - Running `fcrackzip -u -D -p wordlist.txt evidence_photos.zip` or `zip2john` with Hashcat cracks the archive in less than 2 seconds.
> - **Tools Used**: `fcrackzip`, `zip2john`, `john`.
> - **Flag**: `uninvited{Kessler123!}`.
> - **Automation**: `solvers/stage3_solver.py` leverages multi-threaded Python decryption to crack and unpack the 10 evidence images, including `apple_juice.jpg`.
>
> Now, Member 3 will walk you through the second half of the attack chain."

---

## 👤 Member 3: Challenge Design B — Stages 4, 5, 6 (7:15 – 11:00)

### 🎬 Screen Action:
> Show terminal running `stage4_solver.py` frequency output, then run `steghide` on `apple_juice.jpg`, then open Wireshark showing `upload_capture.pcap` TCP stream.

### 🗣️ Spoken Script:

> "Thank you, Member 2. I am Member 3, and I engineered Stages 4, 5, and 6, which focus on Digital Forensics, Steganography, and Network Traffic Analysis, culminating in The Dark Exchange portal.
>
> ---
>
> ### 📊 Stage 4: Digital Forensics — Follow the Clicks
> - **How it was built**: Using `generate_proxy_log.py`, we generated a 114 KB authentic Burp Suite XML proxy log (`proxy_history.xml`) simulating over 80 HTTP transactions against Juice Shop. We introduced deliberate statistical skewing towards one specific product image.
> - **Vulnerability & Exploitation**:
>   - The player analyzes the proxy log to identify anomalies in user browsing behavior.
>   - While ordinary product images receive between 2 and 4 requests, one specific image registers an extreme outlier count of **45 requests**: `apple_juice.jpg`.
>   - Cross-referencing this filename with the extracted photos from Stage 3 confirms `apple_juice.jpg` as the focal point of the investigation.
> - **Tools Used**: Python XML parser, grep / awk frequency analysis.
> - **Flag**: `uninvited{apple_juice.jpg}`.
> - **Automation**: `solvers/stage4_solver.py` parses XML tags, counts request paths, and isolates the statistical outlier.
>
> ---
>
> ### 🖼️ Stage 5: Steganography — Hidden in Plain Sight
> - **How it was built**: We developed `embed_stego.py` using Steghide to embed covert text into the Discrete Cosine Transform (DCT) coefficients of `apple_juice.jpg`.
> - **Vulnerability & Exploitation**:
>   - With `apple_juice.jpg` identified as the carrier, the player applies steganographic extraction.
>   - Running `steghide extract -sf apple_juice.jpg -p ""` with an empty passphrase successfully extracts `link.txt`.
>   - Reading `link.txt` reveals an internal communication portal address: `http://localhost:8086`.
> - **Tools Used**: `steghide`, `exiftool`.
> - **Flag**: `uninvited{http://localhost:8086}`.
> - **Automation**: `solvers/stage5_solver.py` programmatically runs the extraction pipeline and parses the hidden internal URL.
>
> ---
>
> ### 📡 Stage 6: Networking — Unmasking the Accomplice
> - **How it was built**: We created a standalone Node.js web service, **The Dark Exchange Portal** (`:8086`), and authored `generate_pcap.py` using Scapy to forge a realistic 25 KB network packet capture (`upload_capture.pcap`) with SYN/ACK handshakes, metadata, and a rogue multipart POST exfiltration stream.
> - **Vulnerability & Exploitation**:
>   - Accessing `http://192.168.60.10:8086`, the player logs in with Adrian Kessler's credentials (`adrian.kessler@uninvited.local` / `Kessler123!`) recovered from Stages 1 and 3.
>   - From the transfer vault, the player downloads `upload_capture.pcap`.
>   - In Wireshark, filtering for `http.request.method == "POST"` isolates a transmission to `/upload` containing a custom header `X-Exfil-Operator: VmljdG9yIEhhbGU=`.
>   - Decoding the Base64 operator token `VmljdG9yIEhhbGU=` reveals the rogue operative: **Victor Hale**.
> - **Tools Used**: Wireshark, `tshark`, `base64`.
> - **Flag**: `uninvited{victor_hale}`.
> - **Automation**: `solvers/stage6_solver.py` reassembles the TCP packet stream using Scapy and extracts the decoded operator flag.
>
> I now hand over to Member 4 for integration, QA testing, and our verification audit."

---

## 👤 Member 4: Integration, Testing & Documentation (11:00 – 14:00)

### 🎬 Screen Action:
> Show `tests/run_all_tests.py` running in terminal and completing with all green checkmarks. Display `EVIDENCE_OF_CONTRIBUTION.md` and `test_execution.log`.

### 🗣️ Spoken Script:

> "Thank you, Member 3. I am Member 4, responsible for cross-stage integration, end-to-end quality assurance, vulnerability validation, and technical documentation.
>
> ### 1. End-to-End Progression & Dependency Flow
> Our CTF is not a collection of disconnected challenges; it is a single, continuous forensic narrative:
> - **Stage 1 (OSINT)** produces the email needed for **Stage 2 (SQLi)**.
> - **Stage 2** provides the admin session needed to download the vault in **Stage 3 (Crypto)**.
> - **Stage 3** decrypts the image archive needed for **Stage 4 (Forensics)** and **Stage 5 (Stego)**.
> - **Stage 3's password** and **Stage 5's URL** together unlock **Stage 6 (Networking)**, which delivers the final conclusion.
>
> This dependency chain ensures that every flag directly unlocks the next piece of the investigation.
>
> ### 2. Automated Test Suite & Defect Resolution
> To meet the requirement that all features must be built and rigorously tested:
> - We engineered a master test harness: `tests/run_all_tests.py`.
> - It executes 7 infrastructure unit tests (`test_environment.py`) checking port accessibility, HTTP status codes, SQLi reflection, JWT generation, and archive integrity.
> - It then sequentially executes all 6 reference solver scripts against the live environment.
> - **Defects Identified & Resolved**:
>   1. *Infinite DOM loop*: Fixed an issue in `challenges.html` where a recursive MutationObserver caused high CPU usage.
>   2. *CTFd Attachment 404s*: Configured container permissions and explicit upload volume mounts.
>   3. *Spoiler Mitigation*: We removed all visual card highlights and spoilers from the Stage 1 files and home page to guarantee a fair player experience.
>
> As documented in `tests/test_execution.log`, our test suite runs with a **100% pass rate** across all components.
>
> ### 3. Design Justifications & Changes from Assignment 01
> In comparison to our initial Assignment 01 design proposal:
> 1. **Modular Containerization**: Shifted from bare-metal services to a unified Docker Compose architecture, enhancing reproducibility and isolation.
> 2. **Tactical Cyber HUD**: Replaced CTFd's generic interface with a custom cyberpunk HUD featuring live progression badges and dynamic IP binding for seamless multi-device play.
> 3. **Standalone Contraband Portal**: Upgraded Stage 6 to include a dedicated custom-built web application (`The Dark Exchange`) rather than a simple static download.
>
> All evidence of individual contributions, commit logs, and test evidence is formally documented in `EVIDENCE_OF_CONTRIBUTION.md`. Thank you, and we now welcome any questions."

---

## 📋 Quick Speaker Reference Card (Cheat Sheet)

| Stage | Domain | Target / Asset | Exploit / Tool | Canonical Flag | Wrapped Flag |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | **OSINT** | `blog_about.html` + `leaked_paste.html` | Cross-source correlation | `Adrian Kessler` | `uninvited{adrian_kessler}` |
| **2** | **Web** | Juice Shop `:3000` | SQLi: `adrian.kessler@uninvited.local'--` | `adrian.kessler` | `uninvited{adrian.kessler}` |
| **3** | **Crypto** | `evidence_photos.zip` | Dictionary crack (`fcrackzip` / `wordlist.txt`) | `Kessler123!` | `uninvited{Kessler123!}` |
| **4** | **Forensics** | `proxy_history.xml` | Frequency outlier analysis (45 requests) | `apple_juice.jpg` | `uninvited{apple_juice.jpg}` |
| **5** | **Stego** | `apple_juice.jpg` | `steghide extract -sf apple_juice.jpg -p ""` | `http://localhost:8086` | `uninvited{http://localhost:8086}` |
| **6** | **Network** | `upload_capture.pcap` | Wireshark POST filter + Base64 decode | `Victor Hale` | `uninvited{victor_hale}` |

---
*End of Script — Total Presentation Time: ~14 Minutes*
