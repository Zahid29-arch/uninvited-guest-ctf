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

# 3. Update Home Page (index) to Minimal Cyber Incident Briefing Dossier
home_html = """
<div class="container py-4">
  <!-- Top Hero Header -->
  <div class="text-center mb-5">
    <div class="d-inline-flex align-items-center mb-3 px-3 py-1 bg-dark border border-secondary rounded-pill">
      <span class="badge bg-danger rounded-pill me-2"><i class="fas fa-radiation me-1"></i> CLASSIFIED</span>
      <span class="text-danger font-monospace small">INCIDENT CASE: IR-2026-UNINVITED</span>
    </div>
    <h1 class="display-4 fw-bold text-white mb-2" style="letter-spacing: 2px;">
      OPERATION UNINVITED GUEST
    </h1>
    <p class="lead text-secondary mb-4 mx-auto" style="max-width: 720px; font-size: 1.1rem;">
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

  <!-- Minimal Incident Briefing Container -->
  <div class="p-4 rounded border border-secondary bg-dark text-light mb-4" style="background-color: #0d1117 !important; border-color: #30363d !important;">
    
    <!-- 1. Mission Overview & Storyline -->
    <div class="row g-4 mb-4 pb-4 border-bottom border-secondary" style="border-color: #21262d !important;">
      <div class="col-lg-6">
        <div class="d-flex align-items-center mb-2">
          <i class="fas fa-bullseye text-info me-2"></i>
          <span class="text-uppercase font-monospace text-info small fw-bold tracking-wider">About This CTF</span>
        </div>
        <h5 class="text-white fw-bold mb-2">Scenario-Driven Investigation</h5>
        <p class="text-secondary small mb-0" style="line-height: 1.7;">
          <strong>Operation Uninvited Guest</strong> is an immersive incident response competition simulating a real-world enterprise compromise. Participants take on the role of forensic investigators conducting Open-Source Intelligence (OSINT), web exploitation, credential cracking, traffic log forensics, steganographic recovery, and network packet analysis.
        </p>
      </div>

      <div class="col-lg-6">
        <div class="d-flex align-items-center mb-2">
          <i class="fas fa-user-secret text-danger me-2"></i>
          <span class="text-uppercase font-monospace text-danger small fw-bold tracking-wider">Incident Storyline</span>
        </div>
        <h5 class="text-white fw-bold mb-2">The Insider Threat</h5>
        <p class="text-secondary small mb-0" style="line-height: 1.7;">
          Security alerts flagged unauthorized exfiltration from internal systems. Audit logs pinpoint lead infrastructure architect <strong>Adrian Kessler</strong> (alias <code>k3ss_void</code>) abusing his administrative access to pivot across network boundaries. Further telemetry reveals Adrian conspired with an external operative, <strong>Victor Hale</strong>. Reconstruct the full kill chain to bring them to justice.
        </p>
      </div>
    </div>

    <!-- 2. Rules & Operational Parameters -->
    <div class="row g-4 mb-4 pb-4 border-bottom border-secondary" style="border-color: #21262d !important;">
      <!-- Rules of Engagement -->
      <div class="col-lg-7">
        <div class="d-flex align-items-center mb-2">
          <i class="fas fa-shield-alt text-warning me-2"></i>
          <span class="text-uppercase font-monospace text-warning small fw-bold tracking-wider">Rules of Engagement</span>
        </div>
        <ul class="list-unstyled text-secondary small mb-0" style="line-height: 1.8;">
          <li class="mb-1"><i class="fas fa-check text-success me-2"></i><strong>Sequential Unlocking:</strong> Challenges must be solved in order (Stage 1 &rarr; Stage 6). Solving each stage unlocks downstream leads.</li>
          <li class="mb-1"><i class="fas fa-check text-success me-2"></i><strong>Target Scope:</strong> Focus strictly on target services: Juice Shop (<code>:3000</code>) and Exchange Portal (<code>:8086</code>).</li>
          <li class="mb-1"><i class="fas fa-ban text-danger me-2"></i><strong>No Platform Attacks:</strong> Do not attack CTFd infrastructure (<code>:8000</code>) or attempt container denial of service (DoS).</li>
          <li><i class="fas fa-ban text-danger me-2"></i><strong>No Aggressive Scanners:</strong> Heavy automated fuzzers or brute-force tools that degrade container stability are strictly prohibited.</li>
        </ul>
      </div>

      <!-- Operational Parameters: Duration & Hints -->
      <div class="col-lg-5">
        <div class="d-flex align-items-center mb-2">
          <i class="fas fa-sliders-h text-primary me-2"></i>
          <span class="text-uppercase font-monospace text-primary small fw-bold tracking-wider">Operational Parameters</span>
        </div>
        <div class="row g-2">
          <div class="col-6">
            <div class="p-3 rounded border border-secondary h-100" style="background-color: #161b22; border-color: #30363d !important;">
              <div class="text-muted small text-uppercase font-monospace">Duration</div>
              <div class="h5 text-white mb-0 fw-bold">60–90 Min</div>
              <div class="text-secondary small">Walkthrough: ~20m</div>
            </div>
          </div>
          <div class="col-6">
            <div class="p-3 rounded border border-secondary h-100" style="background-color: #161b22; border-color: #30363d !important;">
              <div class="text-muted small text-uppercase font-monospace">Hint Cost</div>
              <div class="h5 text-warning mb-0 fw-bold">-10 Pts</div>
              <div class="text-secondary small">Per unlocked hint</div>
            </div>
          </div>
          <div class="col-12 mt-2">
            <div class="p-2 rounded border border-secondary d-flex justify-content-between align-items-center" style="background-color: #161b22; border-color: #30363d !important;">
              <span class="text-secondary small font-monospace"><i class="fas fa-layer-group text-info me-2"></i>Total Scoring</span>
              <span class="text-info font-monospace fw-bold small">6 Stages &bull; 1,150 Maximum Pts</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. Flag Submission Template & Format -->
    <div>
      <div class="d-flex align-items-center mb-2">
        <i class="fas fa-flag text-success me-2"></i>
        <span class="text-uppercase font-monospace text-success small fw-bold tracking-wider">Flag Submission Template</span>
      </div>
      <p class="text-secondary small mb-3">
        Flags can be submitted either in the standard CTF wrapper format <code class="text-info bg-black px-2 py-1 rounded">uninvited{...}</code> or as raw plaintext values discovered during your forensic analysis. Both formats are recognized by the scoring engine:
      </p>

      <div class="table-responsive">
        <table class="table table-dark table-sm table-borderless font-monospace small mb-0" style="background-color: transparent;">
          <thead>
            <tr class="text-muted border-bottom border-secondary" style="border-color: #30363d !important;">
              <th scope="col" style="width: 15%;">Stage</th>
              <th scope="col" style="width: 25%;">Domain</th>
              <th scope="col" style="width: 32%;">Standard Wrapped Format</th>
              <th scope="col" style="width: 28%;">Accepted Plain Value</th>
            </tr>
          </thead>
          <tbody class="text-secondary">
            <tr class="border-bottom border-secondary" style="border-color: #21262d !important;">
              <td class="text-white fw-bold">Stage 1</td>
              <td>OSINT Investigation</td>
              <td><code class="text-info">uninvited{adrian_kessler}</code></td>
              <td><code>Adrian Kessler</code></td>
            </tr>
            <tr class="border-bottom border-secondary" style="border-color: #21262d !important;">
              <td class="text-white fw-bold">Stage 2</td>
              <td>Web Exploitation (SQLi)</td>
              <td><code class="text-info">uninvited{adrian.kessler}</code></td>
              <td><code>adrian.kessler</code></td>
            </tr>
            <tr class="border-bottom border-secondary" style="border-color: #21262d !important;">
              <td class="text-white fw-bold">Stage 3</td>
              <td>Password Hash Cracking</td>
              <td><code class="text-info">uninvited{Kessler123!}</code></td>
              <td><code>Kessler123!</code></td>
            </tr>
            <tr class="border-bottom border-secondary" style="border-color: #21262d !important;">
              <td class="text-white fw-bold">Stage 4</td>
              <td>Forensic Log Analysis</td>
              <td><code class="text-info">uninvited{apple_juice.jpg}</code></td>
              <td><code>apple_juice.jpg</code></td>
            </tr>
            <tr class="border-bottom border-secondary" style="border-color: #21262d !important;">
              <td class="text-white fw-bold">Stage 5</td>
              <td>Steganography Extraction</td>
              <td><code class="text-info">uninvited{http://localhost:8086}</code></td>
              <td><code>http://localhost:8086</code></td>
            </tr>
            <tr>
              <td class="text-white fw-bold">Stage 6</td>
              <td>Network Forensics (PCAP)</td>
              <td><code class="text-info">uninvited{victor_hale}</code></td>
              <td><code>Victor Hale</code></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>

  <!-- Minimal Meta Bar -->
  <div class="d-flex flex-wrap justify-content-between align-items-center text-muted small px-3 py-2 border border-secondary rounded font-monospace" style="background-color: #0d1117; border-color: #21262d !important;">
    <div><i class="fas fa-network-wired text-success me-2"></i>Network: <strong>Docker uninvited_net</strong></div>
    <div><i class="fas fa-crosshairs text-warning me-2"></i>Target Hosts: <strong>Juice Shop (:3000) &bull; Exchange (:8086)</strong></div>
    <div><i class="fas fa-microchip text-info me-2"></i>Engine: <strong>CTFd v3.7.0</strong></div>
  </div>
</div>
"""

c.execute("UPDATE pages SET title = 'Operation Uninvited Guest', content = ? WHERE route = 'index'", (home_html,))
print("[+] Updated Home Page (index) with classified mission dossier.")

conn.commit()
conn.close()
print("[+] Database updates complete.")
