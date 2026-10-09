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

# 3. Update Home Page (index) to Classified Cyber Mission Dossier
home_html = """
<div class="container py-4">
  <div class="row align-items-center mb-5">
    <div class="col-lg-8 mx-auto text-center">
      <div class="d-inline-flex align-items-center mb-3 px-3 py-1 bg-dark border border-danger rounded-pill">
        <span class="badge bg-danger rounded-pill me-2"><i class="fas fa-radiation fa-spin me-1"></i> CLASSIFIED</span>
        <span class="text-danger font-monospace small">INCIDENT CASE: IR-2026-UNINVITED</span>
      </div>
      <h1 class="display-4 fw-bold text-white mb-3" style="letter-spacing: 2px;">
        OPERATION UNINVITED GUEST
      </h1>
      <p class="lead text-info mb-4">
        SLIIT IE3132 Penetration Testing // Incident Response & Forensic CTF Play Box
      </p>
      <div class="d-flex justify-content-center gap-3">
        <a href="/challenges" class="btn btn-info btn-lg px-4 py-2 fw-bold text-dark shadow-sm">
          <i class="fas fa-terminal me-2"></i> Enter Challenges
        </a>
        <a href="/scoreboard" class="btn btn-outline-warning btn-lg px-4 py-2 fw-bold">
          <i class="fas fa-trophy me-2"></i> Live Scoreboard
        </a>
      </div>
    </div>
  </div>

  <div class="row g-4 mb-5">
    <div class="col-md-4">
      <div class="card h-100 bg-dark text-white border-secondary shadow-sm">
        <div class="card-body">
          <div class="text-danger h3 mb-3"><i class="fas fa-user-secret"></i> Threat Actor Dossier</div>
          <h5 class="card-title text-white">Target: Adrian Kessler</h5>
          <p class="card-text text-muted small">
            Infrastructure architect operating under the alias <code>k3ss_void</code>. Audit records indicate deliberate exfiltration pipelines established across internal perimeter services.
          </p>
          <div class="border-top border-secondary pt-2 text-danger small">
            <strong>Accomplice:</strong> Identity concealed in network traffic
          </div>
        </div>
      </div>
    </div>

    <div class="col-md-4">
      <div class="card h-100 bg-dark text-white border-secondary shadow-sm">
        <div class="card-body">
          <div class="text-info h3 mb-3"><i class="fas fa-diagram-project"></i> Investigation Pathway</div>
          <h5 class="card-title text-white">6 Progressive Stages</h5>
          <p class="card-text text-muted small">
            Investigation spans 6 critical security domains: Open-Source Intelligence, Web Exploitation, Cryptographic Cracking, Proxy Forensics, Steganographic Extraction, and Deep Packet Inspection.
          </p>
          <div class="border-top border-secondary pt-2 text-info small">
            <strong>Flag Validation:</strong> CTFd scoring engine (Platform-based)
          </div>
        </div>
      </div>
    </div>

    <div class="col-md-4">
      <div class="card h-100 bg-dark text-white border-secondary shadow-sm">
        <div class="card-body">
          <div class="text-warning h3 mb-3"><i class="fas fa-shield-halved"></i> Rules of Engagement</div>
          <h5 class="card-title text-white">Standard CTF Protocol</h5>
          <p class="card-text text-muted small">
            Sequential unlocking is strictly enforced. Complete prerequisite challenges to reveal downstream attack vectors. Denial of service against platform containers is prohibited.
          </p>
          <div class="border-top border-secondary pt-2 text-warning small">
            <strong>Total Scoring:</strong> 1,150 Maximum Points
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="card bg-dark text-white border-secondary p-4 text-center">
    <div class="row align-items-center">
      <div class="col-md-3 text-center border-end border-secondary">
        <div class="text-muted small text-uppercase">Platform Framework</div>
        <div class="h5 text-info mb-0">CTFd v3.7.0</div>
      </div>
      <div class="col-md-3 text-center border-end border-secondary">
        <div class="text-muted small text-uppercase">Target Services</div>
        <div class="h5 text-warning mb-0">Juice Shop & Exchange</div>
      </div>
      <div class="col-md-3 text-center border-end border-secondary">
        <div class="text-muted small text-uppercase">Environment Isolation</div>
        <div class="h5 text-success mb-0">Docker uninvited_net</div>
      </div>
      <div class="col-md-3 text-center">
        <div class="text-muted small text-uppercase">Host System</div>
        <div class="h5 text-danger mb-0">Ubuntu Server 22.04</div>
      </div>
    </div>
  </div>
</div>
"""

c.execute("UPDATE pages SET title = 'Operation Uninvited Guest', content = ? WHERE route = 'index'", (home_html,))
print("[+] Updated Home Page (index) with classified mission dossier.")

conn.commit()
conn.close()
print("[+] Database updates complete.")
