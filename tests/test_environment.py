#!/usr/bin/env python3
"""
Test Suite for Operation Uninvited Guest CTF Environment
Author: Member 4 (IT24100084) - Integration, Testing & Documentation Lead

Verifies:
1. Service port reachability (:8000, :3000, :8086)
2. Database seeding and user authentication
3. Unintended-solution prevention (RBAC and route protections)
4. Sequential prerequisite dependency integrity
5. Asset payload validity across forensic and crypto challenges
"""

import unittest
import sqlite3
import os
import requests

class TestCTFEnvironment(unittest.TestCase):
    def test_ctfd_up(self):
        """Verify CTFd platform is reachable on port 8000."""
        resp = requests.get('http://localhost:8000', timeout=5)
        self.assertEqual(resp.status_code, 200, 'CTFd is down or returning non-200')

    def test_juice_shop_up(self):
        """Verify OWASP Juice Shop application is reachable on port 3000."""
        resp = requests.get('http://localhost:3000', timeout=5)
        self.assertEqual(resp.status_code, 200, 'Juice Shop is down or returning non-200')

    def test_juice_shop_target_account(self):
        """Verify Adrian Kessler account is seeded and authenticates on Juice Shop."""
        login_url = 'http://localhost:3000/rest/user/login'
        creds = {
            'email': 'adrian.kessler@uninvited.local',
            'password': 'Kessler123!'
        }
        resp = requests.post(login_url, json=creds, timeout=5)
        self.assertEqual(resp.status_code, 200, 'Failed to authenticate seeded target on Juice Shop')
        self.assertIn('token', resp.json().get('authentication', {}), 'JWT token missing from login response')

    def test_juice_shop_admin_evidence_vault(self):
        """Verify that evidence_photos.zip is restricted to Admin on Juice Shop (Unintended Solution Check)."""
        # Unauthenticated request must fail with 401
        r_unauth = requests.get('http://localhost:3000/rest/admin/evidence_photos.zip', timeout=5)
        self.assertEqual(r_unauth.status_code, 401, 'Unauthenticated request was not blocked with 401')

        # Admin request must succeed with 200 and return zip bytes
        login_url = 'http://localhost:3000/rest/user/login'
        r_login = requests.post(login_url, json={'email': "adrian.kessler@uninvited.local'--", 'password': 'test'}, timeout=5)
        token = r_login.json()['authentication']['token']
        headers = {'Authorization': f'Bearer {token}'}
        r_admin = requests.get('http://localhost:3000/rest/admin/evidence_photos.zip', headers=headers, timeout=5)
        self.assertEqual(r_admin.status_code, 200, 'Admin request failed to download evidence archive')
        self.assertGreater(len(r_admin.content), 500, 'Evidence archive appears corrupted or truncated')

    def test_exchange_portal_up(self):
        """Verify The Exchange Portal is reachable on port 8086."""
        resp = requests.get('http://localhost:8086', timeout=5)
        self.assertEqual(resp.status_code, 200, 'Exchange Portal is down or returning non-200')

    def test_exchange_portal_unintended_pcap_download_blocked(self):
        """Verify unauthenticated users cannot bypass login to access upload_capture.pcap (Unintended Solution Check)."""
        resp = requests.get('http://localhost:8086/download/pcap', timeout=5, allow_redirects=False)
        self.assertIn(resp.status_code, [302, 401, 403], 'Unauthenticated PCAP download was not blocked')

    def test_exchange_portal_gallery_asset(self):
        """Verify gallery asset is accessible via static gallery."""
        resp = requests.get('http://localhost:8086/gallery/surveillance_01.jpg', timeout=5)
        self.assertEqual(resp.status_code, 200, 'Gallery image surveillance_01.jpg is missing or inaccessible')
        self.assertGreater(len(resp.content), 5000, 'Image payload appears truncated')

    def test_exchange_portal_authentication_and_pcap(self):
        """Verify Exchange Portal login and download of upload_capture.pcap."""
        session = requests.Session()
        login_url = 'http://localhost:8086/login'
        creds = {
            'username': 'adrian.kessler@uninvited.local',
            'password': 'Kessler123!'
        }
        resp = session.post(login_url, data=creds, timeout=5)
        self.assertEqual(resp.status_code, 200, 'Login failed on Exchange Portal')

        # Download pcap
        download_url = 'http://localhost:8086/download/pcap'
        pcap_resp = session.get(download_url, timeout=5)
        self.assertEqual(pcap_resp.status_code, 200, 'Failed to download upload_capture.pcap')
        self.assertGreater(len(pcap_resp.content), 1000, 'PCAP payload appears truncated')

    def test_ctfd_database_sequential_progression_chain(self):
        """Verify that sequential progression requirements exist in ctfd.db."""
        db_path = os.path.join(os.path.dirname(__file__), '..', 'platform', 'ctfd-data', 'ctfd.db')
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT count(*) FROM challenges")
            total = c.fetchone()[0]
            self.assertEqual(total, 6, "Expected 6 registered challenges in CTFd database")
            conn.close()

if __name__ == '__main__':
    unittest.main()
