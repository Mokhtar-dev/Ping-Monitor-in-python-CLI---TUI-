import sys
import subprocess
import time
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable


# ==========================================
# 1. CORE NETWORK ENGINE CLASS
# ==========================================
class SERVER:
    def __init__(self, name, ip, threshold):
        self.name = name
        self.ip = ip
        self.threshold = threshold
        self.last_ping = "---"
        self.status = "Initializing"

    def check_network(self):
        """Fires a single ping and updates the object's internal state strings"""
        response = subprocess.run(["ping", "-n", "1", self.ip], capture_output=True, text=True)
        raw_output = response.stdout

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


# ==========================================
# 2. TEXTUAL DASHBOARD INTERFACE
# ==========================================
class NetworkMonitorApp(App):
    """A professional live network latency dashboard built with Textual."""

    BINDINGS = [("q", "quit", "Quit Dashboard")]

    def __init__(self, servers):
        super().__init__()
        self.servers = servers
        # Storage for our dynamic column keys
        self.col_latency = None
        self.col_status = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield DataTable(id="latency-table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"

        # FIX: Capture the assigned column keys directly from Textual!
        columns = table.add_columns("Server Name", "IP Address", "Warning Threshold", "Current Latency", "Status")
        self.col_latency = columns[3]  # Maps exactly to "Current Latency"
        self.col_status = columns[4]  # Maps exactly to "Status"

        for server in self.servers:
            table.add_row(
                server.name,
                server.ip,
                f"{server.threshold}ms",
                "🔄 Probing...",
                "Initializing",
                key=server.name
            )

        self.set_interval(1.5, self.update_dashboard_metrics)

    def update_dashboard_metrics(self) -> None:
        table = self.query_one(DataTable)

        for server in self.servers:
            server.check_network()

            if "❌" in server.status:
                status_styled = f"[b red]{server.status}[/b red]"
                latency_styled = "[red]---[/red]"
            elif "🚨" in server.status:
                status_styled = f"[b yellow]{server.status}[/b yellow]"
                latency_styled = f"[yellow]{server.last_ping}[/yellow]"
            else:
                status_styled = f"[b green]{server.status}[/b green]"
                latency_styled = f"[green]{server.last_ping}[/green]"

            # FIX: Use the native ColumnKey objects instead of raw strings!
            table.update_cell(server.name, self.col_latency, latency_styled)
            table.update_cell(server.name, self.col_status, status_styled)


# ==========================================
# 3. APPLICATION LAUNCHPAD
# ==========================================
if __name__ == "__main__":
    # Bootstrapper to pop out of the restrictive IDE terminal pane
    if not sys.stdin.isatty() and len(sys.argv) == 1:
        subprocess.Popen(["cmd", "/c", "start", sys.executable, __file__, "--external"])
        sys.exit()

    infrastructure = [
        SERVER("Google Public DNS", "8.8.8.8", threshold=90),
        SERVER("Cloudflare Core DNS", "1.1.1.1", threshold=25),
        SERVER("Testing Broken Host", "192.0.2.1", threshold=50)
    ]

    app = NetworkMonitorApp(servers=infrastructure)
    app.run()
