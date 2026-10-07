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

// Serve static assets from public/ (including /gallery/ and /upload_capture.pcap)
const publicDir = path.join(__dirname, 'public');
app.use(express.static(publicDir));
// Explicit route for gallery if accessed via /gallery
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
    <title>The Exchange Portal :: Restricted Gateway</title>
    <style>
        :root {
            --bg: #0b0f19;
            --card: #151d2f;
            --border: #232f48;
            --accent: #3b82f6;
            --text: #f1f5f9;
            --muted: #94a3b8;
            --danger: #ef4444;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
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
            max-width: 420px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .header { text-align: center; margin-bottom: 28px; }
        .badge {
            display: inline-block;
            background: rgba(59, 130, 246, 0.15);
            border: 1px solid var(--accent);
            color: var(--accent);
            font-family: monospace;
            font-size: 0.8rem;
            padding: 4px 10px;
            border-radius: 20px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        h1 { font-size: 1.4rem; font-weight: 700; color: #fff; margin-bottom: 6px; }
        p.sub { color: var(--muted); font-size: 0.88rem; }
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
        label { display: block; font-size: 0.82rem; font-weight: 600; color: var(--muted); margin-bottom: 6px; text-transform: uppercase; }
        input[type="text"], input[type="password"] {
            width: 100%;
            background: #0b0f19;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 12px 14px;
            color: #fff;
            font-size: 0.95rem;
            outline: none;
        }
        input[type="text"]:focus, input[type="password"]:focus { border-color: var(--accent); }
        button.btn-submit {
            width: 100%;
            background: var(--accent);
            color: #fff;
            border: none;
            padding: 12px;
            border-radius: 6px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            margin-top: 8px;
        }
        button.btn-submit:hover { opacity: 0.9; }
        .footer-note { text-align: center; margin-top: 24px; font-size: 0.75rem; color: #475569; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="header">
            <div class="badge">SECURE GATEWAY</div>
            <h1>The Exchange Portal</h1>
            <p class="sub">Operator Authentication Terminal</p>
        </div>
        ${errorHtml}
        <form action="/login" method="POST">
            <div class="form-group">
                <label for="username">Username or Operator Email</label>
                <input type="text" id="username" name="username" placeholder="adrian.kessler@uninvited.local" required autocomplete="off">
            </div>
            <div class="form-group">
                <label for="password">Security Password</label>
                <input type="password" id="password" name="password" placeholder="••••••••••••" required>
            </div>
            <button type="submit" class="btn-submit">Authenticate</button>
        </form>
        <div class="footer-note">NODE: EXCH-8086 • UNINVITED INTERNAL TRANSIT</div>
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
    <title>The Exchange Portal :: Dashboard</title>
    <style>
        :root {
            --bg: #0b0f19;
            --card: #151d2f;
            --border: #232f48;
            --accent: #3b82f6;
            --success: #10b981;
            --text: #f1f5f9;
            --muted: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 30px 20px;
        }
        .container { max-width: 860px; margin: 0 auto; }
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
        .brand { font-size: 1.1rem; font-weight: 700; color: #fff; }
        .user-tag { color: var(--success); font-weight: 600; }
        .btn-logout {
            background: #1e293b;
            color: #ef4444;
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
        }
        h2 { font-size: 1.3rem; margin-bottom: 12px; color: #fff; }
        p.desc { color: var(--muted); font-size: 0.95rem; line-height: 1.6; margin-bottom: 24px; }
        .files-table { width: 100%; border-collapse: collapse; }
        .files-table th { text-align: left; padding: 12px 16px; border-bottom: 1px solid var(--border); color: var(--muted); font-size: 0.8rem; text-transform: uppercase; }
        .files-table td { padding: 16px; border-bottom: 1px solid #1e293b; font-size: 0.92rem; }
        .btn-download {
            display: inline-block;
            background: var(--accent);
            color: #fff;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.85rem;
        }
        .btn-download:hover { background: #2563eb; }
        .badge { background: #1e293b; color: var(--muted); padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="topbar">
            <div class="brand">THE EXCHANGE PORTAL</div>
            <div>
                <span>Authenticated: <strong class="user-tag">${username}</strong></span>
                <a href="/logout" class="btn-logout" style="margin-left: 14px;">Sign Out</a>
            </div>
        </div>
        <div class="panel">
            <h2>Authorized Transfer Vault</h2>
            <p class="desc">
                Welcome, Operator. All transactions routed across <code>uninvited_net</code> are mirrored here.
            </p>
            <table class="files-table">
                <thead>
                    <tr><th>Filename</th><th>Format</th><th>Classification</th><th>Action</th></tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>📄 upload_capture.pcap</strong></td>
                        <td><span class="badge">Wireshark PCAP</span></td>
                        <td><span class="badge" style="color:#f59e0b; border: 1px solid #78350f;">CONFIDENTIAL</span></td>
                        <td><a href="/upload_capture.pcap" class="btn-download" download>Download Capture</a></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>`);
});

// Download alias routes
app.get('/download/upload_capture.pcap', (req, res) => {
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
