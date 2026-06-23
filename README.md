# Network Ping Monitor TUI

A lightweight, automated command-line tool written in Python designed to monitor network latency and alert
administrators of performance degradation in real-time.

## 🚀 Why This Exists

In a DevOps environment, unexpected network latency can break database synchronization and degrade user experience. This
tool automates continuous latency tracking, removing the need for manual network probing.

## 🛠️ Key Features & Architecture

- **Object-Oriented Design:** Built using a modular class structure to represent independent target servers.
- **Automated Probing:** Utilizes Python's native `subprocess` engine to interface directly with system-level network
  utilities.
- **Intelligent Thresholding:** Monitors round-trip time (RTT) every 5 minutes and flags any spike exceeding 90ms.
- **TUI Interface (Planned):** A terminal user interface dashboard for visual, live monitoring.

## 📦 Getting Started

### Prerequisites

- Python 3.x Installed
- Git

### Installation

```bash
git clone [https://github.com/yourusername/ping-monitor.git](https://github.com/yourusername/ping-monitor.git)
cd ping-monitor

