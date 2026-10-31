"""Unit tests for the detection layer (no device, no network)."""
import importlib.util, os, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "app", "justmgz-engine.py")
spec = importlib.util.spec_from_file_location("bridge", SPEC)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class TestSerial(unittest.TestCase):
    DFU = "CPID:8015 ECID:1a2b3c4d5e SRTG:[iBoot-4076.0.38]"

    def test_cpid(self):
        self.assertEqual(bridge.parse_serial(self.DFU)["cpid"], "0x8015")

    def test_ecid(self):
        self.assertEqual(bridge.parse_serial(self.DFU)["ecid"], "0x1a2b3c4d5e")

    def test_srtg(self):
        self.assertEqual(bridge.parse_serial(self.DFU)["srtg"], "iBoot-4076.0.38")

    def test_empty(self):
        self.assertEqual(bridge.parse_serial(""), {})


class TestChips(unittest.TestCase):
    def test_a7(self):
        self.assertEqual(bridge.chip_name("0x8960"), "A7")

    def test_a11(self):
        self.assertEqual(bridge.chip_name("8015"), "A11")

    def test_a12(self):
        self.assertEqual(bridge.chip_name("0x8020"), "A12")

    def test_unknown(self):
        self.assertEqual(bridge.chip_name("0xffff"), "")

    def test_path_a_set(self):
        self.assertTrue({"A7", "A8", "A9", "A10", "A11"} <= bridge.A_CHIPS)

    def test_path_b_not_in_a(self):
        self.assertNotIn("A12", bridge.A_CHIPS)


class TestMaps(unittest.TestCase):
    def test_pid_modes(self):
        self.assertEqual(bridge.PID_MODE["1227"], "DFU")
        self.assertEqual(bridge.PID_MODE["1281"], "Recovery")
        self.assertEqual(bridge.PID_MODE["12a8"], "عادي")

    def test_names(self):
        self.assertEqual(bridge.NAMES.get("iPhone14,5"), "iPhone 13")
        self.assertGreater(len(bridge.NAMES), 70)


class TestNoDevice(unittest.TestCase):
    def test_detect_all_returns_trace(self):
        dev, trace = bridge.detect_all()
        self.assertIn("present", dev)
        self.assertEqual(len(trace), 5)
        self.assertEqual({t["backend"] for t in trace},
                         {"pyusb", "pnp", "usbipd", "pmd3", "idevice"})

    def test_probe_without_device_is_honest(self):
        d = bridge.probe_device(force=True)
        self.assertFalse(d["connected"])
        self.assertFalse(d.get("simulated"))


class TestSimulator(unittest.TestCase):
    def test_sim_device(self):
        os.environ["TR4MPASS_SIM"] = "dfu_a12"
        bridge.DEV_CACHE["v"] = None
        d = bridge.probe_device(force=True)
        self.assertTrue(d["connected"])
        self.assertTrue(d["simulated"])
        self.assertEqual(d["chip"], "A12")
        os.environ["TR4MPASS_SIM"] = "0"
        bridge.DEV_CACHE["v"] = None


if __name__ == "__main__":
    unittest.main(verbosity=2)
