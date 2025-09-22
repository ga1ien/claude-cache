#!/usr/bin/env python3
"""Test the automated execution success detection"""

import sys
sys.path.insert(0, 'src')

from cache_for_claude.execution_monitor import ExecutionMonitor

def test_execution_detection():
    """Test various execution outputs"""
    monitor = ExecutionMonitor()

    test_cases = [
        # Test execution outputs
        {
            'command': 'pytest',
            'output': """
                ============================= test session starts ==============================
                collected 15 items

                tests/test_api.py::test_create_user PASSED                              [ 6%]
                tests/test_api.py::test_update_user PASSED                              [13%]
                tests/test_api.py::test_delete_user PASSED                              [20%]
                tests/test_models.py ...........                                        [93%]
                tests/test_utils.py .                                                   [100%]

                ============================== 15 passed in 3.21s ==============================
            """,
            'expected': 'test_pass'
        },
        {
            'command': 'npm test',
            'output': """
                > my-app@1.0.0 test
                > jest

                 PASS  src/App.test.js
                  ✓ renders without crashing (42ms)
                  ✓ handles user input correctly (15ms)

                Test Suites: 1 passed, 1 total
                Tests:       2 passed, 2 total
                Snapshots:   0 total
                Time:        1.234s
            """,
            'expected': 'test_pass'
        },
        {
            'command': 'npm test',
            'output': """
                 FAIL  src/App.test.js
                  ✕ renders without crashing (125ms)

                  ● renders without crashing

                    expect(received).toBe(expected)

                    Expected: true
                    Received: false

                Tests:       1 failed, 1 total
            """,
            'expected': 'test_fail'
        },
        # Build outputs
        {
            'command': 'npm run build',
            'output': """
                > my-app@1.0.0 build
                > webpack

                webpack 5.74.0 compiled successfully in 4523 ms
                Build complete! Files written to dist/
            """,
            'expected': 'build_success'
        },
        {
            'command': 'npm run build',
            'output': """
                ERROR in ./src/index.js
                Module not found: Error: Can't resolve './App' in '/src'

                webpack 5.74.0 compiled with 1 error
                Build failed!
            """,
            'expected': 'build_fail'
        },
        # Server startup
        {
            'command': 'npm start',
            'output': """
                Starting development server...
                Compiled successfully!

                You can now view my-app in the browser.

                  Local:            http://localhost:3000
                  On Your Network:  http://192.168.1.100:3000

                Note that the development build is not optimized.
                To create a production build, use npm run build.

                webpack compiled successfully
            """,
            'expected': 'server_start'
        },
        # Type checking
        {
            'command': 'npm run typecheck',
            'output': """
                > tsc --noEmit

                Found 0 errors. Watching for file changes.
            """,
            'expected': 'typecheck_pass'
        },
        {
            'command': 'tsc',
            'output': """
                src/components/Button.tsx:15:5 - error TS2322: Type 'string' is not assignable to type 'number'.

                15     count = "hello";
                       ~~~~~

                Found 1 error in src/components/Button.tsx:15
            """,
            'expected': 'typecheck_fail'
        },
        # Linting
        {
            'command': 'npm run lint',
            'output': """
                > eslint src/

                ✔ All files pass linting.
            """,
            'expected': 'lint_pass'
        },
        # Installation
        {
            'command': 'npm install express',
            'output': """

                added 57 packages, and audited 1024 packages in 3s

                123 packages are looking for funding
                  run `npm fund` for details

                found 0 vulnerabilities
            """,
            'expected': 'install_success'
        }
    ]

    print("=" * 60)
    print("AUTOMATED EXECUTION DETECTION TEST")
    print("=" * 60)

    for case in test_cases:
        signals = monitor.analyze_output(case['output'], case['command'])

        print(f"\n📋 Command: {case['command'][:50]}")
        print(f"Expected: {case['expected']}")

        if signals:
            signal = signals[0]  # Get primary signal

            # Color code the output
            if 'pass' in signal.signal_type or 'success' in signal.signal_type or 'start' in signal.signal_type:
                color = '\033[92m'  # Green
                symbol = '✅'
            else:
                color = '\033[91m'  # Red
                symbol = '❌'

            reset = '\033[0m'

            print(f"Detected: {color}{signal.signal_type}{reset} (confidence: {signal.confidence:.2f}) {symbol}")
            print(f"Details: {signal.details}")

            if signal.context:
                print(f"Context: {signal.context}")
        else:
            print("No signals detected ⚠️")

    # Test overall success calculation
    print("\n" + "=" * 60)
    print("OVERALL SUCCESS CALCULATION TEST")
    print("=" * 60)

    # Simulate a successful session
    success_output = """
    Running tests...
    ============================== 10 passed in 2.34s ==============================

    Building project...
    webpack compiled successfully

    Starting server...
    Server running on http://localhost:3000
    """

    signals = monitor.analyze_output(success_output, "npm run dev")
    is_success, confidence = monitor.calculate_overall_success(signals)

    print(f"\n✨ Successful session simulation:")
    print(f"Success: {is_success}")
    print(f"Confidence: {confidence:.2f}")
    print(f"Signals detected: {[s.signal_type for s in signals]}")

    # Simulate a failed session
    failed_output = """
    Running tests...
    FAILED: 3 tests failed

    Building project...
    ERROR: Compilation failed

    Server crashed with error
    """

    signals = monitor.analyze_output(failed_output, "npm run dev")
    is_success, confidence = monitor.calculate_overall_success(signals)

    print(f"\n💥 Failed session simulation:")
    print(f"Success: {is_success}")
    print(f"Confidence: {confidence:.2f}")
    print(f"Signals detected: {[s.signal_type for s in signals]}")

if __name__ == "__main__":
    test_execution_detection()