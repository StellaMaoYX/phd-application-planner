#!/usr/bin/env python3
"""phd-application-planner · launch.py — start the marimo dashboard, detached and persistent.

Usage:
  python3 launch.py [dashboard.py] [--port N] [--edit] [--no-open]

- Runs `marimo run` (app mode) by default, or `marimo edit` with --edit.
- Detaches via os.setsid so the server survives across shells / tool turns.
- Waits for the port to answer, then opens the default browser (unless --no-open).
- Must be run with a Python that has marimo installed (the same interpreter that
  runs this script is reused for `-m marimo`).
"""
import os
import sys
import time
import socket
import subprocess
import urllib.request
import webbrowser
from pathlib import Path


def free_port(start: int) -> int:
    p = start
    for _ in range(50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
        p += 1
    return start


def main():
    argv = sys.argv[1:]
    edit = "--edit" in argv
    no_open = "--no-open" in argv
    port = None
    if "--port" in argv:
        port = int(argv[argv.index("--port") + 1])
    files = [a for a in argv if not a.startswith("--") and a != (str(port) if port else None)]
    app = files[0] if files else "phd_explorer.py"
    app = str(Path(app).resolve())
    if not Path(app).exists():
        print(f"error: {app} not found", file=sys.stderr)
        sys.exit(1)
    if port is None:
        port = free_port(2740)

    mode = "edit" if edit else "run"
    py = sys.executable
    # Detached launch so the server persists across shells / tool turns.
    # start_new_session=True puts it in its own session+process group (survives parent exit);
    # do NOT also call os.setsid() — that would double-create the session and fail.
    cmd = [py, "-m", "marimo", mode, app, "--headless", "--no-token", "--port", str(port)]
    log = Path(app).parent / "_marimo_run.log"
    with open(log, "w") as lf:
        subprocess.Popen(cmd, stdout=lf, stderr=lf, start_new_session=True, close_fds=True)

    url = f"http://localhost:{port}"
    for _ in range(60):
        try:
            urllib.request.urlopen(url, timeout=1)
            break
        except Exception:
            time.sleep(1)
    print(f"dashboard: {url}  (mode={mode}, log={log})")
    if not no_open:
        try:
            webbrowser.open(url)
        except Exception:
            pass


if __name__ == "__main__":
    main()
