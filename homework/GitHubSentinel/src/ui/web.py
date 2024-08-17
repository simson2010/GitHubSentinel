# src/ui/web.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, request, jsonify, render_template_string
from subscription.subscription_manager import SubscriptionManager

app = Flask(__name__)
manager = SubscriptionManager()

# 首页路由
@app.route('/')
def home():
    return render_template_string('''
        <h1>Welcome to GitHub Sentinel</h1>
        <p>This is an AI Agent designed to help developers and project managers track GitHub repositories.</p>
        <ul>
            <li><a href="/subscriptions">View Subscriptions</a></li>
            <li><a href="/subscribe">Subscribe to a Repository</a></li>
            <li><a href="/unsubscribe">Unsubscribe from a Repository</a></li>
        </ul>
    ''')

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

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "This route is not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
