from .base import Method


class Usbliter8(Method):
    def __init__(self):
        super().__init__(
            name="usbliter8",
            chips=["A12", "A12X", "A12Z", "A13"],
            offline=True,
            needs_hardware=["RP2350", "Lightning cable"],
            ios_max=99.0,
            description="ثغرة BootROM جديدة — محلية، تحتاج لوحة")

    def steps(self):
        return [
            "فلّش RP2350 بفيرموير usbliter8",
            "DFU → لوحة → تحقق PWND: usbliter8",
            "SSHRD ramdisk + SSH",
            "mount rw + استبدال RaptorActivation.pem",
            "سيرفر تنشيط محلي + ideviceactivation",
            "حذف Setup.app + uicache",
        ]

    def run(self, device):
        # المسار يحتاج هاردوير بشري — لا يُنفّذ تلقائياً
        return {"ok": False, "manual": True,
                "log": "هذا المسار يحتاج خطوات يدوية مع لوحة RP2350 — راجع steps()"}
