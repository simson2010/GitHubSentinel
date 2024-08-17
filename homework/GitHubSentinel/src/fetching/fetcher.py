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
