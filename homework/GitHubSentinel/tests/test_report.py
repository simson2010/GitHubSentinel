# tests/test_report.py

import unittest
from src.report.report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def test_generate_report(self):
        generator = ReportGenerator()
        updates = {
            "test/repo": [{"commit": {"message": "Test commit"}}]
        }
        report = generator.generate_report(updates)
        self.assertIn("Test commit", report)

if __name__ == '__main__':
    unittest.main()
