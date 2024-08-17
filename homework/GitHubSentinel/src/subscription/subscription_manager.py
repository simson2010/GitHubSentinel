# src/subscription/subscription_manager.py

class SubscriptionManager:
    def __init__(self):
        self.subscriptions = []

    def add_subscription(self, repo_name):
        if repo_name not in self.subscriptions:
            self.subscriptions.append(repo_name)

    def remove_subscription(self, repo_name):
        if repo_name in self.subscriptions:
            self.subscriptions.remove(repo_name)

    def get_subscriptions(self):
        return self.subscriptions
