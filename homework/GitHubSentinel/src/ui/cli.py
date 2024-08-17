# src/ui/cli.py

import argparse
from subscription.subscription_manager import SubscriptionManager

def main():
    parser = argparse.ArgumentParser(description='GitHub Sentinel CLI')
    parser.add_argument('action', choices=['add', 'remove', 'list'], help='Action to perform')
    parser.add_argument('--repo', help='Repository name')

    args = parser.parse_args()
    manager = SubscriptionManager()

    if args.action == 'add' and args.repo:
        manager.add_subscription(args.repo)
        print(f"Added subscription to {args.repo}")
    elif args.action == 'remove' and args.repo:
        manager.remove_subscription(args.repo)
        print(f"Removed subscription from {args.repo}")
    elif args.action == 'list':
        subscriptions = manager.get_subscriptions()
        print("Current subscriptions:")
        for repo in subscriptions:
            print(f"- {repo}")

if __name__ == "__main__":
    main()
