Yes! In stock buy and sell problems, there are several variations that are commonly asked in interviews. Each has a different constraint, and you need a different strategy or pattern to solve it efficiently.

⸻

📊 All Variants of “Stock Buy and Sell” Problems

⸻

✅ 1. Best Time to Buy and Sell Stock (Single Transaction)
	•	Problem: Buy once and sell once to maximize profit.
	•	Pattern: Greedy / Single Pass
	•	Solution: Track the minimum price so far and max profit.

```python
def max_profit(prices):
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit
```



⸻

✅ 2. Best Time to Buy and Sell Stock II (Unlimited Transactions)
	•	Problem: You can buy and sell as many times as you want (but must sell before buying again).
	•	Pattern: Greedy
	•	Solution: Add every price increase to profit.

```python
def max_profit(prices):
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit
```




✅ 3. Best Time to Buy and Sell Stock III (At Most Two Transactions)
	•	Problem: You may complete at most two transactions.
	•	Pattern: Dynamic Programming (DP)
	•	Solution: Use two passes with profit tracking.

```python
def max_profit(prices):
    n = len(prices)
    left_profits = [0]*n
    right_profits = [0]*n
    
    min_price = prices[0]
    for i in range(1, n):
        min_price = min(min_price, prices[i])
        left_profits[i] = max(left_profits[i-1], prices[i] - min_price)
    
    max_price = prices[-1]
    for i in range(n-2, -1, -1):
        max_price = max(max_price, prices[i])
        right_profits[i] = max(right_profits[i+1], max_price - prices[i])
    
    return max(left + right for left, right in zip(left_profits, right_profits))
```


✅ 4. Best Time to Buy and Sell Stock IV (At Most k Transactions)
	•	Problem: You may complete at most k transactions.
	•	Pattern: DP with Transaction State
	•	Solution: Use 2D DP table: dp[k+1][n]

```python
def max_profit(k, prices):
    if not prices or k == 0:
        return 0
    n = len(prices)
    if k >= n // 2:
        return sum(max(prices[i+1] - prices[i], 0) for i in range(n-1))
    
    dp = [[0] * n for _ in range(k+1)]
    for t in range(1, k+1):
        max_diff = -prices[0]
        for d in range(1, n):
            dp[t][d] = max(dp[t][d-1], prices[d] + max_diff)
            max_diff = max(max_diff, dp[t-1][d] - prices[d])
    return dp[k][-1]

```




✅ 5. Best Time to Buy and Sell Stock with Cooldown
	•	Problem: After you sell a stock, you cannot buy stock on the next day (1 day cooldown).
	•	Pattern: DP with State Machine
	•	States:
	•	hold: Max profit if holding a stock
	•	sold: Max profit if just sold a stock
	•	rest: Max profit if in cooldown or resting

```python
def max_profit(prices):
    if not prices:
        return 0
    n = len(prices)
    hold, sold, rest = -float('inf'), 0, 0
    for price in prices:
        prev_sold = sold
        sold = hold + price
        hold = max(hold, rest - price)
        rest = max(rest, prev_sold)
    return max(sold, rest)

```

⸻

✅ 6. Best Time to Buy and Sell Stock with Transaction Fee
	•	Problem: Each transaction costs a fee. Maximize profit.
	•	Pattern: DP
	•	States:
	•	cash: max profit without holding stock
	•	hold: max profit with holding stock

```python
def max_profit(prices, fee):
    cash, hold = 0, -prices[0]
    for price in prices[1:]:
        cash = max(cash, hold + price - fee)
        hold = max(hold, cash - price)
    return cash

```


⸻

🧠 Summary Table
```
Problem Variant	   Max Transactions	 Fee	Cooldown	Pattern Used	Time Complexity
 1.   I	                1	 	               No	   Greedy	            O(n)
 2.   II	Unlimited	No	No	Greedy	O(n)
 3.   III	2	No	No	DP (2-pass)	O(n)
 4.   IV	k	No	No	DP	O(k * n)
 5.   Cooldown	Unlimited	No	Yes	DP	O(n)
 6.   With Fee	Unlimited	Yes	No	DP	O(n)

```


⸻

