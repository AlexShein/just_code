from functools import lru_cache


@lru_cache(maxsize=10000)
def fib(n: int) -> int:
    if n > 1:
        return fib(n - 1) + fib(n - 2)
    return n


def perimeter(n: int) -> int:
    return sum([fib(i) * 4 for i in range(n + 2)])  # Using n+2 because element #0 of fib sequence is 0


def assert_equals(x, y):
    try:
        assert x == y
    except AssertionError as exc:
        print(f'# Error\n{x} != {y}')
        raise


if __name__ == '__main__':
    assert_equals(perimeter(5), 80)
    assert_equals(perimeter(7), 216)
    assert_equals(perimeter(20), 114624)
    assert_equals(perimeter(30), 14098308)
    assert_equals(perimeter(100), 6002082144827584333104)
    print('Success')
