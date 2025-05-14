def climbStairs(n:int):
    # Bottom-Up Tabulation
    if n <= 1:
        return 1
    prev1 = 1
    prev2 = 1
    for i in range(2, n+1):
        total = prev1 + prev2
        prev2 = prev1
        prev1 = total
    return prev1

def climbStairs_v2(n: int):
    memo = {}
    if n <= 1:
        return 1
    if n in memo:
        return memo[n]
    memo[n] = climbStairs(n-1) + climbStairs(n-2)

    return memo[n]

if __name__ == '__main__':
    n = 1000000
    print("Total ways he can climb", climbStairs(n))
    print("Total ways he can climb V2", climbStairs_v2(n))
