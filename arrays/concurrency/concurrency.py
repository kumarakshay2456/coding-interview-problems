import asyncio

async def task(name, delay):
    print(f"Task {name} stated")
    await asyncio.sleep(delay)
    print(f"{name} finished after {delay} second")


async def main():
    await asyncio.gather(task("Task A", 2), task("Task B", 3), task("Task C", 1))

if __name__ == '__main__':

    """
    Example: asyncio – concurrent tasks
    """
    asyncio.run(main())



import threading
import time

def task(name, delay):
    print(f"{name} started")
    time.sleep(delay)
    print(f"{name} finished after {delay} seconds")

# Create threads
thread1 = threading.Thread(target=task, args=("Task A", 2))
thread2 = threading.Thread(target=task, args=("Task B", 3))
thread3 = threading.Thread(target=task, args=("Task C", 1))

# Start threads
thread1.start()
thread2.start()
thread3.start()

# Wait for threads to complete
thread1.join()
thread2.join()
thread3.join()