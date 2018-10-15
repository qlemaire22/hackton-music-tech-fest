from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import os
from flask import jsonify
from space import Space
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import sys
from flask import send_file


print("Starting the app...")
sys.stdout.flush()

app = Flask(__name__)
api = Api(app)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://heqjmprseveiui:2da7e3c217dd0b0f3678002aedf69da10dca78ab4f61523f47a460c984b5a4b8@ec2-50-17-250-38.compute-1.amazonaws.com:5432/d9h6mslcovrogp'

db = SQLAlchemy(app)

from models import HubD, User


post_sequence_parser = reqparse.RequestParser()
post_sequence_parser.add_argument('location')
post_sequence_parser.add_argument('sequence_layer')

get_sequence_parser = reqparse.RequestParser()
get_sequence_parser.add_argument('location')

last_user_id = 0


class SequenceAPI(Resource):
    def get(self):
        args = get_sequence_parser.parse_args()
        location = args['location']

        hubs_data = HubD.query.all()

        space = Space()
        space.init(hubs_data)

        hub = space.getClosestHub(location)
        object = hub.getHubObject()

        # print(object)
        sys.stdout.flush()

        object2 = {"location": hub.getLocation(), "sequence": json.loads(json.dumps(object))}

        response = app.response_class(
            response=json.dumps(object2),
            status=200,
            mimetype='application/json'
        )

        print("GET output: ", object2)
        sys.stdout.flush()

        return response

    def post(self):
        global space

        args = post_sequence_parser.parse_args()
        location = args['location']
        # print(location)

        hubs_data = HubD.query.all()

        space = Space()
        space.init(hubs_data)

        sequence_layer = json.loads(args['sequence_layer'].replace("'", '"'))

        hub = space.getClosestHub(location)
        hub.updateLayer(sequence_layer["user_id"], sequence_layer["sound_id"], sequence_layer["rhythm"])
        location = hub.getLocation()

        admin = HubD.query.filter_by(location=location).first()
        admin.sequence = json.dumps(json.loads(json.dumps(hub.getHubObject())))
        db.session.commit()

        object2 = {"location": hub.getLocation()}

        response = app.response_class(
            response=json.dumps(object2),
            status=200,
            mimetype='application/json'
        )

        print("POST output: ", object2)
        sys.stdout.flush()

        # save_json(str(hub.getLocation()) + ".hub", sequence_layer)
        return response


class UserAPI(Resource):
    def get(self):
        global last_user_id
        admin = User.query.filter_by(id=1).first()
        last_user_id = admin.last_id
        last_user_id += 1
        admin = User.query.filter_by(id=1).first()
        admin.last_id = last_user_id
        db.session.commit()

        print("GET user_id: ", last_user_id)
        sys.stdout.flush()

        return jsonify(user_id=last_user_id)


class YaserAPI(Resource):
    def get(self):
        return send_file("yaser.jpg", mimetype='image/jpg')


# def save_json(name, data):
#     with open(name, 'w') as f:
#         json.dump(data, f, ensure_ascii=False)


# def load_hub_files():
#     hubs_data = HubD.query.all()
#     print("hubs files " + hubs_data[0])
#     sys.stdout.flush()
#     return hubs_data
#
#
# def load_user_last_id():
#     global last_user_id
#     print("load last_user_id")
#     sys.stdout.flush()
#
#     user = User.query.filter_by(id=1).first()
#     last_user_id = user.last_id
#
#     print("last_user_id " + str(last_user_id))
#     sys.stdout.flush()
#
#
# def save_user_last_id():
#     global last_user_id
#     admin = User.query.filter_by(id=1).first()
#     admin.last_id = last_user_id
#     db.session.commit()


api.add_resource(UserAPI, '/user_id')
api.add_resource(SequenceAPI, '/sequence')
api.add_resource(YaserAPI, '/god')


if __name__ == '__main__':
    # app.run(host="130.229.135.119", port=5002)
    app.run(port=os.Getenv("PORT"))
    #
    # print("START MAIN")
    # sys.stdout.flush()
    # load_user_last_id()
    # space.init(load_hub_files())
