import sys
import re
import datetime
from flask import Flask, jsonify, abort, request
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.DateTime(dt_format='iso8601')
}

parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)

parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)


class EventResource(Resource):
    def post(self):
        args = parser.parse_args()
        if not args.get('date', False) or not re.match(r'\d\d\d\d-\d\d-\d\d', str(args['date'])):
            return None
        if not args.get('event', False):
            return None
        db.session.add(Event(event=args['event'], date=args['date']))
        db.session.commit()
        args['message'] = 'The event has been added!'
        args['date'] = str(args['date'])[:10]
        return jsonify(args)

    @marshal_with(resource_fields)
    def get(self):
        start = request.args.get('start_time')
        end = request.args.get('end_time')
        if start and end:
            return Event.query.filter(Event.date.between(start, end)).all()
        return Event.query.all()


class EventTodayResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return Event.query.filter(Event.date == datetime.date.today()).all()


class EventByIdResource(Resource):
    @marshal_with(resource_fields)
    def get(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()
        if event:
            return event
        return abort(404, "The event doesn't exist!")

    def delete(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()
        if event:
            db.session.delete(event)
            db.session.commit()
            return jsonify({"message": "The event has been deleted!"})
        return abort(404, "The event doesn't exist!")


api.add_resource(EventResource, '/event')
api.add_resource(EventTodayResource, '/event/today')
api.add_resource(EventByIdResource, '/event/<int:event_id>')


if __name__ == '__main__':
    db.create_all()
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
