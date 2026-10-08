const express = require('express');
const cookieParser = require('cookie-parser');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 8086;

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());

// Serve static assets from public/ (including /gallery/)
const publicDir = path.join(__dirname, 'public');
app.use(express.static(publicDir));
app.use('/gallery', express.static(path.join(publicDir, 'gallery')));

// Check authentication
function isAuthenticated(req) {
    return req.cookies && req.cookies.portal_auth;
}

// Login Page (GET / and GET /login)
function renderLoginPage(req, res) {
    if (isAuthenticated(req)) {
        return res.redirect('/portal');
    }

    const hasError = req.query.error === '1';
    const errorHtml = hasError ? '<div class="alert-error">Invalid operator credentials. Access Denied.</div>' : '';

    res.send(`<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Exchange :: Covert Network Gateway</title>
    <style>
        :root {
            --bg: #07090e;
            --card: #0f141f;
            --border: #1e2638;
            --accent: #ef4444;
            --text: #f1f5f9;
            --muted: #8b9bb4;
            --danger: #ef4444;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        .login-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 36px 32px;
            width: 100%;
            max-width: 440px;
            box-shadow: 0 10px 35px rgba(0,0,0,0.7);
        }
        .header { text-align: center; margin-bottom: 26px; }
        .badge {
            display: inline-block;
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid var(--accent);
            color: var(--accent);
            font-family: monospace;
            font-size: 0.78rem;
            padding: 4px 10px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
        }
        h1 { font-size: 1.35rem; font-weight: 700; color: #fff; margin-bottom: 6px; letter-spacing: -0.3px; }
        p.sub { color: var(--muted); font-size: 0.85rem; line-height: 1.5; }
        .alert-error {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid var(--danger);
            color: #fca5a5;
            padding: 10px 14px;
            border-radius: 6px;
            font-size: 0.85rem;
            margin-bottom: 20px;
            text-align: center;
        }
        .form-group { margin-bottom: 18px; }
        label { display: block; font-size: 0.8rem; font-weight: 600; color: var(--muted); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
        input[type="text"], input[type="password"] {
            width: 100%;
            background: #07090e;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 12px 14px;
            color: #fff;
            font-size: 0.95rem;
            font-family: monospace;
            outline: none;
            transition: border-color 0.2s;
        }
        input[type="text"]:focus, input[type="password"]:focus {
            border-color: var(--accent);
        }
        .btn-submit {
            width: 100%;
            background: #b91c1c;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 12px;
            font-size: 0.95rem;
            font-weight: 700;
            cursor: pointer;
            margin-top: 8px;
            letter-spacing: 0.5px;
            transition: background 0.2s;
        }
        .btn-submit:hover { background: #dc2626; }
        .footer-note {
            text-align: center;
            font-family: monospace;
            font-size: 0.72rem;
            color: #55657e;
            margin-top: 24px;
            border-top: 1px solid var(--border);
            padding-top: 14px;
        }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="header">
            <div class="badge">Restricted Contraband Network</div>
            <h1>THE EXCHANGE // PORTAL</h1>
            <p class="sub">Encrypted internal clearinghouse for illicit consignments, contraband exchanges, and exfiltrated payloads.</p>
        </div>
        ${errorHtml}
        <form action="/login" method="POST">
            <div class="form-group">
                <label for="username">Operator Email / Handle</label>
                <input type="text" id="username" name="username" placeholder="adrian.kessler@uninvited.local" required autocomplete="off">
            </div>
            <div class="form-group">
                <label for="password">Cryptographic Master Key</label>
                <input type="password" id="password" name="password" placeholder="••••••••••••" required>
            </div>
            <button type="submit" class="btn-submit">Access Exchange Vault</button>
        </form>
        <div class="footer-note">NODE: EXCH-8086 • UNINVITED CLANDESTINE ROUTING</div>
    </div>
</body>
</html>`);
}

app.get('/', renderLoginPage);
app.get('/login', renderLoginPage);

// Authentication Handler (POST /login)
app.post('/login', (req, res) => {
    const user = (req.body.username || req.body.user || '').trim();
    const pass = (req.body.password || req.body.pass || '').trim();

    const validUser = (
        user === 'adrian.kessler@uninvited.local' ||
        user === 'adrian.kessler' ||
        user === 'DragonFly'
    );

    const validPass = (
        pass === 'Kessler123!' ||
        pass === 'Password123!' ||
        pass === 'Exch@nge2026'
    );

    if (validUser && validPass) {
        res.cookie('portal_auth', user, {
            httpOnly: true,
            maxAge: 3600000
        });
        return res.redirect('/portal');
    }

    res.redirect('/login?error=1');
});

// Authenticated Dashboard (GET /portal)
app.get('/portal', (req, res) => {
    if (!isAuthenticated(req)) {
        return res.redirect('/login');
    }

    const username = req.cookies.portal_auth || 'adrian.kessler';

    res.send(`<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Exchange :: Active Consignment Vault</title>
    <style>
        :root {
            --bg: #07090e;
            --card: #0f141f;
            --border: #1e2638;
            --accent: #ef4444;
            --success: #10b981;
            --text: #f1f5f9;
            --muted: #8b9bb4;
            --warning: #f59e0b;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace, sans-serif;
            padding: 30px 20px;
        }
        .container { max-width: 920px; margin: 0 auto; }
        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--card);
            border: 1px solid var(--border);
            padding: 16px 24px;
            border-radius: 10px;
            margin-bottom: 24px;
        }
        .brand { font-size: 1.15rem; font-weight: 800; color: #fff; letter-spacing: 0.5px; }
        .brand span { color: var(--accent); }
        .user-tag { color: var(--success); font-weight: 600; font-family: monospace; }
        .btn-logout {
            background: #1e2638;
            color: #f87171;
            border: 1px solid #334155;
            padding: 6px 12px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.82rem;
            font-weight: 600;
        }
        .panel {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 28px;
            margin-bottom: 24px;
        }
        h2 { font-size: 1.25rem; margin-bottom: 10px; color: #fff; display: flex; align-items: center; gap: 8px; }
        p.desc { color: var(--muted); font-size: 0.92rem; line-height: 1.6; margin-bottom: 22px; }
        .status-badge {
            display: inline-block;
            background: rgba(16, 185, 129, 0.15);
            color: var(--success);
            border: 1px solid var(--success);
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 700;
            font-family: monospace;
        }
        .badge-danger {
            background: rgba(239, 68, 68, 0.15);
            color: var(--accent);
            border-color: var(--accent);
        }
        .badge-warn {
            background: rgba(245, 158, 11, 0.15);
            color: var(--warning);
            border-color: var(--warning);
        }
        .ledger-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.88rem; }
        .ledger-table th { text-align: left; padding: 12px 14px; border-bottom: 1px solid var(--border); color: var(--muted); font-size: 0.78rem; text-transform: uppercase; font-family: monospace; }
        .ledger-table td { padding: 14px; border-bottom: 1px solid #141a29; vertical-align: middle; }
        .notice-box {
            background: #141720;
            border-left: 4px solid var(--warning);
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
            margin-top: 24px;
            font-size: 0.88rem;
            color: #d1d5db;
            line-height: 1.6;
        }
        .notice-box strong { color: var(--warning); }
        code { background: #07090e; padding: 2px 6px; border-radius: 4px; color: #f87171; font-family: monospace; font-size: 0.85rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="topbar">
            <div class="brand">THE EXCHANGE <span>//</span> CONTRABAND VAULT</div>
            <div>
                <span>Session: <strong class="user-tag">${username}</strong></span>
                <a href="/logout" class="btn-logout" style="margin-left: 14px;">Sign Out</a>
            </div>
        </div>

        <div class="panel">
            <h2>📦 Active Consignment Manifests &amp; Exfiltration Ledger</h2>
            <p class="desc">
                Authenticated clearance verified. This terminal mirrors covert file exchanges and illicit shipments dispatched through <code>uninvited_net</code>.
            </p>

            <table class="ledger-table">
                <thead>
                    <tr>
                        <th>Manifest ID</th>
                        <th>Consignment Description</th>
                        <th>Origin Host</th>
                        <th>Operator Alias</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code>EXFIL-99201</code></td>
                        <td><strong>Classified Consignment Manifest &amp; Contraband Assets</strong></td>
                        <td><code>10.5.5.15 [00:1c:42:8a:b1:15]</code></td>
                        <td><code>DragonFly</code></td>
                        <td><span class="status-badge">DISPATCHED</span></td>
                    </tr>
                    <tr>
                        <td><code>EXFIL-99188</code></td>
                        <td><strong>Encrypted Vault Partition Backup</strong></td>
                        <td><code>10.5.5.80 [52:54:00:12:34:80]</code></td>
                        <td><code>k3ss_void</code></td>
                        <td><span class="status-badge badge-warn">ARCHIVED</span></td>
                    </tr>
                    <tr>
                        <td><code>EXFIL-99042</code></td>
                        <td><strong>Edge Proxy Access Credentials &amp; Keyrings</strong></td>
                        <td><code>10.5.5.34 [00:1c:42:8a:b1:34]</code></td>
                        <td><code>system_relay</code></td>
                        <td><span class="status-badge badge-warn">CLOSED</span></td>
                    </tr>
                </tbody>
            </table>

            <div class="notice-box">
                <strong>⚠️ INVESTIGATIVE ALERT: TRAFFIC INTERCEPTION DETECTED</strong><br>
                Perimeter sensors intercepted the raw network transmission for <code>EXFIL-99201</code>. The raw packet capture file (<code>upload_capture.pcap</code>) has been captured and quarantined on the <strong>CTFd Incident Desk (Stage 6)</strong>.<br>
                <em>Investigators must examine the PCAP in Wireshark to inspect the HTTP POST request originating from host <code>10.5.5.15</code> (MAC <code>00:1c:42:8a:b1:15</code>) and decode the operator token to confirm the culprit's true identity.</em>
            </div>
        </div>
    </div>
</body>
</html>`);
});

// Download alias route (retained for backward compatibility and integration test health check)
app.get('/upload_capture.pcap', (req, res) => {
    const filePath = path.join(publicDir, 'upload_capture.pcap');
    if (fs.existsSync(filePath)) {
        res.download(filePath, 'upload_capture.pcap');
    } else {
        res.status(404).send('File not found');
    }
});

// Logout Handler
app.get('/logout', (req, res) => {
    res.clearCookie('portal_auth');
    res.redirect('/login');
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`[exchange-portal] Running on http://0.0.0.0:${PORT}`);
});
