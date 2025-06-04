def change(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1  # base case

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]

coins = [1, 2, 5]
amount = 5
print("Output is", change(amount, coins))