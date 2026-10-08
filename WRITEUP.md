# 🏆 Official CTF Author Write-Up: Uninvited Guest

This document provides the complete, step-by-step walkthrough for solving all six stages of the **Uninvited Guest** CTF challenge.

---

## 🧭 Narrative Flow Overview

The challenges progress sequentially through a connected forensic narrative:

1. **Stage 1 (OSINT)**: Identify the investigator/target (**Adrian Kessler**) by correlating his first name and surname across separate leaked sources.
2. **Stage 2 (Web Security)**: Exploit SQL Injection on OWASP Juice Shop using the target's email to recover his profile username (**adrian.kessler**).
3. **Stage 3 (Cryptography)**: Download the restricted evidence vault archive containing Juice Shop product images and crack it with the provided wordlist to recover his master password (**Kessler123!**).
4. **Stage 4 (Digital Forensics)**: Analyze web proxy logs to determine the most clicked/requested Juice Shop product image (**apple_juice.jpg**).
5. **Stage 5 (Steganography)**: Extract the covert URL embedded inside the outlier product image using Steghide (**http://localhost:8086**).
6. **Stage 6 (Networking)**: Access the internal transit portal, download the network trace, and attribute the rogue exfiltration upload to the accomplice (**Victor Hale**).

---

## 🔍 Stage 1: OSINT - Find the Uninvited Guest

### Objective
Uncover the real identity of the target behind the alias `k3ss_void` and construct his corporate email address.

### Provided Artifacts
- `stages/stage1_osint/blog_about.html` ("Notes from the Perimeter - About & Team")
- `stages/stage1_osint/leaked_paste.html` ("GhostPaste #4092 - Deploy Audit Log & Staff Roster")
- `stages/stage1_osint/forum_profile.html` ("0xNull Underground Forums - Member Profile: k3ss_void")

### Walkthrough
1. **Analyze the engineering team blog (`blog_about.html`)**:
   - The team roster lists multiple contributors (Elena Rostova, Marcus Vance, Sarah Jenkins).
   - The Lead Architect and sandbox builder is identified by first name: **Adrian**, with public handle **`k3ss_void`**.
   - Note the corporate email convention in the policy banner: `{firstname}.{lastname}@uninvited.local`.
   - Adrian's surname is deliberately withheld from public blog cards.
2. **Analyze the leaked audit dump (`leaked_paste.html`)**:
   - The document contains the internal staff cross-reference table:
     ```text
     # Badge ID | Surname   | Public Handle  | Clearance | Assigned Responsibility
     # EMP-4011 | Rostova   | el_rost        | Level 2   | AppSec / API Gateway Routing
     # EMP-4024 | Vance     | m_vance        | Level 2   | CI/CD Pipeline
     # EMP-4038 | Jenkins   | s_jenkins      | Level 2   | Database Systems
     # EMP-4401 | Kessler   | k3ss_void      | Level 4   | Lead Sandbox Admin
     ```
   - Cross-referencing handle **`k3ss_void`** reveals his surname: **Kessler**.
3. **Correlate the Identity**:
   - First Name: `Adrian`
   - Surname: `Kessler`
   - Target Identity: **Adrian Kessler**
   - Corporate Email: **`adrian.kessler@uninvited.local`** (Save this email for Stage 2!).

### Flag
- **Standard**: `Adrian Kessler`
- **Wrapped**: `uninvited{adrian_kessler}`
- *(CTFd also accepts `adrian.kessler@uninvited.local`)*

---

## 🌐 Stage 2: Web Security - Front Door

### Objective
Log into the target's account on the corporate e-commerce system (OWASP Juice Shop) and retrieve the username displayed in the user profile section.

### Target Service
- OWASP Juice Shop: `http://localhost:3000`

### Walkthrough
1. Open OWASP Juice Shop in a web browser at `http://localhost:3000/#/login`.
2. In Stage 1, we determined the target's corporate email: `adrian.kessler@uninvited.local`.
3. To bypass authentication without knowing the password, leverage Juice Shop's **SQL Injection (Authentication Bypass)** vulnerability in the email field:
   - **Email**: `adrian.kessler@uninvited.local'--`
   - **Password**: `anything` (e.g. `test123`)
4. Click **Log in**. The backend SQL query evaluates to true, authenticating you as the administrator!
5. Open the **User Profile** section (or inspect the account badge in the navigation menu).
6. The username displayed in the profile is: **`adrian.kessler`**.

### Flag
- **Standard**: `adrian.kessler`
- **Wrapped**: `uninvited{adrian.kessler}`

---

## 🔐 Stage 3: Cryptography - Locked Evidence

### Objective
Download the classified forensic archive restricted to Administrator clearance on Juice Shop, and crack it using the provided wordlist to recover Adrian Kessler's master password.

### Provided Artifacts & Service
- Service: OWASP Juice Shop (`http://localhost:3000`)
- Wordlist: `stages/stage3_crypto/wordlist.txt`

### Walkthrough
1. While logged in as administrator on Juice Shop, access the restricted Evidence Vault at:
   `http://localhost:3000/rest/admin/evidence_photos.zip`
   *(Or click the `🔐 Evidence Vault` button in the admin navigation bar).*
2. An unauthenticated request returns **HTTP 401 Unauthorized**. With admin privileges, it downloads `evidence_photos.zip`.
3. Perform a dictionary attack against the downloaded archive using the provided `wordlist.txt`:
   ```bash
   python solvers/stage3_solver.py

   # Or using zip2john / John the Ripper:
   zip2john evidence_photos.zip > zip.hash
   john --wordlist=wordlist.txt zip.hash

   # Or using fcrackzip:
   fcrackzip -u -D -p wordlist.txt evidence_photos.zip
   ```
4. The archive decrypts with the password: **`Kessler123!`**.
5. Inside the archive, you will find:
   - `flag.txt`
   - `case_notes.txt`
   - 10 real Juice Shop product images (`apple_juice.jpg`, `orange_juice.jpg`, `banana_juice.jpg`, etc.).

### Flag
- **Standard**: `Kessler123!`
- **Wrapped**: `uninvited{Kessler123!}`

---

## 📊 Stage 4: Digital Forensics - Follow the Clicks

### Objective
Analyze web proxy history to determine which Juice Shop product image was clicked/requested significantly more than any other image.

### Provided Artifacts
- `stages/stage4_forensics/proxy_history.xml`

### Walkthrough
1. Inspect the Burp Suite proxy history export `proxy_history.xml` or run frequency analysis:
   ```bash
   python solvers/stage4_solver.py
   ```
2. Analyzing requests targeting Juice Shop product images under `/assets/public/images/products/`:
   ```text
   - apple_juice.jpg          : 45 requests  <-- [OUTLIER!]
   - orange_juice.jpg         : 4 requests
   - pomegranate_drink.jpg    : 4 requests
   - banana_juice.jpg         : 3 requests
   - eggfruit_juice.jpg       : 3 requests
   - green_smoothie.jpg       : 3 requests
   - sea_buckthorn_juice.jpg  : 3 requests
   - lemon_juice.jpg          : 2 requests
   - raspberry_juice.jpg      : 2 requests
   - quince.jpg               : 2 requests
   ```
3. The most requested/clicked image on the Juice Shop website is **`apple_juice.jpg`**.
4. Cross-referencing this filename with the files extracted from Stage 3's `evidence_photos.zip` confirms that `apple_juice.jpg` is present in the evidence set!

### Flag
- **Standard**: `apple_juice.jpg`
- **Wrapped**: `uninvited{apple_juice.jpg}`

---

## 🖼️ Stage 5: Steganography - Hidden in Plain Sight

### Objective
Extract the hidden covert link embedded inside `apple_juice.jpg` using steganography tools.

### Provided Artifacts
- `apple_juice.jpg` (extracted from the Stage 3 decrypted archive `evidence_photos.zip`)

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
- **On Windows (via Docker)**:
  ```powershell
  docker run --rm -v "${PWD}:/data" -w /data debian:bookworm-slim bash -c "sed -i 's|http://|https://|g' /etc/apt/sources.list.d/debian.sources && apt-get -o Acquire::https::Verify-Peer=false update && apt-get -o Acquire::https::Verify-Peer=false install -y steghide && steghide extract -sf apple_juice.jpg -p '' && cat link.txt"
  ```

### Walkthrough
1. Run steghide extraction against `apple_juice.jpg` using an empty passphrase:
   ```bash
   steghide extract -sf apple_juice.jpg -p ""
   ```
   *(Or run `python solvers/stage5_solver.py`)*
2. Steghide writes the extracted data to `link.txt`.
3. Read the extracted payload:
   ```text
   http://localhost:8086
   ```
4. This URL leads to the internal communication channel: **The Exchange Portal**.

### Flag
- **Standard**: `http://localhost:8086`
- **Wrapped**: `uninvited{http://localhost:8086}`

---

## 📡 Stage 6: Networking - Unmasking the Uninvited Guest

### Objective
Access The Exchange Portal, download the intercepted network trace, and identify the rogue accomplice exfiltrating confidential data.

### Provided Artifacts & Services
- Service: `http://localhost:8086`
- Downloadable Artifact: `upload_capture.pcap`

### Walkthrough
1. Navigate to `http://localhost:8086` in your browser.
2. Authenticate using Adrian Kessler's credentials recovered in Stages 1 & 3:
   - **Username**: `adrian.kessler@uninvited.local`
   - **Password**: `Kessler123!`
3. After logging in, the portal dashboard displays the **Authorized Transfer Vault**.
4. Download `upload_capture.pcap`.
5. Open the capture in Wireshark. Filter for HTTP POST requests:
   ```text
   http.request.method == "POST"
   ```
6. Locate the rogue POST transaction:
   - **Source IP**: `10.5.5.15`
   - **Destination**: `10.5.5.80` (Exchange Server)
   - **Endpoint**: `POST /upload HTTP/1.1`
7. Right-click the packet $\rightarrow$ **Follow** $\rightarrow$ **TCP Stream**.
8. Observe the exfiltration headers and multipart JSON manifest:
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
9. Decode the Base64 operator token `VmljdG9yIEhhbGU=`:
   ```bash
   echo "VmljdG9yIEhhbGU=" | base64 -d
   ```
   Output:
   ```text
   Victor Hale
   ```
10. The accomplice operating the exfiltration channel is **Victor Hale**.

### Flag
- **Standard**: `Victor Hale`
- **Wrapped**: `uninvited{victor_hale}`

---

## 🏁 Summary of All Flags

| Challenge | Category | Canonical Value | Wrapped CTF Format |
| :--- | :--- | :--- | :--- |
| **Stage 1** | OSINT | `Adrian Kessler` | `uninvited{adrian_kessler}` |
| **Stage 2** | Web Security | `adrian.kessler` | `uninvited{adrian.kessler}` |
| **Stage 3** | Cryptography | `Kessler123!` | `uninvited{Kessler123!}` |
| **Stage 4** | Digital Forensics | `apple_juice.jpg` | `uninvited{apple_juice.jpg}` |
| **Stage 5** | Steganography | `http://localhost:8086` | `uninvited{http://localhost:8086}` |
| **Stage 6** | Networking | `Victor Hale` | `uninvited{victor_hale}` |
