"""Chip identifiers -> chip names -> exploit families."""

CPID_CHIP = {
    "8960": "A7", "7000": "A8", "7001": "A8", "8000": "A9", "8003": "A9X",
    "8010": "A10", "8011": "A10X", "8015": "A11",
    "8020": "A12", "8027": "A12X", "8028": "A12Z",
    "8030": "A13", "8101": "A14", "8110": "A15", "8120": "A16",
    "8130": "A17", "8140": "A18", "8150": "A19",
}

# chip -> bootrom exploit family
BOOTROM = {
    "A7": "checkm8", "A8": "checkm8", "A9": "checkm8", "A9X": "checkm8",
    "A10": "checkm8", "A10X": "checkm8", "A11": "checkm8",
    "A12": "usbliter8", "A12X": "usbliter8", "A12Z": "usbliter8", "A13": "usbliter8",
}

# chips that lose cellular after offline activation
NO_CELLULAR = {"A7", "A8"}

CHIP_MODELS = {
    "A7": ["iPhone 5s", "iPad Air", "iPad mini 2/3"],
    "A8": ["iPhone 6", "6 Plus", "iPad mini 4", "iPad Air 2 (A8X)"],
    "A9": ["iPhone 6s", "6s Plus", "SE 1", "iPad 5"],
    "A10": ["iPhone 7", "7 Plus", "iPad 6/7"],
    "A11": ["iPhone 8", "8 Plus", "X"],
    "A12": ["iPhone XR", "XS", "XS Max", "iPad Air 3", "mini 5", "iPad 8"],
    "A13": ["iPhone 11", "11 Pro", "11 Pro Max", "SE 2", "iPad 9"],
    "A14": ["iPhone 12 series", "iPad Air 4", "iPad 10"],
    "A15": ["iPhone 13 series", "SE 3", "iPhone 14", "14 Plus", "mini 6"],
    "A16": ["iPhone 14 Pro", "14 Pro Max", "15", "15 Plus", "iPad 11"],
    "A17": ["iPhone 15 Pro", "15 Pro Max"],
    "A18": ["iPhone 16 series", "16e"],
}

def chip_name(cpid: str) -> str:
    if not cpid:
        return ""
    key = cpid.lower().replace("0x", "").zfill(4)
    return CPID_CHIP.get(key, "")

def bootrom(chip: str):
    return BOOTROM.get(chip)

# آخر إصدار رسمي يدعمه كل معالج
MAX_IOS = {
    "A7": 12.5, "A8": 12.5, "A9": 15.8, "A9X": 15.8,
    "A10": 15.8, "A10X": 16.7, "A11": 16.7,
    "A12": 26.9, "A12X": 26.9, "A12Z": 26.9, "A13": 26.9,
    "A14": 26.9, "A15": 26.9, "A16": 26.9, "A17": 26.9, "A18": 26.9,
}

def max_ios(chip: str) -> float:
    return MAX_IOS.get(chip, 26.9)
