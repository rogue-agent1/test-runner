#!/usr/bin/env python3
"""test_runner - Minimal test framework with assertions, fixtures, and reporting."""
import sys, time, traceback

class TestResult:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.errors = []
        self.skipped = []
    @property
    def total(self): return len(self.passed)+len(self.failed)+len(self.errors)+len(self.skipped)
    def summary(self):
        return f"{len(self.passed)} passed, {len(self.failed)} failed, {len(self.errors)} errors, {len(self.skipped)} skipped / {self.total} total"

class TestCase:
    def setup(self): pass
    def teardown(self): pass

def run_tests(test_class):
    result = TestResult()
    methods = [m for m in dir(test_class) if m.startswith("test_")]
    instance = test_class()
    for method in sorted(methods):
        fn = getattr(instance, method)
        if getattr(fn, "_skip", False):
            result.skipped.append(method); continue
        try:
            instance.setup()
            fn()
            instance.teardown()
            result.passed.append(method)
        except AssertionError as e:
            result.failed.append((method, str(e)))
        except Exception as e:
            result.errors.append((method, traceback.format_exc()))
    return result

def skip(fn):
    fn._skip = True
    return fn

def test():
    class MyTests(TestCase):
        def setup(self):
            self.data = [1, 2, 3]
        def test_sum(self):
            assert sum(self.data) == 6
        def test_len(self):
            assert len(self.data) == 3
        def test_fail(self):
            assert 1 == 2, "intentional"
        @skip
        def test_skipped(self):
            pass
    r = run_tests(MyTests)
    assert len(r.passed) == 2
    assert len(r.failed) == 1
    assert r.failed[0][0] == "test_fail"
    assert len(r.skipped) == 1
    print("test_runner: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: test_runner.py --test")
