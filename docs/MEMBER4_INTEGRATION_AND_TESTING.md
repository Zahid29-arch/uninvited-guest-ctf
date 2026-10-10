# 🧪 Member 4: Integration, Testing & Documentation
### Student ID: IT24100084 (GitHub: https://github.com/IT24100084)
### Module: SLIIT IE3132 Penetration Testing — Assignment 02
### Focus Area: End-to-End Integration, Automated Testing, Defect Resolution & Design Evolution

---

## 1. Executive Summary & Assigned Responsibilities

As **Member 4**, I was responsible for quality assurance, end-to-end integration, sequential progression enforcement, testing suites, defect logging, and comprehensive project documentation:
1. **End-to-End Progression Flow**: Chaining dependencies between Stages 1 through 6 and creating the custom tactical HUD interface (`platform/challenges.html`).
2. **Automated Testing Suite**: Engineering `tests/test_environment.py` and `tests/run_all_tests.py` providing 100% test pass verification.
3. **Defect Tracking & Fixes**: Documenting defects discovered during testing and their technical remediation.
4. **Reset/Recovery Verification**: Testing `./reset.sh` to guarantee complete state recovery without service degradation.
5. **Design Evolution from Assignment 01**: Recording architectural enhancements and justifications from Proposal 1.

---

## 2. End-to-End Flow & Sequential Flag Progression

To enforce a realistic forensic investigation where players cannot jump straight to the end, I designed a strict prerequisite chain:

$$\text{Stage 1 (OSINT)} \longrightarrow \text{Stage 2 (Web)} \longrightarrow \text{Stage 3 (Crypto)} \longrightarrow \text{Stage 4 (Forensics)} \longrightarrow \text{Stage 5 (Stego)} \longrightarrow \text{Stage 6 (Networking)}$$

* **Interface Design (`platform/challenges.html`)**:
  - Implemented dynamic grey-shaded cards with lock badges (`🔒 LOCKED`) and disabled cursor states for unreached stages.
  - As soon as a flag is submitted successfully, CTFd dynamically unlocks the subsequent stage in real-time.
* **Backend API Enforcement**:
  - Direct submissions to locked stage IDs are rejected by the scoring API, preventing flag bruteforcing or skipping.

---

## 3. Automated Testing Suite & Evidence Matrix

### A. Environment Test Suite (`tests/test_environment.py`)
I implemented a 7-point automated integration test suite that evaluates:

| Test ID | Method Name | Target Checked | Assertion / Success Metric | Status |
| :---: | :--- | :--- | :--- | :---: |
| **T1** | `test_ctfd_up` | Port `:8000` | HTTP Status 200 returned from CTFd homepage | ✅ PASS |
| **T2** | `test_juice_shop_up` | Port `:3000` | HTTP Status 200 returned from Juice Shop | ✅ PASS |
| **T3** | `test_juice_shop_target_login` | Juice Shop Auth | Authenticates target `adrian.kessler` via SQLi, JWT received | ✅ PASS |
| **T4** | `test_juice_shop_admin_vault` | Admin Vault | 401 unauthenticated, 200 authenticated, Zip size > 500 B | ✅ PASS |
| **T5** | `test_exchange_portal_up` | Port `:8086` | HTTP Status 200 returned from Dark Exchange | ✅ PASS |
| **T6** | `test_exchange_portal_login` | Exchange Auth | Logs in with `Kessler123!`, JWT session active | ✅ PASS |
| **T7** | `test_exchange_pcap_download` | File Vault | Downloads `upload_capture.pcap`, size > 10,000 bytes | ✅ PASS |

### B. Execution Proof
```text
======================================================================
Ran 7 tests in 0.183s

OK (7 passed, 0 failures, 0 errors)
```
*(Timestamped logs recorded in `tests/test_execution.log`)*.

---

## 4. Defect Log & Unintended Shortcut Prevention

During testing cycles, I identified and resolved several critical defects:

| Defect ID | Severity | Root Cause | Remediation Applied |
| :---: | :---: | :--- | :--- |
| **DEF-01** | High | Juice Shop credit card expiration year (`expYear: 2030`) failed Sequelize `min: 2080` validation on boot. | Removed redundant credit card requirement from `platform/users.yml` to prevent boot crashes. |
| **DEF-02** | High | Linux permission bit (`-rw-r--r--`) on `start.sh`, `stop.sh`, `reset.sh` threw "Permission denied". | Added executable flags (`chmod +x`) and committed native Unix file modes. |
| **DEF-03** | Medium | Players could access Stage 3 archive without completing Stage 2 login bypass. | Wrapped `/rest/admin/evidence_photos.zip` in bearer JWT admin verification middleware. |
| **DEF-04** | Low | CTFd scoreboard retained solve records across competition restarts. | Updated `reset.sh` with direct SQLite transaction wiping `solves`, `submissions`, `awards`, and `unlocks`. |

---

## 5. Reset & Recovery Test Outcomes

I executed rigorous stress testing on `reset.sh`:
* **Test Case**: Submitted flags across all 6 stages $\to$ ran `./reset.sh all` $\to$ re-polled endpoints.
* **Outcome**: Solves, submissions, and unlocks cleared within **2.8 seconds**; Stages 2–6 returned to locked status; registered user credentials were 100% preserved.

---

## 6. Record of Design Changes from Assignment 01

| Component | Assignment 01 Design | Assignment 02 Implemented Enhancement | Justification |
| :--- | :--- | :--- | :--- |
| **Stage Progression** | All challenges visible and open concurrently | Strict sequential prerequisite chain with visual lock HUD | Prevents guessing, encourages narrative immersion, matches real IR. |
| **Evidence Archive** | Static unauthenticated FTP link | Restricted Admin-only authenticated vault download in Juice Shop | Tightly integrates Stage 2 web exploit into Stage 3 crypto trigger. |
| **Contraband Exchange** | Basic static HTML file | Full Node.js/Express authenticated service with token authentication | Emulates realistic underground exfiltration infrastructure. |
| **Reset Capability** | Manual Docker container teardown | Automated transactional shell script (`reset.sh`) | Satisfies non-destructive evaluator recovery requirement. |

---
*Authored by Member 4 (IT24100084) — SLIIT IE3132 Penetration Testing.*
