from __future__ import annotations

from flask import Flask, render_template, request

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import json

from .metrics import get_metrics
from .services import get_friends, lookup_ids_bulk

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per day", "50 per hour", "10 per minute"],
    storage_uri="memory://",
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/friends', methods=['GET'])
@limiter.limit("10 per minute")
def get_friends_api():
    """Returns information about a user's friends"""

    user_id = request.args.get("user_id")
    friend_ids = get_friends(user_id)
    id_to_summary = lookup_ids_bulk(friend_ids)
    summaries = [id_to_summary[id] for id in friend_ids]
    return json.dumps(summaries)

@app.route('/health', methods=['GET'])
def health():
    """Returns metrics"""
    
    metrics = get_metrics()
    return json.dumps(metrics)
    
    

if __name__ == "__main__":
    app.run(debug=True)