def lengthOfLongestSubstring(s: str) -> int:
    res = 0
    for index, _ in enumerate(s):
        acc = set()
        for letter in s[index:]:
            if letter in acc:
                break
            acc.add(letter)
            res = max((res, len(acc)))
    return res


if __name__ == "__main__":
    assert lengthOfLongestSubstring("abcabcbb") == 3, 'Test 1'
