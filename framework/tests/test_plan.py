import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jmz.support import capability
from jmz.plan import build_plan
from jmz.chips import chip_name, bootrom, max_ios


class TestCapability(unittest.TestCase):
    def test_a11_supported_offline(self):
        c = capability("A11", "16")
        self.assertEqual(c["verdict"], "supported")
        self.assertTrue(c["offline"])
        self.assertEqual(c["method"], "checkm8")

    def test_a7_no_cellular(self):
        c = capability("A7", "12")
        self.assertTrue(any("واي فاي" in n for n in c["notes"]))

    def test_a9_cellular(self):
        c = capability("A9", "15")
        self.assertFalse(any("واي فاي" in n for n in c["notes"]))

    def test_a13_usbliter8(self):
        c = capability("A13", "26.1")
        self.assertEqual(c["method"], "usbliter8")
        self.assertTrue(c["offline"])

    def test_a13_high_ios_needs_patch(self):
        c = capability("A13", "26.2")
        self.assertTrue(any("mobileactivationd" in n for n in c["notes"]))

    def test_a15_conditional(self):
        c = capability("A15", "26.1")
        self.assertEqual(c["verdict"], "conditional")
        self.assertFalse(c["offline"])

    def test_a15_above_261_unsupported(self):
        c = capability("A15", "26.2")
        self.assertEqual(c["verdict"], "unsupported")

    def test_a18_unsupported(self):
        self.assertEqual(capability("A18", "26.0")["verdict"], "unsupported")

    def test_impossible_version(self):
        self.assertEqual(capability("A7", "26.1")["verdict"], "impossible")


class TestChips(unittest.TestCase):
    def test_cpid(self):
        self.assertEqual(chip_name("0x8015"), "A11")
        self.assertEqual(chip_name("8020"), "A12")

    def test_bootrom(self):
        self.assertEqual(bootrom("A11"), "checkm8")
        self.assertEqual(bootrom("A13"), "usbliter8")
        self.assertIsNone(bootrom("A15"))

    def test_max_ios(self):
        self.assertEqual(max_ios("A7"), 12.5)


class TestPlan(unittest.TestCase):
    def test_plan_steps(self):
        p = build_plan("A12", "26.1", "iPhone XR")
        self.assertTrue(p["ready"])
        self.assertGreaterEqual(len(p["steps"]), 5)

    def test_plan_session_steps(self):
        p = build_plan("A15", "26.1", "iPhone 13")
        self.assertEqual(p["method"], "session")
        self.assertTrue(any("activate-only" in s for s in p["steps"]))

    def test_plan_unsupported(self):
        self.assertFalse(build_plan("A15", "26.2")["ready"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
