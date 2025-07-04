from collections import defaultdict

def totalFruit(fruits):
    from collections import defaultdict

    fruit_count = defaultdict(int)
    left = 0
    max_fruits = 0

    for right in range(len(fruits)):
        fruit_count[fruits[right]] += 1

        # Shrink the window until we have at most 2 types
        while len(fruit_count) > 2:
            fruit_count[fruits[left]] -= 1
            if fruit_count[fruits[left]] == 0:
                del fruit_count[fruits[left]]
            left += 1

        max_fruits = max(max_fruits, right - left + 1)

    return max_fruits

def totalFruit_v2(fruits) -> int:
        fruits_count = {}
        fruits_type = 0
        start = 0
        max_fruits = 0
        for end in range(len(fruits)):
            if fruits[end] not in  fruits_count or fruits_count[fruits[end]] == 0:
                fruits_count[fruits[end]]  = 1
                fruits_type += 1
            else:
                fruits_count[fruits[end]] += 1
            while fruits_type > 2:
                fruits_count[fruits[start]] -= 1
                if fruits_count[fruits[start]] == 0:
                    fruits_type -= 1
                start = start + 1
                
            max_fruits = max(max_fruits, end-start+1)

        return max_fruits

if __name__ == '__main__':
    """
    You are visiting a farm that has a single row of fruit trees arranged from left to right. 
    The trees are represented by an integer array fruits where fruits[i] is the type of fruit the ith tree produces.

    You want to collect as much fruit as possible. However, the owner has some strict rules that you must follow:

    You only have two baskets, and each basket can only hold a single type of fruit. There is no limit on the amount of fruit each basket can hold.
    Starting from any tree of your choice, you must pick exactly one fruit from every tree (including the start tree) while moving to the right. The picked fruits must fit in one of your baskets.
    Once you reach a tree with fruit that cannot fit in your baskets, you must stop.

    Given the integer array fruits, return the maximum number of fruits you can pick.

    Example 1:

    Input: fruits = [1,2,1]
    Output: 3
    Explanation: We can pick from all 3 trees.

    
    Summary - 

        1. Sliding Window -> Expand right to include more fruits
        2. HashMap (dictionary) -> Keep count of fruit types in the window
        3. Shrink When > 2 types -> Move left pointer and update the basket
        4. Goal -> Max size of a valid window (with â‰¤ 2 fruit types)

    """
    arr = [1,2,1]
    print("Maximum Fruits ->", totalFruit(arr))

    arr = [3,3,3,1,2,1,1,2,3,3,4]
    print("Maximum Fruits ->", totalFruit_v2(arr))