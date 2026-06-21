import subprocess
import time


class SERVER:
    def __init__(self, name, ip, threshold):
        self.name = name
        self.ip = ip
        self.threshold = threshold

    def diagnostics(self, duration=10):
        end_time = time.time() + duration
        print(f"Starting real time ping {self.name} monitoring for {duration} sec...")
        while time.time() < end_time:
            response = subprocess.run(["ping", "-n", "1", self.ip], capture_output=True, text=True)
            raw_output = response.stdout
            for line in raw_output.splitlines():
                if "time=" in line:
                    part1 = line.split("time=")[1]
                    part2 = part1.split("ms")[0]
                    ping_time = int(part2)
                    if ping_time > self.threshold:
                        print(f"Ping time is greater than 90ms your ping is {ping_time} ms")
                    else:
                        print(f"the ping is good: {ping_time}ms")
            time.sleep(1)


cloud_flare = SERVER("cloud_flare", ip="1.1.1.1", threshold=90)
Google = SERVER("Google_DNS", ip="8.8.8.8", threshold=90)
Google.diagnostics(duration=5)
cloud_flare.diagnostics(duration=5)
