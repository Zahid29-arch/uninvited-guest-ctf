import unittest
import requests

class TestCTFEnvironment(unittest.TestCase):
    def test_ctfd_up(self):
        resp = requests.get('http://localhost:8000')
        self.assertEqual(resp.status_code, 200, 'CTFd is down')

    def test_juice_shop_up(self):
        resp = requests.get('http://localhost:3000')
        self.assertEqual(resp.status_code, 200, 'Juice Shop is down')

    def test_exchange_portal_up(self):
        resp = requests.get('http://localhost:8086')
        self.assertEqual(resp.status_code, 200, 'Exchange Portal is down')

if __name__ == '__main__':
    unittest.main()
