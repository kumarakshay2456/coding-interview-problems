def get_car_in_each_hour(data, maximum_hour)->list:
    diff = [0] * (maximum_hour + 2)  # one extra for end+1
    for start, end in data:
        if start <= maximum_hour:
            diff[start] += 1
        if end+1 <= maximum_hour:
            diff[end+1] -= 1
    print("diff", diff)
    total = [0] * (maximum_hour + 1)
    count = 0
    for h in range(1, maximum_hour+1):
        count += diff[h]
        total[h] = count
    return total[1:]
            
if __name__ == '__main__':
    data = [[4,5], [1,3], [2,6]]
    """
    You are designing a system for a parking lot.

	•	Each car enters at some hour start_time and leaves at end_time.
	•	Both start_time and end_time are inclusive, meaning the car is present during both of those hours.
	•	You are given N parking tickets, where each ticket is represented as an interval [start_time, end_time].
	•	You are also given a maximum observation time M (in hours).

    Your task is to determine how many cars are present in the parking lot at each hour from 1 to M.

    🔹 Input

        •	tickets: A list of intervals, where each interval [start, end] represents the time a car was parked.
        •	M: An integer, the maximum number of hours to observe.
        tickets = [[4, 5], [1, 3], [2, 6]]
        M = 8 

    🔹 Output
  
        [1, 2, 2, 2, 2, 1, 0, 0]
        Explanation:

            •	Hour 1 → Car [1,3] → 1 car
            •	Hour 2 → Cars [1,3], [2,6] → 2 cars
            •	Hour 3 → Cars [1,3], [2,6] → 2 cars
            •	Hour 4 → Cars [4,5], [2,6] → 2 car
            •	Hour 5 → Car [4,5], [2,6] → 2 car
            •	Hour 6 → Car [2,6] → 1 car
            •	Hours 7 & 8 → No cars

	•	A list of length M, where the i-th element represents the number of cars present in the parking lot at hour i.
    Time Complexity:
	•	Marking changes = O(N)
	•	Prefix sum over hours = O(M)
	•	✅ Total = O(N + M)
	•	Space Complexity:
	•	Difference array = O(M)
	•	Result array = O(M)
	•	✅ Total = O(M)
    """
    maximum_hour = 8
    print(*get_car_in_each_hour(data, maximum_hour))