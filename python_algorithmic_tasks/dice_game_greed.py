from collections import Counter

"""
Three 1's => 1000 points
Three 6's =>  600 points
Three 5's =>  500 points
Three 4's =>  400 points
Three 3's =>  300 points
Three 2's =>  200 points
One   1   =>  100 points
One   5   =>   50 point
"""
RULES = {
    (1, 3): 1000,
    (6, 3): 600,
    (5, 3): 500,
    (4, 3): 400,
    (3, 3): 300,
    (2, 3): 200,
    (1, 1): 100,
    (5, 1): 50,
}


def score(arr: list) -> int:
    total_score = 0
    dice_counts = Counter(arr)
    for (number, req_count), score in RULES.items():
        while number in dice_counts and dice_counts[number] >= req_count:
            total_score += score
            dice_counts[number] -= req_count
    return total_score


def assert_equals(x, y):
    try:
        assert x == y
    except AssertionError as exc:
        print(f'# Error\n{x} != {y}')
        raise


if __name__ == '__main__':

    assert_equals(score([2, 3, 4, 6, 2]), 0)
    assert_equals(score([4, 4, 4, 3, 3]), 400)
    assert_equals(score([2, 4, 4, 5, 4]), 450)
    assert_equals(score([1, 1, 1, 1, 4]), 1100)
    assert_equals(score([1, 5, 1, 3, 4]), 250)
    print('Success')
