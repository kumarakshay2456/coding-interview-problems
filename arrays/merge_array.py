def get_start(interval):
    return interval[0]

def merge(intervals):
    if not intervals:
        return []

    # Step 1: Sort 
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


def merge_v2(intervals):
    # Space complexcity is O(1)

    if not intervals:
        return []

    intervals.sort(key=get_start)

    index = 0  # Points to the last merged interval

    for i in range(1, len(intervals)):
        current = intervals[i]
        last = intervals[index]

        if current[0] <= last[1]:  # Overlap
            last[1] = max(last[1], current[1])
        else:
            index += 1
            intervals[index] = current  # Move non-overlapping interval forward

    return intervals[:index + 1]

if __name__ =='__main__':
    print(merge(intervals = [[1, 4], [2, 5], [7, 9]]))
    print(merge_v2(intervals = [[1, 4], [2, 5], [7, 9]]))