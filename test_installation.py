#!/usr/bin/env python3
"""Test script to verify installation"""

import sys
from pathlib import Path


def test_imports():
    """Test that all modules can be imported"""
    try:
        from cache_for_claude import (
            CacheAgent,
            LogWatcher,
            LogProcessor,
            SuccessDetector,
            KnowledgeBase,
            ContextInjector
        )
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_cli():
    """Test that CLI is accessible"""
    try:
        from cache_for_claude.cli import cli
        print("✓ CLI interface available")
        return True
    except ImportError as e:
        print(f"✗ CLI import error: {e}")
        return False


def test_database_creation():
    """Test that database can be created"""
    try:
        from cache_for_claude import KnowledgeBase
        import tempfile

        with tempfile.NamedTemporaryFile(suffix='.db', delete=True) as tf:
            kb = KnowledgeBase(tf.name)
            print("✓ Database creation successful")
            return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False


def test_log_directory():
    """Check if Claude log directory exists"""
    claude_dir = Path.home() / '.claude' / 'projects'
    if claude_dir.exists():
        print(f"✓ Claude log directory found: {claude_dir}")
    else:
        print(f"✗ Claude log directory not found: {claude_dir}")
        print("  This is normal if you haven't used Claude Code yet")
    return True


def main():
    """Run all tests"""
    print("Claude Cache - Installation Test\n")
    print("=" * 50)

    tests = [
        ("Module imports", test_imports),
        ("CLI interface", test_cli),
        ("Database creation", test_database_creation),
        ("Log directory", test_log_directory),
    ]

    results = []
    for name, test_func in tests:
        print(f"\nTesting {name}...")
        results.append(test_func())

    print("\n" + "=" * 50)
    if all(results):
        print("\n✅ All tests passed! Installation successful.")
        print("\nYou can now run: cache --help")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())