import argparse, sys
from .chips import CPID_CHIP, CHIP_MODELS, BOOTROM
from .support import capability
from .plan import build_plan
from .methods import all_methods

RISK = {"supported": "✅ مدعوم", "conditional": "⚠️ بشرط", "unsupported": "❌ غير مدعوم",
        "unknown": "؟", "impossible": "— إصدار غير موجود لهذا الجهاز"}

def cmd_matrix(args):
    chips = args.chips or list(CHIP_MODELS.keys())
    versions = args.ios or ["12", "15", "18", "26.0", "26.1", "26.2"]
    print(f"{'chip':6} {'model':22} " + " ".join(f"{v:>7}" for v in versions))
    print("-" * (30 + 8 * len(versions)))
    for c in chips:
        row = []
        for v in versions:
            cap = capability(c, v)
            row.append({"supported": "  ✅  ", "conditional": "  ⚠️  ",
                        "unsupported": "  ❌  ", "impossible": "  —  "}.get(cap["verdict"], "  ?  "))
        model = (CHIP_MODELS.get(c) or [""])[0][:22]
        print(f"{c:6} {model:22} " + " ".join(f"{x:>7}" for x in row))
    print("\n✅ ينفتح كامل · ⚠️ بشرط (إنترنت/غير مضمون) · ❌ لا")

def cmd_plan(args):
    plan = build_plan(args.chip, args.ios, args.model or "")
    print("=" * 52)
    print(f"  الجهاز: {plan['model'] or plan['chip']}   |   iOS {plan['ios']}")
    print("=" * 52)
    print(f"  الحكم   : {RISK.get(plan['verdict'], plan['verdict'])}")
    print(f"  الطريقة : {plan['method'] or '—'}")
    print(f"  بدون إنترنت: {'نعم' if plan['offline'] else 'لا'}")
    if plan["requires"]:
        print(f"  يحتاج   : {' · '.join(plan['requires'])}")
    for n in plan["notes"]:
        print(f"  ملاحظة  : {n}")
    print("-" * 52)
    for i, s in enumerate(plan["steps"], 1):
        print(f"  {i}. {s}")
    print()

def cmd_methods(args):
    for m in all_methods():
        print(f"{m.name:12} | offline={'yes' if m.offline else 'no ':3} | ios<= {m.ios_max:<5} | {m.description}")
        print(f"             chips: {', '.join(m.chips)}")

def cmd_doctor(args):
    import shutil, subprocess
    checks = [
        ("python", sys.version.split()[0]),
        ("engine (tr4mpass)", shutil.which("tr4mpass") or "غير موجود"),
        ("usbipd", shutil.which("usbipd.exe") or shutil.which("usbipd") or "غير موجود"),
        ("ideviceinfo", shutil.which("ideviceinfo") or "غير موجود"),
        ("curl", shutil.which("curl") or "غير موجود"),
    ]
    for k, v in checks:
        print(f"{k:22} {v}")

def main(argv=None):
    p = argparse.ArgumentParser(prog="jmz", description="إطار فتح قفل التنشيط — كل الإصدارات")
    sub = p.add_subparsers(dest="cmd")

    m = sub.add_parser("matrix", help="مصفوفة الدعم")
    m.add_argument("--chips", nargs="*")
    m.add_argument("--ios", nargs="*")
    m.set_defaults(func=cmd_matrix)

    pl = sub.add_parser("plan", help="خطة جهاز")
    pl.add_argument("--chip", required=True)
    pl.add_argument("--ios", required=True)
    pl.add_argument("--model", default="")
    pl.set_defaults(func=cmd_plan)

    ms = sub.add_parser("methods", help="الطرق المسجلة")
    ms.set_defaults(func=cmd_methods)

    d = sub.add_parser("doctor", help="فحص البيئة")
    d.set_defaults(func=cmd_doctor)

    a = p.parse_args(argv)
    if not getattr(a, "func", None):
        p.print_help()
        return 1
    a.func(a)
    return 0

if __name__ == "__main__":
    sys.exit(main())
