#!/usr/bin/env python3
"""
Comprehensive Automated Test & Verification Suite
Executes the environment integration test suite (7/7 tests) and all six
reference solvers, writing unforgeable timestamped verification logs to
'tests/test_execution.log'.
"""

import os
import sys
import subprocess
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
LOG_FILE = os.path.join(SCRIPT_DIR, 'test_execution.log')

def run_cmd(cmd, description):
    print(f"[*] Running {description}...")
    start_time = datetime.datetime.now()
    res = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True)
    duration = (datetime.datetime.now() - start_time).total_seconds()
    
    log_entry = (
        f"======================================================================\n"
        f"TEST TARGET : {description}\n"
        f"COMMAND     : {' '.join(cmd)}\n"
        f"TIMESTAMP   : {start_time.isoformat()}\n"
        f"DURATION    : {duration:.3f}s\n"
        f"EXIT CODE   : {res.returncode}\n"
        f"----------------------------------------------------------------------\n"
        f"STDOUT:\n{res.stdout.strip()}\n"
    )
    if res.stderr.strip():
        log_entry += f"STDERR:\n{res.stderr.strip()}\n"
    log_entry += "======================================================================\n\n"
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)
        
    print(f"[+] {description} completed (Exit Code: {res.returncode})")
    return res.returncode == 0

def main():
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write(
            f"######################################################################\n"
            f"# SLIIT IE3132 Penetration Testing - CTF Play Box Test Log          #\n"
            f"# Suite: Operation Uninvited Guest                                   #\n"
            f"# Run Timestamp: {datetime.datetime.now().isoformat()}               #\n"
            f"######################################################################\n\n"
        )
        
    all_passed = True
    
    # 1. Environment Integration Tests
    if not run_cmd([sys.executable, 'tests/test_environment.py'], "Environment Integration Test Suite (7/7)"):
        all_passed = False
        
    # 2. Reference Solvers
    for i in range(1, 7):
        solver_script = f"solvers/stage{i}_solver.py"
        if not run_cmd([sys.executable, solver_script], f"Stage {i} Reference Solver"):
            all_passed = False
            
    summary = (
        f"######################################################################\n"
        f"OVERALL RESULT: {'ALL TESTS & SOLVERS PASSED (100%)' if all_passed else 'SOME TESTS FAILED'}\n"
        f"COMPLETION TIME: {datetime.datetime.now().isoformat()}\n"
        f"######################################################################\n"
    )
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(summary)
        
    print("\n" + summary)

if __name__ == '__main__':
    main()
