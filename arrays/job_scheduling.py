def get_maximum_profit(jobs) -> int:
    if not jobs:
        return 0
    jobs.sort(reverse=True, key= lambda x:x[2])
    max_deadline = max(job[1] for job in jobs)
    deadline_array = [False] * (max_deadline+1)
    max_profit = 0
    for job in jobs:
        profit = job[2]
        deadline = job[1]
        for i in range(deadline,0,-1):
            if not deadline_array[i]:
                deadline_array[i] = True
                max_profit += profit
                break
    return max_profit
    

if __name__ == '__main__':
    """
    You are given n jobs, where each job takes 1 unit of time to complete.
        Each job has:

	•	an ID
	•	a deadline (the latest time slot by which it should be completed)
	•	a profit (earned only if the job is finished before or on its deadline).

    Your task is to schedule jobs in such a way that total profit is maximized.
    You can only schedule one job per unit of time, and each job takes exactly 1 time unit. 
    
    """
    jobs = [
    ("A", 2, 100),
    ("B", 1, 19),
    ("C", 2, 27),
    ("D", 1, 25),
    ("E", 3, 15)
    ]
    print(get_maximum_profit(jobs))