#!/usr/bin/env python3
"""Minimal test runner. Zero dependencies."""
import sys, time, traceback, re

class TestResult:
    def __init__(self):
        self.passed = []; self.failed = []; self.skipped = []; self.errors = []
    @property
    def total(self): return len(self.passed)+len(self.failed)+len(self.skipped)+len(self.errors)

def discover(module):
    tests = []
    for name in dir(module):
        if name.startswith("test_"):
            fn = getattr(module, name)
            if callable(fn): tests.append((name, fn))
    return sorted(tests)

def run(tests, verbose=False):
    result = TestResult()
    for name, fn in tests:
        try:
            start = time.time()
            fn()
            elapsed = time.time() - start
            result.passed.append((name, elapsed))
            if verbose: print(f"  ✅ {name} ({elapsed:.3f}s)")
        except AssertionError as e:
            result.failed.append((name, str(e)))
            if verbose: print(f"  ❌ {name}: {e}")
        except Exception as e:
            result.errors.append((name, traceback.format_exc()))
            if verbose: print(f"  💥 {name}: {e}")
    return result

def summary(result):
    total = result.total
    lines = [f"\nResults: {len(result.passed)}/{total} passed"]
    if result.failed:
        lines.append(f"  Failed ({len(result.failed)}):")
        for name, msg in result.failed:
            lines.append(f"    - {name}: {msg}")
    if result.errors:
        lines.append(f"  Errors ({len(result.errors)}):")
        for name, tb in result.errors:
            lines.append(f"    - {name}")
    return "\n".join(lines)

def assert_eq(a, b, msg=""): assert a == b, msg or f"Expected {b}, got {a}"
def assert_ne(a, b, msg=""): assert a != b, msg or f"Expected != {b}"
def assert_true(v, msg=""): assert v, msg or "Expected truthy"
def assert_false(v, msg=""): assert not v, msg or "Expected falsy"
def assert_raises(exc, fn, *args):
    try: fn(*args); assert False, f"Expected {exc.__name__}"
    except exc: pass
def assert_approx(a, b, tol=1e-6): assert abs(a-b) < tol, f"{a} != {b} (tol={tol})"

if __name__ == "__main__":
    def test_pass(): assert 1 + 1 == 2
    def test_fail(): assert 1 == 2
    tests = [("test_pass", test_pass), ("test_fail", test_fail)]
    result = run(tests, verbose=True)
    print(summary(result))
