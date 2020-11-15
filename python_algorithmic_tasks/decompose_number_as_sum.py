from typing import List


class Solution:
    def __init__(self):
        self.resulting_sequences = set()

    def _decompose(self, current_numbers, current_target):
        for number in self.candidates:
            if current_target - number == 0:
                self.resulting_sequences.add(tuple(sorted((*current_numbers, number))))
            elif current_target - number > 0:
                self._decompose([*current_numbers, number], current_target - number)

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        self.candidates = candidates
        self._decompose([], target)
        return self.resulting_sequences


if __name__ == "__main__":
    assert Solution().combinationSum([2, 3, 6, 7], 7) == {(2, 2, 3), (7,)}, 'Test1'
