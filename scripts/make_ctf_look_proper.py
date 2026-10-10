import sqlite3

conn = sqlite3.connect('platform/ctfd-data/ctfd.db')
c = conn.cursor()

# 1. Update challenge names and point values according to difficulty progression
challenges_data = [
    (1, 'Stage 1: Find the Uninvited Guest', 100),
    (2, 'Stage 2: Front Door', 100),
    (3, 'Stage 3: Locked Evidence', 150),
    (4, 'Stage 4: Follow the Clicks', 200),
    (5, 'Stage 5: Hidden in Plain Sight', 250),
    (6, 'Stage 6: Unmasking the Uninvited Guest', 350),
]

for cid, name, val in challenges_data:
    c.execute("UPDATE challenges SET name = ?, value = ? WHERE id = ?", (name, val, cid))
    print(f"[+] Updated Challenge {cid}: '{name}' ({val} pts)")

# 2. Add professional tags to tags table
c.execute("DELETE FROM tags")

tags_data = [
    (1, 'Easy'),
    (1, 'OSINT'),
    (2, 'Easy'),
    (2, 'Web Security'),
    (3, 'Moderate'),
    (3, 'Cryptography'),
    (4, 'Moderate'),
    (4, 'Digital Forensics'),
    (5, 'Mod-Hard'),
    (5, 'Steganography'),
    (6, 'Hard Capstone'),
    (6, 'Networking'),
]

tag_id = 1
for cid, tag in tags_data:
    c.execute("INSERT INTO tags (id, challenge_id, value) VALUES (?, ?, ?)", (tag_id, cid, tag))
    tag_id += 1

print(f"[+] Added {len(tags_data)} tags.")

# 3. Update Hints Cost Structure: First Hint = 10 pts, Subsequent Hints = 20 pts
c.execute("UPDATE hints SET cost = 10 WHERE title = 'Hint 1' OR title = 'Hint 1 (Cost: -10 points)'")
c.execute("UPDATE hints SET cost = 20 WHERE title != 'Hint 1' AND title != 'Hint 1 (Cost: -10 points)'")
c.execute("UPDATE hints SET title = 'Hint 1 (Cost: -10 pts)' WHERE cost = 10")
c.execute("UPDATE hints SET title = 'Hint 2 (Cost: -20 pts)' WHERE cost = 20 AND id != 13")
c.execute("UPDATE hints SET title = 'Hint 3 (Cost: -20 pts)' WHERE id = 13")
print("[+] Configured Hint deduction rules: Hint 1 = 10 pts, Hint 2+ = 20 pts.")

# 4. Ensure Wrapped Flags in Database
flags_to_ensure = [
    (1, 'uninvited{adrian.kessler@uninvited.local}'),
    (1, 'uninvited{adrian_kessler}'),
    (2, 'uninvited{dilfer}'),
    (2, 'uninvited{adrian.kessler}'),
    (3, 'uninvited{Kessler123!}'),
    (4, 'uninvited{apple_juice.jpg}'),
    (5, 'uninvited{http://localhost:8086}'),
    (5, 'uninvited{http://192.168.60.10:8086}'),
    (5, 'uninvited{http://10.67.110.77:8086}'),
    (6, 'uninvited{victor_hale}'),
    (6, 'uninvited{Victor Hale}'),
]

for cid, flag_str in flags_to_ensure:
    c.execute("SELECT id FROM flags WHERE challenge_id = ? AND content = ?", (cid, flag_str))
    if not c.fetchone():
        c.execute("INSERT INTO flags (challenge_id, type, content, data) VALUES (?, 'static', ?, '')", (cid, flag_str))
        print(f"[+] Added flag option for Challenge {cid}: {flag_str}")

# 5. Update Home Page (index) to Minimal, Professional Briefing (No leaked flags, placeholder uninvited{xxxxxx})
home_html = """<div class="container py-4">
  <div class="text-center mb-5">
    <div class="d-inline-flex align-items-center mb-3 px-3 py-1 bg-dark border border-secondary rounded-pill">
      <span class="badge bg-danger rounded-pill me-2"><i class="fas fa-shield-alt me-1"></i> CLASSIFIED</span>
      <span class="text-danger font-monospace small">INCIDENT CASE: IR-2026-UNINVITED</span>
    </div>
    <h1 class="display-4 fw-bold text-white mb-2" style="letter-spacing: 2px;">
      OPERATION UNINVITED GUEST
    </h1>
    <p class="text-secondary mb-4 mx-auto" style="max-width: 680px; font-size: 1.05rem;">
      SLIIT IE3132 Incident Response &amp; Penetration Testing CTF. Trace the digital footprint of a privileged insider threat across 6 progressive forensic stages.
    </p>
    <div class="d-flex justify-content-center gap-3">
      <a href="/challenges" class="btn btn-info px-4 py-2 fw-bold text-dark shadow-sm">
        <i class="fas fa-terminal me-2"></i> Enter Challenges
      </a>
      <a href="/scoreboard" class="btn btn-outline-warning px-4 py-2 fw-bold">
        <i class="fas fa-trophy me-2"></i> Live Scoreboard
      </a>
    </div>
  </div>

  <div class="p-4 rounded border border-secondary bg-dark text-light mb-4" style="background-color: #0d1117 !important; border-color: #30363d !important;">
    <div class="row g-4 mb-4 pb-4 border-bottom border-secondary" style="border-color: #21262d !important;">
      <div class="col-lg-6">
        <div class="d-flex align-items-center mb-2">
          <i class="fas fa-bullseye text-info me-2"></i>
          <span class="text-uppercase font-monospace text-info small fw-bold">About This CTF</span>
        </div>
        <h5 class="text-white fw-bold mb-2">Scenario-Driven Investigation</h5>
        <p class="text-secondary small mb-0" style="line-height: 1.7;">
          <strong>Operation Uninvited Guest</strong> is a multi-stage incident response and digital forensics competition. Participants assume the role of security analysts investigating an enterprise breach across six progressive domains: Open-Source Intelligence (OSINT), web exploitation, credential recovery, traffic log forensics, steganographic analysis, and network packet forensics.
        </p>
      </div>

      <div class="col-lg-6">
        <div class="d-flex align-items-center mb-2">
          <i class="fas fa-user-secret text-danger me-2"></i>
          <span class="text-uppercase font-monospace text-danger small fw-bold">Incident Storyline</span>
        </div>
        <h5 class="text-white fw-bold mb-2">The Insider Threat</h5>
        <p class="text-secondary small mb-0" style="line-height: 1.7;">
          Intrusion detection systems flagged suspicious data exfiltration originating within the internal network. Digital evidence points to a rogue infrastructure architect operating under the alias <code>k3ss_void</code> abusing privileged credentials to establish clandestine pivot points. Further telemetry reveals this insider was aided by an external operative coordinating from the shadows. Reconstruct the complete kill chain to uncover the full scope of the breach and identify the perpetrators.
        </p>
      </div>
    </div>

    <div class="row g-4 mb-4 pb-4 border-bottom border-secondary" style="border-color: #21262d !important;">
      <div class="col-lg-7">
        <div class="d-flex align-items-center mb-2">
          <i class="fas fa-shield-alt text-warning me-2"></i>
          <span class="text-uppercase font-monospace text-warning small fw-bold">Rules of Engagement</span>
        </div>
        <ul class="list-unstyled text-secondary small mb-0" style="line-height: 1.8;">
          <li class="mb-1"><i class="fas fa-check text-success me-2"></i><strong>Sequential Unlocking:</strong> Challenges must be solved in order (Stage 1 &rarr; Stage 6). Submitting a valid flag unlocks the subsequent stage.</li>
          <li class="mb-1"><i class="fas fa-check text-success me-2"></i><strong>Target Scope:</strong> Focus strictly on designated targets: OWASP Juice Shop (<code>:3000</code>) and The Exchange Portal (<code>:8086</code>).</li>
          <li class="mb-1"><i class="fas fa-ban text-danger me-2"></i><strong>No Platform Attacks:</strong> Do not attack CTFd (<code>:8000</code>) or attempt container denial of service (DoS).</li>
          <li><i class="fas fa-ban text-danger me-2"></i><strong>No High-Rate Automated Tools:</strong> Aggressive multi-threaded scanners or brute-force tools that degrade container stability are strictly prohibited.</li>
        </ul>
      </div>

      <div class="col-lg-5">
        <div class="d-flex align-items-center mb-2">
          <i class="fas fa-sliders-h text-primary me-2"></i>
          <span class="text-uppercase font-monospace text-primary small fw-bold">Operational Parameters</span>
        </div>
        <div class="p-3 rounded border border-secondary" style="background-color: #161b22; border-color: #30363d !important;">
          <div class="row g-2 mb-2">
            <div class="col-6">
              <div class="text-muted small text-uppercase font-monospace">Time Duration</div>
              <div class="h6 text-white mb-0 fw-bold">60 – 90 Minutes</div>
              <div class="text-secondary" style="font-size: 0.75rem;">Walkthrough: ~20m</div>
            </div>
            <div class="col-6">
              <div class="text-muted small text-uppercase font-monospace">Total Points</div>
              <div class="h6 text-info mb-0 fw-bold">1,150 Maximum Pts</div>
              <div class="text-secondary" style="font-size: 0.75rem;">6 Progressive Stages</div>
            </div>
          </div>
          <div class="pt-2 border-top border-secondary" style="border-color: #30363d !important;">
            <div class="text-muted small text-uppercase font-monospace mb-1">Hint Cost &amp; Penalty</div>
            <div class="text-warning small mb-0 font-monospace">
              <i class="fas fa-exclamation-triangle me-1"></i>
              <strong>First Hint:</strong> -10 Pts &bull; <strong>Remaining Hints:</strong> -20 Pts each
            </div>
          </div>
        </div>
      </div>
    </div>

    <div>
      <div class="d-flex align-items-center mb-2">
        <i class="fas fa-flag text-success me-2"></i>
        <span class="text-uppercase font-monospace text-success small fw-bold">Flag Submission Format</span>
      </div>
      <p class="text-secondary small mb-3" style="line-height: 1.6;">
        All flags must be submitted using the standardized CTF format: <code class="text-info bg-black px-2 py-1 rounded font-monospace">uninvited{xxxxxx}</code>. Replace <code class="text-info font-monospace">xxxxxx</code> with the specific target value discovered during your investigation.
      </p>

      <div class="table-responsive">
        <table class="table table-dark table-sm table-borderless font-monospace small mb-0" style="background-color: transparent;">
          <thead>
            <tr class="text-muted border-bottom border-secondary" style="border-color: #30363d !important;">
              <th scope="col" style="width: 20%;">Stage</th>
              <th scope="col" style="width: 35%;">Investigation Domain</th>
              <th scope="col" style="width: 45%;">Required Flag Submission Format</th>
            </tr>
          </thead>
          <tbody class="text-secondary">
            <tr class="border-bottom border-secondary" style="border-color: #21262d !important;">
              <td class="text-white fw-bold">Stage 1</td>
              <td>OSINT Reconnaissance</td>
              <td><code class="text-info">uninvited{xxxxxx}</code> <span class="text-muted">(Suspect Email or Identity)</span></td>
            </tr>
            <tr class="border-bottom border-secondary" style="border-color: #21262d !important;">
              <td class="text-white fw-bold">Stage 2</td>
              <td>Web Exploitation (SQLi)</td>
              <td><code class="text-info">uninvited{xxxxxx}</code> <span class="text-muted">(Extracted Admin Username)</span></td>
            </tr>
            <tr class="border-bottom border-secondary" style="border-color: #21262d !important;">
              <td class="text-white fw-bold">Stage 3</td>
              <td>Password Hash Cracking</td>
              <td><code class="text-info">uninvited{xxxxxx}</code> <span class="text-muted">(Recovered Master Password)</span></td>
            </tr>
            <tr class="border-bottom border-secondary" style="border-color: #21262d !important;">
              <td class="text-white fw-bold">Stage 4</td>
              <td>Forensic Log Analysis</td>
              <td><code class="text-info">uninvited{xxxxxx}</code> <span class="text-muted">(Exfiltrated Outlier Filename)</span></td>
            </tr>
            <tr class="border-bottom border-secondary" style="border-color: #21262d !important;">
              <td class="text-white fw-bold">Stage 5</td>
              <td>Steganography Extraction</td>
              <td><code class="text-info">uninvited{xxxxxx}</code> <span class="text-muted">(Extracted Internal Service URL)</span></td>
            </tr>
            <tr>
              <td class="text-white fw-bold">Stage 6</td>
              <td>Network Forensics (PCAP)</td>
              <td><code class="text-info">uninvited{xxxxxx}</code> <span class="text-muted">(Accomplice Real Name)</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="d-flex flex-wrap justify-content-between align-items-center text-muted small px-3 py-2 border border-secondary rounded font-monospace" style="background-color: #0d1117; border-color: #21262d !important;">
    <div><i class="fas fa-network-wired text-success me-2"></i>Network: <strong>Docker uninvited_net</strong></div>
    <div><i class="fas fa-crosshairs text-warning me-2"></i>Target Hosts: <strong>Juice Shop (:3000) &bull; Exchange (:8086)</strong></div>
    <div><i class="fas fa-microchip text-info me-2"></i>Engine: <strong>CTFd v3.7.0</strong></div>
  </div>
</div>"""

c.execute("UPDATE pages SET title = 'Operation Uninvited Guest', content = ?, format = 'html' WHERE route = 'index'", (home_html,))
print("[+] Updated Home Page (index) with format='html' and clean minimal layout.")

conn.commit()
conn.close()
print("[+] Database updates complete.")
