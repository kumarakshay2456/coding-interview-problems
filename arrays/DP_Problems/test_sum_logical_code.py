# def check_num(a):
#     print("Number is ",  a)
#     a = a + 6
#     print("A is", a)

# a = 5
# check_num(a)
# print("A is", a)


# def check_list(s):
#     print("List is", s)
#     s.append(9)
#     print("List after the append", s)
# # check the list
# s = [1,2,3,6]

# check_list(s)
# print("Python list is", s)


import sys

# Regular function returning a list
def get_all_numbers(n):
    return [x for x in range(n)]

# Generator function
def get_numbers_generator(n):
    for i in range(n):
        yield i

# Compare memory usage for a large sequence
# n = 1000000

# # List approach
# numbers_list = get_all_numbers(n)
# list_size = sys.getsizeof(numbers_list)

# # Generator approach
# numbers_gen = get_numbers_generator(n)
# gen_size = sys.getsizeof(numbers_gen)
# print("List  is", numbers_list)
# print(f"List size: {list_size:,} bytes")  # Will be many megabytes
# print(f"Generator size: {gen_size} bytes")  # Will be tiny (around 112 bytes)

import sys
import time

# List comprehension
start = time.time()
list_comp = [x * x for x in range(10000000)]
list_time = time.time() - start
list_size = sys.getsizeof(list_comp)

# Generator expression
start = time.time()
gen_exp = (x * x for x in range(10000000))
gen_time = time.time() - start
gen_size = sys.getsizeof(gen_exp)

print(f"List comprehension:")
print(f"  - Creation time: {list_time:.6f} seconds")
print(f"  - Memory size: {list_size:,} bytes")

print(f"Generator expression:")
print(f"  - Creation time: {gen_time:.6f} seconds")
print(f"  - Memory size: {gen_size} bytes")

# Iteration time
start = time.time()
sum_list = sum(list_comp)  # Already computed, just sums
list_iter_time = time.time() - start

start = time.time()
sum_gen = sum(gen_exp)  # Computes each value during iteration
gen_iter_time = time.time() - start

print(f"List iteration time: {list_iter_time:.6f} seconds")
print(f"Generator iteration time: {gen_iter_time:.6f} seconds")

