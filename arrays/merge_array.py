def get_start(interval):
    return interval[0]

def merge(intervals):
    if not intervals:
        return []

    # Step 1: Sort using a regular function instead of lambda
    intervals.sort(key=get_start)

    merged = [intervals[0]]

    for current in intervals[1:]:
        last = merged[-1]

        # Check for overlap
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])  # Merge
        else:
            merged.append(current)

    return merged

if __name__ =='__main__':
    print(merge(intervals = [[1, 4], [2, 5], [7, 9]]))