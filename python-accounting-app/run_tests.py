#!/usr/bin/env python3
"""
Test runner script for the accounting application.
Provides different test execution options based on TESTPLAN_EN.md
"""

import subprocess
import sys
import argparse


def run_command(cmd):
    """Run a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Run tests for the COBOL-to-Python accounting application")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--parallel", "-n", type=int, help="Run tests in parallel")
    parser.add_argument("--testplan", action="store_true", help="Run tests matching TESTPLAN_EN.md test cases")
    
    args = parser.parse_args()
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add verbosity
    if args.verbose:
        cmd.append("-v")
    
    # Add parallel execution
    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])
    
    # Add coverage
    if args.coverage:
        cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term-missing"])
    
    # Add test selection
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    elif args.testplan:
        # Run specific test cases mentioned in TESTPLAN_EN.md
        cmd.extend(["-k", "tc_main or tc_bal or tc_cre or tc_deb or tc_data or tc_int"])
    
    # Run the tests
    success = run_command(cmd)
    
    if success:
        print("\n✅ All tests passed!")
        if args.coverage:
            print("📊 Coverage report generated in htmlcov/index.html")
        print("\n🎯 Test Plan Coverage:")
        print("   - TC_MAIN_* : Main program navigation tests")
        print("   - TC_BAL_*  : Balance inquiry tests")
        print("   - TC_CRE_*  : Credit operation tests")
        print("   - TC_DEB_*  : Debit operation tests")
        print("   - TC_DATA_* : Data persistence tests")
        print("   - TC_INT_*  : Integration tests")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
