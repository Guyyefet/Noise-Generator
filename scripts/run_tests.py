#!/usr/bin/env python3
from typing import Dict, Any
from pathlib import Path
import subprocess
import json
import sys

def run_tests(test_path: str = None, full_output: bool = False, coverage: bool = False) -> None:
    """
    Run pytest with specified test path or all tests.
    
    Args:
        test_path: Optional path to specific test file or directory
        full_output: If True, show full pytest output
        coverage: If True, show detailed coverage report
    """
    cmd = ["pytest", "-v"]
    if test_path and test_path not in ["--full", "--coverage"]:
        cmd.append(test_path)
    
    if coverage:
        cmd.extend(["--cov=App", "--cov-report", "term-missing"])
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    elif full_output:
        # Show complete pytest output
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    else:
        # Run tests with filtered output
        with open('/dev/null', 'w') as devnull:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=devnull, text=True)
        
        try:
            with open('.test_output.json', 'r') as f:
                output = json.load(f)
            display_clean_output(output)
        except FileNotFoundError:
            # If clean output not available, filter and show pytest output
            filtered_output = '\n'.join(
                line for line in result.stdout.split('\n')
                if not any(x in line.lower() for x in 
                    ['===', 'platform', 'pytest', 'rootdir', 'plugins', 'collected', 'pyqt', 'qt runtime', 'asyncio']) and
                not any(x in line for x in ['object at 0x', 'self =', 'noise_parameters ='])
            ).strip()
            if filtered_output:
                print(filtered_output)
            sys.exit(result.returncode)

def display_clean_output(output: Dict[str, Any]) -> None:
    """Display test results in a clean format."""
    has_issues = False
    
    # Print failures if any
    if output["failures"]:
        has_issues = True
        for failure in output["failures"]:
            print(f"FAIL: {failure['test']}")
            print(f"Error: {failure['error']}\n")
    
    # Print files with no tests
    if output["no_coverage"]:
        has_issues = True
        print("No Tests:")
        for file in output["no_coverage"]:
            print(f"- {file}")
    
    if not has_issues:
        print("All tests passed!")
    
    # Exit with appropriate status code
    sys.exit(1 if output["failures"] else 0)

def print_usage():
    """Print script usage information."""
    print("Usage: python run_tests.py [test_path] [--full] [--coverage]")
    print("  test_path: Optional path to test file or directory")
    print("  --full: Show complete pytest output")
    print("  --coverage: Show detailed coverage report")
    sys.exit(1)

if __name__ == "__main__":
    args = sys.argv[1:]
    test_path = None
    full_output = False
    coverage = False
    
    # Parse command line arguments
    for arg in args:
        if arg == "--full":
            full_output = True
        elif arg == "--coverage":
            coverage = True
        elif arg.startswith("-"):
            print_usage()
        else:
            test_path = arg
    
    run_tests(test_path, full_output, coverage)
