# ⚡ DevOps Live Network Latency Dashboard: Project Post-Mortem

**Developer:** Mokhtar  
**Academic Level:** 1st Year, 6th of October Technological University  
**Target Roadmap:** Senior DevOps Engineer  
**Completion Date:** June 22, 2026 (Achieved 8 Days Ahead of Milestone Deadline)  
**Version:** v1.0.0 (Officially Stamped & Tagged)

---

## 🏗️ 1. ARCHITECTURAL PATTERNS & ENGINE LOGIC

### Object-Oriented Uptime Tracking (`class SERVER`)

Instead of relying on messy, unscalable global lists or parallel arrays to track infrastructure data, the project is
anchored by a decoupled **Object-Oriented Programming (OOP)** state engine.

* **State Encapsulation:** Each target infrastructure node is initialized as an independent instance tracking its unique
  properties (`name`, `ip`, `threshold`, `last_ping`, `status`).
* **Dynamic Mutation:** The `check_network` method isolates network probing operations entirely inside the object,
  modifying internal string properties natively so that any attached interface can read the updated state cleanly.

### High-Performance Modular Code Splitting

The project evolved from a single monolithic script into a clean, professional, multi-tier file structure:

* `engine.py`: Houses the pure, interface-agnostic `SERVER` blueprint. Completely decoupled from display frameworks.
* `main_rich.py`: Uses the `rich` stream engine to render a clean, live terminal table.
* `main_textual.py`: Consolidates the advanced, asynchronous full-screen interactive TUI dashboard.

---

## ⚡ 2. NETWORK PROTOCOLS & SUBPROCESS MECHANICS

### ICMP Telemetry Parsing vs. Bandwidth Metrics

The tool operates as a localized telemetry service checking network responsiveness. We differentiated the two core
pillars of network speed:

* **Bandwidth (e.g., FAST.com / Speedtest):** Capacity over time—how much data a network pipe can carry concurrently.
* **Latency / Round-Trip Time (Our Tool):** Network response agility—the exact time in milliseconds ($ms$) required for
  a small signaling packet to navigate the routing fabric to a target destination and echo back.

### Windows Subprocess Interrogation

The core probing engine invokes the underlying operating system's networking stack via Python's `subprocess.Popen` and
`subprocess.run`.

* We customized execution flags (`["ping", "-n", "1", self.ip]`) to explicitly mandate a single iteration, preventing
  the script from hanging on standard 4-packet default loops.
* We captured low-level OS standard output streams (`capture_output=True, text=True`) and developed raw text string
  parsers to dissect the raw output buffer, isolating localized success blocks (`"time="`) or catastrophic failures (
  `"timed out"`, `"unreachable"`).

---

## 🛠️ 3. SYSTEM INTERFACES (TUI) & PERFORMANCE OPTIMIZATION

### Web-Inspired Layout Engineering (Textual & TCSS)

We upgraded the interface from a scrolling stdout text stream to a fully interactive Terminal User Interface (TUI) using
the **Textual** framework.

* **Component Widgets:** Leveraged `DataTable`, `Header(show_clock=True)`, and `Footer` to mimic modern desktop
  application shells.
* **Cell Key Mapping Quirk:** Encountered and solved a critical Textual rendering constraint: Textual automatically
  mutates raw string column descriptors into unique structural `ColumnKey` entities. We fixed a runtime
  `CellDoesNotExist` crash by explicitly capturing those keys during component mounting (
  `self.col_latency = columns[3]`) and using them for cell mutation.

### Multi-Threaded Asynchronous Concurrency

* **The Synchronous Blocking I/O Bottleneck:** Running an OS command like `ping` inside a single-threaded loop freezes
  the execution flow. The main thread sits completely idle waiting for network response loops, causing user interaction
  loops (mouse hovering, keyboard scrolling) to experience severe input lag and stuttering.
* **The Threaded Solution:** We solved this using Textual's `@work(thread=True)` framework. We offloaded the heavy
  operating system blocking operations to a isolated **worker background thread**.
* **Thread-Safe Cross Communication:** Background threads are structurally restricted from directly drawing to user
  interface pixels to avoid race conditions. We implemented `self.call_from_thread(self.update_ui_display)` to safely
  push parsed background telemetry strings up to the main UI UI rendering engine, achieving a smooth interface.

### Self-Bootstrapping Process Liberation

IDE integrated terminal windows (like PyCharm's run panes) do not expose a raw operating system Teletypewriter/TTY
interface, which breaks TUI mouse tracking and formatting. We implemented a professional self-bootstrapping escape
sequence:

```python
if not sys.stdin.isatty() and len(sys.argv) == 1:
    subprocess.Popen(["cmd", "/c", "start", sys.executable, __file__, "--external"])
    sys.exit()