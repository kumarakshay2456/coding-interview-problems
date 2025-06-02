def coinChange(coins, amount):
    # Initialize DP array with inf, and 0 at index 0
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    # Build up the DP array
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

coins = [1, 2, 5]
amount = 11
print(coinChange(coins, amount))  # Output: 3 (5 + 5 + 1)