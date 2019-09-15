from flask import Flask, request
from flask_restplus import Api, Resource, fields
from mongoengine import connect
from datetime import datetime

import model

app = Flask(__name__)
api = Api(app, doc='/api/doc/')

connect('data', host='db', port=27017)

page = api.model('Page', {
    'user_id': fields.String,
    'name': fields.String,
    'timestamp': fields.String
})


@api.route('/v1/page')
class Page(Resource):
    @api.expect(page)
    def post(self):
        json = request.json
        user_id = json['user_id']
        name = json['name']
        timestamp = json['timestamp']
        try:
            user = model.User.objects.get(user_id=user_id)
        except:
            user = model.User(user_id=user_id, records=[])
        try:
            day_and_time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return {'result': False}
        if day_and_time > datetime.now():
            return {'result': False}
        user.insert_record(name, day_and_time)
        try:
            user.save()
        except:
            return {'result': False}
        return {'result': True}


@api.route('/v1/user/<uid>')
class User(Resource):
    def get(self, uid):
        try:
            user = model.User.objects.get(user_id=uid)
        except:
            return {'result': False}
        return user.get_result()

    def delete(self, uid):
        try:
            user = model.User.objects.get(user_id=uid)
        except:
            return {'result': False}
        user.delete()
        return {'result': True}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
