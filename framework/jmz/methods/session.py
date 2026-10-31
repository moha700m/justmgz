import subprocess, os
from .base import Method


class Session(Method):
    def __init__(self):
        super().__init__(
            name="session",
            chips=["A12", "A12X", "A12Z", "A13", "A14", "A15", "A16", "A17"],
            offline=False, needs_hardware=[], ios_max=26.1,
            description="تنشيط عبر الجلسة — يحتاج إنترنت وغير مضمون")

    def steps(self):
        return ["tr4mpass -d", "tr4mpass --activate-only -v", "راقب السجل"]

    def run(self, device):
        engine = os.environ.get("TR4MPASS_BIN", "tr4mpass")
        try:
            p = subprocess.run([engine, "--activate-only", "-v"],
                               capture_output=True, text=True, timeout=1800)
            log = (p.stdout or "") + (p.stderr or "")
            return {"ok": p.returncode == 0 and "[ERROR]" not in log, "log": log}
        except Exception as e:
            return {"ok": False, "log": str(e)}
