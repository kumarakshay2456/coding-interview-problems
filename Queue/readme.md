# 🧾 Python Queues: Complete Guide

A comprehensive guide to Python's queue implementations: **Queue**, **deque**, and **list**

## Table of Contents

- [Overview](#overview)
- [1. queue.Queue - Thread-Safe FIFO Queue](#1-queuequeue---thread-safe-fifo-queue)
- [2. collections.deque - Fast, Flexible Queue or Stack](#2-collectionsdeque---fast-flexible-queue-or-stack)
- [3. list - Simple but Not Ideal for Queues](#3-list---simple-but-not-ideal-for-queues)
- [When to Use Which Queue?](#when-to-use-which-queue)
- [Performance Comparison](#performance-comparison)
- [Advanced Examples](#advanced-examples)
- [Best Practices](#best-practices)

## Overview

Python provides several data structures that can be used as queues. Each has its own strengths and use cases:

- **`queue.Queue`**: Thread-safe, ideal for multi-threaded applications
- **`collections.deque`**: Fast and flexible, perfect for single-threaded scenarios
- **`list`**: Simple but inefficient for queue operations

---

## 🔹 1. queue.Queue – Thread-Safe FIFO Queue

### 📦 Import

```python
from queue import Queue
```

### ✅ Use When

- You are working in a **multi-threaded** environment
- You need **built-in locking** to avoid race conditions
- Implementing producer-consumer patterns
- Building thread-safe applications

### 🚫 Not Ideal For

- BFS or simple algorithms (has overhead due to thread safety)
- Single-threaded applications where performance is critical
- Memory-constrained environments

### 📚 Common Methods

| Method | Description | Time Complexity |
|--------|-------------|-----------------|
| `q.put(item)` | Add item to queue (blocks if full) | O(1) |
| `q.get()` | Remove and return item (blocks if empty) | O(1) |
| `q.put_nowait(item)` | Add item without blocking (raises exception if full) | O(1) |
| `q.get_nowait()` | Get item without blocking (raises exception if empty) | O(1) |
| `q.qsize()` | Approximate number of items in the queue | O(1) |
| `q.empty()` | Returns True if queue is empty | O(1) |
| `q.full()` | Returns True if queue is full | O(1) |
| `q.task_done()` | Mark a task as done | O(1) |
| `q.join()` | Block until all tasks are done | - |

### ✅ Basic Example

```python
from queue import Queue

# Create a queue with maximum size of 5
q = Queue(maxsize=5)

# Add items
q.put("A")
q.put("B")
q.put("C")

print(f"Queue size: {q.qsize()}")  # 3
print(f"Is empty: {q.empty()}")    # False
print(f"Is full: {q.full()}")      # False

# Remove items
print(q.get())  # A
print(q.get())  # B
print(f"Queue size after getting 2 items: {q.qsize()}")  # 1
```

### 🔧 Advanced Example: Producer-Consumer Pattern

```python
import threading
import time
from queue import Queue

def producer(q, name):
    """Producer function that adds items to queue"""
    for i in range(5):
        item = f"{name}-item-{i}"
        q.put(item)
        print(f"Producer {name} produced: {item}")
        time.sleep(0.1)

def consumer(q, name):
    """Consumer function that processes items from queue"""
    while True:
        try:
            item = q.get(timeout=1)  # Wait 1 second for item
            print(f"Consumer {name} consumed: {item}")
            time.sleep(0.2)  # Simulate processing time
            q.task_done()
        except:
            print(f"Consumer {name} finished")
            break

# Create queue and threads
q = Queue()
threads = []

# Start producers
for i in range(2):
    t = threading.Thread(target=producer, args=(q, f"P{i}"))
    t.start()
    threads.append(t)

# Start consumers  
for i in range(2):
    t = threading.Thread(target=consumer, args=(q, f"C{i}"))
    t.daemon = True  # Dies when main thread dies
    t.start()
    threads.append(t)

# Wait for all producers to finish
for t in threads[:2]:  # Only producer threads
    t.join()

# Wait for all tasks to be processed
q.join()
print("All tasks completed!")
```

---

## 🔹 2. collections.deque – Fast, Flexible Queue or Stack

### 📦 Import

```python
from collections import deque
```

### ✅ Use When

- You want a **fast queue or stack**
- You are doing BFS, DFS, or general queue operations in a **single-threaded** context
- You need to add/remove elements from both ends
- Performance is critical

### ⚡ Why It's Fast

- **O(1)** time for append, pop, appendleft, and popleft
- Implemented with a **doubly linked list** with optimized memory blocks
- No thread-safety overhead
- Memory efficient for large datasets

### 📚 Common Methods

| Method | Description | Time Complexity |
|--------|-------------|-----------------|
| `dq.append(x)` | Add item to the **right** end | O(1) |
| `dq.appendleft(x)` | Add item to the **left** end | O(1) |
| `dq.pop()` | Remove and return item from **right** end | O(1) |
| `dq.popleft()` | Remove and return item from **left** end | O(1) |
| `dq.extend(iterable)` | Add multiple items to right end | O(k) |
| `dq.extendleft(iterable)` | Add multiple items to left end | O(k) |
| `dq.rotate(n)` | Rotate deque n steps to the right | O(k) |
| `dq.clear()` | Remove all elements | O(n) |
| `dq.count(x)` | Count occurrences of x | O(n) |
| `dq.remove(x)` | Remove first occurrence of x | O(n) |
| `len(dq)` | Get number of elements | O(1) |
| `dq[i]` | Access element by index | O(n) |

### ✅ Basic Example

```python
from collections import deque

# Create deque
dq = deque()

# Add elements
dq.append('A')      # Add to right: ['A']
dq.appendleft('B')  # Add to left: ['B', 'A']
dq.append('C')      # Add to right: ['B', 'A', 'C']

print(f"Deque: {list(dq)}")  # ['B', 'A', 'C']

# Remove elements
print(dq.popleft())  # B (FIFO - queue behavior)
print(dq.pop())      # C (LIFO - stack behavior)
print(f"Remaining: {list(dq)}")  # ['A']
```

### 🔧 Advanced Example: BFS Implementation

```python
from collections import deque

def bfs_traversal(graph, start):
    """
    Breadth-First Search traversal using deque
    """
    visited = set()
    queue = deque([start])
    result = []
    
    while queue:
        vertex = queue.popleft()  # O(1) dequeue operation
        
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)
            
            # Add neighbors to queue
            for neighbor in graph.get(vertex, []):
                if neighbor not in visited:
                    queue.append(neighbor)  # O(1) enqueue operation
    
    return result

# Example usage
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

traversal_order = bfs_traversal(graph, 'A')
print(f"BFS traversal: {traversal_order}")  # ['A', 'B', 'C', 'D', 'E', 'F']
```

### 🔄 Deque as Sliding Window

```python
from collections import deque

def sliding_window_maximum(arr, k):
    """
    Find maximum in each sliding window of size k
    """
    dq = deque()  # Store indices
    result = []
    
    for i in range(len(arr)):
        # Remove indices outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove indices of smaller elements
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        
        dq.append(i)
        
        # Add to result if window is complete
        if i >= k - 1:
            result.append(arr[dq[0]])
    
    return result

# Example
arr = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(sliding_window_maximum(arr, k))  # [3, 3, 5, 5, 6, 7]
```

---

## 🔹 3. list – Simple but Not Ideal for Queues

### 📦 Built-in

```python
q = []
```

### ✅ Use When

- You need a **simple collection**
- You're not removing from the front (only append and pop from end)
- Working with small datasets where performance isn't critical
- Quick prototyping or simple scripts

### 🚫 Avoid For

- Queue use cases with `pop(0)` — **O(n)** time because of element shifting
- Large datasets requiring frequent front removals
- Performance-critical applications

### 📚 Common Methods

| Method | Description | Time Complexity |
|--------|-------------|-----------------|
| `q.append(x)` | Add to end | O(1) amortized |
| `q.pop()` | Remove from end (LIFO) | O(1) |
| `q.pop(0)` | Remove from front (❌ O(n) – inefficient) | O(n) |
| `q.insert(0, x)` | Insert at beginning (❌ O(n) – inefficient) | O(n) |
| `q[0]` | Access first element | O(1) |
| `q[-1]` | Access last element | O(1) |
| `len(q)` | Get length | O(1) |
| `x in q` | Check membership | O(n) |

### ⚠️ Example: Why Lists Are Poor Queues

```python
import time

def test_queue_performance(n=10000):
    """
    Demonstrate why lists are inefficient for queue operations
    """
    print(f"Testing with {n} operations...")
    
    # Test list as queue (inefficient)
    start_time = time.time()
    q_list = []
    
    # Add elements
    for i in range(n):
        q_list.append(i)
    
    # Remove from front (O(n) each time!)
    for i in range(n):
        q_list.pop(0)  # This is slow!
    
    list_time = time.time() - start_time
    
    # Test deque as queue (efficient)
    start_time = time.time()
    q_deque = deque()
    
    # Add elements
    for i in range(n):
        q_deque.append(i)
    
    # Remove from front (O(1) each time)
    for i in range(n):
        q_deque.popleft()  # This is fast!
    
    deque_time = time.time() - start_time
    
    print(f"List time: {list_time:.4f} seconds")
    print(f"Deque time: {deque_time:.4f} seconds")
    print(f"Deque is {list_time/deque_time:.1f}x faster!")

# Run the test
test_queue_performance()
```

### ✅ When Lists Are Actually Good

```python
# Stack operations (LIFO) - lists are perfect for this
stack = []

# Push operations
stack.append(1)
stack.append(2)
stack.append(3)
print(f"Stack: {stack}")  # [1, 2, 3]

# Pop operations (from end - O(1))
print(stack.pop())  # 3
print(stack.pop())  # 2
print(f"Stack after pops: {stack}")  # [1]
```

---

## 🧠 When to Use Which Queue?

| Use Case | Recommended | Why |
|----------|-------------|-----|
| **BFS/DFS traversal** | `collections.deque` ✅ | O(1) operations, no thread overhead |
| **Multi-threaded task queue** | `queue.Queue` ✅ | Thread-safe, built-in synchronization |
| **Simple stack (LIFO)** | `list` or `deque` | Both work well for stack operations |
| **Need to insert/remove both ends** | `collections.deque` ✅ | Optimized for both ends |
| **Sliding window problems** | `collections.deque` ✅ | Efficient double-ended operations |
| **Producer-consumer pattern** | `queue.Queue` ✅ | Thread synchronization features |
| **Web scraping task queue** | `queue.Queue` ✅ | Thread-safe for concurrent requests |
| **Undo/Redo functionality** | `collections.deque` ✅ | Efficient history management |
| **Simple data collection** | `list` | Fine for small, simple use cases |

---

## 🧪 Performance Comparison

| Operation | list | deque | queue.Queue |
|-----------|------|-------|-------------|
| **append(x)** | ✅ O(1) | ✅ O(1) | ✅ O(1) |
| **pop(0) / popleft()** | ❌ O(n) | ✅ O(1) | ✅ O(1) |
| **Access by index** | ✅ O(1) | ❌ O(n) | ❌ Not supported |
| **Thread-Safe** | ❌ No | ❌ No | ✅ Yes |
| **Memory overhead** | ✅ Low | ✅ Low | ❌ Higher (locks) |
| **Use case** | Stack/Array | Queue/Deque | Thread-safe queue |

### 📊 Benchmark Results

```python
import time
from collections import deque
from queue import Queue

def benchmark_queues(n=100000):
    """
    Benchmark different queue implementations
    """
    print(f"Benchmarking {n} operations...\n")
    
    # Test append operations
    data = list(range(n))
    
    # List append
    start = time.time()
    l = []
    for item in data:
        l.append(item)
    list_append_time = time.time() - start
    
    # Deque append
    start = time.time()
    d = deque()
    for item in data:
        d.append(item)
    deque_append_time = time.time() - start
    
    # Queue put
    start = time.time()
    q = Queue()
    for item in data:
        q.put(item)
    queue_put_time = time.time() - start
    
    print("APPEND/PUT Operations:")
    print(f"List:  {list_append_time:.4f}s")
    print(f"Deque: {deque_append_time:.4f}s")
    print(f"Queue: {queue_put_time:.4f}s")
    
    # Test pop/get operations (first 1000 items for list to be reasonable)
    test_n = min(1000, n)
    
    # List pop(0) - only test small number due to O(n) complexity
    l_test = list(range(test_n))
    start = time.time()
    while l_test:
        l_test.pop(0)
    list_pop_time = time.time() - start
    
    # Deque popleft
    start = time.time()
    while d and len(d) > n - test_n:
        d.popleft()
    deque_pop_time = time.time() - start
    
    # Queue get
    start = time.time()
    for _ in range(test_n):
        if not q.empty():
            q.get()
    queue_get_time = time.time() - start
    
    print(f"\nPOP/GET Operations ({test_n} items):")
    print(f"List pop(0):     {list_pop_time:.4f}s")
    print(f"Deque popleft(): {deque_pop_time:.4f}s")
    print(f"Queue get():     {queue_get_time:.4f}s")

# Run benchmark
benchmark_queues()
```

---

## 🔧 Advanced Examples

### Example 1: Rate Limiter Using Deque

```python
import time
from collections import deque

class RateLimiter:
    """
    Rate limiter using sliding window with deque
    """
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    def is_allowed(self):
        now = time.time()
        
        # Remove old requests outside time window
        while self.requests and self.requests[0] <= now - self.time_window:
            self.requests.popleft()
        
        # Check if we can make a new request
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        
        return False

# Usage
limiter = RateLimiter(max_requests=5, time_window=60)  # 5 requests per minute

for i in range(10):
    if limiter.is_allowed():
        print(f"Request {i+1}: Allowed")
    else:
        print(f"Request {i+1}: Rate limited")
    time.sleep(10)  # Wait 10 seconds between requests
```

### Example 2: Multi-threaded Web Scraper

```python
import threading
import requests
import time
from queue import Queue

class WebScraper:
    """
    Multi-threaded web scraper using Queue
    """
    def __init__(self, num_workers=5):
        self.url_queue = Queue()
        self.result_queue = Queue()
        self.num_workers = num_workers
    
    def worker(self):
        """Worker thread function"""
        while True:
            url = self.url_queue.get()
            if url is None:
                break
            
            try:
                response = requests.get(url, timeout=10)
                result = {
                    'url': url,
                    'status': response.status_code,
                    'size': len(response.content)
                }
                self.result_queue.put(result)
                print(f"✅ Scraped: {url}")
            except Exception as e:
                print(f"❌ Error scraping {url}: {e}")
            finally:
                self.url_queue.task_done()
    
    def scrape_urls(self, urls):
        """Scrape multiple URLs concurrently"""
        # Start worker threads
        threads = []
        for _ in range(self.num_workers):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Add URLs to queue
        for url in urls:
            self.url_queue.put(url)
        
        # Wait for all tasks to complete
        self.url_queue.join()
        
        # Stop workers
        for _ in range(self.num_workers):
            self.url_queue.put(None)
        
        # Collect results
        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get())
        
        return results

# Usage
scraper = WebScraper(num_workers=3)
urls = [
    'https://httpbin.org/delay/1',
    'https://httpbin.org/delay/2',
    'https://httpbin.org/status/200',
    'https://httpbin.org/json',
]

results = scraper.scrape_urls(urls)
for result in results:
    print(f"URL: {result['url']}, Status: {result['status']}, Size: {result['size']} bytes")
```

### Example 3: Undo/Redo System

```python
from collections import deque

class UndoRedoSystem:
    """
    Undo/Redo system using deque for efficient operations
    """
    def __init__(self, max_history=100):
        self.history = deque(maxlen=max_history)
        self.current_state = None
        self.redo_stack = deque()
    
    def execute_command(self, command, *args, **kwargs):
        """Execute a command and save it to history"""
        if self.current_state is not None:
            self.history.append(self.current_state.copy())
        
        # Execute the command
        result = command(*args, **kwargs)
        self.current_state = result
        
        # Clear redo stack when new command is executed
        self.redo_stack.clear()
        
        return result
    
    def undo(self):
        """Undo the last command"""
        if not self.history:
            print("Nothing to undo")
            return None
        
        if self.current_state is not None:
            self.redo_stack.append(self.current_state.copy())
        
        self.current_state = self.history.pop()
        return self.current_state
    
    def redo(self):
        """Redo the last undone command"""
        if not self.redo_stack:
            print("Nothing to redo")
            return None
        
        if self.current_state is not None:
            self.history.append(self.current_state.copy())
        
        self.current_state = self.redo_stack.pop()
        return self.current_state

# Example usage with a simple text editor
class SimpleTextEditor:
    def __init__(self):
        self.text = ""
        self.undo_system = UndoRedoSystem()
    
    def insert_text(self, text):
        """Insert text at the end"""
        new_text = self.text + text
        self.text = self.undo_system.execute_command(lambda: new_text)
        return self.text
    
    def delete_chars(self, count):
        """Delete characters from the end"""
        new_text = self.text[:-count] if count <= len(self.text) else ""
        self.text = self.undo_system.execute_command(lambda: new_text)
        return self.text
    
    def undo(self):
        """Undo last operation"""
        result = self.undo_system.undo()
        if result is not None:
            self.text = result
        return self.text
    
    def redo(self):
        """Redo last undone operation"""
        result = self.undo_system.redo()
        if result is not None:
            self.text = result
        return self.text

# Usage
editor = SimpleTextEditor()
print(f"Initial: '{editor.text}'")

editor.insert_text("Hello")
print(f"After insert 'Hello': '{editor.text}'")

editor.insert_text(" World")
print(f"After insert ' World': '{editor.text}'")

editor.delete_chars(6)
print(f"After delete 6 chars: '{editor.text}'")

editor.undo()
print(f"After undo: '{editor.text}'")

editor.undo()
print(f"After another undo: '{editor.text}'")

editor.redo()
print(f"After redo: '{editor.text}'")
```

---

## 🎯 Best Practices

### 1. Choose the Right Queue Type

```python
# ❌ Wrong: Using list for queue operations
def bad_bfs(graph, start):
    queue = []  # Bad choice for queue
    queue.append(start)
    
    while queue:
        node = queue.pop(0)  # O(n) operation!
        # ... rest of BFS

# ✅ Right: Using deque for queue operations
def good_bfs(graph, start):
    from collections import deque
    queue = deque([start])  # Perfect for queue
    
    while queue:
        node = queue.popleft()  # O(1) operation!
        # ... rest of BFS
```

### 2. Handle Thread Safety Properly

```python
# ❌ Wrong: Using deque in multi-threaded environment
import threading
from collections import deque

shared_deque = deque()  # Not thread-safe!

def worker():
    # Race conditions possible here
    if shared_deque:
        item = shared_deque.popleft()

# ✅ Right: Using Queue for thread safety
from queue import Queue

shared_queue = Queue()  # Thread-safe

def worker():
    try:
        item = shared_queue.get(timeout=1)
        # Process item safely
        shared_queue.task_done()
    except:
        pass  # Handle timeout
```

### 3. Set Appropriate Queue Sizes

```python
# ✅ Good: Set reasonable limits to prevent memory issues
from queue import Queue

# Limit queue size to prevent unlimited growth
task_queue = Queue(maxsize=1000)

# For deque, use maxlen for circular buffer behavior
from collections import deque
recent_items = deque(maxlen=100)  # Keep only last 100 items
```

### 4. Handle Exceptions Properly

```python
from queue import Queue, Empty, Full
import time

def robust_queue_operations():
    q = Queue(maxsize=2)
    
    try:
        # Use timeout to avoid indefinite blocking
        q.put("item1", timeout=1)
        q.put("item2", timeout=1)
        
        # This will raise Full exception due to maxsize=2
        q.put_nowait("item3")  # Non-blocking put
        
    except Full:
        print("Queue is full!")
    
    try:
        # Safe get with timeout
        item = q.get(timeout=1)
        print(f"Got: {item}")
        q.task_done()
        
    except Empty:
        print("Queue is empty!")
```

### 5. Memory Management

```python
# ✅ Good: Clean up queues properly
def cleanup_example():
    from collections import deque
    
    # For large queues, clear explicitly when done
    large_queue = deque(range(1000000))
    
    # Process items...
    while large_queue:
        process_item(large_queue.popleft())
    
    # Explicitly clear if reusing
    large_queue.clear()

def process_item(item):
    # Simulate processing
    pass
```

---

## 📝 Summary

Python provides three main queue implementations, each with distinct advantages:

1. **`queue.Queue`**: Thread-safe, ideal for multi-threaded applications and producer-consumer patterns
2. **`collections.deque`**: Fast and flexible, perfect for single-threaded algorithms like BFS/DFS
3. **`list`**: Simple but inefficient for queue operations due to O(n) front removal

Choose based on your specific needs:
- **Thread safety required** → `queue.Queue`
- **Performance critical, single-threaded** → `collections.deque` 
- **Simple stack operations** → `list` or `deque`
- **Both ends access needed** → `collections.deque`

Remember: avoid using `list.pop(0)` for queue operations in performance-critical code!