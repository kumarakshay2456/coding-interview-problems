import multiprocessing
import threading
import time

# def io_bound_task1(name):
#     # apis calls here
#     print(f"Thread {name} is called")
#     time.sleep(25)

# def io_bound_task2(name):
#     print(f"Thread {name} is called")
#     time.sleep(6)

# def io_bound_task3(name):
#     print(f"Thread {name} is called")
#     time.sleep(1)


# start_time = time.time()
# threads = []
# for i in range(4):
#     if i == 1:
#         t = threading.Thread(target=io_bound_task1, args=(i,))
#     elif i == 2:
#         t = threading.Thread(target=io_bound_task2, args=(i,))   
#     else:
#         t = threading.Thread(target=io_bound_task2, args=(i,))
#     threads.append(t)
#     t.start()

# for i in threads:
#     i.join()
# print(f"Total time {(time.time() - start_time):.2f}")


# def cpu_task(n):
#     def fib(n):
#         if n <= 1:
#             return n
#         return fib(n-1) + fib(n-2)

#     print(f"[Process for fib({n})] started")
#     result = fib(n)
#     print(f"[Process for fib({n})] result: {result}")

# if __name__ == "__main__":
#     start_time = time.time()
#     multi_process = []

#     for i in [5, 10, 12]:
#         p = multiprocessing.Process(target=io_bound_task1, args=(i,))
#         multi_process.append(p)
#         p.start()

#     for p in multi_process:
#         p.join()

#     print(f"Total time {(time.time() - start_time):.2f}")



# import multiprocessing
# import threading
# import time

# def io_task(filename):
#     with open(filename, 'r') as f:
#         data = f.read()
#     print(f"{filename} read {len(data)} bytes")

# # create a small file
# for i in range(3):
#     with open(f"text_{i}.txt", "w") as f:
#         f.write("hell word\n" * 10000000)

# def run_with_processes():
#     start = time.time()
#     process = []
#     for i in range(3):
#         p = multiprocessing.Process(target=io_task, args=(f"text_{i}.txt", ))
#         process.append(p)
#         p.start()
#     for p in process:
#         p.join()
#     print(f"Total time in multiprocess {(time.time() - start):.2f}")

# def run_with_threads():
#     start = time.time()
#     process = []
#     for i in range(3):
#         p = threading.Thread(target=io_task, args=(f"text_{i}.txt", ))
#         process.append(p)
#         p.start()
#     for p in process:
#         p.join()
#     print(f"Total time in threading {(time.time() - start):.2f}")


# if __name__ == "__main__":
#     run_with_processes()
#     run_with_threads()

# import time
# import threading
# import multiprocessing

# # CPU-bound function
# def calculate_sum(n):
#     total = 0
#     for i in range(n):
#         total += i
#     return total

# # Single-threaded execution
# def single_thread():
#     start = time.time()
#     calculate_sum(50000000)
#     calculate_sum(50000000)
#     end = time.time()
#     return end - start

# # Multi-threaded execution (limited by GIL)
# def multi_thread():
#     start = time.time()
    
#     t1 = threading.Thread(target=calculate_sum, args=(50000000,))
#     t2 = threading.Thread(target=calculate_sum, args=(50000000,))
    
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()
    
#     end = time.time()
#     return end - start

# # Multi-process execution (bypasses GIL)
# def multi_process():
#     start = time.time()
    
#     p1 = multiprocessing.Process(target=calculate_sum, args=(50000000,))
#     p2 = multiprocessing.Process(target=calculate_sum, args=(50000000,))
    
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
    
#     end = time.time()
#     return end - start

# if __name__ == "__main__":
#     print(f"Single thread time: {single_thread():.2f} seconds")
#     print(f"Multi thread time: {multi_thread():.2f} seconds")
#     print(f"Multi process time: {multi_process():.2f} seconds")


import time
import threading
import multiprocessing
import asyncio
import aiohttp
import requests
import concurrent.futures

# ----- CPU-BOUND EXAMPLE -----
def cpu_heavy_task(n):
    """A CPU-intensive function"""
    count = 0
    for i in range(n):
        count += i
    return count

# Sequential CPU execution
def sequential_cpu():
    start = time.time()
    results = [cpu_heavy_task(10000000) for _ in range(4)]
    return time.time() - start

# Thread-based CPU execution
def threaded_cpu():
    start = time.time()
    threads = []
    for _ in range(4):
        thread = threading.Thread(target=cpu_heavy_task, args=(10000000,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    return time.time() - start

# Process-based CPU execution
def process_cpu():
    start = time.time()
    processes = []
    for _ in range(4):
        process = multiprocessing.Process(target=cpu_heavy_task, args=(10000000,))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    return time.time() - start

# ----- I/O-BOUND EXAMPLE -----
def io_task(url):
    """An I/O-bound function"""
    response = requests.get(url)
    return len(response.content)

# URLs for testing
urls = [
    "https://python.org",
    "https://github.com",
    "https://stackoverflow.com",
    "https://wikipedia.org",
] * 3  # 12 URLs total

# Sequential I/O
def sequential_io():
    start = time.time()
    results = [io_task(url) for url in urls]
    return time.time() - start

# Thread-based I/O
def threaded_io():
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        results = list(executor.map(io_task, urls))
    return time.time() - start

# Process-based I/O
def process_io():
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(io_task, urls))
    return time.time() - start

# Asyncio I/O
async def async_io_task(url, session):
    """Async version of I/O task"""
    async with session.get(url) as response:
        content = await response.read()
        return len(content)

async def async_main():
    async with aiohttp.ClientSession() as session:
        tasks = [async_io_task(url, session) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

def asyncio_io():
    start = time.time()
    asyncio.run(async_main())
    return time.time() - start

# Run all examples
if __name__ == "__main__":
    print("--- CPU-BOUND TASK COMPARISON ---")
    print(f"Sequential execution: {sequential_cpu():.2f} seconds")
    print(f"Threaded execution: {threaded_cpu():.2f} seconds")
    print(f"Process execution: {process_cpu():.2f} seconds")
    
    print("\n--- I/O-BOUND TASK COMPARISON ---")
    print(f"Sequential execution: {sequential_io():.2f} seconds")
    print(f"Threaded execution: {threaded_io():.2f} seconds")
    print(f"Process execution: {process_io():.2f} seconds")
    print(f"Asyncio execution: {asyncio_io():.2f} seconds")




