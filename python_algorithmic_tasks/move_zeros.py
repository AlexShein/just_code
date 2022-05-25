def move_zeros(arr: list) -> list:
    return [el for el in arr if not el == 0] + [0] * arr.count(0)


def assert_equals(x, y):
    assert x == y


if __name__ == '__main__':

    assert_equals(move_zeros([1, 2, 0, 1, 0, 1, 0, 3, 0, 1]), [1, 2, 1, 1, 3, 1, 0, 0, 0, 0])
    assert_equals(
        move_zeros([9, 0, 0, 9, 1, 2, 0, 1, 0, 1, 0, 3, 0, 1, 9, 0, 0, 0, 0, 9]),
        [9, 9, 1, 2, 1, 1, 3, 1, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )
    assert_equals(move_zeros([0, 0]), [0, 0])
    assert_equals(move_zeros([0]), [0])
    assert_equals(move_zeros([]), [])
    print('Success')
