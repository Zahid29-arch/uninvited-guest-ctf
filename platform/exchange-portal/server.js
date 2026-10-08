const express = require('express');
const cookieParser = require('cookie-parser');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 8086;

// =========================================================================
// ⚙️ [ADMIN CONFIGURATION] - MANUALLY CHANGE THE PORTAL NAME HERE
// You can change any of the text values below to customize the portal!
// =========================================================================
const PORTAL_NAME        = process.env.PORTAL_NAME        || "THE DARK EXCHANGE";
const PORTAL_TAGLINE     = process.env.PORTAL_TAGLINE     || "THE DARK EXCHANGE";
const PORTAL_BADGE       = process.env.PORTAL_BADGE       || "Treasured Collections";
const PORTAL_DESCRIPTION = process.env.PORTAL_DESCRIPTION || "Encrypted repository for visual assets, consignment previews, and covert transmissions.";
// =========================================================================

// Middleware - increase payload limit for base64 image uploads
app.use(express.urlencoded({ extended: true, limit: '25mb' }));
app.use(express.json({ limit: '25mb' }));
app.use(cookieParser());

// Serve static assets from public/ (including /gallery/)
const publicDir = path.join(__dirname, 'public');
const galleryDir = path.join(publicDir, 'gallery');

if (!fs.existsSync(galleryDir)) {
    fs.mkdirSync(galleryDir, { recursive: true });
}

app.use(express.static(publicDir));
app.use('/gallery', express.static(galleryDir));

// Helper: check authentication
function isAuthenticated(req) {
    return req.cookies && req.cookies.portal_auth;
}

// Helper: list images in gallery directory
function getGalleryImages() {
    if (!fs.existsSync(galleryDir)) return [];
    const validExts = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'];
    return fs.readdirSync(galleryDir)
        .filter(f => validExts.includes(path.extname(f).toLowerCase()))
        .map(f => {
            const stat = fs.statSync(path.join(galleryDir, f));
            return {
                name: f,
                url: `/gallery/${encodeURIComponent(f)}`,
                size: (stat.size / 1024).toFixed(1) + ' KB',
                modified: stat.mtime.toLocaleDateString()
            };
        });
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
    <title>${PORTAL_NAME} :: Secure Gateway</title>
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
        h1 { font-size: 1.35rem; font-weight: 700; color: #fff; margin-bottom: 6px; }
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
        label { display: block; font-size: 0.8rem; font-weight: 600; color: var(--muted); margin-bottom: 6px; text-transform: uppercase; }
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
            <div class="badge">${PORTAL_BADGE}</div>
            <h1>${PORTAL_NAME} // ${PORTAL_TAGLINE}</h1>
            <p class="sub">${PORTAL_DESCRIPTION}</p>
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
            <button type="submit" class="btn-submit">Access ${PORTAL_NAME}</button>
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

// API endpoint to upload images manually
app.post('/api/upload', (req, res) => {
    if (!isAuthenticated(req)) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    const { filename, data } = req.body;
    if (!filename || !data) {
        return res.status(400).json({ error: 'Missing filename or image data' });
    }

    try {
        const baseName = path.basename(filename).replace(/[^a-zA-Z0-9._-]/g, '_');
        const targetPath = path.join(galleryDir, baseName);
        const base64Data = data.replace(/^data:image\/\w+;base64,/, '');
        const buffer = Buffer.from(base64Data, 'base64');

        fs.writeFileSync(targetPath, buffer);
        console.log(`[+] Uploaded image: ${baseName} (${buffer.length} bytes)`);

        return res.json({ success: true, filename: baseName, url: `/gallery/${encodeURIComponent(baseName)}` });
    } catch (err) {
        console.error('[-] Upload error:', err);
        return res.status(500).json({ error: 'Failed to write file' });
    }
});

// API endpoint to delete an image
app.post('/api/delete', (req, res) => {
    if (!isAuthenticated(req)) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    const { filename } = req.body;
    if (!filename) return res.status(400).json({ error: 'Missing filename' });

    const safeName = path.basename(filename);
    const targetPath = path.join(galleryDir, safeName);

    if (fs.existsSync(targetPath)) {
        fs.unlinkSync(targetPath);
        return res.json({ success: true });
    }
    return res.status(404).json({ error: 'File not found' });
});

// Authenticated Dashboard & Gallery (GET /portal)
app.get('/portal', (req, res) => {
    if (!isAuthenticated(req)) {
        return res.redirect('/login');
    }

    const username = req.cookies.portal_auth || 'adrian.kessler';
    const images = getGalleryImages();

    res.send(`<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${PORTAL_NAME} :: ${PORTAL_TAGLINE}</title>
    <style>
        :root {
            --bg: #07090e;
            --card: #0f141f;
            --card-hover: #151c2c;
            --border: #1e2638;
            --accent: #ef4444;
            --accent-hover: #dc2626;
            --success: #10b981;
            --text: #f1f5f9;
            --muted: #8b9bb4;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace, sans-serif;
            padding: 30px 24px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
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
        .brand { font-size: 1.2rem; font-weight: 800; color: #fff; letter-spacing: 0.5px; }
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
        .header-section {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 24px;
            margin-bottom: 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        .header-text h2 { font-size: 1.35rem; color: #fff; margin-bottom: 6px; }
        .header-text p { color: var(--muted); font-size: 0.9rem; }
        .upload-box {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .upload-btn {
            background: #b91c1c;
            color: #fff;
            padding: 10px 18px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.88rem;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 1px solid #dc2626;
            transition: all 0.2s;
        }
        .upload-btn:hover { background: var(--accent-hover); }
        input[type="file"] { display: none; }
        .status-msg { font-size: 0.82rem; color: var(--success); display: none; font-family: monospace; }

        /* Gallery Grid */
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 22px;
        }
        .image-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
        }
        .image-card:hover {
            transform: translateY(-4px);
            border-color: var(--accent);
            box-shadow: 0 10px 24px rgba(239, 68, 68, 0.15);
        }
        .image-wrapper {
            width: 100%;
            height: 220px;
            background: #05070a;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            cursor: pointer;
            position: relative;
        }
        .image-wrapper img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s;
        }
        .image-card:hover .image-wrapper img {
            transform: scale(1.05);
        }
        .card-body {
            padding: 14px 16px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .image-name {
            font-family: monospace;
            font-size: 0.92rem;
            color: #fff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-weight: 600;
        }
        .card-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.78rem;
            color: var(--muted);
        }
        .badge-size {
            background: #141a29;
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid #1e2638;
        }
        .card-actions {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 4px;
            padding-top: 10px;
            border-top: 1px solid #141a29;
        }
        .btn-view {
            color: var(--accent);
            text-decoration: none;
            font-size: 0.82rem;
            font-weight: 600;
        }
        .btn-delete {
            background: none;
            border: none;
            color: #64748b;
            cursor: pointer;
            font-size: 0.82rem;
        }
        .btn-delete:hover { color: #ef4444; }

        /* Modal Lightbox */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.88);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .modal img {
            max-width: 90%;
            max-height: 85vh;
            border-radius: 8px;
            border: 2px solid var(--accent);
            box-shadow: 0 0 30px rgba(0,0,0,0.9);
        }
        .modal-close {
            position: absolute;
            top: 25px;
            right: 35px;
            font-size: 2.2rem;
            color: #fff;
            cursor: pointer;
            font-weight: bold;
        }
        .empty-state {
            grid-column: 1 / -1;
            text-align: center;
            padding: 60px 20px;
            color: var(--muted);
            background: var(--card);
            border: 1px dashed var(--border);
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="topbar">
            <div class="brand">${PORTAL_NAME} <span>//</span> ${PORTAL_TAGLINE}</div>
            <div>
                <span>Session: <strong class="user-tag">${username}</strong></span>
                <a href="/logout" class="btn-logout" style="margin-left: 14px;">Sign Out</a>
            </div>
        </div>

        <div class="header-section">
            <div class="header-text">
                <h2>🖼️ ${PORTAL_NAME} Gallery &amp; Asset Vault</h2>
                <p>Browse active consignment images or upload new assets directly into the vault.</p>
            </div>
            <div class="upload-box">
                <label for="image-upload" class="upload-btn">
                    <span>➕ Add Image to Vault</span>
                </label>
                <input type="file" id="image-upload" accept="image/*" onchange="handleImageUpload(event)">
                <span id="upload-status" class="status-msg">Uploading...</span>
            </div>
        </div>

        <div class="gallery-grid" id="gallery-container">
            ${images.length === 0 ? `
                <div class="empty-state">
                    <h3>No images found in vault</h3>
                    <p style="margin-top: 8px;">Upload images using the button above or place them in <code>public/gallery/</code>.</p>
                </div>
            ` : images.map(img => `
                <div class="image-card" id="card-${encodeURIComponent(img.name)}">
                    <div class="image-wrapper" onclick="openModal('${img.url}')">
                        <img src="${img.url}" alt="${img.name}" loading="lazy">
                    </div>
                    <div class="card-body">
                        <div class="image-name" title="${img.name}">${img.name}</div>
                        <div class="card-meta">
                            <span class="badge-size">${img.size}</span>
                            <span>${img.modified}</span>
                        </div>
                        <div class="card-actions">
                            <a href="${img.url}" target="_blank" class="btn-view">Open Full Size ↗</a>
                            <button class="btn-delete" onclick="deleteImage('${img.name}')" title="Delete">🗑️ Remove</button>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    </div>

    <!-- Lightbox Modal -->
    <div class="modal" id="image-modal" onclick="closeModal()">
        <span class="modal-close">&times;</span>
        <img id="modal-img" src="" alt="Enlarged Preview" onclick="event.stopPropagation()">
    </div>

    <script>
        function openModal(src) {
            document.getElementById('modal-img').src = src;
            document.getElementById('image-modal').style.display = 'flex';
        }
        function closeModal() {
            document.getElementById('image-modal').style.display = 'none';
        }
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeModal();
        });

        async function handleImageUpload(e) {
            const file = e.target.files[0];
            if (!file) return;

            const status = document.getElementById('upload-status');
            status.innerText = 'Uploading ' + file.name + '...';
            status.style.display = 'inline';

            const reader = new FileReader();
            reader.onload = async function() {
                try {
                    const res = await fetch('/api/upload', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            filename: file.name,
                            data: reader.result
                        })
                    });
                    const data = await res.json();
                    if (data.success) {
                        status.innerText = 'Upload complete! Refreshing...';
                        setTimeout(() => window.location.reload(), 600);
                    } else {
                        status.innerText = 'Error: ' + (data.error || 'Upload failed');
                        status.style.color = '#ef4444';
                    }
                } catch (err) {
                    status.innerText = 'Network upload error';
                    status.style.color = '#ef4444';
                }
            };
            reader.readAsDataURL(file);
        }

        async function deleteImage(filename) {
            if (!confirm('Remove ' + filename + ' from the gallery?')) return;
            try {
                const res = await fetch('/api/delete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ filename })
                });
                const data = await res.json();
                if (data.success) {
                    window.location.reload();
                }
            } catch (err) {
                alert('Failed to remove image');
            }
        }
    </script>
</body>
</html>`);
});

// Download alias route (retained for backward compatibility and test suite)
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
