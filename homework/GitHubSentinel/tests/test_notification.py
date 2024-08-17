# tests/test_notification.py

import unittest
from unittest.mock import patch
from src.notification.notifier import Notifier

class TestNotifier(unittest.TestCase):
    @patch('src.notification.notifier.smtplib.SMTP')
    def test_send_notifications(self, mock_smtp):
        notifier = Notifier()
        notifier.send_notifications("Test Report")
        mock_smtp.assert_called_once()

if __name__ == '__main__':
    unittest.main()
