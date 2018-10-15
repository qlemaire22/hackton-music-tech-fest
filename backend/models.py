from manage import db, app
import json


class HubD(db.Model):
    __tablename__ = 'hub'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(120), index=True, unique=True)
    sequence = db.Column(db.String(1000), index=True, unique=True)

    def __repr__(self):
        object = {'location': self.location, 'sequence': self.sequence}
        return json.dumps(object)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    last_id = db.Column(db.Integer, index=True, unique=True)
