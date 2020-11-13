class Solution:
    MIN = -(2 ** 31)
    MAX = -MIN - 1
    SIGNS = ['-', '+']

    def myAtoi(self, s: str) -> int:
        s = s.strip()
        total_chars = len(s)
        i = result = 0
        intermediate_res = []
        while i < total_chars and (i == 0 and (s[i] in Solution.SIGNS) or s[i].isdigit()):
            intermediate_res.append(s[i])
            i += 1
        if intermediate_res and (len(intermediate_res) > 1 or intermediate_res[0] not in Solution.SIGNS):
            result = int(''.join(intermediate_res))
            if result > Solution.MAX:
                result = Solution.MAX
            elif result < Solution.MIN:
                result = Solution.MIN
        return result


if __name__ == "__main__":
    assert Solution().myAtoi('42') == 42, 'Test1'
    assert Solution().myAtoi('  -42') == -42, 'Test2'
    assert Solution().myAtoi('4193 with words') == 4193, 'Test3'
    assert Solution().myAtoi('  -  ') == 0, 'Test4'
    assert Solution().myAtoi('  +  ') == 0, 'Test5'
    assert Solution().myAtoi('  +1  ') == 1, 'Test6'
