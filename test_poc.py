import unittest
from poc import Principal, VulnerableReportService, PatchedReportService

class TestReportIsolation(unittest.TestCase):
    def setUp(self):
        self.alice = Principal("alice", "alpha")
        self.bob = Principal("bob", "beta")

    def test_vulnerable_cache_leaks_after_owner_warms_cache(self):
        svc = VulnerableReportService()
        self.assertEqual(svc.get_report(self.alice, "report-7"), "ALPHA-INTERNAL-REPORT")
        self.assertEqual(svc.get_report(self.bob, "report-7"), "ALPHA-INTERNAL-REPORT")

    def test_vulnerable_cold_cache_blocks_non_owner(self):
        svc = VulnerableReportService()
        with self.assertRaises(PermissionError):
            svc.get_report(self.bob, "report-7")

    def test_patch_blocks_even_after_cache_warmup(self):
        svc = PatchedReportService()
        self.assertEqual(svc.get_report(self.alice, "report-7"), "ALPHA-INTERNAL-REPORT")
        with self.assertRaises(PermissionError):
            svc.get_report(self.bob, "report-7")

    def test_patch_preserves_owner_functionality(self):
        svc = PatchedReportService()
        self.assertEqual(svc.get_report(self.alice, "report-7"), svc.get_report(self.alice, "report-7"))

if __name__ == "__main__":
    unittest.main()
