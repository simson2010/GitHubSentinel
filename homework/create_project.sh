#!/bin/bash

# 创建主目录
mkdir -p GitHubSentinel/src

# 创建模块目录及文件
mkdir -p GitHubSentinel/src/subscription
mkdir -p GitHubSentinel/src/fetching
mkdir -p GitHubSentinel/src/notification
mkdir -p GitHubSentinel/src/report
mkdir -p GitHubSentinel/src/ui

# 创建测试目录及文件
mkdir -p GitHubSentinel/tests

# 创建主程序入口文件和配置文件
touch GitHubSentinel/src/__init__.py
touch GitHubSentinel/src/main.py
touch GitHubSentinel/src/config.py

# 创建各模块的 __init__.py 文件
touch GitHubSentinel/src/subscription/__init__.py
touch GitHubSentinel/src/fetching/__init__.py
touch GitHubSentinel/src/notification/__init__.py
touch GitHubSentinel/src/report/__init__.py
touch GitHubSentinel/src/ui/__init__.py

# 创建各模块的主要文件
touch GitHubSentinel/src/subscription/subscription_manager.py
touch GitHubSentinel/src/fetching/fetcher.py
touch GitHubSentinel/src/notification/notifier.py
touch GitHubSentinel/src/report/report_generator.py
touch GitHubSentinel/src/ui/cli.py
touch GitHubSentinel/src/ui/web.py

# 创建测试文件
touch GitHubSentinel/tests/test_subscription.py
touch GitHubSentinel/tests/test_fetching.py
touch GitHubSentinel/tests/test_notification.py
touch GitHubSentinel/tests/test_report.py
touch GitHubSentinel/tests/test_ui.py

# 创建根目录下的文件
touch GitHubSentinel/requirements.txt
touch GitHubSentinel/README.md
touch GitHubSentinel/.gitignore
touch GitHubSentinel/setup.py

# 填充 main.py
cat <<EOL > GitHubSentinel/src/main.py
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
EOL

# 填充 config.py
cat <<EOL > GitHubSentinel/src/config.py
# src/config.py

class Config:
    GITHUB_API_URL = "https://api.github.com"
    NOTIFICATION_EMAIL = "user@example.com"
    REPORT_SCHEDULE = "daily"  # 可选：'daily' 或 'weekly'
EOL

# 填充 subscription_manager.py
cat <<EOL > GitHubSentinel/src/subscription/subscription_manager.py
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
EOL

# 填充 fetcher.py
cat <<EOL > GitHubSentinel/src/fetching/fetcher.py
# src/fetching/fetcher.py

import requests
from config import Config

class Fetcher:
    def __init__(self):
        self.api_url = Config.GITHUB_API_URL

    def fetch_updates(self, subscriptions):
        updates = {}
        for repo in subscriptions:
            url = f"{self.api_url}/repos/{repo}/commits"
            response = requests.get(url)
            if response.status_code == 200:
                updates[repo] = response.json()
        return updates
EOL

# 填充 notifier.py
cat <<EOL > GitHubSentinel/src/notification/notifier.py
# src/notification/notifier.py

import smtplib
from email.mime.text import MIMEText
from config import Config

class Notifier:
    def __init__(self):
        self.email = Config.NOTIFICATION_EMAIL

    def send_notifications(self, report):
        msg = MIMEText(report)
        msg['Subject'] = "GitHub Sentinel Report"
        msg['From'] = "sentinel@example.com"
        msg['To'] = self.email

        with smtplib.SMTP('localhost') as server:
            server.send_message(msg)
EOL

# 填充 report_generator.py
cat <<EOL > GitHubSentinel/src/report/report_generator.py
# src/report/report_generator.py

class ReportGenerator:
    def generate_report(self, updates):
        report = "GitHub Sentinel Report\n\n"
        for repo, commits in updates.items():
            report += f"Repository: {repo}\n"
            for commit in commits:
                report += f"- {commit['commit']['message']}\n"
            report += "\n"
        return report
EOL

# 填充 cli.py
cat <<EOL > GitHubSentinel/src/ui/cli.py
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
EOL

# 填充 web.py
cat <<EOL > GitHubSentinel/src/ui/web.py
# src/ui/web.py

from flask import Flask, request, jsonify
from subscription.subscription_manager import SubscriptionManager

app = Flask(__name__)
manager = SubscriptionManager()

@app.route('/subscribe', methods=['POST'])
def subscribe():
    repo = request.json.get('repo')
    if repo:
        manager.add_subscription(repo)
        return jsonify({"message": f"Subscribed to {repo}"}), 200
    return jsonify({"error": "Repository name required"}), 400

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    repo = request.json.get('repo')
    if repo:
        manager.remove_subscription(repo)
        return jsonify({"message": f"Unsubscribed from {repo}"}), 200
    return jsonify({"error": "Repository name required"}), 400

@app.route('/subscriptions', methods=['GET'])
def subscriptions():
    return jsonify(manager.get_subscriptions()), 200

if __name__ == "__main__":
    app.run(debug=True)
EOL

# 填充 test_subscription.py
cat <<EOL > GitHubSentinel/tests/test_subscription.py
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
EOL

# 填充 test_fetching.py
cat <<EOL > GitHubSentinel/tests/test_fetching.py
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
EOL

# 填充 test_notification.py
cat <<EOL > GitHubSentinel/tests/test_notification.py
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
EOL

# 填充 test_report.py
cat <<EOL > GitHubSentinel/tests/test_report.py
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
EOL

# 填充 test_ui.py
cat <<EOL > GitHubSentinel/tests/test_ui.py
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
EOL

# 填充 requirements.txt
cat <<EOL > GitHubSentinel/requirements.txt
flask
requests
EOL

# 填充 README.md
cat <<EOL > GitHubSentinel/README.md
# GitHub Sentinel

GitHub Sentinel is an open-source AI Agent designed for developers and project managers. It automatically fetches and summarizes the latest updates from subscribed GitHub repositories on a daily or weekly basis. The main features include subscription management, update fetching, a notification system, and report generation.

## Installation

\`\`\`
pip install -r requirements.txt
\`\`\`

## Usage

### CLI

\`\`\`
python src/ui/cli.py add --repo username/repo
\`\`\`

### Web Interface

\`\`\`
python src/ui/web.py
\`\`\`

## Testing

Run the tests using:

\`\`\`
python -m unittest discover tests
\`\`\`
EOL

# 填充 .gitignore
cat <<EOL > GitHubSentinel/.gitignore
__pycache__/
*.pyc
.env
EOL

# 填充 setup.py
cat <<EOL > GitHubSentinel/setup.py
from setuptools import setup, find_packages

setup(
    name='GitHubSentinel',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'flask',
        'requests'
    ],
    entry_points={
    },
)
EOL

echo "项目结构已经生成完毕"
