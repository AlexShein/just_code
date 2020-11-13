from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        result = 0
        length = len(height)
        x = 0
        y = length - 1
        while True:
            area = min((height[x], height[y])) * (y - x)
            result = max((result, area))
            if height[x] < height[y]:
                x += 1
            else:
                y -= 1
            if x == y:
                break
        return result


if __name__ == "__main__":
    assert Solution().maxArea([1, 2]) == 1, 'Test0'
    assert Solution().maxArea([1, 1]) == 1, 'Test1'
    assert Solution().maxArea([4, 3, 2, 1, 4]) == 16, 'Test2'
    assert Solution().maxArea([1, 2, 1]) == 2, 'Test3'
    assert Solution().maxArea([2, 3, 4, 5, 18, 17, 6]) == 17, 'Test3'
