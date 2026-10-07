#!/usr/bin/env python3
"""
Test Suite for Uninvited Guest CTF Environment
Verifies all platform services, network ports, authentication endpoints, and challenge assets.
"""

import unittest
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

    def test_exchange_portal_up(self):
        """Verify The Exchange Portal is reachable on port 8086."""
        resp = requests.get('http://localhost:8086', timeout=5)
        self.assertEqual(resp.status_code, 200, 'Exchange Portal is down or returning non-200')

    def test_exchange_portal_gallery_asset(self):
        """Verify Stage 4 / 5 stego image is accessible via static gallery."""
        resp = requests.get('http://localhost:8086/gallery/consignment_07.jpg', timeout=5)
        self.assertEqual(resp.status_code, 200, 'Gallery image consignment_07.jpg is missing or inaccessible')
        self.assertGreater(len(resp.content), 5000, 'Image payload appears truncated')

    def test_exchange_portal_authentication_and_pcap(self):
        """Verify Exchange Portal login and download of upload_capture.pcap."""
        session = requests.Session()
        login_resp = session.post(
            'http://localhost:8086/login',
            data={'username': 'adrian.kessler@uninvited.local', 'password': 'Kessler123!'},
            allow_redirects=True,
            timeout=5
        )
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn('Authorized Transfer Vault', login_resp.text, 'Portal dashboard failed to render after login')

        pcap_resp = session.get('http://localhost:8086/upload_capture.pcap', timeout=5)
        self.assertEqual(pcap_resp.status_code, 200, 'Failed to download upload_capture.pcap')
        self.assertGreater(len(pcap_resp.content), 20000, 'PCAP capture payload appears incomplete')

if __name__ == '__main__':
    unittest.main()
