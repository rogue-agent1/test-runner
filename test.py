from test_runner import run, assert_eq, assert_raises, assert_approx
def test_ok(): assert_eq(1+1, 2)
def test_fail(): assert_eq(1, 2, "bad")
r = run([("ok", test_ok), ("fail", test_fail)])
assert len(r.passed) == 1
assert len(r.failed) == 1
assert_raises(AssertionError, lambda: assert_eq(1, 2))
assert_approx(3.14159, 3.14159, 1e-4)
print("Test runner tests passed")