from flask import Flask, render_template, request
import json
from .config import USER_ID
from .metrics import get_metrics
from .services import get_friends, lookup_ids

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/friends', methods=['GET'])
def get_friends_api():
    """Returns information about a user's friends"""

    user_id = request.args.get("user_id")
    friend_ids = get_friends(user_id)
    id_to_summary = lookup_ids(friend_ids)
    return [id_to_summary[id] for id in friend_ids]

@app.route('/health', methods=['GET'])
def health():
    """Returns metrics"""
    metrics = get_metrics()
    return json.dumps(metrics)
    
    

if __name__ == "__main__":
    app.run(debug=True)