import subprocess
import time

start_time = time.time()
subprocess.run(["./c_exec"])
print(f"Execution time (C): {time.time() - start_time} seconds")

start_time = time.time()
subprocess.run(["./cpp_exec"])
print(f"Execution time (C++): {time.time() - start_time} seconds")

start_time = time.time()
subprocess.run(["java", "Main"])
print(f"Execution time (Java): {time.time() - start_time} seconds")

# start_time = time.time()
# subprocess.run(["python3", "script2.py"])
# print(f"Execution time (Python): {time.time() - start_time} seconds")

start_time = time.time()
subprocess.run(["python3", "script1.py"])
print(f"Execution time (Numba Python): {time.time() - start_time} seconds")