# 🏆 Official CTF Author Write-Up: Uninvited Guest

This document provides the complete, step-by-step walkthrough for solving all six stages of the **Uninvited Guest** CTF challenge.

---

## 🧭 Narrative Flow Overview

The challenges progress sequentially through a connected forensic narrative:

1. **Stage 1 (OSINT)**: Identify the investigator/target (**Adrian Kessler**).
2. **Stage 2 (Web)**: Locate his corporate web account on Juice Shop (**adrian.kessler**).
3. **Stage 3 (Crypto)**: Crack his personal encrypted evidence archive to recover his master password (**Kessler123!**).
4. **Stage 4 (Forensics)**: Analyze web proxy logs to find anomalous file downloads (**consignment_07.jpg**).
5. **Stage 5 (Stego)**: Extract the hidden URL embedded in the image metadata (**http://localhost:8086**).
6. **Stage 6 (Network)**: Access the internal transit portal, download the network trace, and attribute the rogue upload to the antagonist (**Victor Hale**).

---

## 🔍 Stage 1: OSINT - Perimeter Footprint

### Objective
Uncover the real identity of the target behind the handles `k3ss_void` and `UninvitedGuest99`.

### Provided Artifacts
- `stages/stage1_osint/leaked_paste.html`
- `stages/stage1_osint/blog_about.html`
- `stages/stage1_osint/paste_dump.txt`

### Walkthrough
1. Inspect `leaked_paste.html`, `paste_dump.txt`, or `blog_about.html`.
2. The target engineer is identified as **Adrian Kessler** (alias: `k3ss_void`).
3. To prevent scraping, his corporate email is masked using a Base64 identity token:
   ```text
   IdentityToken = YWRyaWFuLmtlc3NsZXJAdW5pbnZpdGVkLmxvY2Fs
   ```
4. Decoding this token (`echo "YWRyaWFuLmtlc3NsZXJAdW5pbnZpdGVkLmxvY2Fs" | base64 -d`) or applying the noted company policy `{firstname}.{lastname}@uninvited.local` reveals his email address:
   ```text
   adrian.kessler@uninvited.local
   ```

### Flag
- **Standard**: `Adrian Kessler`
- **Wrapped**: `uninvited{adrian_kessler}`

---

## 🌐 Stage 2: Web - The Target's Cart

### Objective
Identify the target's username on the corporate e-commerce system (OWASP Juice Shop).

### Target Service
- OWASP Juice Shop: `http://localhost:3000`

### Walkthrough
1. Open OWASP Juice Shop in a web browser at `http://localhost:3000/#/login`.
2. In Stage 1, we recovered the target's email: `adrian.kessler@uninvited.local`.
3. To breach his account without knowing his password, leverage Juice Shop's **SQL Injection (Authentication Bypass)** vulnerability:
   - **Email**: `adrian.kessler@uninvited.local'--`
   - **Password**: (any character, e.g. `test`)
4. The application skips the password check and logs you into Adrian Kessler's administrator account!
5. Inspecting the authenticated session reveals the target's web username: `adrian.kessler`.

### Flag
- **Standard**: `adrian.kessler`
- **Wrapped**: `uninvited{adrian.kessler}`

---

## 🔐 Stage 3: Crypto - Classified Vault

### Objective
Download the classified forensic archive restricted to Administrator clearance on Juice Shop, and crack it to recover Adrian Kessler's master password.

### Provided Artifacts & Service
- Service: OWASP Juice Shop `http://localhost:3000`
- Wordlist: `stages/stage3_crypto/wordlist.txt`

### Walkthrough
1. Once logged into Juice Shop as Adrian Kessler, an in-page **`🔐 Evidence Vault`** button appears in the top navigation bar.
2. Clicking it opens the admin terminal, allowing direct download of `evidence_photos.zip` (also accessible via `http://localhost:3000/rest/admin/evidence_photos.zip?token=<JWT>`).
3. Attempting to download without administrator credentials returns **HTTP 401 Unauthorized** (or **403 Forbidden** for normal customer accounts).
4. Perform a dictionary attack against the downloaded archive using the provided `wordlist.txt`:
   ```bash
   python solvers/stage3_solver.py

   # Or using zip2john / John the Ripper:
   zip2john evidence_photos.zip > zip.hash
   john --wordlist=wordlist.txt zip.hash
   ```
5. The password `Kessler123!` unlocks the archive.
6. Extracting the archive reveals `case_notes.txt` confirming Adrian Kessler's credentials and `flag.txt`.

### Flag
- **Standard**: `Kessler123!`
- **Wrapped**: `uninvited{Kessler123!}`

---

## 📊 Stage 4: Forensics - Burp Anomaly

### Objective
Analyze web proxy history to identify an unusual, high-frequency image asset retrieved from the server.

### Provided Artifacts
- `stages/stage4_forensics/proxy_history.xml`

### Walkthrough
1. Open `proxy_history.xml` or write a quick parser to analyze request frequencies:
   ```bash
   python solvers/stage4_solver.py
   ```
2. Frequency analysis across the 100 logged requests reveals:
   - Baseline gallery thumbnails: 3 to 4 requests each.
   - Outlier: `/gallery/consignment_07.jpg` was requested **45 times**.
3. The outlier file is `consignment_07.jpg`.

### Flag
- **Standard**: `consignment_07.jpg`
- **Wrapped**: `uninvited{consignment_07.jpg}`

---

## 🖼️ Stage 5: Stego - Covert Transmission

### Objective
Extract the hidden covert gateway link embedded inside `consignment_07.jpg` using steganography tools.

### Provided Artifacts
- `stages/stage5_stego/consignment_07.jpg` (hosted live at `http://localhost:8086/gallery/consignment_07.jpg`)

### Tool Installation Guide for Players
Players need the `steghide` utility to extract data embedded into JPEG DCT coefficients.

- **On Kali Linux / Debian / Ubuntu**:
  ```bash
  sudo apt update && sudo apt install -y steghide
  ```
- **On macOS (via Homebrew)**:
  ```bash
  brew install steghide
  ```
- **On Windows (via Docker sandbox)**:
  ```powershell
  docker run --rm -v "${PWD}:/data" -w /data debian:bookworm-slim bash -c "apt update && apt install -y steghide && steghide extract -sf consignment_07.jpg -p '' && cat link.txt"
  ```

### Walkthrough
1. Verify the carrier image contains embedded data:
   ```bash
   steghide info consignment_07.jpg
   ```
2. Extract the hidden payload:
   ```bash
   steghide extract -sf consignment_07.jpg -p ""
   ```
   *(Or run `python solvers/stage5_solver.py`)*
3. Steghide writes the extracted payload to `link.txt`.
4. Inspecting `link.txt` reveals:
   ```text
   http://localhost:8086
   ```
5. This URL points directly to the private internal service: **The Exchange Portal**.

### Flag
- **Standard**: `http://localhost:8086` (or `http://localhost:8086/portal`)
- **Wrapped**: `uninvited{http://localhost:8086}`

---

## 📡 Stage 6: Network - The Uninvited Guest

### Objective
Access The Exchange Portal, download the intercepted network trace, and identify the rogue accomplice exfiltrating data.

### Provided Artifacts / Services
- Service: `http://localhost:8086`
- Downloadable Artifact: `upload_capture.pcap`

### Walkthrough
1. Navigate to `http://localhost:8086` in your browser.
2. Authenticate using Adrian Kessler's credentials recovered in Stages 1 & 3:
   - **Username**: `adrian.kessler@uninvited.local`
   - **Password**: `Kessler123!`
3. After logging in, the dashboard displays the **Authorized Transfer Vault**.
4. Download `upload_capture.pcap` (21.8 KB).
5. Open the capture in Wireshark. 
   *(Note: Naive string grepping for names will fail because transit identifiers are protected!)*
6. Filter for HTTP POST requests in Wireshark:
   ```text
   http.request.method == "POST"
   ```
7. Locate the single rogue POST transaction:
   - **Source IP**: `10.5.5.15`
   - **Destination**: `10.5.5.80` (Exchange Server)
   - **Endpoint**: `POST /upload HTTP/1.1`
8. Right-click the packet $\rightarrow$ **Follow** $\rightarrow$ **TCP Stream**.
9. Observe the exfiltration headers and JSON manifest payload:
   ```http
   POST /upload HTTP/1.1
   Host: exchange.uninvited.local
   X-Exfil-Operator: VmljdG9yIEhhbGU=
   X-Agent-Alias: DragonFly
   Content-Type: multipart/form-data; boundary=---------------------------39281749281739281749

   -----------------------------39281749281739281749
   Content-Disposition: form-data; name="operator_token"

   VmljdG9yIEhhbGU=
   -----------------------------39281749281739281749
   Content-Disposition: form-data; name="file"; filename="confidential_exfil_manifest.json"
   Content-Type: application/json

   {"manifest_id":"EXFIL-99201","sender_identity":"VmljdG9yIEhhbGU=","encoding":"base64","alias":"DragonFly","status":"dispatched"}
   ```
10. The operator token `VmljdG9yIEhhbGU=` is Base64 encoded. Decode it:
    ```bash
    echo "VmljdG9yIEhhbGU=" | base64 -d
    ```
    Output:
    ```text
    Victor Hale
    ```
11. The true identity of the rogue insider / accomplice is **Victor Hale**.

### Flag
- **Standard**: `Victor Hale`
- **Wrapped**: `uninvited{victor_hale}`

---

## 🏁 Summary of All Flags

| Challenge | Canonical Value | Wrapped Format |
| :--- | :--- | :--- |
| **Stage 1** | `Adrian Kessler` | `uninvited{adrian_kessler}` |
| **Stage 2** | `adrian.kessler` | `uninvited{adrian.kessler}` |
| **Stage 3** | `Kessler123!` | `uninvited{Kessler123!}` |
| **Stage 4** | `consignment_07.jpg` | `uninvited{consignment_07.jpg}` |
| **Stage 5** | `http://localhost:8086` | `uninvited{http://localhost:8086}` |
| **Stage 6** | `Victor Hale` | `uninvited{victor_hale}` |
