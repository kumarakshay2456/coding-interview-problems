def merge_intervas(intervals):
    merged = []
    intervals.sort()
    for start , end in intervals:
        if not merged or merged[-1][1] < start:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def insert_intervals(intervals, new_inter):
    # intervals = [[2,5],[6,9]], new = [1,3]
    # intervals = [[1,3],[6,9]], new = [2,5]
    merged = []
    for start , end in intervals:
        if not merged:
            if new_inter[0] < start:
                if new_inter[1] > start:
                    merged.append([new_inter[0], end])
                else:
                    merged.append(new_inter)
                    merged.append([start, end])
            else:
                merged.append([start, end])
        else:
            if merged[-1][1] > new_inter[0]:





        





    
if __name__ == '__main__':
    intervals = [[1,6],[2,3],[8,10],[15,18]]
    print(merge_intervas(intervals))
