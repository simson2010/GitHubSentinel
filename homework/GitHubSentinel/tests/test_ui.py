# tests/test_ui.py

import unittest
from unittest.mock import patch
from src.ui.cli import main

class TestCLI(unittest.TestCase):
    @patch('src.ui.cli.SubscriptionManager.add_subscription')
    @patch('src.ui.cli.argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(action='add', repo='test/repo'))
    def test_cli_add(self, mock_args, mock_add):
        main()
        mock_add.assert_called_once_with('test/repo')

if __name__ == '__main__':
    unittest.main()
