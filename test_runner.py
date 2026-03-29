#!/usr/bin/env python3
"""test_runner: Minimal test framework with assertions and reporting."""
import sys, time, traceback

class TestResult:
    def __init__(self):
        self.passed = []; self.failed = []; self.errors = []; self.skipped = []

    @property
    def total(self): return len(self.passed)+len(self.failed)+len(self.errors)+len(self.skipped)

    def summary(self):
        return f"{self.total} tests: {len(self.passed)} passed, {len(self.failed)} failed, {len(self.errors)} errors, {len(self.skipped)} skipped"

class TestCase:
    def setup(self): pass
    def teardown(self): pass

def run_tests(test_class, result=None):
    if result is None: result = TestResult()
    obj = test_class()
    methods = [m for m in dir(obj) if m.startswith("test_")]
    for name in sorted(methods):
        method = getattr(obj, name)
        if getattr(method, "_skip", False):
            result.skipped.append(name); continue
        try:
            obj.setup()
            method()
            obj.teardown()
            result.passed.append(name)
        except AssertionError as e:
            result.failed.append((name, str(e)))
        except Exception as e:
            result.errors.append((name, traceback.format_exc()))
    return result

def skip(fn):
    fn._skip = True; return fn

def assert_eq(a, b, msg=""):
    if a != b: raise AssertionError(msg or f"Expected {a!r} == {b!r}")

def assert_near(a, b, tol=1e-6, msg=""):
    if abs(a - b) > tol: raise AssertionError(msg or f"{a} not near {b}")

def assert_raises(exc_type, fn, *args):
    try:
        fn(*args)
        raise AssertionError(f"Expected {exc_type.__name__}")
    except exc_type:
        pass

def test():
    class MyTests(TestCase):
        def setup(self): self.data = [1,2,3]
        def test_sum(self): assert_eq(sum(self.data), 6)
        def test_len(self): assert_eq(len(self.data), 3)
        def test_fail(self): assert_eq(1, 2)
        @skip
        def test_skipped(self): pass

    result = run_tests(MyTests)
    assert len(result.passed) == 2
    assert len(result.failed) == 1
    assert len(result.skipped) == 1
    assert "test_sum" in result.passed
    assert result.failed[0][0] == "test_fail"
    # Helpers
    assert_eq(1, 1)
    assert_near(3.14, 3.14159, tol=0.01)
    assert_raises(ZeroDivisionError, lambda: 1/0)
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: test_runner.py test")
