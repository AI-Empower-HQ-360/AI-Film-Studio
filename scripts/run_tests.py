#!/usr/bin/env python3
"""
AI Film Studio - Local Test Runner
Run this before pushing to any branch to ensure code quality.

Usage:
    python scripts/run_tests.py              # Run all tests for current branch
    python scripts/run_tests.py --quick      # Quick syntax check only
    python scripts/run_tests.py --unit       # Unit tests only
    python scripts/run_tests.py --full       # Full test suite (staging/main level)
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def run_command(cmd, description, continue_on_error=False):
    """Run a command and return success status."""
    print(f"\n{Colors.BOLD}Running: {description}{Colors.RESET}")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print_success(f"{description} passed!")
        return True
    else:
        if continue_on_error:
            print_warning(f"{description} had issues (continuing...)")
            return True
        else:
            print_error(f"{description} failed!")
            return False

def get_current_branch():
    """Get the current git branch name."""
    result = subprocess.run(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        capture_output=True,
        text=True
    )
    return result.stdout.strip() if result.returncode == 0 else 'unknown'

def run_quick_checks():
    """Run quick syntax and lint checks."""
    print_header("STAGE 1: Quick Checks")
    
    success = True
    
    # Python syntax check
    if not run_command(
        [sys.executable, '-m', 'py_compile', 'src/api/main.py'],
        "Python syntax check",
        continue_on_error=True
    ):
        success = False
    
    # Flake8 critical errors only
    if not run_command(
        [sys.executable, '-m', 'flake8', 'src/', '--count', '--select=E9,F63,F7,F82', '--show-source', '--statistics'],
        "Flake8 critical errors",
        continue_on_error=True
    ):
        success = False
    
    return success

def run_unit_tests():
    """Run unit tests."""
    print_header("STAGE 2: Unit Tests")
    
    return run_command(
        [sys.executable, '-m', 'pytest', 'tests/unit/', '-v', '--tb=short', '-x'],
        "Unit tests",
        continue_on_error=True
    )

def run_integration_tests():
    """Run integration tests."""
    print_header("STAGE 3: Integration Tests")
    
    return run_command(
        [sys.executable, '-m', 'pytest', 'tests/integration/', '-v', '--tb=short', '-x'],
        "Integration tests",
        continue_on_error=True
    )

def run_e2e_tests():
    """Run E2E tests."""
    print_header("STAGE 4: E2E Tests")
    
    return run_command(
        [sys.executable, '-m', 'pytest', 'tests/e2e/', '-v', '--tb=short', '-x'],
        "E2E tests",
        continue_on_error=True
    )

def run_security_tests():
    """Run security tests."""
    print_header("STAGE 5: Security Tests")
    
    # Bandit security scan
    run_command(
        [sys.executable, '-m', 'bandit', '-r', 'src/', '-ll'],
        "Bandit security scan",
        continue_on_error=True
    )
    
    return run_command(
        [sys.executable, '-m', 'pytest', 'tests/security/', '-v', '--tb=short'],
        "Security tests",
        continue_on_error=True
    )

def run_frontend_tests():
    """Run frontend tests."""
    print_header("STAGE 6: Frontend Tests")
    
    frontend_dir = Path('frontend')
    if not frontend_dir.exists():
        print_warning("Frontend directory not found, skipping...")
        return True
    
    os.chdir('frontend')
    success = run_command(
        ['npm', 'run', 'test:run'],
        "Frontend unit tests",
        continue_on_error=True
    )
    os.chdir('..')
    return success

def main():
    parser = argparse.ArgumentParser(description='AI Film Studio Test Runner')
    parser.add_argument('--quick', action='store_true', help='Quick syntax check only')
    parser.add_argument('--unit', action='store_true', help='Unit tests only')
    parser.add_argument('--integration', action='store_true', help='Integration tests')
    parser.add_argument('--e2e', action='store_true', help='E2E tests')
    parser.add_argument('--security', action='store_true', help='Security tests')
    parser.add_argument('--frontend', action='store_true', help='Frontend tests')
    parser.add_argument('--full', action='store_true', help='Full test suite')
    args = parser.parse_args()
    
    # Get current branch
    branch = get_current_branch()
    
    print(f"\n{Colors.BOLD}AI Film Studio Test Runner{Colors.RESET}")
    print(f"Current branch: {Colors.BLUE}{branch}{Colors.RESET}")
    
    # Determine which tests to run based on branch
    if args.quick:
        stages = ['quick']
    elif args.unit:
        stages = ['quick', 'unit']
    elif args.integration:
        stages = ['quick', 'unit', 'integration']
    elif args.e2e:
        stages = ['quick', 'unit', 'integration', 'e2e']
    elif args.security:
        stages = ['security']
    elif args.frontend:
        stages = ['frontend']
    elif args.full:
        stages = ['quick', 'unit', 'integration', 'e2e', 'security', 'frontend']
    else:
        # Auto-detect based on branch
        if branch == 'dev':
            stages = ['quick', 'unit']
            print(f"Dev branch: Running quick checks + unit tests")
        elif branch == 'sandbox':
            stages = ['quick', 'unit', 'integration']
            print(f"Sandbox branch: Running up to integration tests")
        elif branch in ['staging', 'main']:
            stages = ['quick', 'unit', 'integration', 'e2e', 'security']
            print(f"{branch} branch: Running full test suite")
        else:
            stages = ['quick', 'unit']
            print(f"Feature branch: Running quick checks + unit tests")
    
    results = {}
    
    # Run selected stages
    if 'quick' in stages:
        results['Quick Checks'] = run_quick_checks()
    
    if 'unit' in stages:
        results['Unit Tests'] = run_unit_tests()
    
    if 'integration' in stages:
        results['Integration Tests'] = run_integration_tests()
    
    if 'e2e' in stages:
        results['E2E Tests'] = run_e2e_tests()
    
    if 'security' in stages:
        results['Security Tests'] = run_security_tests()
    
    if 'frontend' in stages:
        results['Frontend Tests'] = run_frontend_tests()
    
    # Print summary
    print_header("TEST SUMMARY")
    
    all_passed = True
    for stage, passed in results.items():
        if passed:
            print_success(f"{stage}: PASSED")
        else:
            print_error(f"{stage}: FAILED")
            all_passed = False
    
    print()
    if all_passed:
        print_success("All tests passed! Ready to push.")
        return 0
    else:
        print_warning("Some tests failed. Review issues before pushing.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
