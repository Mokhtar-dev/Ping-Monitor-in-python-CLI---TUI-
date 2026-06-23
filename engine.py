import subprocess


class SERVER:
    def __init__(self, name, ip, threshold):
        self.name = name
        self.ip = ip
        self.threshold = threshold
        # Make sure these placeholder properties exist for Textual to read!
        self.last_ping = "---"
        self.status = "Initializing"

    def check_network(self):  # <--- RENAME THIS FROM diagnostics TO check_network
        """Fires a single ping and updates the object's internal state strings"""
        response = subprocess.run(["ping", "-n", "1", self.ip], capture_output=True, text=True)
        raw_output = response.stdout

        # Check for Windows-specific failure phrases
        if "timed out" in raw_output.lower() or "unreachable" in raw_output.lower():
            self.last_ping = "---"
            self.status = "❌ DOWN"
        else:
            for line in raw_output.splitlines():
                if "time=" in line:
                    part1 = line.split("time=")[1]
                    part2 = part1.split("ms")[0]
                    ping_time = int(part2)
                    self.last_ping = f"{ping_time}ms"

                    if ping_time > self.threshold:
                        self.status = "🚨 HIGH LATENCY"
                    else:
                        self.status = "✅ HEALTHY"
