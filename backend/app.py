from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "full_name": self.full_name, "event_name": self.event_name}

@app.route('/participants', methods=['POST'])
def add_participant():
    data = request.json
    participant = Participant(full_name=data["full_name"], event_name=data["event_name"])
    db.session.add(participant)
    db.session.commit()
    return jsonify({"message": "Participant added successfully!"}), 201

@app.route('/participants', methods=['GET'])
def get_participants():
    participants = Participant.query.all()
    return jsonify([p.to_dict() for p in participants]), 200

@app.route('/events/<event_name>', methods=['GET'])
def get_event_participants(event_name):
    participants = Participant.query.filter_by(event_name=event_name).all()
    return jsonify([p.to_dict() for p in participants]), 200

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
