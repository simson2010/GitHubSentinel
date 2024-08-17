# tests/test_fetching.py

import unittest
from unittest.mock import patch
from src.fetching.fetcher import Fetcher

class TestFetcher(unittest.TestCase):
    @patch('src.fetching.fetcher.requests.get')
    def test_fetch_updates(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"commit": {"message": "Test commit"}}]

        fetcher = Fetcher()
        updates = fetcher.fetch_updates(["test/repo"])

        self.assertIn("test/repo", updates)
        self.assertEqual(updates["test/repo"][0]["commit"]["message"], "Test commit")

if __name__ == '__main__':
    unittest.main()
