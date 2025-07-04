import time

def loop(n: int):
    tmp = []
    for i in range(n):
        tmp.append(i)  # Collecting values to avoid optimization
    return tmp

start_time = time.time()
# loop(1_000_000_000)
loop(10_000_000)
print(f"Execution time: {time.time() - start_time} seconds")

