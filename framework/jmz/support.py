"""Capability matrix: chip x ios -> what can be done."""

from .chips import max_ios

def _f(v):
    try:
        return float(v)
    except Exception:
        return 0.0

def capability(chip: str, ios: str) -> dict:
    """Return the honest capability record for a chip + iOS version."""
    v = _f(ios)
    br = {"A7": "checkm8", "A8": "checkm8", "A9": "checkm8", "A9X": "checkm8",
          "A10": "checkm8", "A10X": "checkm8", "A11": "checkm8",
          "A12": "usbliter8", "A12X": "usbliter8", "A12Z": "usbliter8",
          "A13": "usbliter8"}.get(chip)

    if not chip:
        return {"verdict": "unknown", "method": None, "offline": None,
                "requires": [], "notes": ["ما قدرنا نحدد الشريحة"]}

    if v > max_ios(chip):
        return {"verdict": "impossible", "method": None, "offline": None,
                "requires": [], "notes": [f"{chip} لا يستقبل iOS {ios} أصلاً"]}

    # checkm8 family: offline, any iOS the engine supports (<= 26.1 in tr4mpass)
    if br == "checkm8":
        if v > 26.1:
            return {"verdict": "unsupported", "method": "checkm8", "offline": True,
                    "requires": [], "notes": ["iOS أحدث من 26.1 — لا يدعمه المحرك الحالي"]}
        cellular = chip not in ("A7", "A8")
        return {"verdict": "supported", "method": "checkm8", "offline": True,
                "requires": ["USB فقط"],
                "notes": ["الشبكة تعمل" if cellular else "بدون شبكة (واي فاي فقط)"]}

    # usbliter8 family: A12/A13, needs RP2350 board, offline activation
    if br == "usbliter8":
        notes = ["يحتاج لوحة RP2350 + كابل Lightning"]
        if v >= 26.2:
            notes.append("iOS 26.2+ يحتاج باتش mobileactivationd (خطوة إضافية)")
        return {"verdict": "supported", "method": "usbliter8", "offline": True,
                "requires": ["RP2350", "kابل Lightning", "host لينكس/ماك"],
                "notes": notes}

    # A14+: no bootrom exploit
    if chip in ("A14", "A15", "A16", "A17"):
        if v > 26.1:
            return {"verdict": "unsupported", "method": None, "offline": False,
                    "requires": [], "notes": ["لا ثغرة بوت + iOS 26.2+ أغلق أوامر التنشيط"]}
        return {"verdict": "conditional", "method": "session", "offline": False,
                "requires": ["إنترنت"],
                "notes": ["مسار جلسة — غير مضمون، وكوده ناقص في المحرك"]}

    if chip in ("A18", "A19"):
        return {"verdict": "unsupported", "method": None, "offline": False,
                "requires": [], "notes": ["بدون ثغرة عامة"]}

    return {"verdict": "unknown", "method": None, "offline": None,
            "requires": [], "notes": []}
