#!/usr/bin/env python
"""
Test runner script for Python Notes Website.
Run this file directly to execute the test suite:
    python run_tests.py
"""

import sys
import pytest

if __name__ == '__main__':
    # Get command line arguments
    args = sys.argv[1:]
    
    # Default arguments if none provided
    if not args:
        args = ['-v', 'tests']
    
    print("Running Python Notes Website tests...")
    result = pytest.main(args)
    
    sys.exit(result)