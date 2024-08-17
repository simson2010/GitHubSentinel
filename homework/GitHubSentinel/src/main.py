# src/main.py

from subscription.subscription_manager import SubscriptionManager
from fetching.fetcher import Fetcher
from notification.notifier import Notifier
from report.report_generator import ReportGenerator

def main():
    subscription_manager = SubscriptionManager()
    fetcher = Fetcher()
    notifier = Notifier()
    report_generator = ReportGenerator()

    subscriptions = subscription_manager.get_subscriptions()
    updates = fetcher.fetch_updates(subscriptions)
    report = report_generator.generate_report(updates)
    notifier.send_notifications(report)

if __name__ == "__main__":
    main()
