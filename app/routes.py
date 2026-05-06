from flask import Flask, render_template, request
import json
from .config import USER_ID
from .services import get_friends

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/friends', methods=['GET'])
def get_friends_api():
    user_id = request.args.get("user_id")
    friends_dict = get_friends(user_id)
    friends_json = json.dumps(friends_dict)
    return friends_json

if __name__ == "__main__":
    app.run(debug=True)