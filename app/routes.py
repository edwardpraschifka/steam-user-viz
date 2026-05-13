from __future__ import annotations

from flask import Flask, render_template, request

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import json

from .graph import Graph, graphs
from .metrics import get_metrics
from .services import get_friends, lookup_ids, lookup_ids_bulk

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per hour", "10 per minute"],
    storage_uri="memory://",
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/graph', methods=['POST'])
@limiter.limit("10 per minute")
def update_graph():
    """Returns information about a user's friends"""

    result = {}
    data = request.get_json()
    id = data.get("id")
    session_id = data.get("session_id")

    if not session_id:
        return json.dumps({"success": "False", "data": {}}), 400

    if session_id not in graphs:
        graphs[session_id] = Graph()
    graph = graphs[session_id]

    # to initialize the graph,
    # fetch the profile summary
    # of the queried user
    skip_self = False if data.get("skip_self", 0) == 0 else True


    profile = get_friends(id) # = {is_private: True/False, friends: [id_1, id_2, ...]}
    if profile["is_private"]:
        result["private"] = "True"
        result["data"] = {}

    else:
        result["private"] = "False"
        summaries = []

        if not skip_self:
            self_summary = lookup_ids_bulk([id])
            summaries.append(self_summary[id])
            print(f"zy={summaries}")

        friend_ids = [friend["steamid"] for friend in profile["friends"]]
        id_to_summary = lookup_ids_bulk(friend_ids)
        summaries.extend([id_to_summary[fid] for fid in friend_ids])        

        for friend in summaries:
            graph.add_node(
                friend["steamid"], 
                friend["personaname"], 
                friend["profileurl"], 
                friend["avatar"],
            )
            
            graph.add_link(id, friend["steamid"])
        
        result["data"] = graph.serialize()
    
    return json.dumps(result)

@app.route('/health', methods=['GET'])
def health():
    """Returns metrics"""
    
    metrics = get_metrics()
    return json.dumps(metrics)
    
    

if __name__ == "__main__":
    app.run(debug=True)