import subprocess

print("Sending a background ping probe...")
response = subprocess.run(["ping", "-n", "1", "8.8.8.8"], capture_output=True, text=True)
raw_output = response.stdout

# Loop through the output line by line to find our target
for line in raw_output.splitlines():
    if "time=" in line:

        part1 = line.split("time=")[1]
        part2 = part1.split("ms")[0]
        print(part1)
        print(part2)




        # --- YOUR FISHING CHALLENGE AREA ---
        # 1. Split the line at "time=" and grab the right side (index 1)
        # 2. Split that result at "ms" and grab the left side (index 0)
        # 3. Type cast the final string into an integer

        # Write your code here to isolate the number!
        # ping_time = ...

        # print(f"Successfully extracted integer: {ping_time}")