import subprocess
import time

start_time = time.time()
end_time = time.time() + 10

print("Starting real time ping monitoring for 10 sec...")
while time.time() < end_time:
    response = subprocess.run(["ping", "-n", "1", "1.1.1.1"], capture_output=True, text=True)
    raw_output = response.stdout
    for line in raw_output.splitlines():
        if "time=" in line:
            part1 = line.split("time=")[1]
            part2 = part1.split("ms")[0]
            ping_time = int(part2)
            if ping_time > 90:
                print(f"Ping time is greater than 90ms your ping is {ping_time} ms")
            else:
                print(f"the ping is good: {ping_time}ms")
    time.sleep(1)
print("Successful scan no delays")
