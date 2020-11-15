from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []
        if n == 0:
            result.append("")
        else:
            for c in range(n):
                for left in self.generateParenthesis(c):
                    for right in self.generateParenthesis(n - c - 1):
                        result.append(f'({left}){right}')
        return result


if __name__ == '__main__':
    assert Solution().generateParenthesis(1) == ['()'], 'Test1'
    assert set(Solution().generateParenthesis(3)) == set(
        ['((()))', '(()())', '(())()', '()(())', '()()()']
    ), 'Test2'
