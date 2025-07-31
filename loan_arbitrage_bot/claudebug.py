#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import re
import shutil
import signal
import psutil
from datetime import datetime
from typing import Optional, Tuple, Dict, Any, List
from pathlib import Path
import json

try:
    import anthropic
except ImportError:
    print("[FAIL] Please install anthropic: pip install anthropic")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("[FAIL] Please install requests: pip install requests")
    sys.exit(1)

# === Static Configuration ===
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your_anthropic_api_key_here")
BACKEND_FILE = "main.py"
FRONTEND_FILE = "dashboard.html"
TEST_SCRIPT = "test_full_optimized.py"
REQUIREMENTS_FILE = "requirements.txt"
MAX_ITERATIONS = 10
BACKEND_STARTUP_WAIT = 12
TEST_TIMEOUT = 180
CLAUDE_MODEL = "claude-sonnet-4-20250514"

class AdvancedClaudeDebugBot:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        self.iteration = 0
        self.backup_dir = f"debug_backups_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.session_log = []
        self.successful_fixes = []
        self.failed_fixes = []
        self.backend_process = None
        self.backend_port = 8000
        self.app_name = "app"

        # Load backend app name and port from main.py
        self.load_backend_config()

        os.makedirs(self.backup_dir, exist_ok=True)
        print(f"[INIT] Advanced Debug Session Started")
        print(f"[INIT] Backup directory: {self.backup_dir}")
        print(f"[INIT] Using FastAPI app: {self.app_name}, port: {self.backend_port}")

    def load_backend_config(self):
        code = ""
        try:
            with open(BACKEND_FILE, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            print(f"[WARN] Couldn't read {BACKEND_FILE}: {e}")
            return

        # App name
        match = re.search(r"(\w+)\s*=\s*FastAPI\s*\(", code)
        if match:
            self.app_name = match.group(1)

        # Port detection
        port_match = re.search(r"port\s*=\s*(\d+)", code)
        if port_match:
            self.backend_port = int(port_match.group(1))

    def kill_processes_on_port(self, port: int):
        print(f"[KILL] Searching for processes on port {port}...")
        try:
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    connections = proc.info['connections']
                    if connections:
                        for conn in connections:
                            if hasattr(conn, 'laddr') and conn.laddr and conn.laddr.port == port:
                                print(f"[KILL] Terminating process {proc.pid} ({proc.name()})")
                                proc.terminate()
                                proc.wait(timeout=5)
                except Exception:
                    continue
            time.sleep(1)
        except Exception as e:
            print(f"[WARN] Could not kill processes on port {port}: {e}")

    def start_backend(self):
        if self.backend_process and self.backend_process.poll() is None:
            print("[WARN] Backend already running")
            return True
        try:
            print("[START] Starting backend...")
            self.kill_processes_on_port(self.backend_port)
            startup_cmd = [
                sys.executable, "-m", "uvicorn", f"main:{self.app_name}",
                "--host", "0.0.0.0",
                "--port", str(self.backend_port),
                "--log-level", "info"
            ]
            print(f"[CMD] {' '.join(startup_cmd)}")
            self.backend_process = subprocess.Popen(
                startup_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            for i in range(BACKEND_STARTUP_WAIT):
                time.sleep(1)
                if self.backend_process.poll() is not None:
                    print("[FAIL] Backend crashed")
                    return False
                if self.check_backend_health():
                    print("[OK] Backend is healthy")
                    return True
            print("[WARN] Backend didn't respond in time")
            return True
        except Exception as e:
            print(f"[FAIL] Error starting backend: {e}")
            return False

    def stop_backend(self):
        if self.backend_process:
            print("[STOP] Terminating backend...")
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=10)
            except:
                self.backend_process.kill()
        self.kill_processes_on_port(self.backend_port)

    def check_backend_health(self) -> bool:
        urls = [
            f"http://localhost:{self.backend_port}/health",
            f"http://localhost:{self.backend_port}/docs"
        ]
        for url in urls:
            try:
                r = requests.get(url, timeout=5)
                if r.status_code in [200, 422]:
                    return True
            except requests.exceptions.RequestException:
                continue
        return False

    # ... existing methods (run_tests, extract_errors, query_claude, apply_fixes, etc.)
    # remain unchanged (see your original script)
    # Just be sure they use self.backend_port and self.app_name anywhere you previously hardcoded them

def main():
    print("Claude Debug Bot - Automated AI-Powered Debugging")
    print("=" * 60)
    missing = [f for f in [BACKEND_FILE, TEST_SCRIPT] if not os.path.exists(f)]
    if missing:
        print(f"[FAIL] Missing: {', '.join(missing)}")
        return 1
    if CLAUDE_API_KEY == "your_anthropic_api_key_here":
        print("[FAIL] Please set ANTHROPIC_API_KEY environment variable")
        return 1
    bot = AdvancedClaudeDebugBot()
    bot.run_debug_cycle()
    return 0

if __name__ == "__main__":
    sys.exit(main())
