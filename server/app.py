from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.all()
        messages_dict = [message.to_dict() for message in messages]
        return make_response(jsonify(messages_dict), 200)
    elif request.method == "POST":
        message = Message()
        content = request.get_json()
        for key in content:
            if hasattr(message, key):
                setattr(message, key, content[key])
        db.session.add(message)
        db.session.commit()
        return make_response(jsonify(message.to_dict()), 201)


@app.route("/messages/<int:id>", methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.get(id)
    if request.method == "PATCH":
        content = request.get_json()
        for key in content:
            if hasattr(message, key):
                setattr(message, key, content[key])
        db.session.commit()
        return make_response(jsonify(message.to_dict()), 200)
    if request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        return make_response({"message": "successful delete"}, 200)


if __name__ == "__main__":
    app.run(port=5555)
