# 👥 Evidence of Individual Contribution & Role Allocation
### SLIIT IE3132 Penetration Testing — Year 3 Semester 1 — Assignment 02
**Project: Operation Uninvited Guest**

This document provides formal evidence of individual member contributions, file ownership, test execution logs, and architecture responsibilities in full accordance with the **Assignment 02 Final Stage Deliverables** specification.

---

## 1. Member Contribution & Allocation Matrix

Following the approved project plan, the workload was systematically distributed across four specialized roles:

| Member / Role | Focus Area | GitHub Account & Commits | Files Authored & Managed | Deliverables & Technical Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **Member 1**<br>*(Platform Architect)*<br>`IT24103264` | **CTF Infrastructure & Orchestration** | [`@IT24103264`](https://github.com/IT24103264)<br>*(Commits authored by `IT24103264`)* | • `docker-compose.yml`<br>• `start.sh`<br>• `stop.sh`<br>• `reset.sh`<br>• `docs/MEMBER1_ARCHITECTURE_AND_DEPLOYMENT.md` | • Docker Compose orchestration of 3 services<br>• Isolated bridge network `uninvited_net`<br>• Host port restriction (`:8000`, `:3000`, `:8086`)<br>• Zero-setup state reset script (`reset.sh`)<br>• Database seeding & hint deduction policy |
| **Member 2**<br>*(Challenge Engineer A)*<br>`IT24100066` | **Challenge Design: Stages 1–3**<br>*(OSINT, Web Security, Cryptography)* | [`@IT24100066`](https://github.com/IT24100066)<br>*(Commits authored by `IT24100066`)* | • `stages/stage1_osint/*`<br>• `stages/stage3_crypto/*`<br>• `solvers/stage1_solver.py`<br>• `solvers/stage2_solver.py`<br>• `solvers/stage3_solver.py`<br>• `docs/MEMBER2_CHALLENGE_DESIGN_A.md` | • Multi-source OSINT correlation scenario<br>• Juice Shop target account configuration<br>• SQL Injection authentication bypass vector<br>• Restricted evidence vault authorization<br>• AES/ZipCrypto dictionary cracking build<br>• Reference solvers for Stages 1, 2, and 3 |
| **Member 3**<br>*(Challenge Engineer B)*<br>`Zahid29-arch` *(Repo Owner)* | **Challenge Design: Stages 4–6**<br>*(Forensics, Steganography, PCAP)* | [`@Zahid29-arch`](https://github.com/Zahid29-arch)<br>*(Repository Owner & Lead Integrator)* | • `stages/stage4_forensics/*`<br>• `stages/stage5_stego/*`<br>• `stages/stage6_pcap/*`<br>• `platform/exchange-portal/*`<br>• `solvers/stage4_solver.py`<br>• `solvers/stage5_solver.py`<br>• `solvers/stage6_solver.py`<br>• `docs/MEMBER3_CHALLENGE_DESIGN_B.md` | • Synthetic Burp proxy log generator (114 KB)<br>• Log outlier frequency distribution logic<br>• Steghide payload embedding automation<br>• Scapy PCAP stream generator script (25 KB)<br>• Custom Express.js Dark Exchange Portal<br>• Multi-stage reference solvers 4, 5, and 6 |
| **Member 4**<br>*(Integration & QA)*<br>`IT24100084` | **Integration, Testing & Documentation** | [`@IT24100084`](https://github.com/IT24100084)<br>*(Commits authored by `IT24100084`)* | • `tests/test_environment.py`<br>• `tests/run_all_tests.py`<br>• `tests/test_execution.log`<br>• `platform/challenges.html`<br>• `README.md`<br>• `WRITEUP.md`<br>• `EVIDENCE_OF_CONTRIBUTION.md`<br>• `docs/MEMBER4_INTEGRATION_AND_TESTING.md` | • 7-point automated environment unit test suite<br>• Real-time progressive locking HUD<br>• Dynamic IP binding & multi-device resolution<br>• Unintended shortcut validation<br>• Complete author write-up & submission docs<br>• Execution log audit verification |

---

## 2. Component Ownership & Source Code Mapping

### A. Exploit & Reference Solvers (`solvers/`)
- `solvers/stage1_solver.py`: OSINT identity correlation engine *(Member 2)*
- `solvers/stage2_solver.py`: SQL injection bypass & admin JWT extractor *(Member 2)*
- `solvers/stage3_solver.py`: Multi-threaded dictionary cracking solver *(Member 2)*
- `solvers/stage4_solver.py`: XML log parsing & request frequency analyzer *(Member 3)*
- `solvers/stage5_solver.py`: Steghide carrier payload extractor *(Member 3)*
- `solvers/stage6_solver.py`: Scapy/native PCAP stream reassembler & Base64 decoder *(Member 3)*

### B. Challenge Generation & Synthesis Scripts (`stages/`)
- `stages/stage3_crypto/build_evidence_zip.py`: Packages and encrypts `evidence_photos.zip` with target password `Kessler123!` *(Member 2)*
- `stages/stage4_forensics/generate_proxy_log.py`: Synthesizes 114 KB Burp Suite XML history with realistic HTTP headers and access skew *(Member 3)*
- `stages/stage5_stego/embed_stego.py`: Injects secret link into JPEG DCT coefficients via Steghide *(Member 3)*
- `stages/stage6_pcap/generate_pcap.py`: Generates synthetic network trace with handshakes, background traffic, and rogue multipart POST *(Member 3)*

### C. Platform Architecture & Orchestration (`platform/`, Root)
- `docker-compose.yml`: Multi-container topology, isolated bridge network, port restrictions *(Member 1)*
- `start.sh` / `stop.sh`: Linux deployment and container lifecycle management *(Member 1)*
- `reset.sh`: Automated database wipe, solve cleanup, and state zero restoration *(Member 1)*
- `scripts/make_ctf_look_proper.py`: Automated CTFd database provisioning, hint costs, and theme seeding *(Member 1)*
- `platform/challenges.html`: Cyber HUD interface with progressive lock states and dynamic IP discovery *(Member 4)*

### D. Testing & Quality Assurance (`tests/`)
- `tests/test_environment.py`: Automated integration test suite covering ports, endpoints, JWTs, and archives *(Member 4)*
- `tests/run_all_tests.py`: Master test runner executing both environment tests and all 6 solver pipelines *(Member 4)*
- `tests/test_execution.log`: Verifiable timestamped log recording 100% test pass rate *(Member 4)*

---

## 3. Git Repository Commit & Contribution History

Repository URL: `https://github.com/Zahid29-arch/uninvited-guest-ctf`

In team development, work was consolidated through pair-programming and centralized integration by the repository administrator (`Zahid29-arch`), with clear thematic commits corresponding to each functional area:

1. **Infrastructure & Platform Orchestration (Member 1 — IT24103264)**:
   - `ce87acb`: `feat(infra): document platform architecture, deployment orchestration, and security controls` (Author: `IT24103264`)
   - `0ce7a0f`: `chore(compose): remove obsolete version attribute`
   - `8a7141a`: `feat(linux): add start.sh/stop.sh launchers and gitattributes for native Ubuntu/Kali compatibility`
   - `750fb76`: `feat(deploy): bundle preconfigured ctfd-data for seamless zero-setup player deployment`
   - `9646240`: `Add sequential stage unlocking prerequisites and reset.sh script`

2. **Stage 1–3 Challenge Engineering (Member 2 — IT24100066)**:
   - `a6430d4`: `feat(design-a): author Challenge Design A specification, exploit walkthroughs, and solvers for Stages 1-3` (Author: `IT24100066`)
   - `b7d7f1a`: `feat(ctf): overhaul game flow across stages 1-6 with split OSINT, real product images, log anomaly`
   - `58fe136`: `fix(ctfd): remove tooling commands and flag spoilers from challenge descriptions`
   - `d946eb5`: `Refactor CTFd home page: minimal layout, placeholder flag format uninvited{xxxxxx}, no plain values, and updated hint costs`

3. **Stage 4–6 Challenge Engineering & Exchange Portal (Member 3 — Zahid29-arch)**:
   - `bcbc458`: `feat(design-b): author Challenge Design B specification, forensic artifacts, and solvers for Stages 4-6` (Author: `Zahid29-arch`)
   - `10ce19a`: `feat(portal): update Exchange UI to contraband ledger, bind DHCP/ARP/MAC metadata in PCAP`
   - `8706dd6`: `feat(portal): add dynamic image gallery with manual upload and lightbox viewer`
   - `eada641`: `feat(portal): update portal branding to THE DARK EXCHANGE and add gitignore entries`
   - `776749a`: `Replace exchange portal gallery with custom surveillance images`

4. **Integration, Automated Testing & Documentation (Member 4 — IT24100084)**:
   - `fbed1af`: `feat(testing): author integration test matrix, defect tracking log, and design evolution record` (Author: `IT24100084`)
   - `a2af531`: `test: make portal dashboard verification dynamic to portal branding`
   - `fd98386`: `Remove localhost links from challenge descriptions and enable dynamic host IP adjustment`
   - `63f7a87`: `Fix Page Unresponsive freeze caused by recursive MutationObserver in challenges.html`
   - `cfa22fd`: `Number all 6 stages, add domain badges/tags, and upgrade CTFd to cyber tactical HUD interface`
   - `d40e394`: `Update README with Assignment 02 rubric matrix, reset guide, and native PCAP solver fallback`

---

## 4. Test Logs & Verification Evidence

All automated test logs are saved directly in [`tests/test_execution.log`](tests/test_execution.log).

### Summary of Latest Verification Run:
- **Environment Unit Tests (`tests/test_environment.py`)**: 7/7 PASSED (0.183s)
- **Stage 1 Solver (`solvers/stage1_solver.py`)**: PASSED (Exit Code: 0)
- **Stage 2 Solver (`solvers/stage2_solver.py`)**: PASSED (Exit Code: 0)
- **Stage 3 Solver (`solvers/stage3_solver.py`)**: PASSED (Exit Code: 0)
- **Stage 4 Solver (`solvers/stage4_solver.py`)**: PASSED (Exit Code: 0)
- **Stage 5 Solver (`solvers/stage5_solver.py`)**: PASSED (Exit Code: 0)
- **Stage 6 Solver (`solvers/stage6_solver.py`)**: PASSED (Exit Code: 0)
- **Overall Result**: **100% Passed (Zero Failures)**
