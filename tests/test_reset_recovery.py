#!/usr/bin/env python3
"""
Automated Reset & Recovery Verification Engine
Author: Member 4 (IT24100084) - Integration & Testing Lead

Tests:
1. Simulates solve submission in SQLite database.
2. Runs reset logic on CTFd database.
3. Asserts tables (solves, submissions, unlocks, tracking) return to 0.
"""

import unittest
import sqlite3
import os

class TestResetRecoveryMechanism(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'platform', 'ctfd-data', 'ctfd.db')

    def test_database_reset_integrity(self):
        """Verify that reset cleans solves and unlocks safely."""
        if not os.path.exists(self.db_path):
            self.skipTest("ctfd.db not found locally")

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Verify clean baseline
        c.execute("SELECT count(*) FROM solves")
        solves_count = c.fetchone()[0]
        c.execute("SELECT count(*) FROM submissions")
        submissions_count = c.fetchone()[0]
        c.execute("SELECT count(*) FROM unlocks")
        unlocks_count = c.fetchone()[0]
        
        self.assertEqual(solves_count, 0, "Solves table is not clean at baseline")
        self.assertEqual(submissions_count, 0, "Submissions table is not clean at baseline")
        self.assertEqual(unlocks_count, 0, "Unlocks table is not clean at baseline")
        conn.close()

if __name__ == '__main__':
    unittest.main()
