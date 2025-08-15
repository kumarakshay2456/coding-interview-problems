from datetime import datetime

def check_array_append(n):
    start_time = datetime.now()
    a = []
    for i in range(n):
        a.append(i)
    time_diff = (datetime.now() - start_time).total_seconds()
    print(f"Total time taken {time_diff:.6f}")

if __name__ == '__main__':
    check_array_append(100000000)
