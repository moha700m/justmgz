"""Decision engine: device + iOS -> ordered plan."""

from .support import capability

STEPS = {
    "checkm8": [
        "تأكد من الكيبل ووضع الجهاز (عادي أو DFU)",
        "شغّل المحرك: tr4mpass -d للكشف",
        "نفّذ: tr4mpass -a -v  (مسار checkm8)",
        "تحقق من النتيجة: شاشة رئيسية + شبكة",
    ],
    "usbliter8": [
        "وصّل لوحة RP2350 وفلّش فيرموير usbliter8",
        "أدخل الجهاز DFU ثم انقله للوحة → تحقق PWND: usbliter8",
        "أقلع SSHRD ramdisk واتصل SSH",
        "mount -o rw,union,update /System",
        "استبدل RaptorActivation.pem",
        "شغّل سيرفر التنشيط المحلي + ideviceactivation",
        "احذف Setup.app واعمل uicache",
    ],
    "session": [
        "وصّل الجهاز وأدخل DFU",
        "شغّل المحرك: tr4mpass --activate-only -v",
        "راقب السجل — النتيجة غير مضمونة",
    ],
    None: ["لا يوجد مسار متاح لهذا الجهاز حالياً"],
}

def build_plan(chip: str, ios: str, model: str = "") -> dict:
    cap = capability(chip, ios)
    method = cap.get("method")
    return {
        "model": model,
        "chip": chip,
        "ios": ios,
        "verdict": cap["verdict"],
        "method": method,
        "offline": cap["offline"],
        "requires": cap["requires"],
        "notes": cap["notes"],
        "steps": STEPS.get(method, STEPS[None]),
        "ready": cap["verdict"] in ("supported", "conditional"),
    }
