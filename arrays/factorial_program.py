def fact(n=int):
    if n==1 or n==0:
        return 1
    return n * fact(n-1)

def fact_without_recursion(n=int):
    number = 1
    for i in range(1,n+1):
        number = number * i
    return number

factorial_cache = {}

def fact_dp(n):
    if n in factorial_cache:
        return factorial_cache[n]
    
    if n == 0 or n == 1:
        factorial_cache[n] = 1
    else:
        factorial_cache[n] = n * fact_dp(n - 1)
    
    return factorial_cache[n]

    
if __name__  == '__main__':
    print("With Recrusion -> ", fact(10))
    print("Without Recrusion -> ", fact_without_recursion(10)) 
    print("factorial using the DP Recrusion -> ", fact_dp(10)) 