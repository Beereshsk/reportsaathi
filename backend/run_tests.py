#!/usr/bin/env python3
"""
Backend Test Runner
Executes unit, contract, and smoke test suites.
Works in sandbox environments using Python unittest and supports pytest when installed.
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def main():
    test_dir = os.path.join(os.path.dirname(__file__), "tests")
    print(f"Discovering tests in {test_dir}...")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    total_run = result.testsRun
    failed = len(result.failures)
    errored = len(result.errors)

    print("\n" + "=" * 50)
    print(f"Tests Run: {total_run} | Failures: {failed} | Errors: {errored}")
    print("=" * 50)

    if not result.wasSuccessful():
        sys.exit(1)
    print("All backend tests passed successfully!")
    sys.exit(0)


if __name__ == "__main__":
    main()
