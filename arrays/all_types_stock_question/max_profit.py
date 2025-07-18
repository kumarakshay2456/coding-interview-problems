def get_maximum_profit(arr):
    maxPro = 0
    minPrice = float('inf')
    for i in range(len(arr)):
        minPrice = min(minPrice, arr[i])
        maxPro = max(maxPro, arr[i] - minPrice)
    return maxPro

def get_maximum_profit_v2(prices):
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        # Update min_price if current price is smaller
        if price < min_price:
            min_price = price
        else:
            # Calculate profit if sold today
            profit = price - min_price
            max_profit = max(max_profit, profit)
    
    return max_profit

        
if __name__ == '__main__':
    """
    Problem Statement: You are given an array of prices where prices[i] is the price of a given stock on an ith day.

    You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. 
    Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.


    Example 1:

        Input: prices = [7,1,5,3,6,4]
        Output: 5
        Explanation: Buy on day 2 (price = 1) and 
        sell on day 5 (price = 6), profit = 6-1 = 5.

        Note: That buying on day 2 and selling on day 1 
        is not allowed because you must buy before 
        you sell.

    Example 2:

        Input: prices = [7,6,4,3,1]
        Output: 0
        Explanation: In this case, no transactions are 
        done and the max profit = 0
            
    """
    arr = [7,6,4,3,1]
    print("Maximum Profit is -> ", get_maximum_profit(arr))
    arr = [7,1,5,3,6,4]
    print("Maximum Profit is -> ", get_maximum_profit(arr))
