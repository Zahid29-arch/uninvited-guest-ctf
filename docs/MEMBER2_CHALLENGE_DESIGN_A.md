# 🎯 Member 2: Challenge Design A — Stages 1, 2 & 3
### Student ID: IT24100066 (GitHub: https://github.com/IT24100066)
### Module: SLIIT IE3132 Penetration Testing — Assignment 02
### Focus Area: Challenge Design A (Stages 1, 2 & 3), Vulnerability Engineering & Exploitation Tooling

---

## 1. Executive Summary & Assigned Responsibilities

As **Member 2**, I was responsible for the end-to-end conceptualization, artifact engineering, vulnerability implementation, and reference exploit tooling for **Challenge Design A**, comprising:
1. **Stage 1 (OSINT)**: *Find the Uninvited Guest* — Multi-source threat intelligence correlation.
2. **Stage 2 (Web Security)**: *Front Door* — OWASP Juice Shop SQL Injection authentication bypass.
3. **Stage 3 (Cryptography)**: *Locked Evidence* — Encrypted zip archive password cracking.
4. **Reference Solvers & Hints**: Implementing automated Python solvers (`solvers/stage1_solver.py`, `stage2_solver.py`, `stage3_solver.py`), graduated hints, and stage reset logic.

---

## 2. Stage 1: OSINT — Find the Uninvited Guest

### A. How It Was Built
* **Source Files**: `stages/stage1_osint/blog_about.html`, `leaked_paste.html`, `forum_profile.html`
* **Artifact Design**: Synthesized three authentic OSINT breadcrumbs:
  - An engineering tech blog authored by developer `k3ss_void`, revealing his first name **Adrian** and email domain `@uninvited.local`.
  - A leaked staff pastebin dump mapping badge ID `EMP-4401` to surname **Kessler**.
  - A dark-web forum profile corroborating `k3ss_void`'s insider communications.
* **Flag Placement**: Target full identity correlation $\to$ `Adrian Kessler` (`uninvited{adrian_kessler}`).

### B. Live Solve Path
1. **Information Gathering**: Inspect downloaded HTML files in browser or text editor.
2. **Correlation**: Match developer handle `k3ss_void` across blog and leaked paste.
3. **Exploitation**: Correlate first name `Adrian` and surname `Kessler` to recover corporate email `adrian.kessler@uninvited.local`.
4. **Automated Solver**: `solvers/stage1_solver.py` uses Regex to extract and correlate the target identity automatically.

---

## 3. Stage 2: Web Security — Front Door (OWASP Juice Shop)

### A. How It Was Built
* **Configuration**: `platform/users.yml` injects Adrian Kessler as an administrator with role `'admin'` and email `adrian.kessler@uninvited.local`.
* **Vulnerability**: Injected an intentional SQL Injection flaw into the backend SQLite user authentication endpoint.
* **Flag Placement**: Recovered inside the administrator dashboard profile badge $\to$ `adrian.kessler` (`uninvited{adrian.kessler}`).

### B. Live Solve Path
1. **Target Identification**: Navigate to Juice Shop login page at `http://192.168.60.10:3000/#/login`.
2. **Exploitation**:
   - In email field, enter SQLi payload: `adrian.kessler@uninvited.local'--`
   - In password field, enter arbitrary text (e.g. `test`).
   - The SQLite backend executes: `SELECT * FROM Users WHERE email = 'adrian.kessler@uninvited.local'--' AND password = ...;`
   - Authentication succeeds immediately, bypassing password verification.
3. **Flag Extraction**: In the user profile menu, inspect account details to extract username `adrian.kessler`.
4. **Automated Solver**: `solvers/stage2_solver.py` issues a raw HTTP POST payload and extracts the JWT admin token.

---

## 4. Stage 3: Cryptography — Locked Evidence Vault

### A. How It Was Built
* **Synthesis Script**: `stages/stage3_crypto/build_evidence_zip.py`
* **Encryption**: Compiles `evidence_photos.zip` using standard ZipCrypto cipher with target password `Kessler123!`.
* **Access Control**: Restricted to authenticated administrators via endpoint `/rest/admin/evidence_photos.zip`.
* **Flag Placement**: Password unlocking the archive $\to$ `Kessler123!` (`uninvited{Kessler123!}`).

### B. Live Solve Path
1. **Download**: Authenticate as administrator in Stage 2, download `evidence_photos.zip`.
2. **Dictionary Attack**: Run dictionary attack using targeted wordlist:
   ```bash
   fcrackzip -u -D -p wordlist.txt evidence_photos.zip
   # Or using zip2john and John the Ripper:
   zip2john evidence_photos.zip > hash.txt && john --wordlist=wordlist.txt hash.txt
   ```
3. **Decryption**: Password cracked in < 2 seconds: `Kessler123!`.
4. **Automated Solver**: `solvers/stage3_solver.py` extracts files and returns the flag.

---

## 5. Hints & Stage Reset Policy

* **Stage 1 Hint (-10 pts)**: "Cross-reference the employee badge number in the pastebin dump."
* **Stage 2 Hint (-10 pts)**: "SQL injection payload comments out password check using standard SQL delimiter `'--`."
* **Stage 3 Hint (-10 pts)**: "The archive password follows corporate policy: Capital letter, word, and numbers."
* **Reset**: Integrated into `./reset.sh stage 1`, `./reset.sh stage 2`, `./reset.sh stage 3`.

---
*Authored by Member 2 (IT24100066) — SLIIT IE3132 Penetration Testing.*
