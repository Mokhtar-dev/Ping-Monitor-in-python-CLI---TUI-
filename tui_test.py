import sys
import os
import subprocess
from textual.app import App


class MyTUI(App):
    pass  # Your TUI implementation goes here


if __name__ == "__main__":
    # Check if we are running in an interactive terminal or a detached process
    # If sys.stdin is not a TTY (like inside some IDEs) or an external flag is missing:
    if not sys.stdin.isatty() and len(sys.argv) == 1:
        # Re-execute itself in an external terminal window (Windows example)
        subprocess.Popen(["cmd", "/c", "start", sys.executable, __file__, "--external"])
        sys.exit()

    # If it is already running in a valid TTY, execute normally
    app = MyTUI()
    app.run()
