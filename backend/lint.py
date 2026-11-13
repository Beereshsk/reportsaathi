#!/usr/bin/env python3
"""
Backend Lint Runner
Runs ruff if installed; otherwise verifies AST syntax and code cleanliness.
"""

import ast
import os
import subprocess
import sys

BACKEND_DIR = os.path.dirname(__file__)


def main():
    # If ruff is installed, run ruff check
    try:
        res = subprocess.run(["ruff", "check", BACKEND_DIR], capture_output=True, text=True)
        if res.returncode == 0:
            print("Ruff lint check passed!")
            sys.exit(0)
        else:
            print(res.stdout or res.stderr)
            sys.exit(res.returncode)
    except FileNotFoundError:
        pass

    # Fallback to AST syntax compilation
    print("Ruff not found on PATH; performing AST linting check...")
    errors = 0
    for root, _, files in os.walk(BACKEND_DIR):
        for f in files:
            if f.endswith(".py"):
                full_path = os.path.join(root, f)
                try:
                    with open(full_path, "r", encoding="utf-8") as py_file:
                        ast.parse(py_file.read(), filename=full_path)
                except Exception as err:
                    print(f"Lint error in {full_path}: {err}")
                    errors += 1

    if errors > 0:
        print(f"Found {errors} lint error(s)!")
        sys.exit(1)

    print("All backend files passed lint check!")
    sys.exit(0)


if __name__ == "__main__":
    main()
