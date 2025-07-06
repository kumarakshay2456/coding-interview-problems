arr = [[1, 3], [2, 6], [4, 5]]

# Step 1: Find max time to define range
max_time = max(end for _, end in arr)

# Step 2: Initialize timeline array
timeline = [0] * (max_time + 2)  # +2 to safely handle end+1

# Step 3: Mark starts and ends
for start, end in arr:
    timeline[start] += 1
    timeline[end + 1] -= 1

# Step 4: Compute prefix sum
active_counts = []
current = 0
for t in range(1, max_time + 1):
    current += timeline[t]
    active_counts.append(current)

print(active_counts)  # Output: [1, 2, 2, 2, 2, 1]