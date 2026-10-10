#!/usr/bin/env python3
"""
Test Harness for Challenge Design A (Stages 1 to 3)
Author: Member 2 (IT24100066)

Validates:
1. Stage 1 OSINT identity correlation logic
2. Stage 2 Web SQL injection solver execution
3. Stage 3 Cryptographic archive dictionary crack
"""

import sys
import unittest
import stage1_solver
import stage3_solver

class TestChallengeDesignA(unittest.TestCase):
    def test_stage1_osint_solve(self):
        """Verify Stage 1 extracts Adrian Kessler correctly."""
        result = stage1_solver.solve(verbose=False)
        self.assertIsNotNone(result, "Stage 1 solver failed to extract identity")
        self.assertEqual(result["flag"], "Adrian Kessler")
        self.assertEqual(result["email"], "adrian.kessler@uninvited.local")

    def test_stage3_crypto_solve(self):
        """Verify Stage 3 cracks evidence_photos.zip with target password."""
        result = stage3_solver.solve(verbose=False)
        self.assertIsNotNone(result, "Stage 3 solver failed to crack archive")
        self.assertEqual(result["flag"], "Kessler123!")

if __name__ == '__main__':
    unittest.main()
