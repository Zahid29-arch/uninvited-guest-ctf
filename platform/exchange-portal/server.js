const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({ secret: 'uninvited-secret', resave: false, saveUninitialized: true }));
app.use(express.static('public'));

app.get('/', (req, res) => {
    res.send('<h2>The Exchange Portal</h2><form action="/login" method="POST">Username: <input type="text" name="user"><br>Password: <input type="password" name="pass"><br><button type="submit">Login</button></form>');
});

app.post('/login', (req, res) => {
    if (req.body.user === 'DragonFly' && req.body.pass === 'Exch@nge2026') {
        req.session.loggedIn = true;
        res.redirect('/portal');
    } else {
        res.send('Invalid credentials. <a href="/">Try again</a>');
    }
});

app.get('/portal', (req, res) => {
    if (!req.session.loggedIn) return res.redirect('/');
    res.send('<h2>Welcome, DragonFly.</h2><p>Secure file exchange portal.</p><p><a href="/upload_capture.pcap">Download Latest Upload Capture (PCAP)</a></p>');
});

app.listen(8086, () => console.log('Exchange Portal running on 8086'));
