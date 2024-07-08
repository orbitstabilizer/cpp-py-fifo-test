import os
import subprocess
import time
from matplotlib import pyplot as plt

# Create pipes
pipe_r1, pipe_w1 = os.pipe()  # Pipe for Python to write to C++ (stdin of C++)
pipe_r2, pipe_w2 = os.pipe()  # Pipe for C++ to write to Python (stdout of C++)

# Launch C++ process with the appropriate file descriptors
cpp_process = subprocess.Popen(
    ["./main"],
    stdin=pipe_r1,
    stdout=pipe_w2,
    close_fds=True
)

# Close unused pipe ends in the parent process
os.close(pipe_r1)
os.close(pipe_w2)

# Write data to C++ process
diffs = []
for _ in range(10000):
    now = time.perf_counter()
    data_to_send =  str(now).encode() + b'\n'
    os.write(pipe_w1, data_to_send)

# Read response from C++ process
    cpp_output = float(os.read(pipe_r2,18).decode())
    read_time = time.perf_counter()
    diff = read_time - now
    diffs.append(diff)
fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(range(10000), diffs)

fig.savefig("pipe.png")



print(f"Average time taken to read from pipe: {sum(diffs[100:])/len(diffs[100:])*1e6: .6f}  microseconds")
os.close(pipe_r2)  # Close read end after receiving data
os.close(pipe_w1)  # Close write end after sending data
