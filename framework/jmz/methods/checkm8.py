import subprocess, os
from .base import Method


class Checkm8(Method):
    def __init__(self):
        super().__init__(
            name="checkm8",
            chips=["A7", "A8", "A9", "A9X", "A10", "A10X", "A11"],
            offline=True, needs_hardware=[], ios_max=26.1,
            description="ثغرة BootROM — محلية، بدون إنترنت")

    def steps(self):
        return ["tr4mpass -d", "tr4mpass -a -v", "تحقق: شاشة رئيسية + شبكة"]

    def run(self, device):
        engine = os.environ.get("TR4MPASS_BIN", "tr4mpass")
        try:
            p = subprocess.run([engine, "-a", "-v"], capture_output=True, text=True, timeout=1800)
            return {"ok": p.returncode == 0 and "[ERROR]" not in p.stdout,
                    "log": (p.stdout or "") + (p.stderr or "")}
        except Exception as e:
            return {"ok": False, "log": str(e)}
