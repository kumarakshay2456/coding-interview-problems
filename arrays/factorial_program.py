def fact(n=int):
    if n==1 or n==0:
        return 1
    return n * fact(n-1)

def fact_without_recursion(n=int):
    number = 1
    for i in range(1,n+1):
        number = number * i
    return number

    
if __name__  == '__main__':
    print("With Recrusion -> ", fact(10))
    print("Without Recrusion -> ", fact_without_recursion(10)) 