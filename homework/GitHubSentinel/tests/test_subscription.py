# tests/test_subscription.py

import unittest
from src.subscription.subscription_manager import SubscriptionManager

class TestSubscriptionManager(unittest.TestCase):
    def test_add_subscription(self):
        manager = SubscriptionManager()
        manager.add_subscription("test/repo")
        self.assertIn("test/repo", manager.get_subscriptions())

    def test_remove_subscription(self):
        manager = SubscriptionManager()
        manager.add_subscription("test/repo")
        manager.remove_subscription("test/repo")
        self.assertNotIn("test/repo", manager.get_subscriptions())

    def test_get_subscriptions(self):
        manager = SubscriptionManager()
        self.assertEqual(manager.get_subscriptions(), [])

if __name__ == '__main__':
    unittest.main()
